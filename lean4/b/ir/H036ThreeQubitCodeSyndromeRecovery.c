// Lean compiler output
// Module: H036ThreeQubitCodeSyndromeRecovery
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
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "s2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__16_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqBitFlipError(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqBitFlipError___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 48, .m_capacity = 48, .m_length = 47, .m_data = "FableHilbertWalk20260819.H036.BitFlipError.errI"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "FableHilbertWalk20260819.H036.BitFlipError.errX1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "FableHilbertWalk20260819.H036.BitFlipError.errX2"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "FableHilbertWalk20260819.H036.BitFlipError.errX3"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__7_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___boxed(lean_object*);
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__3_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome_decEq(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
lean_object* v_s1_3_; lean_object* v_s2_4_; lean_object* v_s1_5_; lean_object* v_s2_6_; uint8_t v___x_7_; 
v_s1_3_ = lean_ctor_get(v_x_1_, 0);
v_s2_4_ = lean_ctor_get(v_x_1_, 1);
v_s1_5_ = lean_ctor_get(v_x_2_, 0);
v_s2_6_ = lean_ctor_get(v_x_2_, 1);
v___x_7_ = lean_int_dec_eq(v_s1_3_, v_s1_5_);
if (v___x_7_ == 0)
{
return v___x_7_;
}
else
{
uint8_t v___x_8_; 
v___x_8_ = lean_int_dec_eq(v_s2_4_, v_s2_6_);
return v___x_8_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome_decEq___boxed(lean_object* v_x_9_, lean_object* v_x_10_){
_start:
{
uint8_t v_res_11_; lean_object* v_r_12_; 
v_res_11_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome_decEq(v_x_9_, v_x_10_);
lean_dec_ref(v_x_10_);
lean_dec_ref(v_x_9_);
v_r_12_ = lean_box(v_res_11_);
return v_r_12_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome(lean_object* v_x_13_, lean_object* v_x_14_){
_start:
{
uint8_t v___x_15_; 
v___x_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome_decEq(v_x_13_, v_x_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome___boxed(lean_object* v_x_16_, lean_object* v_x_17_){
_start:
{
uint8_t v_res_18_; lean_object* v_r_19_; 
v_res_18_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqSyndrome(v_x_16_, v_x_17_);
lean_dec_ref(v_x_17_);
lean_dec_ref(v_x_16_);
v_r_19_ = lean_box(v_res_18_);
return v_r_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_unsigned_to_nat(6u);
v___x_34_ = lean_nat_to_int(v___x_33_);
return v___x_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_36_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__0));
v___x_37_ = lean_string_length(v___x_36_);
return v___x_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__9);
v___x_39_ = lean_nat_to_int(v___x_38_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_50_ = lean_unsigned_to_nat(0u);
v___x_51_ = lean_nat_to_int(v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg(lean_object* v_x_52_){
_start:
{
lean_object* v_s1_53_; lean_object* v_s2_54_; lean_object* v___x_56_; uint8_t v_isShared_57_; uint8_t v_isSharedCheck_106_; 
v_s1_53_ = lean_ctor_get(v_x_52_, 0);
v_s2_54_ = lean_ctor_get(v_x_52_, 1);
v_isSharedCheck_106_ = !lean_is_exclusive(v_x_52_);
if (v_isSharedCheck_106_ == 0)
{
v___x_56_ = v_x_52_;
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
else
{
lean_inc(v_s2_54_);
lean_inc(v_s1_53_);
lean_dec(v_x_52_);
v___x_56_ = lean_box(0);
v_isShared_57_ = v_isSharedCheck_106_;
goto v_resetjp_55_;
}
v_resetjp_55_:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___y_62_; uint8_t v___y_63_; lean_object* v___y_64_; lean_object* v___y_78_; lean_object* v___x_98_; lean_object* v___x_99_; uint8_t v___x_100_; 
v___x_58_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__5));
v___x_59_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__6));
v___x_60_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__7);
v___x_98_ = lean_unsigned_to_nat(0u);
v___x_99_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17);
v___x_100_ = lean_int_dec_lt(v_s1_53_, v___x_99_);
if (v___x_100_ == 0)
{
lean_object* v___x_101_; lean_object* v___x_102_; 
v___x_101_ = l_Int_repr(v_s1_53_);
lean_dec(v_s1_53_);
v___x_102_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_102_, 0, v___x_101_);
v___y_78_ = v___x_102_;
goto v___jp_77_;
}
else
{
lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; 
v___x_103_ = l_Int_repr(v_s1_53_);
lean_dec(v_s1_53_);
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
v___x_69_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__10);
v___x_70_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__11));
v___x_71_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_71_, 0, v___x_70_);
lean_ctor_set(v___x_71_, 1, v___x_68_);
v___x_72_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__12));
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
v___x_83_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__14));
v___x_84_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_84_, 0, v___x_82_);
lean_ctor_set(v___x_84_, 1, v___x_83_);
v___x_85_ = lean_box(1);
v___x_86_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_84_);
lean_ctor_set(v___x_86_, 1, v___x_85_);
v___x_87_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__16));
v___x_88_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_88_, 0, v___x_86_);
lean_ctor_set(v___x_88_, 1, v___x_87_);
v___x_89_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_88_);
lean_ctor_set(v___x_89_, 1, v___x_58_);
v___x_90_ = lean_unsigned_to_nat(0u);
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg___closed__17);
v___x_92_ = lean_int_dec_lt(v_s2_54_, v___x_91_);
if (v___x_92_ == 0)
{
lean_object* v___x_93_; lean_object* v___x_94_; 
v___x_93_ = l_Int_repr(v_s2_54_);
lean_dec(v_s2_54_);
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
v___x_95_ = l_Int_repr(v_s2_54_);
lean_dec(v_s2_54_);
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr(lean_object* v_x_107_, lean_object* v_prec_108_){
_start:
{
lean_object* v___x_109_; 
v___x_109_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___redArg(v_x_107_);
return v___x_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr___boxed(lean_object* v_x_110_, lean_object* v_prec_111_){
_start:
{
lean_object* v_res_112_; 
v_res_112_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprSyndrome_repr(v_x_110_, v_prec_111_);
lean_dec(v_prec_111_);
return v_res_112_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx(uint8_t v_x_115_){
_start:
{
switch(v_x_115_)
{
case 0:
{
lean_object* v___x_116_; 
v___x_116_ = lean_unsigned_to_nat(0u);
return v___x_116_;
}
case 1:
{
lean_object* v___x_117_; 
v___x_117_ = lean_unsigned_to_nat(1u);
return v___x_117_;
}
case 2:
{
lean_object* v___x_118_; 
v___x_118_ = lean_unsigned_to_nat(2u);
return v___x_118_;
}
default: 
{
lean_object* v___x_119_; 
v___x_119_ = lean_unsigned_to_nat(3u);
return v___x_119_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx___boxed(lean_object* v_x_120_){
_start:
{
uint8_t v_x_boxed_121_; lean_object* v_res_122_; 
v_x_boxed_121_ = lean_unbox(v_x_120_);
v_res_122_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx(v_x_boxed_121_);
return v_res_122_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_toCtorIdx(uint8_t v_x_123_){
_start:
{
lean_object* v___x_124_; 
v___x_124_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx(v_x_123_);
return v___x_124_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_toCtorIdx___boxed(lean_object* v_x_125_){
_start:
{
uint8_t v_x_4__boxed_126_; lean_object* v_res_127_; 
v_x_4__boxed_126_ = lean_unbox(v_x_125_);
v_res_127_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_toCtorIdx(v_x_4__boxed_126_);
return v_res_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___redArg(lean_object* v_k_128_){
_start:
{
lean_inc(v_k_128_);
return v_k_128_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___redArg___boxed(lean_object* v_k_129_){
_start:
{
lean_object* v_res_130_; 
v_res_130_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___redArg(v_k_129_);
lean_dec(v_k_129_);
return v_res_130_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim(lean_object* v_motive_131_, lean_object* v_ctorIdx_132_, uint8_t v_t_133_, lean_object* v_h_134_, lean_object* v_k_135_){
_start:
{
lean_inc(v_k_135_);
return v_k_135_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim___boxed(lean_object* v_motive_136_, lean_object* v_ctorIdx_137_, lean_object* v_t_138_, lean_object* v_h_139_, lean_object* v_k_140_){
_start:
{
uint8_t v_t_boxed_141_; lean_object* v_res_142_; 
v_t_boxed_141_ = lean_unbox(v_t_138_);
v_res_142_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorElim(v_motive_136_, v_ctorIdx_137_, v_t_boxed_141_, v_h_139_, v_k_140_);
lean_dec(v_k_140_);
lean_dec(v_ctorIdx_137_);
return v_res_142_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___redArg(lean_object* v_errI_143_){
_start:
{
lean_inc(v_errI_143_);
return v_errI_143_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___redArg___boxed(lean_object* v_errI_144_){
_start:
{
lean_object* v_res_145_; 
v_res_145_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___redArg(v_errI_144_);
lean_dec(v_errI_144_);
return v_res_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim(lean_object* v_motive_146_, uint8_t v_t_147_, lean_object* v_h_148_, lean_object* v_errI_149_){
_start:
{
lean_inc(v_errI_149_);
return v_errI_149_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim___boxed(lean_object* v_motive_150_, lean_object* v_t_151_, lean_object* v_h_152_, lean_object* v_errI_153_){
_start:
{
uint8_t v_t_boxed_154_; lean_object* v_res_155_; 
v_t_boxed_154_ = lean_unbox(v_t_151_);
v_res_155_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errI_elim(v_motive_150_, v_t_boxed_154_, v_h_152_, v_errI_153_);
lean_dec(v_errI_153_);
return v_res_155_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___redArg(lean_object* v_errX1_156_){
_start:
{
lean_inc(v_errX1_156_);
return v_errX1_156_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___redArg___boxed(lean_object* v_errX1_157_){
_start:
{
lean_object* v_res_158_; 
v_res_158_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___redArg(v_errX1_157_);
lean_dec(v_errX1_157_);
return v_res_158_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim(lean_object* v_motive_159_, uint8_t v_t_160_, lean_object* v_h_161_, lean_object* v_errX1_162_){
_start:
{
lean_inc(v_errX1_162_);
return v_errX1_162_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim___boxed(lean_object* v_motive_163_, lean_object* v_t_164_, lean_object* v_h_165_, lean_object* v_errX1_166_){
_start:
{
uint8_t v_t_boxed_167_; lean_object* v_res_168_; 
v_t_boxed_167_ = lean_unbox(v_t_164_);
v_res_168_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX1_elim(v_motive_163_, v_t_boxed_167_, v_h_165_, v_errX1_166_);
lean_dec(v_errX1_166_);
return v_res_168_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___redArg(lean_object* v_errX2_169_){
_start:
{
lean_inc(v_errX2_169_);
return v_errX2_169_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___redArg___boxed(lean_object* v_errX2_170_){
_start:
{
lean_object* v_res_171_; 
v_res_171_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___redArg(v_errX2_170_);
lean_dec(v_errX2_170_);
return v_res_171_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim(lean_object* v_motive_172_, uint8_t v_t_173_, lean_object* v_h_174_, lean_object* v_errX2_175_){
_start:
{
lean_inc(v_errX2_175_);
return v_errX2_175_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim___boxed(lean_object* v_motive_176_, lean_object* v_t_177_, lean_object* v_h_178_, lean_object* v_errX2_179_){
_start:
{
uint8_t v_t_boxed_180_; lean_object* v_res_181_; 
v_t_boxed_180_ = lean_unbox(v_t_177_);
v_res_181_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX2_elim(v_motive_176_, v_t_boxed_180_, v_h_178_, v_errX2_179_);
lean_dec(v_errX2_179_);
return v_res_181_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___redArg(lean_object* v_errX3_182_){
_start:
{
lean_inc(v_errX3_182_);
return v_errX3_182_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___redArg___boxed(lean_object* v_errX3_183_){
_start:
{
lean_object* v_res_184_; 
v_res_184_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___redArg(v_errX3_183_);
lean_dec(v_errX3_183_);
return v_res_184_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim(lean_object* v_motive_185_, uint8_t v_t_186_, lean_object* v_h_187_, lean_object* v_errX3_188_){
_start:
{
lean_inc(v_errX3_188_);
return v_errX3_188_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim___boxed(lean_object* v_motive_189_, lean_object* v_t_190_, lean_object* v_h_191_, lean_object* v_errX3_192_){
_start:
{
uint8_t v_t_boxed_193_; lean_object* v_res_194_; 
v_t_boxed_193_ = lean_unbox(v_t_190_);
v_res_194_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_errX3_elim(v_motive_189_, v_t_boxed_193_, v_h_191_, v_errX3_192_);
lean_dec(v_errX3_192_);
return v_res_194_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ofNat(lean_object* v_n_195_){
_start:
{
lean_object* v___x_196_; uint8_t v___x_197_; 
v___x_196_ = lean_unsigned_to_nat(1u);
v___x_197_ = lean_nat_dec_le(v_n_195_, v___x_196_);
if (v___x_197_ == 0)
{
lean_object* v___x_198_; uint8_t v___x_199_; 
v___x_198_ = lean_unsigned_to_nat(2u);
v___x_199_ = lean_nat_dec_le(v_n_195_, v___x_198_);
if (v___x_199_ == 0)
{
uint8_t v___x_200_; 
v___x_200_ = 3;
return v___x_200_;
}
else
{
uint8_t v___x_201_; 
v___x_201_ = 2;
return v___x_201_;
}
}
else
{
lean_object* v___x_202_; uint8_t v___x_203_; 
v___x_202_ = lean_unsigned_to_nat(0u);
v___x_203_ = lean_nat_dec_le(v_n_195_, v___x_202_);
if (v___x_203_ == 0)
{
uint8_t v___x_204_; 
v___x_204_ = 1;
return v___x_204_;
}
else
{
uint8_t v___x_205_; 
v___x_205_ = 0;
return v___x_205_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ofNat___boxed(lean_object* v_n_206_){
_start:
{
uint8_t v_res_207_; lean_object* v_r_208_; 
v_res_207_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ofNat(v_n_206_);
lean_dec(v_n_206_);
v_r_208_ = lean_box(v_res_207_);
return v_r_208_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqBitFlipError(uint8_t v_x_209_, uint8_t v_y_210_){
_start:
{
lean_object* v___x_211_; lean_object* v___x_212_; uint8_t v___x_213_; 
v___x_211_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx(v_x_209_);
v___x_212_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_BitFlipError_ctorIdx(v_y_210_);
v___x_213_ = lean_nat_dec_eq(v___x_211_, v___x_212_);
lean_dec(v___x_212_);
lean_dec(v___x_211_);
return v___x_213_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqBitFlipError___boxed(lean_object* v_x_214_, lean_object* v_y_215_){
_start:
{
uint8_t v_x_13__boxed_216_; uint8_t v_y_14__boxed_217_; uint8_t v_res_218_; lean_object* v_r_219_; 
v_x_13__boxed_216_ = lean_unbox(v_x_214_);
v_y_14__boxed_217_ = lean_unbox(v_y_215_);
v_res_218_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instDecidableEqBitFlipError(v_x_13__boxed_216_, v_y_14__boxed_217_);
v_r_219_ = lean_box(v_res_218_);
return v_r_219_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8(void){
_start:
{
lean_object* v___x_232_; lean_object* v___x_233_; 
v___x_232_ = lean_unsigned_to_nat(2u);
v___x_233_ = lean_nat_to_int(v___x_232_);
return v___x_233_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9(void){
_start:
{
lean_object* v___x_234_; lean_object* v___x_235_; 
v___x_234_ = lean_unsigned_to_nat(1u);
v___x_235_ = lean_nat_to_int(v___x_234_);
return v___x_235_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr(uint8_t v_x_236_, lean_object* v_prec_237_){
_start:
{
lean_object* v___y_239_; lean_object* v___y_246_; lean_object* v___y_253_; lean_object* v___y_260_; 
switch(v_x_236_)
{
case 0:
{
lean_object* v___x_266_; uint8_t v___x_267_; 
v___x_266_ = lean_unsigned_to_nat(1024u);
v___x_267_ = lean_nat_dec_le(v___x_266_, v_prec_237_);
if (v___x_267_ == 0)
{
lean_object* v___x_268_; 
v___x_268_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8);
v___y_239_ = v___x_268_;
goto v___jp_238_;
}
else
{
lean_object* v___x_269_; 
v___x_269_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___y_239_ = v___x_269_;
goto v___jp_238_;
}
}
case 1:
{
lean_object* v___x_270_; uint8_t v___x_271_; 
v___x_270_ = lean_unsigned_to_nat(1024u);
v___x_271_ = lean_nat_dec_le(v___x_270_, v_prec_237_);
if (v___x_271_ == 0)
{
lean_object* v___x_272_; 
v___x_272_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8);
v___y_246_ = v___x_272_;
goto v___jp_245_;
}
else
{
lean_object* v___x_273_; 
v___x_273_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___y_246_ = v___x_273_;
goto v___jp_245_;
}
}
case 2:
{
lean_object* v___x_274_; uint8_t v___x_275_; 
v___x_274_ = lean_unsigned_to_nat(1024u);
v___x_275_ = lean_nat_dec_le(v___x_274_, v_prec_237_);
if (v___x_275_ == 0)
{
lean_object* v___x_276_; 
v___x_276_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8);
v___y_253_ = v___x_276_;
goto v___jp_252_;
}
else
{
lean_object* v___x_277_; 
v___x_277_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___y_253_ = v___x_277_;
goto v___jp_252_;
}
}
default: 
{
lean_object* v___x_278_; uint8_t v___x_279_; 
v___x_278_ = lean_unsigned_to_nat(1024u);
v___x_279_ = lean_nat_dec_le(v___x_278_, v_prec_237_);
if (v___x_279_ == 0)
{
lean_object* v___x_280_; 
v___x_280_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__8);
v___y_260_ = v___x_280_;
goto v___jp_259_;
}
else
{
lean_object* v___x_281_; 
v___x_281_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___y_260_ = v___x_281_;
goto v___jp_259_;
}
}
}
v___jp_238_:
{
lean_object* v___x_240_; lean_object* v___x_241_; uint8_t v___x_242_; lean_object* v___x_243_; lean_object* v___x_244_; 
v___x_240_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__1));
lean_inc(v___y_239_);
v___x_241_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_241_, 0, v___y_239_);
lean_ctor_set(v___x_241_, 1, v___x_240_);
v___x_242_ = 0;
v___x_243_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_243_, 0, v___x_241_);
lean_ctor_set_uint8(v___x_243_, sizeof(void*)*1, v___x_242_);
v___x_244_ = l_Repr_addAppParen(v___x_243_, v_prec_237_);
return v___x_244_;
}
v___jp_245_:
{
lean_object* v___x_247_; lean_object* v___x_248_; uint8_t v___x_249_; lean_object* v___x_250_; lean_object* v___x_251_; 
v___x_247_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__3));
lean_inc(v___y_246_);
v___x_248_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_248_, 0, v___y_246_);
lean_ctor_set(v___x_248_, 1, v___x_247_);
v___x_249_ = 0;
v___x_250_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_250_, 0, v___x_248_);
lean_ctor_set_uint8(v___x_250_, sizeof(void*)*1, v___x_249_);
v___x_251_ = l_Repr_addAppParen(v___x_250_, v_prec_237_);
return v___x_251_;
}
v___jp_252_:
{
lean_object* v___x_254_; lean_object* v___x_255_; uint8_t v___x_256_; lean_object* v___x_257_; lean_object* v___x_258_; 
v___x_254_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__5));
lean_inc(v___y_253_);
v___x_255_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_255_, 0, v___y_253_);
lean_ctor_set(v___x_255_, 1, v___x_254_);
v___x_256_ = 0;
v___x_257_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_257_, 0, v___x_255_);
lean_ctor_set_uint8(v___x_257_, sizeof(void*)*1, v___x_256_);
v___x_258_ = l_Repr_addAppParen(v___x_257_, v_prec_237_);
return v___x_258_;
}
v___jp_259_:
{
lean_object* v___x_261_; lean_object* v___x_262_; uint8_t v___x_263_; lean_object* v___x_264_; lean_object* v___x_265_; 
v___x_261_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__7));
lean_inc(v___y_260_);
v___x_262_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_262_, 0, v___y_260_);
lean_ctor_set(v___x_262_, 1, v___x_261_);
v___x_263_ = 0;
v___x_264_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_264_, 0, v___x_262_);
lean_ctor_set_uint8(v___x_264_, sizeof(void*)*1, v___x_263_);
v___x_265_ = l_Repr_addAppParen(v___x_264_, v_prec_237_);
return v___x_265_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___boxed(lean_object* v_x_282_, lean_object* v_prec_283_){
_start:
{
uint8_t v_x_233__boxed_284_; lean_object* v_res_285_; 
v_x_233__boxed_284_ = lean_unbox(v_x_282_);
v_res_285_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr(v_x_233__boxed_284_, v_prec_283_);
lean_dec(v_prec_283_);
return v_res_285_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__0(void){
_start:
{
lean_object* v___x_288_; lean_object* v___x_289_; 
v___x_288_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___x_289_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_289_, 0, v___x_288_);
lean_ctor_set(v___x_289_, 1, v___x_288_);
return v___x_289_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1(void){
_start:
{
lean_object* v___x_290_; lean_object* v___x_291_; 
v___x_290_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___x_291_ = lean_int_neg(v___x_290_);
return v___x_291_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__2(void){
_start:
{
lean_object* v___x_292_; lean_object* v___x_293_; lean_object* v___x_294_; 
v___x_292_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___x_293_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1);
v___x_294_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_294_, 0, v___x_293_);
lean_ctor_set(v___x_294_, 1, v___x_292_);
return v___x_294_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__3(void){
_start:
{
lean_object* v___x_295_; lean_object* v___x_296_; 
v___x_295_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1);
v___x_296_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_296_, 0, v___x_295_);
lean_ctor_set(v___x_296_, 1, v___x_295_);
return v___x_296_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__4(void){
_start:
{
lean_object* v___x_297_; lean_object* v___x_298_; lean_object* v___x_299_; 
v___x_297_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1);
v___x_298_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___x_299_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_299_, 0, v___x_298_);
lean_ctor_set(v___x_299_, 1, v___x_297_);
return v___x_299_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf(uint8_t v_x_300_){
_start:
{
switch(v_x_300_)
{
case 0:
{
lean_object* v___x_301_; 
v___x_301_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__0);
return v___x_301_;
}
case 1:
{
lean_object* v___x_302_; 
v___x_302_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__2);
return v___x_302_;
}
case 2:
{
lean_object* v___x_303_; 
v___x_303_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__3);
return v___x_303_;
}
default: 
{
lean_object* v___x_304_; 
v___x_304_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__4);
return v___x_304_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___boxed(lean_object* v_x_305_){
_start:
{
uint8_t v_x_118__boxed_306_; lean_object* v_res_307_; 
v_x_118__boxed_306_ = lean_unbox(v_x_305_);
v_res_307_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf(v_x_118__boxed_306_);
return v_res_307_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome(lean_object* v_s_320_){
_start:
{
lean_object* v_s1_321_; lean_object* v_s2_322_; lean_object* v___x_323_; uint8_t v___x_324_; lean_object* v___y_326_; lean_object* v___y_332_; uint8_t v___y_333_; 
v_s1_321_ = lean_ctor_get(v_s_320_, 0);
v_s2_322_ = lean_ctor_get(v_s_320_, 1);
v___x_323_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_instReprBitFlipError_repr___closed__9);
v___x_324_ = lean_int_dec_eq(v_s1_321_, v___x_323_);
if (v___x_324_ == 0)
{
goto v___jp_336_;
}
else
{
uint8_t v___x_341_; 
v___x_341_ = lean_int_dec_eq(v_s2_322_, v___x_323_);
if (v___x_341_ == 0)
{
goto v___jp_336_;
}
else
{
lean_object* v___x_342_; 
v___x_342_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__3));
return v___x_342_;
}
}
v___jp_325_:
{
if (v___x_324_ == 0)
{
lean_object* v___x_327_; 
v___x_327_ = lean_box(0);
return v___x_327_;
}
else
{
uint8_t v___x_328_; 
v___x_328_ = lean_int_dec_eq(v_s2_322_, v___y_326_);
if (v___x_328_ == 0)
{
lean_object* v___x_329_; 
v___x_329_ = lean_box(0);
return v___x_329_;
}
else
{
lean_object* v___x_330_; 
v___x_330_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__0));
return v___x_330_;
}
}
}
v___jp_331_:
{
if (v___y_333_ == 0)
{
v___y_326_ = v___y_332_;
goto v___jp_325_;
}
else
{
uint8_t v___x_334_; 
v___x_334_ = lean_int_dec_eq(v_s2_322_, v___y_332_);
if (v___x_334_ == 0)
{
v___y_326_ = v___y_332_;
goto v___jp_325_;
}
else
{
lean_object* v___x_335_; 
v___x_335_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__1));
return v___x_335_;
}
}
}
v___jp_336_:
{
lean_object* v___x_337_; uint8_t v___x_338_; 
v___x_337_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H036_syndromeOf___closed__1);
v___x_338_ = lean_int_dec_eq(v_s1_321_, v___x_337_);
if (v___x_338_ == 0)
{
v___y_332_ = v___x_337_;
v___y_333_ = v___x_338_;
goto v___jp_331_;
}
else
{
uint8_t v___x_339_; 
v___x_339_ = lean_int_dec_eq(v_s2_322_, v___x_323_);
if (v___x_339_ == 0)
{
v___y_332_ = v___x_337_;
v___y_333_ = v___x_338_;
goto v___jp_331_;
}
else
{
lean_object* v___x_340_; 
v___x_340_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___closed__2));
return v___x_340_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome___boxed(lean_object* v_s_343_){
_start:
{
lean_object* v_res_344_; 
v_res_344_ = lp_FiniteQuantum_FableHilbertWalk20260819_H036_decodeSyndrome(v_s_343_);
lean_dec_ref(v_s_343_);
return v_res_344_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H036ThreeQubitCodeSyndromeRecovery(uint8_t builtin) {
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
