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
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector___boxed(lean_object*, lean_object*);
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "NonAbelianGaugeSigns.Su2FluxSector.Sector0"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__0_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1_value;
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "NonAbelianGaugeSigns.Su2FluxSector.Sector1"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__2_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3_value;
static lean_once_cell_t lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4;
static lean_once_cell_t lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0_value;
LEAN_EXPORT const lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector___closed__0_value;
static lean_once_cell_t lp_po023_NonAbelianGaugeSigns_su2__sign___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_po023_NonAbelianGaugeSigns_su2__sign___closed__0;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_su2__sign(uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_su2__sign___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_HadronTopology_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqHadronTopology(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqHadronTopology___boxed(lean_object*, lean_object*);
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "NonAbelianGaugeSigns.HadronTopology.Meson"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__0_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1_value;
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 43, .m_capacity = 43, .m_length = 42, .m_data = "NonAbelianGaugeSigns.HadronTopology.Baryon"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__2_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3_value;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_po023_NonAbelianGaugeSigns_instReprHadronTopology___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology___closed__0_value;
LEAN_EXPORT const lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprHadronTopology___closed__0_value;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_hadronCochainCurvature(uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_hadronCochainCurvature___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector___boxed(lean_object*, lean_object*);
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 50, .m_capacity = 50, .m_length = 49, .m_data = "NonAbelianGaugeSigns.PolyakovCenterSector.Trivial"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__0_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1_value;
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 52, .m_capacity = 52, .m_length = 51, .m_data = "NonAbelianGaugeSigns.PolyakovCenterSector.Clockwise"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__2_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3_value;
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 50, .m_capacity = 50, .m_length = 49, .m_data = "NonAbelianGaugeSigns.PolyakovCenterSector.Counter"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__4_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0_value;
LEAN_EXPORT const lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector___closed__0_value;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqColorRepresentation(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqColorRepresentation___boxed(lean_object*, lean_object*);
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 53, .m_capacity = 53, .m_length = 52, .m_data = "NonAbelianGaugeSigns.ColorRepresentation.Fundamental"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__0_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1_value;
static const lean_string_object lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 49, .m_capacity = 49, .m_length = 48, .m_data = "NonAbelianGaugeSigns.ColorRepresentation.Adjoint"};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2_value;
static const lean_ctor_object lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__2_value)}};
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3_value;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0 = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0_value;
LEAN_EXPORT const lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation = (const lean_object*)&lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation___closed__0_value;
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_n__ality(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_n__ality___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_fluxTubeCurvature(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_fluxTubeCurvature___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(uint8_t v_x_1_){
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
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx___boxed(lean_object* v_x_4_){
_start:
{
uint8_t v_x_boxed_5_; lean_object* v_res_6_; 
v_x_boxed_5_ = lean_unbox(v_x_4_);
v_res_6_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_x_boxed_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg(lean_object* v_k_7_){
_start:
{
lean_inc(v_k_7_);
return v_k_7_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg___boxed(lean_object* v_k_8_){
_start:
{
lean_object* v_res_9_; 
v_res_9_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___redArg(v_k_8_);
lean_dec(v_k_8_);
return v_res_9_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim(lean_object* v_motive_10_, lean_object* v_ctorIdx_11_, uint8_t v_t_12_, lean_object* v_h_13_, lean_object* v_k_14_){
_start:
{
lean_inc(v_k_14_);
return v_k_14_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim___boxed(lean_object* v_motive_15_, lean_object* v_ctorIdx_16_, lean_object* v_t_17_, lean_object* v_h_18_, lean_object* v_k_19_){
_start:
{
uint8_t v_t_boxed_20_; lean_object* v_res_21_; 
v_t_boxed_20_ = lean_unbox(v_t_17_);
v_res_21_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorElim(v_motive_15_, v_ctorIdx_16_, v_t_boxed_20_, v_h_18_, v_k_19_);
lean_dec(v_k_19_);
lean_dec(v_ctorIdx_16_);
return v_res_21_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg(lean_object* v_Sector0_22_){
_start:
{
lean_inc(v_Sector0_22_);
return v_Sector0_22_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg___boxed(lean_object* v_Sector0_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___redArg(v_Sector0_23_);
lean_dec(v_Sector0_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim(lean_object* v_motive_25_, uint8_t v_t_26_, lean_object* v_h_27_, lean_object* v_Sector0_28_){
_start:
{
lean_inc(v_Sector0_28_);
return v_Sector0_28_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim___boxed(lean_object* v_motive_29_, lean_object* v_t_30_, lean_object* v_h_31_, lean_object* v_Sector0_32_){
_start:
{
uint8_t v_t_boxed_33_; lean_object* v_res_34_; 
v_t_boxed_33_ = lean_unbox(v_t_30_);
v_res_34_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector0_elim(v_motive_29_, v_t_boxed_33_, v_h_31_, v_Sector0_32_);
lean_dec(v_Sector0_32_);
return v_res_34_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg(lean_object* v_Sector1_35_){
_start:
{
lean_inc(v_Sector1_35_);
return v_Sector1_35_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg___boxed(lean_object* v_Sector1_36_){
_start:
{
lean_object* v_res_37_; 
v_res_37_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___redArg(v_Sector1_36_);
lean_dec(v_Sector1_36_);
return v_res_37_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim(lean_object* v_motive_38_, uint8_t v_t_39_, lean_object* v_h_40_, lean_object* v_Sector1_41_){
_start:
{
lean_inc(v_Sector1_41_);
return v_Sector1_41_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim___boxed(lean_object* v_motive_42_, lean_object* v_t_43_, lean_object* v_h_44_, lean_object* v_Sector1_45_){
_start:
{
uint8_t v_t_boxed_46_; lean_object* v_res_47_; 
v_t_boxed_46_ = lean_unbox(v_t_43_);
v_res_47_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_Sector1_elim(v_motive_42_, v_t_boxed_46_, v_h_44_, v_Sector1_45_);
lean_dec(v_Sector1_45_);
return v_res_47_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ofNat(lean_object* v_n_48_){
_start:
{
lean_object* v___x_49_; uint8_t v___x_50_; 
v___x_49_ = lean_unsigned_to_nat(0u);
v___x_50_ = lean_nat_dec_le(v_n_48_, v___x_49_);
if (v___x_50_ == 0)
{
uint8_t v___x_51_; 
v___x_51_ = 1;
return v___x_51_;
}
else
{
uint8_t v___x_52_; 
v___x_52_ = 0;
return v___x_52_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ofNat___boxed(lean_object* v_n_53_){
_start:
{
uint8_t v_res_54_; lean_object* v_r_55_; 
v_res_54_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ofNat(v_n_53_);
lean_dec(v_n_53_);
v_r_55_ = lean_box(v_res_54_);
return v_r_55_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector(uint8_t v_x_56_, uint8_t v_y_57_){
_start:
{
lean_object* v___x_58_; lean_object* v___x_59_; uint8_t v___x_60_; 
v___x_58_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_x_56_);
v___x_59_ = lp_po023_NonAbelianGaugeSigns_Su2FluxSector_ctorIdx(v_y_57_);
v___x_60_ = lean_nat_dec_eq(v___x_58_, v___x_59_);
lean_dec(v___x_59_);
lean_dec(v___x_58_);
return v___x_60_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector___boxed(lean_object* v_x_61_, lean_object* v_y_62_){
_start:
{
uint8_t v_x_13__boxed_63_; uint8_t v_y_14__boxed_64_; uint8_t v_res_65_; lean_object* v_r_66_; 
v_x_13__boxed_63_ = lean_unbox(v_x_61_);
v_y_14__boxed_64_ = lean_unbox(v_y_62_);
v_res_65_ = lp_po023_NonAbelianGaugeSigns_instDecidableEqSu2FluxSector(v_x_13__boxed_63_, v_y_14__boxed_64_);
v_r_66_ = lean_box(v_res_65_);
return v_r_66_;
}
}
static lean_object* _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4(void){
_start:
{
lean_object* v___x_73_; lean_object* v___x_74_; 
v___x_73_ = lean_unsigned_to_nat(2u);
v___x_74_ = lean_nat_to_int(v___x_73_);
return v___x_74_;
}
}
static lean_object* _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5(void){
_start:
{
lean_object* v___x_75_; lean_object* v___x_76_; 
v___x_75_ = lean_unsigned_to_nat(1u);
v___x_76_ = lean_nat_to_int(v___x_75_);
return v___x_76_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr(uint8_t v_x_77_, lean_object* v_prec_78_){
_start:
{
lean_object* v___y_80_; lean_object* v___y_87_; 
if (v_x_77_ == 0)
{
lean_object* v___x_93_; uint8_t v___x_94_; 
v___x_93_ = lean_unsigned_to_nat(1024u);
v___x_94_ = lean_nat_dec_le(v___x_93_, v_prec_78_);
if (v___x_94_ == 0)
{
lean_object* v___x_95_; 
v___x_95_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_80_ = v___x_95_;
goto v___jp_79_;
}
else
{
lean_object* v___x_96_; 
v___x_96_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_80_ = v___x_96_;
goto v___jp_79_;
}
}
else
{
lean_object* v___x_97_; uint8_t v___x_98_; 
v___x_97_ = lean_unsigned_to_nat(1024u);
v___x_98_ = lean_nat_dec_le(v___x_97_, v_prec_78_);
if (v___x_98_ == 0)
{
lean_object* v___x_99_; 
v___x_99_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_87_ = v___x_99_;
goto v___jp_86_;
}
else
{
lean_object* v___x_100_; 
v___x_100_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_87_ = v___x_100_;
goto v___jp_86_;
}
}
v___jp_79_:
{
lean_object* v___x_81_; lean_object* v___x_82_; uint8_t v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; 
v___x_81_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__1));
lean_inc(v___y_80_);
v___x_82_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_82_, 0, v___y_80_);
lean_ctor_set(v___x_82_, 1, v___x_81_);
v___x_83_ = 0;
v___x_84_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_84_, 0, v___x_82_);
lean_ctor_set_uint8(v___x_84_, sizeof(void*)*1, v___x_83_);
v___x_85_ = l_Repr_addAppParen(v___x_84_, v_prec_78_);
return v___x_85_;
}
v___jp_86_:
{
lean_object* v___x_88_; lean_object* v___x_89_; uint8_t v___x_90_; lean_object* v___x_91_; lean_object* v___x_92_; 
v___x_88_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__3));
lean_inc(v___y_87_);
v___x_89_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_89_, 0, v___y_87_);
lean_ctor_set(v___x_89_, 1, v___x_88_);
v___x_90_ = 0;
v___x_91_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_91_, 0, v___x_89_);
lean_ctor_set_uint8(v___x_91_, sizeof(void*)*1, v___x_90_);
v___x_92_ = l_Repr_addAppParen(v___x_91_, v_prec_78_);
return v___x_92_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___boxed(lean_object* v_x_101_, lean_object* v_prec_102_){
_start:
{
uint8_t v_x_121__boxed_103_; lean_object* v_res_104_; 
v_x_121__boxed_103_ = lean_unbox(v_x_101_);
v_res_104_ = lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr(v_x_121__boxed_103_, v_prec_102_);
lean_dec(v_prec_102_);
return v_res_104_;
}
}
static lean_object* _init_lp_po023_NonAbelianGaugeSigns_su2__sign___closed__0(void){
_start:
{
lean_object* v___x_107_; lean_object* v___x_108_; 
v___x_107_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___x_108_ = lean_int_neg(v___x_107_);
return v___x_108_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_su2__sign(uint8_t v_x_109_){
_start:
{
if (v_x_109_ == 0)
{
lean_object* v___x_110_; 
v___x_110_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
return v___x_110_;
}
else
{
lean_object* v___x_111_; 
v___x_111_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_su2__sign___closed__0, &lp_po023_NonAbelianGaugeSigns_su2__sign___closed__0_once, _init_lp_po023_NonAbelianGaugeSigns_su2__sign___closed__0);
return v___x_111_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_su2__sign___boxed(lean_object* v_x_112_){
_start:
{
uint8_t v_x_42__boxed_113_; lean_object* v_res_114_; 
v_x_42__boxed_113_ = lean_unbox(v_x_112_);
v_res_114_ = lp_po023_NonAbelianGaugeSigns_su2__sign(v_x_42__boxed_113_);
return v_res_114_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx(uint8_t v_x_115_){
_start:
{
if (v_x_115_ == 0)
{
lean_object* v___x_116_; 
v___x_116_ = lean_unsigned_to_nat(0u);
return v___x_116_;
}
else
{
lean_object* v___x_117_; 
v___x_117_ = lean_unsigned_to_nat(1u);
return v___x_117_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx___boxed(lean_object* v_x_118_){
_start:
{
uint8_t v_x_boxed_119_; lean_object* v_res_120_; 
v_x_boxed_119_ = lean_unbox(v_x_118_);
v_res_120_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_x_boxed_119_);
return v_res_120_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg(lean_object* v_k_121_){
_start:
{
lean_inc(v_k_121_);
return v_k_121_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg___boxed(lean_object* v_k_122_){
_start:
{
lean_object* v_res_123_; 
v_res_123_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___redArg(v_k_122_);
lean_dec(v_k_122_);
return v_res_123_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim(lean_object* v_motive_124_, lean_object* v_ctorIdx_125_, uint8_t v_t_126_, lean_object* v_h_127_, lean_object* v_k_128_){
_start:
{
lean_inc(v_k_128_);
return v_k_128_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim___boxed(lean_object* v_motive_129_, lean_object* v_ctorIdx_130_, lean_object* v_t_131_, lean_object* v_h_132_, lean_object* v_k_133_){
_start:
{
uint8_t v_t_boxed_134_; lean_object* v_res_135_; 
v_t_boxed_134_ = lean_unbox(v_t_131_);
v_res_135_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorElim(v_motive_129_, v_ctorIdx_130_, v_t_boxed_134_, v_h_132_, v_k_133_);
lean_dec(v_k_133_);
lean_dec(v_ctorIdx_130_);
return v_res_135_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg(lean_object* v_Meson_136_){
_start:
{
lean_inc(v_Meson_136_);
return v_Meson_136_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg___boxed(lean_object* v_Meson_137_){
_start:
{
lean_object* v_res_138_; 
v_res_138_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___redArg(v_Meson_137_);
lean_dec(v_Meson_137_);
return v_res_138_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim(lean_object* v_motive_139_, uint8_t v_t_140_, lean_object* v_h_141_, lean_object* v_Meson_142_){
_start:
{
lean_inc(v_Meson_142_);
return v_Meson_142_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim___boxed(lean_object* v_motive_143_, lean_object* v_t_144_, lean_object* v_h_145_, lean_object* v_Meson_146_){
_start:
{
uint8_t v_t_boxed_147_; lean_object* v_res_148_; 
v_t_boxed_147_ = lean_unbox(v_t_144_);
v_res_148_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_Meson_elim(v_motive_143_, v_t_boxed_147_, v_h_145_, v_Meson_146_);
lean_dec(v_Meson_146_);
return v_res_148_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg(lean_object* v_Baryon_149_){
_start:
{
lean_inc(v_Baryon_149_);
return v_Baryon_149_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg___boxed(lean_object* v_Baryon_150_){
_start:
{
lean_object* v_res_151_; 
v_res_151_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___redArg(v_Baryon_150_);
lean_dec(v_Baryon_150_);
return v_res_151_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim(lean_object* v_motive_152_, uint8_t v_t_153_, lean_object* v_h_154_, lean_object* v_Baryon_155_){
_start:
{
lean_inc(v_Baryon_155_);
return v_Baryon_155_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim___boxed(lean_object* v_motive_156_, lean_object* v_t_157_, lean_object* v_h_158_, lean_object* v_Baryon_159_){
_start:
{
uint8_t v_t_boxed_160_; lean_object* v_res_161_; 
v_t_boxed_160_ = lean_unbox(v_t_157_);
v_res_161_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_Baryon_elim(v_motive_156_, v_t_boxed_160_, v_h_158_, v_Baryon_159_);
lean_dec(v_Baryon_159_);
return v_res_161_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_HadronTopology_ofNat(lean_object* v_n_162_){
_start:
{
lean_object* v___x_163_; uint8_t v___x_164_; 
v___x_163_ = lean_unsigned_to_nat(0u);
v___x_164_ = lean_nat_dec_le(v_n_162_, v___x_163_);
if (v___x_164_ == 0)
{
uint8_t v___x_165_; 
v___x_165_ = 1;
return v___x_165_;
}
else
{
uint8_t v___x_166_; 
v___x_166_ = 0;
return v___x_166_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_HadronTopology_ofNat___boxed(lean_object* v_n_167_){
_start:
{
uint8_t v_res_168_; lean_object* v_r_169_; 
v_res_168_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_ofNat(v_n_167_);
lean_dec(v_n_167_);
v_r_169_ = lean_box(v_res_168_);
return v_r_169_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqHadronTopology(uint8_t v_x_170_, uint8_t v_y_171_){
_start:
{
lean_object* v___x_172_; lean_object* v___x_173_; uint8_t v___x_174_; 
v___x_172_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_x_170_);
v___x_173_ = lp_po023_NonAbelianGaugeSigns_HadronTopology_ctorIdx(v_y_171_);
v___x_174_ = lean_nat_dec_eq(v___x_172_, v___x_173_);
lean_dec(v___x_173_);
lean_dec(v___x_172_);
return v___x_174_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqHadronTopology___boxed(lean_object* v_x_175_, lean_object* v_y_176_){
_start:
{
uint8_t v_x_13__boxed_177_; uint8_t v_y_14__boxed_178_; uint8_t v_res_179_; lean_object* v_r_180_; 
v_x_13__boxed_177_ = lean_unbox(v_x_175_);
v_y_14__boxed_178_ = lean_unbox(v_y_176_);
v_res_179_ = lp_po023_NonAbelianGaugeSigns_instDecidableEqHadronTopology(v_x_13__boxed_177_, v_y_14__boxed_178_);
v_r_180_ = lean_box(v_res_179_);
return v_r_180_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr(uint8_t v_x_187_, lean_object* v_prec_188_){
_start:
{
lean_object* v___y_190_; lean_object* v___y_197_; 
if (v_x_187_ == 0)
{
lean_object* v___x_203_; uint8_t v___x_204_; 
v___x_203_ = lean_unsigned_to_nat(1024u);
v___x_204_ = lean_nat_dec_le(v___x_203_, v_prec_188_);
if (v___x_204_ == 0)
{
lean_object* v___x_205_; 
v___x_205_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_190_ = v___x_205_;
goto v___jp_189_;
}
else
{
lean_object* v___x_206_; 
v___x_206_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_190_ = v___x_206_;
goto v___jp_189_;
}
}
else
{
lean_object* v___x_207_; uint8_t v___x_208_; 
v___x_207_ = lean_unsigned_to_nat(1024u);
v___x_208_ = lean_nat_dec_le(v___x_207_, v_prec_188_);
if (v___x_208_ == 0)
{
lean_object* v___x_209_; 
v___x_209_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_197_ = v___x_209_;
goto v___jp_196_;
}
else
{
lean_object* v___x_210_; 
v___x_210_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_197_ = v___x_210_;
goto v___jp_196_;
}
}
v___jp_189_:
{
lean_object* v___x_191_; lean_object* v___x_192_; uint8_t v___x_193_; lean_object* v___x_194_; lean_object* v___x_195_; 
v___x_191_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__1));
lean_inc(v___y_190_);
v___x_192_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_192_, 0, v___y_190_);
lean_ctor_set(v___x_192_, 1, v___x_191_);
v___x_193_ = 0;
v___x_194_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_194_, 0, v___x_192_);
lean_ctor_set_uint8(v___x_194_, sizeof(void*)*1, v___x_193_);
v___x_195_ = l_Repr_addAppParen(v___x_194_, v_prec_188_);
return v___x_195_;
}
v___jp_196_:
{
lean_object* v___x_198_; lean_object* v___x_199_; uint8_t v___x_200_; lean_object* v___x_201_; lean_object* v___x_202_; 
v___x_198_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___closed__3));
lean_inc(v___y_197_);
v___x_199_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_199_, 0, v___y_197_);
lean_ctor_set(v___x_199_, 1, v___x_198_);
v___x_200_ = 0;
v___x_201_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_201_, 0, v___x_199_);
lean_ctor_set_uint8(v___x_201_, sizeof(void*)*1, v___x_200_);
v___x_202_ = l_Repr_addAppParen(v___x_201_, v_prec_188_);
return v___x_202_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr___boxed(lean_object* v_x_211_, lean_object* v_prec_212_){
_start:
{
uint8_t v_x_117__boxed_213_; lean_object* v_res_214_; 
v_x_117__boxed_213_ = lean_unbox(v_x_211_);
v_res_214_ = lp_po023_NonAbelianGaugeSigns_instReprHadronTopology_repr(v_x_117__boxed_213_, v_prec_212_);
lean_dec(v_prec_212_);
return v_res_214_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_hadronCochainCurvature(uint8_t v_x_217_){
_start:
{
if (v_x_217_ == 0)
{
lean_object* v___x_218_; 
v___x_218_ = lean_unsigned_to_nat(0u);
return v___x_218_;
}
else
{
lean_object* v___x_219_; 
v___x_219_ = lean_unsigned_to_nat(5u);
return v___x_219_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_hadronCochainCurvature___boxed(lean_object* v_x_220_){
_start:
{
uint8_t v_x_24__boxed_221_; lean_object* v_res_222_; 
v_x_24__boxed_221_ = lean_unbox(v_x_220_);
v_res_222_ = lp_po023_NonAbelianGaugeSigns_hadronCochainCurvature(v_x_24__boxed_221_);
return v_res_222_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(uint8_t v_x_223_){
_start:
{
switch(v_x_223_)
{
case 0:
{
lean_object* v___x_224_; 
v___x_224_ = lean_unsigned_to_nat(0u);
return v___x_224_;
}
case 1:
{
lean_object* v___x_225_; 
v___x_225_ = lean_unsigned_to_nat(1u);
return v___x_225_;
}
default: 
{
lean_object* v___x_226_; 
v___x_226_ = lean_unsigned_to_nat(2u);
return v___x_226_;
}
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx___boxed(lean_object* v_x_227_){
_start:
{
uint8_t v_x_boxed_228_; lean_object* v_res_229_; 
v_x_boxed_228_ = lean_unbox(v_x_227_);
v_res_229_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_x_boxed_228_);
return v_res_229_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg(lean_object* v_k_230_){
_start:
{
lean_inc(v_k_230_);
return v_k_230_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg___boxed(lean_object* v_k_231_){
_start:
{
lean_object* v_res_232_; 
v_res_232_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___redArg(v_k_231_);
lean_dec(v_k_231_);
return v_res_232_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim(lean_object* v_motive_233_, lean_object* v_ctorIdx_234_, uint8_t v_t_235_, lean_object* v_h_236_, lean_object* v_k_237_){
_start:
{
lean_inc(v_k_237_);
return v_k_237_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim___boxed(lean_object* v_motive_238_, lean_object* v_ctorIdx_239_, lean_object* v_t_240_, lean_object* v_h_241_, lean_object* v_k_242_){
_start:
{
uint8_t v_t_boxed_243_; lean_object* v_res_244_; 
v_t_boxed_243_ = lean_unbox(v_t_240_);
v_res_244_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorElim(v_motive_238_, v_ctorIdx_239_, v_t_boxed_243_, v_h_241_, v_k_242_);
lean_dec(v_k_242_);
lean_dec(v_ctorIdx_239_);
return v_res_244_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg(lean_object* v_Trivial_245_){
_start:
{
lean_inc(v_Trivial_245_);
return v_Trivial_245_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg___boxed(lean_object* v_Trivial_246_){
_start:
{
lean_object* v_res_247_; 
v_res_247_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___redArg(v_Trivial_246_);
lean_dec(v_Trivial_246_);
return v_res_247_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim(lean_object* v_motive_248_, uint8_t v_t_249_, lean_object* v_h_250_, lean_object* v_Trivial_251_){
_start:
{
lean_inc(v_Trivial_251_);
return v_Trivial_251_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim___boxed(lean_object* v_motive_252_, lean_object* v_t_253_, lean_object* v_h_254_, lean_object* v_Trivial_255_){
_start:
{
uint8_t v_t_boxed_256_; lean_object* v_res_257_; 
v_t_boxed_256_ = lean_unbox(v_t_253_);
v_res_257_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Trivial_elim(v_motive_252_, v_t_boxed_256_, v_h_254_, v_Trivial_255_);
lean_dec(v_Trivial_255_);
return v_res_257_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg(lean_object* v_Clockwise_258_){
_start:
{
lean_inc(v_Clockwise_258_);
return v_Clockwise_258_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg___boxed(lean_object* v_Clockwise_259_){
_start:
{
lean_object* v_res_260_; 
v_res_260_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___redArg(v_Clockwise_259_);
lean_dec(v_Clockwise_259_);
return v_res_260_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim(lean_object* v_motive_261_, uint8_t v_t_262_, lean_object* v_h_263_, lean_object* v_Clockwise_264_){
_start:
{
lean_inc(v_Clockwise_264_);
return v_Clockwise_264_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim___boxed(lean_object* v_motive_265_, lean_object* v_t_266_, lean_object* v_h_267_, lean_object* v_Clockwise_268_){
_start:
{
uint8_t v_t_boxed_269_; lean_object* v_res_270_; 
v_t_boxed_269_ = lean_unbox(v_t_266_);
v_res_270_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Clockwise_elim(v_motive_265_, v_t_boxed_269_, v_h_267_, v_Clockwise_268_);
lean_dec(v_Clockwise_268_);
return v_res_270_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg(lean_object* v_Counter_271_){
_start:
{
lean_inc(v_Counter_271_);
return v_Counter_271_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg___boxed(lean_object* v_Counter_272_){
_start:
{
lean_object* v_res_273_; 
v_res_273_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___redArg(v_Counter_272_);
lean_dec(v_Counter_272_);
return v_res_273_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim(lean_object* v_motive_274_, uint8_t v_t_275_, lean_object* v_h_276_, lean_object* v_Counter_277_){
_start:
{
lean_inc(v_Counter_277_);
return v_Counter_277_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim___boxed(lean_object* v_motive_278_, lean_object* v_t_279_, lean_object* v_h_280_, lean_object* v_Counter_281_){
_start:
{
uint8_t v_t_boxed_282_; lean_object* v_res_283_; 
v_t_boxed_282_ = lean_unbox(v_t_279_);
v_res_283_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_Counter_elim(v_motive_278_, v_t_boxed_282_, v_h_280_, v_Counter_281_);
lean_dec(v_Counter_281_);
return v_res_283_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat(lean_object* v_n_284_){
_start:
{
lean_object* v___x_285_; uint8_t v___x_286_; 
v___x_285_ = lean_unsigned_to_nat(0u);
v___x_286_ = lean_nat_dec_le(v_n_284_, v___x_285_);
if (v___x_286_ == 0)
{
lean_object* v___x_287_; uint8_t v___x_288_; 
v___x_287_ = lean_unsigned_to_nat(1u);
v___x_288_ = lean_nat_dec_le(v_n_284_, v___x_287_);
if (v___x_288_ == 0)
{
uint8_t v___x_289_; 
v___x_289_ = 2;
return v___x_289_;
}
else
{
uint8_t v___x_290_; 
v___x_290_ = 1;
return v___x_290_;
}
}
else
{
uint8_t v___x_291_; 
v___x_291_ = 0;
return v___x_291_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat___boxed(lean_object* v_n_292_){
_start:
{
uint8_t v_res_293_; lean_object* v_r_294_; 
v_res_293_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ofNat(v_n_292_);
lean_dec(v_n_292_);
v_r_294_ = lean_box(v_res_293_);
return v_r_294_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector(uint8_t v_x_295_, uint8_t v_y_296_){
_start:
{
lean_object* v___x_297_; lean_object* v___x_298_; uint8_t v___x_299_; 
v___x_297_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_x_295_);
v___x_298_ = lp_po023_NonAbelianGaugeSigns_PolyakovCenterSector_ctorIdx(v_y_296_);
v___x_299_ = lean_nat_dec_eq(v___x_297_, v___x_298_);
lean_dec(v___x_298_);
lean_dec(v___x_297_);
return v___x_299_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector___boxed(lean_object* v_x_300_, lean_object* v_y_301_){
_start:
{
uint8_t v_x_13__boxed_302_; uint8_t v_y_14__boxed_303_; uint8_t v_res_304_; lean_object* v_r_305_; 
v_x_13__boxed_302_ = lean_unbox(v_x_300_);
v_y_14__boxed_303_ = lean_unbox(v_y_301_);
v_res_304_ = lp_po023_NonAbelianGaugeSigns_instDecidableEqPolyakovCenterSector(v_x_13__boxed_302_, v_y_14__boxed_303_);
v_r_305_ = lean_box(v_res_304_);
return v_r_305_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr(uint8_t v_x_315_, lean_object* v_prec_316_){
_start:
{
lean_object* v___y_318_; lean_object* v___y_325_; lean_object* v___y_332_; 
switch(v_x_315_)
{
case 0:
{
lean_object* v___x_338_; uint8_t v___x_339_; 
v___x_338_ = lean_unsigned_to_nat(1024u);
v___x_339_ = lean_nat_dec_le(v___x_338_, v_prec_316_);
if (v___x_339_ == 0)
{
lean_object* v___x_340_; 
v___x_340_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_318_ = v___x_340_;
goto v___jp_317_;
}
else
{
lean_object* v___x_341_; 
v___x_341_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_318_ = v___x_341_;
goto v___jp_317_;
}
}
case 1:
{
lean_object* v___x_342_; uint8_t v___x_343_; 
v___x_342_ = lean_unsigned_to_nat(1024u);
v___x_343_ = lean_nat_dec_le(v___x_342_, v_prec_316_);
if (v___x_343_ == 0)
{
lean_object* v___x_344_; 
v___x_344_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_325_ = v___x_344_;
goto v___jp_324_;
}
else
{
lean_object* v___x_345_; 
v___x_345_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_325_ = v___x_345_;
goto v___jp_324_;
}
}
default: 
{
lean_object* v___x_346_; uint8_t v___x_347_; 
v___x_346_ = lean_unsigned_to_nat(1024u);
v___x_347_ = lean_nat_dec_le(v___x_346_, v_prec_316_);
if (v___x_347_ == 0)
{
lean_object* v___x_348_; 
v___x_348_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_332_ = v___x_348_;
goto v___jp_331_;
}
else
{
lean_object* v___x_349_; 
v___x_349_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_332_ = v___x_349_;
goto v___jp_331_;
}
}
}
v___jp_317_:
{
lean_object* v___x_319_; lean_object* v___x_320_; uint8_t v___x_321_; lean_object* v___x_322_; lean_object* v___x_323_; 
v___x_319_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__1));
lean_inc(v___y_318_);
v___x_320_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_320_, 0, v___y_318_);
lean_ctor_set(v___x_320_, 1, v___x_319_);
v___x_321_ = 0;
v___x_322_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_322_, 0, v___x_320_);
lean_ctor_set_uint8(v___x_322_, sizeof(void*)*1, v___x_321_);
v___x_323_ = l_Repr_addAppParen(v___x_322_, v_prec_316_);
return v___x_323_;
}
v___jp_324_:
{
lean_object* v___x_326_; lean_object* v___x_327_; uint8_t v___x_328_; lean_object* v___x_329_; lean_object* v___x_330_; 
v___x_326_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__3));
lean_inc(v___y_325_);
v___x_327_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_327_, 0, v___y_325_);
lean_ctor_set(v___x_327_, 1, v___x_326_);
v___x_328_ = 0;
v___x_329_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_329_, 0, v___x_327_);
lean_ctor_set_uint8(v___x_329_, sizeof(void*)*1, v___x_328_);
v___x_330_ = l_Repr_addAppParen(v___x_329_, v_prec_316_);
return v___x_330_;
}
v___jp_331_:
{
lean_object* v___x_333_; lean_object* v___x_334_; uint8_t v___x_335_; lean_object* v___x_336_; lean_object* v___x_337_; 
v___x_333_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___closed__5));
lean_inc(v___y_332_);
v___x_334_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_334_, 0, v___y_332_);
lean_ctor_set(v___x_334_, 1, v___x_333_);
v___x_335_ = 0;
v___x_336_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_336_, 0, v___x_334_);
lean_ctor_set_uint8(v___x_336_, sizeof(void*)*1, v___x_335_);
v___x_337_ = l_Repr_addAppParen(v___x_336_, v_prec_316_);
return v___x_337_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr___boxed(lean_object* v_x_350_, lean_object* v_prec_351_){
_start:
{
uint8_t v_x_173__boxed_352_; lean_object* v_res_353_; 
v_x_173__boxed_352_ = lean_unbox(v_x_350_);
v_res_353_ = lp_po023_NonAbelianGaugeSigns_instReprPolyakovCenterSector_repr(v_x_173__boxed_352_, v_prec_351_);
lean_dec(v_prec_351_);
return v_res_353_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(uint8_t v_x_356_){
_start:
{
if (v_x_356_ == 0)
{
lean_object* v___x_357_; 
v___x_357_ = lean_unsigned_to_nat(0u);
return v___x_357_;
}
else
{
lean_object* v___x_358_; 
v___x_358_ = lean_unsigned_to_nat(1u);
return v___x_358_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx___boxed(lean_object* v_x_359_){
_start:
{
uint8_t v_x_boxed_360_; lean_object* v_res_361_; 
v_x_boxed_360_ = lean_unbox(v_x_359_);
v_res_361_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_x_boxed_360_);
return v_res_361_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg(lean_object* v_k_362_){
_start:
{
lean_inc(v_k_362_);
return v_k_362_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg___boxed(lean_object* v_k_363_){
_start:
{
lean_object* v_res_364_; 
v_res_364_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___redArg(v_k_363_);
lean_dec(v_k_363_);
return v_res_364_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim(lean_object* v_motive_365_, lean_object* v_ctorIdx_366_, uint8_t v_t_367_, lean_object* v_h_368_, lean_object* v_k_369_){
_start:
{
lean_inc(v_k_369_);
return v_k_369_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim___boxed(lean_object* v_motive_370_, lean_object* v_ctorIdx_371_, lean_object* v_t_372_, lean_object* v_h_373_, lean_object* v_k_374_){
_start:
{
uint8_t v_t_boxed_375_; lean_object* v_res_376_; 
v_t_boxed_375_ = lean_unbox(v_t_372_);
v_res_376_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorElim(v_motive_370_, v_ctorIdx_371_, v_t_boxed_375_, v_h_373_, v_k_374_);
lean_dec(v_k_374_);
lean_dec(v_ctorIdx_371_);
return v_res_376_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg(lean_object* v_Fundamental_377_){
_start:
{
lean_inc(v_Fundamental_377_);
return v_Fundamental_377_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg___boxed(lean_object* v_Fundamental_378_){
_start:
{
lean_object* v_res_379_; 
v_res_379_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___redArg(v_Fundamental_378_);
lean_dec(v_Fundamental_378_);
return v_res_379_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim(lean_object* v_motive_380_, uint8_t v_t_381_, lean_object* v_h_382_, lean_object* v_Fundamental_383_){
_start:
{
lean_inc(v_Fundamental_383_);
return v_Fundamental_383_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim___boxed(lean_object* v_motive_384_, lean_object* v_t_385_, lean_object* v_h_386_, lean_object* v_Fundamental_387_){
_start:
{
uint8_t v_t_boxed_388_; lean_object* v_res_389_; 
v_t_boxed_388_ = lean_unbox(v_t_385_);
v_res_389_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Fundamental_elim(v_motive_384_, v_t_boxed_388_, v_h_386_, v_Fundamental_387_);
lean_dec(v_Fundamental_387_);
return v_res_389_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg(lean_object* v_Adjoint_390_){
_start:
{
lean_inc(v_Adjoint_390_);
return v_Adjoint_390_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg___boxed(lean_object* v_Adjoint_391_){
_start:
{
lean_object* v_res_392_; 
v_res_392_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___redArg(v_Adjoint_391_);
lean_dec(v_Adjoint_391_);
return v_res_392_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim(lean_object* v_motive_393_, uint8_t v_t_394_, lean_object* v_h_395_, lean_object* v_Adjoint_396_){
_start:
{
lean_inc(v_Adjoint_396_);
return v_Adjoint_396_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim___boxed(lean_object* v_motive_397_, lean_object* v_t_398_, lean_object* v_h_399_, lean_object* v_Adjoint_400_){
_start:
{
uint8_t v_t_boxed_401_; lean_object* v_res_402_; 
v_t_boxed_401_ = lean_unbox(v_t_398_);
v_res_402_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_Adjoint_elim(v_motive_397_, v_t_boxed_401_, v_h_399_, v_Adjoint_400_);
lean_dec(v_Adjoint_400_);
return v_res_402_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ofNat(lean_object* v_n_403_){
_start:
{
lean_object* v___x_404_; uint8_t v___x_405_; 
v___x_404_ = lean_unsigned_to_nat(0u);
v___x_405_ = lean_nat_dec_le(v_n_403_, v___x_404_);
if (v___x_405_ == 0)
{
uint8_t v___x_406_; 
v___x_406_ = 1;
return v___x_406_;
}
else
{
uint8_t v___x_407_; 
v___x_407_ = 0;
return v___x_407_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ofNat___boxed(lean_object* v_n_408_){
_start:
{
uint8_t v_res_409_; lean_object* v_r_410_; 
v_res_409_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ofNat(v_n_408_);
lean_dec(v_n_408_);
v_r_410_ = lean_box(v_res_409_);
return v_r_410_;
}
}
LEAN_EXPORT uint8_t lp_po023_NonAbelianGaugeSigns_instDecidableEqColorRepresentation(uint8_t v_x_411_, uint8_t v_y_412_){
_start:
{
lean_object* v___x_413_; lean_object* v___x_414_; uint8_t v___x_415_; 
v___x_413_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_x_411_);
v___x_414_ = lp_po023_NonAbelianGaugeSigns_ColorRepresentation_ctorIdx(v_y_412_);
v___x_415_ = lean_nat_dec_eq(v___x_413_, v___x_414_);
lean_dec(v___x_414_);
lean_dec(v___x_413_);
return v___x_415_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instDecidableEqColorRepresentation___boxed(lean_object* v_x_416_, lean_object* v_y_417_){
_start:
{
uint8_t v_x_13__boxed_418_; uint8_t v_y_14__boxed_419_; uint8_t v_res_420_; lean_object* v_r_421_; 
v_x_13__boxed_418_ = lean_unbox(v_x_416_);
v_y_14__boxed_419_ = lean_unbox(v_y_417_);
v_res_420_ = lp_po023_NonAbelianGaugeSigns_instDecidableEqColorRepresentation(v_x_13__boxed_418_, v_y_14__boxed_419_);
v_r_421_ = lean_box(v_res_420_);
return v_r_421_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr(uint8_t v_x_428_, lean_object* v_prec_429_){
_start:
{
lean_object* v___y_431_; lean_object* v___y_438_; 
if (v_x_428_ == 0)
{
lean_object* v___x_444_; uint8_t v___x_445_; 
v___x_444_ = lean_unsigned_to_nat(1024u);
v___x_445_ = lean_nat_dec_le(v___x_444_, v_prec_429_);
if (v___x_445_ == 0)
{
lean_object* v___x_446_; 
v___x_446_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_431_ = v___x_446_;
goto v___jp_430_;
}
else
{
lean_object* v___x_447_; 
v___x_447_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_431_ = v___x_447_;
goto v___jp_430_;
}
}
else
{
lean_object* v___x_448_; uint8_t v___x_449_; 
v___x_448_ = lean_unsigned_to_nat(1024u);
v___x_449_ = lean_nat_dec_le(v___x_448_, v_prec_429_);
if (v___x_449_ == 0)
{
lean_object* v___x_450_; 
v___x_450_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__4);
v___y_438_ = v___x_450_;
goto v___jp_437_;
}
else
{
lean_object* v___x_451_; 
v___x_451_ = lean_obj_once(&lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5, &lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5_once, _init_lp_po023_NonAbelianGaugeSigns_instReprSu2FluxSector_repr___closed__5);
v___y_438_ = v___x_451_;
goto v___jp_437_;
}
}
v___jp_430_:
{
lean_object* v___x_432_; lean_object* v___x_433_; uint8_t v___x_434_; lean_object* v___x_435_; lean_object* v___x_436_; 
v___x_432_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__1));
lean_inc(v___y_431_);
v___x_433_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_433_, 0, v___y_431_);
lean_ctor_set(v___x_433_, 1, v___x_432_);
v___x_434_ = 0;
v___x_435_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_435_, 0, v___x_433_);
lean_ctor_set_uint8(v___x_435_, sizeof(void*)*1, v___x_434_);
v___x_436_ = l_Repr_addAppParen(v___x_435_, v_prec_429_);
return v___x_436_;
}
v___jp_437_:
{
lean_object* v___x_439_; lean_object* v___x_440_; uint8_t v___x_441_; lean_object* v___x_442_; lean_object* v___x_443_; 
v___x_439_ = ((lean_object*)(lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___closed__3));
lean_inc(v___y_438_);
v___x_440_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_440_, 0, v___y_438_);
lean_ctor_set(v___x_440_, 1, v___x_439_);
v___x_441_ = 0;
v___x_442_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_442_, 0, v___x_440_);
lean_ctor_set_uint8(v___x_442_, sizeof(void*)*1, v___x_441_);
v___x_443_ = l_Repr_addAppParen(v___x_442_, v_prec_429_);
return v___x_443_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr___boxed(lean_object* v_x_452_, lean_object* v_prec_453_){
_start:
{
uint8_t v_x_117__boxed_454_; lean_object* v_res_455_; 
v_x_117__boxed_454_ = lean_unbox(v_x_452_);
v_res_455_ = lp_po023_NonAbelianGaugeSigns_instReprColorRepresentation_repr(v_x_117__boxed_454_, v_prec_453_);
lean_dec(v_prec_453_);
return v_res_455_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_n__ality(lean_object* v_N__c_458_, uint8_t v_x_459_){
_start:
{
if (v_x_459_ == 0)
{
lean_object* v___x_460_; lean_object* v___x_461_; 
v___x_460_ = lean_unsigned_to_nat(1u);
v___x_461_ = lean_nat_mod(v___x_460_, v_N__c_458_);
return v___x_461_;
}
else
{
lean_object* v___x_462_; 
v___x_462_ = lean_unsigned_to_nat(0u);
return v___x_462_;
}
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_n__ality___boxed(lean_object* v_N__c_463_, lean_object* v_x_464_){
_start:
{
uint8_t v_x_37__boxed_465_; lean_object* v_res_466_; 
v_x_37__boxed_465_ = lean_unbox(v_x_464_);
v_res_466_ = lp_po023_NonAbelianGaugeSigns_n__ality(v_N__c_463_, v_x_37__boxed_465_);
lean_dec(v_N__c_463_);
return v_res_466_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_fluxTubeCurvature(lean_object* v_N__c_467_, uint8_t v_rep_468_){
_start:
{
lean_object* v___x_469_; 
v___x_469_ = lp_po023_NonAbelianGaugeSigns_n__ality(v_N__c_467_, v_rep_468_);
return v___x_469_;
}
}
LEAN_EXPORT lean_object* lp_po023_NonAbelianGaugeSigns_fluxTubeCurvature___boxed(lean_object* v_N__c_470_, lean_object* v_rep_471_){
_start:
{
uint8_t v_rep_boxed_472_; lean_object* v_res_473_; 
v_rep_boxed_472_ = lean_unbox(v_rep_471_);
v_res_473_ = lp_po023_NonAbelianGaugeSigns_fluxTubeCurvature(v_N__c_470_, v_rep_boxed_472_);
lean_dec(v_N__c_470_);
return v_res_473_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
void lean_initialize_runtime_module();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_po023_NonAbelianGaugeSigns(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize_runtime_module();
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
