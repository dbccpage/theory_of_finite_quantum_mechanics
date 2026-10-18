// Lean compiler output
// Module: ChiralSuperconductorCore
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
lean_object* lean_int_neg(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqChirality(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqChirality___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 47, .m_capacity = 47, .m_length = 46, .m_data = "ChiralSuperconductorCore.Chirality.RightHanded"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 46, .m_capacity = 46, .m_length = 45, .m_data = "ChiralSuperconductorCore.Chirality.LeftHanded"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4;
static lean_once_cell_t lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality___closed__0 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqSurfaceOrientation(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqSurfaceOrientation___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 48, .m_capacity = 48, .m_length = 47, .m_data = "ChiralSuperconductorCore.SurfaceOrientation.Top"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 51, .m_capacity = 51, .m_length = 50, .m_data = "ChiralSuperconductorCore.SurfaceOrientation.Bottom"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__3_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation___closed__0 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqTerminalRoute(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqTerminalRoute___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 46, .m_capacity = 46, .m_length = 45, .m_data = "ChiralSuperconductorCore.TerminalRoute.Repair"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 57, .m_capacity = 57, .m_length = 56, .m_data = "ChiralSuperconductorCore.TerminalRoute.SplitBrainRefusal"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 54, .m_capacity = 54, .m_length = 53, .m_data = "ChiralSuperconductorCore.TerminalRoute.ClosureFailure"};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute___closed__0 = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute = (const lean_object*)&lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_bulk__chern__difference(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_bulk__chern__difference___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___closed__0;
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor(lean_object*, lean_object*, uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_toCtorIdx(uint8_t v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_toCtorIdx___boxed(lean_object* v_x_9_){
_start:
{
uint8_t v_x_4__boxed_10_; lean_object* v_res_11_; 
v_x_4__boxed_10_ = lean_unbox(v_x_9_);
v_res_11_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_toCtorIdx(v_x_4__boxed_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___redArg(lean_object* v_k_12_){
_start:
{
lean_inc(v_k_12_);
return v_k_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___redArg___boxed(lean_object* v_k_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___redArg(v_k_13_);
lean_dec(v_k_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, uint8_t v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
lean_inc(v_k_19_);
return v_k_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim___boxed(lean_object* v_motive_20_, lean_object* v_ctorIdx_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
uint8_t v_t_boxed_25_; lean_object* v_res_26_; 
v_t_boxed_25_ = lean_unbox(v_t_22_);
v_res_26_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorElim(v_motive_20_, v_ctorIdx_21_, v_t_boxed_25_, v_h_23_, v_k_24_);
lean_dec(v_k_24_);
lean_dec(v_ctorIdx_21_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___redArg(lean_object* v_RightHanded_27_){
_start:
{
lean_inc(v_RightHanded_27_);
return v_RightHanded_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___redArg___boxed(lean_object* v_RightHanded_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___redArg(v_RightHanded_28_);
lean_dec(v_RightHanded_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim(lean_object* v_motive_30_, uint8_t v_t_31_, lean_object* v_h_32_, lean_object* v_RightHanded_33_){
_start:
{
lean_inc(v_RightHanded_33_);
return v_RightHanded_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim___boxed(lean_object* v_motive_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_RightHanded_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_RightHanded_elim(v_motive_34_, v_t_boxed_38_, v_h_36_, v_RightHanded_37_);
lean_dec(v_RightHanded_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___redArg(lean_object* v_LeftHanded_40_){
_start:
{
lean_inc(v_LeftHanded_40_);
return v_LeftHanded_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___redArg___boxed(lean_object* v_LeftHanded_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___redArg(v_LeftHanded_41_);
lean_dec(v_LeftHanded_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_LeftHanded_46_){
_start:
{
lean_inc(v_LeftHanded_46_);
return v_LeftHanded_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_LeftHanded_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_LeftHanded_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_LeftHanded_50_);
lean_dec(v_LeftHanded_50_);
return v_res_52_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ofNat(lean_object* v_n_53_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ofNat___boxed(lean_object* v_n_58_){
_start:
{
uint8_t v_res_59_; lean_object* v_r_60_; 
v_res_59_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ofNat(v_n_58_);
lean_dec(v_n_58_);
v_r_60_ = lean_box(v_res_59_);
return v_r_60_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqChirality(uint8_t v_x_61_, uint8_t v_y_62_){
_start:
{
lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___x_65_; 
v___x_63_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx(v_x_61_);
v___x_64_ = lp_FiniteQuantum_ChiralSuperconductorCore_Chirality_ctorIdx(v_y_62_);
v___x_65_ = lean_nat_dec_eq(v___x_63_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_63_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqChirality___boxed(lean_object* v_x_66_, lean_object* v_y_67_){
_start:
{
uint8_t v_x_13__boxed_68_; uint8_t v_y_14__boxed_69_; uint8_t v_res_70_; lean_object* v_r_71_; 
v_x_13__boxed_68_ = lean_unbox(v_x_66_);
v_y_14__boxed_69_ = lean_unbox(v_y_67_);
v_res_70_ = lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqChirality(v_x_13__boxed_68_, v_y_14__boxed_69_);
v_r_71_ = lean_box(v_res_70_);
return v_r_71_;
}
}
static lean_object* _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4(void){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_78_ = lean_unsigned_to_nat(2u);
v___x_79_ = lean_nat_to_int(v___x_78_);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5(void){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; 
v___x_80_ = lean_unsigned_to_nat(1u);
v___x_81_ = lean_nat_to_int(v___x_80_);
return v___x_81_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr(uint8_t v_x_82_, lean_object* v_prec_83_){
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
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_85_ = v___x_100_;
goto v___jp_84_;
}
else
{
lean_object* v___x_101_; 
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
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
v___x_104_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_92_ = v___x_104_;
goto v___jp_91_;
}
else
{
lean_object* v___x_105_; 
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___y_92_ = v___x_105_;
goto v___jp_91_;
}
}
v___jp_84_:
{
lean_object* v___x_86_; lean_object* v___x_87_; uint8_t v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; 
v___x_86_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__1));
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
v___x_93_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__3));
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___boxed(lean_object* v_x_106_, lean_object* v_prec_107_){
_start:
{
uint8_t v_x_121__boxed_108_; lean_object* v_res_109_; 
v_x_121__boxed_108_ = lean_unbox(v_x_106_);
v_res_109_ = lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr(v_x_121__boxed_108_, v_prec_107_);
lean_dec(v_prec_107_);
return v_res_109_;
}
}
static lean_object* _init_lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___closed__0(void){
_start:
{
lean_object* v___x_112_; lean_object* v___x_113_; 
v___x_112_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___x_113_ = lean_int_neg(v___x_112_);
return v___x_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value(uint8_t v_x_114_){
_start:
{
if (v_x_114_ == 0)
{
lean_object* v___x_115_; 
v___x_115_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
return v___x_115_;
}
else
{
lean_object* v___x_116_; 
v___x_116_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___closed__0, &lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___closed__0_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___closed__0);
return v___x_116_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value___boxed(lean_object* v_x_117_){
_start:
{
uint8_t v_x_42__boxed_118_; lean_object* v_res_119_; 
v_x_42__boxed_118_ = lean_unbox(v_x_117_);
v_res_119_ = lp_FiniteQuantum_ChiralSuperconductorCore_chirality__value(v_x_42__boxed_118_);
return v_res_119_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx(uint8_t v_x_120_){
_start:
{
if (v_x_120_ == 0)
{
lean_object* v___x_121_; 
v___x_121_ = lean_unsigned_to_nat(0u);
return v___x_121_;
}
else
{
lean_object* v___x_122_; 
v___x_122_ = lean_unsigned_to_nat(1u);
return v___x_122_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx___boxed(lean_object* v_x_123_){
_start:
{
uint8_t v_x_boxed_124_; lean_object* v_res_125_; 
v_x_boxed_124_ = lean_unbox(v_x_123_);
v_res_125_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx(v_x_boxed_124_);
return v_res_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_toCtorIdx(uint8_t v_x_126_){
_start:
{
lean_object* v___x_127_; 
v___x_127_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx(v_x_126_);
return v___x_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_toCtorIdx___boxed(lean_object* v_x_128_){
_start:
{
uint8_t v_x_4__boxed_129_; lean_object* v_res_130_; 
v_x_4__boxed_129_ = lean_unbox(v_x_128_);
v_res_130_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_toCtorIdx(v_x_4__boxed_129_);
return v_res_130_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___redArg(lean_object* v_k_131_){
_start:
{
lean_inc(v_k_131_);
return v_k_131_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___redArg___boxed(lean_object* v_k_132_){
_start:
{
lean_object* v_res_133_; 
v_res_133_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___redArg(v_k_132_);
lean_dec(v_k_132_);
return v_res_133_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim(lean_object* v_motive_134_, lean_object* v_ctorIdx_135_, uint8_t v_t_136_, lean_object* v_h_137_, lean_object* v_k_138_){
_start:
{
lean_inc(v_k_138_);
return v_k_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim___boxed(lean_object* v_motive_139_, lean_object* v_ctorIdx_140_, lean_object* v_t_141_, lean_object* v_h_142_, lean_object* v_k_143_){
_start:
{
uint8_t v_t_boxed_144_; lean_object* v_res_145_; 
v_t_boxed_144_ = lean_unbox(v_t_141_);
v_res_145_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorElim(v_motive_139_, v_ctorIdx_140_, v_t_boxed_144_, v_h_142_, v_k_143_);
lean_dec(v_k_143_);
lean_dec(v_ctorIdx_140_);
return v_res_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___redArg(lean_object* v_Top_146_){
_start:
{
lean_inc(v_Top_146_);
return v_Top_146_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___redArg___boxed(lean_object* v_Top_147_){
_start:
{
lean_object* v_res_148_; 
v_res_148_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___redArg(v_Top_147_);
lean_dec(v_Top_147_);
return v_res_148_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim(lean_object* v_motive_149_, uint8_t v_t_150_, lean_object* v_h_151_, lean_object* v_Top_152_){
_start:
{
lean_inc(v_Top_152_);
return v_Top_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim___boxed(lean_object* v_motive_153_, lean_object* v_t_154_, lean_object* v_h_155_, lean_object* v_Top_156_){
_start:
{
uint8_t v_t_boxed_157_; lean_object* v_res_158_; 
v_t_boxed_157_ = lean_unbox(v_t_154_);
v_res_158_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Top_elim(v_motive_153_, v_t_boxed_157_, v_h_155_, v_Top_156_);
lean_dec(v_Top_156_);
return v_res_158_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___redArg(lean_object* v_Bottom_159_){
_start:
{
lean_inc(v_Bottom_159_);
return v_Bottom_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___redArg___boxed(lean_object* v_Bottom_160_){
_start:
{
lean_object* v_res_161_; 
v_res_161_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___redArg(v_Bottom_160_);
lean_dec(v_Bottom_160_);
return v_res_161_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim(lean_object* v_motive_162_, uint8_t v_t_163_, lean_object* v_h_164_, lean_object* v_Bottom_165_){
_start:
{
lean_inc(v_Bottom_165_);
return v_Bottom_165_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim___boxed(lean_object* v_motive_166_, lean_object* v_t_167_, lean_object* v_h_168_, lean_object* v_Bottom_169_){
_start:
{
uint8_t v_t_boxed_170_; lean_object* v_res_171_; 
v_t_boxed_170_ = lean_unbox(v_t_167_);
v_res_171_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_Bottom_elim(v_motive_166_, v_t_boxed_170_, v_h_168_, v_Bottom_169_);
lean_dec(v_Bottom_169_);
return v_res_171_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ofNat(lean_object* v_n_172_){
_start:
{
lean_object* v___x_173_; uint8_t v___x_174_; 
v___x_173_ = lean_unsigned_to_nat(0u);
v___x_174_ = lean_nat_dec_le(v_n_172_, v___x_173_);
if (v___x_174_ == 0)
{
uint8_t v___x_175_; 
v___x_175_ = 1;
return v___x_175_;
}
else
{
uint8_t v___x_176_; 
v___x_176_ = 0;
return v___x_176_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ofNat___boxed(lean_object* v_n_177_){
_start:
{
uint8_t v_res_178_; lean_object* v_r_179_; 
v_res_178_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ofNat(v_n_177_);
lean_dec(v_n_177_);
v_r_179_ = lean_box(v_res_178_);
return v_r_179_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqSurfaceOrientation(uint8_t v_x_180_, uint8_t v_y_181_){
_start:
{
lean_object* v___x_182_; lean_object* v___x_183_; uint8_t v___x_184_; 
v___x_182_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx(v_x_180_);
v___x_183_ = lp_FiniteQuantum_ChiralSuperconductorCore_SurfaceOrientation_ctorIdx(v_y_181_);
v___x_184_ = lean_nat_dec_eq(v___x_182_, v___x_183_);
lean_dec(v___x_183_);
lean_dec(v___x_182_);
return v___x_184_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqSurfaceOrientation___boxed(lean_object* v_x_185_, lean_object* v_y_186_){
_start:
{
uint8_t v_x_13__boxed_187_; uint8_t v_y_14__boxed_188_; uint8_t v_res_189_; lean_object* v_r_190_; 
v_x_13__boxed_187_ = lean_unbox(v_x_185_);
v_y_14__boxed_188_ = lean_unbox(v_y_186_);
v_res_189_ = lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqSurfaceOrientation(v_x_13__boxed_187_, v_y_14__boxed_188_);
v_r_190_ = lean_box(v_res_189_);
return v_r_190_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr(uint8_t v_x_197_, lean_object* v_prec_198_){
_start:
{
lean_object* v___y_200_; lean_object* v___y_207_; 
if (v_x_197_ == 0)
{
lean_object* v___x_213_; uint8_t v___x_214_; 
v___x_213_ = lean_unsigned_to_nat(1024u);
v___x_214_ = lean_nat_dec_le(v___x_213_, v_prec_198_);
if (v___x_214_ == 0)
{
lean_object* v___x_215_; 
v___x_215_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_200_ = v___x_215_;
goto v___jp_199_;
}
else
{
lean_object* v___x_216_; 
v___x_216_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___y_200_ = v___x_216_;
goto v___jp_199_;
}
}
else
{
lean_object* v___x_217_; uint8_t v___x_218_; 
v___x_217_ = lean_unsigned_to_nat(1024u);
v___x_218_ = lean_nat_dec_le(v___x_217_, v_prec_198_);
if (v___x_218_ == 0)
{
lean_object* v___x_219_; 
v___x_219_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_207_ = v___x_219_;
goto v___jp_206_;
}
else
{
lean_object* v___x_220_; 
v___x_220_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___y_207_ = v___x_220_;
goto v___jp_206_;
}
}
v___jp_199_:
{
lean_object* v___x_201_; lean_object* v___x_202_; uint8_t v___x_203_; lean_object* v___x_204_; lean_object* v___x_205_; 
v___x_201_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__1));
lean_inc(v___y_200_);
v___x_202_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_202_, 0, v___y_200_);
lean_ctor_set(v___x_202_, 1, v___x_201_);
v___x_203_ = 0;
v___x_204_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_204_, 0, v___x_202_);
lean_ctor_set_uint8(v___x_204_, sizeof(void*)*1, v___x_203_);
v___x_205_ = l_Repr_addAppParen(v___x_204_, v_prec_198_);
return v___x_205_;
}
v___jp_206_:
{
lean_object* v___x_208_; lean_object* v___x_209_; uint8_t v___x_210_; lean_object* v___x_211_; lean_object* v___x_212_; 
v___x_208_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___closed__3));
lean_inc(v___y_207_);
v___x_209_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_209_, 0, v___y_207_);
lean_ctor_set(v___x_209_, 1, v___x_208_);
v___x_210_ = 0;
v___x_211_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_211_, 0, v___x_209_);
lean_ctor_set_uint8(v___x_211_, sizeof(void*)*1, v___x_210_);
v___x_212_ = l_Repr_addAppParen(v___x_211_, v_prec_198_);
return v___x_212_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr___boxed(lean_object* v_x_221_, lean_object* v_prec_222_){
_start:
{
uint8_t v_x_117__boxed_223_; lean_object* v_res_224_; 
v_x_117__boxed_223_ = lean_unbox(v_x_221_);
v_res_224_ = lp_FiniteQuantum_ChiralSuperconductorCore_instReprSurfaceOrientation_repr(v_x_117__boxed_223_, v_prec_222_);
lean_dec(v_prec_222_);
return v_res_224_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx(uint8_t v_x_227_){
_start:
{
switch(v_x_227_)
{
case 0:
{
lean_object* v___x_228_; 
v___x_228_ = lean_unsigned_to_nat(0u);
return v___x_228_;
}
case 1:
{
lean_object* v___x_229_; 
v___x_229_ = lean_unsigned_to_nat(1u);
return v___x_229_;
}
default: 
{
lean_object* v___x_230_; 
v___x_230_ = lean_unsigned_to_nat(2u);
return v___x_230_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx___boxed(lean_object* v_x_231_){
_start:
{
uint8_t v_x_boxed_232_; lean_object* v_res_233_; 
v_x_boxed_232_ = lean_unbox(v_x_231_);
v_res_233_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx(v_x_boxed_232_);
return v_res_233_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_toCtorIdx(uint8_t v_x_234_){
_start:
{
lean_object* v___x_235_; 
v___x_235_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx(v_x_234_);
return v___x_235_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_toCtorIdx___boxed(lean_object* v_x_236_){
_start:
{
uint8_t v_x_4__boxed_237_; lean_object* v_res_238_; 
v_x_4__boxed_237_ = lean_unbox(v_x_236_);
v_res_238_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_toCtorIdx(v_x_4__boxed_237_);
return v_res_238_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___redArg(lean_object* v_k_239_){
_start:
{
lean_inc(v_k_239_);
return v_k_239_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___redArg___boxed(lean_object* v_k_240_){
_start:
{
lean_object* v_res_241_; 
v_res_241_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___redArg(v_k_240_);
lean_dec(v_k_240_);
return v_res_241_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim(lean_object* v_motive_242_, lean_object* v_ctorIdx_243_, uint8_t v_t_244_, lean_object* v_h_245_, lean_object* v_k_246_){
_start:
{
lean_inc(v_k_246_);
return v_k_246_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim___boxed(lean_object* v_motive_247_, lean_object* v_ctorIdx_248_, lean_object* v_t_249_, lean_object* v_h_250_, lean_object* v_k_251_){
_start:
{
uint8_t v_t_boxed_252_; lean_object* v_res_253_; 
v_t_boxed_252_ = lean_unbox(v_t_249_);
v_res_253_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorElim(v_motive_247_, v_ctorIdx_248_, v_t_boxed_252_, v_h_250_, v_k_251_);
lean_dec(v_k_251_);
lean_dec(v_ctorIdx_248_);
return v_res_253_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___redArg(lean_object* v_Repair_254_){
_start:
{
lean_inc(v_Repair_254_);
return v_Repair_254_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___redArg___boxed(lean_object* v_Repair_255_){
_start:
{
lean_object* v_res_256_; 
v_res_256_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___redArg(v_Repair_255_);
lean_dec(v_Repair_255_);
return v_res_256_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim(lean_object* v_motive_257_, uint8_t v_t_258_, lean_object* v_h_259_, lean_object* v_Repair_260_){
_start:
{
lean_inc(v_Repair_260_);
return v_Repair_260_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim___boxed(lean_object* v_motive_261_, lean_object* v_t_262_, lean_object* v_h_263_, lean_object* v_Repair_264_){
_start:
{
uint8_t v_t_boxed_265_; lean_object* v_res_266_; 
v_t_boxed_265_ = lean_unbox(v_t_262_);
v_res_266_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_Repair_elim(v_motive_261_, v_t_boxed_265_, v_h_263_, v_Repair_264_);
lean_dec(v_Repair_264_);
return v_res_266_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___redArg(lean_object* v_SplitBrainRefusal_267_){
_start:
{
lean_inc(v_SplitBrainRefusal_267_);
return v_SplitBrainRefusal_267_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___redArg___boxed(lean_object* v_SplitBrainRefusal_268_){
_start:
{
lean_object* v_res_269_; 
v_res_269_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___redArg(v_SplitBrainRefusal_268_);
lean_dec(v_SplitBrainRefusal_268_);
return v_res_269_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim(lean_object* v_motive_270_, uint8_t v_t_271_, lean_object* v_h_272_, lean_object* v_SplitBrainRefusal_273_){
_start:
{
lean_inc(v_SplitBrainRefusal_273_);
return v_SplitBrainRefusal_273_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim___boxed(lean_object* v_motive_274_, lean_object* v_t_275_, lean_object* v_h_276_, lean_object* v_SplitBrainRefusal_277_){
_start:
{
uint8_t v_t_boxed_278_; lean_object* v_res_279_; 
v_t_boxed_278_ = lean_unbox(v_t_275_);
v_res_279_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_SplitBrainRefusal_elim(v_motive_274_, v_t_boxed_278_, v_h_276_, v_SplitBrainRefusal_277_);
lean_dec(v_SplitBrainRefusal_277_);
return v_res_279_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___redArg(lean_object* v_ClosureFailure_280_){
_start:
{
lean_inc(v_ClosureFailure_280_);
return v_ClosureFailure_280_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___redArg___boxed(lean_object* v_ClosureFailure_281_){
_start:
{
lean_object* v_res_282_; 
v_res_282_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___redArg(v_ClosureFailure_281_);
lean_dec(v_ClosureFailure_281_);
return v_res_282_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim(lean_object* v_motive_283_, uint8_t v_t_284_, lean_object* v_h_285_, lean_object* v_ClosureFailure_286_){
_start:
{
lean_inc(v_ClosureFailure_286_);
return v_ClosureFailure_286_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim___boxed(lean_object* v_motive_287_, lean_object* v_t_288_, lean_object* v_h_289_, lean_object* v_ClosureFailure_290_){
_start:
{
uint8_t v_t_boxed_291_; lean_object* v_res_292_; 
v_t_boxed_291_ = lean_unbox(v_t_288_);
v_res_292_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ClosureFailure_elim(v_motive_287_, v_t_boxed_291_, v_h_289_, v_ClosureFailure_290_);
lean_dec(v_ClosureFailure_290_);
return v_res_292_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ofNat(lean_object* v_n_293_){
_start:
{
lean_object* v___x_294_; uint8_t v___x_295_; 
v___x_294_ = lean_unsigned_to_nat(0u);
v___x_295_ = lean_nat_dec_le(v_n_293_, v___x_294_);
if (v___x_295_ == 0)
{
lean_object* v___x_296_; uint8_t v___x_297_; 
v___x_296_ = lean_unsigned_to_nat(1u);
v___x_297_ = lean_nat_dec_le(v_n_293_, v___x_296_);
if (v___x_297_ == 0)
{
uint8_t v___x_298_; 
v___x_298_ = 2;
return v___x_298_;
}
else
{
uint8_t v___x_299_; 
v___x_299_ = 1;
return v___x_299_;
}
}
else
{
uint8_t v___x_300_; 
v___x_300_ = 0;
return v___x_300_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ofNat___boxed(lean_object* v_n_301_){
_start:
{
uint8_t v_res_302_; lean_object* v_r_303_; 
v_res_302_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ofNat(v_n_301_);
lean_dec(v_n_301_);
v_r_303_ = lean_box(v_res_302_);
return v_r_303_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqTerminalRoute(uint8_t v_x_304_, uint8_t v_y_305_){
_start:
{
lean_object* v___x_306_; lean_object* v___x_307_; uint8_t v___x_308_; 
v___x_306_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx(v_x_304_);
v___x_307_ = lp_FiniteQuantum_ChiralSuperconductorCore_TerminalRoute_ctorIdx(v_y_305_);
v___x_308_ = lean_nat_dec_eq(v___x_306_, v___x_307_);
lean_dec(v___x_307_);
lean_dec(v___x_306_);
return v___x_308_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqTerminalRoute___boxed(lean_object* v_x_309_, lean_object* v_y_310_){
_start:
{
uint8_t v_x_13__boxed_311_; uint8_t v_y_14__boxed_312_; uint8_t v_res_313_; lean_object* v_r_314_; 
v_x_13__boxed_311_ = lean_unbox(v_x_309_);
v_y_14__boxed_312_ = lean_unbox(v_y_310_);
v_res_313_ = lp_FiniteQuantum_ChiralSuperconductorCore_instDecidableEqTerminalRoute(v_x_13__boxed_311_, v_y_14__boxed_312_);
v_r_314_ = lean_box(v_res_313_);
return v_r_314_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr(uint8_t v_x_324_, lean_object* v_prec_325_){
_start:
{
lean_object* v___y_327_; lean_object* v___y_334_; lean_object* v___y_341_; 
switch(v_x_324_)
{
case 0:
{
lean_object* v___x_347_; uint8_t v___x_348_; 
v___x_347_ = lean_unsigned_to_nat(1024u);
v___x_348_ = lean_nat_dec_le(v___x_347_, v_prec_325_);
if (v___x_348_ == 0)
{
lean_object* v___x_349_; 
v___x_349_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_327_ = v___x_349_;
goto v___jp_326_;
}
else
{
lean_object* v___x_350_; 
v___x_350_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___y_327_ = v___x_350_;
goto v___jp_326_;
}
}
case 1:
{
lean_object* v___x_351_; uint8_t v___x_352_; 
v___x_351_ = lean_unsigned_to_nat(1024u);
v___x_352_ = lean_nat_dec_le(v___x_351_, v_prec_325_);
if (v___x_352_ == 0)
{
lean_object* v___x_353_; 
v___x_353_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_334_ = v___x_353_;
goto v___jp_333_;
}
else
{
lean_object* v___x_354_; 
v___x_354_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___y_334_ = v___x_354_;
goto v___jp_333_;
}
}
default: 
{
lean_object* v___x_355_; uint8_t v___x_356_; 
v___x_355_ = lean_unsigned_to_nat(1024u);
v___x_356_ = lean_nat_dec_le(v___x_355_, v_prec_325_);
if (v___x_356_ == 0)
{
lean_object* v___x_357_; 
v___x_357_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__4);
v___y_341_ = v___x_357_;
goto v___jp_340_;
}
else
{
lean_object* v___x_358_; 
v___x_358_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5, &lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_instReprChirality_repr___closed__5);
v___y_341_ = v___x_358_;
goto v___jp_340_;
}
}
}
v___jp_326_:
{
lean_object* v___x_328_; lean_object* v___x_329_; uint8_t v___x_330_; lean_object* v___x_331_; lean_object* v___x_332_; 
v___x_328_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__1));
lean_inc(v___y_327_);
v___x_329_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_329_, 0, v___y_327_);
lean_ctor_set(v___x_329_, 1, v___x_328_);
v___x_330_ = 0;
v___x_331_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_331_, 0, v___x_329_);
lean_ctor_set_uint8(v___x_331_, sizeof(void*)*1, v___x_330_);
v___x_332_ = l_Repr_addAppParen(v___x_331_, v_prec_325_);
return v___x_332_;
}
v___jp_333_:
{
lean_object* v___x_335_; lean_object* v___x_336_; uint8_t v___x_337_; lean_object* v___x_338_; lean_object* v___x_339_; 
v___x_335_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__3));
lean_inc(v___y_334_);
v___x_336_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_336_, 0, v___y_334_);
lean_ctor_set(v___x_336_, 1, v___x_335_);
v___x_337_ = 0;
v___x_338_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_338_, 0, v___x_336_);
lean_ctor_set_uint8(v___x_338_, sizeof(void*)*1, v___x_337_);
v___x_339_ = l_Repr_addAppParen(v___x_338_, v_prec_325_);
return v___x_339_;
}
v___jp_340_:
{
lean_object* v___x_342_; lean_object* v___x_343_; uint8_t v___x_344_; lean_object* v___x_345_; lean_object* v___x_346_; 
v___x_342_ = ((lean_object*)(lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___closed__5));
lean_inc(v___y_341_);
v___x_343_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_343_, 0, v___y_341_);
lean_ctor_set(v___x_343_, 1, v___x_342_);
v___x_344_ = 0;
v___x_345_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_345_, 0, v___x_343_);
lean_ctor_set_uint8(v___x_345_, sizeof(void*)*1, v___x_344_);
v___x_346_ = l_Repr_addAppParen(v___x_345_, v_prec_325_);
return v___x_346_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr___boxed(lean_object* v_x_359_, lean_object* v_prec_360_){
_start:
{
uint8_t v_x_173__boxed_361_; lean_object* v_res_362_; 
v_x_173__boxed_361_ = lean_unbox(v_x_359_);
v_res_362_ = lp_FiniteQuantum_ChiralSuperconductorCore_instReprTerminalRoute_repr(v_x_173__boxed_361_, v_prec_360_);
lean_dec(v_prec_360_);
return v_res_362_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_bulk__chern__difference(lean_object* v_c__plus_365_, lean_object* v_c__minus_366_){
_start:
{
lean_object* v___x_367_; 
v___x_367_ = lean_int_sub(v_c__plus_365_, v_c__minus_366_);
return v___x_367_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_bulk__chern__difference___boxed(lean_object* v_c__plus_368_, lean_object* v_c__minus_369_){
_start:
{
lean_object* v_res_370_; 
v_res_370_ = lp_FiniteQuantum_ChiralSuperconductorCore_bulk__chern__difference(v_c__plus_368_, v_c__minus_369_);
lean_dec(v_c__minus_369_);
lean_dec(v_c__plus_368_);
return v_res_370_;
}
}
static lean_object* _init_lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___closed__0(void){
_start:
{
lean_object* v___x_371_; lean_object* v___x_372_; 
v___x_371_ = lean_unsigned_to_nat(0u);
v___x_372_ = lean_nat_to_int(v___x_371_);
return v___x_372_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor(lean_object* v_net__chiral__charge_373_, lean_object* v_arc__discrepancy_374_, uint8_t v_phs__valid_375_, lean_object* v_inflow__anomaly_376_){
_start:
{
if (v_phs__valid_375_ == 0)
{
uint8_t v___x_377_; 
v___x_377_ = 2;
return v___x_377_;
}
else
{
lean_object* v___x_378_; lean_object* v___x_379_; uint8_t v___x_380_; 
v___x_378_ = lean_unsigned_to_nat(0u);
v___x_379_ = lean_obj_once(&lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___closed__0, &lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___closed__0_once, _init_lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___closed__0);
v___x_380_ = lean_int_dec_eq(v_net__chiral__charge_373_, v___x_379_);
if (v___x_380_ == 0)
{
uint8_t v___x_381_; 
v___x_381_ = 1;
return v___x_381_;
}
else
{
uint8_t v___x_382_; 
v___x_382_ = lean_nat_dec_eq(v_arc__discrepancy_374_, v___x_378_);
if (v___x_382_ == 0)
{
uint8_t v___x_383_; 
v___x_383_ = 1;
return v___x_383_;
}
else
{
uint8_t v___x_384_; 
v___x_384_ = lean_int_dec_eq(v_inflow__anomaly_376_, v___x_379_);
if (v___x_384_ == 0)
{
uint8_t v___x_385_; 
v___x_385_ = 1;
return v___x_385_;
}
else
{
uint8_t v___x_386_; 
v___x_386_ = 0;
return v___x_386_;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor___boxed(lean_object* v_net__chiral__charge_387_, lean_object* v_arc__discrepancy_388_, lean_object* v_phs__valid_389_, lean_object* v_inflow__anomaly_390_){
_start:
{
uint8_t v_phs__valid_boxed_391_; uint8_t v_res_392_; lean_object* v_r_393_; 
v_phs__valid_boxed_391_ = lean_unbox(v_phs__valid_389_);
v_res_392_ = lp_FiniteQuantum_ChiralSuperconductorCore_route__chiral__superconductor(v_net__chiral__charge_387_, v_arc__discrepancy_388_, v_phs__valid_boxed_391_, v_inflow__anomaly_390_);
lean_dec(v_inflow__anomaly_390_);
lean_dec(v_arc__discrepancy_388_);
lean_dec(v_net__chiral__charge_387_);
v_r_393_ = lean_box(v_res_392_);
return v_r_393_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_ChiralSuperconductorCore(uint8_t builtin) {
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
