#ifndef TTCSIL_INGRESS_GUARD_H
#define TTCSIL_INGRESS_GUARD_H

/* Standalone pre-dispatch security policy, not a CryptoLib or cFE patch.
 * Inputs marked 'trusted' MUST come from independently controlled config
 * or verified library state, never solely from incoming frame bytes.
 * This header intentionally depends on C11 standard headers only.
 */
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum {
    TTCSIL_REJECT_INPUT = -1,
    TTCSIL_REJECT_LENGTH = -2,
    TTCSIL_REJECT_CRYPTO = -3,
    TTCSIL_REJECT_SA = -4,
    TTCSIL_REJECT_CHANNEL = -5,
    TTCSIL_REJECT_EPOCH = -6,
    TTCSIL_ALLOW = 0
} ttcsil_verdict;

typedef struct {
    uint8_t tfvn;
    uint16_t scid;
    uint8_t vcid;
    uint8_t map_id;
} ttcsil_channel;

typedef struct {
    ttcsil_channel expected_channel;
    uint16_t expected_spi;
    uint64_t expected_epoch;
    size_t max_total_bytes;
    size_t min_payload_bytes;
} ttcsil_policy;

typedef struct {
    /* Parsed frame identity: untrusted until independently authorized. */
    ttcsil_channel observed_channel;
    uint16_t frame_spi;
    /* Selected library SA identity and channel binding: TRUSTED only after
     * verified SA lookup / authorization from the integration adapter. */
    ttcsil_channel selected_sa_channel;
    uint16_t selected_sa_spi;
    uint64_t active_epoch;
    bool selected_sa_operational;
    bool selected_sa_authentication_required;
    /* Must be derived from CryptoLib's real authenticated processing path. */
    bool cryptographic_verification_succeeded;
} ttcsil_evidence;

/* No arithmetic underflow: the payload output is zeroed on every failure.
 * total: declared cFE message length; header: trusted header size;
 * available: actual allocated input buffer bound; max_total: policy cap.
 */
ttcsil_verdict ttcsil_guard_length(
    size_t total, size_t header, size_t available,
    size_t max_total, size_t min_payload, size_t *payload);

/* Admission is only a pre-dispatch gate, NOT proof of recovery, telemetry
 * confirmation, cryptographic soundness or CCSDS conformance. */
ttcsil_verdict ttcsil_guard_tc(
    const ttcsil_policy *policy, const ttcsil_evidence *evidence,
    size_t total, size_t header, size_t available,
    size_t *payload);

#endif
