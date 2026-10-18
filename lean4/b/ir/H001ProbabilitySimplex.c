// Lean compiler output
// Module: H001ProbabilitySimplex
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
lean_object* l_List_reverse___redArg(lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_mass_spec__0___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_mass___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_mass(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_mass_spec__0(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_l1dist_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_l1dist___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_l1dist(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_l1dist_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointMass___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointMass___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointMass___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointMass = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointMass___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_doubleW(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_doubleW___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_mass_spec__0___redArg(lean_object* v_w_1_, lean_object* v_a_2_, lean_object* v_a_3_){
_start:
{
if (lean_obj_tag(v_a_2_) == 0)
{
lean_object* v___x_4_; 
lean_dec_ref(v_w_1_);
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
lean_inc_ref(v_w_1_);
v___x_10_ = lean_apply_1(v_w_1_, v_head_5_);
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_mass___redArg(lean_object* v_E_16_, lean_object* v_w_17_){
_start:
{
lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___x_18_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
v___x_19_ = lean_box(0);
v___x_20_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_mass_spec__0___redArg(v_w_17_, v_E_16_, v___x_19_);
v___x_21_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v___x_18_, v___x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_mass(lean_object* v_Q_22_, lean_object* v_E_23_, lean_object* v_w_24_){
_start:
{
lean_object* v___x_25_; 
v___x_25_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_mass___redArg(v_E_23_, v_w_24_);
return v___x_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_mass_spec__0(lean_object* v_Q_26_, lean_object* v_w_27_, lean_object* v_a_28_, lean_object* v_a_29_){
_start:
{
lean_object* v___x_30_; 
v___x_30_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_mass_spec__0___redArg(v_w_27_, v_a_28_, v_a_29_);
return v___x_30_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0(void){
_start:
{
lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_31_ = lean_unsigned_to_nat(0u);
v___x_32_ = lean_nat_to_int(v___x_31_);
return v___x_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs(lean_object* v_a_33_){
_start:
{
lean_object* v___x_34_; uint8_t v___x_35_; 
v___x_34_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0);
v___x_35_ = lean_int_dec_lt(v_a_33_, v___x_34_);
if (v___x_35_ == 0)
{
lean_inc(v_a_33_);
return v_a_33_;
}
else
{
lean_object* v___x_36_; 
v___x_36_ = lean_int_neg(v_a_33_);
return v___x_36_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___boxed(lean_object* v_a_37_){
_start:
{
lean_object* v_res_38_; 
v_res_38_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs(v_a_37_);
lean_dec(v_a_37_);
return v_res_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_l1dist_spec__0___redArg(lean_object* v_v_39_, lean_object* v_w_40_, lean_object* v_a_41_, lean_object* v_a_42_){
_start:
{
if (lean_obj_tag(v_a_41_) == 0)
{
lean_object* v___x_43_; 
lean_dec_ref(v_w_40_);
lean_dec_ref(v_v_39_);
v___x_43_ = l_List_reverse___redArg(v_a_42_);
return v___x_43_;
}
else
{
lean_object* v_head_44_; lean_object* v_tail_45_; lean_object* v___x_47_; uint8_t v_isShared_48_; uint8_t v_isSharedCheck_57_; 
v_head_44_ = lean_ctor_get(v_a_41_, 0);
v_tail_45_ = lean_ctor_get(v_a_41_, 1);
v_isSharedCheck_57_ = !lean_is_exclusive(v_a_41_);
if (v_isSharedCheck_57_ == 0)
{
v___x_47_ = v_a_41_;
v_isShared_48_ = v_isSharedCheck_57_;
goto v_resetjp_46_;
}
else
{
lean_inc(v_tail_45_);
lean_inc(v_head_44_);
lean_dec(v_a_41_);
v___x_47_ = lean_box(0);
v_isShared_48_ = v_isSharedCheck_57_;
goto v_resetjp_46_;
}
v_resetjp_46_:
{
lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; lean_object* v___x_52_; lean_object* v___x_54_; 
lean_inc_ref(v_v_39_);
lean_inc(v_head_44_);
v___x_49_ = lean_apply_1(v_v_39_, v_head_44_);
lean_inc_ref(v_w_40_);
v___x_50_ = lean_apply_1(v_w_40_, v_head_44_);
v___x_51_ = lean_int_sub(v___x_49_, v___x_50_);
lean_dec(v___x_50_);
lean_dec(v___x_49_);
v___x_52_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs(v___x_51_);
lean_dec(v___x_51_);
if (v_isShared_48_ == 0)
{
lean_ctor_set(v___x_47_, 1, v_a_42_);
lean_ctor_set(v___x_47_, 0, v___x_52_);
v___x_54_ = v___x_47_;
goto v_reusejp_53_;
}
else
{
lean_object* v_reuseFailAlloc_56_; 
v_reuseFailAlloc_56_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_56_, 0, v___x_52_);
lean_ctor_set(v_reuseFailAlloc_56_, 1, v_a_42_);
v___x_54_ = v_reuseFailAlloc_56_;
goto v_reusejp_53_;
}
v_reusejp_53_:
{
v_a_41_ = v_tail_45_;
v_a_42_ = v___x_54_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_l1dist___redArg(lean_object* v_E_58_, lean_object* v_v_59_, lean_object* v_w_60_){
_start:
{
lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; 
v___x_61_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
v___x_62_ = lean_box(0);
v___x_63_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_l1dist_spec__0___redArg(v_v_59_, v_w_60_, v_E_58_, v___x_62_);
v___x_64_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v___x_61_, v___x_63_);
return v___x_64_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_l1dist(lean_object* v_Q_65_, lean_object* v_E_66_, lean_object* v_v_67_, lean_object* v_w_68_){
_start:
{
lean_object* v___x_69_; 
v___x_69_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_l1dist___redArg(v_E_66_, v_v_67_, v_w_68_);
return v___x_69_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_l1dist_spec__0(lean_object* v_Q_70_, lean_object* v_v_71_, lean_object* v_w_72_, lean_object* v_a_73_, lean_object* v_a_74_){
_start:
{
lean_object* v___x_75_; 
v___x_75_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H001_l1dist_spec__0___redArg(v_v_71_, v_w_72_, v_a_73_, v_a_74_);
return v___x_75_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0(void){
_start:
{
lean_object* v___x_76_; lean_object* v___x_77_; 
v___x_76_ = lean_unsigned_to_nat(1u);
v___x_77_ = lean_nat_to_int(v___x_76_);
return v___x_77_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW(uint8_t v_q_78_){
_start:
{
if (v_q_78_ == 0)
{
lean_object* v___x_79_; 
v___x_79_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0);
return v___x_79_;
}
else
{
lean_object* v___x_80_; 
v___x_80_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_iabs___closed__0);
return v___x_80_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___boxed(lean_object* v_q_81_){
_start:
{
uint8_t v_q_boxed_82_; lean_object* v_res_83_; 
v_q_boxed_82_ = lean_unbox(v_q_81_);
v_res_83_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW(v_q_boxed_82_);
return v_res_83_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__0(void){
_start:
{
lean_object* v___x_86_; lean_object* v___x_87_; 
v___x_86_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0);
v___x_87_ = lean_int_neg(v___x_86_);
return v___x_87_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__1(void){
_start:
{
lean_object* v___x_88_; lean_object* v___x_89_; 
v___x_88_ = lean_unsigned_to_nat(2u);
v___x_89_ = lean_nat_to_int(v___x_88_);
return v___x_89_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW(uint8_t v_q_90_){
_start:
{
if (v_q_90_ == 0)
{
lean_object* v___x_91_; 
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__0);
return v___x_91_;
}
else
{
lean_object* v___x_92_; 
v___x_92_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___closed__1);
return v___x_92_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW___boxed(lean_object* v_q_93_){
_start:
{
uint8_t v_q_boxed_94_; lean_object* v_res_95_; 
v_q_boxed_94_ = lean_unbox(v_q_93_);
v_res_95_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_signedW(v_q_boxed_94_);
return v_res_95_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_doubleW(uint8_t v_x_96_){
_start:
{
lean_object* v___x_97_; 
v___x_97_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001_pointW___closed__0);
return v___x_97_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001_doubleW___boxed(lean_object* v_x_98_){
_start:
{
uint8_t v_x_10__boxed_99_; lean_object* v_res_100_; 
v_x_10__boxed_99_ = lean_unbox(v_x_98_);
v_res_100_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001_doubleW(v_x_10__boxed_99_);
return v_res_100_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H001ProbabilitySimplex(uint8_t builtin) {
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
