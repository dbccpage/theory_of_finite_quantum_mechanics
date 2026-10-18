// Lean compiler output
// Module: WorldFiniteReconstruction
// Imports: public import Init public meta import Init public import WorldPresentation
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
lean_object* lean_nat_sub(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Basis2_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqBasis2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqBasis2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Preparation_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqPreparation(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqPreparation___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_TensorBasis_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqTensorBasis(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqTensorBasis___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_ImportSlot_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqImportSlot(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqImportSlot___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_probabilityCount(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_probabilityCount___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_tensorPair(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_tensorPair___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__1;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_absDiff(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_absDiff___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_stateDistance(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_stateDistance___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_OmegaWorld_importPayload___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 30, .m_capacity = 30, .m_length = 29, .m_data = "three-normalized-preparations"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_importPayload___closed__0_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_importPayload___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "nine-sixteen-mixture"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_importPayload___closed__1_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_importPayload___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 22, .m_capacity = 22, .m_length = 21, .m_data = "four-basis-pair-table"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_importPayload___closed__2_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_importPayload___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 25, .m_capacity = 25, .m_length = 24, .m_data = "finite-l1-born-lipschitz"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___closed__3 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_importPayload___closed__3_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_importPayload___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "three-zero-zero-four"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___closed__4 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_importPayload___closed__4_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_importPayload___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "two-diagonal-effects"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___closed__5 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_importPayload___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_importPayload(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_tensorPair___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_purificationAmplitude___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_importPayload___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__2_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "GaussianRational"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__3 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__3_value;
static const lean_string_object lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 18, .m_capacity = 18, .m_length = 17, .m_data = "i^2=-1 (declared)"};
static const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__4 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*6 + 0, .m_other = 6, .m_tag = 0}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__0_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__1_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__2_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__3_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__4_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__5 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__5_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaWorld_smallestReconstruction = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_smallestReconstruction___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx(uint8_t v_x_1_){
_start:
{
if (v_x_1_ == 0)
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
else
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(1u);
return v___x_3_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_toCtorIdx(uint8_t v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_toCtorIdx___boxed(lean_object* v_x_9_){
_start:
{
uint8_t v_x_4__boxed_10_; lean_object* v_res_11_; 
v_x_4__boxed_10_ = lean_unbox(v_x_9_);
v_res_11_ = lp_FiniteQuantum_OmegaWorld_Basis2_toCtorIdx(v_x_4__boxed_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___redArg(lean_object* v_k_12_){
_start:
{
lean_inc(v_k_12_);
return v_k_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___redArg___boxed(lean_object* v_k_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___redArg(v_k_13_);
lean_dec(v_k_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, uint8_t v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
lean_inc(v_k_19_);
return v_k_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim___boxed(lean_object* v_motive_20_, lean_object* v_ctorIdx_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
uint8_t v_t_boxed_25_; lean_object* v_res_26_; 
v_t_boxed_25_ = lean_unbox(v_t_22_);
v_res_26_ = lp_FiniteQuantum_OmegaWorld_Basis2_ctorElim(v_motive_20_, v_ctorIdx_21_, v_t_boxed_25_, v_h_23_, v_k_24_);
lean_dec(v_k_24_);
lean_dec(v_ctorIdx_21_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___redArg(lean_object* v_zero_27_){
_start:
{
lean_inc(v_zero_27_);
return v_zero_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___redArg___boxed(lean_object* v_zero_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___redArg(v_zero_28_);
lean_dec(v_zero_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim(lean_object* v_motive_30_, uint8_t v_t_31_, lean_object* v_h_32_, lean_object* v_zero_33_){
_start:
{
lean_inc(v_zero_33_);
return v_zero_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim___boxed(lean_object* v_motive_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_zero_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_OmegaWorld_Basis2_zero_elim(v_motive_34_, v_t_boxed_38_, v_h_36_, v_zero_37_);
lean_dec(v_zero_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___redArg(lean_object* v_one_40_){
_start:
{
lean_inc(v_one_40_);
return v_one_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___redArg___boxed(lean_object* v_one_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___redArg(v_one_41_);
lean_dec(v_one_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_one_46_){
_start:
{
lean_inc(v_one_46_);
return v_one_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_one_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_one_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_OmegaWorld_Basis2_one_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_one_50_);
lean_dec(v_one_50_);
return v_res_52_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Basis2_ofNat(lean_object* v_n_53_){
_start:
{
lean_object* v___x_54_; uint8_t v___x_55_; 
v___x_54_ = lean_unsigned_to_nat(0u);
v___x_55_ = lean_nat_dec_le(v_n_53_, v___x_54_);
if (v___x_55_ == 0)
{
uint8_t v___x_56_; 
v___x_56_ = 1;
return v___x_56_;
}
else
{
uint8_t v___x_57_; 
v___x_57_ = 0;
return v___x_57_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Basis2_ofNat___boxed(lean_object* v_n_58_){
_start:
{
uint8_t v_res_59_; lean_object* v_r_60_; 
v_res_59_ = lp_FiniteQuantum_OmegaWorld_Basis2_ofNat(v_n_58_);
lean_dec(v_n_58_);
v_r_60_ = lean_box(v_res_59_);
return v_r_60_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqBasis2(uint8_t v_x_61_, uint8_t v_y_62_){
_start:
{
lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___x_65_; 
v___x_63_ = lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx(v_x_61_);
v___x_64_ = lp_FiniteQuantum_OmegaWorld_Basis2_ctorIdx(v_y_62_);
v___x_65_ = lean_nat_dec_eq(v___x_63_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_63_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqBasis2___boxed(lean_object* v_x_66_, lean_object* v_y_67_){
_start:
{
uint8_t v_x_13__boxed_68_; uint8_t v_y_14__boxed_69_; uint8_t v_res_70_; lean_object* v_r_71_; 
v_x_13__boxed_68_ = lean_unbox(v_x_66_);
v_y_14__boxed_69_ = lean_unbox(v_y_67_);
v_res_70_ = lp_FiniteQuantum_OmegaWorld_instDecidableEqBasis2(v_x_13__boxed_68_, v_y_14__boxed_69_);
v_r_71_ = lean_box(v_res_70_);
return v_r_71_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx(uint8_t v_x_72_){
_start:
{
switch(v_x_72_)
{
case 0:
{
lean_object* v___x_73_; 
v___x_73_ = lean_unsigned_to_nat(0u);
return v___x_73_;
}
case 1:
{
lean_object* v___x_74_; 
v___x_74_ = lean_unsigned_to_nat(1u);
return v___x_74_;
}
default: 
{
lean_object* v___x_75_; 
v___x_75_ = lean_unsigned_to_nat(2u);
return v___x_75_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx___boxed(lean_object* v_x_76_){
_start:
{
uint8_t v_x_boxed_77_; lean_object* v_res_78_; 
v_x_boxed_77_ = lean_unbox(v_x_76_);
v_res_78_ = lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx(v_x_boxed_77_);
return v_res_78_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_toCtorIdx(uint8_t v_x_79_){
_start:
{
lean_object* v___x_80_; 
v___x_80_ = lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx(v_x_79_);
return v___x_80_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_toCtorIdx___boxed(lean_object* v_x_81_){
_start:
{
uint8_t v_x_4__boxed_82_; lean_object* v_res_83_; 
v_x_4__boxed_82_ = lean_unbox(v_x_81_);
v_res_83_ = lp_FiniteQuantum_OmegaWorld_Preparation_toCtorIdx(v_x_4__boxed_82_);
return v_res_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___redArg(lean_object* v_k_84_){
_start:
{
lean_inc(v_k_84_);
return v_k_84_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___redArg___boxed(lean_object* v_k_85_){
_start:
{
lean_object* v_res_86_; 
v_res_86_ = lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___redArg(v_k_85_);
lean_dec(v_k_85_);
return v_res_86_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim(lean_object* v_motive_87_, lean_object* v_ctorIdx_88_, uint8_t v_t_89_, lean_object* v_h_90_, lean_object* v_k_91_){
_start:
{
lean_inc(v_k_91_);
return v_k_91_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim___boxed(lean_object* v_motive_92_, lean_object* v_ctorIdx_93_, lean_object* v_t_94_, lean_object* v_h_95_, lean_object* v_k_96_){
_start:
{
uint8_t v_t_boxed_97_; lean_object* v_res_98_; 
v_t_boxed_97_ = lean_unbox(v_t_94_);
v_res_98_ = lp_FiniteQuantum_OmegaWorld_Preparation_ctorElim(v_motive_92_, v_ctorIdx_93_, v_t_boxed_97_, v_h_95_, v_k_96_);
lean_dec(v_k_96_);
lean_dec(v_ctorIdx_93_);
return v_res_98_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___redArg(lean_object* v_pureZero_99_){
_start:
{
lean_inc(v_pureZero_99_);
return v_pureZero_99_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___redArg___boxed(lean_object* v_pureZero_100_){
_start:
{
lean_object* v_res_101_; 
v_res_101_ = lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___redArg(v_pureZero_100_);
lean_dec(v_pureZero_100_);
return v_res_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim(lean_object* v_motive_102_, uint8_t v_t_103_, lean_object* v_h_104_, lean_object* v_pureZero_105_){
_start:
{
lean_inc(v_pureZero_105_);
return v_pureZero_105_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim___boxed(lean_object* v_motive_106_, lean_object* v_t_107_, lean_object* v_h_108_, lean_object* v_pureZero_109_){
_start:
{
uint8_t v_t_boxed_110_; lean_object* v_res_111_; 
v_t_boxed_110_ = lean_unbox(v_t_107_);
v_res_111_ = lp_FiniteQuantum_OmegaWorld_Preparation_pureZero_elim(v_motive_106_, v_t_boxed_110_, v_h_108_, v_pureZero_109_);
lean_dec(v_pureZero_109_);
return v_res_111_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___redArg(lean_object* v_pureOne_112_){
_start:
{
lean_inc(v_pureOne_112_);
return v_pureOne_112_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___redArg___boxed(lean_object* v_pureOne_113_){
_start:
{
lean_object* v_res_114_; 
v_res_114_ = lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___redArg(v_pureOne_113_);
lean_dec(v_pureOne_113_);
return v_res_114_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim(lean_object* v_motive_115_, uint8_t v_t_116_, lean_object* v_h_117_, lean_object* v_pureOne_118_){
_start:
{
lean_inc(v_pureOne_118_);
return v_pureOne_118_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim___boxed(lean_object* v_motive_119_, lean_object* v_t_120_, lean_object* v_h_121_, lean_object* v_pureOne_122_){
_start:
{
uint8_t v_t_boxed_123_; lean_object* v_res_124_; 
v_t_boxed_123_ = lean_unbox(v_t_120_);
v_res_124_ = lp_FiniteQuantum_OmegaWorld_Preparation_pureOne_elim(v_motive_119_, v_t_boxed_123_, v_h_121_, v_pureOne_122_);
lean_dec(v_pureOne_122_);
return v_res_124_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___redArg(lean_object* v_mixedNineSixteen_125_){
_start:
{
lean_inc(v_mixedNineSixteen_125_);
return v_mixedNineSixteen_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___redArg___boxed(lean_object* v_mixedNineSixteen_126_){
_start:
{
lean_object* v_res_127_; 
v_res_127_ = lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___redArg(v_mixedNineSixteen_126_);
lean_dec(v_mixedNineSixteen_126_);
return v_res_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim(lean_object* v_motive_128_, uint8_t v_t_129_, lean_object* v_h_130_, lean_object* v_mixedNineSixteen_131_){
_start:
{
lean_inc(v_mixedNineSixteen_131_);
return v_mixedNineSixteen_131_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim___boxed(lean_object* v_motive_132_, lean_object* v_t_133_, lean_object* v_h_134_, lean_object* v_mixedNineSixteen_135_){
_start:
{
uint8_t v_t_boxed_136_; lean_object* v_res_137_; 
v_t_boxed_136_ = lean_unbox(v_t_133_);
v_res_137_ = lp_FiniteQuantum_OmegaWorld_Preparation_mixedNineSixteen_elim(v_motive_132_, v_t_boxed_136_, v_h_134_, v_mixedNineSixteen_135_);
lean_dec(v_mixedNineSixteen_135_);
return v_res_137_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_Preparation_ofNat(lean_object* v_n_138_){
_start:
{
lean_object* v___x_139_; uint8_t v___x_140_; 
v___x_139_ = lean_unsigned_to_nat(0u);
v___x_140_ = lean_nat_dec_le(v_n_138_, v___x_139_);
if (v___x_140_ == 0)
{
lean_object* v___x_141_; uint8_t v___x_142_; 
v___x_141_ = lean_unsigned_to_nat(1u);
v___x_142_ = lean_nat_dec_le(v_n_138_, v___x_141_);
if (v___x_142_ == 0)
{
uint8_t v___x_143_; 
v___x_143_ = 2;
return v___x_143_;
}
else
{
uint8_t v___x_144_; 
v___x_144_ = 1;
return v___x_144_;
}
}
else
{
uint8_t v___x_145_; 
v___x_145_ = 0;
return v___x_145_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_Preparation_ofNat___boxed(lean_object* v_n_146_){
_start:
{
uint8_t v_res_147_; lean_object* v_r_148_; 
v_res_147_ = lp_FiniteQuantum_OmegaWorld_Preparation_ofNat(v_n_146_);
lean_dec(v_n_146_);
v_r_148_ = lean_box(v_res_147_);
return v_r_148_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqPreparation(uint8_t v_x_149_, uint8_t v_y_150_){
_start:
{
lean_object* v___x_151_; lean_object* v___x_152_; uint8_t v___x_153_; 
v___x_151_ = lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx(v_x_149_);
v___x_152_ = lp_FiniteQuantum_OmegaWorld_Preparation_ctorIdx(v_y_150_);
v___x_153_ = lean_nat_dec_eq(v___x_151_, v___x_152_);
lean_dec(v___x_152_);
lean_dec(v___x_151_);
return v___x_153_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqPreparation___boxed(lean_object* v_x_154_, lean_object* v_y_155_){
_start:
{
uint8_t v_x_13__boxed_156_; uint8_t v_y_14__boxed_157_; uint8_t v_res_158_; lean_object* v_r_159_; 
v_x_13__boxed_156_ = lean_unbox(v_x_154_);
v_y_14__boxed_157_ = lean_unbox(v_y_155_);
v_res_158_ = lp_FiniteQuantum_OmegaWorld_instDecidableEqPreparation(v_x_13__boxed_156_, v_y_14__boxed_157_);
v_r_159_ = lean_box(v_res_158_);
return v_r_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx(uint8_t v_x_160_){
_start:
{
switch(v_x_160_)
{
case 0:
{
lean_object* v___x_161_; 
v___x_161_ = lean_unsigned_to_nat(0u);
return v___x_161_;
}
case 1:
{
lean_object* v___x_162_; 
v___x_162_ = lean_unsigned_to_nat(1u);
return v___x_162_;
}
case 2:
{
lean_object* v___x_163_; 
v___x_163_ = lean_unsigned_to_nat(2u);
return v___x_163_;
}
default: 
{
lean_object* v___x_164_; 
v___x_164_ = lean_unsigned_to_nat(3u);
return v___x_164_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx___boxed(lean_object* v_x_165_){
_start:
{
uint8_t v_x_boxed_166_; lean_object* v_res_167_; 
v_x_boxed_166_ = lean_unbox(v_x_165_);
v_res_167_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx(v_x_boxed_166_);
return v_res_167_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_toCtorIdx(uint8_t v_x_168_){
_start:
{
lean_object* v___x_169_; 
v___x_169_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx(v_x_168_);
return v___x_169_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_toCtorIdx___boxed(lean_object* v_x_170_){
_start:
{
uint8_t v_x_4__boxed_171_; lean_object* v_res_172_; 
v_x_4__boxed_171_ = lean_unbox(v_x_170_);
v_res_172_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_toCtorIdx(v_x_4__boxed_171_);
return v_res_172_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___redArg(lean_object* v_k_173_){
_start:
{
lean_inc(v_k_173_);
return v_k_173_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___redArg___boxed(lean_object* v_k_174_){
_start:
{
lean_object* v_res_175_; 
v_res_175_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___redArg(v_k_174_);
lean_dec(v_k_174_);
return v_res_175_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim(lean_object* v_motive_176_, lean_object* v_ctorIdx_177_, uint8_t v_t_178_, lean_object* v_h_179_, lean_object* v_k_180_){
_start:
{
lean_inc(v_k_180_);
return v_k_180_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim___boxed(lean_object* v_motive_181_, lean_object* v_ctorIdx_182_, lean_object* v_t_183_, lean_object* v_h_184_, lean_object* v_k_185_){
_start:
{
uint8_t v_t_boxed_186_; lean_object* v_res_187_; 
v_t_boxed_186_ = lean_unbox(v_t_183_);
v_res_187_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorElim(v_motive_181_, v_ctorIdx_182_, v_t_boxed_186_, v_h_184_, v_k_185_);
lean_dec(v_k_185_);
lean_dec(v_ctorIdx_182_);
return v_res_187_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___redArg(lean_object* v_zeroZero_188_){
_start:
{
lean_inc(v_zeroZero_188_);
return v_zeroZero_188_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___redArg___boxed(lean_object* v_zeroZero_189_){
_start:
{
lean_object* v_res_190_; 
v_res_190_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___redArg(v_zeroZero_189_);
lean_dec(v_zeroZero_189_);
return v_res_190_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim(lean_object* v_motive_191_, uint8_t v_t_192_, lean_object* v_h_193_, lean_object* v_zeroZero_194_){
_start:
{
lean_inc(v_zeroZero_194_);
return v_zeroZero_194_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim___boxed(lean_object* v_motive_195_, lean_object* v_t_196_, lean_object* v_h_197_, lean_object* v_zeroZero_198_){
_start:
{
uint8_t v_t_boxed_199_; lean_object* v_res_200_; 
v_t_boxed_199_ = lean_unbox(v_t_196_);
v_res_200_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroZero_elim(v_motive_195_, v_t_boxed_199_, v_h_197_, v_zeroZero_198_);
lean_dec(v_zeroZero_198_);
return v_res_200_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___redArg(lean_object* v_zeroOne_201_){
_start:
{
lean_inc(v_zeroOne_201_);
return v_zeroOne_201_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___redArg___boxed(lean_object* v_zeroOne_202_){
_start:
{
lean_object* v_res_203_; 
v_res_203_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___redArg(v_zeroOne_202_);
lean_dec(v_zeroOne_202_);
return v_res_203_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim(lean_object* v_motive_204_, uint8_t v_t_205_, lean_object* v_h_206_, lean_object* v_zeroOne_207_){
_start:
{
lean_inc(v_zeroOne_207_);
return v_zeroOne_207_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim___boxed(lean_object* v_motive_208_, lean_object* v_t_209_, lean_object* v_h_210_, lean_object* v_zeroOne_211_){
_start:
{
uint8_t v_t_boxed_212_; lean_object* v_res_213_; 
v_t_boxed_212_ = lean_unbox(v_t_209_);
v_res_213_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_zeroOne_elim(v_motive_208_, v_t_boxed_212_, v_h_210_, v_zeroOne_211_);
lean_dec(v_zeroOne_211_);
return v_res_213_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___redArg(lean_object* v_oneZero_214_){
_start:
{
lean_inc(v_oneZero_214_);
return v_oneZero_214_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___redArg___boxed(lean_object* v_oneZero_215_){
_start:
{
lean_object* v_res_216_; 
v_res_216_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___redArg(v_oneZero_215_);
lean_dec(v_oneZero_215_);
return v_res_216_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim(lean_object* v_motive_217_, uint8_t v_t_218_, lean_object* v_h_219_, lean_object* v_oneZero_220_){
_start:
{
lean_inc(v_oneZero_220_);
return v_oneZero_220_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim___boxed(lean_object* v_motive_221_, lean_object* v_t_222_, lean_object* v_h_223_, lean_object* v_oneZero_224_){
_start:
{
uint8_t v_t_boxed_225_; lean_object* v_res_226_; 
v_t_boxed_225_ = lean_unbox(v_t_222_);
v_res_226_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_oneZero_elim(v_motive_221_, v_t_boxed_225_, v_h_223_, v_oneZero_224_);
lean_dec(v_oneZero_224_);
return v_res_226_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___redArg(lean_object* v_oneOne_227_){
_start:
{
lean_inc(v_oneOne_227_);
return v_oneOne_227_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___redArg___boxed(lean_object* v_oneOne_228_){
_start:
{
lean_object* v_res_229_; 
v_res_229_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___redArg(v_oneOne_228_);
lean_dec(v_oneOne_228_);
return v_res_229_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim(lean_object* v_motive_230_, uint8_t v_t_231_, lean_object* v_h_232_, lean_object* v_oneOne_233_){
_start:
{
lean_inc(v_oneOne_233_);
return v_oneOne_233_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim___boxed(lean_object* v_motive_234_, lean_object* v_t_235_, lean_object* v_h_236_, lean_object* v_oneOne_237_){
_start:
{
uint8_t v_t_boxed_238_; lean_object* v_res_239_; 
v_t_boxed_238_ = lean_unbox(v_t_235_);
v_res_239_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_oneOne_elim(v_motive_234_, v_t_boxed_238_, v_h_236_, v_oneOne_237_);
lean_dec(v_oneOne_237_);
return v_res_239_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_TensorBasis_ofNat(lean_object* v_n_240_){
_start:
{
lean_object* v___x_241_; uint8_t v___x_242_; 
v___x_241_ = lean_unsigned_to_nat(1u);
v___x_242_ = lean_nat_dec_le(v_n_240_, v___x_241_);
if (v___x_242_ == 0)
{
lean_object* v___x_243_; uint8_t v___x_244_; 
v___x_243_ = lean_unsigned_to_nat(2u);
v___x_244_ = lean_nat_dec_le(v_n_240_, v___x_243_);
if (v___x_244_ == 0)
{
uint8_t v___x_245_; 
v___x_245_ = 3;
return v___x_245_;
}
else
{
uint8_t v___x_246_; 
v___x_246_ = 2;
return v___x_246_;
}
}
else
{
lean_object* v___x_247_; uint8_t v___x_248_; 
v___x_247_ = lean_unsigned_to_nat(0u);
v___x_248_ = lean_nat_dec_le(v_n_240_, v___x_247_);
if (v___x_248_ == 0)
{
uint8_t v___x_249_; 
v___x_249_ = 1;
return v___x_249_;
}
else
{
uint8_t v___x_250_; 
v___x_250_ = 0;
return v___x_250_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_TensorBasis_ofNat___boxed(lean_object* v_n_251_){
_start:
{
uint8_t v_res_252_; lean_object* v_r_253_; 
v_res_252_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ofNat(v_n_251_);
lean_dec(v_n_251_);
v_r_253_ = lean_box(v_res_252_);
return v_r_253_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqTensorBasis(uint8_t v_x_254_, uint8_t v_y_255_){
_start:
{
lean_object* v___x_256_; lean_object* v___x_257_; uint8_t v___x_258_; 
v___x_256_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx(v_x_254_);
v___x_257_ = lp_FiniteQuantum_OmegaWorld_TensorBasis_ctorIdx(v_y_255_);
v___x_258_ = lean_nat_dec_eq(v___x_256_, v___x_257_);
lean_dec(v___x_257_);
lean_dec(v___x_256_);
return v___x_258_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqTensorBasis___boxed(lean_object* v_x_259_, lean_object* v_y_260_){
_start:
{
uint8_t v_x_13__boxed_261_; uint8_t v_y_14__boxed_262_; uint8_t v_res_263_; lean_object* v_r_264_; 
v_x_13__boxed_261_ = lean_unbox(v_x_259_);
v_y_14__boxed_262_ = lean_unbox(v_y_260_);
v_res_263_ = lp_FiniteQuantum_OmegaWorld_instDecidableEqTensorBasis(v_x_13__boxed_261_, v_y_14__boxed_262_);
v_r_264_ = lean_box(v_res_263_);
return v_r_264_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx(uint8_t v_x_265_){
_start:
{
switch(v_x_265_)
{
case 0:
{
lean_object* v___x_266_; 
v___x_266_ = lean_unsigned_to_nat(0u);
return v___x_266_;
}
case 1:
{
lean_object* v___x_267_; 
v___x_267_ = lean_unsigned_to_nat(1u);
return v___x_267_;
}
case 2:
{
lean_object* v___x_268_; 
v___x_268_ = lean_unsigned_to_nat(2u);
return v___x_268_;
}
case 3:
{
lean_object* v___x_269_; 
v___x_269_ = lean_unsigned_to_nat(3u);
return v___x_269_;
}
case 4:
{
lean_object* v___x_270_; 
v___x_270_ = lean_unsigned_to_nat(4u);
return v___x_270_;
}
default: 
{
lean_object* v___x_271_; 
v___x_271_ = lean_unsigned_to_nat(5u);
return v___x_271_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx___boxed(lean_object* v_x_272_){
_start:
{
uint8_t v_x_boxed_273_; lean_object* v_res_274_; 
v_x_boxed_273_ = lean_unbox(v_x_272_);
v_res_274_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx(v_x_boxed_273_);
return v_res_274_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_toCtorIdx(uint8_t v_x_275_){
_start:
{
lean_object* v___x_276_; 
v___x_276_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx(v_x_275_);
return v___x_276_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_toCtorIdx___boxed(lean_object* v_x_277_){
_start:
{
uint8_t v_x_4__boxed_278_; lean_object* v_res_279_; 
v_x_4__boxed_278_ = lean_unbox(v_x_277_);
v_res_279_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_toCtorIdx(v_x_4__boxed_278_);
return v_res_279_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___redArg(lean_object* v_k_280_){
_start:
{
lean_inc(v_k_280_);
return v_k_280_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___redArg___boxed(lean_object* v_k_281_){
_start:
{
lean_object* v_res_282_; 
v_res_282_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___redArg(v_k_281_);
lean_dec(v_k_281_);
return v_res_282_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim(lean_object* v_motive_283_, lean_object* v_ctorIdx_284_, uint8_t v_t_285_, lean_object* v_h_286_, lean_object* v_k_287_){
_start:
{
lean_inc(v_k_287_);
return v_k_287_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim___boxed(lean_object* v_motive_288_, lean_object* v_ctorIdx_289_, lean_object* v_t_290_, lean_object* v_h_291_, lean_object* v_k_292_){
_start:
{
uint8_t v_t_boxed_293_; lean_object* v_res_294_; 
v_t_boxed_293_ = lean_unbox(v_t_290_);
v_res_294_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorElim(v_motive_288_, v_ctorIdx_289_, v_t_boxed_293_, v_h_291_, v_k_292_);
lean_dec(v_k_292_);
lean_dec(v_ctorIdx_289_);
return v_res_294_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___redArg(lean_object* v_operational_295_){
_start:
{
lean_inc(v_operational_295_);
return v_operational_295_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___redArg___boxed(lean_object* v_operational_296_){
_start:
{
lean_object* v_res_297_; 
v_res_297_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___redArg(v_operational_296_);
lean_dec(v_operational_296_);
return v_res_297_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim(lean_object* v_motive_298_, uint8_t v_t_299_, lean_object* v_h_300_, lean_object* v_operational_301_){
_start:
{
lean_inc(v_operational_301_);
return v_operational_301_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim___boxed(lean_object* v_motive_302_, lean_object* v_t_303_, lean_object* v_h_304_, lean_object* v_operational_305_){
_start:
{
uint8_t v_t_boxed_306_; lean_object* v_res_307_; 
v_t_boxed_306_ = lean_unbox(v_t_303_);
v_res_307_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_operational_elim(v_motive_302_, v_t_boxed_306_, v_h_304_, v_operational_305_);
lean_dec(v_operational_305_);
return v_res_307_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___redArg(lean_object* v_convex_308_){
_start:
{
lean_inc(v_convex_308_);
return v_convex_308_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___redArg___boxed(lean_object* v_convex_309_){
_start:
{
lean_object* v_res_310_; 
v_res_310_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___redArg(v_convex_309_);
lean_dec(v_convex_309_);
return v_res_310_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim(lean_object* v_motive_311_, uint8_t v_t_312_, lean_object* v_h_313_, lean_object* v_convex_314_){
_start:
{
lean_inc(v_convex_314_);
return v_convex_314_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim___boxed(lean_object* v_motive_315_, lean_object* v_t_316_, lean_object* v_h_317_, lean_object* v_convex_318_){
_start:
{
uint8_t v_t_boxed_319_; lean_object* v_res_320_; 
v_t_boxed_319_ = lean_unbox(v_t_316_);
v_res_320_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_convex_elim(v_motive_315_, v_t_boxed_319_, v_h_317_, v_convex_318_);
lean_dec(v_convex_318_);
return v_res_320_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___redArg(lean_object* v_tensor_321_){
_start:
{
lean_inc(v_tensor_321_);
return v_tensor_321_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___redArg___boxed(lean_object* v_tensor_322_){
_start:
{
lean_object* v_res_323_; 
v_res_323_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___redArg(v_tensor_322_);
lean_dec(v_tensor_322_);
return v_res_323_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim(lean_object* v_motive_324_, uint8_t v_t_325_, lean_object* v_h_326_, lean_object* v_tensor_327_){
_start:
{
lean_inc(v_tensor_327_);
return v_tensor_327_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim___boxed(lean_object* v_motive_328_, lean_object* v_t_329_, lean_object* v_h_330_, lean_object* v_tensor_331_){
_start:
{
uint8_t v_t_boxed_332_; lean_object* v_res_333_; 
v_t_boxed_332_ = lean_unbox(v_t_329_);
v_res_333_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_tensor_elim(v_motive_328_, v_t_boxed_332_, v_h_330_, v_tensor_331_);
lean_dec(v_tensor_331_);
return v_res_333_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___redArg(lean_object* v_continuity_334_){
_start:
{
lean_inc(v_continuity_334_);
return v_continuity_334_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___redArg___boxed(lean_object* v_continuity_335_){
_start:
{
lean_object* v_res_336_; 
v_res_336_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___redArg(v_continuity_335_);
lean_dec(v_continuity_335_);
return v_res_336_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim(lean_object* v_motive_337_, uint8_t v_t_338_, lean_object* v_h_339_, lean_object* v_continuity_340_){
_start:
{
lean_inc(v_continuity_340_);
return v_continuity_340_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim___boxed(lean_object* v_motive_341_, lean_object* v_t_342_, lean_object* v_h_343_, lean_object* v_continuity_344_){
_start:
{
uint8_t v_t_boxed_345_; lean_object* v_res_346_; 
v_t_boxed_345_ = lean_unbox(v_t_342_);
v_res_346_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_continuity_elim(v_motive_341_, v_t_boxed_345_, v_h_343_, v_continuity_344_);
lean_dec(v_continuity_344_);
return v_res_346_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___redArg(lean_object* v_purification_347_){
_start:
{
lean_inc(v_purification_347_);
return v_purification_347_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___redArg___boxed(lean_object* v_purification_348_){
_start:
{
lean_object* v_res_349_; 
v_res_349_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___redArg(v_purification_348_);
lean_dec(v_purification_348_);
return v_res_349_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim(lean_object* v_motive_350_, uint8_t v_t_351_, lean_object* v_h_352_, lean_object* v_purification_353_){
_start:
{
lean_inc(v_purification_353_);
return v_purification_353_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim___boxed(lean_object* v_motive_354_, lean_object* v_t_355_, lean_object* v_h_356_, lean_object* v_purification_357_){
_start:
{
uint8_t v_t_boxed_358_; lean_object* v_res_359_; 
v_t_boxed_358_ = lean_unbox(v_t_355_);
v_res_359_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_purification_elim(v_motive_354_, v_t_boxed_358_, v_h_356_, v_purification_357_);
lean_dec(v_purification_357_);
return v_res_359_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___redArg(lean_object* v_born_360_){
_start:
{
lean_inc(v_born_360_);
return v_born_360_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___redArg___boxed(lean_object* v_born_361_){
_start:
{
lean_object* v_res_362_; 
v_res_362_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___redArg(v_born_361_);
lean_dec(v_born_361_);
return v_res_362_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim(lean_object* v_motive_363_, uint8_t v_t_364_, lean_object* v_h_365_, lean_object* v_born_366_){
_start:
{
lean_inc(v_born_366_);
return v_born_366_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim___boxed(lean_object* v_motive_367_, lean_object* v_t_368_, lean_object* v_h_369_, lean_object* v_born_370_){
_start:
{
uint8_t v_t_boxed_371_; lean_object* v_res_372_; 
v_t_boxed_371_ = lean_unbox(v_t_368_);
v_res_372_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_born_elim(v_motive_367_, v_t_boxed_371_, v_h_369_, v_born_370_);
lean_dec(v_born_370_);
return v_res_372_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_ImportSlot_ofNat(lean_object* v_n_373_){
_start:
{
lean_object* v___x_374_; uint8_t v___x_375_; 
v___x_374_ = lean_unsigned_to_nat(2u);
v___x_375_ = lean_nat_dec_le(v_n_373_, v___x_374_);
if (v___x_375_ == 0)
{
lean_object* v___x_376_; uint8_t v___x_377_; 
v___x_376_ = lean_unsigned_to_nat(3u);
v___x_377_ = lean_nat_dec_le(v_n_373_, v___x_376_);
if (v___x_377_ == 0)
{
lean_object* v___x_378_; uint8_t v___x_379_; 
v___x_378_ = lean_unsigned_to_nat(4u);
v___x_379_ = lean_nat_dec_le(v_n_373_, v___x_378_);
if (v___x_379_ == 0)
{
uint8_t v___x_380_; 
v___x_380_ = 5;
return v___x_380_;
}
else
{
uint8_t v___x_381_; 
v___x_381_ = 4;
return v___x_381_;
}
}
else
{
uint8_t v___x_382_; 
v___x_382_ = 3;
return v___x_382_;
}
}
else
{
lean_object* v___x_383_; uint8_t v___x_384_; 
v___x_383_ = lean_unsigned_to_nat(0u);
v___x_384_ = lean_nat_dec_le(v_n_373_, v___x_383_);
if (v___x_384_ == 0)
{
lean_object* v___x_385_; uint8_t v___x_386_; 
v___x_385_ = lean_unsigned_to_nat(1u);
v___x_386_ = lean_nat_dec_le(v_n_373_, v___x_385_);
if (v___x_386_ == 0)
{
uint8_t v___x_387_; 
v___x_387_ = 2;
return v___x_387_;
}
else
{
uint8_t v___x_388_; 
v___x_388_ = 1;
return v___x_388_;
}
}
else
{
uint8_t v___x_389_; 
v___x_389_ = 0;
return v___x_389_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_ImportSlot_ofNat___boxed(lean_object* v_n_390_){
_start:
{
uint8_t v_res_391_; lean_object* v_r_392_; 
v_res_391_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ofNat(v_n_390_);
lean_dec(v_n_390_);
v_r_392_ = lean_box(v_res_391_);
return v_r_392_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqImportSlot(uint8_t v_x_393_, uint8_t v_y_394_){
_start:
{
lean_object* v___x_395_; lean_object* v___x_396_; uint8_t v___x_397_; 
v___x_395_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx(v_x_393_);
v___x_396_ = lp_FiniteQuantum_OmegaWorld_ImportSlot_ctorIdx(v_y_394_);
v___x_397_ = lean_nat_dec_eq(v___x_395_, v___x_396_);
lean_dec(v___x_396_);
lean_dec(v___x_395_);
return v___x_397_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqImportSlot___boxed(lean_object* v_x_398_, lean_object* v_y_399_){
_start:
{
uint8_t v_x_13__boxed_400_; uint8_t v_y_14__boxed_401_; uint8_t v_res_402_; lean_object* v_r_403_; 
v_x_13__boxed_400_ = lean_unbox(v_x_398_);
v_y_14__boxed_401_ = lean_unbox(v_y_399_);
v_res_402_ = lp_FiniteQuantum_OmegaWorld_instDecidableEqImportSlot(v_x_13__boxed_400_, v_y_14__boxed_401_);
v_r_403_ = lean_box(v_res_402_);
return v_r_403_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_probabilityCount(uint8_t v_x_404_, uint8_t v_x_405_){
_start:
{
switch(v_x_404_)
{
case 0:
{
if (v_x_405_ == 0)
{
lean_object* v___x_406_; 
v___x_406_ = lean_unsigned_to_nat(25u);
return v___x_406_;
}
else
{
lean_object* v___x_407_; 
v___x_407_ = lean_unsigned_to_nat(0u);
return v___x_407_;
}
}
case 1:
{
if (v_x_405_ == 0)
{
lean_object* v___x_408_; 
v___x_408_ = lean_unsigned_to_nat(0u);
return v___x_408_;
}
else
{
lean_object* v___x_409_; 
v___x_409_ = lean_unsigned_to_nat(25u);
return v___x_409_;
}
}
default: 
{
if (v_x_405_ == 0)
{
lean_object* v___x_410_; 
v___x_410_ = lean_unsigned_to_nat(9u);
return v___x_410_;
}
else
{
lean_object* v___x_411_; 
v___x_411_ = lean_unsigned_to_nat(16u);
return v___x_411_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_probabilityCount___boxed(lean_object* v_x_412_, lean_object* v_x_413_){
_start:
{
uint8_t v_x_58__boxed_414_; uint8_t v_x_59__boxed_415_; lean_object* v_res_416_; 
v_x_58__boxed_414_ = lean_unbox(v_x_412_);
v_x_59__boxed_415_ = lean_unbox(v_x_413_);
v_res_416_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_x_58__boxed_414_, v_x_59__boxed_415_);
return v_res_416_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_tensorPair(uint8_t v_x_417_, uint8_t v_x_418_){
_start:
{
if (v_x_417_ == 0)
{
if (v_x_418_ == 0)
{
uint8_t v___x_419_; 
v___x_419_ = 0;
return v___x_419_;
}
else
{
uint8_t v___x_420_; 
v___x_420_ = 1;
return v___x_420_;
}
}
else
{
if (v_x_418_ == 0)
{
uint8_t v___x_421_; 
v___x_421_ = 2;
return v___x_421_;
}
else
{
uint8_t v___x_422_; 
v___x_422_ = 3;
return v___x_422_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_tensorPair___boxed(lean_object* v_x_423_, lean_object* v_x_424_){
_start:
{
uint8_t v_x_35__boxed_425_; uint8_t v_x_36__boxed_426_; uint8_t v_res_427_; lean_object* v_r_428_; 
v_x_35__boxed_425_ = lean_unbox(v_x_423_);
v_x_36__boxed_426_ = lean_unbox(v_x_424_);
v_res_427_ = lp_FiniteQuantum_OmegaWorld_tensorPair(v_x_35__boxed_425_, v_x_36__boxed_426_);
v_r_428_ = lean_box(v_res_427_);
return v_r_428_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__0(void){
_start:
{
lean_object* v___x_429_; lean_object* v___x_430_; 
v___x_429_ = lean_unsigned_to_nat(3u);
v___x_430_ = lean_nat_to_int(v___x_429_);
return v___x_430_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__1(void){
_start:
{
lean_object* v___x_431_; lean_object* v___x_432_; 
v___x_431_ = lean_unsigned_to_nat(4u);
v___x_432_ = lean_nat_to_int(v___x_431_);
return v___x_432_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__2(void){
_start:
{
lean_object* v___x_433_; lean_object* v___x_434_; 
v___x_433_ = lean_unsigned_to_nat(0u);
v___x_434_ = lean_nat_to_int(v___x_433_);
return v___x_434_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude(uint8_t v_x_435_){
_start:
{
switch(v_x_435_)
{
case 0:
{
lean_object* v___x_436_; 
v___x_436_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__0, &lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__0);
return v___x_436_;
}
case 3:
{
lean_object* v___x_437_; 
v___x_437_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__1, &lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__1);
return v___x_437_;
}
default: 
{
lean_object* v___x_438_; 
v___x_438_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__2, &lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__2_once, _init_lp_FiniteQuantum_OmegaWorld_purificationAmplitude___closed__2);
return v___x_438_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_purificationAmplitude___boxed(lean_object* v_x_439_){
_start:
{
uint8_t v_x_56__boxed_440_; lean_object* v_res_441_; 
v_x_56__boxed_440_ = lean_unbox(v_x_439_);
v_res_441_ = lp_FiniteQuantum_OmegaWorld_purificationAmplitude(v_x_56__boxed_440_);
return v_res_441_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_absDiff(lean_object* v_left_442_, lean_object* v_right_443_){
_start:
{
lean_object* v___x_444_; lean_object* v___x_445_; lean_object* v___x_446_; 
v___x_444_ = lean_nat_sub(v_left_442_, v_right_443_);
v___x_445_ = lean_nat_sub(v_right_443_, v_left_442_);
v___x_446_ = lean_nat_add(v___x_444_, v___x_445_);
lean_dec(v___x_445_);
lean_dec(v___x_444_);
return v___x_446_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_absDiff___boxed(lean_object* v_left_447_, lean_object* v_right_448_){
_start:
{
lean_object* v_res_449_; 
v_res_449_ = lp_FiniteQuantum_OmegaWorld_absDiff(v_left_447_, v_right_448_);
lean_dec(v_right_448_);
lean_dec(v_left_447_);
return v_res_449_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_stateDistance(uint8_t v_left_450_, uint8_t v_right_451_){
_start:
{
uint8_t v___x_452_; lean_object* v___x_453_; lean_object* v___x_454_; lean_object* v___x_455_; uint8_t v___x_456_; lean_object* v___x_457_; lean_object* v___x_458_; lean_object* v___x_459_; lean_object* v___x_460_; 
v___x_452_ = 0;
v___x_453_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_left_450_, v___x_452_);
v___x_454_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_right_451_, v___x_452_);
v___x_455_ = lp_FiniteQuantum_OmegaWorld_absDiff(v___x_453_, v___x_454_);
lean_dec(v___x_454_);
lean_dec(v___x_453_);
v___x_456_ = 1;
v___x_457_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_left_450_, v___x_456_);
v___x_458_ = lp_FiniteQuantum_OmegaWorld_probabilityCount(v_right_451_, v___x_456_);
v___x_459_ = lp_FiniteQuantum_OmegaWorld_absDiff(v___x_457_, v___x_458_);
lean_dec(v___x_458_);
lean_dec(v___x_457_);
v___x_460_ = lean_nat_add(v___x_455_, v___x_459_);
lean_dec(v___x_459_);
lean_dec(v___x_455_);
return v___x_460_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_stateDistance___boxed(lean_object* v_left_461_, lean_object* v_right_462_){
_start:
{
uint8_t v_left_boxed_463_; uint8_t v_right_boxed_464_; lean_object* v_res_465_; 
v_left_boxed_463_ = lean_unbox(v_left_461_);
v_right_boxed_464_ = lean_unbox(v_right_462_);
v_res_465_ = lp_FiniteQuantum_OmegaWorld_stateDistance(v_left_boxed_463_, v_right_boxed_464_);
return v_res_465_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_importPayload(uint8_t v_x_472_){
_start:
{
switch(v_x_472_)
{
case 0:
{
lean_object* v___x_473_; 
v___x_473_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_importPayload___closed__0));
return v___x_473_;
}
case 1:
{
lean_object* v___x_474_; 
v___x_474_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_importPayload___closed__1));
return v___x_474_;
}
case 2:
{
lean_object* v___x_475_; 
v___x_475_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_importPayload___closed__2));
return v___x_475_;
}
case 3:
{
lean_object* v___x_476_; 
v___x_476_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_importPayload___closed__3));
return v___x_476_;
}
case 4:
{
lean_object* v___x_477_; 
v___x_477_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_importPayload___closed__4));
return v___x_477_;
}
default: 
{
lean_object* v___x_478_; 
v___x_478_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_importPayload___closed__5));
return v___x_478_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_importPayload___boxed(lean_object* v_x_479_){
_start:
{
uint8_t v_x_58__boxed_480_; lean_object* v_res_481_; 
v_x_58__boxed_480_ = lean_unbox(v_x_479_);
v_res_481_ = lp_FiniteQuantum_OmegaWorld_importPayload(v_x_58__boxed_480_);
return v_res_481_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_WorldPresentation(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldFiniteReconstruction(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_WorldPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
