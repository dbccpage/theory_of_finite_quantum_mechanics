// Lean compiler output
// Module: WorldGateVacuity
// Imports: public import Init public meta import Init public import PrimitiveDifference
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
lean_object* l_List_reverse___redArg(lean_object*);
uint8_t l_List_instDecidableEqNil___redArg(lean_object*);
lean_object* l_instBEqOfDecidableEq___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
uint8_t l_List_elem___redArg(lean_object*, lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqGateClass(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqGateClass___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___lam__0(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___lam__0___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___lam__0___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*1, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_instBEqOfDecidableEq___redArg___lam__0___boxed, .m_arity = 3, .m_num_fixed = 1, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__0_value)} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__1_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaWorld_GateVacuityW810_observedOutcomes_spec__0___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_observedOutcomes___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_observedOutcomes(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaWorld_GateVacuityW810_observedOutcomes_spec__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_constantPassGate(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_constantPassGate___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_outcomeDelta(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_outcomeDelta___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_gateOutcomePD___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_GateVacuityW810_outcomeDelta___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_gateOutcomePD___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_gateOutcomePD___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_gateOutcomePD = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_gateOutcomePD___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqTwoPoint(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqTwoPoint___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointGate(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointGate___boxed(lean_object*);
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointGate___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__1_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__3 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__3_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__3_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointCertificate___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointCertificate___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointCertificate___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointCertificate = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointCertificate___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3Point(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3Point___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3GateCode(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3GateCode___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Gate(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Gate___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3CodeOf(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3CodeOf___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___redArg___boxed(lean_object**);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___boxed(lean_object**);
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__2_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__1;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__2;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__3;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__4;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__5;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__6;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_toCtorIdx(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqW810AuthorityEffect(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqW810AuthorityEffect___boxed(lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_GateVacuityW810_finiteGateVacuitySurface___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 8, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointFamily___closed__3_value),((lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointCertificate___closed__0_value),((lean_object*)(((size_t)(0) << 1) | 1)),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_finiteGateVacuitySurface___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_finiteGateVacuitySurface___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_finiteGateVacuitySurface = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_finiteGateVacuitySurface___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx___boxed(lean_object* v_x_6_){
_start:
{
uint8_t v_x_boxed_7_; lean_object* v_res_8_; 
v_x_boxed_7_ = lean_unbox(v_x_6_);
v_res_8_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx(v_x_boxed_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_toCtorIdx(uint8_t v_x_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx(v_x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_toCtorIdx___boxed(lean_object* v_x_11_){
_start:
{
uint8_t v_x_4__boxed_12_; lean_object* v_res_13_; 
v_x_4__boxed_12_ = lean_unbox(v_x_11_);
v_res_13_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_toCtorIdx(v_x_4__boxed_12_);
return v_res_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___redArg(lean_object* v_k_14_){
_start:
{
lean_inc(v_k_14_);
return v_k_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___redArg___boxed(lean_object* v_k_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___redArg(v_k_15_);
lean_dec(v_k_15_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim(lean_object* v_motive_17_, lean_object* v_ctorIdx_18_, uint8_t v_t_19_, lean_object* v_h_20_, lean_object* v_k_21_){
_start:
{
lean_inc(v_k_21_);
return v_k_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim___boxed(lean_object* v_motive_22_, lean_object* v_ctorIdx_23_, lean_object* v_t_24_, lean_object* v_h_25_, lean_object* v_k_26_){
_start:
{
uint8_t v_t_boxed_27_; lean_object* v_res_28_; 
v_t_boxed_27_ = lean_unbox(v_t_24_);
v_res_28_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorElim(v_motive_22_, v_ctorIdx_23_, v_t_boxed_27_, v_h_25_, v_k_26_);
lean_dec(v_k_26_);
lean_dec(v_ctorIdx_23_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___redArg(lean_object* v_emptyScope_29_){
_start:
{
lean_inc(v_emptyScope_29_);
return v_emptyScope_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___redArg___boxed(lean_object* v_emptyScope_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___redArg(v_emptyScope_30_);
lean_dec(v_emptyScope_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim(lean_object* v_motive_32_, uint8_t v_t_33_, lean_object* v_h_34_, lean_object* v_emptyScope_35_){
_start:
{
lean_inc(v_emptyScope_35_);
return v_emptyScope_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim___boxed(lean_object* v_motive_36_, lean_object* v_t_37_, lean_object* v_h_38_, lean_object* v_emptyScope_39_){
_start:
{
uint8_t v_t_boxed_40_; lean_object* v_res_41_; 
v_t_boxed_40_ = lean_unbox(v_t_37_);
v_res_41_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_emptyScope_elim(v_motive_36_, v_t_boxed_40_, v_h_38_, v_emptyScope_39_);
lean_dec(v_emptyScope_39_);
return v_res_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___redArg(lean_object* v_allPass_42_){
_start:
{
lean_inc(v_allPass_42_);
return v_allPass_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___redArg___boxed(lean_object* v_allPass_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___redArg(v_allPass_43_);
lean_dec(v_allPass_43_);
return v_res_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim(lean_object* v_motive_45_, uint8_t v_t_46_, lean_object* v_h_47_, lean_object* v_allPass_48_){
_start:
{
lean_inc(v_allPass_48_);
return v_allPass_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim___boxed(lean_object* v_motive_49_, lean_object* v_t_50_, lean_object* v_h_51_, lean_object* v_allPass_52_){
_start:
{
uint8_t v_t_boxed_53_; lean_object* v_res_54_; 
v_t_boxed_53_ = lean_unbox(v_t_50_);
v_res_54_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allPass_elim(v_motive_49_, v_t_boxed_53_, v_h_51_, v_allPass_52_);
lean_dec(v_allPass_52_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___redArg(lean_object* v_allFail_55_){
_start:
{
lean_inc(v_allFail_55_);
return v_allFail_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___redArg___boxed(lean_object* v_allFail_56_){
_start:
{
lean_object* v_res_57_; 
v_res_57_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___redArg(v_allFail_56_);
lean_dec(v_allFail_56_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim(lean_object* v_motive_58_, uint8_t v_t_59_, lean_object* v_h_60_, lean_object* v_allFail_61_){
_start:
{
lean_inc(v_allFail_61_);
return v_allFail_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim___boxed(lean_object* v_motive_62_, lean_object* v_t_63_, lean_object* v_h_64_, lean_object* v_allFail_65_){
_start:
{
uint8_t v_t_boxed_66_; lean_object* v_res_67_; 
v_t_boxed_66_ = lean_unbox(v_t_63_);
v_res_67_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_allFail_elim(v_motive_62_, v_t_boxed_66_, v_h_64_, v_allFail_65_);
lean_dec(v_allFail_65_);
return v_res_67_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___redArg(lean_object* v_mixed_68_){
_start:
{
lean_inc(v_mixed_68_);
return v_mixed_68_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___redArg___boxed(lean_object* v_mixed_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___redArg(v_mixed_69_);
lean_dec(v_mixed_69_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim(lean_object* v_motive_71_, uint8_t v_t_72_, lean_object* v_h_73_, lean_object* v_mixed_74_){
_start:
{
lean_inc(v_mixed_74_);
return v_mixed_74_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim___boxed(lean_object* v_motive_75_, lean_object* v_t_76_, lean_object* v_h_77_, lean_object* v_mixed_78_){
_start:
{
uint8_t v_t_boxed_79_; lean_object* v_res_80_; 
v_t_boxed_79_ = lean_unbox(v_t_76_);
v_res_80_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_mixed_elim(v_motive_75_, v_t_boxed_79_, v_h_77_, v_mixed_78_);
lean_dec(v_mixed_78_);
return v_res_80_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ofNat(lean_object* v_n_81_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ofNat___boxed(lean_object* v_n_92_){
_start:
{
uint8_t v_res_93_; lean_object* v_r_94_; 
v_res_93_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ofNat(v_n_92_);
lean_dec(v_n_92_);
v_r_94_ = lean_box(v_res_93_);
return v_r_94_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqGateClass(uint8_t v_x_95_, uint8_t v_y_96_){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_97_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx(v_x_95_);
v___x_98_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_GateClass_ctorIdx(v_y_96_);
v___x_99_ = lean_nat_dec_eq(v___x_97_, v___x_98_);
lean_dec(v___x_98_);
lean_dec(v___x_97_);
return v___x_99_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqGateClass___boxed(lean_object* v_x_100_, lean_object* v_y_101_){
_start:
{
uint8_t v_x_13__boxed_102_; uint8_t v_y_14__boxed_103_; uint8_t v_res_104_; lean_object* v_r_105_; 
v_x_13__boxed_102_ = lean_unbox(v_x_100_);
v_y_14__boxed_103_ = lean_unbox(v_y_101_);
v_res_104_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqGateClass(v_x_13__boxed_102_, v_y_14__boxed_103_);
v_r_105_ = lean_box(v_res_104_);
return v_r_105_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___lam__0(uint8_t v___y_106_, uint8_t v___y_107_){
_start:
{
if (v___y_106_ == 0)
{
if (v___y_107_ == 0)
{
uint8_t v___x_108_; 
v___x_108_ = 1;
return v___x_108_;
}
else
{
return v___y_106_;
}
}
else
{
return v___y_107_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___lam__0___boxed(lean_object* v___y_109_, lean_object* v___y_110_){
_start:
{
uint8_t v___y_35__boxed_111_; uint8_t v___y_36__boxed_112_; uint8_t v_res_113_; lean_object* v_r_114_; 
v___y_35__boxed_111_ = lean_unbox(v___y_109_);
v___y_36__boxed_112_ = lean_unbox(v___y_110_);
v_res_113_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___lam__0(v___y_35__boxed_111_, v___y_36__boxed_112_);
v_r_114_ = lean_box(v_res_113_);
return v_r_114_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes(lean_object* v_outcomes_118_){
_start:
{
uint8_t v___x_119_; 
v___x_119_ = l_List_instDecidableEqNil___redArg(v_outcomes_118_);
if (v___x_119_ == 0)
{
lean_object* v___f_120_; uint8_t v___x_121_; lean_object* v___x_122_; uint8_t v___x_123_; 
v___f_120_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___closed__1));
v___x_121_ = 1;
v___x_122_ = lean_box(v___x_121_);
lean_inc(v_outcomes_118_);
v___x_123_ = l_List_elem___redArg(v___f_120_, v___x_122_, v_outcomes_118_);
if (v___x_123_ == 0)
{
uint8_t v___x_124_; 
lean_dec(v_outcomes_118_);
v___x_124_ = 2;
return v___x_124_;
}
else
{
lean_object* v___x_125_; uint8_t v___x_126_; 
v___x_125_ = lean_box(v___x_119_);
v___x_126_ = l_List_elem___redArg(v___f_120_, v___x_125_, v_outcomes_118_);
if (v___x_126_ == 0)
{
uint8_t v___x_127_; 
v___x_127_ = 1;
return v___x_127_;
}
else
{
uint8_t v___x_128_; 
v___x_128_ = 3;
return v___x_128_;
}
}
}
else
{
uint8_t v___x_129_; 
lean_dec(v_outcomes_118_);
v___x_129_ = 0;
return v___x_129_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes___boxed(lean_object* v_outcomes_130_){
_start:
{
uint8_t v_res_131_; lean_object* v_r_132_; 
v_res_131_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes(v_outcomes_130_);
v_r_132_ = lean_box(v_res_131_);
return v_r_132_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaWorld_GateVacuityW810_observedOutcomes_spec__0___redArg(lean_object* v___x_133_, lean_object* v_a_134_, lean_object* v_a_135_){
_start:
{
if (lean_obj_tag(v_a_134_) == 0)
{
lean_object* v___x_136_; 
lean_dec_ref(v___x_133_);
v___x_136_ = l_List_reverse___redArg(v_a_135_);
return v___x_136_;
}
else
{
lean_object* v_head_137_; lean_object* v_tail_138_; lean_object* v___x_140_; uint8_t v_isShared_141_; uint8_t v_isSharedCheck_147_; 
v_head_137_ = lean_ctor_get(v_a_134_, 0);
v_tail_138_ = lean_ctor_get(v_a_134_, 1);
v_isSharedCheck_147_ = !lean_is_exclusive(v_a_134_);
if (v_isSharedCheck_147_ == 0)
{
v___x_140_ = v_a_134_;
v_isShared_141_ = v_isSharedCheck_147_;
goto v_resetjp_139_;
}
else
{
lean_inc(v_tail_138_);
lean_inc(v_head_137_);
lean_dec(v_a_134_);
v___x_140_ = lean_box(0);
v_isShared_141_ = v_isSharedCheck_147_;
goto v_resetjp_139_;
}
v_resetjp_139_:
{
lean_object* v___x_142_; lean_object* v___x_144_; 
lean_inc_ref(v___x_133_);
v___x_142_ = lean_apply_1(v___x_133_, v_head_137_);
if (v_isShared_141_ == 0)
{
lean_ctor_set(v___x_140_, 1, v_a_135_);
lean_ctor_set(v___x_140_, 0, v___x_142_);
v___x_144_ = v___x_140_;
goto v_reusejp_143_;
}
else
{
lean_object* v_reuseFailAlloc_146_; 
v_reuseFailAlloc_146_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_146_, 0, v___x_142_);
lean_ctor_set(v_reuseFailAlloc_146_, 1, v_a_135_);
v___x_144_ = v_reuseFailAlloc_146_;
goto v_reusejp_143_;
}
v_reusejp_143_:
{
v_a_134_ = v_tail_138_;
v_a_135_ = v___x_144_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_observedOutcomes___redArg(lean_object* v_family_148_){
_start:
{
lean_object* v_inputs_149_; lean_object* v_gate_150_; lean_object* v___x_151_; lean_object* v___x_152_; 
v_inputs_149_ = lean_ctor_get(v_family_148_, 0);
lean_inc(v_inputs_149_);
v_gate_150_ = lean_ctor_get(v_family_148_, 1);
lean_inc_ref(v_gate_150_);
lean_dec_ref(v_family_148_);
v___x_151_ = lean_box(0);
v___x_152_ = lp_FiniteQuantum_List_mapTR_loop___at___00OmegaWorld_GateVacuityW810_observedOutcomes_spec__0___redArg(v_gate_150_, v_inputs_149_, v___x_151_);
return v___x_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_observedOutcomes(lean_object* v_00_u03b1_153_, lean_object* v_family_154_){
_start:
{
lean_object* v___x_155_; 
v___x_155_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_observedOutcomes___redArg(v_family_154_);
return v___x_155_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00OmegaWorld_GateVacuityW810_observedOutcomes_spec__0(lean_object* v_00_u03b1_156_, lean_object* v___x_157_, lean_object* v_a_158_, lean_object* v_a_159_){
_start:
{
lean_object* v___x_160_; 
v___x_160_ = lp_FiniteQuantum_List_mapTR_loop___at___00OmegaWorld_GateVacuityW810_observedOutcomes_spec__0___redArg(v___x_157_, v_a_158_, v_a_159_);
return v___x_160_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg(lean_object* v_family_161_){
_start:
{
lean_object* v___x_162_; uint8_t v___x_163_; 
v___x_162_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_observedOutcomes___redArg(v_family_161_);
v___x_163_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classifyOutcomes(v___x_162_);
return v___x_163_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg___boxed(lean_object* v_family_164_){
_start:
{
uint8_t v_res_165_; lean_object* v_r_166_; 
v_res_165_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg(v_family_164_);
v_r_166_ = lean_box(v_res_165_);
return v_r_166_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate(lean_object* v_00_u03b1_167_, lean_object* v_family_168_){
_start:
{
uint8_t v___x_169_; 
v___x_169_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg(v_family_168_);
return v___x_169_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___boxed(lean_object* v_00_u03b1_170_, lean_object* v_family_171_){
_start:
{
uint8_t v_res_172_; lean_object* v_r_173_; 
v_res_172_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate(v_00_u03b1_170_, v_family_171_);
v_r_173_ = lean_box(v_res_172_);
return v_r_173_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_constantPassGate(lean_object* v_00_u03b1_174_, lean_object* v___input_175_){
_start:
{
uint8_t v___x_176_; 
v___x_176_ = 1;
return v___x_176_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_constantPassGate___boxed(lean_object* v_00_u03b1_177_, lean_object* v___input_178_){
_start:
{
uint8_t v_res_179_; lean_object* v_r_180_; 
v_res_179_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_constantPassGate(v_00_u03b1_177_, v___input_178_);
lean_dec(v___input_178_);
v_r_180_ = lean_box(v_res_179_);
return v_r_180_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___redArg(lean_object* v_inst_181_, lean_object* v_hidden_182_, lean_object* v_input_183_){
_start:
{
lean_object* v___x_184_; uint8_t v___x_185_; 
v___x_184_ = lean_apply_2(v_inst_181_, v_input_183_, v_hidden_182_);
v___x_185_ = lean_unbox(v___x_184_);
if (v___x_185_ == 0)
{
uint8_t v___x_186_; 
v___x_186_ = 1;
return v___x_186_;
}
else
{
uint8_t v___x_187_; 
v___x_187_ = 0;
return v___x_187_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___redArg___boxed(lean_object* v_inst_188_, lean_object* v_hidden_189_, lean_object* v_input_190_){
_start:
{
uint8_t v_res_191_; lean_object* v_r_192_; 
v_res_191_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___redArg(v_inst_188_, v_hidden_189_, v_input_190_);
v_r_192_ = lean_box(v_res_191_);
return v_r_192_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt(lean_object* v_00_u03b1_193_, lean_object* v_inst_194_, lean_object* v_hidden_195_, lean_object* v_input_196_){
_start:
{
uint8_t v___x_197_; 
v___x_197_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___redArg(v_inst_194_, v_hidden_195_, v_input_196_);
return v___x_197_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt___boxed(lean_object* v_00_u03b1_198_, lean_object* v_inst_199_, lean_object* v_hidden_200_, lean_object* v_input_201_){
_start:
{
uint8_t v_res_202_; lean_object* v_r_203_; 
v_res_202_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_failOnlyAt(v_00_u03b1_198_, v_inst_199_, v_hidden_200_, v_input_201_);
v_r_203_ = lean_box(v_res_202_);
return v_r_203_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_outcomeDelta(uint8_t v_x_204_, uint8_t v_x_205_){
_start:
{
if (v_x_204_ == 0)
{
return v_x_205_;
}
else
{
if (v_x_205_ == 0)
{
return v_x_204_;
}
else
{
uint8_t v___x_206_; 
v___x_206_ = 0;
return v___x_206_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_outcomeDelta___boxed(lean_object* v_x_207_, lean_object* v_x_208_){
_start:
{
uint8_t v_x_31__boxed_209_; uint8_t v_x_32__boxed_210_; uint8_t v_res_211_; lean_object* v_r_212_; 
v_x_31__boxed_209_ = lean_unbox(v_x_207_);
v_x_32__boxed_210_ = lean_unbox(v_x_208_);
v_res_211_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_outcomeDelta(v_x_31__boxed_209_, v_x_32__boxed_210_);
v_r_212_ = lean_box(v_res_211_);
return v_r_212_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___redArg(uint8_t v_x_213_, uint8_t v_x_214_, lean_object* v_h__1_215_, lean_object* v_h__2_216_, lean_object* v_h__3_217_, lean_object* v_h__4_218_){
_start:
{
if (v_x_213_ == 0)
{
lean_dec(v_h__4_218_);
lean_dec(v_h__3_217_);
if (v_x_214_ == 0)
{
lean_object* v___x_219_; lean_object* v___x_220_; 
lean_dec(v_h__2_216_);
v___x_219_ = lean_box(0);
v___x_220_ = lean_apply_1(v_h__1_215_, v___x_219_);
return v___x_220_;
}
else
{
lean_object* v___x_221_; lean_object* v___x_222_; 
lean_dec(v_h__1_215_);
v___x_221_ = lean_box(0);
v___x_222_ = lean_apply_1(v_h__2_216_, v___x_221_);
return v___x_222_;
}
}
else
{
lean_dec(v_h__2_216_);
lean_dec(v_h__1_215_);
if (v_x_214_ == 0)
{
lean_object* v___x_223_; lean_object* v___x_224_; 
lean_dec(v_h__4_218_);
v___x_223_ = lean_box(0);
v___x_224_ = lean_apply_1(v_h__3_217_, v___x_223_);
return v___x_224_;
}
else
{
lean_object* v___x_225_; lean_object* v___x_226_; 
lean_dec(v_h__3_217_);
v___x_225_ = lean_box(0);
v___x_226_ = lean_apply_1(v_h__4_218_, v___x_225_);
return v___x_226_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___redArg___boxed(lean_object* v_x_227_, lean_object* v_x_228_, lean_object* v_h__1_229_, lean_object* v_h__2_230_, lean_object* v_h__3_231_, lean_object* v_h__4_232_){
_start:
{
uint8_t v_x_46__boxed_233_; uint8_t v_x_47__boxed_234_; lean_object* v_res_235_; 
v_x_46__boxed_233_ = lean_unbox(v_x_227_);
v_x_47__boxed_234_ = lean_unbox(v_x_228_);
v_res_235_ = lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___redArg(v_x_46__boxed_233_, v_x_47__boxed_234_, v_h__1_229_, v_h__2_230_, v_h__3_231_, v_h__4_232_);
return v_res_235_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter(lean_object* v_motive_236_, uint8_t v_x_237_, uint8_t v_x_238_, lean_object* v_h__1_239_, lean_object* v_h__2_240_, lean_object* v_h__3_241_, lean_object* v_h__4_242_){
_start:
{
if (v_x_237_ == 0)
{
lean_dec(v_h__4_242_);
lean_dec(v_h__3_241_);
if (v_x_238_ == 0)
{
lean_object* v___x_243_; lean_object* v___x_244_; 
lean_dec(v_h__2_240_);
v___x_243_ = lean_box(0);
v___x_244_ = lean_apply_1(v_h__1_239_, v___x_243_);
return v___x_244_;
}
else
{
lean_object* v___x_245_; lean_object* v___x_246_; 
lean_dec(v_h__1_239_);
v___x_245_ = lean_box(0);
v___x_246_ = lean_apply_1(v_h__2_240_, v___x_245_);
return v___x_246_;
}
}
else
{
lean_dec(v_h__2_240_);
lean_dec(v_h__1_239_);
if (v_x_238_ == 0)
{
lean_object* v___x_247_; lean_object* v___x_248_; 
lean_dec(v_h__4_242_);
v___x_247_ = lean_box(0);
v___x_248_ = lean_apply_1(v_h__3_241_, v___x_247_);
return v___x_248_;
}
else
{
lean_object* v___x_249_; lean_object* v___x_250_; 
lean_dec(v_h__3_241_);
v___x_249_ = lean_box(0);
v___x_250_ = lean_apply_1(v_h__4_242_, v___x_249_);
return v___x_250_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter___boxed(lean_object* v_motive_251_, lean_object* v_x_252_, lean_object* v_x_253_, lean_object* v_h__1_254_, lean_object* v_h__2_255_, lean_object* v_h__3_256_, lean_object* v_h__4_257_){
_start:
{
uint8_t v_x_68__boxed_258_; uint8_t v_x_69__boxed_259_; lean_object* v_res_260_; 
v_x_68__boxed_258_ = lean_unbox(v_x_252_);
v_x_69__boxed_259_ = lean_unbox(v_x_253_);
v_res_260_ = lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_outcomeDelta_match__1_splitter(v_motive_251_, v_x_68__boxed_258_, v_x_69__boxed_259_, v_h__1_254_, v_h__2_255_, v_h__3_256_, v_h__4_257_);
return v_res_260_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx(uint8_t v_x_263_){
_start:
{
if (v_x_263_ == 0)
{
lean_object* v___x_264_; 
v___x_264_ = lean_unsigned_to_nat(0u);
return v___x_264_;
}
else
{
lean_object* v___x_265_; 
v___x_265_ = lean_unsigned_to_nat(1u);
return v___x_265_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx___boxed(lean_object* v_x_266_){
_start:
{
uint8_t v_x_boxed_267_; lean_object* v_res_268_; 
v_x_boxed_267_ = lean_unbox(v_x_266_);
v_res_268_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx(v_x_boxed_267_);
return v_res_268_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_toCtorIdx(uint8_t v_x_269_){
_start:
{
lean_object* v___x_270_; 
v___x_270_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx(v_x_269_);
return v___x_270_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_toCtorIdx___boxed(lean_object* v_x_271_){
_start:
{
uint8_t v_x_4__boxed_272_; lean_object* v_res_273_; 
v_x_4__boxed_272_ = lean_unbox(v_x_271_);
v_res_273_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_toCtorIdx(v_x_4__boxed_272_);
return v_res_273_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___redArg(lean_object* v_k_274_){
_start:
{
lean_inc(v_k_274_);
return v_k_274_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___redArg___boxed(lean_object* v_k_275_){
_start:
{
lean_object* v_res_276_; 
v_res_276_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___redArg(v_k_275_);
lean_dec(v_k_275_);
return v_res_276_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim(lean_object* v_motive_277_, lean_object* v_ctorIdx_278_, uint8_t v_t_279_, lean_object* v_h_280_, lean_object* v_k_281_){
_start:
{
lean_inc(v_k_281_);
return v_k_281_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim___boxed(lean_object* v_motive_282_, lean_object* v_ctorIdx_283_, lean_object* v_t_284_, lean_object* v_h_285_, lean_object* v_k_286_){
_start:
{
uint8_t v_t_boxed_287_; lean_object* v_res_288_; 
v_t_boxed_287_ = lean_unbox(v_t_284_);
v_res_288_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorElim(v_motive_282_, v_ctorIdx_283_, v_t_boxed_287_, v_h_285_, v_k_286_);
lean_dec(v_k_286_);
lean_dec(v_ctorIdx_283_);
return v_res_288_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___redArg(lean_object* v_passPoint_289_){
_start:
{
lean_inc(v_passPoint_289_);
return v_passPoint_289_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___redArg___boxed(lean_object* v_passPoint_290_){
_start:
{
lean_object* v_res_291_; 
v_res_291_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___redArg(v_passPoint_290_);
lean_dec(v_passPoint_290_);
return v_res_291_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim(lean_object* v_motive_292_, uint8_t v_t_293_, lean_object* v_h_294_, lean_object* v_passPoint_295_){
_start:
{
lean_inc(v_passPoint_295_);
return v_passPoint_295_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim___boxed(lean_object* v_motive_296_, lean_object* v_t_297_, lean_object* v_h_298_, lean_object* v_passPoint_299_){
_start:
{
uint8_t v_t_boxed_300_; lean_object* v_res_301_; 
v_t_boxed_300_ = lean_unbox(v_t_297_);
v_res_301_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_passPoint_elim(v_motive_296_, v_t_boxed_300_, v_h_298_, v_passPoint_299_);
lean_dec(v_passPoint_299_);
return v_res_301_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___redArg(lean_object* v_failPoint_302_){
_start:
{
lean_inc(v_failPoint_302_);
return v_failPoint_302_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___redArg___boxed(lean_object* v_failPoint_303_){
_start:
{
lean_object* v_res_304_; 
v_res_304_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___redArg(v_failPoint_303_);
lean_dec(v_failPoint_303_);
return v_res_304_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim(lean_object* v_motive_305_, uint8_t v_t_306_, lean_object* v_h_307_, lean_object* v_failPoint_308_){
_start:
{
lean_inc(v_failPoint_308_);
return v_failPoint_308_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim___boxed(lean_object* v_motive_309_, lean_object* v_t_310_, lean_object* v_h_311_, lean_object* v_failPoint_312_){
_start:
{
uint8_t v_t_boxed_313_; lean_object* v_res_314_; 
v_t_boxed_313_ = lean_unbox(v_t_310_);
v_res_314_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_failPoint_elim(v_motive_309_, v_t_boxed_313_, v_h_311_, v_failPoint_312_);
lean_dec(v_failPoint_312_);
return v_res_314_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ofNat(lean_object* v_n_315_){
_start:
{
lean_object* v___x_316_; uint8_t v___x_317_; 
v___x_316_ = lean_unsigned_to_nat(0u);
v___x_317_ = lean_nat_dec_le(v_n_315_, v___x_316_);
if (v___x_317_ == 0)
{
uint8_t v___x_318_; 
v___x_318_ = 1;
return v___x_318_;
}
else
{
uint8_t v___x_319_; 
v___x_319_ = 0;
return v___x_319_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ofNat___boxed(lean_object* v_n_320_){
_start:
{
uint8_t v_res_321_; lean_object* v_r_322_; 
v_res_321_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ofNat(v_n_320_);
lean_dec(v_n_320_);
v_r_322_ = lean_box(v_res_321_);
return v_r_322_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqTwoPoint(uint8_t v_x_323_, uint8_t v_y_324_){
_start:
{
lean_object* v___x_325_; lean_object* v___x_326_; uint8_t v___x_327_; 
v___x_325_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx(v_x_323_);
v___x_326_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_TwoPoint_ctorIdx(v_y_324_);
v___x_327_ = lean_nat_dec_eq(v___x_325_, v___x_326_);
lean_dec(v___x_326_);
lean_dec(v___x_325_);
return v___x_327_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqTwoPoint___boxed(lean_object* v_x_328_, lean_object* v_y_329_){
_start:
{
uint8_t v_x_13__boxed_330_; uint8_t v_y_14__boxed_331_; uint8_t v_res_332_; lean_object* v_r_333_; 
v_x_13__boxed_330_ = lean_unbox(v_x_328_);
v_y_14__boxed_331_ = lean_unbox(v_y_329_);
v_res_332_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqTwoPoint(v_x_13__boxed_330_, v_y_14__boxed_331_);
v_r_333_ = lean_box(v_res_332_);
return v_r_333_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointGate(uint8_t v_x_334_){
_start:
{
if (v_x_334_ == 0)
{
uint8_t v___x_335_; 
v___x_335_ = 1;
return v___x_335_;
}
else
{
uint8_t v___x_336_; 
v___x_336_ = 0;
return v___x_336_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointGate___boxed(lean_object* v_x_337_){
_start:
{
uint8_t v_x_18__boxed_338_; uint8_t v_res_339_; lean_object* v_r_340_; 
v_x_18__boxed_338_ = lean_unbox(v_x_337_);
v_res_339_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_twoPointGate(v_x_18__boxed_338_);
v_r_340_ = lean_box(v_res_339_);
return v_r_340_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx(uint8_t v_x_360_){
_start:
{
switch(v_x_360_)
{
case 0:
{
lean_object* v___x_361_; 
v___x_361_ = lean_unsigned_to_nat(0u);
return v___x_361_;
}
case 1:
{
lean_object* v___x_362_; 
v___x_362_ = lean_unsigned_to_nat(1u);
return v___x_362_;
}
default: 
{
lean_object* v___x_363_; 
v___x_363_ = lean_unsigned_to_nat(2u);
return v___x_363_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx___boxed(lean_object* v_x_364_){
_start:
{
uint8_t v_x_boxed_365_; lean_object* v_res_366_; 
v_x_boxed_365_ = lean_unbox(v_x_364_);
v_res_366_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx(v_x_boxed_365_);
return v_res_366_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_toCtorIdx(uint8_t v_x_367_){
_start:
{
lean_object* v___x_368_; 
v___x_368_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx(v_x_367_);
return v___x_368_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_toCtorIdx___boxed(lean_object* v_x_369_){
_start:
{
uint8_t v_x_4__boxed_370_; lean_object* v_res_371_; 
v_x_4__boxed_370_ = lean_unbox(v_x_369_);
v_res_371_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_toCtorIdx(v_x_4__boxed_370_);
return v_res_371_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___redArg(lean_object* v_k_372_){
_start:
{
lean_inc(v_k_372_);
return v_k_372_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___redArg___boxed(lean_object* v_k_373_){
_start:
{
lean_object* v_res_374_; 
v_res_374_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___redArg(v_k_373_);
lean_dec(v_k_373_);
return v_res_374_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim(lean_object* v_motive_375_, lean_object* v_ctorIdx_376_, uint8_t v_t_377_, lean_object* v_h_378_, lean_object* v_k_379_){
_start:
{
lean_inc(v_k_379_);
return v_k_379_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim___boxed(lean_object* v_motive_380_, lean_object* v_ctorIdx_381_, lean_object* v_t_382_, lean_object* v_h_383_, lean_object* v_k_384_){
_start:
{
uint8_t v_t_boxed_385_; lean_object* v_res_386_; 
v_t_boxed_385_ = lean_unbox(v_t_382_);
v_res_386_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorElim(v_motive_380_, v_ctorIdx_381_, v_t_boxed_385_, v_h_383_, v_k_384_);
lean_dec(v_k_384_);
lean_dec(v_ctorIdx_381_);
return v_res_386_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___redArg(lean_object* v_p0_387_){
_start:
{
lean_inc(v_p0_387_);
return v_p0_387_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___redArg___boxed(lean_object* v_p0_388_){
_start:
{
lean_object* v_res_389_; 
v_res_389_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___redArg(v_p0_388_);
lean_dec(v_p0_388_);
return v_res_389_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim(lean_object* v_motive_390_, uint8_t v_t_391_, lean_object* v_h_392_, lean_object* v_p0_393_){
_start:
{
lean_inc(v_p0_393_);
return v_p0_393_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim___boxed(lean_object* v_motive_394_, lean_object* v_t_395_, lean_object* v_h_396_, lean_object* v_p0_397_){
_start:
{
uint8_t v_t_boxed_398_; lean_object* v_res_399_; 
v_t_boxed_398_ = lean_unbox(v_t_395_);
v_res_399_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p0_elim(v_motive_394_, v_t_boxed_398_, v_h_396_, v_p0_397_);
lean_dec(v_p0_397_);
return v_res_399_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___redArg(lean_object* v_p1_400_){
_start:
{
lean_inc(v_p1_400_);
return v_p1_400_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___redArg___boxed(lean_object* v_p1_401_){
_start:
{
lean_object* v_res_402_; 
v_res_402_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___redArg(v_p1_401_);
lean_dec(v_p1_401_);
return v_res_402_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim(lean_object* v_motive_403_, uint8_t v_t_404_, lean_object* v_h_405_, lean_object* v_p1_406_){
_start:
{
lean_inc(v_p1_406_);
return v_p1_406_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim___boxed(lean_object* v_motive_407_, lean_object* v_t_408_, lean_object* v_h_409_, lean_object* v_p1_410_){
_start:
{
uint8_t v_t_boxed_411_; lean_object* v_res_412_; 
v_t_boxed_411_ = lean_unbox(v_t_408_);
v_res_412_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p1_elim(v_motive_407_, v_t_boxed_411_, v_h_409_, v_p1_410_);
lean_dec(v_p1_410_);
return v_res_412_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___redArg(lean_object* v_p2_413_){
_start:
{
lean_inc(v_p2_413_);
return v_p2_413_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___redArg___boxed(lean_object* v_p2_414_){
_start:
{
lean_object* v_res_415_; 
v_res_415_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___redArg(v_p2_414_);
lean_dec(v_p2_414_);
return v_res_415_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim(lean_object* v_motive_416_, uint8_t v_t_417_, lean_object* v_h_418_, lean_object* v_p2_419_){
_start:
{
lean_inc(v_p2_419_);
return v_p2_419_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim___boxed(lean_object* v_motive_420_, lean_object* v_t_421_, lean_object* v_h_422_, lean_object* v_p2_423_){
_start:
{
uint8_t v_t_boxed_424_; lean_object* v_res_425_; 
v_t_boxed_424_ = lean_unbox(v_t_421_);
v_res_425_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_p2_elim(v_motive_420_, v_t_boxed_424_, v_h_422_, v_p2_423_);
lean_dec(v_p2_423_);
return v_res_425_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ofNat(lean_object* v_n_426_){
_start:
{
lean_object* v___x_427_; uint8_t v___x_428_; 
v___x_427_ = lean_unsigned_to_nat(0u);
v___x_428_ = lean_nat_dec_le(v_n_426_, v___x_427_);
if (v___x_428_ == 0)
{
lean_object* v___x_429_; uint8_t v___x_430_; 
v___x_429_ = lean_unsigned_to_nat(1u);
v___x_430_ = lean_nat_dec_le(v_n_426_, v___x_429_);
if (v___x_430_ == 0)
{
uint8_t v___x_431_; 
v___x_431_ = 2;
return v___x_431_;
}
else
{
uint8_t v___x_432_; 
v___x_432_ = 1;
return v___x_432_;
}
}
else
{
uint8_t v___x_433_; 
v___x_433_ = 0;
return v___x_433_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ofNat___boxed(lean_object* v_n_434_){
_start:
{
uint8_t v_res_435_; lean_object* v_r_436_; 
v_res_435_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ofNat(v_n_434_);
lean_dec(v_n_434_);
v_r_436_ = lean_box(v_res_435_);
return v_r_436_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3Point(uint8_t v_x_437_, uint8_t v_y_438_){
_start:
{
lean_object* v___x_439_; lean_object* v___x_440_; uint8_t v___x_441_; 
v___x_439_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx(v_x_437_);
v___x_440_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3Point_ctorIdx(v_y_438_);
v___x_441_ = lean_nat_dec_eq(v___x_439_, v___x_440_);
lean_dec(v___x_440_);
lean_dec(v___x_439_);
return v___x_441_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3Point___boxed(lean_object* v_x_442_, lean_object* v_y_443_){
_start:
{
uint8_t v_x_13__boxed_444_; uint8_t v_y_14__boxed_445_; uint8_t v_res_446_; lean_object* v_r_447_; 
v_x_13__boxed_444_ = lean_unbox(v_x_442_);
v_y_14__boxed_445_ = lean_unbox(v_y_443_);
v_res_446_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3Point(v_x_13__boxed_444_, v_y_14__boxed_445_);
v_r_447_ = lean_box(v_res_446_);
return v_r_447_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx(uint8_t v_x_448_){
_start:
{
switch(v_x_448_)
{
case 0:
{
lean_object* v___x_449_; 
v___x_449_ = lean_unsigned_to_nat(0u);
return v___x_449_;
}
case 1:
{
lean_object* v___x_450_; 
v___x_450_ = lean_unsigned_to_nat(1u);
return v___x_450_;
}
case 2:
{
lean_object* v___x_451_; 
v___x_451_ = lean_unsigned_to_nat(2u);
return v___x_451_;
}
case 3:
{
lean_object* v___x_452_; 
v___x_452_ = lean_unsigned_to_nat(3u);
return v___x_452_;
}
case 4:
{
lean_object* v___x_453_; 
v___x_453_ = lean_unsigned_to_nat(4u);
return v___x_453_;
}
case 5:
{
lean_object* v___x_454_; 
v___x_454_ = lean_unsigned_to_nat(5u);
return v___x_454_;
}
case 6:
{
lean_object* v___x_455_; 
v___x_455_ = lean_unsigned_to_nat(6u);
return v___x_455_;
}
default: 
{
lean_object* v___x_456_; 
v___x_456_ = lean_unsigned_to_nat(7u);
return v___x_456_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx___boxed(lean_object* v_x_457_){
_start:
{
uint8_t v_x_boxed_458_; lean_object* v_res_459_; 
v_x_boxed_458_ = lean_unbox(v_x_457_);
v_res_459_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx(v_x_boxed_458_);
return v_res_459_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_toCtorIdx(uint8_t v_x_460_){
_start:
{
lean_object* v___x_461_; 
v___x_461_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx(v_x_460_);
return v___x_461_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_toCtorIdx___boxed(lean_object* v_x_462_){
_start:
{
uint8_t v_x_4__boxed_463_; lean_object* v_res_464_; 
v_x_4__boxed_463_ = lean_unbox(v_x_462_);
v_res_464_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_toCtorIdx(v_x_4__boxed_463_);
return v_res_464_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___redArg(lean_object* v_k_465_){
_start:
{
lean_inc(v_k_465_);
return v_k_465_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___redArg___boxed(lean_object* v_k_466_){
_start:
{
lean_object* v_res_467_; 
v_res_467_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___redArg(v_k_466_);
lean_dec(v_k_466_);
return v_res_467_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim(lean_object* v_motive_468_, lean_object* v_ctorIdx_469_, uint8_t v_t_470_, lean_object* v_h_471_, lean_object* v_k_472_){
_start:
{
lean_inc(v_k_472_);
return v_k_472_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim___boxed(lean_object* v_motive_473_, lean_object* v_ctorIdx_474_, lean_object* v_t_475_, lean_object* v_h_476_, lean_object* v_k_477_){
_start:
{
uint8_t v_t_boxed_478_; lean_object* v_res_479_; 
v_t_boxed_478_ = lean_unbox(v_t_475_);
v_res_479_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorElim(v_motive_473_, v_ctorIdx_474_, v_t_boxed_478_, v_h_476_, v_k_477_);
lean_dec(v_k_477_);
lean_dec(v_ctorIdx_474_);
return v_res_479_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___redArg(lean_object* v_fff_480_){
_start:
{
lean_inc(v_fff_480_);
return v_fff_480_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___redArg___boxed(lean_object* v_fff_481_){
_start:
{
lean_object* v_res_482_; 
v_res_482_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___redArg(v_fff_481_);
lean_dec(v_fff_481_);
return v_res_482_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim(lean_object* v_motive_483_, uint8_t v_t_484_, lean_object* v_h_485_, lean_object* v_fff_486_){
_start:
{
lean_inc(v_fff_486_);
return v_fff_486_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim___boxed(lean_object* v_motive_487_, lean_object* v_t_488_, lean_object* v_h_489_, lean_object* v_fff_490_){
_start:
{
uint8_t v_t_boxed_491_; lean_object* v_res_492_; 
v_t_boxed_491_ = lean_unbox(v_t_488_);
v_res_492_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fff_elim(v_motive_487_, v_t_boxed_491_, v_h_489_, v_fff_490_);
lean_dec(v_fff_490_);
return v_res_492_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___redArg(lean_object* v_fft_493_){
_start:
{
lean_inc(v_fft_493_);
return v_fft_493_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___redArg___boxed(lean_object* v_fft_494_){
_start:
{
lean_object* v_res_495_; 
v_res_495_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___redArg(v_fft_494_);
lean_dec(v_fft_494_);
return v_res_495_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim(lean_object* v_motive_496_, uint8_t v_t_497_, lean_object* v_h_498_, lean_object* v_fft_499_){
_start:
{
lean_inc(v_fft_499_);
return v_fft_499_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim___boxed(lean_object* v_motive_500_, lean_object* v_t_501_, lean_object* v_h_502_, lean_object* v_fft_503_){
_start:
{
uint8_t v_t_boxed_504_; lean_object* v_res_505_; 
v_t_boxed_504_ = lean_unbox(v_t_501_);
v_res_505_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_fft_elim(v_motive_500_, v_t_boxed_504_, v_h_502_, v_fft_503_);
lean_dec(v_fft_503_);
return v_res_505_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___redArg(lean_object* v_ftf_506_){
_start:
{
lean_inc(v_ftf_506_);
return v_ftf_506_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___redArg___boxed(lean_object* v_ftf_507_){
_start:
{
lean_object* v_res_508_; 
v_res_508_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___redArg(v_ftf_507_);
lean_dec(v_ftf_507_);
return v_res_508_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim(lean_object* v_motive_509_, uint8_t v_t_510_, lean_object* v_h_511_, lean_object* v_ftf_512_){
_start:
{
lean_inc(v_ftf_512_);
return v_ftf_512_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim___boxed(lean_object* v_motive_513_, lean_object* v_t_514_, lean_object* v_h_515_, lean_object* v_ftf_516_){
_start:
{
uint8_t v_t_boxed_517_; lean_object* v_res_518_; 
v_t_boxed_517_ = lean_unbox(v_t_514_);
v_res_518_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftf_elim(v_motive_513_, v_t_boxed_517_, v_h_515_, v_ftf_516_);
lean_dec(v_ftf_516_);
return v_res_518_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___redArg(lean_object* v_ftt_519_){
_start:
{
lean_inc(v_ftt_519_);
return v_ftt_519_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___redArg___boxed(lean_object* v_ftt_520_){
_start:
{
lean_object* v_res_521_; 
v_res_521_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___redArg(v_ftt_520_);
lean_dec(v_ftt_520_);
return v_res_521_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim(lean_object* v_motive_522_, uint8_t v_t_523_, lean_object* v_h_524_, lean_object* v_ftt_525_){
_start:
{
lean_inc(v_ftt_525_);
return v_ftt_525_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim___boxed(lean_object* v_motive_526_, lean_object* v_t_527_, lean_object* v_h_528_, lean_object* v_ftt_529_){
_start:
{
uint8_t v_t_boxed_530_; lean_object* v_res_531_; 
v_t_boxed_530_ = lean_unbox(v_t_527_);
v_res_531_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ftt_elim(v_motive_526_, v_t_boxed_530_, v_h_528_, v_ftt_529_);
lean_dec(v_ftt_529_);
return v_res_531_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___redArg(lean_object* v_tff_532_){
_start:
{
lean_inc(v_tff_532_);
return v_tff_532_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___redArg___boxed(lean_object* v_tff_533_){
_start:
{
lean_object* v_res_534_; 
v_res_534_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___redArg(v_tff_533_);
lean_dec(v_tff_533_);
return v_res_534_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim(lean_object* v_motive_535_, uint8_t v_t_536_, lean_object* v_h_537_, lean_object* v_tff_538_){
_start:
{
lean_inc(v_tff_538_);
return v_tff_538_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim___boxed(lean_object* v_motive_539_, lean_object* v_t_540_, lean_object* v_h_541_, lean_object* v_tff_542_){
_start:
{
uint8_t v_t_boxed_543_; lean_object* v_res_544_; 
v_t_boxed_543_ = lean_unbox(v_t_540_);
v_res_544_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tff_elim(v_motive_539_, v_t_boxed_543_, v_h_541_, v_tff_542_);
lean_dec(v_tff_542_);
return v_res_544_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___redArg(lean_object* v_tft_545_){
_start:
{
lean_inc(v_tft_545_);
return v_tft_545_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___redArg___boxed(lean_object* v_tft_546_){
_start:
{
lean_object* v_res_547_; 
v_res_547_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___redArg(v_tft_546_);
lean_dec(v_tft_546_);
return v_res_547_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim(lean_object* v_motive_548_, uint8_t v_t_549_, lean_object* v_h_550_, lean_object* v_tft_551_){
_start:
{
lean_inc(v_tft_551_);
return v_tft_551_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim___boxed(lean_object* v_motive_552_, lean_object* v_t_553_, lean_object* v_h_554_, lean_object* v_tft_555_){
_start:
{
uint8_t v_t_boxed_556_; lean_object* v_res_557_; 
v_t_boxed_556_ = lean_unbox(v_t_553_);
v_res_557_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_tft_elim(v_motive_552_, v_t_boxed_556_, v_h_554_, v_tft_555_);
lean_dec(v_tft_555_);
return v_res_557_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___redArg(lean_object* v_ttf_558_){
_start:
{
lean_inc(v_ttf_558_);
return v_ttf_558_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___redArg___boxed(lean_object* v_ttf_559_){
_start:
{
lean_object* v_res_560_; 
v_res_560_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___redArg(v_ttf_559_);
lean_dec(v_ttf_559_);
return v_res_560_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim(lean_object* v_motive_561_, uint8_t v_t_562_, lean_object* v_h_563_, lean_object* v_ttf_564_){
_start:
{
lean_inc(v_ttf_564_);
return v_ttf_564_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim___boxed(lean_object* v_motive_565_, lean_object* v_t_566_, lean_object* v_h_567_, lean_object* v_ttf_568_){
_start:
{
uint8_t v_t_boxed_569_; lean_object* v_res_570_; 
v_t_boxed_569_ = lean_unbox(v_t_566_);
v_res_570_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttf_elim(v_motive_565_, v_t_boxed_569_, v_h_567_, v_ttf_568_);
lean_dec(v_ttf_568_);
return v_res_570_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___redArg(lean_object* v_ttt_571_){
_start:
{
lean_inc(v_ttt_571_);
return v_ttt_571_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___redArg___boxed(lean_object* v_ttt_572_){
_start:
{
lean_object* v_res_573_; 
v_res_573_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___redArg(v_ttt_572_);
lean_dec(v_ttt_572_);
return v_res_573_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim(lean_object* v_motive_574_, uint8_t v_t_575_, lean_object* v_h_576_, lean_object* v_ttt_577_){
_start:
{
lean_inc(v_ttt_577_);
return v_ttt_577_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim___boxed(lean_object* v_motive_578_, lean_object* v_t_579_, lean_object* v_h_580_, lean_object* v_ttt_581_){
_start:
{
uint8_t v_t_boxed_582_; lean_object* v_res_583_; 
v_t_boxed_582_ = lean_unbox(v_t_579_);
v_res_583_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ttt_elim(v_motive_578_, v_t_boxed_582_, v_h_580_, v_ttt_581_);
lean_dec(v_ttt_581_);
return v_res_583_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ofNat(lean_object* v_n_584_){
_start:
{
lean_object* v___x_585_; uint8_t v___x_586_; 
v___x_585_ = lean_unsigned_to_nat(3u);
v___x_586_ = lean_nat_dec_le(v_n_584_, v___x_585_);
if (v___x_586_ == 0)
{
lean_object* v___x_587_; uint8_t v___x_588_; 
v___x_587_ = lean_unsigned_to_nat(5u);
v___x_588_ = lean_nat_dec_le(v_n_584_, v___x_587_);
if (v___x_588_ == 0)
{
lean_object* v___x_589_; uint8_t v___x_590_; 
v___x_589_ = lean_unsigned_to_nat(6u);
v___x_590_ = lean_nat_dec_le(v_n_584_, v___x_589_);
if (v___x_590_ == 0)
{
uint8_t v___x_591_; 
v___x_591_ = 7;
return v___x_591_;
}
else
{
uint8_t v___x_592_; 
v___x_592_ = 6;
return v___x_592_;
}
}
else
{
lean_object* v___x_593_; uint8_t v___x_594_; 
v___x_593_ = lean_unsigned_to_nat(4u);
v___x_594_ = lean_nat_dec_le(v_n_584_, v___x_593_);
if (v___x_594_ == 0)
{
uint8_t v___x_595_; 
v___x_595_ = 5;
return v___x_595_;
}
else
{
uint8_t v___x_596_; 
v___x_596_ = 4;
return v___x_596_;
}
}
}
else
{
lean_object* v___x_597_; uint8_t v___x_598_; 
v___x_597_ = lean_unsigned_to_nat(1u);
v___x_598_ = lean_nat_dec_le(v_n_584_, v___x_597_);
if (v___x_598_ == 0)
{
lean_object* v___x_599_; uint8_t v___x_600_; 
v___x_599_ = lean_unsigned_to_nat(2u);
v___x_600_ = lean_nat_dec_le(v_n_584_, v___x_599_);
if (v___x_600_ == 0)
{
uint8_t v___x_601_; 
v___x_601_ = 3;
return v___x_601_;
}
else
{
uint8_t v___x_602_; 
v___x_602_ = 2;
return v___x_602_;
}
}
else
{
lean_object* v___x_603_; uint8_t v___x_604_; 
v___x_603_ = lean_unsigned_to_nat(0u);
v___x_604_ = lean_nat_dec_le(v_n_584_, v___x_603_);
if (v___x_604_ == 0)
{
uint8_t v___x_605_; 
v___x_605_ = 1;
return v___x_605_;
}
else
{
uint8_t v___x_606_; 
v___x_606_ = 0;
return v___x_606_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ofNat___boxed(lean_object* v_n_607_){
_start:
{
uint8_t v_res_608_; lean_object* v_r_609_; 
v_res_608_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ofNat(v_n_607_);
lean_dec(v_n_607_);
v_r_609_ = lean_box(v_res_608_);
return v_r_609_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3GateCode(uint8_t v_x_610_, uint8_t v_y_611_){
_start:
{
lean_object* v___x_612_; lean_object* v___x_613_; uint8_t v___x_614_; 
v___x_612_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx(v_x_610_);
v___x_613_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_Fin3GateCode_ctorIdx(v_y_611_);
v___x_614_ = lean_nat_dec_eq(v___x_612_, v___x_613_);
lean_dec(v___x_613_);
lean_dec(v___x_612_);
return v___x_614_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3GateCode___boxed(lean_object* v_x_615_, lean_object* v_y_616_){
_start:
{
uint8_t v_x_13__boxed_617_; uint8_t v_y_14__boxed_618_; uint8_t v_res_619_; lean_object* v_r_620_; 
v_x_13__boxed_617_ = lean_unbox(v_x_615_);
v_y_14__boxed_618_ = lean_unbox(v_y_616_);
v_res_619_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqFin3GateCode(v_x_13__boxed_617_, v_y_14__boxed_618_);
v_r_620_ = lean_box(v_res_619_);
return v_r_620_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Gate(uint8_t v_x_621_, uint8_t v_x_622_){
_start:
{
switch(v_x_621_)
{
case 0:
{
uint8_t v___x_623_; 
v___x_623_ = 0;
return v___x_623_;
}
case 1:
{
if (v_x_622_ == 2)
{
uint8_t v___x_624_; 
v___x_624_ = 1;
return v___x_624_;
}
else
{
uint8_t v___x_625_; 
v___x_625_ = 0;
return v___x_625_;
}
}
case 2:
{
if (v_x_622_ == 1)
{
uint8_t v___x_626_; 
v___x_626_ = 1;
return v___x_626_;
}
else
{
uint8_t v___x_627_; 
v___x_627_ = 0;
return v___x_627_;
}
}
case 3:
{
if (v_x_622_ == 0)
{
uint8_t v___x_628_; 
v___x_628_ = 0;
return v___x_628_;
}
else
{
uint8_t v___x_629_; 
v___x_629_ = 1;
return v___x_629_;
}
}
case 4:
{
if (v_x_622_ == 0)
{
uint8_t v___x_630_; 
v___x_630_ = 1;
return v___x_630_;
}
else
{
uint8_t v___x_631_; 
v___x_631_ = 0;
return v___x_631_;
}
}
case 5:
{
if (v_x_622_ == 1)
{
uint8_t v___x_632_; 
v___x_632_ = 0;
return v___x_632_;
}
else
{
uint8_t v___x_633_; 
v___x_633_ = 1;
return v___x_633_;
}
}
case 6:
{
if (v_x_622_ == 2)
{
uint8_t v___x_634_; 
v___x_634_ = 0;
return v___x_634_;
}
else
{
uint8_t v___x_635_; 
v___x_635_ = 1;
return v___x_635_;
}
}
default: 
{
uint8_t v___x_636_; 
v___x_636_ = 1;
return v___x_636_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Gate___boxed(lean_object* v_x_637_, lean_object* v_x_638_){
_start:
{
uint8_t v_x_117__boxed_639_; uint8_t v_x_118__boxed_640_; uint8_t v_res_641_; lean_object* v_r_642_; 
v_x_117__boxed_639_ = lean_unbox(v_x_637_);
v_x_118__boxed_640_ = lean_unbox(v_x_638_);
v_res_641_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Gate(v_x_117__boxed_639_, v_x_118__boxed_640_);
v_r_642_ = lean_box(v_res_641_);
return v_r_642_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3CodeOf(lean_object* v_gate_643_){
_start:
{
uint8_t v___x_644_; lean_object* v___x_645_; lean_object* v___x_646_; uint8_t v___x_647_; 
v___x_644_ = 0;
v___x_645_ = lean_box(v___x_644_);
lean_inc_ref(v_gate_643_);
v___x_646_ = lean_apply_1(v_gate_643_, v___x_645_);
v___x_647_ = lean_unbox(v___x_646_);
if (v___x_647_ == 0)
{
uint8_t v___x_648_; lean_object* v___x_649_; lean_object* v___x_650_; uint8_t v___x_651_; 
v___x_648_ = 1;
v___x_649_ = lean_box(v___x_648_);
lean_inc_ref(v_gate_643_);
v___x_650_ = lean_apply_1(v_gate_643_, v___x_649_);
v___x_651_ = lean_unbox(v___x_650_);
if (v___x_651_ == 0)
{
uint8_t v___x_652_; lean_object* v___x_653_; lean_object* v___x_654_; uint8_t v___x_655_; 
v___x_652_ = 2;
v___x_653_ = lean_box(v___x_652_);
v___x_654_ = lean_apply_1(v_gate_643_, v___x_653_);
v___x_655_ = lean_unbox(v___x_654_);
if (v___x_655_ == 0)
{
uint8_t v___x_656_; 
v___x_656_ = 0;
return v___x_656_;
}
else
{
uint8_t v___x_657_; 
v___x_657_ = 1;
return v___x_657_;
}
}
else
{
uint8_t v___x_658_; lean_object* v___x_659_; lean_object* v___x_660_; uint8_t v___x_661_; 
v___x_658_ = 2;
v___x_659_ = lean_box(v___x_658_);
v___x_660_ = lean_apply_1(v_gate_643_, v___x_659_);
v___x_661_ = lean_unbox(v___x_660_);
if (v___x_661_ == 0)
{
uint8_t v___x_662_; 
v___x_662_ = 2;
return v___x_662_;
}
else
{
uint8_t v___x_663_; 
v___x_663_ = 3;
return v___x_663_;
}
}
}
else
{
uint8_t v___x_664_; lean_object* v___x_665_; lean_object* v___x_666_; uint8_t v___x_667_; 
v___x_664_ = 1;
v___x_665_ = lean_box(v___x_664_);
lean_inc_ref(v_gate_643_);
v___x_666_ = lean_apply_1(v_gate_643_, v___x_665_);
v___x_667_ = lean_unbox(v___x_666_);
if (v___x_667_ == 0)
{
uint8_t v___x_668_; lean_object* v___x_669_; lean_object* v___x_670_; uint8_t v___x_671_; 
v___x_668_ = 2;
v___x_669_ = lean_box(v___x_668_);
v___x_670_ = lean_apply_1(v_gate_643_, v___x_669_);
v___x_671_ = lean_unbox(v___x_670_);
if (v___x_671_ == 0)
{
uint8_t v___x_672_; 
v___x_672_ = 4;
return v___x_672_;
}
else
{
uint8_t v___x_673_; 
v___x_673_ = 5;
return v___x_673_;
}
}
else
{
uint8_t v___x_674_; lean_object* v___x_675_; lean_object* v___x_676_; uint8_t v___x_677_; 
v___x_674_ = 2;
v___x_675_ = lean_box(v___x_674_);
v___x_676_ = lean_apply_1(v_gate_643_, v___x_675_);
v___x_677_ = lean_unbox(v___x_676_);
if (v___x_677_ == 0)
{
uint8_t v___x_678_; 
v___x_678_ = 6;
return v___x_678_;
}
else
{
uint8_t v___x_679_; 
v___x_679_ = 7;
return v___x_679_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3CodeOf___boxed(lean_object* v_gate_680_){
_start:
{
uint8_t v_res_681_; lean_object* v_r_682_; 
v_res_681_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3CodeOf(v_gate_680_);
v_r_682_ = lean_box(v_res_681_);
return v_r_682_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___redArg(uint8_t v_x_683_, uint8_t v_x_684_, lean_object* v_h__1_685_, lean_object* v_h__2_686_, lean_object* v_h__3_687_, lean_object* v_h__4_688_, lean_object* v_h__5_689_, lean_object* v_h__6_690_, lean_object* v_h__7_691_, lean_object* v_h__8_692_, lean_object* v_h__9_693_, lean_object* v_h__10_694_, lean_object* v_h__11_695_, lean_object* v_h__12_696_, lean_object* v_h__13_697_, lean_object* v_h__14_698_, lean_object* v_h__15_699_, lean_object* v_h__16_700_, lean_object* v_h__17_701_, lean_object* v_h__18_702_, lean_object* v_h__19_703_, lean_object* v_h__20_704_){
_start:
{
switch(v_x_683_)
{
case 0:
{
lean_object* v___x_705_; lean_object* v___x_706_; 
lean_dec(v_h__20_704_);
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
v___x_705_ = lean_box(v_x_684_);
v___x_706_ = lean_apply_1(v_h__1_685_, v___x_705_);
return v___x_706_;
}
case 1:
{
lean_dec(v_h__20_704_);
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__1_685_);
switch(v_x_684_)
{
case 0:
{
lean_object* v___x_707_; lean_object* v___x_708_; 
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
v___x_707_ = lean_box(0);
v___x_708_ = lean_apply_1(v_h__2_686_, v___x_707_);
return v___x_708_;
}
case 1:
{
lean_object* v___x_709_; lean_object* v___x_710_; 
lean_dec(v_h__4_688_);
lean_dec(v_h__2_686_);
v___x_709_ = lean_box(0);
v___x_710_ = lean_apply_1(v_h__3_687_, v___x_709_);
return v___x_710_;
}
default: 
{
lean_object* v___x_711_; lean_object* v___x_712_; 
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
v___x_711_ = lean_box(0);
v___x_712_ = lean_apply_1(v_h__4_688_, v___x_711_);
return v___x_712_;
}
}
}
case 2:
{
lean_dec(v_h__20_704_);
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
lean_dec(v_h__1_685_);
switch(v_x_684_)
{
case 0:
{
lean_object* v___x_713_; lean_object* v___x_714_; 
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
v___x_713_ = lean_box(0);
v___x_714_ = lean_apply_1(v_h__5_689_, v___x_713_);
return v___x_714_;
}
case 1:
{
lean_object* v___x_715_; lean_object* v___x_716_; 
lean_dec(v_h__7_691_);
lean_dec(v_h__5_689_);
v___x_715_ = lean_box(0);
v___x_716_ = lean_apply_1(v_h__6_690_, v___x_715_);
return v___x_716_;
}
default: 
{
lean_object* v___x_717_; lean_object* v___x_718_; 
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
v___x_717_ = lean_box(0);
v___x_718_ = lean_apply_1(v_h__7_691_, v___x_717_);
return v___x_718_;
}
}
}
case 3:
{
lean_dec(v_h__20_704_);
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
lean_dec(v_h__1_685_);
switch(v_x_684_)
{
case 0:
{
lean_object* v___x_719_; lean_object* v___x_720_; 
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
v___x_719_ = lean_box(0);
v___x_720_ = lean_apply_1(v_h__8_692_, v___x_719_);
return v___x_720_;
}
case 1:
{
lean_object* v___x_721_; lean_object* v___x_722_; 
lean_dec(v_h__10_694_);
lean_dec(v_h__8_692_);
v___x_721_ = lean_box(0);
v___x_722_ = lean_apply_1(v_h__9_693_, v___x_721_);
return v___x_722_;
}
default: 
{
lean_object* v___x_723_; lean_object* v___x_724_; 
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
v___x_723_ = lean_box(0);
v___x_724_ = lean_apply_1(v_h__10_694_, v___x_723_);
return v___x_724_;
}
}
}
case 4:
{
lean_dec(v_h__20_704_);
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
lean_dec(v_h__1_685_);
switch(v_x_684_)
{
case 0:
{
lean_object* v___x_725_; lean_object* v___x_726_; 
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
v___x_725_ = lean_box(0);
v___x_726_ = lean_apply_1(v_h__11_695_, v___x_725_);
return v___x_726_;
}
case 1:
{
lean_object* v___x_727_; lean_object* v___x_728_; 
lean_dec(v_h__13_697_);
lean_dec(v_h__11_695_);
v___x_727_ = lean_box(0);
v___x_728_ = lean_apply_1(v_h__12_696_, v___x_727_);
return v___x_728_;
}
default: 
{
lean_object* v___x_729_; lean_object* v___x_730_; 
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
v___x_729_ = lean_box(0);
v___x_730_ = lean_apply_1(v_h__13_697_, v___x_729_);
return v___x_730_;
}
}
}
case 5:
{
lean_dec(v_h__20_704_);
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
lean_dec(v_h__1_685_);
switch(v_x_684_)
{
case 0:
{
lean_object* v___x_731_; lean_object* v___x_732_; 
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
v___x_731_ = lean_box(0);
v___x_732_ = lean_apply_1(v_h__14_698_, v___x_731_);
return v___x_732_;
}
case 1:
{
lean_object* v___x_733_; lean_object* v___x_734_; 
lean_dec(v_h__16_700_);
lean_dec(v_h__14_698_);
v___x_733_ = lean_box(0);
v___x_734_ = lean_apply_1(v_h__15_699_, v___x_733_);
return v___x_734_;
}
default: 
{
lean_object* v___x_735_; lean_object* v___x_736_; 
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
v___x_735_ = lean_box(0);
v___x_736_ = lean_apply_1(v_h__16_700_, v___x_735_);
return v___x_736_;
}
}
}
case 6:
{
lean_dec(v_h__20_704_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
lean_dec(v_h__1_685_);
switch(v_x_684_)
{
case 0:
{
lean_object* v___x_737_; lean_object* v___x_738_; 
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
v___x_737_ = lean_box(0);
v___x_738_ = lean_apply_1(v_h__17_701_, v___x_737_);
return v___x_738_;
}
case 1:
{
lean_object* v___x_739_; lean_object* v___x_740_; 
lean_dec(v_h__19_703_);
lean_dec(v_h__17_701_);
v___x_739_ = lean_box(0);
v___x_740_ = lean_apply_1(v_h__18_702_, v___x_739_);
return v___x_740_;
}
default: 
{
lean_object* v___x_741_; lean_object* v___x_742_; 
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
v___x_741_ = lean_box(0);
v___x_742_ = lean_apply_1(v_h__19_703_, v___x_741_);
return v___x_742_;
}
}
}
default: 
{
lean_object* v___x_743_; lean_object* v___x_744_; 
lean_dec(v_h__19_703_);
lean_dec(v_h__18_702_);
lean_dec(v_h__17_701_);
lean_dec(v_h__16_700_);
lean_dec(v_h__15_699_);
lean_dec(v_h__14_698_);
lean_dec(v_h__13_697_);
lean_dec(v_h__12_696_);
lean_dec(v_h__11_695_);
lean_dec(v_h__10_694_);
lean_dec(v_h__9_693_);
lean_dec(v_h__8_692_);
lean_dec(v_h__7_691_);
lean_dec(v_h__6_690_);
lean_dec(v_h__5_689_);
lean_dec(v_h__4_688_);
lean_dec(v_h__3_687_);
lean_dec(v_h__2_686_);
lean_dec(v_h__1_685_);
v___x_743_ = lean_box(v_x_684_);
v___x_744_ = lean_apply_1(v_h__20_704_, v___x_743_);
return v___x_744_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___redArg___boxed(lean_object** _args){
lean_object* v_x_745_ = _args[0];
lean_object* v_x_746_ = _args[1];
lean_object* v_h__1_747_ = _args[2];
lean_object* v_h__2_748_ = _args[3];
lean_object* v_h__3_749_ = _args[4];
lean_object* v_h__4_750_ = _args[5];
lean_object* v_h__5_751_ = _args[6];
lean_object* v_h__6_752_ = _args[7];
lean_object* v_h__7_753_ = _args[8];
lean_object* v_h__8_754_ = _args[9];
lean_object* v_h__9_755_ = _args[10];
lean_object* v_h__10_756_ = _args[11];
lean_object* v_h__11_757_ = _args[12];
lean_object* v_h__12_758_ = _args[13];
lean_object* v_h__13_759_ = _args[14];
lean_object* v_h__14_760_ = _args[15];
lean_object* v_h__15_761_ = _args[16];
lean_object* v_h__16_762_ = _args[17];
lean_object* v_h__17_763_ = _args[18];
lean_object* v_h__18_764_ = _args[19];
lean_object* v_h__19_765_ = _args[20];
lean_object* v_h__20_766_ = _args[21];
_start:
{
uint8_t v_x_190__boxed_767_; uint8_t v_x_191__boxed_768_; lean_object* v_res_769_; 
v_x_190__boxed_767_ = lean_unbox(v_x_745_);
v_x_191__boxed_768_ = lean_unbox(v_x_746_);
v_res_769_ = lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___redArg(v_x_190__boxed_767_, v_x_191__boxed_768_, v_h__1_747_, v_h__2_748_, v_h__3_749_, v_h__4_750_, v_h__5_751_, v_h__6_752_, v_h__7_753_, v_h__8_754_, v_h__9_755_, v_h__10_756_, v_h__11_757_, v_h__12_758_, v_h__13_759_, v_h__14_760_, v_h__15_761_, v_h__16_762_, v_h__17_763_, v_h__18_764_, v_h__19_765_, v_h__20_766_);
return v_res_769_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter(lean_object* v_motive_770_, uint8_t v_x_771_, uint8_t v_x_772_, lean_object* v_h__1_773_, lean_object* v_h__2_774_, lean_object* v_h__3_775_, lean_object* v_h__4_776_, lean_object* v_h__5_777_, lean_object* v_h__6_778_, lean_object* v_h__7_779_, lean_object* v_h__8_780_, lean_object* v_h__9_781_, lean_object* v_h__10_782_, lean_object* v_h__11_783_, lean_object* v_h__12_784_, lean_object* v_h__13_785_, lean_object* v_h__14_786_, lean_object* v_h__15_787_, lean_object* v_h__16_788_, lean_object* v_h__17_789_, lean_object* v_h__18_790_, lean_object* v_h__19_791_, lean_object* v_h__20_792_){
_start:
{
switch(v_x_771_)
{
case 0:
{
lean_object* v___x_793_; lean_object* v___x_794_; 
lean_dec(v_h__20_792_);
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
v___x_793_ = lean_box(v_x_772_);
v___x_794_ = lean_apply_1(v_h__1_773_, v___x_793_);
return v___x_794_;
}
case 1:
{
lean_dec(v_h__20_792_);
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__1_773_);
switch(v_x_772_)
{
case 0:
{
lean_object* v___x_795_; lean_object* v___x_796_; 
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
v___x_795_ = lean_box(0);
v___x_796_ = lean_apply_1(v_h__2_774_, v___x_795_);
return v___x_796_;
}
case 1:
{
lean_object* v___x_797_; lean_object* v___x_798_; 
lean_dec(v_h__4_776_);
lean_dec(v_h__2_774_);
v___x_797_ = lean_box(0);
v___x_798_ = lean_apply_1(v_h__3_775_, v___x_797_);
return v___x_798_;
}
default: 
{
lean_object* v___x_799_; lean_object* v___x_800_; 
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
v___x_799_ = lean_box(0);
v___x_800_ = lean_apply_1(v_h__4_776_, v___x_799_);
return v___x_800_;
}
}
}
case 2:
{
lean_dec(v_h__20_792_);
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
lean_dec(v_h__1_773_);
switch(v_x_772_)
{
case 0:
{
lean_object* v___x_801_; lean_object* v___x_802_; 
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
v___x_801_ = lean_box(0);
v___x_802_ = lean_apply_1(v_h__5_777_, v___x_801_);
return v___x_802_;
}
case 1:
{
lean_object* v___x_803_; lean_object* v___x_804_; 
lean_dec(v_h__7_779_);
lean_dec(v_h__5_777_);
v___x_803_ = lean_box(0);
v___x_804_ = lean_apply_1(v_h__6_778_, v___x_803_);
return v___x_804_;
}
default: 
{
lean_object* v___x_805_; lean_object* v___x_806_; 
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
v___x_805_ = lean_box(0);
v___x_806_ = lean_apply_1(v_h__7_779_, v___x_805_);
return v___x_806_;
}
}
}
case 3:
{
lean_dec(v_h__20_792_);
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
lean_dec(v_h__1_773_);
switch(v_x_772_)
{
case 0:
{
lean_object* v___x_807_; lean_object* v___x_808_; 
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
v___x_807_ = lean_box(0);
v___x_808_ = lean_apply_1(v_h__8_780_, v___x_807_);
return v___x_808_;
}
case 1:
{
lean_object* v___x_809_; lean_object* v___x_810_; 
lean_dec(v_h__10_782_);
lean_dec(v_h__8_780_);
v___x_809_ = lean_box(0);
v___x_810_ = lean_apply_1(v_h__9_781_, v___x_809_);
return v___x_810_;
}
default: 
{
lean_object* v___x_811_; lean_object* v___x_812_; 
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
v___x_811_ = lean_box(0);
v___x_812_ = lean_apply_1(v_h__10_782_, v___x_811_);
return v___x_812_;
}
}
}
case 4:
{
lean_dec(v_h__20_792_);
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
lean_dec(v_h__1_773_);
switch(v_x_772_)
{
case 0:
{
lean_object* v___x_813_; lean_object* v___x_814_; 
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
v___x_813_ = lean_box(0);
v___x_814_ = lean_apply_1(v_h__11_783_, v___x_813_);
return v___x_814_;
}
case 1:
{
lean_object* v___x_815_; lean_object* v___x_816_; 
lean_dec(v_h__13_785_);
lean_dec(v_h__11_783_);
v___x_815_ = lean_box(0);
v___x_816_ = lean_apply_1(v_h__12_784_, v___x_815_);
return v___x_816_;
}
default: 
{
lean_object* v___x_817_; lean_object* v___x_818_; 
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
v___x_817_ = lean_box(0);
v___x_818_ = lean_apply_1(v_h__13_785_, v___x_817_);
return v___x_818_;
}
}
}
case 5:
{
lean_dec(v_h__20_792_);
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
lean_dec(v_h__1_773_);
switch(v_x_772_)
{
case 0:
{
lean_object* v___x_819_; lean_object* v___x_820_; 
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
v___x_819_ = lean_box(0);
v___x_820_ = lean_apply_1(v_h__14_786_, v___x_819_);
return v___x_820_;
}
case 1:
{
lean_object* v___x_821_; lean_object* v___x_822_; 
lean_dec(v_h__16_788_);
lean_dec(v_h__14_786_);
v___x_821_ = lean_box(0);
v___x_822_ = lean_apply_1(v_h__15_787_, v___x_821_);
return v___x_822_;
}
default: 
{
lean_object* v___x_823_; lean_object* v___x_824_; 
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
v___x_823_ = lean_box(0);
v___x_824_ = lean_apply_1(v_h__16_788_, v___x_823_);
return v___x_824_;
}
}
}
case 6:
{
lean_dec(v_h__20_792_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
lean_dec(v_h__1_773_);
switch(v_x_772_)
{
case 0:
{
lean_object* v___x_825_; lean_object* v___x_826_; 
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
v___x_825_ = lean_box(0);
v___x_826_ = lean_apply_1(v_h__17_789_, v___x_825_);
return v___x_826_;
}
case 1:
{
lean_object* v___x_827_; lean_object* v___x_828_; 
lean_dec(v_h__19_791_);
lean_dec(v_h__17_789_);
v___x_827_ = lean_box(0);
v___x_828_ = lean_apply_1(v_h__18_790_, v___x_827_);
return v___x_828_;
}
default: 
{
lean_object* v___x_829_; lean_object* v___x_830_; 
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
v___x_829_ = lean_box(0);
v___x_830_ = lean_apply_1(v_h__19_791_, v___x_829_);
return v___x_830_;
}
}
}
default: 
{
lean_object* v___x_831_; lean_object* v___x_832_; 
lean_dec(v_h__19_791_);
lean_dec(v_h__18_790_);
lean_dec(v_h__17_789_);
lean_dec(v_h__16_788_);
lean_dec(v_h__15_787_);
lean_dec(v_h__14_786_);
lean_dec(v_h__13_785_);
lean_dec(v_h__12_784_);
lean_dec(v_h__11_783_);
lean_dec(v_h__10_782_);
lean_dec(v_h__9_781_);
lean_dec(v_h__8_780_);
lean_dec(v_h__7_779_);
lean_dec(v_h__6_778_);
lean_dec(v_h__5_777_);
lean_dec(v_h__4_776_);
lean_dec(v_h__3_775_);
lean_dec(v_h__2_774_);
lean_dec(v_h__1_773_);
v___x_831_ = lean_box(v_x_772_);
v___x_832_ = lean_apply_1(v_h__20_792_, v___x_831_);
return v___x_832_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter___boxed(lean_object** _args){
lean_object* v_motive_833_ = _args[0];
lean_object* v_x_834_ = _args[1];
lean_object* v_x_835_ = _args[2];
lean_object* v_h__1_836_ = _args[3];
lean_object* v_h__2_837_ = _args[4];
lean_object* v_h__3_838_ = _args[5];
lean_object* v_h__4_839_ = _args[6];
lean_object* v_h__5_840_ = _args[7];
lean_object* v_h__6_841_ = _args[8];
lean_object* v_h__7_842_ = _args[9];
lean_object* v_h__8_843_ = _args[10];
lean_object* v_h__9_844_ = _args[11];
lean_object* v_h__10_845_ = _args[12];
lean_object* v_h__11_846_ = _args[13];
lean_object* v_h__12_847_ = _args[14];
lean_object* v_h__13_848_ = _args[15];
lean_object* v_h__14_849_ = _args[16];
lean_object* v_h__15_850_ = _args[17];
lean_object* v_h__16_851_ = _args[18];
lean_object* v_h__17_852_ = _args[19];
lean_object* v_h__18_853_ = _args[20];
lean_object* v_h__19_854_ = _args[21];
lean_object* v_h__20_855_ = _args[22];
_start:
{
uint8_t v_x_276__boxed_856_; uint8_t v_x_277__boxed_857_; lean_object* v_res_858_; 
v_x_276__boxed_856_ = lean_unbox(v_x_834_);
v_x_277__boxed_857_ = lean_unbox(v_x_835_);
v_res_858_ = lp_FiniteQuantum___private_WorldGateVacuity_0__OmegaWorld_GateVacuityW810_fin3Gate_match__1_splitter(v_motive_833_, v_x_276__boxed_856_, v_x_277__boxed_857_, v_h__1_836_, v_h__2_837_, v_h__3_838_, v_h__4_839_, v_h__5_840_, v_h__6_841_, v_h__7_842_, v_h__8_843_, v_h__9_844_, v_h__10_845_, v_h__11_846_, v_h__12_847_, v_h__13_848_, v_h__14_849_, v_h__15_850_, v_h__16_851_, v_h__17_852_, v_h__18_853_, v_h__19_854_, v_h__20_855_);
return v_res_858_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family(uint8_t v_code_871_){
_start:
{
lean_object* v___x_872_; lean_object* v___x_873_; lean_object* v___x_874_; lean_object* v___x_875_; 
v___x_872_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___closed__2));
v___x_873_ = lean_box(v_code_871_);
v___x_874_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Gate___boxed), 2, 1);
lean_closure_set(v___x_874_, 0, v___x_873_);
v___x_875_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_875_, 0, v___x_872_);
lean_ctor_set(v___x_875_, 1, v___x_874_);
return v___x_875_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family___boxed(lean_object* v_code_876_){
_start:
{
uint8_t v_code_boxed_877_; lean_object* v_res_878_; 
v_code_boxed_877_ = lean_unbox(v_code_876_);
v_res_878_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family(v_code_boxed_877_);
return v_res_878_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(uint8_t v_code_879_){
_start:
{
lean_object* v___x_880_; uint8_t v___x_881_; 
v___x_880_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Family(v_code_879_);
v___x_881_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_scanGate___redArg(v___x_880_);
return v___x_881_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class___boxed(lean_object* v_code_882_){
_start:
{
uint8_t v_code_boxed_883_; uint8_t v_res_884_; lean_object* v_r_885_; 
v_code_boxed_883_ = lean_unbox(v_code_882_);
v_res_884_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v_code_boxed_883_);
v_r_885_ = lean_box(v_res_884_);
return v_r_885_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(uint8_t v_target_886_, uint8_t v_observed_887_){
_start:
{
uint8_t v___x_888_; 
v___x_888_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqGateClass(v_target_886_, v_observed_887_);
if (v___x_888_ == 0)
{
lean_object* v___x_889_; 
v___x_889_ = lean_unsigned_to_nat(0u);
return v___x_889_;
}
else
{
lean_object* v___x_890_; 
v___x_890_ = lean_unsigned_to_nat(1u);
return v___x_890_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator___boxed(lean_object* v_target_891_, lean_object* v_observed_892_){
_start:
{
uint8_t v_target_boxed_893_; uint8_t v_observed_boxed_894_; lean_object* v_res_895_; 
v_target_boxed_893_ = lean_unbox(v_target_891_);
v_observed_boxed_894_ = lean_unbox(v_observed_892_);
v_res_895_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_boxed_893_, v_observed_boxed_894_);
return v_res_895_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__0(void){
_start:
{
uint8_t v___x_896_; uint8_t v___x_897_; 
v___x_896_ = 0;
v___x_897_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_896_);
return v___x_897_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__1(void){
_start:
{
uint8_t v___x_898_; uint8_t v___x_899_; 
v___x_898_ = 1;
v___x_899_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_898_);
return v___x_899_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__2(void){
_start:
{
uint8_t v___x_900_; uint8_t v___x_901_; 
v___x_900_ = 2;
v___x_901_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_900_);
return v___x_901_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__3(void){
_start:
{
uint8_t v___x_902_; uint8_t v___x_903_; 
v___x_902_ = 3;
v___x_903_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_902_);
return v___x_903_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__4(void){
_start:
{
uint8_t v___x_904_; uint8_t v___x_905_; 
v___x_904_ = 4;
v___x_905_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_904_);
return v___x_905_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__5(void){
_start:
{
uint8_t v___x_906_; uint8_t v___x_907_; 
v___x_906_ = 5;
v___x_907_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_906_);
return v___x_907_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__6(void){
_start:
{
uint8_t v___x_908_; uint8_t v___x_909_; 
v___x_908_ = 6;
v___x_909_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_908_);
return v___x_909_;
}
}
static uint8_t _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__7(void){
_start:
{
uint8_t v___x_910_; uint8_t v___x_911_; 
v___x_910_ = 7;
v___x_911_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3Class(v___x_910_);
return v___x_911_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount(uint8_t v_target_912_){
_start:
{
uint8_t v___x_913_; lean_object* v___x_914_; uint8_t v___x_915_; lean_object* v___x_916_; lean_object* v___x_917_; uint8_t v___x_918_; lean_object* v___x_919_; lean_object* v___x_920_; uint8_t v___x_921_; lean_object* v___x_922_; lean_object* v___x_923_; uint8_t v___x_924_; lean_object* v___x_925_; lean_object* v___x_926_; uint8_t v___x_927_; lean_object* v___x_928_; lean_object* v___x_929_; uint8_t v___x_930_; lean_object* v___x_931_; lean_object* v___x_932_; uint8_t v___x_933_; lean_object* v___x_934_; lean_object* v___x_935_; 
v___x_913_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__0, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__0);
v___x_914_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_913_);
v___x_915_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__1, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__1);
v___x_916_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_915_);
v___x_917_ = lean_nat_add(v___x_914_, v___x_916_);
lean_dec(v___x_916_);
lean_dec(v___x_914_);
v___x_918_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__2, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__2_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__2);
v___x_919_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_918_);
v___x_920_ = lean_nat_add(v___x_917_, v___x_919_);
lean_dec(v___x_919_);
lean_dec(v___x_917_);
v___x_921_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__3, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__3_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__3);
v___x_922_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_921_);
v___x_923_ = lean_nat_add(v___x_920_, v___x_922_);
lean_dec(v___x_922_);
lean_dec(v___x_920_);
v___x_924_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__4, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__4_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__4);
v___x_925_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_924_);
v___x_926_ = lean_nat_add(v___x_923_, v___x_925_);
lean_dec(v___x_925_);
lean_dec(v___x_923_);
v___x_927_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__5, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__5_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__5);
v___x_928_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_927_);
v___x_929_ = lean_nat_add(v___x_926_, v___x_928_);
lean_dec(v___x_928_);
lean_dec(v___x_926_);
v___x_930_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__6, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__6_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__6);
v___x_931_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_930_);
v___x_932_ = lean_nat_add(v___x_929_, v___x_931_);
lean_dec(v___x_931_);
lean_dec(v___x_929_);
v___x_933_ = lean_uint8_once(&lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__7, &lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__7_once, _init_lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___closed__7);
v___x_934_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_classIndicator(v_target_912_, v___x_933_);
v___x_935_ = lean_nat_add(v___x_932_, v___x_934_);
lean_dec(v___x_934_);
lean_dec(v___x_932_);
return v___x_935_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount___boxed(lean_object* v_target_936_){
_start:
{
uint8_t v_target_boxed_937_; lean_object* v_res_938_; 
v_target_boxed_937_ = lean_unbox(v_target_936_);
v_res_938_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_fin3ClassCount(v_target_boxed_937_);
return v_res_938_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_toCtorIdx(lean_object* v_x_939_){
_start:
{
lean_object* v___x_940_; 
v___x_940_ = lean_unsigned_to_nat(0u);
return v___x_940_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_ofNat(lean_object* v_n_941_){
_start:
{
lean_object* v___x_942_; 
v___x_942_ = lean_box(0);
return v___x_942_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_ofNat___boxed(lean_object* v_n_943_){
_start:
{
lean_object* v_res_944_; 
v_res_944_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_W810AuthorityEffect_ofNat(v_n_943_);
lean_dec(v_n_943_);
return v_res_944_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqW810AuthorityEffect(lean_object* v_x_945_, lean_object* v_y_946_){
_start:
{
uint8_t v___x_947_; 
v___x_947_ = 1;
return v___x_947_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqW810AuthorityEffect___boxed(lean_object* v_x_948_, lean_object* v_y_949_){
_start:
{
uint8_t v_res_950_; lean_object* v_r_951_; 
v_res_950_ = lp_FiniteQuantum_OmegaWorld_GateVacuityW810_instDecidableEqW810AuthorityEffect(v_x_948_, v_y_949_);
v_r_951_ = lean_box(v_res_950_);
return v_r_951_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveDifference(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldGateVacuity(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveDifference(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
