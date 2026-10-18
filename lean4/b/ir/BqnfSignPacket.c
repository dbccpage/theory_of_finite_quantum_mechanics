// Lean compiler output
// Module: BqnfSignPacket
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
lean_object* l_Bool_repr___redArg(uint8_t);
lean_object* l_Nat_reprFast(lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_instDecidableEqTerminalRoute(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instDecidableEqTerminalRoute___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 41, .m_capacity = 41, .m_length = 40, .m_data = "BqnfSignPacket.TerminalRoute.ExactRepair"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 44, .m_capacity = 44, .m_length = 43, .m_data = "BqnfSignPacket.TerminalRoute.ClosedResidual"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "BqnfSignPacket.TerminalRoute.OpenSignObstruction"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__5_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 47, .m_capacity = 47, .m_length = 46, .m_data = "BqnfSignPacket.TerminalRoute.SplitBrainRefusal"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__6 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__6_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__6_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__7 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__7_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 44, .m_capacity = 44, .m_length = 43, .m_data = "BqnfSignPacket.TerminalRoute.ClosureFailure"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__8 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__9 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__9_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute___closed__0 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "isValidComplex"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__9_value;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "disjointSupports"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__11_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__12;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "closureDefect"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "residualMass"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__17_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__18_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__18;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "hasInvolutionWitness"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__19 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__19_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__19_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__20 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__20_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__21_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__21;
static const lean_string_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__22 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__22_value;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__23_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__23;
static lean_once_cell_t lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__24_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__24;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__25 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__25_value;
static const lean_ctor_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__22_value)}};
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__26 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__26_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics___closed__0 = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics = (const lean_object*)&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_routePacket(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_routePacket___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx(uint8_t v_x_1_){
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
case 3:
{
lean_object* v___x_5_; 
v___x_5_ = lean_unsigned_to_nat(3u);
return v___x_5_;
}
default: 
{
lean_object* v___x_6_; 
v___x_6_ = lean_unsigned_to_nat(4u);
return v___x_6_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx___boxed(lean_object* v_x_7_){
_start:
{
uint8_t v_x_boxed_8_; lean_object* v_res_9_; 
v_x_boxed_8_ = lean_unbox(v_x_7_);
v_res_9_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx(v_x_boxed_8_);
return v_res_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_toCtorIdx(uint8_t v_x_10_){
_start:
{
lean_object* v___x_11_; 
v___x_11_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx(v_x_10_);
return v___x_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_toCtorIdx___boxed(lean_object* v_x_12_){
_start:
{
uint8_t v_x_4__boxed_13_; lean_object* v_res_14_; 
v_x_4__boxed_13_ = lean_unbox(v_x_12_);
v_res_14_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_toCtorIdx(v_x_4__boxed_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___redArg(lean_object* v_k_15_){
_start:
{
lean_inc(v_k_15_);
return v_k_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___redArg___boxed(lean_object* v_k_16_){
_start:
{
lean_object* v_res_17_; 
v_res_17_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___redArg(v_k_16_);
lean_dec(v_k_16_);
return v_res_17_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim(lean_object* v_motive_18_, lean_object* v_ctorIdx_19_, uint8_t v_t_20_, lean_object* v_h_21_, lean_object* v_k_22_){
_start:
{
lean_inc(v_k_22_);
return v_k_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim___boxed(lean_object* v_motive_23_, lean_object* v_ctorIdx_24_, lean_object* v_t_25_, lean_object* v_h_26_, lean_object* v_k_27_){
_start:
{
uint8_t v_t_boxed_28_; lean_object* v_res_29_; 
v_t_boxed_28_ = lean_unbox(v_t_25_);
v_res_29_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorElim(v_motive_23_, v_ctorIdx_24_, v_t_boxed_28_, v_h_26_, v_k_27_);
lean_dec(v_k_27_);
lean_dec(v_ctorIdx_24_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___redArg(lean_object* v_ExactRepair_30_){
_start:
{
lean_inc(v_ExactRepair_30_);
return v_ExactRepair_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___redArg___boxed(lean_object* v_ExactRepair_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___redArg(v_ExactRepair_31_);
lean_dec(v_ExactRepair_31_);
return v_res_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim(lean_object* v_motive_33_, uint8_t v_t_34_, lean_object* v_h_35_, lean_object* v_ExactRepair_36_){
_start:
{
lean_inc(v_ExactRepair_36_);
return v_ExactRepair_36_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim___boxed(lean_object* v_motive_37_, lean_object* v_t_38_, lean_object* v_h_39_, lean_object* v_ExactRepair_40_){
_start:
{
uint8_t v_t_boxed_41_; lean_object* v_res_42_; 
v_t_boxed_41_ = lean_unbox(v_t_38_);
v_res_42_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ExactRepair_elim(v_motive_37_, v_t_boxed_41_, v_h_39_, v_ExactRepair_40_);
lean_dec(v_ExactRepair_40_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___redArg(lean_object* v_ClosedResidual_43_){
_start:
{
lean_inc(v_ClosedResidual_43_);
return v_ClosedResidual_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___redArg___boxed(lean_object* v_ClosedResidual_44_){
_start:
{
lean_object* v_res_45_; 
v_res_45_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___redArg(v_ClosedResidual_44_);
lean_dec(v_ClosedResidual_44_);
return v_res_45_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim(lean_object* v_motive_46_, uint8_t v_t_47_, lean_object* v_h_48_, lean_object* v_ClosedResidual_49_){
_start:
{
lean_inc(v_ClosedResidual_49_);
return v_ClosedResidual_49_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim___boxed(lean_object* v_motive_50_, lean_object* v_t_51_, lean_object* v_h_52_, lean_object* v_ClosedResidual_53_){
_start:
{
uint8_t v_t_boxed_54_; lean_object* v_res_55_; 
v_t_boxed_54_ = lean_unbox(v_t_51_);
v_res_55_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosedResidual_elim(v_motive_50_, v_t_boxed_54_, v_h_52_, v_ClosedResidual_53_);
lean_dec(v_ClosedResidual_53_);
return v_res_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___redArg(lean_object* v_OpenSignObstruction_56_){
_start:
{
lean_inc(v_OpenSignObstruction_56_);
return v_OpenSignObstruction_56_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___redArg___boxed(lean_object* v_OpenSignObstruction_57_){
_start:
{
lean_object* v_res_58_; 
v_res_58_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___redArg(v_OpenSignObstruction_57_);
lean_dec(v_OpenSignObstruction_57_);
return v_res_58_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim(lean_object* v_motive_59_, uint8_t v_t_60_, lean_object* v_h_61_, lean_object* v_OpenSignObstruction_62_){
_start:
{
lean_inc(v_OpenSignObstruction_62_);
return v_OpenSignObstruction_62_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim___boxed(lean_object* v_motive_63_, lean_object* v_t_64_, lean_object* v_h_65_, lean_object* v_OpenSignObstruction_66_){
_start:
{
uint8_t v_t_boxed_67_; lean_object* v_res_68_; 
v_t_boxed_67_ = lean_unbox(v_t_64_);
v_res_68_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_OpenSignObstruction_elim(v_motive_63_, v_t_boxed_67_, v_h_65_, v_OpenSignObstruction_66_);
lean_dec(v_OpenSignObstruction_66_);
return v_res_68_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object* v_SplitBrainRefusal_69_){
_start:
{
lean_inc(v_SplitBrainRefusal_69_);
return v_SplitBrainRefusal_69_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object* v_SplitBrainRefusal_70_){
_start:
{
lean_object* v_res_71_; 
v_res_71_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___redArg(v_SplitBrainRefusal_70_);
lean_dec(v_SplitBrainRefusal_70_);
return v_res_71_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim(lean_object* v_motive_72_, uint8_t v_t_73_, lean_object* v_h_74_, lean_object* v_SplitBrainRefusal_75_){
_start:
{
lean_inc(v_SplitBrainRefusal_75_);
return v_SplitBrainRefusal_75_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object* v_motive_76_, lean_object* v_t_77_, lean_object* v_h_78_, lean_object* v_SplitBrainRefusal_79_){
_start:
{
uint8_t v_t_boxed_80_; lean_object* v_res_81_; 
v_t_boxed_80_ = lean_unbox(v_t_77_);
v_res_81_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_SplitBrainRefusal_elim(v_motive_76_, v_t_boxed_80_, v_h_78_, v_SplitBrainRefusal_79_);
lean_dec(v_SplitBrainRefusal_79_);
return v_res_81_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___redArg(lean_object* v_ClosureFailure_82_){
_start:
{
lean_inc(v_ClosureFailure_82_);
return v_ClosureFailure_82_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object* v_ClosureFailure_83_){
_start:
{
lean_object* v_res_84_; 
v_res_84_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___redArg(v_ClosureFailure_83_);
lean_dec(v_ClosureFailure_83_);
return v_res_84_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim(lean_object* v_motive_85_, uint8_t v_t_86_, lean_object* v_h_87_, lean_object* v_ClosureFailure_88_){
_start:
{
lean_inc(v_ClosureFailure_88_);
return v_ClosureFailure_88_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim___boxed(lean_object* v_motive_89_, lean_object* v_t_90_, lean_object* v_h_91_, lean_object* v_ClosureFailure_92_){
_start:
{
uint8_t v_t_boxed_93_; lean_object* v_res_94_; 
v_t_boxed_93_ = lean_unbox(v_t_90_);
v_res_94_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ClosureFailure_elim(v_motive_89_, v_t_boxed_93_, v_h_91_, v_ClosureFailure_92_);
lean_dec(v_ClosureFailure_92_);
return v_res_94_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ofNat(lean_object* v_n_95_){
_start:
{
lean_object* v___x_96_; uint8_t v___x_97_; 
v___x_96_ = lean_unsigned_to_nat(1u);
v___x_97_ = lean_nat_dec_le(v_n_95_, v___x_96_);
if (v___x_97_ == 0)
{
lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(2u);
v___x_99_ = lean_nat_dec_le(v_n_95_, v___x_98_);
if (v___x_99_ == 0)
{
lean_object* v___x_100_; uint8_t v___x_101_; 
v___x_100_ = lean_unsigned_to_nat(3u);
v___x_101_ = lean_nat_dec_le(v_n_95_, v___x_100_);
if (v___x_101_ == 0)
{
uint8_t v___x_102_; 
v___x_102_ = 4;
return v___x_102_;
}
else
{
uint8_t v___x_103_; 
v___x_103_ = 3;
return v___x_103_;
}
}
else
{
uint8_t v___x_104_; 
v___x_104_ = 2;
return v___x_104_;
}
}
else
{
lean_object* v___x_105_; uint8_t v___x_106_; 
v___x_105_ = lean_unsigned_to_nat(0u);
v___x_106_ = lean_nat_dec_le(v_n_95_, v___x_105_);
if (v___x_106_ == 0)
{
uint8_t v___x_107_; 
v___x_107_ = 1;
return v___x_107_;
}
else
{
uint8_t v___x_108_; 
v___x_108_ = 0;
return v___x_108_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ofNat___boxed(lean_object* v_n_109_){
_start:
{
uint8_t v_res_110_; lean_object* v_r_111_; 
v_res_110_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ofNat(v_n_109_);
lean_dec(v_n_109_);
v_r_111_ = lean_box(v_res_110_);
return v_r_111_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_instDecidableEqTerminalRoute(uint8_t v_x_112_, uint8_t v_y_113_){
_start:
{
lean_object* v___x_114_; lean_object* v___x_115_; uint8_t v___x_116_; 
v___x_114_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx(v_x_112_);
v___x_115_ = lp_FiniteQuantum_BqnfSignPacket_TerminalRoute_ctorIdx(v_y_113_);
v___x_116_ = lean_nat_dec_eq(v___x_114_, v___x_115_);
lean_dec(v___x_115_);
lean_dec(v___x_114_);
return v___x_116_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instDecidableEqTerminalRoute___boxed(lean_object* v_x_117_, lean_object* v_y_118_){
_start:
{
uint8_t v_x_13__boxed_119_; uint8_t v_y_14__boxed_120_; uint8_t v_res_121_; lean_object* v_r_122_; 
v_x_13__boxed_119_ = lean_unbox(v_x_117_);
v_y_14__boxed_120_ = lean_unbox(v_y_118_);
v_res_121_ = lp_FiniteQuantum_BqnfSignPacket_instDecidableEqTerminalRoute(v_x_13__boxed_119_, v_y_14__boxed_120_);
v_r_122_ = lean_box(v_res_121_);
return v_r_122_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10(void){
_start:
{
lean_object* v___x_138_; lean_object* v___x_139_; 
v___x_138_ = lean_unsigned_to_nat(2u);
v___x_139_ = lean_nat_to_int(v___x_138_);
return v___x_139_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11(void){
_start:
{
lean_object* v___x_140_; lean_object* v___x_141_; 
v___x_140_ = lean_unsigned_to_nat(1u);
v___x_141_ = lean_nat_to_int(v___x_140_);
return v___x_141_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr(uint8_t v_x_142_, lean_object* v_prec_143_){
_start:
{
lean_object* v___y_145_; lean_object* v___y_152_; lean_object* v___y_159_; lean_object* v___y_166_; lean_object* v___y_173_; 
switch(v_x_142_)
{
case 0:
{
lean_object* v___x_179_; uint8_t v___x_180_; 
v___x_179_ = lean_unsigned_to_nat(1024u);
v___x_180_ = lean_nat_dec_le(v___x_179_, v_prec_143_);
if (v___x_180_ == 0)
{
lean_object* v___x_181_; 
v___x_181_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10);
v___y_145_ = v___x_181_;
goto v___jp_144_;
}
else
{
lean_object* v___x_182_; 
v___x_182_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11);
v___y_145_ = v___x_182_;
goto v___jp_144_;
}
}
case 1:
{
lean_object* v___x_183_; uint8_t v___x_184_; 
v___x_183_ = lean_unsigned_to_nat(1024u);
v___x_184_ = lean_nat_dec_le(v___x_183_, v_prec_143_);
if (v___x_184_ == 0)
{
lean_object* v___x_185_; 
v___x_185_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10);
v___y_152_ = v___x_185_;
goto v___jp_151_;
}
else
{
lean_object* v___x_186_; 
v___x_186_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11);
v___y_152_ = v___x_186_;
goto v___jp_151_;
}
}
case 2:
{
lean_object* v___x_187_; uint8_t v___x_188_; 
v___x_187_ = lean_unsigned_to_nat(1024u);
v___x_188_ = lean_nat_dec_le(v___x_187_, v_prec_143_);
if (v___x_188_ == 0)
{
lean_object* v___x_189_; 
v___x_189_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10);
v___y_159_ = v___x_189_;
goto v___jp_158_;
}
else
{
lean_object* v___x_190_; 
v___x_190_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11);
v___y_159_ = v___x_190_;
goto v___jp_158_;
}
}
case 3:
{
lean_object* v___x_191_; uint8_t v___x_192_; 
v___x_191_ = lean_unsigned_to_nat(1024u);
v___x_192_ = lean_nat_dec_le(v___x_191_, v_prec_143_);
if (v___x_192_ == 0)
{
lean_object* v___x_193_; 
v___x_193_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10);
v___y_166_ = v___x_193_;
goto v___jp_165_;
}
else
{
lean_object* v___x_194_; 
v___x_194_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11);
v___y_166_ = v___x_194_;
goto v___jp_165_;
}
}
default: 
{
lean_object* v___x_195_; uint8_t v___x_196_; 
v___x_195_ = lean_unsigned_to_nat(1024u);
v___x_196_ = lean_nat_dec_le(v___x_195_, v_prec_143_);
if (v___x_196_ == 0)
{
lean_object* v___x_197_; 
v___x_197_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__10);
v___y_173_ = v___x_197_;
goto v___jp_172_;
}
else
{
lean_object* v___x_198_; 
v___x_198_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11, &lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__11);
v___y_173_ = v___x_198_;
goto v___jp_172_;
}
}
}
v___jp_144_:
{
lean_object* v___x_146_; lean_object* v___x_147_; uint8_t v___x_148_; lean_object* v___x_149_; lean_object* v___x_150_; 
v___x_146_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__1));
lean_inc(v___y_145_);
v___x_147_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_147_, 0, v___y_145_);
lean_ctor_set(v___x_147_, 1, v___x_146_);
v___x_148_ = 0;
v___x_149_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_149_, 0, v___x_147_);
lean_ctor_set_uint8(v___x_149_, sizeof(void*)*1, v___x_148_);
v___x_150_ = l_Repr_addAppParen(v___x_149_, v_prec_143_);
return v___x_150_;
}
v___jp_151_:
{
lean_object* v___x_153_; lean_object* v___x_154_; uint8_t v___x_155_; lean_object* v___x_156_; lean_object* v___x_157_; 
v___x_153_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__3));
lean_inc(v___y_152_);
v___x_154_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_154_, 0, v___y_152_);
lean_ctor_set(v___x_154_, 1, v___x_153_);
v___x_155_ = 0;
v___x_156_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_156_, 0, v___x_154_);
lean_ctor_set_uint8(v___x_156_, sizeof(void*)*1, v___x_155_);
v___x_157_ = l_Repr_addAppParen(v___x_156_, v_prec_143_);
return v___x_157_;
}
v___jp_158_:
{
lean_object* v___x_160_; lean_object* v___x_161_; uint8_t v___x_162_; lean_object* v___x_163_; lean_object* v___x_164_; 
v___x_160_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__5));
lean_inc(v___y_159_);
v___x_161_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_161_, 0, v___y_159_);
lean_ctor_set(v___x_161_, 1, v___x_160_);
v___x_162_ = 0;
v___x_163_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_163_, 0, v___x_161_);
lean_ctor_set_uint8(v___x_163_, sizeof(void*)*1, v___x_162_);
v___x_164_ = l_Repr_addAppParen(v___x_163_, v_prec_143_);
return v___x_164_;
}
v___jp_165_:
{
lean_object* v___x_167_; lean_object* v___x_168_; uint8_t v___x_169_; lean_object* v___x_170_; lean_object* v___x_171_; 
v___x_167_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__7));
lean_inc(v___y_166_);
v___x_168_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_168_, 0, v___y_166_);
lean_ctor_set(v___x_168_, 1, v___x_167_);
v___x_169_ = 0;
v___x_170_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_170_, 0, v___x_168_);
lean_ctor_set_uint8(v___x_170_, sizeof(void*)*1, v___x_169_);
v___x_171_ = l_Repr_addAppParen(v___x_170_, v_prec_143_);
return v___x_171_;
}
v___jp_172_:
{
lean_object* v___x_174_; lean_object* v___x_175_; uint8_t v___x_176_; lean_object* v___x_177_; lean_object* v___x_178_; 
v___x_174_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___closed__9));
lean_inc(v___y_173_);
v___x_175_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_175_, 0, v___y_173_);
lean_ctor_set(v___x_175_, 1, v___x_174_);
v___x_176_ = 0;
v___x_177_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_177_, 0, v___x_175_);
lean_ctor_set_uint8(v___x_177_, sizeof(void*)*1, v___x_176_);
v___x_178_ = l_Repr_addAppParen(v___x_177_, v_prec_143_);
return v___x_178_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr___boxed(lean_object* v_x_199_, lean_object* v_prec_200_){
_start:
{
uint8_t v_x_289__boxed_201_; lean_object* v_res_202_; 
v_x_289__boxed_201_ = lean_unbox(v_x_199_);
v_res_202_ = lp_FiniteQuantum_BqnfSignPacket_instReprTerminalRoute_repr(v_x_289__boxed_201_, v_prec_200_);
lean_dec(v_prec_200_);
return v_res_202_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics_decEq(lean_object* v_x_205_, lean_object* v_x_206_){
_start:
{
uint8_t v_isValidComplex_207_; uint8_t v_disjointSupports_208_; lean_object* v_closureDefect_209_; lean_object* v_residualMass_210_; uint8_t v_hasInvolutionWitness_211_; uint8_t v_isValidComplex_212_; uint8_t v_disjointSupports_213_; lean_object* v_closureDefect_214_; lean_object* v_residualMass_215_; uint8_t v_hasInvolutionWitness_216_; 
v_isValidComplex_207_ = lean_ctor_get_uint8(v_x_205_, sizeof(void*)*2);
v_disjointSupports_208_ = lean_ctor_get_uint8(v_x_205_, sizeof(void*)*2 + 1);
v_closureDefect_209_ = lean_ctor_get(v_x_205_, 0);
v_residualMass_210_ = lean_ctor_get(v_x_205_, 1);
v_hasInvolutionWitness_211_ = lean_ctor_get_uint8(v_x_205_, sizeof(void*)*2 + 2);
v_isValidComplex_212_ = lean_ctor_get_uint8(v_x_206_, sizeof(void*)*2);
v_disjointSupports_213_ = lean_ctor_get_uint8(v_x_206_, sizeof(void*)*2 + 1);
v_closureDefect_214_ = lean_ctor_get(v_x_206_, 0);
v_residualMass_215_ = lean_ctor_get(v_x_206_, 1);
v_hasInvolutionWitness_216_ = lean_ctor_get_uint8(v_x_206_, sizeof(void*)*2 + 2);
if (v_isValidComplex_207_ == 0)
{
if (v_isValidComplex_212_ == 0)
{
goto v___jp_220_;
}
else
{
return v_isValidComplex_207_;
}
}
else
{
if (v_isValidComplex_212_ == 0)
{
return v_isValidComplex_212_;
}
else
{
goto v___jp_220_;
}
}
v___jp_217_:
{
uint8_t v___x_218_; 
v___x_218_ = lean_nat_dec_eq(v_closureDefect_209_, v_closureDefect_214_);
if (v___x_218_ == 0)
{
return v___x_218_;
}
else
{
uint8_t v___x_219_; 
v___x_219_ = lean_nat_dec_eq(v_residualMass_210_, v_residualMass_215_);
if (v___x_219_ == 0)
{
return v___x_219_;
}
else
{
if (v_hasInvolutionWitness_211_ == 0)
{
if (v_hasInvolutionWitness_216_ == 0)
{
return v___x_219_;
}
else
{
return v_hasInvolutionWitness_211_;
}
}
else
{
return v_hasInvolutionWitness_216_;
}
}
}
}
v___jp_220_:
{
if (v_disjointSupports_208_ == 0)
{
if (v_disjointSupports_213_ == 0)
{
goto v___jp_217_;
}
else
{
return v_disjointSupports_208_;
}
}
else
{
if (v_disjointSupports_213_ == 0)
{
return v_disjointSupports_213_;
}
else
{
goto v___jp_217_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics_decEq___boxed(lean_object* v_x_221_, lean_object* v_x_222_){
_start:
{
uint8_t v_res_223_; lean_object* v_r_224_; 
v_res_223_ = lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics_decEq(v_x_221_, v_x_222_);
lean_dec_ref(v_x_222_);
lean_dec_ref(v_x_221_);
v_r_224_ = lean_box(v_res_223_);
return v_r_224_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics(lean_object* v_x_225_, lean_object* v_x_226_){
_start:
{
uint8_t v___x_227_; 
v___x_227_ = lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics_decEq(v_x_225_, v_x_226_);
return v___x_227_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics___boxed(lean_object* v_x_228_, lean_object* v_x_229_){
_start:
{
uint8_t v_res_230_; lean_object* v_r_231_; 
v_res_230_ = lp_FiniteQuantum_BqnfSignPacket_instDecidableEqSignPacketMetrics(v_x_228_, v_x_229_);
lean_dec_ref(v_x_229_);
lean_dec_ref(v_x_228_);
v_r_231_ = lean_box(v_res_230_);
return v_r_231_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_245_; lean_object* v___x_246_; 
v___x_245_ = lean_unsigned_to_nat(18u);
v___x_246_ = lean_nat_to_int(v___x_245_);
return v___x_246_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__12(void){
_start:
{
lean_object* v___x_253_; lean_object* v___x_254_; 
v___x_253_ = lean_unsigned_to_nat(20u);
v___x_254_ = lean_nat_to_int(v___x_253_);
return v___x_254_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_258_; lean_object* v___x_259_; 
v___x_258_ = lean_unsigned_to_nat(17u);
v___x_259_ = lean_nat_to_int(v___x_258_);
return v___x_259_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__18(void){
_start:
{
lean_object* v___x_263_; lean_object* v___x_264_; 
v___x_263_ = lean_unsigned_to_nat(16u);
v___x_264_ = lean_nat_to_int(v___x_263_);
return v___x_264_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__21(void){
_start:
{
lean_object* v___x_268_; lean_object* v___x_269_; 
v___x_268_ = lean_unsigned_to_nat(24u);
v___x_269_ = lean_nat_to_int(v___x_268_);
return v___x_269_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__23(void){
_start:
{
lean_object* v___x_271_; lean_object* v___x_272_; 
v___x_271_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__0));
v___x_272_ = lean_string_length(v___x_271_);
return v___x_272_;
}
}
static lean_object* _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__24(void){
_start:
{
lean_object* v___x_273_; lean_object* v___x_274_; 
v___x_273_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__23, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__23_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__23);
v___x_274_ = lean_nat_to_int(v___x_273_);
return v___x_274_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg(lean_object* v_x_279_){
_start:
{
uint8_t v_isValidComplex_280_; uint8_t v_disjointSupports_281_; lean_object* v_closureDefect_282_; lean_object* v_residualMass_283_; uint8_t v_hasInvolutionWitness_284_; lean_object* v___x_285_; lean_object* v___x_286_; lean_object* v___x_287_; lean_object* v___x_288_; lean_object* v___x_289_; uint8_t v___x_290_; lean_object* v___x_291_; lean_object* v___x_292_; lean_object* v___x_293_; lean_object* v___x_294_; lean_object* v___x_295_; lean_object* v___x_296_; lean_object* v___x_297_; lean_object* v___x_298_; lean_object* v___x_299_; lean_object* v___x_300_; lean_object* v___x_301_; lean_object* v___x_302_; lean_object* v___x_303_; lean_object* v___x_304_; lean_object* v___x_305_; lean_object* v___x_306_; lean_object* v___x_307_; lean_object* v___x_308_; lean_object* v___x_309_; lean_object* v___x_310_; lean_object* v___x_311_; lean_object* v___x_312_; lean_object* v___x_313_; lean_object* v___x_314_; lean_object* v___x_315_; lean_object* v___x_316_; lean_object* v___x_317_; lean_object* v___x_318_; lean_object* v___x_319_; lean_object* v___x_320_; lean_object* v___x_321_; lean_object* v___x_322_; lean_object* v___x_323_; lean_object* v___x_324_; lean_object* v___x_325_; lean_object* v___x_326_; lean_object* v___x_327_; lean_object* v___x_328_; lean_object* v___x_329_; lean_object* v___x_330_; lean_object* v___x_331_; lean_object* v___x_332_; lean_object* v___x_333_; lean_object* v___x_334_; lean_object* v___x_335_; lean_object* v___x_336_; lean_object* v___x_337_; lean_object* v___x_338_; lean_object* v___x_339_; lean_object* v___x_340_; lean_object* v___x_341_; lean_object* v___x_342_; lean_object* v___x_343_; 
v_isValidComplex_280_ = lean_ctor_get_uint8(v_x_279_, sizeof(void*)*2);
v_disjointSupports_281_ = lean_ctor_get_uint8(v_x_279_, sizeof(void*)*2 + 1);
v_closureDefect_282_ = lean_ctor_get(v_x_279_, 0);
lean_inc(v_closureDefect_282_);
v_residualMass_283_ = lean_ctor_get(v_x_279_, 1);
lean_inc(v_residualMass_283_);
v_hasInvolutionWitness_284_ = lean_ctor_get_uint8(v_x_279_, sizeof(void*)*2 + 2);
lean_dec_ref(v_x_279_);
v___x_285_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__5));
v___x_286_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__6));
v___x_287_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__7, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__7);
v___x_288_ = l_Bool_repr___redArg(v_isValidComplex_280_);
v___x_289_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_289_, 0, v___x_287_);
lean_ctor_set(v___x_289_, 1, v___x_288_);
v___x_290_ = 0;
v___x_291_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_291_, 0, v___x_289_);
lean_ctor_set_uint8(v___x_291_, sizeof(void*)*1, v___x_290_);
v___x_292_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_292_, 0, v___x_286_);
lean_ctor_set(v___x_292_, 1, v___x_291_);
v___x_293_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__9));
v___x_294_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_294_, 0, v___x_292_);
lean_ctor_set(v___x_294_, 1, v___x_293_);
v___x_295_ = lean_box(1);
v___x_296_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_296_, 0, v___x_294_);
lean_ctor_set(v___x_296_, 1, v___x_295_);
v___x_297_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__11));
v___x_298_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_298_, 0, v___x_296_);
lean_ctor_set(v___x_298_, 1, v___x_297_);
v___x_299_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_299_, 0, v___x_298_);
lean_ctor_set(v___x_299_, 1, v___x_285_);
v___x_300_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__12, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__12_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__12);
v___x_301_ = l_Bool_repr___redArg(v_disjointSupports_281_);
v___x_302_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_302_, 0, v___x_300_);
lean_ctor_set(v___x_302_, 1, v___x_301_);
v___x_303_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_303_, 0, v___x_302_);
lean_ctor_set_uint8(v___x_303_, sizeof(void*)*1, v___x_290_);
v___x_304_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_304_, 0, v___x_299_);
lean_ctor_set(v___x_304_, 1, v___x_303_);
v___x_305_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_305_, 0, v___x_304_);
lean_ctor_set(v___x_305_, 1, v___x_293_);
v___x_306_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_306_, 0, v___x_305_);
lean_ctor_set(v___x_306_, 1, v___x_295_);
v___x_307_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__14));
v___x_308_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_308_, 0, v___x_306_);
lean_ctor_set(v___x_308_, 1, v___x_307_);
v___x_309_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_309_, 0, v___x_308_);
lean_ctor_set(v___x_309_, 1, v___x_285_);
v___x_310_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__15, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__15);
v___x_311_ = l_Nat_reprFast(v_closureDefect_282_);
v___x_312_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_312_, 0, v___x_311_);
v___x_313_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_313_, 0, v___x_310_);
lean_ctor_set(v___x_313_, 1, v___x_312_);
v___x_314_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_314_, 0, v___x_313_);
lean_ctor_set_uint8(v___x_314_, sizeof(void*)*1, v___x_290_);
v___x_315_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_315_, 0, v___x_309_);
lean_ctor_set(v___x_315_, 1, v___x_314_);
v___x_316_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_316_, 0, v___x_315_);
lean_ctor_set(v___x_316_, 1, v___x_293_);
v___x_317_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_317_, 0, v___x_316_);
lean_ctor_set(v___x_317_, 1, v___x_295_);
v___x_318_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__17));
v___x_319_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_319_, 0, v___x_317_);
lean_ctor_set(v___x_319_, 1, v___x_318_);
v___x_320_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_320_, 0, v___x_319_);
lean_ctor_set(v___x_320_, 1, v___x_285_);
v___x_321_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__18, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__18_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__18);
v___x_322_ = l_Nat_reprFast(v_residualMass_283_);
v___x_323_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_323_, 0, v___x_322_);
v___x_324_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_324_, 0, v___x_321_);
lean_ctor_set(v___x_324_, 1, v___x_323_);
v___x_325_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_325_, 0, v___x_324_);
lean_ctor_set_uint8(v___x_325_, sizeof(void*)*1, v___x_290_);
v___x_326_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_326_, 0, v___x_320_);
lean_ctor_set(v___x_326_, 1, v___x_325_);
v___x_327_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_327_, 0, v___x_326_);
lean_ctor_set(v___x_327_, 1, v___x_293_);
v___x_328_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_328_, 0, v___x_327_);
lean_ctor_set(v___x_328_, 1, v___x_295_);
v___x_329_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__20));
v___x_330_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_330_, 0, v___x_328_);
lean_ctor_set(v___x_330_, 1, v___x_329_);
v___x_331_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_331_, 0, v___x_330_);
lean_ctor_set(v___x_331_, 1, v___x_285_);
v___x_332_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__21, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__21_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__21);
v___x_333_ = l_Bool_repr___redArg(v_hasInvolutionWitness_284_);
v___x_334_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_334_, 0, v___x_332_);
lean_ctor_set(v___x_334_, 1, v___x_333_);
v___x_335_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_335_, 0, v___x_334_);
lean_ctor_set_uint8(v___x_335_, sizeof(void*)*1, v___x_290_);
v___x_336_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_336_, 0, v___x_331_);
lean_ctor_set(v___x_336_, 1, v___x_335_);
v___x_337_ = lean_obj_once(&lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__24, &lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__24_once, _init_lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__24);
v___x_338_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__25));
v___x_339_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_339_, 0, v___x_338_);
lean_ctor_set(v___x_339_, 1, v___x_336_);
v___x_340_ = ((lean_object*)(lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg___closed__26));
v___x_341_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_341_, 0, v___x_339_);
lean_ctor_set(v___x_341_, 1, v___x_340_);
v___x_342_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_342_, 0, v___x_337_);
lean_ctor_set(v___x_342_, 1, v___x_341_);
v___x_343_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_343_, 0, v___x_342_);
lean_ctor_set_uint8(v___x_343_, sizeof(void*)*1, v___x_290_);
return v___x_343_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr(lean_object* v_x_344_, lean_object* v_prec_345_){
_start:
{
lean_object* v___x_346_; 
v___x_346_ = lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___redArg(v_x_344_);
return v___x_346_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr___boxed(lean_object* v_x_347_, lean_object* v_prec_348_){
_start:
{
lean_object* v_res_349_; 
v_res_349_ = lp_FiniteQuantum_BqnfSignPacket_instReprSignPacketMetrics_repr(v_x_347_, v_prec_348_);
lean_dec(v_prec_348_);
return v_res_349_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_BqnfSignPacket_routePacket(lean_object* v_m_352_){
_start:
{
uint8_t v_isValidComplex_353_; 
v_isValidComplex_353_ = lean_ctor_get_uint8(v_m_352_, sizeof(void*)*2);
if (v_isValidComplex_353_ == 0)
{
uint8_t v___x_354_; 
v___x_354_ = 4;
return v___x_354_;
}
else
{
uint8_t v_disjointSupports_355_; 
v_disjointSupports_355_ = lean_ctor_get_uint8(v_m_352_, sizeof(void*)*2 + 1);
if (v_disjointSupports_355_ == 0)
{
lean_object* v_closureDefect_356_; lean_object* v_residualMass_357_; uint8_t v_hasInvolutionWitness_358_; lean_object* v___x_359_; uint8_t v___x_360_; 
v_closureDefect_356_ = lean_ctor_get(v_m_352_, 0);
v_residualMass_357_ = lean_ctor_get(v_m_352_, 1);
v_hasInvolutionWitness_358_ = lean_ctor_get_uint8(v_m_352_, sizeof(void*)*2 + 2);
v___x_359_ = lean_unsigned_to_nat(0u);
v___x_360_ = lean_nat_dec_lt(v___x_359_, v_closureDefect_356_);
if (v___x_360_ == 0)
{
uint8_t v___x_361_; 
v___x_361_ = lean_nat_dec_eq(v_residualMass_357_, v___x_359_);
if (v___x_361_ == 0)
{
if (v_hasInvolutionWitness_358_ == 0)
{
uint8_t v___x_362_; 
v___x_362_ = 1;
return v___x_362_;
}
else
{
uint8_t v___x_363_; 
v___x_363_ = 0;
return v___x_363_;
}
}
else
{
uint8_t v___x_364_; 
v___x_364_ = 0;
return v___x_364_;
}
}
else
{
uint8_t v___x_365_; 
v___x_365_ = 2;
return v___x_365_;
}
}
else
{
uint8_t v___x_366_; 
v___x_366_ = 3;
return v___x_366_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BqnfSignPacket_routePacket___boxed(lean_object* v_m_367_){
_start:
{
uint8_t v_res_368_; lean_object* v_r_369_; 
v_res_368_ = lp_FiniteQuantum_BqnfSignPacket_routePacket(v_m_367_);
lean_dec_ref(v_m_367_);
v_r_369_ = lean_box(v_res_368_);
return v_r_369_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_BqnfSignPacket(uint8_t builtin) {
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
