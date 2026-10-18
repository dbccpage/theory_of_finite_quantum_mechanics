// Lean compiler output
// Module: H017MatrixFiniteRecovery
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H005InnerProductAdmission public import H007Complexification
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___redArg(lean_object*, lean_object*, lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat(lean_object*, lean_object*, lean_object*, lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg(lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul(lean_object*, lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___redArg(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___redArg(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj(lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___lam__0(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf(lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_endOfMat___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_endOfMat(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliX(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliX___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___redArg(lean_object* v_P_1_, lean_object* v_A_2_, lean_object* v_v_3_, uint8_t v_i_4_){
_start:
{
lean_object* v_add_5_; lean_object* v_mul_6_; uint8_t v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; uint8_t v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v_add_5_ = lean_ctor_get(v_P_1_, 0);
lean_inc(v_add_5_);
v_mul_6_ = lean_ctor_get(v_P_1_, 1);
lean_inc_n(v_mul_6_, 2);
lean_dec_ref(v_P_1_);
v___x_7_ = 0;
v___x_8_ = lean_box(v_i_4_);
v___x_9_ = lean_box(v___x_7_);
lean_inc(v_A_2_);
v___x_10_ = lean_apply_2(v_A_2_, v___x_8_, v___x_9_);
v___x_11_ = lean_box(v___x_7_);
lean_inc(v_v_3_);
v___x_12_ = lean_apply_1(v_v_3_, v___x_11_);
v___x_13_ = lean_apply_2(v_mul_6_, v___x_10_, v___x_12_);
v___x_14_ = 1;
v___x_15_ = lean_box(v_i_4_);
v___x_16_ = lean_box(v___x_14_);
v___x_17_ = lean_apply_2(v_A_2_, v___x_15_, v___x_16_);
v___x_18_ = lean_box(v___x_14_);
v___x_19_ = lean_apply_1(v_v_3_, v___x_18_);
v___x_20_ = lean_apply_2(v_mul_6_, v___x_17_, v___x_19_);
v___x_21_ = lean_apply_2(v_add_5_, v___x_13_, v___x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___redArg___boxed(lean_object* v_P_22_, lean_object* v_A_23_, lean_object* v_v_24_, lean_object* v_i_25_){
_start:
{
uint8_t v_i_boxed_26_; lean_object* v_res_27_; 
v_i_boxed_26_ = lean_unbox(v_i_25_);
v_res_27_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___redArg(v_P_22_, v_A_23_, v_v_24_, v_i_boxed_26_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat(lean_object* v_K_28_, lean_object* v_P_29_, lean_object* v_A_30_, lean_object* v_v_31_, uint8_t v_i_32_){
_start:
{
lean_object* v___x_33_; 
v___x_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___redArg(v_P_29_, v_A_30_, v_v_31_, v_i_32_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___boxed(lean_object* v_K_34_, lean_object* v_P_35_, lean_object* v_A_36_, lean_object* v_v_37_, lean_object* v_i_38_){
_start:
{
uint8_t v_i_boxed_39_; lean_object* v_res_40_; 
v_i_boxed_39_ = lean_unbox(v_i_38_);
v_res_40_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat(v_K_34_, v_P_35_, v_A_36_, v_v_37_, v_i_boxed_39_);
return v_res_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg(lean_object* v_P_41_, lean_object* v_A_42_, lean_object* v_B_43_, uint8_t v_i_44_, uint8_t v_j_45_){
_start:
{
lean_object* v_add_46_; lean_object* v_mul_47_; uint8_t v___x_48_; lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; lean_object* v___x_52_; lean_object* v___x_53_; lean_object* v___x_54_; lean_object* v___x_55_; uint8_t v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; 
v_add_46_ = lean_ctor_get(v_P_41_, 0);
lean_inc(v_add_46_);
v_mul_47_ = lean_ctor_get(v_P_41_, 1);
lean_inc_n(v_mul_47_, 2);
lean_dec_ref(v_P_41_);
v___x_48_ = 0;
v___x_49_ = lean_box(v_i_44_);
v___x_50_ = lean_box(v___x_48_);
lean_inc(v_A_42_);
v___x_51_ = lean_apply_2(v_A_42_, v___x_49_, v___x_50_);
v___x_52_ = lean_box(v___x_48_);
v___x_53_ = lean_box(v_j_45_);
lean_inc(v_B_43_);
v___x_54_ = lean_apply_2(v_B_43_, v___x_52_, v___x_53_);
v___x_55_ = lean_apply_2(v_mul_47_, v___x_51_, v___x_54_);
v___x_56_ = 1;
v___x_57_ = lean_box(v_i_44_);
v___x_58_ = lean_box(v___x_56_);
v___x_59_ = lean_apply_2(v_A_42_, v___x_57_, v___x_58_);
v___x_60_ = lean_box(v___x_56_);
v___x_61_ = lean_box(v_j_45_);
v___x_62_ = lean_apply_2(v_B_43_, v___x_60_, v___x_61_);
v___x_63_ = lean_apply_2(v_mul_47_, v___x_59_, v___x_62_);
v___x_64_ = lean_apply_2(v_add_46_, v___x_55_, v___x_63_);
return v___x_64_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg___boxed(lean_object* v_P_65_, lean_object* v_A_66_, lean_object* v_B_67_, lean_object* v_i_68_, lean_object* v_j_69_){
_start:
{
uint8_t v_i_boxed_70_; uint8_t v_j_boxed_71_; lean_object* v_res_72_; 
v_i_boxed_70_ = lean_unbox(v_i_68_);
v_j_boxed_71_ = lean_unbox(v_j_69_);
v_res_72_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg(v_P_65_, v_A_66_, v_B_67_, v_i_boxed_70_, v_j_boxed_71_);
return v_res_72_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul(lean_object* v_K_73_, lean_object* v_P_74_, lean_object* v_A_75_, lean_object* v_B_76_, uint8_t v_i_77_, uint8_t v_j_78_){
_start:
{
lean_object* v___x_79_; 
v___x_79_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___redArg(v_P_74_, v_A_75_, v_B_76_, v_i_77_, v_j_78_);
return v___x_79_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul___boxed(lean_object* v_K_80_, lean_object* v_P_81_, lean_object* v_A_82_, lean_object* v_B_83_, lean_object* v_i_84_, lean_object* v_j_85_){
_start:
{
uint8_t v_i_boxed_86_; uint8_t v_j_boxed_87_; lean_object* v_res_88_; 
v_i_boxed_86_ = lean_unbox(v_i_84_);
v_j_boxed_87_ = lean_unbox(v_j_85_);
v_res_88_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_mmul(v_K_80_, v_P_81_, v_A_82_, v_B_83_, v_i_boxed_86_, v_j_boxed_87_);
return v_res_88_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___redArg(lean_object* v_P_89_, uint8_t v_i_90_, uint8_t v_j_91_){
_start:
{
if (v_i_90_ == 0)
{
if (v_j_91_ == 0)
{
lean_object* v_one_92_; 
v_one_92_ = lean_ctor_get(v_P_89_, 4);
lean_inc(v_one_92_);
return v_one_92_;
}
else
{
lean_object* v_zero_93_; 
v_zero_93_ = lean_ctor_get(v_P_89_, 3);
lean_inc(v_zero_93_);
return v_zero_93_;
}
}
else
{
if (v_j_91_ == 0)
{
lean_object* v_zero_94_; 
v_zero_94_ = lean_ctor_get(v_P_89_, 3);
lean_inc(v_zero_94_);
return v_zero_94_;
}
else
{
lean_object* v_one_95_; 
v_one_95_ = lean_ctor_get(v_P_89_, 4);
lean_inc(v_one_95_);
return v_one_95_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___redArg___boxed(lean_object* v_P_96_, lean_object* v_i_97_, lean_object* v_j_98_){
_start:
{
uint8_t v_i_boxed_99_; uint8_t v_j_boxed_100_; lean_object* v_res_101_; 
v_i_boxed_99_ = lean_unbox(v_i_97_);
v_j_boxed_100_ = lean_unbox(v_j_98_);
v_res_101_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___redArg(v_P_96_, v_i_boxed_99_, v_j_boxed_100_);
lean_dec_ref(v_P_96_);
return v_res_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident(lean_object* v_K_102_, lean_object* v_P_103_, uint8_t v_i_104_, uint8_t v_j_105_){
_start:
{
lean_object* v___x_106_; 
v___x_106_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___redArg(v_P_103_, v_i_104_, v_j_105_);
return v___x_106_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident___boxed(lean_object* v_K_107_, lean_object* v_P_108_, lean_object* v_i_109_, lean_object* v_j_110_){
_start:
{
uint8_t v_i_boxed_111_; uint8_t v_j_boxed_112_; lean_object* v_res_113_; 
v_i_boxed_111_ = lean_unbox(v_i_109_);
v_j_boxed_112_ = lean_unbox(v_j_110_);
v_res_113_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_ident(v_K_107_, v_P_108_, v_i_boxed_111_, v_j_boxed_112_);
lean_dec_ref(v_P_108_);
return v_res_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___redArg(lean_object* v_P_114_, lean_object* v_A_115_, uint8_t v_i_116_, uint8_t v_j_117_){
_start:
{
lean_object* v_conj_118_; lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; 
v_conj_118_ = lean_ctor_get(v_P_114_, 5);
lean_inc(v_conj_118_);
lean_dec_ref(v_P_114_);
v___x_119_ = lean_box(v_j_117_);
v___x_120_ = lean_box(v_i_116_);
v___x_121_ = lean_apply_2(v_A_115_, v___x_119_, v___x_120_);
v___x_122_ = lean_apply_1(v_conj_118_, v___x_121_);
return v___x_122_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___redArg___boxed(lean_object* v_P_123_, lean_object* v_A_124_, lean_object* v_i_125_, lean_object* v_j_126_){
_start:
{
uint8_t v_i_boxed_127_; uint8_t v_j_boxed_128_; lean_object* v_res_129_; 
v_i_boxed_127_ = lean_unbox(v_i_125_);
v_j_boxed_128_ = lean_unbox(v_j_126_);
v_res_129_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___redArg(v_P_123_, v_A_124_, v_i_boxed_127_, v_j_boxed_128_);
return v_res_129_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj(lean_object* v_K_130_, lean_object* v_P_131_, lean_object* v_A_132_, uint8_t v_i_133_, uint8_t v_j_134_){
_start:
{
lean_object* v___x_135_; 
v___x_135_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___redArg(v_P_131_, v_A_132_, v_i_133_, v_j_134_);
return v___x_135_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj___boxed(lean_object* v_K_136_, lean_object* v_P_137_, lean_object* v_A_138_, lean_object* v_i_139_, lean_object* v_j_140_){
_start:
{
uint8_t v_i_boxed_141_; uint8_t v_j_boxed_142_; lean_object* v_res_143_; 
v_i_boxed_141_ = lean_unbox(v_i_139_);
v_j_boxed_142_ = lean_unbox(v_j_140_);
v_res_143_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_adj(v_K_136_, v_P_137_, v_A_138_, v_i_boxed_141_, v_j_boxed_142_);
return v_res_143_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___lam__0(lean_object* v_P_144_, uint8_t v_j_145_, uint8_t v___y_146_){
_start:
{
lean_object* v___x_147_; 
v___x_147_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(v_P_144_, v_j_145_, v___y_146_);
return v___x_147_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___lam__0___boxed(lean_object* v_P_148_, lean_object* v_j_149_, lean_object* v___y_150_){
_start:
{
uint8_t v_j_boxed_151_; uint8_t v___y_19__boxed_152_; lean_object* v_res_153_; 
v_j_boxed_151_ = lean_unbox(v_j_149_);
v___y_19__boxed_152_ = lean_unbox(v___y_150_);
v_res_153_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___lam__0(v_P_148_, v_j_boxed_151_, v___y_19__boxed_152_);
lean_dec_ref(v_P_148_);
return v_res_153_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg(lean_object* v_P_154_, lean_object* v_T_155_, uint8_t v_i_156_, uint8_t v_j_157_){
_start:
{
lean_object* v___x_158_; lean_object* v___f_159_; lean_object* v___x_160_; lean_object* v___x_161_; 
v___x_158_ = lean_box(v_j_157_);
v___f_159_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___lam__0___boxed), 3, 2);
lean_closure_set(v___f_159_, 0, v_P_154_);
lean_closure_set(v___f_159_, 1, v___x_158_);
v___x_160_ = lean_box(v_i_156_);
v___x_161_ = lean_apply_2(v_T_155_, v___f_159_, v___x_160_);
return v___x_161_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg___boxed(lean_object* v_P_162_, lean_object* v_T_163_, lean_object* v_i_164_, lean_object* v_j_165_){
_start:
{
uint8_t v_i_boxed_166_; uint8_t v_j_boxed_167_; lean_object* v_res_168_; 
v_i_boxed_166_ = lean_unbox(v_i_164_);
v_j_boxed_167_ = lean_unbox(v_j_165_);
v_res_168_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg(v_P_162_, v_T_163_, v_i_boxed_166_, v_j_boxed_167_);
return v_res_168_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf(lean_object* v_K_169_, lean_object* v_P_170_, lean_object* v_T_171_, uint8_t v_i_172_, uint8_t v_j_173_){
_start:
{
lean_object* v___x_174_; 
v___x_174_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___redArg(v_P_170_, v_T_171_, v_i_172_, v_j_173_);
return v___x_174_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf___boxed(lean_object* v_K_175_, lean_object* v_P_176_, lean_object* v_T_177_, lean_object* v_i_178_, lean_object* v_j_179_){
_start:
{
uint8_t v_i_boxed_180_; uint8_t v_j_boxed_181_; lean_object* v_res_182_; 
v_i_boxed_180_ = lean_unbox(v_i_178_);
v_j_boxed_181_ = lean_unbox(v_j_179_);
v_res_182_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_matOf(v_K_175_, v_P_176_, v_T_177_, v_i_boxed_180_, v_j_boxed_181_);
return v_res_182_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_endOfMat___redArg(lean_object* v_P_183_, lean_object* v_A_184_){
_start:
{
lean_object* v___x_185_; 
v___x_185_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___boxed), 5, 3);
lean_closure_set(v___x_185_, 0, lean_box(0));
lean_closure_set(v___x_185_, 1, v_P_183_);
lean_closure_set(v___x_185_, 2, v_A_184_);
return v___x_185_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_endOfMat(lean_object* v_K_186_, lean_object* v_P_187_, lean_object* v_A_188_){
_start:
{
lean_object* v___x_189_; 
v___x_189_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_applyMat___boxed), 5, 3);
lean_closure_set(v___x_189_, 0, lean_box(0));
lean_closure_set(v___x_189_, 1, v_P_187_);
lean_closure_set(v___x_189_, 2, v_A_188_);
return v___x_189_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliX(uint8_t v_i_190_, uint8_t v_j_191_){
_start:
{
if (v_i_190_ == 0)
{
if (v_j_191_ == 0)
{
lean_object* v___x_192_; 
v___x_192_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_192_;
}
else
{
lean_object* v___x_193_; 
v___x_193_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_193_;
}
}
else
{
if (v_j_191_ == 0)
{
lean_object* v___x_194_; 
v___x_194_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_194_;
}
else
{
lean_object* v___x_195_; 
v___x_195_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_195_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliX___boxed(lean_object* v_i_196_, lean_object* v_j_197_){
_start:
{
uint8_t v_i_boxed_198_; uint8_t v_j_boxed_199_; lean_object* v_res_200_; 
v_i_boxed_198_ = lean_unbox(v_i_196_);
v_j_boxed_199_ = lean_unbox(v_j_197_);
v_res_200_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliX(v_i_boxed_198_, v_j_boxed_199_);
return v_res_200_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___closed__0(void){
_start:
{
lean_object* v___x_201_; lean_object* v___x_202_; 
v___x_201_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
v___x_202_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_201_);
return v___x_202_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ(uint8_t v_i_203_, uint8_t v_j_204_){
_start:
{
if (v_i_203_ == 0)
{
if (v_j_204_ == 0)
{
goto v___jp_205_;
}
else
{
lean_object* v___x_208_; 
v___x_208_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_208_;
}
}
else
{
if (v_j_204_ == 0)
{
lean_object* v___x_209_; 
v___x_209_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_209_;
}
else
{
goto v___jp_205_;
}
}
v___jp_205_:
{
if (v_i_203_ == 0)
{
lean_object* v___x_206_; 
v___x_206_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_206_;
}
else
{
lean_object* v___x_207_; 
v___x_207_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___closed__0);
return v___x_207_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ___boxed(lean_object* v_i_210_, lean_object* v_j_211_){
_start:
{
uint8_t v_i_boxed_212_; uint8_t v_j_boxed_213_; lean_object* v_res_214_; 
v_i_boxed_212_ = lean_unbox(v_i_210_);
v_j_boxed_213_ = lean_unbox(v_j_211_);
v_res_214_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliZ(v_i_boxed_212_, v_j_boxed_213_);
return v_res_214_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___closed__0(void){
_start:
{
lean_object* v___x_215_; lean_object* v___x_216_; 
v___x_215_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
v___x_216_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_215_);
return v___x_216_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY(uint8_t v_i_217_, uint8_t v_j_218_){
_start:
{
if (v_i_217_ == 0)
{
if (v_j_218_ == 0)
{
lean_object* v___x_222_; 
v___x_222_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_222_;
}
else
{
goto v___jp_219_;
}
}
else
{
if (v_j_218_ == 0)
{
goto v___jp_219_;
}
else
{
lean_object* v___x_223_; 
v___x_223_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_223_;
}
}
v___jp_219_:
{
if (v_i_217_ == 0)
{
lean_object* v___x_220_; 
v___x_220_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___closed__0);
return v___x_220_;
}
else
{
lean_object* v___x_221_; 
v___x_221_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
return v___x_221_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY___boxed(lean_object* v_i_224_, lean_object* v_j_225_){
_start:
{
uint8_t v_i_boxed_226_; uint8_t v_j_boxed_227_; lean_object* v_res_228_; 
v_i_boxed_226_ = lean_unbox(v_i_224_);
v_j_boxed_227_ = lean_unbox(v_j_225_);
v_res_228_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Matrix_pauliY(v_i_boxed_226_, v_j_boxed_227_);
return v_res_228_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H007Complexification(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H017MatrixFiniteRecovery(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H005InnerProductAdmission(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H007Complexification(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
