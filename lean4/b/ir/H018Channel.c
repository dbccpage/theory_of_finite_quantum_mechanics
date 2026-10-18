// Lean compiler output
// Module: H018Channel
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H017MatrixFiniteRecovery public import H018Density
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg(lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_dephase(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_dephase___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
v___x_2_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat(uint8_t v_i_3_, uint8_t v_j_4_){
_start:
{
if (v_i_3_ == 0)
{
lean_object* v___x_5_; 
v___x_5_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_5_;
}
else
{
if (v_j_4_ == 0)
{
lean_object* v___x_6_; 
v___x_6_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_6_;
}
else
{
lean_object* v___x_7_; 
v___x_7_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___closed__0);
return v___x_7_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___boxed(lean_object* v_i_8_, lean_object* v_j_9_){
_start:
{
uint8_t v_i_boxed_10_; uint8_t v_j_boxed_11_; lean_object* v_res_12_; 
v_i_boxed_10_ = lean_unbox(v_i_8_);
v_j_boxed_11_ = lean_unbox(v_j_9_);
v_res_12_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat(v_i_boxed_10_, v_j_boxed_11_);
return v_res_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_dephase(lean_object* v_A_13_, uint8_t v_i_14_, uint8_t v_j_15_){
_start:
{
if (v_i_14_ == 0)
{
if (v_j_15_ == 0)
{
lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; 
v___x_16_ = lean_box(v_i_14_);
v___x_17_ = lean_box(v_j_15_);
v___x_18_ = lean_apply_2(v_A_13_, v___x_16_, v___x_17_);
return v___x_18_;
}
else
{
lean_object* v___x_19_; 
lean_dec_ref(v_A_13_);
v___x_19_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_19_;
}
}
else
{
if (v_j_15_ == 0)
{
lean_object* v___x_20_; 
lean_dec_ref(v_A_13_);
v___x_20_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_20_;
}
else
{
lean_object* v___x_21_; lean_object* v___x_22_; lean_object* v___x_23_; 
v___x_21_ = lean_box(v_i_14_);
v___x_22_ = lean_box(v_j_15_);
v___x_23_ = lean_apply_2(v_A_13_, v___x_21_, v___x_22_);
return v___x_23_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_dephase___boxed(lean_object* v_A_24_, lean_object* v_i_25_, lean_object* v_j_26_){
_start:
{
uint8_t v_i_boxed_27_; uint8_t v_j_boxed_28_; lean_object* v_res_29_; 
v_i_boxed_27_ = lean_unbox(v_i_25_);
v_j_boxed_28_ = lean_unbox(v_j_26_);
v_res_29_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_dephase(v_A_24_, v_i_boxed_27_, v_j_boxed_28_);
return v_res_29_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___closed__0(void){
_start:
{
lean_object* v___x_30_; lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_30_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___boxed), 2, 0);
v___x_31_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
v___x_32_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___boxed), 5, 3);
lean_closure_set(v___x_32_, 0, lean_box(0));
lean_closure_set(v___x_32_, 1, v___x_31_);
lean_closure_set(v___x_32_, 2, v___x_30_);
return v___x_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix(lean_object* v_A_33_, uint8_t v_a_34_, uint8_t v_a_35_){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; lean_object* v___x_40_; 
v___x_36_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
v___x_37_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_mixMat___boxed), 2, 0);
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___closed__0);
v___x_39_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___boxed), 6, 4);
lean_closure_set(v___x_39_, 0, lean_box(0));
lean_closure_set(v___x_39_, 1, v___x_36_);
lean_closure_set(v___x_39_, 2, v_A_33_);
lean_closure_set(v___x_39_, 3, v___x_38_);
v___x_40_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg(v___x_36_, v___x_37_, v___x_39_, v_a_34_, v_a_35_);
return v___x_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix___boxed(lean_object* v_A_41_, lean_object* v_a_42_, lean_object* v_a_43_){
_start:
{
uint8_t v_a_15__boxed_44_; uint8_t v_a_16__boxed_45_; lean_object* v_res_46_; 
v_a_15__boxed_44_ = lean_unbox(v_a_42_);
v_a_16__boxed_45_ = lean_unbox(v_a_43_);
v_res_46_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Channel_conjMix(v_A_41_, v_a_15__boxed_44_, v_a_16__boxed_45_);
return v_res_46_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H017MatrixFiniteRecovery(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H018Density(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H018Channel(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H004FreeLinearization(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H017MatrixFiniteRecovery(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H018Density(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
