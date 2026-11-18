/*
 * Native F1-only CryptoLib -> independent TTCSIL admission-policy bridge.
 * Synthetic fixed laboratory TC and configuration; no NOS3/cFS/T1 transaction,
 * flight validation, measured epoch, authenticated return TM, or crypto proof.
 * Do not process mission keys or expose on public networks.
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "crypto.h"
#include "crypto_error.h"
#include "sa_interface.h"
#include "ttcsil_ingress_guard.h"

#define TEST_SPI 4u
#define TEST_EPOCH 17u
#define TEST_MAX_TC 1024u

static int same_verdict(ttcsil_verdict actual, ttcsil_verdict expected,
                        const char *case_id, size_t payload)
{
    if (actual != expected || (expected != TTCSIL_ALLOW && payload != 0u))
    {
        fprintf(stderr, "TTCSIL_NATIVE_GUARD_FAIL case=%s got=%d expected=%d payload=%zu\n",
                case_id, (int)actual, (int)expected, payload);
        return 1;
    }
    printf("TTCSIL_NATIVE_GUARD_%s=PASS\n", case_id);
    return 0;
}

static int init_crypto(void)
{
    int32_t rc = Crypto_Init_TC_Unit_Test();
    if (rc != CRYPTO_LIB_SUCCESS) {
        fprintf(stderr, "Native CryptoLib init failed: %ld\n", (long)rc);
        return 1;
    }
    SaInterface api = get_sa_interface_inmemory();
    SecurityAssociation_t *clear = NULL, *auth = NULL;
    if (api->sa_get_from_spi(1u, &clear) != CRYPTO_LIB_SUCCESS || clear == NULL ||
        api->sa_get_from_spi(TEST_SPI, &auth) != CRYPTO_LIB_SUCCESS || auth == NULL)
        return 1;
    clear->sa_state = SA_NONE; /* block nominal clear-mode fixture */
    auth->gvcid_blk.vcid = 0;
    auth->sa_state = SA_OPERATIONAL;
    auth->arsn_len = 0;
    auth->ekid = 130u; /* upstream synthetic test key index only */
    return 0;
}

static int read_frame(const char *path, uint8_t *buffer, size_t capacity,
                      size_t *length)
{
    FILE *f = fopen(path, "rb");
    if (f == NULL) { perror("open test frame"); return 1; }
    size_t n = fread(buffer, 1, capacity, f);
    int failed = ferror(f) || !feof(f) || fclose(f) != 0 || n < 16 || n >= capacity;
    if (failed) {
        fprintf(stderr, "Invalid synthetic protected-frame input\n");
        return 1;
    }
    *length = n;
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s PROTECTED_TEST_TC_PATH\n", argv[0]);
        return 64;
    }
    if (init_crypto()) return 1;

    uint8_t frame[4096] = {0};
    size_t frame_size = 0u;
    if (read_frame(argv[1], frame, sizeof(frame), &frame_size)) return 1;

    TC_t *decoded = (TC_t *)calloc(1, sizeof(TC_t));
    if (decoded == NULL) return 1;
    int n_ingest = (int)frame_size;
    const int32_t status = Crypto_TC_ProcessSecurity(frame, &n_ingest, decoded);
    if (status != CRYPTO_LIB_SUCCESS) {
        fprintf(stderr, "CryptoLib authenticating processing rejected frame: %ld\n", (long)status);
        free(decoded);
        return 1;
    }

    /* Security profile is an independent, fixed TEST fixture. Never build
     * expected authorization from the incoming frame/its chosen SPI. */
    const ttcsil_policy policy = {
        .expected_channel = {0u, 3u, 0u, 0u},
        .expected_spi = TEST_SPI,
        .expected_epoch = TEST_EPOCH, /* NOT measured by native CryptoLib */
        .max_total_bytes = TEST_MAX_TC,
        .min_payload_bytes = 1u
    };
    /* The SPI-indexed SA is re-read from the native library. This is not a
     * separate upstream proof of channel authorization; our fixed policy is
     * what checks it. The decoded MAP ID comes from the segment header. */
    SecurityAssociation_t *selected = NULL;
    SaInterface api = get_sa_interface_inmemory();
    if (api->sa_get_from_spi(decoded->tc_sec_header.spi, &selected) != CRYPTO_LIB_SUCCESS ||
        selected == NULL) {
        free(decoded);
        return 1;
    }
    const ttcsil_evidence evidence = {
        .observed_channel = {
            (uint8_t)decoded->tc_header.tfvn,
            (uint16_t)decoded->tc_header.scid,
            (uint8_t)decoded->tc_header.vcid,
            (uint8_t)(decoded->tc_sec_header.sh & 0x3fu)
        },
        .frame_spi = decoded->tc_sec_header.spi,
        .selected_sa_channel = {
            (uint8_t)selected->gvcid_blk.tfvn,
            (uint16_t)selected->gvcid_blk.scid,
            (uint8_t)selected->gvcid_blk.vcid,
            (uint8_t)selected->gvcid_blk.mapid
        },
        .selected_sa_spi = selected->spi,
        .active_epoch = TEST_EPOCH, /* injected lab metadata: not F3 */
        .selected_sa_operational = (selected->sa_state == SA_OPERATIONAL),
        .selected_sa_authentication_required = (selected->ast == 1u),
        .cryptographic_verification_succeeded = (status == CRYPTO_LIB_SUCCESS)
    };
    free(decoded);

    int fails = 0;
    size_t payload = 999u;
    ttcsil_verdict rc = ttcsil_guard_tc(&policy, &evidence, frame_size, 5u,
                                        frame_size, &payload);
    printf("TTCSIL_NATIVE_GUARD_DEBUG=channel_%u_%u_%u_%u sa_%u_%u_%u_%u spi_%u epoch_LAB_ONLY\n",
           (unsigned)evidence.observed_channel.tfvn,
           (unsigned)evidence.observed_channel.scid,
           (unsigned)evidence.observed_channel.vcid,
           (unsigned)evidence.observed_channel.map_id,
           (unsigned)evidence.selected_sa_channel.tfvn,
           (unsigned)evidence.selected_sa_channel.scid,
           (unsigned)evidence.selected_sa_channel.vcid,
           (unsigned)evidence.selected_sa_channel.map_id,
           (unsigned)evidence.selected_sa_spi);
    fails += same_verdict(rc, TTCSIL_ALLOW, "REAL_CRYPTO_ACCEPT", payload);
    if (rc == TTCSIL_ALLOW && payload != frame_size - 5u) ++fails;

    ttcsil_policy wrong_channel = policy;
    wrong_channel.expected_channel.vcid = 1u;
    payload = 999u;
    rc = ttcsil_guard_tc(&wrong_channel, &evidence, frame_size, 5u, frame_size, &payload);
    fails += same_verdict(rc, TTCSIL_REJECT_CHANNEL, "WRONG_AUTHORIZED_VCID", payload);

    ttcsil_evidence wrong_selected_channel = evidence;
    wrong_selected_channel.selected_sa_channel.vcid = 2u;
    payload = 999u;
    rc = ttcsil_guard_tc(&policy, &wrong_selected_channel, frame_size, 5u, frame_size, &payload);
    fails += same_verdict(rc, TTCSIL_REJECT_CHANNEL, "WRONG_SELECTED_SA_CHANNEL", payload);

    ttcsil_evidence no_auth = evidence;
    no_auth.selected_sa_authentication_required = false;
    payload = 999u;
    rc = ttcsil_guard_tc(&policy, &no_auth, frame_size, 5u, frame_size, &payload);
    fails += same_verdict(rc, TTCSIL_REJECT_SA, "CLEAR_MODE_DOWNGRADE", payload);

    ttcsil_evidence no_crypto = evidence;
    no_crypto.cryptographic_verification_succeeded = false;
    payload = 999u;
    rc = ttcsil_guard_tc(&policy, &no_crypto, frame_size, 5u, frame_size, &payload);
    fails += same_verdict(rc, TTCSIL_REJECT_CRYPTO, "MISSING_AUTH", payload);

    ttcsil_evidence stale_epoch = evidence;
    stale_epoch.active_epoch = TEST_EPOCH - 1u;
    payload = 999u;
    rc = ttcsil_guard_tc(&policy, &stale_epoch, frame_size, 5u, frame_size, &payload);
    fails += same_verdict(rc, TTCSIL_REJECT_EPOCH, "STALE_SYNTHETIC_EPOCH", payload);

    payload = 999u;
    rc = ttcsil_guard_tc(&policy, &evidence, 4u, 5u, frame_size, &payload);
    fails += same_verdict(rc, TTCSIL_REJECT_LENGTH, "SHORT_DECLARED_LENGTH", payload);

    if (Crypto_Shutdown() != CRYPTO_LIB_SUCCESS) ++fails;
    printf("TTCSIL_NATIVE_GUARD_AUTH_STATUS=CRYPTO_LIB_SUCCESS\n");
    printf("TTCSIL_NATIVE_GUARD_EPOCH_PROVENANCE=LAB_FIXTURE_ONLY\n");
    printf("TTCSIL_NATIVE_GUARD_NOS3_CFS_INTEGRATION=NOT_EXECUTED\n");
    printf("TTCSIL_NATIVE_GUARD_VERDICT=%s checks=7\n", fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
}
