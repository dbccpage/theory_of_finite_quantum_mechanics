// Lean compiler output
// Module: U1AngleAddition
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_U1AngleAddition_Coord2_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_U1AngleAddition_instDecidableEqCoord2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_instDecidableEqCoord2___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_U1AngleAddition_id2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_U1AngleAddition_id2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_U1AngleAddition_id2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_U1AngleAddition_id2___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_id2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_id2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_mul2(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_mul2___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_transpose2(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_transpose2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_det2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_rotMat(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_rotMat___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_U1AngleAddition_circleId___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_U1AngleAddition_circleId___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_circleId;
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_J(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_J___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx(uint8_t v_x_1_){
_start:
{
if (v_x_1_ == 0)
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
else
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(1u);
return v___x_3_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_toCtorIdx(uint8_t v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_toCtorIdx___boxed(lean_object* v_x_9_){
_start:
{
uint8_t v_x_4__boxed_10_; lean_object* v_res_11_; 
v_x_4__boxed_10_ = lean_unbox(v_x_9_);
v_res_11_ = lp_FiniteQuantum_U1AngleAddition_Coord2_toCtorIdx(v_x_4__boxed_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___redArg(lean_object* v_k_12_){
_start:
{
lean_inc(v_k_12_);
return v_k_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___redArg___boxed(lean_object* v_k_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___redArg(v_k_13_);
lean_dec(v_k_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, uint8_t v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
lean_inc(v_k_19_);
return v_k_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim___boxed(lean_object* v_motive_20_, lean_object* v_ctorIdx_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
uint8_t v_t_boxed_25_; lean_object* v_res_26_; 
v_t_boxed_25_ = lean_unbox(v_t_22_);
v_res_26_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ctorElim(v_motive_20_, v_ctorIdx_21_, v_t_boxed_25_, v_h_23_, v_k_24_);
lean_dec(v_k_24_);
lean_dec(v_ctorIdx_21_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___redArg(lean_object* v_zero_27_){
_start:
{
lean_inc(v_zero_27_);
return v_zero_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___redArg___boxed(lean_object* v_zero_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___redArg(v_zero_28_);
lean_dec(v_zero_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim(lean_object* v_motive_30_, uint8_t v_t_31_, lean_object* v_h_32_, lean_object* v_zero_33_){
_start:
{
lean_inc(v_zero_33_);
return v_zero_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim___boxed(lean_object* v_motive_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_zero_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_U1AngleAddition_Coord2_zero_elim(v_motive_34_, v_t_boxed_38_, v_h_36_, v_zero_37_);
lean_dec(v_zero_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___redArg(lean_object* v_one_40_){
_start:
{
lean_inc(v_one_40_);
return v_one_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___redArg___boxed(lean_object* v_one_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___redArg(v_one_41_);
lean_dec(v_one_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_one_46_){
_start:
{
lean_inc(v_one_46_);
return v_one_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_one_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_U1AngleAddition_Coord2_one_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_one_50_);
lean_dec(v_one_50_);
return v_res_52_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_U1AngleAddition_Coord2_ofNat(lean_object* v_n_53_){
_start:
{
lean_object* v___x_54_; uint8_t v___x_55_; 
v___x_54_ = lean_unsigned_to_nat(0u);
v___x_55_ = lean_nat_dec_le(v_n_53_, v___x_54_);
if (v___x_55_ == 0)
{
uint8_t v___x_56_; 
v___x_56_ = 1;
return v___x_56_;
}
else
{
uint8_t v___x_57_; 
v___x_57_ = 0;
return v___x_57_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_Coord2_ofNat___boxed(lean_object* v_n_58_){
_start:
{
uint8_t v_res_59_; lean_object* v_r_60_; 
v_res_59_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ofNat(v_n_58_);
lean_dec(v_n_58_);
v_r_60_ = lean_box(v_res_59_);
return v_r_60_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_U1AngleAddition_instDecidableEqCoord2(uint8_t v_x_61_, uint8_t v_y_62_){
_start:
{
lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___x_65_; 
v___x_63_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx(v_x_61_);
v___x_64_ = lp_FiniteQuantum_U1AngleAddition_Coord2_ctorIdx(v_y_62_);
v___x_65_ = lean_nat_dec_eq(v___x_63_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_63_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_instDecidableEqCoord2___boxed(lean_object* v_x_66_, lean_object* v_y_67_){
_start:
{
uint8_t v_x_13__boxed_68_; uint8_t v_y_14__boxed_69_; uint8_t v_res_70_; lean_object* v_r_71_; 
v_x_13__boxed_68_ = lean_unbox(v_x_66_);
v_y_14__boxed_69_ = lean_unbox(v_y_67_);
v_res_70_ = lp_FiniteQuantum_U1AngleAddition_instDecidableEqCoord2(v_x_13__boxed_68_, v_y_14__boxed_69_);
v_r_71_ = lean_box(v_res_70_);
return v_r_71_;
}
}
static lean_object* _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__0(void){
_start:
{
lean_object* v___x_72_; lean_object* v___x_73_; 
v___x_72_ = lean_unsigned_to_nat(0u);
v___x_73_ = lean_nat_to_int(v___x_72_);
return v___x_73_;
}
}
static lean_object* _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__1(void){
_start:
{
lean_object* v___x_74_; lean_object* v___x_75_; 
v___x_74_ = lean_unsigned_to_nat(1u);
v___x_75_ = lean_nat_to_int(v___x_74_);
return v___x_75_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_id2(uint8_t v_i_76_, uint8_t v_j_77_){
_start:
{
uint8_t v___x_78_; 
v___x_78_ = lp_FiniteQuantum_U1AngleAddition_instDecidableEqCoord2(v_i_76_, v_j_77_);
if (v___x_78_ == 0)
{
lean_object* v___x_79_; 
v___x_79_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_id2___closed__0, &lp_FiniteQuantum_U1AngleAddition_id2___closed__0_once, _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__0);
return v___x_79_;
}
else
{
lean_object* v___x_80_; 
v___x_80_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_id2___closed__1, &lp_FiniteQuantum_U1AngleAddition_id2___closed__1_once, _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__1);
return v___x_80_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_id2___boxed(lean_object* v_i_81_, lean_object* v_j_82_){
_start:
{
uint8_t v_i_boxed_83_; uint8_t v_j_boxed_84_; lean_object* v_res_85_; 
v_i_boxed_83_ = lean_unbox(v_i_81_);
v_j_boxed_84_ = lean_unbox(v_j_82_);
v_res_85_ = lp_FiniteQuantum_U1AngleAddition_id2(v_i_boxed_83_, v_j_boxed_84_);
return v_res_85_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_mul2(lean_object* v_A_86_, lean_object* v_B_87_, uint8_t v_i_88_, uint8_t v_k_89_){
_start:
{
uint8_t v___x_90_; lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; lean_object* v___x_94_; lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; uint8_t v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; lean_object* v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; lean_object* v___x_106_; 
v___x_90_ = 0;
v___x_91_ = lean_box(v_i_88_);
v___x_92_ = lean_box(v___x_90_);
lean_inc_ref(v_A_86_);
v___x_93_ = lean_apply_2(v_A_86_, v___x_91_, v___x_92_);
v___x_94_ = lean_box(v___x_90_);
v___x_95_ = lean_box(v_k_89_);
lean_inc_ref(v_B_87_);
v___x_96_ = lean_apply_2(v_B_87_, v___x_94_, v___x_95_);
v___x_97_ = lean_int_mul(v___x_93_, v___x_96_);
lean_dec(v___x_96_);
lean_dec(v___x_93_);
v___x_98_ = 1;
v___x_99_ = lean_box(v_i_88_);
v___x_100_ = lean_box(v___x_98_);
v___x_101_ = lean_apply_2(v_A_86_, v___x_99_, v___x_100_);
v___x_102_ = lean_box(v___x_98_);
v___x_103_ = lean_box(v_k_89_);
v___x_104_ = lean_apply_2(v_B_87_, v___x_102_, v___x_103_);
v___x_105_ = lean_int_mul(v___x_101_, v___x_104_);
lean_dec(v___x_104_);
lean_dec(v___x_101_);
v___x_106_ = lean_int_add(v___x_97_, v___x_105_);
lean_dec(v___x_105_);
lean_dec(v___x_97_);
return v___x_106_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_mul2___boxed(lean_object* v_A_107_, lean_object* v_B_108_, lean_object* v_i_109_, lean_object* v_k_110_){
_start:
{
uint8_t v_i_boxed_111_; uint8_t v_k_boxed_112_; lean_object* v_res_113_; 
v_i_boxed_111_ = lean_unbox(v_i_109_);
v_k_boxed_112_ = lean_unbox(v_k_110_);
v_res_113_ = lp_FiniteQuantum_U1AngleAddition_mul2(v_A_107_, v_B_108_, v_i_boxed_111_, v_k_boxed_112_);
return v_res_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_transpose2(lean_object* v_A_114_, uint8_t v_i_115_, uint8_t v_j_116_){
_start:
{
lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_117_ = lean_box(v_j_116_);
v___x_118_ = lean_box(v_i_115_);
v___x_119_ = lean_apply_2(v_A_114_, v___x_117_, v___x_118_);
return v___x_119_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_transpose2___boxed(lean_object* v_A_120_, lean_object* v_i_121_, lean_object* v_j_122_){
_start:
{
uint8_t v_i_boxed_123_; uint8_t v_j_boxed_124_; lean_object* v_res_125_; 
v_i_boxed_123_ = lean_unbox(v_i_121_);
v_j_boxed_124_ = lean_unbox(v_j_122_);
v_res_125_ = lp_FiniteQuantum_U1AngleAddition_transpose2(v_A_120_, v_i_boxed_123_, v_j_boxed_124_);
return v_res_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_det2(lean_object* v_A_126_){
_start:
{
uint8_t v___x_127_; lean_object* v___x_128_; lean_object* v___x_129_; lean_object* v___x_130_; uint8_t v___x_131_; lean_object* v___x_132_; lean_object* v___x_133_; lean_object* v___x_134_; lean_object* v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; lean_object* v___x_138_; lean_object* v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; 
v___x_127_ = 0;
v___x_128_ = lean_box(v___x_127_);
v___x_129_ = lean_box(v___x_127_);
lean_inc_ref_n(v_A_126_, 3);
v___x_130_ = lean_apply_2(v_A_126_, v___x_128_, v___x_129_);
v___x_131_ = 1;
v___x_132_ = lean_box(v___x_131_);
v___x_133_ = lean_box(v___x_131_);
v___x_134_ = lean_apply_2(v_A_126_, v___x_132_, v___x_133_);
v___x_135_ = lean_int_mul(v___x_130_, v___x_134_);
lean_dec(v___x_134_);
lean_dec(v___x_130_);
v___x_136_ = lean_box(v___x_127_);
v___x_137_ = lean_box(v___x_131_);
v___x_138_ = lean_apply_2(v_A_126_, v___x_136_, v___x_137_);
v___x_139_ = lean_box(v___x_131_);
v___x_140_ = lean_box(v___x_127_);
v___x_141_ = lean_apply_2(v_A_126_, v___x_139_, v___x_140_);
v___x_142_ = lean_int_mul(v___x_138_, v___x_141_);
lean_dec(v___x_141_);
lean_dec(v___x_138_);
v___x_143_ = lean_int_sub(v___x_135_, v___x_142_);
lean_dec(v___x_142_);
lean_dec(v___x_135_);
return v___x_143_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_rotMat(lean_object* v_c_144_, lean_object* v_s_145_, uint8_t v_i_146_, uint8_t v_j_147_){
_start:
{
if (v_i_146_ == 0)
{
if (v_j_147_ == 0)
{
lean_inc(v_c_144_);
return v_c_144_;
}
else
{
lean_object* v___x_148_; 
v___x_148_ = lean_int_neg(v_s_145_);
return v___x_148_;
}
}
else
{
if (v_j_147_ == 0)
{
lean_inc(v_s_145_);
return v_s_145_;
}
else
{
lean_inc(v_c_144_);
return v_c_144_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_rotMat___boxed(lean_object* v_c_149_, lean_object* v_s_150_, lean_object* v_i_151_, lean_object* v_j_152_){
_start:
{
uint8_t v_i_boxed_153_; uint8_t v_j_boxed_154_; lean_object* v_res_155_; 
v_i_boxed_153_ = lean_unbox(v_i_151_);
v_j_boxed_154_ = lean_unbox(v_j_152_);
v_res_155_ = lp_FiniteQuantum_U1AngleAddition_rotMat(v_c_149_, v_s_150_, v_i_boxed_153_, v_j_boxed_154_);
lean_dec(v_s_150_);
lean_dec(v_c_149_);
return v_res_155_;
}
}
static lean_object* _init_lp_FiniteQuantum_U1AngleAddition_circleId___closed__0(void){
_start:
{
lean_object* v___x_156_; lean_object* v___x_157_; lean_object* v___x_158_; 
v___x_156_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_id2___closed__0, &lp_FiniteQuantum_U1AngleAddition_id2___closed__0_once, _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__0);
v___x_157_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_id2___closed__1, &lp_FiniteQuantum_U1AngleAddition_id2___closed__1_once, _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__1);
v___x_158_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_158_, 0, v___x_157_);
lean_ctor_set(v___x_158_, 1, v___x_156_);
return v___x_158_;
}
}
static lean_object* _init_lp_FiniteQuantum_U1AngleAddition_circleId(void){
_start:
{
lean_object* v___x_159_; 
v___x_159_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_circleId___closed__0, &lp_FiniteQuantum_U1AngleAddition_circleId___closed__0_once, _init_lp_FiniteQuantum_U1AngleAddition_circleId___closed__0);
return v___x_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_J(uint8_t v_a_160_, uint8_t v_a_161_){
_start:
{
lean_object* v___x_162_; lean_object* v___x_163_; lean_object* v___x_164_; 
v___x_162_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_id2___closed__0, &lp_FiniteQuantum_U1AngleAddition_id2___closed__0_once, _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__0);
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_U1AngleAddition_id2___closed__1, &lp_FiniteQuantum_U1AngleAddition_id2___closed__1_once, _init_lp_FiniteQuantum_U1AngleAddition_id2___closed__1);
v___x_164_ = lp_FiniteQuantum_U1AngleAddition_rotMat(v___x_162_, v___x_163_, v_a_160_, v_a_161_);
return v___x_164_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_U1AngleAddition_J___boxed(lean_object* v_a_165_, lean_object* v_a_166_){
_start:
{
uint8_t v_a_19__boxed_167_; uint8_t v_a_20__boxed_168_; lean_object* v_res_169_; 
v_a_19__boxed_167_ = lean_unbox(v_a_165_);
v_a_20__boxed_168_ = lean_unbox(v_a_166_);
v_res_169_ = lp_FiniteQuantum_U1AngleAddition_J(v_a_19__boxed_167_, v_a_20__boxed_168_);
return v_res_169_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_U1AngleAddition(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_U1AngleAddition_circleId = _init_lp_FiniteQuantum_U1AngleAddition_circleId();
lean_mark_persistent(lp_FiniteQuantum_U1AngleAddition_circleId);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
