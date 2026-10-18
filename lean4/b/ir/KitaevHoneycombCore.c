// Lean compiler output
// Module: KitaevHoneycombCore
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
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_nat_mod(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqSublattice(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqSublattice___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 33, .m_capacity = 33, .m_length = 32, .m_data = "KitaevHoneycombCore.Sublattice.A"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 33, .m_capacity = 33, .m_length = 32, .m_data = "KitaevHoneycombCore.Sublattice.B"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4;
static lean_once_cell_t lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice___closed__0 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqBondDir(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqBondDir___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 30, .m_capacity = 30, .m_length = 29, .m_data = "KitaevHoneycombCore.BondDir.X"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 30, .m_capacity = 30, .m_length = 29, .m_data = "KitaevHoneycombCore.BondDir.Y"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 30, .m_capacity = 30, .m_length = 29, .m_data = "KitaevHoneycombCore.BondDir.Z"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir___closed__0 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqTerminalRoute(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqTerminalRoute___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 41, .m_capacity = 41, .m_length = 40, .m_data = "KitaevHoneycombCore.TerminalRoute.Repair"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "KitaevHoneycombCore.TerminalRoute.SplitBrainRefusal"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "KitaevHoneycombCore.TerminalRoute.ClosureFailure"};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute___closed__0 = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute = (const lean_object*)&lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__0;
static lean_once_cell_t lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_route__honeycomb__state(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_route__honeycomb__state___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_toCtorIdx(uint8_t v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_toCtorIdx___boxed(lean_object* v_x_9_){
_start:
{
uint8_t v_x_4__boxed_10_; lean_object* v_res_11_; 
v_x_4__boxed_10_ = lean_unbox(v_x_9_);
v_res_11_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_toCtorIdx(v_x_4__boxed_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___redArg(lean_object* v_k_12_){
_start:
{
lean_inc(v_k_12_);
return v_k_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___redArg___boxed(lean_object* v_k_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___redArg(v_k_13_);
lean_dec(v_k_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, uint8_t v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
lean_inc(v_k_19_);
return v_k_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim___boxed(lean_object* v_motive_20_, lean_object* v_ctorIdx_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
uint8_t v_t_boxed_25_; lean_object* v_res_26_; 
v_t_boxed_25_ = lean_unbox(v_t_22_);
v_res_26_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorElim(v_motive_20_, v_ctorIdx_21_, v_t_boxed_25_, v_h_23_, v_k_24_);
lean_dec(v_k_24_);
lean_dec(v_ctorIdx_21_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___redArg(lean_object* v_A_27_){
_start:
{
lean_inc(v_A_27_);
return v_A_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___redArg___boxed(lean_object* v_A_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___redArg(v_A_28_);
lean_dec(v_A_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim(lean_object* v_motive_30_, uint8_t v_t_31_, lean_object* v_h_32_, lean_object* v_A_33_){
_start:
{
lean_inc(v_A_33_);
return v_A_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim___boxed(lean_object* v_motive_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_A_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_A_elim(v_motive_34_, v_t_boxed_38_, v_h_36_, v_A_37_);
lean_dec(v_A_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___redArg(lean_object* v_B_40_){
_start:
{
lean_inc(v_B_40_);
return v_B_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___redArg___boxed(lean_object* v_B_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___redArg(v_B_41_);
lean_dec(v_B_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_B_46_){
_start:
{
lean_inc(v_B_46_);
return v_B_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_B_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_B_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_B_50_);
lean_dec(v_B_50_);
return v_res_52_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ofNat(lean_object* v_n_53_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ofNat___boxed(lean_object* v_n_58_){
_start:
{
uint8_t v_res_59_; lean_object* v_r_60_; 
v_res_59_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ofNat(v_n_58_);
lean_dec(v_n_58_);
v_r_60_ = lean_box(v_res_59_);
return v_r_60_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqSublattice(uint8_t v_x_61_, uint8_t v_y_62_){
_start:
{
lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___x_65_; 
v___x_63_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx(v_x_61_);
v___x_64_ = lp_FiniteQuantum_KitaevHoneycombCore_Sublattice_ctorIdx(v_y_62_);
v___x_65_ = lean_nat_dec_eq(v___x_63_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_63_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqSublattice___boxed(lean_object* v_x_66_, lean_object* v_y_67_){
_start:
{
uint8_t v_x_13__boxed_68_; uint8_t v_y_14__boxed_69_; uint8_t v_res_70_; lean_object* v_r_71_; 
v_x_13__boxed_68_ = lean_unbox(v_x_66_);
v_y_14__boxed_69_ = lean_unbox(v_y_67_);
v_res_70_ = lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqSublattice(v_x_13__boxed_68_, v_y_14__boxed_69_);
v_r_71_ = lean_box(v_res_70_);
return v_r_71_;
}
}
static lean_object* _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4(void){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_78_ = lean_unsigned_to_nat(2u);
v___x_79_ = lean_nat_to_int(v___x_78_);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5(void){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; 
v___x_80_ = lean_unsigned_to_nat(1u);
v___x_81_ = lean_nat_to_int(v___x_80_);
return v___x_81_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr(uint8_t v_x_82_, lean_object* v_prec_83_){
_start:
{
lean_object* v___y_85_; lean_object* v___y_92_; 
if (v_x_82_ == 0)
{
lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(1024u);
v___x_99_ = lean_nat_dec_le(v___x_98_, v_prec_83_);
if (v___x_99_ == 0)
{
lean_object* v___x_100_; 
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_85_ = v___x_100_;
goto v___jp_84_;
}
else
{
lean_object* v___x_101_; 
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_85_ = v___x_101_;
goto v___jp_84_;
}
}
else
{
lean_object* v___x_102_; uint8_t v___x_103_; 
v___x_102_ = lean_unsigned_to_nat(1024u);
v___x_103_ = lean_nat_dec_le(v___x_102_, v_prec_83_);
if (v___x_103_ == 0)
{
lean_object* v___x_104_; 
v___x_104_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_92_ = v___x_104_;
goto v___jp_91_;
}
else
{
lean_object* v___x_105_; 
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_92_ = v___x_105_;
goto v___jp_91_;
}
}
v___jp_84_:
{
lean_object* v___x_86_; lean_object* v___x_87_; uint8_t v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; 
v___x_86_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__1));
lean_inc(v___y_85_);
v___x_87_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_87_, 0, v___y_85_);
lean_ctor_set(v___x_87_, 1, v___x_86_);
v___x_88_ = 0;
v___x_89_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_89_, 0, v___x_87_);
lean_ctor_set_uint8(v___x_89_, sizeof(void*)*1, v___x_88_);
v___x_90_ = l_Repr_addAppParen(v___x_89_, v_prec_83_);
return v___x_90_;
}
v___jp_91_:
{
lean_object* v___x_93_; lean_object* v___x_94_; uint8_t v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; 
v___x_93_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__3));
lean_inc(v___y_92_);
v___x_94_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_94_, 0, v___y_92_);
lean_ctor_set(v___x_94_, 1, v___x_93_);
v___x_95_ = 0;
v___x_96_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_96_, 0, v___x_94_);
lean_ctor_set_uint8(v___x_96_, sizeof(void*)*1, v___x_95_);
v___x_97_ = l_Repr_addAppParen(v___x_96_, v_prec_83_);
return v___x_97_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___boxed(lean_object* v_x_106_, lean_object* v_prec_107_){
_start:
{
uint8_t v_x_121__boxed_108_; lean_object* v_res_109_; 
v_x_121__boxed_108_ = lean_unbox(v_x_106_);
v_res_109_ = lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr(v_x_121__boxed_108_, v_prec_107_);
lean_dec(v_prec_107_);
return v_res_109_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx(uint8_t v_x_112_){
_start:
{
switch(v_x_112_)
{
case 0:
{
lean_object* v___x_113_; 
v___x_113_ = lean_unsigned_to_nat(0u);
return v___x_113_;
}
case 1:
{
lean_object* v___x_114_; 
v___x_114_ = lean_unsigned_to_nat(1u);
return v___x_114_;
}
default: 
{
lean_object* v___x_115_; 
v___x_115_ = lean_unsigned_to_nat(2u);
return v___x_115_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx___boxed(lean_object* v_x_116_){
_start:
{
uint8_t v_x_boxed_117_; lean_object* v_res_118_; 
v_x_boxed_117_ = lean_unbox(v_x_116_);
v_res_118_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx(v_x_boxed_117_);
return v_res_118_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_toCtorIdx(uint8_t v_x_119_){
_start:
{
lean_object* v___x_120_; 
v___x_120_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx(v_x_119_);
return v___x_120_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_toCtorIdx___boxed(lean_object* v_x_121_){
_start:
{
uint8_t v_x_4__boxed_122_; lean_object* v_res_123_; 
v_x_4__boxed_122_ = lean_unbox(v_x_121_);
v_res_123_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_toCtorIdx(v_x_4__boxed_122_);
return v_res_123_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___redArg(lean_object* v_k_124_){
_start:
{
lean_inc(v_k_124_);
return v_k_124_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___redArg___boxed(lean_object* v_k_125_){
_start:
{
lean_object* v_res_126_; 
v_res_126_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___redArg(v_k_125_);
lean_dec(v_k_125_);
return v_res_126_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim(lean_object* v_motive_127_, lean_object* v_ctorIdx_128_, uint8_t v_t_129_, lean_object* v_h_130_, lean_object* v_k_131_){
_start:
{
lean_inc(v_k_131_);
return v_k_131_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim___boxed(lean_object* v_motive_132_, lean_object* v_ctorIdx_133_, lean_object* v_t_134_, lean_object* v_h_135_, lean_object* v_k_136_){
_start:
{
uint8_t v_t_boxed_137_; lean_object* v_res_138_; 
v_t_boxed_137_ = lean_unbox(v_t_134_);
v_res_138_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorElim(v_motive_132_, v_ctorIdx_133_, v_t_boxed_137_, v_h_135_, v_k_136_);
lean_dec(v_k_136_);
lean_dec(v_ctorIdx_133_);
return v_res_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___redArg(lean_object* v_X_139_){
_start:
{
lean_inc(v_X_139_);
return v_X_139_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___redArg___boxed(lean_object* v_X_140_){
_start:
{
lean_object* v_res_141_; 
v_res_141_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___redArg(v_X_140_);
lean_dec(v_X_140_);
return v_res_141_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim(lean_object* v_motive_142_, uint8_t v_t_143_, lean_object* v_h_144_, lean_object* v_X_145_){
_start:
{
lean_inc(v_X_145_);
return v_X_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim___boxed(lean_object* v_motive_146_, lean_object* v_t_147_, lean_object* v_h_148_, lean_object* v_X_149_){
_start:
{
uint8_t v_t_boxed_150_; lean_object* v_res_151_; 
v_t_boxed_150_ = lean_unbox(v_t_147_);
v_res_151_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_X_elim(v_motive_146_, v_t_boxed_150_, v_h_148_, v_X_149_);
lean_dec(v_X_149_);
return v_res_151_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___redArg(lean_object* v_Y_152_){
_start:
{
lean_inc(v_Y_152_);
return v_Y_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___redArg___boxed(lean_object* v_Y_153_){
_start:
{
lean_object* v_res_154_; 
v_res_154_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___redArg(v_Y_153_);
lean_dec(v_Y_153_);
return v_res_154_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim(lean_object* v_motive_155_, uint8_t v_t_156_, lean_object* v_h_157_, lean_object* v_Y_158_){
_start:
{
lean_inc(v_Y_158_);
return v_Y_158_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim___boxed(lean_object* v_motive_159_, lean_object* v_t_160_, lean_object* v_h_161_, lean_object* v_Y_162_){
_start:
{
uint8_t v_t_boxed_163_; lean_object* v_res_164_; 
v_t_boxed_163_ = lean_unbox(v_t_160_);
v_res_164_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Y_elim(v_motive_159_, v_t_boxed_163_, v_h_161_, v_Y_162_);
lean_dec(v_Y_162_);
return v_res_164_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___redArg(lean_object* v_Z_165_){
_start:
{
lean_inc(v_Z_165_);
return v_Z_165_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___redArg___boxed(lean_object* v_Z_166_){
_start:
{
lean_object* v_res_167_; 
v_res_167_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___redArg(v_Z_166_);
lean_dec(v_Z_166_);
return v_res_167_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim(lean_object* v_motive_168_, uint8_t v_t_169_, lean_object* v_h_170_, lean_object* v_Z_171_){
_start:
{
lean_inc(v_Z_171_);
return v_Z_171_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim___boxed(lean_object* v_motive_172_, lean_object* v_t_173_, lean_object* v_h_174_, lean_object* v_Z_175_){
_start:
{
uint8_t v_t_boxed_176_; lean_object* v_res_177_; 
v_t_boxed_176_ = lean_unbox(v_t_173_);
v_res_177_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_Z_elim(v_motive_172_, v_t_boxed_176_, v_h_174_, v_Z_175_);
lean_dec(v_Z_175_);
return v_res_177_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ofNat(lean_object* v_n_178_){
_start:
{
lean_object* v___x_179_; uint8_t v___x_180_; 
v___x_179_ = lean_unsigned_to_nat(0u);
v___x_180_ = lean_nat_dec_le(v_n_178_, v___x_179_);
if (v___x_180_ == 0)
{
lean_object* v___x_181_; uint8_t v___x_182_; 
v___x_181_ = lean_unsigned_to_nat(1u);
v___x_182_ = lean_nat_dec_le(v_n_178_, v___x_181_);
if (v___x_182_ == 0)
{
uint8_t v___x_183_; 
v___x_183_ = 2;
return v___x_183_;
}
else
{
uint8_t v___x_184_; 
v___x_184_ = 1;
return v___x_184_;
}
}
else
{
uint8_t v___x_185_; 
v___x_185_ = 0;
return v___x_185_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ofNat___boxed(lean_object* v_n_186_){
_start:
{
uint8_t v_res_187_; lean_object* v_r_188_; 
v_res_187_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ofNat(v_n_186_);
lean_dec(v_n_186_);
v_r_188_ = lean_box(v_res_187_);
return v_r_188_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqBondDir(uint8_t v_x_189_, uint8_t v_y_190_){
_start:
{
lean_object* v___x_191_; lean_object* v___x_192_; uint8_t v___x_193_; 
v___x_191_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx(v_x_189_);
v___x_192_ = lp_FiniteQuantum_KitaevHoneycombCore_BondDir_ctorIdx(v_y_190_);
v___x_193_ = lean_nat_dec_eq(v___x_191_, v___x_192_);
lean_dec(v___x_192_);
lean_dec(v___x_191_);
return v___x_193_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqBondDir___boxed(lean_object* v_x_194_, lean_object* v_y_195_){
_start:
{
uint8_t v_x_13__boxed_196_; uint8_t v_y_14__boxed_197_; uint8_t v_res_198_; lean_object* v_r_199_; 
v_x_13__boxed_196_ = lean_unbox(v_x_194_);
v_y_14__boxed_197_ = lean_unbox(v_y_195_);
v_res_198_ = lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqBondDir(v_x_13__boxed_196_, v_y_14__boxed_197_);
v_r_199_ = lean_box(v_res_198_);
return v_r_199_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr(uint8_t v_x_209_, lean_object* v_prec_210_){
_start:
{
lean_object* v___y_212_; lean_object* v___y_219_; lean_object* v___y_226_; 
switch(v_x_209_)
{
case 0:
{
lean_object* v___x_232_; uint8_t v___x_233_; 
v___x_232_ = lean_unsigned_to_nat(1024u);
v___x_233_ = lean_nat_dec_le(v___x_232_, v_prec_210_);
if (v___x_233_ == 0)
{
lean_object* v___x_234_; 
v___x_234_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_212_ = v___x_234_;
goto v___jp_211_;
}
else
{
lean_object* v___x_235_; 
v___x_235_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_212_ = v___x_235_;
goto v___jp_211_;
}
}
case 1:
{
lean_object* v___x_236_; uint8_t v___x_237_; 
v___x_236_ = lean_unsigned_to_nat(1024u);
v___x_237_ = lean_nat_dec_le(v___x_236_, v_prec_210_);
if (v___x_237_ == 0)
{
lean_object* v___x_238_; 
v___x_238_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_219_ = v___x_238_;
goto v___jp_218_;
}
else
{
lean_object* v___x_239_; 
v___x_239_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_219_ = v___x_239_;
goto v___jp_218_;
}
}
default: 
{
lean_object* v___x_240_; uint8_t v___x_241_; 
v___x_240_ = lean_unsigned_to_nat(1024u);
v___x_241_ = lean_nat_dec_le(v___x_240_, v_prec_210_);
if (v___x_241_ == 0)
{
lean_object* v___x_242_; 
v___x_242_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_226_ = v___x_242_;
goto v___jp_225_;
}
else
{
lean_object* v___x_243_; 
v___x_243_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_226_ = v___x_243_;
goto v___jp_225_;
}
}
}
v___jp_211_:
{
lean_object* v___x_213_; lean_object* v___x_214_; uint8_t v___x_215_; lean_object* v___x_216_; lean_object* v___x_217_; 
v___x_213_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__1));
lean_inc(v___y_212_);
v___x_214_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_214_, 0, v___y_212_);
lean_ctor_set(v___x_214_, 1, v___x_213_);
v___x_215_ = 0;
v___x_216_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_216_, 0, v___x_214_);
lean_ctor_set_uint8(v___x_216_, sizeof(void*)*1, v___x_215_);
v___x_217_ = l_Repr_addAppParen(v___x_216_, v_prec_210_);
return v___x_217_;
}
v___jp_218_:
{
lean_object* v___x_220_; lean_object* v___x_221_; uint8_t v___x_222_; lean_object* v___x_223_; lean_object* v___x_224_; 
v___x_220_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__3));
lean_inc(v___y_219_);
v___x_221_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_221_, 0, v___y_219_);
lean_ctor_set(v___x_221_, 1, v___x_220_);
v___x_222_ = 0;
v___x_223_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_223_, 0, v___x_221_);
lean_ctor_set_uint8(v___x_223_, sizeof(void*)*1, v___x_222_);
v___x_224_ = l_Repr_addAppParen(v___x_223_, v_prec_210_);
return v___x_224_;
}
v___jp_225_:
{
lean_object* v___x_227_; lean_object* v___x_228_; uint8_t v___x_229_; lean_object* v___x_230_; lean_object* v___x_231_; 
v___x_227_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___closed__5));
lean_inc(v___y_226_);
v___x_228_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_228_, 0, v___y_226_);
lean_ctor_set(v___x_228_, 1, v___x_227_);
v___x_229_ = 0;
v___x_230_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_230_, 0, v___x_228_);
lean_ctor_set_uint8(v___x_230_, sizeof(void*)*1, v___x_229_);
v___x_231_ = l_Repr_addAppParen(v___x_230_, v_prec_210_);
return v___x_231_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr___boxed(lean_object* v_x_244_, lean_object* v_prec_245_){
_start:
{
uint8_t v_x_173__boxed_246_; lean_object* v_res_247_; 
v_x_173__boxed_246_ = lean_unbox(v_x_244_);
v_res_247_ = lp_FiniteQuantum_KitaevHoneycombCore_instReprBondDir_repr(v_x_173__boxed_246_, v_prec_245_);
lean_dec(v_prec_245_);
return v_res_247_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx(uint8_t v_x_250_){
_start:
{
switch(v_x_250_)
{
case 0:
{
lean_object* v___x_251_; 
v___x_251_ = lean_unsigned_to_nat(0u);
return v___x_251_;
}
case 1:
{
lean_object* v___x_252_; 
v___x_252_ = lean_unsigned_to_nat(1u);
return v___x_252_;
}
default: 
{
lean_object* v___x_253_; 
v___x_253_ = lean_unsigned_to_nat(2u);
return v___x_253_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx___boxed(lean_object* v_x_254_){
_start:
{
uint8_t v_x_boxed_255_; lean_object* v_res_256_; 
v_x_boxed_255_ = lean_unbox(v_x_254_);
v_res_256_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx(v_x_boxed_255_);
return v_res_256_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_toCtorIdx(uint8_t v_x_257_){
_start:
{
lean_object* v___x_258_; 
v___x_258_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx(v_x_257_);
return v___x_258_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_toCtorIdx___boxed(lean_object* v_x_259_){
_start:
{
uint8_t v_x_4__boxed_260_; lean_object* v_res_261_; 
v_x_4__boxed_260_ = lean_unbox(v_x_259_);
v_res_261_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_toCtorIdx(v_x_4__boxed_260_);
return v_res_261_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___redArg(lean_object* v_k_262_){
_start:
{
lean_inc(v_k_262_);
return v_k_262_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___redArg___boxed(lean_object* v_k_263_){
_start:
{
lean_object* v_res_264_; 
v_res_264_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___redArg(v_k_263_);
lean_dec(v_k_263_);
return v_res_264_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim(lean_object* v_motive_265_, lean_object* v_ctorIdx_266_, uint8_t v_t_267_, lean_object* v_h_268_, lean_object* v_k_269_){
_start:
{
lean_inc(v_k_269_);
return v_k_269_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim___boxed(lean_object* v_motive_270_, lean_object* v_ctorIdx_271_, lean_object* v_t_272_, lean_object* v_h_273_, lean_object* v_k_274_){
_start:
{
uint8_t v_t_boxed_275_; lean_object* v_res_276_; 
v_t_boxed_275_ = lean_unbox(v_t_272_);
v_res_276_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorElim(v_motive_270_, v_ctorIdx_271_, v_t_boxed_275_, v_h_273_, v_k_274_);
lean_dec(v_k_274_);
lean_dec(v_ctorIdx_271_);
return v_res_276_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___redArg(lean_object* v_Repair_277_){
_start:
{
lean_inc(v_Repair_277_);
return v_Repair_277_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___redArg___boxed(lean_object* v_Repair_278_){
_start:
{
lean_object* v_res_279_; 
v_res_279_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___redArg(v_Repair_278_);
lean_dec(v_Repair_278_);
return v_res_279_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim(lean_object* v_motive_280_, uint8_t v_t_281_, lean_object* v_h_282_, lean_object* v_Repair_283_){
_start:
{
lean_inc(v_Repair_283_);
return v_Repair_283_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim___boxed(lean_object* v_motive_284_, lean_object* v_t_285_, lean_object* v_h_286_, lean_object* v_Repair_287_){
_start:
{
uint8_t v_t_boxed_288_; lean_object* v_res_289_; 
v_t_boxed_288_ = lean_unbox(v_t_285_);
v_res_289_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_Repair_elim(v_motive_284_, v_t_boxed_288_, v_h_286_, v_Repair_287_);
lean_dec(v_Repair_287_);
return v_res_289_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object* v_SplitBrainRefusal_290_){
_start:
{
lean_inc(v_SplitBrainRefusal_290_);
return v_SplitBrainRefusal_290_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object* v_SplitBrainRefusal_291_){
_start:
{
lean_object* v_res_292_; 
v_res_292_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___redArg(v_SplitBrainRefusal_291_);
lean_dec(v_SplitBrainRefusal_291_);
return v_res_292_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim(lean_object* v_motive_293_, uint8_t v_t_294_, lean_object* v_h_295_, lean_object* v_SplitBrainRefusal_296_){
_start:
{
lean_inc(v_SplitBrainRefusal_296_);
return v_SplitBrainRefusal_296_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object* v_motive_297_, lean_object* v_t_298_, lean_object* v_h_299_, lean_object* v_SplitBrainRefusal_300_){
_start:
{
uint8_t v_t_boxed_301_; lean_object* v_res_302_; 
v_t_boxed_301_ = lean_unbox(v_t_298_);
v_res_302_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_SplitBrainRefusal_elim(v_motive_297_, v_t_boxed_301_, v_h_299_, v_SplitBrainRefusal_300_);
lean_dec(v_SplitBrainRefusal_300_);
return v_res_302_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___redArg(lean_object* v_ClosureFailure_303_){
_start:
{
lean_inc(v_ClosureFailure_303_);
return v_ClosureFailure_303_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object* v_ClosureFailure_304_){
_start:
{
lean_object* v_res_305_; 
v_res_305_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___redArg(v_ClosureFailure_304_);
lean_dec(v_ClosureFailure_304_);
return v_res_305_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim(lean_object* v_motive_306_, uint8_t v_t_307_, lean_object* v_h_308_, lean_object* v_ClosureFailure_309_){
_start:
{
lean_inc(v_ClosureFailure_309_);
return v_ClosureFailure_309_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim___boxed(lean_object* v_motive_310_, lean_object* v_t_311_, lean_object* v_h_312_, lean_object* v_ClosureFailure_313_){
_start:
{
uint8_t v_t_boxed_314_; lean_object* v_res_315_; 
v_t_boxed_314_ = lean_unbox(v_t_311_);
v_res_315_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ClosureFailure_elim(v_motive_310_, v_t_boxed_314_, v_h_312_, v_ClosureFailure_313_);
lean_dec(v_ClosureFailure_313_);
return v_res_315_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ofNat(lean_object* v_n_316_){
_start:
{
lean_object* v___x_317_; uint8_t v___x_318_; 
v___x_317_ = lean_unsigned_to_nat(0u);
v___x_318_ = lean_nat_dec_le(v_n_316_, v___x_317_);
if (v___x_318_ == 0)
{
lean_object* v___x_319_; uint8_t v___x_320_; 
v___x_319_ = lean_unsigned_to_nat(1u);
v___x_320_ = lean_nat_dec_le(v_n_316_, v___x_319_);
if (v___x_320_ == 0)
{
uint8_t v___x_321_; 
v___x_321_ = 2;
return v___x_321_;
}
else
{
uint8_t v___x_322_; 
v___x_322_ = 1;
return v___x_322_;
}
}
else
{
uint8_t v___x_323_; 
v___x_323_ = 0;
return v___x_323_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ofNat___boxed(lean_object* v_n_324_){
_start:
{
uint8_t v_res_325_; lean_object* v_r_326_; 
v_res_325_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ofNat(v_n_324_);
lean_dec(v_n_324_);
v_r_326_ = lean_box(v_res_325_);
return v_r_326_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqTerminalRoute(uint8_t v_x_327_, uint8_t v_y_328_){
_start:
{
lean_object* v___x_329_; lean_object* v___x_330_; uint8_t v___x_331_; 
v___x_329_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx(v_x_327_);
v___x_330_ = lp_FiniteQuantum_KitaevHoneycombCore_TerminalRoute_ctorIdx(v_y_328_);
v___x_331_ = lean_nat_dec_eq(v___x_329_, v___x_330_);
lean_dec(v___x_330_);
lean_dec(v___x_329_);
return v___x_331_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqTerminalRoute___boxed(lean_object* v_x_332_, lean_object* v_y_333_){
_start:
{
uint8_t v_x_13__boxed_334_; uint8_t v_y_14__boxed_335_; uint8_t v_res_336_; lean_object* v_r_337_; 
v_x_13__boxed_334_ = lean_unbox(v_x_332_);
v_y_14__boxed_335_ = lean_unbox(v_y_333_);
v_res_336_ = lp_FiniteQuantum_KitaevHoneycombCore_instDecidableEqTerminalRoute(v_x_13__boxed_334_, v_y_14__boxed_335_);
v_r_337_ = lean_box(v_res_336_);
return v_r_337_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr(uint8_t v_x_347_, lean_object* v_prec_348_){
_start:
{
lean_object* v___y_350_; lean_object* v___y_357_; lean_object* v___y_364_; 
switch(v_x_347_)
{
case 0:
{
lean_object* v___x_370_; uint8_t v___x_371_; 
v___x_370_ = lean_unsigned_to_nat(1024u);
v___x_371_ = lean_nat_dec_le(v___x_370_, v_prec_348_);
if (v___x_371_ == 0)
{
lean_object* v___x_372_; 
v___x_372_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_350_ = v___x_372_;
goto v___jp_349_;
}
else
{
lean_object* v___x_373_; 
v___x_373_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_350_ = v___x_373_;
goto v___jp_349_;
}
}
case 1:
{
lean_object* v___x_374_; uint8_t v___x_375_; 
v___x_374_ = lean_unsigned_to_nat(1024u);
v___x_375_ = lean_nat_dec_le(v___x_374_, v_prec_348_);
if (v___x_375_ == 0)
{
lean_object* v___x_376_; 
v___x_376_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_357_ = v___x_376_;
goto v___jp_356_;
}
else
{
lean_object* v___x_377_; 
v___x_377_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_357_ = v___x_377_;
goto v___jp_356_;
}
}
default: 
{
lean_object* v___x_378_; uint8_t v___x_379_; 
v___x_378_ = lean_unsigned_to_nat(1024u);
v___x_379_ = lean_nat_dec_le(v___x_378_, v_prec_348_);
if (v___x_379_ == 0)
{
lean_object* v___x_380_; 
v___x_380_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__4);
v___y_364_ = v___x_380_;
goto v___jp_363_;
}
else
{
lean_object* v___x_381_; 
v___x_381_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___y_364_ = v___x_381_;
goto v___jp_363_;
}
}
}
v___jp_349_:
{
lean_object* v___x_351_; lean_object* v___x_352_; uint8_t v___x_353_; lean_object* v___x_354_; lean_object* v___x_355_; 
v___x_351_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__1));
lean_inc(v___y_350_);
v___x_352_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_352_, 0, v___y_350_);
lean_ctor_set(v___x_352_, 1, v___x_351_);
v___x_353_ = 0;
v___x_354_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_354_, 0, v___x_352_);
lean_ctor_set_uint8(v___x_354_, sizeof(void*)*1, v___x_353_);
v___x_355_ = l_Repr_addAppParen(v___x_354_, v_prec_348_);
return v___x_355_;
}
v___jp_356_:
{
lean_object* v___x_358_; lean_object* v___x_359_; uint8_t v___x_360_; lean_object* v___x_361_; lean_object* v___x_362_; 
v___x_358_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__3));
lean_inc(v___y_357_);
v___x_359_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_359_, 0, v___y_357_);
lean_ctor_set(v___x_359_, 1, v___x_358_);
v___x_360_ = 0;
v___x_361_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_361_, 0, v___x_359_);
lean_ctor_set_uint8(v___x_361_, sizeof(void*)*1, v___x_360_);
v___x_362_ = l_Repr_addAppParen(v___x_361_, v_prec_348_);
return v___x_362_;
}
v___jp_363_:
{
lean_object* v___x_365_; lean_object* v___x_366_; uint8_t v___x_367_; lean_object* v___x_368_; lean_object* v___x_369_; 
v___x_365_ = ((lean_object*)(lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___closed__5));
lean_inc(v___y_364_);
v___x_366_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_366_, 0, v___y_364_);
lean_ctor_set(v___x_366_, 1, v___x_365_);
v___x_367_ = 0;
v___x_368_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_368_, 0, v___x_366_);
lean_ctor_set_uint8(v___x_368_, sizeof(void*)*1, v___x_367_);
v___x_369_ = l_Repr_addAppParen(v___x_368_, v_prec_348_);
return v___x_369_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr___boxed(lean_object* v_x_382_, lean_object* v_prec_383_){
_start:
{
uint8_t v_x_173__boxed_384_; lean_object* v_res_385_; 
v_x_173__boxed_384_ = lean_unbox(v_x_382_);
v_res_385_ = lp_FiniteQuantum_KitaevHoneycombCore_instReprTerminalRoute_repr(v_x_173__boxed_384_, v_prec_383_);
lean_dec(v_prec_383_);
return v_res_385_;
}
}
static lean_object* _init_lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__0(void){
_start:
{
lean_object* v___x_388_; lean_object* v___x_389_; 
v___x_388_ = lean_unsigned_to_nat(3u);
v___x_389_ = lean_nat_to_int(v___x_388_);
return v___x_389_;
}
}
static lean_object* _init_lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__1(void){
_start:
{
lean_object* v___x_390_; lean_object* v___x_391_; 
v___x_390_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5, &lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_instReprSublattice_repr___closed__5);
v___x_391_ = lean_int_neg(v___x_390_);
return v___x_391_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units(lean_object* v_f_392_){
_start:
{
lean_object* v___x_393_; lean_object* v___x_394_; lean_object* v___x_395_; uint8_t v___x_396_; 
v___x_393_ = lean_unsigned_to_nat(2u);
v___x_394_ = lean_nat_mod(v_f_392_, v___x_393_);
v___x_395_ = lean_unsigned_to_nat(0u);
v___x_396_ = lean_nat_dec_eq(v___x_394_, v___x_395_);
lean_dec(v___x_394_);
if (v___x_396_ == 0)
{
lean_object* v___x_397_; 
v___x_397_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__0, &lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__0_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__0);
return v___x_397_;
}
else
{
lean_object* v___x_398_; 
v___x_398_ = lean_obj_once(&lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__1, &lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__1_once, _init_lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___closed__1);
return v___x_398_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units___boxed(lean_object* v_f_399_){
_start:
{
lean_object* v_res_400_; 
v_res_400_ = lp_FiniteQuantum_KitaevHoneycombCore_ising__mutual__braiding__angle__units(v_f_399_);
lean_dec(v_f_399_);
return v_res_400_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_KitaevHoneycombCore_route__honeycomb__state(lean_object* v_vortex__count_401_, uint8_t v_parity__defect_402_, uint8_t v_gauge__invariant_403_){
_start:
{
if (v_gauge__invariant_403_ == 0)
{
uint8_t v___x_404_; 
v___x_404_ = 2;
return v___x_404_;
}
else
{
if (v_parity__defect_402_ == 0)
{
lean_object* v___x_405_; lean_object* v___x_406_; lean_object* v___x_407_; uint8_t v___x_408_; 
v___x_405_ = lean_unsigned_to_nat(2u);
v___x_406_ = lean_nat_mod(v_vortex__count_401_, v___x_405_);
v___x_407_ = lean_unsigned_to_nat(0u);
v___x_408_ = lean_nat_dec_eq(v___x_406_, v___x_407_);
lean_dec(v___x_406_);
if (v___x_408_ == 0)
{
uint8_t v___x_409_; 
v___x_409_ = 1;
return v___x_409_;
}
else
{
uint8_t v___x_410_; 
v___x_410_ = 0;
return v___x_410_;
}
}
else
{
uint8_t v___x_411_; 
v___x_411_ = 1;
return v___x_411_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_KitaevHoneycombCore_route__honeycomb__state___boxed(lean_object* v_vortex__count_412_, lean_object* v_parity__defect_413_, lean_object* v_gauge__invariant_414_){
_start:
{
uint8_t v_parity__defect_boxed_415_; uint8_t v_gauge__invariant_boxed_416_; uint8_t v_res_417_; lean_object* v_r_418_; 
v_parity__defect_boxed_415_ = lean_unbox(v_parity__defect_413_);
v_gauge__invariant_boxed_416_ = lean_unbox(v_gauge__invariant_414_);
v_res_417_ = lp_FiniteQuantum_KitaevHoneycombCore_route__honeycomb__state(v_vortex__count_412_, v_parity__defect_boxed_415_, v_gauge__invariant_boxed_416_);
lean_dec(v_vortex__count_412_);
v_r_418_ = lean_box(v_res_417_);
return v_r_418_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_KitaevHoneycombCore(uint8_t builtin) {
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
