// Lean compiler output
// Module: GenesisFspBridge
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
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GenesisFspBridge_instDecidableD2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_instDecidableD2___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GenesisFspBridge_swap(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_swap___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GenesisFspBridge_instDecidableS2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_instDecidableS2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_zero_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_zero_elim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_edge_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_edge_elim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_add_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_add_elim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary1(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0;
static lean_once_cell_t lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_d__joint__eval(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_det__skew__2x2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_det__skew__2x2___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GenesisFspBridge_instDecidableD2(uint8_t v_x_1_, uint8_t v_y_2_){
_start:
{
uint8_t v___x_3_; 
v___x_3_ = 0;
if (v_x_1_ == 0)
{
if (v_y_2_ == 0)
{
return v___x_3_;
}
else
{
return v_y_2_;
}
}
else
{
return v___x_3_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_instDecidableD2___boxed(lean_object* v_x_4_, lean_object* v_y_5_){
_start:
{
uint8_t v_x_boxed_6_; uint8_t v_y_boxed_7_; uint8_t v_res_8_; lean_object* v_r_9_; 
v_x_boxed_6_ = lean_unbox(v_x_4_);
v_y_boxed_7_ = lean_unbox(v_y_5_);
v_res_8_ = lp_FiniteQuantum_GenesisFspBridge_instDecidableD2(v_x_boxed_6_, v_y_boxed_7_);
v_r_9_ = lean_box(v_res_8_);
return v_r_9_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_GenesisFspBridge_swap(uint8_t v_b_10_){
_start:
{
if (v_b_10_ == 0)
{
uint8_t v___x_11_; 
v___x_11_ = 1;
return v___x_11_;
}
else
{
uint8_t v___x_12_; 
v___x_12_ = 0;
return v___x_12_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_swap___boxed(lean_object* v_b_13_){
_start:
{
uint8_t v_b_boxed_14_; uint8_t v_res_15_; lean_object* v_r_16_; 
v_b_boxed_14_ = lean_unbox(v_b_13_);
v_res_15_ = lp_FiniteQuantum_GenesisFspBridge_swap(v_b_boxed_14_);
v_r_16_ = lean_box(v_res_15_);
return v_r_16_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_GenesisFspBridge_instDecidableS2(uint8_t v_x_17_, uint8_t v_y_18_){
_start:
{
uint8_t v___x_19_; uint8_t v___x_20_; 
v___x_19_ = lp_FiniteQuantum_GenesisFspBridge_instDecidableD2(v_y_18_, v_x_17_);
v___x_20_ = lp_FiniteQuantum_GenesisFspBridge_instDecidableD2(v_x_17_, v_y_18_);
if (v___x_20_ == 0)
{
return v___x_19_;
}
else
{
return v___x_20_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_instDecidableS2___boxed(lean_object* v_x_21_, lean_object* v_y_22_){
_start:
{
uint8_t v_x_boxed_23_; uint8_t v_y_boxed_24_; uint8_t v_res_25_; lean_object* v_r_26_; 
v_x_boxed_23_ = lean_unbox(v_x_21_);
v_y_boxed_24_ = lean_unbox(v_y_22_);
v_res_25_ = lp_FiniteQuantum_GenesisFspBridge_instDecidableS2(v_x_boxed_23_, v_y_boxed_24_);
v_r_26_ = lean_box(v_res_25_);
return v_r_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___redArg(lean_object* v_x_27_){
_start:
{
switch(lean_obj_tag(v_x_27_))
{
case 0:
{
lean_object* v___x_28_; 
v___x_28_ = lean_unsigned_to_nat(0u);
return v___x_28_;
}
case 1:
{
lean_object* v___x_29_; 
v___x_29_ = lean_unsigned_to_nat(1u);
return v___x_29_;
}
default: 
{
lean_object* v___x_30_; 
v___x_30_ = lean_unsigned_to_nat(2u);
return v___x_30_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___redArg___boxed(lean_object* v_x_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___redArg(v_x_31_);
lean_dec(v_x_31_);
return v_res_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx(lean_object* v_V_33_, lean_object* v_x_34_){
_start:
{
lean_object* v___x_35_; 
v___x_35_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___redArg(v_x_34_);
return v___x_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx___boxed(lean_object* v_V_36_, lean_object* v_x_37_){
_start:
{
lean_object* v_res_38_; 
v_res_38_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorIdx(v_V_36_, v_x_37_);
lean_dec(v_x_37_);
return v_res_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(lean_object* v_t_39_, lean_object* v_k_40_){
_start:
{
switch(lean_obj_tag(v_t_39_))
{
case 0:
{
return v_k_40_;
}
case 1:
{
lean_object* v_a_41_; lean_object* v_a_42_; lean_object* v_a_43_; lean_object* v___x_44_; 
v_a_41_ = lean_ctor_get(v_t_39_, 0);
lean_inc(v_a_41_);
v_a_42_ = lean_ctor_get(v_t_39_, 1);
lean_inc(v_a_42_);
v_a_43_ = lean_ctor_get(v_t_39_, 2);
lean_inc(v_a_43_);
lean_dec_ref_known(v_t_39_, 3);
v___x_44_ = lean_apply_3(v_k_40_, v_a_41_, v_a_42_, v_a_43_);
return v___x_44_;
}
default: 
{
lean_object* v_a_45_; lean_object* v_a_46_; lean_object* v___x_47_; 
v_a_45_ = lean_ctor_get(v_t_39_, 0);
lean_inc(v_a_45_);
v_a_46_ = lean_ctor_get(v_t_39_, 1);
lean_inc(v_a_46_);
lean_dec_ref_known(v_t_39_, 2);
v___x_47_ = lean_apply_2(v_k_40_, v_a_45_, v_a_46_);
return v___x_47_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim(lean_object* v_V_48_, lean_object* v_motive_49_, lean_object* v_ctorIdx_50_, lean_object* v_t_51_, lean_object* v_h_52_, lean_object* v_k_53_){
_start:
{
lean_object* v___x_54_; 
v___x_54_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_51_, v_k_53_);
return v___x_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___boxed(lean_object* v_V_55_, lean_object* v_motive_56_, lean_object* v_ctorIdx_57_, lean_object* v_t_58_, lean_object* v_h_59_, lean_object* v_k_60_){
_start:
{
lean_object* v_res_61_; 
v_res_61_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim(v_V_55_, v_motive_56_, v_ctorIdx_57_, v_t_58_, v_h_59_, v_k_60_);
lean_dec(v_ctorIdx_57_);
return v_res_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_zero_elim___redArg(lean_object* v_t_62_, lean_object* v_zero_63_){
_start:
{
lean_object* v___x_64_; 
v___x_64_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_62_, v_zero_63_);
return v___x_64_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_zero_elim(lean_object* v_V_65_, lean_object* v_motive_66_, lean_object* v_t_67_, lean_object* v_h_68_, lean_object* v_zero_69_){
_start:
{
lean_object* v___x_70_; 
v___x_70_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_67_, v_zero_69_);
return v___x_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_edge_elim___redArg(lean_object* v_t_71_, lean_object* v_edge_72_){
_start:
{
lean_object* v___x_73_; 
v___x_73_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_71_, v_edge_72_);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_edge_elim(lean_object* v_V_74_, lean_object* v_motive_75_, lean_object* v_t_76_, lean_object* v_h_77_, lean_object* v_edge_78_){
_start:
{
lean_object* v___x_79_; 
v___x_79_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_76_, v_edge_78_);
return v___x_79_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_add_elim___redArg(lean_object* v_t_80_, lean_object* v_add_81_){
_start:
{
lean_object* v___x_82_; 
v___x_82_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_80_, v_add_81_);
return v___x_82_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_Chain1_add_elim(lean_object* v_V_83_, lean_object* v_motive_84_, lean_object* v_t_85_, lean_object* v_h_86_, lean_object* v_add_87_){
_start:
{
lean_object* v___x_88_; 
v___x_88_ = lp_FiniteQuantum_GenesisFspBridge_Chain1_ctorElim___redArg(v_t_85_, v_add_87_);
return v___x_88_;
}
}
static lean_object* _init_lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0(void){
_start:
{
lean_object* v___x_89_; lean_object* v___x_90_; 
v___x_89_ = lean_unsigned_to_nat(0u);
v___x_90_ = lean_nat_to_int(v___x_89_);
return v___x_90_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg(lean_object* v_inst_91_, lean_object* v_x_92_, lean_object* v_a_93_){
_start:
{
switch(lean_obj_tag(v_x_92_))
{
case 0:
{
lean_object* v___x_94_; 
lean_dec(v_a_93_);
lean_dec_ref(v_inst_91_);
v___x_94_ = lean_obj_once(&lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0, &lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0_once, _init_lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0);
return v___x_94_;
}
case 1:
{
lean_object* v_a_95_; lean_object* v_a_96_; lean_object* v_a_97_; lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___y_101_; uint8_t v___x_106_; 
v_a_95_ = lean_ctor_get(v_x_92_, 0);
lean_inc(v_a_95_);
v_a_96_ = lean_ctor_get(v_x_92_, 1);
lean_inc(v_a_96_);
v_a_97_ = lean_ctor_get(v_x_92_, 2);
lean_inc(v_a_97_);
lean_dec_ref_known(v_x_92_, 3);
lean_inc_ref(v_inst_91_);
lean_inc(v_a_93_);
v___x_98_ = lean_apply_2(v_inst_91_, v_a_93_, v_a_97_);
v___x_99_ = lean_apply_2(v_inst_91_, v_a_93_, v_a_96_);
v___x_106_ = lean_unbox(v___x_98_);
if (v___x_106_ == 0)
{
lean_object* v___x_107_; 
v___x_107_ = lean_obj_once(&lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0, &lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0_once, _init_lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0);
v___y_101_ = v___x_107_;
goto v___jp_100_;
}
else
{
lean_inc(v_a_95_);
v___y_101_ = v_a_95_;
goto v___jp_100_;
}
v___jp_100_:
{
uint8_t v___x_102_; 
v___x_102_ = lean_unbox(v___x_99_);
if (v___x_102_ == 0)
{
lean_object* v___x_103_; lean_object* v___x_104_; 
lean_dec(v_a_95_);
v___x_103_ = lean_obj_once(&lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0, &lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0_once, _init_lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg___closed__0);
v___x_104_ = lean_int_sub(v___y_101_, v___x_103_);
lean_dec(v___y_101_);
return v___x_104_;
}
else
{
lean_object* v___x_105_; 
v___x_105_ = lean_int_sub(v___y_101_, v_a_95_);
lean_dec(v_a_95_);
lean_dec(v___y_101_);
return v___x_105_;
}
}
}
default: 
{
lean_object* v_a_108_; lean_object* v_a_109_; lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; 
v_a_108_ = lean_ctor_get(v_x_92_, 0);
lean_inc(v_a_108_);
v_a_109_ = lean_ctor_get(v_x_92_, 1);
lean_inc(v_a_109_);
lean_dec_ref_known(v_x_92_, 2);
lean_inc(v_a_93_);
lean_inc_ref(v_inst_91_);
v___x_110_ = lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg(v_inst_91_, v_a_108_, v_a_93_);
v___x_111_ = lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg(v_inst_91_, v_a_109_, v_a_93_);
v___x_112_ = lean_int_add(v___x_110_, v___x_111_);
lean_dec(v___x_111_);
lean_dec(v___x_110_);
return v___x_112_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary1(lean_object* v_V_113_, lean_object* v_inst_114_, lean_object* v_x_115_, lean_object* v_a_116_){
_start:
{
lean_object* v___x_117_; 
v___x_117_ = lp_FiniteQuantum_GenesisFspBridge_boundary1___redArg(v_inst_114_, v_x_115_, v_a_116_);
return v___x_117_;
}
}
static lean_object* _init_lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(1u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__1(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_120_ = lean_obj_once(&lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0, &lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0_once, _init_lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0);
v___x_121_ = lean_int_neg(v___x_120_);
return v___x_121_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg(lean_object* v_s_122_){
_start:
{
lean_object* v_u_123_; lean_object* v_v_124_; lean_object* v_w_125_; lean_object* v___x_127_; uint8_t v_isShared_128_; uint8_t v_isSharedCheck_138_; 
v_u_123_ = lean_ctor_get(v_s_122_, 0);
v_v_124_ = lean_ctor_get(v_s_122_, 1);
v_w_125_ = lean_ctor_get(v_s_122_, 2);
v_isSharedCheck_138_ = !lean_is_exclusive(v_s_122_);
if (v_isSharedCheck_138_ == 0)
{
v___x_127_ = v_s_122_;
v_isShared_128_ = v_isSharedCheck_138_;
goto v_resetjp_126_;
}
else
{
lean_inc(v_w_125_);
lean_inc(v_v_124_);
lean_inc(v_u_123_);
lean_dec(v_s_122_);
v___x_127_ = lean_box(0);
v_isShared_128_ = v_isSharedCheck_138_;
goto v_resetjp_126_;
}
v_resetjp_126_:
{
lean_object* v___x_129_; lean_object* v___x_131_; 
v___x_129_ = lean_obj_once(&lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0, &lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0_once, _init_lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__0);
lean_inc(v_w_125_);
lean_inc(v_v_124_);
if (v_isShared_128_ == 0)
{
lean_ctor_set_tag(v___x_127_, 1);
lean_ctor_set(v___x_127_, 0, v___x_129_);
v___x_131_ = v___x_127_;
goto v_reusejp_130_;
}
else
{
lean_object* v_reuseFailAlloc_137_; 
v_reuseFailAlloc_137_ = lean_alloc_ctor(1, 3, 0);
lean_ctor_set(v_reuseFailAlloc_137_, 0, v___x_129_);
lean_ctor_set(v_reuseFailAlloc_137_, 1, v_v_124_);
lean_ctor_set(v_reuseFailAlloc_137_, 2, v_w_125_);
v___x_131_ = v_reuseFailAlloc_137_;
goto v_reusejp_130_;
}
v_reusejp_130_:
{
lean_object* v___x_132_; lean_object* v___x_133_; lean_object* v___x_134_; lean_object* v___x_135_; lean_object* v___x_136_; 
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__1, &lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__1_once, _init_lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg___closed__1);
lean_inc(v_u_123_);
v___x_133_ = lean_alloc_ctor(1, 3, 0);
lean_ctor_set(v___x_133_, 0, v___x_132_);
lean_ctor_set(v___x_133_, 1, v_u_123_);
lean_ctor_set(v___x_133_, 2, v_w_125_);
v___x_134_ = lean_alloc_ctor(1, 3, 0);
lean_ctor_set(v___x_134_, 0, v___x_129_);
lean_ctor_set(v___x_134_, 1, v_u_123_);
lean_ctor_set(v___x_134_, 2, v_v_124_);
v___x_135_ = lean_alloc_ctor(2, 2, 0);
lean_ctor_set(v___x_135_, 0, v___x_133_);
lean_ctor_set(v___x_135_, 1, v___x_134_);
v___x_136_ = lean_alloc_ctor(2, 2, 0);
lean_ctor_set(v___x_136_, 0, v___x_131_);
lean_ctor_set(v___x_136_, 1, v___x_135_);
return v___x_136_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_boundary2(lean_object* v_V_139_, lean_object* v_s_140_){
_start:
{
lean_object* v___x_141_; 
v___x_141_ = lp_FiniteQuantum_GenesisFspBridge_boundary2___redArg(v_s_140_);
return v___x_141_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_d__joint__eval(lean_object* v_alpha__gauge_142_){
_start:
{
lean_object* v___x_143_; lean_object* v___x_144_; 
v___x_143_ = lean_unsigned_to_nat(0u);
v___x_144_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_144_, 0, v_alpha__gauge_142_);
lean_ctor_set(v___x_144_, 1, v___x_143_);
return v___x_144_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_det__skew__2x2(lean_object* v_a_145_){
_start:
{
lean_object* v___x_146_; 
v___x_146_ = lean_int_mul(v_a_145_, v_a_145_);
return v___x_146_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GenesisFspBridge_det__skew__2x2___boxed(lean_object* v_a_147_){
_start:
{
lean_object* v_res_148_; 
v_res_148_ = lp_FiniteQuantum_GenesisFspBridge_det__skew__2x2(v_a_147_);
lean_dec(v_a_147_);
return v_res_148_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_GenesisFspBridge(uint8_t builtin) {
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
