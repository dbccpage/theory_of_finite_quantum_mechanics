// Lean compiler output
// Module: H012OperatorAlgebraShadow
// Imports: public import Init public meta import Init public import HWKernel
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
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_mmul(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_mmul___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat_x27(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat_x27___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_diag(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_diag___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_mmul(lean_object* v_A_1_, lean_object* v_B_2_, uint8_t v_i_3_, uint8_t v_j_4_){
_start:
{
uint8_t v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; uint8_t v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___x_5_ = 0;
v___x_6_ = lean_box(v_i_3_);
v___x_7_ = lean_box(v___x_5_);
lean_inc_ref(v_A_1_);
v___x_8_ = lean_apply_2(v_A_1_, v___x_6_, v___x_7_);
v___x_9_ = lean_box(v___x_5_);
v___x_10_ = lean_box(v_j_4_);
lean_inc_ref(v_B_2_);
v___x_11_ = lean_apply_2(v_B_2_, v___x_9_, v___x_10_);
v___x_12_ = lean_int_mul(v___x_8_, v___x_11_);
lean_dec(v___x_11_);
lean_dec(v___x_8_);
v___x_13_ = 1;
v___x_14_ = lean_box(v_i_3_);
v___x_15_ = lean_box(v___x_13_);
v___x_16_ = lean_apply_2(v_A_1_, v___x_14_, v___x_15_);
v___x_17_ = lean_box(v___x_13_);
v___x_18_ = lean_box(v_j_4_);
v___x_19_ = lean_apply_2(v_B_2_, v___x_17_, v___x_18_);
v___x_20_ = lean_int_mul(v___x_16_, v___x_19_);
lean_dec(v___x_19_);
lean_dec(v___x_16_);
v___x_21_ = lean_int_add(v___x_12_, v___x_20_);
lean_dec(v___x_20_);
lean_dec(v___x_12_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_mmul___boxed(lean_object* v_A_22_, lean_object* v_B_23_, lean_object* v_i_24_, lean_object* v_j_25_){
_start:
{
uint8_t v_i_boxed_26_; uint8_t v_j_boxed_27_; lean_object* v_res_28_; 
v_i_boxed_26_ = lean_unbox(v_i_24_);
v_j_boxed_27_ = lean_unbox(v_j_25_);
v_res_28_ = lp_FiniteQuantum_FableHilbertWalk20260819_H012_mmul(v_A_22_, v_B_23_, v_i_boxed_26_, v_j_boxed_27_);
return v_res_28_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0(void){
_start:
{
lean_object* v___x_29_; lean_object* v___x_30_; 
v___x_29_ = lean_unsigned_to_nat(0u);
v___x_30_ = lean_nat_to_int(v___x_29_);
return v___x_30_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1(void){
_start:
{
lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_31_ = lean_unsigned_to_nat(1u);
v___x_32_ = lean_nat_to_int(v___x_31_);
return v___x_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat(uint8_t v_i_33_, uint8_t v_j_34_){
_start:
{
if (v_i_33_ == 0)
{
if (v_j_34_ == 0)
{
goto v___jp_35_;
}
else
{
lean_object* v___x_37_; 
v___x_37_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1);
return v___x_37_;
}
}
else
{
goto v___jp_35_;
}
v___jp_35_:
{
lean_object* v___x_36_; 
v___x_36_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0);
return v___x_36_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___boxed(lean_object* v_i_38_, lean_object* v_j_39_){
_start:
{
uint8_t v_i_boxed_40_; uint8_t v_j_boxed_41_; lean_object* v_res_42_; 
v_i_boxed_40_ = lean_unbox(v_i_38_);
v_j_boxed_41_ = lean_unbox(v_j_39_);
v_res_42_ = lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat(v_i_boxed_40_, v_j_boxed_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat_x27(uint8_t v_i_43_, uint8_t v_j_44_){
_start:
{
if (v_i_43_ == 0)
{
goto v___jp_45_;
}
else
{
if (v_j_44_ == 0)
{
lean_object* v___x_47_; 
v___x_47_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__1);
return v___x_47_;
}
else
{
goto v___jp_45_;
}
}
v___jp_45_:
{
lean_object* v___x_46_; 
v___x_46_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0);
return v___x_46_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat_x27___boxed(lean_object* v_i_48_, lean_object* v_j_49_){
_start:
{
uint8_t v_i_boxed_50_; uint8_t v_j_boxed_51_; lean_object* v_res_52_; 
v_i_boxed_50_ = lean_unbox(v_i_48_);
v_j_boxed_51_ = lean_unbox(v_j_49_);
v_res_52_ = lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat_x27(v_i_boxed_50_, v_j_boxed_51_);
return v_res_52_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_diag(lean_object* v_d_53_, uint8_t v_i_54_, uint8_t v_j_55_){
_start:
{
if (v_i_54_ == 0)
{
if (v_j_55_ == 0)
{
lean_object* v___x_58_; lean_object* v___x_59_; 
v___x_58_ = lean_box(v_i_54_);
v___x_59_ = lean_apply_1(v_d_53_, v___x_58_);
return v___x_59_;
}
else
{
lean_dec_ref(v_d_53_);
goto v___jp_56_;
}
}
else
{
if (v_j_55_ == 0)
{
lean_dec_ref(v_d_53_);
goto v___jp_56_;
}
else
{
lean_object* v___x_60_; lean_object* v___x_61_; 
v___x_60_ = lean_box(v_i_54_);
v___x_61_ = lean_apply_1(v_d_53_, v___x_60_);
return v___x_61_;
}
}
v___jp_56_:
{
lean_object* v___x_57_; 
v___x_57_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H012_nMat___closed__0);
return v___x_57_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H012_diag___boxed(lean_object* v_d_62_, lean_object* v_i_63_, lean_object* v_j_64_){
_start:
{
uint8_t v_i_boxed_65_; uint8_t v_j_boxed_66_; lean_object* v_res_67_; 
v_i_boxed_65_ = lean_unbox(v_i_63_);
v_j_boxed_66_ = lean_unbox(v_j_64_);
v_res_67_ = lp_FiniteQuantum_FableHilbertWalk20260819_H012_diag(v_d_62_, v_i_boxed_65_, v_j_boxed_66_);
return v_res_67_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H012OperatorAlgebraShadow(uint8_t builtin) {
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
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
