// Lean compiler output
// Module: NoSignallingCore
// Imports: public import Init public meta import Init
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
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_sumList(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_sumList___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_NoSignallingCore_0__NoSignallingCore_sumList_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_NoSignallingCore_0__NoSignallingCore_sumList_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00NoSignallingCore_marginalA_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_marginalA___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_marginalA(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00NoSignallingCore_marginalA_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig___redArg(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig___redArg___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig(lean_object*, uint8_t, uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_sumList(lean_object* v_x_1_){
_start:
{
if (lean_obj_tag(v_x_1_) == 0)
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
else
{
lean_object* v_head_3_; lean_object* v_tail_4_; lean_object* v___x_5_; lean_object* v___x_6_; 
v_head_3_ = lean_ctor_get(v_x_1_, 0);
v_tail_4_ = lean_ctor_get(v_x_1_, 1);
v___x_5_ = lp_FiniteQuantum_NoSignallingCore_sumList(v_tail_4_);
v___x_6_ = lean_nat_add(v_head_3_, v___x_5_);
lean_dec(v___x_5_);
return v___x_6_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_sumList___boxed(lean_object* v_x_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_FiniteQuantum_NoSignallingCore_sumList(v_x_7_);
lean_dec(v_x_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_NoSignallingCore_0__NoSignallingCore_sumList_match__1_splitter___redArg(lean_object* v_x_9_, lean_object* v_h__1_10_, lean_object* v_h__2_11_){
_start:
{
if (lean_obj_tag(v_x_9_) == 0)
{
lean_object* v___x_12_; lean_object* v___x_13_; 
lean_dec(v_h__2_11_);
v___x_12_ = lean_box(0);
v___x_13_ = lean_apply_1(v_h__1_10_, v___x_12_);
return v___x_13_;
}
else
{
lean_object* v_head_14_; lean_object* v_tail_15_; lean_object* v___x_16_; 
lean_dec(v_h__1_10_);
v_head_14_ = lean_ctor_get(v_x_9_, 0);
lean_inc(v_head_14_);
v_tail_15_ = lean_ctor_get(v_x_9_, 1);
lean_inc(v_tail_15_);
lean_dec_ref_known(v_x_9_, 2);
v___x_16_ = lean_apply_2(v_h__2_11_, v_head_14_, v_tail_15_);
return v___x_16_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_NoSignallingCore_0__NoSignallingCore_sumList_match__1_splitter(lean_object* v_motive_17_, lean_object* v_x_18_, lean_object* v_h__1_19_, lean_object* v_h__2_20_){
_start:
{
if (lean_obj_tag(v_x_18_) == 0)
{
lean_object* v___x_21_; lean_object* v___x_22_; 
lean_dec(v_h__2_20_);
v___x_21_ = lean_box(0);
v___x_22_ = lean_apply_1(v_h__1_19_, v___x_21_);
return v___x_22_;
}
else
{
lean_object* v_head_23_; lean_object* v_tail_24_; lean_object* v___x_25_; 
lean_dec(v_h__1_19_);
v_head_23_ = lean_ctor_get(v_x_18_, 0);
lean_inc(v_head_23_);
v_tail_24_ = lean_ctor_get(v_x_18_, 1);
lean_inc(v_tail_24_);
lean_dec_ref_known(v_x_18_, 2);
v___x_25_ = lean_apply_2(v_h__2_20_, v_head_23_, v_tail_24_);
return v___x_25_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00NoSignallingCore_marginalA_spec__0___redArg(lean_object* v_P_26_, lean_object* v_x_27_, lean_object* v_y_28_, lean_object* v_a_29_, lean_object* v_a_30_, lean_object* v_a_31_){
_start:
{
if (lean_obj_tag(v_a_30_) == 0)
{
lean_object* v___x_32_; 
lean_dec(v_a_29_);
lean_dec(v_y_28_);
lean_dec(v_x_27_);
lean_dec_ref(v_P_26_);
v___x_32_ = l_List_reverse___redArg(v_a_31_);
return v___x_32_;
}
else
{
lean_object* v_head_33_; lean_object* v_tail_34_; lean_object* v___x_36_; uint8_t v_isShared_37_; uint8_t v_isSharedCheck_43_; 
v_head_33_ = lean_ctor_get(v_a_30_, 0);
v_tail_34_ = lean_ctor_get(v_a_30_, 1);
v_isSharedCheck_43_ = !lean_is_exclusive(v_a_30_);
if (v_isSharedCheck_43_ == 0)
{
v___x_36_ = v_a_30_;
v_isShared_37_ = v_isSharedCheck_43_;
goto v_resetjp_35_;
}
else
{
lean_inc(v_tail_34_);
lean_inc(v_head_33_);
lean_dec(v_a_30_);
v___x_36_ = lean_box(0);
v_isShared_37_ = v_isSharedCheck_43_;
goto v_resetjp_35_;
}
v_resetjp_35_:
{
lean_object* v___x_38_; lean_object* v___x_40_; 
lean_inc_ref(v_P_26_);
lean_inc(v_a_29_);
lean_inc(v_y_28_);
lean_inc(v_x_27_);
v___x_38_ = lean_apply_4(v_P_26_, v_x_27_, v_y_28_, v_a_29_, v_head_33_);
if (v_isShared_37_ == 0)
{
lean_ctor_set(v___x_36_, 1, v_a_31_);
lean_ctor_set(v___x_36_, 0, v___x_38_);
v___x_40_ = v___x_36_;
goto v_reusejp_39_;
}
else
{
lean_object* v_reuseFailAlloc_42_; 
v_reuseFailAlloc_42_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_42_, 0, v___x_38_);
lean_ctor_set(v_reuseFailAlloc_42_, 1, v_a_31_);
v___x_40_ = v_reuseFailAlloc_42_;
goto v_reusejp_39_;
}
v_reusejp_39_:
{
v_a_30_ = v_tail_34_;
v_a_31_ = v___x_40_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_marginalA___redArg(lean_object* v_P_44_, lean_object* v_outcomesB_45_, lean_object* v_x_46_, lean_object* v_y_47_, lean_object* v_a_48_){
_start:
{
lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_49_ = lean_box(0);
v___x_50_ = lp_FiniteQuantum_List_mapTR_loop___at___00NoSignallingCore_marginalA_spec__0___redArg(v_P_44_, v_x_46_, v_y_47_, v_a_48_, v_outcomesB_45_, v___x_49_);
v___x_51_ = lp_FiniteQuantum_NoSignallingCore_sumList(v___x_50_);
lean_dec(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_marginalA(lean_object* v_X_52_, lean_object* v_Y_53_, lean_object* v_A_54_, lean_object* v_B_55_, lean_object* v_P_56_, lean_object* v_outcomesB_57_, lean_object* v_x_58_, lean_object* v_y_59_, lean_object* v_a_60_){
_start:
{
lean_object* v___x_61_; 
v___x_61_ = lp_FiniteQuantum_NoSignallingCore_marginalA___redArg(v_P_56_, v_outcomesB_57_, v_x_58_, v_y_59_, v_a_60_);
return v___x_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00NoSignallingCore_marginalA_spec__0(lean_object* v_B_62_, lean_object* v_X_63_, lean_object* v_Y_64_, lean_object* v_A_65_, lean_object* v_P_66_, lean_object* v_x_67_, lean_object* v_y_68_, lean_object* v_a_69_, lean_object* v_a_70_, lean_object* v_a_71_){
_start:
{
lean_object* v___x_72_; 
v___x_72_ = lp_FiniteQuantum_List_mapTR_loop___at___00NoSignallingCore_marginalA_spec__0___redArg(v_P_66_, v_x_67_, v_y_68_, v_a_69_, v_a_70_, v_a_71_);
return v___x_72_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig___redArg(uint8_t v_y_73_, uint8_t v_a_74_){
_start:
{
if (v_a_74_ == 0)
{
if (v_y_73_ == 0)
{
lean_object* v___x_75_; 
v___x_75_ = lean_unsigned_to_nat(1u);
return v___x_75_;
}
else
{
lean_object* v___x_76_; 
v___x_76_ = lean_unsigned_to_nat(0u);
return v___x_76_;
}
}
else
{
if (v_y_73_ == 0)
{
lean_object* v___x_77_; 
v___x_77_ = lean_unsigned_to_nat(0u);
return v___x_77_;
}
else
{
lean_object* v___x_78_; 
v___x_78_ = lean_unsigned_to_nat(1u);
return v___x_78_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig___redArg___boxed(lean_object* v_y_79_, lean_object* v_a_80_){
_start:
{
uint8_t v_y_boxed_81_; uint8_t v_a_boxed_82_; lean_object* v_res_83_; 
v_y_boxed_81_ = lean_unbox(v_y_79_);
v_a_boxed_82_ = lean_unbox(v_a_80_);
v_res_83_ = lp_FiniteQuantum_NoSignallingCore_Witness_sig___redArg(v_y_boxed_81_, v_a_boxed_82_);
return v_res_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig(lean_object* v___x_84_, uint8_t v_y_85_, uint8_t v_a_86_, lean_object* v___b_87_){
_start:
{
lean_object* v___x_88_; 
v___x_88_ = lp_FiniteQuantum_NoSignallingCore_Witness_sig___redArg(v_y_85_, v_a_86_);
return v___x_88_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NoSignallingCore_Witness_sig___boxed(lean_object* v___x_89_, lean_object* v_y_90_, lean_object* v_a_91_, lean_object* v___b_92_){
_start:
{
uint8_t v_y_boxed_93_; uint8_t v_a_boxed_94_; lean_object* v_res_95_; 
v_y_boxed_93_ = lean_unbox(v_y_90_);
v_a_boxed_94_ = lean_unbox(v_a_91_);
v_res_95_ = lp_FiniteQuantum_NoSignallingCore_Witness_sig(v___x_89_, v_y_boxed_93_, v_a_boxed_94_, v___b_92_);
return v_res_95_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_NoSignallingCore(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
