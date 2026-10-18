// Lean compiler output
// Module: H006PermutationUnitary
// Imports: public import Init public meta import Init public import HWKernel public import H003ReversibilityGate public import H004FreeLinearization public import H005InnerProductAdmission
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_swapI(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_swapI___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU___redArg(lean_object* v_R_1_, lean_object* v_v_2_, lean_object* v_q_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; 
v___x_4_ = lean_apply_1(v_R_1_, v_q_3_);
v___x_5_ = lean_apply_1(v_v_2_, v___x_4_);
return v___x_5_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU(lean_object* v_K_6_, lean_object* v_Q_7_, lean_object* v_x_8_, lean_object* v_00_u03c4_9_, lean_object* v_R_10_, lean_object* v_v_11_, lean_object* v_q_12_){
_start:
{
lean_object* v___x_13_; 
v___x_13_ = lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU___redArg(v_R_10_, v_v_11_, v_q_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU___boxed(lean_object* v_K_14_, lean_object* v_Q_15_, lean_object* v_x_16_, lean_object* v_00_u03c4_17_, lean_object* v_R_18_, lean_object* v_v_19_, lean_object* v_q_20_){
_start:
{
lean_object* v_res_21_; 
v_res_21_ = lp_FiniteQuantum_FableHilbertWalk20260819_H006_permU(v_K_14_, v_Q_15_, v_x_16_, v_00_u03c4_17_, v_R_18_, v_v_19_, v_q_20_);
lean_dec(v_00_u03c4_17_);
lean_dec_ref(v_x_16_);
return v_res_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___redArg(lean_object* v_00_u03c4_22_){
_start:
{
lean_inc(v_00_u03c4_22_);
return v_00_u03c4_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___redArg___boxed(lean_object* v_00_u03c4_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___redArg(v_00_u03c4_23_);
lean_dec(v_00_u03c4_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv(lean_object* v_Q_25_, lean_object* v_00_u03c4_26_, lean_object* v_R_27_){
_start:
{
lean_inc(v_00_u03c4_26_);
return v_00_u03c4_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv___boxed(lean_object* v_Q_28_, lean_object* v_00_u03c4_29_, lean_object* v_R_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_FiniteQuantum_FableHilbertWalk20260819_H006_revInv(v_Q_28_, v_00_u03c4_29_, v_R_30_);
lean_dec(v_R_30_);
lean_dec(v_00_u03c4_29_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_swapI(lean_object* v_v_32_, uint8_t v_q_33_){
_start:
{
lean_object* v___x_34_; uint8_t v___y_36_; 
v___x_34_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
if (v_q_33_ == 0)
{
uint8_t v___x_40_; 
v___x_40_ = 1;
v___y_36_ = v___x_40_;
goto v___jp_35_;
}
else
{
uint8_t v___x_41_; 
v___x_41_ = 0;
v___y_36_ = v___x_41_;
goto v___jp_35_;
}
v___jp_35_:
{
lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_37_ = lean_box(v___y_36_);
v___x_38_ = lean_apply_1(v_v_32_, v___x_37_);
v___x_39_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(v___x_34_, v___x_38_);
return v___x_39_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H006_swapI___boxed(lean_object* v_v_42_, lean_object* v_q_43_){
_start:
{
uint8_t v_q_boxed_44_; lean_object* v_res_45_; 
v_q_boxed_44_ = lean_unbox(v_q_43_);
v_res_45_ = lp_FiniteQuantum_FableHilbertWalk20260819_H006_swapI(v_v_42_, v_q_boxed_44_);
return v_res_45_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H006PermutationUnitary(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H005InnerProductAdmission(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
