// Lean compiler output
// Module: T2MarkedFreeLift
// Imports: public import Init public meta import Init public import Std
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
lean_object* l_Bool_repr___redArg(uint8_t);
lean_object* lean_string_length(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_markedLift(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_markedLift___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "uniqueLiftOnInt"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__9_value;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "residualForcesFreeZ"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__11_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__12;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "piFromExactQ"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "u1FromL1Mass"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__17_value;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "znSoldAsU1"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__18_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__18_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__19_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__20_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__20;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "authorityEffectNone"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__21 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__21_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__21_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__22 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__22_value;
static const lean_string_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__23 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__23_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__24_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__24;
static lean_once_cell_t lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__25_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__25;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__26 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__26_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__23_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__27 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__27_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OvernightT2_instReprScopeBoundary___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary___closed__0 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary = (const lean_object*)&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT2_scopeBoundary___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 0, 0, 0, 0, 1, 0, 0)}};
static const lean_object* lp_FiniteQuantum_OvernightT2_scopeBoundary___closed__0 = (const lean_object*)&lp_FiniteQuantum_OvernightT2_scopeBoundary___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OvernightT2_scopeBoundary = (const lean_object*)&lp_FiniteQuantum_OvernightT2_scopeBoundary___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_markedLift(lean_object* v_g_1_, lean_object* v_n_2_){
_start:
{
lean_object* v___x_3_; 
v___x_3_ = lean_int_mul(v_n_2_, v_g_1_);
return v___x_3_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_markedLift___boxed(lean_object* v_g_4_, lean_object* v_n_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_FiniteQuantum_OvernightT2_markedLift(v_g_4_, v_n_5_);
lean_dec(v_n_5_);
lean_dec(v_g_4_);
return v_res_6_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary_decEq(lean_object* v_x_7_, lean_object* v_x_8_){
_start:
{
uint8_t v_uniqueLiftOnInt_9_; uint8_t v_residualForcesFreeZ_10_; uint8_t v_piFromExactQ_11_; uint8_t v_u1FromL1Mass_12_; uint8_t v_znSoldAsU1_13_; uint8_t v_authorityEffectNone_14_; uint8_t v_uniqueLiftOnInt_15_; uint8_t v_residualForcesFreeZ_16_; uint8_t v_piFromExactQ_17_; uint8_t v_u1FromL1Mass_18_; uint8_t v_znSoldAsU1_19_; uint8_t v_authorityEffectNone_20_; 
v_uniqueLiftOnInt_9_ = lean_ctor_get_uint8(v_x_7_, 0);
v_residualForcesFreeZ_10_ = lean_ctor_get_uint8(v_x_7_, 1);
v_piFromExactQ_11_ = lean_ctor_get_uint8(v_x_7_, 2);
v_u1FromL1Mass_12_ = lean_ctor_get_uint8(v_x_7_, 3);
v_znSoldAsU1_13_ = lean_ctor_get_uint8(v_x_7_, 4);
v_authorityEffectNone_14_ = lean_ctor_get_uint8(v_x_7_, 5);
v_uniqueLiftOnInt_15_ = lean_ctor_get_uint8(v_x_8_, 0);
v_residualForcesFreeZ_16_ = lean_ctor_get_uint8(v_x_8_, 1);
v_piFromExactQ_17_ = lean_ctor_get_uint8(v_x_8_, 2);
v_u1FromL1Mass_18_ = lean_ctor_get_uint8(v_x_8_, 3);
v_znSoldAsU1_19_ = lean_ctor_get_uint8(v_x_8_, 4);
v_authorityEffectNone_20_ = lean_ctor_get_uint8(v_x_8_, 5);
if (v_uniqueLiftOnInt_9_ == 0)
{
if (v_uniqueLiftOnInt_15_ == 0)
{
goto v___jp_26_;
}
else
{
return v_uniqueLiftOnInt_9_;
}
}
else
{
if (v_uniqueLiftOnInt_15_ == 0)
{
return v_uniqueLiftOnInt_15_;
}
else
{
goto v___jp_26_;
}
}
v___jp_21_:
{
if (v_authorityEffectNone_14_ == 0)
{
if (v_authorityEffectNone_20_ == 0)
{
uint8_t v___x_22_; 
v___x_22_ = 1;
return v___x_22_;
}
else
{
return v_authorityEffectNone_14_;
}
}
else
{
return v_authorityEffectNone_20_;
}
}
v___jp_23_:
{
if (v_znSoldAsU1_13_ == 0)
{
if (v_znSoldAsU1_19_ == 0)
{
goto v___jp_21_;
}
else
{
return v_znSoldAsU1_13_;
}
}
else
{
if (v_znSoldAsU1_19_ == 0)
{
return v_znSoldAsU1_19_;
}
else
{
goto v___jp_21_;
}
}
}
v___jp_24_:
{
if (v_u1FromL1Mass_12_ == 0)
{
if (v_u1FromL1Mass_18_ == 0)
{
goto v___jp_23_;
}
else
{
return v_u1FromL1Mass_12_;
}
}
else
{
if (v_u1FromL1Mass_18_ == 0)
{
return v_u1FromL1Mass_18_;
}
else
{
goto v___jp_23_;
}
}
}
v___jp_25_:
{
if (v_piFromExactQ_11_ == 0)
{
if (v_piFromExactQ_17_ == 0)
{
goto v___jp_24_;
}
else
{
return v_piFromExactQ_11_;
}
}
else
{
if (v_piFromExactQ_17_ == 0)
{
return v_piFromExactQ_17_;
}
else
{
goto v___jp_24_;
}
}
}
v___jp_26_:
{
if (v_residualForcesFreeZ_10_ == 0)
{
if (v_residualForcesFreeZ_16_ == 0)
{
goto v___jp_25_;
}
else
{
return v_residualForcesFreeZ_10_;
}
}
else
{
if (v_residualForcesFreeZ_16_ == 0)
{
return v_residualForcesFreeZ_16_;
}
else
{
goto v___jp_25_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary_decEq___boxed(lean_object* v_x_27_, lean_object* v_x_28_){
_start:
{
uint8_t v_res_29_; lean_object* v_r_30_; 
v_res_29_ = lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary_decEq(v_x_27_, v_x_28_);
lean_dec_ref(v_x_28_);
lean_dec_ref(v_x_27_);
v_r_30_ = lean_box(v_res_29_);
return v_r_30_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary(lean_object* v_x_31_, lean_object* v_x_32_){
_start:
{
uint8_t v___x_33_; 
v___x_33_ = lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary_decEq(v_x_31_, v_x_32_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary___boxed(lean_object* v_x_34_, lean_object* v_x_35_){
_start:
{
uint8_t v_res_36_; lean_object* v_r_37_; 
v_res_36_ = lp_FiniteQuantum_OvernightT2_instDecidableEqScopeBoundary(v_x_34_, v_x_35_);
lean_dec_ref(v_x_35_);
lean_dec_ref(v_x_34_);
v_r_37_ = lean_box(v_res_36_);
return v_r_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_51_; lean_object* v___x_52_; 
v___x_51_ = lean_unsigned_to_nat(19u);
v___x_52_ = lean_nat_to_int(v___x_51_);
return v___x_52_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__12(void){
_start:
{
lean_object* v___x_59_; lean_object* v___x_60_; 
v___x_59_ = lean_unsigned_to_nat(23u);
v___x_60_ = lean_nat_to_int(v___x_59_);
return v___x_60_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_64_; lean_object* v___x_65_; 
v___x_64_ = lean_unsigned_to_nat(16u);
v___x_65_ = lean_nat_to_int(v___x_64_);
return v___x_65_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__20(void){
_start:
{
lean_object* v___x_72_; lean_object* v___x_73_; 
v___x_72_ = lean_unsigned_to_nat(14u);
v___x_73_ = lean_nat_to_int(v___x_72_);
return v___x_73_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__24(void){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_78_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__0));
v___x_79_ = lean_string_length(v___x_78_);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__25(void){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; 
v___x_80_ = lean_obj_once(&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__24, &lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__24_once, _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__24);
v___x_81_ = lean_nat_to_int(v___x_80_);
return v___x_81_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg(lean_object* v_x_86_){
_start:
{
uint8_t v_uniqueLiftOnInt_87_; uint8_t v_residualForcesFreeZ_88_; uint8_t v_piFromExactQ_89_; uint8_t v_u1FromL1Mass_90_; uint8_t v_znSoldAsU1_91_; uint8_t v_authorityEffectNone_92_; lean_object* v___x_93_; lean_object* v___x_94_; lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; uint8_t v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; lean_object* v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; lean_object* v___x_106_; lean_object* v___x_107_; lean_object* v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; lean_object* v___x_113_; lean_object* v___x_114_; lean_object* v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; lean_object* v___x_127_; lean_object* v___x_128_; lean_object* v___x_129_; lean_object* v___x_130_; lean_object* v___x_131_; lean_object* v___x_132_; lean_object* v___x_133_; lean_object* v___x_134_; lean_object* v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; lean_object* v___x_138_; lean_object* v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; lean_object* v___x_145_; lean_object* v___x_146_; lean_object* v___x_147_; lean_object* v___x_148_; lean_object* v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; lean_object* v___x_152_; lean_object* v___x_153_; lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; lean_object* v___x_157_; 
v_uniqueLiftOnInt_87_ = lean_ctor_get_uint8(v_x_86_, 0);
v_residualForcesFreeZ_88_ = lean_ctor_get_uint8(v_x_86_, 1);
v_piFromExactQ_89_ = lean_ctor_get_uint8(v_x_86_, 2);
v_u1FromL1Mass_90_ = lean_ctor_get_uint8(v_x_86_, 3);
v_znSoldAsU1_91_ = lean_ctor_get_uint8(v_x_86_, 4);
v_authorityEffectNone_92_ = lean_ctor_get_uint8(v_x_86_, 5);
v___x_93_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__5));
v___x_94_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__6));
v___x_95_ = lean_obj_once(&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__7, &lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__7);
v___x_96_ = l_Bool_repr___redArg(v_uniqueLiftOnInt_87_);
v___x_97_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_97_, 0, v___x_95_);
lean_ctor_set(v___x_97_, 1, v___x_96_);
v___x_98_ = 0;
v___x_99_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_99_, 0, v___x_97_);
lean_ctor_set_uint8(v___x_99_, sizeof(void*)*1, v___x_98_);
v___x_100_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_100_, 0, v___x_94_);
lean_ctor_set(v___x_100_, 1, v___x_99_);
v___x_101_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__9));
v___x_102_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_102_, 0, v___x_100_);
lean_ctor_set(v___x_102_, 1, v___x_101_);
v___x_103_ = lean_box(1);
v___x_104_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_104_, 0, v___x_102_);
lean_ctor_set(v___x_104_, 1, v___x_103_);
v___x_105_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__11));
v___x_106_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_106_, 0, v___x_104_);
lean_ctor_set(v___x_106_, 1, v___x_105_);
v___x_107_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_107_, 0, v___x_106_);
lean_ctor_set(v___x_107_, 1, v___x_93_);
v___x_108_ = lean_obj_once(&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__12, &lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__12_once, _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__12);
v___x_109_ = l_Bool_repr___redArg(v_residualForcesFreeZ_88_);
v___x_110_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_110_, 0, v___x_108_);
lean_ctor_set(v___x_110_, 1, v___x_109_);
v___x_111_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_111_, 0, v___x_110_);
lean_ctor_set_uint8(v___x_111_, sizeof(void*)*1, v___x_98_);
v___x_112_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_112_, 0, v___x_107_);
lean_ctor_set(v___x_112_, 1, v___x_111_);
v___x_113_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_113_, 0, v___x_112_);
lean_ctor_set(v___x_113_, 1, v___x_101_);
v___x_114_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_114_, 0, v___x_113_);
lean_ctor_set(v___x_114_, 1, v___x_103_);
v___x_115_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__14));
v___x_116_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_116_, 0, v___x_114_);
lean_ctor_set(v___x_116_, 1, v___x_115_);
v___x_117_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_117_, 0, v___x_116_);
lean_ctor_set(v___x_117_, 1, v___x_93_);
v___x_118_ = lean_obj_once(&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__15, &lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__15);
v___x_119_ = l_Bool_repr___redArg(v_piFromExactQ_89_);
v___x_120_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_120_, 0, v___x_118_);
lean_ctor_set(v___x_120_, 1, v___x_119_);
v___x_121_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_121_, 0, v___x_120_);
lean_ctor_set_uint8(v___x_121_, sizeof(void*)*1, v___x_98_);
v___x_122_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_122_, 0, v___x_117_);
lean_ctor_set(v___x_122_, 1, v___x_121_);
v___x_123_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_123_, 0, v___x_122_);
lean_ctor_set(v___x_123_, 1, v___x_101_);
v___x_124_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_124_, 0, v___x_123_);
lean_ctor_set(v___x_124_, 1, v___x_103_);
v___x_125_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__17));
v___x_126_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_126_, 0, v___x_124_);
lean_ctor_set(v___x_126_, 1, v___x_125_);
v___x_127_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_127_, 0, v___x_126_);
lean_ctor_set(v___x_127_, 1, v___x_93_);
v___x_128_ = l_Bool_repr___redArg(v_u1FromL1Mass_90_);
v___x_129_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_129_, 0, v___x_118_);
lean_ctor_set(v___x_129_, 1, v___x_128_);
v___x_130_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_130_, 0, v___x_129_);
lean_ctor_set_uint8(v___x_130_, sizeof(void*)*1, v___x_98_);
v___x_131_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_131_, 0, v___x_127_);
lean_ctor_set(v___x_131_, 1, v___x_130_);
v___x_132_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_132_, 0, v___x_131_);
lean_ctor_set(v___x_132_, 1, v___x_101_);
v___x_133_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_133_, 0, v___x_132_);
lean_ctor_set(v___x_133_, 1, v___x_103_);
v___x_134_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__19));
v___x_135_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_135_, 0, v___x_133_);
lean_ctor_set(v___x_135_, 1, v___x_134_);
v___x_136_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_136_, 0, v___x_135_);
lean_ctor_set(v___x_136_, 1, v___x_93_);
v___x_137_ = lean_obj_once(&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__20, &lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__20_once, _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__20);
v___x_138_ = l_Bool_repr___redArg(v_znSoldAsU1_91_);
v___x_139_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_139_, 0, v___x_137_);
lean_ctor_set(v___x_139_, 1, v___x_138_);
v___x_140_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_140_, 0, v___x_139_);
lean_ctor_set_uint8(v___x_140_, sizeof(void*)*1, v___x_98_);
v___x_141_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_141_, 0, v___x_136_);
lean_ctor_set(v___x_141_, 1, v___x_140_);
v___x_142_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_142_, 0, v___x_141_);
lean_ctor_set(v___x_142_, 1, v___x_101_);
v___x_143_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_143_, 0, v___x_142_);
lean_ctor_set(v___x_143_, 1, v___x_103_);
v___x_144_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__22));
v___x_145_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_145_, 0, v___x_143_);
lean_ctor_set(v___x_145_, 1, v___x_144_);
v___x_146_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_146_, 0, v___x_145_);
lean_ctor_set(v___x_146_, 1, v___x_93_);
v___x_147_ = l_Bool_repr___redArg(v_authorityEffectNone_92_);
v___x_148_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_148_, 0, v___x_108_);
lean_ctor_set(v___x_148_, 1, v___x_147_);
v___x_149_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_149_, 0, v___x_148_);
lean_ctor_set_uint8(v___x_149_, sizeof(void*)*1, v___x_98_);
v___x_150_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_150_, 0, v___x_146_);
lean_ctor_set(v___x_150_, 1, v___x_149_);
v___x_151_ = lean_obj_once(&lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__25, &lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__25_once, _init_lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__25);
v___x_152_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__26));
v___x_153_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_153_, 0, v___x_152_);
lean_ctor_set(v___x_153_, 1, v___x_150_);
v___x_154_ = ((lean_object*)(lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___closed__27));
v___x_155_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_155_, 0, v___x_153_);
lean_ctor_set(v___x_155_, 1, v___x_154_);
v___x_156_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_156_, 0, v___x_151_);
lean_ctor_set(v___x_156_, 1, v___x_155_);
v___x_157_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_157_, 0, v___x_156_);
lean_ctor_set_uint8(v___x_157_, sizeof(void*)*1, v___x_98_);
return v___x_157_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg___boxed(lean_object* v_x_158_){
_start:
{
lean_object* v_res_159_; 
v_res_159_ = lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg(v_x_158_);
lean_dec_ref(v_x_158_);
return v_res_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr(lean_object* v_x_160_, lean_object* v_prec_161_){
_start:
{
lean_object* v___x_162_; 
v___x_162_ = lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___redArg(v_x_160_);
return v___x_162_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr___boxed(lean_object* v_x_163_, lean_object* v_prec_164_){
_start:
{
lean_object* v_res_165_; 
v_res_165_ = lp_FiniteQuantum_OvernightT2_instReprScopeBoundary_repr(v_x_163_, v_prec_164_);
lean_dec(v_prec_164_);
lean_dec_ref(v_x_163_);
return v_res_165_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Std(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_T2MarkedFreeLift(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Std(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
