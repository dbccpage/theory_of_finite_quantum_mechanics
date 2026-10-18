// Lean compiler output
// Module: DerivationDagQMClosure
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
lean_object* lean_nat_mod(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* l_Nat_reprFast(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_nat_abs(lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* l_instDecidableEqNat___boxed(lean_object*, lean_object*);
uint8_t l_instDecidableEqProd___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* l_Fin_add(lean_object*, lean_object*, lean_object*);
lean_object* l_List_lengthTR___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPrimGenEvent(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPrimGenEvent___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 65, .m_capacity = 65, .m_length = 64, .m_data = "QuantumMechanics.DerivationDagQMClosure.PrimGenEvent.declareTerm"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 64, .m_capacity = 64, .m_length = 63, .m_data = "QuantumMechanics.DerivationDagQMClosure.PrimGenEvent.assertDiff"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 64, .m_capacity = 64, .m_length = 63, .m_data = "QuantumMechanics.DerivationDagQMClosure.PrimGenEvent.removeDiff"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 67, .m_capacity = 67, .m_length = 66, .m_data = "QuantumMechanics.DerivationDagQMClosure.PrimGenEvent.identifyTerms"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__7_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "termsAdded"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__9_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "assertionsAdded"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__11_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__12;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "destructiveOps"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__16_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__17;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_zero___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_zero___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_zero___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_zero = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_zero___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_add___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_totalCost(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_totalCost___boxed(lean_object*);
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__2_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceObligation(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceObligation___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_traceObligation_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_traceObligation_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_edgeResidualL1(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_edgeResidualL1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_edgeResidualL1_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_edgeResidualL1_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_attachTwoSimplex(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerOne(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerOne___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerTwo(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerTwo___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_sqDiffSum3(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_sqDiffSum3___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagExpectation3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagExpectation3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityDiag3(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityDiag3___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityRankOneExpanded3(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityRankOneExpanded3___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_plusMinusExpectation(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_plusMinusExpectation___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m00"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m11"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m10"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__9_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "m01"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__11_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagMat2(lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__3_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(6) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__4 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(5) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__5 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(4) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__6 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__7 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__7_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(9) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__8 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(8) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__9 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__9_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(7) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__9_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__10 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(6) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__11 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(12) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__12 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__12_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(11) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__12_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__13 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(10) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__14 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__14_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(9) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__14_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__15 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(15) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__16 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(14) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__17 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__17_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(13) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__17_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__18 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__18_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(12) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__18_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__19 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__19_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__20 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__20_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(17) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__20_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__21 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__21_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(16) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__21_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__22 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__22_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(15) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__22_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__23 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__23_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(17) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__24 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__24_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(10) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__24_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__25 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__25_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(8) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__25_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__26 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__26_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__26_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__27 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__27_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__28_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(14) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__28 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__28_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__29_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(11) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__28_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__29 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__29_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__30_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(4) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__29_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__30 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__30_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__31_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__30_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__31 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__31_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__32_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(16) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__32 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__32_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__33_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(13) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__32_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__33 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__33_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__34_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(7) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__33_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__34 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__34_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__35_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(5) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__34_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__35 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__35_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__36_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__35_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__36 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__36_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__37_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__31_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__36_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__37 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__37_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__38_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__27_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__37_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__38 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__38_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__39_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__23_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__38_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__39 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__39_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__40_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__19_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__39_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__40 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__40_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__41_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__15_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__40_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__41 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__41_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__42_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__11_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__41_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__42 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__42_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__43_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__7_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__42_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__43 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__43_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__44_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__3_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__43_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__44 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__44_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts___closed__44_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_List_elem___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_elem___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__1___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceZeroDetNeg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceZeroDetNeg___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_sub___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_trace(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_trace___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 6, .m_capacity = 6, .m_length = 5, .m_data = "score"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "defect"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__2_value),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__4;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "witnessBound"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizeFromReceipt(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizeFromReceipt___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_trivalentSpinAdmissible(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_trivalentSpinAdmissible___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_add___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_pairInList(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_pairInList___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_pairInList_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_pairInList_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet(uint8_t, uint8_t, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_totalWeight(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedChshSum(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_totalWeight_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_totalWeight_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mat2Det(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mat2Det___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__0;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__1;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__2;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__3;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__4;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__5;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__6;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__7;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__8;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__9;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__10;
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__11_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__11;
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedL1Two(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedL1Two___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gAdd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gAdd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gConj(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gMul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gMul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gNormSq(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gNormSq___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPreGenOp(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPreGenOp___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 57, .m_capacity = 57, .m_length = 56, .m_data = "QuantumMechanics.DerivationDagQMClosure.PreGenOp.mention"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 56, .m_capacity = 56, .m_length = 55, .m_data = "QuantumMechanics.DerivationDagQMClosure.PreGenOp.supply"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 59, .m_capacity = 59, .m_length = 58, .m_data = "QuantumMechanics.DerivationDagQMClosure.PreGenOp.designate"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "QuantumMechanics.DerivationDagQMClosure.PreGenOp.admit"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__7_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 56, .m_capacity = 56, .m_length = 55, .m_data = "QuantumMechanics.DerivationDagQMClosure.PreGenOp.retain"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__8 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__9 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__9_value;
static const lean_string_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 57, .m_capacity = 57, .m_length = 56, .m_data = "QuantumMechanics.DerivationDagQMClosure.PreGenOp.operate"};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__10 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__11 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__11_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_applyPreGenOp(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_applyPreGenOp___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___redArg(uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__2_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowAdmits(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowAdmits___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm101ThresholdCertificate(uint8_t, uint8_t, uint8_t, uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm101ThresholdCertificate___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm207To211StageAdmits(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm207To211StageAdmits___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockScopedFiniteHold(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockScopedFiniteHold___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockUnboundedTargetHold(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockUnboundedTargetHold___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_readoutScaled(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_readoutScaled___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizedStanding(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizedStanding___boxed(lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__2_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep1___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__2_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Rep2___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__0 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__1 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__2 = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__2_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum = (const lean_object*)&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4OrbitSum___closed__2_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Shift(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm122FullMncRecovered(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm122FullMncRecovered___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx(uint8_t v_x_1_){
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
case 2:
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(2u);
return v___x_4_;
}
default: 
{
lean_object* v___x_5_; 
v___x_5_ = lean_unsigned_to_nat(3u);
return v___x_5_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx___boxed(lean_object* v_x_6_){
_start:
{
uint8_t v_x_boxed_7_; lean_object* v_res_8_; 
v_x_boxed_7_ = lean_unbox(v_x_6_);
v_res_8_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx(v_x_boxed_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_toCtorIdx(uint8_t v_x_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx(v_x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_toCtorIdx___boxed(lean_object* v_x_11_){
_start:
{
uint8_t v_x_4__boxed_12_; lean_object* v_res_13_; 
v_x_4__boxed_12_ = lean_unbox(v_x_11_);
v_res_13_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_toCtorIdx(v_x_4__boxed_12_);
return v_res_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___redArg(lean_object* v_k_14_){
_start:
{
lean_inc(v_k_14_);
return v_k_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___redArg___boxed(lean_object* v_k_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___redArg(v_k_15_);
lean_dec(v_k_15_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim(lean_object* v_motive_17_, lean_object* v_ctorIdx_18_, uint8_t v_t_19_, lean_object* v_h_20_, lean_object* v_k_21_){
_start:
{
lean_inc(v_k_21_);
return v_k_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim___boxed(lean_object* v_motive_22_, lean_object* v_ctorIdx_23_, lean_object* v_t_24_, lean_object* v_h_25_, lean_object* v_k_26_){
_start:
{
uint8_t v_t_boxed_27_; lean_object* v_res_28_; 
v_t_boxed_27_ = lean_unbox(v_t_24_);
v_res_28_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorElim(v_motive_22_, v_ctorIdx_23_, v_t_boxed_27_, v_h_25_, v_k_26_);
lean_dec(v_k_26_);
lean_dec(v_ctorIdx_23_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___redArg(lean_object* v_declareTerm_29_){
_start:
{
lean_inc(v_declareTerm_29_);
return v_declareTerm_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___redArg___boxed(lean_object* v_declareTerm_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___redArg(v_declareTerm_30_);
lean_dec(v_declareTerm_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim(lean_object* v_motive_32_, uint8_t v_t_33_, lean_object* v_h_34_, lean_object* v_declareTerm_35_){
_start:
{
lean_inc(v_declareTerm_35_);
return v_declareTerm_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim___boxed(lean_object* v_motive_36_, lean_object* v_t_37_, lean_object* v_h_38_, lean_object* v_declareTerm_39_){
_start:
{
uint8_t v_t_boxed_40_; lean_object* v_res_41_; 
v_t_boxed_40_ = lean_unbox(v_t_37_);
v_res_41_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_declareTerm_elim(v_motive_36_, v_t_boxed_40_, v_h_38_, v_declareTerm_39_);
lean_dec(v_declareTerm_39_);
return v_res_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___redArg(lean_object* v_assertDiff_42_){
_start:
{
lean_inc(v_assertDiff_42_);
return v_assertDiff_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___redArg___boxed(lean_object* v_assertDiff_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___redArg(v_assertDiff_43_);
lean_dec(v_assertDiff_43_);
return v_res_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim(lean_object* v_motive_45_, uint8_t v_t_46_, lean_object* v_h_47_, lean_object* v_assertDiff_48_){
_start:
{
lean_inc(v_assertDiff_48_);
return v_assertDiff_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim___boxed(lean_object* v_motive_49_, lean_object* v_t_50_, lean_object* v_h_51_, lean_object* v_assertDiff_52_){
_start:
{
uint8_t v_t_boxed_53_; lean_object* v_res_54_; 
v_t_boxed_53_ = lean_unbox(v_t_50_);
v_res_54_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_assertDiff_elim(v_motive_49_, v_t_boxed_53_, v_h_51_, v_assertDiff_52_);
lean_dec(v_assertDiff_52_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___redArg(lean_object* v_removeDiff_55_){
_start:
{
lean_inc(v_removeDiff_55_);
return v_removeDiff_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___redArg___boxed(lean_object* v_removeDiff_56_){
_start:
{
lean_object* v_res_57_; 
v_res_57_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___redArg(v_removeDiff_56_);
lean_dec(v_removeDiff_56_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim(lean_object* v_motive_58_, uint8_t v_t_59_, lean_object* v_h_60_, lean_object* v_removeDiff_61_){
_start:
{
lean_inc(v_removeDiff_61_);
return v_removeDiff_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim___boxed(lean_object* v_motive_62_, lean_object* v_t_63_, lean_object* v_h_64_, lean_object* v_removeDiff_65_){
_start:
{
uint8_t v_t_boxed_66_; lean_object* v_res_67_; 
v_t_boxed_66_ = lean_unbox(v_t_63_);
v_res_67_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_removeDiff_elim(v_motive_62_, v_t_boxed_66_, v_h_64_, v_removeDiff_65_);
lean_dec(v_removeDiff_65_);
return v_res_67_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___redArg(lean_object* v_identifyTerms_68_){
_start:
{
lean_inc(v_identifyTerms_68_);
return v_identifyTerms_68_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___redArg___boxed(lean_object* v_identifyTerms_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___redArg(v_identifyTerms_69_);
lean_dec(v_identifyTerms_69_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim(lean_object* v_motive_71_, uint8_t v_t_72_, lean_object* v_h_73_, lean_object* v_identifyTerms_74_){
_start:
{
lean_inc(v_identifyTerms_74_);
return v_identifyTerms_74_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim___boxed(lean_object* v_motive_75_, lean_object* v_t_76_, lean_object* v_h_77_, lean_object* v_identifyTerms_78_){
_start:
{
uint8_t v_t_boxed_79_; lean_object* v_res_80_; 
v_t_boxed_79_ = lean_unbox(v_t_76_);
v_res_80_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_identifyTerms_elim(v_motive_75_, v_t_boxed_79_, v_h_77_, v_identifyTerms_78_);
lean_dec(v_identifyTerms_78_);
return v_res_80_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ofNat(lean_object* v_n_81_){
_start:
{
lean_object* v___x_82_; uint8_t v___x_83_; 
v___x_82_ = lean_unsigned_to_nat(1u);
v___x_83_ = lean_nat_dec_le(v_n_81_, v___x_82_);
if (v___x_83_ == 0)
{
lean_object* v___x_84_; uint8_t v___x_85_; 
v___x_84_ = lean_unsigned_to_nat(2u);
v___x_85_ = lean_nat_dec_le(v_n_81_, v___x_84_);
if (v___x_85_ == 0)
{
uint8_t v___x_86_; 
v___x_86_ = 3;
return v___x_86_;
}
else
{
uint8_t v___x_87_; 
v___x_87_ = 2;
return v___x_87_;
}
}
else
{
lean_object* v___x_88_; uint8_t v___x_89_; 
v___x_88_ = lean_unsigned_to_nat(0u);
v___x_89_ = lean_nat_dec_le(v_n_81_, v___x_88_);
if (v___x_89_ == 0)
{
uint8_t v___x_90_; 
v___x_90_ = 1;
return v___x_90_;
}
else
{
uint8_t v___x_91_; 
v___x_91_ = 0;
return v___x_91_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ofNat___boxed(lean_object* v_n_92_){
_start:
{
uint8_t v_res_93_; lean_object* v_r_94_; 
v_res_93_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ofNat(v_n_92_);
lean_dec(v_n_92_);
v_r_94_ = lean_box(v_res_93_);
return v_r_94_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPrimGenEvent(uint8_t v_x_95_, uint8_t v_y_96_){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_97_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx(v_x_95_);
v___x_98_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PrimGenEvent_ctorIdx(v_y_96_);
v___x_99_ = lean_nat_dec_eq(v___x_97_, v___x_98_);
lean_dec(v___x_98_);
lean_dec(v___x_97_);
return v___x_99_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPrimGenEvent___boxed(lean_object* v_x_100_, lean_object* v_y_101_){
_start:
{
uint8_t v_x_13__boxed_102_; uint8_t v_y_14__boxed_103_; uint8_t v_res_104_; lean_object* v_r_105_; 
v_x_13__boxed_102_ = lean_unbox(v_x_100_);
v_y_14__boxed_103_ = lean_unbox(v_y_101_);
v_res_104_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPrimGenEvent(v_x_13__boxed_102_, v_y_14__boxed_103_);
v_r_105_ = lean_box(v_res_104_);
return v_r_105_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(2u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_120_ = lean_unsigned_to_nat(1u);
v___x_121_ = lean_nat_to_int(v___x_120_);
return v___x_121_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr(uint8_t v_x_122_, lean_object* v_prec_123_){
_start:
{
lean_object* v___y_125_; lean_object* v___y_132_; lean_object* v___y_139_; lean_object* v___y_146_; 
switch(v_x_122_)
{
case 0:
{
lean_object* v___x_152_; uint8_t v___x_153_; 
v___x_152_ = lean_unsigned_to_nat(1024u);
v___x_153_ = lean_nat_dec_le(v___x_152_, v_prec_123_);
if (v___x_153_ == 0)
{
lean_object* v___x_154_; 
v___x_154_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_125_ = v___x_154_;
goto v___jp_124_;
}
else
{
lean_object* v___x_155_; 
v___x_155_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_125_ = v___x_155_;
goto v___jp_124_;
}
}
case 1:
{
lean_object* v___x_156_; uint8_t v___x_157_; 
v___x_156_ = lean_unsigned_to_nat(1024u);
v___x_157_ = lean_nat_dec_le(v___x_156_, v_prec_123_);
if (v___x_157_ == 0)
{
lean_object* v___x_158_; 
v___x_158_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_132_ = v___x_158_;
goto v___jp_131_;
}
else
{
lean_object* v___x_159_; 
v___x_159_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_132_ = v___x_159_;
goto v___jp_131_;
}
}
case 2:
{
lean_object* v___x_160_; uint8_t v___x_161_; 
v___x_160_ = lean_unsigned_to_nat(1024u);
v___x_161_ = lean_nat_dec_le(v___x_160_, v_prec_123_);
if (v___x_161_ == 0)
{
lean_object* v___x_162_; 
v___x_162_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_139_ = v___x_162_;
goto v___jp_138_;
}
else
{
lean_object* v___x_163_; 
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_139_ = v___x_163_;
goto v___jp_138_;
}
}
default: 
{
lean_object* v___x_164_; uint8_t v___x_165_; 
v___x_164_ = lean_unsigned_to_nat(1024u);
v___x_165_ = lean_nat_dec_le(v___x_164_, v_prec_123_);
if (v___x_165_ == 0)
{
lean_object* v___x_166_; 
v___x_166_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_146_ = v___x_166_;
goto v___jp_145_;
}
else
{
lean_object* v___x_167_; 
v___x_167_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_146_ = v___x_167_;
goto v___jp_145_;
}
}
}
v___jp_124_:
{
lean_object* v___x_126_; lean_object* v___x_127_; uint8_t v___x_128_; lean_object* v___x_129_; lean_object* v___x_130_; 
v___x_126_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__1));
lean_inc(v___y_125_);
v___x_127_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_127_, 0, v___y_125_);
lean_ctor_set(v___x_127_, 1, v___x_126_);
v___x_128_ = 0;
v___x_129_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_129_, 0, v___x_127_);
lean_ctor_set_uint8(v___x_129_, sizeof(void*)*1, v___x_128_);
v___x_130_ = l_Repr_addAppParen(v___x_129_, v_prec_123_);
return v___x_130_;
}
v___jp_131_:
{
lean_object* v___x_133_; lean_object* v___x_134_; uint8_t v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; 
v___x_133_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__3));
lean_inc(v___y_132_);
v___x_134_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_134_, 0, v___y_132_);
lean_ctor_set(v___x_134_, 1, v___x_133_);
v___x_135_ = 0;
v___x_136_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_136_, 0, v___x_134_);
lean_ctor_set_uint8(v___x_136_, sizeof(void*)*1, v___x_135_);
v___x_137_ = l_Repr_addAppParen(v___x_136_, v_prec_123_);
return v___x_137_;
}
v___jp_138_:
{
lean_object* v___x_140_; lean_object* v___x_141_; uint8_t v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; 
v___x_140_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__5));
lean_inc(v___y_139_);
v___x_141_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_141_, 0, v___y_139_);
lean_ctor_set(v___x_141_, 1, v___x_140_);
v___x_142_ = 0;
v___x_143_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_143_, 0, v___x_141_);
lean_ctor_set_uint8(v___x_143_, sizeof(void*)*1, v___x_142_);
v___x_144_ = l_Repr_addAppParen(v___x_143_, v_prec_123_);
return v___x_144_;
}
v___jp_145_:
{
lean_object* v___x_147_; lean_object* v___x_148_; uint8_t v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; 
v___x_147_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__7));
lean_inc(v___y_146_);
v___x_148_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_148_, 0, v___y_146_);
lean_ctor_set(v___x_148_, 1, v___x_147_);
v___x_149_ = 0;
v___x_150_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_150_, 0, v___x_148_);
lean_ctor_set_uint8(v___x_150_, sizeof(void*)*1, v___x_149_);
v___x_151_ = l_Repr_addAppParen(v___x_150_, v_prec_123_);
return v___x_151_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___boxed(lean_object* v_x_168_, lean_object* v_prec_169_){
_start:
{
uint8_t v_x_233__boxed_170_; lean_object* v_res_171_; 
v_x_233__boxed_170_ = lean_unbox(v_x_168_);
v_res_171_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr(v_x_233__boxed_170_, v_prec_169_);
lean_dec(v_prec_169_);
return v_res_171_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid_decEq(lean_object* v_x_174_, lean_object* v_x_175_){
_start:
{
lean_object* v_termsAdded_176_; lean_object* v_assertionsAdded_177_; lean_object* v_destructiveOps_178_; lean_object* v_termsAdded_179_; lean_object* v_assertionsAdded_180_; lean_object* v_destructiveOps_181_; uint8_t v___x_182_; 
v_termsAdded_176_ = lean_ctor_get(v_x_174_, 0);
v_assertionsAdded_177_ = lean_ctor_get(v_x_174_, 1);
v_destructiveOps_178_ = lean_ctor_get(v_x_174_, 2);
v_termsAdded_179_ = lean_ctor_get(v_x_175_, 0);
v_assertionsAdded_180_ = lean_ctor_get(v_x_175_, 1);
v_destructiveOps_181_ = lean_ctor_get(v_x_175_, 2);
v___x_182_ = lean_nat_dec_eq(v_termsAdded_176_, v_termsAdded_179_);
if (v___x_182_ == 0)
{
return v___x_182_;
}
else
{
uint8_t v___x_183_; 
v___x_183_ = lean_nat_dec_eq(v_assertionsAdded_177_, v_assertionsAdded_180_);
if (v___x_183_ == 0)
{
return v___x_183_;
}
else
{
uint8_t v___x_184_; 
v___x_184_ = lean_nat_dec_eq(v_destructiveOps_178_, v_destructiveOps_181_);
return v___x_184_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid_decEq___boxed(lean_object* v_x_185_, lean_object* v_x_186_){
_start:
{
uint8_t v_res_187_; lean_object* v_r_188_; 
v_res_187_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid_decEq(v_x_185_, v_x_186_);
lean_dec_ref(v_x_186_);
lean_dec_ref(v_x_185_);
v_r_188_ = lean_box(v_res_187_);
return v_r_188_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid(lean_object* v_x_189_, lean_object* v_x_190_){
_start:
{
uint8_t v___x_191_; 
v___x_191_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid_decEq(v_x_189_, v_x_190_);
return v___x_191_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid___boxed(lean_object* v_x_192_, lean_object* v_x_193_){
_start:
{
uint8_t v_res_194_; lean_object* v_r_195_; 
v_res_194_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqObligationMonoid(v_x_192_, v_x_193_);
lean_dec_ref(v_x_193_);
lean_dec_ref(v_x_192_);
v_r_195_ = lean_box(v_res_194_);
return v_r_195_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_209_; lean_object* v___x_210_; 
v___x_209_ = lean_unsigned_to_nat(14u);
v___x_210_ = lean_nat_to_int(v___x_209_);
return v___x_210_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__12(void){
_start:
{
lean_object* v___x_217_; lean_object* v___x_218_; 
v___x_217_ = lean_unsigned_to_nat(19u);
v___x_218_ = lean_nat_to_int(v___x_217_);
return v___x_218_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_222_; lean_object* v___x_223_; 
v___x_222_ = lean_unsigned_to_nat(18u);
v___x_223_ = lean_nat_to_int(v___x_222_);
return v___x_223_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_225_; lean_object* v___x_226_; 
v___x_225_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__0));
v___x_226_ = lean_string_length(v___x_225_);
return v___x_226_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18(void){
_start:
{
lean_object* v___x_227_; lean_object* v___x_228_; 
v___x_227_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__17, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__17);
v___x_228_ = lean_nat_to_int(v___x_227_);
return v___x_228_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg(lean_object* v_x_233_){
_start:
{
lean_object* v_termsAdded_234_; lean_object* v_assertionsAdded_235_; lean_object* v_destructiveOps_236_; lean_object* v___x_237_; lean_object* v___x_238_; lean_object* v___x_239_; lean_object* v___x_240_; lean_object* v___x_241_; lean_object* v___x_242_; uint8_t v___x_243_; lean_object* v___x_244_; lean_object* v___x_245_; lean_object* v___x_246_; lean_object* v___x_247_; lean_object* v___x_248_; lean_object* v___x_249_; lean_object* v___x_250_; lean_object* v___x_251_; lean_object* v___x_252_; lean_object* v___x_253_; lean_object* v___x_254_; lean_object* v___x_255_; lean_object* v___x_256_; lean_object* v___x_257_; lean_object* v___x_258_; lean_object* v___x_259_; lean_object* v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; lean_object* v___x_263_; lean_object* v___x_264_; lean_object* v___x_265_; lean_object* v___x_266_; lean_object* v___x_267_; lean_object* v___x_268_; lean_object* v___x_269_; lean_object* v___x_270_; lean_object* v___x_271_; lean_object* v___x_272_; lean_object* v___x_273_; lean_object* v___x_274_; lean_object* v___x_275_; lean_object* v___x_276_; 
v_termsAdded_234_ = lean_ctor_get(v_x_233_, 0);
lean_inc(v_termsAdded_234_);
v_assertionsAdded_235_ = lean_ctor_get(v_x_233_, 1);
lean_inc(v_assertionsAdded_235_);
v_destructiveOps_236_ = lean_ctor_get(v_x_233_, 2);
lean_inc(v_destructiveOps_236_);
lean_dec_ref(v_x_233_);
v___x_237_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5));
v___x_238_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__6));
v___x_239_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__7);
v___x_240_ = l_Nat_reprFast(v_termsAdded_234_);
v___x_241_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_241_, 0, v___x_240_);
v___x_242_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_242_, 0, v___x_239_);
lean_ctor_set(v___x_242_, 1, v___x_241_);
v___x_243_ = 0;
v___x_244_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_244_, 0, v___x_242_);
lean_ctor_set_uint8(v___x_244_, sizeof(void*)*1, v___x_243_);
v___x_245_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_245_, 0, v___x_238_);
lean_ctor_set(v___x_245_, 1, v___x_244_);
v___x_246_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__9));
v___x_247_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_247_, 0, v___x_245_);
lean_ctor_set(v___x_247_, 1, v___x_246_);
v___x_248_ = lean_box(1);
v___x_249_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_249_, 0, v___x_247_);
lean_ctor_set(v___x_249_, 1, v___x_248_);
v___x_250_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__11));
v___x_251_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_251_, 0, v___x_249_);
lean_ctor_set(v___x_251_, 1, v___x_250_);
v___x_252_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_252_, 0, v___x_251_);
lean_ctor_set(v___x_252_, 1, v___x_237_);
v___x_253_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__12, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__12_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__12);
v___x_254_ = l_Nat_reprFast(v_assertionsAdded_235_);
v___x_255_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_255_, 0, v___x_254_);
v___x_256_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_256_, 0, v___x_253_);
lean_ctor_set(v___x_256_, 1, v___x_255_);
v___x_257_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_257_, 0, v___x_256_);
lean_ctor_set_uint8(v___x_257_, sizeof(void*)*1, v___x_243_);
v___x_258_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_258_, 0, v___x_252_);
lean_ctor_set(v___x_258_, 1, v___x_257_);
v___x_259_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_259_, 0, v___x_258_);
lean_ctor_set(v___x_259_, 1, v___x_246_);
v___x_260_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_260_, 0, v___x_259_);
lean_ctor_set(v___x_260_, 1, v___x_248_);
v___x_261_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__14));
v___x_262_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_262_, 0, v___x_260_);
lean_ctor_set(v___x_262_, 1, v___x_261_);
v___x_263_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_263_, 0, v___x_262_);
lean_ctor_set(v___x_263_, 1, v___x_237_);
v___x_264_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__15, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__15);
v___x_265_ = l_Nat_reprFast(v_destructiveOps_236_);
v___x_266_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_266_, 0, v___x_265_);
v___x_267_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_267_, 0, v___x_264_);
lean_ctor_set(v___x_267_, 1, v___x_266_);
v___x_268_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_268_, 0, v___x_267_);
lean_ctor_set_uint8(v___x_268_, sizeof(void*)*1, v___x_243_);
v___x_269_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_269_, 0, v___x_263_);
lean_ctor_set(v___x_269_, 1, v___x_268_);
v___x_270_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18);
v___x_271_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19));
v___x_272_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_272_, 0, v___x_271_);
lean_ctor_set(v___x_272_, 1, v___x_269_);
v___x_273_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20));
v___x_274_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_274_, 0, v___x_272_);
lean_ctor_set(v___x_274_, 1, v___x_273_);
v___x_275_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_275_, 0, v___x_270_);
lean_ctor_set(v___x_275_, 1, v___x_274_);
v___x_276_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_276_, 0, v___x_275_);
lean_ctor_set_uint8(v___x_276_, sizeof(void*)*1, v___x_243_);
return v___x_276_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr(lean_object* v_x_277_, lean_object* v_prec_278_){
_start:
{
lean_object* v___x_279_; 
v___x_279_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg(v_x_277_);
return v___x_279_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___boxed(lean_object* v_x_280_, lean_object* v_prec_281_){
_start:
{
lean_object* v_res_282_; 
v_res_282_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr(v_x_280_, v_prec_281_);
lean_dec(v_prec_281_);
return v_res_282_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_add(lean_object* v_x_288_, lean_object* v_y_289_){
_start:
{
lean_object* v_termsAdded_290_; lean_object* v_assertionsAdded_291_; lean_object* v_destructiveOps_292_; lean_object* v_termsAdded_293_; lean_object* v_assertionsAdded_294_; lean_object* v_destructiveOps_295_; lean_object* v___x_297_; uint8_t v_isShared_298_; uint8_t v_isSharedCheck_305_; 
v_termsAdded_290_ = lean_ctor_get(v_x_288_, 0);
v_assertionsAdded_291_ = lean_ctor_get(v_x_288_, 1);
v_destructiveOps_292_ = lean_ctor_get(v_x_288_, 2);
v_termsAdded_293_ = lean_ctor_get(v_y_289_, 0);
v_assertionsAdded_294_ = lean_ctor_get(v_y_289_, 1);
v_destructiveOps_295_ = lean_ctor_get(v_y_289_, 2);
v_isSharedCheck_305_ = !lean_is_exclusive(v_y_289_);
if (v_isSharedCheck_305_ == 0)
{
v___x_297_ = v_y_289_;
v_isShared_298_ = v_isSharedCheck_305_;
goto v_resetjp_296_;
}
else
{
lean_inc(v_destructiveOps_295_);
lean_inc(v_assertionsAdded_294_);
lean_inc(v_termsAdded_293_);
lean_dec(v_y_289_);
v___x_297_ = lean_box(0);
v_isShared_298_ = v_isSharedCheck_305_;
goto v_resetjp_296_;
}
v_resetjp_296_:
{
lean_object* v___x_299_; lean_object* v___x_300_; lean_object* v___x_301_; lean_object* v___x_303_; 
v___x_299_ = lean_nat_add(v_termsAdded_290_, v_termsAdded_293_);
lean_dec(v_termsAdded_293_);
v___x_300_ = lean_nat_add(v_assertionsAdded_291_, v_assertionsAdded_294_);
lean_dec(v_assertionsAdded_294_);
v___x_301_ = lean_nat_add(v_destructiveOps_292_, v_destructiveOps_295_);
lean_dec(v_destructiveOps_295_);
if (v_isShared_298_ == 0)
{
lean_ctor_set(v___x_297_, 2, v___x_301_);
lean_ctor_set(v___x_297_, 1, v___x_300_);
lean_ctor_set(v___x_297_, 0, v___x_299_);
v___x_303_ = v___x_297_;
goto v_reusejp_302_;
}
else
{
lean_object* v_reuseFailAlloc_304_; 
v_reuseFailAlloc_304_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_304_, 0, v___x_299_);
lean_ctor_set(v_reuseFailAlloc_304_, 1, v___x_300_);
lean_ctor_set(v_reuseFailAlloc_304_, 2, v___x_301_);
v___x_303_ = v_reuseFailAlloc_304_;
goto v_reusejp_302_;
}
v_reusejp_302_:
{
return v___x_303_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_add___boxed(lean_object* v_x_306_, lean_object* v_y_307_){
_start:
{
lean_object* v_res_308_; 
v_res_308_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_add(v_x_306_, v_y_307_);
lean_dec_ref(v_x_306_);
return v_res_308_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_totalCost(lean_object* v_x_309_){
_start:
{
lean_object* v_termsAdded_310_; lean_object* v_assertionsAdded_311_; lean_object* v_destructiveOps_312_; lean_object* v___x_313_; lean_object* v___x_314_; 
v_termsAdded_310_ = lean_ctor_get(v_x_309_, 0);
v_assertionsAdded_311_ = lean_ctor_get(v_x_309_, 1);
v_destructiveOps_312_ = lean_ctor_get(v_x_309_, 2);
v___x_313_ = lean_nat_add(v_termsAdded_310_, v_assertionsAdded_311_);
v___x_314_ = lean_nat_add(v___x_313_, v_destructiveOps_312_);
lean_dec(v___x_313_);
return v___x_314_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_totalCost___boxed(lean_object* v_x_315_){
_start:
{
lean_object* v_res_316_; 
v_res_316_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_totalCost(v_x_315_);
lean_dec_ref(v_x_315_);
return v_res_316_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation(uint8_t v_x_326_){
_start:
{
switch(v_x_326_)
{
case 0:
{
lean_object* v___x_327_; 
v___x_327_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__0));
return v___x_327_;
}
case 1:
{
lean_object* v___x_328_; 
v___x_328_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__1));
return v___x_328_;
}
default: 
{
lean_object* v___x_329_; 
v___x_329_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___closed__2));
return v___x_329_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation___boxed(lean_object* v_x_330_){
_start:
{
uint8_t v_x_83__boxed_331_; lean_object* v_res_332_; 
v_x_83__boxed_331_ = lean_unbox(v_x_330_);
v_res_332_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation(v_x_83__boxed_331_);
return v_res_332_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceObligation(lean_object* v_x_333_){
_start:
{
if (lean_obj_tag(v_x_333_) == 0)
{
lean_object* v___x_334_; 
v___x_334_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_zero));
return v___x_334_;
}
else
{
lean_object* v_head_335_; lean_object* v_tail_336_; uint8_t v___x_337_; lean_object* v___x_338_; lean_object* v___x_339_; lean_object* v___x_340_; 
v_head_335_ = lean_ctor_get(v_x_333_, 0);
v_tail_336_ = lean_ctor_get(v_x_333_, 1);
v___x_337_ = lean_unbox(v_head_335_);
v___x_338_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_eventObligation(v___x_337_);
v___x_339_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceObligation(v_tail_336_);
v___x_340_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_ObligationMonoid_add(v___x_338_, v___x_339_);
lean_dec_ref(v___x_338_);
return v___x_340_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceObligation___boxed(lean_object* v_x_341_){
_start:
{
lean_object* v_res_342_; 
v_res_342_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceObligation(v_x_341_);
lean_dec(v_x_341_);
return v_res_342_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_traceObligation_match__1_splitter___redArg(lean_object* v_x_343_, lean_object* v_h__1_344_, lean_object* v_h__2_345_){
_start:
{
if (lean_obj_tag(v_x_343_) == 0)
{
lean_object* v___x_346_; lean_object* v___x_347_; 
lean_dec(v_h__2_345_);
v___x_346_ = lean_box(0);
v___x_347_ = lean_apply_1(v_h__1_344_, v___x_346_);
return v___x_347_;
}
else
{
lean_object* v_head_348_; lean_object* v_tail_349_; lean_object* v___x_350_; 
lean_dec(v_h__1_344_);
v_head_348_ = lean_ctor_get(v_x_343_, 0);
lean_inc(v_head_348_);
v_tail_349_ = lean_ctor_get(v_x_343_, 1);
lean_inc(v_tail_349_);
lean_dec_ref_known(v_x_343_, 2);
v___x_350_ = lean_apply_2(v_h__2_345_, v_head_348_, v_tail_349_);
return v___x_350_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_traceObligation_match__1_splitter(lean_object* v_motive_351_, lean_object* v_x_352_, lean_object* v_h__1_353_, lean_object* v_h__2_354_){
_start:
{
if (lean_obj_tag(v_x_352_) == 0)
{
lean_object* v___x_355_; lean_object* v___x_356_; 
lean_dec(v_h__2_354_);
v___x_355_ = lean_box(0);
v___x_356_ = lean_apply_1(v_h__1_353_, v___x_355_);
return v___x_356_;
}
else
{
lean_object* v_head_357_; lean_object* v_tail_358_; lean_object* v___x_359_; 
lean_dec(v_h__1_353_);
v_head_357_ = lean_ctor_get(v_x_352_, 0);
lean_inc(v_head_357_);
v_tail_358_ = lean_ctor_get(v_x_352_, 1);
lean_inc(v_tail_358_);
lean_dec_ref_known(v_x_352_, 2);
v___x_359_ = lean_apply_2(v_h__2_354_, v_head_357_, v_tail_358_);
return v___x_359_;
}
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___redArg(lean_object* v_w_360_, lean_object* v_u_361_, lean_object* v_v_362_){
_start:
{
lean_object* v___x_363_; uint8_t v___x_364_; 
lean_inc_ref(v_w_360_);
lean_inc(v_v_362_);
lean_inc(v_u_361_);
v___x_363_ = lean_apply_2(v_w_360_, v_u_361_, v_v_362_);
v___x_364_ = lean_unbox(v___x_363_);
if (v___x_364_ == 0)
{
lean_object* v___x_365_; uint8_t v___x_366_; 
v___x_365_ = lean_apply_2(v_w_360_, v_v_362_, v_u_361_);
v___x_366_ = lean_unbox(v___x_365_);
return v___x_366_;
}
else
{
uint8_t v___x_367_; 
lean_dec(v_v_362_);
lean_dec(v_u_361_);
lean_dec_ref(v_w_360_);
v___x_367_ = lean_unbox(v___x_363_);
return v___x_367_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___redArg___boxed(lean_object* v_w_368_, lean_object* v_u_369_, lean_object* v_v_370_){
_start:
{
uint8_t v_res_371_; lean_object* v_r_372_; 
v_res_371_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___redArg(v_w_368_, v_u_369_, v_v_370_);
v_r_372_ = lean_box(v_res_371_);
return v_r_372_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect(lean_object* v_n_373_, lean_object* v_w_374_, lean_object* v_u_375_, lean_object* v_v_376_){
_start:
{
uint8_t v___x_377_; 
v___x_377_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___redArg(v_w_374_, v_u_375_, v_v_376_);
return v___x_377_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect___boxed(lean_object* v_n_378_, lean_object* v_w_379_, lean_object* v_u_380_, lean_object* v_v_381_){
_start:
{
uint8_t v_res_382_; lean_object* v_r_383_; 
v_res_382_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_wdpPairDefect(v_n_378_, v_w_379_, v_u_380_, v_v_381_);
lean_dec(v_n_378_);
v_r_383_ = lean_box(v_res_382_);
return v_r_383_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_edgeResidualL1(lean_object* v_x_384_){
_start:
{
if (lean_obj_tag(v_x_384_) == 0)
{
lean_object* v___x_385_; 
v___x_385_ = lean_unsigned_to_nat(0u);
return v___x_385_;
}
else
{
lean_object* v_head_386_; lean_object* v_tail_387_; lean_object* v___x_388_; lean_object* v___x_389_; 
v_head_386_ = lean_ctor_get(v_x_384_, 0);
v_tail_387_ = lean_ctor_get(v_x_384_, 1);
v___x_388_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_edgeResidualL1(v_tail_387_);
v___x_389_ = lean_nat_add(v_head_386_, v___x_388_);
lean_dec(v___x_388_);
return v___x_389_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_edgeResidualL1___boxed(lean_object* v_x_390_){
_start:
{
lean_object* v_res_391_; 
v_res_391_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_edgeResidualL1(v_x_390_);
lean_dec(v_x_390_);
return v_res_391_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_edgeResidualL1_match__1_splitter___redArg(lean_object* v_x_392_, lean_object* v_h__1_393_, lean_object* v_h__2_394_){
_start:
{
if (lean_obj_tag(v_x_392_) == 0)
{
lean_object* v___x_395_; lean_object* v___x_396_; 
lean_dec(v_h__2_394_);
v___x_395_ = lean_box(0);
v___x_396_ = lean_apply_1(v_h__1_393_, v___x_395_);
return v___x_396_;
}
else
{
lean_object* v_head_397_; lean_object* v_tail_398_; lean_object* v___x_399_; 
lean_dec(v_h__1_393_);
v_head_397_ = lean_ctor_get(v_x_392_, 0);
lean_inc(v_head_397_);
v_tail_398_ = lean_ctor_get(v_x_392_, 1);
lean_inc(v_tail_398_);
lean_dec_ref_known(v_x_392_, 2);
v___x_399_ = lean_apply_2(v_h__2_394_, v_head_397_, v_tail_398_);
return v___x_399_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_edgeResidualL1_match__1_splitter(lean_object* v_motive_400_, lean_object* v_x_401_, lean_object* v_h__1_402_, lean_object* v_h__2_403_){
_start:
{
if (lean_obj_tag(v_x_401_) == 0)
{
lean_object* v___x_404_; lean_object* v___x_405_; 
lean_dec(v_h__2_403_);
v___x_404_ = lean_box(0);
v___x_405_ = lean_apply_1(v_h__1_402_, v___x_404_);
return v___x_405_;
}
else
{
lean_object* v_head_406_; lean_object* v_tail_407_; lean_object* v___x_408_; 
lean_dec(v_h__1_402_);
v_head_406_ = lean_ctor_get(v_x_401_, 0);
lean_inc(v_head_406_);
v_tail_407_ = lean_ctor_get(v_x_401_, 1);
lean_inc(v_tail_407_);
lean_dec_ref_known(v_x_401_, 2);
v___x_408_ = lean_apply_2(v_h__2_403_, v_head_406_, v_tail_407_);
return v___x_408_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_attachTwoSimplex(lean_object* v_K_409_, lean_object* v_tri_410_){
_start:
{
lean_object* v_edgeResiduals_411_; lean_object* v_triangles_412_; lean_object* v___x_414_; uint8_t v_isShared_415_; uint8_t v_isSharedCheck_420_; 
v_edgeResiduals_411_ = lean_ctor_get(v_K_409_, 0);
v_triangles_412_ = lean_ctor_get(v_K_409_, 1);
v_isSharedCheck_420_ = !lean_is_exclusive(v_K_409_);
if (v_isSharedCheck_420_ == 0)
{
v___x_414_ = v_K_409_;
v_isShared_415_ = v_isSharedCheck_420_;
goto v_resetjp_413_;
}
else
{
lean_inc(v_triangles_412_);
lean_inc(v_edgeResiduals_411_);
lean_dec(v_K_409_);
v___x_414_ = lean_box(0);
v_isShared_415_ = v_isSharedCheck_420_;
goto v_resetjp_413_;
}
v_resetjp_413_:
{
lean_object* v___x_416_; lean_object* v___x_418_; 
v___x_416_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_416_, 0, v_tri_410_);
lean_ctor_set(v___x_416_, 1, v_triangles_412_);
if (v_isShared_415_ == 0)
{
lean_ctor_set(v___x_414_, 1, v___x_416_);
v___x_418_ = v___x_414_;
goto v_reusejp_417_;
}
else
{
lean_object* v_reuseFailAlloc_419_; 
v_reuseFailAlloc_419_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_419_, 0, v_edgeResiduals_411_);
lean_ctor_set(v_reuseFailAlloc_419_, 1, v___x_416_);
v___x_418_ = v_reuseFailAlloc_419_;
goto v_reusejp_417_;
}
v_reusejp_417_:
{
return v___x_418_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerOne(lean_object* v_x_421_){
_start:
{
lean_object* v_zero_422_; uint8_t v_isZero_423_; 
v_zero_422_ = lean_unsigned_to_nat(0u);
v_isZero_423_ = lean_nat_dec_eq(v_x_421_, v_zero_422_);
if (v_isZero_423_ == 1)
{
lean_object* v___x_424_; 
v___x_424_ = lean_unsigned_to_nat(1u);
return v___x_424_;
}
else
{
lean_object* v_one_425_; lean_object* v_n_426_; uint8_t v_isZero_427_; 
v_one_425_ = lean_unsigned_to_nat(1u);
v_n_426_ = lean_nat_sub(v_x_421_, v_one_425_);
v_isZero_427_ = lean_nat_dec_eq(v_n_426_, v_zero_422_);
if (v_isZero_427_ == 1)
{
lean_dec(v_n_426_);
return v_zero_422_;
}
else
{
lean_object* v_n_428_; uint8_t v_isZero_429_; 
v_n_428_ = lean_nat_sub(v_n_426_, v_one_425_);
lean_dec(v_n_426_);
v_isZero_429_ = lean_nat_dec_eq(v_n_428_, v_zero_422_);
if (v_isZero_429_ == 1)
{
lean_dec(v_n_428_);
return v_zero_422_;
}
else
{
lean_object* v_n_430_; uint8_t v_isZero_431_; 
v_n_430_ = lean_nat_sub(v_n_428_, v_one_425_);
lean_dec(v_n_428_);
v_isZero_431_ = lean_nat_dec_eq(v_n_430_, v_zero_422_);
lean_dec(v_n_430_);
return v_zero_422_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerOne___boxed(lean_object* v_x_432_){
_start:
{
lean_object* v_res_433_; 
v_res_433_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerOne(v_x_432_);
lean_dec(v_x_432_);
return v_res_433_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerTwo(lean_object* v_x_434_){
_start:
{
lean_object* v_zero_435_; uint8_t v_isZero_436_; 
v_zero_435_ = lean_unsigned_to_nat(0u);
v_isZero_436_ = lean_nat_dec_eq(v_x_434_, v_zero_435_);
if (v_isZero_436_ == 1)
{
return v_zero_435_;
}
else
{
lean_object* v_one_437_; lean_object* v_n_438_; uint8_t v_isZero_439_; 
v_one_437_ = lean_unsigned_to_nat(1u);
v_n_438_ = lean_nat_sub(v_x_434_, v_one_437_);
v_isZero_439_ = lean_nat_dec_eq(v_n_438_, v_zero_435_);
if (v_isZero_439_ == 1)
{
lean_dec(v_n_438_);
return v_one_437_;
}
else
{
lean_object* v_n_440_; uint8_t v_isZero_441_; 
v_n_440_ = lean_nat_sub(v_n_438_, v_one_437_);
lean_dec(v_n_438_);
v_isZero_441_ = lean_nat_dec_eq(v_n_440_, v_zero_435_);
if (v_isZero_441_ == 1)
{
lean_dec(v_n_440_);
return v_zero_435_;
}
else
{
lean_object* v_n_442_; uint8_t v_isZero_443_; 
v_n_442_ = lean_nat_sub(v_n_440_, v_one_437_);
lean_dec(v_n_440_);
v_isZero_443_ = lean_nat_dec_eq(v_n_442_, v_zero_435_);
lean_dec(v_n_442_);
return v_zero_435_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerTwo___boxed(lean_object* v_x_444_){
_start:
{
lean_object* v_res_445_; 
v_res_445_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4MinimizerTwo(v_x_444_);
lean_dec(v_x_444_);
return v_res_445_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_sqDiffSum3(lean_object* v_w0_446_, lean_object* v_w1_447_, lean_object* v_w2_448_){
_start:
{
lean_object* v___x_449_; lean_object* v___x_450_; lean_object* v___x_451_; lean_object* v___x_452_; lean_object* v___x_453_; lean_object* v___x_454_; lean_object* v___x_455_; lean_object* v___x_456_; 
v___x_449_ = lean_int_sub(v_w0_446_, v_w1_447_);
v___x_450_ = lean_int_mul(v___x_449_, v___x_449_);
lean_dec(v___x_449_);
v___x_451_ = lean_int_sub(v_w1_447_, v_w2_448_);
v___x_452_ = lean_int_mul(v___x_451_, v___x_451_);
lean_dec(v___x_451_);
v___x_453_ = lean_int_add(v___x_450_, v___x_452_);
lean_dec(v___x_452_);
lean_dec(v___x_450_);
v___x_454_ = lean_int_sub(v_w2_448_, v_w0_446_);
v___x_455_ = lean_int_mul(v___x_454_, v___x_454_);
lean_dec(v___x_454_);
v___x_456_ = lean_int_add(v___x_453_, v___x_455_);
lean_dec(v___x_455_);
lean_dec(v___x_453_);
return v___x_456_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_sqDiffSum3___boxed(lean_object* v_w0_457_, lean_object* v_w1_458_, lean_object* v_w2_459_){
_start:
{
lean_object* v_res_460_; 
v_res_460_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_sqDiffSum3(v_w0_457_, v_w1_458_, v_w2_459_);
lean_dec(v_w2_459_);
lean_dec(v_w1_458_);
lean_dec(v_w0_457_);
return v_res_460_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagExpectation3(lean_object* v_o0_461_, lean_object* v_o1_462_, lean_object* v_o2_463_, lean_object* v_w0_464_, lean_object* v_w1_465_, lean_object* v_w2_466_){
_start:
{
lean_object* v___x_467_; lean_object* v___x_468_; lean_object* v___x_469_; lean_object* v___x_470_; lean_object* v___x_471_; 
v___x_467_ = lean_nat_mul(v_o0_461_, v_w0_464_);
v___x_468_ = lean_nat_mul(v_o1_462_, v_w1_465_);
v___x_469_ = lean_nat_add(v___x_467_, v___x_468_);
lean_dec(v___x_468_);
lean_dec(v___x_467_);
v___x_470_ = lean_nat_mul(v_o2_463_, v_w2_466_);
v___x_471_ = lean_nat_add(v___x_469_, v___x_470_);
lean_dec(v___x_470_);
lean_dec(v___x_469_);
return v___x_471_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagExpectation3___boxed(lean_object* v_o0_472_, lean_object* v_o1_473_, lean_object* v_o2_474_, lean_object* v_w0_475_, lean_object* v_w1_476_, lean_object* v_w2_477_){
_start:
{
lean_object* v_res_478_; 
v_res_478_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagExpectation3(v_o0_472_, v_o1_473_, v_o2_474_, v_w0_475_, v_w1_476_, v_w2_477_);
lean_dec(v_w2_477_);
lean_dec(v_w1_476_);
lean_dec(v_w0_475_);
lean_dec(v_o2_474_);
lean_dec(v_o1_473_);
lean_dec(v_o0_472_);
return v_res_478_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityDiag3(lean_object* v_w0_479_, lean_object* v_w1_480_, lean_object* v_w2_481_){
_start:
{
lean_object* v___x_482_; lean_object* v___x_483_; lean_object* v___x_484_; lean_object* v___x_485_; lean_object* v___x_486_; 
v___x_482_ = lean_nat_mul(v_w0_479_, v_w0_479_);
v___x_483_ = lean_nat_mul(v_w1_480_, v_w1_480_);
v___x_484_ = lean_nat_add(v___x_482_, v___x_483_);
lean_dec(v___x_483_);
lean_dec(v___x_482_);
v___x_485_ = lean_nat_mul(v_w2_481_, v_w2_481_);
v___x_486_ = lean_nat_add(v___x_484_, v___x_485_);
lean_dec(v___x_485_);
lean_dec(v___x_484_);
return v___x_486_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityDiag3___boxed(lean_object* v_w0_487_, lean_object* v_w1_488_, lean_object* v_w2_489_){
_start:
{
lean_object* v_res_490_; 
v_res_490_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityDiag3(v_w0_487_, v_w1_488_, v_w2_489_);
lean_dec(v_w2_489_);
lean_dec(v_w1_488_);
lean_dec(v_w0_487_);
return v_res_490_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityRankOneExpanded3(lean_object* v_w0_491_, lean_object* v_w1_492_, lean_object* v_w2_493_){
_start:
{
lean_object* v___x_494_; lean_object* v___x_495_; lean_object* v___x_496_; lean_object* v___x_497_; lean_object* v___x_498_; lean_object* v___x_499_; lean_object* v___x_500_; lean_object* v___x_501_; lean_object* v___x_502_; 
v___x_494_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityDiag3(v_w0_491_, v_w1_492_, v_w2_493_);
v___x_495_ = lean_unsigned_to_nat(2u);
v___x_496_ = lean_nat_mul(v_w0_491_, v_w1_492_);
v___x_497_ = lean_nat_mul(v_w1_492_, v_w2_493_);
v___x_498_ = lean_nat_add(v___x_496_, v___x_497_);
lean_dec(v___x_497_);
lean_dec(v___x_496_);
v___x_499_ = lean_nat_mul(v_w2_493_, v_w0_491_);
v___x_500_ = lean_nat_add(v___x_498_, v___x_499_);
lean_dec(v___x_499_);
lean_dec(v___x_498_);
v___x_501_ = lean_nat_mul(v___x_495_, v___x_500_);
lean_dec(v___x_500_);
v___x_502_ = lean_nat_add(v___x_494_, v___x_501_);
lean_dec(v___x_501_);
lean_dec(v___x_494_);
return v___x_502_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityRankOneExpanded3___boxed(lean_object* v_w0_503_, lean_object* v_w1_504_, lean_object* v_w2_505_){
_start:
{
lean_object* v_res_506_; 
v_res_506_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_purityRankOneExpanded3(v_w0_503_, v_w1_504_, v_w2_505_);
lean_dec(v_w2_505_);
lean_dec(v_w1_504_);
lean_dec(v_w0_503_);
return v_res_506_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_plusMinusExpectation(lean_object* v_d0_507_, lean_object* v_d1_508_, lean_object* v_c_509_, lean_object* v_sign_510_){
_start:
{
lean_object* v___x_511_; lean_object* v___x_512_; lean_object* v___x_513_; lean_object* v___x_514_; lean_object* v___x_515_; 
v___x_511_ = lean_int_add(v_d0_507_, v_d1_508_);
v___x_512_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___x_513_ = lean_int_mul(v___x_512_, v_sign_510_);
v___x_514_ = lean_int_mul(v___x_513_, v_c_509_);
lean_dec(v___x_513_);
v___x_515_ = lean_int_add(v___x_511_, v___x_514_);
lean_dec(v___x_514_);
lean_dec(v___x_511_);
return v___x_515_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_plusMinusExpectation___boxed(lean_object* v_d0_516_, lean_object* v_d1_517_, lean_object* v_c_518_, lean_object* v_sign_519_){
_start:
{
lean_object* v_res_520_; 
v_res_520_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_plusMinusExpectation(v_d0_516_, v_d1_517_, v_c_518_, v_sign_519_);
lean_dec(v_sign_519_);
lean_dec(v_c_518_);
lean_dec(v_d1_517_);
lean_dec(v_d0_516_);
return v_res_520_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int_decEq(lean_object* v_x_521_, lean_object* v_x_522_){
_start:
{
lean_object* v_m00_523_; lean_object* v_m01_524_; lean_object* v_m10_525_; lean_object* v_m11_526_; lean_object* v_m00_527_; lean_object* v_m01_528_; lean_object* v_m10_529_; lean_object* v_m11_530_; uint8_t v___x_531_; 
v_m00_523_ = lean_ctor_get(v_x_521_, 0);
v_m01_524_ = lean_ctor_get(v_x_521_, 1);
v_m10_525_ = lean_ctor_get(v_x_521_, 2);
v_m11_526_ = lean_ctor_get(v_x_521_, 3);
v_m00_527_ = lean_ctor_get(v_x_522_, 0);
v_m01_528_ = lean_ctor_get(v_x_522_, 1);
v_m10_529_ = lean_ctor_get(v_x_522_, 2);
v_m11_530_ = lean_ctor_get(v_x_522_, 3);
v___x_531_ = lean_int_dec_eq(v_m00_523_, v_m00_527_);
if (v___x_531_ == 0)
{
return v___x_531_;
}
else
{
uint8_t v___x_532_; 
v___x_532_ = lean_int_dec_eq(v_m01_524_, v_m01_528_);
if (v___x_532_ == 0)
{
return v___x_532_;
}
else
{
uint8_t v___x_533_; 
v___x_533_ = lean_int_dec_eq(v_m10_525_, v_m10_529_);
if (v___x_533_ == 0)
{
return v___x_533_;
}
else
{
uint8_t v___x_534_; 
v___x_534_ = lean_int_dec_eq(v_m11_526_, v_m11_530_);
return v___x_534_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int_decEq___boxed(lean_object* v_x_535_, lean_object* v_x_536_){
_start:
{
uint8_t v_res_537_; lean_object* v_r_538_; 
v_res_537_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int_decEq(v_x_535_, v_x_536_);
lean_dec_ref(v_x_536_);
lean_dec_ref(v_x_535_);
v_r_538_ = lean_box(v_res_537_);
return v_r_538_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int(lean_object* v_x_539_, lean_object* v_x_540_){
_start:
{
uint8_t v___x_541_; 
v___x_541_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int_decEq(v_x_539_, v_x_540_);
return v___x_541_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int___boxed(lean_object* v_x_542_, lean_object* v_x_543_){
_start:
{
uint8_t v_res_544_; lean_object* v_r_545_; 
v_res_544_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqMat2Int(v_x_542_, v_x_543_);
lean_dec_ref(v_x_543_);
lean_dec_ref(v_x_542_);
v_r_545_ = lean_box(v_res_544_);
return v_r_545_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_555_; lean_object* v___x_556_; 
v___x_555_ = lean_unsigned_to_nat(7u);
v___x_556_ = lean_nat_to_int(v___x_555_);
return v___x_556_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_560_; lean_object* v___x_561_; 
v___x_560_ = lean_unsigned_to_nat(0u);
v___x_561_ = lean_nat_to_int(v___x_560_);
return v___x_561_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg(lean_object* v_x_568_){
_start:
{
lean_object* v_m00_569_; lean_object* v_m01_570_; lean_object* v_m10_571_; lean_object* v_m11_572_; lean_object* v___x_573_; lean_object* v___x_574_; lean_object* v___x_575_; lean_object* v___y_577_; uint8_t v___y_578_; lean_object* v___y_579_; lean_object* v___y_591_; lean_object* v___y_592_; lean_object* v___y_593_; uint8_t v___y_594_; lean_object* v___y_595_; lean_object* v___y_613_; lean_object* v___y_614_; lean_object* v___y_615_; uint8_t v___y_616_; lean_object* v___y_617_; lean_object* v___y_635_; lean_object* v___x_655_; lean_object* v___x_656_; uint8_t v___x_657_; 
v_m00_569_ = lean_ctor_get(v_x_568_, 0);
v_m01_570_ = lean_ctor_get(v_x_568_, 1);
v_m10_571_ = lean_ctor_get(v_x_568_, 2);
v_m11_572_ = lean_ctor_get(v_x_568_, 3);
v___x_573_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5));
v___x_574_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__3));
v___x_575_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__4, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__4);
v___x_655_ = lean_unsigned_to_nat(0u);
v___x_656_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_657_ = lean_int_dec_lt(v_m00_569_, v___x_656_);
if (v___x_657_ == 0)
{
lean_object* v___x_658_; lean_object* v___x_659_; 
v___x_658_ = l_Int_repr(v_m00_569_);
v___x_659_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_659_, 0, v___x_658_);
v___y_635_ = v___x_659_;
goto v___jp_634_;
}
else
{
lean_object* v___x_660_; lean_object* v___x_661_; lean_object* v___x_662_; 
v___x_660_ = l_Int_repr(v_m00_569_);
v___x_661_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_661_, 0, v___x_660_);
v___x_662_ = l_Repr_addAppParen(v___x_661_, v___x_655_);
v___y_635_ = v___x_662_;
goto v___jp_634_;
}
v___jp_576_:
{
lean_object* v___x_580_; lean_object* v___x_581_; lean_object* v___x_582_; lean_object* v___x_583_; lean_object* v___x_584_; lean_object* v___x_585_; lean_object* v___x_586_; lean_object* v___x_587_; lean_object* v___x_588_; lean_object* v___x_589_; 
v___x_580_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_580_, 0, v___x_575_);
lean_ctor_set(v___x_580_, 1, v___y_579_);
v___x_581_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_581_, 0, v___x_580_);
lean_ctor_set_uint8(v___x_581_, sizeof(void*)*1, v___y_578_);
v___x_582_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_582_, 0, v___y_577_);
lean_ctor_set(v___x_582_, 1, v___x_581_);
v___x_583_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18);
v___x_584_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19));
v___x_585_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_585_, 0, v___x_584_);
lean_ctor_set(v___x_585_, 1, v___x_582_);
v___x_586_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20));
v___x_587_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_587_, 0, v___x_585_);
lean_ctor_set(v___x_587_, 1, v___x_586_);
v___x_588_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_588_, 0, v___x_583_);
lean_ctor_set(v___x_588_, 1, v___x_587_);
v___x_589_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_589_, 0, v___x_588_);
lean_ctor_set_uint8(v___x_589_, sizeof(void*)*1, v___y_578_);
return v___x_589_;
}
v___jp_590_:
{
lean_object* v___x_596_; lean_object* v___x_597_; lean_object* v___x_598_; lean_object* v___x_599_; lean_object* v___x_600_; lean_object* v___x_601_; lean_object* v___x_602_; lean_object* v___x_603_; lean_object* v___x_604_; lean_object* v___x_605_; uint8_t v___x_606_; 
v___x_596_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_596_, 0, v___x_575_);
lean_ctor_set(v___x_596_, 1, v___y_595_);
v___x_597_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_597_, 0, v___x_596_);
lean_ctor_set_uint8(v___x_597_, sizeof(void*)*1, v___y_594_);
v___x_598_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_598_, 0, v___y_591_);
lean_ctor_set(v___x_598_, 1, v___x_597_);
lean_inc(v___y_592_);
v___x_599_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_599_, 0, v___x_598_);
lean_ctor_set(v___x_599_, 1, v___y_592_);
lean_inc(v___y_593_);
v___x_600_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_600_, 0, v___x_599_);
lean_ctor_set(v___x_600_, 1, v___y_593_);
v___x_601_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__6));
v___x_602_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_602_, 0, v___x_600_);
lean_ctor_set(v___x_602_, 1, v___x_601_);
v___x_603_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_603_, 0, v___x_602_);
lean_ctor_set(v___x_603_, 1, v___x_573_);
v___x_604_ = lean_unsigned_to_nat(0u);
v___x_605_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_606_ = lean_int_dec_lt(v_m11_572_, v___x_605_);
if (v___x_606_ == 0)
{
lean_object* v___x_607_; lean_object* v___x_608_; 
v___x_607_ = l_Int_repr(v_m11_572_);
v___x_608_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_608_, 0, v___x_607_);
v___y_577_ = v___x_603_;
v___y_578_ = v___y_594_;
v___y_579_ = v___x_608_;
goto v___jp_576_;
}
else
{
lean_object* v___x_609_; lean_object* v___x_610_; lean_object* v___x_611_; 
v___x_609_ = l_Int_repr(v_m11_572_);
v___x_610_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_610_, 0, v___x_609_);
v___x_611_ = l_Repr_addAppParen(v___x_610_, v___x_604_);
v___y_577_ = v___x_603_;
v___y_578_ = v___y_594_;
v___y_579_ = v___x_611_;
goto v___jp_576_;
}
}
v___jp_612_:
{
lean_object* v___x_618_; lean_object* v___x_619_; lean_object* v___x_620_; lean_object* v___x_621_; lean_object* v___x_622_; lean_object* v___x_623_; lean_object* v___x_624_; lean_object* v___x_625_; lean_object* v___x_626_; lean_object* v___x_627_; uint8_t v___x_628_; 
v___x_618_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_618_, 0, v___x_575_);
lean_ctor_set(v___x_618_, 1, v___y_617_);
v___x_619_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_619_, 0, v___x_618_);
lean_ctor_set_uint8(v___x_619_, sizeof(void*)*1, v___y_616_);
v___x_620_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_620_, 0, v___y_614_);
lean_ctor_set(v___x_620_, 1, v___x_619_);
lean_inc(v___y_613_);
v___x_621_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_621_, 0, v___x_620_);
lean_ctor_set(v___x_621_, 1, v___y_613_);
lean_inc(v___y_615_);
v___x_622_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_622_, 0, v___x_621_);
lean_ctor_set(v___x_622_, 1, v___y_615_);
v___x_623_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__9));
v___x_624_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_624_, 0, v___x_622_);
lean_ctor_set(v___x_624_, 1, v___x_623_);
v___x_625_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_625_, 0, v___x_624_);
lean_ctor_set(v___x_625_, 1, v___x_573_);
v___x_626_ = lean_unsigned_to_nat(0u);
v___x_627_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_628_ = lean_int_dec_lt(v_m10_571_, v___x_627_);
if (v___x_628_ == 0)
{
lean_object* v___x_629_; lean_object* v___x_630_; 
v___x_629_ = l_Int_repr(v_m10_571_);
v___x_630_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_630_, 0, v___x_629_);
v___y_591_ = v___x_625_;
v___y_592_ = v___y_613_;
v___y_593_ = v___y_615_;
v___y_594_ = v___y_616_;
v___y_595_ = v___x_630_;
goto v___jp_590_;
}
else
{
lean_object* v___x_631_; lean_object* v___x_632_; lean_object* v___x_633_; 
v___x_631_ = l_Int_repr(v_m10_571_);
v___x_632_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_632_, 0, v___x_631_);
v___x_633_ = l_Repr_addAppParen(v___x_632_, v___x_626_);
v___y_591_ = v___x_625_;
v___y_592_ = v___y_613_;
v___y_593_ = v___y_615_;
v___y_594_ = v___y_616_;
v___y_595_ = v___x_633_;
goto v___jp_590_;
}
}
v___jp_634_:
{
lean_object* v___x_636_; uint8_t v___x_637_; lean_object* v___x_638_; lean_object* v___x_639_; lean_object* v___x_640_; lean_object* v___x_641_; lean_object* v___x_642_; lean_object* v___x_643_; lean_object* v___x_644_; lean_object* v___x_645_; lean_object* v___x_646_; lean_object* v___x_647_; lean_object* v___x_648_; uint8_t v___x_649_; 
v___x_636_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_636_, 0, v___x_575_);
lean_ctor_set(v___x_636_, 1, v___y_635_);
v___x_637_ = 0;
v___x_638_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_638_, 0, v___x_636_);
lean_ctor_set_uint8(v___x_638_, sizeof(void*)*1, v___x_637_);
v___x_639_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_639_, 0, v___x_574_);
lean_ctor_set(v___x_639_, 1, v___x_638_);
v___x_640_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__9));
v___x_641_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_641_, 0, v___x_639_);
lean_ctor_set(v___x_641_, 1, v___x_640_);
v___x_642_ = lean_box(1);
v___x_643_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_643_, 0, v___x_641_);
lean_ctor_set(v___x_643_, 1, v___x_642_);
v___x_644_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__11));
v___x_645_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_645_, 0, v___x_643_);
lean_ctor_set(v___x_645_, 1, v___x_644_);
v___x_646_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_646_, 0, v___x_645_);
lean_ctor_set(v___x_646_, 1, v___x_573_);
v___x_647_ = lean_unsigned_to_nat(0u);
v___x_648_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_649_ = lean_int_dec_lt(v_m01_570_, v___x_648_);
if (v___x_649_ == 0)
{
lean_object* v___x_650_; lean_object* v___x_651_; 
v___x_650_ = l_Int_repr(v_m01_570_);
v___x_651_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_651_, 0, v___x_650_);
v___y_613_ = v___x_640_;
v___y_614_ = v___x_646_;
v___y_615_ = v___x_642_;
v___y_616_ = v___x_637_;
v___y_617_ = v___x_651_;
goto v___jp_612_;
}
else
{
lean_object* v___x_652_; lean_object* v___x_653_; lean_object* v___x_654_; 
v___x_652_ = l_Int_repr(v_m01_570_);
v___x_653_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_653_, 0, v___x_652_);
v___x_654_ = l_Repr_addAppParen(v___x_653_, v___x_647_);
v___y_613_ = v___x_640_;
v___y_614_ = v___x_646_;
v___y_615_ = v___x_642_;
v___y_616_ = v___x_637_;
v___y_617_ = v___x_654_;
goto v___jp_612_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___boxed(lean_object* v_x_663_){
_start:
{
lean_object* v_res_664_; 
v_res_664_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg(v_x_663_);
lean_dec_ref(v_x_663_);
return v_res_664_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr(lean_object* v_x_665_, lean_object* v_prec_666_){
_start:
{
lean_object* v___x_667_; 
v___x_667_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg(v_x_665_);
return v___x_667_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___boxed(lean_object* v_x_668_, lean_object* v_prec_669_){
_start:
{
lean_object* v_res_670_; 
v_res_670_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr(v_x_668_, v_prec_669_);
lean_dec(v_prec_669_);
lean_dec_ref(v_x_668_);
return v_res_670_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(lean_object* v_A_673_, lean_object* v_B_674_){
_start:
{
lean_object* v_m00_675_; lean_object* v_m01_676_; lean_object* v_m10_677_; lean_object* v_m11_678_; lean_object* v_m00_679_; lean_object* v_m01_680_; lean_object* v_m10_681_; lean_object* v_m11_682_; lean_object* v___x_684_; uint8_t v_isShared_685_; uint8_t v_isSharedCheck_701_; 
v_m00_675_ = lean_ctor_get(v_A_673_, 0);
v_m01_676_ = lean_ctor_get(v_A_673_, 1);
v_m10_677_ = lean_ctor_get(v_A_673_, 2);
v_m11_678_ = lean_ctor_get(v_A_673_, 3);
v_m00_679_ = lean_ctor_get(v_B_674_, 0);
v_m01_680_ = lean_ctor_get(v_B_674_, 1);
v_m10_681_ = lean_ctor_get(v_B_674_, 2);
v_m11_682_ = lean_ctor_get(v_B_674_, 3);
v_isSharedCheck_701_ = !lean_is_exclusive(v_B_674_);
if (v_isSharedCheck_701_ == 0)
{
v___x_684_ = v_B_674_;
v_isShared_685_ = v_isSharedCheck_701_;
goto v_resetjp_683_;
}
else
{
lean_inc(v_m11_682_);
lean_inc(v_m10_681_);
lean_inc(v_m01_680_);
lean_inc(v_m00_679_);
lean_dec(v_B_674_);
v___x_684_ = lean_box(0);
v_isShared_685_ = v_isSharedCheck_701_;
goto v_resetjp_683_;
}
v_resetjp_683_:
{
lean_object* v___x_686_; lean_object* v___x_687_; lean_object* v___x_688_; lean_object* v___x_689_; lean_object* v___x_690_; lean_object* v___x_691_; lean_object* v___x_692_; lean_object* v___x_693_; lean_object* v___x_694_; lean_object* v___x_695_; lean_object* v___x_696_; lean_object* v___x_697_; lean_object* v___x_699_; 
v___x_686_ = lean_int_mul(v_m00_675_, v_m00_679_);
v___x_687_ = lean_int_mul(v_m01_676_, v_m10_681_);
v___x_688_ = lean_int_add(v___x_686_, v___x_687_);
lean_dec(v___x_687_);
lean_dec(v___x_686_);
v___x_689_ = lean_int_mul(v_m00_675_, v_m01_680_);
v___x_690_ = lean_int_mul(v_m01_676_, v_m11_682_);
v___x_691_ = lean_int_add(v___x_689_, v___x_690_);
lean_dec(v___x_690_);
lean_dec(v___x_689_);
v___x_692_ = lean_int_mul(v_m10_677_, v_m00_679_);
lean_dec(v_m00_679_);
v___x_693_ = lean_int_mul(v_m11_678_, v_m10_681_);
lean_dec(v_m10_681_);
v___x_694_ = lean_int_add(v___x_692_, v___x_693_);
lean_dec(v___x_693_);
lean_dec(v___x_692_);
v___x_695_ = lean_int_mul(v_m10_677_, v_m01_680_);
lean_dec(v_m01_680_);
v___x_696_ = lean_int_mul(v_m11_678_, v_m11_682_);
lean_dec(v_m11_682_);
v___x_697_ = lean_int_add(v___x_695_, v___x_696_);
lean_dec(v___x_696_);
lean_dec(v___x_695_);
if (v_isShared_685_ == 0)
{
lean_ctor_set(v___x_684_, 3, v___x_697_);
lean_ctor_set(v___x_684_, 2, v___x_694_);
lean_ctor_set(v___x_684_, 1, v___x_691_);
lean_ctor_set(v___x_684_, 0, v___x_688_);
v___x_699_ = v___x_684_;
goto v_reusejp_698_;
}
else
{
lean_object* v_reuseFailAlloc_700_; 
v_reuseFailAlloc_700_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_700_, 0, v___x_688_);
lean_ctor_set(v_reuseFailAlloc_700_, 1, v___x_691_);
lean_ctor_set(v_reuseFailAlloc_700_, 2, v___x_694_);
lean_ctor_set(v_reuseFailAlloc_700_, 3, v___x_697_);
v___x_699_ = v_reuseFailAlloc_700_;
goto v_reusejp_698_;
}
v_reusejp_698_:
{
return v___x_699_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul___boxed(lean_object* v_A_702_, lean_object* v_B_703_){
_start:
{
lean_object* v_res_704_; 
v_res_704_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(v_A_702_, v_B_703_);
lean_dec_ref(v_A_702_);
return v_res_704_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_diagMat2(lean_object* v_d0_705_, lean_object* v_d1_706_){
_start:
{
lean_object* v___x_707_; lean_object* v___x_708_; 
v___x_707_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_708_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_708_, 0, v_d0_705_);
lean_ctor_set(v___x_708_, 1, v___x_707_);
lean_ctor_set(v___x_708_, 2, v___x_707_);
lean_ctor_set(v___x_708_, 3, v_d1_706_);
return v___x_708_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_List_elem___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__0(lean_object* v_a_845_, lean_object* v_x_846_){
_start:
{
if (lean_obj_tag(v_x_846_) == 0)
{
uint8_t v___x_847_; 
v___x_847_ = 0;
return v___x_847_;
}
else
{
lean_object* v_head_848_; lean_object* v_tail_849_; uint8_t v___x_850_; 
v_head_848_ = lean_ctor_get(v_x_846_, 0);
v_tail_849_ = lean_ctor_get(v_x_846_, 1);
v___x_850_ = lean_nat_dec_eq(v_a_845_, v_head_848_);
if (v___x_850_ == 0)
{
v_x_846_ = v_tail_849_;
goto _start;
}
else
{
return v___x_850_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_elem___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__0___boxed(lean_object* v_a_852_, lean_object* v_x_853_){
_start:
{
uint8_t v_res_854_; lean_object* v_r_855_; 
v_res_854_ = lp_FiniteQuantum_List_elem___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__0(v_a_852_, v_x_853_);
lean_dec(v_x_853_);
lean_dec(v_a_852_);
v_r_855_ = lean_box(v_res_854_);
return v_r_855_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__1(lean_object* v_r_856_, lean_object* v_a_857_, lean_object* v_a_858_){
_start:
{
if (lean_obj_tag(v_a_857_) == 0)
{
lean_object* v___x_859_; 
v___x_859_ = l_List_reverse___redArg(v_a_858_);
return v___x_859_;
}
else
{
lean_object* v_head_860_; lean_object* v_tail_861_; lean_object* v___x_863_; uint8_t v_isShared_864_; uint8_t v_isSharedCheck_871_; 
v_head_860_ = lean_ctor_get(v_a_857_, 0);
v_tail_861_ = lean_ctor_get(v_a_857_, 1);
v_isSharedCheck_871_ = !lean_is_exclusive(v_a_857_);
if (v_isSharedCheck_871_ == 0)
{
v___x_863_ = v_a_857_;
v_isShared_864_ = v_isSharedCheck_871_;
goto v_resetjp_862_;
}
else
{
lean_inc(v_tail_861_);
lean_inc(v_head_860_);
lean_dec(v_a_857_);
v___x_863_ = lean_box(0);
v_isShared_864_ = v_isSharedCheck_871_;
goto v_resetjp_862_;
}
v_resetjp_862_:
{
uint8_t v___x_865_; 
v___x_865_ = lp_FiniteQuantum_List_elem___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__0(v_r_856_, v_head_860_);
if (v___x_865_ == 0)
{
lean_del_object(v___x_863_);
lean_dec(v_head_860_);
v_a_857_ = v_tail_861_;
goto _start;
}
else
{
lean_object* v___x_868_; 
if (v_isShared_864_ == 0)
{
lean_ctor_set(v___x_863_, 1, v_a_858_);
v___x_868_ = v___x_863_;
goto v_reusejp_867_;
}
else
{
lean_object* v_reuseFailAlloc_870_; 
v_reuseFailAlloc_870_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_870_, 0, v_head_860_);
lean_ctor_set(v_reuseFailAlloc_870_, 1, v_a_858_);
v___x_868_ = v_reuseFailAlloc_870_;
goto v_reusejp_867_;
}
v_reusejp_867_:
{
v_a_857_ = v_tail_861_;
v_a_858_ = v___x_868_;
goto _start;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_filterTR_loop___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__1___boxed(lean_object* v_r_872_, lean_object* v_a_873_, lean_object* v_a_874_){
_start:
{
lean_object* v_res_875_; 
v_res_875_ = lp_FiniteQuantum_List_filterTR_loop___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__1(v_r_872_, v_a_873_, v_a_874_);
lean_dec(v_r_872_);
return v_res_875_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello(lean_object* v_r_876_){
_start:
{
lean_object* v___x_877_; lean_object* v___x_878_; lean_object* v___x_879_; lean_object* v___x_880_; 
v___x_877_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_cabelloContexts));
v___x_878_ = lean_box(0);
v___x_879_ = lp_FiniteQuantum_List_filterTR_loop___at___00QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello_spec__1(v_r_876_, v___x_877_, v___x_878_);
v___x_880_ = l_List_lengthTR___redArg(v___x_879_);
lean_dec(v___x_879_);
return v___x_880_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello___boxed(lean_object* v_r_881_){
_start:
{
lean_object* v_res_882_; 
v_res_882_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_rayDegreeInCabello(v_r_881_);
lean_dec(v_r_881_);
return v_res_882_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceZeroDetNeg(lean_object* v_a_883_, lean_object* v_b_884_){
_start:
{
lean_object* v___x_885_; lean_object* v___x_886_; lean_object* v___x_887_; 
v___x_885_ = lean_int_mul(v_a_883_, v_a_883_);
v___x_886_ = lean_int_mul(v_b_884_, v_b_884_);
v___x_887_ = lean_int_add(v___x_885_, v___x_886_);
lean_dec(v___x_886_);
lean_dec(v___x_885_);
return v___x_887_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceZeroDetNeg___boxed(lean_object* v_a_888_, lean_object* v_b_889_){
_start:
{
lean_object* v_res_890_; 
v_res_890_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_traceZeroDetNeg(v_a_888_, v_b_889_);
lean_dec(v_b_889_);
lean_dec(v_a_888_);
return v_res_890_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0(void){
_start:
{
lean_object* v___x_891_; lean_object* v___x_892_; 
v___x_891_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___x_892_ = lean_int_neg(v___x_891_);
return v___x_892_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt(lean_object* v_u0_893_, lean_object* v_u1_894_, lean_object* v_v0_895_, lean_object* v_v1_896_, lean_object* v_v2_897_){
_start:
{
lean_object* v___x_898_; lean_object* v___x_899_; lean_object* v___x_900_; lean_object* v___x_901_; lean_object* v___x_902_; lean_object* v___x_903_; lean_object* v___x_904_; lean_object* v___x_905_; lean_object* v___x_906_; lean_object* v___x_907_; lean_object* v___x_908_; lean_object* v___x_909_; lean_object* v___x_910_; lean_object* v___x_911_; lean_object* v___x_912_; lean_object* v___x_913_; lean_object* v___x_914_; lean_object* v___x_915_; lean_object* v___x_916_; lean_object* v___x_917_; lean_object* v___x_918_; lean_object* v___x_919_; lean_object* v___x_920_; lean_object* v___x_921_; lean_object* v___x_922_; 
v___x_898_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___x_899_ = lean_int_sub(v_v0_895_, v_u0_893_);
v___x_900_ = lean_int_sub(v___x_898_, v___x_899_);
lean_dec(v___x_899_);
v___x_901_ = lean_nat_abs(v___x_900_);
lean_dec(v___x_900_);
v___x_902_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0);
v___x_903_ = lean_int_sub(v_v0_895_, v_u1_894_);
v___x_904_ = lean_int_sub(v___x_902_, v___x_903_);
lean_dec(v___x_903_);
v___x_905_ = lean_nat_abs(v___x_904_);
lean_dec(v___x_904_);
v___x_906_ = lean_nat_add(v___x_901_, v___x_905_);
lean_dec(v___x_905_);
lean_dec(v___x_901_);
v___x_907_ = lean_int_sub(v_v1_896_, v_u0_893_);
v___x_908_ = lean_int_sub(v___x_902_, v___x_907_);
lean_dec(v___x_907_);
v___x_909_ = lean_nat_abs(v___x_908_);
lean_dec(v___x_908_);
v___x_910_ = lean_nat_add(v___x_906_, v___x_909_);
lean_dec(v___x_909_);
lean_dec(v___x_906_);
v___x_911_ = lean_int_sub(v_v1_896_, v_u1_894_);
v___x_912_ = lean_int_sub(v___x_898_, v___x_911_);
lean_dec(v___x_911_);
v___x_913_ = lean_nat_abs(v___x_912_);
lean_dec(v___x_912_);
v___x_914_ = lean_nat_add(v___x_910_, v___x_913_);
lean_dec(v___x_913_);
lean_dec(v___x_910_);
v___x_915_ = lean_int_sub(v_v2_897_, v_u0_893_);
v___x_916_ = lean_int_sub(v___x_898_, v___x_915_);
lean_dec(v___x_915_);
v___x_917_ = lean_nat_abs(v___x_916_);
lean_dec(v___x_916_);
v___x_918_ = lean_nat_add(v___x_914_, v___x_917_);
lean_dec(v___x_917_);
lean_dec(v___x_914_);
v___x_919_ = lean_int_sub(v_v2_897_, v_u1_894_);
v___x_920_ = lean_int_sub(v___x_902_, v___x_919_);
lean_dec(v___x_919_);
v___x_921_ = lean_nat_abs(v___x_920_);
lean_dec(v___x_920_);
v___x_922_ = lean_nat_add(v___x_918_, v___x_921_);
lean_dec(v___x_921_);
lean_dec(v___x_918_);
return v___x_922_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___boxed(lean_object* v_u0_923_, lean_object* v_u1_924_, lean_object* v_v0_925_, lean_object* v_v1_926_, lean_object* v_v2_927_){
_start:
{
lean_object* v_res_928_; 
v_res_928_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt(v_u0_923_, v_u1_924_, v_v0_925_, v_v1_926_, v_v2_927_);
lean_dec(v_v2_927_);
lean_dec(v_v1_926_);
lean_dec(v_v0_925_);
lean_dec(v_u1_924_);
lean_dec(v_u0_923_);
return v_res_928_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0(void){
_start:
{
lean_object* v___x_929_; lean_object* v___x_930_; 
v___x_929_ = lean_unsigned_to_nat(3u);
v___x_930_ = lean_nat_to_int(v___x_929_);
return v___x_930_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__1(void){
_start:
{
lean_object* v___x_931_; lean_object* v___x_932_; 
v___x_931_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0);
v___x_932_ = lean_int_neg(v___x_931_);
return v___x_932_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2(lean_object* v_u0_933_, lean_object* v_u1_934_, lean_object* v_v0_935_, lean_object* v_v1_936_, lean_object* v_v2_937_){
_start:
{
lean_object* v___x_938_; lean_object* v___x_939_; lean_object* v___x_940_; lean_object* v___x_941_; lean_object* v___x_942_; lean_object* v___x_943_; lean_object* v___x_944_; lean_object* v___x_945_; lean_object* v___x_946_; lean_object* v___x_947_; lean_object* v___x_948_; lean_object* v___x_949_; lean_object* v___x_950_; lean_object* v___x_951_; lean_object* v___x_952_; lean_object* v___x_953_; lean_object* v___x_954_; lean_object* v___x_955_; lean_object* v___x_956_; lean_object* v___x_957_; lean_object* v___x_958_; lean_object* v___x_959_; lean_object* v___x_960_; lean_object* v___x_961_; lean_object* v___x_962_; 
v___x_938_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__0);
v___x_939_ = lean_int_sub(v_v0_935_, v_u0_933_);
v___x_940_ = lean_int_sub(v___x_938_, v___x_939_);
lean_dec(v___x_939_);
v___x_941_ = lean_nat_abs(v___x_940_);
lean_dec(v___x_940_);
v___x_942_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__1, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__1_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___closed__1);
v___x_943_ = lean_int_sub(v_v0_935_, v_u1_934_);
v___x_944_ = lean_int_sub(v___x_942_, v___x_943_);
lean_dec(v___x_943_);
v___x_945_ = lean_nat_abs(v___x_944_);
lean_dec(v___x_944_);
v___x_946_ = lean_nat_add(v___x_941_, v___x_945_);
lean_dec(v___x_945_);
lean_dec(v___x_941_);
v___x_947_ = lean_int_sub(v_v1_936_, v_u0_933_);
v___x_948_ = lean_int_sub(v___x_942_, v___x_947_);
lean_dec(v___x_947_);
v___x_949_ = lean_nat_abs(v___x_948_);
lean_dec(v___x_948_);
v___x_950_ = lean_nat_add(v___x_946_, v___x_949_);
lean_dec(v___x_949_);
lean_dec(v___x_946_);
v___x_951_ = lean_int_sub(v_v1_936_, v_u1_934_);
v___x_952_ = lean_int_sub(v___x_938_, v___x_951_);
lean_dec(v___x_951_);
v___x_953_ = lean_nat_abs(v___x_952_);
lean_dec(v___x_952_);
v___x_954_ = lean_nat_add(v___x_950_, v___x_953_);
lean_dec(v___x_953_);
lean_dec(v___x_950_);
v___x_955_ = lean_int_sub(v_v2_937_, v_u0_933_);
v___x_956_ = lean_int_sub(v___x_938_, v___x_955_);
lean_dec(v___x_955_);
v___x_957_ = lean_nat_abs(v___x_956_);
lean_dec(v___x_956_);
v___x_958_ = lean_nat_add(v___x_954_, v___x_957_);
lean_dec(v___x_957_);
lean_dec(v___x_954_);
v___x_959_ = lean_int_sub(v_v2_937_, v_u1_934_);
v___x_960_ = lean_int_sub(v___x_942_, v___x_959_);
lean_dec(v___x_959_);
v___x_961_ = lean_nat_abs(v___x_960_);
lean_dec(v___x_960_);
v___x_962_ = lean_nat_add(v___x_958_, v___x_961_);
lean_dec(v___x_961_);
lean_dec(v___x_958_);
return v___x_962_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2___boxed(lean_object* v_u0_963_, lean_object* v_u1_964_, lean_object* v_v0_965_, lean_object* v_v1_966_, lean_object* v_v2_967_){
_start:
{
lean_object* v_res_968_; 
v_res_968_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalCenteredScaled2(v_u0_963_, v_u1_964_, v_v0_965_, v_v1_966_, v_v2_967_);
lean_dec(v_v2_967_);
lean_dec(v_v1_966_);
lean_dec(v_v0_965_);
lean_dec(v_u1_964_);
lean_dec(v_u0_963_);
return v_res_968_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___closed__0(void){
_start:
{
lean_object* v___x_969_; lean_object* v___x_970_; lean_object* v___x_971_; 
v___x_969_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_970_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___x_971_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_971_, 0, v___x_970_);
lean_ctor_set(v___x_971_, 1, v___x_969_);
lean_ctor_set(v___x_971_, 2, v___x_969_);
lean_ctor_set(v___x_971_, 3, v___x_969_);
return v___x_971_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0(lean_object* v_A_972_){
_start:
{
lean_object* v___x_973_; lean_object* v___x_974_; lean_object* v___x_975_; 
v___x_973_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___closed__0);
v___x_974_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(v_A_972_, v___x_973_);
v___x_975_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(v___x_973_, v___x_974_);
return v___x_975_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0___boxed(lean_object* v_A_976_){
_start:
{
lean_object* v_res_977_; 
v_res_977_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_projZ0(v_A_976_);
lean_dec_ref(v_A_976_);
return v_res_977_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_sub(lean_object* v_A_978_, lean_object* v_B_979_){
_start:
{
lean_object* v_m00_980_; lean_object* v_m01_981_; lean_object* v_m10_982_; lean_object* v_m11_983_; lean_object* v_m00_984_; lean_object* v_m01_985_; lean_object* v_m10_986_; lean_object* v_m11_987_; lean_object* v___x_989_; uint8_t v_isShared_990_; uint8_t v_isSharedCheck_998_; 
v_m00_980_ = lean_ctor_get(v_A_978_, 0);
v_m01_981_ = lean_ctor_get(v_A_978_, 1);
v_m10_982_ = lean_ctor_get(v_A_978_, 2);
v_m11_983_ = lean_ctor_get(v_A_978_, 3);
v_m00_984_ = lean_ctor_get(v_B_979_, 0);
v_m01_985_ = lean_ctor_get(v_B_979_, 1);
v_m10_986_ = lean_ctor_get(v_B_979_, 2);
v_m11_987_ = lean_ctor_get(v_B_979_, 3);
v_isSharedCheck_998_ = !lean_is_exclusive(v_B_979_);
if (v_isSharedCheck_998_ == 0)
{
v___x_989_ = v_B_979_;
v_isShared_990_ = v_isSharedCheck_998_;
goto v_resetjp_988_;
}
else
{
lean_inc(v_m11_987_);
lean_inc(v_m10_986_);
lean_inc(v_m01_985_);
lean_inc(v_m00_984_);
lean_dec(v_B_979_);
v___x_989_ = lean_box(0);
v_isShared_990_ = v_isSharedCheck_998_;
goto v_resetjp_988_;
}
v_resetjp_988_:
{
lean_object* v___x_991_; lean_object* v___x_992_; lean_object* v___x_993_; lean_object* v___x_994_; lean_object* v___x_996_; 
v___x_991_ = lean_int_sub(v_m00_980_, v_m00_984_);
lean_dec(v_m00_984_);
v___x_992_ = lean_int_sub(v_m01_981_, v_m01_985_);
lean_dec(v_m01_985_);
v___x_993_ = lean_int_sub(v_m10_982_, v_m10_986_);
lean_dec(v_m10_986_);
v___x_994_ = lean_int_sub(v_m11_983_, v_m11_987_);
lean_dec(v_m11_987_);
if (v_isShared_990_ == 0)
{
lean_ctor_set(v___x_989_, 3, v___x_994_);
lean_ctor_set(v___x_989_, 2, v___x_993_);
lean_ctor_set(v___x_989_, 1, v___x_992_);
lean_ctor_set(v___x_989_, 0, v___x_991_);
v___x_996_ = v___x_989_;
goto v_reusejp_995_;
}
else
{
lean_object* v_reuseFailAlloc_997_; 
v_reuseFailAlloc_997_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_997_, 0, v___x_991_);
lean_ctor_set(v_reuseFailAlloc_997_, 1, v___x_992_);
lean_ctor_set(v_reuseFailAlloc_997_, 2, v___x_993_);
lean_ctor_set(v_reuseFailAlloc_997_, 3, v___x_994_);
v___x_996_ = v_reuseFailAlloc_997_;
goto v_reusejp_995_;
}
v_reusejp_995_:
{
return v___x_996_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_sub___boxed(lean_object* v_A_999_, lean_object* v_B_1000_){
_start:
{
lean_object* v_res_1001_; 
v_res_1001_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_sub(v_A_999_, v_B_1000_);
lean_dec_ref(v_A_999_);
return v_res_1001_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_trace(lean_object* v_A_1002_){
_start:
{
lean_object* v_m00_1003_; lean_object* v_m11_1004_; lean_object* v___x_1005_; 
v_m00_1003_ = lean_ctor_get(v_A_1002_, 0);
v_m11_1004_ = lean_ctor_get(v_A_1002_, 3);
v___x_1005_ = lean_int_add(v_m00_1003_, v_m11_1004_);
return v___x_1005_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_trace___boxed(lean_object* v_A_1006_){
_start:
{
lean_object* v_res_1007_; 
v_res_1007_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_trace(v_A_1006_);
lean_dec_ref(v_A_1006_);
return v_res_1007_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe_decEq(lean_object* v_x_1008_, lean_object* v_x_1009_){
_start:
{
uint8_t v___x_1010_; 
v___x_1010_ = lean_nat_dec_eq(v_x_1008_, v_x_1009_);
return v___x_1010_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe_decEq___boxed(lean_object* v_x_1011_, lean_object* v_x_1012_){
_start:
{
uint8_t v_res_1013_; lean_object* v_r_1014_; 
v_res_1013_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe_decEq(v_x_1011_, v_x_1012_);
lean_dec(v_x_1012_);
lean_dec(v_x_1011_);
v_r_1014_ = lean_box(v_res_1013_);
return v_r_1014_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe(lean_object* v_x_1015_, lean_object* v_x_1016_){
_start:
{
uint8_t v___x_1017_; 
v___x_1017_ = lean_nat_dec_eq(v_x_1015_, v_x_1016_);
return v___x_1017_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe___boxed(lean_object* v_x_1018_, lean_object* v_x_1019_){
_start:
{
uint8_t v_res_1020_; lean_object* v_r_1021_; 
v_res_1020_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqDiagnosticProbe(v_x_1018_, v_x_1019_);
lean_dec(v_x_1019_);
lean_dec(v_x_1018_);
v_r_1021_ = lean_box(v_res_1020_);
return v_r_1021_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_1031_; lean_object* v___x_1032_; 
v___x_1031_ = lean_unsigned_to_nat(9u);
v___x_1032_ = lean_nat_to_int(v___x_1031_);
return v___x_1032_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg(lean_object* v_x_1033_){
_start:
{
lean_object* v___x_1034_; lean_object* v___x_1035_; lean_object* v___x_1036_; lean_object* v___x_1037_; lean_object* v___x_1038_; uint8_t v___x_1039_; lean_object* v___x_1040_; lean_object* v___x_1041_; lean_object* v___x_1042_; lean_object* v___x_1043_; lean_object* v___x_1044_; lean_object* v___x_1045_; lean_object* v___x_1046_; lean_object* v___x_1047_; lean_object* v___x_1048_; 
v___x_1034_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__3));
v___x_1035_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__4, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg___closed__4);
v___x_1036_ = l_Nat_reprFast(v_x_1033_);
v___x_1037_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1037_, 0, v___x_1036_);
v___x_1038_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1038_, 0, v___x_1035_);
lean_ctor_set(v___x_1038_, 1, v___x_1037_);
v___x_1039_ = 0;
v___x_1040_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1040_, 0, v___x_1038_);
lean_ctor_set_uint8(v___x_1040_, sizeof(void*)*1, v___x_1039_);
v___x_1041_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1041_, 0, v___x_1034_);
lean_ctor_set(v___x_1041_, 1, v___x_1040_);
v___x_1042_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18);
v___x_1043_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19));
v___x_1044_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1044_, 0, v___x_1043_);
lean_ctor_set(v___x_1044_, 1, v___x_1041_);
v___x_1045_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20));
v___x_1046_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1046_, 0, v___x_1044_);
lean_ctor_set(v___x_1046_, 1, v___x_1045_);
v___x_1047_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1047_, 0, v___x_1042_);
lean_ctor_set(v___x_1047_, 1, v___x_1046_);
v___x_1048_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1048_, 0, v___x_1047_);
lean_ctor_set_uint8(v___x_1048_, sizeof(void*)*1, v___x_1039_);
return v___x_1048_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr(lean_object* v_x_1049_, lean_object* v_prec_1050_){
_start:
{
lean_object* v___x_1051_; 
v___x_1051_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___redArg(v_x_1049_);
return v___x_1051_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr___boxed(lean_object* v_x_1052_, lean_object* v_prec_1053_){
_start:
{
lean_object* v_res_1054_; 
v_res_1054_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprDiagnosticProbe_repr(v_x_1052_, v_prec_1053_);
lean_dec(v_prec_1053_);
return v_res_1054_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt_decEq(lean_object* v_x_1057_, lean_object* v_x_1058_){
_start:
{
lean_object* v_defect_1059_; lean_object* v_witnessBound_1060_; lean_object* v_defect_1061_; lean_object* v_witnessBound_1062_; uint8_t v___x_1063_; 
v_defect_1059_ = lean_ctor_get(v_x_1057_, 0);
v_witnessBound_1060_ = lean_ctor_get(v_x_1057_, 1);
v_defect_1061_ = lean_ctor_get(v_x_1058_, 0);
v_witnessBound_1062_ = lean_ctor_get(v_x_1058_, 1);
v___x_1063_ = lean_nat_dec_eq(v_defect_1059_, v_defect_1061_);
if (v___x_1063_ == 0)
{
return v___x_1063_;
}
else
{
uint8_t v___x_1064_; 
v___x_1064_ = lean_nat_dec_eq(v_witnessBound_1060_, v_witnessBound_1062_);
return v___x_1064_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt_decEq___boxed(lean_object* v_x_1065_, lean_object* v_x_1066_){
_start:
{
uint8_t v_res_1067_; lean_object* v_r_1068_; 
v_res_1067_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt_decEq(v_x_1065_, v_x_1066_);
lean_dec_ref(v_x_1066_);
lean_dec_ref(v_x_1065_);
v_r_1068_ = lean_box(v_res_1067_);
return v_r_1068_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt(lean_object* v_x_1069_, lean_object* v_x_1070_){
_start:
{
uint8_t v___x_1071_; 
v___x_1071_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt_decEq(v_x_1069_, v_x_1070_);
return v___x_1071_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt___boxed(lean_object* v_x_1072_, lean_object* v_x_1073_){
_start:
{
uint8_t v_res_1074_; lean_object* v_r_1075_; 
v_res_1074_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqCertifierReceipt(v_x_1072_, v_x_1073_);
lean_dec_ref(v_x_1073_);
lean_dec_ref(v_x_1072_);
v_r_1075_ = lean_box(v_res_1074_);
return v_r_1075_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__4(void){
_start:
{
lean_object* v___x_1085_; lean_object* v___x_1086_; 
v___x_1085_ = lean_unsigned_to_nat(10u);
v___x_1086_ = lean_nat_to_int(v___x_1085_);
return v___x_1086_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_1090_; lean_object* v___x_1091_; 
v___x_1090_ = lean_unsigned_to_nat(16u);
v___x_1091_ = lean_nat_to_int(v___x_1090_);
return v___x_1091_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg(lean_object* v_x_1092_){
_start:
{
lean_object* v_defect_1093_; lean_object* v_witnessBound_1094_; lean_object* v___x_1096_; uint8_t v_isShared_1097_; uint8_t v_isSharedCheck_1129_; 
v_defect_1093_ = lean_ctor_get(v_x_1092_, 0);
v_witnessBound_1094_ = lean_ctor_get(v_x_1092_, 1);
v_isSharedCheck_1129_ = !lean_is_exclusive(v_x_1092_);
if (v_isSharedCheck_1129_ == 0)
{
v___x_1096_ = v_x_1092_;
v_isShared_1097_ = v_isSharedCheck_1129_;
goto v_resetjp_1095_;
}
else
{
lean_inc(v_witnessBound_1094_);
lean_inc(v_defect_1093_);
lean_dec(v_x_1092_);
v___x_1096_ = lean_box(0);
v_isShared_1097_ = v_isSharedCheck_1129_;
goto v_resetjp_1095_;
}
v_resetjp_1095_:
{
lean_object* v___x_1098_; lean_object* v___x_1099_; lean_object* v___x_1100_; lean_object* v___x_1101_; lean_object* v___x_1102_; lean_object* v___x_1104_; 
v___x_1098_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__5));
v___x_1099_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__3));
v___x_1100_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__4, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__4_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__4);
v___x_1101_ = l_Nat_reprFast(v_defect_1093_);
v___x_1102_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1102_, 0, v___x_1101_);
if (v_isShared_1097_ == 0)
{
lean_ctor_set_tag(v___x_1096_, 4);
lean_ctor_set(v___x_1096_, 1, v___x_1102_);
lean_ctor_set(v___x_1096_, 0, v___x_1100_);
v___x_1104_ = v___x_1096_;
goto v_reusejp_1103_;
}
else
{
lean_object* v_reuseFailAlloc_1128_; 
v_reuseFailAlloc_1128_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1128_, 0, v___x_1100_);
lean_ctor_set(v_reuseFailAlloc_1128_, 1, v___x_1102_);
v___x_1104_ = v_reuseFailAlloc_1128_;
goto v_reusejp_1103_;
}
v_reusejp_1103_:
{
uint8_t v___x_1105_; lean_object* v___x_1106_; lean_object* v___x_1107_; lean_object* v___x_1108_; lean_object* v___x_1109_; lean_object* v___x_1110_; lean_object* v___x_1111_; lean_object* v___x_1112_; lean_object* v___x_1113_; lean_object* v___x_1114_; lean_object* v___x_1115_; lean_object* v___x_1116_; lean_object* v___x_1117_; lean_object* v___x_1118_; lean_object* v___x_1119_; lean_object* v___x_1120_; lean_object* v___x_1121_; lean_object* v___x_1122_; lean_object* v___x_1123_; lean_object* v___x_1124_; lean_object* v___x_1125_; lean_object* v___x_1126_; lean_object* v___x_1127_; 
v___x_1105_ = 0;
v___x_1106_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1106_, 0, v___x_1104_);
lean_ctor_set_uint8(v___x_1106_, sizeof(void*)*1, v___x_1105_);
v___x_1107_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1107_, 0, v___x_1099_);
lean_ctor_set(v___x_1107_, 1, v___x_1106_);
v___x_1108_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__9));
v___x_1109_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1109_, 0, v___x_1107_);
lean_ctor_set(v___x_1109_, 1, v___x_1108_);
v___x_1110_ = lean_box(1);
v___x_1111_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1111_, 0, v___x_1109_);
lean_ctor_set(v___x_1111_, 1, v___x_1110_);
v___x_1112_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__6));
v___x_1113_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1113_, 0, v___x_1111_);
lean_ctor_set(v___x_1113_, 1, v___x_1112_);
v___x_1114_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1114_, 0, v___x_1113_);
lean_ctor_set(v___x_1114_, 1, v___x_1098_);
v___x_1115_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg___closed__7);
v___x_1116_ = l_Nat_reprFast(v_witnessBound_1094_);
v___x_1117_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_1117_, 0, v___x_1116_);
v___x_1118_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1118_, 0, v___x_1115_);
lean_ctor_set(v___x_1118_, 1, v___x_1117_);
v___x_1119_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1119_, 0, v___x_1118_);
lean_ctor_set_uint8(v___x_1119_, sizeof(void*)*1, v___x_1105_);
v___x_1120_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1120_, 0, v___x_1114_);
lean_ctor_set(v___x_1120_, 1, v___x_1119_);
v___x_1121_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__18);
v___x_1122_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__19));
v___x_1123_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1123_, 0, v___x_1122_);
lean_ctor_set(v___x_1123_, 1, v___x_1120_);
v___x_1124_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprObligationMonoid_repr___redArg___closed__20));
v___x_1125_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_1125_, 0, v___x_1123_);
lean_ctor_set(v___x_1125_, 1, v___x_1124_);
v___x_1126_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1126_, 0, v___x_1121_);
lean_ctor_set(v___x_1126_, 1, v___x_1125_);
v___x_1127_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1127_, 0, v___x_1126_);
lean_ctor_set_uint8(v___x_1127_, sizeof(void*)*1, v___x_1105_);
return v___x_1127_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr(lean_object* v_x_1130_, lean_object* v_prec_1131_){
_start:
{
lean_object* v___x_1132_; 
v___x_1132_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___redArg(v_x_1130_);
return v___x_1132_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr___boxed(lean_object* v_x_1133_, lean_object* v_prec_1134_){
_start:
{
lean_object* v_res_1135_; 
v_res_1135_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprCertifierReceipt_repr(v_x_1133_, v_prec_1134_);
lean_dec(v_prec_1134_);
return v_res_1135_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizeFromReceipt(lean_object* v_r_1138_){
_start:
{
lean_object* v_defect_1139_; lean_object* v___x_1140_; uint8_t v___x_1141_; 
v_defect_1139_ = lean_ctor_get(v_r_1138_, 0);
v___x_1140_ = lean_unsigned_to_nat(0u);
v___x_1141_ = lean_nat_dec_eq(v_defect_1139_, v___x_1140_);
return v___x_1141_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizeFromReceipt___boxed(lean_object* v_r_1142_){
_start:
{
uint8_t v_res_1143_; lean_object* v_r_1144_; 
v_res_1143_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizeFromReceipt(v_r_1142_);
lean_dec_ref(v_r_1142_);
v_r_1144_ = lean_box(v_res_1143_);
return v_r_1144_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_trivalentSpinAdmissible(lean_object* v_twoJ1_1145_, lean_object* v_twoJ2_1146_, lean_object* v_twoJ3_1147_){
_start:
{
uint8_t v___y_1149_; lean_object* v___x_1157_; uint8_t v___x_1158_; 
v___x_1157_ = lean_nat_add(v_twoJ2_1146_, v_twoJ3_1147_);
v___x_1158_ = lean_nat_dec_le(v_twoJ1_1145_, v___x_1157_);
lean_dec(v___x_1157_);
if (v___x_1158_ == 0)
{
v___y_1149_ = v___x_1158_;
goto v___jp_1148_;
}
else
{
lean_object* v___x_1159_; uint8_t v___x_1160_; 
v___x_1159_ = lean_nat_add(v_twoJ3_1147_, v_twoJ1_1145_);
v___x_1160_ = lean_nat_dec_le(v_twoJ2_1146_, v___x_1159_);
lean_dec(v___x_1159_);
v___y_1149_ = v___x_1160_;
goto v___jp_1148_;
}
v___jp_1148_:
{
if (v___y_1149_ == 0)
{
return v___y_1149_;
}
else
{
lean_object* v___x_1150_; uint8_t v___x_1151_; 
v___x_1150_ = lean_nat_add(v_twoJ1_1145_, v_twoJ2_1146_);
v___x_1151_ = lean_nat_dec_le(v_twoJ3_1147_, v___x_1150_);
if (v___x_1151_ == 0)
{
lean_dec(v___x_1150_);
return v___x_1151_;
}
else
{
lean_object* v___x_1152_; lean_object* v___x_1153_; lean_object* v___x_1154_; lean_object* v___x_1155_; uint8_t v___x_1156_; 
v___x_1152_ = lean_nat_add(v___x_1150_, v_twoJ3_1147_);
lean_dec(v___x_1150_);
v___x_1153_ = lean_unsigned_to_nat(2u);
v___x_1154_ = lean_nat_mod(v___x_1152_, v___x_1153_);
lean_dec(v___x_1152_);
v___x_1155_ = lean_unsigned_to_nat(0u);
v___x_1156_ = lean_nat_dec_eq(v___x_1154_, v___x_1155_);
lean_dec(v___x_1154_);
return v___x_1156_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_trivalentSpinAdmissible___boxed(lean_object* v_twoJ1_1161_, lean_object* v_twoJ2_1162_, lean_object* v_twoJ3_1163_){
_start:
{
uint8_t v_res_1164_; lean_object* v_r_1165_; 
v_res_1164_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_trivalentSpinAdmissible(v_twoJ1_1161_, v_twoJ2_1162_, v_twoJ3_1163_);
lean_dec(v_twoJ3_1163_);
lean_dec(v_twoJ2_1162_);
lean_dec(v_twoJ1_1161_);
v_r_1165_ = lean_box(v_res_1164_);
return v_r_1165_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_add(lean_object* v_A_1166_, lean_object* v_B_1167_){
_start:
{
lean_object* v_m00_1168_; lean_object* v_m01_1169_; lean_object* v_m10_1170_; lean_object* v_m11_1171_; lean_object* v_m00_1172_; lean_object* v_m01_1173_; lean_object* v_m10_1174_; lean_object* v_m11_1175_; lean_object* v___x_1177_; uint8_t v_isShared_1178_; uint8_t v_isSharedCheck_1186_; 
v_m00_1168_ = lean_ctor_get(v_A_1166_, 0);
v_m01_1169_ = lean_ctor_get(v_A_1166_, 1);
v_m10_1170_ = lean_ctor_get(v_A_1166_, 2);
v_m11_1171_ = lean_ctor_get(v_A_1166_, 3);
v_m00_1172_ = lean_ctor_get(v_B_1167_, 0);
v_m01_1173_ = lean_ctor_get(v_B_1167_, 1);
v_m10_1174_ = lean_ctor_get(v_B_1167_, 2);
v_m11_1175_ = lean_ctor_get(v_B_1167_, 3);
v_isSharedCheck_1186_ = !lean_is_exclusive(v_B_1167_);
if (v_isSharedCheck_1186_ == 0)
{
v___x_1177_ = v_B_1167_;
v_isShared_1178_ = v_isSharedCheck_1186_;
goto v_resetjp_1176_;
}
else
{
lean_inc(v_m11_1175_);
lean_inc(v_m10_1174_);
lean_inc(v_m01_1173_);
lean_inc(v_m00_1172_);
lean_dec(v_B_1167_);
v___x_1177_ = lean_box(0);
v_isShared_1178_ = v_isSharedCheck_1186_;
goto v_resetjp_1176_;
}
v_resetjp_1176_:
{
lean_object* v___x_1179_; lean_object* v___x_1180_; lean_object* v___x_1181_; lean_object* v___x_1182_; lean_object* v___x_1184_; 
v___x_1179_ = lean_int_add(v_m00_1168_, v_m00_1172_);
lean_dec(v_m00_1172_);
v___x_1180_ = lean_int_add(v_m01_1169_, v_m01_1173_);
lean_dec(v_m01_1173_);
v___x_1181_ = lean_int_add(v_m10_1170_, v_m10_1174_);
lean_dec(v_m10_1174_);
v___x_1182_ = lean_int_add(v_m11_1171_, v_m11_1175_);
lean_dec(v_m11_1175_);
if (v_isShared_1178_ == 0)
{
lean_ctor_set(v___x_1177_, 3, v___x_1182_);
lean_ctor_set(v___x_1177_, 2, v___x_1181_);
lean_ctor_set(v___x_1177_, 1, v___x_1180_);
lean_ctor_set(v___x_1177_, 0, v___x_1179_);
v___x_1184_ = v___x_1177_;
goto v_reusejp_1183_;
}
else
{
lean_object* v_reuseFailAlloc_1185_; 
v_reuseFailAlloc_1185_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_1185_, 0, v___x_1179_);
lean_ctor_set(v_reuseFailAlloc_1185_, 1, v___x_1180_);
lean_ctor_set(v_reuseFailAlloc_1185_, 2, v___x_1181_);
lean_ctor_set(v_reuseFailAlloc_1185_, 3, v___x_1182_);
v___x_1184_ = v_reuseFailAlloc_1185_;
goto v_reusejp_1183_;
}
v_reusejp_1183_:
{
return v___x_1184_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_add___boxed(lean_object* v_A_1187_, lean_object* v_B_1188_){
_start:
{
lean_object* v_res_1189_; 
v_res_1189_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_add(v_A_1187_, v_B_1188_);
lean_dec_ref(v_A_1187_);
return v_res_1189_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_pairInList(lean_object* v_p_1190_, lean_object* v_x_1191_){
_start:
{
if (lean_obj_tag(v_x_1191_) == 0)
{
uint8_t v___x_1192_; 
lean_dec_ref(v_p_1190_);
v___x_1192_ = 0;
return v___x_1192_;
}
else
{
lean_object* v_head_1193_; lean_object* v_tail_1194_; lean_object* v___x_1195_; uint8_t v___x_1196_; 
v_head_1193_ = lean_ctor_get(v_x_1191_, 0);
lean_inc(v_head_1193_);
v_tail_1194_ = lean_ctor_get(v_x_1191_, 1);
lean_inc(v_tail_1194_);
lean_dec_ref_known(v_x_1191_, 2);
v___x_1195_ = lean_alloc_closure((void*)(l_instDecidableEqNat___boxed), 2, 0);
lean_inc_ref(v_p_1190_);
lean_inc_ref(v___x_1195_);
v___x_1196_ = l_instDecidableEqProd___redArg(v___x_1195_, v___x_1195_, v_p_1190_, v_head_1193_);
if (v___x_1196_ == 0)
{
v_x_1191_ = v_tail_1194_;
goto _start;
}
else
{
lean_dec(v_tail_1194_);
lean_dec_ref(v_p_1190_);
return v___x_1196_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_pairInList___boxed(lean_object* v_p_1198_, lean_object* v_x_1199_){
_start:
{
uint8_t v_res_1200_; lean_object* v_r_1201_; 
v_res_1200_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_pairInList(v_p_1198_, v_x_1199_);
v_r_1201_ = lean_box(v_res_1200_);
return v_r_1201_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_pairInList_match__1_splitter___redArg(lean_object* v_x_1202_, lean_object* v_h__1_1203_, lean_object* v_h__2_1204_){
_start:
{
if (lean_obj_tag(v_x_1202_) == 0)
{
lean_object* v___x_1205_; lean_object* v___x_1206_; 
lean_dec(v_h__2_1204_);
v___x_1205_ = lean_box(0);
v___x_1206_ = lean_apply_1(v_h__1_1203_, v___x_1205_);
return v___x_1206_;
}
else
{
lean_object* v_head_1207_; lean_object* v_tail_1208_; lean_object* v___x_1209_; 
lean_dec(v_h__1_1203_);
v_head_1207_ = lean_ctor_get(v_x_1202_, 0);
lean_inc(v_head_1207_);
v_tail_1208_ = lean_ctor_get(v_x_1202_, 1);
lean_inc(v_tail_1208_);
lean_dec_ref_known(v_x_1202_, 2);
v___x_1209_ = lean_apply_2(v_h__2_1204_, v_head_1207_, v_tail_1208_);
return v___x_1209_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_pairInList_match__1_splitter(lean_object* v_motive_1210_, lean_object* v_x_1211_, lean_object* v_h__1_1212_, lean_object* v_h__2_1213_){
_start:
{
if (lean_obj_tag(v_x_1211_) == 0)
{
lean_object* v___x_1214_; lean_object* v___x_1215_; 
lean_dec(v_h__2_1213_);
v___x_1214_ = lean_box(0);
v___x_1215_ = lean_apply_1(v_h__1_1212_, v___x_1214_);
return v___x_1215_;
}
else
{
lean_object* v_head_1216_; lean_object* v_tail_1217_; lean_object* v___x_1218_; 
lean_dec(v_h__1_1212_);
v_head_1216_ = lean_ctor_get(v_x_1211_, 0);
lean_inc(v_head_1216_);
v_tail_1217_ = lean_ctor_get(v_x_1211_, 1);
lean_inc(v_tail_1217_);
lean_dec_ref_known(v_x_1211_, 2);
v___x_1218_ = lean_apply_2(v_h__2_1213_, v_head_1216_, v_tail_1217_);
return v___x_1218_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(uint8_t v_x_1219_){
_start:
{
if (v_x_1219_ == 0)
{
lean_object* v___x_1220_; 
v___x_1220_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0);
return v___x_1220_;
}
else
{
lean_object* v___x_1221_; 
v___x_1221_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
return v___x_1221_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0___boxed(lean_object* v_x_1222_){
_start:
{
uint8_t v_x_boxed_1223_; lean_object* v_res_1224_; 
v_x_boxed_1223_ = lean_unbox(v_x_1222_);
v_res_1224_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(v_x_boxed_1223_);
return v_res_1224_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet(uint8_t v_a0_1225_, uint8_t v_a1_1226_, uint8_t v_b0_1227_, uint8_t v_b1_1228_){
_start:
{
lean_object* v___x_1229_; lean_object* v___x_1230_; lean_object* v___x_1231_; lean_object* v___x_1232_; lean_object* v___x_1233_; lean_object* v___x_1234_; lean_object* v___x_1235_; lean_object* v___x_1236_; lean_object* v___x_1237_; lean_object* v___x_1238_; lean_object* v___x_1239_; 
v___x_1229_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(v_a0_1225_);
v___x_1230_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(v_b0_1227_);
v___x_1231_ = lean_int_mul(v___x_1229_, v___x_1230_);
v___x_1232_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(v_b1_1228_);
v___x_1233_ = lean_int_mul(v___x_1229_, v___x_1232_);
lean_dec(v___x_1229_);
v___x_1234_ = lean_int_add(v___x_1231_, v___x_1233_);
lean_dec(v___x_1233_);
lean_dec(v___x_1231_);
v___x_1235_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___lam__0(v_a1_1226_);
v___x_1236_ = lean_int_mul(v___x_1235_, v___x_1230_);
lean_dec(v___x_1230_);
v___x_1237_ = lean_int_add(v___x_1234_, v___x_1236_);
lean_dec(v___x_1236_);
lean_dec(v___x_1234_);
v___x_1238_ = lean_int_mul(v___x_1235_, v___x_1232_);
lean_dec(v___x_1232_);
lean_dec(v___x_1235_);
v___x_1239_ = lean_int_sub(v___x_1237_, v___x_1238_);
lean_dec(v___x_1238_);
lean_dec(v___x_1237_);
return v___x_1239_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet___boxed(lean_object* v_a0_1240_, lean_object* v_a1_1241_, lean_object* v_b0_1242_, lean_object* v_b1_1243_){
_start:
{
uint8_t v_a0_boxed_1244_; uint8_t v_a1_boxed_1245_; uint8_t v_b0_boxed_1246_; uint8_t v_b1_boxed_1247_; lean_object* v_res_1248_; 
v_a0_boxed_1244_ = lean_unbox(v_a0_1240_);
v_a1_boxed_1245_ = lean_unbox(v_a1_1241_);
v_b0_boxed_1246_ = lean_unbox(v_b0_1242_);
v_b1_boxed_1247_ = lean_unbox(v_b1_1243_);
v_res_1248_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_chshDet(v_a0_boxed_1244_, v_a1_boxed_1245_, v_b0_boxed_1246_, v_b1_boxed_1247_);
return v_res_1248_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_totalWeight(lean_object* v_x_1249_){
_start:
{
if (lean_obj_tag(v_x_1249_) == 0)
{
lean_object* v___x_1250_; 
v___x_1250_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
return v___x_1250_;
}
else
{
lean_object* v_head_1251_; lean_object* v_tail_1252_; lean_object* v_fst_1253_; lean_object* v___x_1254_; lean_object* v___x_1255_; lean_object* v___x_1256_; 
v_head_1251_ = lean_ctor_get(v_x_1249_, 0);
lean_inc(v_head_1251_);
v_tail_1252_ = lean_ctor_get(v_x_1249_, 1);
lean_inc(v_tail_1252_);
lean_dec_ref_known(v_x_1249_, 2);
v_fst_1253_ = lean_ctor_get(v_head_1251_, 0);
lean_inc(v_fst_1253_);
lean_dec(v_head_1251_);
v___x_1254_ = lean_nat_to_int(v_fst_1253_);
v___x_1255_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_totalWeight(v_tail_1252_);
v___x_1256_ = lean_int_add(v___x_1254_, v___x_1255_);
lean_dec(v___x_1255_);
lean_dec(v___x_1254_);
return v___x_1256_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedChshSum(lean_object* v_x_1257_){
_start:
{
if (lean_obj_tag(v_x_1257_) == 0)
{
lean_object* v___x_1258_; 
v___x_1258_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
return v___x_1258_;
}
else
{
lean_object* v_head_1259_; lean_object* v_tail_1260_; lean_object* v_fst_1261_; lean_object* v_snd_1262_; lean_object* v___x_1263_; lean_object* v___x_1264_; lean_object* v___x_1265_; lean_object* v___x_1266_; 
v_head_1259_ = lean_ctor_get(v_x_1257_, 0);
lean_inc(v_head_1259_);
v_tail_1260_ = lean_ctor_get(v_x_1257_, 1);
lean_inc(v_tail_1260_);
lean_dec_ref_known(v_x_1257_, 2);
v_fst_1261_ = lean_ctor_get(v_head_1259_, 0);
lean_inc(v_fst_1261_);
v_snd_1262_ = lean_ctor_get(v_head_1259_, 1);
lean_inc(v_snd_1262_);
lean_dec(v_head_1259_);
v___x_1263_ = lean_nat_to_int(v_fst_1261_);
v___x_1264_ = lean_int_mul(v___x_1263_, v_snd_1262_);
lean_dec(v_snd_1262_);
lean_dec(v___x_1263_);
v___x_1265_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedChshSum(v_tail_1260_);
v___x_1266_ = lean_int_add(v___x_1264_, v___x_1265_);
lean_dec(v___x_1265_);
lean_dec(v___x_1264_);
return v___x_1266_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_totalWeight_match__1_splitter___redArg(lean_object* v_x_1267_, lean_object* v_h__1_1268_, lean_object* v_h__2_1269_){
_start:
{
if (lean_obj_tag(v_x_1267_) == 0)
{
lean_object* v___x_1270_; lean_object* v___x_1271_; 
lean_dec(v_h__2_1269_);
v___x_1270_ = lean_box(0);
v___x_1271_ = lean_apply_1(v_h__1_1268_, v___x_1270_);
return v___x_1271_;
}
else
{
lean_object* v_head_1272_; lean_object* v_tail_1273_; lean_object* v_fst_1274_; lean_object* v_snd_1275_; lean_object* v___x_1276_; 
lean_dec(v_h__1_1268_);
v_head_1272_ = lean_ctor_get(v_x_1267_, 0);
lean_inc(v_head_1272_);
v_tail_1273_ = lean_ctor_get(v_x_1267_, 1);
lean_inc(v_tail_1273_);
lean_dec_ref_known(v_x_1267_, 2);
v_fst_1274_ = lean_ctor_get(v_head_1272_, 0);
lean_inc(v_fst_1274_);
v_snd_1275_ = lean_ctor_get(v_head_1272_, 1);
lean_inc(v_snd_1275_);
lean_dec(v_head_1272_);
v___x_1276_ = lean_apply_3(v_h__2_1269_, v_fst_1274_, v_snd_1275_, v_tail_1273_);
return v___x_1276_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_totalWeight_match__1_splitter(lean_object* v_motive_1277_, lean_object* v_x_1278_, lean_object* v_h__1_1279_, lean_object* v_h__2_1280_){
_start:
{
if (lean_obj_tag(v_x_1278_) == 0)
{
lean_object* v___x_1281_; lean_object* v___x_1282_; 
lean_dec(v_h__2_1280_);
v___x_1281_ = lean_box(0);
v___x_1282_ = lean_apply_1(v_h__1_1279_, v___x_1281_);
return v___x_1282_;
}
else
{
lean_object* v_head_1283_; lean_object* v_tail_1284_; lean_object* v_fst_1285_; lean_object* v_snd_1286_; lean_object* v___x_1287_; 
lean_dec(v_h__1_1279_);
v_head_1283_ = lean_ctor_get(v_x_1278_, 0);
lean_inc(v_head_1283_);
v_tail_1284_ = lean_ctor_get(v_x_1278_, 1);
lean_inc(v_tail_1284_);
lean_dec_ref_known(v_x_1278_, 2);
v_fst_1285_ = lean_ctor_get(v_head_1283_, 0);
lean_inc(v_fst_1285_);
v_snd_1286_ = lean_ctor_get(v_head_1283_, 1);
lean_inc(v_snd_1286_);
lean_dec(v_head_1283_);
v___x_1287_ = lean_apply_3(v_h__2_1280_, v_fst_1285_, v_snd_1286_, v_tail_1284_);
return v___x_1287_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mat2Det(lean_object* v_A_1288_){
_start:
{
lean_object* v_m00_1289_; lean_object* v_m01_1290_; lean_object* v_m10_1291_; lean_object* v_m11_1292_; lean_object* v___x_1293_; lean_object* v___x_1294_; lean_object* v___x_1295_; 
v_m00_1289_ = lean_ctor_get(v_A_1288_, 0);
v_m01_1290_ = lean_ctor_get(v_A_1288_, 1);
v_m10_1291_ = lean_ctor_get(v_A_1288_, 2);
v_m11_1292_ = lean_ctor_get(v_A_1288_, 3);
v___x_1293_ = lean_int_mul(v_m00_1289_, v_m11_1292_);
v___x_1294_ = lean_int_mul(v_m01_1290_, v_m10_1291_);
v___x_1295_ = lean_int_sub(v___x_1293_, v___x_1294_);
lean_dec(v___x_1294_);
lean_dec(v___x_1293_);
return v___x_1295_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mat2Det___boxed(lean_object* v_A_1296_){
_start:
{
lean_object* v_res_1297_; 
v_res_1297_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mat2Det(v_A_1296_);
lean_dec_ref(v_A_1296_);
return v_res_1297_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__0(void){
_start:
{
lean_object* v___x_1298_; lean_object* v___x_1299_; lean_object* v___x_1300_; 
v___x_1298_ = lean_unsigned_to_nat(9u);
v___x_1299_ = lean_unsigned_to_nat(0u);
v___x_1300_ = lean_nat_mod(v___x_1299_, v___x_1298_);
return v___x_1300_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__1(void){
_start:
{
lean_object* v___x_1301_; lean_object* v___x_1302_; lean_object* v___x_1303_; 
v___x_1301_ = lean_unsigned_to_nat(9u);
v___x_1302_ = lean_unsigned_to_nat(1u);
v___x_1303_ = lean_nat_mod(v___x_1302_, v___x_1301_);
return v___x_1303_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__2(void){
_start:
{
lean_object* v___x_1304_; lean_object* v___x_1305_; lean_object* v___x_1306_; 
v___x_1304_ = lean_unsigned_to_nat(9u);
v___x_1305_ = lean_unsigned_to_nat(2u);
v___x_1306_ = lean_nat_mod(v___x_1305_, v___x_1304_);
return v___x_1306_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__3(void){
_start:
{
lean_object* v___x_1307_; lean_object* v___x_1308_; 
v___x_1307_ = lean_unsigned_to_nat(2u);
v___x_1308_ = lean_nat_mod(v___x_1307_, v___x_1307_);
return v___x_1308_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__4(void){
_start:
{
lean_object* v___x_1309_; lean_object* v___x_1310_; lean_object* v___x_1311_; 
v___x_1309_ = lean_unsigned_to_nat(9u);
v___x_1310_ = lean_unsigned_to_nat(3u);
v___x_1311_ = lean_nat_mod(v___x_1310_, v___x_1309_);
return v___x_1311_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__5(void){
_start:
{
lean_object* v___x_1312_; lean_object* v___x_1313_; lean_object* v___x_1314_; 
v___x_1312_ = lean_unsigned_to_nat(9u);
v___x_1313_ = lean_unsigned_to_nat(4u);
v___x_1314_ = lean_nat_mod(v___x_1313_, v___x_1312_);
return v___x_1314_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__6(void){
_start:
{
lean_object* v___x_1315_; lean_object* v___x_1316_; lean_object* v___x_1317_; 
v___x_1315_ = lean_unsigned_to_nat(9u);
v___x_1316_ = lean_unsigned_to_nat(5u);
v___x_1317_ = lean_nat_mod(v___x_1316_, v___x_1315_);
return v___x_1317_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__7(void){
_start:
{
lean_object* v___x_1318_; lean_object* v___x_1319_; lean_object* v___x_1320_; 
v___x_1318_ = lean_unsigned_to_nat(2u);
v___x_1319_ = lean_unsigned_to_nat(0u);
v___x_1320_ = lean_nat_mod(v___x_1319_, v___x_1318_);
return v___x_1320_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__8(void){
_start:
{
lean_object* v___x_1321_; lean_object* v___x_1322_; lean_object* v___x_1323_; 
v___x_1321_ = lean_unsigned_to_nat(9u);
v___x_1322_ = lean_unsigned_to_nat(6u);
v___x_1323_ = lean_nat_mod(v___x_1322_, v___x_1321_);
return v___x_1323_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__9(void){
_start:
{
lean_object* v___x_1324_; lean_object* v___x_1325_; lean_object* v___x_1326_; 
v___x_1324_ = lean_unsigned_to_nat(9u);
v___x_1325_ = lean_unsigned_to_nat(7u);
v___x_1326_ = lean_nat_mod(v___x_1325_, v___x_1324_);
return v___x_1326_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__10(void){
_start:
{
lean_object* v___x_1327_; lean_object* v___x_1328_; lean_object* v___x_1329_; 
v___x_1327_ = lean_unsigned_to_nat(9u);
v___x_1328_ = lean_unsigned_to_nat(8u);
v___x_1329_ = lean_nat_mod(v___x_1328_, v___x_1327_);
return v___x_1329_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__11(void){
_start:
{
lean_object* v___x_1330_; lean_object* v___x_1331_; lean_object* v___x_1332_; 
v___x_1330_ = lean_unsigned_to_nat(2u);
v___x_1331_ = lean_unsigned_to_nat(1u);
v___x_1332_ = lean_nat_mod(v___x_1331_, v___x_1330_);
return v___x_1332_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent(lean_object* v_s_1333_){
_start:
{
lean_object* v___x_1334_; lean_object* v___x_1335_; lean_object* v___x_1336_; lean_object* v___x_1337_; lean_object* v___x_1338_; lean_object* v___x_1339_; lean_object* v___x_1340_; lean_object* v___x_1341_; lean_object* v___x_1342_; lean_object* v___x_1343_; lean_object* v_r0_1344_; lean_object* v___x_1345_; lean_object* v___x_1346_; lean_object* v___x_1347_; lean_object* v___x_1348_; lean_object* v___x_1349_; lean_object* v___x_1350_; lean_object* v___x_1351_; uint8_t v___x_1352_; 
v___x_1334_ = lean_unsigned_to_nat(2u);
v___x_1335_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__0);
lean_inc_ref_n(v_s_1333_, 6);
v___x_1336_ = lean_apply_1(v_s_1333_, v___x_1335_);
v___x_1337_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__1, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__1_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__1);
v___x_1338_ = lean_apply_1(v_s_1333_, v___x_1337_);
v___x_1339_ = l_Fin_add(v___x_1334_, v___x_1336_, v___x_1338_);
v___x_1340_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__2, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__2_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__2);
v___x_1341_ = lean_apply_1(v_s_1333_, v___x_1340_);
v___x_1342_ = l_Fin_add(v___x_1334_, v___x_1339_, v___x_1341_);
lean_dec(v___x_1339_);
v___x_1343_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__3, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__3_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__3);
v_r0_1344_ = lean_nat_mod(v___x_1342_, v___x_1343_);
lean_dec(v___x_1342_);
v___x_1345_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__4, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__4_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__4);
v___x_1346_ = lean_apply_1(v_s_1333_, v___x_1345_);
v___x_1347_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__5, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__5_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__5);
v___x_1348_ = lean_apply_1(v_s_1333_, v___x_1347_);
v___x_1349_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__6, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__6_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__6);
v___x_1350_ = lean_apply_1(v_s_1333_, v___x_1349_);
v___x_1351_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__7);
v___x_1352_ = lean_nat_dec_eq(v_r0_1344_, v___x_1351_);
lean_dec(v_r0_1344_);
if (v___x_1352_ == 0)
{
lean_dec(v___x_1350_);
lean_dec(v___x_1348_);
lean_dec(v___x_1346_);
lean_dec(v___x_1341_);
lean_dec(v___x_1338_);
lean_dec(v___x_1336_);
lean_dec_ref(v_s_1333_);
return v___x_1352_;
}
else
{
lean_object* v___x_1353_; lean_object* v___x_1354_; lean_object* v_r1_1355_; uint8_t v___x_1356_; 
v___x_1353_ = l_Fin_add(v___x_1334_, v___x_1346_, v___x_1348_);
v___x_1354_ = l_Fin_add(v___x_1334_, v___x_1353_, v___x_1350_);
lean_dec(v___x_1353_);
v_r1_1355_ = lean_nat_mod(v___x_1354_, v___x_1343_);
lean_dec(v___x_1354_);
v___x_1356_ = lean_nat_dec_eq(v_r1_1355_, v___x_1351_);
lean_dec(v_r1_1355_);
if (v___x_1356_ == 0)
{
lean_dec(v___x_1350_);
lean_dec(v___x_1348_);
lean_dec(v___x_1346_);
lean_dec(v___x_1341_);
lean_dec(v___x_1338_);
lean_dec(v___x_1336_);
lean_dec_ref(v_s_1333_);
return v___x_1356_;
}
else
{
lean_object* v___x_1357_; lean_object* v___x_1358_; lean_object* v___x_1359_; lean_object* v___x_1360_; lean_object* v___x_1361_; lean_object* v___x_1362_; lean_object* v___x_1363_; lean_object* v___x_1364_; lean_object* v_r2_1365_; uint8_t v___x_1366_; 
v___x_1357_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__8);
lean_inc_ref_n(v_s_1333_, 2);
v___x_1358_ = lean_apply_1(v_s_1333_, v___x_1357_);
v___x_1359_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__9);
v___x_1360_ = lean_apply_1(v_s_1333_, v___x_1359_);
v___x_1361_ = l_Fin_add(v___x_1334_, v___x_1358_, v___x_1360_);
v___x_1362_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__10, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__10_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__10);
v___x_1363_ = lean_apply_1(v_s_1333_, v___x_1362_);
v___x_1364_ = l_Fin_add(v___x_1334_, v___x_1361_, v___x_1363_);
lean_dec(v___x_1361_);
v_r2_1365_ = lean_nat_mod(v___x_1364_, v___x_1343_);
lean_dec(v___x_1364_);
v___x_1366_ = lean_nat_dec_eq(v_r2_1365_, v___x_1351_);
lean_dec(v_r2_1365_);
if (v___x_1366_ == 0)
{
lean_dec(v___x_1363_);
lean_dec(v___x_1360_);
lean_dec(v___x_1358_);
lean_dec(v___x_1350_);
lean_dec(v___x_1348_);
lean_dec(v___x_1346_);
lean_dec(v___x_1341_);
lean_dec(v___x_1338_);
lean_dec(v___x_1336_);
return v___x_1366_;
}
else
{
lean_object* v___x_1367_; lean_object* v___x_1368_; lean_object* v_c0_1369_; uint8_t v___x_1370_; 
v___x_1367_ = l_Fin_add(v___x_1334_, v___x_1336_, v___x_1346_);
lean_dec(v___x_1346_);
lean_dec(v___x_1336_);
v___x_1368_ = l_Fin_add(v___x_1334_, v___x_1367_, v___x_1358_);
lean_dec(v___x_1358_);
lean_dec(v___x_1367_);
v_c0_1369_ = lean_nat_mod(v___x_1368_, v___x_1343_);
lean_dec(v___x_1368_);
v___x_1370_ = lean_nat_dec_eq(v_c0_1369_, v___x_1351_);
lean_dec(v_c0_1369_);
if (v___x_1370_ == 0)
{
lean_dec(v___x_1363_);
lean_dec(v___x_1360_);
lean_dec(v___x_1350_);
lean_dec(v___x_1348_);
lean_dec(v___x_1341_);
lean_dec(v___x_1338_);
return v___x_1370_;
}
else
{
lean_object* v___x_1371_; lean_object* v___x_1372_; lean_object* v_c1_1373_; uint8_t v___x_1374_; 
v___x_1371_ = l_Fin_add(v___x_1334_, v___x_1338_, v___x_1348_);
lean_dec(v___x_1348_);
lean_dec(v___x_1338_);
v___x_1372_ = l_Fin_add(v___x_1334_, v___x_1371_, v___x_1360_);
lean_dec(v___x_1360_);
lean_dec(v___x_1371_);
v_c1_1373_ = lean_nat_mod(v___x_1372_, v___x_1343_);
lean_dec(v___x_1372_);
v___x_1374_ = lean_nat_dec_eq(v_c1_1373_, v___x_1351_);
lean_dec(v_c1_1373_);
if (v___x_1374_ == 0)
{
lean_dec(v___x_1363_);
lean_dec(v___x_1350_);
lean_dec(v___x_1341_);
return v___x_1374_;
}
else
{
lean_object* v___x_1375_; lean_object* v___x_1376_; lean_object* v_c2_1377_; lean_object* v___x_1378_; uint8_t v___x_1379_; 
v___x_1375_ = l_Fin_add(v___x_1334_, v___x_1341_, v___x_1350_);
lean_dec(v___x_1350_);
lean_dec(v___x_1341_);
v___x_1376_ = l_Fin_add(v___x_1334_, v___x_1375_, v___x_1363_);
lean_dec(v___x_1363_);
lean_dec(v___x_1375_);
v_c2_1377_ = lean_nat_mod(v___x_1376_, v___x_1343_);
lean_dec(v___x_1376_);
v___x_1378_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__11, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__11_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___closed__11);
v___x_1379_ = lean_nat_dec_eq(v_c2_1377_, v___x_1378_);
lean_dec(v_c2_1377_);
return v___x_1379_;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent___boxed(lean_object* v_s_1380_){
_start:
{
uint8_t v_res_1381_; lean_object* v_r_1382_; 
v_res_1381_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_mpRowColConsistent(v_s_1380_);
v_r_1382_ = lean_box(v_res_1381_);
return v_r_1382_;
}
}
static lean_object* _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___closed__0(void){
_start:
{
lean_object* v___x_1383_; lean_object* v___x_1384_; lean_object* v___x_1385_; lean_object* v_Z_1386_; 
v___x_1383_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_k23PrimalAlt___closed__0);
v___x_1384_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprMat2Int_repr___redArg___closed__7);
v___x_1385_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v_Z_1386_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_Z_1386_, 0, v___x_1385_);
lean_ctor_set(v_Z_1386_, 1, v___x_1384_);
lean_ctor_set(v_Z_1386_, 2, v___x_1384_);
lean_ctor_set(v_Z_1386_, 3, v___x_1383_);
return v_Z_1386_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2(lean_object* v_A_1387_){
_start:
{
lean_object* v_Z_1388_; lean_object* v___x_1389_; lean_object* v___x_1390_; lean_object* v___x_1391_; 
v_Z_1388_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___closed__0, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___closed__0_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___closed__0);
v___x_1389_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(v_A_1387_, v_Z_1388_);
v___x_1390_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_mul(v_Z_1388_, v___x_1389_);
v___x_1391_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_Mat2Int_add(v_A_1387_, v___x_1390_);
return v___x_1391_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2___boxed(lean_object* v_A_1392_){
_start:
{
lean_object* v_res_1393_; 
v_res_1393_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_zPinch2(v_A_1392_);
lean_dec_ref(v_A_1392_);
return v_res_1393_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedL1Two(lean_object* v_w1_1394_, lean_object* v_w2_1395_, lean_object* v_r1_1396_, lean_object* v_r2_1397_){
_start:
{
lean_object* v___x_1398_; lean_object* v___x_1399_; lean_object* v___x_1400_; lean_object* v___x_1401_; lean_object* v___x_1402_; 
v___x_1398_ = lean_nat_abs(v_r1_1396_);
v___x_1399_ = lean_nat_mul(v_w1_1394_, v___x_1398_);
lean_dec(v___x_1398_);
v___x_1400_ = lean_nat_abs(v_r2_1397_);
v___x_1401_ = lean_nat_mul(v_w2_1395_, v___x_1400_);
lean_dec(v___x_1400_);
v___x_1402_ = lean_nat_add(v___x_1399_, v___x_1401_);
lean_dec(v___x_1401_);
lean_dec(v___x_1399_);
return v___x_1402_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedL1Two___boxed(lean_object* v_w1_1403_, lean_object* v_w2_1404_, lean_object* v_r1_1405_, lean_object* v_r2_1406_){
_start:
{
lean_object* v_res_1407_; 
v_res_1407_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_weightedL1Two(v_w1_1403_, v_w2_1404_, v_r1_1405_, v_r2_1406_);
lean_dec(v_r2_1406_);
lean_dec(v_r1_1405_);
lean_dec(v_w2_1404_);
lean_dec(v_w1_1403_);
return v_res_1407_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gAdd(lean_object* v_z1_1408_, lean_object* v_z2_1409_){
_start:
{
lean_object* v_fst_1410_; lean_object* v_snd_1411_; lean_object* v_fst_1412_; lean_object* v_snd_1413_; lean_object* v___x_1415_; uint8_t v_isShared_1416_; uint8_t v_isSharedCheck_1422_; 
v_fst_1410_ = lean_ctor_get(v_z1_1408_, 0);
v_snd_1411_ = lean_ctor_get(v_z1_1408_, 1);
v_fst_1412_ = lean_ctor_get(v_z2_1409_, 0);
v_snd_1413_ = lean_ctor_get(v_z2_1409_, 1);
v_isSharedCheck_1422_ = !lean_is_exclusive(v_z2_1409_);
if (v_isSharedCheck_1422_ == 0)
{
v___x_1415_ = v_z2_1409_;
v_isShared_1416_ = v_isSharedCheck_1422_;
goto v_resetjp_1414_;
}
else
{
lean_inc(v_snd_1413_);
lean_inc(v_fst_1412_);
lean_dec(v_z2_1409_);
v___x_1415_ = lean_box(0);
v_isShared_1416_ = v_isSharedCheck_1422_;
goto v_resetjp_1414_;
}
v_resetjp_1414_:
{
lean_object* v___x_1417_; lean_object* v___x_1418_; lean_object* v___x_1420_; 
v___x_1417_ = lean_int_add(v_fst_1410_, v_fst_1412_);
lean_dec(v_fst_1412_);
v___x_1418_ = lean_int_add(v_snd_1411_, v_snd_1413_);
lean_dec(v_snd_1413_);
if (v_isShared_1416_ == 0)
{
lean_ctor_set(v___x_1415_, 1, v___x_1418_);
lean_ctor_set(v___x_1415_, 0, v___x_1417_);
v___x_1420_ = v___x_1415_;
goto v_reusejp_1419_;
}
else
{
lean_object* v_reuseFailAlloc_1421_; 
v_reuseFailAlloc_1421_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1421_, 0, v___x_1417_);
lean_ctor_set(v_reuseFailAlloc_1421_, 1, v___x_1418_);
v___x_1420_ = v_reuseFailAlloc_1421_;
goto v_reusejp_1419_;
}
v_reusejp_1419_:
{
return v___x_1420_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gAdd___boxed(lean_object* v_z1_1423_, lean_object* v_z2_1424_){
_start:
{
lean_object* v_res_1425_; 
v_res_1425_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gAdd(v_z1_1423_, v_z2_1424_);
lean_dec_ref(v_z1_1423_);
return v_res_1425_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gConj(lean_object* v_z_1426_){
_start:
{
lean_object* v_fst_1427_; lean_object* v_snd_1428_; lean_object* v___x_1430_; uint8_t v_isShared_1431_; uint8_t v_isSharedCheck_1436_; 
v_fst_1427_ = lean_ctor_get(v_z_1426_, 0);
v_snd_1428_ = lean_ctor_get(v_z_1426_, 1);
v_isSharedCheck_1436_ = !lean_is_exclusive(v_z_1426_);
if (v_isSharedCheck_1436_ == 0)
{
v___x_1430_ = v_z_1426_;
v_isShared_1431_ = v_isSharedCheck_1436_;
goto v_resetjp_1429_;
}
else
{
lean_inc(v_snd_1428_);
lean_inc(v_fst_1427_);
lean_dec(v_z_1426_);
v___x_1430_ = lean_box(0);
v_isShared_1431_ = v_isSharedCheck_1436_;
goto v_resetjp_1429_;
}
v_resetjp_1429_:
{
lean_object* v___x_1432_; lean_object* v___x_1434_; 
v___x_1432_ = lean_int_neg(v_snd_1428_);
lean_dec(v_snd_1428_);
if (v_isShared_1431_ == 0)
{
lean_ctor_set(v___x_1430_, 1, v___x_1432_);
v___x_1434_ = v___x_1430_;
goto v_reusejp_1433_;
}
else
{
lean_object* v_reuseFailAlloc_1435_; 
v_reuseFailAlloc_1435_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1435_, 0, v_fst_1427_);
lean_ctor_set(v_reuseFailAlloc_1435_, 1, v___x_1432_);
v___x_1434_ = v_reuseFailAlloc_1435_;
goto v_reusejp_1433_;
}
v_reusejp_1433_:
{
return v___x_1434_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gMul(lean_object* v_z1_1437_, lean_object* v_z2_1438_){
_start:
{
lean_object* v_fst_1439_; lean_object* v_snd_1440_; lean_object* v_fst_1441_; lean_object* v_snd_1442_; lean_object* v___x_1444_; uint8_t v_isShared_1445_; uint8_t v_isSharedCheck_1455_; 
v_fst_1439_ = lean_ctor_get(v_z1_1437_, 0);
v_snd_1440_ = lean_ctor_get(v_z1_1437_, 1);
v_fst_1441_ = lean_ctor_get(v_z2_1438_, 0);
v_snd_1442_ = lean_ctor_get(v_z2_1438_, 1);
v_isSharedCheck_1455_ = !lean_is_exclusive(v_z2_1438_);
if (v_isSharedCheck_1455_ == 0)
{
v___x_1444_ = v_z2_1438_;
v_isShared_1445_ = v_isSharedCheck_1455_;
goto v_resetjp_1443_;
}
else
{
lean_inc(v_snd_1442_);
lean_inc(v_fst_1441_);
lean_dec(v_z2_1438_);
v___x_1444_ = lean_box(0);
v_isShared_1445_ = v_isSharedCheck_1455_;
goto v_resetjp_1443_;
}
v_resetjp_1443_:
{
lean_object* v___x_1446_; lean_object* v___x_1447_; lean_object* v___x_1448_; lean_object* v___x_1449_; lean_object* v___x_1450_; lean_object* v___x_1451_; lean_object* v___x_1453_; 
v___x_1446_ = lean_int_mul(v_fst_1439_, v_fst_1441_);
v___x_1447_ = lean_int_mul(v_snd_1440_, v_snd_1442_);
v___x_1448_ = lean_int_sub(v___x_1446_, v___x_1447_);
lean_dec(v___x_1447_);
lean_dec(v___x_1446_);
v___x_1449_ = lean_int_mul(v_fst_1439_, v_snd_1442_);
lean_dec(v_snd_1442_);
v___x_1450_ = lean_int_mul(v_snd_1440_, v_fst_1441_);
lean_dec(v_fst_1441_);
v___x_1451_ = lean_int_add(v___x_1449_, v___x_1450_);
lean_dec(v___x_1450_);
lean_dec(v___x_1449_);
if (v_isShared_1445_ == 0)
{
lean_ctor_set(v___x_1444_, 1, v___x_1451_);
lean_ctor_set(v___x_1444_, 0, v___x_1448_);
v___x_1453_ = v___x_1444_;
goto v_reusejp_1452_;
}
else
{
lean_object* v_reuseFailAlloc_1454_; 
v_reuseFailAlloc_1454_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1454_, 0, v___x_1448_);
lean_ctor_set(v_reuseFailAlloc_1454_, 1, v___x_1451_);
v___x_1453_ = v_reuseFailAlloc_1454_;
goto v_reusejp_1452_;
}
v_reusejp_1452_:
{
return v___x_1453_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gMul___boxed(lean_object* v_z1_1456_, lean_object* v_z2_1457_){
_start:
{
lean_object* v_res_1458_; 
v_res_1458_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gMul(v_z1_1456_, v_z2_1457_);
lean_dec_ref(v_z1_1456_);
return v_res_1458_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gNormSq(lean_object* v_z_1459_){
_start:
{
lean_object* v_fst_1460_; lean_object* v_snd_1461_; lean_object* v___x_1462_; lean_object* v___x_1463_; lean_object* v___x_1464_; 
v_fst_1460_ = lean_ctor_get(v_z_1459_, 0);
v_snd_1461_ = lean_ctor_get(v_z_1459_, 1);
v___x_1462_ = lean_int_mul(v_fst_1460_, v_fst_1460_);
v___x_1463_ = lean_int_mul(v_snd_1461_, v_snd_1461_);
v___x_1464_ = lean_int_add(v___x_1462_, v___x_1463_);
lean_dec(v___x_1463_);
lean_dec(v___x_1462_);
return v___x_1464_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gNormSq___boxed(lean_object* v_z_1465_){
_start:
{
lean_object* v_res_1466_; 
v_res_1466_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_gNormSq(v_z_1465_);
lean_dec_ref(v_z_1465_);
return v_res_1466_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx(uint8_t v_x_1467_){
_start:
{
switch(v_x_1467_)
{
case 0:
{
lean_object* v___x_1468_; 
v___x_1468_ = lean_unsigned_to_nat(0u);
return v___x_1468_;
}
case 1:
{
lean_object* v___x_1469_; 
v___x_1469_ = lean_unsigned_to_nat(1u);
return v___x_1469_;
}
case 2:
{
lean_object* v___x_1470_; 
v___x_1470_ = lean_unsigned_to_nat(2u);
return v___x_1470_;
}
case 3:
{
lean_object* v___x_1471_; 
v___x_1471_ = lean_unsigned_to_nat(3u);
return v___x_1471_;
}
case 4:
{
lean_object* v___x_1472_; 
v___x_1472_ = lean_unsigned_to_nat(4u);
return v___x_1472_;
}
default: 
{
lean_object* v___x_1473_; 
v___x_1473_ = lean_unsigned_to_nat(5u);
return v___x_1473_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx___boxed(lean_object* v_x_1474_){
_start:
{
uint8_t v_x_boxed_1475_; lean_object* v_res_1476_; 
v_x_boxed_1475_ = lean_unbox(v_x_1474_);
v_res_1476_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx(v_x_boxed_1475_);
return v_res_1476_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_toCtorIdx(uint8_t v_x_1477_){
_start:
{
lean_object* v___x_1478_; 
v___x_1478_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx(v_x_1477_);
return v___x_1478_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_toCtorIdx___boxed(lean_object* v_x_1479_){
_start:
{
uint8_t v_x_4__boxed_1480_; lean_object* v_res_1481_; 
v_x_4__boxed_1480_ = lean_unbox(v_x_1479_);
v_res_1481_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_toCtorIdx(v_x_4__boxed_1480_);
return v_res_1481_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___redArg(lean_object* v_k_1482_){
_start:
{
lean_inc(v_k_1482_);
return v_k_1482_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___redArg___boxed(lean_object* v_k_1483_){
_start:
{
lean_object* v_res_1484_; 
v_res_1484_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___redArg(v_k_1483_);
lean_dec(v_k_1483_);
return v_res_1484_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim(lean_object* v_motive_1485_, lean_object* v_ctorIdx_1486_, uint8_t v_t_1487_, lean_object* v_h_1488_, lean_object* v_k_1489_){
_start:
{
lean_inc(v_k_1489_);
return v_k_1489_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim___boxed(lean_object* v_motive_1490_, lean_object* v_ctorIdx_1491_, lean_object* v_t_1492_, lean_object* v_h_1493_, lean_object* v_k_1494_){
_start:
{
uint8_t v_t_boxed_1495_; lean_object* v_res_1496_; 
v_t_boxed_1495_ = lean_unbox(v_t_1492_);
v_res_1496_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorElim(v_motive_1490_, v_ctorIdx_1491_, v_t_boxed_1495_, v_h_1493_, v_k_1494_);
lean_dec(v_k_1494_);
lean_dec(v_ctorIdx_1491_);
return v_res_1496_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___redArg(lean_object* v_mention_1497_){
_start:
{
lean_inc(v_mention_1497_);
return v_mention_1497_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___redArg___boxed(lean_object* v_mention_1498_){
_start:
{
lean_object* v_res_1499_; 
v_res_1499_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___redArg(v_mention_1498_);
lean_dec(v_mention_1498_);
return v_res_1499_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim(lean_object* v_motive_1500_, uint8_t v_t_1501_, lean_object* v_h_1502_, lean_object* v_mention_1503_){
_start:
{
lean_inc(v_mention_1503_);
return v_mention_1503_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim___boxed(lean_object* v_motive_1504_, lean_object* v_t_1505_, lean_object* v_h_1506_, lean_object* v_mention_1507_){
_start:
{
uint8_t v_t_boxed_1508_; lean_object* v_res_1509_; 
v_t_boxed_1508_ = lean_unbox(v_t_1505_);
v_res_1509_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_mention_elim(v_motive_1504_, v_t_boxed_1508_, v_h_1506_, v_mention_1507_);
lean_dec(v_mention_1507_);
return v_res_1509_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___redArg(lean_object* v_supply_1510_){
_start:
{
lean_inc(v_supply_1510_);
return v_supply_1510_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___redArg___boxed(lean_object* v_supply_1511_){
_start:
{
lean_object* v_res_1512_; 
v_res_1512_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___redArg(v_supply_1511_);
lean_dec(v_supply_1511_);
return v_res_1512_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim(lean_object* v_motive_1513_, uint8_t v_t_1514_, lean_object* v_h_1515_, lean_object* v_supply_1516_){
_start:
{
lean_inc(v_supply_1516_);
return v_supply_1516_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim___boxed(lean_object* v_motive_1517_, lean_object* v_t_1518_, lean_object* v_h_1519_, lean_object* v_supply_1520_){
_start:
{
uint8_t v_t_boxed_1521_; lean_object* v_res_1522_; 
v_t_boxed_1521_ = lean_unbox(v_t_1518_);
v_res_1522_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_supply_elim(v_motive_1517_, v_t_boxed_1521_, v_h_1519_, v_supply_1520_);
lean_dec(v_supply_1520_);
return v_res_1522_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___redArg(lean_object* v_designate_1523_){
_start:
{
lean_inc(v_designate_1523_);
return v_designate_1523_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___redArg___boxed(lean_object* v_designate_1524_){
_start:
{
lean_object* v_res_1525_; 
v_res_1525_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___redArg(v_designate_1524_);
lean_dec(v_designate_1524_);
return v_res_1525_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim(lean_object* v_motive_1526_, uint8_t v_t_1527_, lean_object* v_h_1528_, lean_object* v_designate_1529_){
_start:
{
lean_inc(v_designate_1529_);
return v_designate_1529_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim___boxed(lean_object* v_motive_1530_, lean_object* v_t_1531_, lean_object* v_h_1532_, lean_object* v_designate_1533_){
_start:
{
uint8_t v_t_boxed_1534_; lean_object* v_res_1535_; 
v_t_boxed_1534_ = lean_unbox(v_t_1531_);
v_res_1535_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_designate_elim(v_motive_1530_, v_t_boxed_1534_, v_h_1532_, v_designate_1533_);
lean_dec(v_designate_1533_);
return v_res_1535_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___redArg(lean_object* v_admit_1536_){
_start:
{
lean_inc(v_admit_1536_);
return v_admit_1536_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___redArg___boxed(lean_object* v_admit_1537_){
_start:
{
lean_object* v_res_1538_; 
v_res_1538_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___redArg(v_admit_1537_);
lean_dec(v_admit_1537_);
return v_res_1538_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim(lean_object* v_motive_1539_, uint8_t v_t_1540_, lean_object* v_h_1541_, lean_object* v_admit_1542_){
_start:
{
lean_inc(v_admit_1542_);
return v_admit_1542_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim___boxed(lean_object* v_motive_1543_, lean_object* v_t_1544_, lean_object* v_h_1545_, lean_object* v_admit_1546_){
_start:
{
uint8_t v_t_boxed_1547_; lean_object* v_res_1548_; 
v_t_boxed_1547_ = lean_unbox(v_t_1544_);
v_res_1548_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_admit_elim(v_motive_1543_, v_t_boxed_1547_, v_h_1545_, v_admit_1546_);
lean_dec(v_admit_1546_);
return v_res_1548_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___redArg(lean_object* v_retain_1549_){
_start:
{
lean_inc(v_retain_1549_);
return v_retain_1549_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___redArg___boxed(lean_object* v_retain_1550_){
_start:
{
lean_object* v_res_1551_; 
v_res_1551_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___redArg(v_retain_1550_);
lean_dec(v_retain_1550_);
return v_res_1551_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim(lean_object* v_motive_1552_, uint8_t v_t_1553_, lean_object* v_h_1554_, lean_object* v_retain_1555_){
_start:
{
lean_inc(v_retain_1555_);
return v_retain_1555_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim___boxed(lean_object* v_motive_1556_, lean_object* v_t_1557_, lean_object* v_h_1558_, lean_object* v_retain_1559_){
_start:
{
uint8_t v_t_boxed_1560_; lean_object* v_res_1561_; 
v_t_boxed_1560_ = lean_unbox(v_t_1557_);
v_res_1561_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_retain_elim(v_motive_1556_, v_t_boxed_1560_, v_h_1558_, v_retain_1559_);
lean_dec(v_retain_1559_);
return v_res_1561_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___redArg(lean_object* v_operate_1562_){
_start:
{
lean_inc(v_operate_1562_);
return v_operate_1562_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___redArg___boxed(lean_object* v_operate_1563_){
_start:
{
lean_object* v_res_1564_; 
v_res_1564_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___redArg(v_operate_1563_);
lean_dec(v_operate_1563_);
return v_res_1564_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim(lean_object* v_motive_1565_, uint8_t v_t_1566_, lean_object* v_h_1567_, lean_object* v_operate_1568_){
_start:
{
lean_inc(v_operate_1568_);
return v_operate_1568_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim___boxed(lean_object* v_motive_1569_, lean_object* v_t_1570_, lean_object* v_h_1571_, lean_object* v_operate_1572_){
_start:
{
uint8_t v_t_boxed_1573_; lean_object* v_res_1574_; 
v_t_boxed_1573_ = lean_unbox(v_t_1570_);
v_res_1574_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_operate_elim(v_motive_1569_, v_t_boxed_1573_, v_h_1571_, v_operate_1572_);
lean_dec(v_operate_1572_);
return v_res_1574_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ofNat(lean_object* v_n_1575_){
_start:
{
lean_object* v___x_1576_; uint8_t v___x_1577_; 
v___x_1576_ = lean_unsigned_to_nat(2u);
v___x_1577_ = lean_nat_dec_le(v_n_1575_, v___x_1576_);
if (v___x_1577_ == 0)
{
lean_object* v___x_1578_; uint8_t v___x_1579_; 
v___x_1578_ = lean_unsigned_to_nat(3u);
v___x_1579_ = lean_nat_dec_le(v_n_1575_, v___x_1578_);
if (v___x_1579_ == 0)
{
lean_object* v___x_1580_; uint8_t v___x_1581_; 
v___x_1580_ = lean_unsigned_to_nat(4u);
v___x_1581_ = lean_nat_dec_le(v_n_1575_, v___x_1580_);
if (v___x_1581_ == 0)
{
uint8_t v___x_1582_; 
v___x_1582_ = 5;
return v___x_1582_;
}
else
{
uint8_t v___x_1583_; 
v___x_1583_ = 4;
return v___x_1583_;
}
}
else
{
uint8_t v___x_1584_; 
v___x_1584_ = 3;
return v___x_1584_;
}
}
else
{
lean_object* v___x_1585_; uint8_t v___x_1586_; 
v___x_1585_ = lean_unsigned_to_nat(0u);
v___x_1586_ = lean_nat_dec_le(v_n_1575_, v___x_1585_);
if (v___x_1586_ == 0)
{
lean_object* v___x_1587_; uint8_t v___x_1588_; 
v___x_1587_ = lean_unsigned_to_nat(1u);
v___x_1588_ = lean_nat_dec_le(v_n_1575_, v___x_1587_);
if (v___x_1588_ == 0)
{
uint8_t v___x_1589_; 
v___x_1589_ = 2;
return v___x_1589_;
}
else
{
uint8_t v___x_1590_; 
v___x_1590_ = 1;
return v___x_1590_;
}
}
else
{
uint8_t v___x_1591_; 
v___x_1591_ = 0;
return v___x_1591_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ofNat___boxed(lean_object* v_n_1592_){
_start:
{
uint8_t v_res_1593_; lean_object* v_r_1594_; 
v_res_1593_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ofNat(v_n_1592_);
lean_dec(v_n_1592_);
v_r_1594_ = lean_box(v_res_1593_);
return v_r_1594_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPreGenOp(uint8_t v_x_1595_, uint8_t v_y_1596_){
_start:
{
lean_object* v___x_1597_; lean_object* v___x_1598_; uint8_t v___x_1599_; 
v___x_1597_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx(v_x_1595_);
v___x_1598_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_PreGenOp_ctorIdx(v_y_1596_);
v___x_1599_ = lean_nat_dec_eq(v___x_1597_, v___x_1598_);
lean_dec(v___x_1598_);
lean_dec(v___x_1597_);
return v___x_1599_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPreGenOp___boxed(lean_object* v_x_1600_, lean_object* v_y_1601_){
_start:
{
uint8_t v_x_13__boxed_1602_; uint8_t v_y_14__boxed_1603_; uint8_t v_res_1604_; lean_object* v_r_1605_; 
v_x_13__boxed_1602_ = lean_unbox(v_x_1600_);
v_y_14__boxed_1603_ = lean_unbox(v_y_1601_);
v_res_1604_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instDecidableEqPreGenOp(v_x_13__boxed_1602_, v_y_14__boxed_1603_);
v_r_1605_ = lean_box(v_res_1604_);
return v_r_1605_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr(uint8_t v_x_1624_, lean_object* v_prec_1625_){
_start:
{
lean_object* v___y_1627_; lean_object* v___y_1634_; lean_object* v___y_1641_; lean_object* v___y_1648_; lean_object* v___y_1655_; lean_object* v___y_1662_; 
switch(v_x_1624_)
{
case 0:
{
lean_object* v___x_1668_; uint8_t v___x_1669_; 
v___x_1668_ = lean_unsigned_to_nat(1024u);
v___x_1669_ = lean_nat_dec_le(v___x_1668_, v_prec_1625_);
if (v___x_1669_ == 0)
{
lean_object* v___x_1670_; 
v___x_1670_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_1627_ = v___x_1670_;
goto v___jp_1626_;
}
else
{
lean_object* v___x_1671_; 
v___x_1671_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_1627_ = v___x_1671_;
goto v___jp_1626_;
}
}
case 1:
{
lean_object* v___x_1672_; uint8_t v___x_1673_; 
v___x_1672_ = lean_unsigned_to_nat(1024u);
v___x_1673_ = lean_nat_dec_le(v___x_1672_, v_prec_1625_);
if (v___x_1673_ == 0)
{
lean_object* v___x_1674_; 
v___x_1674_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_1634_ = v___x_1674_;
goto v___jp_1633_;
}
else
{
lean_object* v___x_1675_; 
v___x_1675_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_1634_ = v___x_1675_;
goto v___jp_1633_;
}
}
case 2:
{
lean_object* v___x_1676_; uint8_t v___x_1677_; 
v___x_1676_ = lean_unsigned_to_nat(1024u);
v___x_1677_ = lean_nat_dec_le(v___x_1676_, v_prec_1625_);
if (v___x_1677_ == 0)
{
lean_object* v___x_1678_; 
v___x_1678_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_1641_ = v___x_1678_;
goto v___jp_1640_;
}
else
{
lean_object* v___x_1679_; 
v___x_1679_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_1641_ = v___x_1679_;
goto v___jp_1640_;
}
}
case 3:
{
lean_object* v___x_1680_; uint8_t v___x_1681_; 
v___x_1680_ = lean_unsigned_to_nat(1024u);
v___x_1681_ = lean_nat_dec_le(v___x_1680_, v_prec_1625_);
if (v___x_1681_ == 0)
{
lean_object* v___x_1682_; 
v___x_1682_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_1648_ = v___x_1682_;
goto v___jp_1647_;
}
else
{
lean_object* v___x_1683_; 
v___x_1683_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_1648_ = v___x_1683_;
goto v___jp_1647_;
}
}
case 4:
{
lean_object* v___x_1684_; uint8_t v___x_1685_; 
v___x_1684_ = lean_unsigned_to_nat(1024u);
v___x_1685_ = lean_nat_dec_le(v___x_1684_, v_prec_1625_);
if (v___x_1685_ == 0)
{
lean_object* v___x_1686_; 
v___x_1686_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_1655_ = v___x_1686_;
goto v___jp_1654_;
}
else
{
lean_object* v___x_1687_; 
v___x_1687_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_1655_ = v___x_1687_;
goto v___jp_1654_;
}
}
default: 
{
lean_object* v___x_1688_; uint8_t v___x_1689_; 
v___x_1688_ = lean_unsigned_to_nat(1024u);
v___x_1689_ = lean_nat_dec_le(v___x_1688_, v_prec_1625_);
if (v___x_1689_ == 0)
{
lean_object* v___x_1690_; 
v___x_1690_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___y_1662_ = v___x_1690_;
goto v___jp_1661_;
}
else
{
lean_object* v___x_1691_; 
v___x_1691_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__9);
v___y_1662_ = v___x_1691_;
goto v___jp_1661_;
}
}
}
v___jp_1626_:
{
lean_object* v___x_1628_; lean_object* v___x_1629_; uint8_t v___x_1630_; lean_object* v___x_1631_; lean_object* v___x_1632_; 
v___x_1628_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__1));
lean_inc(v___y_1627_);
v___x_1629_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1629_, 0, v___y_1627_);
lean_ctor_set(v___x_1629_, 1, v___x_1628_);
v___x_1630_ = 0;
v___x_1631_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1631_, 0, v___x_1629_);
lean_ctor_set_uint8(v___x_1631_, sizeof(void*)*1, v___x_1630_);
v___x_1632_ = l_Repr_addAppParen(v___x_1631_, v_prec_1625_);
return v___x_1632_;
}
v___jp_1633_:
{
lean_object* v___x_1635_; lean_object* v___x_1636_; uint8_t v___x_1637_; lean_object* v___x_1638_; lean_object* v___x_1639_; 
v___x_1635_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__3));
lean_inc(v___y_1634_);
v___x_1636_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1636_, 0, v___y_1634_);
lean_ctor_set(v___x_1636_, 1, v___x_1635_);
v___x_1637_ = 0;
v___x_1638_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1638_, 0, v___x_1636_);
lean_ctor_set_uint8(v___x_1638_, sizeof(void*)*1, v___x_1637_);
v___x_1639_ = l_Repr_addAppParen(v___x_1638_, v_prec_1625_);
return v___x_1639_;
}
v___jp_1640_:
{
lean_object* v___x_1642_; lean_object* v___x_1643_; uint8_t v___x_1644_; lean_object* v___x_1645_; lean_object* v___x_1646_; 
v___x_1642_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__5));
lean_inc(v___y_1641_);
v___x_1643_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1643_, 0, v___y_1641_);
lean_ctor_set(v___x_1643_, 1, v___x_1642_);
v___x_1644_ = 0;
v___x_1645_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1645_, 0, v___x_1643_);
lean_ctor_set_uint8(v___x_1645_, sizeof(void*)*1, v___x_1644_);
v___x_1646_ = l_Repr_addAppParen(v___x_1645_, v_prec_1625_);
return v___x_1646_;
}
v___jp_1647_:
{
lean_object* v___x_1649_; lean_object* v___x_1650_; uint8_t v___x_1651_; lean_object* v___x_1652_; lean_object* v___x_1653_; 
v___x_1649_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__7));
lean_inc(v___y_1648_);
v___x_1650_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1650_, 0, v___y_1648_);
lean_ctor_set(v___x_1650_, 1, v___x_1649_);
v___x_1651_ = 0;
v___x_1652_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1652_, 0, v___x_1650_);
lean_ctor_set_uint8(v___x_1652_, sizeof(void*)*1, v___x_1651_);
v___x_1653_ = l_Repr_addAppParen(v___x_1652_, v_prec_1625_);
return v___x_1653_;
}
v___jp_1654_:
{
lean_object* v___x_1656_; lean_object* v___x_1657_; uint8_t v___x_1658_; lean_object* v___x_1659_; lean_object* v___x_1660_; 
v___x_1656_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__9));
lean_inc(v___y_1655_);
v___x_1657_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1657_, 0, v___y_1655_);
lean_ctor_set(v___x_1657_, 1, v___x_1656_);
v___x_1658_ = 0;
v___x_1659_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1659_, 0, v___x_1657_);
lean_ctor_set_uint8(v___x_1659_, sizeof(void*)*1, v___x_1658_);
v___x_1660_ = l_Repr_addAppParen(v___x_1659_, v_prec_1625_);
return v___x_1660_;
}
v___jp_1661_:
{
lean_object* v___x_1663_; lean_object* v___x_1664_; uint8_t v___x_1665_; lean_object* v___x_1666_; lean_object* v___x_1667_; 
v___x_1663_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___closed__11));
lean_inc(v___y_1662_);
v___x_1664_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_1664_, 0, v___y_1662_);
lean_ctor_set(v___x_1664_, 1, v___x_1663_);
v___x_1665_ = 0;
v___x_1666_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_1666_, 0, v___x_1664_);
lean_ctor_set_uint8(v___x_1666_, sizeof(void*)*1, v___x_1665_);
v___x_1667_ = l_Repr_addAppParen(v___x_1666_, v_prec_1625_);
return v___x_1667_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr___boxed(lean_object* v_x_1692_, lean_object* v_prec_1693_){
_start:
{
uint8_t v_x_341__boxed_1694_; lean_object* v_res_1695_; 
v_x_341__boxed_1694_ = lean_unbox(v_x_1692_);
v_res_1695_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPreGenOp_repr(v_x_341__boxed_1694_, v_prec_1693_);
lean_dec(v_prec_1693_);
return v_res_1695_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_applyPreGenOp(uint8_t v_op_1698_, lean_object* v_admittedCount_1699_){
_start:
{
if (v_op_1698_ == 3)
{
lean_object* v___x_1700_; lean_object* v___x_1701_; 
v___x_1700_ = lean_unsigned_to_nat(1u);
v___x_1701_ = lean_nat_add(v_admittedCount_1699_, v___x_1700_);
return v___x_1701_;
}
else
{
lean_inc(v_admittedCount_1699_);
return v_admittedCount_1699_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_applyPreGenOp___boxed(lean_object* v_op_1702_, lean_object* v_admittedCount_1703_){
_start:
{
uint8_t v_op_boxed_1704_; lean_object* v_res_1705_; 
v_op_boxed_1704_ = lean_unbox(v_op_1702_);
v_res_1705_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_applyPreGenOp(v_op_boxed_1704_, v_admittedCount_1703_);
lean_dec(v_admittedCount_1703_);
return v_res_1705_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___redArg(uint8_t v_op_1706_, lean_object* v_h__1_1707_, lean_object* v_h__2_1708_){
_start:
{
if (v_op_1706_ == 3)
{
lean_object* v___x_1709_; lean_object* v___x_1710_; 
lean_dec(v_h__2_1708_);
v___x_1709_ = lean_box(0);
v___x_1710_ = lean_apply_1(v_h__1_1707_, v___x_1709_);
return v___x_1710_;
}
else
{
lean_object* v___x_1711_; lean_object* v___x_1712_; 
lean_dec(v_h__1_1707_);
v___x_1711_ = lean_box(v_op_1706_);
v___x_1712_ = lean_apply_2(v_h__2_1708_, v___x_1711_, lean_box(0));
return v___x_1712_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___redArg___boxed(lean_object* v_op_1713_, lean_object* v_h__1_1714_, lean_object* v_h__2_1715_){
_start:
{
uint8_t v_op_17__boxed_1716_; lean_object* v_res_1717_; 
v_op_17__boxed_1716_ = lean_unbox(v_op_1713_);
v_res_1717_ = lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___redArg(v_op_17__boxed_1716_, v_h__1_1714_, v_h__2_1715_);
return v_res_1717_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter(lean_object* v_motive_1718_, uint8_t v_op_1719_, lean_object* v_h__1_1720_, lean_object* v_h__2_1721_){
_start:
{
if (v_op_1719_ == 3)
{
lean_object* v___x_1722_; lean_object* v___x_1723_; 
lean_dec(v_h__2_1721_);
v___x_1722_ = lean_box(0);
v___x_1723_ = lean_apply_1(v_h__1_1720_, v___x_1722_);
return v___x_1723_;
}
else
{
lean_object* v___x_1724_; lean_object* v___x_1725_; 
lean_dec(v_h__1_1720_);
v___x_1724_ = lean_box(v_op_1719_);
v___x_1725_ = lean_apply_2(v_h__2_1721_, v___x_1724_, lean_box(0));
return v___x_1725_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter___boxed(lean_object* v_motive_1726_, lean_object* v_op_1727_, lean_object* v_h__1_1728_, lean_object* v_h__2_1729_){
_start:
{
uint8_t v_op_28__boxed_1730_; lean_object* v_res_1731_; 
v_op_28__boxed_1730_ = lean_unbox(v_op_1727_);
v_res_1731_ = lp_FiniteQuantum___private_DerivationDagQMClosure_0__QuantumMechanics_DerivationDagQMClosure_applyPreGenOp_match__1_splitter(v_motive_1726_, v_op_28__boxed_1730_, v_h__1_1728_, v_h__2_1729_);
return v_res_1731_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities(lean_object* v_r_1744_){
_start:
{
lean_object* v___x_1745_; uint8_t v___x_1746_; 
v___x_1745_ = lean_unsigned_to_nat(0u);
v___x_1746_ = lean_nat_dec_eq(v_r_1744_, v___x_1745_);
if (v___x_1746_ == 0)
{
lean_object* v___x_1747_; uint8_t v___x_1748_; 
v___x_1747_ = lean_unsigned_to_nat(1u);
v___x_1748_ = lean_nat_dec_eq(v_r_1744_, v___x_1747_);
if (v___x_1748_ == 0)
{
lean_object* v___x_1758_; uint8_t v___x_1759_; 
v___x_1758_ = lean_unsigned_to_nat(2u);
v___x_1759_ = lean_nat_dec_eq(v_r_1744_, v___x_1758_);
if (v___x_1759_ == 0)
{
lean_object* v___x_1760_; uint8_t v___x_1761_; 
v___x_1760_ = lean_unsigned_to_nat(3u);
v___x_1761_ = lean_nat_dec_eq(v_r_1744_, v___x_1760_);
if (v___x_1761_ == 0)
{
lean_object* v___x_1762_; uint8_t v___x_1763_; 
v___x_1762_ = lean_unsigned_to_nat(4u);
v___x_1763_ = lean_nat_dec_eq(v_r_1744_, v___x_1762_);
if (v___x_1763_ == 0)
{
lean_object* v___x_1764_; uint8_t v___x_1765_; 
v___x_1764_ = lean_unsigned_to_nat(5u);
v___x_1765_ = lean_nat_dec_eq(v_r_1744_, v___x_1764_);
if (v___x_1765_ == 0)
{
lean_object* v___x_1766_; 
v___x_1766_ = ((lean_object*)(lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___closed__2));
return v___x_1766_;
}
else
{
lean_object* v___x_1767_; lean_object* v___x_1768_; lean_object* v___x_1769_; lean_object* v___x_1770_; lean_object* v___x_1771_; lean_object* v___x_1772_; lean_object* v___x_1773_; 
v___x_1767_ = lean_box(v___x_1763_);
v___x_1768_ = lean_box(v___x_1765_);
v___x_1769_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1769_, 0, v___x_1767_);
lean_ctor_set(v___x_1769_, 1, v___x_1768_);
v___x_1770_ = lean_box(v___x_1765_);
v___x_1771_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1771_, 0, v___x_1770_);
lean_ctor_set(v___x_1771_, 1, v___x_1769_);
v___x_1772_ = lean_box(v___x_1763_);
v___x_1773_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1773_, 0, v___x_1772_);
lean_ctor_set(v___x_1773_, 1, v___x_1771_);
return v___x_1773_;
}
}
else
{
lean_object* v___x_1774_; lean_object* v___x_1775_; lean_object* v___x_1776_; lean_object* v___x_1777_; lean_object* v___x_1778_; lean_object* v___x_1779_; lean_object* v___x_1780_; 
v___x_1774_ = lean_box(v___x_1763_);
v___x_1775_ = lean_box(v___x_1761_);
v___x_1776_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1776_, 0, v___x_1774_);
lean_ctor_set(v___x_1776_, 1, v___x_1775_);
v___x_1777_ = lean_box(v___x_1763_);
v___x_1778_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1778_, 0, v___x_1777_);
lean_ctor_set(v___x_1778_, 1, v___x_1776_);
v___x_1779_ = lean_box(v___x_1763_);
v___x_1780_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1780_, 0, v___x_1779_);
lean_ctor_set(v___x_1780_, 1, v___x_1778_);
return v___x_1780_;
}
}
else
{
goto v___jp_1749_;
}
}
else
{
goto v___jp_1749_;
}
}
else
{
lean_object* v___x_1781_; lean_object* v___x_1782_; lean_object* v___x_1783_; lean_object* v___x_1784_; lean_object* v___x_1785_; lean_object* v___x_1786_; lean_object* v___x_1787_; 
v___x_1781_ = lean_box(v___x_1746_);
v___x_1782_ = lean_box(v___x_1748_);
v___x_1783_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1783_, 0, v___x_1781_);
lean_ctor_set(v___x_1783_, 1, v___x_1782_);
v___x_1784_ = lean_box(v___x_1746_);
v___x_1785_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1785_, 0, v___x_1784_);
lean_ctor_set(v___x_1785_, 1, v___x_1783_);
v___x_1786_ = lean_box(v___x_1748_);
v___x_1787_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1787_, 0, v___x_1786_);
lean_ctor_set(v___x_1787_, 1, v___x_1785_);
return v___x_1787_;
}
v___jp_1749_:
{
uint8_t v___x_1750_; lean_object* v___x_1751_; lean_object* v___x_1752_; lean_object* v___x_1753_; lean_object* v___x_1754_; lean_object* v___x_1755_; lean_object* v___x_1756_; lean_object* v___x_1757_; 
v___x_1750_ = 1;
v___x_1751_ = lean_box(v___x_1748_);
v___x_1752_ = lean_box(v___x_1750_);
v___x_1753_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1753_, 0, v___x_1751_);
lean_ctor_set(v___x_1753_, 1, v___x_1752_);
v___x_1754_ = lean_box(v___x_1750_);
v___x_1755_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1755_, 0, v___x_1754_);
lean_ctor_set(v___x_1755_, 1, v___x_1753_);
v___x_1756_ = lean_box(v___x_1750_);
v___x_1757_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1757_, 0, v___x_1756_);
lean_ctor_set(v___x_1757_, 1, v___x_1755_);
return v___x_1757_;
}
}
else
{
uint8_t v___x_1788_; lean_object* v___x_1789_; lean_object* v___x_1790_; lean_object* v___x_1791_; lean_object* v___x_1792_; lean_object* v___x_1793_; lean_object* v___x_1794_; lean_object* v___x_1795_; 
v___x_1788_ = 0;
v___x_1789_ = lean_box(v___x_1746_);
v___x_1790_ = lean_box(v___x_1746_);
v___x_1791_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1791_, 0, v___x_1789_);
lean_ctor_set(v___x_1791_, 1, v___x_1790_);
v___x_1792_ = lean_box(v___x_1788_);
v___x_1793_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1793_, 0, v___x_1792_);
lean_ctor_set(v___x_1793_, 1, v___x_1791_);
v___x_1794_ = lean_box(v___x_1788_);
v___x_1795_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_1795_, 0, v___x_1794_);
lean_ctor_set(v___x_1795_, 1, v___x_1793_);
return v___x_1795_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities___boxed(lean_object* v_r_1796_){
_start:
{
lean_object* v_res_1797_; 
v_res_1797_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities(v_r_1796_);
lean_dec(v_r_1796_);
return v_res_1797_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowAdmits(lean_object* v_r_1798_){
_start:
{
lean_object* v___x_1799_; lean_object* v_snd_1800_; lean_object* v_snd_1801_; lean_object* v_fst_1802_; uint8_t v___x_1803_; 
v___x_1799_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowCapabilities(v_r_1798_);
v_snd_1800_ = lean_ctor_get(v___x_1799_, 1);
lean_inc(v_snd_1800_);
v_snd_1801_ = lean_ctor_get(v_snd_1800_, 1);
lean_inc(v_snd_1801_);
v_fst_1802_ = lean_ctor_get(v___x_1799_, 0);
lean_inc(v_fst_1802_);
lean_dec_ref(v___x_1799_);
v___x_1803_ = lean_unbox(v_fst_1802_);
if (v___x_1803_ == 0)
{
uint8_t v___x_1804_; 
lean_dec(v_snd_1801_);
lean_dec(v_snd_1800_);
v___x_1804_ = lean_unbox(v_fst_1802_);
lean_dec(v_fst_1802_);
return v___x_1804_;
}
else
{
lean_object* v_fst_1805_; uint8_t v___x_1806_; 
lean_dec(v_fst_1802_);
v_fst_1805_ = lean_ctor_get(v_snd_1800_, 0);
lean_inc(v_fst_1805_);
lean_dec(v_snd_1800_);
v___x_1806_ = lean_unbox(v_fst_1805_);
if (v___x_1806_ == 0)
{
uint8_t v___x_1807_; 
lean_dec(v_snd_1801_);
v___x_1807_ = lean_unbox(v_fst_1805_);
lean_dec(v_fst_1805_);
return v___x_1807_;
}
else
{
lean_object* v_fst_1808_; uint8_t v___x_1809_; 
lean_dec(v_fst_1805_);
v_fst_1808_ = lean_ctor_get(v_snd_1801_, 0);
v___x_1809_ = lean_unbox(v_fst_1808_);
if (v___x_1809_ == 0)
{
uint8_t v___x_1810_; 
lean_inc(v_fst_1808_);
lean_dec(v_snd_1801_);
v___x_1810_ = lean_unbox(v_fst_1808_);
lean_dec(v_fst_1808_);
return v___x_1810_;
}
else
{
lean_object* v_snd_1811_; uint8_t v___x_1812_; 
v_snd_1811_ = lean_ctor_get(v_snd_1801_, 1);
lean_inc(v_snd_1811_);
lean_dec(v_snd_1801_);
v___x_1812_ = lean_unbox(v_snd_1811_);
lean_dec(v_snd_1811_);
return v___x_1812_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowAdmits___boxed(lean_object* v_r_1813_){
_start:
{
uint8_t v_res_1814_; lean_object* v_r_1815_; 
v_res_1814_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_o022RowAdmits(v_r_1813_);
lean_dec(v_r_1813_);
v_r_1815_ = lean_box(v_res_1814_);
return v_r_1815_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm101ThresholdCertificate(uint8_t v_ob1_1816_, uint8_t v_ob2_1817_, uint8_t v_ob3_1818_, uint8_t v_ob4_1819_, uint8_t v_ob5_1820_, lean_object* v_muRepair_1821_, lean_object* v_lambdaProj_1822_){
_start:
{
if (v_ob1_1816_ == 0)
{
return v_ob1_1816_;
}
else
{
if (v_ob2_1817_ == 0)
{
return v_ob2_1817_;
}
else
{
if (v_ob3_1818_ == 0)
{
return v_ob3_1818_;
}
else
{
if (v_ob4_1819_ == 0)
{
return v_ob4_1819_;
}
else
{
if (v_ob5_1820_ == 0)
{
return v_ob5_1820_;
}
else
{
uint8_t v___x_1823_; 
v___x_1823_ = lean_nat_dec_le(v_lambdaProj_1822_, v_muRepair_1821_);
return v___x_1823_;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm101ThresholdCertificate___boxed(lean_object* v_ob1_1824_, lean_object* v_ob2_1825_, lean_object* v_ob3_1826_, lean_object* v_ob4_1827_, lean_object* v_ob5_1828_, lean_object* v_muRepair_1829_, lean_object* v_lambdaProj_1830_){
_start:
{
uint8_t v_ob1_boxed_1831_; uint8_t v_ob2_boxed_1832_; uint8_t v_ob3_boxed_1833_; uint8_t v_ob4_boxed_1834_; uint8_t v_ob5_boxed_1835_; uint8_t v_res_1836_; lean_object* v_r_1837_; 
v_ob1_boxed_1831_ = lean_unbox(v_ob1_1824_);
v_ob2_boxed_1832_ = lean_unbox(v_ob2_1825_);
v_ob3_boxed_1833_ = lean_unbox(v_ob3_1826_);
v_ob4_boxed_1834_ = lean_unbox(v_ob4_1827_);
v_ob5_boxed_1835_ = lean_unbox(v_ob5_1828_);
v_res_1836_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm101ThresholdCertificate(v_ob1_boxed_1831_, v_ob2_boxed_1832_, v_ob3_boxed_1833_, v_ob4_boxed_1834_, v_ob5_boxed_1835_, v_muRepair_1829_, v_lambdaProj_1830_);
lean_dec(v_lambdaProj_1830_);
lean_dec(v_muRepair_1829_);
v_r_1837_ = lean_box(v_res_1836_);
return v_r_1837_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm207To211StageAdmits(lean_object* v_stage_1838_, lean_object* v_imports_1839_){
_start:
{
lean_object* v___x_1840_; uint8_t v___x_1841_; 
v___x_1840_ = lean_unsigned_to_nat(0u);
v___x_1841_ = lean_nat_dec_eq(v_stage_1838_, v___x_1840_);
if (v___x_1841_ == 0)
{
lean_object* v___x_1842_; uint8_t v___x_1843_; 
v___x_1842_ = lean_unsigned_to_nat(1u);
v___x_1843_ = lean_nat_dec_eq(v_stage_1838_, v___x_1842_);
if (v___x_1843_ == 0)
{
lean_object* v___x_1844_; uint8_t v___x_1845_; 
v___x_1844_ = lean_unsigned_to_nat(2u);
v___x_1845_ = lean_nat_dec_eq(v_stage_1838_, v___x_1844_);
if (v___x_1845_ == 0)
{
lean_object* v___x_1846_; uint8_t v___x_1847_; 
v___x_1846_ = lean_unsigned_to_nat(3u);
v___x_1847_ = lean_nat_dec_eq(v_stage_1838_, v___x_1846_);
if (v___x_1847_ == 0)
{
lean_object* v___x_1848_; uint8_t v___x_1849_; 
lean_inc_ref(v_imports_1839_);
v___x_1848_ = lean_apply_1(v_imports_1839_, v___x_1840_);
v___x_1849_ = lean_unbox(v___x_1848_);
if (v___x_1849_ == 0)
{
uint8_t v___x_1850_; 
lean_dec_ref(v_imports_1839_);
v___x_1850_ = lean_unbox(v___x_1848_);
return v___x_1850_;
}
else
{
lean_object* v___x_1851_; uint8_t v___x_1852_; 
lean_inc_ref(v_imports_1839_);
v___x_1851_ = lean_apply_1(v_imports_1839_, v___x_1842_);
v___x_1852_ = lean_unbox(v___x_1851_);
if (v___x_1852_ == 0)
{
uint8_t v___x_1853_; 
lean_dec_ref(v_imports_1839_);
v___x_1853_ = lean_unbox(v___x_1851_);
return v___x_1853_;
}
else
{
lean_object* v___x_1854_; uint8_t v___x_1855_; 
lean_inc_ref(v_imports_1839_);
v___x_1854_ = lean_apply_1(v_imports_1839_, v___x_1844_);
v___x_1855_ = lean_unbox(v___x_1854_);
if (v___x_1855_ == 0)
{
uint8_t v___x_1856_; 
lean_dec_ref(v_imports_1839_);
v___x_1856_ = lean_unbox(v___x_1854_);
return v___x_1856_;
}
else
{
lean_object* v___x_1857_; uint8_t v___x_1858_; 
lean_inc_ref(v_imports_1839_);
v___x_1857_ = lean_apply_1(v_imports_1839_, v___x_1846_);
v___x_1858_ = lean_unbox(v___x_1857_);
if (v___x_1858_ == 0)
{
uint8_t v___x_1859_; 
lean_dec_ref(v_imports_1839_);
v___x_1859_ = lean_unbox(v___x_1857_);
return v___x_1859_;
}
else
{
lean_object* v___x_1860_; lean_object* v___x_1861_; uint8_t v___x_1862_; 
v___x_1860_ = lean_unsigned_to_nat(4u);
v___x_1861_ = lean_apply_1(v_imports_1839_, v___x_1860_);
v___x_1862_ = lean_unbox(v___x_1861_);
return v___x_1862_;
}
}
}
}
}
else
{
lean_object* v___x_1863_; uint8_t v___x_1864_; 
lean_inc_ref(v_imports_1839_);
v___x_1863_ = lean_apply_1(v_imports_1839_, v___x_1840_);
v___x_1864_ = lean_unbox(v___x_1863_);
if (v___x_1864_ == 0)
{
uint8_t v___x_1865_; 
lean_dec_ref(v_imports_1839_);
v___x_1865_ = lean_unbox(v___x_1863_);
return v___x_1865_;
}
else
{
lean_object* v___x_1866_; uint8_t v___x_1867_; 
lean_inc_ref(v_imports_1839_);
v___x_1866_ = lean_apply_1(v_imports_1839_, v___x_1842_);
v___x_1867_ = lean_unbox(v___x_1866_);
if (v___x_1867_ == 0)
{
uint8_t v___x_1868_; 
lean_dec_ref(v_imports_1839_);
v___x_1868_ = lean_unbox(v___x_1866_);
return v___x_1868_;
}
else
{
lean_object* v___x_1869_; uint8_t v___x_1870_; 
lean_inc_ref(v_imports_1839_);
v___x_1869_ = lean_apply_1(v_imports_1839_, v___x_1844_);
v___x_1870_ = lean_unbox(v___x_1869_);
if (v___x_1870_ == 0)
{
uint8_t v___x_1871_; 
lean_dec_ref(v_imports_1839_);
v___x_1871_ = lean_unbox(v___x_1869_);
return v___x_1871_;
}
else
{
lean_object* v___x_1872_; uint8_t v___x_1873_; 
v___x_1872_ = lean_apply_1(v_imports_1839_, v___x_1846_);
v___x_1873_ = lean_unbox(v___x_1872_);
return v___x_1873_;
}
}
}
}
}
else
{
lean_object* v___x_1874_; uint8_t v___x_1875_; 
lean_inc_ref(v_imports_1839_);
v___x_1874_ = lean_apply_1(v_imports_1839_, v___x_1840_);
v___x_1875_ = lean_unbox(v___x_1874_);
if (v___x_1875_ == 0)
{
uint8_t v___x_1876_; 
lean_dec_ref(v_imports_1839_);
v___x_1876_ = lean_unbox(v___x_1874_);
return v___x_1876_;
}
else
{
lean_object* v___x_1877_; uint8_t v___x_1878_; 
lean_inc_ref(v_imports_1839_);
v___x_1877_ = lean_apply_1(v_imports_1839_, v___x_1842_);
v___x_1878_ = lean_unbox(v___x_1877_);
if (v___x_1878_ == 0)
{
uint8_t v___x_1879_; 
lean_dec_ref(v_imports_1839_);
v___x_1879_ = lean_unbox(v___x_1877_);
return v___x_1879_;
}
else
{
lean_object* v___x_1880_; uint8_t v___x_1881_; 
v___x_1880_ = lean_apply_1(v_imports_1839_, v___x_1844_);
v___x_1881_ = lean_unbox(v___x_1880_);
return v___x_1881_;
}
}
}
}
else
{
lean_object* v___x_1882_; uint8_t v___x_1883_; 
lean_inc_ref(v_imports_1839_);
v___x_1882_ = lean_apply_1(v_imports_1839_, v___x_1840_);
v___x_1883_ = lean_unbox(v___x_1882_);
if (v___x_1883_ == 0)
{
uint8_t v___x_1884_; 
lean_dec_ref(v_imports_1839_);
v___x_1884_ = lean_unbox(v___x_1882_);
return v___x_1884_;
}
else
{
lean_object* v___x_1885_; uint8_t v___x_1886_; 
v___x_1885_ = lean_apply_1(v_imports_1839_, v___x_1842_);
v___x_1886_ = lean_unbox(v___x_1885_);
return v___x_1886_;
}
}
}
else
{
lean_object* v___x_1887_; uint8_t v___x_1888_; 
v___x_1887_ = lean_apply_1(v_imports_1839_, v___x_1840_);
v___x_1888_ = lean_unbox(v___x_1887_);
return v___x_1888_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm207To211StageAdmits___boxed(lean_object* v_stage_1889_, lean_object* v_imports_1890_){
_start:
{
uint8_t v_res_1891_; lean_object* v_r_1892_; 
v_res_1891_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm207To211StageAdmits(v_stage_1889_, v_imports_1890_);
lean_dec(v_stage_1889_);
v_r_1892_ = lean_box(v_res_1891_);
return v_r_1892_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockScopedFiniteHold(lean_object* v_x_1893_){
_start:
{
uint8_t v___x_1894_; 
v___x_1894_ = 1;
return v___x_1894_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockScopedFiniteHold___boxed(lean_object* v_x_1895_){
_start:
{
uint8_t v_res_1896_; lean_object* v_r_1897_; 
v_res_1896_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockScopedFiniteHold(v_x_1895_);
lean_dec(v_x_1895_);
v_r_1897_ = lean_box(v_res_1896_);
return v_r_1897_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockUnboundedTargetHold(lean_object* v_x_1898_){
_start:
{
uint8_t v___x_1899_; 
v___x_1899_ = 0;
return v___x_1899_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockUnboundedTargetHold___boxed(lean_object* v_x_1900_){
_start:
{
uint8_t v_res_1901_; lean_object* v_r_1902_; 
v_res_1901_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c500BlockUnboundedTargetHold(v_x_1900_);
lean_dec(v_x_1900_);
v_r_1902_ = lean_box(v_res_1901_);
return v_r_1902_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_readoutScaled(lean_object* v_t_1903_, lean_object* v_p_1904_){
_start:
{
lean_object* v___x_1905_; lean_object* v___x_1906_; lean_object* v___x_1907_; lean_object* v___x_1908_; 
v___x_1905_ = lean_obj_once(&lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8, &lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8_once, _init_lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_instReprPrimGenEvent_repr___closed__8);
v___x_1906_ = lean_int_sub(v___x_1905_, v_t_1903_);
v___x_1907_ = lean_int_mul(v___x_1906_, v_p_1904_);
lean_dec(v___x_1906_);
v___x_1908_ = lean_int_add(v___x_1907_, v_t_1903_);
lean_dec(v___x_1907_);
return v___x_1908_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_readoutScaled___boxed(lean_object* v_t_1909_, lean_object* v_p_1910_){
_start:
{
lean_object* v_res_1911_; 
v_res_1911_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_readoutScaled(v_t_1909_, v_p_1910_);
lean_dec(v_p_1910_);
lean_dec(v_t_1909_);
return v_res_1911_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizedStanding(uint8_t v_receiptValid_1912_, uint8_t v_standingMap_1913_){
_start:
{
if (v_receiptValid_1912_ == 0)
{
return v_receiptValid_1912_;
}
else
{
return v_standingMap_1913_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizedStanding___boxed(lean_object* v_receiptValid_1914_, lean_object* v_standingMap_1915_){
_start:
{
uint8_t v_receiptValid_boxed_1916_; uint8_t v_standingMap_boxed_1917_; uint8_t v_res_1918_; lean_object* v_r_1919_; 
v_receiptValid_boxed_1916_ = lean_unbox(v_receiptValid_1914_);
v_standingMap_boxed_1917_ = lean_unbox(v_standingMap_1915_);
v_res_1918_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_authorizedStanding(v_receiptValid_boxed_1916_, v_standingMap_boxed_1917_);
v_r_1919_ = lean_box(v_res_1918_);
return v_r_1919_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_c4Shift(lean_object* v_v_1949_){
_start:
{
lean_object* v_snd_1950_; lean_object* v_snd_1951_; lean_object* v_fst_1952_; lean_object* v___x_1954_; uint8_t v_isShared_1955_; uint8_t v_isSharedCheck_1977_; 
v_snd_1950_ = lean_ctor_get(v_v_1949_, 1);
lean_inc(v_snd_1950_);
v_snd_1951_ = lean_ctor_get(v_snd_1950_, 1);
lean_inc(v_snd_1951_);
v_fst_1952_ = lean_ctor_get(v_v_1949_, 0);
v_isSharedCheck_1977_ = !lean_is_exclusive(v_v_1949_);
if (v_isSharedCheck_1977_ == 0)
{
lean_object* v_unused_1978_; 
v_unused_1978_ = lean_ctor_get(v_v_1949_, 1);
lean_dec(v_unused_1978_);
v___x_1954_ = v_v_1949_;
v_isShared_1955_ = v_isSharedCheck_1977_;
goto v_resetjp_1953_;
}
else
{
lean_inc(v_fst_1952_);
lean_dec(v_v_1949_);
v___x_1954_ = lean_box(0);
v_isShared_1955_ = v_isSharedCheck_1977_;
goto v_resetjp_1953_;
}
v_resetjp_1953_:
{
lean_object* v_fst_1956_; lean_object* v___x_1958_; uint8_t v_isShared_1959_; uint8_t v_isSharedCheck_1975_; 
v_fst_1956_ = lean_ctor_get(v_snd_1950_, 0);
v_isSharedCheck_1975_ = !lean_is_exclusive(v_snd_1950_);
if (v_isSharedCheck_1975_ == 0)
{
lean_object* v_unused_1976_; 
v_unused_1976_ = lean_ctor_get(v_snd_1950_, 1);
lean_dec(v_unused_1976_);
v___x_1958_ = v_snd_1950_;
v_isShared_1959_ = v_isSharedCheck_1975_;
goto v_resetjp_1957_;
}
else
{
lean_inc(v_fst_1956_);
lean_dec(v_snd_1950_);
v___x_1958_ = lean_box(0);
v_isShared_1959_ = v_isSharedCheck_1975_;
goto v_resetjp_1957_;
}
v_resetjp_1957_:
{
lean_object* v_fst_1960_; lean_object* v_snd_1961_; lean_object* v___x_1963_; uint8_t v_isShared_1964_; uint8_t v_isSharedCheck_1974_; 
v_fst_1960_ = lean_ctor_get(v_snd_1951_, 0);
v_snd_1961_ = lean_ctor_get(v_snd_1951_, 1);
v_isSharedCheck_1974_ = !lean_is_exclusive(v_snd_1951_);
if (v_isSharedCheck_1974_ == 0)
{
v___x_1963_ = v_snd_1951_;
v_isShared_1964_ = v_isSharedCheck_1974_;
goto v_resetjp_1962_;
}
else
{
lean_inc(v_snd_1961_);
lean_inc(v_fst_1960_);
lean_dec(v_snd_1951_);
v___x_1963_ = lean_box(0);
v_isShared_1964_ = v_isSharedCheck_1974_;
goto v_resetjp_1962_;
}
v_resetjp_1962_:
{
lean_object* v___x_1966_; 
if (v_isShared_1964_ == 0)
{
lean_ctor_set(v___x_1963_, 1, v_fst_1952_);
lean_ctor_set(v___x_1963_, 0, v_snd_1961_);
v___x_1966_ = v___x_1963_;
goto v_reusejp_1965_;
}
else
{
lean_object* v_reuseFailAlloc_1973_; 
v_reuseFailAlloc_1973_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1973_, 0, v_snd_1961_);
lean_ctor_set(v_reuseFailAlloc_1973_, 1, v_fst_1952_);
v___x_1966_ = v_reuseFailAlloc_1973_;
goto v_reusejp_1965_;
}
v_reusejp_1965_:
{
lean_object* v___x_1968_; 
if (v_isShared_1959_ == 0)
{
lean_ctor_set(v___x_1958_, 1, v___x_1966_);
lean_ctor_set(v___x_1958_, 0, v_fst_1960_);
v___x_1968_ = v___x_1958_;
goto v_reusejp_1967_;
}
else
{
lean_object* v_reuseFailAlloc_1972_; 
v_reuseFailAlloc_1972_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1972_, 0, v_fst_1960_);
lean_ctor_set(v_reuseFailAlloc_1972_, 1, v___x_1966_);
v___x_1968_ = v_reuseFailAlloc_1972_;
goto v_reusejp_1967_;
}
v_reusejp_1967_:
{
lean_object* v___x_1970_; 
if (v_isShared_1955_ == 0)
{
lean_ctor_set(v___x_1954_, 1, v___x_1968_);
lean_ctor_set(v___x_1954_, 0, v_fst_1956_);
v___x_1970_ = v___x_1954_;
goto v_reusejp_1969_;
}
else
{
lean_object* v_reuseFailAlloc_1971_; 
v_reuseFailAlloc_1971_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_1971_, 0, v_fst_1956_);
lean_ctor_set(v_reuseFailAlloc_1971_, 1, v___x_1968_);
v___x_1970_ = v_reuseFailAlloc_1971_;
goto v_reusejp_1969_;
}
v_reusejp_1969_:
{
return v___x_1970_;
}
}
}
}
}
}
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm122FullMncRecovered(lean_object* v_imp_1979_){
_start:
{
lean_object* v___x_1980_; lean_object* v___x_1981_; uint8_t v___x_1982_; 
v___x_1980_ = lean_unsigned_to_nat(0u);
lean_inc_ref(v_imp_1979_);
v___x_1981_ = lean_apply_1(v_imp_1979_, v___x_1980_);
v___x_1982_ = lean_unbox(v___x_1981_);
if (v___x_1982_ == 0)
{
uint8_t v___x_1983_; 
lean_dec_ref(v_imp_1979_);
v___x_1983_ = lean_unbox(v___x_1981_);
return v___x_1983_;
}
else
{
lean_object* v___x_1984_; lean_object* v___x_1985_; uint8_t v___x_1986_; 
v___x_1984_ = lean_unsigned_to_nat(1u);
lean_inc_ref(v_imp_1979_);
v___x_1985_ = lean_apply_1(v_imp_1979_, v___x_1984_);
v___x_1986_ = lean_unbox(v___x_1985_);
if (v___x_1986_ == 0)
{
uint8_t v___x_1987_; 
lean_dec_ref(v_imp_1979_);
v___x_1987_ = lean_unbox(v___x_1985_);
return v___x_1987_;
}
else
{
lean_object* v___x_1988_; lean_object* v___x_1989_; uint8_t v___x_1990_; 
v___x_1988_ = lean_unsigned_to_nat(2u);
lean_inc_ref(v_imp_1979_);
v___x_1989_ = lean_apply_1(v_imp_1979_, v___x_1988_);
v___x_1990_ = lean_unbox(v___x_1989_);
if (v___x_1990_ == 0)
{
uint8_t v___x_1991_; 
lean_dec_ref(v_imp_1979_);
v___x_1991_ = lean_unbox(v___x_1989_);
return v___x_1991_;
}
else
{
lean_object* v___x_1992_; lean_object* v___x_1993_; uint8_t v___x_1994_; 
v___x_1992_ = lean_unsigned_to_nat(3u);
lean_inc_ref(v_imp_1979_);
v___x_1993_ = lean_apply_1(v_imp_1979_, v___x_1992_);
v___x_1994_ = lean_unbox(v___x_1993_);
if (v___x_1994_ == 0)
{
uint8_t v___x_1995_; 
lean_dec_ref(v_imp_1979_);
v___x_1995_ = lean_unbox(v___x_1993_);
return v___x_1995_;
}
else
{
lean_object* v___x_1996_; lean_object* v___x_1997_; uint8_t v___x_1998_; 
v___x_1996_ = lean_unsigned_to_nat(4u);
lean_inc_ref(v_imp_1979_);
v___x_1997_ = lean_apply_1(v_imp_1979_, v___x_1996_);
v___x_1998_ = lean_unbox(v___x_1997_);
if (v___x_1998_ == 0)
{
uint8_t v___x_1999_; 
lean_dec_ref(v_imp_1979_);
v___x_1999_ = lean_unbox(v___x_1997_);
return v___x_1999_;
}
else
{
lean_object* v___x_2000_; lean_object* v___x_2001_; uint8_t v___x_2002_; 
v___x_2000_ = lean_unsigned_to_nat(5u);
v___x_2001_ = lean_apply_1(v_imp_1979_, v___x_2000_);
v___x_2002_ = lean_unbox(v___x_2001_);
return v___x_2002_;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm122FullMncRecovered___boxed(lean_object* v_imp_2003_){
_start:
{
uint8_t v_res_2004_; lean_object* v_r_2005_; 
v_res_2004_ = lp_FiniteQuantum_QuantumMechanics_DerivationDagQMClosure_qm122FullMncRecovered(v_imp_2003_);
v_r_2005_ = lean_box(v_res_2004_);
return v_r_2005_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_DerivationDagQMClosure(uint8_t builtin) {
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
