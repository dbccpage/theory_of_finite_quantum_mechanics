// Lean compiler output
// Module: NonAbelianGaugeSigns
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
lean_object* lean_int_neg(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "NonAbelianGaugeSigns.Su2FluxSector.Sector0"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "NonAbelianGaugeSigns.Su2FluxSector.Sector1"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4;
static lean_once_cell_t lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqHadronTopology(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqHadronTopology___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "NonAbelianGaugeSigns.HadronTopology.Meson"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "NonAbelianGaugeSigns.HadronTopology.Baryon"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_hadronCochainCurvature(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_hadronCochainCurvature___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 50, .m_capacity = 50, .m_length = 49, .m_data = "NonAbelianGaugeSigns.PolyakovCenterSector.Trivial"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "NonAbelianGaugeSigns.PolyakovCenterSector.Clockwise"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 50, .m_capacity = 50, .m_length = 49, .m_data = "NonAbelianGaugeSigns.PolyakovCenterSector.Counter"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqColorRepresentation(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqColorRepresentation___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 53, .m_capacity = 53, .m_length = 52, .m_data = "NonAbelianGaugeSigns.ColorRepresentation.Fundamental"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "NonAbelianGaugeSigns.ColorRepresentation.Adjoint"};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0 = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation = (const lean_object*)&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_n__ality(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_n__ality___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_fluxTubeCurvature(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_fluxTubeCurvature___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_toCtorIdx(uint8_t v_x_7_){
_start:
{
lean_object* v___x_8_; 
v___x_8_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_toCtorIdx___boxed(lean_object* v_x_9_){
_start:
{
uint8_t v_x_4__boxed_10_; lean_object* v_res_11_; 
v_x_4__boxed_10_ = lean_unbox(v_x_9_);
v_res_11_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_toCtorIdx(v_x_4__boxed_10_);
return v_res_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg(lean_object* v_k_12_){
_start:
{
lean_inc(v_k_12_);
return v_k_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg___boxed(lean_object* v_k_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg(v_k_13_);
lean_dec(v_k_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, uint8_t v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
lean_inc(v_k_19_);
return v_k_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___boxed(lean_object* v_motive_20_, lean_object* v_ctorIdx_21_, lean_object* v_t_22_, lean_object* v_h_23_, lean_object* v_k_24_){
_start:
{
uint8_t v_t_boxed_25_; lean_object* v_res_26_; 
v_t_boxed_25_ = lean_unbox(v_t_22_);
v_res_26_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorElim(v_motive_20_, v_ctorIdx_21_, v_t_boxed_25_, v_h_23_, v_k_24_);
lean_dec(v_k_24_);
lean_dec(v_ctorIdx_21_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg(lean_object* v_Sector0_27_){
_start:
{
lean_inc(v_Sector0_27_);
return v_Sector0_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg___boxed(lean_object* v_Sector0_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg(v_Sector0_28_);
lean_dec(v_Sector0_28_);
return v_res_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim(lean_object* v_motive_30_, uint8_t v_t_31_, lean_object* v_h_32_, lean_object* v_Sector0_33_){
_start:
{
lean_inc(v_Sector0_33_);
return v_Sector0_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___boxed(lean_object* v_motive_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_Sector0_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim(v_motive_34_, v_t_boxed_38_, v_h_36_, v_Sector0_37_);
lean_dec(v_Sector0_37_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg(lean_object* v_Sector1_40_){
_start:
{
lean_inc(v_Sector1_40_);
return v_Sector1_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg___boxed(lean_object* v_Sector1_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg(v_Sector1_41_);
lean_dec(v_Sector1_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_Sector1_46_){
_start:
{
lean_inc(v_Sector1_46_);
return v_Sector1_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_Sector1_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_Sector1_50_);
lean_dec(v_Sector1_50_);
return v_res_52_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ofNat(lean_object* v_n_53_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ofNat___boxed(lean_object* v_n_58_){
_start:
{
uint8_t v_res_59_; lean_object* v_r_60_; 
v_res_59_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ofNat(v_n_58_);
lean_dec(v_n_58_);
v_r_60_ = lean_box(v_res_59_);
return v_r_60_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector(uint8_t v_x_61_, uint8_t v_y_62_){
_start:
{
lean_object* v___x_63_; lean_object* v___x_64_; uint8_t v___x_65_; 
v___x_63_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_x_61_);
v___x_64_ = lp_FiniteQuantum_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_y_62_);
v___x_65_ = lean_nat_dec_eq(v___x_63_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_63_);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector___boxed(lean_object* v_x_66_, lean_object* v_y_67_){
_start:
{
uint8_t v_x_13__boxed_68_; uint8_t v_y_14__boxed_69_; uint8_t v_res_70_; lean_object* v_r_71_; 
v_x_13__boxed_68_ = lean_unbox(v_x_66_);
v_y_14__boxed_69_ = lean_unbox(v_y_67_);
v_res_70_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector(v_x_13__boxed_68_, v_y_14__boxed_69_);
v_r_71_ = lean_box(v_res_70_);
return v_r_71_;
}
}
static lean_object* _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4(void){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_78_ = lean_unsigned_to_nat(2u);
v___x_79_ = lean_nat_to_int(v___x_78_);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5(void){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; 
v___x_80_ = lean_unsigned_to_nat(1u);
v___x_81_ = lean_nat_to_int(v___x_80_);
return v___x_81_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr(uint8_t v_x_82_, lean_object* v_prec_83_){
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
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_85_ = v___x_100_;
goto v___jp_84_;
}
else
{
lean_object* v___x_101_; 
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
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
v___x_104_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_92_ = v___x_104_;
goto v___jp_91_;
}
else
{
lean_object* v___x_105_; 
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_92_ = v___x_105_;
goto v___jp_91_;
}
}
v___jp_84_:
{
lean_object* v___x_86_; lean_object* v___x_87_; uint8_t v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; 
v___x_86_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1));
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
v___x_93_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3));
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___boxed(lean_object* v_x_106_, lean_object* v_prec_107_){
_start:
{
uint8_t v_x_121__boxed_108_; lean_object* v_res_109_; 
v_x_121__boxed_108_ = lean_unbox(v_x_106_);
v_res_109_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr(v_x_121__boxed_108_, v_prec_107_);
lean_dec(v_prec_107_);
return v_res_109_;
}
}
static lean_object* _init_lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___closed__0(void){
_start:
{
lean_object* v___x_112_; lean_object* v___x_113_; 
v___x_112_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___x_113_ = lean_int_neg(v___x_112_);
return v___x_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign(uint8_t v_x_114_){
_start:
{
if (v_x_114_ == 0)
{
lean_object* v___x_115_; 
v___x_115_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
return v___x_115_;
}
else
{
lean_object* v___x_116_; 
v___x_116_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___closed__0, &lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___closed__0_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___closed__0);
return v___x_116_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign___boxed(lean_object* v_x_117_){
_start:
{
uint8_t v_x_42__boxed_118_; lean_object* v_res_119_; 
v_x_42__boxed_118_ = lean_unbox(v_x_117_);
v_res_119_ = lp_FiniteQuantum_NonAbelianGaugeSigns_su2__sign(v_x_42__boxed_118_);
return v_res_119_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx(uint8_t v_x_120_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx___boxed(lean_object* v_x_123_){
_start:
{
uint8_t v_x_boxed_124_; lean_object* v_res_125_; 
v_x_boxed_124_ = lean_unbox(v_x_123_);
v_res_125_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_x_boxed_124_);
return v_res_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_toCtorIdx(uint8_t v_x_126_){
_start:
{
lean_object* v___x_127_; 
v___x_127_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_x_126_);
return v___x_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_toCtorIdx___boxed(lean_object* v_x_128_){
_start:
{
uint8_t v_x_4__boxed_129_; lean_object* v_res_130_; 
v_x_4__boxed_129_ = lean_unbox(v_x_128_);
v_res_130_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_toCtorIdx(v_x_4__boxed_129_);
return v_res_130_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg(lean_object* v_k_131_){
_start:
{
lean_inc(v_k_131_);
return v_k_131_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg___boxed(lean_object* v_k_132_){
_start:
{
lean_object* v_res_133_; 
v_res_133_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg(v_k_132_);
lean_dec(v_k_132_);
return v_res_133_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim(lean_object* v_motive_134_, lean_object* v_ctorIdx_135_, uint8_t v_t_136_, lean_object* v_h_137_, lean_object* v_k_138_){
_start:
{
lean_inc(v_k_138_);
return v_k_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim___boxed(lean_object* v_motive_139_, lean_object* v_ctorIdx_140_, lean_object* v_t_141_, lean_object* v_h_142_, lean_object* v_k_143_){
_start:
{
uint8_t v_t_boxed_144_; lean_object* v_res_145_; 
v_t_boxed_144_ = lean_unbox(v_t_141_);
v_res_145_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorElim(v_motive_139_, v_ctorIdx_140_, v_t_boxed_144_, v_h_142_, v_k_143_);
lean_dec(v_k_143_);
lean_dec(v_ctorIdx_140_);
return v_res_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg(lean_object* v_Meson_146_){
_start:
{
lean_inc(v_Meson_146_);
return v_Meson_146_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg___boxed(lean_object* v_Meson_147_){
_start:
{
lean_object* v_res_148_; 
v_res_148_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg(v_Meson_147_);
lean_dec(v_Meson_147_);
return v_res_148_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim(lean_object* v_motive_149_, uint8_t v_t_150_, lean_object* v_h_151_, lean_object* v_Meson_152_){
_start:
{
lean_inc(v_Meson_152_);
return v_Meson_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim___boxed(lean_object* v_motive_153_, lean_object* v_t_154_, lean_object* v_h_155_, lean_object* v_Meson_156_){
_start:
{
uint8_t v_t_boxed_157_; lean_object* v_res_158_; 
v_t_boxed_157_ = lean_unbox(v_t_154_);
v_res_158_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Meson_elim(v_motive_153_, v_t_boxed_157_, v_h_155_, v_Meson_156_);
lean_dec(v_Meson_156_);
return v_res_158_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg(lean_object* v_Baryon_159_){
_start:
{
lean_inc(v_Baryon_159_);
return v_Baryon_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg___boxed(lean_object* v_Baryon_160_){
_start:
{
lean_object* v_res_161_; 
v_res_161_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg(v_Baryon_160_);
lean_dec(v_Baryon_160_);
return v_res_161_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim(lean_object* v_motive_162_, uint8_t v_t_163_, lean_object* v_h_164_, lean_object* v_Baryon_165_){
_start:
{
lean_inc(v_Baryon_165_);
return v_Baryon_165_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___boxed(lean_object* v_motive_166_, lean_object* v_t_167_, lean_object* v_h_168_, lean_object* v_Baryon_169_){
_start:
{
uint8_t v_t_boxed_170_; lean_object* v_res_171_; 
v_t_boxed_170_ = lean_unbox(v_t_167_);
v_res_171_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_Baryon_elim(v_motive_166_, v_t_boxed_170_, v_h_168_, v_Baryon_169_);
lean_dec(v_Baryon_169_);
return v_res_171_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ofNat(lean_object* v_n_172_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ofNat___boxed(lean_object* v_n_177_){
_start:
{
uint8_t v_res_178_; lean_object* v_r_179_; 
v_res_178_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ofNat(v_n_177_);
lean_dec(v_n_177_);
v_r_179_ = lean_box(v_res_178_);
return v_r_179_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqHadronTopology(uint8_t v_x_180_, uint8_t v_y_181_){
_start:
{
lean_object* v___x_182_; lean_object* v___x_183_; uint8_t v___x_184_; 
v___x_182_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_x_180_);
v___x_183_ = lp_FiniteQuantum_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_y_181_);
v___x_184_ = lean_nat_dec_eq(v___x_182_, v___x_183_);
lean_dec(v___x_183_);
lean_dec(v___x_182_);
return v___x_184_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqHadronTopology___boxed(lean_object* v_x_185_, lean_object* v_y_186_){
_start:
{
uint8_t v_x_13__boxed_187_; uint8_t v_y_14__boxed_188_; uint8_t v_res_189_; lean_object* v_r_190_; 
v_x_13__boxed_187_ = lean_unbox(v_x_185_);
v_y_14__boxed_188_ = lean_unbox(v_y_186_);
v_res_189_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqHadronTopology(v_x_13__boxed_187_, v_y_14__boxed_188_);
v_r_190_ = lean_box(v_res_189_);
return v_r_190_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr(uint8_t v_x_197_, lean_object* v_prec_198_){
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
v___x_215_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_200_ = v___x_215_;
goto v___jp_199_;
}
else
{
lean_object* v___x_216_; 
v___x_216_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
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
v___x_219_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_207_ = v___x_219_;
goto v___jp_206_;
}
else
{
lean_object* v___x_220_; 
v___x_220_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_207_ = v___x_220_;
goto v___jp_206_;
}
}
v___jp_199_:
{
lean_object* v___x_201_; lean_object* v___x_202_; uint8_t v___x_203_; lean_object* v___x_204_; lean_object* v___x_205_; 
v___x_201_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1));
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
v___x_208_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3));
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr___boxed(lean_object* v_x_221_, lean_object* v_prec_222_){
_start:
{
uint8_t v_x_117__boxed_223_; lean_object* v_res_224_; 
v_x_117__boxed_223_ = lean_unbox(v_x_221_);
v_res_224_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instReprHadronTopology_repr(v_x_117__boxed_223_, v_prec_222_);
lean_dec(v_prec_222_);
return v_res_224_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_hadronCochainCurvature(uint8_t v_x_227_){
_start:
{
if (v_x_227_ == 0)
{
lean_object* v___x_228_; 
v___x_228_ = lean_unsigned_to_nat(0u);
return v___x_228_;
}
else
{
lean_object* v___x_229_; 
v___x_229_ = lean_unsigned_to_nat(5u);
return v___x_229_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_hadronCochainCurvature___boxed(lean_object* v_x_230_){
_start:
{
uint8_t v_x_24__boxed_231_; lean_object* v_res_232_; 
v_x_24__boxed_231_ = lean_unbox(v_x_230_);
v_res_232_ = lp_FiniteQuantum_NonAbelianGaugeSigns_hadronCochainCurvature(v_x_24__boxed_231_);
return v_res_232_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(uint8_t v_x_233_){
_start:
{
switch(v_x_233_)
{
case 0:
{
lean_object* v___x_234_; 
v___x_234_ = lean_unsigned_to_nat(0u);
return v___x_234_;
}
case 1:
{
lean_object* v___x_235_; 
v___x_235_ = lean_unsigned_to_nat(1u);
return v___x_235_;
}
default: 
{
lean_object* v___x_236_; 
v___x_236_ = lean_unsigned_to_nat(2u);
return v___x_236_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx___boxed(lean_object* v_x_237_){
_start:
{
uint8_t v_x_boxed_238_; lean_object* v_res_239_; 
v_x_boxed_238_ = lean_unbox(v_x_237_);
v_res_239_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_x_boxed_238_);
return v_res_239_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_toCtorIdx(uint8_t v_x_240_){
_start:
{
lean_object* v___x_241_; 
v___x_241_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_x_240_);
return v___x_241_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_toCtorIdx___boxed(lean_object* v_x_242_){
_start:
{
uint8_t v_x_4__boxed_243_; lean_object* v_res_244_; 
v_x_4__boxed_243_ = lean_unbox(v_x_242_);
v_res_244_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_toCtorIdx(v_x_4__boxed_243_);
return v_res_244_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg(lean_object* v_k_245_){
_start:
{
lean_inc(v_k_245_);
return v_k_245_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg___boxed(lean_object* v_k_246_){
_start:
{
lean_object* v_res_247_; 
v_res_247_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg(v_k_246_);
lean_dec(v_k_246_);
return v_res_247_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim(lean_object* v_motive_248_, lean_object* v_ctorIdx_249_, uint8_t v_t_250_, lean_object* v_h_251_, lean_object* v_k_252_){
_start:
{
lean_inc(v_k_252_);
return v_k_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___boxed(lean_object* v_motive_253_, lean_object* v_ctorIdx_254_, lean_object* v_t_255_, lean_object* v_h_256_, lean_object* v_k_257_){
_start:
{
uint8_t v_t_boxed_258_; lean_object* v_res_259_; 
v_t_boxed_258_ = lean_unbox(v_t_255_);
v_res_259_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim(v_motive_253_, v_ctorIdx_254_, v_t_boxed_258_, v_h_256_, v_k_257_);
lean_dec(v_k_257_);
lean_dec(v_ctorIdx_254_);
return v_res_259_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg(lean_object* v_Trivial_260_){
_start:
{
lean_inc(v_Trivial_260_);
return v_Trivial_260_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg___boxed(lean_object* v_Trivial_261_){
_start:
{
lean_object* v_res_262_; 
v_res_262_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg(v_Trivial_261_);
lean_dec(v_Trivial_261_);
return v_res_262_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim(lean_object* v_motive_263_, uint8_t v_t_264_, lean_object* v_h_265_, lean_object* v_Trivial_266_){
_start:
{
lean_inc(v_Trivial_266_);
return v_Trivial_266_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___boxed(lean_object* v_motive_267_, lean_object* v_t_268_, lean_object* v_h_269_, lean_object* v_Trivial_270_){
_start:
{
uint8_t v_t_boxed_271_; lean_object* v_res_272_; 
v_t_boxed_271_ = lean_unbox(v_t_268_);
v_res_272_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim(v_motive_267_, v_t_boxed_271_, v_h_269_, v_Trivial_270_);
lean_dec(v_Trivial_270_);
return v_res_272_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg(lean_object* v_Clockwise_273_){
_start:
{
lean_inc(v_Clockwise_273_);
return v_Clockwise_273_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg___boxed(lean_object* v_Clockwise_274_){
_start:
{
lean_object* v_res_275_; 
v_res_275_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg(v_Clockwise_274_);
lean_dec(v_Clockwise_274_);
return v_res_275_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim(lean_object* v_motive_276_, uint8_t v_t_277_, lean_object* v_h_278_, lean_object* v_Clockwise_279_){
_start:
{
lean_inc(v_Clockwise_279_);
return v_Clockwise_279_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___boxed(lean_object* v_motive_280_, lean_object* v_t_281_, lean_object* v_h_282_, lean_object* v_Clockwise_283_){
_start:
{
uint8_t v_t_boxed_284_; lean_object* v_res_285_; 
v_t_boxed_284_ = lean_unbox(v_t_281_);
v_res_285_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim(v_motive_280_, v_t_boxed_284_, v_h_282_, v_Clockwise_283_);
lean_dec(v_Clockwise_283_);
return v_res_285_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg(lean_object* v_Counter_286_){
_start:
{
lean_inc(v_Counter_286_);
return v_Counter_286_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg___boxed(lean_object* v_Counter_287_){
_start:
{
lean_object* v_res_288_; 
v_res_288_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg(v_Counter_287_);
lean_dec(v_Counter_287_);
return v_res_288_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim(lean_object* v_motive_289_, uint8_t v_t_290_, lean_object* v_h_291_, lean_object* v_Counter_292_){
_start:
{
lean_inc(v_Counter_292_);
return v_Counter_292_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___boxed(lean_object* v_motive_293_, lean_object* v_t_294_, lean_object* v_h_295_, lean_object* v_Counter_296_){
_start:
{
uint8_t v_t_boxed_297_; lean_object* v_res_298_; 
v_t_boxed_297_ = lean_unbox(v_t_294_);
v_res_298_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim(v_motive_293_, v_t_boxed_297_, v_h_295_, v_Counter_296_);
lean_dec(v_Counter_296_);
return v_res_298_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat(lean_object* v_n_299_){
_start:
{
lean_object* v___x_300_; uint8_t v___x_301_; 
v___x_300_ = lean_unsigned_to_nat(0u);
v___x_301_ = lean_nat_dec_le(v_n_299_, v___x_300_);
if (v___x_301_ == 0)
{
lean_object* v___x_302_; uint8_t v___x_303_; 
v___x_302_ = lean_unsigned_to_nat(1u);
v___x_303_ = lean_nat_dec_le(v_n_299_, v___x_302_);
if (v___x_303_ == 0)
{
uint8_t v___x_304_; 
v___x_304_ = 2;
return v___x_304_;
}
else
{
uint8_t v___x_305_; 
v___x_305_ = 1;
return v___x_305_;
}
}
else
{
uint8_t v___x_306_; 
v___x_306_ = 0;
return v___x_306_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat___boxed(lean_object* v_n_307_){
_start:
{
uint8_t v_res_308_; lean_object* v_r_309_; 
v_res_308_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat(v_n_307_);
lean_dec(v_n_307_);
v_r_309_ = lean_box(v_res_308_);
return v_r_309_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector(uint8_t v_x_310_, uint8_t v_y_311_){
_start:
{
lean_object* v___x_312_; lean_object* v___x_313_; uint8_t v___x_314_; 
v___x_312_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_x_310_);
v___x_313_ = lp_FiniteQuantum_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_y_311_);
v___x_314_ = lean_nat_dec_eq(v___x_312_, v___x_313_);
lean_dec(v___x_313_);
lean_dec(v___x_312_);
return v___x_314_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector___boxed(lean_object* v_x_315_, lean_object* v_y_316_){
_start:
{
uint8_t v_x_13__boxed_317_; uint8_t v_y_14__boxed_318_; uint8_t v_res_319_; lean_object* v_r_320_; 
v_x_13__boxed_317_ = lean_unbox(v_x_315_);
v_y_14__boxed_318_ = lean_unbox(v_y_316_);
v_res_319_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector(v_x_13__boxed_317_, v_y_14__boxed_318_);
v_r_320_ = lean_box(v_res_319_);
return v_r_320_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr(uint8_t v_x_330_, lean_object* v_prec_331_){
_start:
{
lean_object* v___y_333_; lean_object* v___y_340_; lean_object* v___y_347_; 
switch(v_x_330_)
{
case 0:
{
lean_object* v___x_353_; uint8_t v___x_354_; 
v___x_353_ = lean_unsigned_to_nat(1024u);
v___x_354_ = lean_nat_dec_le(v___x_353_, v_prec_331_);
if (v___x_354_ == 0)
{
lean_object* v___x_355_; 
v___x_355_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_333_ = v___x_355_;
goto v___jp_332_;
}
else
{
lean_object* v___x_356_; 
v___x_356_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_333_ = v___x_356_;
goto v___jp_332_;
}
}
case 1:
{
lean_object* v___x_357_; uint8_t v___x_358_; 
v___x_357_ = lean_unsigned_to_nat(1024u);
v___x_358_ = lean_nat_dec_le(v___x_357_, v_prec_331_);
if (v___x_358_ == 0)
{
lean_object* v___x_359_; 
v___x_359_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_340_ = v___x_359_;
goto v___jp_339_;
}
else
{
lean_object* v___x_360_; 
v___x_360_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_340_ = v___x_360_;
goto v___jp_339_;
}
}
default: 
{
lean_object* v___x_361_; uint8_t v___x_362_; 
v___x_361_ = lean_unsigned_to_nat(1024u);
v___x_362_ = lean_nat_dec_le(v___x_361_, v_prec_331_);
if (v___x_362_ == 0)
{
lean_object* v___x_363_; 
v___x_363_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_347_ = v___x_363_;
goto v___jp_346_;
}
else
{
lean_object* v___x_364_; 
v___x_364_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_347_ = v___x_364_;
goto v___jp_346_;
}
}
}
v___jp_332_:
{
lean_object* v___x_334_; lean_object* v___x_335_; uint8_t v___x_336_; lean_object* v___x_337_; lean_object* v___x_338_; 
v___x_334_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1));
lean_inc(v___y_333_);
v___x_335_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_335_, 0, v___y_333_);
lean_ctor_set(v___x_335_, 1, v___x_334_);
v___x_336_ = 0;
v___x_337_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_337_, 0, v___x_335_);
lean_ctor_set_uint8(v___x_337_, sizeof(void*)*1, v___x_336_);
v___x_338_ = l_Repr_addAppParen(v___x_337_, v_prec_331_);
return v___x_338_;
}
v___jp_339_:
{
lean_object* v___x_341_; lean_object* v___x_342_; uint8_t v___x_343_; lean_object* v___x_344_; lean_object* v___x_345_; 
v___x_341_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3));
lean_inc(v___y_340_);
v___x_342_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_342_, 0, v___y_340_);
lean_ctor_set(v___x_342_, 1, v___x_341_);
v___x_343_ = 0;
v___x_344_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_344_, 0, v___x_342_);
lean_ctor_set_uint8(v___x_344_, sizeof(void*)*1, v___x_343_);
v___x_345_ = l_Repr_addAppParen(v___x_344_, v_prec_331_);
return v___x_345_;
}
v___jp_346_:
{
lean_object* v___x_348_; lean_object* v___x_349_; uint8_t v___x_350_; lean_object* v___x_351_; lean_object* v___x_352_; 
v___x_348_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5));
lean_inc(v___y_347_);
v___x_349_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_349_, 0, v___y_347_);
lean_ctor_set(v___x_349_, 1, v___x_348_);
v___x_350_ = 0;
v___x_351_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_351_, 0, v___x_349_);
lean_ctor_set_uint8(v___x_351_, sizeof(void*)*1, v___x_350_);
v___x_352_ = l_Repr_addAppParen(v___x_351_, v_prec_331_);
return v___x_352_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___boxed(lean_object* v_x_365_, lean_object* v_prec_366_){
_start:
{
uint8_t v_x_173__boxed_367_; lean_object* v_res_368_; 
v_x_173__boxed_367_ = lean_unbox(v_x_365_);
v_res_368_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr(v_x_173__boxed_367_, v_prec_366_);
lean_dec(v_prec_366_);
return v_res_368_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(uint8_t v_x_371_){
_start:
{
if (v_x_371_ == 0)
{
lean_object* v___x_372_; 
v___x_372_ = lean_unsigned_to_nat(0u);
return v___x_372_;
}
else
{
lean_object* v___x_373_; 
v___x_373_ = lean_unsigned_to_nat(1u);
return v___x_373_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx___boxed(lean_object* v_x_374_){
_start:
{
uint8_t v_x_boxed_375_; lean_object* v_res_376_; 
v_x_boxed_375_ = lean_unbox(v_x_374_);
v_res_376_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_x_boxed_375_);
return v_res_376_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_toCtorIdx(uint8_t v_x_377_){
_start:
{
lean_object* v___x_378_; 
v___x_378_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_x_377_);
return v___x_378_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_toCtorIdx___boxed(lean_object* v_x_379_){
_start:
{
uint8_t v_x_4__boxed_380_; lean_object* v_res_381_; 
v_x_4__boxed_380_ = lean_unbox(v_x_379_);
v_res_381_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_toCtorIdx(v_x_4__boxed_380_);
return v_res_381_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg(lean_object* v_k_382_){
_start:
{
lean_inc(v_k_382_);
return v_k_382_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg___boxed(lean_object* v_k_383_){
_start:
{
lean_object* v_res_384_; 
v_res_384_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg(v_k_383_);
lean_dec(v_k_383_);
return v_res_384_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim(lean_object* v_motive_385_, lean_object* v_ctorIdx_386_, uint8_t v_t_387_, lean_object* v_h_388_, lean_object* v_k_389_){
_start:
{
lean_inc(v_k_389_);
return v_k_389_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___boxed(lean_object* v_motive_390_, lean_object* v_ctorIdx_391_, lean_object* v_t_392_, lean_object* v_h_393_, lean_object* v_k_394_){
_start:
{
uint8_t v_t_boxed_395_; lean_object* v_res_396_; 
v_t_boxed_395_ = lean_unbox(v_t_392_);
v_res_396_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorElim(v_motive_390_, v_ctorIdx_391_, v_t_boxed_395_, v_h_393_, v_k_394_);
lean_dec(v_k_394_);
lean_dec(v_ctorIdx_391_);
return v_res_396_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg(lean_object* v_Fundamental_397_){
_start:
{
lean_inc(v_Fundamental_397_);
return v_Fundamental_397_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg___boxed(lean_object* v_Fundamental_398_){
_start:
{
lean_object* v_res_399_; 
v_res_399_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg(v_Fundamental_398_);
lean_dec(v_Fundamental_398_);
return v_res_399_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim(lean_object* v_motive_400_, uint8_t v_t_401_, lean_object* v_h_402_, lean_object* v_Fundamental_403_){
_start:
{
lean_inc(v_Fundamental_403_);
return v_Fundamental_403_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___boxed(lean_object* v_motive_404_, lean_object* v_t_405_, lean_object* v_h_406_, lean_object* v_Fundamental_407_){
_start:
{
uint8_t v_t_boxed_408_; lean_object* v_res_409_; 
v_t_boxed_408_ = lean_unbox(v_t_405_);
v_res_409_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim(v_motive_404_, v_t_boxed_408_, v_h_406_, v_Fundamental_407_);
lean_dec(v_Fundamental_407_);
return v_res_409_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg(lean_object* v_Adjoint_410_){
_start:
{
lean_inc(v_Adjoint_410_);
return v_Adjoint_410_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg___boxed(lean_object* v_Adjoint_411_){
_start:
{
lean_object* v_res_412_; 
v_res_412_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg(v_Adjoint_411_);
lean_dec(v_Adjoint_411_);
return v_res_412_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim(lean_object* v_motive_413_, uint8_t v_t_414_, lean_object* v_h_415_, lean_object* v_Adjoint_416_){
_start:
{
lean_inc(v_Adjoint_416_);
return v_Adjoint_416_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___boxed(lean_object* v_motive_417_, lean_object* v_t_418_, lean_object* v_h_419_, lean_object* v_Adjoint_420_){
_start:
{
uint8_t v_t_boxed_421_; lean_object* v_res_422_; 
v_t_boxed_421_ = lean_unbox(v_t_418_);
v_res_422_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim(v_motive_417_, v_t_boxed_421_, v_h_419_, v_Adjoint_420_);
lean_dec(v_Adjoint_420_);
return v_res_422_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ofNat(lean_object* v_n_423_){
_start:
{
lean_object* v___x_424_; uint8_t v___x_425_; 
v___x_424_ = lean_unsigned_to_nat(0u);
v___x_425_ = lean_nat_dec_le(v_n_423_, v___x_424_);
if (v___x_425_ == 0)
{
uint8_t v___x_426_; 
v___x_426_ = 1;
return v___x_426_;
}
else
{
uint8_t v___x_427_; 
v___x_427_ = 0;
return v___x_427_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ofNat___boxed(lean_object* v_n_428_){
_start:
{
uint8_t v_res_429_; lean_object* v_r_430_; 
v_res_429_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ofNat(v_n_428_);
lean_dec(v_n_428_);
v_r_430_ = lean_box(v_res_429_);
return v_r_430_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqColorRepresentation(uint8_t v_x_431_, uint8_t v_y_432_){
_start:
{
lean_object* v___x_433_; lean_object* v___x_434_; uint8_t v___x_435_; 
v___x_433_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_x_431_);
v___x_434_ = lp_FiniteQuantum_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_y_432_);
v___x_435_ = lean_nat_dec_eq(v___x_433_, v___x_434_);
lean_dec(v___x_434_);
lean_dec(v___x_433_);
return v___x_435_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqColorRepresentation___boxed(lean_object* v_x_436_, lean_object* v_y_437_){
_start:
{
uint8_t v_x_13__boxed_438_; uint8_t v_y_14__boxed_439_; uint8_t v_res_440_; lean_object* v_r_441_; 
v_x_13__boxed_438_ = lean_unbox(v_x_436_);
v_y_14__boxed_439_ = lean_unbox(v_y_437_);
v_res_440_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instDecidableEqColorRepresentation(v_x_13__boxed_438_, v_y_14__boxed_439_);
v_r_441_ = lean_box(v_res_440_);
return v_r_441_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr(uint8_t v_x_448_, lean_object* v_prec_449_){
_start:
{
lean_object* v___y_451_; lean_object* v___y_458_; 
if (v_x_448_ == 0)
{
lean_object* v___x_464_; uint8_t v___x_465_; 
v___x_464_ = lean_unsigned_to_nat(1024u);
v___x_465_ = lean_nat_dec_le(v___x_464_, v_prec_449_);
if (v___x_465_ == 0)
{
lean_object* v___x_466_; 
v___x_466_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_451_ = v___x_466_;
goto v___jp_450_;
}
else
{
lean_object* v___x_467_; 
v___x_467_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_451_ = v___x_467_;
goto v___jp_450_;
}
}
else
{
lean_object* v___x_468_; uint8_t v___x_469_; 
v___x_468_ = lean_unsigned_to_nat(1024u);
v___x_469_ = lean_nat_dec_le(v___x_468_, v_prec_449_);
if (v___x_469_ == 0)
{
lean_object* v___x_470_; 
v___x_470_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_458_ = v___x_470_;
goto v___jp_457_;
}
else
{
lean_object* v___x_471_; 
v___x_471_ = lean_obj_once(&lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_FiniteQuantum_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_458_ = v___x_471_;
goto v___jp_457_;
}
}
v___jp_450_:
{
lean_object* v___x_452_; lean_object* v___x_453_; uint8_t v___x_454_; lean_object* v___x_455_; lean_object* v___x_456_; 
v___x_452_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1));
lean_inc(v___y_451_);
v___x_453_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_453_, 0, v___y_451_);
lean_ctor_set(v___x_453_, 1, v___x_452_);
v___x_454_ = 0;
v___x_455_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_455_, 0, v___x_453_);
lean_ctor_set_uint8(v___x_455_, sizeof(void*)*1, v___x_454_);
v___x_456_ = l_Repr_addAppParen(v___x_455_, v_prec_449_);
return v___x_456_;
}
v___jp_457_:
{
lean_object* v___x_459_; lean_object* v___x_460_; uint8_t v___x_461_; lean_object* v___x_462_; lean_object* v___x_463_; 
v___x_459_ = ((lean_object*)(lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3));
lean_inc(v___y_458_);
v___x_460_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_460_, 0, v___y_458_);
lean_ctor_set(v___x_460_, 1, v___x_459_);
v___x_461_ = 0;
v___x_462_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_462_, 0, v___x_460_);
lean_ctor_set_uint8(v___x_462_, sizeof(void*)*1, v___x_461_);
v___x_463_ = l_Repr_addAppParen(v___x_462_, v_prec_449_);
return v___x_463_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr___boxed(lean_object* v_x_472_, lean_object* v_prec_473_){
_start:
{
uint8_t v_x_117__boxed_474_; lean_object* v_res_475_; 
v_x_117__boxed_474_ = lean_unbox(v_x_472_);
v_res_475_ = lp_FiniteQuantum_NonAbelianGaugeSigns_instReprColorRepresentation_repr(v_x_117__boxed_474_, v_prec_473_);
lean_dec(v_prec_473_);
return v_res_475_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_n__ality(lean_object* v_N__c_478_, uint8_t v_x_479_){
_start:
{
if (v_x_479_ == 0)
{
lean_object* v___x_480_; lean_object* v___x_481_; 
v___x_480_ = lean_unsigned_to_nat(1u);
v___x_481_ = lean_nat_mod(v___x_480_, v_N__c_478_);
return v___x_481_;
}
else
{
lean_object* v___x_482_; 
v___x_482_ = lean_unsigned_to_nat(0u);
return v___x_482_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_n__ality___boxed(lean_object* v_N__c_483_, lean_object* v_x_484_){
_start:
{
uint8_t v_x_37__boxed_485_; lean_object* v_res_486_; 
v_x_37__boxed_485_ = lean_unbox(v_x_484_);
v_res_486_ = lp_FiniteQuantum_NonAbelianGaugeSigns_n__ality(v_N__c_483_, v_x_37__boxed_485_);
lean_dec(v_N__c_483_);
return v_res_486_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_fluxTubeCurvature(lean_object* v_N__c_487_, uint8_t v_rep_488_){
_start:
{
lean_object* v___x_489_; 
v___x_489_ = lp_FiniteQuantum_NonAbelianGaugeSigns_n__ality(v_N__c_487_, v_rep_488_);
return v___x_489_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianGaugeSigns_fluxTubeCurvature___boxed(lean_object* v_N__c_490_, lean_object* v_rep_491_){
_start:
{
uint8_t v_rep_boxed_492_; lean_object* v_res_493_; 
v_rep_boxed_492_ = lean_unbox(v_rep_491_);
v_res_493_ = lp_FiniteQuantum_NonAbelianGaugeSigns_fluxTubeCurvature(v_N__c_490_, v_rep_boxed_492_);
lean_dec(v_N__c_490_);
return v_res_493_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_NonAbelianGaugeSigns(uint8_t builtin) {
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
