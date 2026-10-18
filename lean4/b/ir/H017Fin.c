// Lean compiler output
// Module: H017Fin
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H005InnerProductAdmission public import H017MatrixFiniteRecovery
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
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_List_mapTR_loop___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_applyMat_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_applyMat_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_mmul_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_mmul___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_mmul(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_mmul_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_adj___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_adj(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_matOf___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_matOf(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_endOfMat___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_endOfMat(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_applyMat_spec__0___redArg(lean_object* v_P_1_, lean_object* v_A_2_, lean_object* v_i_3_, lean_object* v_v_4_, lean_object* v_a_5_, lean_object* v_a_6_){
_start:
{
if (lean_obj_tag(v_a_5_) == 0)
{
lean_object* v___x_7_; 
lean_dec(v_v_4_);
lean_dec(v_i_3_);
lean_dec(v_A_2_);
lean_dec_ref(v_P_1_);
v___x_7_ = l_List_reverse___redArg(v_a_6_);
return v___x_7_;
}
else
{
lean_object* v_head_8_; lean_object* v_tail_9_; lean_object* v___x_11_; uint8_t v_isShared_12_; uint8_t v_isSharedCheck_21_; 
v_head_8_ = lean_ctor_get(v_a_5_, 0);
v_tail_9_ = lean_ctor_get(v_a_5_, 1);
v_isSharedCheck_21_ = !lean_is_exclusive(v_a_5_);
if (v_isSharedCheck_21_ == 0)
{
v___x_11_ = v_a_5_;
v_isShared_12_ = v_isSharedCheck_21_;
goto v_resetjp_10_;
}
else
{
lean_inc(v_tail_9_);
lean_inc(v_head_8_);
lean_dec(v_a_5_);
v___x_11_ = lean_box(0);
v_isShared_12_ = v_isSharedCheck_21_;
goto v_resetjp_10_;
}
v_resetjp_10_:
{
lean_object* v_mul_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_18_; 
v_mul_13_ = lean_ctor_get(v_P_1_, 1);
lean_inc(v_A_2_);
lean_inc(v_head_8_);
lean_inc(v_i_3_);
v___x_14_ = lean_apply_2(v_A_2_, v_i_3_, v_head_8_);
lean_inc(v_v_4_);
v___x_15_ = lean_apply_1(v_v_4_, v_head_8_);
lean_inc(v_mul_13_);
v___x_16_ = lean_apply_2(v_mul_13_, v___x_14_, v___x_15_);
if (v_isShared_12_ == 0)
{
lean_ctor_set(v___x_11_, 1, v_a_6_);
lean_ctor_set(v___x_11_, 0, v___x_16_);
v___x_18_ = v___x_11_;
goto v_reusejp_17_;
}
else
{
lean_object* v_reuseFailAlloc_20_; 
v_reuseFailAlloc_20_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_20_, 0, v___x_16_);
lean_ctor_set(v_reuseFailAlloc_20_, 1, v_a_6_);
v___x_18_ = v_reuseFailAlloc_20_;
goto v_reusejp_17_;
}
v_reusejp_17_:
{
v_a_5_ = v_tail_9_;
v_a_6_ = v___x_18_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat___redArg(lean_object* v_P_22_, lean_object* v_E_23_, lean_object* v_A_24_, lean_object* v_v_25_, lean_object* v_i_26_){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; 
v___x_27_ = lean_box(0);
lean_inc_ref(v_P_22_);
v___x_28_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_applyMat_spec__0___redArg(v_P_22_, v_A_24_, v_i_26_, v_v_25_, v_E_23_, v___x_27_);
v___x_29_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_22_, v___x_28_);
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat(lean_object* v_K_30_, lean_object* v_Q_31_, lean_object* v_P_32_, lean_object* v_E_33_, lean_object* v_A_34_, lean_object* v_v_35_, lean_object* v_i_36_){
_start:
{
lean_object* v___x_37_; 
v___x_37_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat___redArg(v_P_32_, v_E_33_, v_A_34_, v_v_35_, v_i_36_);
return v___x_37_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_applyMat_spec__0(lean_object* v_Q_38_, lean_object* v_K_39_, lean_object* v_P_40_, lean_object* v_A_41_, lean_object* v_i_42_, lean_object* v_v_43_, lean_object* v_a_44_, lean_object* v_a_45_){
_start:
{
lean_object* v___x_46_; 
v___x_46_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_applyMat_spec__0___redArg(v_P_40_, v_A_41_, v_i_42_, v_v_43_, v_a_44_, v_a_45_);
return v___x_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_mmul_spec__0___redArg(lean_object* v_P_47_, lean_object* v_A_48_, lean_object* v_i_49_, lean_object* v_B_50_, lean_object* v_j_51_, lean_object* v_a_52_, lean_object* v_a_53_){
_start:
{
if (lean_obj_tag(v_a_52_) == 0)
{
lean_object* v___x_54_; 
lean_dec(v_j_51_);
lean_dec(v_B_50_);
lean_dec(v_i_49_);
lean_dec(v_A_48_);
lean_dec_ref(v_P_47_);
v___x_54_ = l_List_reverse___redArg(v_a_53_);
return v___x_54_;
}
else
{
lean_object* v_head_55_; lean_object* v_tail_56_; lean_object* v___x_58_; uint8_t v_isShared_59_; uint8_t v_isSharedCheck_68_; 
v_head_55_ = lean_ctor_get(v_a_52_, 0);
v_tail_56_ = lean_ctor_get(v_a_52_, 1);
v_isSharedCheck_68_ = !lean_is_exclusive(v_a_52_);
if (v_isSharedCheck_68_ == 0)
{
v___x_58_ = v_a_52_;
v_isShared_59_ = v_isSharedCheck_68_;
goto v_resetjp_57_;
}
else
{
lean_inc(v_tail_56_);
lean_inc(v_head_55_);
lean_dec(v_a_52_);
v___x_58_ = lean_box(0);
v_isShared_59_ = v_isSharedCheck_68_;
goto v_resetjp_57_;
}
v_resetjp_57_:
{
lean_object* v_mul_60_; lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_65_; 
v_mul_60_ = lean_ctor_get(v_P_47_, 1);
lean_inc(v_A_48_);
lean_inc(v_head_55_);
lean_inc(v_i_49_);
v___x_61_ = lean_apply_2(v_A_48_, v_i_49_, v_head_55_);
lean_inc(v_B_50_);
lean_inc(v_j_51_);
v___x_62_ = lean_apply_2(v_B_50_, v_head_55_, v_j_51_);
lean_inc(v_mul_60_);
v___x_63_ = lean_apply_2(v_mul_60_, v___x_61_, v___x_62_);
if (v_isShared_59_ == 0)
{
lean_ctor_set(v___x_58_, 1, v_a_53_);
lean_ctor_set(v___x_58_, 0, v___x_63_);
v___x_65_ = v___x_58_;
goto v_reusejp_64_;
}
else
{
lean_object* v_reuseFailAlloc_67_; 
v_reuseFailAlloc_67_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_67_, 0, v___x_63_);
lean_ctor_set(v_reuseFailAlloc_67_, 1, v_a_53_);
v___x_65_ = v_reuseFailAlloc_67_;
goto v_reusejp_64_;
}
v_reusejp_64_:
{
v_a_52_ = v_tail_56_;
v_a_53_ = v___x_65_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_mmul___redArg(lean_object* v_P_69_, lean_object* v_E_70_, lean_object* v_A_71_, lean_object* v_B_72_, lean_object* v_i_73_, lean_object* v_j_74_){
_start:
{
lean_object* v___x_75_; lean_object* v___x_76_; lean_object* v___x_77_; 
v___x_75_ = lean_box(0);
lean_inc_ref(v_P_69_);
v___x_76_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_mmul_spec__0___redArg(v_P_69_, v_A_71_, v_i_73_, v_B_72_, v_j_74_, v_E_70_, v___x_75_);
v___x_77_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_69_, v___x_76_);
return v___x_77_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_mmul(lean_object* v_K_78_, lean_object* v_Q_79_, lean_object* v_P_80_, lean_object* v_E_81_, lean_object* v_A_82_, lean_object* v_B_83_, lean_object* v_i_84_, lean_object* v_j_85_){
_start:
{
lean_object* v___x_86_; 
v___x_86_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_mmul___redArg(v_P_80_, v_E_81_, v_A_82_, v_B_83_, v_i_84_, v_j_85_);
return v___x_86_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_mmul_spec__0(lean_object* v_Q_87_, lean_object* v_K_88_, lean_object* v_P_89_, lean_object* v_A_90_, lean_object* v_i_91_, lean_object* v_B_92_, lean_object* v_j_93_, lean_object* v_a_94_, lean_object* v_a_95_){
_start:
{
lean_object* v___x_96_; 
v___x_96_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H017Fin_mmul_spec__0___redArg(v_P_89_, v_A_90_, v_i_91_, v_B_92_, v_j_93_, v_a_94_, v_a_95_);
return v___x_96_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___redArg(lean_object* v_P_97_, lean_object* v_inst_98_, lean_object* v_i_99_, lean_object* v_j_100_){
_start:
{
lean_object* v___x_101_; uint8_t v___x_102_; 
v___x_101_ = lean_apply_2(v_inst_98_, v_i_99_, v_j_100_);
v___x_102_ = lean_unbox(v___x_101_);
if (v___x_102_ == 0)
{
lean_object* v_zero_103_; 
v_zero_103_ = lean_ctor_get(v_P_97_, 3);
lean_inc(v_zero_103_);
return v_zero_103_;
}
else
{
lean_object* v_one_104_; 
v_one_104_ = lean_ctor_get(v_P_97_, 4);
lean_inc(v_one_104_);
return v_one_104_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___redArg___boxed(lean_object* v_P_105_, lean_object* v_inst_106_, lean_object* v_i_107_, lean_object* v_j_108_){
_start:
{
lean_object* v_res_109_; 
v_res_109_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___redArg(v_P_105_, v_inst_106_, v_i_107_, v_j_108_);
lean_dec_ref(v_P_105_);
return v_res_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident(lean_object* v_K_110_, lean_object* v_Q_111_, lean_object* v_P_112_, lean_object* v_inst_113_, lean_object* v_i_114_, lean_object* v_j_115_){
_start:
{
lean_object* v___x_116_; 
v___x_116_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___redArg(v_P_112_, v_inst_113_, v_i_114_, v_j_115_);
return v___x_116_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident___boxed(lean_object* v_K_117_, lean_object* v_Q_118_, lean_object* v_P_119_, lean_object* v_inst_120_, lean_object* v_i_121_, lean_object* v_j_122_){
_start:
{
lean_object* v_res_123_; 
v_res_123_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_ident(v_K_117_, v_Q_118_, v_P_119_, v_inst_120_, v_i_121_, v_j_122_);
lean_dec_ref(v_P_119_);
return v_res_123_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_adj___redArg(lean_object* v_P_124_, lean_object* v_A_125_, lean_object* v_i_126_, lean_object* v_j_127_){
_start:
{
lean_object* v_conj_128_; lean_object* v___x_129_; lean_object* v___x_130_; 
v_conj_128_ = lean_ctor_get(v_P_124_, 5);
lean_inc(v_conj_128_);
lean_dec_ref(v_P_124_);
v___x_129_ = lean_apply_2(v_A_125_, v_j_127_, v_i_126_);
v___x_130_ = lean_apply_1(v_conj_128_, v___x_129_);
return v___x_130_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_adj(lean_object* v_K_131_, lean_object* v_Q_132_, lean_object* v_P_133_, lean_object* v_A_134_, lean_object* v_i_135_, lean_object* v_j_136_){
_start:
{
lean_object* v___x_137_; 
v___x_137_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_adj___redArg(v_P_133_, v_A_134_, v_i_135_, v_j_136_);
return v___x_137_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_matOf___redArg(lean_object* v_inst_138_, lean_object* v_P_139_, lean_object* v_T_140_, lean_object* v_i_141_, lean_object* v_j_142_){
_start:
{
lean_object* v___x_143_; lean_object* v___x_144_; 
v___x_143_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___boxed), 6, 5);
lean_closure_set(v___x_143_, 0, lean_box(0));
lean_closure_set(v___x_143_, 1, lean_box(0));
lean_closure_set(v___x_143_, 2, v_P_139_);
lean_closure_set(v___x_143_, 3, v_inst_138_);
lean_closure_set(v___x_143_, 4, v_j_142_);
v___x_144_ = lean_apply_2(v_T_140_, v___x_143_, v_i_141_);
return v___x_144_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_matOf(lean_object* v_K_145_, lean_object* v_Q_146_, lean_object* v_inst_147_, lean_object* v_P_148_, lean_object* v_T_149_, lean_object* v_i_150_, lean_object* v_j_151_){
_start:
{
lean_object* v___x_152_; 
v___x_152_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_matOf___redArg(v_inst_147_, v_P_148_, v_T_149_, v_i_150_, v_j_151_);
return v___x_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_endOfMat___redArg(lean_object* v_P_153_, lean_object* v_E_154_, lean_object* v_A_155_){
_start:
{
lean_object* v___x_156_; 
v___x_156_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat), 7, 5);
lean_closure_set(v___x_156_, 0, lean_box(0));
lean_closure_set(v___x_156_, 1, lean_box(0));
lean_closure_set(v___x_156_, 2, v_P_153_);
lean_closure_set(v___x_156_, 3, v_E_154_);
lean_closure_set(v___x_156_, 4, v_A_155_);
return v___x_156_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_endOfMat(lean_object* v_K_157_, lean_object* v_Q_158_, lean_object* v_P_159_, lean_object* v_E_160_, lean_object* v_A_161_){
_start:
{
lean_object* v___x_162_; 
v___x_162_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_applyMat), 7, 5);
lean_closure_set(v___x_162_, 0, lean_box(0));
lean_closure_set(v___x_162_, 1, lean_box(0));
lean_closure_set(v___x_162_, 2, v_P_159_);
lean_closure_set(v___x_162_, 3, v_E_160_);
lean_closure_set(v___x_162_, 4, v_A_161_);
return v___x_162_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn___redArg___lam__0(lean_object* v_P_163_, lean_object* v_v_164_, lean_object* v_inst_165_, lean_object* v_x_166_, lean_object* v_j_167_){
_start:
{
lean_object* v_mul_168_; lean_object* v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; 
v_mul_168_ = lean_ctor_get(v_P_163_, 1);
lean_inc(v_mul_168_);
lean_inc(v_j_167_);
v___x_169_ = lean_apply_1(v_v_164_, v_j_167_);
v___x_170_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg(v_P_163_, v_inst_165_, v_j_167_, v_x_166_);
lean_dec_ref(v_P_163_);
v___x_171_ = lean_apply_2(v_mul_168_, v___x_169_, v___x_170_);
return v___x_171_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn___redArg(lean_object* v_inst_172_, lean_object* v_P_173_, lean_object* v_v_174_, lean_object* v_l_175_, lean_object* v_x_176_){
_start:
{
lean_object* v___f_177_; lean_object* v___x_178_; lean_object* v___x_179_; lean_object* v___x_180_; 
lean_inc_ref(v_P_173_);
v___f_177_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn___redArg___lam__0), 5, 4);
lean_closure_set(v___f_177_, 0, v_P_173_);
lean_closure_set(v___f_177_, 1, v_v_174_);
lean_closure_set(v___f_177_, 2, v_inst_172_);
lean_closure_set(v___f_177_, 3, v_x_176_);
v___x_178_ = lean_box(0);
v___x_179_ = l_List_mapTR_loop___redArg(v___f_177_, v_l_175_, v___x_178_);
v___x_180_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_173_, v___x_179_);
return v___x_180_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn(lean_object* v_K_181_, lean_object* v_Q_182_, lean_object* v_inst_183_, lean_object* v_P_184_, lean_object* v_v_185_, lean_object* v_l_186_, lean_object* v_x_187_){
_start:
{
lean_object* v___x_188_; 
v___x_188_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017Fin_expandOn___redArg(v_inst_183_, v_P_184_, v_v_185_, v_l_186_, v_x_187_);
return v___x_188_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H017MatrixFiniteRecovery(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H017Fin(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H017MatrixFiniteRecovery(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
