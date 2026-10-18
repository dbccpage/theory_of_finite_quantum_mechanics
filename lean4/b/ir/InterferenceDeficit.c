// Lean compiler output
// Module: InterferenceDeficit
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
extern lean_object* lp_FiniteQuantum_GaussInt_one;
lean_object* lp_FiniteQuantum_GaussInt_neg(lean_object*);
extern lean_object* lp_FiniteQuantum_GaussInt_i;
lean_object* lp_FiniteQuantum_GaussInt_add(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_GaussInt_sqMod(lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_L1__norm(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_interfered__weight(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_interference__deficit(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__plus(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__plus___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__ortho(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__ortho___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_L1__norm(lean_object* v_v_1_){
_start:
{
uint8_t v___x_2_; lean_object* v___x_3_; lean_object* v___x_4_; lean_object* v___x_5_; uint8_t v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_2_ = 0;
v___x_3_ = lean_box(v___x_2_);
lean_inc_ref(v_v_1_);
v___x_4_ = lean_apply_1(v_v_1_, v___x_3_);
v___x_5_ = lp_FiniteQuantum_GaussInt_sqMod(v___x_4_);
lean_dec_ref(v___x_4_);
v___x_6_ = 1;
v___x_7_ = lean_box(v___x_6_);
v___x_8_ = lean_apply_1(v_v_1_, v___x_7_);
v___x_9_ = lp_FiniteQuantum_GaussInt_sqMod(v___x_8_);
lean_dec_ref(v___x_8_);
v___x_10_ = lean_int_add(v___x_5_, v___x_9_);
lean_dec(v___x_9_);
lean_dec(v___x_5_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_interfered__weight(lean_object* v_v_11_){
_start:
{
uint8_t v___x_12_; lean_object* v___x_13_; lean_object* v___x_14_; uint8_t v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; 
v___x_12_ = 0;
v___x_13_ = lean_box(v___x_12_);
lean_inc_ref(v_v_11_);
v___x_14_ = lean_apply_1(v_v_11_, v___x_13_);
v___x_15_ = 1;
v___x_16_ = lean_box(v___x_15_);
v___x_17_ = lean_apply_1(v_v_11_, v___x_16_);
v___x_18_ = lp_FiniteQuantum_GaussInt_add(v___x_14_, v___x_17_);
lean_dec_ref(v___x_14_);
v___x_19_ = lp_FiniteQuantum_GaussInt_sqMod(v___x_18_);
lean_dec_ref(v___x_18_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_interference__deficit(lean_object* v_v_20_){
_start:
{
lean_object* v___x_21_; lean_object* v___x_22_; lean_object* v___x_23_; 
lean_inc_ref(v_v_20_);
v___x_21_ = lp_FiniteQuantum_InterferenceNonL1Resource_interfered__weight(v_v_20_);
v___x_22_ = lp_FiniteQuantum_InterferenceNonL1Resource_L1__norm(v_v_20_);
v___x_23_ = lean_int_sub(v___x_21_, v___x_22_);
lean_dec(v___x_22_);
lean_dec(v___x_21_);
return v___x_23_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__plus(uint8_t v_x_24_){
_start:
{
lean_object* v___x_25_; 
v___x_25_ = lp_FiniteQuantum_GaussInt_one;
return v___x_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__plus___boxed(lean_object* v_x_26_){
_start:
{
uint8_t v_x_4__boxed_27_; lean_object* v_res_28_; 
v_x_4__boxed_27_ = lean_unbox(v_x_26_);
v_res_28_ = lp_FiniteQuantum_InterferenceNonL1Resource_psi__plus(v_x_4__boxed_27_);
return v_res_28_;
}
}
static lean_object* _init_lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___closed__0(void){
_start:
{
lean_object* v___x_29_; lean_object* v___x_30_; 
v___x_29_ = lp_FiniteQuantum_GaussInt_one;
v___x_30_ = lp_FiniteQuantum_GaussInt_neg(v___x_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus(uint8_t v_q_31_){
_start:
{
if (v_q_31_ == 0)
{
lean_object* v___x_32_; 
v___x_32_ = lp_FiniteQuantum_GaussInt_one;
return v___x_32_;
}
else
{
lean_object* v___x_33_; 
v___x_33_ = lean_obj_once(&lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___closed__0, &lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___closed__0_once, _init_lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___closed__0);
return v___x_33_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus___boxed(lean_object* v_q_34_){
_start:
{
uint8_t v_q_boxed_35_; lean_object* v_res_36_; 
v_q_boxed_35_ = lean_unbox(v_q_34_);
v_res_36_ = lp_FiniteQuantum_InterferenceNonL1Resource_psi__minus(v_q_boxed_35_);
return v_res_36_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__ortho(uint8_t v_q_37_){
_start:
{
if (v_q_37_ == 0)
{
lean_object* v___x_38_; 
v___x_38_ = lp_FiniteQuantum_GaussInt_one;
return v___x_38_;
}
else
{
lean_object* v___x_39_; 
v___x_39_ = lp_FiniteQuantum_GaussInt_i;
return v___x_39_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InterferenceNonL1Resource_psi__ortho___boxed(lean_object* v_q_40_){
_start:
{
uint8_t v_q_boxed_41_; lean_object* v_res_42_; 
v_q_boxed_41_ = lean_unbox(v_q_40_);
v_res_42_ = lp_FiniteQuantum_InterferenceNonL1Resource_psi__ortho(v_q_boxed_41_);
return v_res_42_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_GaussIntKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_InterferenceDeficit(uint8_t builtin) {
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
