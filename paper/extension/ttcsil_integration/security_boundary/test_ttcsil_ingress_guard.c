#include "ttcsil_ingress_guard.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static unsigned passed = 0;

#define CHECK(cond) do { if (!(cond)) { \
    fprintf(stderr, "FAIL at %s:%d: %s\\n", __FILE__, __LINE__, #cond); \
    return 1; } ++passed; } while (0)

static ttcsil_policy good_policy(void)
{
    ttcsil_policy p = {{0, 71, 3, 2}, 4, 17, 128, 1};
    return p;
}

static ttcsil_evidence good_evidence(void)
{
    ttcsil_evidence e = {{0, 71, 3, 2}, 4, {0, 71, 3, 2},
                        4, 17, true, true, true};
    return e;
}

static int test_length(void)
{
    size_t n = 999;
    CHECK(ttcsil_guard_length(35, 12, 35, 64, 1, &n) == TTCSIL_ALLOW);
    CHECK(n == 23);
    CHECK(ttcsil_guard_length(11, 12, 100, 64, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(65, 12, 100, 64, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(35, 12, 34, 64, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(12, 12, 12, 64, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(0, 0, 0, 64, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(35, 12, 35, 10, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(35, 12, 35, 64, 100, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(SIZE_MAX, 12, SIZE_MAX, 64, 1, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    CHECK(ttcsil_guard_length(35, 12, 35, 64, 1, NULL) == TTCSIL_REJECT_INPUT);
    CHECK(ttcsil_guard_length(12, 12, 12, 64, 0, &n) == TTCSIL_ALLOW && n == 0);
    return 0;
}

static int test_authorization(void)
{
    ttcsil_policy p = good_policy();
    ttcsil_evidence e = good_evidence();
    size_t n = SIZE_MAX;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_ALLOW && n == 23);
    CHECK(ttcsil_guard_tc(NULL, &e, 35, 12, 35, &n) == TTCSIL_REJECT_INPUT && n == 0);
    CHECK(ttcsil_guard_tc(&p, NULL, 35, 12, 35, &n) == TTCSIL_REJECT_INPUT && n == 0);
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, NULL) == TTCSIL_REJECT_INPUT);
    CHECK(ttcsil_guard_tc(&p, &e, 11, 12, 35, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    e.cryptographic_verification_succeeded = false;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CRYPTO && n == 0);
    e = good_evidence(); e.selected_sa_authentication_required = false;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_SA && n == 0);
    e = good_evidence(); e.selected_sa_operational = false;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_SA && n == 0);
    e = good_evidence(); e.frame_spi = 1;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_SA && n == 0);
    e = good_evidence(); e.selected_sa_spi = 1;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_SA && n == 0);
    e = good_evidence(); e.observed_channel.vcid = 4;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CHANNEL && n == 0);
    e = good_evidence(); e.observed_channel.scid = 72;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CHANNEL && n == 0);
    e = good_evidence(); e.observed_channel.tfvn = 1;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CHANNEL && n == 0);
    e = good_evidence(); e.observed_channel.map_id = 3;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CHANNEL && n == 0);
    e = good_evidence(); e.selected_sa_channel.vcid = 4;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CHANNEL && n == 0);
    e = good_evidence(); e.selected_sa_channel.map_id = 3;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_CHANNEL && n == 0);
    e = good_evidence(); e.active_epoch = 18;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_EPOCH && n == 0);
    p.expected_epoch = 0; e = good_evidence();
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_EPOCH && n == 0);
    p = good_policy(); p.expected_spi = 0;
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 35, &n) == TTCSIL_REJECT_SA && n == 0);
    p = good_policy(); e = good_evidence();
    CHECK(ttcsil_guard_tc(&p, &e, 35, 12, 30, &n) == TTCSIL_REJECT_LENGTH && n == 0);
    return 0;
}

int main(void)
{
    if (test_length() || test_authorization()) return EXIT_FAILURE;
    printf("TTCSIL_GUARD_UNIT_ASSERTIONS=%u PASS\\n", passed);
    puts("TTCSIL_F1_GUARD_UNIT=PASS; F1_INTEGRATION=HOLD; F2_F3_F4=NOT_EXECUTED");
    return EXIT_SUCCESS;
}
