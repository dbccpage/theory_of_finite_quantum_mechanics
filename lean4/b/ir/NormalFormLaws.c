// Lean compiler output
// Module: NormalFormLaws
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
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
lean_object* l_Bool_repr___redArg(uint8_t);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "x"};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "y"};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__16_value;
static lean_once_cell_t lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain___closed__0 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_integralGauge(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_integralGauge___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_integralNormal(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "s01"};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "s12"};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__6_value;
static const lean_string_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "s20"};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__7 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__7_value;
static const lean_ctor_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__7_value)}};
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__8_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns___closed__0 = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns = (const lean_object*)&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_triangleCycle(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleCycle___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleNormal(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleNormal___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleGauge(uint8_t, uint8_t, uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleGauge___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_x_3_; lean_object* v_y_4_; lean_object* v_x_5_; lean_object* v_y_6_; uint8_t v___x_7_; 
v_x_3_ = lean_ctor_get(v_x_1_, 0);
v_y_4_ = lean_ctor_get(v_x_1_, 1);
v_x_5_ = lean_ctor_get(v_x_2_, 0);
v_y_6_ = lean_ctor_get(v_x_2_, 1);
v___x_7_ = lean_int_dec_eq(v_x_3_, v_x_5_);
if (v___x_7_ == 0)
{
return v___x_7_;
}
else
{
uint8_t v___x_8_; 
v___x_8_ = lean_int_dec_eq(v_y_4_, v_y_6_);
return v___x_8_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain_decEq___boxed(lean_object* v_x_9_, lean_object* v_x_10_){
_start:
{
uint8_t v_res_11_; lean_object* v_r_12_; 
v_res_11_ = lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain_decEq(v_x_9_, v_x_10_);
lean_dec_ref(v_x_10_);
lean_dec_ref(v_x_9_);
v_r_12_ = lean_box(v_res_11_);
return v_r_12_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain(lean_object* v_x_13_, lean_object* v_x_14_){
_start:
{
uint8_t v___x_15_; 
v___x_15_ = lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain_decEq(v_x_13_, v_x_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain___boxed(lean_object* v_x_16_, lean_object* v_x_17_){
_start:
{
uint8_t v_res_18_; lean_object* v_r_19_; 
v_res_18_ = lp_FiniteQuantum_NormalFormLaws_instDecidableEqIntegralCochain(v_x_16_, v_x_17_);
lean_dec_ref(v_x_17_);
lean_dec_ref(v_x_16_);
v_r_19_ = lean_box(v_res_18_);
return v_r_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_unsigned_to_nat(5u);
v___x_34_ = lean_nat_to_int(v___x_33_);
return v___x_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_36_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__0));
v___x_37_ = lean_string_length(v___x_36_);
return v___x_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__9, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__9);
v___x_39_ = lean_nat_to_int(v___x_38_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_50_ = lean_unsigned_to_nat(0u);
v___x_51_ = lean_nat_to_int(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg(lean_object* v_x_52_){
_start:
{
lean_object* v_x_53_; lean_object* v_y_54_; lean_object* v___x_56_; uint8_t v_isShared_57_; uint8_t v_isSharedCheck_106_; 
v_x_53_ = lean_ctor_get(v_x_52_, 0);
v_y_54_ = lean_ctor_get(v_x_52_, 1);
v_isSharedCheck_106_ = !lean_is_exclusive(v_x_52_);
if (v_isSharedCheck_106_ == 0)
{
v___x_56_ = v_x_52_;
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
else
{
lean_inc(v_y_54_);
lean_inc(v_x_53_);
lean_dec(v_x_52_);
v___x_56_ = lean_box(0);
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
v_resetjp_55_:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___y_62_; uint8_t v___y_63_; lean_object* v___y_64_; lean_object* v___y_78_; lean_object* v___x_98_; lean_object* v___x_99_; uint8_t v___x_100_; 
v___x_58_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5));
v___x_59_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__6));
v___x_60_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__7, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__7);
v___x_98_ = lean_unsigned_to_nat(0u);
v___x_99_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17);
v___x_100_ = lean_int_dec_lt(v_x_53_, v___x_99_);
if (v___x_100_ == 0)
{
lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_101_ = l_Int_repr(v_x_53_);
lean_dec(v_x_53_);
v___x_102_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_102_, 0, v___x_101_);
v___y_78_ = v___x_102_;
goto v___jp_77_;
}
else
{
lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; 
v___x_103_ = l_Int_repr(v_x_53_);
lean_dec(v_x_53_);
v___x_104_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_104_, 0, v___x_103_);
v___x_105_ = l_Repr_addAppParen(v___x_104_, v___x_98_);
v___y_78_ = v___x_105_;
goto v___jp_77_;
}
v___jp_61_:
{
lean_object* v___x_66_; 
if (v_isShared_57_ == 0)
{
lean_ctor_set_tag(v___x_56_, 4);
lean_ctor_set(v___x_56_, 1, v___y_64_);
lean_ctor_set(v___x_56_, 0, v___x_60_);
v___x_66_ = v___x_56_;
goto v_reusejp_65_;
}
else
{
lean_object* v_reuseFailAlloc_76_; 
v_reuseFailAlloc_76_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_76_, 0, v___x_60_);
lean_ctor_set(v_reuseFailAlloc_76_, 1, v___y_64_);
v___x_66_ = v_reuseFailAlloc_76_;
goto v_reusejp_65_;
}
v_reusejp_65_:
{
lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; lean_object* v___x_74_; lean_object* v___x_75_; 
v___x_67_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_67_, 0, v___x_66_);
lean_ctor_set_uint8(v___x_67_, sizeof(void*)*1, v___y_63_);
v___x_68_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_68_, 0, v___y_62_);
lean_ctor_set(v___x_68_, 1, v___x_67_);
v___x_69_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10);
v___x_70_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__11));
v___x_71_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_71_, 0, v___x_70_);
lean_ctor_set(v___x_71_, 1, v___x_68_);
v___x_72_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__12));
v___x_73_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_73_, 0, v___x_71_);
lean_ctor_set(v___x_73_, 1, v___x_72_);
v___x_74_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_74_, 0, v___x_69_);
lean_ctor_set(v___x_74_, 1, v___x_73_);
v___x_75_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_75_, 0, v___x_74_);
lean_ctor_set_uint8(v___x_75_, sizeof(void*)*1, v___y_63_);
return v___x_75_;
}
}
v___jp_77_:
{
lean_object* v___x_79_; uint8_t v___x_80_; lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; lean_object* v___x_86_; lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; lean_object* v___x_91_; uint8_t v___x_92_; 
v___x_79_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_79_, 0, v___x_60_);
lean_ctor_set(v___x_79_, 1, v___y_78_);
v___x_80_ = 0;
v___x_81_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_81_, 0, v___x_79_);
lean_ctor_set_uint8(v___x_81_, sizeof(void*)*1, v___x_80_);
v___x_82_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_82_, 0, v___x_59_);
lean_ctor_set(v___x_82_, 1, v___x_81_);
v___x_83_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__14));
v___x_84_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_84_, 0, v___x_82_);
lean_ctor_set(v___x_84_, 1, v___x_83_);
v___x_85_ = lean_box(1);
v___x_86_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_84_);
lean_ctor_set(v___x_86_, 1, v___x_85_);
v___x_87_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__16));
v___x_88_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_88_, 0, v___x_86_);
lean_ctor_set(v___x_88_, 1, v___x_87_);
v___x_89_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_88_);
lean_ctor_set(v___x_89_, 1, v___x_58_);
v___x_90_ = lean_unsigned_to_nat(0u);
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17);
v___x_92_ = lean_int_dec_lt(v_y_54_, v___x_91_);
if (v___x_92_ == 0)
{
lean_object* v___x_93_; lean_object* v___x_94_; 
v___x_93_ = l_Int_repr(v_y_54_);
lean_dec(v_y_54_);
v___x_94_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_94_, 0, v___x_93_);
v___y_62_ = v___x_89_;
v___y_63_ = v___x_80_;
v___y_64_ = v___x_94_;
goto v___jp_61_;
}
else
{
lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; 
v___x_95_ = l_Int_repr(v_y_54_);
lean_dec(v_y_54_);
v___x_96_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_96_, 0, v___x_95_);
v___x_97_ = l_Repr_addAppParen(v___x_96_, v___x_90_);
v___y_62_ = v___x_89_;
v___y_63_ = v___x_80_;
v___y_64_ = v___x_97_;
goto v___jp_61_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr(lean_object* v_x_107_, lean_object* v_prec_108_){
_start:
{
lean_object* v___x_109_; 
v___x_109_ = lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg(v_x_107_);
return v___x_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___boxed(lean_object* v_x_110_, lean_object* v_prec_111_){
_start:
{
lean_object* v_res_112_; 
v_res_112_ = lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr(v_x_110_, v_prec_111_);
lean_dec(v_prec_111_);
return v_res_112_;
}
}
static lean_object* _init_lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0(void){
_start:
{
lean_object* v___x_115_; lean_object* v___x_116_; 
v___x_115_ = lean_unsigned_to_nat(2u);
v___x_116_ = lean_nat_to_int(v___x_115_);
return v___x_116_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_integralGauge(lean_object* v_a_117_, lean_object* v_c_118_){
_start:
{
lean_object* v_x_119_; lean_object* v_y_120_; lean_object* v___x_122_; uint8_t v_isShared_123_; uint8_t v_isSharedCheck_131_; 
v_x_119_ = lean_ctor_get(v_c_118_, 0);
v_y_120_ = lean_ctor_get(v_c_118_, 1);
v_isSharedCheck_131_ = !lean_is_exclusive(v_c_118_);
if (v_isSharedCheck_131_ == 0)
{
v___x_122_ = v_c_118_;
v_isShared_123_ = v_isSharedCheck_131_;
goto v_resetjp_121_;
}
else
{
lean_inc(v_y_120_);
lean_inc(v_x_119_);
lean_dec(v_c_118_);
v___x_122_ = lean_box(0);
v_isShared_123_ = v_isSharedCheck_131_;
goto v_resetjp_121_;
}
v_resetjp_121_:
{
lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; lean_object* v___x_127_; lean_object* v___x_129_; 
v___x_124_ = lean_int_add(v_x_119_, v_a_117_);
lean_dec(v_x_119_);
v___x_125_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0, &lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0_once, _init_lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0);
v___x_126_ = lean_int_mul(v___x_125_, v_a_117_);
v___x_127_ = lean_int_add(v_y_120_, v___x_126_);
lean_dec(v___x_126_);
lean_dec(v_y_120_);
if (v_isShared_123_ == 0)
{
lean_ctor_set(v___x_122_, 1, v___x_127_);
lean_ctor_set(v___x_122_, 0, v___x_124_);
v___x_129_ = v___x_122_;
goto v_reusejp_128_;
}
else
{
lean_object* v_reuseFailAlloc_130_; 
v_reuseFailAlloc_130_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_130_, 0, v___x_124_);
lean_ctor_set(v_reuseFailAlloc_130_, 1, v___x_127_);
v___x_129_ = v_reuseFailAlloc_130_;
goto v_reusejp_128_;
}
v_reusejp_128_:
{
return v___x_129_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_integralGauge___boxed(lean_object* v_a_132_, lean_object* v_c_133_){
_start:
{
lean_object* v_res_134_; 
v_res_134_ = lp_FiniteQuantum_NormalFormLaws_integralGauge(v_a_132_, v_c_133_);
lean_dec(v_a_132_);
return v_res_134_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_integralNormal(lean_object* v_c_135_){
_start:
{
lean_object* v_x_136_; lean_object* v_y_137_; lean_object* v___x_139_; uint8_t v_isShared_140_; uint8_t v_isSharedCheck_148_; 
v_x_136_ = lean_ctor_get(v_c_135_, 0);
v_y_137_ = lean_ctor_get(v_c_135_, 1);
v_isSharedCheck_148_ = !lean_is_exclusive(v_c_135_);
if (v_isSharedCheck_148_ == 0)
{
v___x_139_ = v_c_135_;
v_isShared_140_ = v_isSharedCheck_148_;
goto v_resetjp_138_;
}
else
{
lean_inc(v_y_137_);
lean_inc(v_x_136_);
lean_dec(v_c_135_);
v___x_139_ = lean_box(0);
v_isShared_140_ = v_isSharedCheck_148_;
goto v_resetjp_138_;
}
v_resetjp_138_:
{
lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; lean_object* v___x_146_; 
v___x_141_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__17);
v___x_142_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0, &lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0_once, _init_lp_FiniteQuantum_NormalFormLaws_integralGauge___closed__0);
v___x_143_ = lean_int_mul(v___x_142_, v_x_136_);
lean_dec(v_x_136_);
v___x_144_ = lean_int_sub(v_y_137_, v___x_143_);
lean_dec(v___x_143_);
lean_dec(v_y_137_);
if (v_isShared_140_ == 0)
{
lean_ctor_set(v___x_139_, 1, v___x_144_);
lean_ctor_set(v___x_139_, 0, v___x_141_);
v___x_146_ = v___x_139_;
goto v_reusejp_145_;
}
else
{
lean_object* v_reuseFailAlloc_147_; 
v_reuseFailAlloc_147_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_147_, 0, v___x_141_);
lean_ctor_set(v_reuseFailAlloc_147_, 1, v___x_144_);
v___x_146_ = v_reuseFailAlloc_147_;
goto v_reusejp_145_;
}
v_reusejp_145_:
{
return v___x_146_;
}
}
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns_decEq(lean_object* v_x_149_, lean_object* v_x_150_){
_start:
{
uint8_t v_s01_151_; uint8_t v_s12_152_; uint8_t v_s20_153_; uint8_t v_s01_154_; uint8_t v_s12_155_; uint8_t v_s20_156_; 
v_s01_151_ = lean_ctor_get_uint8(v_x_149_, 0);
v_s12_152_ = lean_ctor_get_uint8(v_x_149_, 1);
v_s20_153_ = lean_ctor_get_uint8(v_x_149_, 2);
v_s01_154_ = lean_ctor_get_uint8(v_x_150_, 0);
v_s12_155_ = lean_ctor_get_uint8(v_x_150_, 1);
v_s20_156_ = lean_ctor_get_uint8(v_x_150_, 2);
if (v_s01_151_ == 0)
{
if (v_s01_154_ == 0)
{
goto v___jp_159_;
}
else
{
return v_s01_151_;
}
}
else
{
if (v_s01_154_ == 0)
{
return v_s01_154_;
}
else
{
goto v___jp_159_;
}
}
v___jp_157_:
{
if (v_s20_153_ == 0)
{
if (v_s20_156_ == 0)
{
uint8_t v___x_158_; 
v___x_158_ = 1;
return v___x_158_;
}
else
{
return v_s20_153_;
}
}
else
{
return v_s20_156_;
}
}
v___jp_159_:
{
if (v_s12_152_ == 0)
{
if (v_s12_155_ == 0)
{
goto v___jp_157_;
}
else
{
return v_s12_152_;
}
}
else
{
if (v_s12_155_ == 0)
{
return v_s12_155_;
}
else
{
goto v___jp_157_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns_decEq___boxed(lean_object* v_x_160_, lean_object* v_x_161_){
_start:
{
uint8_t v_res_162_; lean_object* v_r_163_; 
v_res_162_ = lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns_decEq(v_x_160_, v_x_161_);
lean_dec_ref(v_x_161_);
lean_dec_ref(v_x_160_);
v_r_163_ = lean_box(v_res_162_);
return v_r_163_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns(lean_object* v_x_164_, lean_object* v_x_165_){
_start:
{
uint8_t v___x_166_; 
v___x_166_ = lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns_decEq(v_x_164_, v_x_165_);
return v___x_166_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns___boxed(lean_object* v_x_167_, lean_object* v_x_168_){
_start:
{
uint8_t v_res_169_; lean_object* v_r_170_; 
v_res_169_ = lp_FiniteQuantum_NormalFormLaws_instDecidableEqTriangleSigns(v_x_167_, v_x_168_);
lean_dec_ref(v_x_168_);
lean_dec_ref(v_x_167_);
v_r_170_ = lean_box(v_res_169_);
return v_r_170_;
}
}
static lean_object* _init_lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_180_; lean_object* v___x_181_; 
v___x_180_ = lean_unsigned_to_nat(7u);
v___x_181_ = lean_nat_to_int(v___x_180_);
return v___x_181_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg(lean_object* v_x_188_){
_start:
{
uint8_t v_s01_189_; uint8_t v_s12_190_; uint8_t v_s20_191_; lean_object* v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; uint8_t v___x_197_; lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_200_; lean_object* v___x_201_; lean_object* v___x_202_; lean_object* v___x_203_; lean_object* v___x_204_; lean_object* v___x_205_; lean_object* v___x_206_; lean_object* v___x_207_; lean_object* v___x_208_; lean_object* v___x_209_; lean_object* v___x_210_; lean_object* v___x_211_; lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_214_; lean_object* v___x_215_; lean_object* v___x_216_; lean_object* v___x_217_; lean_object* v___x_218_; lean_object* v___x_219_; lean_object* v___x_220_; lean_object* v___x_221_; lean_object* v___x_222_; lean_object* v___x_223_; lean_object* v___x_224_; lean_object* v___x_225_; lean_object* v___x_226_; 
v_s01_189_ = lean_ctor_get_uint8(v_x_188_, 0);
v_s12_190_ = lean_ctor_get_uint8(v_x_188_, 1);
v_s20_191_ = lean_ctor_get_uint8(v_x_188_, 2);
v___x_192_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__5));
v___x_193_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__3));
v___x_194_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__4, &lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__4);
v___x_195_ = l_Bool_repr___redArg(v_s01_189_);
v___x_196_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_196_, 0, v___x_194_);
lean_ctor_set(v___x_196_, 1, v___x_195_);
v___x_197_ = 0;
v___x_198_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_198_, 0, v___x_196_);
lean_ctor_set_uint8(v___x_198_, sizeof(void*)*1, v___x_197_);
v___x_199_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_199_, 0, v___x_193_);
lean_ctor_set(v___x_199_, 1, v___x_198_);
v___x_200_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__14));
v___x_201_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_201_, 0, v___x_199_);
lean_ctor_set(v___x_201_, 1, v___x_200_);
v___x_202_ = lean_box(1);
v___x_203_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_203_, 0, v___x_201_);
lean_ctor_set(v___x_203_, 1, v___x_202_);
v___x_204_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__6));
v___x_205_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_205_, 0, v___x_203_);
lean_ctor_set(v___x_205_, 1, v___x_204_);
v___x_206_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_206_, 0, v___x_205_);
lean_ctor_set(v___x_206_, 1, v___x_192_);
v___x_207_ = l_Bool_repr___redArg(v_s12_190_);
v___x_208_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_208_, 0, v___x_194_);
lean_ctor_set(v___x_208_, 1, v___x_207_);
v___x_209_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_209_, 0, v___x_208_);
lean_ctor_set_uint8(v___x_209_, sizeof(void*)*1, v___x_197_);
v___x_210_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_210_, 0, v___x_206_);
lean_ctor_set(v___x_210_, 1, v___x_209_);
v___x_211_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_211_, 0, v___x_210_);
lean_ctor_set(v___x_211_, 1, v___x_200_);
v___x_212_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_212_, 0, v___x_211_);
lean_ctor_set(v___x_212_, 1, v___x_202_);
v___x_213_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___closed__8));
v___x_214_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_214_, 0, v___x_212_);
lean_ctor_set(v___x_214_, 1, v___x_213_);
v___x_215_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_215_, 0, v___x_214_);
lean_ctor_set(v___x_215_, 1, v___x_192_);
v___x_216_ = l_Bool_repr___redArg(v_s20_191_);
v___x_217_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_217_, 0, v___x_194_);
lean_ctor_set(v___x_217_, 1, v___x_216_);
v___x_218_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_218_, 0, v___x_217_);
lean_ctor_set_uint8(v___x_218_, sizeof(void*)*1, v___x_197_);
v___x_219_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_219_, 0, v___x_215_);
lean_ctor_set(v___x_219_, 1, v___x_218_);
v___x_220_ = lean_obj_once(&lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10, &lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__10);
v___x_221_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__11));
v___x_222_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_222_, 0, v___x_221_);
lean_ctor_set(v___x_222_, 1, v___x_219_);
v___x_223_ = ((lean_object*)(lp_FiniteQuantum_NormalFormLaws_instReprIntegralCochain_repr___redArg___closed__12));
v___x_224_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_224_, 0, v___x_222_);
lean_ctor_set(v___x_224_, 1, v___x_223_);
v___x_225_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_225_, 0, v___x_220_);
lean_ctor_set(v___x_225_, 1, v___x_224_);
v___x_226_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_226_, 0, v___x_225_);
lean_ctor_set_uint8(v___x_226_, sizeof(void*)*1, v___x_197_);
return v___x_226_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg___boxed(lean_object* v_x_227_){
_start:
{
lean_object* v_res_228_; 
v_res_228_ = lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg(v_x_227_);
lean_dec_ref(v_x_227_);
return v_res_228_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr(lean_object* v_x_229_, lean_object* v_prec_230_){
_start:
{
lean_object* v___x_231_; 
v___x_231_ = lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___redArg(v_x_229_);
return v___x_231_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr___boxed(lean_object* v_x_232_, lean_object* v_prec_233_){
_start:
{
lean_object* v_res_234_; 
v_res_234_ = lp_FiniteQuantum_NormalFormLaws_instReprTriangleSigns_repr(v_x_232_, v_prec_233_);
lean_dec(v_prec_233_);
lean_dec_ref(v_x_232_);
return v_res_234_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NormalFormLaws_triangleCycle(lean_object* v_s_237_){
_start:
{
uint8_t v_s01_238_; uint8_t v_s12_239_; uint8_t v_s20_240_; 
v_s01_238_ = lean_ctor_get_uint8(v_s_237_, 0);
v_s12_239_ = lean_ctor_get_uint8(v_s_237_, 1);
v_s20_240_ = lean_ctor_get_uint8(v_s_237_, 2);
if (v_s01_238_ == 0)
{
if (v_s12_239_ == 0)
{
return v_s20_240_;
}
else
{
goto v___jp_241_;
}
}
else
{
if (v_s12_239_ == 0)
{
goto v___jp_241_;
}
else
{
return v_s20_240_;
}
}
v___jp_241_:
{
if (v_s20_240_ == 0)
{
uint8_t v___x_242_; 
v___x_242_ = 1;
return v___x_242_;
}
else
{
uint8_t v___x_243_; 
v___x_243_ = 0;
return v___x_243_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleCycle___boxed(lean_object* v_s_244_){
_start:
{
uint8_t v_res_245_; lean_object* v_r_246_; 
v_res_245_ = lp_FiniteQuantum_NormalFormLaws_triangleCycle(v_s_244_);
lean_dec_ref(v_s_244_);
v_r_246_ = lean_box(v_res_245_);
return v_r_246_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleNormal(lean_object* v_s_247_){
_start:
{
uint8_t v___x_248_; uint8_t v___x_249_; lean_object* v___x_250_; 
v___x_248_ = 0;
v___x_249_ = lp_FiniteQuantum_NormalFormLaws_triangleCycle(v_s_247_);
v___x_250_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_250_, 0, v___x_248_);
lean_ctor_set_uint8(v___x_250_, 1, v___x_248_);
lean_ctor_set_uint8(v___x_250_, 2, v___x_249_);
return v___x_250_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleNormal___boxed(lean_object* v_s_251_){
_start:
{
lean_object* v_res_252_; 
v_res_252_ = lp_FiniteQuantum_NormalFormLaws_triangleNormal(v_s_251_);
lean_dec_ref(v_s_251_);
return v_res_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleGauge(uint8_t v_a0_253_, uint8_t v_a1_254_, uint8_t v_a2_255_, lean_object* v_s_256_){
_start:
{
uint8_t v___y_258_; uint8_t v___y_259_; uint8_t v___y_263_; uint8_t v___y_264_; uint8_t v___y_268_; uint8_t v___y_269_; uint8_t v___y_271_; uint8_t v___y_272_; uint8_t v_s01_273_; uint8_t v_s12_274_; uint8_t v_s20_275_; uint8_t v___y_277_; uint8_t v___y_278_; uint8_t v___y_280_; uint8_t v___y_283_; uint8_t v___y_286_; uint8_t v___y_288_; uint8_t v___y_290_; 
v_s01_273_ = lean_ctor_get_uint8(v_s_256_, 0);
v_s12_274_ = lean_ctor_get_uint8(v_s_256_, 1);
v_s20_275_ = lean_ctor_get_uint8(v_s_256_, 2);
if (v_s01_273_ == 0)
{
if (v_a0_253_ == 0)
{
goto v___jp_295_;
}
else
{
goto v___jp_296_;
}
}
else
{
if (v_a0_253_ == 0)
{
goto v___jp_296_;
}
else
{
goto v___jp_295_;
}
}
v___jp_257_:
{
uint8_t v___x_260_; lean_object* v___x_261_; 
v___x_260_ = 1;
v___x_261_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_261_, 0, v___y_259_);
lean_ctor_set_uint8(v___x_261_, 1, v___y_258_);
lean_ctor_set_uint8(v___x_261_, 2, v___x_260_);
return v___x_261_;
}
v___jp_262_:
{
uint8_t v___x_265_; lean_object* v___x_266_; 
v___x_265_ = 0;
v___x_266_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_266_, 0, v___y_264_);
lean_ctor_set_uint8(v___x_266_, 1, v___y_263_);
lean_ctor_set_uint8(v___x_266_, 2, v___x_265_);
return v___x_266_;
}
v___jp_267_:
{
if (v_a0_253_ == 0)
{
v___y_258_ = v___y_268_;
v___y_259_ = v___y_269_;
goto v___jp_257_;
}
else
{
v___y_263_ = v___y_268_;
v___y_264_ = v___y_269_;
goto v___jp_262_;
}
}
v___jp_270_:
{
if (v_a0_253_ == 0)
{
v___y_263_ = v___y_271_;
v___y_264_ = v___y_272_;
goto v___jp_262_;
}
else
{
v___y_258_ = v___y_271_;
v___y_259_ = v___y_272_;
goto v___jp_257_;
}
}
v___jp_276_:
{
if (v_s20_275_ == 0)
{
if (v_a2_255_ == 0)
{
v___y_271_ = v___y_278_;
v___y_272_ = v___y_277_;
goto v___jp_270_;
}
else
{
v___y_268_ = v___y_278_;
v___y_269_ = v___y_277_;
goto v___jp_267_;
}
}
else
{
if (v_a2_255_ == 0)
{
v___y_268_ = v___y_278_;
v___y_269_ = v___y_277_;
goto v___jp_267_;
}
else
{
v___y_271_ = v___y_278_;
v___y_272_ = v___y_277_;
goto v___jp_270_;
}
}
}
v___jp_279_:
{
uint8_t v___x_281_; 
v___x_281_ = 0;
v___y_277_ = v___y_280_;
v___y_278_ = v___x_281_;
goto v___jp_276_;
}
v___jp_282_:
{
uint8_t v___x_284_; 
v___x_284_ = 1;
v___y_277_ = v___y_283_;
v___y_278_ = v___x_284_;
goto v___jp_276_;
}
v___jp_285_:
{
if (v_a2_255_ == 0)
{
v___y_283_ = v___y_286_;
goto v___jp_282_;
}
else
{
v___y_280_ = v___y_286_;
goto v___jp_279_;
}
}
v___jp_287_:
{
if (v_a2_255_ == 0)
{
v___y_280_ = v___y_288_;
goto v___jp_279_;
}
else
{
v___y_283_ = v___y_288_;
goto v___jp_282_;
}
}
v___jp_289_:
{
if (v_s12_274_ == 0)
{
if (v_a1_254_ == 0)
{
v___y_288_ = v___y_290_;
goto v___jp_287_;
}
else
{
v___y_286_ = v___y_290_;
goto v___jp_285_;
}
}
else
{
if (v_a1_254_ == 0)
{
v___y_286_ = v___y_290_;
goto v___jp_285_;
}
else
{
v___y_288_ = v___y_290_;
goto v___jp_287_;
}
}
}
v___jp_291_:
{
uint8_t v___x_292_; 
v___x_292_ = 1;
v___y_290_ = v___x_292_;
goto v___jp_289_;
}
v___jp_293_:
{
uint8_t v___x_294_; 
v___x_294_ = 0;
v___y_290_ = v___x_294_;
goto v___jp_289_;
}
v___jp_295_:
{
if (v_a1_254_ == 0)
{
goto v___jp_293_;
}
else
{
goto v___jp_291_;
}
}
v___jp_296_:
{
if (v_a1_254_ == 0)
{
goto v___jp_291_;
}
else
{
goto v___jp_293_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NormalFormLaws_triangleGauge___boxed(lean_object* v_a0_297_, lean_object* v_a1_298_, lean_object* v_a2_299_, lean_object* v_s_300_){
_start:
{
uint8_t v_a0_boxed_301_; uint8_t v_a1_boxed_302_; uint8_t v_a2_boxed_303_; lean_object* v_res_304_; 
v_a0_boxed_301_ = lean_unbox(v_a0_297_);
v_a1_boxed_302_ = lean_unbox(v_a1_298_);
v_a2_boxed_303_ = lean_unbox(v_a2_299_);
v_res_304_ = lp_FiniteQuantum_NormalFormLaws_triangleGauge(v_a0_boxed_301_, v_a1_boxed_302_, v_a2_boxed_303_, v_s_300_);
lean_dec_ref(v_s_300_);
return v_res_304_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Std(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_NormalFormLaws(uint8_t builtin) {
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
