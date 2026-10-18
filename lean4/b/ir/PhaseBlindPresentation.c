// Lean compiler output
// Module: PhaseBlindPresentation
// Imports: public import Init public meta import Init public import GaussIntKernel
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
lean_object* lp_FiniteQuantum_GaussInt_sqMod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind___redArg(lean_object* v_v_1_, lean_object* v_q_2_){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_apply_1(v_v_1_, v_q_2_);
v___x_4_ = lp_FiniteQuantum_GaussInt_sqMod(v___x_3_);
lean_dec_ref(v___x_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind(lean_object* v_Q_5_, lean_object* v_v_6_, lean_object* v_q_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind___redArg(v_v_6_, v_q_7_);
return v___x_8_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_GaussIntKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PhaseBlindPresentation(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_GaussIntKernel(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
