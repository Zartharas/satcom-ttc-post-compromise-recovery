#include "ttcsil_ingress_guard.h"

static bool same_channel(ttcsil_channel a, ttcsil_channel b)
{
    return a.tfvn == b.tfvn && a.scid == b.scid &&
           a.vcid == b.vcid && a.map_id == b.map_id;
}

ttcsil_verdict ttcsil_guard_length(
    size_t total, size_t header, size_t available,
    size_t max_total, size_t min_payload, size_t *payload)
{
    if (payload == NULL) {
        return TTCSIL_REJECT_INPUT;
    }
    *payload = 0;
    if (header == 0 || max_total < header || min_payload > max_total ||
        total < header || total > available || total > max_total) {
        return TTCSIL_REJECT_LENGTH;
    }
    const size_t n = total - header; /* safe because total >= header */
    if (n < min_payload) {
        return TTCSIL_REJECT_LENGTH;
    }
    *payload = n;
    return TTCSIL_ALLOW;
}

ttcsil_verdict ttcsil_guard_tc(
    const ttcsil_policy *policy, const ttcsil_evidence *evidence,
    size_t total, size_t header, size_t available,
    size_t *payload)
{
    if (payload == NULL) {
        return TTCSIL_REJECT_INPUT;
    }
    *payload = 0;
    if (policy == NULL || evidence == NULL) {
        return TTCSIL_REJECT_INPUT;
    }
    size_t length = 0;
    ttcsil_verdict rc = ttcsil_guard_length(
        total, header, available, policy->max_total_bytes,
        policy->min_payload_bytes, &length);
    if (rc != TTCSIL_ALLOW) {
        return rc;
    }
    if (!evidence->cryptographic_verification_succeeded) {
        return TTCSIL_REJECT_CRYPTO;
    }
    if (!evidence->selected_sa_operational ||
        !evidence->selected_sa_authentication_required ||
        policy->expected_spi == 0 || evidence->selected_sa_spi == 0 ||
        evidence->selected_sa_spi != evidence->frame_spi ||
        evidence->selected_sa_spi != policy->expected_spi) {
        return TTCSIL_REJECT_SA;
    }
    if (!same_channel(policy->expected_channel, evidence->observed_channel) ||
        !same_channel(policy->expected_channel, evidence->selected_sa_channel)) {
        return TTCSIL_REJECT_CHANNEL;
    }
    if (policy->expected_epoch == 0 ||
        evidence->active_epoch != policy->expected_epoch) {
        return TTCSIL_REJECT_EPOCH;
    }
    *payload = length;
    return TTCSIL_ALLOW;
}
