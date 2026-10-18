// Lean compiler output
// Module: H045DiscreteGroverSearch
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
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "a"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "b"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__16_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instZeroQuad3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instOneQuad3;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instAddQuad3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instAddQuad3___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instAddQuad3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instAddQuad3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instAddQuad3___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instSubQuad3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instSubQuad3___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instSubQuad3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instSubQuad3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instSubQuad3___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instMulQuad3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instMulQuad3___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instMulQuad3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instMulQuad3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instMulQuad3___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v0"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v3"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__6_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__7_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__7_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__8_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "v1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__9_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__9_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__10_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "r0"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "r1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__5_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "r2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__7_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "r3"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__9_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_grover__step(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_grover__step___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "x"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "y"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_rot2d(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_a_3_; lean_object* v_b_4_; lean_object* v_a_5_; lean_object* v_b_6_; uint8_t v___x_7_; 
v_a_3_ = lean_ctor_get(v_x_1_, 0);
v_b_4_ = lean_ctor_get(v_x_1_, 1);
v_a_5_ = lean_ctor_get(v_x_2_, 0);
v_b_6_ = lean_ctor_get(v_x_2_, 1);
v___x_7_ = lean_int_dec_eq(v_a_3_, v_a_5_);
if (v___x_7_ == 0)
{
return v___x_7_;
}
else
{
uint8_t v___x_8_; 
v___x_8_ = lean_int_dec_eq(v_b_4_, v_b_6_);
return v___x_8_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq___boxed(lean_object* v_x_9_, lean_object* v_x_10_){
_start:
{
uint8_t v_res_11_; lean_object* v_r_12_; 
v_res_11_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq(v_x_9_, v_x_10_);
lean_dec_ref(v_x_10_);
lean_dec_ref(v_x_9_);
v_r_12_ = lean_box(v_res_11_);
return v_r_12_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3(lean_object* v_x_13_, lean_object* v_x_14_){
_start:
{
uint8_t v___x_15_; 
v___x_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq(v_x_13_, v_x_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3___boxed(lean_object* v_x_16_, lean_object* v_x_17_){
_start:
{
uint8_t v_res_18_; lean_object* v_r_19_; 
v_res_18_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3(v_x_16_, v_x_17_);
lean_dec_ref(v_x_17_);
lean_dec_ref(v_x_16_);
v_r_19_ = lean_box(v_res_18_);
return v_r_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_unsigned_to_nat(5u);
v___x_34_ = lean_nat_to_int(v___x_33_);
return v___x_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_36_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__0));
v___x_37_ = lean_string_length(v___x_36_);
return v___x_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__9);
v___x_39_ = lean_nat_to_int(v___x_38_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_50_ = lean_unsigned_to_nat(0u);
v___x_51_ = lean_nat_to_int(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg(lean_object* v_x_52_){
_start:
{
lean_object* v_a_53_; lean_object* v_b_54_; lean_object* v___x_56_; uint8_t v_isShared_57_; uint8_t v_isSharedCheck_106_; 
v_a_53_ = lean_ctor_get(v_x_52_, 0);
v_b_54_ = lean_ctor_get(v_x_52_, 1);
v_isSharedCheck_106_ = !lean_is_exclusive(v_x_52_);
if (v_isSharedCheck_106_ == 0)
{
v___x_56_ = v_x_52_;
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
else
{
lean_inc(v_b_54_);
lean_inc(v_a_53_);
lean_dec(v_x_52_);
v___x_56_ = lean_box(0);
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
v_resetjp_55_:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___y_62_; uint8_t v___y_63_; lean_object* v___y_64_; lean_object* v___y_78_; lean_object* v___x_98_; lean_object* v___x_99_; uint8_t v___x_100_; 
v___x_58_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5));
v___x_59_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__6));
v___x_60_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7);
v___x_98_ = lean_unsigned_to_nat(0u);
v___x_99_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_100_ = lean_int_dec_lt(v_a_53_, v___x_99_);
if (v___x_100_ == 0)
{
lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_101_ = l_Int_repr(v_a_53_);
lean_dec(v_a_53_);
v___x_102_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_102_, 0, v___x_101_);
v___y_78_ = v___x_102_;
goto v___jp_77_;
}
else
{
lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; 
v___x_103_ = l_Int_repr(v_a_53_);
lean_dec(v_a_53_);
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
v___x_69_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10);
v___x_70_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11));
v___x_71_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_71_, 0, v___x_70_);
lean_ctor_set(v___x_71_, 1, v___x_68_);
v___x_72_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12));
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
v___x_83_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14));
v___x_84_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_84_, 0, v___x_82_);
lean_ctor_set(v___x_84_, 1, v___x_83_);
v___x_85_ = lean_box(1);
v___x_86_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_84_);
lean_ctor_set(v___x_86_, 1, v___x_85_);
v___x_87_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__16));
v___x_88_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_88_, 0, v___x_86_);
lean_ctor_set(v___x_88_, 1, v___x_87_);
v___x_89_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_88_);
lean_ctor_set(v___x_89_, 1, v___x_58_);
v___x_90_ = lean_unsigned_to_nat(0u);
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_92_ = lean_int_dec_lt(v_b_54_, v___x_91_);
if (v___x_92_ == 0)
{
lean_object* v___x_93_; lean_object* v___x_94_; 
v___x_93_ = l_Int_repr(v_b_54_);
lean_dec(v_b_54_);
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
v___x_95_ = l_Int_repr(v_b_54_);
lean_dec(v_b_54_);
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr(lean_object* v_x_107_, lean_object* v_prec_108_){
_start:
{
lean_object* v___x_109_; 
v___x_109_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg(v_x_107_);
return v___x_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___boxed(lean_object* v_x_110_, lean_object* v_prec_111_){
_start:
{
lean_object* v_res_112_; 
v_res_112_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr(v_x_110_, v_prec_111_);
lean_dec(v_prec_111_);
return v_res_112_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz___closed__0(void){
_start:
{
lean_object* v___x_115_; lean_object* v___x_116_; 
v___x_115_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_116_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_116_, 0, v___x_115_);
lean_ctor_set(v___x_116_, 1, v___x_115_);
return v___x_116_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz(void){
_start:
{
lean_object* v___x_117_; 
v___x_117_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz___closed__0);
return v___x_117_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(1u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; 
v___x_120_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_121_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_122_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_122_, 0, v___x_121_);
lean_ctor_set(v___x_122_, 1, v___x_120_);
return v___x_122_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone(void){
_start:
{
lean_object* v___x_123_; 
v___x_123_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1);
return v___x_123_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0(void){
_start:
{
lean_object* v___x_124_; lean_object* v___x_125_; lean_object* v___x_126_; 
v___x_124_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_125_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_126_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_126_, 0, v___x_125_);
lean_ctor_set(v___x_126_, 1, v___x_124_);
return v___x_126_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3(void){
_start:
{
lean_object* v___x_127_; 
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0);
return v___x_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd(lean_object* v_x_128_, lean_object* v_y_129_){
_start:
{
lean_object* v_a_130_; lean_object* v_b_131_; lean_object* v_a_132_; lean_object* v_b_133_; lean_object* v___x_135_; uint8_t v_isShared_136_; uint8_t v_isSharedCheck_142_; 
v_a_130_ = lean_ctor_get(v_x_128_, 0);
v_b_131_ = lean_ctor_get(v_x_128_, 1);
v_a_132_ = lean_ctor_get(v_y_129_, 0);
v_b_133_ = lean_ctor_get(v_y_129_, 1);
v_isSharedCheck_142_ = !lean_is_exclusive(v_y_129_);
if (v_isSharedCheck_142_ == 0)
{
v___x_135_ = v_y_129_;
v_isShared_136_ = v_isSharedCheck_142_;
goto v_resetjp_134_;
}
else
{
lean_inc(v_b_133_);
lean_inc(v_a_132_);
lean_dec(v_y_129_);
v___x_135_ = lean_box(0);
v_isShared_136_ = v_isSharedCheck_142_;
goto v_resetjp_134_;
}
v_resetjp_134_:
{
lean_object* v___x_137_; lean_object* v___x_138_; lean_object* v___x_140_; 
v___x_137_ = lean_int_add(v_a_130_, v_a_132_);
lean_dec(v_a_132_);
v___x_138_ = lean_int_add(v_b_131_, v_b_133_);
lean_dec(v_b_133_);
if (v_isShared_136_ == 0)
{
lean_ctor_set(v___x_135_, 1, v___x_138_);
lean_ctor_set(v___x_135_, 0, v___x_137_);
v___x_140_ = v___x_135_;
goto v_reusejp_139_;
}
else
{
lean_object* v_reuseFailAlloc_141_; 
v_reuseFailAlloc_141_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_141_, 0, v___x_137_);
lean_ctor_set(v_reuseFailAlloc_141_, 1, v___x_138_);
v___x_140_ = v_reuseFailAlloc_141_;
goto v_reusejp_139_;
}
v_reusejp_139_:
{
return v___x_140_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd___boxed(lean_object* v_x_143_, lean_object* v_y_144_){
_start:
{
lean_object* v_res_145_; 
v_res_145_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd(v_x_143_, v_y_144_);
lean_dec_ref(v_x_143_);
return v_res_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub(lean_object* v_x_146_, lean_object* v_y_147_){
_start:
{
lean_object* v_a_148_; lean_object* v_b_149_; lean_object* v_a_150_; lean_object* v_b_151_; lean_object* v___x_153_; uint8_t v_isShared_154_; uint8_t v_isSharedCheck_160_; 
v_a_148_ = lean_ctor_get(v_x_146_, 0);
v_b_149_ = lean_ctor_get(v_x_146_, 1);
v_a_150_ = lean_ctor_get(v_y_147_, 0);
v_b_151_ = lean_ctor_get(v_y_147_, 1);
v_isSharedCheck_160_ = !lean_is_exclusive(v_y_147_);
if (v_isSharedCheck_160_ == 0)
{
v___x_153_ = v_y_147_;
v_isShared_154_ = v_isSharedCheck_160_;
goto v_resetjp_152_;
}
else
{
lean_inc(v_b_151_);
lean_inc(v_a_150_);
lean_dec(v_y_147_);
v___x_153_ = lean_box(0);
v_isShared_154_ = v_isSharedCheck_160_;
goto v_resetjp_152_;
}
v_resetjp_152_:
{
lean_object* v___x_155_; lean_object* v___x_156_; lean_object* v___x_158_; 
v___x_155_ = lean_int_sub(v_a_148_, v_a_150_);
lean_dec(v_a_150_);
v___x_156_ = lean_int_sub(v_b_149_, v_b_151_);
lean_dec(v_b_151_);
if (v_isShared_154_ == 0)
{
lean_ctor_set(v___x_153_, 1, v___x_156_);
lean_ctor_set(v___x_153_, 0, v___x_155_);
v___x_158_ = v___x_153_;
goto v_reusejp_157_;
}
else
{
lean_object* v_reuseFailAlloc_159_; 
v_reuseFailAlloc_159_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_159_, 0, v___x_155_);
lean_ctor_set(v_reuseFailAlloc_159_, 1, v___x_156_);
v___x_158_ = v_reuseFailAlloc_159_;
goto v_reusejp_157_;
}
v_reusejp_157_:
{
return v___x_158_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub___boxed(lean_object* v_x_161_, lean_object* v_y_162_){
_start:
{
lean_object* v_res_163_; 
v_res_163_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub(v_x_161_, v_y_162_);
lean_dec_ref(v_x_161_);
return v_res_163_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___closed__0(void){
_start:
{
lean_object* v___x_164_; lean_object* v___x_165_; 
v___x_164_ = lean_unsigned_to_nat(3u);
v___x_165_ = lean_nat_to_int(v___x_164_);
return v___x_165_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(lean_object* v_x_166_, lean_object* v_y_167_){
_start:
{
lean_object* v_a_168_; lean_object* v_b_169_; lean_object* v_a_170_; lean_object* v_b_171_; lean_object* v___x_173_; uint8_t v_isShared_174_; uint8_t v_isSharedCheck_186_; 
v_a_168_ = lean_ctor_get(v_x_166_, 0);
v_b_169_ = lean_ctor_get(v_x_166_, 1);
v_a_170_ = lean_ctor_get(v_y_167_, 0);
v_b_171_ = lean_ctor_get(v_y_167_, 1);
v_isSharedCheck_186_ = !lean_is_exclusive(v_y_167_);
if (v_isSharedCheck_186_ == 0)
{
v___x_173_ = v_y_167_;
v_isShared_174_ = v_isSharedCheck_186_;
goto v_resetjp_172_;
}
else
{
lean_inc(v_b_171_);
lean_inc(v_a_170_);
lean_dec(v_y_167_);
v___x_173_ = lean_box(0);
v_isShared_174_ = v_isSharedCheck_186_;
goto v_resetjp_172_;
}
v_resetjp_172_:
{
lean_object* v___x_175_; lean_object* v___x_176_; lean_object* v___x_177_; lean_object* v___x_178_; lean_object* v___x_179_; lean_object* v___x_180_; lean_object* v___x_181_; lean_object* v___x_182_; lean_object* v___x_184_; 
v___x_175_ = lean_int_mul(v_a_168_, v_a_170_);
v___x_176_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___closed__0);
v___x_177_ = lean_int_mul(v___x_176_, v_b_169_);
v___x_178_ = lean_int_mul(v___x_177_, v_b_171_);
lean_dec(v___x_177_);
v___x_179_ = lean_int_add(v___x_175_, v___x_178_);
lean_dec(v___x_178_);
lean_dec(v___x_175_);
v___x_180_ = lean_int_mul(v_a_168_, v_b_171_);
lean_dec(v_b_171_);
v___x_181_ = lean_int_mul(v_b_169_, v_a_170_);
lean_dec(v_a_170_);
v___x_182_ = lean_int_add(v___x_180_, v___x_181_);
lean_dec(v___x_181_);
lean_dec(v___x_180_);
if (v_isShared_174_ == 0)
{
lean_ctor_set(v___x_173_, 1, v___x_182_);
lean_ctor_set(v___x_173_, 0, v___x_179_);
v___x_184_ = v___x_173_;
goto v_reusejp_183_;
}
else
{
lean_object* v_reuseFailAlloc_185_; 
v_reuseFailAlloc_185_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_185_, 0, v___x_179_);
lean_ctor_set(v_reuseFailAlloc_185_, 1, v___x_182_);
v___x_184_ = v_reuseFailAlloc_185_;
goto v_reusejp_183_;
}
v_reusejp_183_:
{
return v___x_184_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul___boxed(lean_object* v_x_187_, lean_object* v_y_188_){
_start:
{
lean_object* v_res_189_; 
v_res_189_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(v_x_187_, v_y_188_);
lean_dec_ref(v_x_187_);
return v_res_189_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsmul(lean_object* v_c_190_, lean_object* v_x_191_){
_start:
{
lean_object* v_a_192_; lean_object* v_b_193_; lean_object* v___x_195_; uint8_t v_isShared_196_; uint8_t v_isSharedCheck_202_; 
v_a_192_ = lean_ctor_get(v_x_191_, 0);
v_b_193_ = lean_ctor_get(v_x_191_, 1);
v_isSharedCheck_202_ = !lean_is_exclusive(v_x_191_);
if (v_isSharedCheck_202_ == 0)
{
v___x_195_ = v_x_191_;
v_isShared_196_ = v_isSharedCheck_202_;
goto v_resetjp_194_;
}
else
{
lean_inc(v_b_193_);
lean_inc(v_a_192_);
lean_dec(v_x_191_);
v___x_195_ = lean_box(0);
v_isShared_196_ = v_isSharedCheck_202_;
goto v_resetjp_194_;
}
v_resetjp_194_:
{
lean_object* v___x_197_; lean_object* v___x_198_; lean_object* v___x_200_; 
v___x_197_ = lean_int_mul(v_c_190_, v_a_192_);
lean_dec(v_a_192_);
v___x_198_ = lean_int_mul(v_c_190_, v_b_193_);
lean_dec(v_b_193_);
if (v_isShared_196_ == 0)
{
lean_ctor_set(v___x_195_, 1, v___x_198_);
lean_ctor_set(v___x_195_, 0, v___x_197_);
v___x_200_ = v___x_195_;
goto v_reusejp_199_;
}
else
{
lean_object* v_reuseFailAlloc_201_; 
v_reuseFailAlloc_201_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_201_, 0, v___x_197_);
lean_ctor_set(v_reuseFailAlloc_201_, 1, v___x_198_);
v___x_200_ = v_reuseFailAlloc_201_;
goto v_reusejp_199_;
}
v_reusejp_199_:
{
return v___x_200_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsmul___boxed(lean_object* v_c_203_, lean_object* v_x_204_){
_start:
{
lean_object* v_res_205_; 
v_res_205_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsmul(v_c_203_, v_x_204_);
lean_dec(v_c_203_);
return v_res_205_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instZeroQuad3(void){
_start:
{
lean_object* v___x_206_; 
v___x_206_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz;
return v___x_206_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instOneQuad3(void){
_start:
{
lean_object* v___x_207_; 
v___x_207_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone;
return v___x_207_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(lean_object* v_x_214_, lean_object* v_x_215_){
_start:
{
lean_object* v_v0_216_; lean_object* v_v1_217_; lean_object* v_v2_218_; lean_object* v_v3_219_; lean_object* v_v0_220_; lean_object* v_v1_221_; lean_object* v_v2_222_; lean_object* v_v3_223_; uint8_t v___x_224_; 
v_v0_216_ = lean_ctor_get(v_x_214_, 0);
v_v1_217_ = lean_ctor_get(v_x_214_, 1);
v_v2_218_ = lean_ctor_get(v_x_214_, 2);
v_v3_219_ = lean_ctor_get(v_x_214_, 3);
v_v0_220_ = lean_ctor_get(v_x_215_, 0);
v_v1_221_ = lean_ctor_get(v_x_215_, 1);
v_v2_222_ = lean_ctor_get(v_x_215_, 2);
v_v3_223_ = lean_ctor_get(v_x_215_, 3);
v___x_224_ = lean_int_dec_eq(v_v0_216_, v_v0_220_);
if (v___x_224_ == 0)
{
return v___x_224_;
}
else
{
uint8_t v___x_225_; 
v___x_225_ = lean_int_dec_eq(v_v1_217_, v_v1_221_);
if (v___x_225_ == 0)
{
return v___x_225_;
}
else
{
uint8_t v___x_226_; 
v___x_226_ = lean_int_dec_eq(v_v2_218_, v_v2_222_);
if (v___x_226_ == 0)
{
return v___x_226_;
}
else
{
uint8_t v___x_227_; 
v___x_227_ = lean_int_dec_eq(v_v3_219_, v_v3_223_);
return v___x_227_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq___boxed(lean_object* v_x_228_, lean_object* v_x_229_){
_start:
{
uint8_t v_res_230_; lean_object* v_r_231_; 
v_res_230_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(v_x_228_, v_x_229_);
lean_dec_ref(v_x_229_);
lean_dec_ref(v_x_228_);
v_r_231_ = lean_box(v_res_230_);
return v_r_231_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4(lean_object* v_x_232_, lean_object* v_x_233_){
_start:
{
uint8_t v___x_234_; 
v___x_234_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(v_x_232_, v_x_233_);
return v___x_234_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4___boxed(lean_object* v_x_235_, lean_object* v_x_236_){
_start:
{
uint8_t v_res_237_; lean_object* v_r_238_; 
v_res_237_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4(v_x_235_, v_x_236_);
lean_dec_ref(v_x_236_);
lean_dec_ref(v_x_235_);
v_r_238_ = lean_box(v_res_237_);
return v_r_238_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_248_; lean_object* v___x_249_; 
v___x_248_ = lean_unsigned_to_nat(6u);
v___x_249_ = lean_nat_to_int(v___x_248_);
return v___x_249_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(lean_object* v_x_259_){
_start:
{
lean_object* v_v0_260_; lean_object* v_v1_261_; lean_object* v_v2_262_; lean_object* v_v3_263_; lean_object* v___x_264_; lean_object* v___x_265_; lean_object* v___x_266_; lean_object* v___y_268_; uint8_t v___y_269_; lean_object* v___y_270_; lean_object* v___y_282_; lean_object* v___y_283_; uint8_t v___y_284_; lean_object* v___y_285_; lean_object* v___y_286_; lean_object* v___y_304_; lean_object* v___y_305_; uint8_t v___y_306_; lean_object* v___y_307_; lean_object* v___y_308_; lean_object* v___y_326_; lean_object* v___x_346_; lean_object* v___x_347_; uint8_t v___x_348_; 
v_v0_260_ = lean_ctor_get(v_x_259_, 0);
v_v1_261_ = lean_ctor_get(v_x_259_, 1);
v_v2_262_ = lean_ctor_get(v_x_259_, 2);
v_v3_263_ = lean_ctor_get(v_x_259_, 3);
v___x_264_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5));
v___x_265_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__3));
v___x_266_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4);
v___x_346_ = lean_unsigned_to_nat(0u);
v___x_347_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_348_ = lean_int_dec_lt(v_v0_260_, v___x_347_);
if (v___x_348_ == 0)
{
lean_object* v___x_349_; lean_object* v___x_350_; 
v___x_349_ = l_Int_repr(v_v0_260_);
v___x_350_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_350_, 0, v___x_349_);
v___y_326_ = v___x_350_;
goto v___jp_325_;
}
else
{
lean_object* v___x_351_; lean_object* v___x_352_; lean_object* v___x_353_; 
v___x_351_ = l_Int_repr(v_v0_260_);
v___x_352_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_352_, 0, v___x_351_);
v___x_353_ = l_Repr_addAppParen(v___x_352_, v___x_346_);
v___y_326_ = v___x_353_;
goto v___jp_325_;
}
v___jp_267_:
{
lean_object* v___x_271_; lean_object* v___x_272_; lean_object* v___x_273_; lean_object* v___x_274_; lean_object* v___x_275_; lean_object* v___x_276_; lean_object* v___x_277_; lean_object* v___x_278_; lean_object* v___x_279_; lean_object* v___x_280_; 
v___x_271_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_271_, 0, v___x_266_);
lean_ctor_set(v___x_271_, 1, v___y_270_);
v___x_272_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_272_, 0, v___x_271_);
lean_ctor_set_uint8(v___x_272_, sizeof(void*)*1, v___y_269_);
v___x_273_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_273_, 0, v___y_268_);
lean_ctor_set(v___x_273_, 1, v___x_272_);
v___x_274_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10);
v___x_275_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11));
v___x_276_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_276_, 0, v___x_275_);
lean_ctor_set(v___x_276_, 1, v___x_273_);
v___x_277_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12));
v___x_278_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_278_, 0, v___x_276_);
lean_ctor_set(v___x_278_, 1, v___x_277_);
v___x_279_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_279_, 0, v___x_274_);
lean_ctor_set(v___x_279_, 1, v___x_278_);
v___x_280_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_280_, 0, v___x_279_);
lean_ctor_set_uint8(v___x_280_, sizeof(void*)*1, v___y_269_);
return v___x_280_;
}
v___jp_281_:
{
lean_object* v___x_287_; lean_object* v___x_288_; lean_object* v___x_289_; lean_object* v___x_290_; lean_object* v___x_291_; lean_object* v___x_292_; lean_object* v___x_293_; lean_object* v___x_294_; lean_object* v___x_295_; lean_object* v___x_296_; uint8_t v___x_297_; 
v___x_287_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_287_, 0, v___x_266_);
lean_ctor_set(v___x_287_, 1, v___y_286_);
v___x_288_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_288_, 0, v___x_287_);
lean_ctor_set_uint8(v___x_288_, sizeof(void*)*1, v___y_284_);
v___x_289_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_289_, 0, v___y_285_);
lean_ctor_set(v___x_289_, 1, v___x_288_);
lean_inc(v___y_282_);
v___x_290_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_290_, 0, v___x_289_);
lean_ctor_set(v___x_290_, 1, v___y_282_);
lean_inc(v___y_283_);
v___x_291_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_291_, 0, v___x_290_);
lean_ctor_set(v___x_291_, 1, v___y_283_);
v___x_292_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__6));
v___x_293_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_293_, 0, v___x_291_);
lean_ctor_set(v___x_293_, 1, v___x_292_);
v___x_294_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_294_, 0, v___x_293_);
lean_ctor_set(v___x_294_, 1, v___x_264_);
v___x_295_ = lean_unsigned_to_nat(0u);
v___x_296_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_297_ = lean_int_dec_lt(v_v3_263_, v___x_296_);
if (v___x_297_ == 0)
{
lean_object* v___x_298_; lean_object* v___x_299_; 
v___x_298_ = l_Int_repr(v_v3_263_);
v___x_299_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_299_, 0, v___x_298_);
v___y_268_ = v___x_294_;
v___y_269_ = v___y_284_;
v___y_270_ = v___x_299_;
goto v___jp_267_;
}
else
{
lean_object* v___x_300_; lean_object* v___x_301_; lean_object* v___x_302_; 
v___x_300_ = l_Int_repr(v_v3_263_);
v___x_301_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_301_, 0, v___x_300_);
v___x_302_ = l_Repr_addAppParen(v___x_301_, v___x_295_);
v___y_268_ = v___x_294_;
v___y_269_ = v___y_284_;
v___y_270_ = v___x_302_;
goto v___jp_267_;
}
}
v___jp_303_:
{
lean_object* v___x_309_; lean_object* v___x_310_; lean_object* v___x_311_; lean_object* v___x_312_; lean_object* v___x_313_; lean_object* v___x_314_; lean_object* v___x_315_; lean_object* v___x_316_; lean_object* v___x_317_; lean_object* v___x_318_; uint8_t v___x_319_; 
v___x_309_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_309_, 0, v___x_266_);
lean_ctor_set(v___x_309_, 1, v___y_308_);
v___x_310_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_310_, 0, v___x_309_);
lean_ctor_set_uint8(v___x_310_, sizeof(void*)*1, v___y_306_);
v___x_311_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_311_, 0, v___y_307_);
lean_ctor_set(v___x_311_, 1, v___x_310_);
lean_inc(v___y_304_);
v___x_312_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_312_, 0, v___x_311_);
lean_ctor_set(v___x_312_, 1, v___y_304_);
lean_inc(v___y_305_);
v___x_313_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_313_, 0, v___x_312_);
lean_ctor_set(v___x_313_, 1, v___y_305_);
v___x_314_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__8));
v___x_315_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_315_, 0, v___x_313_);
lean_ctor_set(v___x_315_, 1, v___x_314_);
v___x_316_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_316_, 0, v___x_315_);
lean_ctor_set(v___x_316_, 1, v___x_264_);
v___x_317_ = lean_unsigned_to_nat(0u);
v___x_318_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_319_ = lean_int_dec_lt(v_v2_262_, v___x_318_);
if (v___x_319_ == 0)
{
lean_object* v___x_320_; lean_object* v___x_321_; 
v___x_320_ = l_Int_repr(v_v2_262_);
v___x_321_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_321_, 0, v___x_320_);
v___y_282_ = v___y_304_;
v___y_283_ = v___y_305_;
v___y_284_ = v___y_306_;
v___y_285_ = v___x_316_;
v___y_286_ = v___x_321_;
goto v___jp_281_;
}
else
{
lean_object* v___x_322_; lean_object* v___x_323_; lean_object* v___x_324_; 
v___x_322_ = l_Int_repr(v_v2_262_);
v___x_323_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_323_, 0, v___x_322_);
v___x_324_ = l_Repr_addAppParen(v___x_323_, v___x_317_);
v___y_282_ = v___y_304_;
v___y_283_ = v___y_305_;
v___y_284_ = v___y_306_;
v___y_285_ = v___x_316_;
v___y_286_ = v___x_324_;
goto v___jp_281_;
}
}
v___jp_325_:
{
lean_object* v___x_327_; uint8_t v___x_328_; lean_object* v___x_329_; lean_object* v___x_330_; lean_object* v___x_331_; lean_object* v___x_332_; lean_object* v___x_333_; lean_object* v___x_334_; lean_object* v___x_335_; lean_object* v___x_336_; lean_object* v___x_337_; lean_object* v___x_338_; lean_object* v___x_339_; uint8_t v___x_340_; 
v___x_327_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_327_, 0, v___x_266_);
lean_ctor_set(v___x_327_, 1, v___y_326_);
v___x_328_ = 0;
v___x_329_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_329_, 0, v___x_327_);
lean_ctor_set_uint8(v___x_329_, sizeof(void*)*1, v___x_328_);
v___x_330_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_330_, 0, v___x_265_);
lean_ctor_set(v___x_330_, 1, v___x_329_);
v___x_331_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14));
v___x_332_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_332_, 0, v___x_330_);
lean_ctor_set(v___x_332_, 1, v___x_331_);
v___x_333_ = lean_box(1);
v___x_334_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_334_, 0, v___x_332_);
lean_ctor_set(v___x_334_, 1, v___x_333_);
v___x_335_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__10));
v___x_336_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_336_, 0, v___x_334_);
lean_ctor_set(v___x_336_, 1, v___x_335_);
v___x_337_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_337_, 0, v___x_336_);
lean_ctor_set(v___x_337_, 1, v___x_264_);
v___x_338_ = lean_unsigned_to_nat(0u);
v___x_339_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_340_ = lean_int_dec_lt(v_v1_261_, v___x_339_);
if (v___x_340_ == 0)
{
lean_object* v___x_341_; lean_object* v___x_342_; 
v___x_341_ = l_Int_repr(v_v1_261_);
v___x_342_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_342_, 0, v___x_341_);
v___y_304_ = v___x_331_;
v___y_305_ = v___x_333_;
v___y_306_ = v___x_328_;
v___y_307_ = v___x_337_;
v___y_308_ = v___x_342_;
goto v___jp_303_;
}
else
{
lean_object* v___x_343_; lean_object* v___x_344_; lean_object* v___x_345_; 
v___x_343_ = l_Int_repr(v_v1_261_);
v___x_344_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_344_, 0, v___x_343_);
v___x_345_ = l_Repr_addAppParen(v___x_344_, v___x_338_);
v___y_304_ = v___x_331_;
v___y_305_ = v___x_333_;
v___y_306_ = v___x_328_;
v___y_307_ = v___x_337_;
v___y_308_ = v___x_345_;
goto v___jp_303_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___boxed(lean_object* v_x_354_){
_start:
{
lean_object* v_res_355_; 
v_res_355_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(v_x_354_);
lean_dec_ref(v_x_354_);
return v_res_355_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr(lean_object* v_x_356_, lean_object* v_prec_357_){
_start:
{
lean_object* v___x_358_; 
v___x_358_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(v_x_356_);
return v___x_358_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___boxed(lean_object* v_x_359_, lean_object* v_prec_360_){
_start:
{
lean_object* v_res_361_; 
v_res_361_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr(v_x_359_, v_prec_360_);
lean_dec(v_prec_360_);
lean_dec_ref(v_x_359_);
return v_res_361_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4_decEq(lean_object* v_x_364_, lean_object* v_x_365_){
_start:
{
lean_object* v_r0_366_; lean_object* v_r1_367_; lean_object* v_r2_368_; lean_object* v_r3_369_; lean_object* v_r0_370_; lean_object* v_r1_371_; lean_object* v_r2_372_; lean_object* v_r3_373_; uint8_t v___x_374_; 
v_r0_366_ = lean_ctor_get(v_x_364_, 0);
v_r1_367_ = lean_ctor_get(v_x_364_, 1);
v_r2_368_ = lean_ctor_get(v_x_364_, 2);
v_r3_369_ = lean_ctor_get(v_x_364_, 3);
v_r0_370_ = lean_ctor_get(v_x_365_, 0);
v_r1_371_ = lean_ctor_get(v_x_365_, 1);
v_r2_372_ = lean_ctor_get(v_x_365_, 2);
v_r3_373_ = lean_ctor_get(v_x_365_, 3);
v___x_374_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(v_r0_366_, v_r0_370_);
if (v___x_374_ == 0)
{
return v___x_374_;
}
else
{
uint8_t v___x_375_; 
v___x_375_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(v_r1_367_, v_r1_371_);
if (v___x_375_ == 0)
{
return v___x_375_;
}
else
{
uint8_t v___x_376_; 
v___x_376_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(v_r2_368_, v_r2_372_);
if (v___x_376_ == 0)
{
return v___x_376_;
}
else
{
uint8_t v___x_377_; 
v___x_377_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec4_decEq(v_r3_369_, v_r3_373_);
return v___x_377_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4_decEq___boxed(lean_object* v_x_378_, lean_object* v_x_379_){
_start:
{
uint8_t v_res_380_; lean_object* v_r_381_; 
v_res_380_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4_decEq(v_x_378_, v_x_379_);
lean_dec_ref(v_x_379_);
lean_dec_ref(v_x_378_);
v_r_381_ = lean_box(v_res_380_);
return v_r_381_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4(lean_object* v_x_382_, lean_object* v_x_383_){
_start:
{
uint8_t v___x_384_; 
v___x_384_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4_decEq(v_x_382_, v_x_383_);
return v___x_384_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4___boxed(lean_object* v_x_385_, lean_object* v_x_386_){
_start:
{
uint8_t v_res_387_; lean_object* v_r_388_; 
v_res_387_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqMat4(v_x_385_, v_x_386_);
lean_dec_ref(v_x_386_);
lean_dec_ref(v_x_385_);
v_r_388_ = lean_box(v_res_387_);
return v_r_388_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg(lean_object* v_x_407_){
_start:
{
lean_object* v_r0_408_; lean_object* v_r1_409_; lean_object* v_r2_410_; lean_object* v_r3_411_; lean_object* v___x_412_; lean_object* v___x_413_; lean_object* v___x_414_; lean_object* v___x_415_; lean_object* v___x_416_; uint8_t v___x_417_; lean_object* v___x_418_; lean_object* v___x_419_; lean_object* v___x_420_; lean_object* v___x_421_; lean_object* v___x_422_; lean_object* v___x_423_; lean_object* v___x_424_; lean_object* v___x_425_; lean_object* v___x_426_; lean_object* v___x_427_; lean_object* v___x_428_; lean_object* v___x_429_; lean_object* v___x_430_; lean_object* v___x_431_; lean_object* v___x_432_; lean_object* v___x_433_; lean_object* v___x_434_; lean_object* v___x_435_; lean_object* v___x_436_; lean_object* v___x_437_; lean_object* v___x_438_; lean_object* v___x_439_; lean_object* v___x_440_; lean_object* v___x_441_; lean_object* v___x_442_; lean_object* v___x_443_; lean_object* v___x_444_; lean_object* v___x_445_; lean_object* v___x_446_; lean_object* v___x_447_; lean_object* v___x_448_; lean_object* v___x_449_; lean_object* v___x_450_; lean_object* v___x_451_; lean_object* v___x_452_; lean_object* v___x_453_; lean_object* v___x_454_; lean_object* v___x_455_; 
v_r0_408_ = lean_ctor_get(v_x_407_, 0);
v_r1_409_ = lean_ctor_get(v_x_407_, 1);
v_r2_410_ = lean_ctor_get(v_x_407_, 2);
v_r3_411_ = lean_ctor_get(v_x_407_, 3);
v___x_412_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5));
v___x_413_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__3));
v___x_414_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg___closed__4);
v___x_415_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(v_r0_408_);
v___x_416_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_416_, 0, v___x_414_);
lean_ctor_set(v___x_416_, 1, v___x_415_);
v___x_417_ = 0;
v___x_418_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_418_, 0, v___x_416_);
lean_ctor_set_uint8(v___x_418_, sizeof(void*)*1, v___x_417_);
v___x_419_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_419_, 0, v___x_413_);
lean_ctor_set(v___x_419_, 1, v___x_418_);
v___x_420_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14));
v___x_421_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_421_, 0, v___x_419_);
lean_ctor_set(v___x_421_, 1, v___x_420_);
v___x_422_ = lean_box(1);
v___x_423_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_423_, 0, v___x_421_);
lean_ctor_set(v___x_423_, 1, v___x_422_);
v___x_424_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__5));
v___x_425_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_425_, 0, v___x_423_);
lean_ctor_set(v___x_425_, 1, v___x_424_);
v___x_426_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_426_, 0, v___x_425_);
lean_ctor_set(v___x_426_, 1, v___x_412_);
v___x_427_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(v_r1_409_);
v___x_428_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_428_, 0, v___x_414_);
lean_ctor_set(v___x_428_, 1, v___x_427_);
v___x_429_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_429_, 0, v___x_428_);
lean_ctor_set_uint8(v___x_429_, sizeof(void*)*1, v___x_417_);
v___x_430_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_430_, 0, v___x_426_);
lean_ctor_set(v___x_430_, 1, v___x_429_);
v___x_431_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_431_, 0, v___x_430_);
lean_ctor_set(v___x_431_, 1, v___x_420_);
v___x_432_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_432_, 0, v___x_431_);
lean_ctor_set(v___x_432_, 1, v___x_422_);
v___x_433_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__7));
v___x_434_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_434_, 0, v___x_432_);
lean_ctor_set(v___x_434_, 1, v___x_433_);
v___x_435_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_435_, 0, v___x_434_);
lean_ctor_set(v___x_435_, 1, v___x_412_);
v___x_436_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(v_r2_410_);
v___x_437_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_437_, 0, v___x_414_);
lean_ctor_set(v___x_437_, 1, v___x_436_);
v___x_438_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_438_, 0, v___x_437_);
lean_ctor_set_uint8(v___x_438_, sizeof(void*)*1, v___x_417_);
v___x_439_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_439_, 0, v___x_435_);
lean_ctor_set(v___x_439_, 1, v___x_438_);
v___x_440_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_440_, 0, v___x_439_);
lean_ctor_set(v___x_440_, 1, v___x_420_);
v___x_441_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_441_, 0, v___x_440_);
lean_ctor_set(v___x_441_, 1, v___x_422_);
v___x_442_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___closed__9));
v___x_443_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_443_, 0, v___x_441_);
lean_ctor_set(v___x_443_, 1, v___x_442_);
v___x_444_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_444_, 0, v___x_443_);
lean_ctor_set(v___x_444_, 1, v___x_412_);
v___x_445_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec4_repr___redArg(v_r3_411_);
v___x_446_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_446_, 0, v___x_414_);
lean_ctor_set(v___x_446_, 1, v___x_445_);
v___x_447_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_447_, 0, v___x_446_);
lean_ctor_set_uint8(v___x_447_, sizeof(void*)*1, v___x_417_);
v___x_448_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_448_, 0, v___x_444_);
lean_ctor_set(v___x_448_, 1, v___x_447_);
v___x_449_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10);
v___x_450_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11));
v___x_451_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_451_, 0, v___x_450_);
lean_ctor_set(v___x_451_, 1, v___x_448_);
v___x_452_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12));
v___x_453_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_453_, 0, v___x_451_);
lean_ctor_set(v___x_453_, 1, v___x_452_);
v___x_454_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_454_, 0, v___x_449_);
lean_ctor_set(v___x_454_, 1, v___x_453_);
v___x_455_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_455_, 0, v___x_454_);
lean_ctor_set_uint8(v___x_455_, sizeof(void*)*1, v___x_417_);
return v___x_455_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg___boxed(lean_object* v_x_456_){
_start:
{
lean_object* v_res_457_; 
v_res_457_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg(v_x_456_);
lean_dec_ref(v_x_456_);
return v_res_457_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr(lean_object* v_x_458_, lean_object* v_prec_459_){
_start:
{
lean_object* v___x_460_; 
v___x_460_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___redArg(v_x_458_);
return v___x_460_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr___boxed(lean_object* v_x_461_, lean_object* v_prec_462_){
_start:
{
lean_object* v_res_463_; 
v_res_463_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprMat4_repr(v_x_461_, v_prec_462_);
lean_dec(v_prec_462_);
lean_dec_ref(v_x_461_);
return v_res_463_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(lean_object* v_u_466_, lean_object* v_v_467_){
_start:
{
lean_object* v_v0_468_; lean_object* v_v1_469_; lean_object* v_v2_470_; lean_object* v_v3_471_; lean_object* v_v0_472_; lean_object* v_v1_473_; lean_object* v_v2_474_; lean_object* v_v3_475_; lean_object* v___x_476_; lean_object* v___x_477_; lean_object* v___x_478_; lean_object* v___x_479_; lean_object* v___x_480_; lean_object* v___x_481_; lean_object* v___x_482_; 
v_v0_468_ = lean_ctor_get(v_u_466_, 0);
v_v1_469_ = lean_ctor_get(v_u_466_, 1);
v_v2_470_ = lean_ctor_get(v_u_466_, 2);
v_v3_471_ = lean_ctor_get(v_u_466_, 3);
v_v0_472_ = lean_ctor_get(v_v_467_, 0);
v_v1_473_ = lean_ctor_get(v_v_467_, 1);
v_v2_474_ = lean_ctor_get(v_v_467_, 2);
v_v3_475_ = lean_ctor_get(v_v_467_, 3);
v___x_476_ = lean_int_mul(v_v0_468_, v_v0_472_);
v___x_477_ = lean_int_mul(v_v1_469_, v_v1_473_);
v___x_478_ = lean_int_add(v___x_476_, v___x_477_);
lean_dec(v___x_477_);
lean_dec(v___x_476_);
v___x_479_ = lean_int_mul(v_v2_470_, v_v2_474_);
v___x_480_ = lean_int_add(v___x_478_, v___x_479_);
lean_dec(v___x_479_);
lean_dec(v___x_478_);
v___x_481_ = lean_int_mul(v_v3_471_, v_v3_475_);
v___x_482_ = lean_int_add(v___x_480_, v___x_481_);
lean_dec(v___x_481_);
lean_dec(v___x_480_);
return v___x_482_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4___boxed(lean_object* v_u_483_, lean_object* v_v_484_){
_start:
{
lean_object* v_res_485_; 
v_res_485_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(v_u_483_, v_v_484_);
lean_dec_ref(v_v_484_);
lean_dec_ref(v_u_483_);
return v_res_485_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec(lean_object* v_M_486_, lean_object* v_v_487_){
_start:
{
lean_object* v_r0_488_; lean_object* v_r1_489_; lean_object* v_r2_490_; lean_object* v_r3_491_; lean_object* v___x_493_; uint8_t v_isShared_494_; uint8_t v_isSharedCheck_502_; 
v_r0_488_ = lean_ctor_get(v_M_486_, 0);
v_r1_489_ = lean_ctor_get(v_M_486_, 1);
v_r2_490_ = lean_ctor_get(v_M_486_, 2);
v_r3_491_ = lean_ctor_get(v_M_486_, 3);
v_isSharedCheck_502_ = !lean_is_exclusive(v_M_486_);
if (v_isSharedCheck_502_ == 0)
{
v___x_493_ = v_M_486_;
v_isShared_494_ = v_isSharedCheck_502_;
goto v_resetjp_492_;
}
else
{
lean_inc(v_r3_491_);
lean_inc(v_r2_490_);
lean_inc(v_r1_489_);
lean_inc(v_r0_488_);
lean_dec(v_M_486_);
v___x_493_ = lean_box(0);
v_isShared_494_ = v_isSharedCheck_502_;
goto v_resetjp_492_;
}
v_resetjp_492_:
{
lean_object* v___x_495_; lean_object* v___x_496_; lean_object* v___x_497_; lean_object* v___x_498_; lean_object* v___x_500_; 
v___x_495_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(v_r0_488_, v_v_487_);
lean_dec_ref(v_r0_488_);
v___x_496_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(v_r1_489_, v_v_487_);
lean_dec_ref(v_r1_489_);
v___x_497_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(v_r2_490_, v_v_487_);
lean_dec_ref(v_r2_490_);
v___x_498_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_dot4(v_r3_491_, v_v_487_);
lean_dec_ref(v_r3_491_);
if (v_isShared_494_ == 0)
{
lean_ctor_set(v___x_493_, 3, v___x_498_);
lean_ctor_set(v___x_493_, 2, v___x_497_);
lean_ctor_set(v___x_493_, 1, v___x_496_);
lean_ctor_set(v___x_493_, 0, v___x_495_);
v___x_500_ = v___x_493_;
goto v_reusejp_499_;
}
else
{
lean_object* v_reuseFailAlloc_501_; 
v_reuseFailAlloc_501_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_501_, 0, v___x_495_);
lean_ctor_set(v_reuseFailAlloc_501_, 1, v___x_496_);
lean_ctor_set(v_reuseFailAlloc_501_, 2, v___x_497_);
lean_ctor_set(v_reuseFailAlloc_501_, 3, v___x_498_);
v___x_500_ = v_reuseFailAlloc_501_;
goto v_reusejp_499_;
}
v_reusejp_499_:
{
return v___x_500_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec___boxed(lean_object* v_M_503_, lean_object* v_v_504_){
_start:
{
lean_object* v_res_505_; 
v_res_505_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec(v_M_503_, v_v_504_);
lean_dec_ref(v_v_504_);
return v_res_505_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform___closed__0(void){
_start:
{
lean_object* v___x_506_; lean_object* v___x_507_; 
v___x_506_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_507_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_507_, 0, v___x_506_);
lean_ctor_set(v___x_507_, 1, v___x_506_);
lean_ctor_set(v___x_507_, 2, v___x_506_);
lean_ctor_set(v___x_507_, 3, v___x_506_);
return v___x_507_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform(void){
_start:
{
lean_object* v___x_508_; 
v___x_508_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform___closed__0);
return v___x_508_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0(void){
_start:
{
lean_object* v___x_509_; lean_object* v___x_510_; lean_object* v___x_511_; 
v___x_509_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_510_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_511_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_511_, 0, v___x_510_);
lean_ctor_set(v___x_511_, 1, v___x_509_);
lean_ctor_set(v___x_511_, 2, v___x_509_);
lean_ctor_set(v___x_511_, 3, v___x_509_);
return v___x_511_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target(void){
_start:
{
lean_object* v___x_512_; 
v___x_512_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0);
return v___x_512_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0(void){
_start:
{
lean_object* v___x_513_; lean_object* v___x_514_; 
v___x_513_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_514_ = lean_int_neg(v___x_513_);
return v___x_514_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__1(void){
_start:
{
lean_object* v___x_515_; lean_object* v___x_516_; lean_object* v___x_517_; 
v___x_515_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_516_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0);
v___x_517_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_517_, 0, v___x_516_);
lean_ctor_set(v___x_517_, 1, v___x_515_);
lean_ctor_set(v___x_517_, 2, v___x_515_);
lean_ctor_set(v___x_517_, 3, v___x_515_);
return v___x_517_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2(void){
_start:
{
lean_object* v___x_518_; lean_object* v___x_519_; lean_object* v___x_520_; 
v___x_518_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_519_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_520_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_520_, 0, v___x_519_);
lean_ctor_set(v___x_520_, 1, v___x_518_);
lean_ctor_set(v___x_520_, 2, v___x_519_);
lean_ctor_set(v___x_520_, 3, v___x_519_);
return v___x_520_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3(void){
_start:
{
lean_object* v___x_521_; lean_object* v___x_522_; lean_object* v___x_523_; 
v___x_521_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_522_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_523_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_523_, 0, v___x_522_);
lean_ctor_set(v___x_523_, 1, v___x_522_);
lean_ctor_set(v___x_523_, 2, v___x_521_);
lean_ctor_set(v___x_523_, 3, v___x_522_);
return v___x_523_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4(void){
_start:
{
lean_object* v___x_524_; lean_object* v___x_525_; lean_object* v___x_526_; 
v___x_524_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_525_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__17);
v___x_526_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_526_, 0, v___x_525_);
lean_ctor_set(v___x_526_, 1, v___x_525_);
lean_ctor_set(v___x_526_, 2, v___x_525_);
lean_ctor_set(v___x_526_, 3, v___x_524_);
return v___x_526_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__5(void){
_start:
{
lean_object* v___x_527_; lean_object* v___x_528_; lean_object* v___x_529_; lean_object* v___x_530_; lean_object* v___x_531_; 
v___x_527_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4);
v___x_528_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3);
v___x_529_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2);
v___x_530_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__1);
v___x_531_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_531_, 0, v___x_530_);
lean_ctor_set(v___x_531_, 1, v___x_529_);
lean_ctor_set(v___x_531_, 2, v___x_528_);
lean_ctor_set(v___x_531_, 3, v___x_527_);
return v___x_531_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle(void){
_start:
{
lean_object* v___x_532_; 
v___x_532_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__5);
return v___x_532_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__0(void){
_start:
{
lean_object* v___x_533_; lean_object* v___x_534_; lean_object* v___x_535_; 
v___x_533_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_534_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0);
v___x_535_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_535_, 0, v___x_534_);
lean_ctor_set(v___x_535_, 1, v___x_533_);
lean_ctor_set(v___x_535_, 2, v___x_533_);
lean_ctor_set(v___x_535_, 3, v___x_533_);
return v___x_535_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__1(void){
_start:
{
lean_object* v___x_536_; lean_object* v___x_537_; lean_object* v___x_538_; 
v___x_536_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0);
v___x_537_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_538_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_538_, 0, v___x_537_);
lean_ctor_set(v___x_538_, 1, v___x_536_);
lean_ctor_set(v___x_538_, 2, v___x_537_);
lean_ctor_set(v___x_538_, 3, v___x_537_);
return v___x_538_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__2(void){
_start:
{
lean_object* v___x_539_; lean_object* v___x_540_; lean_object* v___x_541_; 
v___x_539_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0);
v___x_540_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_541_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_541_, 0, v___x_540_);
lean_ctor_set(v___x_541_, 1, v___x_540_);
lean_ctor_set(v___x_541_, 2, v___x_539_);
lean_ctor_set(v___x_541_, 3, v___x_540_);
return v___x_541_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__3(void){
_start:
{
lean_object* v___x_542_; lean_object* v___x_543_; lean_object* v___x_544_; 
v___x_542_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__0);
v___x_543_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
v___x_544_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_544_, 0, v___x_543_);
lean_ctor_set(v___x_544_, 1, v___x_543_);
lean_ctor_set(v___x_544_, 2, v___x_543_);
lean_ctor_set(v___x_544_, 3, v___x_542_);
return v___x_544_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__4(void){
_start:
{
lean_object* v___x_545_; lean_object* v___x_546_; lean_object* v___x_547_; lean_object* v___x_548_; lean_object* v___x_549_; 
v___x_545_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__3);
v___x_546_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__2);
v___x_547_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__1);
v___x_548_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__0);
v___x_549_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_549_, 0, v___x_548_);
lean_ctor_set(v___x_549_, 1, v___x_547_);
lean_ctor_set(v___x_549_, 2, v___x_546_);
lean_ctor_set(v___x_549_, 3, v___x_545_);
return v___x_549_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde(void){
_start:
{
lean_object* v___x_550_; 
v___x_550_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde___closed__4);
return v___x_550_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_grover__step(lean_object* v_v_551_){
_start:
{
lean_object* v___x_552_; lean_object* v___x_553_; lean_object* v___x_554_; lean_object* v___x_555_; 
v___x_552_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde;
v___x_553_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle;
v___x_554_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec(v___x_553_, v_v_551_);
v___x_555_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul__vec(v___x_552_, v___x_554_);
lean_dec_ref(v___x_554_);
return v___x_555_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_grover__step___boxed(lean_object* v_v_556_){
_start:
{
lean_object* v_res_557_; 
v_res_557_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_grover__step(v_v_556_);
lean_dec_ref(v_v_556_);
return v_res_557_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4___closed__0(void){
_start:
{
lean_object* v___x_558_; lean_object* v___x_559_; lean_object* v___x_560_; lean_object* v___x_561_; lean_object* v___x_562_; 
v___x_558_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__4);
v___x_559_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__3);
v___x_560_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle___closed__2);
v___x_561_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target___closed__0);
v___x_562_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_562_, 0, v___x_561_);
lean_ctor_set(v___x_562_, 1, v___x_560_);
lean_ctor_set(v___x_562_, 2, v___x_559_);
lean_ctor_set(v___x_562_, 3, v___x_558_);
return v___x_562_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4(void){
_start:
{
lean_object* v___x_563_; 
v___x_563_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4___closed__0);
return v___x_563_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_mat4__mul(lean_object* v_A_564_, lean_object* v_B_565_){
_start:
{
lean_object* v_r0_566_; lean_object* v_r0_567_; lean_object* v_r1_568_; lean_object* v_r2_569_; lean_object* v_r3_570_; lean_object* v___x_572_; uint8_t v_isShared_573_; uint8_t v_isSharedCheck_752_; 
v_r0_566_ = lean_ctor_get(v_A_564_, 0);
lean_inc_ref(v_r0_566_);
v_r0_567_ = lean_ctor_get(v_B_565_, 0);
v_r1_568_ = lean_ctor_get(v_B_565_, 1);
v_r2_569_ = lean_ctor_get(v_B_565_, 2);
v_r3_570_ = lean_ctor_get(v_B_565_, 3);
v_isSharedCheck_752_ = !lean_is_exclusive(v_B_565_);
if (v_isSharedCheck_752_ == 0)
{
v___x_572_ = v_B_565_;
v_isShared_573_ = v_isSharedCheck_752_;
goto v_resetjp_571_;
}
else
{
lean_inc(v_r3_570_);
lean_inc(v_r2_569_);
lean_inc(v_r1_568_);
lean_inc(v_r0_567_);
lean_dec(v_B_565_);
v___x_572_ = lean_box(0);
v_isShared_573_ = v_isSharedCheck_752_;
goto v_resetjp_571_;
}
v_resetjp_571_:
{
lean_object* v_r1_574_; lean_object* v_r2_575_; lean_object* v_r3_576_; lean_object* v_v0_577_; lean_object* v_v1_578_; lean_object* v_v2_579_; lean_object* v_v3_580_; lean_object* v_v0_581_; lean_object* v_v1_582_; lean_object* v_v2_583_; lean_object* v_v3_584_; lean_object* v_v0_585_; lean_object* v_v1_586_; lean_object* v_v2_587_; lean_object* v_v3_588_; lean_object* v_v0_589_; lean_object* v_v1_590_; lean_object* v_v2_591_; lean_object* v_v3_592_; lean_object* v_v0_593_; lean_object* v_v1_594_; lean_object* v_v2_595_; lean_object* v_v3_596_; lean_object* v___x_598_; uint8_t v_isShared_599_; uint8_t v_isSharedCheck_751_; 
v_r1_574_ = lean_ctor_get(v_A_564_, 1);
lean_inc_ref(v_r1_574_);
v_r2_575_ = lean_ctor_get(v_A_564_, 2);
lean_inc_ref(v_r2_575_);
v_r3_576_ = lean_ctor_get(v_A_564_, 3);
lean_inc_ref(v_r3_576_);
lean_dec_ref(v_A_564_);
v_v0_577_ = lean_ctor_get(v_r0_566_, 0);
lean_inc(v_v0_577_);
v_v1_578_ = lean_ctor_get(v_r0_566_, 1);
lean_inc(v_v1_578_);
v_v2_579_ = lean_ctor_get(v_r0_566_, 2);
lean_inc(v_v2_579_);
v_v3_580_ = lean_ctor_get(v_r0_566_, 3);
lean_inc(v_v3_580_);
lean_dec_ref(v_r0_566_);
v_v0_581_ = lean_ctor_get(v_r0_567_, 0);
lean_inc(v_v0_581_);
v_v1_582_ = lean_ctor_get(v_r0_567_, 1);
lean_inc(v_v1_582_);
v_v2_583_ = lean_ctor_get(v_r0_567_, 2);
lean_inc(v_v2_583_);
v_v3_584_ = lean_ctor_get(v_r0_567_, 3);
lean_inc(v_v3_584_);
lean_dec_ref(v_r0_567_);
v_v0_585_ = lean_ctor_get(v_r1_568_, 0);
lean_inc(v_v0_585_);
v_v1_586_ = lean_ctor_get(v_r1_568_, 1);
lean_inc(v_v1_586_);
v_v2_587_ = lean_ctor_get(v_r1_568_, 2);
lean_inc(v_v2_587_);
v_v3_588_ = lean_ctor_get(v_r1_568_, 3);
lean_inc(v_v3_588_);
lean_dec_ref(v_r1_568_);
v_v0_589_ = lean_ctor_get(v_r2_569_, 0);
lean_inc(v_v0_589_);
v_v1_590_ = lean_ctor_get(v_r2_569_, 1);
lean_inc(v_v1_590_);
v_v2_591_ = lean_ctor_get(v_r2_569_, 2);
lean_inc(v_v2_591_);
v_v3_592_ = lean_ctor_get(v_r2_569_, 3);
lean_inc(v_v3_592_);
lean_dec_ref(v_r2_569_);
v_v0_593_ = lean_ctor_get(v_r3_570_, 0);
v_v1_594_ = lean_ctor_get(v_r3_570_, 1);
v_v2_595_ = lean_ctor_get(v_r3_570_, 2);
v_v3_596_ = lean_ctor_get(v_r3_570_, 3);
v_isSharedCheck_751_ = !lean_is_exclusive(v_r3_570_);
if (v_isSharedCheck_751_ == 0)
{
v___x_598_ = v_r3_570_;
v_isShared_599_ = v_isSharedCheck_751_;
goto v_resetjp_597_;
}
else
{
lean_inc(v_v3_596_);
lean_inc(v_v2_595_);
lean_inc(v_v1_594_);
lean_inc(v_v0_593_);
lean_dec(v_r3_570_);
v___x_598_ = lean_box(0);
v_isShared_599_ = v_isSharedCheck_751_;
goto v_resetjp_597_;
}
v_resetjp_597_:
{
lean_object* v_v0_600_; lean_object* v_v1_601_; lean_object* v_v2_602_; lean_object* v_v3_603_; lean_object* v___x_605_; uint8_t v_isShared_606_; uint8_t v_isSharedCheck_750_; 
v_v0_600_ = lean_ctor_get(v_r1_574_, 0);
v_v1_601_ = lean_ctor_get(v_r1_574_, 1);
v_v2_602_ = lean_ctor_get(v_r1_574_, 2);
v_v3_603_ = lean_ctor_get(v_r1_574_, 3);
v_isSharedCheck_750_ = !lean_is_exclusive(v_r1_574_);
if (v_isSharedCheck_750_ == 0)
{
v___x_605_ = v_r1_574_;
v_isShared_606_ = v_isSharedCheck_750_;
goto v_resetjp_604_;
}
else
{
lean_inc(v_v3_603_);
lean_inc(v_v2_602_);
lean_inc(v_v1_601_);
lean_inc(v_v0_600_);
lean_dec(v_r1_574_);
v___x_605_ = lean_box(0);
v_isShared_606_ = v_isSharedCheck_750_;
goto v_resetjp_604_;
}
v_resetjp_604_:
{
lean_object* v_v0_607_; lean_object* v_v1_608_; lean_object* v_v2_609_; lean_object* v_v3_610_; lean_object* v___x_612_; uint8_t v_isShared_613_; uint8_t v_isSharedCheck_749_; 
v_v0_607_ = lean_ctor_get(v_r2_575_, 0);
v_v1_608_ = lean_ctor_get(v_r2_575_, 1);
v_v2_609_ = lean_ctor_get(v_r2_575_, 2);
v_v3_610_ = lean_ctor_get(v_r2_575_, 3);
v_isSharedCheck_749_ = !lean_is_exclusive(v_r2_575_);
if (v_isSharedCheck_749_ == 0)
{
v___x_612_ = v_r2_575_;
v_isShared_613_ = v_isSharedCheck_749_;
goto v_resetjp_611_;
}
else
{
lean_inc(v_v3_610_);
lean_inc(v_v2_609_);
lean_inc(v_v1_608_);
lean_inc(v_v0_607_);
lean_dec(v_r2_575_);
v___x_612_ = lean_box(0);
v_isShared_613_ = v_isSharedCheck_749_;
goto v_resetjp_611_;
}
v_resetjp_611_:
{
lean_object* v_v0_614_; lean_object* v_v1_615_; lean_object* v_v2_616_; lean_object* v_v3_617_; lean_object* v___x_619_; uint8_t v_isShared_620_; uint8_t v_isSharedCheck_748_; 
v_v0_614_ = lean_ctor_get(v_r3_576_, 0);
v_v1_615_ = lean_ctor_get(v_r3_576_, 1);
v_v2_616_ = lean_ctor_get(v_r3_576_, 2);
v_v3_617_ = lean_ctor_get(v_r3_576_, 3);
v_isSharedCheck_748_ = !lean_is_exclusive(v_r3_576_);
if (v_isSharedCheck_748_ == 0)
{
v___x_619_ = v_r3_576_;
v_isShared_620_ = v_isSharedCheck_748_;
goto v_resetjp_618_;
}
else
{
lean_inc(v_v3_617_);
lean_inc(v_v2_616_);
lean_inc(v_v1_615_);
lean_inc(v_v0_614_);
lean_dec(v_r3_576_);
v___x_619_ = lean_box(0);
v_isShared_620_ = v_isSharedCheck_748_;
goto v_resetjp_618_;
}
v_resetjp_618_:
{
lean_object* v___x_621_; lean_object* v___x_622_; lean_object* v___x_623_; lean_object* v___x_624_; lean_object* v___x_625_; lean_object* v___x_626_; lean_object* v___x_627_; lean_object* v___x_628_; lean_object* v___x_629_; lean_object* v___x_630_; lean_object* v___x_631_; lean_object* v___x_632_; lean_object* v___x_633_; lean_object* v___x_634_; lean_object* v___x_635_; lean_object* v___x_636_; lean_object* v___x_637_; lean_object* v___x_638_; lean_object* v___x_639_; lean_object* v___x_640_; lean_object* v___x_641_; lean_object* v___x_642_; lean_object* v___x_643_; lean_object* v___x_644_; lean_object* v___x_645_; lean_object* v___x_646_; lean_object* v___x_647_; lean_object* v___x_648_; lean_object* v___x_650_; 
v___x_621_ = lean_int_mul(v_v0_577_, v_v0_581_);
v___x_622_ = lean_int_mul(v_v1_578_, v_v0_585_);
v___x_623_ = lean_int_add(v___x_621_, v___x_622_);
lean_dec(v___x_622_);
lean_dec(v___x_621_);
v___x_624_ = lean_int_mul(v_v2_579_, v_v0_589_);
v___x_625_ = lean_int_add(v___x_623_, v___x_624_);
lean_dec(v___x_624_);
lean_dec(v___x_623_);
v___x_626_ = lean_int_mul(v_v3_580_, v_v0_593_);
v___x_627_ = lean_int_add(v___x_625_, v___x_626_);
lean_dec(v___x_626_);
lean_dec(v___x_625_);
v___x_628_ = lean_int_mul(v_v0_577_, v_v1_582_);
v___x_629_ = lean_int_mul(v_v1_578_, v_v1_586_);
v___x_630_ = lean_int_add(v___x_628_, v___x_629_);
lean_dec(v___x_629_);
lean_dec(v___x_628_);
v___x_631_ = lean_int_mul(v_v2_579_, v_v1_590_);
v___x_632_ = lean_int_add(v___x_630_, v___x_631_);
lean_dec(v___x_631_);
lean_dec(v___x_630_);
v___x_633_ = lean_int_mul(v_v3_580_, v_v1_594_);
v___x_634_ = lean_int_add(v___x_632_, v___x_633_);
lean_dec(v___x_633_);
lean_dec(v___x_632_);
v___x_635_ = lean_int_mul(v_v0_577_, v_v2_583_);
v___x_636_ = lean_int_mul(v_v1_578_, v_v2_587_);
v___x_637_ = lean_int_add(v___x_635_, v___x_636_);
lean_dec(v___x_636_);
lean_dec(v___x_635_);
v___x_638_ = lean_int_mul(v_v2_579_, v_v2_591_);
v___x_639_ = lean_int_add(v___x_637_, v___x_638_);
lean_dec(v___x_638_);
lean_dec(v___x_637_);
v___x_640_ = lean_int_mul(v_v3_580_, v_v2_595_);
v___x_641_ = lean_int_add(v___x_639_, v___x_640_);
lean_dec(v___x_640_);
lean_dec(v___x_639_);
v___x_642_ = lean_int_mul(v_v0_577_, v_v3_584_);
lean_dec(v_v0_577_);
v___x_643_ = lean_int_mul(v_v1_578_, v_v3_588_);
lean_dec(v_v1_578_);
v___x_644_ = lean_int_add(v___x_642_, v___x_643_);
lean_dec(v___x_643_);
lean_dec(v___x_642_);
v___x_645_ = lean_int_mul(v_v2_579_, v_v3_592_);
lean_dec(v_v2_579_);
v___x_646_ = lean_int_add(v___x_644_, v___x_645_);
lean_dec(v___x_645_);
lean_dec(v___x_644_);
v___x_647_ = lean_int_mul(v_v3_580_, v_v3_596_);
lean_dec(v_v3_580_);
v___x_648_ = lean_int_add(v___x_646_, v___x_647_);
lean_dec(v___x_647_);
lean_dec(v___x_646_);
if (v_isShared_620_ == 0)
{
lean_ctor_set(v___x_619_, 3, v___x_648_);
lean_ctor_set(v___x_619_, 2, v___x_641_);
lean_ctor_set(v___x_619_, 1, v___x_634_);
lean_ctor_set(v___x_619_, 0, v___x_627_);
v___x_650_ = v___x_619_;
goto v_reusejp_649_;
}
else
{
lean_object* v_reuseFailAlloc_747_; 
v_reuseFailAlloc_747_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_747_, 0, v___x_627_);
lean_ctor_set(v_reuseFailAlloc_747_, 1, v___x_634_);
lean_ctor_set(v_reuseFailAlloc_747_, 2, v___x_641_);
lean_ctor_set(v_reuseFailAlloc_747_, 3, v___x_648_);
v___x_650_ = v_reuseFailAlloc_747_;
goto v_reusejp_649_;
}
v_reusejp_649_:
{
lean_object* v___x_651_; lean_object* v___x_652_; lean_object* v___x_653_; lean_object* v___x_654_; lean_object* v___x_655_; lean_object* v___x_656_; lean_object* v___x_657_; lean_object* v___x_658_; lean_object* v___x_659_; lean_object* v___x_660_; lean_object* v___x_661_; lean_object* v___x_662_; lean_object* v___x_663_; lean_object* v___x_664_; lean_object* v___x_665_; lean_object* v___x_666_; lean_object* v___x_667_; lean_object* v___x_668_; lean_object* v___x_669_; lean_object* v___x_670_; lean_object* v___x_671_; lean_object* v___x_672_; lean_object* v___x_673_; lean_object* v___x_674_; lean_object* v___x_675_; lean_object* v___x_676_; lean_object* v___x_677_; lean_object* v___x_678_; lean_object* v___x_680_; 
v___x_651_ = lean_int_mul(v_v0_600_, v_v0_581_);
v___x_652_ = lean_int_mul(v_v1_601_, v_v0_585_);
v___x_653_ = lean_int_add(v___x_651_, v___x_652_);
lean_dec(v___x_652_);
lean_dec(v___x_651_);
v___x_654_ = lean_int_mul(v_v2_602_, v_v0_589_);
v___x_655_ = lean_int_add(v___x_653_, v___x_654_);
lean_dec(v___x_654_);
lean_dec(v___x_653_);
v___x_656_ = lean_int_mul(v_v3_603_, v_v0_593_);
v___x_657_ = lean_int_add(v___x_655_, v___x_656_);
lean_dec(v___x_656_);
lean_dec(v___x_655_);
v___x_658_ = lean_int_mul(v_v0_600_, v_v1_582_);
v___x_659_ = lean_int_mul(v_v1_601_, v_v1_586_);
v___x_660_ = lean_int_add(v___x_658_, v___x_659_);
lean_dec(v___x_659_);
lean_dec(v___x_658_);
v___x_661_ = lean_int_mul(v_v2_602_, v_v1_590_);
v___x_662_ = lean_int_add(v___x_660_, v___x_661_);
lean_dec(v___x_661_);
lean_dec(v___x_660_);
v___x_663_ = lean_int_mul(v_v3_603_, v_v1_594_);
v___x_664_ = lean_int_add(v___x_662_, v___x_663_);
lean_dec(v___x_663_);
lean_dec(v___x_662_);
v___x_665_ = lean_int_mul(v_v0_600_, v_v2_583_);
v___x_666_ = lean_int_mul(v_v1_601_, v_v2_587_);
v___x_667_ = lean_int_add(v___x_665_, v___x_666_);
lean_dec(v___x_666_);
lean_dec(v___x_665_);
v___x_668_ = lean_int_mul(v_v2_602_, v_v2_591_);
v___x_669_ = lean_int_add(v___x_667_, v___x_668_);
lean_dec(v___x_668_);
lean_dec(v___x_667_);
v___x_670_ = lean_int_mul(v_v3_603_, v_v2_595_);
v___x_671_ = lean_int_add(v___x_669_, v___x_670_);
lean_dec(v___x_670_);
lean_dec(v___x_669_);
v___x_672_ = lean_int_mul(v_v0_600_, v_v3_584_);
lean_dec(v_v0_600_);
v___x_673_ = lean_int_mul(v_v1_601_, v_v3_588_);
lean_dec(v_v1_601_);
v___x_674_ = lean_int_add(v___x_672_, v___x_673_);
lean_dec(v___x_673_);
lean_dec(v___x_672_);
v___x_675_ = lean_int_mul(v_v2_602_, v_v3_592_);
lean_dec(v_v2_602_);
v___x_676_ = lean_int_add(v___x_674_, v___x_675_);
lean_dec(v___x_675_);
lean_dec(v___x_674_);
v___x_677_ = lean_int_mul(v_v3_603_, v_v3_596_);
lean_dec(v_v3_603_);
v___x_678_ = lean_int_add(v___x_676_, v___x_677_);
lean_dec(v___x_677_);
lean_dec(v___x_676_);
if (v_isShared_613_ == 0)
{
lean_ctor_set(v___x_612_, 3, v___x_678_);
lean_ctor_set(v___x_612_, 2, v___x_671_);
lean_ctor_set(v___x_612_, 1, v___x_664_);
lean_ctor_set(v___x_612_, 0, v___x_657_);
v___x_680_ = v___x_612_;
goto v_reusejp_679_;
}
else
{
lean_object* v_reuseFailAlloc_746_; 
v_reuseFailAlloc_746_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_746_, 0, v___x_657_);
lean_ctor_set(v_reuseFailAlloc_746_, 1, v___x_664_);
lean_ctor_set(v_reuseFailAlloc_746_, 2, v___x_671_);
lean_ctor_set(v_reuseFailAlloc_746_, 3, v___x_678_);
v___x_680_ = v_reuseFailAlloc_746_;
goto v_reusejp_679_;
}
v_reusejp_679_:
{
lean_object* v___x_681_; lean_object* v___x_682_; lean_object* v___x_683_; lean_object* v___x_684_; lean_object* v___x_685_; lean_object* v___x_686_; lean_object* v___x_687_; lean_object* v___x_688_; lean_object* v___x_689_; lean_object* v___x_690_; lean_object* v___x_691_; lean_object* v___x_692_; lean_object* v___x_693_; lean_object* v___x_694_; lean_object* v___x_695_; lean_object* v___x_696_; lean_object* v___x_697_; lean_object* v___x_698_; lean_object* v___x_699_; lean_object* v___x_700_; lean_object* v___x_701_; lean_object* v___x_702_; lean_object* v___x_703_; lean_object* v___x_704_; lean_object* v___x_705_; lean_object* v___x_706_; lean_object* v___x_707_; lean_object* v___x_708_; lean_object* v___x_710_; 
v___x_681_ = lean_int_mul(v_v0_607_, v_v0_581_);
v___x_682_ = lean_int_mul(v_v1_608_, v_v0_585_);
v___x_683_ = lean_int_add(v___x_681_, v___x_682_);
lean_dec(v___x_682_);
lean_dec(v___x_681_);
v___x_684_ = lean_int_mul(v_v2_609_, v_v0_589_);
v___x_685_ = lean_int_add(v___x_683_, v___x_684_);
lean_dec(v___x_684_);
lean_dec(v___x_683_);
v___x_686_ = lean_int_mul(v_v3_610_, v_v0_593_);
v___x_687_ = lean_int_add(v___x_685_, v___x_686_);
lean_dec(v___x_686_);
lean_dec(v___x_685_);
v___x_688_ = lean_int_mul(v_v0_607_, v_v1_582_);
v___x_689_ = lean_int_mul(v_v1_608_, v_v1_586_);
v___x_690_ = lean_int_add(v___x_688_, v___x_689_);
lean_dec(v___x_689_);
lean_dec(v___x_688_);
v___x_691_ = lean_int_mul(v_v2_609_, v_v1_590_);
v___x_692_ = lean_int_add(v___x_690_, v___x_691_);
lean_dec(v___x_691_);
lean_dec(v___x_690_);
v___x_693_ = lean_int_mul(v_v3_610_, v_v1_594_);
v___x_694_ = lean_int_add(v___x_692_, v___x_693_);
lean_dec(v___x_693_);
lean_dec(v___x_692_);
v___x_695_ = lean_int_mul(v_v0_607_, v_v2_583_);
v___x_696_ = lean_int_mul(v_v1_608_, v_v2_587_);
v___x_697_ = lean_int_add(v___x_695_, v___x_696_);
lean_dec(v___x_696_);
lean_dec(v___x_695_);
v___x_698_ = lean_int_mul(v_v2_609_, v_v2_591_);
v___x_699_ = lean_int_add(v___x_697_, v___x_698_);
lean_dec(v___x_698_);
lean_dec(v___x_697_);
v___x_700_ = lean_int_mul(v_v3_610_, v_v2_595_);
v___x_701_ = lean_int_add(v___x_699_, v___x_700_);
lean_dec(v___x_700_);
lean_dec(v___x_699_);
v___x_702_ = lean_int_mul(v_v0_607_, v_v3_584_);
lean_dec(v_v0_607_);
v___x_703_ = lean_int_mul(v_v1_608_, v_v3_588_);
lean_dec(v_v1_608_);
v___x_704_ = lean_int_add(v___x_702_, v___x_703_);
lean_dec(v___x_703_);
lean_dec(v___x_702_);
v___x_705_ = lean_int_mul(v_v2_609_, v_v3_592_);
lean_dec(v_v2_609_);
v___x_706_ = lean_int_add(v___x_704_, v___x_705_);
lean_dec(v___x_705_);
lean_dec(v___x_704_);
v___x_707_ = lean_int_mul(v_v3_610_, v_v3_596_);
lean_dec(v_v3_610_);
v___x_708_ = lean_int_add(v___x_706_, v___x_707_);
lean_dec(v___x_707_);
lean_dec(v___x_706_);
if (v_isShared_606_ == 0)
{
lean_ctor_set(v___x_605_, 3, v___x_708_);
lean_ctor_set(v___x_605_, 2, v___x_701_);
lean_ctor_set(v___x_605_, 1, v___x_694_);
lean_ctor_set(v___x_605_, 0, v___x_687_);
v___x_710_ = v___x_605_;
goto v_reusejp_709_;
}
else
{
lean_object* v_reuseFailAlloc_745_; 
v_reuseFailAlloc_745_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_745_, 0, v___x_687_);
lean_ctor_set(v_reuseFailAlloc_745_, 1, v___x_694_);
lean_ctor_set(v_reuseFailAlloc_745_, 2, v___x_701_);
lean_ctor_set(v_reuseFailAlloc_745_, 3, v___x_708_);
v___x_710_ = v_reuseFailAlloc_745_;
goto v_reusejp_709_;
}
v_reusejp_709_:
{
lean_object* v___x_711_; lean_object* v___x_712_; lean_object* v___x_713_; lean_object* v___x_714_; lean_object* v___x_715_; lean_object* v___x_716_; lean_object* v___x_717_; lean_object* v___x_718_; lean_object* v___x_719_; lean_object* v___x_720_; lean_object* v___x_721_; lean_object* v___x_722_; lean_object* v___x_723_; lean_object* v___x_724_; lean_object* v___x_725_; lean_object* v___x_726_; lean_object* v___x_727_; lean_object* v___x_728_; lean_object* v___x_729_; lean_object* v___x_730_; lean_object* v___x_731_; lean_object* v___x_732_; lean_object* v___x_733_; lean_object* v___x_734_; lean_object* v___x_735_; lean_object* v___x_736_; lean_object* v___x_737_; lean_object* v___x_738_; lean_object* v___x_740_; 
v___x_711_ = lean_int_mul(v_v0_614_, v_v0_581_);
lean_dec(v_v0_581_);
v___x_712_ = lean_int_mul(v_v1_615_, v_v0_585_);
lean_dec(v_v0_585_);
v___x_713_ = lean_int_add(v___x_711_, v___x_712_);
lean_dec(v___x_712_);
lean_dec(v___x_711_);
v___x_714_ = lean_int_mul(v_v2_616_, v_v0_589_);
lean_dec(v_v0_589_);
v___x_715_ = lean_int_add(v___x_713_, v___x_714_);
lean_dec(v___x_714_);
lean_dec(v___x_713_);
v___x_716_ = lean_int_mul(v_v3_617_, v_v0_593_);
lean_dec(v_v0_593_);
v___x_717_ = lean_int_add(v___x_715_, v___x_716_);
lean_dec(v___x_716_);
lean_dec(v___x_715_);
v___x_718_ = lean_int_mul(v_v0_614_, v_v1_582_);
lean_dec(v_v1_582_);
v___x_719_ = lean_int_mul(v_v1_615_, v_v1_586_);
lean_dec(v_v1_586_);
v___x_720_ = lean_int_add(v___x_718_, v___x_719_);
lean_dec(v___x_719_);
lean_dec(v___x_718_);
v___x_721_ = lean_int_mul(v_v2_616_, v_v1_590_);
lean_dec(v_v1_590_);
v___x_722_ = lean_int_add(v___x_720_, v___x_721_);
lean_dec(v___x_721_);
lean_dec(v___x_720_);
v___x_723_ = lean_int_mul(v_v3_617_, v_v1_594_);
lean_dec(v_v1_594_);
v___x_724_ = lean_int_add(v___x_722_, v___x_723_);
lean_dec(v___x_723_);
lean_dec(v___x_722_);
v___x_725_ = lean_int_mul(v_v0_614_, v_v2_583_);
lean_dec(v_v2_583_);
v___x_726_ = lean_int_mul(v_v1_615_, v_v2_587_);
lean_dec(v_v2_587_);
v___x_727_ = lean_int_add(v___x_725_, v___x_726_);
lean_dec(v___x_726_);
lean_dec(v___x_725_);
v___x_728_ = lean_int_mul(v_v2_616_, v_v2_591_);
lean_dec(v_v2_591_);
v___x_729_ = lean_int_add(v___x_727_, v___x_728_);
lean_dec(v___x_728_);
lean_dec(v___x_727_);
v___x_730_ = lean_int_mul(v_v3_617_, v_v2_595_);
lean_dec(v_v2_595_);
v___x_731_ = lean_int_add(v___x_729_, v___x_730_);
lean_dec(v___x_730_);
lean_dec(v___x_729_);
v___x_732_ = lean_int_mul(v_v0_614_, v_v3_584_);
lean_dec(v_v3_584_);
lean_dec(v_v0_614_);
v___x_733_ = lean_int_mul(v_v1_615_, v_v3_588_);
lean_dec(v_v3_588_);
lean_dec(v_v1_615_);
v___x_734_ = lean_int_add(v___x_732_, v___x_733_);
lean_dec(v___x_733_);
lean_dec(v___x_732_);
v___x_735_ = lean_int_mul(v_v2_616_, v_v3_592_);
lean_dec(v_v3_592_);
lean_dec(v_v2_616_);
v___x_736_ = lean_int_add(v___x_734_, v___x_735_);
lean_dec(v___x_735_);
lean_dec(v___x_734_);
v___x_737_ = lean_int_mul(v_v3_617_, v_v3_596_);
lean_dec(v_v3_596_);
lean_dec(v_v3_617_);
v___x_738_ = lean_int_add(v___x_736_, v___x_737_);
lean_dec(v___x_737_);
lean_dec(v___x_736_);
if (v_isShared_599_ == 0)
{
lean_ctor_set(v___x_598_, 3, v___x_738_);
lean_ctor_set(v___x_598_, 2, v___x_731_);
lean_ctor_set(v___x_598_, 1, v___x_724_);
lean_ctor_set(v___x_598_, 0, v___x_717_);
v___x_740_ = v___x_598_;
goto v_reusejp_739_;
}
else
{
lean_object* v_reuseFailAlloc_744_; 
v_reuseFailAlloc_744_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_744_, 0, v___x_717_);
lean_ctor_set(v_reuseFailAlloc_744_, 1, v___x_724_);
lean_ctor_set(v_reuseFailAlloc_744_, 2, v___x_731_);
lean_ctor_set(v_reuseFailAlloc_744_, 3, v___x_738_);
v___x_740_ = v_reuseFailAlloc_744_;
goto v_reusejp_739_;
}
v_reusejp_739_:
{
lean_object* v___x_742_; 
if (v_isShared_573_ == 0)
{
lean_ctor_set(v___x_572_, 3, v___x_740_);
lean_ctor_set(v___x_572_, 2, v___x_710_);
lean_ctor_set(v___x_572_, 1, v___x_680_);
lean_ctor_set(v___x_572_, 0, v___x_650_);
v___x_742_ = v___x_572_;
goto v_reusejp_741_;
}
else
{
lean_object* v_reuseFailAlloc_743_; 
v_reuseFailAlloc_743_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_743_, 0, v___x_650_);
lean_ctor_set(v_reuseFailAlloc_743_, 1, v___x_680_);
lean_ctor_set(v_reuseFailAlloc_743_, 2, v___x_710_);
lean_ctor_set(v_reuseFailAlloc_743_, 3, v___x_740_);
v___x_742_ = v_reuseFailAlloc_743_;
goto v_reusejp_741_;
}
v_reusejp_741_:
{
return v___x_742_;
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
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q_decEq(lean_object* v_x_753_, lean_object* v_x_754_){
_start:
{
lean_object* v_x_755_; lean_object* v_y_756_; lean_object* v_x_757_; lean_object* v_y_758_; uint8_t v___x_759_; 
v_x_755_ = lean_ctor_get(v_x_753_, 0);
v_y_756_ = lean_ctor_get(v_x_753_, 1);
v_x_757_ = lean_ctor_get(v_x_754_, 0);
v_y_758_ = lean_ctor_get(v_x_754_, 1);
v___x_759_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq(v_x_755_, v_x_757_);
if (v___x_759_ == 0)
{
return v___x_759_;
}
else
{
uint8_t v___x_760_; 
v___x_760_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqQuad3_decEq(v_y_756_, v_y_758_);
return v___x_760_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q_decEq___boxed(lean_object* v_x_761_, lean_object* v_x_762_){
_start:
{
uint8_t v_res_763_; lean_object* v_r_764_; 
v_res_763_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q_decEq(v_x_761_, v_x_762_);
lean_dec_ref(v_x_762_);
lean_dec_ref(v_x_761_);
v_r_764_ = lean_box(v_res_763_);
return v_r_764_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q(lean_object* v_x_765_, lean_object* v_x_766_){
_start:
{
uint8_t v___x_767_; 
v___x_767_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q_decEq(v_x_765_, v_x_766_);
return v___x_767_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q___boxed(lean_object* v_x_768_, lean_object* v_x_769_){
_start:
{
uint8_t v_res_770_; lean_object* v_r_771_; 
v_res_770_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instDecidableEqVec2Q(v_x_768_, v_x_769_);
lean_dec_ref(v_x_769_);
lean_dec_ref(v_x_768_);
v_r_771_ = lean_box(v_res_770_);
return v_r_771_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg(lean_object* v_x_784_){
_start:
{
lean_object* v_x_785_; lean_object* v_y_786_; lean_object* v___x_788_; uint8_t v_isShared_789_; uint8_t v_isSharedCheck_818_; 
v_x_785_ = lean_ctor_get(v_x_784_, 0);
v_y_786_ = lean_ctor_get(v_x_784_, 1);
v_isSharedCheck_818_ = !lean_is_exclusive(v_x_784_);
if (v_isSharedCheck_818_ == 0)
{
v___x_788_ = v_x_784_;
v_isShared_789_ = v_isSharedCheck_818_;
goto v_resetjp_787_;
}
else
{
lean_inc(v_y_786_);
lean_inc(v_x_785_);
lean_dec(v_x_784_);
v___x_788_ = lean_box(0);
v_isShared_789_ = v_isSharedCheck_818_;
goto v_resetjp_787_;
}
v_resetjp_787_:
{
lean_object* v___x_790_; lean_object* v___x_791_; lean_object* v___x_792_; lean_object* v___x_793_; lean_object* v___x_795_; 
v___x_790_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__5));
v___x_791_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__3));
v___x_792_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__7);
v___x_793_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg(v_x_785_);
if (v_isShared_789_ == 0)
{
lean_ctor_set_tag(v___x_788_, 4);
lean_ctor_set(v___x_788_, 1, v___x_793_);
lean_ctor_set(v___x_788_, 0, v___x_792_);
v___x_795_ = v___x_788_;
goto v_reusejp_794_;
}
else
{
lean_object* v_reuseFailAlloc_817_; 
v_reuseFailAlloc_817_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_817_, 0, v___x_792_);
lean_ctor_set(v_reuseFailAlloc_817_, 1, v___x_793_);
v___x_795_ = v_reuseFailAlloc_817_;
goto v_reusejp_794_;
}
v_reusejp_794_:
{
uint8_t v___x_796_; lean_object* v___x_797_; lean_object* v___x_798_; lean_object* v___x_799_; lean_object* v___x_800_; lean_object* v___x_801_; lean_object* v___x_802_; lean_object* v___x_803_; lean_object* v___x_804_; lean_object* v___x_805_; lean_object* v___x_806_; lean_object* v___x_807_; lean_object* v___x_808_; lean_object* v___x_809_; lean_object* v___x_810_; lean_object* v___x_811_; lean_object* v___x_812_; lean_object* v___x_813_; lean_object* v___x_814_; lean_object* v___x_815_; lean_object* v___x_816_; 
v___x_796_ = 0;
v___x_797_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_797_, 0, v___x_795_);
lean_ctor_set_uint8(v___x_797_, sizeof(void*)*1, v___x_796_);
v___x_798_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_798_, 0, v___x_791_);
lean_ctor_set(v___x_798_, 1, v___x_797_);
v___x_799_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__14));
v___x_800_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_800_, 0, v___x_798_);
lean_ctor_set(v___x_800_, 1, v___x_799_);
v___x_801_ = lean_box(1);
v___x_802_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_802_, 0, v___x_800_);
lean_ctor_set(v___x_802_, 1, v___x_801_);
v___x_803_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg___closed__5));
v___x_804_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_804_, 0, v___x_802_);
lean_ctor_set(v___x_804_, 1, v___x_803_);
v___x_805_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_805_, 0, v___x_804_);
lean_ctor_set(v___x_805_, 1, v___x_790_);
v___x_806_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg(v_y_786_);
v___x_807_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_807_, 0, v___x_792_);
lean_ctor_set(v___x_807_, 1, v___x_806_);
v___x_808_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_808_, 0, v___x_807_);
lean_ctor_set_uint8(v___x_808_, sizeof(void*)*1, v___x_796_);
v___x_809_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_809_, 0, v___x_805_);
lean_ctor_set(v___x_809_, 1, v___x_808_);
v___x_810_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__10);
v___x_811_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__11));
v___x_812_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_812_, 0, v___x_811_);
lean_ctor_set(v___x_812_, 1, v___x_809_);
v___x_813_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprQuad3_repr___redArg___closed__12));
v___x_814_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_814_, 0, v___x_812_);
lean_ctor_set(v___x_814_, 1, v___x_813_);
v___x_815_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_815_, 0, v___x_810_);
lean_ctor_set(v___x_815_, 1, v___x_814_);
v___x_816_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_816_, 0, v___x_815_);
lean_ctor_set_uint8(v___x_816_, sizeof(void*)*1, v___x_796_);
return v___x_816_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr(lean_object* v_x_819_, lean_object* v_prec_820_){
_start:
{
lean_object* v___x_821_; 
v___x_821_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___redArg(v_x_819_);
return v___x_821_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr___boxed(lean_object* v_x_822_, lean_object* v_prec_823_){
_start:
{
lean_object* v_res_824_; 
v_res_824_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_instReprVec2Q_repr(v_x_822_, v_prec_823_);
lean_dec(v_prec_823_);
return v_res_824_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_rot2d(lean_object* v_v_827_){
_start:
{
lean_object* v_x_828_; lean_object* v_y_829_; lean_object* v___x_831_; uint8_t v_isShared_832_; uint8_t v_isSharedCheck_844_; 
v_x_828_ = lean_ctor_get(v_v_827_, 0);
v_y_829_ = lean_ctor_get(v_v_827_, 1);
v_isSharedCheck_844_ = !lean_is_exclusive(v_v_827_);
if (v_isSharedCheck_844_ == 0)
{
v___x_831_ = v_v_827_;
v_isShared_832_ = v_isSharedCheck_844_;
goto v_resetjp_830_;
}
else
{
lean_inc(v_y_829_);
lean_inc(v_x_828_);
lean_dec(v_v_827_);
v___x_831_ = lean_box(0);
v_isShared_832_ = v_isSharedCheck_844_;
goto v_resetjp_830_;
}
v_resetjp_830_:
{
lean_object* v___x_833_; lean_object* v___x_834_; lean_object* v___x_835_; lean_object* v___x_836_; lean_object* v___x_837_; lean_object* v___x_838_; lean_object* v___x_839_; lean_object* v___x_840_; lean_object* v___x_842_; 
v___x_833_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__1);
lean_inc_ref(v_x_828_);
v___x_834_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(v___x_833_, v_x_828_);
v___x_835_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3___closed__0);
lean_inc_ref(v_y_829_);
v___x_836_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(v___x_835_, v_y_829_);
v___x_837_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsub(v___x_834_, v___x_836_);
lean_dec_ref(v___x_834_);
v___x_838_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(v___x_835_, v_x_828_);
v___x_839_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qmul(v___x_833_, v_y_829_);
v___x_840_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qadd(v___x_838_, v___x_839_);
lean_dec_ref(v___x_838_);
if (v_isShared_832_ == 0)
{
lean_ctor_set(v___x_831_, 1, v___x_840_);
lean_ctor_set(v___x_831_, 0, v___x_837_);
v___x_842_ = v___x_831_;
goto v_reusejp_841_;
}
else
{
lean_object* v_reuseFailAlloc_843_; 
v_reuseFailAlloc_843_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_843_, 0, v___x_837_);
lean_ctor_set(v_reuseFailAlloc_843_, 1, v___x_840_);
v___x_842_ = v_reuseFailAlloc_843_;
goto v_reusejp_841_;
}
v_reusejp_841_:
{
return v___x_842_;
}
}
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state___closed__0(void){
_start:
{
lean_object* v___x_845_; lean_object* v___x_846_; lean_object* v___x_847_; 
v___x_845_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone;
v___x_846_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3;
v___x_847_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_847_, 0, v___x_846_);
lean_ctor_set(v___x_847_, 1, v___x_845_);
return v___x_847_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state(void){
_start:
{
lean_object* v___x_848_; 
v___x_848_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state___closed__0);
return v___x_848_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___closed__0(void){
_start:
{
lean_object* v___x_849_; lean_object* v___x_850_; 
v___x_849_ = lean_unsigned_to_nat(2u);
v___x_850_ = lean_nat_to_int(v___x_849_);
return v___x_850_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec(lean_object* v_x_851_){
_start:
{
lean_object* v_zero_852_; uint8_t v_isZero_853_; 
v_zero_852_ = lean_unsigned_to_nat(0u);
v_isZero_853_ = lean_nat_dec_eq(v_x_851_, v_zero_852_);
if (v_isZero_853_ == 1)
{
lean_object* v___x_854_; 
v___x_854_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone___closed__0);
return v___x_854_;
}
else
{
lean_object* v_one_855_; lean_object* v_n_856_; uint8_t v_isZero_857_; 
v_one_855_ = lean_unsigned_to_nat(1u);
v_n_856_ = lean_nat_sub(v_x_851_, v_one_855_);
v_isZero_857_ = lean_nat_dec_eq(v_n_856_, v_zero_852_);
if (v_isZero_857_ == 1)
{
lean_object* v___x_858_; 
lean_dec(v_n_856_);
v___x_858_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___closed__0);
return v___x_858_;
}
else
{
lean_object* v_n_859_; lean_object* v___x_860_; lean_object* v___x_861_; lean_object* v___x_862_; lean_object* v___x_863_; 
v_n_859_ = lean_nat_sub(v_n_856_, v_one_855_);
lean_dec(v_n_856_);
v___x_860_ = lean_nat_add(v_n_859_, v_one_855_);
v___x_861_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec(v___x_860_);
lean_dec(v___x_860_);
v___x_862_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec(v_n_859_);
lean_dec(v_n_859_);
v___x_863_ = lean_int_sub(v___x_861_, v___x_862_);
lean_dec(v___x_862_);
lean_dec(v___x_861_);
return v___x_863_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec___boxed(lean_object* v_x_864_){
_start:
{
lean_object* v_res_865_; 
v_res_865_ = lp_FiniteQuantum_FableHilbertWalk20260819_H045_S__rec(v_x_864_);
lean_dec(v_x_864_);
return v_res_865_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H045DiscreteGroverSearch(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_qz);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_qone);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_qsqrt3);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_instZeroQuad3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instZeroQuad3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instZeroQuad3);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_instOneQuad3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_instOneQuad3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_instOneQuad3);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__uniform);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_v__target);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_R__oracle);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_D__tilde);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_eye4);
lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H045_v0__state);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
