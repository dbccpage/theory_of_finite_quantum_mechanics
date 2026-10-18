// Lean compiler output
// Module: SolverFrontier
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
lean_object* l_List_reverse___redArg(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00OmegaCore_SolverFrontier_selectFrontier_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_selectFrontier___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_selectFrontier(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00OmegaCore_SolverFrontier_selectFrontier_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg(lean_object* v_candidate_1_, lean_object* v_strictlyBetter_2_, lean_object* v_x_3_){
_start:
{
if (lean_obj_tag(v_x_3_) == 0)
{
uint8_t v___x_4_; 
lean_dec_ref(v_strictlyBetter_2_);
lean_dec_ref(v_candidate_1_);
v___x_4_ = 0;
return v___x_4_;
}
else
{
lean_object* v_head_5_; uint8_t v_verified_6_; 
v_head_5_ = lean_ctor_get(v_x_3_, 0);
v_verified_6_ = lean_ctor_get_uint8(v_head_5_, sizeof(void*)*2);
if (v_verified_6_ == 0)
{
lean_object* v_tail_7_; 
v_tail_7_ = lean_ctor_get(v_x_3_, 1);
lean_inc(v_tail_7_);
lean_dec_ref_known(v_x_3_, 2);
v_x_3_ = v_tail_7_;
goto _start;
}
else
{
lean_object* v_tail_9_; lean_object* v_cost_10_; lean_object* v_cost_11_; lean_object* v___x_12_; uint8_t v___x_13_; 
lean_inc(v_head_5_);
v_tail_9_ = lean_ctor_get(v_x_3_, 1);
lean_inc(v_tail_9_);
lean_dec_ref_known(v_x_3_, 2);
v_cost_10_ = lean_ctor_get(v_head_5_, 1);
lean_inc(v_cost_10_);
lean_dec(v_head_5_);
v_cost_11_ = lean_ctor_get(v_candidate_1_, 1);
lean_inc_ref(v_strictlyBetter_2_);
lean_inc(v_cost_11_);
v___x_12_ = lean_apply_2(v_strictlyBetter_2_, v_cost_10_, v_cost_11_);
v___x_13_ = lean_unbox(v___x_12_);
if (v___x_13_ == 0)
{
v_x_3_ = v_tail_9_;
goto _start;
}
else
{
uint8_t v___x_15_; 
lean_dec(v_tail_9_);
lean_dec_ref(v_strictlyBetter_2_);
lean_dec_ref(v_candidate_1_);
v___x_15_ = lean_unbox(v___x_12_);
return v___x_15_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg___boxed(lean_object* v_candidate_16_, lean_object* v_strictlyBetter_17_, lean_object* v_x_18_){
_start:
{
uint8_t v_res_19_; lean_object* v_r_20_; 
v_res_19_ = lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg(v_candidate_16_, v_strictlyBetter_17_, v_x_18_);
v_r_20_ = lean_box(v_res_19_);
return v_r_20_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg(lean_object* v_strictlyBetter_21_, lean_object* v_batch_22_, lean_object* v_candidate_23_){
_start:
{
uint8_t v_verified_24_; 
v_verified_24_ = lean_ctor_get_uint8(v_candidate_23_, sizeof(void*)*2);
if (v_verified_24_ == 0)
{
lean_dec_ref(v_candidate_23_);
lean_dec(v_batch_22_);
lean_dec_ref(v_strictlyBetter_21_);
return v_verified_24_;
}
else
{
uint8_t v___x_25_; 
v___x_25_ = lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg(v_candidate_23_, v_strictlyBetter_21_, v_batch_22_);
if (v___x_25_ == 0)
{
return v_verified_24_;
}
else
{
uint8_t v___x_26_; 
v___x_26_ = 0;
return v___x_26_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg___boxed(lean_object* v_strictlyBetter_27_, lean_object* v_batch_28_, lean_object* v_candidate_29_){
_start:
{
uint8_t v_res_30_; lean_object* v_r_31_; 
v_res_30_ = lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg(v_strictlyBetter_27_, v_batch_28_, v_candidate_29_);
v_r_31_ = lean_box(v_res_30_);
return v_r_31_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier(lean_object* v_Plan_32_, lean_object* v_Cost_33_, lean_object* v_strictlyBetter_34_, lean_object* v_batch_35_, lean_object* v_candidate_36_){
_start:
{
uint8_t v___x_37_; 
v___x_37_ = lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg(v_strictlyBetter_34_, v_batch_35_, v_candidate_36_);
return v___x_37_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___boxed(lean_object* v_Plan_38_, lean_object* v_Cost_39_, lean_object* v_strictlyBetter_40_, lean_object* v_batch_41_, lean_object* v_candidate_42_){
_start:
{
uint8_t v_res_43_; lean_object* v_r_44_; 
v_res_43_ = lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier(v_Plan_38_, v_Cost_39_, v_strictlyBetter_40_, v_batch_41_, v_candidate_42_);
v_r_44_ = lean_box(v_res_43_);
return v_r_44_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0(lean_object* v_Plan_45_, lean_object* v_Cost_46_, lean_object* v_candidate_47_, lean_object* v_strictlyBetter_48_, lean_object* v_x_49_){
_start:
{
uint8_t v___x_50_; 
v___x_50_ = lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___redArg(v_candidate_47_, v_strictlyBetter_48_, v_x_49_);
return v___x_50_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0___boxed(lean_object* v_Plan_51_, lean_object* v_Cost_52_, lean_object* v_candidate_53_, lean_object* v_strictlyBetter_54_, lean_object* v_x_55_){
_start:
{
uint8_t v_res_56_; lean_object* v_r_57_; 
v_res_56_ = lp_FiniteQuantum_List_any___at___00OmegaCore_SolverFrontier_onFrontier_spec__0(v_Plan_51_, v_Cost_52_, v_candidate_53_, v_strictlyBetter_54_, v_x_55_);
v_r_57_ = lean_box(v_res_56_);
return v_r_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00OmegaCore_SolverFrontier_selectFrontier_spec__0___redArg(lean_object* v_strictlyBetter_58_, lean_object* v_batch_59_, lean_object* v_a_60_, lean_object* v_a_61_){
_start:
{
if (lean_obj_tag(v_a_60_) == 0)
{
lean_object* v___x_62_; 
lean_dec(v_batch_59_);
lean_dec_ref(v_strictlyBetter_58_);
v___x_62_ = l_List_reverse___redArg(v_a_61_);
return v___x_62_;
}
else
{
lean_object* v_head_63_; lean_object* v_tail_64_; lean_object* v___x_66_; uint8_t v_isShared_67_; uint8_t v_isSharedCheck_74_; 
v_head_63_ = lean_ctor_get(v_a_60_, 0);
v_tail_64_ = lean_ctor_get(v_a_60_, 1);
v_isSharedCheck_74_ = !lean_is_exclusive(v_a_60_);
if (v_isSharedCheck_74_ == 0)
{
v___x_66_ = v_a_60_;
v_isShared_67_ = v_isSharedCheck_74_;
goto v_resetjp_65_;
}
else
{
lean_inc(v_tail_64_);
lean_inc(v_head_63_);
lean_dec(v_a_60_);
v___x_66_ = lean_box(0);
v_isShared_67_ = v_isSharedCheck_74_;
goto v_resetjp_65_;
}
v_resetjp_65_:
{
uint8_t v___x_68_; 
lean_inc(v_head_63_);
lean_inc(v_batch_59_);
lean_inc_ref(v_strictlyBetter_58_);
v___x_68_ = lp_FiniteQuantum_OmegaCore_SolverFrontier_onFrontier___redArg(v_strictlyBetter_58_, v_batch_59_, v_head_63_);
if (v___x_68_ == 0)
{
lean_del_object(v___x_66_);
lean_dec(v_head_63_);
v_a_60_ = v_tail_64_;
goto _start;
}
else
{
lean_object* v___x_71_; 
if (v_isShared_67_ == 0)
{
lean_ctor_set(v___x_66_, 1, v_a_61_);
v___x_71_ = v___x_66_;
goto v_reusejp_70_;
}
else
{
lean_object* v_reuseFailAlloc_73_; 
v_reuseFailAlloc_73_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_73_, 0, v_head_63_);
lean_ctor_set(v_reuseFailAlloc_73_, 1, v_a_61_);
v___x_71_ = v_reuseFailAlloc_73_;
goto v_reusejp_70_;
}
v_reusejp_70_:
{
v_a_60_ = v_tail_64_;
v_a_61_ = v___x_71_;
goto _start;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_selectFrontier___redArg(lean_object* v_strictlyBetter_75_, lean_object* v_batch_76_){
_start:
{
lean_object* v___x_77_; lean_object* v___x_78_; 
v___x_77_ = lean_box(0);
lean_inc(v_batch_76_);
v___x_78_ = lp_FiniteQuantum_List_filterTR_loop___at___00OmegaCore_SolverFrontier_selectFrontier_spec__0___redArg(v_strictlyBetter_75_, v_batch_76_, v_batch_76_, v___x_77_);
return v___x_78_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_SolverFrontier_selectFrontier(lean_object* v_Plan_79_, lean_object* v_Cost_80_, lean_object* v_strictlyBetter_81_, lean_object* v_batch_82_){
_start:
{
lean_object* v___x_83_; 
v___x_83_ = lp_FiniteQuantum_OmegaCore_SolverFrontier_selectFrontier___redArg(v_strictlyBetter_81_, v_batch_82_);
return v___x_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00OmegaCore_SolverFrontier_selectFrontier_spec__0(lean_object* v_Plan_84_, lean_object* v_Cost_85_, lean_object* v_strictlyBetter_86_, lean_object* v_batch_87_, lean_object* v_a_88_, lean_object* v_a_89_){
_start:
{
lean_object* v___x_90_; 
v___x_90_ = lp_FiniteQuantum_List_filterTR_loop___at___00OmegaCore_SolverFrontier_selectFrontier_spec__0___redArg(v_strictlyBetter_86_, v_batch_87_, v_a_88_, v_a_89_);
return v___x_90_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_SolverFrontier(uint8_t builtin) {
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
