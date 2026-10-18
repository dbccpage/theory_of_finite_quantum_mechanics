// Lean compiler output
// Module: H006Envelope
// Imports: public import Init public meta import Init public import HWKernel public import H003ReversibilityGate public import H004FreeLinearization public import H006PermutationUnitary
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
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___lam__0(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___lam__0___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___lam__0(uint8_t v_q_1_){
_start:
{
return v_q_1_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___lam__0___boxed(lean_object* v_q_2_){
_start:
{
uint8_t v_q_boxed_3_; uint8_t v_res_4_; lean_object* v_r_5_; 
v_q_boxed_3_ = lean_unbox(v_q_2_);
v_res_4_ = lp_FiniteQuantum_FableHilbertWalk20260819_H006Envelope_idRev___lam__0(v_q_boxed_3_);
v_r_5_ = lean_box(v_res_4_);
return v_r_5_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H006PermutationUnitary(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H006Envelope(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_HWKernel(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H003ReversibilityGate(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H004FreeLinearization(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H006PermutationUnitary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
