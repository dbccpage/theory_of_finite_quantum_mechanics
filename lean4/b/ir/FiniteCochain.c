// Lean compiler output
// Module: FiniteCochain
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
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v0"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v2"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__17_value;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v1"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__18_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__18_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__19_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FiniteCochain_instReprCochain0___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0___closed__0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "e01"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "e20"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__6_value;
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "e12"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__7 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__7_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__7_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__8_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FiniteCochain_instReprCochain1___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1___closed__0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain1___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "f0"};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__3_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FiniteCochain_instReprCochain2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2 = (const lean_object*)&lp_FiniteQuantum_FiniteCochain_instReprCochain2___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_d0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_d1(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_d1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_add1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_add1___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_v0_3_; lean_object* v_v1_4_; lean_object* v_v2_5_; lean_object* v_v0_6_; lean_object* v_v1_7_; lean_object* v_v2_8_; uint8_t v___x_9_; 
v_v0_3_ = lean_ctor_get(v_x_1_, 0);
v_v1_4_ = lean_ctor_get(v_x_1_, 1);
v_v2_5_ = lean_ctor_get(v_x_1_, 2);
v_v0_6_ = lean_ctor_get(v_x_2_, 0);
v_v1_7_ = lean_ctor_get(v_x_2_, 1);
v_v2_8_ = lean_ctor_get(v_x_2_, 2);
v___x_9_ = lean_int_dec_eq(v_v0_3_, v_v0_6_);
if (v___x_9_ == 0)
{
return v___x_9_;
}
else
{
uint8_t v___x_10_; 
v___x_10_ = lean_int_dec_eq(v_v1_4_, v_v1_7_);
if (v___x_10_ == 0)
{
return v___x_10_;
}
else
{
uint8_t v___x_11_; 
v___x_11_ = lean_int_dec_eq(v_v2_5_, v_v2_8_);
return v___x_11_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0_decEq___boxed(lean_object* v_x_12_, lean_object* v_x_13_){
_start:
{
uint8_t v_res_14_; lean_object* v_r_15_; 
v_res_14_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0_decEq(v_x_12_, v_x_13_);
lean_dec_ref(v_x_13_);
lean_dec_ref(v_x_12_);
v_r_15_ = lean_box(v_res_14_);
return v_r_15_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0(lean_object* v_x_16_, lean_object* v_x_17_){
_start:
{
uint8_t v___x_18_; 
v___x_18_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0_decEq(v_x_16_, v_x_17_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0___boxed(lean_object* v_x_19_, lean_object* v_x_20_){
_start:
{
uint8_t v_res_21_; lean_object* v_r_22_; 
v_res_21_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain0(v_x_19_, v_x_20_);
lean_dec_ref(v_x_20_);
lean_dec_ref(v_x_19_);
v_r_22_ = lean_box(v_res_21_);
return v_r_22_;
}
}
static lean_object* _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_36_ = lean_unsigned_to_nat(6u);
v___x_37_ = lean_nat_to_int(v___x_36_);
return v___x_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_39_; lean_object* v___x_40_; 
v___x_39_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__0));
v___x_40_ = lean_string_length(v___x_39_);
return v___x_40_;
}
}
static lean_object* _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_41_; lean_object* v___x_42_; 
v___x_41_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__9, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__9);
v___x_42_ = lean_nat_to_int(v___x_41_);
return v___x_42_;
}
}
static lean_object* _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_50_ = lean_unsigned_to_nat(0u);
v___x_51_ = lean_nat_to_int(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg(lean_object* v_x_58_){
_start:
{
lean_object* v_v0_59_; lean_object* v_v1_60_; lean_object* v_v2_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___y_66_; lean_object* v___y_67_; lean_object* v___y_68_; uint8_t v___y_80_; lean_object* v___y_81_; lean_object* v___y_82_; lean_object* v___y_83_; lean_object* v___y_84_; lean_object* v___y_102_; lean_object* v___x_122_; lean_object* v___x_123_; uint8_t v___x_124_; 
v_v0_59_ = lean_ctor_get(v_x_58_, 0);
v_v1_60_ = lean_ctor_get(v_x_58_, 1);
v_v2_61_ = lean_ctor_get(v_x_58_, 2);
v___x_62_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5));
v___x_63_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__6));
v___x_64_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7);
v___x_122_ = lean_unsigned_to_nat(0u);
v___x_123_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_124_ = lean_int_dec_lt(v_v0_59_, v___x_123_);
if (v___x_124_ == 0)
{
lean_object* v___x_125_; lean_object* v___x_126_; 
v___x_125_ = l_Int_repr(v_v0_59_);
v___x_126_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_126_, 0, v___x_125_);
v___y_102_ = v___x_126_;
goto v___jp_101_;
}
else
{
lean_object* v___x_127_; lean_object* v___x_128_; lean_object* v___x_129_; 
v___x_127_ = l_Int_repr(v_v0_59_);
v___x_128_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_128_, 0, v___x_127_);
v___x_129_ = l_Repr_addAppParen(v___x_128_, v___x_122_);
v___y_102_ = v___x_129_;
goto v___jp_101_;
}
v___jp_65_:
{
lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; lean_object* v___x_74_; lean_object* v___x_75_; lean_object* v___x_76_; lean_object* v___x_77_; lean_object* v___x_78_; 
v___x_69_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_69_, 0, v___x_64_);
lean_ctor_set(v___x_69_, 1, v___y_68_);
v___x_70_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_70_, 0, v___x_69_);
lean_ctor_set_uint8(v___x_70_, sizeof(void*)*1, v___y_66_);
v___x_71_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_71_, 0, v___y_67_);
lean_ctor_set(v___x_71_, 1, v___x_70_);
v___x_72_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10);
v___x_73_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__11));
v___x_74_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_74_, 0, v___x_73_);
lean_ctor_set(v___x_74_, 1, v___x_71_);
v___x_75_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__12));
v___x_76_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_76_, 0, v___x_74_);
lean_ctor_set(v___x_76_, 1, v___x_75_);
v___x_77_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_77_, 0, v___x_72_);
lean_ctor_set(v___x_77_, 1, v___x_76_);
v___x_78_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_78_, 0, v___x_77_);
lean_ctor_set_uint8(v___x_78_, sizeof(void*)*1, v___y_66_);
return v___x_78_;
}
v___jp_79_:
{
lean_object* v___x_85_; lean_object* v___x_86_; lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; lean_object* v___x_94_; uint8_t v___x_95_; 
v___x_85_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_85_, 0, v___x_64_);
lean_ctor_set(v___x_85_, 1, v___y_84_);
v___x_86_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_86_, 0, v___x_85_);
lean_ctor_set_uint8(v___x_86_, sizeof(void*)*1, v___y_80_);
v___x_87_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_87_, 0, v___y_83_);
lean_ctor_set(v___x_87_, 1, v___x_86_);
lean_inc(v___y_81_);
v___x_88_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_88_, 0, v___x_87_);
lean_ctor_set(v___x_88_, 1, v___y_81_);
lean_inc(v___y_82_);
v___x_89_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_88_);
lean_ctor_set(v___x_89_, 1, v___y_82_);
v___x_90_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__14));
v___x_91_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_91_, 0, v___x_89_);
lean_ctor_set(v___x_91_, 1, v___x_90_);
v___x_92_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_92_, 0, v___x_91_);
lean_ctor_set(v___x_92_, 1, v___x_62_);
v___x_93_ = lean_unsigned_to_nat(0u);
v___x_94_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_95_ = lean_int_dec_lt(v_v2_61_, v___x_94_);
if (v___x_95_ == 0)
{
lean_object* v___x_96_; lean_object* v___x_97_; 
v___x_96_ = l_Int_repr(v_v2_61_);
v___x_97_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_97_, 0, v___x_96_);
v___y_66_ = v___y_80_;
v___y_67_ = v___x_92_;
v___y_68_ = v___x_97_;
goto v___jp_65_;
}
else
{
lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; 
v___x_98_ = l_Int_repr(v_v2_61_);
v___x_99_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_99_, 0, v___x_98_);
v___x_100_ = l_Repr_addAppParen(v___x_99_, v___x_93_);
v___y_66_ = v___y_80_;
v___y_67_ = v___x_92_;
v___y_68_ = v___x_100_;
goto v___jp_65_;
}
}
v___jp_101_:
{
lean_object* v___x_103_; uint8_t v___x_104_; lean_object* v___x_105_; lean_object* v___x_106_; lean_object* v___x_107_; lean_object* v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; lean_object* v___x_113_; lean_object* v___x_114_; lean_object* v___x_115_; uint8_t v___x_116_; 
v___x_103_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_103_, 0, v___x_64_);
lean_ctor_set(v___x_103_, 1, v___y_102_);
v___x_104_ = 0;
v___x_105_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_105_, 0, v___x_103_);
lean_ctor_set_uint8(v___x_105_, sizeof(void*)*1, v___x_104_);
v___x_106_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_106_, 0, v___x_63_);
lean_ctor_set(v___x_106_, 1, v___x_105_);
v___x_107_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__17));
v___x_108_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_108_, 0, v___x_106_);
lean_ctor_set(v___x_108_, 1, v___x_107_);
v___x_109_ = lean_box(1);
v___x_110_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_110_, 0, v___x_108_);
lean_ctor_set(v___x_110_, 1, v___x_109_);
v___x_111_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__19));
v___x_112_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_112_, 0, v___x_110_);
lean_ctor_set(v___x_112_, 1, v___x_111_);
v___x_113_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_113_, 0, v___x_112_);
lean_ctor_set(v___x_113_, 1, v___x_62_);
v___x_114_ = lean_unsigned_to_nat(0u);
v___x_115_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_116_ = lean_int_dec_lt(v_v1_60_, v___x_115_);
if (v___x_116_ == 0)
{
lean_object* v___x_117_; lean_object* v___x_118_; 
v___x_117_ = l_Int_repr(v_v1_60_);
v___x_118_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_118_, 0, v___x_117_);
v___y_80_ = v___x_104_;
v___y_81_ = v___x_107_;
v___y_82_ = v___x_109_;
v___y_83_ = v___x_113_;
v___y_84_ = v___x_118_;
goto v___jp_79_;
}
else
{
lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_119_ = l_Int_repr(v_v1_60_);
v___x_120_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_120_, 0, v___x_119_);
v___x_121_ = l_Repr_addAppParen(v___x_120_, v___x_114_);
v___y_80_ = v___x_104_;
v___y_81_ = v___x_107_;
v___y_82_ = v___x_109_;
v___y_83_ = v___x_113_;
v___y_84_ = v___x_121_;
goto v___jp_79_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___boxed(lean_object* v_x_130_){
_start:
{
lean_object* v_res_131_; 
v_res_131_ = lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg(v_x_130_);
lean_dec_ref(v_x_130_);
return v_res_131_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr(lean_object* v_x_132_, lean_object* v_prec_133_){
_start:
{
lean_object* v___x_134_; 
v___x_134_ = lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg(v_x_132_);
return v___x_134_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___boxed(lean_object* v_x_135_, lean_object* v_prec_136_){
_start:
{
lean_object* v_res_137_; 
v_res_137_ = lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr(v_x_135_, v_prec_136_);
lean_dec(v_prec_136_);
lean_dec_ref(v_x_135_);
return v_res_137_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1_decEq(lean_object* v_x_140_, lean_object* v_x_141_){
_start:
{
lean_object* v_e01_142_; lean_object* v_e12_143_; lean_object* v_e20_144_; lean_object* v_e01_145_; lean_object* v_e12_146_; lean_object* v_e20_147_; uint8_t v___x_148_; 
v_e01_142_ = lean_ctor_get(v_x_140_, 0);
v_e12_143_ = lean_ctor_get(v_x_140_, 1);
v_e20_144_ = lean_ctor_get(v_x_140_, 2);
v_e01_145_ = lean_ctor_get(v_x_141_, 0);
v_e12_146_ = lean_ctor_get(v_x_141_, 1);
v_e20_147_ = lean_ctor_get(v_x_141_, 2);
v___x_148_ = lean_int_dec_eq(v_e01_142_, v_e01_145_);
if (v___x_148_ == 0)
{
return v___x_148_;
}
else
{
uint8_t v___x_149_; 
v___x_149_ = lean_int_dec_eq(v_e12_143_, v_e12_146_);
if (v___x_149_ == 0)
{
return v___x_149_;
}
else
{
uint8_t v___x_150_; 
v___x_150_ = lean_int_dec_eq(v_e20_144_, v_e20_147_);
return v___x_150_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1_decEq___boxed(lean_object* v_x_151_, lean_object* v_x_152_){
_start:
{
uint8_t v_res_153_; lean_object* v_r_154_; 
v_res_153_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1_decEq(v_x_151_, v_x_152_);
lean_dec_ref(v_x_152_);
lean_dec_ref(v_x_151_);
v_r_154_ = lean_box(v_res_153_);
return v_r_154_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1(lean_object* v_x_155_, lean_object* v_x_156_){
_start:
{
uint8_t v___x_157_; 
v___x_157_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1_decEq(v_x_155_, v_x_156_);
return v___x_157_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1___boxed(lean_object* v_x_158_, lean_object* v_x_159_){
_start:
{
uint8_t v_res_160_; lean_object* v_r_161_; 
v_res_160_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain1(v_x_158_, v_x_159_);
lean_dec_ref(v_x_159_);
lean_dec_ref(v_x_158_);
v_r_161_ = lean_box(v_res_160_);
return v_r_161_;
}
}
static lean_object* _init_lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_171_; lean_object* v___x_172_; 
v___x_171_ = lean_unsigned_to_nat(7u);
v___x_172_ = lean_nat_to_int(v___x_171_);
return v___x_172_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg(lean_object* v_x_179_){
_start:
{
lean_object* v_e01_180_; lean_object* v_e12_181_; lean_object* v_e20_182_; lean_object* v___x_183_; lean_object* v___x_184_; lean_object* v___x_185_; uint8_t v___y_187_; lean_object* v___y_188_; lean_object* v___y_189_; lean_object* v___y_201_; lean_object* v___y_202_; uint8_t v___y_203_; lean_object* v___y_204_; lean_object* v___y_205_; lean_object* v___y_223_; lean_object* v___x_243_; lean_object* v___x_244_; uint8_t v___x_245_; 
v_e01_180_ = lean_ctor_get(v_x_179_, 0);
v_e12_181_ = lean_ctor_get(v_x_179_, 1);
v_e20_182_ = lean_ctor_get(v_x_179_, 2);
v___x_183_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__5));
v___x_184_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__3));
v___x_185_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__4, &lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__4);
v___x_243_ = lean_unsigned_to_nat(0u);
v___x_244_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_245_ = lean_int_dec_lt(v_e01_180_, v___x_244_);
if (v___x_245_ == 0)
{
lean_object* v___x_246_; lean_object* v___x_247_; 
v___x_246_ = l_Int_repr(v_e01_180_);
v___x_247_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_247_, 0, v___x_246_);
v___y_223_ = v___x_247_;
goto v___jp_222_;
}
else
{
lean_object* v___x_248_; lean_object* v___x_249_; lean_object* v___x_250_; 
v___x_248_ = l_Int_repr(v_e01_180_);
v___x_249_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_249_, 0, v___x_248_);
v___x_250_ = l_Repr_addAppParen(v___x_249_, v___x_243_);
v___y_223_ = v___x_250_;
goto v___jp_222_;
}
v___jp_186_:
{
lean_object* v___x_190_; lean_object* v___x_191_; lean_object* v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; lean_object* v___x_197_; lean_object* v___x_198_; lean_object* v___x_199_; 
v___x_190_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_190_, 0, v___x_185_);
lean_ctor_set(v___x_190_, 1, v___y_189_);
v___x_191_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_191_, 0, v___x_190_);
lean_ctor_set_uint8(v___x_191_, sizeof(void*)*1, v___y_187_);
v___x_192_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_192_, 0, v___y_188_);
lean_ctor_set(v___x_192_, 1, v___x_191_);
v___x_193_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10);
v___x_194_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__11));
v___x_195_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_195_, 0, v___x_194_);
lean_ctor_set(v___x_195_, 1, v___x_192_);
v___x_196_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__12));
v___x_197_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_197_, 0, v___x_195_);
lean_ctor_set(v___x_197_, 1, v___x_196_);
v___x_198_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_198_, 0, v___x_193_);
lean_ctor_set(v___x_198_, 1, v___x_197_);
v___x_199_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_199_, 0, v___x_198_);
lean_ctor_set_uint8(v___x_199_, sizeof(void*)*1, v___y_187_);
return v___x_199_;
}
v___jp_200_:
{
lean_object* v___x_206_; lean_object* v___x_207_; lean_object* v___x_208_; lean_object* v___x_209_; lean_object* v___x_210_; lean_object* v___x_211_; lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_214_; lean_object* v___x_215_; uint8_t v___x_216_; 
v___x_206_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_206_, 0, v___x_185_);
lean_ctor_set(v___x_206_, 1, v___y_205_);
v___x_207_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_207_, 0, v___x_206_);
lean_ctor_set_uint8(v___x_207_, sizeof(void*)*1, v___y_203_);
v___x_208_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_208_, 0, v___y_202_);
lean_ctor_set(v___x_208_, 1, v___x_207_);
lean_inc(v___y_201_);
v___x_209_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_209_, 0, v___x_208_);
lean_ctor_set(v___x_209_, 1, v___y_201_);
lean_inc(v___y_204_);
v___x_210_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_210_, 0, v___x_209_);
lean_ctor_set(v___x_210_, 1, v___y_204_);
v___x_211_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__6));
v___x_212_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_212_, 0, v___x_210_);
lean_ctor_set(v___x_212_, 1, v___x_211_);
v___x_213_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_213_, 0, v___x_212_);
lean_ctor_set(v___x_213_, 1, v___x_183_);
v___x_214_ = lean_unsigned_to_nat(0u);
v___x_215_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_216_ = lean_int_dec_lt(v_e20_182_, v___x_215_);
if (v___x_216_ == 0)
{
lean_object* v___x_217_; lean_object* v___x_218_; 
v___x_217_ = l_Int_repr(v_e20_182_);
v___x_218_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_218_, 0, v___x_217_);
v___y_187_ = v___y_203_;
v___y_188_ = v___x_213_;
v___y_189_ = v___x_218_;
goto v___jp_186_;
}
else
{
lean_object* v___x_219_; lean_object* v___x_220_; lean_object* v___x_221_; 
v___x_219_ = l_Int_repr(v_e20_182_);
v___x_220_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_220_, 0, v___x_219_);
v___x_221_ = l_Repr_addAppParen(v___x_220_, v___x_214_);
v___y_187_ = v___y_203_;
v___y_188_ = v___x_213_;
v___y_189_ = v___x_221_;
goto v___jp_186_;
}
}
v___jp_222_:
{
lean_object* v___x_224_; uint8_t v___x_225_; lean_object* v___x_226_; lean_object* v___x_227_; lean_object* v___x_228_; lean_object* v___x_229_; lean_object* v___x_230_; lean_object* v___x_231_; lean_object* v___x_232_; lean_object* v___x_233_; lean_object* v___x_234_; lean_object* v___x_235_; lean_object* v___x_236_; uint8_t v___x_237_; 
v___x_224_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_224_, 0, v___x_185_);
lean_ctor_set(v___x_224_, 1, v___y_223_);
v___x_225_ = 0;
v___x_226_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_226_, 0, v___x_224_);
lean_ctor_set_uint8(v___x_226_, sizeof(void*)*1, v___x_225_);
v___x_227_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_227_, 0, v___x_184_);
lean_ctor_set(v___x_227_, 1, v___x_226_);
v___x_228_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__17));
v___x_229_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_229_, 0, v___x_227_);
lean_ctor_set(v___x_229_, 1, v___x_228_);
v___x_230_ = lean_box(1);
v___x_231_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_231_, 0, v___x_229_);
lean_ctor_set(v___x_231_, 1, v___x_230_);
v___x_232_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___closed__8));
v___x_233_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_233_, 0, v___x_231_);
lean_ctor_set(v___x_233_, 1, v___x_232_);
v___x_234_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_234_, 0, v___x_233_);
lean_ctor_set(v___x_234_, 1, v___x_183_);
v___x_235_ = lean_unsigned_to_nat(0u);
v___x_236_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_237_ = lean_int_dec_lt(v_e12_181_, v___x_236_);
if (v___x_237_ == 0)
{
lean_object* v___x_238_; lean_object* v___x_239_; 
v___x_238_ = l_Int_repr(v_e12_181_);
v___x_239_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_239_, 0, v___x_238_);
v___y_201_ = v___x_228_;
v___y_202_ = v___x_234_;
v___y_203_ = v___x_225_;
v___y_204_ = v___x_230_;
v___y_205_ = v___x_239_;
goto v___jp_200_;
}
else
{
lean_object* v___x_240_; lean_object* v___x_241_; lean_object* v___x_242_; 
v___x_240_ = l_Int_repr(v_e12_181_);
v___x_241_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_241_, 0, v___x_240_);
v___x_242_ = l_Repr_addAppParen(v___x_241_, v___x_235_);
v___y_201_ = v___x_228_;
v___y_202_ = v___x_234_;
v___y_203_ = v___x_225_;
v___y_204_ = v___x_230_;
v___y_205_ = v___x_242_;
goto v___jp_200_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg___boxed(lean_object* v_x_251_){
_start:
{
lean_object* v_res_252_; 
v_res_252_ = lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg(v_x_251_);
lean_dec_ref(v_x_251_);
return v_res_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr(lean_object* v_x_253_, lean_object* v_prec_254_){
_start:
{
lean_object* v___x_255_; 
v___x_255_ = lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___redArg(v_x_253_);
return v___x_255_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr___boxed(lean_object* v_x_256_, lean_object* v_prec_257_){
_start:
{
lean_object* v_res_258_; 
v_res_258_ = lp_FiniteQuantum_FiniteCochain_instReprCochain1_repr(v_x_256_, v_prec_257_);
lean_dec(v_prec_257_);
lean_dec_ref(v_x_256_);
return v_res_258_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2_decEq(lean_object* v_x_261_, lean_object* v_x_262_){
_start:
{
uint8_t v___x_263_; 
v___x_263_ = lean_int_dec_eq(v_x_261_, v_x_262_);
return v___x_263_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2_decEq___boxed(lean_object* v_x_264_, lean_object* v_x_265_){
_start:
{
uint8_t v_res_266_; lean_object* v_r_267_; 
v_res_266_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2_decEq(v_x_264_, v_x_265_);
lean_dec(v_x_265_);
lean_dec(v_x_264_);
v_r_267_ = lean_box(v_res_266_);
return v_r_267_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2(lean_object* v_x_268_, lean_object* v_x_269_){
_start:
{
uint8_t v___x_270_; 
v___x_270_ = lean_int_dec_eq(v_x_268_, v_x_269_);
return v___x_270_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2___boxed(lean_object* v_x_271_, lean_object* v_x_272_){
_start:
{
uint8_t v_res_273_; lean_object* v_r_274_; 
v_res_273_ = lp_FiniteQuantum_FiniteCochain_instDecidableEqCochain2(v_x_271_, v_x_272_);
lean_dec(v_x_272_);
lean_dec(v_x_271_);
v_r_274_ = lean_box(v_res_273_);
return v_r_274_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg(lean_object* v_x_284_){
_start:
{
lean_object* v___x_285_; lean_object* v___x_286_; lean_object* v___y_288_; lean_object* v___x_300_; lean_object* v___x_301_; uint8_t v___x_302_; 
v___x_285_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___closed__3));
v___x_286_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__7);
v___x_300_ = lean_unsigned_to_nat(0u);
v___x_301_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__15);
v___x_302_ = lean_int_dec_lt(v_x_284_, v___x_301_);
if (v___x_302_ == 0)
{
lean_object* v___x_303_; lean_object* v___x_304_; 
v___x_303_ = l_Int_repr(v_x_284_);
v___x_304_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_304_, 0, v___x_303_);
v___y_288_ = v___x_304_;
goto v___jp_287_;
}
else
{
lean_object* v___x_305_; lean_object* v___x_306_; lean_object* v___x_307_; 
v___x_305_ = l_Int_repr(v_x_284_);
v___x_306_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_306_, 0, v___x_305_);
v___x_307_ = l_Repr_addAppParen(v___x_306_, v___x_300_);
v___y_288_ = v___x_307_;
goto v___jp_287_;
}
v___jp_287_:
{
lean_object* v___x_289_; uint8_t v___x_290_; lean_object* v___x_291_; lean_object* v___x_292_; lean_object* v___x_293_; lean_object* v___x_294_; lean_object* v___x_295_; lean_object* v___x_296_; lean_object* v___x_297_; lean_object* v___x_298_; lean_object* v___x_299_; 
v___x_289_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_289_, 0, v___x_286_);
lean_ctor_set(v___x_289_, 1, v___y_288_);
v___x_290_ = 0;
v___x_291_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_291_, 0, v___x_289_);
lean_ctor_set_uint8(v___x_291_, sizeof(void*)*1, v___x_290_);
v___x_292_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_292_, 0, v___x_285_);
lean_ctor_set(v___x_292_, 1, v___x_291_);
v___x_293_ = lean_obj_once(&lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10, &lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__10);
v___x_294_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__11));
v___x_295_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_295_, 0, v___x_294_);
lean_ctor_set(v___x_295_, 1, v___x_292_);
v___x_296_ = ((lean_object*)(lp_FiniteQuantum_FiniteCochain_instReprCochain0_repr___redArg___closed__12));
v___x_297_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_297_, 0, v___x_295_);
lean_ctor_set(v___x_297_, 1, v___x_296_);
v___x_298_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_298_, 0, v___x_293_);
lean_ctor_set(v___x_298_, 1, v___x_297_);
v___x_299_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_299_, 0, v___x_298_);
lean_ctor_set_uint8(v___x_299_, sizeof(void*)*1, v___x_290_);
return v___x_299_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg___boxed(lean_object* v_x_308_){
_start:
{
lean_object* v_res_309_; 
v_res_309_ = lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg(v_x_308_);
lean_dec(v_x_308_);
return v_res_309_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr(lean_object* v_x_310_, lean_object* v_prec_311_){
_start:
{
lean_object* v___x_312_; 
v___x_312_ = lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___redArg(v_x_310_);
return v___x_312_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr___boxed(lean_object* v_x_313_, lean_object* v_prec_314_){
_start:
{
lean_object* v_res_315_; 
v_res_315_ = lp_FiniteQuantum_FiniteCochain_instReprCochain2_repr(v_x_313_, v_prec_314_);
lean_dec(v_prec_314_);
lean_dec(v_x_313_);
return v_res_315_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_d0(lean_object* v_a_318_){
_start:
{
lean_object* v_v0_319_; lean_object* v_v1_320_; lean_object* v_v2_321_; lean_object* v___x_323_; uint8_t v_isShared_324_; uint8_t v_isSharedCheck_331_; 
v_v0_319_ = lean_ctor_get(v_a_318_, 0);
v_v1_320_ = lean_ctor_get(v_a_318_, 1);
v_v2_321_ = lean_ctor_get(v_a_318_, 2);
v_isSharedCheck_331_ = !lean_is_exclusive(v_a_318_);
if (v_isSharedCheck_331_ == 0)
{
v___x_323_ = v_a_318_;
v_isShared_324_ = v_isSharedCheck_331_;
goto v_resetjp_322_;
}
else
{
lean_inc(v_v2_321_);
lean_inc(v_v1_320_);
lean_inc(v_v0_319_);
lean_dec(v_a_318_);
v___x_323_ = lean_box(0);
v_isShared_324_ = v_isSharedCheck_331_;
goto v_resetjp_322_;
}
v_resetjp_322_:
{
lean_object* v___x_325_; lean_object* v___x_326_; lean_object* v___x_327_; lean_object* v___x_329_; 
v___x_325_ = lean_int_sub(v_v1_320_, v_v0_319_);
v___x_326_ = lean_int_sub(v_v2_321_, v_v1_320_);
lean_dec(v_v1_320_);
v___x_327_ = lean_int_sub(v_v0_319_, v_v2_321_);
lean_dec(v_v2_321_);
lean_dec(v_v0_319_);
if (v_isShared_324_ == 0)
{
lean_ctor_set(v___x_323_, 2, v___x_327_);
lean_ctor_set(v___x_323_, 1, v___x_326_);
lean_ctor_set(v___x_323_, 0, v___x_325_);
v___x_329_ = v___x_323_;
goto v_reusejp_328_;
}
else
{
lean_object* v_reuseFailAlloc_330_; 
v_reuseFailAlloc_330_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_330_, 0, v___x_325_);
lean_ctor_set(v_reuseFailAlloc_330_, 1, v___x_326_);
lean_ctor_set(v_reuseFailAlloc_330_, 2, v___x_327_);
v___x_329_ = v_reuseFailAlloc_330_;
goto v_reusejp_328_;
}
v_reusejp_328_:
{
return v___x_329_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_d1(lean_object* v_b_332_){
_start:
{
lean_object* v_e01_333_; lean_object* v_e12_334_; lean_object* v_e20_335_; lean_object* v___x_336_; lean_object* v___x_337_; 
v_e01_333_ = lean_ctor_get(v_b_332_, 0);
v_e12_334_ = lean_ctor_get(v_b_332_, 1);
v_e20_335_ = lean_ctor_get(v_b_332_, 2);
v___x_336_ = lean_int_add(v_e01_333_, v_e12_334_);
v___x_337_ = lean_int_add(v___x_336_, v_e20_335_);
lean_dec(v___x_336_);
return v___x_337_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_d1___boxed(lean_object* v_b_338_){
_start:
{
lean_object* v_res_339_; 
v_res_339_ = lp_FiniteQuantum_FiniteCochain_d1(v_b_338_);
lean_dec_ref(v_b_338_);
return v_res_339_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_add1(lean_object* v_b1_340_, lean_object* v_b2_341_){
_start:
{
lean_object* v_e01_342_; lean_object* v_e12_343_; lean_object* v_e20_344_; lean_object* v_e01_345_; lean_object* v_e12_346_; lean_object* v_e20_347_; lean_object* v___x_349_; uint8_t v_isShared_350_; uint8_t v_isSharedCheck_357_; 
v_e01_342_ = lean_ctor_get(v_b1_340_, 0);
v_e12_343_ = lean_ctor_get(v_b1_340_, 1);
v_e20_344_ = lean_ctor_get(v_b1_340_, 2);
v_e01_345_ = lean_ctor_get(v_b2_341_, 0);
v_e12_346_ = lean_ctor_get(v_b2_341_, 1);
v_e20_347_ = lean_ctor_get(v_b2_341_, 2);
v_isSharedCheck_357_ = !lean_is_exclusive(v_b2_341_);
if (v_isSharedCheck_357_ == 0)
{
v___x_349_ = v_b2_341_;
v_isShared_350_ = v_isSharedCheck_357_;
goto v_resetjp_348_;
}
else
{
lean_inc(v_e20_347_);
lean_inc(v_e12_346_);
lean_inc(v_e01_345_);
lean_dec(v_b2_341_);
v___x_349_ = lean_box(0);
v_isShared_350_ = v_isSharedCheck_357_;
goto v_resetjp_348_;
}
v_resetjp_348_:
{
lean_object* v___x_351_; lean_object* v___x_352_; lean_object* v___x_353_; lean_object* v___x_355_; 
v___x_351_ = lean_int_add(v_e01_342_, v_e01_345_);
lean_dec(v_e01_345_);
v___x_352_ = lean_int_add(v_e12_343_, v_e12_346_);
lean_dec(v_e12_346_);
v___x_353_ = lean_int_add(v_e20_344_, v_e20_347_);
lean_dec(v_e20_347_);
if (v_isShared_350_ == 0)
{
lean_ctor_set(v___x_349_, 2, v___x_353_);
lean_ctor_set(v___x_349_, 1, v___x_352_);
lean_ctor_set(v___x_349_, 0, v___x_351_);
v___x_355_ = v___x_349_;
goto v_reusejp_354_;
}
else
{
lean_object* v_reuseFailAlloc_356_; 
v_reuseFailAlloc_356_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_356_, 0, v___x_351_);
lean_ctor_set(v_reuseFailAlloc_356_, 1, v___x_352_);
lean_ctor_set(v_reuseFailAlloc_356_, 2, v___x_353_);
v___x_355_ = v_reuseFailAlloc_356_;
goto v_reusejp_354_;
}
v_reusejp_354_:
{
return v___x_355_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteCochain_add1___boxed(lean_object* v_b1_358_, lean_object* v_b2_359_){
_start:
{
lean_object* v_res_360_; 
v_res_360_ = lp_FiniteQuantum_FiniteCochain_add1(v_b1_358_, v_b2_359_);
lean_dec_ref(v_b1_358_);
return v_res_360_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_FiniteCochain(uint8_t builtin) {
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
