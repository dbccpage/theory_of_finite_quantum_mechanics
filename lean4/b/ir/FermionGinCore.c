// Lean compiler output
// Module: FermionGinCore
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* l_Nat_reprFast(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "weight"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__9_value;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "sign"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__11_value;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__12;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__13_value;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__14_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__14;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__17_value;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FermionGinCore_instReprSignedWeight___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight___closed__0 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_is__exact__involution__partner(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_is__exact__involution__partner___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "u"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = "v"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__6_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond___closed__0 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 36, .m_capacity = 36, .m_length = 35, .m_data = "FermionGinCore.TerminalRoute.Repair"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 47, .m_capacity = 47, .m_length = 46, .m_data = "FermionGinCore.TerminalRoute.SplitBrainRefusal"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 44, .m_capacity = 44, .m_length = 43, .m_data = "FermionGinCore.TerminalRoute.ClosureFailure"};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__5_value;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6;
static lean_once_cell_t lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute___closed__0 = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute = (const lean_object*)&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_TerminalRoute_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqTerminalRoute(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqTerminalRoute___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_evaluate__gin__fermion__recovery(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_evaluate__gin__fermion__recovery___boxed(lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_14_; lean_object* v___x_15_; 
v___x_14_ = lean_unsigned_to_nat(10u);
v___x_15_ = lean_nat_to_int(v___x_14_);
return v___x_15_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__12(void){
_start:
{
lean_object* v___x_22_; lean_object* v___x_23_; 
v___x_22_ = lean_unsigned_to_nat(8u);
v___x_23_ = lean_nat_to_int(v___x_22_);
return v___x_23_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__14(void){
_start:
{
lean_object* v___x_25_; lean_object* v___x_26_; 
v___x_25_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__0));
v___x_26_ = lean_string_length(v___x_25_);
return v___x_26_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; 
v___x_27_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__14, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__14_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__14);
v___x_28_ = lean_nat_to_int(v___x_27_);
return v___x_28_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_unsigned_to_nat(0u);
v___x_34_ = lean_nat_to_int(v___x_33_);
return v___x_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg(lean_object* v_x_35_){
_start:
{
lean_object* v_weight_36_; lean_object* v_sign_37_; lean_object* v___x_39_; uint8_t v_isShared_40_; uint8_t v_isSharedCheck_80_; 
v_weight_36_ = lean_ctor_get(v_x_35_, 0);
v_sign_37_ = lean_ctor_get(v_x_35_, 1);
v_isSharedCheck_80_ = !lean_is_exclusive(v_x_35_);
if (v_isSharedCheck_80_ == 0)
{
v___x_39_ = v_x_35_;
v_isShared_40_ = v_isSharedCheck_80_;
goto v_resetjp_38_;
}
else
{
lean_inc(v_sign_37_);
lean_inc(v_weight_36_);
lean_dec(v_x_35_);
v___x_39_ = lean_box(0);
v_isShared_40_ = v_isSharedCheck_80_;
goto v_resetjp_38_;
}
v_resetjp_38_:
{
lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___x_45_; lean_object* v___x_47_; 
v___x_41_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5));
v___x_42_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__6));
v___x_43_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__7, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__7);
v___x_44_ = l_Nat_reprFast(v_weight_36_);
v___x_45_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_45_, 0, v___x_44_);
if (v_isShared_40_ == 0)
{
lean_ctor_set_tag(v___x_39_, 4);
lean_ctor_set(v___x_39_, 1, v___x_45_);
lean_ctor_set(v___x_39_, 0, v___x_43_);
v___x_47_ = v___x_39_;
goto v_reusejp_46_;
}
else
{
lean_object* v_reuseFailAlloc_79_; 
v_reuseFailAlloc_79_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_79_, 0, v___x_43_);
lean_ctor_set(v_reuseFailAlloc_79_, 1, v___x_45_);
v___x_47_ = v_reuseFailAlloc_79_;
goto v_reusejp_46_;
}
v_reusejp_46_:
{
uint8_t v___x_48_; lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; lean_object* v___x_52_; lean_object* v___x_53_; lean_object* v___x_54_; lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; lean_object* v___y_60_; lean_object* v___x_71_; lean_object* v___x_72_; uint8_t v___x_73_; 
v___x_48_ = 0;
v___x_49_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_49_, 0, v___x_47_);
lean_ctor_set_uint8(v___x_49_, sizeof(void*)*1, v___x_48_);
v___x_50_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_50_, 0, v___x_42_);
lean_ctor_set(v___x_50_, 1, v___x_49_);
v___x_51_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__9));
v___x_52_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_52_, 0, v___x_50_);
lean_ctor_set(v___x_52_, 1, v___x_51_);
v___x_53_ = lean_box(1);
v___x_54_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_54_, 0, v___x_52_);
lean_ctor_set(v___x_54_, 1, v___x_53_);
v___x_55_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__11));
v___x_56_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_56_, 0, v___x_54_);
lean_ctor_set(v___x_56_, 1, v___x_55_);
v___x_57_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_57_, 0, v___x_56_);
lean_ctor_set(v___x_57_, 1, v___x_41_);
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__12, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__12_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__12);
v___x_71_ = lean_unsigned_to_nat(0u);
v___x_72_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18);
v___x_73_ = lean_int_dec_lt(v_sign_37_, v___x_72_);
if (v___x_73_ == 0)
{
lean_object* v___x_74_; lean_object* v___x_75_; 
v___x_74_ = l_Int_repr(v_sign_37_);
lean_dec(v_sign_37_);
v___x_75_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_75_, 0, v___x_74_);
v___y_60_ = v___x_75_;
goto v___jp_59_;
}
else
{
lean_object* v___x_76_; lean_object* v___x_77_; lean_object* v___x_78_; 
v___x_76_ = l_Int_repr(v_sign_37_);
lean_dec(v_sign_37_);
v___x_77_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_77_, 0, v___x_76_);
v___x_78_ = l_Repr_addAppParen(v___x_77_, v___x_71_);
v___y_60_ = v___x_78_;
goto v___jp_59_;
}
v___jp_59_:
{
lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; lean_object* v___x_70_; 
v___x_61_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_61_, 0, v___x_58_);
lean_ctor_set(v___x_61_, 1, v___y_60_);
v___x_62_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_62_, 0, v___x_61_);
lean_ctor_set_uint8(v___x_62_, sizeof(void*)*1, v___x_48_);
v___x_63_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_63_, 0, v___x_57_);
lean_ctor_set(v___x_63_, 1, v___x_62_);
v___x_64_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15);
v___x_65_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__16));
v___x_66_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_66_, 0, v___x_65_);
lean_ctor_set(v___x_66_, 1, v___x_63_);
v___x_67_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__17));
v___x_68_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_68_, 0, v___x_66_);
lean_ctor_set(v___x_68_, 1, v___x_67_);
v___x_69_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_69_, 0, v___x_64_);
lean_ctor_set(v___x_69_, 1, v___x_68_);
v___x_70_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_70_, 0, v___x_69_);
lean_ctor_set_uint8(v___x_70_, sizeof(void*)*1, v___x_48_);
return v___x_70_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr(lean_object* v_x_81_, lean_object* v_prec_82_){
_start:
{
lean_object* v___x_83_; 
v___x_83_ = lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg(v_x_81_);
return v___x_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___boxed(lean_object* v_x_84_, lean_object* v_prec_85_){
_start:
{
lean_object* v_res_86_; 
v_res_86_ = lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr(v_x_84_, v_prec_85_);
lean_dec(v_prec_85_);
return v_res_86_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight_decEq(lean_object* v_x_89_, lean_object* v_x_90_){
_start:
{
lean_object* v_weight_91_; lean_object* v_sign_92_; lean_object* v_weight_93_; lean_object* v_sign_94_; uint8_t v___x_95_; 
v_weight_91_ = lean_ctor_get(v_x_89_, 0);
v_sign_92_ = lean_ctor_get(v_x_89_, 1);
v_weight_93_ = lean_ctor_get(v_x_90_, 0);
v_sign_94_ = lean_ctor_get(v_x_90_, 1);
v___x_95_ = lean_nat_dec_eq(v_weight_91_, v_weight_93_);
if (v___x_95_ == 0)
{
return v___x_95_;
}
else
{
uint8_t v___x_96_; 
v___x_96_ = lean_int_dec_eq(v_sign_92_, v_sign_94_);
return v___x_96_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight_decEq___boxed(lean_object* v_x_97_, lean_object* v_x_98_){
_start:
{
uint8_t v_res_99_; lean_object* v_r_100_; 
v_res_99_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight_decEq(v_x_97_, v_x_98_);
lean_dec_ref(v_x_98_);
lean_dec_ref(v_x_97_);
v_r_100_ = lean_box(v_res_99_);
return v_r_100_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight(lean_object* v_x_101_, lean_object* v_x_102_){
_start:
{
uint8_t v___x_103_; 
v___x_103_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight_decEq(v_x_101_, v_x_102_);
return v___x_103_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight___boxed(lean_object* v_x_104_, lean_object* v_x_105_){
_start:
{
uint8_t v_res_106_; lean_object* v_r_107_; 
v_res_106_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqSignedWeight(v_x_104_, v_x_105_);
lean_dec_ref(v_x_105_);
lean_dec_ref(v_x_104_);
v_r_107_ = lean_box(v_res_106_);
return v_r_107_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_is__exact__involution__partner(lean_object* v_c1_108_, lean_object* v_c2_109_){
_start:
{
lean_object* v_weight_110_; lean_object* v_sign_111_; lean_object* v_weight_112_; lean_object* v_sign_113_; uint8_t v___x_114_; 
v_weight_110_ = lean_ctor_get(v_c1_108_, 0);
v_sign_111_ = lean_ctor_get(v_c1_108_, 1);
v_weight_112_ = lean_ctor_get(v_c2_109_, 0);
v_sign_113_ = lean_ctor_get(v_c2_109_, 1);
v___x_114_ = lean_nat_dec_eq(v_weight_110_, v_weight_112_);
if (v___x_114_ == 0)
{
return v___x_114_;
}
else
{
lean_object* v___x_115_; lean_object* v___x_116_; uint8_t v___x_117_; 
v___x_115_ = lean_int_add(v_sign_111_, v_sign_113_);
v___x_116_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__18);
v___x_117_ = lean_int_dec_eq(v___x_115_, v___x_116_);
lean_dec(v___x_115_);
return v___x_117_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_is__exact__involution__partner___boxed(lean_object* v_c1_118_, lean_object* v_c2_119_){
_start:
{
uint8_t v_res_120_; lean_object* v_r_121_; 
v_res_120_ = lp_FiniteQuantum_FermionGinCore_is__exact__involution__partner(v_c1_118_, v_c2_119_);
lean_dec_ref(v_c2_119_);
lean_dec_ref(v_c1_118_);
v_r_121_ = lean_box(v_res_120_);
return v_r_121_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_131_; lean_object* v___x_132_; 
v___x_131_ = lean_unsigned_to_nat(5u);
v___x_132_ = lean_nat_to_int(v___x_131_);
return v___x_132_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg(lean_object* v_x_136_){
_start:
{
lean_object* v_u_137_; lean_object* v_v_138_; lean_object* v___x_140_; uint8_t v_isShared_141_; uint8_t v_isSharedCheck_172_; 
v_u_137_ = lean_ctor_get(v_x_136_, 0);
v_v_138_ = lean_ctor_get(v_x_136_, 1);
v_isSharedCheck_172_ = !lean_is_exclusive(v_x_136_);
if (v_isSharedCheck_172_ == 0)
{
v___x_140_ = v_x_136_;
v_isShared_141_ = v_isSharedCheck_172_;
goto v_resetjp_139_;
}
else
{
lean_inc(v_v_138_);
lean_inc(v_u_137_);
lean_dec(v_x_136_);
v___x_140_ = lean_box(0);
v_isShared_141_ = v_isSharedCheck_172_;
goto v_resetjp_139_;
}
v_resetjp_139_:
{
lean_object* v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; lean_object* v___x_145_; lean_object* v___x_146_; lean_object* v___x_148_; 
v___x_142_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__5));
v___x_143_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__3));
v___x_144_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__4, &lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__4);
v___x_145_ = l_Nat_reprFast(v_u_137_);
v___x_146_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_146_, 0, v___x_145_);
if (v_isShared_141_ == 0)
{
lean_ctor_set_tag(v___x_140_, 4);
lean_ctor_set(v___x_140_, 1, v___x_146_);
lean_ctor_set(v___x_140_, 0, v___x_144_);
v___x_148_ = v___x_140_;
goto v_reusejp_147_;
}
else
{
lean_object* v_reuseFailAlloc_171_; 
v_reuseFailAlloc_171_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_171_, 0, v___x_144_);
lean_ctor_set(v_reuseFailAlloc_171_, 1, v___x_146_);
v___x_148_ = v_reuseFailAlloc_171_;
goto v_reusejp_147_;
}
v_reusejp_147_:
{
uint8_t v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; lean_object* v___x_152_; lean_object* v___x_153_; lean_object* v___x_154_; lean_object* v___x_155_; lean_object* v___x_156_; lean_object* v___x_157_; lean_object* v___x_158_; lean_object* v___x_159_; lean_object* v___x_160_; lean_object* v___x_161_; lean_object* v___x_162_; lean_object* v___x_163_; lean_object* v___x_164_; lean_object* v___x_165_; lean_object* v___x_166_; lean_object* v___x_167_; lean_object* v___x_168_; lean_object* v___x_169_; lean_object* v___x_170_; 
v___x_149_ = 0;
v___x_150_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_150_, 0, v___x_148_);
lean_ctor_set_uint8(v___x_150_, sizeof(void*)*1, v___x_149_);
v___x_151_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_151_, 0, v___x_143_);
lean_ctor_set(v___x_151_, 1, v___x_150_);
v___x_152_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__9));
v___x_153_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_153_, 0, v___x_151_);
lean_ctor_set(v___x_153_, 1, v___x_152_);
v___x_154_ = lean_box(1);
v___x_155_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_155_, 0, v___x_153_);
lean_ctor_set(v___x_155_, 1, v___x_154_);
v___x_156_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg___closed__6));
v___x_157_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_157_, 0, v___x_155_);
lean_ctor_set(v___x_157_, 1, v___x_156_);
v___x_158_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_158_, 0, v___x_157_);
lean_ctor_set(v___x_158_, 1, v___x_142_);
v___x_159_ = l_Nat_reprFast(v_v_138_);
v___x_160_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_160_, 0, v___x_159_);
v___x_161_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_161_, 0, v___x_144_);
lean_ctor_set(v___x_161_, 1, v___x_160_);
v___x_162_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_162_, 0, v___x_161_);
lean_ctor_set_uint8(v___x_162_, sizeof(void*)*1, v___x_149_);
v___x_163_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_163_, 0, v___x_158_);
lean_ctor_set(v___x_163_, 1, v___x_162_);
v___x_164_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15, &lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__15);
v___x_165_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__16));
v___x_166_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_166_, 0, v___x_165_);
lean_ctor_set(v___x_166_, 1, v___x_163_);
v___x_167_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprSignedWeight_repr___redArg___closed__17));
v___x_168_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_168_, 0, v___x_166_);
lean_ctor_set(v___x_168_, 1, v___x_167_);
v___x_169_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_169_, 0, v___x_164_);
lean_ctor_set(v___x_169_, 1, v___x_168_);
v___x_170_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_170_, 0, v___x_169_);
lean_ctor_set_uint8(v___x_170_, sizeof(void*)*1, v___x_149_);
return v___x_170_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr(lean_object* v_x_173_, lean_object* v_prec_174_){
_start:
{
lean_object* v___x_175_; 
v___x_175_ = lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___redArg(v_x_173_);
return v___x_175_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr___boxed(lean_object* v_x_176_, lean_object* v_prec_177_){
_start:
{
lean_object* v_res_178_; 
v_res_178_ = lp_FiniteQuantum_FermionGinCore_instReprMajoranaBond_repr(v_x_176_, v_prec_177_);
lean_dec(v_prec_177_);
return v_res_178_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond_decEq(lean_object* v_x_181_, lean_object* v_x_182_){
_start:
{
lean_object* v_u_183_; lean_object* v_v_184_; lean_object* v_u_185_; lean_object* v_v_186_; uint8_t v___x_187_; 
v_u_183_ = lean_ctor_get(v_x_181_, 0);
v_v_184_ = lean_ctor_get(v_x_181_, 1);
v_u_185_ = lean_ctor_get(v_x_182_, 0);
v_v_186_ = lean_ctor_get(v_x_182_, 1);
v___x_187_ = lean_nat_dec_eq(v_u_183_, v_u_185_);
if (v___x_187_ == 0)
{
return v___x_187_;
}
else
{
uint8_t v___x_188_; 
v___x_188_ = lean_nat_dec_eq(v_v_184_, v_v_186_);
return v___x_188_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond_decEq___boxed(lean_object* v_x_189_, lean_object* v_x_190_){
_start:
{
uint8_t v_res_191_; lean_object* v_r_192_; 
v_res_191_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond_decEq(v_x_189_, v_x_190_);
lean_dec_ref(v_x_190_);
lean_dec_ref(v_x_189_);
v_r_192_ = lean_box(v_res_191_);
return v_r_192_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond(lean_object* v_x_193_, lean_object* v_x_194_){
_start:
{
uint8_t v___x_195_; 
v___x_195_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond_decEq(v_x_193_, v_x_194_);
return v___x_195_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond___boxed(lean_object* v_x_196_, lean_object* v_x_197_){
_start:
{
uint8_t v_res_198_; lean_object* v_r_199_; 
v_res_198_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqMajoranaBond(v_x_196_, v_x_197_);
lean_dec_ref(v_x_197_);
lean_dec_ref(v_x_196_);
v_r_199_ = lean_box(v_res_198_);
return v_r_199_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx(uint8_t v_x_200_){
_start:
{
switch(v_x_200_)
{
case 0:
{
lean_object* v___x_201_; 
v___x_201_ = lean_unsigned_to_nat(0u);
return v___x_201_;
}
case 1:
{
lean_object* v___x_202_; 
v___x_202_ = lean_unsigned_to_nat(1u);
return v___x_202_;
}
default: 
{
lean_object* v___x_203_; 
v___x_203_ = lean_unsigned_to_nat(2u);
return v___x_203_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx___boxed(lean_object* v_x_204_){
_start:
{
uint8_t v_x_boxed_205_; lean_object* v_res_206_; 
v_x_boxed_205_ = lean_unbox(v_x_204_);
v_res_206_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx(v_x_boxed_205_);
return v_res_206_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_toCtorIdx(uint8_t v_x_207_){
_start:
{
lean_object* v___x_208_; 
v___x_208_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx(v_x_207_);
return v___x_208_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_toCtorIdx___boxed(lean_object* v_x_209_){
_start:
{
uint8_t v_x_4__boxed_210_; lean_object* v_res_211_; 
v_x_4__boxed_210_ = lean_unbox(v_x_209_);
v_res_211_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_toCtorIdx(v_x_4__boxed_210_);
return v_res_211_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___redArg(lean_object* v_k_212_){
_start:
{
lean_inc(v_k_212_);
return v_k_212_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___redArg___boxed(lean_object* v_k_213_){
_start:
{
lean_object* v_res_214_; 
v_res_214_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___redArg(v_k_213_);
lean_dec(v_k_213_);
return v_res_214_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim(lean_object* v_motive_215_, lean_object* v_ctorIdx_216_, uint8_t v_t_217_, lean_object* v_h_218_, lean_object* v_k_219_){
_start:
{
lean_inc(v_k_219_);
return v_k_219_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim___boxed(lean_object* v_motive_220_, lean_object* v_ctorIdx_221_, lean_object* v_t_222_, lean_object* v_h_223_, lean_object* v_k_224_){
_start:
{
uint8_t v_t_boxed_225_; lean_object* v_res_226_; 
v_t_boxed_225_ = lean_unbox(v_t_222_);
v_res_226_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorElim(v_motive_220_, v_ctorIdx_221_, v_t_boxed_225_, v_h_223_, v_k_224_);
lean_dec(v_k_224_);
lean_dec(v_ctorIdx_221_);
return v_res_226_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___redArg(lean_object* v_Repair_227_){
_start:
{
lean_inc(v_Repair_227_);
return v_Repair_227_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___redArg___boxed(lean_object* v_Repair_228_){
_start:
{
lean_object* v_res_229_; 
v_res_229_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___redArg(v_Repair_228_);
lean_dec(v_Repair_228_);
return v_res_229_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim(lean_object* v_motive_230_, uint8_t v_t_231_, lean_object* v_h_232_, lean_object* v_Repair_233_){
_start:
{
lean_inc(v_Repair_233_);
return v_Repair_233_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim___boxed(lean_object* v_motive_234_, lean_object* v_t_235_, lean_object* v_h_236_, lean_object* v_Repair_237_){
_start:
{
uint8_t v_t_boxed_238_; lean_object* v_res_239_; 
v_t_boxed_238_ = lean_unbox(v_t_235_);
v_res_239_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_Repair_elim(v_motive_234_, v_t_boxed_238_, v_h_236_, v_Repair_237_);
lean_dec(v_Repair_237_);
return v_res_239_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object* v_SplitBrainRefusal_240_){
_start:
{
lean_inc(v_SplitBrainRefusal_240_);
return v_SplitBrainRefusal_240_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object* v_SplitBrainRefusal_241_){
_start:
{
lean_object* v_res_242_; 
v_res_242_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___redArg(v_SplitBrainRefusal_241_);
lean_dec(v_SplitBrainRefusal_241_);
return v_res_242_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim(lean_object* v_motive_243_, uint8_t v_t_244_, lean_object* v_h_245_, lean_object* v_SplitBrainRefusal_246_){
_start:
{
lean_inc(v_SplitBrainRefusal_246_);
return v_SplitBrainRefusal_246_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object* v_motive_247_, lean_object* v_t_248_, lean_object* v_h_249_, lean_object* v_SplitBrainRefusal_250_){
_start:
{
uint8_t v_t_boxed_251_; lean_object* v_res_252_; 
v_t_boxed_251_ = lean_unbox(v_t_248_);
v_res_252_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_SplitBrainRefusal_elim(v_motive_247_, v_t_boxed_251_, v_h_249_, v_SplitBrainRefusal_250_);
lean_dec(v_SplitBrainRefusal_250_);
return v_res_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___redArg(lean_object* v_ClosureFailure_253_){
_start:
{
lean_inc(v_ClosureFailure_253_);
return v_ClosureFailure_253_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object* v_ClosureFailure_254_){
_start:
{
lean_object* v_res_255_; 
v_res_255_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___redArg(v_ClosureFailure_254_);
lean_dec(v_ClosureFailure_254_);
return v_res_255_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim(lean_object* v_motive_256_, uint8_t v_t_257_, lean_object* v_h_258_, lean_object* v_ClosureFailure_259_){
_start:
{
lean_inc(v_ClosureFailure_259_);
return v_ClosureFailure_259_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim___boxed(lean_object* v_motive_260_, lean_object* v_t_261_, lean_object* v_h_262_, lean_object* v_ClosureFailure_263_){
_start:
{
uint8_t v_t_boxed_264_; lean_object* v_res_265_; 
v_t_boxed_264_ = lean_unbox(v_t_261_);
v_res_265_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ClosureFailure_elim(v_motive_260_, v_t_boxed_264_, v_h_262_, v_ClosureFailure_263_);
lean_dec(v_ClosureFailure_263_);
return v_res_265_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6(void){
_start:
{
lean_object* v___x_275_; lean_object* v___x_276_; 
v___x_275_ = lean_unsigned_to_nat(2u);
v___x_276_ = lean_nat_to_int(v___x_275_);
return v___x_276_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7(void){
_start:
{
lean_object* v___x_277_; lean_object* v___x_278_; 
v___x_277_ = lean_unsigned_to_nat(1u);
v___x_278_ = lean_nat_to_int(v___x_277_);
return v___x_278_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr(uint8_t v_x_279_, lean_object* v_prec_280_){
_start:
{
lean_object* v___y_282_; lean_object* v___y_289_; lean_object* v___y_296_; 
switch(v_x_279_)
{
case 0:
{
lean_object* v___x_302_; uint8_t v___x_303_; 
v___x_302_ = lean_unsigned_to_nat(1024u);
v___x_303_ = lean_nat_dec_le(v___x_302_, v_prec_280_);
if (v___x_303_ == 0)
{
lean_object* v___x_304_; 
v___x_304_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6, &lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6_once, _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6);
v___y_282_ = v___x_304_;
goto v___jp_281_;
}
else
{
lean_object* v___x_305_; 
v___x_305_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7, &lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7_once, _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7);
v___y_282_ = v___x_305_;
goto v___jp_281_;
}
}
case 1:
{
lean_object* v___x_306_; uint8_t v___x_307_; 
v___x_306_ = lean_unsigned_to_nat(1024u);
v___x_307_ = lean_nat_dec_le(v___x_306_, v_prec_280_);
if (v___x_307_ == 0)
{
lean_object* v___x_308_; 
v___x_308_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6, &lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6_once, _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6);
v___y_289_ = v___x_308_;
goto v___jp_288_;
}
else
{
lean_object* v___x_309_; 
v___x_309_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7, &lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7_once, _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7);
v___y_289_ = v___x_309_;
goto v___jp_288_;
}
}
default: 
{
lean_object* v___x_310_; uint8_t v___x_311_; 
v___x_310_ = lean_unsigned_to_nat(1024u);
v___x_311_ = lean_nat_dec_le(v___x_310_, v_prec_280_);
if (v___x_311_ == 0)
{
lean_object* v___x_312_; 
v___x_312_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6, &lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6_once, _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__6);
v___y_296_ = v___x_312_;
goto v___jp_295_;
}
else
{
lean_object* v___x_313_; 
v___x_313_ = lean_obj_once(&lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7, &lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7_once, _init_lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__7);
v___y_296_ = v___x_313_;
goto v___jp_295_;
}
}
}
v___jp_281_:
{
lean_object* v___x_283_; lean_object* v___x_284_; uint8_t v___x_285_; lean_object* v___x_286_; lean_object* v___x_287_; 
v___x_283_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__1));
lean_inc(v___y_282_);
v___x_284_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_284_, 0, v___y_282_);
lean_ctor_set(v___x_284_, 1, v___x_283_);
v___x_285_ = 0;
v___x_286_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_286_, 0, v___x_284_);
lean_ctor_set_uint8(v___x_286_, sizeof(void*)*1, v___x_285_);
v___x_287_ = l_Repr_addAppParen(v___x_286_, v_prec_280_);
return v___x_287_;
}
v___jp_288_:
{
lean_object* v___x_290_; lean_object* v___x_291_; uint8_t v___x_292_; lean_object* v___x_293_; lean_object* v___x_294_; 
v___x_290_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__3));
lean_inc(v___y_289_);
v___x_291_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_291_, 0, v___y_289_);
lean_ctor_set(v___x_291_, 1, v___x_290_);
v___x_292_ = 0;
v___x_293_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_293_, 0, v___x_291_);
lean_ctor_set_uint8(v___x_293_, sizeof(void*)*1, v___x_292_);
v___x_294_ = l_Repr_addAppParen(v___x_293_, v_prec_280_);
return v___x_294_;
}
v___jp_295_:
{
lean_object* v___x_297_; lean_object* v___x_298_; uint8_t v___x_299_; lean_object* v___x_300_; lean_object* v___x_301_; 
v___x_297_ = ((lean_object*)(lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___closed__5));
lean_inc(v___y_296_);
v___x_298_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_298_, 0, v___y_296_);
lean_ctor_set(v___x_298_, 1, v___x_297_);
v___x_299_ = 0;
v___x_300_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_300_, 0, v___x_298_);
lean_ctor_set_uint8(v___x_300_, sizeof(void*)*1, v___x_299_);
v___x_301_ = l_Repr_addAppParen(v___x_300_, v_prec_280_);
return v___x_301_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr___boxed(lean_object* v_x_314_, lean_object* v_prec_315_){
_start:
{
uint8_t v_x_177__boxed_316_; lean_object* v_res_317_; 
v_x_177__boxed_316_ = lean_unbox(v_x_314_);
v_res_317_ = lp_FiniteQuantum_FermionGinCore_instReprTerminalRoute_repr(v_x_177__boxed_316_, v_prec_315_);
lean_dec(v_prec_315_);
return v_res_317_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_TerminalRoute_ofNat(lean_object* v_n_320_){
_start:
{
lean_object* v___x_321_; uint8_t v___x_322_; 
v___x_321_ = lean_unsigned_to_nat(0u);
v___x_322_ = lean_nat_dec_le(v_n_320_, v___x_321_);
if (v___x_322_ == 0)
{
lean_object* v___x_323_; uint8_t v___x_324_; 
v___x_323_ = lean_unsigned_to_nat(1u);
v___x_324_ = lean_nat_dec_le(v_n_320_, v___x_323_);
if (v___x_324_ == 0)
{
uint8_t v___x_325_; 
v___x_325_ = 2;
return v___x_325_;
}
else
{
uint8_t v___x_326_; 
v___x_326_ = 1;
return v___x_326_;
}
}
else
{
uint8_t v___x_327_; 
v___x_327_ = 0;
return v___x_327_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_TerminalRoute_ofNat___boxed(lean_object* v_n_328_){
_start:
{
uint8_t v_res_329_; lean_object* v_r_330_; 
v_res_329_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ofNat(v_n_328_);
lean_dec(v_n_328_);
v_r_330_ = lean_box(v_res_329_);
return v_r_330_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_instDecidableEqTerminalRoute(uint8_t v_x_331_, uint8_t v_y_332_){
_start:
{
lean_object* v___x_333_; lean_object* v___x_334_; uint8_t v___x_335_; 
v___x_333_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx(v_x_331_);
v___x_334_ = lp_FiniteQuantum_FermionGinCore_TerminalRoute_ctorIdx(v_y_332_);
v___x_335_ = lean_nat_dec_eq(v___x_333_, v___x_334_);
lean_dec(v___x_334_);
lean_dec(v___x_333_);
return v___x_335_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_instDecidableEqTerminalRoute___boxed(lean_object* v_x_336_, lean_object* v_y_337_){
_start:
{
uint8_t v_x_13__boxed_338_; uint8_t v_y_14__boxed_339_; uint8_t v_res_340_; lean_object* v_r_341_; 
v_x_13__boxed_338_ = lean_unbox(v_x_336_);
v_y_14__boxed_339_ = lean_unbox(v_y_337_);
v_res_340_ = lp_FiniteQuantum_FermionGinCore_instDecidableEqTerminalRoute(v_x_13__boxed_338_, v_y_14__boxed_339_);
v_r_341_ = lean_box(v_res_340_);
return v_r_341_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionGinCore_evaluate__gin__fermion__recovery(uint8_t v_is__valid__index_342_, lean_object* v_uncancelled__sign__mass_343_){
_start:
{
if (v_is__valid__index_342_ == 0)
{
uint8_t v___x_344_; 
v___x_344_ = 2;
return v___x_344_;
}
else
{
lean_object* v___x_345_; uint8_t v___x_346_; 
v___x_345_ = lean_unsigned_to_nat(0u);
v___x_346_ = lean_nat_dec_eq(v_uncancelled__sign__mass_343_, v___x_345_);
if (v___x_346_ == 0)
{
uint8_t v___x_347_; 
v___x_347_ = 1;
return v___x_347_;
}
else
{
uint8_t v___x_348_; 
v___x_348_ = 0;
return v___x_348_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionGinCore_evaluate__gin__fermion__recovery___boxed(lean_object* v_is__valid__index_349_, lean_object* v_uncancelled__sign__mass_350_){
_start:
{
uint8_t v_is__valid__index_boxed_351_; uint8_t v_res_352_; lean_object* v_r_353_; 
v_is__valid__index_boxed_351_ = lean_unbox(v_is__valid__index_349_);
v_res_352_ = lp_FiniteQuantum_FermionGinCore_evaluate__gin__fermion__recovery(v_is__valid__index_boxed_351_, v_uncancelled__sign__mass_350_);
lean_dec(v_uncancelled__sign__mass_350_);
v_r_353_ = lean_box(v_res_352_);
return v_r_353_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_FermionGinCore(uint8_t builtin) {
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
