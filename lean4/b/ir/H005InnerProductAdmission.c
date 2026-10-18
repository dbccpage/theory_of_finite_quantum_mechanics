// Lean compiler output
// Module: H005InnerProductAdmission
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization
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
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H005_sesq_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H005_sesq_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramStd(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H005_oneOneF2(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_oneOneF2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H005_sesq_spec__0___redArg(lean_object* v_P_1_, lean_object* v_u_2_, lean_object* v_v_3_, lean_object* v_a_4_, lean_object* v_a_5_){
_start:
{
if (lean_obj_tag(v_a_4_) == 0)
{
lean_object* v___x_6_; 
lean_dec(v_v_3_);
lean_dec(v_u_2_);
lean_dec_ref(v_P_1_);
v___x_6_ = l_List_reverse___redArg(v_a_5_);
return v___x_6_;
}
else
{
lean_object* v_head_7_; lean_object* v_tail_8_; lean_object* v___x_10_; uint8_t v_isShared_11_; uint8_t v_isSharedCheck_22_; 
v_head_7_ = lean_ctor_get(v_a_4_, 0);
v_tail_8_ = lean_ctor_get(v_a_4_, 1);
v_isSharedCheck_22_ = !lean_is_exclusive(v_a_4_);
if (v_isSharedCheck_22_ == 0)
{
v___x_10_ = v_a_4_;
v_isShared_11_ = v_isSharedCheck_22_;
goto v_resetjp_9_;
}
else
{
lean_inc(v_tail_8_);
lean_inc(v_head_7_);
lean_dec(v_a_4_);
v___x_10_ = lean_box(0);
v_isShared_11_ = v_isSharedCheck_22_;
goto v_resetjp_9_;
}
v_resetjp_9_:
{
lean_object* v_mul_12_; lean_object* v_conj_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_19_; 
v_mul_12_ = lean_ctor_get(v_P_1_, 1);
v_conj_13_ = lean_ctor_get(v_P_1_, 5);
lean_inc(v_u_2_);
lean_inc(v_head_7_);
v___x_14_ = lean_apply_1(v_u_2_, v_head_7_);
lean_inc(v_conj_13_);
v___x_15_ = lean_apply_1(v_conj_13_, v___x_14_);
lean_inc(v_v_3_);
v___x_16_ = lean_apply_1(v_v_3_, v_head_7_);
lean_inc(v_mul_12_);
v___x_17_ = lean_apply_2(v_mul_12_, v___x_15_, v___x_16_);
if (v_isShared_11_ == 0)
{
lean_ctor_set(v___x_10_, 1, v_a_5_);
lean_ctor_set(v___x_10_, 0, v___x_17_);
v___x_19_ = v___x_10_;
goto v_reusejp_18_;
}
else
{
lean_object* v_reuseFailAlloc_21_; 
v_reuseFailAlloc_21_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_21_, 0, v___x_17_);
lean_ctor_set(v_reuseFailAlloc_21_, 1, v_a_5_);
v___x_19_ = v_reuseFailAlloc_21_;
goto v_reusejp_18_;
}
v_reusejp_18_:
{
v_a_4_ = v_tail_8_;
v_a_5_ = v___x_19_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq___redArg(lean_object* v_P_23_, lean_object* v_E_24_, lean_object* v_u_25_, lean_object* v_v_26_){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; 
v___x_27_ = lean_box(0);
lean_inc_ref(v_P_23_);
v___x_28_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H005_sesq_spec__0___redArg(v_P_23_, v_u_25_, v_v_26_, v_E_24_, v___x_27_);
v___x_29_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_23_, v___x_28_);
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq(lean_object* v_K_30_, lean_object* v_Q_31_, lean_object* v_P_32_, lean_object* v_E_33_, lean_object* v_u_34_, lean_object* v_v_35_){
_start:
{
lean_object* v___x_36_; 
v___x_36_ = lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq___redArg(v_P_32_, v_E_33_, v_u_34_, v_v_35_);
return v___x_36_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H005_sesq_spec__0(lean_object* v_Q_37_, lean_object* v_K_38_, lean_object* v_P_39_, lean_object* v_u_40_, lean_object* v_v_41_, lean_object* v_a_42_, lean_object* v_a_43_){
_start:
{
lean_object* v___x_44_; 
v___x_44_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H005_sesq_spec__0___redArg(v_P_39_, v_u_40_, v_v_41_, v_a_42_, v_a_43_);
return v___x_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramStd(lean_object* v_u_45_, lean_object* v_v_46_){
_start:
{
lean_object* v___x_47_; lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_47_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
v___x_48_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
v___x_49_ = lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq___redArg(v___x_47_, v___x_48_, v_u_45_, v_v_46_);
return v___x_49_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted___closed__0(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_50_ = lean_unsigned_to_nat(2u);
v___x_51_ = lean_nat_to_int(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted(lean_object* v_u_52_, lean_object* v_v_53_){
_start:
{
uint8_t v___x_54_; lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; uint8_t v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; 
v___x_54_ = 0;
v___x_55_ = lean_box(v___x_54_);
lean_inc_ref(v_u_52_);
v___x_56_ = lean_apply_1(v_u_52_, v___x_55_);
v___x_57_ = lean_box(v___x_54_);
lean_inc_ref(v_v_53_);
v___x_58_ = lean_apply_1(v_v_53_, v___x_57_);
v___x_59_ = lean_int_mul(v___x_56_, v___x_58_);
lean_dec(v___x_58_);
lean_dec(v___x_56_);
v___x_60_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H005_gramWeighted___closed__0);
v___x_61_ = 1;
v___x_62_ = lean_box(v___x_61_);
v___x_63_ = lean_apply_1(v_u_52_, v___x_62_);
v___x_64_ = lean_box(v___x_61_);
v___x_65_ = lean_apply_1(v_v_53_, v___x_64_);
v___x_66_ = lean_int_mul(v___x_63_, v___x_65_);
lean_dec(v___x_65_);
lean_dec(v___x_63_);
v___x_67_ = lean_int_mul(v___x_60_, v___x_66_);
lean_dec(v___x_66_);
v___x_68_ = lean_int_add(v___x_59_, v___x_67_);
lean_dec(v___x_67_);
lean_dec(v___x_59_);
return v___x_68_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H005_oneOneF2(uint8_t v_x_69_){
_start:
{
uint8_t v___x_70_; 
v___x_70_ = 1;
return v___x_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_oneOneF2___boxed(lean_object* v_x_71_){
_start:
{
uint8_t v_x_4__boxed_72_; uint8_t v_res_73_; lean_object* v_r_74_; 
v_x_4__boxed_72_ = lean_unbox(v_x_71_);
v_res_73_ = lp_FiniteQuantum_FableHilbertWalk20260819_H005_oneOneF2(v_x_4__boxed_72_);
v_r_74_ = lean_box(v_res_73_);
return v_r_74_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin) {
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
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
