// Lean compiler output
// Module: PrimitiveLiftCertificate
// Imports: public import Init public meta import Init public import PrimitiveLiftCandidate
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
static const lean_ctor_object lp_FiniteQuantum_OmegaCore_PrimitiveLiftCertificate_LiftCertificate_toCandidate___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 1, 1, 1, 1, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCertificate_LiftCertificate_toCandidate___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_PrimitiveLiftCertificate_LiftCertificate_toCandidate___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCertificate_LiftCertificate_toCandidate(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCertificate_LiftCertificate_toCandidate(lean_object* v___cert_3_){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = ((lean_object*)(lp_FiniteQuantum_OmegaCore_PrimitiveLiftCertificate_LiftCertificate_toCandidate___closed__0));
return v___x_4_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveLiftCandidate(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PrimitiveLiftCertificate(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveLiftCandidate(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
