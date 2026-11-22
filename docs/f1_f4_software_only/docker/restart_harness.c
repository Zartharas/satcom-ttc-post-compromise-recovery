/* F1-F4 software-only restart harness for nasa/CryptoLib (in-memory SA + internal key ring, SA_FILE build).
 * Usage: restart_harness <scenario|dump> ; each invocation is a NEW PROCESS = simulated processor restart
 * (no Crypto_Shutdown, i.e. an abrupt "reset"). Frames/setup copied from CryptoLib test/unit/ut_ep_*.c.
 * Run only inside /tmp/f1f4/work (sa_save_file.bin lives in cwd). */
#include "crypto.h"
#include "sa_interface.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gcrypt.h>

static void hexconv(const char *h, uint8_t **b, int *len) {
    size_t n = strlen(h) / 2; *b = malloc(n);
    for (size_t i = 0; i < n; i++) { unsigned v; sscanf(h + 2*i, "%2x", &v); (*b)[i] = (uint8_t)v; }
    *len = (int)n;
}
static void dump_sa(const char *tag, int spi) {
    SecurityAssociation_t *s = NULL;
    sa_if->sa_get_from_spi(spi, &s);
    fprintf(stderr, "HARNESS|%s|SA%d state=%d ekid=%d iv_len=%d iv=", tag, spi, s->sa_state, s->ekid, s->iv_len);
    for (int i = 0; i < s->iv_len; i++) fprintf(stderr, "%02x", s->iv[i]);
    fprintf(stderr, " arsn_len=%d arsn=", s->arsn_len);
    for (int i = 0; i < s->arsn_len; i++) fprintf(stderr, "%02x", s->arsn[i]);
    fprintf(stderr, " arsnw=%d\n", s->arsnw);
}
static void dump_key(const char *tag, int kid) {
    crypto_key_t *k = key_if->get_key(kid);
    fprintf(stderr, "HARNESS|%s|KEY%d state=%d len=%d val[0..3]=%02x%02x%02x%02x\n", tag, kid, k->key_state, k->key_len,
            k->value[0], k->value[1], k->value[2], k->value[3]);
}
static void dump_all(const char *tag) {
    dump_sa(tag, 0); dump_sa(tag, 6); dump_sa(tag, 7);
    dump_key(tag, 0); dump_key(tag, 132); dump_key(tag, 140); dump_key(tag, 141); dump_key(tag, 142);
}
static int init_lib(int frame_len) {
#ifdef CRYPTOLIB_OLD_API
    /* CryptoLib b46879c (NOS3 pin): single-call config and GvcidManagedParameters_t; same option values as the new-API branch */
    Crypto_Config_CryptoLib(KEY_TYPE_INTERNAL, MC_TYPE_INTERNAL, SA_TYPE_INMEMORY, CRYPTOGRAPHY_TYPE_LIBGCRYPT, IV_INTERNAL,
                            CRYPTO_TC_CREATE_FECF_TRUE, TC_PROCESS_SDLS_PDUS_TRUE, TC_HAS_PUS_HDR, TC_IGNORE_SA_STATE_FALSE,
                            TC_IGNORE_ANTI_REPLAY_FALSE, TC_UNIQUE_SA_PER_MAP_ID_FALSE, TC_CHECK_FECF_TRUE, 0x3F,
                            SA_INCREMENT_NONTRANSMITTED_IV_TRUE);
    GvcidManagedParameters_t p0 = {0, 0x0003, 0, TC_NO_FECF, AOS_FHEC_NA, AOS_IZ_NA, 0, TC_HAS_SEGMENT_HDRS, (uint16_t)frame_len, TC_OCF_NA, 1};
    Crypto_Config_Add_Gvcid_Managed_Parameters(p0);
    GvcidManagedParameters_t p1 = {0, 0x0003, 1, TC_NO_FECF, AOS_FHEC_NA, AOS_IZ_NA, 0, TC_HAS_SEGMENT_HDRS, (uint16_t)frame_len, TC_OCF_NA, 1};
    Crypto_Config_Add_Gvcid_Managed_Parameters(p1);
    return Crypto_Init();
#else
    Crypto_Config_CryptoLib(KEY_TYPE_INTERNAL, MC_TYPE_INTERNAL, SA_TYPE_INMEMORY, CRYPTOGRAPHY_TYPE_LIBGCRYPT, IV_INTERNAL);
    Crypto_Config_TC(CRYPTO_TC_CREATE_FECF_TRUE, TC_PROCESS_SDLS_PDUS_TRUE, TC_HAS_PUS_HDR, TC_IGNORE_ANTI_REPLAY_FALSE,
                     TC_IGNORE_SA_STATE_FALSE, TC_UNIQUE_SA_PER_MAP_ID_FALSE, TC_CHECK_FECF_TRUE, 0x3F,
                     SA_INCREMENT_NONTRANSMITTED_IV_TRUE);
    TCGvcidManagedParameters_t p0 = {0, 0x0003, 0, TC_NO_FECF, TC_HAS_SEGMENT_HDRS, (uint16_t)frame_len, 1};
    Crypto_Config_Add_TC_Gvcid_Managed_Parameters(p0);
    TCGvcidManagedParameters_t p1 = {0, 0x0003, 1, TC_NO_FECF, TC_HAS_SEGMENT_HDRS, (uint16_t)frame_len, 1};
    Crypto_Config_Add_TC_Gvcid_Managed_Parameters(p1);
    return Crypto_Init();
#endif
}
static int send(const char *hex, const char *name) {
    uint8_t *b; int len; TC_t pf; hexconv(hex, &b, &len);
    int st = Crypto_TC_ProcessSecurity(b, &len, &pf);
    fprintf(stderr, "HARNESS|frame|%s status=%d\n", name, st);
    free(b); return st;
}

/* ---- Valid extended-procedure frame builder (added in run 5) ----
 * The CryptoLib unit-test OTAR/ACTIVATE frames carry two extra 0x0000 bytes ahead of the 0x1980 packet header
 * (SA0 shivf_len is 0), so Crypto_Process_Extended_Procedure_Pdu never dispatches them. Frames built here start the
 * TC PDU at 0x1980 and carry correct frame, packet and TLV (bits) lengths. No FECF (managed parameters TC_NO_FECF). */
static int build_ep_frame(uint8_t *out, uint8_t tlv_hdr, const uint8_t *data, int dlen) {
    int pdu = 6 + 4 + 3 + dlen, total = 5 + 1 + 2 + pdu, i = 0;
    out[i++] = 0x20; out[i++] = 0x03; out[i++] = (uint8_t)(((total - 1) >> 8) & 0x03); out[i++] = (uint8_t)((total - 1) & 0xFF);
    out[i++] = 0x00; out[i++] = 0xFF; out[i++] = 0x00; out[i++] = 0x00;      /* seq, MAP/segment hdr, SPI 0 */
    out[i++] = 0x19; out[i++] = 0x80; out[i++] = 0xD0; out[i++] = 0x37;     /* CCSDS apid 0x1980, seq/pktid */
    out[i++] = (uint8_t)(((dlen + 4) >> 8) & 0xFF); out[i++] = (uint8_t)((dlen + 4) & 0xFF);
    out[i++] = 0x19; out[i++] = 0x7F; out[i++] = 0x0B; out[i++] = 0x00;      /* PUS hdr */
    out[i++] = tlv_hdr; out[i++] = (uint8_t)(((dlen * 8) >> 8) & 0xFF); out[i++] = (uint8_t)((dlen * 8) & 0xFF);
    memcpy(out + i, data, dlen); i += dlen;
    return i;
}
static int send_ep(uint8_t *f, int len, const char *name) {
    TC_t pf; int st = Crypto_TC_ProcessSecurity(f, &len, &pf);
    fprintf(stderr, "HARNESS|frame|%s len=%d status=%d\n", name, len, st); return st;
}
/* ACTIVATE keys 140,141,142 (TLV pid 2; data = 2-byte key ids) */
static int send_activate(void) {
    uint8_t d[6] = {0x00,0x8C,0x00,0x8D,0x00,0x8E}, f[64];
    int n = build_ep_frame(f, 0x02, d, 6); return send_ep(f, n, "ACTIVATE_140_142_valid");
}
/* OTAR under master key MKID 0 (must be ACTIVE): data = MKID(2) | IV(12) | AES-256-GCM(keyid(2)|key(32) x3) | tag(16).
 * Master key value is read from the key ring (library default); keys loaded are fixed test patterns 0xA0+n. */
static int send_otar(void) {
    uint8_t iv[12] = {1,2,3,4,5,6,7,8,9,10,11,12}, pt[102], d[2+12+102+16], f[256];
    for (int n = 0; n < 3; n++) { int o = n * 34; pt[o] = 0x00; pt[o+1] = (uint8_t)(0x8C + n); memset(pt + o + 2, 0xA0 + n, 32); }
    crypto_key_t *mk = key_if->get_key(0);
    gcry_cipher_hd_t h; uint8_t tag[16], ct[102];
    if (gcry_cipher_open(&h, GCRY_CIPHER_AES256, GCRY_CIPHER_MODE_GCM, 0)) return -1000;
    gcry_cipher_setkey(h, mk->value, 32); gcry_cipher_setiv(h, iv, 12);
    gcry_cipher_encrypt(h, ct, 102, pt, 102); gcry_cipher_gettag(h, tag, 16); gcry_cipher_close(h);
    d[0] = 0x00; d[1] = 0x00; memcpy(d + 2, iv, 12); memcpy(d + 14, ct, 102); memcpy(d + 116, tag, 16);
    int n = build_ep_frame(f, 0x01, d, 132); return send_ep(f, n, "OTAR_140_142_valid");
}
/* SA0 setup as in ut_ep_key_mgmt.c OTAR test (no IV / no ARSN) */
static void sa0_plain(void) {
    SecurityAssociation_t *s; sa_if->sa_get_from_spi(0, &s);
    s->sa_state = SA_OPERATIONAL; s->ecs_len = 1; s->ecs = CRYPTO_CIPHER_NONE; s->est = 0; s->ast = 0;
    s->shsnf_len = 0; s->arsn_len = 0; s->arsnw = 5; s->iv_len = 0; s->shivf_len = 0;
    s->gvcid_blk.tfvn = 0; s->gvcid_blk.scid = 3; s->gvcid_blk.vcid = 0;
}
/* SA0 setup as in ut_ep_key_mgmt.c ACTIVATE test (12-byte IV) */
static void sa0_iv(void) {
    SecurityAssociation_t *s; sa_if->sa_get_from_spi(0, &s);
    sa_if->sa_get_from_spi(1, &s); s->sa_state = SA_NONE;
    sa_if->sa_get_from_spi(0, &s);
    s->sa_state = SA_OPERATIONAL; s->ecs_len = 1; s->ecs = CRYPTO_CIPHER_NONE; s->shsnf_len = 0; s->arsn_len = 0;
    s->arsnw = 5; s->iv_len = 12; s->gvcid_blk.tfvn = 0; s->gvcid_blk.scid = 3; s->gvcid_blk.vcid = 0;
    uint8_t iv[12] = {0xb6,0xac,0x8e,0x49,0x63,0xf4,0x92,0x07,0xff,0xd6,0x37,0x4b};
    memcpy(s->iv, iv, 12);
}
static const char *OTAR =
 "2003009e00ff000000001980d037008c197f0b000104400000344892bbc54f5395297d4c37172f2a3c46f6a81c1349e9e26ac80985d8bb"
 "d55a5814c662e49fba52f99ba09558cd21cf268b8e50b2184137e80f76122034c580464e2f06d2659a50508bdfe9e9a55990ba4148"
 "af896d8a6eebe8b5d2258685d4ce217a20174fdd4f0efac62758c51b04e55710a47209c923b641d19a39001f9e986166f5ffd9";
static const char *ACTIVATE = "2003001e00ff000000001980d038000c197f0b00020004008d008e82ebe4fc";
static const char *STOP6 = "2003001a00ff00001980d0b6000a197f0b001e00300006938f21c4";
static const char *SETARSN7 = "2003002600ff00001980d0b10016197f0b001a0090000600000000000000000000006413b5983e";
static void sa0_sdls(void) { /* as ut_ep_sa_mgmt.c */
    SecurityAssociation_t *s; sa_if->sa_get_from_spi(0, &s);
    s->shivf_len = 0; s->sa_state = SA_OPERATIONAL; s->iv_len = 12; s->shsnf_len = 0; s->arsnw = 5; s->arsnw_len = 1;
    s->arsn_len = 0; s->gvcid_blk.scid = SCID & 0x3FF;
}
int main(int argc, char **argv) {
    if (argc < 2) return 2;
    const char *sc = argv[1];
    if (!strcmp(sc, "dump")) {            /* restart: init WITHOUT deleting sa_save_file.bin */
        int st = init_lib(200); fprintf(stderr, "HARNESS|dump|init status=%d\n", st); dump_all("after_restart"); return 0;
    }
    remove("sa_save_file.bin");           /* fresh start for a scenario's first process */
    int st = init_lib(200); fprintf(stderr, "HARNESS|%s|init status=%d\n", sc, st);
    dump_all("baseline_after_init");
    if (!strcmp(sc, "otar_only")) {          /* F3a: key load (PREACTIVE) then restart before ACTIVATE */
        sa0_plain(); send_otar();
    } else if (!strcmp(sc, "otar_activate")) { /* F3b: OTAR + ACTIVATE completed, then restart */
        sa0_plain(); send_otar(); send_activate();
    } else if (!strcmp(sc, "activate_only")) { /* F3e: command-driven activation only (keys stay empty PREACTIVE->ACTIVE) */
        sa0_plain(); send_activate();
    } else if (!strcmp(sc, "sa_stop6")) {    /* F1/F3c: SA6 OPERATIONAL -> KEYED by SA_STOP, restart */
        sa0_sdls(); SecurityAssociation_t *s; sa_if->sa_get_from_spi(6, &s); s->sa_state = SA_OPERATIONAL;
        send(STOP6, "SA_STOP_6");
    } else if (!strcmp(sc, "set_arsn7")) {   /* F2: SA7 ARSN set by ground command, restart */
        sa0_sdls(); SecurityAssociation_t *s; sa_if->sa_get_from_spi(7, &s); s->sa_state = SA_OPERATIONAL; s->arsn_len = 11;
        send(SETARSN7, "SA_SET_ARSN_7");
    } else if (!strcmp(sc, "key_direct")) {  /* F3d: key ring mutated DIRECTLY in RAM (not via EP command; EP key frames were not dispatched in this harness) */
        crypto_key_t *k = key_if->get_key(141); k->key_state = KEY_ACTIVE; k->value[0] = 0xAB; k->key_len = 32;
        k = key_if->get_key(132); k->key_state = KEY_ACTIVE; /* populated PREACTIVE -> ACTIVE */
        SecurityAssociation_t *s; sa_if->sa_get_from_spi(0, &s); sa0_sdls();
        send(STOP6, "SA_STOP_6 (used only to trigger a frame-driven SA save)");
    } else { fprintf(stderr, "unknown scenario\n"); return 2; }
    dump_all("end_of_process1_in_RAM");
    return 0;                              /* abrupt exit, no Crypto_Shutdown */
}
