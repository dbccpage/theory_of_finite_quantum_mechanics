// Lean compiler output
// Module: InstantonDyonGas
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
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_emod(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_InstantonDyonGas_instDecidableEqDyonSpecies(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_instDecidableEqDyonSpecies___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 36, .m_capacity = 36, .m_length = 35, .m_data = "InstantonDyonGas.DyonSpecies.M_dyon"};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 36, .m_capacity = 36, .m_length = 35, .m_data = "InstantonDyonGas.DyonSpecies.L_dyon"};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 35, .m_capacity = 35, .m_length = 34, .m_data = "InstantonDyonGas.DyonSpecies.M_bar"};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 35, .m_capacity = 35, .m_length = 34, .m_data = "InstantonDyonGas.DyonSpecies.L_bar"};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__7_value;
static lean_once_cell_t lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8;
static lean_once_cell_t lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9;
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies___closed__0 = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies = (const lean_object*)&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_magnetic__charge(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_topological__charge__units(lean_object*, lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_topological__charge__units___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_InstantonDyonGas_dirac__phase___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_InstantonDyonGas_dirac__phase___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dirac__phase(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dirac__phase___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dyonDefectMass(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dyonDefectMass___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx(uint8_t v_x_1_){
_start:
{
switch(v_x_1_)
{
case 0:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
case 1:
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(1u);
return v___x_3_;
}
case 2:
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(2u);
return v___x_4_;
}
default: 
{
lean_object* v___x_5_; 
v___x_5_ = lean_unsigned_to_nat(3u);
return v___x_5_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx___boxed(lean_object* v_x_6_){
_start:
{
uint8_t v_x_boxed_7_; lean_object* v_res_8_; 
v_x_boxed_7_ = lean_unbox(v_x_6_);
v_res_8_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx(v_x_boxed_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_toCtorIdx(uint8_t v_x_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx(v_x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_toCtorIdx___boxed(lean_object* v_x_11_){
_start:
{
uint8_t v_x_4__boxed_12_; lean_object* v_res_13_; 
v_x_4__boxed_12_ = lean_unbox(v_x_11_);
v_res_13_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_toCtorIdx(v_x_4__boxed_12_);
return v_res_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___redArg(lean_object* v_k_14_){
_start:
{
lean_inc(v_k_14_);
return v_k_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___redArg___boxed(lean_object* v_k_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___redArg(v_k_15_);
lean_dec(v_k_15_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim(lean_object* v_motive_17_, lean_object* v_ctorIdx_18_, uint8_t v_t_19_, lean_object* v_h_20_, lean_object* v_k_21_){
_start:
{
lean_inc(v_k_21_);
return v_k_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim___boxed(lean_object* v_motive_22_, lean_object* v_ctorIdx_23_, lean_object* v_t_24_, lean_object* v_h_25_, lean_object* v_k_26_){
_start:
{
uint8_t v_t_boxed_27_; lean_object* v_res_28_; 
v_t_boxed_27_ = lean_unbox(v_t_24_);
v_res_28_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorElim(v_motive_22_, v_ctorIdx_23_, v_t_boxed_27_, v_h_25_, v_k_26_);
lean_dec(v_k_26_);
lean_dec(v_ctorIdx_23_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___redArg(lean_object* v_M__dyon_29_){
_start:
{
lean_inc(v_M__dyon_29_);
return v_M__dyon_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___redArg___boxed(lean_object* v_M__dyon_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___redArg(v_M__dyon_30_);
lean_dec(v_M__dyon_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim(lean_object* v_motive_32_, uint8_t v_t_33_, lean_object* v_h_34_, lean_object* v_M__dyon_35_){
_start:
{
lean_inc(v_M__dyon_35_);
return v_M__dyon_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim___boxed(lean_object* v_motive_36_, lean_object* v_t_37_, lean_object* v_h_38_, lean_object* v_M__dyon_39_){
_start:
{
uint8_t v_t_boxed_40_; lean_object* v_res_41_; 
v_t_boxed_40_ = lean_unbox(v_t_37_);
v_res_41_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__dyon_elim(v_motive_36_, v_t_boxed_40_, v_h_38_, v_M__dyon_39_);
lean_dec(v_M__dyon_39_);
return v_res_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___redArg(lean_object* v_L__dyon_42_){
_start:
{
lean_inc(v_L__dyon_42_);
return v_L__dyon_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___redArg___boxed(lean_object* v_L__dyon_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___redArg(v_L__dyon_43_);
lean_dec(v_L__dyon_43_);
return v_res_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim(lean_object* v_motive_45_, uint8_t v_t_46_, lean_object* v_h_47_, lean_object* v_L__dyon_48_){
_start:
{
lean_inc(v_L__dyon_48_);
return v_L__dyon_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim___boxed(lean_object* v_motive_49_, lean_object* v_t_50_, lean_object* v_h_51_, lean_object* v_L__dyon_52_){
_start:
{
uint8_t v_t_boxed_53_; lean_object* v_res_54_; 
v_t_boxed_53_ = lean_unbox(v_t_50_);
v_res_54_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__dyon_elim(v_motive_49_, v_t_boxed_53_, v_h_51_, v_L__dyon_52_);
lean_dec(v_L__dyon_52_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___redArg(lean_object* v_M__bar_55_){
_start:
{
lean_inc(v_M__bar_55_);
return v_M__bar_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___redArg___boxed(lean_object* v_M__bar_56_){
_start:
{
lean_object* v_res_57_; 
v_res_57_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___redArg(v_M__bar_56_);
lean_dec(v_M__bar_56_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim(lean_object* v_motive_58_, uint8_t v_t_59_, lean_object* v_h_60_, lean_object* v_M__bar_61_){
_start:
{
lean_inc(v_M__bar_61_);
return v_M__bar_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim___boxed(lean_object* v_motive_62_, lean_object* v_t_63_, lean_object* v_h_64_, lean_object* v_M__bar_65_){
_start:
{
uint8_t v_t_boxed_66_; lean_object* v_res_67_; 
v_t_boxed_66_ = lean_unbox(v_t_63_);
v_res_67_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_M__bar_elim(v_motive_62_, v_t_boxed_66_, v_h_64_, v_M__bar_65_);
lean_dec(v_M__bar_65_);
return v_res_67_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___redArg(lean_object* v_L__bar_68_){
_start:
{
lean_inc(v_L__bar_68_);
return v_L__bar_68_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___redArg___boxed(lean_object* v_L__bar_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___redArg(v_L__bar_69_);
lean_dec(v_L__bar_69_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim(lean_object* v_motive_71_, uint8_t v_t_72_, lean_object* v_h_73_, lean_object* v_L__bar_74_){
_start:
{
lean_inc(v_L__bar_74_);
return v_L__bar_74_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim___boxed(lean_object* v_motive_75_, lean_object* v_t_76_, lean_object* v_h_77_, lean_object* v_L__bar_78_){
_start:
{
uint8_t v_t_boxed_79_; lean_object* v_res_80_; 
v_t_boxed_79_ = lean_unbox(v_t_76_);
v_res_80_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_L__bar_elim(v_motive_75_, v_t_boxed_79_, v_h_77_, v_L__bar_78_);
lean_dec(v_L__bar_78_);
return v_res_80_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ofNat(lean_object* v_n_81_){
_start:
{
lean_object* v___x_82_; uint8_t v___x_83_; 
v___x_82_ = lean_unsigned_to_nat(1u);
v___x_83_ = lean_nat_dec_le(v_n_81_, v___x_82_);
if (v___x_83_ == 0)
{
lean_object* v___x_84_; uint8_t v___x_85_; 
v___x_84_ = lean_unsigned_to_nat(2u);
v___x_85_ = lean_nat_dec_le(v_n_81_, v___x_84_);
if (v___x_85_ == 0)
{
uint8_t v___x_86_; 
v___x_86_ = 3;
return v___x_86_;
}
else
{
uint8_t v___x_87_; 
v___x_87_ = 2;
return v___x_87_;
}
}
else
{
lean_object* v___x_88_; uint8_t v___x_89_; 
v___x_88_ = lean_unsigned_to_nat(0u);
v___x_89_ = lean_nat_dec_le(v_n_81_, v___x_88_);
if (v___x_89_ == 0)
{
uint8_t v___x_90_; 
v___x_90_ = 1;
return v___x_90_;
}
else
{
uint8_t v___x_91_; 
v___x_91_ = 0;
return v___x_91_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ofNat___boxed(lean_object* v_n_92_){
_start:
{
uint8_t v_res_93_; lean_object* v_r_94_; 
v_res_93_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ofNat(v_n_92_);
lean_dec(v_n_92_);
v_r_94_ = lean_box(v_res_93_);
return v_r_94_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_InstantonDyonGas_instDecidableEqDyonSpecies(uint8_t v_x_95_, uint8_t v_y_96_){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_97_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx(v_x_95_);
v___x_98_ = lp_FiniteQuantum_InstantonDyonGas_DyonSpecies_ctorIdx(v_y_96_);
v___x_99_ = lean_nat_dec_eq(v___x_97_, v___x_98_);
lean_dec(v___x_98_);
lean_dec(v___x_97_);
return v___x_99_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_instDecidableEqDyonSpecies___boxed(lean_object* v_x_100_, lean_object* v_y_101_){
_start:
{
uint8_t v_x_13__boxed_102_; uint8_t v_y_14__boxed_103_; uint8_t v_res_104_; lean_object* v_r_105_; 
v_x_13__boxed_102_ = lean_unbox(v_x_100_);
v_y_14__boxed_103_ = lean_unbox(v_y_101_);
v_res_104_ = lp_FiniteQuantum_InstantonDyonGas_instDecidableEqDyonSpecies(v_x_13__boxed_102_, v_y_14__boxed_103_);
v_r_105_ = lean_box(v_res_104_);
return v_r_105_;
}
}
static lean_object* _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(2u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_120_ = lean_unsigned_to_nat(1u);
v___x_121_ = lean_nat_to_int(v___x_120_);
return v___x_121_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr(uint8_t v_x_122_, lean_object* v_prec_123_){
_start:
{
lean_object* v___y_125_; lean_object* v___y_132_; lean_object* v___y_139_; lean_object* v___y_146_; 
switch(v_x_122_)
{
case 0:
{
lean_object* v___x_152_; uint8_t v___x_153_; 
v___x_152_ = lean_unsigned_to_nat(1024u);
v___x_153_ = lean_nat_dec_le(v___x_152_, v_prec_123_);
if (v___x_153_ == 0)
{
lean_object* v___x_154_; 
v___x_154_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8);
v___y_125_ = v___x_154_;
goto v___jp_124_;
}
else
{
lean_object* v___x_155_; 
v___x_155_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
v___y_125_ = v___x_155_;
goto v___jp_124_;
}
}
case 1:
{
lean_object* v___x_156_; uint8_t v___x_157_; 
v___x_156_ = lean_unsigned_to_nat(1024u);
v___x_157_ = lean_nat_dec_le(v___x_156_, v_prec_123_);
if (v___x_157_ == 0)
{
lean_object* v___x_158_; 
v___x_158_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8);
v___y_132_ = v___x_158_;
goto v___jp_131_;
}
else
{
lean_object* v___x_159_; 
v___x_159_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
v___y_132_ = v___x_159_;
goto v___jp_131_;
}
}
case 2:
{
lean_object* v___x_160_; uint8_t v___x_161_; 
v___x_160_ = lean_unsigned_to_nat(1024u);
v___x_161_ = lean_nat_dec_le(v___x_160_, v_prec_123_);
if (v___x_161_ == 0)
{
lean_object* v___x_162_; 
v___x_162_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8);
v___y_139_ = v___x_162_;
goto v___jp_138_;
}
else
{
lean_object* v___x_163_; 
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
v___y_139_ = v___x_163_;
goto v___jp_138_;
}
}
default: 
{
lean_object* v___x_164_; uint8_t v___x_165_; 
v___x_164_ = lean_unsigned_to_nat(1024u);
v___x_165_ = lean_nat_dec_le(v___x_164_, v_prec_123_);
if (v___x_165_ == 0)
{
lean_object* v___x_166_; 
v___x_166_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8);
v___y_146_ = v___x_166_;
goto v___jp_145_;
}
else
{
lean_object* v___x_167_; 
v___x_167_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
v___y_146_ = v___x_167_;
goto v___jp_145_;
}
}
}
v___jp_124_:
{
lean_object* v___x_126_; lean_object* v___x_127_; uint8_t v___x_128_; lean_object* v___x_129_; lean_object* v___x_130_; 
v___x_126_ = ((lean_object*)(lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__1));
lean_inc(v___y_125_);
v___x_127_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_127_, 0, v___y_125_);
lean_ctor_set(v___x_127_, 1, v___x_126_);
v___x_128_ = 0;
v___x_129_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_129_, 0, v___x_127_);
lean_ctor_set_uint8(v___x_129_, sizeof(void*)*1, v___x_128_);
v___x_130_ = l_Repr_addAppParen(v___x_129_, v_prec_123_);
return v___x_130_;
}
v___jp_131_:
{
lean_object* v___x_133_; lean_object* v___x_134_; uint8_t v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; 
v___x_133_ = ((lean_object*)(lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__3));
lean_inc(v___y_132_);
v___x_134_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_134_, 0, v___y_132_);
lean_ctor_set(v___x_134_, 1, v___x_133_);
v___x_135_ = 0;
v___x_136_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_136_, 0, v___x_134_);
lean_ctor_set_uint8(v___x_136_, sizeof(void*)*1, v___x_135_);
v___x_137_ = l_Repr_addAppParen(v___x_136_, v_prec_123_);
return v___x_137_;
}
v___jp_138_:
{
lean_object* v___x_140_; lean_object* v___x_141_; uint8_t v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; 
v___x_140_ = ((lean_object*)(lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__5));
lean_inc(v___y_139_);
v___x_141_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_141_, 0, v___y_139_);
lean_ctor_set(v___x_141_, 1, v___x_140_);
v___x_142_ = 0;
v___x_143_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_143_, 0, v___x_141_);
lean_ctor_set_uint8(v___x_143_, sizeof(void*)*1, v___x_142_);
v___x_144_ = l_Repr_addAppParen(v___x_143_, v_prec_123_);
return v___x_144_;
}
v___jp_145_:
{
lean_object* v___x_147_; lean_object* v___x_148_; uint8_t v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; 
v___x_147_ = ((lean_object*)(lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__7));
lean_inc(v___y_146_);
v___x_148_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_148_, 0, v___y_146_);
lean_ctor_set(v___x_148_, 1, v___x_147_);
v___x_149_ = 0;
v___x_150_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_150_, 0, v___x_148_);
lean_ctor_set_uint8(v___x_150_, sizeof(void*)*1, v___x_149_);
v___x_151_ = l_Repr_addAppParen(v___x_150_, v_prec_123_);
return v___x_151_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___boxed(lean_object* v_x_168_, lean_object* v_prec_169_){
_start:
{
uint8_t v_x_233__boxed_170_; lean_object* v_res_171_; 
v_x_233__boxed_170_ = lean_unbox(v_x_168_);
v_res_171_ = lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr(v_x_233__boxed_170_, v_prec_169_);
lean_dec(v_prec_169_);
return v_res_171_;
}
}
static lean_object* _init_lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0(void){
_start:
{
lean_object* v___x_174_; lean_object* v___x_175_; 
v___x_174_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
v___x_175_ = lean_int_neg(v___x_174_);
return v___x_175_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_magnetic__charge(uint8_t v_x_176_){
_start:
{
switch(v_x_176_)
{
case 1:
{
goto v___jp_177_;
}
case 2:
{
goto v___jp_177_;
}
default: 
{
lean_object* v___x_179_; 
v___x_179_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
return v___x_179_;
}
}
v___jp_177_:
{
lean_object* v___x_178_; 
v___x_178_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0, &lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0_once, _init_lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0);
return v___x_178_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___boxed(lean_object* v_x_180_){
_start:
{
uint8_t v_x_48__boxed_181_; lean_object* v_res_182_; 
v_x_48__boxed_181_ = lean_unbox(v_x_180_);
v_res_182_ = lp_FiniteQuantum_InstantonDyonGas_magnetic__charge(v_x_48__boxed_181_);
return v_res_182_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_topological__charge__units(lean_object* v_nu__units_183_, lean_object* v_D_184_, uint8_t v_x_185_){
_start:
{
switch(v_x_185_)
{
case 0:
{
lean_inc(v_nu__units_183_);
return v_nu__units_183_;
}
case 1:
{
lean_object* v___x_186_; 
v___x_186_ = lean_int_sub(v_D_184_, v_nu__units_183_);
return v___x_186_;
}
case 2:
{
lean_object* v___x_187_; 
v___x_187_ = lean_int_neg(v_nu__units_183_);
return v___x_187_;
}
default: 
{
lean_object* v___x_188_; lean_object* v___x_189_; 
v___x_188_ = lean_int_sub(v_D_184_, v_nu__units_183_);
v___x_189_ = lean_int_neg(v___x_188_);
lean_dec(v___x_188_);
return v___x_189_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_topological__charge__units___boxed(lean_object* v_nu__units_190_, lean_object* v_D_191_, lean_object* v_x_192_){
_start:
{
uint8_t v_x_62__boxed_193_; lean_object* v_res_194_; 
v_x_62__boxed_193_ = lean_unbox(v_x_192_);
v_res_194_ = lp_FiniteQuantum_InstantonDyonGas_topological__charge__units(v_nu__units_190_, v_D_191_, v_x_62__boxed_193_);
lean_dec(v_D_191_);
lean_dec(v_nu__units_190_);
return v_res_194_;
}
}
static lean_object* _init_lp_FiniteQuantum_InstantonDyonGas_dirac__phase___closed__0(void){
_start:
{
lean_object* v___x_195_; lean_object* v___x_196_; 
v___x_195_ = lean_unsigned_to_nat(0u);
v___x_196_ = lean_nat_to_int(v___x_195_);
return v___x_196_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dirac__phase(lean_object* v_lk_197_){
_start:
{
lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_200_; uint8_t v___x_201_; 
v___x_198_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__8);
v___x_199_ = lean_int_emod(v_lk_197_, v___x_198_);
v___x_200_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_dirac__phase___closed__0, &lp_FiniteQuantum_InstantonDyonGas_dirac__phase___closed__0_once, _init_lp_FiniteQuantum_InstantonDyonGas_dirac__phase___closed__0);
v___x_201_ = lean_int_dec_eq(v___x_199_, v___x_200_);
lean_dec(v___x_199_);
if (v___x_201_ == 0)
{
lean_object* v___x_202_; 
v___x_202_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0, &lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0_once, _init_lp_FiniteQuantum_InstantonDyonGas_magnetic__charge___closed__0);
return v___x_202_;
}
else
{
lean_object* v___x_203_; 
v___x_203_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
return v___x_203_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dirac__phase___boxed(lean_object* v_lk_204_){
_start:
{
lean_object* v_res_205_; 
v_res_205_ = lp_FiniteQuantum_InstantonDyonGas_dirac__phase(v_lk_204_);
lean_dec(v_lk_204_);
return v_res_205_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dyonDefectMass(lean_object* v_phase_206_){
_start:
{
lean_object* v___x_207_; uint8_t v___x_208_; 
v___x_207_ = lean_obj_once(&lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9, &lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9_once, _init_lp_FiniteQuantum_InstantonDyonGas_instReprDyonSpecies_repr___closed__9);
v___x_208_ = lean_int_dec_eq(v_phase_206_, v___x_207_);
if (v___x_208_ == 0)
{
lean_object* v___x_209_; 
v___x_209_ = lean_unsigned_to_nat(2u);
return v___x_209_;
}
else
{
lean_object* v___x_210_; 
v___x_210_ = lean_unsigned_to_nat(0u);
return v___x_210_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_InstantonDyonGas_dyonDefectMass___boxed(lean_object* v_phase_211_){
_start:
{
lean_object* v_res_212_; 
v_res_212_ = lp_FiniteQuantum_InstantonDyonGas_dyonDefectMass(v_phase_211_);
lean_dec(v_phase_211_);
return v_res_212_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_InstantonDyonGas(uint8_t builtin) {
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
