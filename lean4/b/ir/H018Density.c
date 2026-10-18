// Lean compiler output
// Module: H018Density
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H017MatrixFiniteRecovery
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
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(lean_object*, uint8_t, uint8_t);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(lean_object*, lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___lam__0(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___lam__0___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_bellAmp(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_bellAmp___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra4(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ptrSecond(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ptrSecond___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra(lean_object* v_v_1_, uint8_t v_i_2_, uint8_t v_j_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v___x_4_ = lean_box(v_i_2_);
lean_inc_ref(v_v_1_);
v___x_5_ = lean_apply_1(v_v_1_, v___x_4_);
v___x_6_ = lean_box(v_j_3_);
v___x_7_ = lean_apply_1(v_v_1_, v___x_6_);
v___x_8_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(v___x_7_);
v___x_9_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(v___x_5_, v___x_8_);
lean_dec_ref(v___x_5_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra___boxed(lean_object* v_v_10_, lean_object* v_i_11_, lean_object* v_j_12_){
_start:
{
uint8_t v_i_boxed_13_; uint8_t v_j_boxed_14_; lean_object* v_res_15_; 
v_i_boxed_13_ = lean_unbox(v_i_11_);
v_j_boxed_14_ = lean_unbox(v_j_12_);
v_res_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra(v_v_10_, v_i_boxed_13_, v_j_boxed_14_);
return v_res_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___lam__0(lean_object* v___x_16_, uint8_t v___x_17_, uint8_t v___y_18_){
_start:
{
lean_object* v___x_19_; 
v___x_19_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(v___x_16_, v___x_17_, v___y_18_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___lam__0___boxed(lean_object* v___x_20_, lean_object* v___x_21_, lean_object* v___y_22_){
_start:
{
uint8_t v___x_24__boxed_23_; uint8_t v___y_25__boxed_24_; lean_object* v_res_25_; 
v___x_24__boxed_23_ = lean_unbox(v___x_21_);
v___y_25__boxed_24_ = lean_unbox(v___y_22_);
v_res_25_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___lam__0(v___x_20_, v___x_24__boxed_23_, v___y_25__boxed_24_);
lean_dec_ref(v___x_20_);
return v_res_25_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___closed__0(void){
_start:
{
uint8_t v___x_26_; lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___f_29_; 
v___x_26_ = 0;
v___x_27_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
v___x_28_ = lean_box(v___x_26_);
v___f_29_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___lam__0___boxed), 3, 2);
lean_closure_set(v___f_29_, 0, v___x_27_);
lean_closure_set(v___f_29_, 1, v___x_28_);
return v___f_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00(uint8_t v_a_30_, uint8_t v_a_31_){
_start:
{
lean_object* v___f_32_; lean_object* v___x_33_; 
v___f_32_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___closed__0);
v___x_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra(v___f_32_, v_a_30_, v_a_31_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00___boxed(lean_object* v_a_34_, lean_object* v_a_35_){
_start:
{
uint8_t v_a_40__boxed_36_; uint8_t v_a_41__boxed_37_; lean_object* v_res_38_; 
v_a_40__boxed_36_ = lean_unbox(v_a_34_);
v_a_41__boxed_37_ = lean_unbox(v_a_35_);
v_res_38_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_e00(v_a_40__boxed_36_, v_a_41__boxed_37_);
return v_res_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_bellAmp(lean_object* v_p_39_){
_start:
{
lean_object* v_fst_40_; uint8_t v___x_41_; 
v_fst_40_ = lean_ctor_get(v_p_39_, 0);
v___x_41_ = lean_unbox(v_fst_40_);
if (v___x_41_ == 0)
{
lean_object* v_snd_42_; uint8_t v___x_43_; 
v_snd_42_ = lean_ctor_get(v_p_39_, 1);
v___x_43_ = lean_unbox(v_snd_42_);
if (v___x_43_ == 0)
{
lean_object* v___x_44_; 
v___x_44_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_44_;
}
else
{
lean_object* v___x_45_; 
v___x_45_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_45_;
}
}
else
{
lean_object* v_snd_46_; uint8_t v___x_47_; 
v_snd_46_ = lean_ctor_get(v_p_39_, 1);
v___x_47_ = lean_unbox(v_snd_46_);
if (v___x_47_ == 0)
{
lean_object* v___x_48_; 
v___x_48_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_48_;
}
else
{
lean_object* v___x_49_; 
v___x_49_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_49_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_bellAmp___boxed(lean_object* v_p_50_){
_start:
{
lean_object* v_res_51_; 
v_res_51_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_bellAmp(v_p_50_);
lean_dec_ref(v_p_50_);
return v_res_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ketbra4(lean_object* v_w_52_, lean_object* v_p_53_, lean_object* v_q_54_){
_start:
{
lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; 
lean_inc_ref(v_w_52_);
v___x_55_ = lean_apply_1(v_w_52_, v_p_53_);
v___x_56_ = lean_apply_1(v_w_52_, v_q_54_);
v___x_57_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(v___x_56_);
v___x_58_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(v___x_55_, v___x_57_);
lean_dec_ref(v___x_55_);
return v___x_58_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ptrSecond(lean_object* v_A_59_, uint8_t v_i_60_, uint8_t v_j_61_){
_start:
{
uint8_t v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; uint8_t v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; lean_object* v___x_74_; lean_object* v___x_75_; lean_object* v___x_76_; lean_object* v___x_77_; lean_object* v___x_78_; 
v___x_62_ = 0;
v___x_63_ = lean_box(v_i_60_);
v___x_64_ = lean_box(v___x_62_);
v___x_65_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_65_, 0, v___x_63_);
lean_ctor_set(v___x_65_, 1, v___x_64_);
v___x_66_ = lean_box(v_j_61_);
v___x_67_ = lean_box(v___x_62_);
v___x_68_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_68_, 0, v___x_66_);
lean_ctor_set(v___x_68_, 1, v___x_67_);
lean_inc_ref(v_A_59_);
v___x_69_ = lean_apply_2(v_A_59_, v___x_65_, v___x_68_);
v___x_70_ = 1;
v___x_71_ = lean_box(v_i_60_);
v___x_72_ = lean_box(v___x_70_);
v___x_73_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_73_, 0, v___x_71_);
lean_ctor_set(v___x_73_, 1, v___x_72_);
v___x_74_ = lean_box(v_j_61_);
v___x_75_ = lean_box(v___x_70_);
v___x_76_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_76_, 0, v___x_74_);
lean_ctor_set(v___x_76_, 1, v___x_75_);
v___x_77_ = lean_apply_2(v_A_59_, v___x_73_, v___x_76_);
v___x_78_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(v___x_69_, v___x_77_);
lean_dec_ref(v___x_69_);
return v___x_78_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ptrSecond___boxed(lean_object* v_A_79_, lean_object* v_i_80_, lean_object* v_j_81_){
_start:
{
uint8_t v_i_boxed_82_; uint8_t v_j_boxed_83_; lean_object* v_res_84_; 
v_i_boxed_82_ = lean_unbox(v_i_80_);
v_j_boxed_83_ = lean_unbox(v_j_81_);
v_res_84_ = lp_FiniteQuantum_FableHilbertWalk20260819_H018Density_ptrSecond(v_A_79_, v_i_boxed_82_, v_j_boxed_83_);
return v_res_84_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H017MatrixFiniteRecovery(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H018Density(uint8_t builtin) {
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
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
