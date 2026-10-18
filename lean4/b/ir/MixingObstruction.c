// Lean compiler output
// Module: MixingObstruction
// Imports: public import Init public meta import Init public import QuotientFiber
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
lean_object* lp_FiniteQuantum_GaussInt_add(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_GaussInt_neg(lean_object*);
lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mix(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mix___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mixedReadout(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mixedReadout___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mix(lean_object* v_v_1_, uint8_t v_q_2_){
_start:
{
uint8_t v___x_3_; 
v___x_3_ = 1;
if (v_q_2_ == 0)
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v___x_4_ = lean_box(v_q_2_);
lean_inc_ref(v_v_1_);
v___x_5_ = lean_apply_1(v_v_1_, v___x_4_);
v___x_6_ = lean_box(v___x_3_);
v___x_7_ = lean_apply_1(v_v_1_, v___x_6_);
v___x_8_ = lp_FiniteQuantum_GaussInt_add(v___x_5_, v___x_7_);
lean_dec_ref(v___x_5_);
return v___x_8_;
}
else
{
uint8_t v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; 
v___x_9_ = 0;
v___x_10_ = lean_box(v___x_9_);
lean_inc_ref(v_v_1_);
v___x_11_ = lean_apply_1(v_v_1_, v___x_10_);
v___x_12_ = lean_box(v___x_3_);
v___x_13_ = lean_apply_1(v_v_1_, v___x_12_);
v___x_14_ = lp_FiniteQuantum_GaussInt_neg(v___x_13_);
v___x_15_ = lp_FiniteQuantum_GaussInt_add(v___x_11_, v___x_14_);
lean_dec_ref(v___x_11_);
return v___x_15_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mix___boxed(lean_object* v_v_16_, lean_object* v_q_17_){
_start:
{
uint8_t v_q_boxed_18_; lean_object* v_res_19_; 
v_q_boxed_18_ = lean_unbox(v_q_17_);
v_res_19_ = lp_FiniteQuantum_SuperpositionQuotientFiber_mix(v_v_16_, v_q_boxed_18_);
return v_res_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mixedReadout(lean_object* v_v_20_, uint8_t v_a_21_){
_start:
{
lean_object* v___x_22_; lean_object* v___x_23_; lean_object* v___x_24_; 
v___x_22_ = lean_alloc_closure((void*)(lp_FiniteQuantum_SuperpositionQuotientFiber_mix___boxed), 2, 1);
lean_closure_set(v___x_22_, 0, v_v_20_);
v___x_23_ = lean_box(v_a_21_);
v___x_24_ = lp_FiniteQuantum_SuperpositionQuotientFiber_phaseBlind___redArg(v___x_22_, v___x_23_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SuperpositionQuotientFiber_mixedReadout___boxed(lean_object* v_v_25_, lean_object* v_a_26_){
_start:
{
uint8_t v_a_5__boxed_27_; lean_object* v_res_28_; 
v_a_5__boxed_27_ = lean_unbox(v_a_26_);
v_res_28_ = lp_FiniteQuantum_SuperpositionQuotientFiber_mixedReadout(v_v_25_, v_a_5__boxed_27_);
return v_res_28_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_QuotientFiber(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_MixingObstruction(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_QuotientFiber(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
