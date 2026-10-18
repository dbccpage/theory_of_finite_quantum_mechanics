// Lean compiler output
// Module: BornRedundancy
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
lean_object* lean_nat_to_int(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* l_Rat_mul(lean_object*, lean_object*);
lean_object* l_Nat_cast___at___00Dyadic_toRat_spec__0(lean_object*);
lean_object* l_Rat_add(lean_object*, lean_object*);
lean_object* l_Rat_inv(lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BornRedundancy_listSum___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BornRedundancy_listSum___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_listSum(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_smul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_smul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_BornRedundancy_0__BornRedundancy_listSum_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_BornRedundancy_0__BornRedundancy_listSum_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_normalize(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BornRedundancy_iabs___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BornRedundancy_iabs___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_iabs(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_iabs___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_D1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_D1___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_applyMat2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_applyMat2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_sqNorm(lean_object*);
static lean_object* _init_lp_FiniteQuantum_BornRedundancy_listSum___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(0u);
v___x_2_ = l_Nat_cast___at___00Dyadic_toRat_spec__0(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_listSum(lean_object* v_x_3_){
_start:
{
if (lean_obj_tag(v_x_3_) == 0)
{
lean_object* v___x_4_; 
v___x_4_ = lean_obj_once(&lp_FiniteQuantum_BornRedundancy_listSum___closed__0, &lp_FiniteQuantum_BornRedundancy_listSum___closed__0_once, _init_lp_FiniteQuantum_BornRedundancy_listSum___closed__0);
return v___x_4_;
}
else
{
lean_object* v_head_5_; lean_object* v_tail_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v_head_5_ = lean_ctor_get(v_x_3_, 0);
lean_inc(v_head_5_);
v_tail_6_ = lean_ctor_get(v_x_3_, 1);
lean_inc(v_tail_6_);
lean_dec_ref_known(v_x_3_, 2);
v___x_7_ = lp_FiniteQuantum_BornRedundancy_listSum(v_tail_6_);
v___x_8_ = l_Rat_add(v_head_5_, v___x_7_);
return v___x_8_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_smul(lean_object* v_c_9_, lean_object* v_x_10_){
_start:
{
if (lean_obj_tag(v_x_10_) == 0)
{
return v_x_10_;
}
else
{
lean_object* v_head_11_; lean_object* v_tail_12_; lean_object* v___x_14_; uint8_t v_isShared_15_; uint8_t v_isSharedCheck_21_; 
v_head_11_ = lean_ctor_get(v_x_10_, 0);
v_tail_12_ = lean_ctor_get(v_x_10_, 1);
v_isSharedCheck_21_ = !lean_is_exclusive(v_x_10_);
if (v_isSharedCheck_21_ == 0)
{
v___x_14_ = v_x_10_;
v_isShared_15_ = v_isSharedCheck_21_;
goto v_resetjp_13_;
}
else
{
lean_inc(v_tail_12_);
lean_inc(v_head_11_);
lean_dec(v_x_10_);
v___x_14_ = lean_box(0);
v_isShared_15_ = v_isSharedCheck_21_;
goto v_resetjp_13_;
}
v_resetjp_13_:
{
lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_19_; 
v___x_16_ = l_Rat_mul(v_c_9_, v_head_11_);
v___x_17_ = lp_FiniteQuantum_BornRedundancy_smul(v_c_9_, v_tail_12_);
if (v_isShared_15_ == 0)
{
lean_ctor_set(v___x_14_, 1, v___x_17_);
lean_ctor_set(v___x_14_, 0, v___x_16_);
v___x_19_ = v___x_14_;
goto v_reusejp_18_;
}
else
{
lean_object* v_reuseFailAlloc_20_; 
v_reuseFailAlloc_20_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_20_, 0, v___x_16_);
lean_ctor_set(v_reuseFailAlloc_20_, 1, v___x_17_);
v___x_19_ = v_reuseFailAlloc_20_;
goto v_reusejp_18_;
}
v_reusejp_18_:
{
return v___x_19_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_smul___boxed(lean_object* v_c_22_, lean_object* v_x_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_FiniteQuantum_BornRedundancy_smul(v_c_22_, v_x_23_);
lean_dec_ref(v_c_22_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_BornRedundancy_0__BornRedundancy_listSum_match__1_splitter___redArg(lean_object* v_x_25_, lean_object* v_h__1_26_, lean_object* v_h__2_27_){
_start:
{
if (lean_obj_tag(v_x_25_) == 0)
{
lean_object* v___x_28_; lean_object* v___x_29_; 
lean_dec(v_h__2_27_);
v___x_28_ = lean_box(0);
v___x_29_ = lean_apply_1(v_h__1_26_, v___x_28_);
return v___x_29_;
}
else
{
lean_object* v_head_30_; lean_object* v_tail_31_; lean_object* v___x_32_; 
lean_dec(v_h__1_26_);
v_head_30_ = lean_ctor_get(v_x_25_, 0);
lean_inc(v_head_30_);
v_tail_31_ = lean_ctor_get(v_x_25_, 1);
lean_inc(v_tail_31_);
lean_dec_ref_known(v_x_25_, 2);
v___x_32_ = lean_apply_2(v_h__2_27_, v_head_30_, v_tail_31_);
return v___x_32_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_BornRedundancy_0__BornRedundancy_listSum_match__1_splitter(lean_object* v_motive_33_, lean_object* v_x_34_, lean_object* v_h__1_35_, lean_object* v_h__2_36_){
_start:
{
if (lean_obj_tag(v_x_34_) == 0)
{
lean_object* v___x_37_; lean_object* v___x_38_; 
lean_dec(v_h__2_36_);
v___x_37_ = lean_box(0);
v___x_38_ = lean_apply_1(v_h__1_35_, v___x_37_);
return v___x_38_;
}
else
{
lean_object* v_head_39_; lean_object* v_tail_40_; lean_object* v___x_41_; 
lean_dec(v_h__1_35_);
v_head_39_ = lean_ctor_get(v_x_34_, 0);
lean_inc(v_head_39_);
v_tail_40_ = lean_ctor_get(v_x_34_, 1);
lean_inc(v_tail_40_);
lean_dec_ref_known(v_x_34_, 2);
v___x_41_ = lean_apply_2(v_h__2_36_, v_head_39_, v_tail_40_);
return v___x_41_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_normalize(lean_object* v_w_42_){
_start:
{
lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___x_45_; 
lean_inc(v_w_42_);
v___x_43_ = lp_FiniteQuantum_BornRedundancy_listSum(v_w_42_);
v___x_44_ = l_Rat_inv(v___x_43_);
v___x_45_ = lp_FiniteQuantum_BornRedundancy_smul(v___x_44_, v_w_42_);
lean_dec_ref(v___x_44_);
return v___x_45_;
}
}
static lean_object* _init_lp_FiniteQuantum_BornRedundancy_iabs___closed__0(void){
_start:
{
lean_object* v___x_46_; lean_object* v___x_47_; 
v___x_46_ = lean_unsigned_to_nat(0u);
v___x_47_ = lean_nat_to_int(v___x_46_);
return v___x_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_iabs(lean_object* v_x_48_){
_start:
{
lean_object* v___x_49_; uint8_t v___x_50_; 
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_BornRedundancy_iabs___closed__0, &lp_FiniteQuantum_BornRedundancy_iabs___closed__0_once, _init_lp_FiniteQuantum_BornRedundancy_iabs___closed__0);
v___x_50_ = lean_int_dec_lt(v_x_48_, v___x_49_);
if (v___x_50_ == 0)
{
lean_inc(v_x_48_);
return v_x_48_;
}
else
{
lean_object* v___x_51_; 
v___x_51_ = lean_int_neg(v_x_48_);
return v___x_51_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_iabs___boxed(lean_object* v_x_52_){
_start:
{
lean_object* v_res_53_; 
v_res_53_ = lp_FiniteQuantum_BornRedundancy_iabs(v_x_52_);
lean_dec(v_x_52_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_D1(lean_object* v_x_54_, lean_object* v_y_55_){
_start:
{
lean_object* v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___x_61_; 
v___x_56_ = lp_FiniteQuantum_BornRedundancy_iabs(v_x_54_);
v___x_57_ = lp_FiniteQuantum_BornRedundancy_iabs(v_y_55_);
v___x_58_ = lean_int_add(v___x_56_, v___x_57_);
lean_dec(v___x_57_);
lean_dec(v___x_56_);
v___x_59_ = lean_int_add(v_x_54_, v_y_55_);
v___x_60_ = lp_FiniteQuantum_BornRedundancy_iabs(v___x_59_);
lean_dec(v___x_59_);
v___x_61_ = lean_int_sub(v___x_58_, v___x_60_);
lean_dec(v___x_60_);
lean_dec(v___x_58_);
return v___x_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_D1___boxed(lean_object* v_x_62_, lean_object* v_y_63_){
_start:
{
lean_object* v_res_64_; 
v_res_64_ = lp_FiniteQuantum_BornRedundancy_D1(v_x_62_, v_y_63_);
lean_dec(v_y_63_);
lean_dec(v_x_62_);
return v_res_64_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2_decEq(lean_object* v_x_65_, lean_object* v_x_66_){
_start:
{
lean_object* v_x_67_; lean_object* v_y_68_; lean_object* v_x_69_; lean_object* v_y_70_; uint8_t v___x_71_; 
v_x_67_ = lean_ctor_get(v_x_65_, 0);
v_y_68_ = lean_ctor_get(v_x_65_, 1);
v_x_69_ = lean_ctor_get(v_x_66_, 0);
v_y_70_ = lean_ctor_get(v_x_66_, 1);
v___x_71_ = lean_int_dec_eq(v_x_67_, v_x_69_);
if (v___x_71_ == 0)
{
return v___x_71_;
}
else
{
uint8_t v___x_72_; 
v___x_72_ = lean_int_dec_eq(v_y_68_, v_y_70_);
return v___x_72_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2_decEq___boxed(lean_object* v_x_73_, lean_object* v_x_74_){
_start:
{
uint8_t v_res_75_; lean_object* v_r_76_; 
v_res_75_ = lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2_decEq(v_x_73_, v_x_74_);
lean_dec_ref(v_x_74_);
lean_dec_ref(v_x_73_);
v_r_76_ = lean_box(v_res_75_);
return v_r_76_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2(lean_object* v_x_77_, lean_object* v_x_78_){
_start:
{
uint8_t v___x_79_; 
v___x_79_ = lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2_decEq(v_x_77_, v_x_78_);
return v___x_79_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2___boxed(lean_object* v_x_80_, lean_object* v_x_81_){
_start:
{
uint8_t v_res_82_; lean_object* v_r_83_; 
v_res_82_ = lp_FiniteQuantum_BornRedundancy_instDecidableEqVec2(v_x_80_, v_x_81_);
lean_dec_ref(v_x_81_);
lean_dec_ref(v_x_80_);
v_r_83_ = lean_box(v_res_82_);
return v_r_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_applyMat2(lean_object* v_M_84_, lean_object* v_v_85_){
_start:
{
lean_object* v_a_86_; lean_object* v_b_87_; lean_object* v_c_88_; lean_object* v_d_89_; lean_object* v_x_90_; lean_object* v_y_91_; lean_object* v___x_93_; uint8_t v_isShared_94_; uint8_t v_isSharedCheck_104_; 
v_a_86_ = lean_ctor_get(v_M_84_, 0);
v_b_87_ = lean_ctor_get(v_M_84_, 1);
v_c_88_ = lean_ctor_get(v_M_84_, 2);
v_d_89_ = lean_ctor_get(v_M_84_, 3);
v_x_90_ = lean_ctor_get(v_v_85_, 0);
v_y_91_ = lean_ctor_get(v_v_85_, 1);
v_isSharedCheck_104_ = !lean_is_exclusive(v_v_85_);
if (v_isSharedCheck_104_ == 0)
{
v___x_93_ = v_v_85_;
v_isShared_94_ = v_isSharedCheck_104_;
goto v_resetjp_92_;
}
else
{
lean_inc(v_y_91_);
lean_inc(v_x_90_);
lean_dec(v_v_85_);
v___x_93_ = lean_box(0);
v_isShared_94_ = v_isSharedCheck_104_;
goto v_resetjp_92_;
}
v_resetjp_92_:
{
lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_102_; 
v___x_95_ = lean_int_mul(v_a_86_, v_x_90_);
v___x_96_ = lean_int_mul(v_b_87_, v_y_91_);
v___x_97_ = lean_int_add(v___x_95_, v___x_96_);
lean_dec(v___x_96_);
lean_dec(v___x_95_);
v___x_98_ = lean_int_mul(v_c_88_, v_x_90_);
lean_dec(v_x_90_);
v___x_99_ = lean_int_mul(v_d_89_, v_y_91_);
lean_dec(v_y_91_);
v___x_100_ = lean_int_add(v___x_98_, v___x_99_);
lean_dec(v___x_99_);
lean_dec(v___x_98_);
if (v_isShared_94_ == 0)
{
lean_ctor_set(v___x_93_, 1, v___x_100_);
lean_ctor_set(v___x_93_, 0, v___x_97_);
v___x_102_ = v___x_93_;
goto v_reusejp_101_;
}
else
{
lean_object* v_reuseFailAlloc_103_; 
v_reuseFailAlloc_103_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_103_, 0, v___x_97_);
lean_ctor_set(v_reuseFailAlloc_103_, 1, v___x_100_);
v___x_102_ = v_reuseFailAlloc_103_;
goto v_reusejp_101_;
}
v_reusejp_101_:
{
return v___x_102_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_applyMat2___boxed(lean_object* v_M_105_, lean_object* v_v_106_){
_start:
{
lean_object* v_res_107_; 
v_res_107_ = lp_FiniteQuantum_BornRedundancy_applyMat2(v_M_105_, v_v_106_);
lean_dec_ref(v_M_105_);
return v_res_107_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornRedundancy_sqNorm(lean_object* v_v_108_){
_start:
{
lean_object* v_x_109_; lean_object* v_y_110_; lean_object* v___x_112_; uint8_t v_isShared_113_; uint8_t v_isSharedCheck_119_; 
v_x_109_ = lean_ctor_get(v_v_108_, 0);
v_y_110_ = lean_ctor_get(v_v_108_, 1);
v_isSharedCheck_119_ = !lean_is_exclusive(v_v_108_);
if (v_isSharedCheck_119_ == 0)
{
v___x_112_ = v_v_108_;
v_isShared_113_ = v_isSharedCheck_119_;
goto v_resetjp_111_;
}
else
{
lean_inc(v_y_110_);
lean_inc(v_x_109_);
lean_dec(v_v_108_);
v___x_112_ = lean_box(0);
v_isShared_113_ = v_isSharedCheck_119_;
goto v_resetjp_111_;
}
v_resetjp_111_:
{
lean_object* v___x_114_; lean_object* v___x_115_; lean_object* v___x_117_; 
v___x_114_ = lean_int_mul(v_x_109_, v_x_109_);
lean_dec(v_x_109_);
v___x_115_ = lean_int_mul(v_y_110_, v_y_110_);
lean_dec(v_y_110_);
if (v_isShared_113_ == 0)
{
lean_ctor_set(v___x_112_, 1, v___x_115_);
lean_ctor_set(v___x_112_, 0, v___x_114_);
v___x_117_ = v___x_112_;
goto v_reusejp_116_;
}
else
{
lean_object* v_reuseFailAlloc_118_; 
v_reuseFailAlloc_118_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_118_, 0, v___x_114_);
lean_ctor_set(v_reuseFailAlloc_118_, 1, v___x_115_);
v___x_117_ = v_reuseFailAlloc_118_;
goto v_reusejp_116_;
}
v_reusejp_116_:
{
return v___x_117_;
}
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_BornRedundancy(uint8_t builtin) {
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
