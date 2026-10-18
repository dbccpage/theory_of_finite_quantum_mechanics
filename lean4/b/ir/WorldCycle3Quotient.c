// Lean compiler output
// Module: WorldCycle3Quotient
// Imports: public import Init public meta import Init public import WorldPresentation
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
uint8_t l_instDecidableEqRat_decEq(lean_object*, lean_object*);
lean_object* l_Rat_add(lean_object*, lean_object*);
lean_object* l_Nat_cast___at___00Dyadic_toRat_spec__0(lean_object*);
lean_object* l_Rat_mul(lean_object*, lean_object*);
lean_object* l_Rat_sub(lean_object*, lean_object*);
uint8_t l_Rat_instDecidableLe(lean_object*, lean_object*);
lean_object* l_Rat_neg(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_scale(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_scale___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_charge(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_repair(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_shiftPotential(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_price(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_l1(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_canonicalPotential(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_canonicalResidual(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_authorityEffect;
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_edge01_3_; lean_object* v_edge12_4_; lean_object* v_edge20_5_; lean_object* v_edge01_6_; lean_object* v_edge12_7_; lean_object* v_edge20_8_; uint8_t v___x_9_; 
v_edge01_3_ = lean_ctor_get(v_x_1_, 0);
v_edge12_4_ = lean_ctor_get(v_x_1_, 1);
v_edge20_5_ = lean_ctor_get(v_x_1_, 2);
v_edge01_6_ = lean_ctor_get(v_x_2_, 0);
v_edge12_7_ = lean_ctor_get(v_x_2_, 1);
v_edge20_8_ = lean_ctor_get(v_x_2_, 2);
v___x_9_ = l_instDecidableEqRat_decEq(v_edge01_3_, v_edge01_6_);
if (v___x_9_ == 0)
{
return v___x_9_;
}
else
{
uint8_t v___x_10_; 
v___x_10_ = l_instDecidableEqRat_decEq(v_edge12_4_, v_edge12_7_);
if (v___x_10_ == 0)
{
return v___x_10_;
}
else
{
uint8_t v___x_11_; 
v___x_11_ = l_instDecidableEqRat_decEq(v_edge20_5_, v_edge20_8_);
return v___x_11_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain_decEq___boxed(lean_object* v_x_12_, lean_object* v_x_13_){
_start:
{
uint8_t v_res_14_; lean_object* v_r_15_; 
v_res_14_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain_decEq(v_x_12_, v_x_13_);
lean_dec_ref(v_x_13_);
lean_dec_ref(v_x_12_);
v_r_15_ = lean_box(v_res_14_);
return v_r_15_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain(lean_object* v_x_16_, lean_object* v_x_17_){
_start:
{
uint8_t v___x_18_; 
v___x_18_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain_decEq(v_x_16_, v_x_17_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain___boxed(lean_object* v_x_19_, lean_object* v_x_20_){
_start:
{
uint8_t v_res_21_; lean_object* v_r_22_; 
v_res_21_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqCochain(v_x_19_, v_x_20_);
lean_dec_ref(v_x_20_);
lean_dec_ref(v_x_19_);
v_r_22_ = lean_box(v_res_21_);
return v_r_22_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential_decEq(lean_object* v_x_23_, lean_object* v_x_24_){
_start:
{
lean_object* v_vertex0_25_; lean_object* v_vertex1_26_; lean_object* v_vertex2_27_; lean_object* v_vertex0_28_; lean_object* v_vertex1_29_; lean_object* v_vertex2_30_; uint8_t v___x_31_; 
v_vertex0_25_ = lean_ctor_get(v_x_23_, 0);
v_vertex1_26_ = lean_ctor_get(v_x_23_, 1);
v_vertex2_27_ = lean_ctor_get(v_x_23_, 2);
v_vertex0_28_ = lean_ctor_get(v_x_24_, 0);
v_vertex1_29_ = lean_ctor_get(v_x_24_, 1);
v_vertex2_30_ = lean_ctor_get(v_x_24_, 2);
v___x_31_ = l_instDecidableEqRat_decEq(v_vertex0_25_, v_vertex0_28_);
if (v___x_31_ == 0)
{
return v___x_31_;
}
else
{
uint8_t v___x_32_; 
v___x_32_ = l_instDecidableEqRat_decEq(v_vertex1_26_, v_vertex1_29_);
if (v___x_32_ == 0)
{
return v___x_32_;
}
else
{
uint8_t v___x_33_; 
v___x_33_ = l_instDecidableEqRat_decEq(v_vertex2_27_, v_vertex2_30_);
return v___x_33_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential_decEq___boxed(lean_object* v_x_34_, lean_object* v_x_35_){
_start:
{
uint8_t v_res_36_; lean_object* v_r_37_; 
v_res_36_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential_decEq(v_x_34_, v_x_35_);
lean_dec_ref(v_x_35_);
lean_dec_ref(v_x_34_);
v_r_37_ = lean_box(v_res_36_);
return v_r_37_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential(lean_object* v_x_38_, lean_object* v_x_39_){
_start:
{
uint8_t v___x_40_; 
v___x_40_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential_decEq(v_x_38_, v_x_39_);
return v___x_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential___boxed(lean_object* v_x_41_, lean_object* v_x_42_){
_start:
{
uint8_t v_res_43_; lean_object* v_r_44_; 
v_res_43_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_instDecidableEqPotential(v_x_41_, v_x_42_);
lean_dec_ref(v_x_42_);
lean_dec_ref(v_x_41_);
v_r_44_ = lean_box(v_res_43_);
return v_r_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_add(lean_object* v_left_45_, lean_object* v_right_46_){
_start:
{
lean_object* v_edge01_47_; lean_object* v_edge12_48_; lean_object* v_edge20_49_; lean_object* v_edge01_50_; lean_object* v_edge12_51_; lean_object* v_edge20_52_; lean_object* v___x_54_; uint8_t v_isShared_55_; uint8_t v_isSharedCheck_62_; 
v_edge01_47_ = lean_ctor_get(v_left_45_, 0);
lean_inc_ref(v_edge01_47_);
v_edge12_48_ = lean_ctor_get(v_left_45_, 1);
lean_inc_ref(v_edge12_48_);
v_edge20_49_ = lean_ctor_get(v_left_45_, 2);
lean_inc_ref(v_edge20_49_);
lean_dec_ref(v_left_45_);
v_edge01_50_ = lean_ctor_get(v_right_46_, 0);
v_edge12_51_ = lean_ctor_get(v_right_46_, 1);
v_edge20_52_ = lean_ctor_get(v_right_46_, 2);
v_isSharedCheck_62_ = !lean_is_exclusive(v_right_46_);
if (v_isSharedCheck_62_ == 0)
{
v___x_54_ = v_right_46_;
v_isShared_55_ = v_isSharedCheck_62_;
goto v_resetjp_53_;
}
else
{
lean_inc(v_edge20_52_);
lean_inc(v_edge12_51_);
lean_inc(v_edge01_50_);
lean_dec(v_right_46_);
v___x_54_ = lean_box(0);
v_isShared_55_ = v_isSharedCheck_62_;
goto v_resetjp_53_;
}
v_resetjp_53_:
{
lean_object* v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; lean_object* v___x_60_; 
v___x_56_ = l_Rat_add(v_edge01_47_, v_edge01_50_);
v___x_57_ = l_Rat_add(v_edge12_48_, v_edge12_51_);
v___x_58_ = l_Rat_add(v_edge20_49_, v_edge20_52_);
if (v_isShared_55_ == 0)
{
lean_ctor_set(v___x_54_, 2, v___x_58_);
lean_ctor_set(v___x_54_, 1, v___x_57_);
lean_ctor_set(v___x_54_, 0, v___x_56_);
v___x_60_ = v___x_54_;
goto v_reusejp_59_;
}
else
{
lean_object* v_reuseFailAlloc_61_; 
v_reuseFailAlloc_61_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_61_, 0, v___x_56_);
lean_ctor_set(v_reuseFailAlloc_61_, 1, v___x_57_);
lean_ctor_set(v_reuseFailAlloc_61_, 2, v___x_58_);
v___x_60_ = v_reuseFailAlloc_61_;
goto v_reusejp_59_;
}
v_reusejp_59_:
{
return v___x_60_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_neg(lean_object* v_q_63_){
_start:
{
lean_object* v_edge01_64_; lean_object* v_edge12_65_; lean_object* v_edge20_66_; lean_object* v___x_68_; uint8_t v_isShared_69_; uint8_t v_isSharedCheck_76_; 
v_edge01_64_ = lean_ctor_get(v_q_63_, 0);
v_edge12_65_ = lean_ctor_get(v_q_63_, 1);
v_edge20_66_ = lean_ctor_get(v_q_63_, 2);
v_isSharedCheck_76_ = !lean_is_exclusive(v_q_63_);
if (v_isSharedCheck_76_ == 0)
{
v___x_68_ = v_q_63_;
v_isShared_69_ = v_isSharedCheck_76_;
goto v_resetjp_67_;
}
else
{
lean_inc(v_edge20_66_);
lean_inc(v_edge12_65_);
lean_inc(v_edge01_64_);
lean_dec(v_q_63_);
v___x_68_ = lean_box(0);
v_isShared_69_ = v_isSharedCheck_76_;
goto v_resetjp_67_;
}
v_resetjp_67_:
{
lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_74_; 
v___x_70_ = l_Rat_neg(v_edge01_64_);
v___x_71_ = l_Rat_neg(v_edge12_65_);
v___x_72_ = l_Rat_neg(v_edge20_66_);
if (v_isShared_69_ == 0)
{
lean_ctor_set(v___x_68_, 2, v___x_72_);
lean_ctor_set(v___x_68_, 1, v___x_71_);
lean_ctor_set(v___x_68_, 0, v___x_70_);
v___x_74_ = v___x_68_;
goto v_reusejp_73_;
}
else
{
lean_object* v_reuseFailAlloc_75_; 
v_reuseFailAlloc_75_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_75_, 0, v___x_70_);
lean_ctor_set(v_reuseFailAlloc_75_, 1, v___x_71_);
lean_ctor_set(v_reuseFailAlloc_75_, 2, v___x_72_);
v___x_74_ = v_reuseFailAlloc_75_;
goto v_reusejp_73_;
}
v_reusejp_73_:
{
return v___x_74_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_sub(lean_object* v_left_77_, lean_object* v_right_78_){
_start:
{
lean_object* v___x_79_; lean_object* v___x_80_; 
v___x_79_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_neg(v_right_78_);
v___x_80_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_add(v_left_77_, v___x_79_);
return v___x_80_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_scale(lean_object* v_scalar_81_, lean_object* v_q_82_){
_start:
{
lean_object* v_edge01_83_; lean_object* v_edge12_84_; lean_object* v_edge20_85_; lean_object* v___x_87_; uint8_t v_isShared_88_; uint8_t v_isSharedCheck_95_; 
v_edge01_83_ = lean_ctor_get(v_q_82_, 0);
v_edge12_84_ = lean_ctor_get(v_q_82_, 1);
v_edge20_85_ = lean_ctor_get(v_q_82_, 2);
v_isSharedCheck_95_ = !lean_is_exclusive(v_q_82_);
if (v_isSharedCheck_95_ == 0)
{
v___x_87_ = v_q_82_;
v_isShared_88_ = v_isSharedCheck_95_;
goto v_resetjp_86_;
}
else
{
lean_inc(v_edge20_85_);
lean_inc(v_edge12_84_);
lean_inc(v_edge01_83_);
lean_dec(v_q_82_);
v___x_87_ = lean_box(0);
v_isShared_88_ = v_isSharedCheck_95_;
goto v_resetjp_86_;
}
v_resetjp_86_:
{
lean_object* v___x_89_; lean_object* v___x_90_; lean_object* v___x_91_; lean_object* v___x_93_; 
v___x_89_ = l_Rat_mul(v_scalar_81_, v_edge01_83_);
v___x_90_ = l_Rat_mul(v_scalar_81_, v_edge12_84_);
v___x_91_ = l_Rat_mul(v_scalar_81_, v_edge20_85_);
if (v_isShared_88_ == 0)
{
lean_ctor_set(v___x_87_, 2, v___x_91_);
lean_ctor_set(v___x_87_, 1, v___x_90_);
lean_ctor_set(v___x_87_, 0, v___x_89_);
v___x_93_ = v___x_87_;
goto v_reusejp_92_;
}
else
{
lean_object* v_reuseFailAlloc_94_; 
v_reuseFailAlloc_94_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_94_, 0, v___x_89_);
lean_ctor_set(v_reuseFailAlloc_94_, 1, v___x_90_);
lean_ctor_set(v_reuseFailAlloc_94_, 2, v___x_91_);
v___x_93_ = v_reuseFailAlloc_94_;
goto v_reusejp_92_;
}
v_reusejp_92_:
{
return v___x_93_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_scale___boxed(lean_object* v_scalar_96_, lean_object* v_q_97_){
_start:
{
lean_object* v_res_98_; 
v_res_98_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_scale(v_scalar_96_, v_q_97_);
lean_dec_ref(v_scalar_96_);
return v_res_98_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_charge(lean_object* v_q_99_){
_start:
{
lean_object* v_edge01_100_; lean_object* v_edge12_101_; lean_object* v_edge20_102_; lean_object* v___x_103_; lean_object* v___x_104_; 
v_edge01_100_ = lean_ctor_get(v_q_99_, 0);
lean_inc_ref(v_edge01_100_);
v_edge12_101_ = lean_ctor_get(v_q_99_, 1);
lean_inc_ref(v_edge12_101_);
v_edge20_102_ = lean_ctor_get(v_q_99_, 2);
lean_inc_ref(v_edge20_102_);
lean_dec_ref(v_q_99_);
v___x_103_ = l_Rat_add(v_edge01_100_, v_edge12_101_);
v___x_104_ = l_Rat_add(v___x_103_, v_edge20_102_);
return v___x_104_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_repair(lean_object* v_potential_105_){
_start:
{
lean_object* v_vertex0_106_; lean_object* v_vertex1_107_; lean_object* v_vertex2_108_; lean_object* v___x_110_; uint8_t v_isShared_111_; uint8_t v_isSharedCheck_118_; 
v_vertex0_106_ = lean_ctor_get(v_potential_105_, 0);
v_vertex1_107_ = lean_ctor_get(v_potential_105_, 1);
v_vertex2_108_ = lean_ctor_get(v_potential_105_, 2);
v_isSharedCheck_118_ = !lean_is_exclusive(v_potential_105_);
if (v_isSharedCheck_118_ == 0)
{
v___x_110_ = v_potential_105_;
v_isShared_111_ = v_isSharedCheck_118_;
goto v_resetjp_109_;
}
else
{
lean_inc(v_vertex2_108_);
lean_inc(v_vertex1_107_);
lean_inc(v_vertex0_106_);
lean_dec(v_potential_105_);
v___x_110_ = lean_box(0);
v_isShared_111_ = v_isSharedCheck_118_;
goto v_resetjp_109_;
}
v_resetjp_109_:
{
lean_object* v___x_112_; lean_object* v___x_113_; lean_object* v___x_114_; lean_object* v___x_116_; 
lean_inc_ref(v_vertex0_106_);
lean_inc_ref(v_vertex1_107_);
v___x_112_ = l_Rat_sub(v_vertex1_107_, v_vertex0_106_);
lean_inc_ref(v_vertex2_108_);
v___x_113_ = l_Rat_sub(v_vertex2_108_, v_vertex1_107_);
v___x_114_ = l_Rat_sub(v_vertex0_106_, v_vertex2_108_);
if (v_isShared_111_ == 0)
{
lean_ctor_set(v___x_110_, 2, v___x_114_);
lean_ctor_set(v___x_110_, 1, v___x_113_);
lean_ctor_set(v___x_110_, 0, v___x_112_);
v___x_116_ = v___x_110_;
goto v_reusejp_115_;
}
else
{
lean_object* v_reuseFailAlloc_117_; 
v_reuseFailAlloc_117_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_117_, 0, v___x_112_);
lean_ctor_set(v_reuseFailAlloc_117_, 1, v___x_113_);
lean_ctor_set(v_reuseFailAlloc_117_, 2, v___x_114_);
v___x_116_ = v_reuseFailAlloc_117_;
goto v_reusejp_115_;
}
v_reusejp_115_:
{
return v___x_116_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_shiftPotential(lean_object* v_offset_119_, lean_object* v_potential_120_){
_start:
{
lean_object* v_vertex0_121_; lean_object* v_vertex1_122_; lean_object* v_vertex2_123_; lean_object* v___x_125_; uint8_t v_isShared_126_; uint8_t v_isSharedCheck_133_; 
v_vertex0_121_ = lean_ctor_get(v_potential_120_, 0);
v_vertex1_122_ = lean_ctor_get(v_potential_120_, 1);
v_vertex2_123_ = lean_ctor_get(v_potential_120_, 2);
v_isSharedCheck_133_ = !lean_is_exclusive(v_potential_120_);
if (v_isSharedCheck_133_ == 0)
{
v___x_125_ = v_potential_120_;
v_isShared_126_ = v_isSharedCheck_133_;
goto v_resetjp_124_;
}
else
{
lean_inc(v_vertex2_123_);
lean_inc(v_vertex1_122_);
lean_inc(v_vertex0_121_);
lean_dec(v_potential_120_);
v___x_125_ = lean_box(0);
v_isShared_126_ = v_isSharedCheck_133_;
goto v_resetjp_124_;
}
v_resetjp_124_:
{
lean_object* v___x_127_; lean_object* v___x_128_; lean_object* v___x_129_; lean_object* v___x_131_; 
lean_inc_ref_n(v_offset_119_, 2);
v___x_127_ = l_Rat_add(v_vertex0_121_, v_offset_119_);
v___x_128_ = l_Rat_add(v_vertex1_122_, v_offset_119_);
v___x_129_ = l_Rat_add(v_vertex2_123_, v_offset_119_);
if (v_isShared_126_ == 0)
{
lean_ctor_set(v___x_125_, 2, v___x_129_);
lean_ctor_set(v___x_125_, 1, v___x_128_);
lean_ctor_set(v___x_125_, 0, v___x_127_);
v___x_131_ = v___x_125_;
goto v_reusejp_130_;
}
else
{
lean_object* v_reuseFailAlloc_132_; 
v_reuseFailAlloc_132_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_132_, 0, v___x_127_);
lean_ctor_set(v_reuseFailAlloc_132_, 1, v___x_128_);
lean_ctor_set(v_reuseFailAlloc_132_, 2, v___x_129_);
v___x_131_ = v_reuseFailAlloc_132_;
goto v_reusejp_130_;
}
v_reusejp_130_:
{
return v___x_131_;
}
}
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0(void){
_start:
{
lean_object* v___x_134_; lean_object* v___x_135_; 
v___x_134_ = lean_unsigned_to_nat(0u);
v___x_135_ = l_Nat_cast___at___00Dyadic_toRat_spec__0(v___x_134_);
return v___x_135_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs(lean_object* v_x_136_){
_start:
{
lean_object* v___x_137_; uint8_t v___x_138_; 
v___x_137_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0, &lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0);
lean_inc_ref(v_x_136_);
v___x_138_ = l_Rat_instDecidableLe(v___x_137_, v_x_136_);
if (v___x_138_ == 0)
{
lean_object* v___x_139_; 
v___x_139_ = l_Rat_neg(v_x_136_);
return v___x_139_;
}
else
{
return v_x_136_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_price(lean_object* v_q_140_){
_start:
{
lean_object* v___x_141_; lean_object* v___x_142_; 
v___x_141_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_charge(v_q_140_);
v___x_142_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs(v___x_141_);
return v___x_142_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_l1(lean_object* v_q_143_){
_start:
{
lean_object* v_edge01_144_; lean_object* v_edge12_145_; lean_object* v_edge20_146_; lean_object* v___x_147_; lean_object* v___x_148_; lean_object* v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; 
v_edge01_144_ = lean_ctor_get(v_q_143_, 0);
lean_inc_ref(v_edge01_144_);
v_edge12_145_ = lean_ctor_get(v_q_143_, 1);
lean_inc_ref(v_edge12_145_);
v_edge20_146_ = lean_ctor_get(v_q_143_, 2);
lean_inc_ref(v_edge20_146_);
lean_dec_ref(v_q_143_);
v___x_147_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs(v_edge01_144_);
v___x_148_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs(v_edge12_145_);
v___x_149_ = l_Rat_add(v___x_147_, v___x_148_);
v___x_150_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs(v_edge20_146_);
v___x_151_ = l_Rat_add(v___x_149_, v___x_150_);
return v___x_151_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_canonicalPotential(lean_object* v_q_152_){
_start:
{
lean_object* v_edge01_153_; lean_object* v_edge12_154_; lean_object* v___x_156_; uint8_t v_isShared_157_; uint8_t v_isSharedCheck_163_; 
v_edge01_153_ = lean_ctor_get(v_q_152_, 0);
v_edge12_154_ = lean_ctor_get(v_q_152_, 1);
v_isSharedCheck_163_ = !lean_is_exclusive(v_q_152_);
if (v_isSharedCheck_163_ == 0)
{
lean_object* v_unused_164_; 
v_unused_164_ = lean_ctor_get(v_q_152_, 2);
lean_dec(v_unused_164_);
v___x_156_ = v_q_152_;
v_isShared_157_ = v_isSharedCheck_163_;
goto v_resetjp_155_;
}
else
{
lean_inc(v_edge12_154_);
lean_inc(v_edge01_153_);
lean_dec(v_q_152_);
v___x_156_ = lean_box(0);
v_isShared_157_ = v_isSharedCheck_163_;
goto v_resetjp_155_;
}
v_resetjp_155_:
{
lean_object* v___x_158_; lean_object* v___x_159_; lean_object* v___x_161_; 
v___x_158_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0, &lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0);
lean_inc_ref(v_edge01_153_);
v___x_159_ = l_Rat_add(v_edge01_153_, v_edge12_154_);
if (v_isShared_157_ == 0)
{
lean_ctor_set(v___x_156_, 2, v___x_159_);
lean_ctor_set(v___x_156_, 1, v_edge01_153_);
lean_ctor_set(v___x_156_, 0, v___x_158_);
v___x_161_ = v___x_156_;
goto v_reusejp_160_;
}
else
{
lean_object* v_reuseFailAlloc_162_; 
v_reuseFailAlloc_162_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_162_, 0, v___x_158_);
lean_ctor_set(v_reuseFailAlloc_162_, 1, v_edge01_153_);
lean_ctor_set(v_reuseFailAlloc_162_, 2, v___x_159_);
v___x_161_ = v_reuseFailAlloc_162_;
goto v_reusejp_160_;
}
v_reusejp_160_:
{
return v___x_161_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_canonicalResidual(lean_object* v_q_165_){
_start:
{
lean_object* v___x_166_; lean_object* v___x_167_; lean_object* v___x_168_; 
v___x_166_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0, &lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_ratAbs___closed__0);
v___x_167_ = lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_charge(v_q_165_);
v___x_168_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_168_, 0, v___x_166_);
lean_ctor_set(v___x_168_, 1, v___x_166_);
lean_ctor_set(v___x_168_, 2, v___x_167_);
return v___x_168_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_authorityEffect(void){
_start:
{
lean_object* v___x_169_; 
v___x_169_ = lean_box(0);
return v___x_169_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_WorldPresentation(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldCycle3Quotient(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_WorldPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_authorityEffect = _init_lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_authorityEffect();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_Cycle3Quotient_authorityEffect);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
