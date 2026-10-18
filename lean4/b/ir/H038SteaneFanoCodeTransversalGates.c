// Lean compiler output
// Module: H038SteaneFanoCodeTransversalGates
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
lean_object* lean_int_neg(lean_object*);
lean_object* l_Int_mul___boxed(lean_object*, lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_emod(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__6;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__7;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__8;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_mul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__0_value;
static const lean_array_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__1_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_list__sum(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_list__sum___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s3"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__16_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__17_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__17_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__18_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqQubitPos(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqQubitPos___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q0"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q3"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__7_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q4"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__9 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__9_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q5"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__10 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__11_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "FableHilbertWalk20260819.H038.QubitPos.q6"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__12_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__12_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__13_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__6;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__5;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__6;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__7;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__8;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__10;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__11_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__11;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__12;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__13_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__13;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__14_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__14;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__15;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__16_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__16;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__17;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__18_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__18;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__19_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__19;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__20_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__20;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__21_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__21;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__22_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__22;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__23_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__23;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__24_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__24;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__25_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__25;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__26_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__26;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__27_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__27;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__28_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__28;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__29_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__29;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__30_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__30;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__31_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__31;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_checkSyndrome(lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_unsigned_to_nat(0u);
v___x_4_ = lean_nat_to_int(v___x_3_);
return v___x_4_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2(void){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; 
v___x_5_ = lean_box(0);
v___x_6_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_7_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_7_, 0, v___x_6_);
lean_ctor_set(v___x_7_, 1, v___x_5_);
return v___x_7_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3(void){
_start:
{
lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_8_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2);
v___x_9_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_10_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_10_, 0, v___x_9_);
lean_ctor_set(v___x_10_, 1, v___x_8_);
return v___x_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__4(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3);
v___x_12_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_13_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_13_, 0, v___x_12_);
lean_ctor_set(v___x_13_, 1, v___x_11_);
return v___x_13_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__5(void){
_start:
{
lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; 
v___x_14_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__4);
v___x_15_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_16_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_16_, 0, v___x_15_);
lean_ctor_set(v___x_16_, 1, v___x_14_);
return v___x_16_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__6(void){
_start:
{
lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; 
v___x_17_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__5);
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_19_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_19_, 0, v___x_18_);
lean_ctor_set(v___x_19_, 1, v___x_17_);
return v___x_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__7(void){
_start:
{
lean_object* v___x_20_; lean_object* v___x_21_; lean_object* v___x_22_; 
v___x_20_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__6);
v___x_21_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_22_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_22_, 0, v___x_21_);
lean_ctor_set(v___x_22_, 1, v___x_20_);
return v___x_22_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__8(void){
_start:
{
lean_object* v___x_23_; lean_object* v___x_24_; lean_object* v___x_25_; 
v___x_23_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__7);
v___x_24_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_25_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_25_, 0, v___x_24_);
lean_ctor_set(v___x_25_, 1, v___x_23_);
return v___x_25_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1(void){
_start:
{
lean_object* v___x_26_; 
v___x_26_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__8);
return v___x_26_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0(void){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; 
v___x_27_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__2);
v___x_28_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_29_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_29_, 0, v___x_28_);
lean_ctor_set(v___x_29_, 1, v___x_27_);
return v___x_29_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__1(void){
_start:
{
lean_object* v___x_30_; lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_30_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0);
v___x_31_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_32_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_32_, 0, v___x_31_);
lean_ctor_set(v___x_32_, 1, v___x_30_);
return v___x_32_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__2(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; 
v___x_33_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__1);
v___x_34_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_35_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_35_, 0, v___x_34_);
lean_ctor_set(v___x_35_, 1, v___x_33_);
return v___x_35_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__3(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; lean_object* v___x_38_; 
v___x_36_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__2);
v___x_37_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_38_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_38_, 0, v___x_37_);
lean_ctor_set(v___x_38_, 1, v___x_36_);
return v___x_38_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__4(void){
_start:
{
lean_object* v___x_39_; lean_object* v___x_40_; lean_object* v___x_41_; 
v___x_39_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__3);
v___x_40_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_41_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_41_, 0, v___x_40_);
lean_ctor_set(v___x_41_, 1, v___x_39_);
return v___x_41_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__5(void){
_start:
{
lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_44_; 
v___x_42_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__4);
v___x_43_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_44_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_44_, 0, v___x_43_);
lean_ctor_set(v___x_44_, 1, v___x_42_);
return v___x_44_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2(void){
_start:
{
lean_object* v___x_45_; 
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__5);
return v___x_45_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__0(void){
_start:
{
lean_object* v___x_46_; lean_object* v___x_47_; lean_object* v___x_48_; 
v___x_46_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2___closed__0);
v___x_47_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_48_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_48_, 0, v___x_47_);
lean_ctor_set(v___x_48_, 1, v___x_46_);
return v___x_48_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1(void){
_start:
{
lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__0);
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_51_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_51_, 0, v___x_50_);
lean_ctor_set(v___x_51_, 1, v___x_49_);
return v___x_51_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__2(void){
_start:
{
lean_object* v___x_52_; lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_52_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1);
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_54_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_54_, 0, v___x_53_);
lean_ctor_set(v___x_54_, 1, v___x_52_);
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__3(void){
_start:
{
lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; 
v___x_55_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__2);
v___x_56_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_57_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_57_, 0, v___x_56_);
lean_ctor_set(v___x_57_, 1, v___x_55_);
return v___x_57_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__4(void){
_start:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; 
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__3);
v___x_59_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_60_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_60_, 0, v___x_59_);
lean_ctor_set(v___x_60_, 1, v___x_58_);
return v___x_60_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3(void){
_start:
{
lean_object* v___x_61_; 
v___x_61_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__4);
return v___x_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0(lean_object* v_x_62_, lean_object* v_x_63_){
_start:
{
if (lean_obj_tag(v_x_63_) == 0)
{
return v_x_62_;
}
else
{
lean_object* v_head_64_; lean_object* v_tail_65_; lean_object* v___x_66_; 
v_head_64_ = lean_ctor_get(v_x_63_, 0);
v_tail_65_ = lean_ctor_get(v_x_63_, 1);
v___x_66_ = lean_int_add(v_x_62_, v_head_64_);
lean_dec(v_x_62_);
v_x_62_ = v___x_66_;
v_x_63_ = v_tail_65_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0___boxed(lean_object* v_x_68_, lean_object* v_x_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0(v_x_68_, v_x_69_);
lean_dec(v_x_69_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod(lean_object* v_l1_74_, lean_object* v_l2_75_){
_start:
{
lean_object* v___f_76_; lean_object* v___x_77_; lean_object* v___x_78_; lean_object* v___x_79_; lean_object* v___x_80_; 
v___f_76_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__0));
v___x_77_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_78_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod___closed__1));
v___x_79_ = l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(v___f_76_, v_l1_74_, v_l2_75_, v___x_78_);
v___x_80_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0(v___x_77_, v___x_79_);
lean_dec(v___x_79_);
return v___x_80_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_list__sum(lean_object* v_l_81_){
_start:
{
lean_object* v___x_82_; lean_object* v___x_83_; 
v___x_82_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_83_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H038_inner__prod_spec__0(v___x_82_, v_l_81_);
return v___x_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_list__sum___boxed(lean_object* v_l_84_){
_start:
{
lean_object* v_res_85_; 
v_res_85_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_list__sum(v_l_84_);
lean_dec(v_l_84_);
return v_res_85_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0(void){
_start:
{
lean_object* v___x_86_; lean_object* v___x_87_; 
v___x_86_ = lean_unsigned_to_nat(2u);
v___x_87_ = lean_nat_to_int(v___x_86_);
return v___x_87_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__1(void){
_start:
{
lean_object* v___x_88_; lean_object* v___x_89_; 
v___x_88_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_89_ = lean_int_neg(v___x_88_);
return v___x_89_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase(lean_object* v_overlap_90_){
_start:
{
lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; uint8_t v___x_94_; 
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___x_92_ = lean_int_emod(v_overlap_90_, v___x_91_);
v___x_93_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_94_ = lean_int_dec_eq(v___x_92_, v___x_93_);
lean_dec(v___x_92_);
if (v___x_94_ == 0)
{
lean_object* v___x_95_; 
v___x_95_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__1);
return v___x_95_;
}
else
{
lean_object* v___x_96_; 
v___x_96_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
return v___x_96_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___boxed(lean_object* v_overlap_97_){
_start:
{
lean_object* v_res_98_; 
v_res_98_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase(v_overlap_97_);
lean_dec(v_overlap_97_);
return v_res_98_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__0(void){
_start:
{
lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; 
v___x_99_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3___closed__1);
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_101_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_101_, 0, v___x_100_);
lean_ctor_set(v___x_101_, 1, v___x_99_);
return v___x_101_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__1(void){
_start:
{
lean_object* v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; 
v___x_102_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__0);
v___x_103_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_104_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_104_, 0, v___x_103_);
lean_ctor_set(v___x_104_, 1, v___x_102_);
return v___x_104_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__2(void){
_start:
{
lean_object* v___x_105_; lean_object* v___x_106_; lean_object* v___x_107_; 
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__1);
v___x_106_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_107_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_107_, 0, v___x_106_);
lean_ctor_set(v___x_107_, 1, v___x_105_);
return v___x_107_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll(void){
_start:
{
lean_object* v___x_108_; 
v___x_108_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll___closed__2);
return v___x_108_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3_decEq(lean_object* v_x_109_, lean_object* v_x_110_){
_start:
{
lean_object* v_s1_111_; lean_object* v_s2_112_; lean_object* v_s3_113_; lean_object* v_s1_114_; lean_object* v_s2_115_; lean_object* v_s3_116_; uint8_t v___x_117_; 
v_s1_111_ = lean_ctor_get(v_x_109_, 0);
v_s2_112_ = lean_ctor_get(v_x_109_, 1);
v_s3_113_ = lean_ctor_get(v_x_109_, 2);
v_s1_114_ = lean_ctor_get(v_x_110_, 0);
v_s2_115_ = lean_ctor_get(v_x_110_, 1);
v_s3_116_ = lean_ctor_get(v_x_110_, 2);
v___x_117_ = lean_int_dec_eq(v_s1_111_, v_s1_114_);
if (v___x_117_ == 0)
{
return v___x_117_;
}
else
{
uint8_t v___x_118_; 
v___x_118_ = lean_int_dec_eq(v_s2_112_, v_s2_115_);
if (v___x_118_ == 0)
{
return v___x_118_;
}
else
{
uint8_t v___x_119_; 
v___x_119_ = lean_int_dec_eq(v_s3_113_, v_s3_116_);
return v___x_119_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3_decEq___boxed(lean_object* v_x_120_, lean_object* v_x_121_){
_start:
{
uint8_t v_res_122_; lean_object* v_r_123_; 
v_res_122_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3_decEq(v_x_120_, v_x_121_);
lean_dec_ref(v_x_121_);
lean_dec_ref(v_x_120_);
v_r_123_ = lean_box(v_res_122_);
return v_r_123_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3(lean_object* v_x_124_, lean_object* v_x_125_){
_start:
{
uint8_t v___x_126_; 
v___x_126_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3_decEq(v_x_124_, v_x_125_);
return v___x_126_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3___boxed(lean_object* v_x_127_, lean_object* v_x_128_){
_start:
{
uint8_t v_res_129_; lean_object* v_r_130_; 
v_res_129_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqSyndrome3(v_x_127_, v_x_128_);
lean_dec_ref(v_x_128_);
lean_dec_ref(v_x_127_);
v_r_130_ = lean_box(v_res_129_);
return v_r_130_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_144_; lean_object* v___x_145_; 
v___x_144_ = lean_unsigned_to_nat(6u);
v___x_145_ = lean_nat_to_int(v___x_144_);
return v___x_145_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_147_; lean_object* v___x_148_; 
v___x_147_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__0));
v___x_148_ = lean_string_length(v___x_147_);
return v___x_148_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_149_; lean_object* v___x_150_; 
v___x_149_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__9);
v___x_150_ = lean_nat_to_int(v___x_149_);
return v___x_150_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg(lean_object* v_x_164_){
_start:
{
lean_object* v_s1_165_; lean_object* v_s2_166_; lean_object* v_s3_167_; lean_object* v___x_168_; lean_object* v___x_169_; lean_object* v___x_170_; uint8_t v___y_172_; lean_object* v___y_173_; lean_object* v___y_174_; lean_object* v___y_186_; lean_object* v___y_187_; uint8_t v___y_188_; lean_object* v___y_189_; lean_object* v___y_190_; lean_object* v___y_208_; lean_object* v___x_228_; lean_object* v___x_229_; uint8_t v___x_230_; 
v_s1_165_ = lean_ctor_get(v_x_164_, 0);
v_s2_166_ = lean_ctor_get(v_x_164_, 1);
v_s3_167_ = lean_ctor_get(v_x_164_, 2);
v___x_168_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__5));
v___x_169_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__6));
v___x_170_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__7);
v___x_228_ = lean_unsigned_to_nat(0u);
v___x_229_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_230_ = lean_int_dec_lt(v_s1_165_, v___x_229_);
if (v___x_230_ == 0)
{
lean_object* v___x_231_; lean_object* v___x_232_; 
v___x_231_ = l_Int_repr(v_s1_165_);
v___x_232_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_232_, 0, v___x_231_);
v___y_208_ = v___x_232_;
goto v___jp_207_;
}
else
{
lean_object* v___x_233_; lean_object* v___x_234_; lean_object* v___x_235_; 
v___x_233_ = l_Int_repr(v_s1_165_);
v___x_234_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_234_, 0, v___x_233_);
v___x_235_ = l_Repr_addAppParen(v___x_234_, v___x_228_);
v___y_208_ = v___x_235_;
goto v___jp_207_;
}
v___jp_171_:
{
lean_object* v___x_175_; lean_object* v___x_176_; lean_object* v___x_177_; lean_object* v___x_178_; lean_object* v___x_179_; lean_object* v___x_180_; lean_object* v___x_181_; lean_object* v___x_182_; lean_object* v___x_183_; lean_object* v___x_184_; 
v___x_175_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_175_, 0, v___x_170_);
lean_ctor_set(v___x_175_, 1, v___y_174_);
v___x_176_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_176_, 0, v___x_175_);
lean_ctor_set_uint8(v___x_176_, sizeof(void*)*1, v___y_172_);
v___x_177_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_177_, 0, v___y_173_);
lean_ctor_set(v___x_177_, 1, v___x_176_);
v___x_178_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__10);
v___x_179_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__11));
v___x_180_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_180_, 0, v___x_179_);
lean_ctor_set(v___x_180_, 1, v___x_177_);
v___x_181_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__12));
v___x_182_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_182_, 0, v___x_180_);
lean_ctor_set(v___x_182_, 1, v___x_181_);
v___x_183_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_183_, 0, v___x_178_);
lean_ctor_set(v___x_183_, 1, v___x_182_);
v___x_184_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_184_, 0, v___x_183_);
lean_ctor_set_uint8(v___x_184_, sizeof(void*)*1, v___y_172_);
return v___x_184_;
}
v___jp_185_:
{
lean_object* v___x_191_; lean_object* v___x_192_; lean_object* v___x_193_; lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; lean_object* v___x_197_; lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_200_; uint8_t v___x_201_; 
v___x_191_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_191_, 0, v___x_170_);
lean_ctor_set(v___x_191_, 1, v___y_190_);
v___x_192_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_192_, 0, v___x_191_);
lean_ctor_set_uint8(v___x_192_, sizeof(void*)*1, v___y_188_);
v___x_193_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_193_, 0, v___y_186_);
lean_ctor_set(v___x_193_, 1, v___x_192_);
lean_inc(v___y_189_);
v___x_194_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_194_, 0, v___x_193_);
lean_ctor_set(v___x_194_, 1, v___y_189_);
lean_inc(v___y_187_);
v___x_195_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_195_, 0, v___x_194_);
lean_ctor_set(v___x_195_, 1, v___y_187_);
v___x_196_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__14));
v___x_197_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_197_, 0, v___x_195_);
lean_ctor_set(v___x_197_, 1, v___x_196_);
v___x_198_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_198_, 0, v___x_197_);
lean_ctor_set(v___x_198_, 1, v___x_168_);
v___x_199_ = lean_unsigned_to_nat(0u);
v___x_200_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_201_ = lean_int_dec_lt(v_s3_167_, v___x_200_);
if (v___x_201_ == 0)
{
lean_object* v___x_202_; lean_object* v___x_203_; 
v___x_202_ = l_Int_repr(v_s3_167_);
v___x_203_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_203_, 0, v___x_202_);
v___y_172_ = v___y_188_;
v___y_173_ = v___x_198_;
v___y_174_ = v___x_203_;
goto v___jp_171_;
}
else
{
lean_object* v___x_204_; lean_object* v___x_205_; lean_object* v___x_206_; 
v___x_204_ = l_Int_repr(v_s3_167_);
v___x_205_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_205_, 0, v___x_204_);
v___x_206_ = l_Repr_addAppParen(v___x_205_, v___x_199_);
v___y_172_ = v___y_188_;
v___y_173_ = v___x_198_;
v___y_174_ = v___x_206_;
goto v___jp_171_;
}
}
v___jp_207_:
{
lean_object* v___x_209_; uint8_t v___x_210_; lean_object* v___x_211_; lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_214_; lean_object* v___x_215_; lean_object* v___x_216_; lean_object* v___x_217_; lean_object* v___x_218_; lean_object* v___x_219_; lean_object* v___x_220_; lean_object* v___x_221_; uint8_t v___x_222_; 
v___x_209_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_209_, 0, v___x_170_);
lean_ctor_set(v___x_209_, 1, v___y_208_);
v___x_210_ = 0;
v___x_211_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_211_, 0, v___x_209_);
lean_ctor_set_uint8(v___x_211_, sizeof(void*)*1, v___x_210_);
v___x_212_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_212_, 0, v___x_169_);
lean_ctor_set(v___x_212_, 1, v___x_211_);
v___x_213_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__16));
v___x_214_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_214_, 0, v___x_212_);
lean_ctor_set(v___x_214_, 1, v___x_213_);
v___x_215_ = lean_box(1);
v___x_216_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_216_, 0, v___x_214_);
lean_ctor_set(v___x_216_, 1, v___x_215_);
v___x_217_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___closed__18));
v___x_218_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_218_, 0, v___x_216_);
lean_ctor_set(v___x_218_, 1, v___x_217_);
v___x_219_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_219_, 0, v___x_218_);
lean_ctor_set(v___x_219_, 1, v___x_168_);
v___x_220_ = lean_unsigned_to_nat(0u);
v___x_221_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_222_ = lean_int_dec_lt(v_s2_166_, v___x_221_);
if (v___x_222_ == 0)
{
lean_object* v___x_223_; lean_object* v___x_224_; 
v___x_223_ = l_Int_repr(v_s2_166_);
v___x_224_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_224_, 0, v___x_223_);
v___y_186_ = v___x_219_;
v___y_187_ = v___x_215_;
v___y_188_ = v___x_210_;
v___y_189_ = v___x_213_;
v___y_190_ = v___x_224_;
goto v___jp_185_;
}
else
{
lean_object* v___x_225_; lean_object* v___x_226_; lean_object* v___x_227_; 
v___x_225_ = l_Int_repr(v_s2_166_);
v___x_226_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_226_, 0, v___x_225_);
v___x_227_ = l_Repr_addAppParen(v___x_226_, v___x_220_);
v___y_186_ = v___x_219_;
v___y_187_ = v___x_215_;
v___y_188_ = v___x_210_;
v___y_189_ = v___x_213_;
v___y_190_ = v___x_227_;
goto v___jp_185_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg___boxed(lean_object* v_x_236_){
_start:
{
lean_object* v_res_237_; 
v_res_237_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg(v_x_236_);
lean_dec_ref(v_x_236_);
return v_res_237_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr(lean_object* v_x_238_, lean_object* v_prec_239_){
_start:
{
lean_object* v___x_240_; 
v___x_240_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___redArg(v_x_238_);
return v___x_240_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr___boxed(lean_object* v_x_241_, lean_object* v_prec_242_){
_start:
{
lean_object* v_res_243_; 
v_res_243_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprSyndrome3_repr(v_x_241_, v_prec_242_);
lean_dec(v_prec_242_);
lean_dec_ref(v_x_241_);
return v_res_243_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx(uint8_t v_x_246_){
_start:
{
switch(v_x_246_)
{
case 0:
{
lean_object* v___x_247_; 
v___x_247_ = lean_unsigned_to_nat(0u);
return v___x_247_;
}
case 1:
{
lean_object* v___x_248_; 
v___x_248_ = lean_unsigned_to_nat(1u);
return v___x_248_;
}
case 2:
{
lean_object* v___x_249_; 
v___x_249_ = lean_unsigned_to_nat(2u);
return v___x_249_;
}
case 3:
{
lean_object* v___x_250_; 
v___x_250_ = lean_unsigned_to_nat(3u);
return v___x_250_;
}
case 4:
{
lean_object* v___x_251_; 
v___x_251_ = lean_unsigned_to_nat(4u);
return v___x_251_;
}
case 5:
{
lean_object* v___x_252_; 
v___x_252_ = lean_unsigned_to_nat(5u);
return v___x_252_;
}
default: 
{
lean_object* v___x_253_; 
v___x_253_ = lean_unsigned_to_nat(6u);
return v___x_253_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx___boxed(lean_object* v_x_254_){
_start:
{
uint8_t v_x_boxed_255_; lean_object* v_res_256_; 
v_x_boxed_255_ = lean_unbox(v_x_254_);
v_res_256_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx(v_x_boxed_255_);
return v_res_256_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_toCtorIdx(uint8_t v_x_257_){
_start:
{
lean_object* v___x_258_; 
v___x_258_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx(v_x_257_);
return v___x_258_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_toCtorIdx___boxed(lean_object* v_x_259_){
_start:
{
uint8_t v_x_4__boxed_260_; lean_object* v_res_261_; 
v_x_4__boxed_260_ = lean_unbox(v_x_259_);
v_res_261_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_toCtorIdx(v_x_4__boxed_260_);
return v_res_261_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___redArg(lean_object* v_k_262_){
_start:
{
lean_inc(v_k_262_);
return v_k_262_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___redArg___boxed(lean_object* v_k_263_){
_start:
{
lean_object* v_res_264_; 
v_res_264_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___redArg(v_k_263_);
lean_dec(v_k_263_);
return v_res_264_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim(lean_object* v_motive_265_, lean_object* v_ctorIdx_266_, uint8_t v_t_267_, lean_object* v_h_268_, lean_object* v_k_269_){
_start:
{
lean_inc(v_k_269_);
return v_k_269_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim___boxed(lean_object* v_motive_270_, lean_object* v_ctorIdx_271_, lean_object* v_t_272_, lean_object* v_h_273_, lean_object* v_k_274_){
_start:
{
uint8_t v_t_boxed_275_; lean_object* v_res_276_; 
v_t_boxed_275_ = lean_unbox(v_t_272_);
v_res_276_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorElim(v_motive_270_, v_ctorIdx_271_, v_t_boxed_275_, v_h_273_, v_k_274_);
lean_dec(v_k_274_);
lean_dec(v_ctorIdx_271_);
return v_res_276_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___redArg(lean_object* v_q0_277_){
_start:
{
lean_inc(v_q0_277_);
return v_q0_277_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___redArg___boxed(lean_object* v_q0_278_){
_start:
{
lean_object* v_res_279_; 
v_res_279_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___redArg(v_q0_278_);
lean_dec(v_q0_278_);
return v_res_279_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim(lean_object* v_motive_280_, uint8_t v_t_281_, lean_object* v_h_282_, lean_object* v_q0_283_){
_start:
{
lean_inc(v_q0_283_);
return v_q0_283_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim___boxed(lean_object* v_motive_284_, lean_object* v_t_285_, lean_object* v_h_286_, lean_object* v_q0_287_){
_start:
{
uint8_t v_t_boxed_288_; lean_object* v_res_289_; 
v_t_boxed_288_ = lean_unbox(v_t_285_);
v_res_289_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q0_elim(v_motive_284_, v_t_boxed_288_, v_h_286_, v_q0_287_);
lean_dec(v_q0_287_);
return v_res_289_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___redArg(lean_object* v_q1_290_){
_start:
{
lean_inc(v_q1_290_);
return v_q1_290_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___redArg___boxed(lean_object* v_q1_291_){
_start:
{
lean_object* v_res_292_; 
v_res_292_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___redArg(v_q1_291_);
lean_dec(v_q1_291_);
return v_res_292_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim(lean_object* v_motive_293_, uint8_t v_t_294_, lean_object* v_h_295_, lean_object* v_q1_296_){
_start:
{
lean_inc(v_q1_296_);
return v_q1_296_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim___boxed(lean_object* v_motive_297_, lean_object* v_t_298_, lean_object* v_h_299_, lean_object* v_q1_300_){
_start:
{
uint8_t v_t_boxed_301_; lean_object* v_res_302_; 
v_t_boxed_301_ = lean_unbox(v_t_298_);
v_res_302_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q1_elim(v_motive_297_, v_t_boxed_301_, v_h_299_, v_q1_300_);
lean_dec(v_q1_300_);
return v_res_302_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___redArg(lean_object* v_q2_303_){
_start:
{
lean_inc(v_q2_303_);
return v_q2_303_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___redArg___boxed(lean_object* v_q2_304_){
_start:
{
lean_object* v_res_305_; 
v_res_305_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___redArg(v_q2_304_);
lean_dec(v_q2_304_);
return v_res_305_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim(lean_object* v_motive_306_, uint8_t v_t_307_, lean_object* v_h_308_, lean_object* v_q2_309_){
_start:
{
lean_inc(v_q2_309_);
return v_q2_309_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim___boxed(lean_object* v_motive_310_, lean_object* v_t_311_, lean_object* v_h_312_, lean_object* v_q2_313_){
_start:
{
uint8_t v_t_boxed_314_; lean_object* v_res_315_; 
v_t_boxed_314_ = lean_unbox(v_t_311_);
v_res_315_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q2_elim(v_motive_310_, v_t_boxed_314_, v_h_312_, v_q2_313_);
lean_dec(v_q2_313_);
return v_res_315_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___redArg(lean_object* v_q3_316_){
_start:
{
lean_inc(v_q3_316_);
return v_q3_316_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___redArg___boxed(lean_object* v_q3_317_){
_start:
{
lean_object* v_res_318_; 
v_res_318_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___redArg(v_q3_317_);
lean_dec(v_q3_317_);
return v_res_318_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim(lean_object* v_motive_319_, uint8_t v_t_320_, lean_object* v_h_321_, lean_object* v_q3_322_){
_start:
{
lean_inc(v_q3_322_);
return v_q3_322_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim___boxed(lean_object* v_motive_323_, lean_object* v_t_324_, lean_object* v_h_325_, lean_object* v_q3_326_){
_start:
{
uint8_t v_t_boxed_327_; lean_object* v_res_328_; 
v_t_boxed_327_ = lean_unbox(v_t_324_);
v_res_328_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q3_elim(v_motive_323_, v_t_boxed_327_, v_h_325_, v_q3_326_);
lean_dec(v_q3_326_);
return v_res_328_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___redArg(lean_object* v_q4_329_){
_start:
{
lean_inc(v_q4_329_);
return v_q4_329_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___redArg___boxed(lean_object* v_q4_330_){
_start:
{
lean_object* v_res_331_; 
v_res_331_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___redArg(v_q4_330_);
lean_dec(v_q4_330_);
return v_res_331_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim(lean_object* v_motive_332_, uint8_t v_t_333_, lean_object* v_h_334_, lean_object* v_q4_335_){
_start:
{
lean_inc(v_q4_335_);
return v_q4_335_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim___boxed(lean_object* v_motive_336_, lean_object* v_t_337_, lean_object* v_h_338_, lean_object* v_q4_339_){
_start:
{
uint8_t v_t_boxed_340_; lean_object* v_res_341_; 
v_t_boxed_340_ = lean_unbox(v_t_337_);
v_res_341_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q4_elim(v_motive_336_, v_t_boxed_340_, v_h_338_, v_q4_339_);
lean_dec(v_q4_339_);
return v_res_341_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___redArg(lean_object* v_q5_342_){
_start:
{
lean_inc(v_q5_342_);
return v_q5_342_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___redArg___boxed(lean_object* v_q5_343_){
_start:
{
lean_object* v_res_344_; 
v_res_344_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___redArg(v_q5_343_);
lean_dec(v_q5_343_);
return v_res_344_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim(lean_object* v_motive_345_, uint8_t v_t_346_, lean_object* v_h_347_, lean_object* v_q5_348_){
_start:
{
lean_inc(v_q5_348_);
return v_q5_348_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim___boxed(lean_object* v_motive_349_, lean_object* v_t_350_, lean_object* v_h_351_, lean_object* v_q5_352_){
_start:
{
uint8_t v_t_boxed_353_; lean_object* v_res_354_; 
v_t_boxed_353_ = lean_unbox(v_t_350_);
v_res_354_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q5_elim(v_motive_349_, v_t_boxed_353_, v_h_351_, v_q5_352_);
lean_dec(v_q5_352_);
return v_res_354_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___redArg(lean_object* v_q6_355_){
_start:
{
lean_inc(v_q6_355_);
return v_q6_355_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___redArg___boxed(lean_object* v_q6_356_){
_start:
{
lean_object* v_res_357_; 
v_res_357_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___redArg(v_q6_356_);
lean_dec(v_q6_356_);
return v_res_357_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim(lean_object* v_motive_358_, uint8_t v_t_359_, lean_object* v_h_360_, lean_object* v_q6_361_){
_start:
{
lean_inc(v_q6_361_);
return v_q6_361_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim___boxed(lean_object* v_motive_362_, lean_object* v_t_363_, lean_object* v_h_364_, lean_object* v_q6_365_){
_start:
{
uint8_t v_t_boxed_366_; lean_object* v_res_367_; 
v_t_boxed_366_ = lean_unbox(v_t_363_);
v_res_367_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_q6_elim(v_motive_362_, v_t_boxed_366_, v_h_364_, v_q6_365_);
lean_dec(v_q6_365_);
return v_res_367_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ofNat(lean_object* v_n_368_){
_start:
{
lean_object* v___x_369_; uint8_t v___x_370_; 
v___x_369_ = lean_unsigned_to_nat(2u);
v___x_370_ = lean_nat_dec_le(v_n_368_, v___x_369_);
if (v___x_370_ == 0)
{
lean_object* v___x_371_; uint8_t v___x_372_; 
v___x_371_ = lean_unsigned_to_nat(4u);
v___x_372_ = lean_nat_dec_le(v_n_368_, v___x_371_);
if (v___x_372_ == 0)
{
lean_object* v___x_373_; uint8_t v___x_374_; 
v___x_373_ = lean_unsigned_to_nat(5u);
v___x_374_ = lean_nat_dec_le(v_n_368_, v___x_373_);
if (v___x_374_ == 0)
{
uint8_t v___x_375_; 
v___x_375_ = 6;
return v___x_375_;
}
else
{
uint8_t v___x_376_; 
v___x_376_ = 5;
return v___x_376_;
}
}
else
{
lean_object* v___x_377_; uint8_t v___x_378_; 
v___x_377_ = lean_unsigned_to_nat(3u);
v___x_378_ = lean_nat_dec_le(v_n_368_, v___x_377_);
if (v___x_378_ == 0)
{
uint8_t v___x_379_; 
v___x_379_ = 4;
return v___x_379_;
}
else
{
uint8_t v___x_380_; 
v___x_380_ = 3;
return v___x_380_;
}
}
}
else
{
lean_object* v___x_381_; uint8_t v___x_382_; 
v___x_381_ = lean_unsigned_to_nat(0u);
v___x_382_ = lean_nat_dec_le(v_n_368_, v___x_381_);
if (v___x_382_ == 0)
{
lean_object* v___x_383_; uint8_t v___x_384_; 
v___x_383_ = lean_unsigned_to_nat(1u);
v___x_384_ = lean_nat_dec_le(v_n_368_, v___x_383_);
if (v___x_384_ == 0)
{
uint8_t v___x_385_; 
v___x_385_ = 2;
return v___x_385_;
}
else
{
uint8_t v___x_386_; 
v___x_386_ = 1;
return v___x_386_;
}
}
else
{
uint8_t v___x_387_; 
v___x_387_ = 0;
return v___x_387_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ofNat___boxed(lean_object* v_n_388_){
_start:
{
uint8_t v_res_389_; lean_object* v_r_390_; 
v_res_389_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ofNat(v_n_388_);
lean_dec(v_n_388_);
v_r_390_ = lean_box(v_res_389_);
return v_r_390_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqQubitPos(uint8_t v_x_391_, uint8_t v_y_392_){
_start:
{
lean_object* v___x_393_; lean_object* v___x_394_; uint8_t v___x_395_; 
v___x_393_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx(v_x_391_);
v___x_394_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_QubitPos_ctorIdx(v_y_392_);
v___x_395_ = lean_nat_dec_eq(v___x_393_, v___x_394_);
lean_dec(v___x_394_);
lean_dec(v___x_393_);
return v___x_395_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqQubitPos___boxed(lean_object* v_x_396_, lean_object* v_y_397_){
_start:
{
uint8_t v_x_13__boxed_398_; uint8_t v_y_14__boxed_399_; uint8_t v_res_400_; lean_object* v_r_401_; 
v_x_13__boxed_398_ = lean_unbox(v_x_396_);
v_y_14__boxed_399_ = lean_unbox(v_y_397_);
v_res_400_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instDecidableEqQubitPos(v_x_13__boxed_398_, v_y_14__boxed_399_);
v_r_401_ = lean_box(v_res_400_);
return v_r_401_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr(uint8_t v_x_423_, lean_object* v_prec_424_){
_start:
{
lean_object* v___y_426_; lean_object* v___y_433_; lean_object* v___y_440_; lean_object* v___y_447_; lean_object* v___y_454_; lean_object* v___y_461_; lean_object* v___y_468_; 
switch(v_x_423_)
{
case 0:
{
lean_object* v___x_474_; uint8_t v___x_475_; 
v___x_474_ = lean_unsigned_to_nat(1024u);
v___x_475_ = lean_nat_dec_le(v___x_474_, v_prec_424_);
if (v___x_475_ == 0)
{
lean_object* v___x_476_; 
v___x_476_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_426_ = v___x_476_;
goto v___jp_425_;
}
else
{
lean_object* v___x_477_; 
v___x_477_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_426_ = v___x_477_;
goto v___jp_425_;
}
}
case 1:
{
lean_object* v___x_478_; uint8_t v___x_479_; 
v___x_478_ = lean_unsigned_to_nat(1024u);
v___x_479_ = lean_nat_dec_le(v___x_478_, v_prec_424_);
if (v___x_479_ == 0)
{
lean_object* v___x_480_; 
v___x_480_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_433_ = v___x_480_;
goto v___jp_432_;
}
else
{
lean_object* v___x_481_; 
v___x_481_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_433_ = v___x_481_;
goto v___jp_432_;
}
}
case 2:
{
lean_object* v___x_482_; uint8_t v___x_483_; 
v___x_482_ = lean_unsigned_to_nat(1024u);
v___x_483_ = lean_nat_dec_le(v___x_482_, v_prec_424_);
if (v___x_483_ == 0)
{
lean_object* v___x_484_; 
v___x_484_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_440_ = v___x_484_;
goto v___jp_439_;
}
else
{
lean_object* v___x_485_; 
v___x_485_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_440_ = v___x_485_;
goto v___jp_439_;
}
}
case 3:
{
lean_object* v___x_486_; uint8_t v___x_487_; 
v___x_486_ = lean_unsigned_to_nat(1024u);
v___x_487_ = lean_nat_dec_le(v___x_486_, v_prec_424_);
if (v___x_487_ == 0)
{
lean_object* v___x_488_; 
v___x_488_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_447_ = v___x_488_;
goto v___jp_446_;
}
else
{
lean_object* v___x_489_; 
v___x_489_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_447_ = v___x_489_;
goto v___jp_446_;
}
}
case 4:
{
lean_object* v___x_490_; uint8_t v___x_491_; 
v___x_490_ = lean_unsigned_to_nat(1024u);
v___x_491_ = lean_nat_dec_le(v___x_490_, v_prec_424_);
if (v___x_491_ == 0)
{
lean_object* v___x_492_; 
v___x_492_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_454_ = v___x_492_;
goto v___jp_453_;
}
else
{
lean_object* v___x_493_; 
v___x_493_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_454_ = v___x_493_;
goto v___jp_453_;
}
}
case 5:
{
lean_object* v___x_494_; uint8_t v___x_495_; 
v___x_494_ = lean_unsigned_to_nat(1024u);
v___x_495_ = lean_nat_dec_le(v___x_494_, v_prec_424_);
if (v___x_495_ == 0)
{
lean_object* v___x_496_; 
v___x_496_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_461_ = v___x_496_;
goto v___jp_460_;
}
else
{
lean_object* v___x_497_; 
v___x_497_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_461_ = v___x_497_;
goto v___jp_460_;
}
}
default: 
{
lean_object* v___x_498_; uint8_t v___x_499_; 
v___x_498_ = lean_unsigned_to_nat(1024u);
v___x_499_ = lean_nat_dec_le(v___x_498_, v_prec_424_);
if (v___x_499_ == 0)
{
lean_object* v___x_500_; 
v___x_500_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_commutePhase___closed__0);
v___y_468_ = v___x_500_;
goto v___jp_467_;
}
else
{
lean_object* v___x_501_; 
v___x_501_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___y_468_ = v___x_501_;
goto v___jp_467_;
}
}
}
v___jp_425_:
{
lean_object* v___x_427_; lean_object* v___x_428_; uint8_t v___x_429_; lean_object* v___x_430_; lean_object* v___x_431_; 
v___x_427_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__1));
lean_inc(v___y_426_);
v___x_428_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_428_, 0, v___y_426_);
lean_ctor_set(v___x_428_, 1, v___x_427_);
v___x_429_ = 0;
v___x_430_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_430_, 0, v___x_428_);
lean_ctor_set_uint8(v___x_430_, sizeof(void*)*1, v___x_429_);
v___x_431_ = l_Repr_addAppParen(v___x_430_, v_prec_424_);
return v___x_431_;
}
v___jp_432_:
{
lean_object* v___x_434_; lean_object* v___x_435_; uint8_t v___x_436_; lean_object* v___x_437_; lean_object* v___x_438_; 
v___x_434_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__3));
lean_inc(v___y_433_);
v___x_435_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_435_, 0, v___y_433_);
lean_ctor_set(v___x_435_, 1, v___x_434_);
v___x_436_ = 0;
v___x_437_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_437_, 0, v___x_435_);
lean_ctor_set_uint8(v___x_437_, sizeof(void*)*1, v___x_436_);
v___x_438_ = l_Repr_addAppParen(v___x_437_, v_prec_424_);
return v___x_438_;
}
v___jp_439_:
{
lean_object* v___x_441_; lean_object* v___x_442_; uint8_t v___x_443_; lean_object* v___x_444_; lean_object* v___x_445_; 
v___x_441_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__5));
lean_inc(v___y_440_);
v___x_442_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_442_, 0, v___y_440_);
lean_ctor_set(v___x_442_, 1, v___x_441_);
v___x_443_ = 0;
v___x_444_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_444_, 0, v___x_442_);
lean_ctor_set_uint8(v___x_444_, sizeof(void*)*1, v___x_443_);
v___x_445_ = l_Repr_addAppParen(v___x_444_, v_prec_424_);
return v___x_445_;
}
v___jp_446_:
{
lean_object* v___x_448_; lean_object* v___x_449_; uint8_t v___x_450_; lean_object* v___x_451_; lean_object* v___x_452_; 
v___x_448_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__7));
lean_inc(v___y_447_);
v___x_449_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_449_, 0, v___y_447_);
lean_ctor_set(v___x_449_, 1, v___x_448_);
v___x_450_ = 0;
v___x_451_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_451_, 0, v___x_449_);
lean_ctor_set_uint8(v___x_451_, sizeof(void*)*1, v___x_450_);
v___x_452_ = l_Repr_addAppParen(v___x_451_, v_prec_424_);
return v___x_452_;
}
v___jp_453_:
{
lean_object* v___x_455_; lean_object* v___x_456_; uint8_t v___x_457_; lean_object* v___x_458_; lean_object* v___x_459_; 
v___x_455_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__9));
lean_inc(v___y_454_);
v___x_456_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_456_, 0, v___y_454_);
lean_ctor_set(v___x_456_, 1, v___x_455_);
v___x_457_ = 0;
v___x_458_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_458_, 0, v___x_456_);
lean_ctor_set_uint8(v___x_458_, sizeof(void*)*1, v___x_457_);
v___x_459_ = l_Repr_addAppParen(v___x_458_, v_prec_424_);
return v___x_459_;
}
v___jp_460_:
{
lean_object* v___x_462_; lean_object* v___x_463_; uint8_t v___x_464_; lean_object* v___x_465_; lean_object* v___x_466_; 
v___x_462_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__11));
lean_inc(v___y_461_);
v___x_463_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_463_, 0, v___y_461_);
lean_ctor_set(v___x_463_, 1, v___x_462_);
v___x_464_ = 0;
v___x_465_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_465_, 0, v___x_463_);
lean_ctor_set_uint8(v___x_465_, sizeof(void*)*1, v___x_464_);
v___x_466_ = l_Repr_addAppParen(v___x_465_, v_prec_424_);
return v___x_466_;
}
v___jp_467_:
{
lean_object* v___x_469_; lean_object* v___x_470_; uint8_t v___x_471_; lean_object* v___x_472_; lean_object* v___x_473_; 
v___x_469_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___closed__13));
lean_inc(v___y_468_);
v___x_470_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_470_, 0, v___y_468_);
lean_ctor_set(v___x_470_, 1, v___x_469_);
v___x_471_ = 0;
v___x_472_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_472_, 0, v___x_470_);
lean_ctor_set_uint8(v___x_472_, sizeof(void*)*1, v___x_471_);
v___x_473_ = l_Repr_addAppParen(v___x_472_, v_prec_424_);
return v___x_473_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr___boxed(lean_object* v_x_502_, lean_object* v_prec_503_){
_start:
{
uint8_t v_x_397__boxed_504_; lean_object* v_res_505_; 
v_x_397__boxed_504_ = lean_unbox(v_x_502_);
v_res_505_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_instReprQubitPos_repr(v_x_397__boxed_504_, v_prec_503_);
lean_dec(v_prec_503_);
return v_res_505_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__0(void){
_start:
{
lean_object* v___x_508_; lean_object* v___x_509_; lean_object* v___x_510_; 
v___x_508_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_509_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_510_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_510_, 0, v___x_509_);
lean_ctor_set(v___x_510_, 1, v___x_508_);
lean_ctor_set(v___x_510_, 2, v___x_508_);
return v___x_510_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__1(void){
_start:
{
lean_object* v___x_511_; lean_object* v___x_512_; lean_object* v___x_513_; 
v___x_511_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_512_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_513_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_513_, 0, v___x_512_);
lean_ctor_set(v___x_513_, 1, v___x_511_);
lean_ctor_set(v___x_513_, 2, v___x_512_);
return v___x_513_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__2(void){
_start:
{
lean_object* v___x_514_; lean_object* v___x_515_; lean_object* v___x_516_; 
v___x_514_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_515_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_516_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_516_, 0, v___x_515_);
lean_ctor_set(v___x_516_, 1, v___x_515_);
lean_ctor_set(v___x_516_, 2, v___x_514_);
return v___x_516_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__3(void){
_start:
{
lean_object* v___x_517_; lean_object* v___x_518_; lean_object* v___x_519_; 
v___x_517_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_518_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_519_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_519_, 0, v___x_518_);
lean_ctor_set(v___x_519_, 1, v___x_518_);
lean_ctor_set(v___x_519_, 2, v___x_517_);
return v___x_519_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__4(void){
_start:
{
lean_object* v___x_520_; lean_object* v___x_521_; lean_object* v___x_522_; 
v___x_520_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_521_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_522_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_522_, 0, v___x_521_);
lean_ctor_set(v___x_522_, 1, v___x_520_);
lean_ctor_set(v___x_522_, 2, v___x_521_);
return v___x_522_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__5(void){
_start:
{
lean_object* v___x_523_; lean_object* v___x_524_; lean_object* v___x_525_; 
v___x_523_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_524_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_525_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_525_, 0, v___x_524_);
lean_ctor_set(v___x_525_, 1, v___x_523_);
lean_ctor_set(v___x_525_, 2, v___x_523_);
return v___x_525_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__6(void){
_start:
{
lean_object* v___x_526_; lean_object* v___x_527_; 
v___x_526_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_527_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_527_, 0, v___x_526_);
lean_ctor_set(v___x_527_, 1, v___x_526_);
lean_ctor_set(v___x_527_, 2, v___x_526_);
return v___x_527_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome(uint8_t v_x_528_){
_start:
{
switch(v_x_528_)
{
case 0:
{
lean_object* v___x_529_; 
v___x_529_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__0);
return v___x_529_;
}
case 1:
{
lean_object* v___x_530_; 
v___x_530_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__1);
return v___x_530_;
}
case 2:
{
lean_object* v___x_531_; 
v___x_531_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__2);
return v___x_531_;
}
case 3:
{
lean_object* v___x_532_; 
v___x_532_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__3);
return v___x_532_;
}
case 4:
{
lean_object* v___x_533_; 
v___x_533_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__4);
return v___x_533_;
}
case 5:
{
lean_object* v___x_534_; 
v___x_534_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__5);
return v___x_534_;
}
default: 
{
lean_object* v___x_535_; 
v___x_535_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___closed__6);
return v___x_535_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome___boxed(lean_object* v_x_536_){
_start:
{
uint8_t v_x_226__boxed_537_; lean_object* v_res_538_; 
v_x_226__boxed_537_ = lean_unbox(v_x_536_);
v_res_538_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_posSyndrome(v_x_226__boxed_537_);
return v_res_538_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome___closed__0(void){
_start:
{
lean_object* v___x_539_; lean_object* v___x_540_; 
v___x_539_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_540_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_540_, 0, v___x_539_);
lean_ctor_set(v___x_540_, 1, v___x_539_);
lean_ctor_set(v___x_540_, 2, v___x_539_);
return v___x_540_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome(void){
_start:
{
lean_object* v___x_541_; 
v___x_541_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome___closed__0);
return v___x_541_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0(void){
_start:
{
lean_object* v___x_542_; lean_object* v___x_543_; lean_object* v___x_544_; 
v___x_542_ = lean_box(0);
v___x_543_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_544_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_544_, 0, v___x_543_);
lean_ctor_set(v___x_544_, 1, v___x_542_);
return v___x_544_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1(void){
_start:
{
lean_object* v___x_545_; lean_object* v___x_546_; lean_object* v___x_547_; 
v___x_545_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0);
v___x_546_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_547_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_547_, 0, v___x_546_);
lean_ctor_set(v___x_547_, 1, v___x_545_);
return v___x_547_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2(void){
_start:
{
lean_object* v___x_548_; lean_object* v___x_549_; lean_object* v___x_550_; 
v___x_548_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1);
v___x_549_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_550_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_550_, 0, v___x_549_);
lean_ctor_set(v___x_550_, 1, v___x_548_);
return v___x_550_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3(void){
_start:
{
lean_object* v___x_551_; lean_object* v___x_552_; lean_object* v___x_553_; 
v___x_551_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2);
v___x_552_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_553_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_553_, 0, v___x_552_);
lean_ctor_set(v___x_553_, 1, v___x_551_);
return v___x_553_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4(void){
_start:
{
lean_object* v___x_554_; lean_object* v___x_555_; lean_object* v___x_556_; 
v___x_554_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3);
v___x_555_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_556_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_556_, 0, v___x_555_);
lean_ctor_set(v___x_556_, 1, v___x_554_);
return v___x_556_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__5(void){
_start:
{
lean_object* v___x_557_; lean_object* v___x_558_; lean_object* v___x_559_; 
v___x_557_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4);
v___x_558_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_559_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_559_, 0, v___x_558_);
lean_ctor_set(v___x_559_, 1, v___x_557_);
return v___x_559_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__6(void){
_start:
{
lean_object* v___x_560_; lean_object* v___x_561_; lean_object* v___x_562_; 
v___x_560_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__5);
v___x_561_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_562_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_562_, 0, v___x_561_);
lean_ctor_set(v___x_562_, 1, v___x_560_);
return v___x_562_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__7(void){
_start:
{
lean_object* v___x_563_; lean_object* v___x_564_; lean_object* v___x_565_; 
v___x_563_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__4);
v___x_564_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_565_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_565_, 0, v___x_564_);
lean_ctor_set(v___x_565_, 1, v___x_563_);
return v___x_565_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__8(void){
_start:
{
lean_object* v___x_566_; lean_object* v___x_567_; lean_object* v___x_568_; 
v___x_566_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__7);
v___x_567_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_568_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_568_, 0, v___x_567_);
lean_ctor_set(v___x_568_, 1, v___x_566_);
return v___x_568_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__9(void){
_start:
{
lean_object* v___x_569_; lean_object* v___x_570_; lean_object* v___x_571_; 
v___x_569_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__3);
v___x_570_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_571_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_571_, 0, v___x_570_);
lean_ctor_set(v___x_571_, 1, v___x_569_);
return v___x_571_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__10(void){
_start:
{
lean_object* v___x_572_; lean_object* v___x_573_; lean_object* v___x_574_; 
v___x_572_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__9);
v___x_573_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_574_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_574_, 0, v___x_573_);
lean_ctor_set(v___x_574_, 1, v___x_572_);
return v___x_574_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__11(void){
_start:
{
lean_object* v___x_575_; lean_object* v___x_576_; lean_object* v___x_577_; 
v___x_575_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__10);
v___x_576_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_577_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_577_, 0, v___x_576_);
lean_ctor_set(v___x_577_, 1, v___x_575_);
return v___x_577_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__12(void){
_start:
{
lean_object* v___x_578_; lean_object* v___x_579_; lean_object* v___x_580_; 
v___x_578_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__2);
v___x_579_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_580_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_580_, 0, v___x_579_);
lean_ctor_set(v___x_580_, 1, v___x_578_);
return v___x_580_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__13(void){
_start:
{
lean_object* v___x_581_; lean_object* v___x_582_; lean_object* v___x_583_; 
v___x_581_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__12, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__12_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__12);
v___x_582_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_583_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_583_, 0, v___x_582_);
lean_ctor_set(v___x_583_, 1, v___x_581_);
return v___x_583_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__14(void){
_start:
{
lean_object* v___x_584_; lean_object* v___x_585_; lean_object* v___x_586_; 
v___x_584_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__13, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__13_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__13);
v___x_585_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_586_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_586_, 0, v___x_585_);
lean_ctor_set(v___x_586_, 1, v___x_584_);
return v___x_586_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__15(void){
_start:
{
lean_object* v___x_587_; lean_object* v___x_588_; lean_object* v___x_589_; 
v___x_587_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__14, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__14_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__14);
v___x_588_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_589_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_589_, 0, v___x_588_);
lean_ctor_set(v___x_589_, 1, v___x_587_);
return v___x_589_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__16(void){
_start:
{
lean_object* v___x_590_; lean_object* v___x_591_; lean_object* v___x_592_; 
v___x_590_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__1);
v___x_591_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_592_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_592_, 0, v___x_591_);
lean_ctor_set(v___x_592_, 1, v___x_590_);
return v___x_592_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__17(void){
_start:
{
lean_object* v___x_593_; lean_object* v___x_594_; lean_object* v___x_595_; 
v___x_593_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__16, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__16_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__16);
v___x_594_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_595_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_595_, 0, v___x_594_);
lean_ctor_set(v___x_595_, 1, v___x_593_);
return v___x_595_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__18(void){
_start:
{
lean_object* v___x_596_; lean_object* v___x_597_; lean_object* v___x_598_; 
v___x_596_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__17);
v___x_597_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_598_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_598_, 0, v___x_597_);
lean_ctor_set(v___x_598_, 1, v___x_596_);
return v___x_598_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__19(void){
_start:
{
lean_object* v___x_599_; lean_object* v___x_600_; lean_object* v___x_601_; 
v___x_599_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__18, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__18_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__18);
v___x_600_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_601_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_601_, 0, v___x_600_);
lean_ctor_set(v___x_601_, 1, v___x_599_);
return v___x_601_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__20(void){
_start:
{
lean_object* v___x_602_; lean_object* v___x_603_; lean_object* v___x_604_; 
v___x_602_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__19, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__19_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__19);
v___x_603_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_604_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_604_, 0, v___x_603_);
lean_ctor_set(v___x_604_, 1, v___x_602_);
return v___x_604_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__21(void){
_start:
{
lean_object* v___x_605_; lean_object* v___x_606_; lean_object* v___x_607_; 
v___x_605_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__0);
v___x_606_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__0);
v___x_607_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_607_, 0, v___x_606_);
lean_ctor_set(v___x_607_, 1, v___x_605_);
return v___x_607_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__22(void){
_start:
{
lean_object* v___x_608_; lean_object* v___x_609_; lean_object* v___x_610_; 
v___x_608_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__21, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__21_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__21);
v___x_609_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_610_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_610_, 0, v___x_609_);
lean_ctor_set(v___x_610_, 1, v___x_608_);
return v___x_610_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__23(void){
_start:
{
lean_object* v___x_611_; lean_object* v___x_612_; lean_object* v___x_613_; 
v___x_611_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__22, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__22_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__22);
v___x_612_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_613_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_613_, 0, v___x_612_);
lean_ctor_set(v___x_613_, 1, v___x_611_);
return v___x_613_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__24(void){
_start:
{
lean_object* v___x_614_; lean_object* v___x_615_; lean_object* v___x_616_; 
v___x_614_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__23, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__23_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__23);
v___x_615_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_616_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_616_, 0, v___x_615_);
lean_ctor_set(v___x_616_, 1, v___x_614_);
return v___x_616_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__25(void){
_start:
{
lean_object* v___x_617_; lean_object* v___x_618_; lean_object* v___x_619_; 
v___x_617_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__24, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__24_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__24);
v___x_618_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_619_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_619_, 0, v___x_618_);
lean_ctor_set(v___x_619_, 1, v___x_617_);
return v___x_619_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__26(void){
_start:
{
lean_object* v___x_620_; lean_object* v___x_621_; lean_object* v___x_622_; 
v___x_620_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__25, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__25_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__25);
v___x_621_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_622_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_622_, 0, v___x_621_);
lean_ctor_set(v___x_622_, 1, v___x_620_);
return v___x_622_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__27(void){
_start:
{
lean_object* v___x_623_; lean_object* v___x_624_; lean_object* v___x_625_; 
v___x_623_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__3);
v___x_624_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_625_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_625_, 0, v___x_624_);
lean_ctor_set(v___x_625_, 1, v___x_623_);
return v___x_625_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__28(void){
_start:
{
lean_object* v___x_626_; lean_object* v___x_627_; lean_object* v___x_628_; 
v___x_626_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__27, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__27_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__27);
v___x_627_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_628_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_628_, 0, v___x_627_);
lean_ctor_set(v___x_628_, 1, v___x_626_);
return v___x_628_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__29(void){
_start:
{
lean_object* v___x_629_; lean_object* v___x_630_; lean_object* v___x_631_; 
v___x_629_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__28, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__28_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__28);
v___x_630_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_631_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_631_, 0, v___x_630_);
lean_ctor_set(v___x_631_, 1, v___x_629_);
return v___x_631_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__30(void){
_start:
{
lean_object* v___x_632_; lean_object* v___x_633_; lean_object* v___x_634_; 
v___x_632_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__29, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__29_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__29);
v___x_633_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_634_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_634_, 0, v___x_633_);
lean_ctor_set(v___x_634_, 1, v___x_632_);
return v___x_634_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__31(void){
_start:
{
lean_object* v___x_635_; lean_object* v___x_636_; lean_object* v___x_637_; 
v___x_635_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__30, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__30_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__30);
v___x_636_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1___closed__1);
v___x_637_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_637_, 0, v___x_636_);
lean_ctor_set(v___x_637_, 1, v___x_635_);
return v___x_637_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt(uint8_t v_x_638_){
_start:
{
switch(v_x_638_)
{
case 0:
{
lean_object* v___x_639_; 
v___x_639_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__6, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__6_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__6);
return v___x_639_;
}
case 1:
{
lean_object* v___x_640_; 
v___x_640_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__8);
return v___x_640_;
}
case 2:
{
lean_object* v___x_641_; 
v___x_641_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__11, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__11_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__11);
return v___x_641_;
}
case 3:
{
lean_object* v___x_642_; 
v___x_642_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__15, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__15_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__15);
return v___x_642_;
}
case 4:
{
lean_object* v___x_643_; 
v___x_643_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__20, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__20_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__20);
return v___x_643_;
}
case 5:
{
lean_object* v___x_644_; 
v___x_644_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__26, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__26_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__26);
return v___x_644_;
}
default: 
{
lean_object* v___x_645_; 
v___x_645_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__31, &lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__31_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___closed__31);
return v___x_645_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt___boxed(lean_object* v_x_646_){
_start:
{
uint8_t v_x_520__boxed_647_; lean_object* v_res_648_; 
v_x_520__boxed_647_ = lean_unbox(v_x_646_);
v_res_648_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_basisAt(v_x_520__boxed_647_);
return v_res_648_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H038_checkSyndrome(lean_object* v_err_649_){
_start:
{
lean_object* v___x_650_; lean_object* v___x_651_; lean_object* v___x_652_; lean_object* v___x_653_; lean_object* v___x_654_; lean_object* v___x_655_; lean_object* v___x_656_; 
v___x_650_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1;
lean_inc_n(v_err_649_, 2);
v___x_651_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod(v___x_650_, v_err_649_);
v___x_652_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2;
v___x_653_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod(v___x_652_, v_err_649_);
v___x_654_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3;
v___x_655_ = lp_FiniteQuantum_FableHilbertWalk20260819_H038_inner__prod(v___x_654_, v_err_649_);
v___x_656_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v___x_656_, 0, v___x_651_);
lean_ctor_set(v___x_656_, 1, v___x_653_);
lean_ctor_set(v___x_656_, 2, v___x_655_);
return v___x_656_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H038SteaneFanoCodeTransversalGates(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H038_h1);
lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H038_h2);
lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H038_h3);
lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H038_logicalAll);
lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H038_zeroSyndrome);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
