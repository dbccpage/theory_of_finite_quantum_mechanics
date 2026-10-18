// Lean compiler output
// Module: PrimitiveDifferenceBridge
// Imports: public import Init public meta import Init public import PrimitiveDifference
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
lean_object* l_List_reverse___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaCore_FablePrimitiveDifferenceBridge_profile_spec__0___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaCore_FablePrimitiveDifferenceBridge_profile_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaCore_FablePrimitiveDifferenceBridge_profile_spec__0___redArg(lean_object* v_x_1_, lean_object* v_a_2_, lean_object* v_a_3_){
_start:
{
if (lean_obj_tag(v_a_2_) == 0)
{
lean_object* v___x_4_; 
lean_dec(v_x_1_);
v___x_4_ = l_List_reverse___redArg(v_a_3_);
return v___x_4_;
}
else
{
lean_object* v_head_5_; lean_object* v_tail_6_; lean_object* v___x_8_; uint8_t v_isShared_9_; uint8_t v_isSharedCheck_15_; 
v_head_5_ = lean_ctor_get(v_a_2_, 0);
v_tail_6_ = lean_ctor_get(v_a_2_, 1);
v_isSharedCheck_15_ = !lean_is_exclusive(v_a_2_);
if (v_isSharedCheck_15_ == 0)
{
v___x_8_ = v_a_2_;
v_isShared_9_ = v_isSharedCheck_15_;
goto v_resetjp_7_;
}
else
{
lean_inc(v_tail_6_);
lean_inc(v_head_5_);
lean_dec(v_a_2_);
v___x_8_ = lean_box(0);
v_isShared_9_ = v_isSharedCheck_15_;
goto v_resetjp_7_;
}
v_resetjp_7_:
{
lean_object* v___x_10_; lean_object* v___x_12_; 
lean_inc(v_x_1_);
v___x_10_ = lean_apply_1(v_head_5_, v_x_1_);
if (v_isShared_9_ == 0)
{
lean_ctor_set(v___x_8_, 1, v_a_3_);
lean_ctor_set(v___x_8_, 0, v___x_10_);
v___x_12_ = v___x_8_;
goto v_reusejp_11_;
}
else
{
lean_object* v_reuseFailAlloc_14_; 
v_reuseFailAlloc_14_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_14_, 0, v___x_10_);
lean_ctor_set(v_reuseFailAlloc_14_, 1, v_a_3_);
v___x_12_ = v_reuseFailAlloc_14_;
goto v_reusejp_11_;
}
v_reusejp_11_:
{
v_a_2_ = v_tail_6_;
v_a_3_ = v___x_12_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile___redArg(lean_object* v_questions_16_, lean_object* v_x_17_){
_start:
{
lean_object* v___x_18_; lean_object* v___x_19_; 
v___x_18_ = lean_box(0);
v___x_19_ = lp_FiniteQuantum_List_mapTR_loop___at___00OmegaCore_FablePrimitiveDifferenceBridge_profile_spec__0___redArg(v_x_17_, v_questions_16_, v___x_18_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile(lean_object* v_00_u03b1_20_, lean_object* v_00_u03b3_21_, lean_object* v_questions_22_, lean_object* v_x_23_){
_start:
{
lean_object* v___x_24_; 
v___x_24_ = lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile___redArg(v_questions_22_, v_x_23_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaCore_FablePrimitiveDifferenceBridge_profile_spec__0(lean_object* v_00_u03b1_25_, lean_object* v_00_u03b3_26_, lean_object* v_x_27_, lean_object* v_a_28_, lean_object* v_a_29_){
_start:
{
lean_object* v___x_30_; 
v___x_30_ = lp_FiniteQuantum_List_mapTR_loop___at___00OmegaCore_FablePrimitiveDifferenceBridge_profile_spec__0___redArg(v_x_27_, v_a_28_, v_a_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference___redArg___lam__0(lean_object* v_questions_31_, lean_object* v_x_32_, lean_object* v_y_33_){
_start:
{
lean_object* v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; 
lean_inc(v_questions_31_);
v___x_34_ = lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile___redArg(v_questions_31_, v_x_32_);
v___x_35_ = lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_profile___redArg(v_questions_31_, v_y_33_);
v___x_36_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_36_, 0, v___x_34_);
lean_ctor_set(v___x_36_, 1, v___x_35_);
return v___x_36_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference___redArg(lean_object* v_questions_37_){
_start:
{
lean_object* v___f_38_; 
v___f_38_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference___redArg___lam__0), 3, 1);
lean_closure_set(v___f_38_, 0, v_questions_37_);
return v___f_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference(lean_object* v_00_u03b1_39_, lean_object* v_00_u03b3_40_, lean_object* v_questions_41_){
_start:
{
lean_object* v___f_42_; 
v___f_42_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_presentationDifference___redArg___lam__0), 3, 1);
lean_closure_set(v___f_42_, 0, v_questions_41_);
return v___f_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___redArg(lean_object* v_a_43_){
_start:
{
lean_inc(v_a_43_);
return v_a_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___redArg___boxed(lean_object* v_a_44_){
_start:
{
lean_object* v_res_45_; 
v_res_45_ = lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___redArg(v_a_44_);
lean_dec(v_a_44_);
return v_res_45_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0(lean_object* v_00_u03b1_46_, lean_object* v_hST_47_, lean_object* v_a_48_){
_start:
{
lean_inc(v_a_48_);
return v_a_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0___boxed(lean_object* v_00_u03b1_49_, lean_object* v_hST_50_, lean_object* v_a_51_){
_start:
{
lean_object* v_res_52_; 
v_res_52_ = lp_FiniteQuantum_OmegaCore_PrimitiveDifference_quotientMapOfSetoidImp___at___00OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap_spec__0(v_00_u03b1_49_, v_hST_50_, v_a_51_);
lean_dec(v_a_51_);
return v_res_52_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___redArg(lean_object* v_a_53_){
_start:
{
lean_inc(v_a_53_);
return v_a_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___redArg___boxed(lean_object* v_a_54_){
_start:
{
lean_object* v_res_55_; 
v_res_55_ = lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___redArg(v_a_54_);
lean_dec(v_a_54_);
return v_res_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap(lean_object* v_00_u03b1_56_, lean_object* v_00_u03b3_57_, lean_object* v_oldQuestions_58_, lean_object* v_newQuestions_59_, lean_object* v_hrefines_60_, lean_object* v_a_61_){
_start:
{
lean_inc(v_a_61_);
return v_a_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap___boxed(lean_object* v_00_u03b1_62_, lean_object* v_00_u03b3_63_, lean_object* v_oldQuestions_64_, lean_object* v_newQuestions_65_, lean_object* v_hrefines_66_, lean_object* v_a_67_){
_start:
{
lean_object* v_res_68_; 
v_res_68_ = lp_FiniteQuantum_OmegaCore_FablePrimitiveDifferenceBridge_residualRefinementMap(v_00_u03b1_62_, v_00_u03b3_63_, v_oldQuestions_64_, v_newQuestions_65_, v_hrefines_66_, v_a_67_);
lean_dec(v_a_67_);
lean_dec(v_newQuestions_65_);
lean_dec(v_oldQuestions_64_);
return v_res_68_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveDifference(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PrimitiveDifferenceBridge(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveDifference(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
