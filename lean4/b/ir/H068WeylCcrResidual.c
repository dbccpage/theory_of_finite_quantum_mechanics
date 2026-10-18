// Lean compiler output
// Module: H068WeylCcrResidual
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
lean_object* lean_int_neg(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* l_Bool_repr___redArg(uint8_t);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m00"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m11"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m10"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__18_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__18_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m01"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__20 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__20_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__20_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m22"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__1_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m21"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m20"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__5_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m12"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__7_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m02"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__9_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr3(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr3___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub3___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm3(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_bmul(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_bmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2Z2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2Z2___boxed(lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2Z2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 0, 0, 1, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2Z2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2Z2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2Z2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2Z2___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_P__char2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(0, 1, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_P__char2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_P__char2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_P__char2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_P__char2___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_Q__char2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(0, 0, 1, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Q__char2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_Q__char2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Q__char2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_Q__char2___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "a"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "b"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__6_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_esub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_esub___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instZeroEisenstein;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instOneEisenstein;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instAddEisenstein___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instAddEisenstein___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instAddEisenstein___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instAddEisenstein = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instAddEisenstein___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instSubEisenstein___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_esub___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instSubEisenstein___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instSubEisenstein___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instSubEisenstein = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instSubEisenstein___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instMulEisenstein___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instMulEisenstein___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instMulEisenstein___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instMulEisenstein = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instMulEisenstein___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3E(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3E___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3E(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3E___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_m00_3_; lean_object* v_m01_4_; lean_object* v_m10_5_; lean_object* v_m11_6_; lean_object* v_m00_7_; lean_object* v_m01_8_; lean_object* v_m10_9_; lean_object* v_m11_10_; uint8_t v___x_11_; 
v_m00_3_ = lean_ctor_get(v_x_1_, 0);
v_m01_4_ = lean_ctor_get(v_x_1_, 1);
v_m10_5_ = lean_ctor_get(v_x_1_, 2);
v_m11_6_ = lean_ctor_get(v_x_1_, 3);
v_m00_7_ = lean_ctor_get(v_x_2_, 0);
v_m01_8_ = lean_ctor_get(v_x_2_, 1);
v_m10_9_ = lean_ctor_get(v_x_2_, 2);
v_m11_10_ = lean_ctor_get(v_x_2_, 3);
v___x_11_ = lean_int_dec_eq(v_m00_3_, v_m00_7_);
if (v___x_11_ == 0)
{
return v___x_11_;
}
else
{
uint8_t v___x_12_; 
v___x_12_ = lean_int_dec_eq(v_m01_4_, v_m01_8_);
if (v___x_12_ == 0)
{
return v___x_12_;
}
else
{
uint8_t v___x_13_; 
v___x_13_ = lean_int_dec_eq(v_m10_5_, v_m10_9_);
if (v___x_13_ == 0)
{
return v___x_13_;
}
else
{
uint8_t v___x_14_; 
v___x_14_ = lean_int_dec_eq(v_m11_6_, v_m11_10_);
return v___x_14_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2_decEq___boxed(lean_object* v_x_15_, lean_object* v_x_16_){
_start:
{
uint8_t v_res_17_; lean_object* v_r_18_; 
v_res_17_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2_decEq(v_x_15_, v_x_16_);
lean_dec_ref(v_x_16_);
lean_dec_ref(v_x_15_);
v_r_18_ = lean_box(v_res_17_);
return v_r_18_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2(lean_object* v_x_19_, lean_object* v_x_20_){
_start:
{
uint8_t v___x_21_; 
v___x_21_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2_decEq(v_x_19_, v_x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2___boxed(lean_object* v_x_22_, lean_object* v_x_23_){
_start:
{
uint8_t v_res_24_; lean_object* v_r_25_; 
v_res_24_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2(v_x_22_, v_x_23_);
lean_dec_ref(v_x_23_);
lean_dec_ref(v_x_22_);
v_r_25_ = lean_box(v_res_24_);
return v_r_25_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_39_; lean_object* v___x_40_; 
v___x_39_ = lean_unsigned_to_nat(7u);
v___x_40_ = lean_nat_to_int(v___x_39_);
return v___x_40_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_42_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__0));
v___x_43_ = lean_string_length(v___x_42_);
return v___x_43_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_44_; lean_object* v___x_45_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__9);
v___x_45_ = lean_nat_to_int(v___x_44_);
return v___x_45_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_53_ = lean_unsigned_to_nat(0u);
v___x_54_ = lean_nat_to_int(v___x_53_);
return v___x_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg(lean_object* v_x_64_){
_start:
{
lean_object* v_m00_65_; lean_object* v_m01_66_; lean_object* v_m10_67_; lean_object* v_m11_68_; lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; uint8_t v___y_73_; lean_object* v___y_74_; lean_object* v___y_75_; uint8_t v___y_87_; lean_object* v___y_88_; lean_object* v___y_89_; lean_object* v___y_90_; lean_object* v___y_91_; uint8_t v___y_109_; lean_object* v___y_110_; lean_object* v___y_111_; lean_object* v___y_112_; lean_object* v___y_113_; lean_object* v___y_131_; lean_object* v___x_151_; lean_object* v___x_152_; uint8_t v___x_153_; 
v_m00_65_ = lean_ctor_get(v_x_64_, 0);
v_m01_66_ = lean_ctor_get(v_x_64_, 1);
v_m10_67_ = lean_ctor_get(v_x_64_, 2);
v_m11_68_ = lean_ctor_get(v_x_64_, 3);
v___x_69_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5));
v___x_70_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6));
v___x_71_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7);
v___x_151_ = lean_unsigned_to_nat(0u);
v___x_152_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_153_ = lean_int_dec_lt(v_m00_65_, v___x_152_);
if (v___x_153_ == 0)
{
lean_object* v___x_154_; lean_object* v___x_155_; 
v___x_154_ = l_Int_repr(v_m00_65_);
v___x_155_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_155_, 0, v___x_154_);
v___y_131_ = v___x_155_;
goto v___jp_130_;
}
else
{
lean_object* v___x_156_; lean_object* v___x_157_; lean_object* v___x_158_; 
v___x_156_ = l_Int_repr(v_m00_65_);
v___x_157_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_157_, 0, v___x_156_);
v___x_158_ = l_Repr_addAppParen(v___x_157_, v___x_151_);
v___y_131_ = v___x_158_;
goto v___jp_130_;
}
v___jp_72_:
{
lean_object* v___x_76_; lean_object* v___x_77_; lean_object* v___x_78_; lean_object* v___x_79_; lean_object* v___x_80_; lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; 
v___x_76_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_76_, 0, v___x_71_);
lean_ctor_set(v___x_76_, 1, v___y_75_);
v___x_77_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_77_, 0, v___x_76_);
lean_ctor_set_uint8(v___x_77_, sizeof(void*)*1, v___y_73_);
v___x_78_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_78_, 0, v___y_74_);
lean_ctor_set(v___x_78_, 1, v___x_77_);
v___x_79_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10);
v___x_80_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11));
v___x_81_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_81_, 0, v___x_80_);
lean_ctor_set(v___x_81_, 1, v___x_78_);
v___x_82_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12));
v___x_83_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_83_, 0, v___x_81_);
lean_ctor_set(v___x_83_, 1, v___x_82_);
v___x_84_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_84_, 0, v___x_79_);
lean_ctor_set(v___x_84_, 1, v___x_83_);
v___x_85_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_85_, 0, v___x_84_);
lean_ctor_set_uint8(v___x_85_, sizeof(void*)*1, v___y_73_);
return v___x_85_;
}
v___jp_86_:
{
lean_object* v___x_92_; lean_object* v___x_93_; lean_object* v___x_94_; lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; uint8_t v___x_102_; 
v___x_92_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_92_, 0, v___x_71_);
lean_ctor_set(v___x_92_, 1, v___y_91_);
v___x_93_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_93_, 0, v___x_92_);
lean_ctor_set_uint8(v___x_93_, sizeof(void*)*1, v___y_87_);
v___x_94_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_94_, 0, v___y_89_);
lean_ctor_set(v___x_94_, 1, v___x_93_);
lean_inc(v___y_90_);
v___x_95_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_95_, 0, v___x_94_);
lean_ctor_set(v___x_95_, 1, v___y_90_);
lean_inc(v___y_88_);
v___x_96_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_96_, 0, v___x_95_);
lean_ctor_set(v___x_96_, 1, v___y_88_);
v___x_97_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14));
v___x_98_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_98_, 0, v___x_96_);
lean_ctor_set(v___x_98_, 1, v___x_97_);
v___x_99_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_99_, 0, v___x_98_);
lean_ctor_set(v___x_99_, 1, v___x_69_);
v___x_100_ = lean_unsigned_to_nat(0u);
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_102_ = lean_int_dec_lt(v_m11_68_, v___x_101_);
if (v___x_102_ == 0)
{
lean_object* v___x_103_; lean_object* v___x_104_; 
v___x_103_ = l_Int_repr(v_m11_68_);
v___x_104_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_104_, 0, v___x_103_);
v___y_73_ = v___y_87_;
v___y_74_ = v___x_99_;
v___y_75_ = v___x_104_;
goto v___jp_72_;
}
else
{
lean_object* v___x_105_; lean_object* v___x_106_; lean_object* v___x_107_; 
v___x_105_ = l_Int_repr(v_m11_68_);
v___x_106_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_106_, 0, v___x_105_);
v___x_107_ = l_Repr_addAppParen(v___x_106_, v___x_100_);
v___y_73_ = v___y_87_;
v___y_74_ = v___x_99_;
v___y_75_ = v___x_107_;
goto v___jp_72_;
}
}
v___jp_108_:
{
lean_object* v___x_114_; lean_object* v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; lean_object* v___x_123_; uint8_t v___x_124_; 
v___x_114_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_114_, 0, v___x_71_);
lean_ctor_set(v___x_114_, 1, v___y_113_);
v___x_115_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_115_, 0, v___x_114_);
lean_ctor_set_uint8(v___x_115_, sizeof(void*)*1, v___y_109_);
v___x_116_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_116_, 0, v___y_112_);
lean_ctor_set(v___x_116_, 1, v___x_115_);
lean_inc(v___y_111_);
v___x_117_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_117_, 0, v___x_116_);
lean_ctor_set(v___x_117_, 1, v___y_111_);
lean_inc(v___y_110_);
v___x_118_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_118_, 0, v___x_117_);
lean_ctor_set(v___x_118_, 1, v___y_110_);
v___x_119_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17));
v___x_120_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_120_, 0, v___x_118_);
lean_ctor_set(v___x_120_, 1, v___x_119_);
v___x_121_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_121_, 0, v___x_120_);
lean_ctor_set(v___x_121_, 1, v___x_69_);
v___x_122_ = lean_unsigned_to_nat(0u);
v___x_123_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_124_ = lean_int_dec_lt(v_m10_67_, v___x_123_);
if (v___x_124_ == 0)
{
lean_object* v___x_125_; lean_object* v___x_126_; 
v___x_125_ = l_Int_repr(v_m10_67_);
v___x_126_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_126_, 0, v___x_125_);
v___y_87_ = v___y_109_;
v___y_88_ = v___y_110_;
v___y_89_ = v___x_121_;
v___y_90_ = v___y_111_;
v___y_91_ = v___x_126_;
goto v___jp_86_;
}
else
{
lean_object* v___x_127_; lean_object* v___x_128_; lean_object* v___x_129_; 
v___x_127_ = l_Int_repr(v_m10_67_);
v___x_128_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_128_, 0, v___x_127_);
v___x_129_ = l_Repr_addAppParen(v___x_128_, v___x_122_);
v___y_87_ = v___y_109_;
v___y_88_ = v___y_110_;
v___y_89_ = v___x_121_;
v___y_90_ = v___y_111_;
v___y_91_ = v___x_129_;
goto v___jp_86_;
}
}
v___jp_130_:
{
lean_object* v___x_132_; uint8_t v___x_133_; lean_object* v___x_134_; lean_object* v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; lean_object* v___x_138_; lean_object* v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; uint8_t v___x_145_; 
v___x_132_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_132_, 0, v___x_71_);
lean_ctor_set(v___x_132_, 1, v___y_131_);
v___x_133_ = 0;
v___x_134_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_134_, 0, v___x_132_);
lean_ctor_set_uint8(v___x_134_, sizeof(void*)*1, v___x_133_);
v___x_135_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_135_, 0, v___x_70_);
lean_ctor_set(v___x_135_, 1, v___x_134_);
v___x_136_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19));
v___x_137_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_137_, 0, v___x_135_);
lean_ctor_set(v___x_137_, 1, v___x_136_);
v___x_138_ = lean_box(1);
v___x_139_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_139_, 0, v___x_137_);
lean_ctor_set(v___x_139_, 1, v___x_138_);
v___x_140_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21));
v___x_141_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_141_, 0, v___x_139_);
lean_ctor_set(v___x_141_, 1, v___x_140_);
v___x_142_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_142_, 0, v___x_141_);
lean_ctor_set(v___x_142_, 1, v___x_69_);
v___x_143_ = lean_unsigned_to_nat(0u);
v___x_144_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_145_ = lean_int_dec_lt(v_m01_66_, v___x_144_);
if (v___x_145_ == 0)
{
lean_object* v___x_146_; lean_object* v___x_147_; 
v___x_146_ = l_Int_repr(v_m01_66_);
v___x_147_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_147_, 0, v___x_146_);
v___y_109_ = v___x_133_;
v___y_110_ = v___x_138_;
v___y_111_ = v___x_136_;
v___y_112_ = v___x_142_;
v___y_113_ = v___x_147_;
goto v___jp_108_;
}
else
{
lean_object* v___x_148_; lean_object* v___x_149_; lean_object* v___x_150_; 
v___x_148_ = l_Int_repr(v_m01_66_);
v___x_149_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_149_, 0, v___x_148_);
v___x_150_ = l_Repr_addAppParen(v___x_149_, v___x_143_);
v___y_109_ = v___x_133_;
v___y_110_ = v___x_138_;
v___y_111_ = v___x_136_;
v___y_112_ = v___x_142_;
v___y_113_ = v___x_150_;
goto v___jp_108_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___boxed(lean_object* v_x_159_){
_start:
{
lean_object* v_res_160_; 
v_res_160_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg(v_x_159_);
lean_dec_ref(v_x_159_);
return v_res_160_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr(lean_object* v_x_161_, lean_object* v_prec_162_){
_start:
{
lean_object* v___x_163_; 
v___x_163_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg(v_x_161_);
return v___x_163_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___boxed(lean_object* v_x_164_, lean_object* v_prec_165_){
_start:
{
lean_object* v_res_166_; 
v_res_166_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr(v_x_164_, v_prec_165_);
lean_dec(v_prec_165_);
lean_dec_ref(v_x_164_);
return v_res_166_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr2(lean_object* v_A_169_){
_start:
{
lean_object* v_m00_170_; lean_object* v_m11_171_; lean_object* v___x_172_; 
v_m00_170_ = lean_ctor_get(v_A_169_, 0);
v_m11_171_ = lean_ctor_get(v_A_169_, 3);
v___x_172_ = lean_int_add(v_m00_170_, v_m11_171_);
return v___x_172_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr2___boxed(lean_object* v_A_173_){
_start:
{
lean_object* v_res_174_; 
v_res_174_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr2(v_A_173_);
lean_dec_ref(v_A_173_);
return v_res_174_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2(lean_object* v_A_175_, lean_object* v_B_176_){
_start:
{
lean_object* v_m00_177_; lean_object* v_m01_178_; lean_object* v_m10_179_; lean_object* v_m11_180_; lean_object* v_m00_181_; lean_object* v_m01_182_; lean_object* v_m10_183_; lean_object* v_m11_184_; lean_object* v___x_186_; uint8_t v_isShared_187_; uint8_t v_isSharedCheck_203_; 
v_m00_177_ = lean_ctor_get(v_A_175_, 0);
v_m01_178_ = lean_ctor_get(v_A_175_, 1);
v_m10_179_ = lean_ctor_get(v_A_175_, 2);
v_m11_180_ = lean_ctor_get(v_A_175_, 3);
v_m00_181_ = lean_ctor_get(v_B_176_, 0);
v_m01_182_ = lean_ctor_get(v_B_176_, 1);
v_m10_183_ = lean_ctor_get(v_B_176_, 2);
v_m11_184_ = lean_ctor_get(v_B_176_, 3);
v_isSharedCheck_203_ = !lean_is_exclusive(v_B_176_);
if (v_isSharedCheck_203_ == 0)
{
v___x_186_ = v_B_176_;
v_isShared_187_ = v_isSharedCheck_203_;
goto v_resetjp_185_;
}
else
{
lean_inc(v_m11_184_);
lean_inc(v_m10_183_);
lean_inc(v_m01_182_);
lean_inc(v_m00_181_);
lean_dec(v_B_176_);
v___x_186_ = lean_box(0);
v_isShared_187_ = v_isSharedCheck_203_;
goto v_resetjp_185_;
}
v_resetjp_185_:
{
lean_object* v___x_188_; lean_object* v___x_189_; lean_object* v___x_190_; lean_object* v___x_191_; lean_object* v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; lean_object* v___x_197_; lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_201_; 
v___x_188_ = lean_int_mul(v_m00_177_, v_m00_181_);
v___x_189_ = lean_int_mul(v_m01_178_, v_m10_183_);
v___x_190_ = lean_int_add(v___x_188_, v___x_189_);
lean_dec(v___x_189_);
lean_dec(v___x_188_);
v___x_191_ = lean_int_mul(v_m00_177_, v_m01_182_);
v___x_192_ = lean_int_mul(v_m01_178_, v_m11_184_);
v___x_193_ = lean_int_add(v___x_191_, v___x_192_);
lean_dec(v___x_192_);
lean_dec(v___x_191_);
v___x_194_ = lean_int_mul(v_m10_179_, v_m00_181_);
lean_dec(v_m00_181_);
v___x_195_ = lean_int_mul(v_m11_180_, v_m10_183_);
lean_dec(v_m10_183_);
v___x_196_ = lean_int_add(v___x_194_, v___x_195_);
lean_dec(v___x_195_);
lean_dec(v___x_194_);
v___x_197_ = lean_int_mul(v_m10_179_, v_m01_182_);
lean_dec(v_m01_182_);
v___x_198_ = lean_int_mul(v_m11_180_, v_m11_184_);
lean_dec(v_m11_184_);
v___x_199_ = lean_int_add(v___x_197_, v___x_198_);
lean_dec(v___x_198_);
lean_dec(v___x_197_);
if (v_isShared_187_ == 0)
{
lean_ctor_set(v___x_186_, 3, v___x_199_);
lean_ctor_set(v___x_186_, 2, v___x_196_);
lean_ctor_set(v___x_186_, 1, v___x_193_);
lean_ctor_set(v___x_186_, 0, v___x_190_);
v___x_201_ = v___x_186_;
goto v_reusejp_200_;
}
else
{
lean_object* v_reuseFailAlloc_202_; 
v_reuseFailAlloc_202_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_202_, 0, v___x_190_);
lean_ctor_set(v_reuseFailAlloc_202_, 1, v___x_193_);
lean_ctor_set(v_reuseFailAlloc_202_, 2, v___x_196_);
lean_ctor_set(v_reuseFailAlloc_202_, 3, v___x_199_);
v___x_201_ = v_reuseFailAlloc_202_;
goto v_reusejp_200_;
}
v_reusejp_200_:
{
return v___x_201_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2___boxed(lean_object* v_A_204_, lean_object* v_B_205_){
_start:
{
lean_object* v_res_206_; 
v_res_206_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2(v_A_204_, v_B_205_);
lean_dec_ref(v_A_204_);
return v_res_206_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub2(lean_object* v_A_207_, lean_object* v_B_208_){
_start:
{
lean_object* v_m00_209_; lean_object* v_m01_210_; lean_object* v_m10_211_; lean_object* v_m11_212_; lean_object* v_m00_213_; lean_object* v_m01_214_; lean_object* v_m10_215_; lean_object* v_m11_216_; lean_object* v___x_218_; uint8_t v_isShared_219_; uint8_t v_isSharedCheck_227_; 
v_m00_209_ = lean_ctor_get(v_A_207_, 0);
v_m01_210_ = lean_ctor_get(v_A_207_, 1);
v_m10_211_ = lean_ctor_get(v_A_207_, 2);
v_m11_212_ = lean_ctor_get(v_A_207_, 3);
v_m00_213_ = lean_ctor_get(v_B_208_, 0);
v_m01_214_ = lean_ctor_get(v_B_208_, 1);
v_m10_215_ = lean_ctor_get(v_B_208_, 2);
v_m11_216_ = lean_ctor_get(v_B_208_, 3);
v_isSharedCheck_227_ = !lean_is_exclusive(v_B_208_);
if (v_isSharedCheck_227_ == 0)
{
v___x_218_ = v_B_208_;
v_isShared_219_ = v_isSharedCheck_227_;
goto v_resetjp_217_;
}
else
{
lean_inc(v_m11_216_);
lean_inc(v_m10_215_);
lean_inc(v_m01_214_);
lean_inc(v_m00_213_);
lean_dec(v_B_208_);
v___x_218_ = lean_box(0);
v_isShared_219_ = v_isSharedCheck_227_;
goto v_resetjp_217_;
}
v_resetjp_217_:
{
lean_object* v___x_220_; lean_object* v___x_221_; lean_object* v___x_222_; lean_object* v___x_223_; lean_object* v___x_225_; 
v___x_220_ = lean_int_sub(v_m00_209_, v_m00_213_);
lean_dec(v_m00_213_);
v___x_221_ = lean_int_sub(v_m01_210_, v_m01_214_);
lean_dec(v_m01_214_);
v___x_222_ = lean_int_sub(v_m10_211_, v_m10_215_);
lean_dec(v_m10_215_);
v___x_223_ = lean_int_sub(v_m11_212_, v_m11_216_);
lean_dec(v_m11_216_);
if (v_isShared_219_ == 0)
{
lean_ctor_set(v___x_218_, 3, v___x_223_);
lean_ctor_set(v___x_218_, 2, v___x_222_);
lean_ctor_set(v___x_218_, 1, v___x_221_);
lean_ctor_set(v___x_218_, 0, v___x_220_);
v___x_225_ = v___x_218_;
goto v_reusejp_224_;
}
else
{
lean_object* v_reuseFailAlloc_226_; 
v_reuseFailAlloc_226_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_226_, 0, v___x_220_);
lean_ctor_set(v_reuseFailAlloc_226_, 1, v___x_221_);
lean_ctor_set(v_reuseFailAlloc_226_, 2, v___x_222_);
lean_ctor_set(v_reuseFailAlloc_226_, 3, v___x_223_);
v___x_225_ = v_reuseFailAlloc_226_;
goto v_reusejp_224_;
}
v_reusejp_224_:
{
return v___x_225_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub2___boxed(lean_object* v_A_228_, lean_object* v_B_229_){
_start:
{
lean_object* v_res_230_; 
v_res_230_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub2(v_A_228_, v_B_229_);
lean_dec_ref(v_A_228_);
return v_res_230_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul2(lean_object* v_c_231_, lean_object* v_A_232_){
_start:
{
lean_object* v_m00_233_; lean_object* v_m01_234_; lean_object* v_m10_235_; lean_object* v_m11_236_; lean_object* v___x_238_; uint8_t v_isShared_239_; uint8_t v_isSharedCheck_247_; 
v_m00_233_ = lean_ctor_get(v_A_232_, 0);
v_m01_234_ = lean_ctor_get(v_A_232_, 1);
v_m10_235_ = lean_ctor_get(v_A_232_, 2);
v_m11_236_ = lean_ctor_get(v_A_232_, 3);
v_isSharedCheck_247_ = !lean_is_exclusive(v_A_232_);
if (v_isSharedCheck_247_ == 0)
{
v___x_238_ = v_A_232_;
v_isShared_239_ = v_isSharedCheck_247_;
goto v_resetjp_237_;
}
else
{
lean_inc(v_m11_236_);
lean_inc(v_m10_235_);
lean_inc(v_m01_234_);
lean_inc(v_m00_233_);
lean_dec(v_A_232_);
v___x_238_ = lean_box(0);
v_isShared_239_ = v_isSharedCheck_247_;
goto v_resetjp_237_;
}
v_resetjp_237_:
{
lean_object* v___x_240_; lean_object* v___x_241_; lean_object* v___x_242_; lean_object* v___x_243_; lean_object* v___x_245_; 
v___x_240_ = lean_int_mul(v_c_231_, v_m00_233_);
lean_dec(v_m00_233_);
v___x_241_ = lean_int_mul(v_c_231_, v_m01_234_);
lean_dec(v_m01_234_);
v___x_242_ = lean_int_mul(v_c_231_, v_m10_235_);
lean_dec(v_m10_235_);
v___x_243_ = lean_int_mul(v_c_231_, v_m11_236_);
lean_dec(v_m11_236_);
if (v_isShared_239_ == 0)
{
lean_ctor_set(v___x_238_, 3, v___x_243_);
lean_ctor_set(v___x_238_, 2, v___x_242_);
lean_ctor_set(v___x_238_, 1, v___x_241_);
lean_ctor_set(v___x_238_, 0, v___x_240_);
v___x_245_ = v___x_238_;
goto v_reusejp_244_;
}
else
{
lean_object* v_reuseFailAlloc_246_; 
v_reuseFailAlloc_246_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_246_, 0, v___x_240_);
lean_ctor_set(v_reuseFailAlloc_246_, 1, v___x_241_);
lean_ctor_set(v_reuseFailAlloc_246_, 2, v___x_242_);
lean_ctor_set(v_reuseFailAlloc_246_, 3, v___x_243_);
v___x_245_ = v_reuseFailAlloc_246_;
goto v_reusejp_244_;
}
v_reusejp_244_:
{
return v___x_245_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul2___boxed(lean_object* v_c_248_, lean_object* v_A_249_){
_start:
{
lean_object* v_res_250_; 
v_res_250_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul2(v_c_248_, v_A_249_);
lean_dec(v_c_248_);
return v_res_250_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2(lean_object* v_A_251_, lean_object* v_B_252_){
_start:
{
lean_object* v___x_253_; lean_object* v___x_254_; lean_object* v___x_255_; 
lean_inc_ref(v_B_252_);
v___x_253_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2(v_A_251_, v_B_252_);
v___x_254_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2(v_B_252_, v_A_251_);
lean_dec_ref(v_B_252_);
v___x_255_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub2(v___x_253_, v___x_254_);
lean_dec_ref(v___x_253_);
return v___x_255_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0(void){
_start:
{
lean_object* v___x_256_; lean_object* v___x_257_; 
v___x_256_ = lean_unsigned_to_nat(1u);
v___x_257_ = lean_nat_to_int(v___x_256_);
return v___x_257_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__1(void){
_start:
{
lean_object* v___x_258_; lean_object* v___x_259_; lean_object* v___x_260_; 
v___x_258_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_259_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_260_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_260_, 0, v___x_259_);
lean_ctor_set(v___x_260_, 1, v___x_258_);
lean_ctor_set(v___x_260_, 2, v___x_258_);
lean_ctor_set(v___x_260_, 3, v___x_259_);
return v___x_260_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2(void){
_start:
{
lean_object* v___x_261_; 
v___x_261_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__1);
return v___x_261_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3_decEq(lean_object* v_x_262_, lean_object* v_x_263_){
_start:
{
lean_object* v_m00_264_; lean_object* v_m01_265_; lean_object* v_m02_266_; lean_object* v_m10_267_; lean_object* v_m11_268_; lean_object* v_m12_269_; lean_object* v_m20_270_; lean_object* v_m21_271_; lean_object* v_m22_272_; lean_object* v_m00_273_; lean_object* v_m01_274_; lean_object* v_m02_275_; lean_object* v_m10_276_; lean_object* v_m11_277_; lean_object* v_m12_278_; lean_object* v_m20_279_; lean_object* v_m21_280_; lean_object* v_m22_281_; uint8_t v___x_282_; 
v_m00_264_ = lean_ctor_get(v_x_262_, 0);
v_m01_265_ = lean_ctor_get(v_x_262_, 1);
v_m02_266_ = lean_ctor_get(v_x_262_, 2);
v_m10_267_ = lean_ctor_get(v_x_262_, 3);
v_m11_268_ = lean_ctor_get(v_x_262_, 4);
v_m12_269_ = lean_ctor_get(v_x_262_, 5);
v_m20_270_ = lean_ctor_get(v_x_262_, 6);
v_m21_271_ = lean_ctor_get(v_x_262_, 7);
v_m22_272_ = lean_ctor_get(v_x_262_, 8);
v_m00_273_ = lean_ctor_get(v_x_263_, 0);
v_m01_274_ = lean_ctor_get(v_x_263_, 1);
v_m02_275_ = lean_ctor_get(v_x_263_, 2);
v_m10_276_ = lean_ctor_get(v_x_263_, 3);
v_m11_277_ = lean_ctor_get(v_x_263_, 4);
v_m12_278_ = lean_ctor_get(v_x_263_, 5);
v_m20_279_ = lean_ctor_get(v_x_263_, 6);
v_m21_280_ = lean_ctor_get(v_x_263_, 7);
v_m22_281_ = lean_ctor_get(v_x_263_, 8);
v___x_282_ = lean_int_dec_eq(v_m00_264_, v_m00_273_);
if (v___x_282_ == 0)
{
return v___x_282_;
}
else
{
uint8_t v___x_283_; 
v___x_283_ = lean_int_dec_eq(v_m01_265_, v_m01_274_);
if (v___x_283_ == 0)
{
return v___x_283_;
}
else
{
uint8_t v___x_284_; 
v___x_284_ = lean_int_dec_eq(v_m02_266_, v_m02_275_);
if (v___x_284_ == 0)
{
return v___x_284_;
}
else
{
uint8_t v___x_285_; 
v___x_285_ = lean_int_dec_eq(v_m10_267_, v_m10_276_);
if (v___x_285_ == 0)
{
return v___x_285_;
}
else
{
uint8_t v___x_286_; 
v___x_286_ = lean_int_dec_eq(v_m11_268_, v_m11_277_);
if (v___x_286_ == 0)
{
return v___x_286_;
}
else
{
uint8_t v___x_287_; 
v___x_287_ = lean_int_dec_eq(v_m12_269_, v_m12_278_);
if (v___x_287_ == 0)
{
return v___x_287_;
}
else
{
uint8_t v___x_288_; 
v___x_288_ = lean_int_dec_eq(v_m20_270_, v_m20_279_);
if (v___x_288_ == 0)
{
return v___x_288_;
}
else
{
uint8_t v___x_289_; 
v___x_289_ = lean_int_dec_eq(v_m21_271_, v_m21_280_);
if (v___x_289_ == 0)
{
return v___x_289_;
}
else
{
uint8_t v___x_290_; 
v___x_290_ = lean_int_dec_eq(v_m22_272_, v_m22_281_);
return v___x_290_;
}
}
}
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3_decEq___boxed(lean_object* v_x_291_, lean_object* v_x_292_){
_start:
{
uint8_t v_res_293_; lean_object* v_r_294_; 
v_res_293_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3_decEq(v_x_291_, v_x_292_);
lean_dec_ref(v_x_292_);
lean_dec_ref(v_x_291_);
v_r_294_ = lean_box(v_res_293_);
return v_r_294_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3(lean_object* v_x_295_, lean_object* v_x_296_){
_start:
{
uint8_t v___x_297_; 
v___x_297_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3_decEq(v_x_295_, v_x_296_);
return v___x_297_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3___boxed(lean_object* v_x_298_, lean_object* v_x_299_){
_start:
{
uint8_t v_res_300_; lean_object* v_r_301_; 
v_res_300_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3(v_x_298_, v_x_299_);
lean_dec_ref(v_x_299_);
lean_dec_ref(v_x_298_);
v_r_301_ = lean_box(v_res_300_);
return v_r_301_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg(lean_object* v_x_317_){
_start:
{
lean_object* v_m00_318_; lean_object* v_m01_319_; lean_object* v_m02_320_; lean_object* v_m10_321_; lean_object* v_m11_322_; lean_object* v_m12_323_; lean_object* v_m20_324_; lean_object* v_m21_325_; lean_object* v_m22_326_; lean_object* v___x_327_; lean_object* v___x_328_; lean_object* v___x_329_; lean_object* v___y_331_; uint8_t v___y_332_; lean_object* v___y_333_; lean_object* v___y_345_; lean_object* v___y_346_; lean_object* v___y_347_; uint8_t v___y_348_; lean_object* v___y_349_; lean_object* v___y_367_; lean_object* v___y_368_; lean_object* v___y_369_; uint8_t v___y_370_; lean_object* v___y_371_; lean_object* v___y_389_; lean_object* v___y_390_; lean_object* v___y_391_; uint8_t v___y_392_; lean_object* v___y_393_; lean_object* v___y_411_; lean_object* v___y_412_; lean_object* v___y_413_; uint8_t v___y_414_; lean_object* v___y_415_; lean_object* v___y_433_; lean_object* v___y_434_; lean_object* v___y_435_; uint8_t v___y_436_; lean_object* v___y_437_; lean_object* v___y_455_; lean_object* v___y_456_; lean_object* v___y_457_; uint8_t v___y_458_; lean_object* v___y_459_; lean_object* v___y_477_; lean_object* v___y_478_; lean_object* v___y_479_; uint8_t v___y_480_; lean_object* v___y_481_; lean_object* v___y_499_; lean_object* v___x_519_; lean_object* v___x_520_; uint8_t v___x_521_; 
v_m00_318_ = lean_ctor_get(v_x_317_, 0);
v_m01_319_ = lean_ctor_get(v_x_317_, 1);
v_m02_320_ = lean_ctor_get(v_x_317_, 2);
v_m10_321_ = lean_ctor_get(v_x_317_, 3);
v_m11_322_ = lean_ctor_get(v_x_317_, 4);
v_m12_323_ = lean_ctor_get(v_x_317_, 5);
v_m20_324_ = lean_ctor_get(v_x_317_, 6);
v_m21_325_ = lean_ctor_get(v_x_317_, 7);
v_m22_326_ = lean_ctor_get(v_x_317_, 8);
v___x_327_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5));
v___x_328_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6));
v___x_329_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7);
v___x_519_ = lean_unsigned_to_nat(0u);
v___x_520_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_521_ = lean_int_dec_lt(v_m00_318_, v___x_520_);
if (v___x_521_ == 0)
{
lean_object* v___x_522_; lean_object* v___x_523_; 
v___x_522_ = l_Int_repr(v_m00_318_);
v___x_523_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_523_, 0, v___x_522_);
v___y_499_ = v___x_523_;
goto v___jp_498_;
}
else
{
lean_object* v___x_524_; lean_object* v___x_525_; lean_object* v___x_526_; 
v___x_524_ = l_Int_repr(v_m00_318_);
v___x_525_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_525_, 0, v___x_524_);
v___x_526_ = l_Repr_addAppParen(v___x_525_, v___x_519_);
v___y_499_ = v___x_526_;
goto v___jp_498_;
}
v___jp_330_:
{
lean_object* v___x_334_; lean_object* v___x_335_; lean_object* v___x_336_; lean_object* v___x_337_; lean_object* v___x_338_; lean_object* v___x_339_; lean_object* v___x_340_; lean_object* v___x_341_; lean_object* v___x_342_; lean_object* v___x_343_; 
v___x_334_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_334_, 0, v___x_329_);
lean_ctor_set(v___x_334_, 1, v___y_333_);
v___x_335_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_335_, 0, v___x_334_);
lean_ctor_set_uint8(v___x_335_, sizeof(void*)*1, v___y_332_);
v___x_336_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_336_, 0, v___y_331_);
lean_ctor_set(v___x_336_, 1, v___x_335_);
v___x_337_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10);
v___x_338_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11));
v___x_339_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_339_, 0, v___x_338_);
lean_ctor_set(v___x_339_, 1, v___x_336_);
v___x_340_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12));
v___x_341_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_341_, 0, v___x_339_);
lean_ctor_set(v___x_341_, 1, v___x_340_);
v___x_342_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_342_, 0, v___x_337_);
lean_ctor_set(v___x_342_, 1, v___x_341_);
v___x_343_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_343_, 0, v___x_342_);
lean_ctor_set_uint8(v___x_343_, sizeof(void*)*1, v___y_332_);
return v___x_343_;
}
v___jp_344_:
{
lean_object* v___x_350_; lean_object* v___x_351_; lean_object* v___x_352_; lean_object* v___x_353_; lean_object* v___x_354_; lean_object* v___x_355_; lean_object* v___x_356_; lean_object* v___x_357_; lean_object* v___x_358_; lean_object* v___x_359_; uint8_t v___x_360_; 
v___x_350_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_350_, 0, v___x_329_);
lean_ctor_set(v___x_350_, 1, v___y_349_);
v___x_351_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_351_, 0, v___x_350_);
lean_ctor_set_uint8(v___x_351_, sizeof(void*)*1, v___y_348_);
v___x_352_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_352_, 0, v___y_347_);
lean_ctor_set(v___x_352_, 1, v___x_351_);
lean_inc(v___y_345_);
v___x_353_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_353_, 0, v___x_352_);
lean_ctor_set(v___x_353_, 1, v___y_345_);
lean_inc(v___y_346_);
v___x_354_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_354_, 0, v___x_353_);
lean_ctor_set(v___x_354_, 1, v___y_346_);
v___x_355_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__1));
v___x_356_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_356_, 0, v___x_354_);
lean_ctor_set(v___x_356_, 1, v___x_355_);
v___x_357_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_357_, 0, v___x_356_);
lean_ctor_set(v___x_357_, 1, v___x_327_);
v___x_358_ = lean_unsigned_to_nat(0u);
v___x_359_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_360_ = lean_int_dec_lt(v_m22_326_, v___x_359_);
if (v___x_360_ == 0)
{
lean_object* v___x_361_; lean_object* v___x_362_; 
v___x_361_ = l_Int_repr(v_m22_326_);
v___x_362_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_362_, 0, v___x_361_);
v___y_331_ = v___x_357_;
v___y_332_ = v___y_348_;
v___y_333_ = v___x_362_;
goto v___jp_330_;
}
else
{
lean_object* v___x_363_; lean_object* v___x_364_; lean_object* v___x_365_; 
v___x_363_ = l_Int_repr(v_m22_326_);
v___x_364_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_364_, 0, v___x_363_);
v___x_365_ = l_Repr_addAppParen(v___x_364_, v___x_358_);
v___y_331_ = v___x_357_;
v___y_332_ = v___y_348_;
v___y_333_ = v___x_365_;
goto v___jp_330_;
}
}
v___jp_366_:
{
lean_object* v___x_372_; lean_object* v___x_373_; lean_object* v___x_374_; lean_object* v___x_375_; lean_object* v___x_376_; lean_object* v___x_377_; lean_object* v___x_378_; lean_object* v___x_379_; lean_object* v___x_380_; lean_object* v___x_381_; uint8_t v___x_382_; 
v___x_372_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_372_, 0, v___x_329_);
lean_ctor_set(v___x_372_, 1, v___y_371_);
v___x_373_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_373_, 0, v___x_372_);
lean_ctor_set_uint8(v___x_373_, sizeof(void*)*1, v___y_370_);
v___x_374_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_374_, 0, v___y_368_);
lean_ctor_set(v___x_374_, 1, v___x_373_);
lean_inc(v___y_367_);
v___x_375_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_375_, 0, v___x_374_);
lean_ctor_set(v___x_375_, 1, v___y_367_);
lean_inc(v___y_369_);
v___x_376_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_376_, 0, v___x_375_);
lean_ctor_set(v___x_376_, 1, v___y_369_);
v___x_377_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__3));
v___x_378_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_378_, 0, v___x_376_);
lean_ctor_set(v___x_378_, 1, v___x_377_);
v___x_379_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_379_, 0, v___x_378_);
lean_ctor_set(v___x_379_, 1, v___x_327_);
v___x_380_ = lean_unsigned_to_nat(0u);
v___x_381_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_382_ = lean_int_dec_lt(v_m21_325_, v___x_381_);
if (v___x_382_ == 0)
{
lean_object* v___x_383_; lean_object* v___x_384_; 
v___x_383_ = l_Int_repr(v_m21_325_);
v___x_384_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_384_, 0, v___x_383_);
v___y_345_ = v___y_367_;
v___y_346_ = v___y_369_;
v___y_347_ = v___x_379_;
v___y_348_ = v___y_370_;
v___y_349_ = v___x_384_;
goto v___jp_344_;
}
else
{
lean_object* v___x_385_; lean_object* v___x_386_; lean_object* v___x_387_; 
v___x_385_ = l_Int_repr(v_m21_325_);
v___x_386_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_386_, 0, v___x_385_);
v___x_387_ = l_Repr_addAppParen(v___x_386_, v___x_380_);
v___y_345_ = v___y_367_;
v___y_346_ = v___y_369_;
v___y_347_ = v___x_379_;
v___y_348_ = v___y_370_;
v___y_349_ = v___x_387_;
goto v___jp_344_;
}
}
v___jp_388_:
{
lean_object* v___x_394_; lean_object* v___x_395_; lean_object* v___x_396_; lean_object* v___x_397_; lean_object* v___x_398_; lean_object* v___x_399_; lean_object* v___x_400_; lean_object* v___x_401_; lean_object* v___x_402_; lean_object* v___x_403_; uint8_t v___x_404_; 
v___x_394_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_394_, 0, v___x_329_);
lean_ctor_set(v___x_394_, 1, v___y_393_);
v___x_395_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_395_, 0, v___x_394_);
lean_ctor_set_uint8(v___x_395_, sizeof(void*)*1, v___y_392_);
v___x_396_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_396_, 0, v___y_389_);
lean_ctor_set(v___x_396_, 1, v___x_395_);
lean_inc(v___y_390_);
v___x_397_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_397_, 0, v___x_396_);
lean_ctor_set(v___x_397_, 1, v___y_390_);
lean_inc(v___y_391_);
v___x_398_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_398_, 0, v___x_397_);
lean_ctor_set(v___x_398_, 1, v___y_391_);
v___x_399_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__5));
v___x_400_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_400_, 0, v___x_398_);
lean_ctor_set(v___x_400_, 1, v___x_399_);
v___x_401_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_401_, 0, v___x_400_);
lean_ctor_set(v___x_401_, 1, v___x_327_);
v___x_402_ = lean_unsigned_to_nat(0u);
v___x_403_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_404_ = lean_int_dec_lt(v_m20_324_, v___x_403_);
if (v___x_404_ == 0)
{
lean_object* v___x_405_; lean_object* v___x_406_; 
v___x_405_ = l_Int_repr(v_m20_324_);
v___x_406_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_406_, 0, v___x_405_);
v___y_367_ = v___y_390_;
v___y_368_ = v___x_401_;
v___y_369_ = v___y_391_;
v___y_370_ = v___y_392_;
v___y_371_ = v___x_406_;
goto v___jp_366_;
}
else
{
lean_object* v___x_407_; lean_object* v___x_408_; lean_object* v___x_409_; 
v___x_407_ = l_Int_repr(v_m20_324_);
v___x_408_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_408_, 0, v___x_407_);
v___x_409_ = l_Repr_addAppParen(v___x_408_, v___x_402_);
v___y_367_ = v___y_390_;
v___y_368_ = v___x_401_;
v___y_369_ = v___y_391_;
v___y_370_ = v___y_392_;
v___y_371_ = v___x_409_;
goto v___jp_366_;
}
}
v___jp_410_:
{
lean_object* v___x_416_; lean_object* v___x_417_; lean_object* v___x_418_; lean_object* v___x_419_; lean_object* v___x_420_; lean_object* v___x_421_; lean_object* v___x_422_; lean_object* v___x_423_; lean_object* v___x_424_; lean_object* v___x_425_; uint8_t v___x_426_; 
v___x_416_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_416_, 0, v___x_329_);
lean_ctor_set(v___x_416_, 1, v___y_415_);
v___x_417_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_417_, 0, v___x_416_);
lean_ctor_set_uint8(v___x_417_, sizeof(void*)*1, v___y_414_);
v___x_418_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_418_, 0, v___y_412_);
lean_ctor_set(v___x_418_, 1, v___x_417_);
lean_inc(v___y_411_);
v___x_419_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_419_, 0, v___x_418_);
lean_ctor_set(v___x_419_, 1, v___y_411_);
lean_inc(v___y_413_);
v___x_420_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_420_, 0, v___x_419_);
lean_ctor_set(v___x_420_, 1, v___y_413_);
v___x_421_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__7));
v___x_422_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_422_, 0, v___x_420_);
lean_ctor_set(v___x_422_, 1, v___x_421_);
v___x_423_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_423_, 0, v___x_422_);
lean_ctor_set(v___x_423_, 1, v___x_327_);
v___x_424_ = lean_unsigned_to_nat(0u);
v___x_425_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_426_ = lean_int_dec_lt(v_m12_323_, v___x_425_);
if (v___x_426_ == 0)
{
lean_object* v___x_427_; lean_object* v___x_428_; 
v___x_427_ = l_Int_repr(v_m12_323_);
v___x_428_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_428_, 0, v___x_427_);
v___y_389_ = v___x_423_;
v___y_390_ = v___y_411_;
v___y_391_ = v___y_413_;
v___y_392_ = v___y_414_;
v___y_393_ = v___x_428_;
goto v___jp_388_;
}
else
{
lean_object* v___x_429_; lean_object* v___x_430_; lean_object* v___x_431_; 
v___x_429_ = l_Int_repr(v_m12_323_);
v___x_430_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_430_, 0, v___x_429_);
v___x_431_ = l_Repr_addAppParen(v___x_430_, v___x_424_);
v___y_389_ = v___x_423_;
v___y_390_ = v___y_411_;
v___y_391_ = v___y_413_;
v___y_392_ = v___y_414_;
v___y_393_ = v___x_431_;
goto v___jp_388_;
}
}
v___jp_432_:
{
lean_object* v___x_438_; lean_object* v___x_439_; lean_object* v___x_440_; lean_object* v___x_441_; lean_object* v___x_442_; lean_object* v___x_443_; lean_object* v___x_444_; lean_object* v___x_445_; lean_object* v___x_446_; lean_object* v___x_447_; uint8_t v___x_448_; 
v___x_438_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_438_, 0, v___x_329_);
lean_ctor_set(v___x_438_, 1, v___y_437_);
v___x_439_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_439_, 0, v___x_438_);
lean_ctor_set_uint8(v___x_439_, sizeof(void*)*1, v___y_436_);
v___x_440_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_440_, 0, v___y_434_);
lean_ctor_set(v___x_440_, 1, v___x_439_);
lean_inc(v___y_433_);
v___x_441_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_441_, 0, v___x_440_);
lean_ctor_set(v___x_441_, 1, v___y_433_);
lean_inc(v___y_435_);
v___x_442_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_442_, 0, v___x_441_);
lean_ctor_set(v___x_442_, 1, v___y_435_);
v___x_443_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14));
v___x_444_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_444_, 0, v___x_442_);
lean_ctor_set(v___x_444_, 1, v___x_443_);
v___x_445_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_445_, 0, v___x_444_);
lean_ctor_set(v___x_445_, 1, v___x_327_);
v___x_446_ = lean_unsigned_to_nat(0u);
v___x_447_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_448_ = lean_int_dec_lt(v_m11_322_, v___x_447_);
if (v___x_448_ == 0)
{
lean_object* v___x_449_; lean_object* v___x_450_; 
v___x_449_ = l_Int_repr(v_m11_322_);
v___x_450_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_450_, 0, v___x_449_);
v___y_411_ = v___y_433_;
v___y_412_ = v___x_445_;
v___y_413_ = v___y_435_;
v___y_414_ = v___y_436_;
v___y_415_ = v___x_450_;
goto v___jp_410_;
}
else
{
lean_object* v___x_451_; lean_object* v___x_452_; lean_object* v___x_453_; 
v___x_451_ = l_Int_repr(v_m11_322_);
v___x_452_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_452_, 0, v___x_451_);
v___x_453_ = l_Repr_addAppParen(v___x_452_, v___x_446_);
v___y_411_ = v___y_433_;
v___y_412_ = v___x_445_;
v___y_413_ = v___y_435_;
v___y_414_ = v___y_436_;
v___y_415_ = v___x_453_;
goto v___jp_410_;
}
}
v___jp_454_:
{
lean_object* v___x_460_; lean_object* v___x_461_; lean_object* v___x_462_; lean_object* v___x_463_; lean_object* v___x_464_; lean_object* v___x_465_; lean_object* v___x_466_; lean_object* v___x_467_; lean_object* v___x_468_; lean_object* v___x_469_; uint8_t v___x_470_; 
v___x_460_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_460_, 0, v___x_329_);
lean_ctor_set(v___x_460_, 1, v___y_459_);
v___x_461_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_461_, 0, v___x_460_);
lean_ctor_set_uint8(v___x_461_, sizeof(void*)*1, v___y_458_);
v___x_462_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_462_, 0, v___y_456_);
lean_ctor_set(v___x_462_, 1, v___x_461_);
lean_inc(v___y_455_);
v___x_463_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_463_, 0, v___x_462_);
lean_ctor_set(v___x_463_, 1, v___y_455_);
lean_inc(v___y_457_);
v___x_464_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_464_, 0, v___x_463_);
lean_ctor_set(v___x_464_, 1, v___y_457_);
v___x_465_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17));
v___x_466_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_466_, 0, v___x_464_);
lean_ctor_set(v___x_466_, 1, v___x_465_);
v___x_467_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_467_, 0, v___x_466_);
lean_ctor_set(v___x_467_, 1, v___x_327_);
v___x_468_ = lean_unsigned_to_nat(0u);
v___x_469_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_470_ = lean_int_dec_lt(v_m10_321_, v___x_469_);
if (v___x_470_ == 0)
{
lean_object* v___x_471_; lean_object* v___x_472_; 
v___x_471_ = l_Int_repr(v_m10_321_);
v___x_472_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_472_, 0, v___x_471_);
v___y_433_ = v___y_455_;
v___y_434_ = v___x_467_;
v___y_435_ = v___y_457_;
v___y_436_ = v___y_458_;
v___y_437_ = v___x_472_;
goto v___jp_432_;
}
else
{
lean_object* v___x_473_; lean_object* v___x_474_; lean_object* v___x_475_; 
v___x_473_ = l_Int_repr(v_m10_321_);
v___x_474_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_474_, 0, v___x_473_);
v___x_475_ = l_Repr_addAppParen(v___x_474_, v___x_468_);
v___y_433_ = v___y_455_;
v___y_434_ = v___x_467_;
v___y_435_ = v___y_457_;
v___y_436_ = v___y_458_;
v___y_437_ = v___x_475_;
goto v___jp_432_;
}
}
v___jp_476_:
{
lean_object* v___x_482_; lean_object* v___x_483_; lean_object* v___x_484_; lean_object* v___x_485_; lean_object* v___x_486_; lean_object* v___x_487_; lean_object* v___x_488_; lean_object* v___x_489_; lean_object* v___x_490_; lean_object* v___x_491_; uint8_t v___x_492_; 
v___x_482_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_482_, 0, v___x_329_);
lean_ctor_set(v___x_482_, 1, v___y_481_);
v___x_483_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_483_, 0, v___x_482_);
lean_ctor_set_uint8(v___x_483_, sizeof(void*)*1, v___y_480_);
v___x_484_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_484_, 0, v___y_477_);
lean_ctor_set(v___x_484_, 1, v___x_483_);
lean_inc(v___y_478_);
v___x_485_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_485_, 0, v___x_484_);
lean_ctor_set(v___x_485_, 1, v___y_478_);
lean_inc(v___y_479_);
v___x_486_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_486_, 0, v___x_485_);
lean_ctor_set(v___x_486_, 1, v___y_479_);
v___x_487_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__9));
v___x_488_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_488_, 0, v___x_486_);
lean_ctor_set(v___x_488_, 1, v___x_487_);
v___x_489_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_489_, 0, v___x_488_);
lean_ctor_set(v___x_489_, 1, v___x_327_);
v___x_490_ = lean_unsigned_to_nat(0u);
v___x_491_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_492_ = lean_int_dec_lt(v_m02_320_, v___x_491_);
if (v___x_492_ == 0)
{
lean_object* v___x_493_; lean_object* v___x_494_; 
v___x_493_ = l_Int_repr(v_m02_320_);
v___x_494_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_494_, 0, v___x_493_);
v___y_455_ = v___y_478_;
v___y_456_ = v___x_489_;
v___y_457_ = v___y_479_;
v___y_458_ = v___y_480_;
v___y_459_ = v___x_494_;
goto v___jp_454_;
}
else
{
lean_object* v___x_495_; lean_object* v___x_496_; lean_object* v___x_497_; 
v___x_495_ = l_Int_repr(v_m02_320_);
v___x_496_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_496_, 0, v___x_495_);
v___x_497_ = l_Repr_addAppParen(v___x_496_, v___x_490_);
v___y_455_ = v___y_478_;
v___y_456_ = v___x_489_;
v___y_457_ = v___y_479_;
v___y_458_ = v___y_480_;
v___y_459_ = v___x_497_;
goto v___jp_454_;
}
}
v___jp_498_:
{
lean_object* v___x_500_; uint8_t v___x_501_; lean_object* v___x_502_; lean_object* v___x_503_; lean_object* v___x_504_; lean_object* v___x_505_; lean_object* v___x_506_; lean_object* v___x_507_; lean_object* v___x_508_; lean_object* v___x_509_; lean_object* v___x_510_; lean_object* v___x_511_; lean_object* v___x_512_; uint8_t v___x_513_; 
v___x_500_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_500_, 0, v___x_329_);
lean_ctor_set(v___x_500_, 1, v___y_499_);
v___x_501_ = 0;
v___x_502_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_502_, 0, v___x_500_);
lean_ctor_set_uint8(v___x_502_, sizeof(void*)*1, v___x_501_);
v___x_503_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_503_, 0, v___x_328_);
lean_ctor_set(v___x_503_, 1, v___x_502_);
v___x_504_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19));
v___x_505_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_505_, 0, v___x_503_);
lean_ctor_set(v___x_505_, 1, v___x_504_);
v___x_506_ = lean_box(1);
v___x_507_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_507_, 0, v___x_505_);
lean_ctor_set(v___x_507_, 1, v___x_506_);
v___x_508_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21));
v___x_509_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_509_, 0, v___x_507_);
lean_ctor_set(v___x_509_, 1, v___x_508_);
v___x_510_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_510_, 0, v___x_509_);
lean_ctor_set(v___x_510_, 1, v___x_327_);
v___x_511_ = lean_unsigned_to_nat(0u);
v___x_512_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_513_ = lean_int_dec_lt(v_m01_319_, v___x_512_);
if (v___x_513_ == 0)
{
lean_object* v___x_514_; lean_object* v___x_515_; 
v___x_514_ = l_Int_repr(v_m01_319_);
v___x_515_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_515_, 0, v___x_514_);
v___y_477_ = v___x_510_;
v___y_478_ = v___x_504_;
v___y_479_ = v___x_506_;
v___y_480_ = v___x_501_;
v___y_481_ = v___x_515_;
goto v___jp_476_;
}
else
{
lean_object* v___x_516_; lean_object* v___x_517_; lean_object* v___x_518_; 
v___x_516_ = l_Int_repr(v_m01_319_);
v___x_517_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_517_, 0, v___x_516_);
v___x_518_ = l_Repr_addAppParen(v___x_517_, v___x_511_);
v___y_477_ = v___x_510_;
v___y_478_ = v___x_504_;
v___y_479_ = v___x_506_;
v___y_480_ = v___x_501_;
v___y_481_ = v___x_518_;
goto v___jp_476_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___boxed(lean_object* v_x_527_){
_start:
{
lean_object* v_res_528_; 
v_res_528_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg(v_x_527_);
lean_dec_ref(v_x_527_);
return v_res_528_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr(lean_object* v_x_529_, lean_object* v_prec_530_){
_start:
{
lean_object* v___x_531_; 
v___x_531_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg(v_x_529_);
return v___x_531_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___boxed(lean_object* v_x_532_, lean_object* v_prec_533_){
_start:
{
lean_object* v_res_534_; 
v_res_534_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr(v_x_532_, v_prec_533_);
lean_dec(v_prec_533_);
lean_dec_ref(v_x_532_);
return v_res_534_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr3(lean_object* v_A_537_){
_start:
{
lean_object* v_m00_538_; lean_object* v_m11_539_; lean_object* v_m22_540_; lean_object* v___x_541_; lean_object* v___x_542_; 
v_m00_538_ = lean_ctor_get(v_A_537_, 0);
v_m11_539_ = lean_ctor_get(v_A_537_, 4);
v_m22_540_ = lean_ctor_get(v_A_537_, 8);
v___x_541_ = lean_int_add(v_m00_538_, v_m11_539_);
v___x_542_ = lean_int_add(v___x_541_, v_m22_540_);
lean_dec(v___x_541_);
return v___x_542_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr3___boxed(lean_object* v_A_543_){
_start:
{
lean_object* v_res_544_; 
v_res_544_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_tr3(v_A_543_);
lean_dec_ref(v_A_543_);
return v_res_544_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3(lean_object* v_A_545_, lean_object* v_B_546_){
_start:
{
lean_object* v_m00_547_; lean_object* v_m01_548_; lean_object* v_m02_549_; lean_object* v_m10_550_; lean_object* v_m11_551_; lean_object* v_m12_552_; lean_object* v_m20_553_; lean_object* v_m21_554_; lean_object* v_m22_555_; lean_object* v_m00_556_; lean_object* v_m01_557_; lean_object* v_m02_558_; lean_object* v_m10_559_; lean_object* v_m11_560_; lean_object* v_m12_561_; lean_object* v_m20_562_; lean_object* v_m21_563_; lean_object* v_m22_564_; lean_object* v___x_566_; uint8_t v_isShared_567_; uint8_t v_isSharedCheck_616_; 
v_m00_547_ = lean_ctor_get(v_A_545_, 0);
v_m01_548_ = lean_ctor_get(v_A_545_, 1);
v_m02_549_ = lean_ctor_get(v_A_545_, 2);
v_m10_550_ = lean_ctor_get(v_A_545_, 3);
v_m11_551_ = lean_ctor_get(v_A_545_, 4);
v_m12_552_ = lean_ctor_get(v_A_545_, 5);
v_m20_553_ = lean_ctor_get(v_A_545_, 6);
v_m21_554_ = lean_ctor_get(v_A_545_, 7);
v_m22_555_ = lean_ctor_get(v_A_545_, 8);
v_m00_556_ = lean_ctor_get(v_B_546_, 0);
v_m01_557_ = lean_ctor_get(v_B_546_, 1);
v_m02_558_ = lean_ctor_get(v_B_546_, 2);
v_m10_559_ = lean_ctor_get(v_B_546_, 3);
v_m11_560_ = lean_ctor_get(v_B_546_, 4);
v_m12_561_ = lean_ctor_get(v_B_546_, 5);
v_m20_562_ = lean_ctor_get(v_B_546_, 6);
v_m21_563_ = lean_ctor_get(v_B_546_, 7);
v_m22_564_ = lean_ctor_get(v_B_546_, 8);
v_isSharedCheck_616_ = !lean_is_exclusive(v_B_546_);
if (v_isSharedCheck_616_ == 0)
{
v___x_566_ = v_B_546_;
v_isShared_567_ = v_isSharedCheck_616_;
goto v_resetjp_565_;
}
else
{
lean_inc(v_m22_564_);
lean_inc(v_m21_563_);
lean_inc(v_m20_562_);
lean_inc(v_m12_561_);
lean_inc(v_m11_560_);
lean_inc(v_m10_559_);
lean_inc(v_m02_558_);
lean_inc(v_m01_557_);
lean_inc(v_m00_556_);
lean_dec(v_B_546_);
v___x_566_ = lean_box(0);
v_isShared_567_ = v_isSharedCheck_616_;
goto v_resetjp_565_;
}
v_resetjp_565_:
{
lean_object* v___x_568_; lean_object* v___x_569_; lean_object* v___x_570_; lean_object* v___x_571_; lean_object* v___x_572_; lean_object* v___x_573_; lean_object* v___x_574_; lean_object* v___x_575_; lean_object* v___x_576_; lean_object* v___x_577_; lean_object* v___x_578_; lean_object* v___x_579_; lean_object* v___x_580_; lean_object* v___x_581_; lean_object* v___x_582_; lean_object* v___x_583_; lean_object* v___x_584_; lean_object* v___x_585_; lean_object* v___x_586_; lean_object* v___x_587_; lean_object* v___x_588_; lean_object* v___x_589_; lean_object* v___x_590_; lean_object* v___x_591_; lean_object* v___x_592_; lean_object* v___x_593_; lean_object* v___x_594_; lean_object* v___x_595_; lean_object* v___x_596_; lean_object* v___x_597_; lean_object* v___x_598_; lean_object* v___x_599_; lean_object* v___x_600_; lean_object* v___x_601_; lean_object* v___x_602_; lean_object* v___x_603_; lean_object* v___x_604_; lean_object* v___x_605_; lean_object* v___x_606_; lean_object* v___x_607_; lean_object* v___x_608_; lean_object* v___x_609_; lean_object* v___x_610_; lean_object* v___x_611_; lean_object* v___x_612_; lean_object* v___x_614_; 
v___x_568_ = lean_int_mul(v_m00_547_, v_m00_556_);
v___x_569_ = lean_int_mul(v_m01_548_, v_m10_559_);
v___x_570_ = lean_int_add(v___x_568_, v___x_569_);
lean_dec(v___x_569_);
lean_dec(v___x_568_);
v___x_571_ = lean_int_mul(v_m02_549_, v_m20_562_);
v___x_572_ = lean_int_add(v___x_570_, v___x_571_);
lean_dec(v___x_571_);
lean_dec(v___x_570_);
v___x_573_ = lean_int_mul(v_m00_547_, v_m01_557_);
v___x_574_ = lean_int_mul(v_m01_548_, v_m11_560_);
v___x_575_ = lean_int_add(v___x_573_, v___x_574_);
lean_dec(v___x_574_);
lean_dec(v___x_573_);
v___x_576_ = lean_int_mul(v_m02_549_, v_m21_563_);
v___x_577_ = lean_int_add(v___x_575_, v___x_576_);
lean_dec(v___x_576_);
lean_dec(v___x_575_);
v___x_578_ = lean_int_mul(v_m00_547_, v_m02_558_);
v___x_579_ = lean_int_mul(v_m01_548_, v_m12_561_);
v___x_580_ = lean_int_add(v___x_578_, v___x_579_);
lean_dec(v___x_579_);
lean_dec(v___x_578_);
v___x_581_ = lean_int_mul(v_m02_549_, v_m22_564_);
v___x_582_ = lean_int_add(v___x_580_, v___x_581_);
lean_dec(v___x_581_);
lean_dec(v___x_580_);
v___x_583_ = lean_int_mul(v_m10_550_, v_m00_556_);
v___x_584_ = lean_int_mul(v_m11_551_, v_m10_559_);
v___x_585_ = lean_int_add(v___x_583_, v___x_584_);
lean_dec(v___x_584_);
lean_dec(v___x_583_);
v___x_586_ = lean_int_mul(v_m12_552_, v_m20_562_);
v___x_587_ = lean_int_add(v___x_585_, v___x_586_);
lean_dec(v___x_586_);
lean_dec(v___x_585_);
v___x_588_ = lean_int_mul(v_m10_550_, v_m01_557_);
v___x_589_ = lean_int_mul(v_m11_551_, v_m11_560_);
v___x_590_ = lean_int_add(v___x_588_, v___x_589_);
lean_dec(v___x_589_);
lean_dec(v___x_588_);
v___x_591_ = lean_int_mul(v_m12_552_, v_m21_563_);
v___x_592_ = lean_int_add(v___x_590_, v___x_591_);
lean_dec(v___x_591_);
lean_dec(v___x_590_);
v___x_593_ = lean_int_mul(v_m10_550_, v_m02_558_);
v___x_594_ = lean_int_mul(v_m11_551_, v_m12_561_);
v___x_595_ = lean_int_add(v___x_593_, v___x_594_);
lean_dec(v___x_594_);
lean_dec(v___x_593_);
v___x_596_ = lean_int_mul(v_m12_552_, v_m22_564_);
v___x_597_ = lean_int_add(v___x_595_, v___x_596_);
lean_dec(v___x_596_);
lean_dec(v___x_595_);
v___x_598_ = lean_int_mul(v_m20_553_, v_m00_556_);
lean_dec(v_m00_556_);
v___x_599_ = lean_int_mul(v_m21_554_, v_m10_559_);
lean_dec(v_m10_559_);
v___x_600_ = lean_int_add(v___x_598_, v___x_599_);
lean_dec(v___x_599_);
lean_dec(v___x_598_);
v___x_601_ = lean_int_mul(v_m22_555_, v_m20_562_);
lean_dec(v_m20_562_);
v___x_602_ = lean_int_add(v___x_600_, v___x_601_);
lean_dec(v___x_601_);
lean_dec(v___x_600_);
v___x_603_ = lean_int_mul(v_m20_553_, v_m01_557_);
lean_dec(v_m01_557_);
v___x_604_ = lean_int_mul(v_m21_554_, v_m11_560_);
lean_dec(v_m11_560_);
v___x_605_ = lean_int_add(v___x_603_, v___x_604_);
lean_dec(v___x_604_);
lean_dec(v___x_603_);
v___x_606_ = lean_int_mul(v_m22_555_, v_m21_563_);
lean_dec(v_m21_563_);
v___x_607_ = lean_int_add(v___x_605_, v___x_606_);
lean_dec(v___x_606_);
lean_dec(v___x_605_);
v___x_608_ = lean_int_mul(v_m20_553_, v_m02_558_);
lean_dec(v_m02_558_);
v___x_609_ = lean_int_mul(v_m21_554_, v_m12_561_);
lean_dec(v_m12_561_);
v___x_610_ = lean_int_add(v___x_608_, v___x_609_);
lean_dec(v___x_609_);
lean_dec(v___x_608_);
v___x_611_ = lean_int_mul(v_m22_555_, v_m22_564_);
lean_dec(v_m22_564_);
v___x_612_ = lean_int_add(v___x_610_, v___x_611_);
lean_dec(v___x_611_);
lean_dec(v___x_610_);
if (v_isShared_567_ == 0)
{
lean_ctor_set(v___x_566_, 8, v___x_612_);
lean_ctor_set(v___x_566_, 7, v___x_607_);
lean_ctor_set(v___x_566_, 6, v___x_602_);
lean_ctor_set(v___x_566_, 5, v___x_597_);
lean_ctor_set(v___x_566_, 4, v___x_592_);
lean_ctor_set(v___x_566_, 3, v___x_587_);
lean_ctor_set(v___x_566_, 2, v___x_582_);
lean_ctor_set(v___x_566_, 1, v___x_577_);
lean_ctor_set(v___x_566_, 0, v___x_572_);
v___x_614_ = v___x_566_;
goto v_reusejp_613_;
}
else
{
lean_object* v_reuseFailAlloc_615_; 
v_reuseFailAlloc_615_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_615_, 0, v___x_572_);
lean_ctor_set(v_reuseFailAlloc_615_, 1, v___x_577_);
lean_ctor_set(v_reuseFailAlloc_615_, 2, v___x_582_);
lean_ctor_set(v_reuseFailAlloc_615_, 3, v___x_587_);
lean_ctor_set(v_reuseFailAlloc_615_, 4, v___x_592_);
lean_ctor_set(v_reuseFailAlloc_615_, 5, v___x_597_);
lean_ctor_set(v_reuseFailAlloc_615_, 6, v___x_602_);
lean_ctor_set(v_reuseFailAlloc_615_, 7, v___x_607_);
lean_ctor_set(v_reuseFailAlloc_615_, 8, v___x_612_);
v___x_614_ = v_reuseFailAlloc_615_;
goto v_reusejp_613_;
}
v_reusejp_613_:
{
return v___x_614_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3___boxed(lean_object* v_A_617_, lean_object* v_B_618_){
_start:
{
lean_object* v_res_619_; 
v_res_619_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3(v_A_617_, v_B_618_);
lean_dec_ref(v_A_617_);
return v_res_619_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub3(lean_object* v_A_620_, lean_object* v_B_621_){
_start:
{
lean_object* v_m00_622_; lean_object* v_m01_623_; lean_object* v_m02_624_; lean_object* v_m10_625_; lean_object* v_m11_626_; lean_object* v_m12_627_; lean_object* v_m20_628_; lean_object* v_m21_629_; lean_object* v_m22_630_; lean_object* v_m00_631_; lean_object* v_m01_632_; lean_object* v_m02_633_; lean_object* v_m10_634_; lean_object* v_m11_635_; lean_object* v_m12_636_; lean_object* v_m20_637_; lean_object* v_m21_638_; lean_object* v_m22_639_; lean_object* v___x_641_; uint8_t v_isShared_642_; uint8_t v_isSharedCheck_655_; 
v_m00_622_ = lean_ctor_get(v_A_620_, 0);
v_m01_623_ = lean_ctor_get(v_A_620_, 1);
v_m02_624_ = lean_ctor_get(v_A_620_, 2);
v_m10_625_ = lean_ctor_get(v_A_620_, 3);
v_m11_626_ = lean_ctor_get(v_A_620_, 4);
v_m12_627_ = lean_ctor_get(v_A_620_, 5);
v_m20_628_ = lean_ctor_get(v_A_620_, 6);
v_m21_629_ = lean_ctor_get(v_A_620_, 7);
v_m22_630_ = lean_ctor_get(v_A_620_, 8);
v_m00_631_ = lean_ctor_get(v_B_621_, 0);
v_m01_632_ = lean_ctor_get(v_B_621_, 1);
v_m02_633_ = lean_ctor_get(v_B_621_, 2);
v_m10_634_ = lean_ctor_get(v_B_621_, 3);
v_m11_635_ = lean_ctor_get(v_B_621_, 4);
v_m12_636_ = lean_ctor_get(v_B_621_, 5);
v_m20_637_ = lean_ctor_get(v_B_621_, 6);
v_m21_638_ = lean_ctor_get(v_B_621_, 7);
v_m22_639_ = lean_ctor_get(v_B_621_, 8);
v_isSharedCheck_655_ = !lean_is_exclusive(v_B_621_);
if (v_isSharedCheck_655_ == 0)
{
v___x_641_ = v_B_621_;
v_isShared_642_ = v_isSharedCheck_655_;
goto v_resetjp_640_;
}
else
{
lean_inc(v_m22_639_);
lean_inc(v_m21_638_);
lean_inc(v_m20_637_);
lean_inc(v_m12_636_);
lean_inc(v_m11_635_);
lean_inc(v_m10_634_);
lean_inc(v_m02_633_);
lean_inc(v_m01_632_);
lean_inc(v_m00_631_);
lean_dec(v_B_621_);
v___x_641_ = lean_box(0);
v_isShared_642_ = v_isSharedCheck_655_;
goto v_resetjp_640_;
}
v_resetjp_640_:
{
lean_object* v___x_643_; lean_object* v___x_644_; lean_object* v___x_645_; lean_object* v___x_646_; lean_object* v___x_647_; lean_object* v___x_648_; lean_object* v___x_649_; lean_object* v___x_650_; lean_object* v___x_651_; lean_object* v___x_653_; 
v___x_643_ = lean_int_sub(v_m00_622_, v_m00_631_);
lean_dec(v_m00_631_);
v___x_644_ = lean_int_sub(v_m01_623_, v_m01_632_);
lean_dec(v_m01_632_);
v___x_645_ = lean_int_sub(v_m02_624_, v_m02_633_);
lean_dec(v_m02_633_);
v___x_646_ = lean_int_sub(v_m10_625_, v_m10_634_);
lean_dec(v_m10_634_);
v___x_647_ = lean_int_sub(v_m11_626_, v_m11_635_);
lean_dec(v_m11_635_);
v___x_648_ = lean_int_sub(v_m12_627_, v_m12_636_);
lean_dec(v_m12_636_);
v___x_649_ = lean_int_sub(v_m20_628_, v_m20_637_);
lean_dec(v_m20_637_);
v___x_650_ = lean_int_sub(v_m21_629_, v_m21_638_);
lean_dec(v_m21_638_);
v___x_651_ = lean_int_sub(v_m22_630_, v_m22_639_);
lean_dec(v_m22_639_);
if (v_isShared_642_ == 0)
{
lean_ctor_set(v___x_641_, 8, v___x_651_);
lean_ctor_set(v___x_641_, 7, v___x_650_);
lean_ctor_set(v___x_641_, 6, v___x_649_);
lean_ctor_set(v___x_641_, 5, v___x_648_);
lean_ctor_set(v___x_641_, 4, v___x_647_);
lean_ctor_set(v___x_641_, 3, v___x_646_);
lean_ctor_set(v___x_641_, 2, v___x_645_);
lean_ctor_set(v___x_641_, 1, v___x_644_);
lean_ctor_set(v___x_641_, 0, v___x_643_);
v___x_653_ = v___x_641_;
goto v_reusejp_652_;
}
else
{
lean_object* v_reuseFailAlloc_654_; 
v_reuseFailAlloc_654_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_654_, 0, v___x_643_);
lean_ctor_set(v_reuseFailAlloc_654_, 1, v___x_644_);
lean_ctor_set(v_reuseFailAlloc_654_, 2, v___x_645_);
lean_ctor_set(v_reuseFailAlloc_654_, 3, v___x_646_);
lean_ctor_set(v_reuseFailAlloc_654_, 4, v___x_647_);
lean_ctor_set(v_reuseFailAlloc_654_, 5, v___x_648_);
lean_ctor_set(v_reuseFailAlloc_654_, 6, v___x_649_);
lean_ctor_set(v_reuseFailAlloc_654_, 7, v___x_650_);
lean_ctor_set(v_reuseFailAlloc_654_, 8, v___x_651_);
v___x_653_ = v_reuseFailAlloc_654_;
goto v_reusejp_652_;
}
v_reusejp_652_:
{
return v___x_653_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub3___boxed(lean_object* v_A_656_, lean_object* v_B_657_){
_start:
{
lean_object* v_res_658_; 
v_res_658_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub3(v_A_656_, v_B_657_);
lean_dec_ref(v_A_656_);
return v_res_658_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3(lean_object* v_c_659_, lean_object* v_A_660_){
_start:
{
lean_object* v_m00_661_; lean_object* v_m01_662_; lean_object* v_m02_663_; lean_object* v_m10_664_; lean_object* v_m11_665_; lean_object* v_m12_666_; lean_object* v_m20_667_; lean_object* v_m21_668_; lean_object* v_m22_669_; lean_object* v___x_671_; uint8_t v_isShared_672_; uint8_t v_isSharedCheck_685_; 
v_m00_661_ = lean_ctor_get(v_A_660_, 0);
v_m01_662_ = lean_ctor_get(v_A_660_, 1);
v_m02_663_ = lean_ctor_get(v_A_660_, 2);
v_m10_664_ = lean_ctor_get(v_A_660_, 3);
v_m11_665_ = lean_ctor_get(v_A_660_, 4);
v_m12_666_ = lean_ctor_get(v_A_660_, 5);
v_m20_667_ = lean_ctor_get(v_A_660_, 6);
v_m21_668_ = lean_ctor_get(v_A_660_, 7);
v_m22_669_ = lean_ctor_get(v_A_660_, 8);
v_isSharedCheck_685_ = !lean_is_exclusive(v_A_660_);
if (v_isSharedCheck_685_ == 0)
{
v___x_671_ = v_A_660_;
v_isShared_672_ = v_isSharedCheck_685_;
goto v_resetjp_670_;
}
else
{
lean_inc(v_m22_669_);
lean_inc(v_m21_668_);
lean_inc(v_m20_667_);
lean_inc(v_m12_666_);
lean_inc(v_m11_665_);
lean_inc(v_m10_664_);
lean_inc(v_m02_663_);
lean_inc(v_m01_662_);
lean_inc(v_m00_661_);
lean_dec(v_A_660_);
v___x_671_ = lean_box(0);
v_isShared_672_ = v_isSharedCheck_685_;
goto v_resetjp_670_;
}
v_resetjp_670_:
{
lean_object* v___x_673_; lean_object* v___x_674_; lean_object* v___x_675_; lean_object* v___x_676_; lean_object* v___x_677_; lean_object* v___x_678_; lean_object* v___x_679_; lean_object* v___x_680_; lean_object* v___x_681_; lean_object* v___x_683_; 
v___x_673_ = lean_int_mul(v_c_659_, v_m00_661_);
lean_dec(v_m00_661_);
v___x_674_ = lean_int_mul(v_c_659_, v_m01_662_);
lean_dec(v_m01_662_);
v___x_675_ = lean_int_mul(v_c_659_, v_m02_663_);
lean_dec(v_m02_663_);
v___x_676_ = lean_int_mul(v_c_659_, v_m10_664_);
lean_dec(v_m10_664_);
v___x_677_ = lean_int_mul(v_c_659_, v_m11_665_);
lean_dec(v_m11_665_);
v___x_678_ = lean_int_mul(v_c_659_, v_m12_666_);
lean_dec(v_m12_666_);
v___x_679_ = lean_int_mul(v_c_659_, v_m20_667_);
lean_dec(v_m20_667_);
v___x_680_ = lean_int_mul(v_c_659_, v_m21_668_);
lean_dec(v_m21_668_);
v___x_681_ = lean_int_mul(v_c_659_, v_m22_669_);
lean_dec(v_m22_669_);
if (v_isShared_672_ == 0)
{
lean_ctor_set(v___x_671_, 8, v___x_681_);
lean_ctor_set(v___x_671_, 7, v___x_680_);
lean_ctor_set(v___x_671_, 6, v___x_679_);
lean_ctor_set(v___x_671_, 5, v___x_678_);
lean_ctor_set(v___x_671_, 4, v___x_677_);
lean_ctor_set(v___x_671_, 3, v___x_676_);
lean_ctor_set(v___x_671_, 2, v___x_675_);
lean_ctor_set(v___x_671_, 1, v___x_674_);
lean_ctor_set(v___x_671_, 0, v___x_673_);
v___x_683_ = v___x_671_;
goto v_reusejp_682_;
}
else
{
lean_object* v_reuseFailAlloc_684_; 
v_reuseFailAlloc_684_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_684_, 0, v___x_673_);
lean_ctor_set(v_reuseFailAlloc_684_, 1, v___x_674_);
lean_ctor_set(v_reuseFailAlloc_684_, 2, v___x_675_);
lean_ctor_set(v_reuseFailAlloc_684_, 3, v___x_676_);
lean_ctor_set(v_reuseFailAlloc_684_, 4, v___x_677_);
lean_ctor_set(v_reuseFailAlloc_684_, 5, v___x_678_);
lean_ctor_set(v_reuseFailAlloc_684_, 6, v___x_679_);
lean_ctor_set(v_reuseFailAlloc_684_, 7, v___x_680_);
lean_ctor_set(v_reuseFailAlloc_684_, 8, v___x_681_);
v___x_683_ = v_reuseFailAlloc_684_;
goto v_reusejp_682_;
}
v_reusejp_682_:
{
return v___x_683_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3___boxed(lean_object* v_c_686_, lean_object* v_A_687_){
_start:
{
lean_object* v_res_688_; 
v_res_688_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3(v_c_686_, v_A_687_);
lean_dec(v_c_686_);
return v_res_688_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm3(lean_object* v_A_689_, lean_object* v_B_690_){
_start:
{
lean_object* v___x_691_; lean_object* v___x_692_; lean_object* v___x_693_; 
lean_inc_ref(v_B_690_);
v___x_691_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3(v_A_689_, v_B_690_);
v___x_692_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3(v_B_690_, v_A_689_);
lean_dec_ref(v_B_690_);
v___x_693_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_sub3(v___x_691_, v___x_692_);
lean_dec_ref(v___x_691_);
return v___x_693_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3___closed__0(void){
_start:
{
lean_object* v___x_694_; lean_object* v___x_695_; lean_object* v___x_696_; 
v___x_694_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_695_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_696_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_696_, 0, v___x_695_);
lean_ctor_set(v___x_696_, 1, v___x_694_);
lean_ctor_set(v___x_696_, 2, v___x_694_);
lean_ctor_set(v___x_696_, 3, v___x_694_);
lean_ctor_set(v___x_696_, 4, v___x_695_);
lean_ctor_set(v___x_696_, 5, v___x_694_);
lean_ctor_set(v___x_696_, 6, v___x_694_);
lean_ctor_set(v___x_696_, 7, v___x_694_);
lean_ctor_set(v___x_696_, 8, v___x_695_);
return v___x_696_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3(void){
_start:
{
lean_object* v___x_697_; 
v___x_697_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3___closed__0);
return v___x_697_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2_decEq(lean_object* v_x_698_, lean_object* v_x_699_){
_start:
{
uint8_t v_m00_700_; uint8_t v_m01_701_; uint8_t v_m10_702_; uint8_t v_m11_703_; uint8_t v_m00_704_; uint8_t v_m01_705_; uint8_t v_m10_706_; uint8_t v_m11_707_; 
v_m00_700_ = lean_ctor_get_uint8(v_x_698_, 0);
v_m01_701_ = lean_ctor_get_uint8(v_x_698_, 1);
v_m10_702_ = lean_ctor_get_uint8(v_x_698_, 2);
v_m11_703_ = lean_ctor_get_uint8(v_x_698_, 3);
v_m00_704_ = lean_ctor_get_uint8(v_x_699_, 0);
v_m01_705_ = lean_ctor_get_uint8(v_x_699_, 1);
v_m10_706_ = lean_ctor_get_uint8(v_x_699_, 2);
v_m11_707_ = lean_ctor_get_uint8(v_x_699_, 3);
if (v_m00_700_ == 0)
{
if (v_m00_704_ == 0)
{
goto v___jp_711_;
}
else
{
return v_m00_700_;
}
}
else
{
if (v_m00_704_ == 0)
{
return v_m00_704_;
}
else
{
goto v___jp_711_;
}
}
v___jp_708_:
{
if (v_m11_703_ == 0)
{
if (v_m11_707_ == 0)
{
uint8_t v___x_709_; 
v___x_709_ = 1;
return v___x_709_;
}
else
{
return v_m11_703_;
}
}
else
{
return v_m11_707_;
}
}
v___jp_710_:
{
if (v_m10_702_ == 0)
{
if (v_m10_706_ == 0)
{
goto v___jp_708_;
}
else
{
return v_m10_702_;
}
}
else
{
if (v_m10_706_ == 0)
{
return v_m10_706_;
}
else
{
goto v___jp_708_;
}
}
}
v___jp_711_:
{
if (v_m01_701_ == 0)
{
if (v_m01_705_ == 0)
{
goto v___jp_710_;
}
else
{
return v_m01_701_;
}
}
else
{
if (v_m01_705_ == 0)
{
return v_m01_705_;
}
else
{
goto v___jp_710_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2_decEq___boxed(lean_object* v_x_712_, lean_object* v_x_713_){
_start:
{
uint8_t v_res_714_; lean_object* v_r_715_; 
v_res_714_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2_decEq(v_x_712_, v_x_713_);
lean_dec_ref(v_x_713_);
lean_dec_ref(v_x_712_);
v_r_715_ = lean_box(v_res_714_);
return v_r_715_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2(lean_object* v_x_716_, lean_object* v_x_717_){
_start:
{
uint8_t v___x_718_; 
v___x_718_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2_decEq(v_x_716_, v_x_717_);
return v___x_718_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2___boxed(lean_object* v_x_719_, lean_object* v_x_720_){
_start:
{
uint8_t v_res_721_; lean_object* v_r_722_; 
v_res_721_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat2Z2(v_x_719_, v_x_720_);
lean_dec_ref(v_x_720_);
lean_dec_ref(v_x_719_);
v_r_722_ = lean_box(v_res_721_);
return v_r_722_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___redArg(lean_object* v_x_723_){
_start:
{
uint8_t v_m00_724_; uint8_t v_m01_725_; uint8_t v_m10_726_; uint8_t v_m11_727_; lean_object* v___x_728_; lean_object* v___x_729_; lean_object* v___x_730_; lean_object* v___x_731_; lean_object* v___x_732_; uint8_t v___x_733_; lean_object* v___x_734_; lean_object* v___x_735_; lean_object* v___x_736_; lean_object* v___x_737_; lean_object* v___x_738_; lean_object* v___x_739_; lean_object* v___x_740_; lean_object* v___x_741_; lean_object* v___x_742_; lean_object* v___x_743_; lean_object* v___x_744_; lean_object* v___x_745_; lean_object* v___x_746_; lean_object* v___x_747_; lean_object* v___x_748_; lean_object* v___x_749_; lean_object* v___x_750_; lean_object* v___x_751_; lean_object* v___x_752_; lean_object* v___x_753_; lean_object* v___x_754_; lean_object* v___x_755_; lean_object* v___x_756_; lean_object* v___x_757_; lean_object* v___x_758_; lean_object* v___x_759_; lean_object* v___x_760_; lean_object* v___x_761_; lean_object* v___x_762_; lean_object* v___x_763_; lean_object* v___x_764_; lean_object* v___x_765_; lean_object* v___x_766_; lean_object* v___x_767_; lean_object* v___x_768_; lean_object* v___x_769_; lean_object* v___x_770_; lean_object* v___x_771_; 
v_m00_724_ = lean_ctor_get_uint8(v_x_723_, 0);
v_m01_725_ = lean_ctor_get_uint8(v_x_723_, 1);
v_m10_726_ = lean_ctor_get_uint8(v_x_723_, 2);
v_m11_727_ = lean_ctor_get_uint8(v_x_723_, 3);
v___x_728_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5));
v___x_729_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6));
v___x_730_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7);
v___x_731_ = l_Bool_repr___redArg(v_m00_724_);
v___x_732_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_732_, 0, v___x_730_);
lean_ctor_set(v___x_732_, 1, v___x_731_);
v___x_733_ = 0;
v___x_734_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_734_, 0, v___x_732_);
lean_ctor_set_uint8(v___x_734_, sizeof(void*)*1, v___x_733_);
v___x_735_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_735_, 0, v___x_729_);
lean_ctor_set(v___x_735_, 1, v___x_734_);
v___x_736_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19));
v___x_737_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_737_, 0, v___x_735_);
lean_ctor_set(v___x_737_, 1, v___x_736_);
v___x_738_ = lean_box(1);
v___x_739_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_739_, 0, v___x_737_);
lean_ctor_set(v___x_739_, 1, v___x_738_);
v___x_740_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21));
v___x_741_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_741_, 0, v___x_739_);
lean_ctor_set(v___x_741_, 1, v___x_740_);
v___x_742_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_742_, 0, v___x_741_);
lean_ctor_set(v___x_742_, 1, v___x_728_);
v___x_743_ = l_Bool_repr___redArg(v_m01_725_);
v___x_744_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_744_, 0, v___x_730_);
lean_ctor_set(v___x_744_, 1, v___x_743_);
v___x_745_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_745_, 0, v___x_744_);
lean_ctor_set_uint8(v___x_745_, sizeof(void*)*1, v___x_733_);
v___x_746_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_746_, 0, v___x_742_);
lean_ctor_set(v___x_746_, 1, v___x_745_);
v___x_747_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_747_, 0, v___x_746_);
lean_ctor_set(v___x_747_, 1, v___x_736_);
v___x_748_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_748_, 0, v___x_747_);
lean_ctor_set(v___x_748_, 1, v___x_738_);
v___x_749_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17));
v___x_750_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_750_, 0, v___x_748_);
lean_ctor_set(v___x_750_, 1, v___x_749_);
v___x_751_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_751_, 0, v___x_750_);
lean_ctor_set(v___x_751_, 1, v___x_728_);
v___x_752_ = l_Bool_repr___redArg(v_m10_726_);
v___x_753_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_753_, 0, v___x_730_);
lean_ctor_set(v___x_753_, 1, v___x_752_);
v___x_754_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_754_, 0, v___x_753_);
lean_ctor_set_uint8(v___x_754_, sizeof(void*)*1, v___x_733_);
v___x_755_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_755_, 0, v___x_751_);
lean_ctor_set(v___x_755_, 1, v___x_754_);
v___x_756_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_756_, 0, v___x_755_);
lean_ctor_set(v___x_756_, 1, v___x_736_);
v___x_757_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_757_, 0, v___x_756_);
lean_ctor_set(v___x_757_, 1, v___x_738_);
v___x_758_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14));
v___x_759_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_759_, 0, v___x_757_);
lean_ctor_set(v___x_759_, 1, v___x_758_);
v___x_760_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_760_, 0, v___x_759_);
lean_ctor_set(v___x_760_, 1, v___x_728_);
v___x_761_ = l_Bool_repr___redArg(v_m11_727_);
v___x_762_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_762_, 0, v___x_730_);
lean_ctor_set(v___x_762_, 1, v___x_761_);
v___x_763_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_763_, 0, v___x_762_);
lean_ctor_set_uint8(v___x_763_, sizeof(void*)*1, v___x_733_);
v___x_764_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_764_, 0, v___x_760_);
lean_ctor_set(v___x_764_, 1, v___x_763_);
v___x_765_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10);
v___x_766_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11));
v___x_767_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_767_, 0, v___x_766_);
lean_ctor_set(v___x_767_, 1, v___x_764_);
v___x_768_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12));
v___x_769_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_769_, 0, v___x_767_);
lean_ctor_set(v___x_769_, 1, v___x_768_);
v___x_770_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_770_, 0, v___x_765_);
lean_ctor_set(v___x_770_, 1, v___x_769_);
v___x_771_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_771_, 0, v___x_770_);
lean_ctor_set_uint8(v___x_771_, sizeof(void*)*1, v___x_733_);
return v___x_771_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___redArg___boxed(lean_object* v_x_772_){
_start:
{
lean_object* v_res_773_; 
v_res_773_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___redArg(v_x_772_);
lean_dec_ref(v_x_772_);
return v_res_773_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr(lean_object* v_x_774_, lean_object* v_prec_775_){
_start:
{
lean_object* v___x_776_; 
v___x_776_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___redArg(v_x_774_);
return v___x_776_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr___boxed(lean_object* v_x_777_, lean_object* v_prec_778_){
_start:
{
lean_object* v_res_779_; 
v_res_779_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2Z2_repr(v_x_777_, v_prec_778_);
lean_dec(v_prec_778_);
lean_dec_ref(v_x_777_);
return v_res_779_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(uint8_t v_x_782_, uint8_t v_y_783_){
_start:
{
if (v_x_782_ == 0)
{
return v_y_783_;
}
else
{
if (v_y_783_ == 0)
{
return v_x_782_;
}
else
{
uint8_t v___x_784_; 
v___x_784_ = 0;
return v___x_784_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd___boxed(lean_object* v_x_785_, lean_object* v_y_786_){
_start:
{
uint8_t v_x_boxed_787_; uint8_t v_y_boxed_788_; uint8_t v_res_789_; lean_object* v_r_790_; 
v_x_boxed_787_ = lean_unbox(v_x_785_);
v_y_boxed_788_ = lean_unbox(v_y_786_);
v_res_789_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v_x_boxed_787_, v_y_boxed_788_);
v_r_790_ = lean_box(v_res_789_);
return v_r_790_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_bmul(uint8_t v_x_791_, uint8_t v_y_792_){
_start:
{
if (v_x_791_ == 0)
{
return v_x_791_;
}
else
{
return v_y_792_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_bmul___boxed(lean_object* v_x_793_, lean_object* v_y_794_){
_start:
{
uint8_t v_x_boxed_795_; uint8_t v_y_boxed_796_; uint8_t v_res_797_; lean_object* v_r_798_; 
v_x_boxed_795_ = lean_unbox(v_x_793_);
v_y_boxed_796_ = lean_unbox(v_y_794_);
v_res_797_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_bmul(v_x_boxed_795_, v_y_boxed_796_);
v_r_798_ = lean_box(v_res_797_);
return v_r_798_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2(lean_object* v_A_799_, lean_object* v_B_800_){
_start:
{
uint8_t v___y_802_; uint8_t v___y_803_; uint8_t v___y_804_; uint8_t v___y_805_; uint8_t v___y_806_; uint8_t v_m00_809_; uint8_t v_m01_810_; uint8_t v_m10_811_; uint8_t v_m11_812_; uint8_t v_m00_813_; uint8_t v_m01_814_; uint8_t v_m10_815_; uint8_t v_m11_816_; uint8_t v___y_818_; uint8_t v___y_819_; uint8_t v___y_820_; uint8_t v___y_821_; uint8_t v___y_823_; uint8_t v___y_824_; uint8_t v___y_825_; uint8_t v___y_826_; uint8_t v___y_829_; uint8_t v___y_830_; uint8_t v___y_831_; uint8_t v___y_833_; uint8_t v___y_834_; uint8_t v___y_835_; uint8_t v___y_838_; uint8_t v___y_839_; uint8_t v___y_841_; uint8_t v___y_842_; uint8_t v___y_845_; 
v_m00_809_ = lean_ctor_get_uint8(v_A_799_, 0);
v_m01_810_ = lean_ctor_get_uint8(v_A_799_, 1);
v_m10_811_ = lean_ctor_get_uint8(v_A_799_, 2);
v_m11_812_ = lean_ctor_get_uint8(v_A_799_, 3);
v_m00_813_ = lean_ctor_get_uint8(v_B_800_, 0);
v_m01_814_ = lean_ctor_get_uint8(v_B_800_, 1);
v_m10_815_ = lean_ctor_get_uint8(v_B_800_, 2);
v_m11_816_ = lean_ctor_get_uint8(v_B_800_, 3);
if (v_m00_809_ == 0)
{
v___y_845_ = v_m00_809_;
goto v___jp_844_;
}
else
{
v___y_845_ = v_m00_813_;
goto v___jp_844_;
}
v___jp_801_:
{
uint8_t v___x_807_; lean_object* v___x_808_; 
v___x_807_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v___y_804_, v___y_806_);
v___x_808_ = lean_alloc_ctor(0, 0, 4);
lean_ctor_set_uint8(v___x_808_, 0, v___y_803_);
lean_ctor_set_uint8(v___x_808_, 1, v___y_805_);
lean_ctor_set_uint8(v___x_808_, 2, v___y_802_);
lean_ctor_set_uint8(v___x_808_, 3, v___x_807_);
return v___x_808_;
}
v___jp_817_:
{
if (v_m11_812_ == 0)
{
v___y_802_ = v___y_818_;
v___y_803_ = v___y_819_;
v___y_804_ = v___y_821_;
v___y_805_ = v___y_820_;
v___y_806_ = v_m11_812_;
goto v___jp_801_;
}
else
{
v___y_802_ = v___y_818_;
v___y_803_ = v___y_819_;
v___y_804_ = v___y_821_;
v___y_805_ = v___y_820_;
v___y_806_ = v_m11_816_;
goto v___jp_801_;
}
}
v___jp_822_:
{
uint8_t v___x_827_; 
v___x_827_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v___y_823_, v___y_826_);
if (v_m10_811_ == 0)
{
v___y_818_ = v___x_827_;
v___y_819_ = v___y_824_;
v___y_820_ = v___y_825_;
v___y_821_ = v_m10_811_;
goto v___jp_817_;
}
else
{
v___y_818_ = v___x_827_;
v___y_819_ = v___y_824_;
v___y_820_ = v___y_825_;
v___y_821_ = v_m01_814_;
goto v___jp_817_;
}
}
v___jp_828_:
{
if (v_m11_812_ == 0)
{
v___y_823_ = v___y_831_;
v___y_824_ = v___y_829_;
v___y_825_ = v___y_830_;
v___y_826_ = v_m11_812_;
goto v___jp_822_;
}
else
{
v___y_823_ = v___y_831_;
v___y_824_ = v___y_829_;
v___y_825_ = v___y_830_;
v___y_826_ = v_m10_815_;
goto v___jp_822_;
}
}
v___jp_832_:
{
uint8_t v___x_836_; 
v___x_836_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v___y_834_, v___y_835_);
if (v_m10_811_ == 0)
{
v___y_829_ = v___y_833_;
v___y_830_ = v___x_836_;
v___y_831_ = v_m10_811_;
goto v___jp_828_;
}
else
{
v___y_829_ = v___y_833_;
v___y_830_ = v___x_836_;
v___y_831_ = v_m00_813_;
goto v___jp_828_;
}
}
v___jp_837_:
{
if (v_m01_810_ == 0)
{
v___y_833_ = v___y_838_;
v___y_834_ = v___y_839_;
v___y_835_ = v_m01_810_;
goto v___jp_832_;
}
else
{
v___y_833_ = v___y_838_;
v___y_834_ = v___y_839_;
v___y_835_ = v_m11_816_;
goto v___jp_832_;
}
}
v___jp_840_:
{
uint8_t v___x_843_; 
v___x_843_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v___y_841_, v___y_842_);
if (v_m00_809_ == 0)
{
v___y_838_ = v___x_843_;
v___y_839_ = v_m00_809_;
goto v___jp_837_;
}
else
{
v___y_838_ = v___x_843_;
v___y_839_ = v_m01_814_;
goto v___jp_837_;
}
}
v___jp_844_:
{
if (v_m01_810_ == 0)
{
v___y_841_ = v___y_845_;
v___y_842_ = v_m01_810_;
goto v___jp_840_;
}
else
{
v___y_841_ = v___y_845_;
v___y_842_ = v_m10_815_;
goto v___jp_840_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2___boxed(lean_object* v_A_846_, lean_object* v_B_847_){
_start:
{
lean_object* v_res_848_; 
v_res_848_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2(v_A_846_, v_B_847_);
lean_dec_ref(v_B_847_);
lean_dec_ref(v_A_846_);
return v_res_848_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2Z2(lean_object* v_A_849_, lean_object* v_B_850_){
_start:
{
lean_object* v_AB_851_; uint8_t v_m00_852_; uint8_t v_m01_853_; uint8_t v_m10_854_; uint8_t v_m11_855_; lean_object* v_BA_856_; uint8_t v_m00_857_; uint8_t v_m01_858_; uint8_t v_m10_859_; uint8_t v_m11_860_; lean_object* v___x_862_; uint8_t v_isShared_863_; uint8_t v_isSharedCheck_871_; 
v_AB_851_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2(v_A_849_, v_B_850_);
v_m00_852_ = lean_ctor_get_uint8(v_AB_851_, 0);
v_m01_853_ = lean_ctor_get_uint8(v_AB_851_, 1);
v_m10_854_ = lean_ctor_get_uint8(v_AB_851_, 2);
v_m11_855_ = lean_ctor_get_uint8(v_AB_851_, 3);
lean_dec_ref(v_AB_851_);
v_BA_856_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul2Z2(v_B_850_, v_A_849_);
v_m00_857_ = lean_ctor_get_uint8(v_BA_856_, 0);
v_m01_858_ = lean_ctor_get_uint8(v_BA_856_, 1);
v_m10_859_ = lean_ctor_get_uint8(v_BA_856_, 2);
v_m11_860_ = lean_ctor_get_uint8(v_BA_856_, 3);
v_isSharedCheck_871_ = !lean_is_exclusive(v_BA_856_);
if (v_isSharedCheck_871_ == 0)
{
v___x_862_ = v_BA_856_;
v_isShared_863_ = v_isSharedCheck_871_;
goto v_resetjp_861_;
}
else
{
lean_dec(v_BA_856_);
v___x_862_ = lean_box(0);
v_isShared_863_ = v_isSharedCheck_871_;
goto v_resetjp_861_;
}
v_resetjp_861_:
{
uint8_t v___x_864_; uint8_t v___x_865_; uint8_t v___x_866_; uint8_t v___x_867_; lean_object* v___x_869_; 
v___x_864_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v_m00_852_, v_m00_857_);
v___x_865_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v_m01_853_, v_m01_858_);
v___x_866_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v_m10_854_, v_m10_859_);
v___x_867_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_badd(v_m11_855_, v_m11_860_);
if (v_isShared_863_ == 0)
{
v___x_869_ = v___x_862_;
goto v_reusejp_868_;
}
else
{
lean_object* v_reuseFailAlloc_870_; 
v_reuseFailAlloc_870_ = lean_alloc_ctor(0, 0, 4);
v___x_869_ = v_reuseFailAlloc_870_;
goto v_reusejp_868_;
}
v_reusejp_868_:
{
lean_ctor_set_uint8(v___x_869_, 0, v___x_864_);
lean_ctor_set_uint8(v___x_869_, 1, v___x_865_);
lean_ctor_set_uint8(v___x_869_, 2, v___x_866_);
lean_ctor_set_uint8(v___x_869_, 3, v___x_867_);
return v___x_869_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2Z2___boxed(lean_object* v_A_872_, lean_object* v_B_873_){
_start:
{
lean_object* v_res_874_; 
v_res_874_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_comm2Z2(v_A_872_, v_B_873_);
lean_dec_ref(v_B_873_);
lean_dec_ref(v_A_872_);
return v_res_874_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2___closed__0(void){
_start:
{
lean_object* v___x_887_; lean_object* v___x_888_; lean_object* v___x_889_; 
v___x_887_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_888_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_889_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_889_, 0, v___x_888_);
lean_ctor_set(v___x_889_, 1, v___x_887_);
lean_ctor_set(v___x_889_, 2, v___x_887_);
lean_ctor_set(v___x_889_, 3, v___x_888_);
return v___x_889_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2(void){
_start:
{
lean_object* v___x_890_; 
v___x_890_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2___closed__0);
return v___x_890_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0(void){
_start:
{
lean_object* v___x_891_; lean_object* v___x_892_; 
v___x_891_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_892_ = lean_int_neg(v___x_891_);
return v___x_892_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__1(void){
_start:
{
lean_object* v___x_893_; lean_object* v___x_894_; lean_object* v___x_895_; lean_object* v___x_896_; 
v___x_893_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0);
v___x_894_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_895_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_896_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_896_, 0, v___x_895_);
lean_ctor_set(v___x_896_, 1, v___x_894_);
lean_ctor_set(v___x_896_, 2, v___x_894_);
lean_ctor_set(v___x_896_, 3, v___x_893_);
return v___x_896_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2(void){
_start:
{
lean_object* v___x_897_; 
v___x_897_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__1);
return v___x_897_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(lean_object* v_x_898_, lean_object* v_x_899_){
_start:
{
lean_object* v_a_900_; lean_object* v_b_901_; lean_object* v_a_902_; lean_object* v_b_903_; uint8_t v___x_904_; 
v_a_900_ = lean_ctor_get(v_x_898_, 0);
v_b_901_ = lean_ctor_get(v_x_898_, 1);
v_a_902_ = lean_ctor_get(v_x_899_, 0);
v_b_903_ = lean_ctor_get(v_x_899_, 1);
v___x_904_ = lean_int_dec_eq(v_a_900_, v_a_902_);
if (v___x_904_ == 0)
{
return v___x_904_;
}
else
{
uint8_t v___x_905_; 
v___x_905_ = lean_int_dec_eq(v_b_901_, v_b_903_);
return v___x_905_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq___boxed(lean_object* v_x_906_, lean_object* v_x_907_){
_start:
{
uint8_t v_res_908_; lean_object* v_r_909_; 
v_res_908_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_x_906_, v_x_907_);
lean_dec_ref(v_x_907_);
lean_dec_ref(v_x_906_);
v_r_909_ = lean_box(v_res_908_);
return v_r_909_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein(lean_object* v_x_910_, lean_object* v_x_911_){
_start:
{
uint8_t v___x_912_; 
v___x_912_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_x_910_, v_x_911_);
return v___x_912_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein___boxed(lean_object* v_x_913_, lean_object* v_x_914_){
_start:
{
uint8_t v_res_915_; lean_object* v_r_916_; 
v_res_915_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein(v_x_913_, v_x_914_);
lean_dec_ref(v_x_914_);
lean_dec_ref(v_x_913_);
v_r_916_ = lean_box(v_res_915_);
return v_r_916_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_926_; lean_object* v___x_927_; 
v___x_926_ = lean_unsigned_to_nat(5u);
v___x_927_ = lean_nat_to_int(v___x_926_);
return v___x_927_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(lean_object* v_x_931_){
_start:
{
lean_object* v_a_932_; lean_object* v_b_933_; lean_object* v___x_935_; uint8_t v_isShared_936_; uint8_t v_isSharedCheck_985_; 
v_a_932_ = lean_ctor_get(v_x_931_, 0);
v_b_933_ = lean_ctor_get(v_x_931_, 1);
v_isSharedCheck_985_ = !lean_is_exclusive(v_x_931_);
if (v_isSharedCheck_985_ == 0)
{
v___x_935_ = v_x_931_;
v_isShared_936_ = v_isSharedCheck_985_;
goto v_resetjp_934_;
}
else
{
lean_inc(v_b_933_);
lean_inc(v_a_932_);
lean_dec(v_x_931_);
v___x_935_ = lean_box(0);
v_isShared_936_ = v_isSharedCheck_985_;
goto v_resetjp_934_;
}
v_resetjp_934_:
{
lean_object* v___x_937_; lean_object* v___x_938_; lean_object* v___x_939_; lean_object* v___y_941_; uint8_t v___y_942_; lean_object* v___y_943_; lean_object* v___y_957_; lean_object* v___x_977_; lean_object* v___x_978_; uint8_t v___x_979_; 
v___x_937_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5));
v___x_938_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__3));
v___x_939_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__4);
v___x_977_ = lean_unsigned_to_nat(0u);
v___x_978_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_979_ = lean_int_dec_lt(v_a_932_, v___x_978_);
if (v___x_979_ == 0)
{
lean_object* v___x_980_; lean_object* v___x_981_; 
v___x_980_ = l_Int_repr(v_a_932_);
lean_dec(v_a_932_);
v___x_981_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_981_, 0, v___x_980_);
v___y_957_ = v___x_981_;
goto v___jp_956_;
}
else
{
lean_object* v___x_982_; lean_object* v___x_983_; lean_object* v___x_984_; 
v___x_982_ = l_Int_repr(v_a_932_);
lean_dec(v_a_932_);
v___x_983_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_983_, 0, v___x_982_);
v___x_984_ = l_Repr_addAppParen(v___x_983_, v___x_977_);
v___y_957_ = v___x_984_;
goto v___jp_956_;
}
v___jp_940_:
{
lean_object* v___x_945_; 
if (v_isShared_936_ == 0)
{
lean_ctor_set_tag(v___x_935_, 4);
lean_ctor_set(v___x_935_, 1, v___y_943_);
lean_ctor_set(v___x_935_, 0, v___x_939_);
v___x_945_ = v___x_935_;
goto v_reusejp_944_;
}
else
{
lean_object* v_reuseFailAlloc_955_; 
v_reuseFailAlloc_955_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_955_, 0, v___x_939_);
lean_ctor_set(v_reuseFailAlloc_955_, 1, v___y_943_);
v___x_945_ = v_reuseFailAlloc_955_;
goto v_reusejp_944_;
}
v_reusejp_944_:
{
lean_object* v___x_946_; lean_object* v___x_947_; lean_object* v___x_948_; lean_object* v___x_949_; lean_object* v___x_950_; lean_object* v___x_951_; lean_object* v___x_952_; lean_object* v___x_953_; lean_object* v___x_954_; 
v___x_946_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_946_, 0, v___x_945_);
lean_ctor_set_uint8(v___x_946_, sizeof(void*)*1, v___y_942_);
v___x_947_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_947_, 0, v___y_941_);
lean_ctor_set(v___x_947_, 1, v___x_946_);
v___x_948_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10);
v___x_949_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11));
v___x_950_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_950_, 0, v___x_949_);
lean_ctor_set(v___x_950_, 1, v___x_947_);
v___x_951_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12));
v___x_952_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_952_, 0, v___x_950_);
lean_ctor_set(v___x_952_, 1, v___x_951_);
v___x_953_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_953_, 0, v___x_948_);
lean_ctor_set(v___x_953_, 1, v___x_952_);
v___x_954_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_954_, 0, v___x_953_);
lean_ctor_set_uint8(v___x_954_, sizeof(void*)*1, v___y_942_);
return v___x_954_;
}
}
v___jp_956_:
{
lean_object* v___x_958_; uint8_t v___x_959_; lean_object* v___x_960_; lean_object* v___x_961_; lean_object* v___x_962_; lean_object* v___x_963_; lean_object* v___x_964_; lean_object* v___x_965_; lean_object* v___x_966_; lean_object* v___x_967_; lean_object* v___x_968_; lean_object* v___x_969_; lean_object* v___x_970_; uint8_t v___x_971_; 
v___x_958_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_958_, 0, v___x_939_);
lean_ctor_set(v___x_958_, 1, v___y_957_);
v___x_959_ = 0;
v___x_960_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_960_, 0, v___x_958_);
lean_ctor_set_uint8(v___x_960_, sizeof(void*)*1, v___x_959_);
v___x_961_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_961_, 0, v___x_938_);
lean_ctor_set(v___x_961_, 1, v___x_960_);
v___x_962_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19));
v___x_963_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_963_, 0, v___x_961_);
lean_ctor_set(v___x_963_, 1, v___x_962_);
v___x_964_ = lean_box(1);
v___x_965_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_965_, 0, v___x_963_);
lean_ctor_set(v___x_965_, 1, v___x_964_);
v___x_966_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg___closed__6));
v___x_967_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_967_, 0, v___x_965_);
lean_ctor_set(v___x_967_, 1, v___x_966_);
v___x_968_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_968_, 0, v___x_967_);
lean_ctor_set(v___x_968_, 1, v___x_937_);
v___x_969_ = lean_unsigned_to_nat(0u);
v___x_970_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_971_ = lean_int_dec_lt(v_b_933_, v___x_970_);
if (v___x_971_ == 0)
{
lean_object* v___x_972_; lean_object* v___x_973_; 
v___x_972_ = l_Int_repr(v_b_933_);
lean_dec(v_b_933_);
v___x_973_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_973_, 0, v___x_972_);
v___y_941_ = v___x_968_;
v___y_942_ = v___x_959_;
v___y_943_ = v___x_973_;
goto v___jp_940_;
}
else
{
lean_object* v___x_974_; lean_object* v___x_975_; lean_object* v___x_976_; 
v___x_974_ = l_Int_repr(v_b_933_);
lean_dec(v_b_933_);
v___x_975_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_975_, 0, v___x_974_);
v___x_976_ = l_Repr_addAppParen(v___x_975_, v___x_969_);
v___y_941_ = v___x_968_;
v___y_942_ = v___x_959_;
v___y_943_ = v___x_976_;
goto v___jp_940_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr(lean_object* v_x_986_, lean_object* v_prec_987_){
_start:
{
lean_object* v___x_988_; 
v___x_988_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_x_986_);
return v___x_988_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___boxed(lean_object* v_x_989_, lean_object* v_prec_990_){
_start:
{
lean_object* v_res_991_; 
v_res_991_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr(v_x_989_, v_prec_990_);
lean_dec(v_prec_990_);
return v_res_991_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez___closed__0(void){
_start:
{
lean_object* v___x_994_; lean_object* v___x_995_; 
v___x_994_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_995_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_995_, 0, v___x_994_);
lean_ctor_set(v___x_995_, 1, v___x_994_);
return v___x_995_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez(void){
_start:
{
lean_object* v___x_996_; 
v___x_996_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez___closed__0);
return v___x_996_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone___closed__0(void){
_start:
{
lean_object* v___x_997_; lean_object* v___x_998_; lean_object* v___x_999_; 
v___x_997_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_998_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_999_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_999_, 0, v___x_998_);
lean_ctor_set(v___x_999_, 1, v___x_997_);
return v___x_999_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone(void){
_start:
{
lean_object* v___x_1000_; 
v___x_1000_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone___closed__0);
return v___x_1000_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega___closed__0(void){
_start:
{
lean_object* v___x_1001_; lean_object* v___x_1002_; lean_object* v___x_1003_; 
v___x_1001_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2___closed__0);
v___x_1002_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__15);
v___x_1003_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1003_, 0, v___x_1002_);
lean_ctor_set(v___x_1003_, 1, v___x_1001_);
return v___x_1003_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega(void){
_start:
{
lean_object* v___x_1004_; 
v___x_1004_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega___closed__0);
return v___x_1004_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2___closed__0(void){
_start:
{
lean_object* v___x_1005_; lean_object* v___x_1006_; 
v___x_1005_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2___closed__0);
v___x_1006_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1006_, 0, v___x_1005_);
lean_ctor_set(v___x_1006_, 1, v___x_1005_);
return v___x_1006_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2(void){
_start:
{
lean_object* v___x_1007_; 
v___x_1007_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2___closed__0);
return v___x_1007_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(lean_object* v_x_1008_, lean_object* v_y_1009_){
_start:
{
lean_object* v_a_1010_; lean_object* v_b_1011_; lean_object* v_a_1012_; lean_object* v_b_1013_; lean_object* v___x_1015_; uint8_t v_isShared_1016_; uint8_t v_isSharedCheck_1022_; 
v_a_1010_ = lean_ctor_get(v_x_1008_, 0);
v_b_1011_ = lean_ctor_get(v_x_1008_, 1);
v_a_1012_ = lean_ctor_get(v_y_1009_, 0);
v_b_1013_ = lean_ctor_get(v_y_1009_, 1);
v_isSharedCheck_1022_ = !lean_is_exclusive(v_y_1009_);
if (v_isSharedCheck_1022_ == 0)
{
v___x_1015_ = v_y_1009_;
v_isShared_1016_ = v_isSharedCheck_1022_;
goto v_resetjp_1014_;
}
else
{
lean_inc(v_b_1013_);
lean_inc(v_a_1012_);
lean_dec(v_y_1009_);
v___x_1015_ = lean_box(0);
v_isShared_1016_ = v_isSharedCheck_1022_;
goto v_resetjp_1014_;
}
v_resetjp_1014_:
{
lean_object* v___x_1017_; lean_object* v___x_1018_; lean_object* v___x_1020_; 
v___x_1017_ = lean_int_add(v_a_1010_, v_a_1012_);
lean_dec(v_a_1012_);
v___x_1018_ = lean_int_add(v_b_1011_, v_b_1013_);
lean_dec(v_b_1013_);
if (v_isShared_1016_ == 0)
{
lean_ctor_set(v___x_1015_, 1, v___x_1018_);
lean_ctor_set(v___x_1015_, 0, v___x_1017_);
v___x_1020_ = v___x_1015_;
goto v_reusejp_1019_;
}
else
{
lean_object* v_reuseFailAlloc_1021_; 
v_reuseFailAlloc_1021_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1021_, 0, v___x_1017_);
lean_ctor_set(v_reuseFailAlloc_1021_, 1, v___x_1018_);
v___x_1020_ = v_reuseFailAlloc_1021_;
goto v_reusejp_1019_;
}
v_reusejp_1019_:
{
return v___x_1020_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd___boxed(lean_object* v_x_1023_, lean_object* v_y_1024_){
_start:
{
lean_object* v_res_1025_; 
v_res_1025_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v_x_1023_, v_y_1024_);
lean_dec_ref(v_x_1023_);
return v_res_1025_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_esub(lean_object* v_x_1026_, lean_object* v_y_1027_){
_start:
{
lean_object* v_a_1028_; lean_object* v_b_1029_; lean_object* v_a_1030_; lean_object* v_b_1031_; lean_object* v___x_1033_; uint8_t v_isShared_1034_; uint8_t v_isSharedCheck_1040_; 
v_a_1028_ = lean_ctor_get(v_x_1026_, 0);
v_b_1029_ = lean_ctor_get(v_x_1026_, 1);
v_a_1030_ = lean_ctor_get(v_y_1027_, 0);
v_b_1031_ = lean_ctor_get(v_y_1027_, 1);
v_isSharedCheck_1040_ = !lean_is_exclusive(v_y_1027_);
if (v_isSharedCheck_1040_ == 0)
{
v___x_1033_ = v_y_1027_;
v_isShared_1034_ = v_isSharedCheck_1040_;
goto v_resetjp_1032_;
}
else
{
lean_inc(v_b_1031_);
lean_inc(v_a_1030_);
lean_dec(v_y_1027_);
v___x_1033_ = lean_box(0);
v_isShared_1034_ = v_isSharedCheck_1040_;
goto v_resetjp_1032_;
}
v_resetjp_1032_:
{
lean_object* v___x_1035_; lean_object* v___x_1036_; lean_object* v___x_1038_; 
v___x_1035_ = lean_int_sub(v_a_1028_, v_a_1030_);
lean_dec(v_a_1030_);
v___x_1036_ = lean_int_sub(v_b_1029_, v_b_1031_);
lean_dec(v_b_1031_);
if (v_isShared_1034_ == 0)
{
lean_ctor_set(v___x_1033_, 1, v___x_1036_);
lean_ctor_set(v___x_1033_, 0, v___x_1035_);
v___x_1038_ = v___x_1033_;
goto v_reusejp_1037_;
}
else
{
lean_object* v_reuseFailAlloc_1039_; 
v_reuseFailAlloc_1039_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1039_, 0, v___x_1035_);
lean_ctor_set(v_reuseFailAlloc_1039_, 1, v___x_1036_);
v___x_1038_ = v_reuseFailAlloc_1039_;
goto v_reusejp_1037_;
}
v_reusejp_1037_:
{
return v___x_1038_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_esub___boxed(lean_object* v_x_1041_, lean_object* v_y_1042_){
_start:
{
lean_object* v_res_1043_; 
v_res_1043_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_esub(v_x_1041_, v_y_1042_);
lean_dec_ref(v_x_1041_);
return v_res_1043_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(lean_object* v_x_1044_, lean_object* v_y_1045_){
_start:
{
lean_object* v_a_1046_; lean_object* v_b_1047_; lean_object* v_a_1048_; lean_object* v_b_1049_; lean_object* v___x_1051_; uint8_t v_isShared_1052_; uint8_t v_isSharedCheck_1063_; 
v_a_1046_ = lean_ctor_get(v_x_1044_, 0);
v_b_1047_ = lean_ctor_get(v_x_1044_, 1);
v_a_1048_ = lean_ctor_get(v_y_1045_, 0);
v_b_1049_ = lean_ctor_get(v_y_1045_, 1);
v_isSharedCheck_1063_ = !lean_is_exclusive(v_y_1045_);
if (v_isSharedCheck_1063_ == 0)
{
v___x_1051_ = v_y_1045_;
v_isShared_1052_ = v_isSharedCheck_1063_;
goto v_resetjp_1050_;
}
else
{
lean_inc(v_b_1049_);
lean_inc(v_a_1048_);
lean_dec(v_y_1045_);
v___x_1051_ = lean_box(0);
v_isShared_1052_ = v_isSharedCheck_1063_;
goto v_resetjp_1050_;
}
v_resetjp_1050_:
{
lean_object* v___x_1053_; lean_object* v___x_1054_; lean_object* v___x_1055_; lean_object* v___x_1056_; lean_object* v___x_1057_; lean_object* v___x_1058_; lean_object* v___x_1059_; lean_object* v___x_1061_; 
v___x_1053_ = lean_int_mul(v_a_1046_, v_a_1048_);
v___x_1054_ = lean_int_mul(v_b_1047_, v_b_1049_);
v___x_1055_ = lean_int_sub(v___x_1053_, v___x_1054_);
lean_dec(v___x_1053_);
v___x_1056_ = lean_int_mul(v_a_1046_, v_b_1049_);
lean_dec(v_b_1049_);
v___x_1057_ = lean_int_mul(v_b_1047_, v_a_1048_);
lean_dec(v_a_1048_);
v___x_1058_ = lean_int_add(v___x_1056_, v___x_1057_);
lean_dec(v___x_1057_);
lean_dec(v___x_1056_);
v___x_1059_ = lean_int_sub(v___x_1058_, v___x_1054_);
lean_dec(v___x_1054_);
lean_dec(v___x_1058_);
if (v_isShared_1052_ == 0)
{
lean_ctor_set(v___x_1051_, 1, v___x_1059_);
lean_ctor_set(v___x_1051_, 0, v___x_1055_);
v___x_1061_ = v___x_1051_;
goto v_reusejp_1060_;
}
else
{
lean_object* v_reuseFailAlloc_1062_; 
v_reuseFailAlloc_1062_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1062_, 0, v___x_1055_);
lean_ctor_set(v_reuseFailAlloc_1062_, 1, v___x_1059_);
v___x_1061_ = v_reuseFailAlloc_1062_;
goto v_reusejp_1060_;
}
v_reusejp_1060_:
{
return v___x_1061_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul___boxed(lean_object* v_x_1064_, lean_object* v_y_1065_){
_start:
{
lean_object* v_res_1066_; 
v_res_1066_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_x_1064_, v_y_1065_);
lean_dec_ref(v_x_1064_);
return v_res_1066_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instZeroEisenstein(void){
_start:
{
lean_object* v___x_1067_; 
v___x_1067_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez;
return v___x_1067_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instOneEisenstein(void){
_start:
{
lean_object* v___x_1068_; 
v___x_1068_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone;
return v___x_1068_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E_decEq(lean_object* v_x_1075_, lean_object* v_x_1076_){
_start:
{
lean_object* v_m00_1077_; lean_object* v_m01_1078_; lean_object* v_m02_1079_; lean_object* v_m10_1080_; lean_object* v_m11_1081_; lean_object* v_m12_1082_; lean_object* v_m20_1083_; lean_object* v_m21_1084_; lean_object* v_m22_1085_; lean_object* v_m00_1086_; lean_object* v_m01_1087_; lean_object* v_m02_1088_; lean_object* v_m10_1089_; lean_object* v_m11_1090_; lean_object* v_m12_1091_; lean_object* v_m20_1092_; lean_object* v_m21_1093_; lean_object* v_m22_1094_; uint8_t v___x_1095_; 
v_m00_1077_ = lean_ctor_get(v_x_1075_, 0);
v_m01_1078_ = lean_ctor_get(v_x_1075_, 1);
v_m02_1079_ = lean_ctor_get(v_x_1075_, 2);
v_m10_1080_ = lean_ctor_get(v_x_1075_, 3);
v_m11_1081_ = lean_ctor_get(v_x_1075_, 4);
v_m12_1082_ = lean_ctor_get(v_x_1075_, 5);
v_m20_1083_ = lean_ctor_get(v_x_1075_, 6);
v_m21_1084_ = lean_ctor_get(v_x_1075_, 7);
v_m22_1085_ = lean_ctor_get(v_x_1075_, 8);
v_m00_1086_ = lean_ctor_get(v_x_1076_, 0);
v_m01_1087_ = lean_ctor_get(v_x_1076_, 1);
v_m02_1088_ = lean_ctor_get(v_x_1076_, 2);
v_m10_1089_ = lean_ctor_get(v_x_1076_, 3);
v_m11_1090_ = lean_ctor_get(v_x_1076_, 4);
v_m12_1091_ = lean_ctor_get(v_x_1076_, 5);
v_m20_1092_ = lean_ctor_get(v_x_1076_, 6);
v_m21_1093_ = lean_ctor_get(v_x_1076_, 7);
v_m22_1094_ = lean_ctor_get(v_x_1076_, 8);
v___x_1095_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m00_1077_, v_m00_1086_);
if (v___x_1095_ == 0)
{
return v___x_1095_;
}
else
{
uint8_t v___x_1096_; 
v___x_1096_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m01_1078_, v_m01_1087_);
if (v___x_1096_ == 0)
{
return v___x_1096_;
}
else
{
uint8_t v___x_1097_; 
v___x_1097_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m02_1079_, v_m02_1088_);
if (v___x_1097_ == 0)
{
return v___x_1097_;
}
else
{
uint8_t v___x_1098_; 
v___x_1098_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m10_1080_, v_m10_1089_);
if (v___x_1098_ == 0)
{
return v___x_1098_;
}
else
{
uint8_t v___x_1099_; 
v___x_1099_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m11_1081_, v_m11_1090_);
if (v___x_1099_ == 0)
{
return v___x_1099_;
}
else
{
uint8_t v___x_1100_; 
v___x_1100_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m12_1082_, v_m12_1091_);
if (v___x_1100_ == 0)
{
return v___x_1100_;
}
else
{
uint8_t v___x_1101_; 
v___x_1101_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m20_1083_, v_m20_1092_);
if (v___x_1101_ == 0)
{
return v___x_1101_;
}
else
{
uint8_t v___x_1102_; 
v___x_1102_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m21_1084_, v_m21_1093_);
if (v___x_1102_ == 0)
{
return v___x_1102_;
}
else
{
uint8_t v___x_1103_; 
v___x_1103_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqEisenstein_decEq(v_m22_1085_, v_m22_1094_);
return v___x_1103_;
}
}
}
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E_decEq___boxed(lean_object* v_x_1104_, lean_object* v_x_1105_){
_start:
{
uint8_t v_res_1106_; lean_object* v_r_1107_; 
v_res_1106_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E_decEq(v_x_1104_, v_x_1105_);
lean_dec_ref(v_x_1105_);
lean_dec_ref(v_x_1104_);
v_r_1107_ = lean_box(v_res_1106_);
return v_r_1107_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E(lean_object* v_x_1108_, lean_object* v_x_1109_){
_start:
{
uint8_t v___x_1110_; 
v___x_1110_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E_decEq(v_x_1108_, v_x_1109_);
return v___x_1110_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E___boxed(lean_object* v_x_1111_, lean_object* v_x_1112_){
_start:
{
uint8_t v_res_1113_; lean_object* v_r_1114_; 
v_res_1113_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instDecidableEqMat3E(v_x_1111_, v_x_1112_);
lean_dec_ref(v_x_1112_);
lean_dec_ref(v_x_1111_);
v_r_1114_ = lean_box(v_res_1113_);
return v_r_1114_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr___redArg(lean_object* v_x_1115_){
_start:
{
lean_object* v_m00_1116_; lean_object* v_m01_1117_; lean_object* v_m02_1118_; lean_object* v_m10_1119_; lean_object* v_m11_1120_; lean_object* v_m12_1121_; lean_object* v_m20_1122_; lean_object* v_m21_1123_; lean_object* v_m22_1124_; lean_object* v___x_1125_; lean_object* v___x_1126_; lean_object* v___x_1127_; lean_object* v___x_1128_; lean_object* v___x_1129_; uint8_t v___x_1130_; lean_object* v___x_1131_; lean_object* v___x_1132_; lean_object* v___x_1133_; lean_object* v___x_1134_; lean_object* v___x_1135_; lean_object* v___x_1136_; lean_object* v___x_1137_; lean_object* v___x_1138_; lean_object* v___x_1139_; lean_object* v___x_1140_; lean_object* v___x_1141_; lean_object* v___x_1142_; lean_object* v___x_1143_; lean_object* v___x_1144_; lean_object* v___x_1145_; lean_object* v___x_1146_; lean_object* v___x_1147_; lean_object* v___x_1148_; lean_object* v___x_1149_; lean_object* v___x_1150_; lean_object* v___x_1151_; lean_object* v___x_1152_; lean_object* v___x_1153_; lean_object* v___x_1154_; lean_object* v___x_1155_; lean_object* v___x_1156_; lean_object* v___x_1157_; lean_object* v___x_1158_; lean_object* v___x_1159_; lean_object* v___x_1160_; lean_object* v___x_1161_; lean_object* v___x_1162_; lean_object* v___x_1163_; lean_object* v___x_1164_; lean_object* v___x_1165_; lean_object* v___x_1166_; lean_object* v___x_1167_; lean_object* v___x_1168_; lean_object* v___x_1169_; lean_object* v___x_1170_; lean_object* v___x_1171_; lean_object* v___x_1172_; lean_object* v___x_1173_; lean_object* v___x_1174_; lean_object* v___x_1175_; lean_object* v___x_1176_; lean_object* v___x_1177_; lean_object* v___x_1178_; lean_object* v___x_1179_; lean_object* v___x_1180_; lean_object* v___x_1181_; lean_object* v___x_1182_; lean_object* v___x_1183_; lean_object* v___x_1184_; lean_object* v___x_1185_; lean_object* v___x_1186_; lean_object* v___x_1187_; lean_object* v___x_1188_; lean_object* v___x_1189_; lean_object* v___x_1190_; lean_object* v___x_1191_; lean_object* v___x_1192_; lean_object* v___x_1193_; lean_object* v___x_1194_; lean_object* v___x_1195_; lean_object* v___x_1196_; lean_object* v___x_1197_; lean_object* v___x_1198_; lean_object* v___x_1199_; lean_object* v___x_1200_; lean_object* v___x_1201_; lean_object* v___x_1202_; lean_object* v___x_1203_; lean_object* v___x_1204_; lean_object* v___x_1205_; lean_object* v___x_1206_; lean_object* v___x_1207_; lean_object* v___x_1208_; lean_object* v___x_1209_; lean_object* v___x_1210_; lean_object* v___x_1211_; lean_object* v___x_1212_; lean_object* v___x_1213_; 
v_m00_1116_ = lean_ctor_get(v_x_1115_, 0);
lean_inc_ref(v_m00_1116_);
v_m01_1117_ = lean_ctor_get(v_x_1115_, 1);
lean_inc_ref(v_m01_1117_);
v_m02_1118_ = lean_ctor_get(v_x_1115_, 2);
lean_inc_ref(v_m02_1118_);
v_m10_1119_ = lean_ctor_get(v_x_1115_, 3);
lean_inc_ref(v_m10_1119_);
v_m11_1120_ = lean_ctor_get(v_x_1115_, 4);
lean_inc_ref(v_m11_1120_);
v_m12_1121_ = lean_ctor_get(v_x_1115_, 5);
lean_inc_ref(v_m12_1121_);
v_m20_1122_ = lean_ctor_get(v_x_1115_, 6);
lean_inc_ref(v_m20_1122_);
v_m21_1123_ = lean_ctor_get(v_x_1115_, 7);
lean_inc_ref(v_m21_1123_);
v_m22_1124_ = lean_ctor_get(v_x_1115_, 8);
lean_inc_ref(v_m22_1124_);
lean_dec_ref(v_x_1115_);
v___x_1125_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__5));
v___x_1126_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__6));
v___x_1127_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__7);
v___x_1128_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m00_1116_);
v___x_1129_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1129_, 0, v___x_1127_);
lean_ctor_set(v___x_1129_, 1, v___x_1128_);
v___x_1130_ = 0;
v___x_1131_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1131_, 0, v___x_1129_);
lean_ctor_set_uint8(v___x_1131_, sizeof(void*)*1, v___x_1130_);
v___x_1132_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1132_, 0, v___x_1126_);
lean_ctor_set(v___x_1132_, 1, v___x_1131_);
v___x_1133_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__19));
v___x_1134_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1134_, 0, v___x_1132_);
lean_ctor_set(v___x_1134_, 1, v___x_1133_);
v___x_1135_ = lean_box(1);
v___x_1136_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1136_, 0, v___x_1134_);
lean_ctor_set(v___x_1136_, 1, v___x_1135_);
v___x_1137_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__21));
v___x_1138_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1138_, 0, v___x_1136_);
lean_ctor_set(v___x_1138_, 1, v___x_1137_);
v___x_1139_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1139_, 0, v___x_1138_);
lean_ctor_set(v___x_1139_, 1, v___x_1125_);
v___x_1140_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m01_1117_);
v___x_1141_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1141_, 0, v___x_1127_);
lean_ctor_set(v___x_1141_, 1, v___x_1140_);
v___x_1142_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1142_, 0, v___x_1141_);
lean_ctor_set_uint8(v___x_1142_, sizeof(void*)*1, v___x_1130_);
v___x_1143_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1143_, 0, v___x_1139_);
lean_ctor_set(v___x_1143_, 1, v___x_1142_);
v___x_1144_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1144_, 0, v___x_1143_);
lean_ctor_set(v___x_1144_, 1, v___x_1133_);
v___x_1145_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1145_, 0, v___x_1144_);
lean_ctor_set(v___x_1145_, 1, v___x_1135_);
v___x_1146_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__9));
v___x_1147_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1147_, 0, v___x_1145_);
lean_ctor_set(v___x_1147_, 1, v___x_1146_);
v___x_1148_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1148_, 0, v___x_1147_);
lean_ctor_set(v___x_1148_, 1, v___x_1125_);
v___x_1149_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m02_1118_);
v___x_1150_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1150_, 0, v___x_1127_);
lean_ctor_set(v___x_1150_, 1, v___x_1149_);
v___x_1151_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1151_, 0, v___x_1150_);
lean_ctor_set_uint8(v___x_1151_, sizeof(void*)*1, v___x_1130_);
v___x_1152_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1152_, 0, v___x_1148_);
lean_ctor_set(v___x_1152_, 1, v___x_1151_);
v___x_1153_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1153_, 0, v___x_1152_);
lean_ctor_set(v___x_1153_, 1, v___x_1133_);
v___x_1154_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1154_, 0, v___x_1153_);
lean_ctor_set(v___x_1154_, 1, v___x_1135_);
v___x_1155_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__17));
v___x_1156_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1156_, 0, v___x_1154_);
lean_ctor_set(v___x_1156_, 1, v___x_1155_);
v___x_1157_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1157_, 0, v___x_1156_);
lean_ctor_set(v___x_1157_, 1, v___x_1125_);
v___x_1158_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m10_1119_);
v___x_1159_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1159_, 0, v___x_1127_);
lean_ctor_set(v___x_1159_, 1, v___x_1158_);
v___x_1160_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1160_, 0, v___x_1159_);
lean_ctor_set_uint8(v___x_1160_, sizeof(void*)*1, v___x_1130_);
v___x_1161_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1161_, 0, v___x_1157_);
lean_ctor_set(v___x_1161_, 1, v___x_1160_);
v___x_1162_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1162_, 0, v___x_1161_);
lean_ctor_set(v___x_1162_, 1, v___x_1133_);
v___x_1163_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1163_, 0, v___x_1162_);
lean_ctor_set(v___x_1163_, 1, v___x_1135_);
v___x_1164_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__14));
v___x_1165_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1165_, 0, v___x_1163_);
lean_ctor_set(v___x_1165_, 1, v___x_1164_);
v___x_1166_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1166_, 0, v___x_1165_);
lean_ctor_set(v___x_1166_, 1, v___x_1125_);
v___x_1167_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m11_1120_);
v___x_1168_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1168_, 0, v___x_1127_);
lean_ctor_set(v___x_1168_, 1, v___x_1167_);
v___x_1169_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1169_, 0, v___x_1168_);
lean_ctor_set_uint8(v___x_1169_, sizeof(void*)*1, v___x_1130_);
v___x_1170_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1170_, 0, v___x_1166_);
lean_ctor_set(v___x_1170_, 1, v___x_1169_);
v___x_1171_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1171_, 0, v___x_1170_);
lean_ctor_set(v___x_1171_, 1, v___x_1133_);
v___x_1172_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1172_, 0, v___x_1171_);
lean_ctor_set(v___x_1172_, 1, v___x_1135_);
v___x_1173_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__7));
v___x_1174_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1174_, 0, v___x_1172_);
lean_ctor_set(v___x_1174_, 1, v___x_1173_);
v___x_1175_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1175_, 0, v___x_1174_);
lean_ctor_set(v___x_1175_, 1, v___x_1125_);
v___x_1176_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m12_1121_);
v___x_1177_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1177_, 0, v___x_1127_);
lean_ctor_set(v___x_1177_, 1, v___x_1176_);
v___x_1178_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1178_, 0, v___x_1177_);
lean_ctor_set_uint8(v___x_1178_, sizeof(void*)*1, v___x_1130_);
v___x_1179_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1179_, 0, v___x_1175_);
lean_ctor_set(v___x_1179_, 1, v___x_1178_);
v___x_1180_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1180_, 0, v___x_1179_);
lean_ctor_set(v___x_1180_, 1, v___x_1133_);
v___x_1181_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1181_, 0, v___x_1180_);
lean_ctor_set(v___x_1181_, 1, v___x_1135_);
v___x_1182_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__5));
v___x_1183_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1183_, 0, v___x_1181_);
lean_ctor_set(v___x_1183_, 1, v___x_1182_);
v___x_1184_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1184_, 0, v___x_1183_);
lean_ctor_set(v___x_1184_, 1, v___x_1125_);
v___x_1185_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m20_1122_);
v___x_1186_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1186_, 0, v___x_1127_);
lean_ctor_set(v___x_1186_, 1, v___x_1185_);
v___x_1187_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1187_, 0, v___x_1186_);
lean_ctor_set_uint8(v___x_1187_, sizeof(void*)*1, v___x_1130_);
v___x_1188_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1188_, 0, v___x_1184_);
lean_ctor_set(v___x_1188_, 1, v___x_1187_);
v___x_1189_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1189_, 0, v___x_1188_);
lean_ctor_set(v___x_1189_, 1, v___x_1133_);
v___x_1190_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1190_, 0, v___x_1189_);
lean_ctor_set(v___x_1190_, 1, v___x_1135_);
v___x_1191_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__3));
v___x_1192_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1192_, 0, v___x_1190_);
lean_ctor_set(v___x_1192_, 1, v___x_1191_);
v___x_1193_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1193_, 0, v___x_1192_);
lean_ctor_set(v___x_1193_, 1, v___x_1125_);
v___x_1194_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m21_1123_);
v___x_1195_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1195_, 0, v___x_1127_);
lean_ctor_set(v___x_1195_, 1, v___x_1194_);
v___x_1196_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1196_, 0, v___x_1195_);
lean_ctor_set_uint8(v___x_1196_, sizeof(void*)*1, v___x_1130_);
v___x_1197_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1197_, 0, v___x_1193_);
lean_ctor_set(v___x_1197_, 1, v___x_1196_);
v___x_1198_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1198_, 0, v___x_1197_);
lean_ctor_set(v___x_1198_, 1, v___x_1133_);
v___x_1199_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1199_, 0, v___x_1198_);
lean_ctor_set(v___x_1199_, 1, v___x_1135_);
v___x_1200_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3_repr___redArg___closed__1));
v___x_1201_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1201_, 0, v___x_1199_);
lean_ctor_set(v___x_1201_, 1, v___x_1200_);
v___x_1202_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1202_, 0, v___x_1201_);
lean_ctor_set(v___x_1202_, 1, v___x_1125_);
v___x_1203_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprEisenstein_repr___redArg(v_m22_1124_);
v___x_1204_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1204_, 0, v___x_1127_);
lean_ctor_set(v___x_1204_, 1, v___x_1203_);
v___x_1205_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1205_, 0, v___x_1204_);
lean_ctor_set_uint8(v___x_1205_, sizeof(void*)*1, v___x_1130_);
v___x_1206_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1206_, 0, v___x_1202_);
lean_ctor_set(v___x_1206_, 1, v___x_1205_);
v___x_1207_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__10);
v___x_1208_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__11));
v___x_1209_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1209_, 0, v___x_1208_);
lean_ctor_set(v___x_1209_, 1, v___x_1206_);
v___x_1210_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat2_repr___redArg___closed__12));
v___x_1211_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1211_, 0, v___x_1209_);
lean_ctor_set(v___x_1211_, 1, v___x_1210_);
v___x_1212_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1212_, 0, v___x_1207_);
lean_ctor_set(v___x_1212_, 1, v___x_1211_);
v___x_1213_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1213_, 0, v___x_1212_);
lean_ctor_set_uint8(v___x_1213_, sizeof(void*)*1, v___x_1130_);
return v___x_1213_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr(lean_object* v_x_1214_, lean_object* v_prec_1215_){
_start:
{
lean_object* v___x_1216_; 
v___x_1216_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr___redArg(v_x_1214_);
return v___x_1216_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr___boxed(lean_object* v_x_1217_, lean_object* v_prec_1218_){
_start:
{
lean_object* v_res_1219_; 
v_res_1219_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_instReprMat3E_repr(v_x_1217_, v_prec_1218_);
lean_dec(v_prec_1218_);
return v_res_1219_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3E(lean_object* v_A_1222_, lean_object* v_B_1223_){
_start:
{
lean_object* v_m00_1224_; lean_object* v_m01_1225_; lean_object* v_m02_1226_; lean_object* v_m10_1227_; lean_object* v_m11_1228_; lean_object* v_m12_1229_; lean_object* v_m20_1230_; lean_object* v_m21_1231_; lean_object* v_m22_1232_; lean_object* v_m00_1233_; lean_object* v_m01_1234_; lean_object* v_m02_1235_; lean_object* v_m10_1236_; lean_object* v_m11_1237_; lean_object* v_m12_1238_; lean_object* v_m20_1239_; lean_object* v_m21_1240_; lean_object* v_m22_1241_; lean_object* v___x_1243_; uint8_t v_isShared_1244_; uint8_t v_isSharedCheck_1293_; 
v_m00_1224_ = lean_ctor_get(v_A_1222_, 0);
v_m01_1225_ = lean_ctor_get(v_A_1222_, 1);
v_m02_1226_ = lean_ctor_get(v_A_1222_, 2);
v_m10_1227_ = lean_ctor_get(v_A_1222_, 3);
v_m11_1228_ = lean_ctor_get(v_A_1222_, 4);
v_m12_1229_ = lean_ctor_get(v_A_1222_, 5);
v_m20_1230_ = lean_ctor_get(v_A_1222_, 6);
v_m21_1231_ = lean_ctor_get(v_A_1222_, 7);
v_m22_1232_ = lean_ctor_get(v_A_1222_, 8);
v_m00_1233_ = lean_ctor_get(v_B_1223_, 0);
v_m01_1234_ = lean_ctor_get(v_B_1223_, 1);
v_m02_1235_ = lean_ctor_get(v_B_1223_, 2);
v_m10_1236_ = lean_ctor_get(v_B_1223_, 3);
v_m11_1237_ = lean_ctor_get(v_B_1223_, 4);
v_m12_1238_ = lean_ctor_get(v_B_1223_, 5);
v_m20_1239_ = lean_ctor_get(v_B_1223_, 6);
v_m21_1240_ = lean_ctor_get(v_B_1223_, 7);
v_m22_1241_ = lean_ctor_get(v_B_1223_, 8);
v_isSharedCheck_1293_ = !lean_is_exclusive(v_B_1223_);
if (v_isSharedCheck_1293_ == 0)
{
v___x_1243_ = v_B_1223_;
v_isShared_1244_ = v_isSharedCheck_1293_;
goto v_resetjp_1242_;
}
else
{
lean_inc(v_m22_1241_);
lean_inc(v_m21_1240_);
lean_inc(v_m20_1239_);
lean_inc(v_m12_1238_);
lean_inc(v_m11_1237_);
lean_inc(v_m10_1236_);
lean_inc(v_m02_1235_);
lean_inc(v_m01_1234_);
lean_inc(v_m00_1233_);
lean_dec(v_B_1223_);
v___x_1243_ = lean_box(0);
v_isShared_1244_ = v_isSharedCheck_1293_;
goto v_resetjp_1242_;
}
v_resetjp_1242_:
{
lean_object* v___x_1245_; lean_object* v___x_1246_; lean_object* v___x_1247_; lean_object* v___x_1248_; lean_object* v___x_1249_; lean_object* v___x_1250_; lean_object* v___x_1251_; lean_object* v___x_1252_; lean_object* v___x_1253_; lean_object* v___x_1254_; lean_object* v___x_1255_; lean_object* v___x_1256_; lean_object* v___x_1257_; lean_object* v___x_1258_; lean_object* v___x_1259_; lean_object* v___x_1260_; lean_object* v___x_1261_; lean_object* v___x_1262_; lean_object* v___x_1263_; lean_object* v___x_1264_; lean_object* v___x_1265_; lean_object* v___x_1266_; lean_object* v___x_1267_; lean_object* v___x_1268_; lean_object* v___x_1269_; lean_object* v___x_1270_; lean_object* v___x_1271_; lean_object* v___x_1272_; lean_object* v___x_1273_; lean_object* v___x_1274_; lean_object* v___x_1275_; lean_object* v___x_1276_; lean_object* v___x_1277_; lean_object* v___x_1278_; lean_object* v___x_1279_; lean_object* v___x_1280_; lean_object* v___x_1281_; lean_object* v___x_1282_; lean_object* v___x_1283_; lean_object* v___x_1284_; lean_object* v___x_1285_; lean_object* v___x_1286_; lean_object* v___x_1287_; lean_object* v___x_1288_; lean_object* v___x_1289_; lean_object* v___x_1291_; 
lean_inc_ref_n(v_m00_1233_, 2);
v___x_1245_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m00_1224_, v_m00_1233_);
lean_inc_ref_n(v_m10_1236_, 2);
v___x_1246_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m01_1225_, v_m10_1236_);
v___x_1247_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1245_, v___x_1246_);
lean_dec_ref(v___x_1245_);
lean_inc_ref_n(v_m20_1239_, 2);
v___x_1248_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m02_1226_, v_m20_1239_);
v___x_1249_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1247_, v___x_1248_);
lean_dec_ref(v___x_1247_);
lean_inc_ref_n(v_m01_1234_, 2);
v___x_1250_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m00_1224_, v_m01_1234_);
lean_inc_ref_n(v_m11_1237_, 2);
v___x_1251_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m01_1225_, v_m11_1237_);
v___x_1252_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1250_, v___x_1251_);
lean_dec_ref(v___x_1250_);
lean_inc_ref_n(v_m21_1240_, 2);
v___x_1253_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m02_1226_, v_m21_1240_);
v___x_1254_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1252_, v___x_1253_);
lean_dec_ref(v___x_1252_);
lean_inc_ref_n(v_m02_1235_, 2);
v___x_1255_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m00_1224_, v_m02_1235_);
lean_inc_ref_n(v_m12_1238_, 2);
v___x_1256_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m01_1225_, v_m12_1238_);
v___x_1257_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1255_, v___x_1256_);
lean_dec_ref(v___x_1255_);
lean_inc_ref_n(v_m22_1241_, 2);
v___x_1258_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m02_1226_, v_m22_1241_);
v___x_1259_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1257_, v___x_1258_);
lean_dec_ref(v___x_1257_);
v___x_1260_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m10_1227_, v_m00_1233_);
v___x_1261_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m11_1228_, v_m10_1236_);
v___x_1262_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1260_, v___x_1261_);
lean_dec_ref(v___x_1260_);
v___x_1263_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m12_1229_, v_m20_1239_);
v___x_1264_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1262_, v___x_1263_);
lean_dec_ref(v___x_1262_);
v___x_1265_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m10_1227_, v_m01_1234_);
v___x_1266_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m11_1228_, v_m11_1237_);
v___x_1267_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1265_, v___x_1266_);
lean_dec_ref(v___x_1265_);
v___x_1268_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m12_1229_, v_m21_1240_);
v___x_1269_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1267_, v___x_1268_);
lean_dec_ref(v___x_1267_);
v___x_1270_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m10_1227_, v_m02_1235_);
v___x_1271_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m11_1228_, v_m12_1238_);
v___x_1272_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1270_, v___x_1271_);
lean_dec_ref(v___x_1270_);
v___x_1273_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m12_1229_, v_m22_1241_);
v___x_1274_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1272_, v___x_1273_);
lean_dec_ref(v___x_1272_);
v___x_1275_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m20_1230_, v_m00_1233_);
v___x_1276_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m21_1231_, v_m10_1236_);
v___x_1277_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1275_, v___x_1276_);
lean_dec_ref(v___x_1275_);
v___x_1278_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m22_1232_, v_m20_1239_);
v___x_1279_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1277_, v___x_1278_);
lean_dec_ref(v___x_1277_);
v___x_1280_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m20_1230_, v_m01_1234_);
v___x_1281_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m21_1231_, v_m11_1237_);
v___x_1282_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1280_, v___x_1281_);
lean_dec_ref(v___x_1280_);
v___x_1283_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m22_1232_, v_m21_1240_);
v___x_1284_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1282_, v___x_1283_);
lean_dec_ref(v___x_1282_);
v___x_1285_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m20_1230_, v_m02_1235_);
v___x_1286_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m21_1231_, v_m12_1238_);
v___x_1287_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1285_, v___x_1286_);
lean_dec_ref(v___x_1285_);
v___x_1288_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_m22_1232_, v_m22_1241_);
v___x_1289_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eadd(v___x_1287_, v___x_1288_);
lean_dec_ref(v___x_1287_);
if (v_isShared_1244_ == 0)
{
lean_ctor_set(v___x_1243_, 8, v___x_1289_);
lean_ctor_set(v___x_1243_, 7, v___x_1284_);
lean_ctor_set(v___x_1243_, 6, v___x_1279_);
lean_ctor_set(v___x_1243_, 5, v___x_1274_);
lean_ctor_set(v___x_1243_, 4, v___x_1269_);
lean_ctor_set(v___x_1243_, 3, v___x_1264_);
lean_ctor_set(v___x_1243_, 2, v___x_1259_);
lean_ctor_set(v___x_1243_, 1, v___x_1254_);
lean_ctor_set(v___x_1243_, 0, v___x_1249_);
v___x_1291_ = v___x_1243_;
goto v_reusejp_1290_;
}
else
{
lean_object* v_reuseFailAlloc_1292_; 
v_reuseFailAlloc_1292_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_1292_, 0, v___x_1249_);
lean_ctor_set(v_reuseFailAlloc_1292_, 1, v___x_1254_);
lean_ctor_set(v_reuseFailAlloc_1292_, 2, v___x_1259_);
lean_ctor_set(v_reuseFailAlloc_1292_, 3, v___x_1264_);
lean_ctor_set(v_reuseFailAlloc_1292_, 4, v___x_1269_);
lean_ctor_set(v_reuseFailAlloc_1292_, 5, v___x_1274_);
lean_ctor_set(v_reuseFailAlloc_1292_, 6, v___x_1279_);
lean_ctor_set(v_reuseFailAlloc_1292_, 7, v___x_1284_);
lean_ctor_set(v_reuseFailAlloc_1292_, 8, v___x_1289_);
v___x_1291_ = v_reuseFailAlloc_1292_;
goto v_reusejp_1290_;
}
v_reusejp_1290_:
{
return v___x_1291_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3E___boxed(lean_object* v_A_1294_, lean_object* v_B_1295_){
_start:
{
lean_object* v_res_1296_; 
v_res_1296_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_mul3E(v_A_1294_, v_B_1295_);
lean_dec_ref(v_A_1294_);
return v_res_1296_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3E(lean_object* v_c_1297_, lean_object* v_A_1298_){
_start:
{
lean_object* v_m00_1299_; lean_object* v_m01_1300_; lean_object* v_m02_1301_; lean_object* v_m10_1302_; lean_object* v_m11_1303_; lean_object* v_m12_1304_; lean_object* v_m20_1305_; lean_object* v_m21_1306_; lean_object* v_m22_1307_; lean_object* v___x_1309_; uint8_t v_isShared_1310_; uint8_t v_isSharedCheck_1323_; 
v_m00_1299_ = lean_ctor_get(v_A_1298_, 0);
v_m01_1300_ = lean_ctor_get(v_A_1298_, 1);
v_m02_1301_ = lean_ctor_get(v_A_1298_, 2);
v_m10_1302_ = lean_ctor_get(v_A_1298_, 3);
v_m11_1303_ = lean_ctor_get(v_A_1298_, 4);
v_m12_1304_ = lean_ctor_get(v_A_1298_, 5);
v_m20_1305_ = lean_ctor_get(v_A_1298_, 6);
v_m21_1306_ = lean_ctor_get(v_A_1298_, 7);
v_m22_1307_ = lean_ctor_get(v_A_1298_, 8);
v_isSharedCheck_1323_ = !lean_is_exclusive(v_A_1298_);
if (v_isSharedCheck_1323_ == 0)
{
v___x_1309_ = v_A_1298_;
v_isShared_1310_ = v_isSharedCheck_1323_;
goto v_resetjp_1308_;
}
else
{
lean_inc(v_m22_1307_);
lean_inc(v_m21_1306_);
lean_inc(v_m20_1305_);
lean_inc(v_m12_1304_);
lean_inc(v_m11_1303_);
lean_inc(v_m10_1302_);
lean_inc(v_m02_1301_);
lean_inc(v_m01_1300_);
lean_inc(v_m00_1299_);
lean_dec(v_A_1298_);
v___x_1309_ = lean_box(0);
v_isShared_1310_ = v_isSharedCheck_1323_;
goto v_resetjp_1308_;
}
v_resetjp_1308_:
{
lean_object* v___x_1311_; lean_object* v___x_1312_; lean_object* v___x_1313_; lean_object* v___x_1314_; lean_object* v___x_1315_; lean_object* v___x_1316_; lean_object* v___x_1317_; lean_object* v___x_1318_; lean_object* v___x_1319_; lean_object* v___x_1321_; 
v___x_1311_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m00_1299_);
v___x_1312_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m01_1300_);
v___x_1313_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m02_1301_);
v___x_1314_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m10_1302_);
v___x_1315_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m11_1303_);
v___x_1316_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m12_1304_);
v___x_1317_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m20_1305_);
v___x_1318_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m21_1306_);
v___x_1319_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_emul(v_c_1297_, v_m22_1307_);
if (v_isShared_1310_ == 0)
{
lean_ctor_set(v___x_1309_, 8, v___x_1319_);
lean_ctor_set(v___x_1309_, 7, v___x_1318_);
lean_ctor_set(v___x_1309_, 6, v___x_1317_);
lean_ctor_set(v___x_1309_, 5, v___x_1316_);
lean_ctor_set(v___x_1309_, 4, v___x_1315_);
lean_ctor_set(v___x_1309_, 3, v___x_1314_);
lean_ctor_set(v___x_1309_, 2, v___x_1313_);
lean_ctor_set(v___x_1309_, 1, v___x_1312_);
lean_ctor_set(v___x_1309_, 0, v___x_1311_);
v___x_1321_ = v___x_1309_;
goto v_reusejp_1320_;
}
else
{
lean_object* v_reuseFailAlloc_1322_; 
v_reuseFailAlloc_1322_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v_reuseFailAlloc_1322_, 0, v___x_1311_);
lean_ctor_set(v_reuseFailAlloc_1322_, 1, v___x_1312_);
lean_ctor_set(v_reuseFailAlloc_1322_, 2, v___x_1313_);
lean_ctor_set(v_reuseFailAlloc_1322_, 3, v___x_1314_);
lean_ctor_set(v_reuseFailAlloc_1322_, 4, v___x_1315_);
lean_ctor_set(v_reuseFailAlloc_1322_, 5, v___x_1316_);
lean_ctor_set(v_reuseFailAlloc_1322_, 6, v___x_1317_);
lean_ctor_set(v_reuseFailAlloc_1322_, 7, v___x_1318_);
lean_ctor_set(v_reuseFailAlloc_1322_, 8, v___x_1319_);
v___x_1321_ = v_reuseFailAlloc_1322_;
goto v_reusejp_1320_;
}
v_reusejp_1320_:
{
return v___x_1321_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3E___boxed(lean_object* v_c_1324_, lean_object* v_A_1325_){
_start:
{
lean_object* v_res_1326_; 
v_res_1326_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_smul3E(v_c_1324_, v_A_1325_);
lean_dec_ref(v_c_1324_);
return v_res_1326_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E___closed__0(void){
_start:
{
lean_object* v___x_1327_; lean_object* v___x_1328_; lean_object* v___x_1329_; 
v___x_1327_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez;
v___x_1328_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone;
v___x_1329_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_1329_, 0, v___x_1328_);
lean_ctor_set(v___x_1329_, 1, v___x_1327_);
lean_ctor_set(v___x_1329_, 2, v___x_1327_);
lean_ctor_set(v___x_1329_, 3, v___x_1327_);
lean_ctor_set(v___x_1329_, 4, v___x_1328_);
lean_ctor_set(v___x_1329_, 5, v___x_1327_);
lean_ctor_set(v___x_1329_, 6, v___x_1327_);
lean_ctor_set(v___x_1329_, 7, v___x_1327_);
lean_ctor_set(v___x_1329_, 8, v___x_1328_);
return v___x_1329_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E(void){
_start:
{
lean_object* v___x_1330_; 
v___x_1330_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E___closed__0);
return v___x_1330_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3___closed__0(void){
_start:
{
lean_object* v___x_1331_; lean_object* v___x_1332_; lean_object* v___x_1333_; 
v___x_1331_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone;
v___x_1332_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez;
v___x_1333_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_1333_, 0, v___x_1332_);
lean_ctor_set(v___x_1333_, 1, v___x_1332_);
lean_ctor_set(v___x_1333_, 2, v___x_1331_);
lean_ctor_set(v___x_1333_, 3, v___x_1331_);
lean_ctor_set(v___x_1333_, 4, v___x_1332_);
lean_ctor_set(v___x_1333_, 5, v___x_1332_);
lean_ctor_set(v___x_1333_, 6, v___x_1332_);
lean_ctor_set(v___x_1333_, 7, v___x_1331_);
lean_ctor_set(v___x_1333_, 8, v___x_1332_);
return v___x_1333_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3(void){
_start:
{
lean_object* v___x_1334_; 
v___x_1334_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3___closed__0);
return v___x_1334_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3___closed__0(void){
_start:
{
lean_object* v___x_1335_; lean_object* v___x_1336_; lean_object* v___x_1337_; lean_object* v___x_1338_; lean_object* v___x_1339_; 
v___x_1335_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2;
v___x_1336_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega;
v___x_1337_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez;
v___x_1338_ = lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone;
v___x_1339_ = lean_alloc_ctor(0, 9, 0);
lean_ctor_set(v___x_1339_, 0, v___x_1338_);
lean_ctor_set(v___x_1339_, 1, v___x_1337_);
lean_ctor_set(v___x_1339_, 2, v___x_1337_);
lean_ctor_set(v___x_1339_, 3, v___x_1337_);
lean_ctor_set(v___x_1339_, 4, v___x_1336_);
lean_ctor_set(v___x_1339_, 5, v___x_1337_);
lean_ctor_set(v___x_1339_, 6, v___x_1337_);
lean_ctor_set(v___x_1339_, 7, v___x_1337_);
lean_ctor_set(v___x_1339_, 8, v___x_1335_);
return v___x_1339_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3(void){
_start:
{
lean_object* v___x_1340_; 
v___x_1340_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3___closed__0);
return v___x_1340_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H068WeylCcrResidual(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye2);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift2);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock2);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_ez);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_eone);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_eomega2);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_instZeroEisenstein = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instZeroEisenstein();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instZeroEisenstein);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_instOneEisenstein = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_instOneEisenstein();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_instOneEisenstein);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_eye3E);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_X__shift3);
lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H068_Z__clock3);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
