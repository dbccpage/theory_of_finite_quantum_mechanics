// Lean compiler output
// Module: H040DiscreteSuperdenseCoding
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* l_Int_mul___boxed(lean_object*, lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__4;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus;
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H040_inner__prod_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H040_inner__prod_spec__0___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_mul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__0_value;
static const lean_array_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__1_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "b1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "b0"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__16_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqBellState(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqBellState___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 53, .m_capacity = 53, .m_length = 52, .m_data = "FableHilbertWalk20260819.H040.BellState.statePhiPlus"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 53, .m_capacity = 53, .m_length = 52, .m_data = "FableHilbertWalk20260819.H040.BellState.statePsiPlus"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 54, .m_capacity = 54, .m_length = 53, .m_data = "FableHilbertWalk20260819.H040.BellState.statePhiMinus"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 54, .m_capacity = 54, .m_length = 53, .m_data = "FableHilbertWalk20260819.H040.BellState.statePsiMinus"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__7_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___boxed(lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_unsigned_to_nat(0u);
v___x_4_ = lean_nat_to_int(v___x_3_);
return v___x_4_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__2(void){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; 
v___x_5_ = lean_box(0);
v___x_6_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_7_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_7_, 0, v___x_6_);
lean_ctor_set(v___x_7_, 1, v___x_5_);
return v___x_7_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__3(void){
_start:
{
lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_8_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__2);
v___x_9_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_10_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_10_, 0, v___x_9_);
lean_ctor_set(v___x_10_, 1, v___x_8_);
return v___x_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__4(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_11_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__3);
v___x_12_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_13_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_13_, 0, v___x_12_);
lean_ctor_set(v___x_13_, 1, v___x_11_);
return v___x_13_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__5(void){
_start:
{
lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; 
v___x_14_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__4);
v___x_15_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_16_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_16_, 0, v___x_15_);
lean_ctor_set(v___x_16_, 1, v___x_14_);
return v___x_16_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus(void){
_start:
{
lean_object* v___x_17_; 
v___x_17_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__5, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__5_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__5);
return v___x_17_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0(void){
_start:
{
lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; 
v___x_18_ = lean_box(0);
v___x_19_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_20_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_20_, 0, v___x_19_);
lean_ctor_set(v___x_20_, 1, v___x_18_);
return v___x_20_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__1(void){
_start:
{
lean_object* v___x_21_; lean_object* v___x_22_; lean_object* v___x_23_; 
v___x_21_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0);
v___x_22_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_23_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_23_, 0, v___x_22_);
lean_ctor_set(v___x_23_, 1, v___x_21_);
return v___x_23_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__2(void){
_start:
{
lean_object* v___x_24_; lean_object* v___x_25_; lean_object* v___x_26_; 
v___x_24_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__1);
v___x_25_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_26_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_26_, 0, v___x_25_);
lean_ctor_set(v___x_26_, 1, v___x_24_);
return v___x_26_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__3(void){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; 
v___x_27_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__2);
v___x_28_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_29_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_29_, 0, v___x_28_);
lean_ctor_set(v___x_29_, 1, v___x_27_);
return v___x_29_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus(void){
_start:
{
lean_object* v___x_30_; 
v___x_30_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__3);
return v___x_30_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0(void){
_start:
{
lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_31_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_32_ = lean_int_neg(v___x_31_);
return v___x_32_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__1(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; 
v___x_33_ = lean_box(0);
v___x_34_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0);
v___x_35_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_35_, 0, v___x_34_);
lean_ctor_set(v___x_35_, 1, v___x_33_);
return v___x_35_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__2(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; lean_object* v___x_38_; 
v___x_36_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__1);
v___x_37_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_38_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_38_, 0, v___x_37_);
lean_ctor_set(v___x_38_, 1, v___x_36_);
return v___x_38_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__3(void){
_start:
{
lean_object* v___x_39_; lean_object* v___x_40_; lean_object* v___x_41_; 
v___x_39_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__2);
v___x_40_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_41_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_41_, 0, v___x_40_);
lean_ctor_set(v___x_41_, 1, v___x_39_);
return v___x_41_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__4(void){
_start:
{
lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_44_; 
v___x_42_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__3);
v___x_43_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_44_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_44_, 0, v___x_43_);
lean_ctor_set(v___x_44_, 1, v___x_42_);
return v___x_44_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus(void){
_start:
{
lean_object* v___x_45_; 
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__4);
return v___x_45_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__0(void){
_start:
{
lean_object* v___x_46_; lean_object* v___x_47_; lean_object* v___x_48_; 
v___x_46_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus___closed__0);
v___x_47_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus___closed__0);
v___x_48_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_48_, 0, v___x_47_);
lean_ctor_set(v___x_48_, 1, v___x_46_);
return v___x_48_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__1(void){
_start:
{
lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__0);
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_51_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_51_, 0, v___x_50_);
lean_ctor_set(v___x_51_, 1, v___x_49_);
return v___x_51_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__2(void){
_start:
{
lean_object* v___x_52_; lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_52_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__1);
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_54_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_54_, 0, v___x_53_);
lean_ctor_set(v___x_54_, 1, v___x_52_);
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus(void){
_start:
{
lean_object* v___x_55_; 
v___x_55_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus___closed__2);
return v___x_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H040_inner__prod_spec__0(lean_object* v_x_56_, lean_object* v_x_57_){
_start:
{
if (lean_obj_tag(v_x_57_) == 0)
{
return v_x_56_;
}
else
{
lean_object* v_head_58_; lean_object* v_tail_59_; lean_object* v___x_60_; 
v_head_58_ = lean_ctor_get(v_x_57_, 0);
v_tail_59_ = lean_ctor_get(v_x_57_, 1);
v___x_60_ = lean_int_add(v_x_56_, v_head_58_);
lean_dec(v_x_56_);
v_x_56_ = v___x_60_;
v_x_57_ = v_tail_59_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H040_inner__prod_spec__0___boxed(lean_object* v_x_62_, lean_object* v_x_63_){
_start:
{
lean_object* v_res_64_; 
v_res_64_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H040_inner__prod_spec__0(v_x_62_, v_x_63_);
lean_dec(v_x_63_);
return v_res_64_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod(lean_object* v_l1_68_, lean_object* v_l2_69_){
_start:
{
lean_object* v___f_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; lean_object* v___x_74_; 
v___f_70_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__0));
v___x_71_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_72_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_inner__prod___closed__1));
v___x_73_ = l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(v___f_70_, v_l1_68_, v_l2_69_, v___x_72_);
v___x_74_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H040_inner__prod_spec__0(v___x_71_, v___x_73_);
lean_dec(v___x_73_);
return v___x_74_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2_decEq(lean_object* v_x_75_, lean_object* v_x_76_){
_start:
{
lean_object* v_b1_77_; lean_object* v_b0_78_; lean_object* v_b1_79_; lean_object* v_b0_80_; uint8_t v___x_81_; 
v_b1_77_ = lean_ctor_get(v_x_75_, 0);
v_b0_78_ = lean_ctor_get(v_x_75_, 1);
v_b1_79_ = lean_ctor_get(v_x_76_, 0);
v_b0_80_ = lean_ctor_get(v_x_76_, 1);
v___x_81_ = lean_int_dec_eq(v_b1_77_, v_b1_79_);
if (v___x_81_ == 0)
{
return v___x_81_;
}
else
{
uint8_t v___x_82_; 
v___x_82_ = lean_int_dec_eq(v_b0_78_, v_b0_80_);
return v___x_82_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2_decEq___boxed(lean_object* v_x_83_, lean_object* v_x_84_){
_start:
{
uint8_t v_res_85_; lean_object* v_r_86_; 
v_res_85_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2_decEq(v_x_83_, v_x_84_);
lean_dec_ref(v_x_84_);
lean_dec_ref(v_x_83_);
v_r_86_ = lean_box(v_res_85_);
return v_r_86_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2(lean_object* v_x_87_, lean_object* v_x_88_){
_start:
{
uint8_t v___x_89_; 
v___x_89_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2_decEq(v_x_87_, v_x_88_);
return v___x_89_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2___boxed(lean_object* v_x_90_, lean_object* v_x_91_){
_start:
{
uint8_t v_res_92_; lean_object* v_r_93_; 
v_res_92_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqMessage2(v_x_90_, v_x_91_);
lean_dec_ref(v_x_91_);
lean_dec_ref(v_x_90_);
v_r_93_ = lean_box(v_res_92_);
return v_r_93_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_107_; lean_object* v___x_108_; 
v___x_107_ = lean_unsigned_to_nat(6u);
v___x_108_ = lean_nat_to_int(v___x_107_);
return v___x_108_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_110_; lean_object* v___x_111_; 
v___x_110_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__0));
v___x_111_ = lean_string_length(v___x_110_);
return v___x_111_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_112_; lean_object* v___x_113_; 
v___x_112_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__9);
v___x_113_ = lean_nat_to_int(v___x_112_);
return v___x_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg(lean_object* v_x_124_){
_start:
{
lean_object* v_b1_125_; lean_object* v_b0_126_; lean_object* v___x_128_; uint8_t v_isShared_129_; uint8_t v_isSharedCheck_178_; 
v_b1_125_ = lean_ctor_get(v_x_124_, 0);
v_b0_126_ = lean_ctor_get(v_x_124_, 1);
v_isSharedCheck_178_ = !lean_is_exclusive(v_x_124_);
if (v_isSharedCheck_178_ == 0)
{
v___x_128_ = v_x_124_;
v_isShared_129_ = v_isSharedCheck_178_;
goto v_resetjp_127_;
}
else
{
lean_inc(v_b0_126_);
lean_inc(v_b1_125_);
lean_dec(v_x_124_);
v___x_128_ = lean_box(0);
v_isShared_129_ = v_isSharedCheck_178_;
goto v_resetjp_127_;
}
v_resetjp_127_:
{
lean_object* v___x_130_; lean_object* v___x_131_; lean_object* v___x_132_; uint8_t v___y_134_; lean_object* v___y_135_; lean_object* v___y_136_; lean_object* v___y_150_; lean_object* v___x_170_; lean_object* v___x_171_; uint8_t v___x_172_; 
v___x_130_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__5));
v___x_131_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__6));
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__7);
v___x_170_ = lean_unsigned_to_nat(0u);
v___x_171_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_172_ = lean_int_dec_lt(v_b1_125_, v___x_171_);
if (v___x_172_ == 0)
{
lean_object* v___x_173_; lean_object* v___x_174_; 
v___x_173_ = l_Int_repr(v_b1_125_);
lean_dec(v_b1_125_);
v___x_174_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_174_, 0, v___x_173_);
v___y_150_ = v___x_174_;
goto v___jp_149_;
}
else
{
lean_object* v___x_175_; lean_object* v___x_176_; lean_object* v___x_177_; 
v___x_175_ = l_Int_repr(v_b1_125_);
lean_dec(v_b1_125_);
v___x_176_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_176_, 0, v___x_175_);
v___x_177_ = l_Repr_addAppParen(v___x_176_, v___x_170_);
v___y_150_ = v___x_177_;
goto v___jp_149_;
}
v___jp_133_:
{
lean_object* v___x_138_; 
if (v_isShared_129_ == 0)
{
lean_ctor_set_tag(v___x_128_, 4);
lean_ctor_set(v___x_128_, 1, v___y_136_);
lean_ctor_set(v___x_128_, 0, v___x_132_);
v___x_138_ = v___x_128_;
goto v_reusejp_137_;
}
else
{
lean_object* v_reuseFailAlloc_148_; 
v_reuseFailAlloc_148_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_148_, 0, v___x_132_);
lean_ctor_set(v_reuseFailAlloc_148_, 1, v___y_136_);
v___x_138_ = v_reuseFailAlloc_148_;
goto v_reusejp_137_;
}
v_reusejp_137_:
{
lean_object* v___x_139_; lean_object* v___x_140_; lean_object* v___x_141_; lean_object* v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; lean_object* v___x_145_; lean_object* v___x_146_; lean_object* v___x_147_; 
v___x_139_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_139_, 0, v___x_138_);
lean_ctor_set_uint8(v___x_139_, sizeof(void*)*1, v___y_134_);
v___x_140_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_140_, 0, v___y_135_);
lean_ctor_set(v___x_140_, 1, v___x_139_);
v___x_141_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__10);
v___x_142_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__11));
v___x_143_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_143_, 0, v___x_142_);
lean_ctor_set(v___x_143_, 1, v___x_140_);
v___x_144_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__12));
v___x_145_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_145_, 0, v___x_143_);
lean_ctor_set(v___x_145_, 1, v___x_144_);
v___x_146_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_146_, 0, v___x_141_);
lean_ctor_set(v___x_146_, 1, v___x_145_);
v___x_147_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_147_, 0, v___x_146_);
lean_ctor_set_uint8(v___x_147_, sizeof(void*)*1, v___y_134_);
return v___x_147_;
}
}
v___jp_149_:
{
lean_object* v___x_151_; uint8_t v___x_152_; lean_object* v___x_153_; lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; lean_object* v___x_157_; lean_object* v___x_158_; lean_object* v___x_159_; lean_object* v___x_160_; lean_object* v___x_161_; lean_object* v___x_162_; lean_object* v___x_163_; uint8_t v___x_164_; 
v___x_151_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_151_, 0, v___x_132_);
lean_ctor_set(v___x_151_, 1, v___y_150_);
v___x_152_ = 0;
v___x_153_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_153_, 0, v___x_151_);
lean_ctor_set_uint8(v___x_153_, sizeof(void*)*1, v___x_152_);
v___x_154_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_154_, 0, v___x_131_);
lean_ctor_set(v___x_154_, 1, v___x_153_);
v___x_155_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__14));
v___x_156_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_156_, 0, v___x_154_);
lean_ctor_set(v___x_156_, 1, v___x_155_);
v___x_157_ = lean_box(1);
v___x_158_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_158_, 0, v___x_156_);
lean_ctor_set(v___x_158_, 1, v___x_157_);
v___x_159_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg___closed__16));
v___x_160_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_160_, 0, v___x_158_);
lean_ctor_set(v___x_160_, 1, v___x_159_);
v___x_161_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_161_, 0, v___x_160_);
lean_ctor_set(v___x_161_, 1, v___x_130_);
v___x_162_ = lean_unsigned_to_nat(0u);
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_164_ = lean_int_dec_lt(v_b0_126_, v___x_163_);
if (v___x_164_ == 0)
{
lean_object* v___x_165_; lean_object* v___x_166_; 
v___x_165_ = l_Int_repr(v_b0_126_);
lean_dec(v_b0_126_);
v___x_166_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_166_, 0, v___x_165_);
v___y_134_ = v___x_152_;
v___y_135_ = v___x_161_;
v___y_136_ = v___x_166_;
goto v___jp_133_;
}
else
{
lean_object* v___x_167_; lean_object* v___x_168_; lean_object* v___x_169_; 
v___x_167_ = l_Int_repr(v_b0_126_);
lean_dec(v_b0_126_);
v___x_168_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_168_, 0, v___x_167_);
v___x_169_ = l_Repr_addAppParen(v___x_168_, v___x_162_);
v___y_134_ = v___x_152_;
v___y_135_ = v___x_161_;
v___y_136_ = v___x_169_;
goto v___jp_133_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr(lean_object* v_x_179_, lean_object* v_prec_180_){
_start:
{
lean_object* v___x_181_; 
v___x_181_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___redArg(v_x_179_);
return v___x_181_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr___boxed(lean_object* v_x_182_, lean_object* v_prec_183_){
_start:
{
lean_object* v_res_184_; 
v_res_184_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprMessage2_repr(v_x_182_, v_prec_183_);
lean_dec(v_prec_183_);
return v_res_184_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx(uint8_t v_x_187_){
_start:
{
switch(v_x_187_)
{
case 0:
{
lean_object* v___x_188_; 
v___x_188_ = lean_unsigned_to_nat(0u);
return v___x_188_;
}
case 1:
{
lean_object* v___x_189_; 
v___x_189_ = lean_unsigned_to_nat(1u);
return v___x_189_;
}
case 2:
{
lean_object* v___x_190_; 
v___x_190_ = lean_unsigned_to_nat(2u);
return v___x_190_;
}
default: 
{
lean_object* v___x_191_; 
v___x_191_ = lean_unsigned_to_nat(3u);
return v___x_191_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx___boxed(lean_object* v_x_192_){
_start:
{
uint8_t v_x_boxed_193_; lean_object* v_res_194_; 
v_x_boxed_193_ = lean_unbox(v_x_192_);
v_res_194_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx(v_x_boxed_193_);
return v_res_194_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_toCtorIdx(uint8_t v_x_195_){
_start:
{
lean_object* v___x_196_; 
v___x_196_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx(v_x_195_);
return v___x_196_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_toCtorIdx___boxed(lean_object* v_x_197_){
_start:
{
uint8_t v_x_4__boxed_198_; lean_object* v_res_199_; 
v_x_4__boxed_198_ = lean_unbox(v_x_197_);
v_res_199_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_toCtorIdx(v_x_4__boxed_198_);
return v_res_199_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___redArg(lean_object* v_k_200_){
_start:
{
lean_inc(v_k_200_);
return v_k_200_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___redArg___boxed(lean_object* v_k_201_){
_start:
{
lean_object* v_res_202_; 
v_res_202_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___redArg(v_k_201_);
lean_dec(v_k_201_);
return v_res_202_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim(lean_object* v_motive_203_, lean_object* v_ctorIdx_204_, uint8_t v_t_205_, lean_object* v_h_206_, lean_object* v_k_207_){
_start:
{
lean_inc(v_k_207_);
return v_k_207_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim___boxed(lean_object* v_motive_208_, lean_object* v_ctorIdx_209_, lean_object* v_t_210_, lean_object* v_h_211_, lean_object* v_k_212_){
_start:
{
uint8_t v_t_boxed_213_; lean_object* v_res_214_; 
v_t_boxed_213_ = lean_unbox(v_t_210_);
v_res_214_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorElim(v_motive_208_, v_ctorIdx_209_, v_t_boxed_213_, v_h_211_, v_k_212_);
lean_dec(v_k_212_);
lean_dec(v_ctorIdx_209_);
return v_res_214_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___redArg(lean_object* v_statePhiPlus_215_){
_start:
{
lean_inc(v_statePhiPlus_215_);
return v_statePhiPlus_215_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___redArg___boxed(lean_object* v_statePhiPlus_216_){
_start:
{
lean_object* v_res_217_; 
v_res_217_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___redArg(v_statePhiPlus_216_);
lean_dec(v_statePhiPlus_216_);
return v_res_217_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim(lean_object* v_motive_218_, uint8_t v_t_219_, lean_object* v_h_220_, lean_object* v_statePhiPlus_221_){
_start:
{
lean_inc(v_statePhiPlus_221_);
return v_statePhiPlus_221_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim___boxed(lean_object* v_motive_222_, lean_object* v_t_223_, lean_object* v_h_224_, lean_object* v_statePhiPlus_225_){
_start:
{
uint8_t v_t_boxed_226_; lean_object* v_res_227_; 
v_t_boxed_226_ = lean_unbox(v_t_223_);
v_res_227_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiPlus_elim(v_motive_222_, v_t_boxed_226_, v_h_224_, v_statePhiPlus_225_);
lean_dec(v_statePhiPlus_225_);
return v_res_227_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___redArg(lean_object* v_statePsiPlus_228_){
_start:
{
lean_inc(v_statePsiPlus_228_);
return v_statePsiPlus_228_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___redArg___boxed(lean_object* v_statePsiPlus_229_){
_start:
{
lean_object* v_res_230_; 
v_res_230_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___redArg(v_statePsiPlus_229_);
lean_dec(v_statePsiPlus_229_);
return v_res_230_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim(lean_object* v_motive_231_, uint8_t v_t_232_, lean_object* v_h_233_, lean_object* v_statePsiPlus_234_){
_start:
{
lean_inc(v_statePsiPlus_234_);
return v_statePsiPlus_234_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim___boxed(lean_object* v_motive_235_, lean_object* v_t_236_, lean_object* v_h_237_, lean_object* v_statePsiPlus_238_){
_start:
{
uint8_t v_t_boxed_239_; lean_object* v_res_240_; 
v_t_boxed_239_ = lean_unbox(v_t_236_);
v_res_240_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiPlus_elim(v_motive_235_, v_t_boxed_239_, v_h_237_, v_statePsiPlus_238_);
lean_dec(v_statePsiPlus_238_);
return v_res_240_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___redArg(lean_object* v_statePhiMinus_241_){
_start:
{
lean_inc(v_statePhiMinus_241_);
return v_statePhiMinus_241_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___redArg___boxed(lean_object* v_statePhiMinus_242_){
_start:
{
lean_object* v_res_243_; 
v_res_243_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___redArg(v_statePhiMinus_242_);
lean_dec(v_statePhiMinus_242_);
return v_res_243_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim(lean_object* v_motive_244_, uint8_t v_t_245_, lean_object* v_h_246_, lean_object* v_statePhiMinus_247_){
_start:
{
lean_inc(v_statePhiMinus_247_);
return v_statePhiMinus_247_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim___boxed(lean_object* v_motive_248_, lean_object* v_t_249_, lean_object* v_h_250_, lean_object* v_statePhiMinus_251_){
_start:
{
uint8_t v_t_boxed_252_; lean_object* v_res_253_; 
v_t_boxed_252_ = lean_unbox(v_t_249_);
v_res_253_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePhiMinus_elim(v_motive_248_, v_t_boxed_252_, v_h_250_, v_statePhiMinus_251_);
lean_dec(v_statePhiMinus_251_);
return v_res_253_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___redArg(lean_object* v_statePsiMinus_254_){
_start:
{
lean_inc(v_statePsiMinus_254_);
return v_statePsiMinus_254_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___redArg___boxed(lean_object* v_statePsiMinus_255_){
_start:
{
lean_object* v_res_256_; 
v_res_256_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___redArg(v_statePsiMinus_255_);
lean_dec(v_statePsiMinus_255_);
return v_res_256_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim(lean_object* v_motive_257_, uint8_t v_t_258_, lean_object* v_h_259_, lean_object* v_statePsiMinus_260_){
_start:
{
lean_inc(v_statePsiMinus_260_);
return v_statePsiMinus_260_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim___boxed(lean_object* v_motive_261_, lean_object* v_t_262_, lean_object* v_h_263_, lean_object* v_statePsiMinus_264_){
_start:
{
uint8_t v_t_boxed_265_; lean_object* v_res_266_; 
v_t_boxed_265_ = lean_unbox(v_t_262_);
v_res_266_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_statePsiMinus_elim(v_motive_261_, v_t_boxed_265_, v_h_263_, v_statePsiMinus_264_);
lean_dec(v_statePsiMinus_264_);
return v_res_266_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ofNat(lean_object* v_n_267_){
_start:
{
lean_object* v___x_268_; uint8_t v___x_269_; 
v___x_268_ = lean_unsigned_to_nat(1u);
v___x_269_ = lean_nat_dec_le(v_n_267_, v___x_268_);
if (v___x_269_ == 0)
{
lean_object* v___x_270_; uint8_t v___x_271_; 
v___x_270_ = lean_unsigned_to_nat(2u);
v___x_271_ = lean_nat_dec_le(v_n_267_, v___x_270_);
if (v___x_271_ == 0)
{
uint8_t v___x_272_; 
v___x_272_ = 3;
return v___x_272_;
}
else
{
uint8_t v___x_273_; 
v___x_273_ = 2;
return v___x_273_;
}
}
else
{
lean_object* v___x_274_; uint8_t v___x_275_; 
v___x_274_ = lean_unsigned_to_nat(0u);
v___x_275_ = lean_nat_dec_le(v_n_267_, v___x_274_);
if (v___x_275_ == 0)
{
uint8_t v___x_276_; 
v___x_276_ = 1;
return v___x_276_;
}
else
{
uint8_t v___x_277_; 
v___x_277_ = 0;
return v___x_277_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ofNat___boxed(lean_object* v_n_278_){
_start:
{
uint8_t v_res_279_; lean_object* v_r_280_; 
v_res_279_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ofNat(v_n_278_);
lean_dec(v_n_278_);
v_r_280_ = lean_box(v_res_279_);
return v_r_280_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqBellState(uint8_t v_x_281_, uint8_t v_y_282_){
_start:
{
lean_object* v___x_283_; lean_object* v___x_284_; uint8_t v___x_285_; 
v___x_283_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx(v_x_281_);
v___x_284_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_BellState_ctorIdx(v_y_282_);
v___x_285_ = lean_nat_dec_eq(v___x_283_, v___x_284_);
lean_dec(v___x_284_);
lean_dec(v___x_283_);
return v___x_285_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqBellState___boxed(lean_object* v_x_286_, lean_object* v_y_287_){
_start:
{
uint8_t v_x_13__boxed_288_; uint8_t v_y_14__boxed_289_; uint8_t v_res_290_; lean_object* v_r_291_; 
v_x_13__boxed_288_ = lean_unbox(v_x_286_);
v_y_14__boxed_289_ = lean_unbox(v_y_287_);
v_res_290_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instDecidableEqBellState(v_x_13__boxed_288_, v_y_14__boxed_289_);
v_r_291_ = lean_box(v_res_290_);
return v_r_291_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8(void){
_start:
{
lean_object* v___x_304_; lean_object* v___x_305_; 
v___x_304_ = lean_unsigned_to_nat(2u);
v___x_305_ = lean_nat_to_int(v___x_304_);
return v___x_305_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr(uint8_t v_x_306_, lean_object* v_prec_307_){
_start:
{
lean_object* v___y_309_; lean_object* v___y_316_; lean_object* v___y_323_; lean_object* v___y_330_; 
switch(v_x_306_)
{
case 0:
{
lean_object* v___x_336_; uint8_t v___x_337_; 
v___x_336_ = lean_unsigned_to_nat(1024u);
v___x_337_ = lean_nat_dec_le(v___x_336_, v_prec_307_);
if (v___x_337_ == 0)
{
lean_object* v___x_338_; 
v___x_338_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8);
v___y_309_ = v___x_338_;
goto v___jp_308_;
}
else
{
lean_object* v___x_339_; 
v___x_339_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___y_309_ = v___x_339_;
goto v___jp_308_;
}
}
case 1:
{
lean_object* v___x_340_; uint8_t v___x_341_; 
v___x_340_ = lean_unsigned_to_nat(1024u);
v___x_341_ = lean_nat_dec_le(v___x_340_, v_prec_307_);
if (v___x_341_ == 0)
{
lean_object* v___x_342_; 
v___x_342_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8);
v___y_316_ = v___x_342_;
goto v___jp_315_;
}
else
{
lean_object* v___x_343_; 
v___x_343_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___y_316_ = v___x_343_;
goto v___jp_315_;
}
}
case 2:
{
lean_object* v___x_344_; uint8_t v___x_345_; 
v___x_344_ = lean_unsigned_to_nat(1024u);
v___x_345_ = lean_nat_dec_le(v___x_344_, v_prec_307_);
if (v___x_345_ == 0)
{
lean_object* v___x_346_; 
v___x_346_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8);
v___y_323_ = v___x_346_;
goto v___jp_322_;
}
else
{
lean_object* v___x_347_; 
v___x_347_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___y_323_ = v___x_347_;
goto v___jp_322_;
}
}
default: 
{
lean_object* v___x_348_; uint8_t v___x_349_; 
v___x_348_ = lean_unsigned_to_nat(1024u);
v___x_349_ = lean_nat_dec_le(v___x_348_, v_prec_307_);
if (v___x_349_ == 0)
{
lean_object* v___x_350_; 
v___x_350_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__8);
v___y_330_ = v___x_350_;
goto v___jp_329_;
}
else
{
lean_object* v___x_351_; 
v___x_351_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___y_330_ = v___x_351_;
goto v___jp_329_;
}
}
}
v___jp_308_:
{
lean_object* v___x_310_; lean_object* v___x_311_; uint8_t v___x_312_; lean_object* v___x_313_; lean_object* v___x_314_; 
v___x_310_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__1));
lean_inc(v___y_309_);
v___x_311_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_311_, 0, v___y_309_);
lean_ctor_set(v___x_311_, 1, v___x_310_);
v___x_312_ = 0;
v___x_313_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_313_, 0, v___x_311_);
lean_ctor_set_uint8(v___x_313_, sizeof(void*)*1, v___x_312_);
v___x_314_ = l_Repr_addAppParen(v___x_313_, v_prec_307_);
return v___x_314_;
}
v___jp_315_:
{
lean_object* v___x_317_; lean_object* v___x_318_; uint8_t v___x_319_; lean_object* v___x_320_; lean_object* v___x_321_; 
v___x_317_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__3));
lean_inc(v___y_316_);
v___x_318_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_318_, 0, v___y_316_);
lean_ctor_set(v___x_318_, 1, v___x_317_);
v___x_319_ = 0;
v___x_320_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_320_, 0, v___x_318_);
lean_ctor_set_uint8(v___x_320_, sizeof(void*)*1, v___x_319_);
v___x_321_ = l_Repr_addAppParen(v___x_320_, v_prec_307_);
return v___x_321_;
}
v___jp_322_:
{
lean_object* v___x_324_; lean_object* v___x_325_; uint8_t v___x_326_; lean_object* v___x_327_; lean_object* v___x_328_; 
v___x_324_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__5));
lean_inc(v___y_323_);
v___x_325_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_325_, 0, v___y_323_);
lean_ctor_set(v___x_325_, 1, v___x_324_);
v___x_326_ = 0;
v___x_327_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_327_, 0, v___x_325_);
lean_ctor_set_uint8(v___x_327_, sizeof(void*)*1, v___x_326_);
v___x_328_ = l_Repr_addAppParen(v___x_327_, v_prec_307_);
return v___x_328_;
}
v___jp_329_:
{
lean_object* v___x_331_; lean_object* v___x_332_; uint8_t v___x_333_; lean_object* v___x_334_; lean_object* v___x_335_; 
v___x_331_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___closed__7));
lean_inc(v___y_330_);
v___x_332_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_332_, 0, v___y_330_);
lean_ctor_set(v___x_332_, 1, v___x_331_);
v___x_333_ = 0;
v___x_334_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_334_, 0, v___x_332_);
lean_ctor_set_uint8(v___x_334_, sizeof(void*)*1, v___x_333_);
v___x_335_ = l_Repr_addAppParen(v___x_334_, v_prec_307_);
return v___x_335_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr___boxed(lean_object* v_x_352_, lean_object* v_prec_353_){
_start:
{
uint8_t v_x_231__boxed_354_; lean_object* v_res_355_; 
v_x_231__boxed_354_ = lean_unbox(v_x_352_);
v_res_355_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_instReprBellState_repr(v_x_231__boxed_354_, v_prec_353_);
lean_dec(v_prec_353_);
return v_res_355_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__0(void){
_start:
{
lean_object* v___x_358_; lean_object* v___x_359_; 
v___x_358_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_359_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_359_, 0, v___x_358_);
lean_ctor_set(v___x_359_, 1, v___x_358_);
return v___x_359_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__1(void){
_start:
{
lean_object* v___x_360_; lean_object* v___x_361_; lean_object* v___x_362_; 
v___x_360_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_361_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_362_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_362_, 0, v___x_361_);
lean_ctor_set(v___x_362_, 1, v___x_360_);
return v___x_362_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__2(void){
_start:
{
lean_object* v___x_363_; lean_object* v___x_364_; lean_object* v___x_365_; 
v___x_363_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__1);
v___x_364_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_365_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_365_, 0, v___x_364_);
lean_ctor_set(v___x_365_, 1, v___x_363_);
return v___x_365_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__3(void){
_start:
{
lean_object* v___x_366_; lean_object* v___x_367_; 
v___x_366_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus___closed__0);
v___x_367_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_367_, 0, v___x_366_);
lean_ctor_set(v___x_367_, 1, v___x_366_);
return v___x_367_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell(uint8_t v_x_368_){
_start:
{
switch(v_x_368_)
{
case 0:
{
lean_object* v___x_369_; 
v___x_369_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__0);
return v___x_369_;
}
case 1:
{
lean_object* v___x_370_; 
v___x_370_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__1);
return v___x_370_;
}
case 2:
{
lean_object* v___x_371_; 
v___x_371_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__2);
return v___x_371_;
}
default: 
{
lean_object* v___x_372_; 
v___x_372_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___closed__3);
return v___x_372_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell___boxed(lean_object* v_x_373_){
_start:
{
uint8_t v_x_110__boxed_374_; lean_object* v_res_375_; 
v_x_110__boxed_374_ = lean_unbox(v_x_373_);
v_res_375_ = lp_FiniteQuantum_FableHilbertWalk20260819_H040_decodeBell(v_x_110__boxed_374_);
return v_res_375_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H040DiscreteSuperdenseCoding(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiPlus);
lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiPlus);
lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H040_phiMinus);
lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H040_psiMinus);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
