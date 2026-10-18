// Lean compiler output
// Module: H017Extras
// Imports: public import Init public meta import Init public import HWKernel public import H003ReversibilityGate public import H004FreeLinearization public import H007Complexification public import H011Circle public import H014TensorCompositionBoundary public import H014Interface public import H015IrreversibleFork public import H016ContinuousDynamicsFork public import H017MatrixFiniteRecovery public import H017Fin public import H017Gleason
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
lean_object* lean_int_neg(lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_gnormSq(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_gnormSq___boxed(lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0);
v___x_4_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_4_, 0, v___x_3_);
lean_ctor_set(v___x_4_, 1, v___x_3_);
return v___x_4_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__2(void){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; 
v___x_5_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0);
v___x_6_ = lean_int_neg(v___x_5_);
return v___x_6_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__3(void){
_start:
{
lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v___x_7_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__2);
v___x_8_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__0);
v___x_9_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_9_, 0, v___x_8_);
lean_ctor_set(v___x_9_, 1, v___x_7_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral(uint8_t v_i_10_, uint8_t v_j_11_){
_start:
{
if (v_i_10_ == 0)
{
if (v_j_11_ == 0)
{
lean_object* v___x_15_; 
v___x_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_15_;
}
else
{
goto v___jp_12_;
}
}
else
{
if (v_j_11_ == 0)
{
goto v___jp_12_;
}
else
{
lean_object* v___x_16_; 
v___x_16_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_16_;
}
}
v___jp_12_:
{
if (v_i_10_ == 0)
{
lean_object* v___x_13_; 
v___x_13_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__1);
return v___x_13_;
}
else
{
lean_object* v___x_14_; 
v___x_14_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___closed__3);
return v___x_14_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral___boxed(lean_object* v_i_17_, lean_object* v_j_18_){
_start:
{
uint8_t v_i_boxed_19_; uint8_t v_j_boxed_20_; lean_object* v_res_21_; 
v_i_boxed_19_ = lean_unbox(v_i_17_);
v_j_boxed_20_ = lean_unbox(v_j_18_);
v_res_21_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_notSpectral(v_i_boxed_19_, v_j_boxed_20_);
return v_res_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_gnormSq(lean_object* v_z_22_){
_start:
{
lean_object* v_re_23_; lean_object* v_im_24_; lean_object* v___x_25_; lean_object* v___x_26_; lean_object* v___x_27_; 
v_re_23_ = lean_ctor_get(v_z_22_, 0);
v_im_24_ = lean_ctor_get(v_z_22_, 1);
v___x_25_ = lean_int_mul(v_re_23_, v_re_23_);
v___x_26_ = lean_int_mul(v_im_24_, v_im_24_);
v___x_27_ = lean_int_add(v___x_25_, v___x_26_);
lean_dec(v___x_26_);
lean_dec(v___x_25_);
return v___x_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_gnormSq___boxed(lean_object* v_z_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Extras_gnormSq(v_z_28_);
lean_dec_ref(v_z_28_);
return v_res_29_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H007Complexification(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H011Circle(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H014TensorCompositionBoundary(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H014Interface(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H015IrreversibleFork(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H016ContinuousDynamicsFork(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H017MatrixFiniteRecovery(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H017Fin(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H017Gleason(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H017Extras(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H007Complexification(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H011Circle(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H014TensorCompositionBoundary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H014Interface(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H015IrreversibleFork(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H016ContinuousDynamicsFork(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H017MatrixFiniteRecovery(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H017Fin(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H017Gleason(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
