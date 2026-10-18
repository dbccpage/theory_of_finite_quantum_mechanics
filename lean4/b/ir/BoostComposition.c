// Lean compiler output
// Module: BoostComposition
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
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BoostComposition_Coord3_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BoostComposition_instDecidableEqCoord3(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_instDecidableEqCoord3___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 27, .m_capacity = 27, .m_length = 26, .m_data = "BoostComposition.Coord3.c0"};
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 27, .m_capacity = 27, .m_length = 26, .m_data = "BoostComposition.Coord3.c1"};
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 27, .m_capacity = 27, .m_length = 26, .m_data = "BoostComposition.Coord3.c2"};
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__5_value;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_BoostComposition_instReprCoord3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3___closed__0 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3 = (const lean_object*)&lp_FiniteQuantum_BoostComposition_instReprCoord3___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mkMat3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mkMat3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_id3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_id3___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_id3(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_id3___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mul3(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mul3___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_transpose3(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_transpose3___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_tr3(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_det3(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_eta3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_eta3___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_eta3(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_eta3___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat2___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__0;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__1;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__2;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__3;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__0;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__1;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__2;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__3;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__4;
static lean_once_cell_t lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_frozenPairCosineNumerator;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_frozenPairCosineDenominator;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx(uint8_t v_x_1_){
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
default: 
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(2u);
return v___x_4_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx___boxed(lean_object* v_x_5_){
_start:
{
uint8_t v_x_boxed_6_; lean_object* v_res_7_; 
v_x_boxed_6_ = lean_unbox(v_x_5_);
v_res_7_ = lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx(v_x_boxed_6_);
return v_res_7_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_toCtorIdx(uint8_t v_x_8_){
_start:
{
lean_object* v___x_9_; 
v___x_9_ = lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx(v_x_8_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_toCtorIdx___boxed(lean_object* v_x_10_){
_start:
{
uint8_t v_x_4__boxed_11_; lean_object* v_res_12_; 
v_x_4__boxed_11_ = lean_unbox(v_x_10_);
v_res_12_ = lp_FiniteQuantum_BoostComposition_Coord3_toCtorIdx(v_x_4__boxed_11_);
return v_res_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___redArg(lean_object* v_k_13_){
_start:
{
lean_inc(v_k_13_);
return v_k_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___redArg___boxed(lean_object* v_k_14_){
_start:
{
lean_object* v_res_15_; 
v_res_15_ = lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___redArg(v_k_14_);
lean_dec(v_k_14_);
return v_res_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim(lean_object* v_motive_16_, lean_object* v_ctorIdx_17_, uint8_t v_t_18_, lean_object* v_h_19_, lean_object* v_k_20_){
_start:
{
lean_inc(v_k_20_);
return v_k_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ctorElim___boxed(lean_object* v_motive_21_, lean_object* v_ctorIdx_22_, lean_object* v_t_23_, lean_object* v_h_24_, lean_object* v_k_25_){
_start:
{
uint8_t v_t_boxed_26_; lean_object* v_res_27_; 
v_t_boxed_26_ = lean_unbox(v_t_23_);
v_res_27_ = lp_FiniteQuantum_BoostComposition_Coord3_ctorElim(v_motive_21_, v_ctorIdx_22_, v_t_boxed_26_, v_h_24_, v_k_25_);
lean_dec(v_k_25_);
lean_dec(v_ctorIdx_22_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___redArg(lean_object* v_c0_28_){
_start:
{
lean_inc(v_c0_28_);
return v_c0_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___redArg___boxed(lean_object* v_c0_29_){
_start:
{
lean_object* v_res_30_; 
v_res_30_ = lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___redArg(v_c0_29_);
lean_dec(v_c0_29_);
return v_res_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim(lean_object* v_motive_31_, uint8_t v_t_32_, lean_object* v_h_33_, lean_object* v_c0_34_){
_start:
{
lean_inc(v_c0_34_);
return v_c0_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c0_elim___boxed(lean_object* v_motive_35_, lean_object* v_t_36_, lean_object* v_h_37_, lean_object* v_c0_38_){
_start:
{
uint8_t v_t_boxed_39_; lean_object* v_res_40_; 
v_t_boxed_39_ = lean_unbox(v_t_36_);
v_res_40_ = lp_FiniteQuantum_BoostComposition_Coord3_c0_elim(v_motive_35_, v_t_boxed_39_, v_h_37_, v_c0_38_);
lean_dec(v_c0_38_);
return v_res_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___redArg(lean_object* v_c1_41_){
_start:
{
lean_inc(v_c1_41_);
return v_c1_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___redArg___boxed(lean_object* v_c1_42_){
_start:
{
lean_object* v_res_43_; 
v_res_43_ = lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___redArg(v_c1_42_);
lean_dec(v_c1_42_);
return v_res_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim(lean_object* v_motive_44_, uint8_t v_t_45_, lean_object* v_h_46_, lean_object* v_c1_47_){
_start:
{
lean_inc(v_c1_47_);
return v_c1_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c1_elim___boxed(lean_object* v_motive_48_, lean_object* v_t_49_, lean_object* v_h_50_, lean_object* v_c1_51_){
_start:
{
uint8_t v_t_boxed_52_; lean_object* v_res_53_; 
v_t_boxed_52_ = lean_unbox(v_t_49_);
v_res_53_ = lp_FiniteQuantum_BoostComposition_Coord3_c1_elim(v_motive_48_, v_t_boxed_52_, v_h_50_, v_c1_51_);
lean_dec(v_c1_51_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___redArg(lean_object* v_c2_54_){
_start:
{
lean_inc(v_c2_54_);
return v_c2_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___redArg___boxed(lean_object* v_c2_55_){
_start:
{
lean_object* v_res_56_; 
v_res_56_ = lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___redArg(v_c2_55_);
lean_dec(v_c2_55_);
return v_res_56_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim(lean_object* v_motive_57_, uint8_t v_t_58_, lean_object* v_h_59_, lean_object* v_c2_60_){
_start:
{
lean_inc(v_c2_60_);
return v_c2_60_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_c2_elim___boxed(lean_object* v_motive_61_, lean_object* v_t_62_, lean_object* v_h_63_, lean_object* v_c2_64_){
_start:
{
uint8_t v_t_boxed_65_; lean_object* v_res_66_; 
v_t_boxed_65_ = lean_unbox(v_t_62_);
v_res_66_ = lp_FiniteQuantum_BoostComposition_Coord3_c2_elim(v_motive_61_, v_t_boxed_65_, v_h_63_, v_c2_64_);
lean_dec(v_c2_64_);
return v_res_66_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BoostComposition_Coord3_ofNat(lean_object* v_n_67_){
_start:
{
lean_object* v___x_68_; uint8_t v___x_69_; 
v___x_68_ = lean_unsigned_to_nat(0u);
v___x_69_ = lean_nat_dec_le(v_n_67_, v___x_68_);
if (v___x_69_ == 0)
{
lean_object* v___x_70_; uint8_t v___x_71_; 
v___x_70_ = lean_unsigned_to_nat(1u);
v___x_71_ = lean_nat_dec_le(v_n_67_, v___x_70_);
if (v___x_71_ == 0)
{
uint8_t v___x_72_; 
v___x_72_ = 2;
return v___x_72_;
}
else
{
uint8_t v___x_73_; 
v___x_73_ = 1;
return v___x_73_;
}
}
else
{
uint8_t v___x_74_; 
v___x_74_ = 0;
return v___x_74_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_Coord3_ofNat___boxed(lean_object* v_n_75_){
_start:
{
uint8_t v_res_76_; lean_object* v_r_77_; 
v_res_76_ = lp_FiniteQuantum_BoostComposition_Coord3_ofNat(v_n_75_);
lean_dec(v_n_75_);
v_r_77_ = lean_box(v_res_76_);
return v_r_77_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BoostComposition_instDecidableEqCoord3(uint8_t v_x_78_, uint8_t v_y_79_){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; uint8_t v___x_82_; 
v___x_80_ = lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx(v_x_78_);
v___x_81_ = lp_FiniteQuantum_BoostComposition_Coord3_ctorIdx(v_y_79_);
v___x_82_ = lean_nat_dec_eq(v___x_80_, v___x_81_);
lean_dec(v___x_81_);
lean_dec(v___x_80_);
return v___x_82_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_instDecidableEqCoord3___boxed(lean_object* v_x_83_, lean_object* v_y_84_){
_start:
{
uint8_t v_x_13__boxed_85_; uint8_t v_y_14__boxed_86_; uint8_t v_res_87_; lean_object* v_r_88_; 
v_x_13__boxed_85_ = lean_unbox(v_x_83_);
v_y_14__boxed_86_ = lean_unbox(v_y_84_);
v_res_87_ = lp_FiniteQuantum_BoostComposition_instDecidableEqCoord3(v_x_13__boxed_85_, v_y_14__boxed_86_);
v_r_88_ = lean_box(v_res_87_);
return v_r_88_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6(void){
_start:
{
lean_object* v___x_98_; lean_object* v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(2u);
v___x_99_ = lean_nat_to_int(v___x_98_);
return v___x_99_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7(void){
_start:
{
lean_object* v___x_100_; lean_object* v___x_101_; 
v___x_100_ = lean_unsigned_to_nat(1u);
v___x_101_ = lean_nat_to_int(v___x_100_);
return v___x_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr(uint8_t v_x_102_, lean_object* v_prec_103_){
_start:
{
lean_object* v___y_105_; lean_object* v___y_112_; lean_object* v___y_119_; 
switch(v_x_102_)
{
case 0:
{
lean_object* v___x_125_; uint8_t v___x_126_; 
v___x_125_ = lean_unsigned_to_nat(1024u);
v___x_126_ = lean_nat_dec_le(v___x_125_, v_prec_103_);
if (v___x_126_ == 0)
{
lean_object* v___x_127_; 
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6);
v___y_105_ = v___x_127_;
goto v___jp_104_;
}
else
{
lean_object* v___x_128_; 
v___x_128_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7);
v___y_105_ = v___x_128_;
goto v___jp_104_;
}
}
case 1:
{
lean_object* v___x_129_; uint8_t v___x_130_; 
v___x_129_ = lean_unsigned_to_nat(1024u);
v___x_130_ = lean_nat_dec_le(v___x_129_, v_prec_103_);
if (v___x_130_ == 0)
{
lean_object* v___x_131_; 
v___x_131_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6);
v___y_112_ = v___x_131_;
goto v___jp_111_;
}
else
{
lean_object* v___x_132_; 
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7);
v___y_112_ = v___x_132_;
goto v___jp_111_;
}
}
default: 
{
lean_object* v___x_133_; uint8_t v___x_134_; 
v___x_133_ = lean_unsigned_to_nat(1024u);
v___x_134_ = lean_nat_dec_le(v___x_133_, v_prec_103_);
if (v___x_134_ == 0)
{
lean_object* v___x_135_; 
v___x_135_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__6);
v___y_119_ = v___x_135_;
goto v___jp_118_;
}
else
{
lean_object* v___x_136_; 
v___x_136_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7);
v___y_119_ = v___x_136_;
goto v___jp_118_;
}
}
}
v___jp_104_:
{
lean_object* v___x_106_; lean_object* v___x_107_; uint8_t v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; 
v___x_106_ = ((lean_object*)(lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__1));
lean_inc(v___y_105_);
v___x_107_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_107_, 0, v___y_105_);
lean_ctor_set(v___x_107_, 1, v___x_106_);
v___x_108_ = 0;
v___x_109_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_109_, 0, v___x_107_);
lean_ctor_set_uint8(v___x_109_, sizeof(void*)*1, v___x_108_);
v___x_110_ = l_Repr_addAppParen(v___x_109_, v_prec_103_);
return v___x_110_;
}
v___jp_111_:
{
lean_object* v___x_113_; lean_object* v___x_114_; uint8_t v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; 
v___x_113_ = ((lean_object*)(lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__3));
lean_inc(v___y_112_);
v___x_114_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_114_, 0, v___y_112_);
lean_ctor_set(v___x_114_, 1, v___x_113_);
v___x_115_ = 0;
v___x_116_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_116_, 0, v___x_114_);
lean_ctor_set_uint8(v___x_116_, sizeof(void*)*1, v___x_115_);
v___x_117_ = l_Repr_addAppParen(v___x_116_, v_prec_103_);
return v___x_117_;
}
v___jp_118_:
{
lean_object* v___x_120_; lean_object* v___x_121_; uint8_t v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; 
v___x_120_ = ((lean_object*)(lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__5));
lean_inc(v___y_119_);
v___x_121_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_121_, 0, v___y_119_);
lean_ctor_set(v___x_121_, 1, v___x_120_);
v___x_122_ = 0;
v___x_123_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_123_, 0, v___x_121_);
lean_ctor_set_uint8(v___x_123_, sizeof(void*)*1, v___x_122_);
v___x_124_ = l_Repr_addAppParen(v___x_123_, v_prec_103_);
return v___x_124_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___boxed(lean_object* v_x_137_, lean_object* v_prec_138_){
_start:
{
uint8_t v_x_177__boxed_139_; lean_object* v_res_140_; 
v_x_177__boxed_139_ = lean_unbox(v_x_137_);
v_res_140_ = lp_FiniteQuantum_BoostComposition_instReprCoord3_repr(v_x_177__boxed_139_, v_prec_138_);
lean_dec(v_prec_138_);
return v_res_140_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mkMat3(lean_object* v_a00_143_, lean_object* v_a01_144_, lean_object* v_a02_145_, lean_object* v_a10_146_, lean_object* v_a11_147_, lean_object* v_a12_148_, lean_object* v_a20_149_, lean_object* v_a21_150_, lean_object* v_a22_151_, uint8_t v_i_152_, uint8_t v_j_153_){
_start:
{
switch(v_i_152_)
{
case 0:
{
switch(v_j_153_)
{
case 0:
{
lean_inc(v_a00_143_);
return v_a00_143_;
}
case 1:
{
lean_inc(v_a01_144_);
return v_a01_144_;
}
default: 
{
lean_inc(v_a02_145_);
return v_a02_145_;
}
}
}
case 1:
{
switch(v_j_153_)
{
case 0:
{
lean_inc(v_a10_146_);
return v_a10_146_;
}
case 1:
{
lean_inc(v_a11_147_);
return v_a11_147_;
}
default: 
{
lean_inc(v_a12_148_);
return v_a12_148_;
}
}
}
default: 
{
switch(v_j_153_)
{
case 0:
{
lean_inc(v_a20_149_);
return v_a20_149_;
}
case 1:
{
lean_inc(v_a21_150_);
return v_a21_150_;
}
default: 
{
lean_inc(v_a22_151_);
return v_a22_151_;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mkMat3___boxed(lean_object* v_a00_154_, lean_object* v_a01_155_, lean_object* v_a02_156_, lean_object* v_a10_157_, lean_object* v_a11_158_, lean_object* v_a12_159_, lean_object* v_a20_160_, lean_object* v_a21_161_, lean_object* v_a22_162_, lean_object* v_i_163_, lean_object* v_j_164_){
_start:
{
uint8_t v_i_boxed_165_; uint8_t v_j_boxed_166_; lean_object* v_res_167_; 
v_i_boxed_165_ = lean_unbox(v_i_163_);
v_j_boxed_166_ = lean_unbox(v_j_164_);
v_res_167_ = lp_FiniteQuantum_BoostComposition_mkMat3(v_a00_154_, v_a01_155_, v_a02_156_, v_a10_157_, v_a11_158_, v_a12_159_, v_a20_160_, v_a21_161_, v_a22_162_, v_i_boxed_165_, v_j_boxed_166_);
lean_dec(v_a22_162_);
lean_dec(v_a21_161_);
lean_dec(v_a20_160_);
lean_dec(v_a12_159_);
lean_dec(v_a11_158_);
lean_dec(v_a10_157_);
lean_dec(v_a02_156_);
lean_dec(v_a01_155_);
lean_dec(v_a00_154_);
return v_res_167_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_id3___closed__0(void){
_start:
{
lean_object* v___x_168_; lean_object* v___x_169_; 
v___x_168_ = lean_unsigned_to_nat(0u);
v___x_169_ = lean_nat_to_int(v___x_168_);
return v___x_169_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_id3(uint8_t v_a_170_, uint8_t v_a_171_){
_start:
{
lean_object* v___x_172_; lean_object* v___x_173_; lean_object* v___x_174_; 
v___x_172_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7);
v___x_173_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_id3___closed__0, &lp_FiniteQuantum_BoostComposition_id3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_id3___closed__0);
v___x_174_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_172_, v___x_173_, v___x_173_, v___x_173_, v___x_172_, v___x_173_, v___x_173_, v___x_173_, v___x_172_, v_a_170_, v_a_171_);
return v___x_174_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_id3___boxed(lean_object* v_a_175_, lean_object* v_a_176_){
_start:
{
uint8_t v_a_21__boxed_177_; uint8_t v_a_22__boxed_178_; lean_object* v_res_179_; 
v_a_21__boxed_177_ = lean_unbox(v_a_175_);
v_a_22__boxed_178_ = lean_unbox(v_a_176_);
v_res_179_ = lp_FiniteQuantum_BoostComposition_id3(v_a_21__boxed_177_, v_a_22__boxed_178_);
return v_res_179_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mul3(lean_object* v_A_180_, lean_object* v_B_181_, uint8_t v_i_182_, uint8_t v_k_183_){
_start:
{
uint8_t v___x_184_; lean_object* v___x_185_; lean_object* v___x_186_; lean_object* v___x_187_; lean_object* v___x_188_; lean_object* v___x_189_; lean_object* v___x_190_; lean_object* v___x_191_; uint8_t v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; lean_object* v___x_197_; lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_200_; uint8_t v___x_201_; lean_object* v___x_202_; lean_object* v___x_203_; lean_object* v___x_204_; lean_object* v___x_205_; lean_object* v___x_206_; lean_object* v___x_207_; lean_object* v___x_208_; lean_object* v___x_209_; 
v___x_184_ = 0;
v___x_185_ = lean_box(v_i_182_);
v___x_186_ = lean_box(v___x_184_);
lean_inc_ref_n(v_A_180_, 2);
v___x_187_ = lean_apply_2(v_A_180_, v___x_185_, v___x_186_);
v___x_188_ = lean_box(v___x_184_);
v___x_189_ = lean_box(v_k_183_);
lean_inc_ref_n(v_B_181_, 2);
v___x_190_ = lean_apply_2(v_B_181_, v___x_188_, v___x_189_);
v___x_191_ = lean_int_mul(v___x_187_, v___x_190_);
lean_dec(v___x_190_);
lean_dec(v___x_187_);
v___x_192_ = 1;
v___x_193_ = lean_box(v_i_182_);
v___x_194_ = lean_box(v___x_192_);
v___x_195_ = lean_apply_2(v_A_180_, v___x_193_, v___x_194_);
v___x_196_ = lean_box(v___x_192_);
v___x_197_ = lean_box(v_k_183_);
v___x_198_ = lean_apply_2(v_B_181_, v___x_196_, v___x_197_);
v___x_199_ = lean_int_mul(v___x_195_, v___x_198_);
lean_dec(v___x_198_);
lean_dec(v___x_195_);
v___x_200_ = lean_int_add(v___x_191_, v___x_199_);
lean_dec(v___x_199_);
lean_dec(v___x_191_);
v___x_201_ = 2;
v___x_202_ = lean_box(v_i_182_);
v___x_203_ = lean_box(v___x_201_);
v___x_204_ = lean_apply_2(v_A_180_, v___x_202_, v___x_203_);
v___x_205_ = lean_box(v___x_201_);
v___x_206_ = lean_box(v_k_183_);
v___x_207_ = lean_apply_2(v_B_181_, v___x_205_, v___x_206_);
v___x_208_ = lean_int_mul(v___x_204_, v___x_207_);
lean_dec(v___x_207_);
lean_dec(v___x_204_);
v___x_209_ = lean_int_add(v___x_200_, v___x_208_);
lean_dec(v___x_208_);
lean_dec(v___x_200_);
return v___x_209_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_mul3___boxed(lean_object* v_A_210_, lean_object* v_B_211_, lean_object* v_i_212_, lean_object* v_k_213_){
_start:
{
uint8_t v_i_boxed_214_; uint8_t v_k_boxed_215_; lean_object* v_res_216_; 
v_i_boxed_214_ = lean_unbox(v_i_212_);
v_k_boxed_215_ = lean_unbox(v_k_213_);
v_res_216_ = lp_FiniteQuantum_BoostComposition_mul3(v_A_210_, v_B_211_, v_i_boxed_214_, v_k_boxed_215_);
return v_res_216_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_transpose3(lean_object* v_A_217_, uint8_t v_i_218_, uint8_t v_j_219_){
_start:
{
lean_object* v___x_220_; lean_object* v___x_221_; lean_object* v___x_222_; 
v___x_220_ = lean_box(v_j_219_);
v___x_221_ = lean_box(v_i_218_);
v___x_222_ = lean_apply_2(v_A_217_, v___x_220_, v___x_221_);
return v___x_222_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_transpose3___boxed(lean_object* v_A_223_, lean_object* v_i_224_, lean_object* v_j_225_){
_start:
{
uint8_t v_i_boxed_226_; uint8_t v_j_boxed_227_; lean_object* v_res_228_; 
v_i_boxed_226_ = lean_unbox(v_i_224_);
v_j_boxed_227_ = lean_unbox(v_j_225_);
v_res_228_ = lp_FiniteQuantum_BoostComposition_transpose3(v_A_223_, v_i_boxed_226_, v_j_boxed_227_);
return v_res_228_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_tr3(lean_object* v_A_229_){
_start:
{
uint8_t v___x_230_; lean_object* v___x_231_; lean_object* v___x_232_; lean_object* v___x_233_; uint8_t v___x_234_; lean_object* v___x_235_; lean_object* v___x_236_; lean_object* v___x_237_; lean_object* v___x_238_; uint8_t v___x_239_; lean_object* v___x_240_; lean_object* v___x_241_; lean_object* v___x_242_; lean_object* v___x_243_; 
v___x_230_ = 0;
v___x_231_ = lean_box(v___x_230_);
v___x_232_ = lean_box(v___x_230_);
lean_inc_ref_n(v_A_229_, 2);
v___x_233_ = lean_apply_2(v_A_229_, v___x_231_, v___x_232_);
v___x_234_ = 1;
v___x_235_ = lean_box(v___x_234_);
v___x_236_ = lean_box(v___x_234_);
v___x_237_ = lean_apply_2(v_A_229_, v___x_235_, v___x_236_);
v___x_238_ = lean_int_add(v___x_233_, v___x_237_);
lean_dec(v___x_237_);
lean_dec(v___x_233_);
v___x_239_ = 2;
v___x_240_ = lean_box(v___x_239_);
v___x_241_ = lean_box(v___x_239_);
v___x_242_ = lean_apply_2(v_A_229_, v___x_240_, v___x_241_);
v___x_243_ = lean_int_add(v___x_238_, v___x_242_);
lean_dec(v___x_242_);
lean_dec(v___x_238_);
return v___x_243_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_det3(lean_object* v_A_244_){
_start:
{
uint8_t v___x_245_; lean_object* v___x_246_; lean_object* v___x_247_; lean_object* v___x_248_; uint8_t v___x_249_; lean_object* v___x_250_; lean_object* v___x_251_; lean_object* v___x_252_; uint8_t v___x_253_; lean_object* v___x_254_; lean_object* v___x_255_; lean_object* v___x_256_; lean_object* v___x_257_; lean_object* v___x_258_; lean_object* v___x_259_; lean_object* v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; lean_object* v___x_263_; lean_object* v___x_264_; lean_object* v___x_265_; lean_object* v___x_266_; lean_object* v___x_267_; lean_object* v___x_268_; lean_object* v___x_269_; lean_object* v___x_270_; lean_object* v___x_271_; lean_object* v___x_272_; lean_object* v___x_273_; lean_object* v___x_274_; lean_object* v___x_275_; lean_object* v___x_276_; lean_object* v___x_277_; lean_object* v___x_278_; lean_object* v___x_279_; lean_object* v___x_280_; lean_object* v___x_281_; lean_object* v___x_282_; lean_object* v___x_283_; lean_object* v___x_284_; lean_object* v___x_285_; lean_object* v___x_286_; lean_object* v___x_287_; lean_object* v___x_288_; 
v___x_245_ = 0;
v___x_246_ = lean_box(v___x_245_);
v___x_247_ = lean_box(v___x_245_);
lean_inc_ref_n(v_A_244_, 8);
v___x_248_ = lean_apply_2(v_A_244_, v___x_246_, v___x_247_);
v___x_249_ = 1;
v___x_250_ = lean_box(v___x_249_);
v___x_251_ = lean_box(v___x_249_);
v___x_252_ = lean_apply_2(v_A_244_, v___x_250_, v___x_251_);
v___x_253_ = 2;
v___x_254_ = lean_box(v___x_253_);
v___x_255_ = lean_box(v___x_253_);
v___x_256_ = lean_apply_2(v_A_244_, v___x_254_, v___x_255_);
v___x_257_ = lean_int_mul(v___x_252_, v___x_256_);
v___x_258_ = lean_box(v___x_249_);
v___x_259_ = lean_box(v___x_253_);
v___x_260_ = lean_apply_2(v_A_244_, v___x_258_, v___x_259_);
v___x_261_ = lean_box(v___x_253_);
v___x_262_ = lean_box(v___x_249_);
v___x_263_ = lean_apply_2(v_A_244_, v___x_261_, v___x_262_);
v___x_264_ = lean_int_mul(v___x_260_, v___x_263_);
v___x_265_ = lean_int_sub(v___x_257_, v___x_264_);
lean_dec(v___x_264_);
lean_dec(v___x_257_);
v___x_266_ = lean_int_mul(v___x_248_, v___x_265_);
lean_dec(v___x_265_);
lean_dec(v___x_248_);
v___x_267_ = lean_box(v___x_245_);
v___x_268_ = lean_box(v___x_249_);
v___x_269_ = lean_apply_2(v_A_244_, v___x_267_, v___x_268_);
v___x_270_ = lean_box(v___x_249_);
v___x_271_ = lean_box(v___x_245_);
v___x_272_ = lean_apply_2(v_A_244_, v___x_270_, v___x_271_);
v___x_273_ = lean_int_mul(v___x_272_, v___x_256_);
lean_dec(v___x_256_);
v___x_274_ = lean_box(v___x_253_);
v___x_275_ = lean_box(v___x_245_);
v___x_276_ = lean_apply_2(v_A_244_, v___x_274_, v___x_275_);
v___x_277_ = lean_int_mul(v___x_260_, v___x_276_);
lean_dec(v___x_260_);
v___x_278_ = lean_int_sub(v___x_273_, v___x_277_);
lean_dec(v___x_277_);
lean_dec(v___x_273_);
v___x_279_ = lean_int_mul(v___x_269_, v___x_278_);
lean_dec(v___x_278_);
lean_dec(v___x_269_);
v___x_280_ = lean_int_sub(v___x_266_, v___x_279_);
lean_dec(v___x_279_);
lean_dec(v___x_266_);
v___x_281_ = lean_box(v___x_245_);
v___x_282_ = lean_box(v___x_253_);
v___x_283_ = lean_apply_2(v_A_244_, v___x_281_, v___x_282_);
v___x_284_ = lean_int_mul(v___x_272_, v___x_263_);
lean_dec(v___x_263_);
lean_dec(v___x_272_);
v___x_285_ = lean_int_mul(v___x_252_, v___x_276_);
lean_dec(v___x_276_);
lean_dec(v___x_252_);
v___x_286_ = lean_int_sub(v___x_284_, v___x_285_);
lean_dec(v___x_285_);
lean_dec(v___x_284_);
v___x_287_ = lean_int_mul(v___x_283_, v___x_286_);
lean_dec(v___x_286_);
lean_dec(v___x_283_);
v___x_288_ = lean_int_add(v___x_280_, v___x_287_);
lean_dec(v___x_287_);
lean_dec(v___x_280_);
return v___x_288_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_eta3___closed__0(void){
_start:
{
lean_object* v___x_289_; lean_object* v___x_290_; 
v___x_289_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7);
v___x_290_ = lean_int_neg(v___x_289_);
return v___x_290_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_eta3(uint8_t v_a_291_, uint8_t v_a_292_){
_start:
{
lean_object* v___x_293_; lean_object* v___x_294_; lean_object* v___x_295_; lean_object* v___x_296_; 
v___x_293_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7, &lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7_once, _init_lp_FiniteQuantum_BoostComposition_instReprCoord3_repr___closed__7);
v___x_294_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_id3___closed__0, &lp_FiniteQuantum_BoostComposition_id3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_id3___closed__0);
v___x_295_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_eta3___closed__0, &lp_FiniteQuantum_BoostComposition_eta3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_eta3___closed__0);
v___x_296_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_293_, v___x_294_, v___x_294_, v___x_294_, v___x_295_, v___x_294_, v___x_294_, v___x_294_, v___x_295_, v_a_291_, v_a_292_);
return v___x_296_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_eta3___boxed(lean_object* v_a_297_, lean_object* v_a_298_){
_start:
{
uint8_t v_a_28__boxed_299_; uint8_t v_a_29__boxed_300_; lean_object* v_res_301_; 
v_a_28__boxed_299_ = lean_unbox(v_a_297_);
v_a_29__boxed_300_ = lean_unbox(v_a_298_);
v_res_301_ = lp_FiniteQuantum_BoostComposition_eta3(v_a_28__boxed_299_, v_a_29__boxed_300_);
return v_res_301_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0(void){
_start:
{
lean_object* v___x_302_; lean_object* v___x_303_; 
v___x_302_ = lean_unsigned_to_nat(5u);
v___x_303_ = lean_nat_to_int(v___x_302_);
return v___x_303_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1(void){
_start:
{
lean_object* v___x_304_; lean_object* v___x_305_; 
v___x_304_ = lean_unsigned_to_nat(3u);
v___x_305_ = lean_nat_to_int(v___x_304_);
return v___x_305_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2(void){
_start:
{
lean_object* v___x_306_; lean_object* v___x_307_; 
v___x_306_ = lean_unsigned_to_nat(4u);
v___x_307_ = lean_nat_to_int(v___x_306_);
return v___x_307_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1(uint8_t v_a_308_, uint8_t v_a_309_){
_start:
{
lean_object* v___x_310_; lean_object* v___x_311_; lean_object* v___x_312_; lean_object* v___x_313_; lean_object* v___x_314_; 
v___x_310_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0, &lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0);
v___x_311_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1, &lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1_once, _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1);
v___x_312_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_id3___closed__0, &lp_FiniteQuantum_BoostComposition_id3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_id3___closed__0);
v___x_313_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2, &lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2_once, _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2);
v___x_314_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_310_, v___x_311_, v___x_312_, v___x_311_, v___x_310_, v___x_312_, v___x_312_, v___x_312_, v___x_313_, v_a_308_, v_a_309_);
return v___x_314_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___boxed(lean_object* v_a_315_, lean_object* v_a_316_){
_start:
{
uint8_t v_a_39__boxed_317_; uint8_t v_a_40__boxed_318_; lean_object* v_res_319_; 
v_a_39__boxed_317_ = lean_unbox(v_a_315_);
v_a_40__boxed_318_ = lean_unbox(v_a_316_);
v_res_319_ = lp_FiniteQuantum_BoostComposition_boostNumeratorMat1(v_a_39__boxed_317_, v_a_40__boxed_318_);
return v_res_319_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat2(uint8_t v_a_320_, uint8_t v_a_321_){
_start:
{
lean_object* v___x_322_; lean_object* v___x_323_; lean_object* v___x_324_; lean_object* v___x_325_; lean_object* v___x_326_; 
v___x_322_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0, &lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__0);
v___x_323_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_id3___closed__0, &lp_FiniteQuantum_BoostComposition_id3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_id3___closed__0);
v___x_324_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1, &lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1_once, _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__1);
v___x_325_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2, &lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2_once, _init_lp_FiniteQuantum_BoostComposition_boostNumeratorMat1___closed__2);
v___x_326_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_322_, v___x_323_, v___x_324_, v___x_323_, v___x_325_, v___x_323_, v___x_324_, v___x_323_, v___x_322_, v_a_320_, v_a_321_);
return v___x_326_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_boostNumeratorMat2___boxed(lean_object* v_a_327_, lean_object* v_a_328_){
_start:
{
uint8_t v_a_33__boxed_329_; uint8_t v_a_34__boxed_330_; lean_object* v_res_331_; 
v_a_33__boxed_329_ = lean_unbox(v_a_327_);
v_a_34__boxed_330_ = lean_unbox(v_a_328_);
v_res_331_ = lp_FiniteQuantum_BoostComposition_boostNumeratorMat2(v_a_33__boxed_329_, v_a_34__boxed_330_);
return v_res_331_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__0(void){
_start:
{
lean_object* v___x_332_; lean_object* v___x_333_; 
v___x_332_ = lean_unsigned_to_nat(25u);
v___x_333_ = lean_nat_to_int(v___x_332_);
return v___x_333_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__1(void){
_start:
{
lean_object* v___x_334_; lean_object* v___x_335_; 
v___x_334_ = lean_unsigned_to_nat(12u);
v___x_335_ = lean_nat_to_int(v___x_334_);
return v___x_335_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__2(void){
_start:
{
lean_object* v___x_336_; lean_object* v___x_337_; 
v___x_336_ = lean_unsigned_to_nat(15u);
v___x_337_ = lean_nat_to_int(v___x_336_);
return v___x_337_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__3(void){
_start:
{
lean_object* v___x_338_; lean_object* v___x_339_; 
v___x_338_ = lean_unsigned_to_nat(20u);
v___x_339_ = lean_nat_to_int(v___x_338_);
return v___x_339_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4(void){
_start:
{
lean_object* v___x_340_; lean_object* v___x_341_; 
v___x_340_ = lean_unsigned_to_nat(9u);
v___x_341_ = lean_nat_to_int(v___x_340_);
return v___x_341_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat(uint8_t v_a_342_, uint8_t v_a_343_){
_start:
{
lean_object* v___x_344_; lean_object* v___x_345_; lean_object* v___x_346_; lean_object* v___x_347_; lean_object* v___x_348_; lean_object* v___x_349_; lean_object* v___x_350_; 
v___x_344_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__0, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__0);
v___x_345_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__1, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__1_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__1);
v___x_346_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__2, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__2_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__2);
v___x_347_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__3, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__3_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__3);
v___x_348_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4);
v___x_349_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_id3___closed__0, &lp_FiniteQuantum_BoostComposition_id3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_id3___closed__0);
v___x_350_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_344_, v___x_345_, v___x_346_, v___x_346_, v___x_347_, v___x_348_, v___x_345_, v___x_349_, v___x_347_, v_a_342_, v_a_343_);
return v___x_350_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___boxed(lean_object* v_a_351_, lean_object* v_a_352_){
_start:
{
uint8_t v_a_57__boxed_353_; uint8_t v_a_58__boxed_354_; lean_object* v_res_355_; 
v_a_57__boxed_353_ = lean_unbox(v_a_351_);
v_a_58__boxed_354_ = lean_unbox(v_a_352_);
v_res_355_ = lp_FiniteQuantum_BoostComposition_compositionNumeratorMat(v_a_57__boxed_353_, v_a_58__boxed_354_);
return v_res_355_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0(void){
_start:
{
lean_object* v___x_356_; lean_object* v___x_357_; 
v___x_356_ = lean_unsigned_to_nat(41u);
v___x_357_ = lean_nat_to_int(v___x_356_);
return v___x_357_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1(void){
_start:
{
lean_object* v___x_358_; lean_object* v___x_359_; 
v___x_358_ = lean_unsigned_to_nat(40u);
v___x_359_ = lean_nat_to_int(v___x_358_);
return v___x_359_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__2(void){
_start:
{
lean_object* v___x_360_; lean_object* v___x_361_; 
v___x_360_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4);
v___x_361_ = lean_int_neg(v___x_360_);
return v___x_361_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat(uint8_t v_a_362_, uint8_t v_a_363_){
_start:
{
lean_object* v___x_364_; lean_object* v___x_365_; lean_object* v___x_366_; lean_object* v___x_367_; lean_object* v___x_368_; lean_object* v___x_369_; 
v___x_364_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0, &lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0);
v___x_365_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_id3___closed__0, &lp_FiniteQuantum_BoostComposition_id3___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_id3___closed__0);
v___x_366_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1, &lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1_once, _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1);
v___x_367_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4, &lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4_once, _init_lp_FiniteQuantum_BoostComposition_compositionNumeratorMat___closed__4);
v___x_368_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__2, &lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__2_once, _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__2);
v___x_369_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_364_, v___x_365_, v___x_365_, v___x_365_, v___x_366_, v___x_367_, v___x_365_, v___x_368_, v___x_366_, v_a_362_, v_a_363_);
return v___x_369_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___boxed(lean_object* v_a_370_, lean_object* v_a_371_){
_start:
{
uint8_t v_a_46__boxed_372_; uint8_t v_a_47__boxed_373_; lean_object* v_res_374_; 
v_a_46__boxed_372_ = lean_unbox(v_a_370_);
v_a_47__boxed_373_ = lean_unbox(v_a_371_);
v_res_374_ = lp_FiniteQuantum_BoostComposition_rotationNumeratorMat(v_a_46__boxed_372_, v_a_47__boxed_373_);
return v_res_374_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__0(void){
_start:
{
lean_object* v___x_375_; lean_object* v___x_376_; 
v___x_375_ = lean_unsigned_to_nat(1025u);
v___x_376_ = lean_nat_to_int(v___x_375_);
return v___x_376_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__1(void){
_start:
{
lean_object* v___x_377_; lean_object* v___x_378_; 
v___x_377_ = lean_unsigned_to_nat(615u);
v___x_378_ = lean_nat_to_int(v___x_377_);
return v___x_378_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__2(void){
_start:
{
lean_object* v___x_379_; lean_object* v___x_380_; 
v___x_379_ = lean_unsigned_to_nat(492u);
v___x_380_ = lean_nat_to_int(v___x_379_);
return v___x_380_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__3(void){
_start:
{
lean_object* v___x_381_; lean_object* v___x_382_; 
v___x_381_ = lean_unsigned_to_nat(881u);
v___x_382_ = lean_nat_to_int(v___x_381_);
return v___x_382_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__4(void){
_start:
{
lean_object* v___x_383_; lean_object* v___x_384_; 
v___x_383_ = lean_unsigned_to_nat(180u);
v___x_384_ = lean_nat_to_int(v___x_383_);
return v___x_384_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__5(void){
_start:
{
lean_object* v___x_385_; lean_object* v___x_386_; 
v___x_385_ = lean_unsigned_to_nat(800u);
v___x_386_ = lean_nat_to_int(v___x_385_);
return v___x_386_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat(uint8_t v_a_387_, uint8_t v_a_388_){
_start:
{
lean_object* v___x_389_; lean_object* v___x_390_; lean_object* v___x_391_; lean_object* v___x_392_; lean_object* v___x_393_; lean_object* v___x_394_; lean_object* v___x_395_; 
v___x_389_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__0, &lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__0);
v___x_390_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__1, &lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__1_once, _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__1);
v___x_391_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__2, &lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__2_once, _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__2);
v___x_392_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__3, &lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__3_once, _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__3);
v___x_393_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__4, &lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__4_once, _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__4);
v___x_394_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__5, &lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__5_once, _init_lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___closed__5);
v___x_395_ = lp_FiniteQuantum_BoostComposition_mkMat3(v___x_389_, v___x_390_, v___x_391_, v___x_390_, v___x_392_, v___x_393_, v___x_391_, v___x_393_, v___x_394_, v_a_387_, v_a_388_);
return v___x_395_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat___boxed(lean_object* v_a_396_, lean_object* v_a_397_){
_start:
{
uint8_t v_a_59__boxed_398_; uint8_t v_a_60__boxed_399_; lean_object* v_res_400_; 
v_a_59__boxed_398_ = lean_unbox(v_a_396_);
v_a_60__boxed_399_ = lean_unbox(v_a_397_);
v_res_400_ = lp_FiniteQuantum_BoostComposition_polarBoostNumeratorMat(v_a_59__boxed_398_, v_a_60__boxed_399_);
return v_res_400_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_frozenPairCosineNumerator(void){
_start:
{
lean_object* v___x_401_; 
v___x_401_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1, &lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1_once, _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__1);
return v___x_401_;
}
}
static lean_object* _init_lp_FiniteQuantum_BoostComposition_frozenPairCosineDenominator(void){
_start:
{
lean_object* v___x_402_; 
v___x_402_ = lean_obj_once(&lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0, &lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0_once, _init_lp_FiniteQuantum_BoostComposition_rotationNumeratorMat___closed__0);
return v___x_402_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_BoostComposition(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_BoostComposition_frozenPairCosineNumerator = _init_lp_FiniteQuantum_BoostComposition_frozenPairCosineNumerator();
lean_mark_persistent(lp_FiniteQuantum_BoostComposition_frozenPairCosineNumerator);
lp_FiniteQuantum_BoostComposition_frozenPairCosineDenominator = _init_lp_FiniteQuantum_BoostComposition_frozenPairCosineDenominator();
lean_mark_persistent(lp_FiniteQuantum_BoostComposition_frozenPairCosineDenominator);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
