/*
 * TTCSIL native feasibility probe. Synthetic test keys/frames only.
 * NOT an experiment, Recovery SA implementation, CCSDS-conformance test,
 * persistence guarantee or operational commandability claim.
 * Uses the actual pinned CryptoLib APIs; no vendor source is included.
 */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "crypto.h"
#include "crypto_error.h"
#include "sa_interface.h"

#define TTCSIL_SPI 4u
#define TTCSIL_SENTINEL_AKID 191u

static int boot(void)
{
    int32_t status = Crypto_Init_TC_Unit_Test();
    if (status != CRYPTO_LIB_SUCCESS)
    {
        fprintf(stderr, "Crypto_Init_TC_Unit_Test failed: %ld\n", (long)status);
        return 1;
    }
    return 0;
}

static int get_sa(SecurityAssociation_t **sa)
{
    SaInterface api = get_sa_interface_inmemory();
    int32_t status = api->sa_get_from_spi(TTCSIL_SPI, sa);
    if (status != CRYPTO_LIB_SUCCESS || *sa == NULL)
    {
        fprintf(stderr, "sa_get_from_spi failed: %ld\n", (long)status);
        return 1;
    }
    return 0;
}

static int sa_seed(void)
{
    if (boot()) return 1;
    SecurityAssociation_t *sa = NULL;
    if (get_sa(&sa)) return 1;
    sa->sa_state = SA_OPERATIONAL;
    sa->akid = TTCSIL_SENTINEL_AKID; /* metadata marker, NOT a usable cryptographic key */
    SaInterface api = get_sa_interface_inmemory();
    int32_t status = api->sa_save_sa(sa);
    struct stat st;
    if (status != CRYPTO_LIB_SUCCESS || stat("sa_save_file.bin", &st) != 0 || st.st_size <= 0)
    {
        fprintf(stderr, "SA persistence write failed: %ld\n", (long)status);
        return 1;
    }
    printf("TTCSIL_NATIVE_SA_WRITE_ACK=PASS pid=%ld spi=%u metadata_marker=%u\n",
           (long)getpid(), (unsigned)sa->spi, (unsigned)sa->akid);
    fflush(stdout);
    /* An actual OS process exit with no graceful Crypto_Shutdown(). */
    _exit(0);
}

static int sa_verify(void)
{
    if (boot()) return 1;
    SecurityAssociation_t *sa = NULL;
    if (get_sa(&sa)) return 1;
    if (sa->sa_state != SA_OPERATIONAL || sa->akid != TTCSIL_SENTINEL_AKID)
    {
        fprintf(stderr, "SA metadata not retained across independent process init\n");
        return 1;
    }
    printf("TTCSIL_NATIVE_SA_RELOAD=PASS pid=%ld spi=%u metadata_marker=%u\n",
           (long)getpid(), (unsigned)sa->spi, (unsigned)sa->akid);
    return Crypto_Shutdown() == CRYPTO_LIB_SUCCESS ? 0 : 1;
}

/* Fixture documented in upstream CryptoLib test/unit/ut_tc_apply.c. */
static const uint8_t tc_fixture[] = {
    0x20,0x03,0x00,0x15,0x00,0x00,0x80,0xd2,0xc7,0x00,0x08,
    0x19,0x7f,0x0b,0x00,0x31,0x00,0x00,0xb1,0xfe,0x31,0x28
};

static int configure_tc_sa(void)
{
    SaInterface api = get_sa_interface_inmemory();
    SecurityAssociation_t *clear = NULL, *auth = NULL;
    if (api->sa_get_from_spi(1u, &clear) != CRYPTO_LIB_SUCCESS || clear == NULL) return 1;
    clear->sa_state = SA_NONE;
    if (get_sa(&auth)) return 1;
    auth->gvcid_blk.vcid = 0;
    auth->sa_state = SA_OPERATIONAL;
    auth->arsn_len = 0;
    auth->ekid = 130u; /* upstream synthetic test key index, no mission secret */
    return 0;
}

static int tc_send(const char *path)
{
    if (boot() || configure_tc_sa()) return 1;
    uint8_t *protected_frame = NULL;
    uint16_t protected_len = 0;
    int32_t rc = Crypto_TC_ApplySecurity(tc_fixture, (uint16_t)sizeof(tc_fixture),
                                        &protected_frame, &protected_len);
    if (rc != CRYPTO_LIB_SUCCESS || protected_frame == NULL || protected_len == 0)
    {
        fprintf(stderr, "TC apply failed: %ld\n", (long)rc);
        free(protected_frame);
        return 1;
    }
    /*
     * The upstream receiver's strict IV window rejects the first (IV=0)
     * sender frame when its local initial state is also IV=0. Advance the
     * sender once and transmit the next protected frame (IV=1). Do not
     * disable or bypass the receiver's replay protection to get a pass.
     */
    free(protected_frame);
    protected_frame = NULL;
    protected_len = 0;
    rc = Crypto_TC_ApplySecurity(tc_fixture, (uint16_t)sizeof(tc_fixture),
                                 &protected_frame, &protected_len);
    if (rc != CRYPTO_LIB_SUCCESS || protected_frame == NULL || protected_len == 0)
    {
        fprintf(stderr, "TC fresh-IV apply failed: %ld\\n", (long)rc);
        free(protected_frame);
        return 1;
    }
    FILE *out = fopen(path, "wb");
    if (out == NULL) { perror("fopen output"); free(protected_frame); return 1; }
    size_t n = fwrite(protected_frame, 1, protected_len, out);
    int close_rc = fclose(out);
    free(protected_frame);
    if (n != protected_len || close_rc != 0) return 1;
    printf("TTCSIL_PROTECTED_TC_PRODUCED=PASS bytes=%u\n", (unsigned)protected_len);
    return Crypto_Shutdown() == CRYPTO_LIB_SUCCESS ? 0 : 1;
}

static int tc_receive(const char *path, int tamper)
{
    if (boot() || configure_tc_sa()) return 1;
    FILE *in = fopen(path, "rb");
    if (in == NULL) { perror("fopen protected input"); return 1; }
    uint8_t frame[4096];
    size_t n = fread(frame, 1, sizeof(frame), in);
    if (ferror(in) || !feof(in) || fclose(in) != 0 || n < 16 || n >= sizeof(frame))
    {
        fprintf(stderr, "Protected input length/read failed\n");
        return 1;
    }
    if (tamper) frame[n - 6] ^= 0x01u; /* negative integrity control; can also fail FECF */
    TC_t *decoded = (TC_t *)calloc(1, TC_SIZE);
    if (decoded == NULL) return 1;
    int frame_len = (int)n;
    int32_t rc = Crypto_TC_ProcessSecurity(frame, &frame_len, decoded);
    free(decoded);
    int good = tamper ? (rc != CRYPTO_LIB_SUCCESS) : (rc == CRYPTO_LIB_SUCCESS);
    printf("TTCSIL_TC_%s=%s api_status=%ld\n",
           tamper ? "TAMPER_REJECTED" : "RECEIVE_ACCEPTED",
           good ? "PASS" : "FAIL", (long)rc);
    int shut_rc = Crypto_Shutdown() == CRYPTO_LIB_SUCCESS ? 0 : 1;
    return good && shut_rc == 0 ? 0 : 1;
}

int main(int argc, char **argv)
{
    if (argc == 2 && strcmp(argv[1], "sa-seed") == 0) return sa_seed();
    if (argc == 2 && strcmp(argv[1], "sa-verify") == 0) return sa_verify();
    if (argc == 3 && strcmp(argv[1], "tc-send") == 0) return tc_send(argv[2]);
    if (argc == 3 && strcmp(argv[1], "tc-receive") == 0) return tc_receive(argv[2], 0);
    if (argc == 3 && strcmp(argv[1], "tc-tamper") == 0) return tc_receive(argv[2], 1);
    fprintf(stderr, "Usage: %s sa-seed|sa-verify|tc-send PATH|tc-receive PATH|tc-tamper PATH\n", argv[0]);
    return 64;
}
