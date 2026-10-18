// Lean compiler output
// Module: LorentzBoost
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lean_nat_pow(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_LorentzBoost_Coord2_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_LorentzBoost_instDecidableEqCoord2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_instDecidableEqCoord2___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 23, .m_capacity = 23, .m_length = 22, .m_data = "LorentzBoost.Coord2.c0"};
static const lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 23, .m_capacity = 23, .m_length = 22, .m_data = "LorentzBoost.Coord2.c1"};
static const lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4;
static lean_once_cell_t lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_LorentzBoost_instReprCoord2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2___closed__0 = (const lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2 = (const lean_object*)&lp_FiniteQuantum_LorentzBoost_instReprCoord2___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mkMat2(lean_object*, lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mkMat2___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_LorentzBoost_id2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_LorentzBoost_id2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_id2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_id2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mul2(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mul2___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_det2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_tr2(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__0;
static lean_once_cell_t lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_boostNumeratorMat(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v1(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v1___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_LorentzBoost_v2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_LorentzBoost_v2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v2(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mulVec2(lean_object*, lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mulVec2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaNum(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaNum___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaDen(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaDen___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_toCtorIdx(uint8_t v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_toCtorIdx___boxed(lean_object* v_x_9_){
_start:
{
uint8_t v_x_4__boxed_10_; lean_object* v_res_11_; 
v_x_4__boxed_10_ = lean_unbox(v_x_9_);
v_res_11_ = lp_FiniteQuantum_LorentzBoost_Coord2_toCtorIdx(v_x_4__boxed_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___redArg(lean_object* v_k_12_){
_start:
{
lean_inc(v_k_12_);
return v_k_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___redArg___boxed(lean_object* v_k_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___redArg(v_k_13_);
lean_dec(v_k_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, uint8_t v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
lean_inc(v_k_19_);
return v_k_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim___boxed(lean_object* v_motive_20_, lean_object* v_ctorIdx_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
uint8_t v_t_boxed_25_; lean_object* v_res_26_; 
v_t_boxed_25_ = lean_unbox(v_t_22_);
v_res_26_ = lp_FiniteQuantum_LorentzBoost_Coord2_ctorElim(v_motive_20_, v_ctorIdx_21_, v_t_boxed_25_, v_h_23_, v_k_24_);
lean_dec(v_k_24_);
lean_dec(v_ctorIdx_21_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___redArg(lean_object* v_c0_27_){
_start:
{
lean_inc(v_c0_27_);
return v_c0_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___redArg___boxed(lean_object* v_c0_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___redArg(v_c0_28_);
lean_dec(v_c0_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim(lean_object* v_motive_30_, uint8_t v_t_31_, lean_object* v_h_32_, lean_object* v_c0_33_){
_start:
{
lean_inc(v_c0_33_);
return v_c0_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim___boxed(lean_object* v_motive_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_c0_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_LorentzBoost_Coord2_c0_elim(v_motive_34_, v_t_boxed_38_, v_h_36_, v_c0_37_);
lean_dec(v_c0_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___redArg(lean_object* v_c1_40_){
_start:
{
lean_inc(v_c1_40_);
return v_c1_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___redArg___boxed(lean_object* v_c1_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___redArg(v_c1_41_);
lean_dec(v_c1_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_c1_46_){
_start:
{
lean_inc(v_c1_46_);
return v_c1_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_c1_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_LorentzBoost_Coord2_c1_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_c1_50_);
lean_dec(v_c1_50_);
return v_res_52_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_LorentzBoost_Coord2_ofNat(lean_object* v_n_53_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_Coord2_ofNat___boxed(lean_object* v_n_58_){
_start:
{
uint8_t v_res_59_; lean_object* v_r_60_; 
v_res_59_ = lp_FiniteQuantum_LorentzBoost_Coord2_ofNat(v_n_58_);
lean_dec(v_n_58_);
v_r_60_ = lean_box(v_res_59_);
return v_r_60_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_LorentzBoost_instDecidableEqCoord2(uint8_t v_x_61_, uint8_t v_y_62_){
_start:
{
lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___x_65_; 
v___x_63_ = lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx(v_x_61_);
v___x_64_ = lp_FiniteQuantum_LorentzBoost_Coord2_ctorIdx(v_y_62_);
v___x_65_ = lean_nat_dec_eq(v___x_63_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_63_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_instDecidableEqCoord2___boxed(lean_object* v_x_66_, lean_object* v_y_67_){
_start:
{
uint8_t v_x_13__boxed_68_; uint8_t v_y_14__boxed_69_; uint8_t v_res_70_; lean_object* v_r_71_; 
v_x_13__boxed_68_ = lean_unbox(v_x_66_);
v_y_14__boxed_69_ = lean_unbox(v_y_67_);
v_res_70_ = lp_FiniteQuantum_LorentzBoost_instDecidableEqCoord2(v_x_13__boxed_68_, v_y_14__boxed_69_);
v_r_71_ = lean_box(v_res_70_);
return v_r_71_;
}
}
static lean_object* _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4(void){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_78_ = lean_unsigned_to_nat(2u);
v___x_79_ = lean_nat_to_int(v___x_78_);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5(void){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; 
v___x_80_ = lean_unsigned_to_nat(1u);
v___x_81_ = lean_nat_to_int(v___x_80_);
return v___x_81_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr(uint8_t v_x_82_, lean_object* v_prec_83_){
_start:
{
lean_object* v___y_85_; lean_object* v___y_92_; 
if (v_x_82_ == 0)
{
lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(1024u);
v___x_99_ = lean_nat_dec_le(v___x_98_, v_prec_83_);
if (v___x_99_ == 0)
{
lean_object* v___x_100_; 
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4);
v___y_85_ = v___x_100_;
goto v___jp_84_;
}
else
{
lean_object* v___x_101_; 
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5);
v___y_85_ = v___x_101_;
goto v___jp_84_;
}
}
else
{
lean_object* v___x_102_; uint8_t v___x_103_; 
v___x_102_ = lean_unsigned_to_nat(1024u);
v___x_103_ = lean_nat_dec_le(v___x_102_, v_prec_83_);
if (v___x_103_ == 0)
{
lean_object* v___x_104_; 
v___x_104_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__4);
v___y_92_ = v___x_104_;
goto v___jp_91_;
}
else
{
lean_object* v___x_105_; 
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5);
v___y_92_ = v___x_105_;
goto v___jp_91_;
}
}
v___jp_84_:
{
lean_object* v___x_86_; lean_object* v___x_87_; uint8_t v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; 
v___x_86_ = ((lean_object*)(lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__1));
lean_inc(v___y_85_);
v___x_87_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_87_, 0, v___y_85_);
lean_ctor_set(v___x_87_, 1, v___x_86_);
v___x_88_ = 0;
v___x_89_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_89_, 0, v___x_87_);
lean_ctor_set_uint8(v___x_89_, sizeof(void*)*1, v___x_88_);
v___x_90_ = l_Repr_addAppParen(v___x_89_, v_prec_83_);
return v___x_90_;
}
v___jp_91_:
{
lean_object* v___x_93_; lean_object* v___x_94_; uint8_t v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; 
v___x_93_ = ((lean_object*)(lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__3));
lean_inc(v___y_92_);
v___x_94_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_94_, 0, v___y_92_);
lean_ctor_set(v___x_94_, 1, v___x_93_);
v___x_95_ = 0;
v___x_96_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_96_, 0, v___x_94_);
lean_ctor_set_uint8(v___x_96_, sizeof(void*)*1, v___x_95_);
v___x_97_ = l_Repr_addAppParen(v___x_96_, v_prec_83_);
return v___x_97_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___boxed(lean_object* v_x_106_, lean_object* v_prec_107_){
_start:
{
uint8_t v_x_121__boxed_108_; lean_object* v_res_109_; 
v_x_121__boxed_108_ = lean_unbox(v_x_106_);
v_res_109_ = lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr(v_x_121__boxed_108_, v_prec_107_);
lean_dec(v_prec_107_);
return v_res_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mkMat2(lean_object* v_a00_112_, lean_object* v_a01_113_, lean_object* v_a10_114_, lean_object* v_a11_115_, uint8_t v_i_116_, uint8_t v_j_117_){
_start:
{
if (v_i_116_ == 0)
{
if (v_j_117_ == 0)
{
lean_inc(v_a00_112_);
return v_a00_112_;
}
else
{
lean_inc(v_a01_113_);
return v_a01_113_;
}
}
else
{
if (v_j_117_ == 0)
{
lean_inc(v_a10_114_);
return v_a10_114_;
}
else
{
lean_inc(v_a11_115_);
return v_a11_115_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mkMat2___boxed(lean_object* v_a00_118_, lean_object* v_a01_119_, lean_object* v_a10_120_, lean_object* v_a11_121_, lean_object* v_i_122_, lean_object* v_j_123_){
_start:
{
uint8_t v_i_boxed_124_; uint8_t v_j_boxed_125_; lean_object* v_res_126_; 
v_i_boxed_124_ = lean_unbox(v_i_122_);
v_j_boxed_125_ = lean_unbox(v_j_123_);
v_res_126_ = lp_FiniteQuantum_LorentzBoost_mkMat2(v_a00_118_, v_a01_119_, v_a10_120_, v_a11_121_, v_i_boxed_124_, v_j_boxed_125_);
lean_dec(v_a11_121_);
lean_dec(v_a10_120_);
lean_dec(v_a01_119_);
lean_dec(v_a00_118_);
return v_res_126_;
}
}
static lean_object* _init_lp_FiniteQuantum_LorentzBoost_id2___closed__0(void){
_start:
{
lean_object* v___x_127_; lean_object* v___x_128_; 
v___x_127_ = lean_unsigned_to_nat(0u);
v___x_128_ = lean_nat_to_int(v___x_127_);
return v___x_128_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_id2(uint8_t v_a_129_, uint8_t v_a_130_){
_start:
{
lean_object* v___x_131_; lean_object* v___x_132_; lean_object* v___x_133_; 
v___x_131_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5);
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_id2___closed__0, &lp_FiniteQuantum_LorentzBoost_id2___closed__0_once, _init_lp_FiniteQuantum_LorentzBoost_id2___closed__0);
v___x_133_ = lp_FiniteQuantum_LorentzBoost_mkMat2(v___x_131_, v___x_132_, v___x_132_, v___x_131_, v_a_129_, v_a_130_);
return v___x_133_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_id2___boxed(lean_object* v_a_134_, lean_object* v_a_135_){
_start:
{
uint8_t v_a_21__boxed_136_; uint8_t v_a_22__boxed_137_; lean_object* v_res_138_; 
v_a_21__boxed_136_ = lean_unbox(v_a_134_);
v_a_22__boxed_137_ = lean_unbox(v_a_135_);
v_res_138_ = lp_FiniteQuantum_LorentzBoost_id2(v_a_21__boxed_136_, v_a_22__boxed_137_);
return v_res_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mul2(lean_object* v_A_139_, lean_object* v_B_140_, uint8_t v_i_141_, uint8_t v_k_142_){
_start:
{
uint8_t v___x_143_; lean_object* v___x_144_; lean_object* v___x_145_; lean_object* v___x_146_; lean_object* v___x_147_; lean_object* v___x_148_; lean_object* v___x_149_; lean_object* v___x_150_; uint8_t v___x_151_; lean_object* v___x_152_; lean_object* v___x_153_; lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; lean_object* v___x_157_; lean_object* v___x_158_; lean_object* v___x_159_; 
v___x_143_ = 0;
v___x_144_ = lean_box(v_i_141_);
v___x_145_ = lean_box(v___x_143_);
lean_inc_ref(v_A_139_);
v___x_146_ = lean_apply_2(v_A_139_, v___x_144_, v___x_145_);
v___x_147_ = lean_box(v___x_143_);
v___x_148_ = lean_box(v_k_142_);
lean_inc_ref(v_B_140_);
v___x_149_ = lean_apply_2(v_B_140_, v___x_147_, v___x_148_);
v___x_150_ = lean_int_mul(v___x_146_, v___x_149_);
lean_dec(v___x_149_);
lean_dec(v___x_146_);
v___x_151_ = 1;
v___x_152_ = lean_box(v_i_141_);
v___x_153_ = lean_box(v___x_151_);
v___x_154_ = lean_apply_2(v_A_139_, v___x_152_, v___x_153_);
v___x_155_ = lean_box(v___x_151_);
v___x_156_ = lean_box(v_k_142_);
v___x_157_ = lean_apply_2(v_B_140_, v___x_155_, v___x_156_);
v___x_158_ = lean_int_mul(v___x_154_, v___x_157_);
lean_dec(v___x_157_);
lean_dec(v___x_154_);
v___x_159_ = lean_int_add(v___x_150_, v___x_158_);
lean_dec(v___x_158_);
lean_dec(v___x_150_);
return v___x_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mul2___boxed(lean_object* v_A_160_, lean_object* v_B_161_, lean_object* v_i_162_, lean_object* v_k_163_){
_start:
{
uint8_t v_i_boxed_164_; uint8_t v_k_boxed_165_; lean_object* v_res_166_; 
v_i_boxed_164_ = lean_unbox(v_i_162_);
v_k_boxed_165_ = lean_unbox(v_k_163_);
v_res_166_ = lp_FiniteQuantum_LorentzBoost_mul2(v_A_160_, v_B_161_, v_i_boxed_164_, v_k_boxed_165_);
return v_res_166_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_det2(lean_object* v_A_167_){
_start:
{
uint8_t v___x_168_; lean_object* v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; uint8_t v___x_172_; lean_object* v___x_173_; lean_object* v___x_174_; lean_object* v___x_175_; lean_object* v___x_176_; lean_object* v___x_177_; lean_object* v___x_178_; lean_object* v___x_179_; lean_object* v___x_180_; lean_object* v___x_181_; lean_object* v___x_182_; lean_object* v___x_183_; lean_object* v___x_184_; 
v___x_168_ = 0;
v___x_169_ = lean_box(v___x_168_);
v___x_170_ = lean_box(v___x_168_);
lean_inc_ref_n(v_A_167_, 3);
v___x_171_ = lean_apply_2(v_A_167_, v___x_169_, v___x_170_);
v___x_172_ = 1;
v___x_173_ = lean_box(v___x_172_);
v___x_174_ = lean_box(v___x_172_);
v___x_175_ = lean_apply_2(v_A_167_, v___x_173_, v___x_174_);
v___x_176_ = lean_int_mul(v___x_171_, v___x_175_);
lean_dec(v___x_175_);
lean_dec(v___x_171_);
v___x_177_ = lean_box(v___x_168_);
v___x_178_ = lean_box(v___x_172_);
v___x_179_ = lean_apply_2(v_A_167_, v___x_177_, v___x_178_);
v___x_180_ = lean_box(v___x_172_);
v___x_181_ = lean_box(v___x_168_);
v___x_182_ = lean_apply_2(v_A_167_, v___x_180_, v___x_181_);
v___x_183_ = lean_int_mul(v___x_179_, v___x_182_);
lean_dec(v___x_182_);
lean_dec(v___x_179_);
v___x_184_ = lean_int_sub(v___x_176_, v___x_183_);
lean_dec(v___x_183_);
lean_dec(v___x_176_);
return v___x_184_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_tr2(lean_object* v_A_185_){
_start:
{
uint8_t v___x_186_; lean_object* v___x_187_; lean_object* v___x_188_; lean_object* v___x_189_; uint8_t v___x_190_; lean_object* v___x_191_; lean_object* v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; 
v___x_186_ = 0;
v___x_187_ = lean_box(v___x_186_);
v___x_188_ = lean_box(v___x_186_);
lean_inc_ref(v_A_185_);
v___x_189_ = lean_apply_2(v_A_185_, v___x_187_, v___x_188_);
v___x_190_ = 1;
v___x_191_ = lean_box(v___x_190_);
v___x_192_ = lean_box(v___x_190_);
v___x_193_ = lean_apply_2(v_A_185_, v___x_191_, v___x_192_);
v___x_194_ = lean_int_add(v___x_189_, v___x_193_);
lean_dec(v___x_193_);
lean_dec(v___x_189_);
return v___x_194_;
}
}
static lean_object* _init_lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__0(void){
_start:
{
lean_object* v___x_195_; lean_object* v___x_196_; 
v___x_195_ = lean_unsigned_to_nat(5u);
v___x_196_ = lean_nat_to_int(v___x_195_);
return v___x_196_;
}
}
static lean_object* _init_lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__1(void){
_start:
{
lean_object* v___x_197_; lean_object* v___x_198_; 
v___x_197_ = lean_unsigned_to_nat(3u);
v___x_198_ = lean_nat_to_int(v___x_197_);
return v___x_198_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_boostNumeratorMat(uint8_t v_a_199_, uint8_t v_a_200_){
_start:
{
lean_object* v___x_201_; lean_object* v___x_202_; lean_object* v___x_203_; 
v___x_201_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__0, &lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__0_once, _init_lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__0);
v___x_202_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__1, &lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__1_once, _init_lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___closed__1);
v___x_203_ = lp_FiniteQuantum_LorentzBoost_mkMat2(v___x_201_, v___x_202_, v___x_202_, v___x_201_, v_a_199_, v_a_200_);
return v___x_203_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_boostNumeratorMat___boxed(lean_object* v_a_204_, lean_object* v_a_205_){
_start:
{
uint8_t v_a_23__boxed_206_; uint8_t v_a_24__boxed_207_; lean_object* v_res_208_; 
v_a_23__boxed_206_ = lean_unbox(v_a_204_);
v_a_24__boxed_207_ = lean_unbox(v_a_205_);
v_res_208_ = lp_FiniteQuantum_LorentzBoost_boostNumeratorMat(v_a_23__boxed_206_, v_a_24__boxed_207_);
return v_res_208_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v1(uint8_t v_i_209_){
_start:
{
lean_object* v___x_210_; 
v___x_210_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5);
return v___x_210_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v1___boxed(lean_object* v_i_211_){
_start:
{
uint8_t v_i_boxed_212_; lean_object* v_res_213_; 
v_i_boxed_212_ = lean_unbox(v_i_211_);
v_res_213_ = lp_FiniteQuantum_LorentzBoost_v1(v_i_boxed_212_);
return v_res_213_;
}
}
static lean_object* _init_lp_FiniteQuantum_LorentzBoost_v2___closed__0(void){
_start:
{
lean_object* v___x_214_; lean_object* v___x_215_; 
v___x_214_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5);
v___x_215_ = lean_int_neg(v___x_214_);
return v___x_215_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v2(uint8_t v_i_216_){
_start:
{
if (v_i_216_ == 0)
{
lean_object* v___x_217_; 
v___x_217_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5, &lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5_once, _init_lp_FiniteQuantum_LorentzBoost_instReprCoord2_repr___closed__5);
return v___x_217_;
}
else
{
lean_object* v___x_218_; 
v___x_218_ = lean_obj_once(&lp_FiniteQuantum_LorentzBoost_v2___closed__0, &lp_FiniteQuantum_LorentzBoost_v2___closed__0_once, _init_lp_FiniteQuantum_LorentzBoost_v2___closed__0);
return v___x_218_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_v2___boxed(lean_object* v_i_219_){
_start:
{
uint8_t v_i_boxed_220_; lean_object* v_res_221_; 
v_i_boxed_220_ = lean_unbox(v_i_219_);
v_res_221_ = lp_FiniteQuantum_LorentzBoost_v2(v_i_boxed_220_);
return v_res_221_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mulVec2(lean_object* v_A_222_, lean_object* v_v_223_, uint8_t v_i_224_){
_start:
{
uint8_t v___x_225_; lean_object* v___x_226_; lean_object* v___x_227_; lean_object* v___x_228_; lean_object* v___x_229_; lean_object* v___x_230_; lean_object* v___x_231_; uint8_t v___x_232_; lean_object* v___x_233_; lean_object* v___x_234_; lean_object* v___x_235_; lean_object* v___x_236_; lean_object* v___x_237_; lean_object* v___x_238_; lean_object* v___x_239_; 
v___x_225_ = 0;
v___x_226_ = lean_box(v_i_224_);
v___x_227_ = lean_box(v___x_225_);
lean_inc_ref(v_A_222_);
v___x_228_ = lean_apply_2(v_A_222_, v___x_226_, v___x_227_);
v___x_229_ = lean_box(v___x_225_);
lean_inc_ref(v_v_223_);
v___x_230_ = lean_apply_1(v_v_223_, v___x_229_);
v___x_231_ = lean_int_mul(v___x_228_, v___x_230_);
lean_dec(v___x_230_);
lean_dec(v___x_228_);
v___x_232_ = 1;
v___x_233_ = lean_box(v_i_224_);
v___x_234_ = lean_box(v___x_232_);
v___x_235_ = lean_apply_2(v_A_222_, v___x_233_, v___x_234_);
v___x_236_ = lean_box(v___x_232_);
v___x_237_ = lean_apply_1(v_v_223_, v___x_236_);
v___x_238_ = lean_int_mul(v___x_235_, v___x_237_);
lean_dec(v___x_237_);
lean_dec(v___x_235_);
v___x_239_ = lean_int_add(v___x_231_, v___x_238_);
lean_dec(v___x_238_);
lean_dec(v___x_231_);
return v___x_239_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_mulVec2___boxed(lean_object* v_A_240_, lean_object* v_v_241_, lean_object* v_i_242_){
_start:
{
uint8_t v_i_boxed_243_; lean_object* v_res_244_; 
v_i_boxed_243_ = lean_unbox(v_i_242_);
v_res_244_ = lp_FiniteQuantum_LorentzBoost_mulVec2(v_A_240_, v_v_241_, v_i_boxed_243_);
return v_res_244_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaNum(lean_object* v_k_245_){
_start:
{
lean_object* v___x_246_; lean_object* v___x_247_; lean_object* v___x_248_; lean_object* v___x_249_; 
v___x_246_ = lean_unsigned_to_nat(4u);
v___x_247_ = lean_nat_pow(v___x_246_, v_k_245_);
v___x_248_ = lean_unsigned_to_nat(1u);
v___x_249_ = lean_nat_add(v___x_247_, v___x_248_);
lean_dec(v___x_247_);
return v___x_249_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaNum___boxed(lean_object* v_k_250_){
_start:
{
lean_object* v_res_251_; 
v_res_251_ = lp_FiniteQuantum_LorentzBoost_gammaNum(v_k_250_);
lean_dec(v_k_250_);
return v_res_251_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaDen(lean_object* v_k_252_){
_start:
{
lean_object* v___x_253_; lean_object* v___x_254_; lean_object* v___x_255_; lean_object* v___x_256_; 
v___x_253_ = lean_unsigned_to_nat(2u);
v___x_254_ = lean_unsigned_to_nat(1u);
v___x_255_ = lean_nat_add(v_k_252_, v___x_254_);
v___x_256_ = lean_nat_pow(v___x_253_, v___x_255_);
lean_dec(v___x_255_);
return v___x_256_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_LorentzBoost_gammaDen___boxed(lean_object* v_k_257_){
_start:
{
lean_object* v_res_258_; 
v_res_258_ = lp_FiniteQuantum_LorentzBoost_gammaDen(v_k_257_);
lean_dec(v_k_257_);
return v_res_258_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_LorentzBoost(uint8_t builtin) {
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
