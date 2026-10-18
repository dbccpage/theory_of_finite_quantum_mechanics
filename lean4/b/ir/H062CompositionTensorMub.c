// Lean compiler output
// Module: H062CompositionTensorMub
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
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* l_Int_repr(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqTensorAxiom(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqTensorAxiom___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 54, .m_capacity = 54, .m_length = 53, .m_data = "FableHilbertWalk20260819.H062.TensorAxiom.bilinearity"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 67, .m_capacity = 67, .m_length = 66, .m_data = "FableHilbertWalk20260819.H062.TensorAxiom.local_unitary_covariance"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 71, .m_capacity = 71, .m_length = 70, .m_data = "FableHilbertWalk20260819.H062.TensorAxiom.product_marginal_consistency"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 55, .m_capacity = 55, .m_length = 54, .m_data = "FableHilbertWalk20260819.H062.TensorAxiom.no_signaling"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__7_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__3_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_tensorAxiomList___closed__3_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "x0"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__8_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__9;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__10;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__11_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__12 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__12_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__14_value;
static const lean_string_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "x1"};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__15 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__15_value;
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__15_value)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__16_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_add___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_smul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_smul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_projDump(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_projDump___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_pauliZ(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d2__denom;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d3__denom;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_composite__d6__overlap__denom;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_product__mub__count__d6;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_gkp__phase__order(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_gkp__phase__order___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx___boxed(lean_object* v_x_6_){
_start:
{
uint8_t v_x_boxed_7_; lean_object* v_res_8_; 
v_x_boxed_7_ = lean_unbox(v_x_6_);
v_res_8_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx(v_x_boxed_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_toCtorIdx(uint8_t v_x_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx(v_x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_toCtorIdx___boxed(lean_object* v_x_11_){
_start:
{
uint8_t v_x_4__boxed_12_; lean_object* v_res_13_; 
v_x_4__boxed_12_ = lean_unbox(v_x_11_);
v_res_13_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_toCtorIdx(v_x_4__boxed_12_);
return v_res_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___redArg(lean_object* v_k_14_){
_start:
{
lean_inc(v_k_14_);
return v_k_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___redArg___boxed(lean_object* v_k_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___redArg(v_k_15_);
lean_dec(v_k_15_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim(lean_object* v_motive_17_, lean_object* v_ctorIdx_18_, uint8_t v_t_19_, lean_object* v_h_20_, lean_object* v_k_21_){
_start:
{
lean_inc(v_k_21_);
return v_k_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim___boxed(lean_object* v_motive_22_, lean_object* v_ctorIdx_23_, lean_object* v_t_24_, lean_object* v_h_25_, lean_object* v_k_26_){
_start:
{
uint8_t v_t_boxed_27_; lean_object* v_res_28_; 
v_t_boxed_27_ = lean_unbox(v_t_24_);
v_res_28_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorElim(v_motive_22_, v_ctorIdx_23_, v_t_boxed_27_, v_h_25_, v_k_26_);
lean_dec(v_k_26_);
lean_dec(v_ctorIdx_23_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___redArg(lean_object* v_bilinearity_29_){
_start:
{
lean_inc(v_bilinearity_29_);
return v_bilinearity_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___redArg___boxed(lean_object* v_bilinearity_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___redArg(v_bilinearity_30_);
lean_dec(v_bilinearity_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim(lean_object* v_motive_32_, uint8_t v_t_33_, lean_object* v_h_34_, lean_object* v_bilinearity_35_){
_start:
{
lean_inc(v_bilinearity_35_);
return v_bilinearity_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim___boxed(lean_object* v_motive_36_, lean_object* v_t_37_, lean_object* v_h_38_, lean_object* v_bilinearity_39_){
_start:
{
uint8_t v_t_boxed_40_; lean_object* v_res_41_; 
v_t_boxed_40_ = lean_unbox(v_t_37_);
v_res_41_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_bilinearity_elim(v_motive_36_, v_t_boxed_40_, v_h_38_, v_bilinearity_39_);
lean_dec(v_bilinearity_39_);
return v_res_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___redArg(lean_object* v_local__unitary__covariance_42_){
_start:
{
lean_inc(v_local__unitary__covariance_42_);
return v_local__unitary__covariance_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___redArg___boxed(lean_object* v_local__unitary__covariance_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___redArg(v_local__unitary__covariance_43_);
lean_dec(v_local__unitary__covariance_43_);
return v_res_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim(lean_object* v_motive_45_, uint8_t v_t_46_, lean_object* v_h_47_, lean_object* v_local__unitary__covariance_48_){
_start:
{
lean_inc(v_local__unitary__covariance_48_);
return v_local__unitary__covariance_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim___boxed(lean_object* v_motive_49_, lean_object* v_t_50_, lean_object* v_h_51_, lean_object* v_local__unitary__covariance_52_){
_start:
{
uint8_t v_t_boxed_53_; lean_object* v_res_54_; 
v_t_boxed_53_ = lean_unbox(v_t_50_);
v_res_54_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_local__unitary__covariance_elim(v_motive_49_, v_t_boxed_53_, v_h_51_, v_local__unitary__covariance_52_);
lean_dec(v_local__unitary__covariance_52_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___redArg(lean_object* v_product__marginal__consistency_55_){
_start:
{
lean_inc(v_product__marginal__consistency_55_);
return v_product__marginal__consistency_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___redArg___boxed(lean_object* v_product__marginal__consistency_56_){
_start:
{
lean_object* v_res_57_; 
v_res_57_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___redArg(v_product__marginal__consistency_56_);
lean_dec(v_product__marginal__consistency_56_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim(lean_object* v_motive_58_, uint8_t v_t_59_, lean_object* v_h_60_, lean_object* v_product__marginal__consistency_61_){
_start:
{
lean_inc(v_product__marginal__consistency_61_);
return v_product__marginal__consistency_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim___boxed(lean_object* v_motive_62_, lean_object* v_t_63_, lean_object* v_h_64_, lean_object* v_product__marginal__consistency_65_){
_start:
{
uint8_t v_t_boxed_66_; lean_object* v_res_67_; 
v_t_boxed_66_ = lean_unbox(v_t_63_);
v_res_67_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_product__marginal__consistency_elim(v_motive_62_, v_t_boxed_66_, v_h_64_, v_product__marginal__consistency_65_);
lean_dec(v_product__marginal__consistency_65_);
return v_res_67_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___redArg(lean_object* v_no__signaling_68_){
_start:
{
lean_inc(v_no__signaling_68_);
return v_no__signaling_68_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___redArg___boxed(lean_object* v_no__signaling_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___redArg(v_no__signaling_69_);
lean_dec(v_no__signaling_69_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim(lean_object* v_motive_71_, uint8_t v_t_72_, lean_object* v_h_73_, lean_object* v_no__signaling_74_){
_start:
{
lean_inc(v_no__signaling_74_);
return v_no__signaling_74_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim___boxed(lean_object* v_motive_75_, lean_object* v_t_76_, lean_object* v_h_77_, lean_object* v_no__signaling_78_){
_start:
{
uint8_t v_t_boxed_79_; lean_object* v_res_80_; 
v_t_boxed_79_ = lean_unbox(v_t_76_);
v_res_80_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_no__signaling_elim(v_motive_75_, v_t_boxed_79_, v_h_77_, v_no__signaling_78_);
lean_dec(v_no__signaling_78_);
return v_res_80_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ofNat(lean_object* v_n_81_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ofNat___boxed(lean_object* v_n_92_){
_start:
{
uint8_t v_res_93_; lean_object* v_r_94_; 
v_res_93_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ofNat(v_n_92_);
lean_dec(v_n_92_);
v_r_94_ = lean_box(v_res_93_);
return v_r_94_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqTensorAxiom(uint8_t v_x_95_, uint8_t v_y_96_){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_97_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx(v_x_95_);
v___x_98_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_TensorAxiom_ctorIdx(v_y_96_);
v___x_99_ = lean_nat_dec_eq(v___x_97_, v___x_98_);
lean_dec(v___x_98_);
lean_dec(v___x_97_);
return v___x_99_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqTensorAxiom___boxed(lean_object* v_x_100_, lean_object* v_y_101_){
_start:
{
uint8_t v_x_13__boxed_102_; uint8_t v_y_14__boxed_103_; uint8_t v_res_104_; lean_object* v_r_105_; 
v_x_13__boxed_102_ = lean_unbox(v_x_100_);
v_y_14__boxed_103_ = lean_unbox(v_y_101_);
v_res_104_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqTensorAxiom(v_x_13__boxed_102_, v_y_14__boxed_103_);
v_r_105_ = lean_box(v_res_104_);
return v_r_105_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(2u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_120_ = lean_unsigned_to_nat(1u);
v___x_121_ = lean_nat_to_int(v___x_120_);
return v___x_121_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr(uint8_t v_x_122_, lean_object* v_prec_123_){
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
v___x_154_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8);
v___y_125_ = v___x_154_;
goto v___jp_124_;
}
else
{
lean_object* v___x_155_; 
v___x_155_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9);
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
v___x_158_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8);
v___y_132_ = v___x_158_;
goto v___jp_131_;
}
else
{
lean_object* v___x_159_; 
v___x_159_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9);
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
v___x_162_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8);
v___y_139_ = v___x_162_;
goto v___jp_138_;
}
else
{
lean_object* v___x_163_; 
v___x_163_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9);
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
v___x_166_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__8);
v___y_146_ = v___x_166_;
goto v___jp_145_;
}
else
{
lean_object* v___x_167_; 
v___x_167_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9);
v___y_146_ = v___x_167_;
goto v___jp_145_;
}
}
}
v___jp_124_:
{
lean_object* v___x_126_; lean_object* v___x_127_; uint8_t v___x_128_; lean_object* v___x_129_; lean_object* v___x_130_; 
v___x_126_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__1));
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
v___x_133_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__3));
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
v___x_140_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__5));
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
v___x_147_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__7));
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___boxed(lean_object* v_x_168_, lean_object* v_prec_169_){
_start:
{
uint8_t v_x_233__boxed_170_; lean_object* v_res_171_; 
v_x_233__boxed_170_ = lean_unbox(v_x_168_);
v_res_171_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr(v_x_233__boxed_170_, v_prec_169_);
lean_dec(v_prec_169_);
return v_res_171_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2_decEq(lean_object* v_x_191_, lean_object* v_x_192_){
_start:
{
lean_object* v_x0_193_; lean_object* v_x1_194_; lean_object* v_x0_195_; lean_object* v_x1_196_; uint8_t v___x_197_; 
v_x0_193_ = lean_ctor_get(v_x_191_, 0);
v_x1_194_ = lean_ctor_get(v_x_191_, 1);
v_x0_195_ = lean_ctor_get(v_x_192_, 0);
v_x1_196_ = lean_ctor_get(v_x_192_, 1);
v___x_197_ = lean_int_dec_eq(v_x0_193_, v_x0_195_);
if (v___x_197_ == 0)
{
return v___x_197_;
}
else
{
uint8_t v___x_198_; 
v___x_198_ = lean_int_dec_eq(v_x1_194_, v_x1_196_);
return v___x_198_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2_decEq___boxed(lean_object* v_x_199_, lean_object* v_x_200_){
_start:
{
uint8_t v_res_201_; lean_object* v_r_202_; 
v_res_201_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2_decEq(v_x_199_, v_x_200_);
lean_dec_ref(v_x_200_);
lean_dec_ref(v_x_199_);
v_r_202_ = lean_box(v_res_201_);
return v_r_202_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2(lean_object* v_x_203_, lean_object* v_x_204_){
_start:
{
uint8_t v___x_205_; 
v___x_205_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2_decEq(v_x_203_, v_x_204_);
return v___x_205_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2___boxed(lean_object* v_x_206_, lean_object* v_x_207_){
_start:
{
uint8_t v_res_208_; lean_object* v_r_209_; 
v_res_208_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instDecidableEqVec2(v_x_206_, v_x_207_);
lean_dec_ref(v_x_207_);
lean_dec_ref(v_x_206_);
v_r_209_ = lean_box(v_res_208_);
return v_r_209_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_223_; lean_object* v___x_224_; 
v___x_223_ = lean_unsigned_to_nat(6u);
v___x_224_ = lean_nat_to_int(v___x_223_);
return v___x_224_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__9(void){
_start:
{
lean_object* v___x_226_; lean_object* v___x_227_; 
v___x_226_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__0));
v___x_227_ = lean_string_length(v___x_226_);
return v___x_227_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__10(void){
_start:
{
lean_object* v___x_228_; lean_object* v___x_229_; 
v___x_228_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__9);
v___x_229_ = lean_nat_to_int(v___x_228_);
return v___x_229_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_240_; lean_object* v___x_241_; 
v___x_240_ = lean_unsigned_to_nat(0u);
v___x_241_ = lean_nat_to_int(v___x_240_);
return v___x_241_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg(lean_object* v_x_242_){
_start:
{
lean_object* v_x0_243_; lean_object* v_x1_244_; lean_object* v___x_246_; uint8_t v_isShared_247_; uint8_t v_isSharedCheck_296_; 
v_x0_243_ = lean_ctor_get(v_x_242_, 0);
v_x1_244_ = lean_ctor_get(v_x_242_, 1);
v_isSharedCheck_296_ = !lean_is_exclusive(v_x_242_);
if (v_isSharedCheck_296_ == 0)
{
v___x_246_ = v_x_242_;
v_isShared_247_ = v_isSharedCheck_296_;
goto v_resetjp_245_;
}
else
{
lean_inc(v_x1_244_);
lean_inc(v_x0_243_);
lean_dec(v_x_242_);
v___x_246_ = lean_box(0);
v_isShared_247_ = v_isSharedCheck_296_;
goto v_resetjp_245_;
}
v_resetjp_245_:
{
lean_object* v___x_248_; lean_object* v___x_249_; lean_object* v___x_250_; lean_object* v___y_252_; uint8_t v___y_253_; lean_object* v___y_254_; lean_object* v___y_268_; lean_object* v___x_288_; lean_object* v___x_289_; uint8_t v___x_290_; 
v___x_248_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__5));
v___x_249_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__6));
v___x_250_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__7, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__7);
v___x_288_ = lean_unsigned_to_nat(0u);
v___x_289_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17);
v___x_290_ = lean_int_dec_lt(v_x0_243_, v___x_289_);
if (v___x_290_ == 0)
{
lean_object* v___x_291_; lean_object* v___x_292_; 
v___x_291_ = l_Int_repr(v_x0_243_);
lean_dec(v_x0_243_);
v___x_292_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_292_, 0, v___x_291_);
v___y_268_ = v___x_292_;
goto v___jp_267_;
}
else
{
lean_object* v___x_293_; lean_object* v___x_294_; lean_object* v___x_295_; 
v___x_293_ = l_Int_repr(v_x0_243_);
lean_dec(v_x0_243_);
v___x_294_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_294_, 0, v___x_293_);
v___x_295_ = l_Repr_addAppParen(v___x_294_, v___x_288_);
v___y_268_ = v___x_295_;
goto v___jp_267_;
}
v___jp_251_:
{
lean_object* v___x_256_; 
if (v_isShared_247_ == 0)
{
lean_ctor_set_tag(v___x_246_, 4);
lean_ctor_set(v___x_246_, 1, v___y_254_);
lean_ctor_set(v___x_246_, 0, v___x_250_);
v___x_256_ = v___x_246_;
goto v_reusejp_255_;
}
else
{
lean_object* v_reuseFailAlloc_266_; 
v_reuseFailAlloc_266_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v_reuseFailAlloc_266_, 0, v___x_250_);
lean_ctor_set(v_reuseFailAlloc_266_, 1, v___y_254_);
v___x_256_ = v_reuseFailAlloc_266_;
goto v_reusejp_255_;
}
v_reusejp_255_:
{
lean_object* v___x_257_; lean_object* v___x_258_; lean_object* v___x_259_; lean_object* v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; lean_object* v___x_263_; lean_object* v___x_264_; lean_object* v___x_265_; 
v___x_257_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_257_, 0, v___x_256_);
lean_ctor_set_uint8(v___x_257_, sizeof(void*)*1, v___y_253_);
v___x_258_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_258_, 0, v___y_252_);
lean_ctor_set(v___x_258_, 1, v___x_257_);
v___x_259_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__10, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__10_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__10);
v___x_260_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__11));
v___x_261_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_261_, 0, v___x_260_);
lean_ctor_set(v___x_261_, 1, v___x_258_);
v___x_262_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__12));
v___x_263_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_263_, 0, v___x_261_);
lean_ctor_set(v___x_263_, 1, v___x_262_);
v___x_264_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_264_, 0, v___x_259_);
lean_ctor_set(v___x_264_, 1, v___x_263_);
v___x_265_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_265_, 0, v___x_264_);
lean_ctor_set_uint8(v___x_265_, sizeof(void*)*1, v___y_253_);
return v___x_265_;
}
}
v___jp_267_:
{
lean_object* v___x_269_; uint8_t v___x_270_; lean_object* v___x_271_; lean_object* v___x_272_; lean_object* v___x_273_; lean_object* v___x_274_; lean_object* v___x_275_; lean_object* v___x_276_; lean_object* v___x_277_; lean_object* v___x_278_; lean_object* v___x_279_; lean_object* v___x_280_; lean_object* v___x_281_; uint8_t v___x_282_; 
v___x_269_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_269_, 0, v___x_250_);
lean_ctor_set(v___x_269_, 1, v___y_268_);
v___x_270_ = 0;
v___x_271_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_271_, 0, v___x_269_);
lean_ctor_set_uint8(v___x_271_, sizeof(void*)*1, v___x_270_);
v___x_272_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_272_, 0, v___x_249_);
lean_ctor_set(v___x_272_, 1, v___x_271_);
v___x_273_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__14));
v___x_274_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_274_, 0, v___x_272_);
lean_ctor_set(v___x_274_, 1, v___x_273_);
v___x_275_ = lean_box(1);
v___x_276_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_276_, 0, v___x_274_);
lean_ctor_set(v___x_276_, 1, v___x_275_);
v___x_277_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__16));
v___x_278_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_278_, 0, v___x_276_);
lean_ctor_set(v___x_278_, 1, v___x_277_);
v___x_279_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_279_, 0, v___x_278_);
lean_ctor_set(v___x_279_, 1, v___x_248_);
v___x_280_ = lean_unsigned_to_nat(0u);
v___x_281_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17);
v___x_282_ = lean_int_dec_lt(v_x1_244_, v___x_281_);
if (v___x_282_ == 0)
{
lean_object* v___x_283_; lean_object* v___x_284_; 
v___x_283_ = l_Int_repr(v_x1_244_);
lean_dec(v_x1_244_);
v___x_284_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_284_, 0, v___x_283_);
v___y_252_ = v___x_279_;
v___y_253_ = v___x_270_;
v___y_254_ = v___x_284_;
goto v___jp_251_;
}
else
{
lean_object* v___x_285_; lean_object* v___x_286_; lean_object* v___x_287_; 
v___x_285_ = l_Int_repr(v_x1_244_);
lean_dec(v_x1_244_);
v___x_286_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_286_, 0, v___x_285_);
v___x_287_ = l_Repr_addAppParen(v___x_286_, v___x_280_);
v___y_252_ = v___x_279_;
v___y_253_ = v___x_270_;
v___y_254_ = v___x_287_;
goto v___jp_251_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr(lean_object* v_x_297_, lean_object* v_prec_298_){
_start:
{
lean_object* v___x_299_; 
v___x_299_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg(v_x_297_);
return v___x_299_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___boxed(lean_object* v_x_300_, lean_object* v_prec_301_){
_start:
{
lean_object* v_res_302_; 
v_res_302_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr(v_x_300_, v_prec_301_);
lean_dec(v_prec_301_);
return v_res_302_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_add(lean_object* v_u_305_, lean_object* v_v_306_){
_start:
{
lean_object* v_x0_307_; lean_object* v_x1_308_; lean_object* v_x0_309_; lean_object* v_x1_310_; lean_object* v___x_312_; uint8_t v_isShared_313_; uint8_t v_isSharedCheck_319_; 
v_x0_307_ = lean_ctor_get(v_u_305_, 0);
v_x1_308_ = lean_ctor_get(v_u_305_, 1);
v_x0_309_ = lean_ctor_get(v_v_306_, 0);
v_x1_310_ = lean_ctor_get(v_v_306_, 1);
v_isSharedCheck_319_ = !lean_is_exclusive(v_v_306_);
if (v_isSharedCheck_319_ == 0)
{
v___x_312_ = v_v_306_;
v_isShared_313_ = v_isSharedCheck_319_;
goto v_resetjp_311_;
}
else
{
lean_inc(v_x1_310_);
lean_inc(v_x0_309_);
lean_dec(v_v_306_);
v___x_312_ = lean_box(0);
v_isShared_313_ = v_isSharedCheck_319_;
goto v_resetjp_311_;
}
v_resetjp_311_:
{
lean_object* v___x_314_; lean_object* v___x_315_; lean_object* v___x_317_; 
v___x_314_ = lean_int_add(v_x0_307_, v_x0_309_);
lean_dec(v_x0_309_);
v___x_315_ = lean_int_add(v_x1_308_, v_x1_310_);
lean_dec(v_x1_310_);
if (v_isShared_313_ == 0)
{
lean_ctor_set(v___x_312_, 1, v___x_315_);
lean_ctor_set(v___x_312_, 0, v___x_314_);
v___x_317_ = v___x_312_;
goto v_reusejp_316_;
}
else
{
lean_object* v_reuseFailAlloc_318_; 
v_reuseFailAlloc_318_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_318_, 0, v___x_314_);
lean_ctor_set(v_reuseFailAlloc_318_, 1, v___x_315_);
v___x_317_ = v_reuseFailAlloc_318_;
goto v_reusejp_316_;
}
v_reusejp_316_:
{
return v___x_317_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_add___boxed(lean_object* v_u_320_, lean_object* v_v_321_){
_start:
{
lean_object* v_res_322_; 
v_res_322_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_add(v_u_320_, v_v_321_);
lean_dec_ref(v_u_320_);
return v_res_322_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_smul(lean_object* v_c_323_, lean_object* v_u_324_){
_start:
{
lean_object* v_x0_325_; lean_object* v_x1_326_; lean_object* v___x_328_; uint8_t v_isShared_329_; uint8_t v_isSharedCheck_335_; 
v_x0_325_ = lean_ctor_get(v_u_324_, 0);
v_x1_326_ = lean_ctor_get(v_u_324_, 1);
v_isSharedCheck_335_ = !lean_is_exclusive(v_u_324_);
if (v_isSharedCheck_335_ == 0)
{
v___x_328_ = v_u_324_;
v_isShared_329_ = v_isSharedCheck_335_;
goto v_resetjp_327_;
}
else
{
lean_inc(v_x1_326_);
lean_inc(v_x0_325_);
lean_dec(v_u_324_);
v___x_328_ = lean_box(0);
v_isShared_329_ = v_isSharedCheck_335_;
goto v_resetjp_327_;
}
v_resetjp_327_:
{
lean_object* v___x_330_; lean_object* v___x_331_; lean_object* v___x_333_; 
v___x_330_ = lean_int_mul(v_c_323_, v_x0_325_);
lean_dec(v_x0_325_);
v___x_331_ = lean_int_mul(v_c_323_, v_x1_326_);
lean_dec(v_x1_326_);
if (v_isShared_329_ == 0)
{
lean_ctor_set(v___x_328_, 1, v___x_331_);
lean_ctor_set(v___x_328_, 0, v___x_330_);
v___x_333_ = v___x_328_;
goto v_reusejp_332_;
}
else
{
lean_object* v_reuseFailAlloc_334_; 
v_reuseFailAlloc_334_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_334_, 0, v___x_330_);
lean_ctor_set(v_reuseFailAlloc_334_, 1, v___x_331_);
v___x_333_ = v_reuseFailAlloc_334_;
goto v_reusejp_332_;
}
v_reusejp_332_:
{
return v___x_333_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_smul___boxed(lean_object* v_c_336_, lean_object* v_u_337_){
_start:
{
lean_object* v_res_338_; 
v_res_338_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_Vec2_smul(v_c_336_, v_u_337_);
lean_dec(v_c_336_);
return v_res_338_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_projDump(lean_object* v_u_339_, lean_object* v_v_340_){
_start:
{
lean_object* v_x0_341_; lean_object* v_x1_342_; lean_object* v_x0_343_; lean_object* v_x1_344_; lean_object* v___x_346_; uint8_t v_isShared_347_; uint8_t v_isSharedCheck_354_; 
v_x0_341_ = lean_ctor_get(v_v_340_, 0);
v_x1_342_ = lean_ctor_get(v_v_340_, 1);
v_x0_343_ = lean_ctor_get(v_u_339_, 0);
v_x1_344_ = lean_ctor_get(v_u_339_, 1);
v_isSharedCheck_354_ = !lean_is_exclusive(v_u_339_);
if (v_isSharedCheck_354_ == 0)
{
v___x_346_ = v_u_339_;
v_isShared_347_ = v_isSharedCheck_354_;
goto v_resetjp_345_;
}
else
{
lean_inc(v_x1_344_);
lean_inc(v_x0_343_);
lean_dec(v_u_339_);
v___x_346_ = lean_box(0);
v_isShared_347_ = v_isSharedCheck_354_;
goto v_resetjp_345_;
}
v_resetjp_345_:
{
lean_object* v___x_348_; lean_object* v___x_349_; lean_object* v___x_350_; lean_object* v___x_352_; 
v___x_348_ = lean_int_add(v_x0_341_, v_x1_342_);
v___x_349_ = lean_int_mul(v___x_348_, v_x0_343_);
lean_dec(v_x0_343_);
v___x_350_ = lean_int_mul(v___x_348_, v_x1_344_);
lean_dec(v_x1_344_);
lean_dec(v___x_348_);
if (v_isShared_347_ == 0)
{
lean_ctor_set(v___x_346_, 1, v___x_350_);
lean_ctor_set(v___x_346_, 0, v___x_349_);
v___x_352_ = v___x_346_;
goto v_reusejp_351_;
}
else
{
lean_object* v_reuseFailAlloc_353_; 
v_reuseFailAlloc_353_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_353_, 0, v___x_349_);
lean_ctor_set(v_reuseFailAlloc_353_, 1, v___x_350_);
v___x_352_ = v_reuseFailAlloc_353_;
goto v_reusejp_351_;
}
v_reusejp_351_:
{
return v___x_352_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_projDump___boxed(lean_object* v_u_355_, lean_object* v_v_356_){
_start:
{
lean_object* v_res_357_; 
v_res_357_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_projDump(v_u_355_, v_v_356_);
lean_dec_ref(v_v_356_);
return v_res_357_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0___closed__0(void){
_start:
{
lean_object* v___x_358_; lean_object* v___x_359_; lean_object* v___x_360_; 
v___x_358_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17);
v___x_359_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9);
v___x_360_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_360_, 0, v___x_359_);
lean_ctor_set(v___x_360_, 1, v___x_358_);
return v___x_360_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0(void){
_start:
{
lean_object* v___x_361_; 
v___x_361_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0___closed__0);
return v___x_361_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1___closed__0(void){
_start:
{
lean_object* v___x_362_; lean_object* v___x_363_; lean_object* v___x_364_; 
v___x_362_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprTensorAxiom_repr___closed__9);
v___x_363_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_instReprVec2_repr___redArg___closed__17);
v___x_364_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_364_, 0, v___x_363_);
lean_ctor_set(v___x_364_, 1, v___x_362_);
return v___x_364_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1(void){
_start:
{
lean_object* v___x_365_; 
v___x_365_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1___closed__0);
return v___x_365_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_pauliZ(lean_object* v_v_366_){
_start:
{
lean_object* v_x0_367_; lean_object* v_x1_368_; lean_object* v___x_370_; uint8_t v_isShared_371_; uint8_t v_isSharedCheck_376_; 
v_x0_367_ = lean_ctor_get(v_v_366_, 0);
v_x1_368_ = lean_ctor_get(v_v_366_, 1);
v_isSharedCheck_376_ = !lean_is_exclusive(v_v_366_);
if (v_isSharedCheck_376_ == 0)
{
v___x_370_ = v_v_366_;
v_isShared_371_ = v_isSharedCheck_376_;
goto v_resetjp_369_;
}
else
{
lean_inc(v_x1_368_);
lean_inc(v_x0_367_);
lean_dec(v_v_366_);
v___x_370_ = lean_box(0);
v_isShared_371_ = v_isSharedCheck_376_;
goto v_resetjp_369_;
}
v_resetjp_369_:
{
lean_object* v___x_372_; lean_object* v___x_374_; 
v___x_372_ = lean_int_neg(v_x1_368_);
lean_dec(v_x1_368_);
if (v_isShared_371_ == 0)
{
lean_ctor_set(v___x_370_, 1, v___x_372_);
v___x_374_ = v___x_370_;
goto v_reusejp_373_;
}
else
{
lean_object* v_reuseFailAlloc_375_; 
v_reuseFailAlloc_375_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_375_, 0, v_x0_367_);
lean_ctor_set(v_reuseFailAlloc_375_, 1, v___x_372_);
v___x_374_ = v_reuseFailAlloc_375_;
goto v_reusejp_373_;
}
v_reusejp_373_:
{
return v___x_374_;
}
}
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d2__denom(void){
_start:
{
lean_object* v___x_377_; 
v___x_377_ = lean_unsigned_to_nat(2u);
return v___x_377_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d3__denom(void){
_start:
{
lean_object* v___x_378_; 
v___x_378_ = lean_unsigned_to_nat(3u);
return v___x_378_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_composite__d6__overlap__denom(void){
_start:
{
lean_object* v___x_379_; 
v___x_379_ = lean_unsigned_to_nat(6u);
return v___x_379_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_product__mub__count__d6(void){
_start:
{
lean_object* v___x_380_; 
v___x_380_ = lean_unsigned_to_nat(3u);
return v___x_380_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_gkp__phase__order(lean_object* v_N_381_){
_start:
{
lean_inc(v_N_381_);
return v_N_381_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H062_gkp__phase__order___boxed(lean_object* v_N_382_){
_start:
{
lean_object* v_res_383_; 
v_res_383_ = lp_FiniteQuantum_FableHilbertWalk20260819_H062_gkp__phase__order(v_N_382_);
lean_dec(v_N_382_);
return v_res_383_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H062CompositionTensorMub(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H062_e0);
lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H062_e1);
lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d2__denom = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d2__denom();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d2__denom);
lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d3__denom = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d3__denom();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H062_rational__overlap__d3__denom);
lp_FiniteQuantum_FableHilbertWalk20260819_H062_composite__d6__overlap__denom = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_composite__d6__overlap__denom();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H062_composite__d6__overlap__denom);
lp_FiniteQuantum_FableHilbertWalk20260819_H062_product__mub__count__d6 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H062_product__mub__count__d6();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H062_product__mub__count__d6);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
