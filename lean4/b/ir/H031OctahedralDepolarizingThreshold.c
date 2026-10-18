// Lean compiler output
// Module: H031OctahedralDepolarizingThreshold
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
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* l_Int_pow(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_emod(lean_object*, lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v0"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__17_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__18_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__18_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__19_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereMinor;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank;
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(3u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator(lean_object* v_a_3_, lean_object* v_d_4_){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v___x_5_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___closed__0);
v___x_6_ = lean_int_sub(v_d_4_, v_a_3_);
v___x_7_ = lean_unsigned_to_nat(2u);
v___x_8_ = l_Int_pow(v___x_6_, v___x_7_);
lean_dec(v___x_6_);
v___x_9_ = lean_int_mul(v___x_5_, v___x_8_);
lean_dec(v___x_8_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator___boxed(lean_object* v_a_10_, lean_object* v_d_11_){
_start:
{
lean_object* v_res_12_; 
v_res_12_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_bloch__numerator(v_a_10_, v_d_11_);
lean_dec(v_d_11_);
lean_dec(v_a_10_);
return v_res_12_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2_decEq(lean_object* v_x_13_, lean_object* v_x_14_){
_start:
{
lean_object* v_v0_15_; lean_object* v_v1_16_; lean_object* v_v2_17_; lean_object* v_v0_18_; lean_object* v_v1_19_; lean_object* v_v2_20_; uint8_t v___x_21_; 
v_v0_15_ = lean_ctor_get(v_x_13_, 0);
v_v1_16_ = lean_ctor_get(v_x_13_, 1);
v_v2_17_ = lean_ctor_get(v_x_13_, 2);
v_v0_18_ = lean_ctor_get(v_x_14_, 0);
v_v1_19_ = lean_ctor_get(v_x_14_, 1);
v_v2_20_ = lean_ctor_get(v_x_14_, 2);
v___x_21_ = lean_int_dec_eq(v_v0_15_, v_v0_18_);
if (v___x_21_ == 0)
{
return v___x_21_;
}
else
{
uint8_t v___x_22_; 
v___x_22_ = lean_int_dec_eq(v_v1_16_, v_v1_19_);
if (v___x_22_ == 0)
{
return v___x_22_;
}
else
{
uint8_t v___x_23_; 
v___x_23_ = lean_int_dec_eq(v_v2_17_, v_v2_20_);
return v___x_23_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2_decEq___boxed(lean_object* v_x_24_, lean_object* v_x_25_){
_start:
{
uint8_t v_res_26_; lean_object* v_r_27_; 
v_res_26_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2_decEq(v_x_24_, v_x_25_);
lean_dec_ref(v_x_25_);
lean_dec_ref(v_x_24_);
v_r_27_ = lean_box(v_res_26_);
return v_r_27_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2(lean_object* v_x_28_, lean_object* v_x_29_){
_start:
{
uint8_t v___x_30_; 
v___x_30_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2_decEq(v_x_28_, v_x_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2___boxed(lean_object* v_x_31_, lean_object* v_x_32_){
_start:
{
uint8_t v_res_33_; lean_object* v_r_34_; 
v_res_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_instDecidableEqVec3F2(v_x_31_, v_x_32_);
lean_dec_ref(v_x_32_);
lean_dec_ref(v_x_31_);
v_r_34_ = lean_box(v_res_33_);
return v_r_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_48_ = lean_unsigned_to_nat(6u);
v___x_49_ = lean_nat_to_int(v___x_48_);
return v___x_49_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_51_; lean_object* v___x_52_; 
v___x_51_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__0));
v___x_52_ = lean_string_length(v___x_51_);
return v___x_52_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__9);
v___x_54_ = lean_nat_to_int(v___x_53_);
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_62_; lean_object* v___x_63_; 
v___x_62_ = lean_unsigned_to_nat(0u);
v___x_63_ = lean_nat_to_int(v___x_62_);
return v___x_63_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg(lean_object* v_x_70_){
_start:
{
lean_object* v_v0_71_; lean_object* v_v1_72_; lean_object* v_v2_73_; lean_object* v___x_74_; lean_object* v___x_75_; lean_object* v___x_76_; lean_object* v___y_78_; uint8_t v___y_79_; lean_object* v___y_80_; lean_object* v___y_92_; lean_object* v___y_93_; lean_object* v___y_94_; uint8_t v___y_95_; lean_object* v___y_96_; lean_object* v___y_114_; lean_object* v___x_134_; lean_object* v___x_135_; uint8_t v___x_136_; 
v_v0_71_ = lean_ctor_get(v_x_70_, 0);
v_v1_72_ = lean_ctor_get(v_x_70_, 1);
v_v2_73_ = lean_ctor_get(v_x_70_, 2);
v___x_74_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__5));
v___x_75_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__6));
v___x_76_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__7);
v___x_134_ = lean_unsigned_to_nat(0u);
v___x_135_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_136_ = lean_int_dec_lt(v_v0_71_, v___x_135_);
if (v___x_136_ == 0)
{
lean_object* v___x_137_; lean_object* v___x_138_; 
v___x_137_ = l_Int_repr(v_v0_71_);
v___x_138_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_138_, 0, v___x_137_);
v___y_114_ = v___x_138_;
goto v___jp_113_;
}
else
{
lean_object* v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; 
v___x_139_ = l_Int_repr(v_v0_71_);
v___x_140_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_140_, 0, v___x_139_);
v___x_141_ = l_Repr_addAppParen(v___x_140_, v___x_134_);
v___y_114_ = v___x_141_;
goto v___jp_113_;
}
v___jp_77_:
{
lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; lean_object* v___x_86_; lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; 
v___x_81_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_81_, 0, v___x_76_);
lean_ctor_set(v___x_81_, 1, v___y_80_);
v___x_82_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_82_, 0, v___x_81_);
lean_ctor_set_uint8(v___x_82_, sizeof(void*)*1, v___y_79_);
v___x_83_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_83_, 0, v___y_78_);
lean_ctor_set(v___x_83_, 1, v___x_82_);
v___x_84_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__10);
v___x_85_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__11));
v___x_86_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_85_);
lean_ctor_set(v___x_86_, 1, v___x_83_);
v___x_87_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__12));
v___x_88_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_88_, 0, v___x_86_);
lean_ctor_set(v___x_88_, 1, v___x_87_);
v___x_89_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_84_);
lean_ctor_set(v___x_89_, 1, v___x_88_);
v___x_90_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_90_, 0, v___x_89_);
lean_ctor_set_uint8(v___x_90_, sizeof(void*)*1, v___y_79_);
return v___x_90_;
}
v___jp_91_:
{
lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; lean_object* v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; lean_object* v___x_106_; uint8_t v___x_107_; 
v___x_97_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_97_, 0, v___x_76_);
lean_ctor_set(v___x_97_, 1, v___y_96_);
v___x_98_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_98_, 0, v___x_97_);
lean_ctor_set_uint8(v___x_98_, sizeof(void*)*1, v___y_95_);
v___x_99_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_99_, 0, v___y_93_);
lean_ctor_set(v___x_99_, 1, v___x_98_);
lean_inc(v___y_92_);
v___x_100_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_100_, 0, v___x_99_);
lean_ctor_set(v___x_100_, 1, v___y_92_);
lean_inc(v___y_94_);
v___x_101_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_101_, 0, v___x_100_);
lean_ctor_set(v___x_101_, 1, v___y_94_);
v___x_102_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__14));
v___x_103_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_103_, 0, v___x_101_);
lean_ctor_set(v___x_103_, 1, v___x_102_);
v___x_104_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_104_, 0, v___x_103_);
lean_ctor_set(v___x_104_, 1, v___x_74_);
v___x_105_ = lean_unsigned_to_nat(0u);
v___x_106_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_107_ = lean_int_dec_lt(v_v2_73_, v___x_106_);
if (v___x_107_ == 0)
{
lean_object* v___x_108_; lean_object* v___x_109_; 
v___x_108_ = l_Int_repr(v_v2_73_);
v___x_109_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_109_, 0, v___x_108_);
v___y_78_ = v___x_104_;
v___y_79_ = v___y_95_;
v___y_80_ = v___x_109_;
goto v___jp_77_;
}
else
{
lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; 
v___x_110_ = l_Int_repr(v_v2_73_);
v___x_111_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_111_, 0, v___x_110_);
v___x_112_ = l_Repr_addAppParen(v___x_111_, v___x_105_);
v___y_78_ = v___x_104_;
v___y_79_ = v___y_95_;
v___y_80_ = v___x_112_;
goto v___jp_77_;
}
}
v___jp_113_:
{
lean_object* v___x_115_; uint8_t v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; lean_object* v___x_127_; uint8_t v___x_128_; 
v___x_115_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_115_, 0, v___x_76_);
lean_ctor_set(v___x_115_, 1, v___y_114_);
v___x_116_ = 0;
v___x_117_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_117_, 0, v___x_115_);
lean_ctor_set_uint8(v___x_117_, sizeof(void*)*1, v___x_116_);
v___x_118_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_118_, 0, v___x_75_);
lean_ctor_set(v___x_118_, 1, v___x_117_);
v___x_119_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__17));
v___x_120_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_120_, 0, v___x_118_);
lean_ctor_set(v___x_120_, 1, v___x_119_);
v___x_121_ = lean_box(1);
v___x_122_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_122_, 0, v___x_120_);
lean_ctor_set(v___x_122_, 1, v___x_121_);
v___x_123_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__19));
v___x_124_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_124_, 0, v___x_122_);
lean_ctor_set(v___x_124_, 1, v___x_123_);
v___x_125_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_125_, 0, v___x_124_);
lean_ctor_set(v___x_125_, 1, v___x_74_);
v___x_126_ = lean_unsigned_to_nat(0u);
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_128_ = lean_int_dec_lt(v_v1_72_, v___x_127_);
if (v___x_128_ == 0)
{
lean_object* v___x_129_; lean_object* v___x_130_; 
v___x_129_ = l_Int_repr(v_v1_72_);
v___x_130_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_130_, 0, v___x_129_);
v___y_92_ = v___x_119_;
v___y_93_ = v___x_125_;
v___y_94_ = v___x_121_;
v___y_95_ = v___x_116_;
v___y_96_ = v___x_130_;
goto v___jp_91_;
}
else
{
lean_object* v___x_131_; lean_object* v___x_132_; lean_object* v___x_133_; 
v___x_131_ = l_Int_repr(v_v1_72_);
v___x_132_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_132_, 0, v___x_131_);
v___x_133_ = l_Repr_addAppParen(v___x_132_, v___x_126_);
v___y_92_ = v___x_119_;
v___y_93_ = v___x_125_;
v___y_94_ = v___x_121_;
v___y_95_ = v___x_116_;
v___y_96_ = v___x_133_;
goto v___jp_91_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___boxed(lean_object* v_x_142_){
_start:
{
lean_object* v_res_143_; 
v_res_143_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg(v_x_142_);
lean_dec_ref(v_x_142_);
return v_res_143_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr(lean_object* v_x_144_, lean_object* v_prec_145_){
_start:
{
lean_object* v___x_146_; 
v___x_146_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg(v_x_144_);
return v___x_146_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___boxed(lean_object* v_x_147_, lean_object* v_prec_148_){
_start:
{
lean_object* v_res_149_; 
v_res_149_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr(v_x_147_, v_prec_148_);
lean_dec(v_prec_148_);
lean_dec_ref(v_x_147_);
return v_res_149_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0(void){
_start:
{
lean_object* v___x_152_; lean_object* v___x_153_; 
v___x_152_ = lean_unsigned_to_nat(1u);
v___x_153_ = lean_nat_to_int(v___x_152_);
return v___x_153_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__1(void){
_start:
{
lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; 
v___x_154_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0);
v___x_155_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_156_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_156_, 0, v___x_155_);
lean_ctor_set(v___x_156_, 1, v___x_154_);
lean_ctor_set(v___x_156_, 2, v___x_154_);
return v___x_156_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0(void){
_start:
{
lean_object* v___x_157_; 
v___x_157_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__1);
return v___x_157_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1___closed__0(void){
_start:
{
lean_object* v___x_158_; lean_object* v___x_159_; lean_object* v___x_160_; 
v___x_158_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_159_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0);
v___x_160_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_160_, 0, v___x_159_);
lean_ctor_set(v___x_160_, 1, v___x_158_);
lean_ctor_set(v___x_160_, 2, v___x_159_);
return v___x_160_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1(void){
_start:
{
lean_object* v___x_161_; 
v___x_161_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1___closed__0);
return v___x_161_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2___closed__0(void){
_start:
{
lean_object* v___x_162_; lean_object* v___x_163_; lean_object* v___x_164_; 
v___x_162_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0___closed__0);
v___x_164_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_164_, 0, v___x_163_);
lean_ctor_set(v___x_164_, 1, v___x_163_);
lean_ctor_set(v___x_164_, 2, v___x_162_);
return v___x_164_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2(void){
_start:
{
lean_object* v___x_165_; 
v___x_165_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2___closed__0);
return v___x_165_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereMinor(void){
_start:
{
lean_object* v___x_166_; lean_object* v_v1_167_; lean_object* v_v2_168_; lean_object* v___x_169_; lean_object* v_v1_170_; lean_object* v_v2_171_; lean_object* v___x_172_; lean_object* v___x_173_; lean_object* v___x_174_; 
v___x_166_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0;
v_v1_167_ = lean_ctor_get(v___x_166_, 1);
v_v2_168_ = lean_ctor_get(v___x_166_, 2);
v___x_169_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1;
v_v1_170_ = lean_ctor_get(v___x_169_, 1);
v_v2_171_ = lean_ctor_get(v___x_169_, 2);
v___x_172_ = lean_int_mul(v_v1_167_, v_v2_171_);
v___x_173_ = lean_int_mul(v_v2_168_, v_v1_170_);
v___x_174_ = lean_int_sub(v___x_172_, v___x_173_);
lean_dec(v___x_173_);
lean_dec(v___x_172_);
return v___x_174_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__0(void){
_start:
{
lean_object* v___x_175_; lean_object* v___x_176_; 
v___x_175_ = lean_unsigned_to_nat(2u);
v___x_176_ = lean_nat_to_int(v___x_175_);
return v___x_176_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__1(void){
_start:
{
lean_object* v___x_177_; lean_object* v___x_178_; lean_object* v___x_179_; 
v___x_177_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__0);
v___x_178_ = lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereMinor;
v___x_179_ = lean_int_emod(v___x_178_, v___x_177_);
return v___x_179_;
}
}
static uint8_t _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__2(void){
_start:
{
lean_object* v___x_180_; lean_object* v___x_181_; uint8_t v___x_182_; 
v___x_180_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_instReprVec3F2_repr___redArg___closed__15);
v___x_181_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__1);
v___x_182_ = lean_int_dec_eq(v___x_181_, v___x_180_);
return v___x_182_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank(void){
_start:
{
lean_object* v___x_183_; uint8_t v___x_184_; 
v___x_183_ = lean_unsigned_to_nat(0u);
v___x_184_ = lean_uint8_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank___closed__2);
if (v___x_184_ == 0)
{
lean_object* v___x_185_; 
v___x_185_ = lean_unsigned_to_nat(4u);
return v___x_185_;
}
else
{
return v___x_183_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H031OctahedralDepolarizingThreshold(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H031_r0);
lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H031_r1);
lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H031_r2);
lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereMinor = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereMinor();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereMinor);
lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H031_hemisphereSchmidtRank);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
