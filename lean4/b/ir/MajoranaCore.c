// Lean compiler output
// Module: MajoranaCore
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* l_List_finRange(lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_f2__add(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_f2__add___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_f2__mul(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_f2__mul___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_F2Vec_zero(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_zero___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_F2Vec_add___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_add___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_F2Vec_add(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_add___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00F2Vec_weight_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_weight(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_TrichotomyClass_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqTrichotomyClass(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqTrichotomyClass___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 22, .m_capacity = 22, .m_length = 21, .m_data = "TrichotomyClass.Exact"};
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 31, .m_capacity = 31, .m_length = 30, .m_data = "TrichotomyClass.ClosedResidual"};
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 32, .m_capacity = 32, .m_length = 31, .m_data = "TrichotomyClass.OpenObstruction"};
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__5_value;
static lean_once_cell_t lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6;
static lean_once_cell_t lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_instReprTrichotomyClass___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_instReprTrichotomyClass_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_instReprTrichotomyClass___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_instReprTrichotomyClass = (const lean_object*)&lp_FiniteQuantum_instReprTrichotomyClass___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_gaussian__elimination__ops(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_gaussian__elimination__ops___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_IsingAnyon_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqIsingAnyon(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqIsingAnyon___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_instReprIsingAnyon_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "IsingAnyon.One"};
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_instReprIsingAnyon_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_instReprIsingAnyon_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "IsingAnyon.Sigma"};
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_instReprIsingAnyon_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_instReprIsingAnyon_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "IsingAnyon.Psi"};
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_instReprIsingAnyon_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_instReprIsingAnyon___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_instReprIsingAnyon_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_instReprIsingAnyon___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_instReprIsingAnyon = (const lean_object*)&lp_FiniteQuantum_instReprIsingAnyon___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_ising__quantum__dim__sq(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ising__quantum__dim__sq___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_SurfaceTopology_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqSurfaceTopology(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqSurfaceTopology___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 21, .m_capacity = 21, .m_length = 20, .m_data = "SurfaceTopology.Disk"};
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 25, .m_capacity = 25, .m_length = 24, .m_data = "SurfaceTopology.Cylinder"};
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 22, .m_capacity = 22, .m_length = 21, .m_data = "SurfaceTopology.Torus"};
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_instReprSurfaceTopology___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_instReprSurfaceTopology_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_instReprSurfaceTopology___closed__0 = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_instReprSurfaceTopology = (const lean_object*)&lp_FiniteQuantum_instReprSurfaceTopology___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_betti1__of__topology(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_betti1__of__topology___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_toric__distance(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_toric__distance___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_coset__weight__upper__bound___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_coset__weight__upper__bound(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_coset__weight__upper__bound___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_f2__add(uint8_t v_a_1_, uint8_t v_b_2_){
_start:
{
if (v_a_1_ == 0)
{
return v_b_2_;
}
else
{
if (v_b_2_ == 0)
{
return v_a_1_;
}
else
{
uint8_t v___x_3_; 
v___x_3_ = 0;
return v___x_3_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_f2__add___boxed(lean_object* v_a_4_, lean_object* v_b_5_){
_start:
{
uint8_t v_a_boxed_6_; uint8_t v_b_boxed_7_; uint8_t v_res_8_; lean_object* v_r_9_; 
v_a_boxed_6_ = lean_unbox(v_a_4_);
v_b_boxed_7_ = lean_unbox(v_b_5_);
v_res_8_ = lp_FiniteQuantum_f2__add(v_a_boxed_6_, v_b_boxed_7_);
v_r_9_ = lean_box(v_res_8_);
return v_r_9_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_f2__mul(uint8_t v_a_10_, uint8_t v_b_11_){
_start:
{
if (v_a_10_ == 0)
{
return v_a_10_;
}
else
{
return v_b_11_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_f2__mul___boxed(lean_object* v_a_12_, lean_object* v_b_13_){
_start:
{
uint8_t v_a_boxed_14_; uint8_t v_b_boxed_15_; uint8_t v_res_16_; lean_object* v_r_17_; 
v_a_boxed_14_ = lean_unbox(v_a_12_);
v_b_boxed_15_ = lean_unbox(v_b_13_);
v_res_16_ = lp_FiniteQuantum_f2__mul(v_a_boxed_14_, v_b_boxed_15_);
v_r_17_ = lean_box(v_res_16_);
return v_r_17_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_F2Vec_zero(lean_object* v_n_18_, lean_object* v_x_19_){
_start:
{
uint8_t v___x_20_; 
v___x_20_ = 0;
return v___x_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_zero___boxed(lean_object* v_n_21_, lean_object* v_x_22_){
_start:
{
uint8_t v_res_23_; lean_object* v_r_24_; 
v_res_23_ = lp_FiniteQuantum_F2Vec_zero(v_n_21_, v_x_22_);
lean_dec(v_x_22_);
lean_dec(v_n_21_);
v_r_24_ = lean_box(v_res_23_);
return v_r_24_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_F2Vec_add___redArg(lean_object* v_v1_25_, lean_object* v_v2_26_, lean_object* v_i_27_){
_start:
{
lean_object* v___x_28_; lean_object* v___x_29_; uint8_t v___x_30_; uint8_t v___x_31_; uint8_t v___x_32_; 
lean_inc(v_i_27_);
v___x_28_ = lean_apply_1(v_v1_25_, v_i_27_);
v___x_29_ = lean_apply_1(v_v2_26_, v_i_27_);
v___x_30_ = lean_unbox(v___x_28_);
v___x_31_ = lean_unbox(v___x_29_);
v___x_32_ = lp_FiniteQuantum_f2__add(v___x_30_, v___x_31_);
return v___x_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_add___redArg___boxed(lean_object* v_v1_33_, lean_object* v_v2_34_, lean_object* v_i_35_){
_start:
{
uint8_t v_res_36_; lean_object* v_r_37_; 
v_res_36_ = lp_FiniteQuantum_F2Vec_add___redArg(v_v1_33_, v_v2_34_, v_i_35_);
v_r_37_ = lean_box(v_res_36_);
return v_r_37_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_F2Vec_add(lean_object* v_n_38_, lean_object* v_v1_39_, lean_object* v_v2_40_, lean_object* v_i_41_){
_start:
{
uint8_t v___x_42_; 
v___x_42_ = lp_FiniteQuantum_F2Vec_add___redArg(v_v1_39_, v_v2_40_, v_i_41_);
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_add___boxed(lean_object* v_n_43_, lean_object* v_v1_44_, lean_object* v_v2_45_, lean_object* v_i_46_){
_start:
{
uint8_t v_res_47_; lean_object* v_r_48_; 
v_res_47_ = lp_FiniteQuantum_F2Vec_add(v_n_43_, v_v1_44_, v_v2_45_, v_i_46_);
lean_dec(v_n_43_);
v_r_48_ = lean_box(v_res_47_);
return v_r_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00F2Vec_weight_spec__0(lean_object* v_v_49_, lean_object* v_x_50_, lean_object* v_x_51_){
_start:
{
if (lean_obj_tag(v_x_51_) == 0)
{
lean_dec_ref(v_v_49_);
return v_x_50_;
}
else
{
lean_object* v_head_52_; lean_object* v_tail_53_; lean_object* v___x_54_; uint8_t v___x_55_; 
v_head_52_ = lean_ctor_get(v_x_51_, 0);
lean_inc(v_head_52_);
v_tail_53_ = lean_ctor_get(v_x_51_, 1);
lean_inc(v_tail_53_);
lean_dec_ref_known(v_x_51_, 2);
lean_inc_ref(v_v_49_);
v___x_54_ = lean_apply_1(v_v_49_, v_head_52_);
v___x_55_ = lean_unbox(v___x_54_);
if (v___x_55_ == 0)
{
v_x_51_ = v_tail_53_;
goto _start;
}
else
{
lean_object* v___x_57_; lean_object* v___x_58_; 
v___x_57_ = lean_unsigned_to_nat(1u);
v___x_58_ = lean_nat_add(v_x_50_, v___x_57_);
lean_dec(v_x_50_);
v_x_50_ = v___x_58_;
v_x_51_ = v_tail_53_;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_F2Vec_weight(lean_object* v_n_60_, lean_object* v_v_61_){
_start:
{
lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; 
v___x_62_ = lean_unsigned_to_nat(0u);
v___x_63_ = l_List_finRange(v_n_60_);
v___x_64_ = lp_FiniteQuantum_List_foldl___at___00F2Vec_weight_spec__0(v_v_61_, v___x_62_, v___x_63_);
return v___x_64_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorIdx(uint8_t v_x_65_){
_start:
{
switch(v_x_65_)
{
case 0:
{
lean_object* v___x_66_; 
v___x_66_ = lean_unsigned_to_nat(0u);
return v___x_66_;
}
case 1:
{
lean_object* v___x_67_; 
v___x_67_ = lean_unsigned_to_nat(1u);
return v___x_67_;
}
default: 
{
lean_object* v___x_68_; 
v___x_68_ = lean_unsigned_to_nat(2u);
return v___x_68_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorIdx___boxed(lean_object* v_x_69_){
_start:
{
uint8_t v_x_boxed_70_; lean_object* v_res_71_; 
v_x_boxed_70_ = lean_unbox(v_x_69_);
v_res_71_ = lp_FiniteQuantum_TrichotomyClass_ctorIdx(v_x_boxed_70_);
return v_res_71_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_toCtorIdx(uint8_t v_x_72_){
_start:
{
lean_object* v___x_73_; 
v___x_73_ = lp_FiniteQuantum_TrichotomyClass_ctorIdx(v_x_72_);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_toCtorIdx___boxed(lean_object* v_x_74_){
_start:
{
uint8_t v_x_4__boxed_75_; lean_object* v_res_76_; 
v_x_4__boxed_75_ = lean_unbox(v_x_74_);
v_res_76_ = lp_FiniteQuantum_TrichotomyClass_toCtorIdx(v_x_4__boxed_75_);
return v_res_76_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim___redArg(lean_object* v_k_77_){
_start:
{
lean_inc(v_k_77_);
return v_k_77_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim___redArg___boxed(lean_object* v_k_78_){
_start:
{
lean_object* v_res_79_; 
v_res_79_ = lp_FiniteQuantum_TrichotomyClass_ctorElim___redArg(v_k_78_);
lean_dec(v_k_78_);
return v_res_79_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim(lean_object* v_motive_80_, lean_object* v_ctorIdx_81_, uint8_t v_t_82_, lean_object* v_h_83_, lean_object* v_k_84_){
_start:
{
lean_inc(v_k_84_);
return v_k_84_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ctorElim___boxed(lean_object* v_motive_85_, lean_object* v_ctorIdx_86_, lean_object* v_t_87_, lean_object* v_h_88_, lean_object* v_k_89_){
_start:
{
uint8_t v_t_boxed_90_; lean_object* v_res_91_; 
v_t_boxed_90_ = lean_unbox(v_t_87_);
v_res_91_ = lp_FiniteQuantum_TrichotomyClass_ctorElim(v_motive_85_, v_ctorIdx_86_, v_t_boxed_90_, v_h_88_, v_k_89_);
lean_dec(v_k_89_);
lean_dec(v_ctorIdx_86_);
return v_res_91_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim___redArg(lean_object* v_Exact_92_){
_start:
{
lean_inc(v_Exact_92_);
return v_Exact_92_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim___redArg___boxed(lean_object* v_Exact_93_){
_start:
{
lean_object* v_res_94_; 
v_res_94_ = lp_FiniteQuantum_TrichotomyClass_Exact_elim___redArg(v_Exact_93_);
lean_dec(v_Exact_93_);
return v_res_94_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim(lean_object* v_motive_95_, uint8_t v_t_96_, lean_object* v_h_97_, lean_object* v_Exact_98_){
_start:
{
lean_inc(v_Exact_98_);
return v_Exact_98_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_Exact_elim___boxed(lean_object* v_motive_99_, lean_object* v_t_100_, lean_object* v_h_101_, lean_object* v_Exact_102_){
_start:
{
uint8_t v_t_boxed_103_; lean_object* v_res_104_; 
v_t_boxed_103_ = lean_unbox(v_t_100_);
v_res_104_ = lp_FiniteQuantum_TrichotomyClass_Exact_elim(v_motive_99_, v_t_boxed_103_, v_h_101_, v_Exact_102_);
lean_dec(v_Exact_102_);
return v_res_104_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___redArg(lean_object* v_ClosedResidual_105_){
_start:
{
lean_inc(v_ClosedResidual_105_);
return v_ClosedResidual_105_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___redArg___boxed(lean_object* v_ClosedResidual_106_){
_start:
{
lean_object* v_res_107_; 
v_res_107_ = lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___redArg(v_ClosedResidual_106_);
lean_dec(v_ClosedResidual_106_);
return v_res_107_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim(lean_object* v_motive_108_, uint8_t v_t_109_, lean_object* v_h_110_, lean_object* v_ClosedResidual_111_){
_start:
{
lean_inc(v_ClosedResidual_111_);
return v_ClosedResidual_111_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim___boxed(lean_object* v_motive_112_, lean_object* v_t_113_, lean_object* v_h_114_, lean_object* v_ClosedResidual_115_){
_start:
{
uint8_t v_t_boxed_116_; lean_object* v_res_117_; 
v_t_boxed_116_ = lean_unbox(v_t_113_);
v_res_117_ = lp_FiniteQuantum_TrichotomyClass_ClosedResidual_elim(v_motive_112_, v_t_boxed_116_, v_h_114_, v_ClosedResidual_115_);
lean_dec(v_ClosedResidual_115_);
return v_res_117_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___redArg(lean_object* v_OpenObstruction_118_){
_start:
{
lean_inc(v_OpenObstruction_118_);
return v_OpenObstruction_118_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___redArg___boxed(lean_object* v_OpenObstruction_119_){
_start:
{
lean_object* v_res_120_; 
v_res_120_ = lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___redArg(v_OpenObstruction_119_);
lean_dec(v_OpenObstruction_119_);
return v_res_120_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim(lean_object* v_motive_121_, uint8_t v_t_122_, lean_object* v_h_123_, lean_object* v_OpenObstruction_124_){
_start:
{
lean_inc(v_OpenObstruction_124_);
return v_OpenObstruction_124_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim___boxed(lean_object* v_motive_125_, lean_object* v_t_126_, lean_object* v_h_127_, lean_object* v_OpenObstruction_128_){
_start:
{
uint8_t v_t_boxed_129_; lean_object* v_res_130_; 
v_t_boxed_129_ = lean_unbox(v_t_126_);
v_res_130_ = lp_FiniteQuantum_TrichotomyClass_OpenObstruction_elim(v_motive_125_, v_t_boxed_129_, v_h_127_, v_OpenObstruction_128_);
lean_dec(v_OpenObstruction_128_);
return v_res_130_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_TrichotomyClass_ofNat(lean_object* v_n_131_){
_start:
{
lean_object* v___x_132_; uint8_t v___x_133_; 
v___x_132_ = lean_unsigned_to_nat(0u);
v___x_133_ = lean_nat_dec_le(v_n_131_, v___x_132_);
if (v___x_133_ == 0)
{
lean_object* v___x_134_; uint8_t v___x_135_; 
v___x_134_ = lean_unsigned_to_nat(1u);
v___x_135_ = lean_nat_dec_le(v_n_131_, v___x_134_);
if (v___x_135_ == 0)
{
uint8_t v___x_136_; 
v___x_136_ = 2;
return v___x_136_;
}
else
{
uint8_t v___x_137_; 
v___x_137_ = 1;
return v___x_137_;
}
}
else
{
uint8_t v___x_138_; 
v___x_138_ = 0;
return v___x_138_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TrichotomyClass_ofNat___boxed(lean_object* v_n_139_){
_start:
{
uint8_t v_res_140_; lean_object* v_r_141_; 
v_res_140_ = lp_FiniteQuantum_TrichotomyClass_ofNat(v_n_139_);
lean_dec(v_n_139_);
v_r_141_ = lean_box(v_res_140_);
return v_r_141_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqTrichotomyClass(uint8_t v_x_142_, uint8_t v_y_143_){
_start:
{
lean_object* v___x_144_; lean_object* v___x_145_; uint8_t v___x_146_; 
v___x_144_ = lp_FiniteQuantum_TrichotomyClass_ctorIdx(v_x_142_);
v___x_145_ = lp_FiniteQuantum_TrichotomyClass_ctorIdx(v_y_143_);
v___x_146_ = lean_nat_dec_eq(v___x_144_, v___x_145_);
lean_dec(v___x_145_);
lean_dec(v___x_144_);
return v___x_146_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqTrichotomyClass___boxed(lean_object* v_x_147_, lean_object* v_y_148_){
_start:
{
uint8_t v_x_13__boxed_149_; uint8_t v_y_14__boxed_150_; uint8_t v_res_151_; lean_object* v_r_152_; 
v_x_13__boxed_149_ = lean_unbox(v_x_147_);
v_y_14__boxed_150_ = lean_unbox(v_y_148_);
v_res_151_ = lp_FiniteQuantum_instDecidableEqTrichotomyClass(v_x_13__boxed_149_, v_y_14__boxed_150_);
v_r_152_ = lean_box(v_res_151_);
return v_r_152_;
}
}
static lean_object* _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6(void){
_start:
{
lean_object* v___x_162_; lean_object* v___x_163_; 
v___x_162_ = lean_unsigned_to_nat(2u);
v___x_163_ = lean_nat_to_int(v___x_162_);
return v___x_163_;
}
}
static lean_object* _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7(void){
_start:
{
lean_object* v___x_164_; lean_object* v___x_165_; 
v___x_164_ = lean_unsigned_to_nat(1u);
v___x_165_ = lean_nat_to_int(v___x_164_);
return v___x_165_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr(uint8_t v_x_166_, lean_object* v_prec_167_){
_start:
{
lean_object* v___y_169_; lean_object* v___y_176_; lean_object* v___y_183_; 
switch(v_x_166_)
{
case 0:
{
lean_object* v___x_189_; uint8_t v___x_190_; 
v___x_189_ = lean_unsigned_to_nat(1024u);
v___x_190_ = lean_nat_dec_le(v___x_189_, v_prec_167_);
if (v___x_190_ == 0)
{
lean_object* v___x_191_; 
v___x_191_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_169_ = v___x_191_;
goto v___jp_168_;
}
else
{
lean_object* v___x_192_; 
v___x_192_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_169_ = v___x_192_;
goto v___jp_168_;
}
}
case 1:
{
lean_object* v___x_193_; uint8_t v___x_194_; 
v___x_193_ = lean_unsigned_to_nat(1024u);
v___x_194_ = lean_nat_dec_le(v___x_193_, v_prec_167_);
if (v___x_194_ == 0)
{
lean_object* v___x_195_; 
v___x_195_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_176_ = v___x_195_;
goto v___jp_175_;
}
else
{
lean_object* v___x_196_; 
v___x_196_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_176_ = v___x_196_;
goto v___jp_175_;
}
}
default: 
{
lean_object* v___x_197_; uint8_t v___x_198_; 
v___x_197_ = lean_unsigned_to_nat(1024u);
v___x_198_ = lean_nat_dec_le(v___x_197_, v_prec_167_);
if (v___x_198_ == 0)
{
lean_object* v___x_199_; 
v___x_199_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_183_ = v___x_199_;
goto v___jp_182_;
}
else
{
lean_object* v___x_200_; 
v___x_200_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_183_ = v___x_200_;
goto v___jp_182_;
}
}
}
v___jp_168_:
{
lean_object* v___x_170_; lean_object* v___x_171_; uint8_t v___x_172_; lean_object* v___x_173_; lean_object* v___x_174_; 
v___x_170_ = ((lean_object*)(lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__1));
lean_inc(v___y_169_);
v___x_171_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_171_, 0, v___y_169_);
lean_ctor_set(v___x_171_, 1, v___x_170_);
v___x_172_ = 0;
v___x_173_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_173_, 0, v___x_171_);
lean_ctor_set_uint8(v___x_173_, sizeof(void*)*1, v___x_172_);
v___x_174_ = l_Repr_addAppParen(v___x_173_, v_prec_167_);
return v___x_174_;
}
v___jp_175_:
{
lean_object* v___x_177_; lean_object* v___x_178_; uint8_t v___x_179_; lean_object* v___x_180_; lean_object* v___x_181_; 
v___x_177_ = ((lean_object*)(lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__3));
lean_inc(v___y_176_);
v___x_178_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_178_, 0, v___y_176_);
lean_ctor_set(v___x_178_, 1, v___x_177_);
v___x_179_ = 0;
v___x_180_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_180_, 0, v___x_178_);
lean_ctor_set_uint8(v___x_180_, sizeof(void*)*1, v___x_179_);
v___x_181_ = l_Repr_addAppParen(v___x_180_, v_prec_167_);
return v___x_181_;
}
v___jp_182_:
{
lean_object* v___x_184_; lean_object* v___x_185_; uint8_t v___x_186_; lean_object* v___x_187_; lean_object* v___x_188_; 
v___x_184_ = ((lean_object*)(lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__5));
lean_inc(v___y_183_);
v___x_185_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_185_, 0, v___y_183_);
lean_ctor_set(v___x_185_, 1, v___x_184_);
v___x_186_ = 0;
v___x_187_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_187_, 0, v___x_185_);
lean_ctor_set_uint8(v___x_187_, sizeof(void*)*1, v___x_186_);
v___x_188_ = l_Repr_addAppParen(v___x_187_, v_prec_167_);
return v___x_188_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprTrichotomyClass_repr___boxed(lean_object* v_x_201_, lean_object* v_prec_202_){
_start:
{
uint8_t v_x_177__boxed_203_; lean_object* v_res_204_; 
v_x_177__boxed_203_ = lean_unbox(v_x_201_);
v_res_204_ = lp_FiniteQuantum_instReprTrichotomyClass_repr(v_x_177__boxed_203_, v_prec_202_);
lean_dec(v_prec_202_);
return v_res_204_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_gaussian__elimination__ops(lean_object* v_n_207_){
_start:
{
lean_object* v___x_208_; lean_object* v___x_209_; 
v___x_208_ = lean_nat_mul(v_n_207_, v_n_207_);
v___x_209_ = lean_nat_mul(v___x_208_, v_n_207_);
lean_dec(v___x_208_);
return v___x_209_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_gaussian__elimination__ops___boxed(lean_object* v_n_210_){
_start:
{
lean_object* v_res_211_; 
v_res_211_ = lp_FiniteQuantum_gaussian__elimination__ops(v_n_210_);
lean_dec(v_n_210_);
return v_res_211_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorIdx(uint8_t v_x_212_){
_start:
{
switch(v_x_212_)
{
case 0:
{
lean_object* v___x_213_; 
v___x_213_ = lean_unsigned_to_nat(0u);
return v___x_213_;
}
case 1:
{
lean_object* v___x_214_; 
v___x_214_ = lean_unsigned_to_nat(1u);
return v___x_214_;
}
default: 
{
lean_object* v___x_215_; 
v___x_215_ = lean_unsigned_to_nat(2u);
return v___x_215_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorIdx___boxed(lean_object* v_x_216_){
_start:
{
uint8_t v_x_boxed_217_; lean_object* v_res_218_; 
v_x_boxed_217_ = lean_unbox(v_x_216_);
v_res_218_ = lp_FiniteQuantum_IsingAnyon_ctorIdx(v_x_boxed_217_);
return v_res_218_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_toCtorIdx(uint8_t v_x_219_){
_start:
{
lean_object* v___x_220_; 
v___x_220_ = lp_FiniteQuantum_IsingAnyon_ctorIdx(v_x_219_);
return v___x_220_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_toCtorIdx___boxed(lean_object* v_x_221_){
_start:
{
uint8_t v_x_4__boxed_222_; lean_object* v_res_223_; 
v_x_4__boxed_222_ = lean_unbox(v_x_221_);
v_res_223_ = lp_FiniteQuantum_IsingAnyon_toCtorIdx(v_x_4__boxed_222_);
return v_res_223_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim___redArg(lean_object* v_k_224_){
_start:
{
lean_inc(v_k_224_);
return v_k_224_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim___redArg___boxed(lean_object* v_k_225_){
_start:
{
lean_object* v_res_226_; 
v_res_226_ = lp_FiniteQuantum_IsingAnyon_ctorElim___redArg(v_k_225_);
lean_dec(v_k_225_);
return v_res_226_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim(lean_object* v_motive_227_, lean_object* v_ctorIdx_228_, uint8_t v_t_229_, lean_object* v_h_230_, lean_object* v_k_231_){
_start:
{
lean_inc(v_k_231_);
return v_k_231_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ctorElim___boxed(lean_object* v_motive_232_, lean_object* v_ctorIdx_233_, lean_object* v_t_234_, lean_object* v_h_235_, lean_object* v_k_236_){
_start:
{
uint8_t v_t_boxed_237_; lean_object* v_res_238_; 
v_t_boxed_237_ = lean_unbox(v_t_234_);
v_res_238_ = lp_FiniteQuantum_IsingAnyon_ctorElim(v_motive_232_, v_ctorIdx_233_, v_t_boxed_237_, v_h_235_, v_k_236_);
lean_dec(v_k_236_);
lean_dec(v_ctorIdx_233_);
return v_res_238_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim___redArg(lean_object* v_One_239_){
_start:
{
lean_inc(v_One_239_);
return v_One_239_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim___redArg___boxed(lean_object* v_One_240_){
_start:
{
lean_object* v_res_241_; 
v_res_241_ = lp_FiniteQuantum_IsingAnyon_One_elim___redArg(v_One_240_);
lean_dec(v_One_240_);
return v_res_241_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim(lean_object* v_motive_242_, uint8_t v_t_243_, lean_object* v_h_244_, lean_object* v_One_245_){
_start:
{
lean_inc(v_One_245_);
return v_One_245_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_One_elim___boxed(lean_object* v_motive_246_, lean_object* v_t_247_, lean_object* v_h_248_, lean_object* v_One_249_){
_start:
{
uint8_t v_t_boxed_250_; lean_object* v_res_251_; 
v_t_boxed_250_ = lean_unbox(v_t_247_);
v_res_251_ = lp_FiniteQuantum_IsingAnyon_One_elim(v_motive_246_, v_t_boxed_250_, v_h_248_, v_One_249_);
lean_dec(v_One_249_);
return v_res_251_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim___redArg(lean_object* v_Sigma_252_){
_start:
{
lean_inc(v_Sigma_252_);
return v_Sigma_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim___redArg___boxed(lean_object* v_Sigma_253_){
_start:
{
lean_object* v_res_254_; 
v_res_254_ = lp_FiniteQuantum_IsingAnyon_Sigma_elim___redArg(v_Sigma_253_);
lean_dec(v_Sigma_253_);
return v_res_254_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim(lean_object* v_motive_255_, uint8_t v_t_256_, lean_object* v_h_257_, lean_object* v_Sigma_258_){
_start:
{
lean_inc(v_Sigma_258_);
return v_Sigma_258_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Sigma_elim___boxed(lean_object* v_motive_259_, lean_object* v_t_260_, lean_object* v_h_261_, lean_object* v_Sigma_262_){
_start:
{
uint8_t v_t_boxed_263_; lean_object* v_res_264_; 
v_t_boxed_263_ = lean_unbox(v_t_260_);
v_res_264_ = lp_FiniteQuantum_IsingAnyon_Sigma_elim(v_motive_259_, v_t_boxed_263_, v_h_261_, v_Sigma_262_);
lean_dec(v_Sigma_262_);
return v_res_264_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim___redArg(lean_object* v_Psi_265_){
_start:
{
lean_inc(v_Psi_265_);
return v_Psi_265_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim___redArg___boxed(lean_object* v_Psi_266_){
_start:
{
lean_object* v_res_267_; 
v_res_267_ = lp_FiniteQuantum_IsingAnyon_Psi_elim___redArg(v_Psi_266_);
lean_dec(v_Psi_266_);
return v_res_267_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim(lean_object* v_motive_268_, uint8_t v_t_269_, lean_object* v_h_270_, lean_object* v_Psi_271_){
_start:
{
lean_inc(v_Psi_271_);
return v_Psi_271_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_Psi_elim___boxed(lean_object* v_motive_272_, lean_object* v_t_273_, lean_object* v_h_274_, lean_object* v_Psi_275_){
_start:
{
uint8_t v_t_boxed_276_; lean_object* v_res_277_; 
v_t_boxed_276_ = lean_unbox(v_t_273_);
v_res_277_ = lp_FiniteQuantum_IsingAnyon_Psi_elim(v_motive_272_, v_t_boxed_276_, v_h_274_, v_Psi_275_);
lean_dec(v_Psi_275_);
return v_res_277_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_IsingAnyon_ofNat(lean_object* v_n_278_){
_start:
{
lean_object* v___x_279_; uint8_t v___x_280_; 
v___x_279_ = lean_unsigned_to_nat(0u);
v___x_280_ = lean_nat_dec_le(v_n_278_, v___x_279_);
if (v___x_280_ == 0)
{
lean_object* v___x_281_; uint8_t v___x_282_; 
v___x_281_ = lean_unsigned_to_nat(1u);
v___x_282_ = lean_nat_dec_le(v_n_278_, v___x_281_);
if (v___x_282_ == 0)
{
uint8_t v___x_283_; 
v___x_283_ = 2;
return v___x_283_;
}
else
{
uint8_t v___x_284_; 
v___x_284_ = 1;
return v___x_284_;
}
}
else
{
uint8_t v___x_285_; 
v___x_285_ = 0;
return v___x_285_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_IsingAnyon_ofNat___boxed(lean_object* v_n_286_){
_start:
{
uint8_t v_res_287_; lean_object* v_r_288_; 
v_res_287_ = lp_FiniteQuantum_IsingAnyon_ofNat(v_n_286_);
lean_dec(v_n_286_);
v_r_288_ = lean_box(v_res_287_);
return v_r_288_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqIsingAnyon(uint8_t v_x_289_, uint8_t v_y_290_){
_start:
{
lean_object* v___x_291_; lean_object* v___x_292_; uint8_t v___x_293_; 
v___x_291_ = lp_FiniteQuantum_IsingAnyon_ctorIdx(v_x_289_);
v___x_292_ = lp_FiniteQuantum_IsingAnyon_ctorIdx(v_y_290_);
v___x_293_ = lean_nat_dec_eq(v___x_291_, v___x_292_);
lean_dec(v___x_292_);
lean_dec(v___x_291_);
return v___x_293_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqIsingAnyon___boxed(lean_object* v_x_294_, lean_object* v_y_295_){
_start:
{
uint8_t v_x_13__boxed_296_; uint8_t v_y_14__boxed_297_; uint8_t v_res_298_; lean_object* v_r_299_; 
v_x_13__boxed_296_ = lean_unbox(v_x_294_);
v_y_14__boxed_297_ = lean_unbox(v_y_295_);
v_res_298_ = lp_FiniteQuantum_instDecidableEqIsingAnyon(v_x_13__boxed_296_, v_y_14__boxed_297_);
v_r_299_ = lean_box(v_res_298_);
return v_r_299_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr(uint8_t v_x_309_, lean_object* v_prec_310_){
_start:
{
lean_object* v___y_312_; lean_object* v___y_319_; lean_object* v___y_326_; 
switch(v_x_309_)
{
case 0:
{
lean_object* v___x_332_; uint8_t v___x_333_; 
v___x_332_ = lean_unsigned_to_nat(1024u);
v___x_333_ = lean_nat_dec_le(v___x_332_, v_prec_310_);
if (v___x_333_ == 0)
{
lean_object* v___x_334_; 
v___x_334_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_312_ = v___x_334_;
goto v___jp_311_;
}
else
{
lean_object* v___x_335_; 
v___x_335_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_312_ = v___x_335_;
goto v___jp_311_;
}
}
case 1:
{
lean_object* v___x_336_; uint8_t v___x_337_; 
v___x_336_ = lean_unsigned_to_nat(1024u);
v___x_337_ = lean_nat_dec_le(v___x_336_, v_prec_310_);
if (v___x_337_ == 0)
{
lean_object* v___x_338_; 
v___x_338_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_319_ = v___x_338_;
goto v___jp_318_;
}
else
{
lean_object* v___x_339_; 
v___x_339_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_319_ = v___x_339_;
goto v___jp_318_;
}
}
default: 
{
lean_object* v___x_340_; uint8_t v___x_341_; 
v___x_340_ = lean_unsigned_to_nat(1024u);
v___x_341_ = lean_nat_dec_le(v___x_340_, v_prec_310_);
if (v___x_341_ == 0)
{
lean_object* v___x_342_; 
v___x_342_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_326_ = v___x_342_;
goto v___jp_325_;
}
else
{
lean_object* v___x_343_; 
v___x_343_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_326_ = v___x_343_;
goto v___jp_325_;
}
}
}
v___jp_311_:
{
lean_object* v___x_313_; lean_object* v___x_314_; uint8_t v___x_315_; lean_object* v___x_316_; lean_object* v___x_317_; 
v___x_313_ = ((lean_object*)(lp_FiniteQuantum_instReprIsingAnyon_repr___closed__1));
lean_inc(v___y_312_);
v___x_314_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_314_, 0, v___y_312_);
lean_ctor_set(v___x_314_, 1, v___x_313_);
v___x_315_ = 0;
v___x_316_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_316_, 0, v___x_314_);
lean_ctor_set_uint8(v___x_316_, sizeof(void*)*1, v___x_315_);
v___x_317_ = l_Repr_addAppParen(v___x_316_, v_prec_310_);
return v___x_317_;
}
v___jp_318_:
{
lean_object* v___x_320_; lean_object* v___x_321_; uint8_t v___x_322_; lean_object* v___x_323_; lean_object* v___x_324_; 
v___x_320_ = ((lean_object*)(lp_FiniteQuantum_instReprIsingAnyon_repr___closed__3));
lean_inc(v___y_319_);
v___x_321_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_321_, 0, v___y_319_);
lean_ctor_set(v___x_321_, 1, v___x_320_);
v___x_322_ = 0;
v___x_323_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_323_, 0, v___x_321_);
lean_ctor_set_uint8(v___x_323_, sizeof(void*)*1, v___x_322_);
v___x_324_ = l_Repr_addAppParen(v___x_323_, v_prec_310_);
return v___x_324_;
}
v___jp_325_:
{
lean_object* v___x_327_; lean_object* v___x_328_; uint8_t v___x_329_; lean_object* v___x_330_; lean_object* v___x_331_; 
v___x_327_ = ((lean_object*)(lp_FiniteQuantum_instReprIsingAnyon_repr___closed__5));
lean_inc(v___y_326_);
v___x_328_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_328_, 0, v___y_326_);
lean_ctor_set(v___x_328_, 1, v___x_327_);
v___x_329_ = 0;
v___x_330_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_330_, 0, v___x_328_);
lean_ctor_set_uint8(v___x_330_, sizeof(void*)*1, v___x_329_);
v___x_331_ = l_Repr_addAppParen(v___x_330_, v_prec_310_);
return v___x_331_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprIsingAnyon_repr___boxed(lean_object* v_x_344_, lean_object* v_prec_345_){
_start:
{
uint8_t v_x_173__boxed_346_; lean_object* v_res_347_; 
v_x_173__boxed_346_ = lean_unbox(v_x_344_);
v_res_347_ = lp_FiniteQuantum_instReprIsingAnyon_repr(v_x_173__boxed_346_, v_prec_345_);
lean_dec(v_prec_345_);
return v_res_347_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ising__quantum__dim__sq(uint8_t v_a_350_){
_start:
{
if (v_a_350_ == 1)
{
lean_object* v___x_351_; 
v___x_351_ = lean_unsigned_to_nat(2u);
return v___x_351_;
}
else
{
lean_object* v___x_352_; 
v___x_352_ = lean_unsigned_to_nat(1u);
return v___x_352_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ising__quantum__dim__sq___boxed(lean_object* v_a_353_){
_start:
{
uint8_t v_a_boxed_354_; lean_object* v_res_355_; 
v_a_boxed_354_ = lean_unbox(v_a_353_);
v_res_355_ = lp_FiniteQuantum_ising__quantum__dim__sq(v_a_boxed_354_);
return v_res_355_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorIdx(uint8_t v_x_356_){
_start:
{
switch(v_x_356_)
{
case 0:
{
lean_object* v___x_357_; 
v___x_357_ = lean_unsigned_to_nat(0u);
return v___x_357_;
}
case 1:
{
lean_object* v___x_358_; 
v___x_358_ = lean_unsigned_to_nat(1u);
return v___x_358_;
}
default: 
{
lean_object* v___x_359_; 
v___x_359_ = lean_unsigned_to_nat(2u);
return v___x_359_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorIdx___boxed(lean_object* v_x_360_){
_start:
{
uint8_t v_x_boxed_361_; lean_object* v_res_362_; 
v_x_boxed_361_ = lean_unbox(v_x_360_);
v_res_362_ = lp_FiniteQuantum_SurfaceTopology_ctorIdx(v_x_boxed_361_);
return v_res_362_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_toCtorIdx(uint8_t v_x_363_){
_start:
{
lean_object* v___x_364_; 
v___x_364_ = lp_FiniteQuantum_SurfaceTopology_ctorIdx(v_x_363_);
return v___x_364_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_toCtorIdx___boxed(lean_object* v_x_365_){
_start:
{
uint8_t v_x_4__boxed_366_; lean_object* v_res_367_; 
v_x_4__boxed_366_ = lean_unbox(v_x_365_);
v_res_367_ = lp_FiniteQuantum_SurfaceTopology_toCtorIdx(v_x_4__boxed_366_);
return v_res_367_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim___redArg(lean_object* v_k_368_){
_start:
{
lean_inc(v_k_368_);
return v_k_368_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim___redArg___boxed(lean_object* v_k_369_){
_start:
{
lean_object* v_res_370_; 
v_res_370_ = lp_FiniteQuantum_SurfaceTopology_ctorElim___redArg(v_k_369_);
lean_dec(v_k_369_);
return v_res_370_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim(lean_object* v_motive_371_, lean_object* v_ctorIdx_372_, uint8_t v_t_373_, lean_object* v_h_374_, lean_object* v_k_375_){
_start:
{
lean_inc(v_k_375_);
return v_k_375_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ctorElim___boxed(lean_object* v_motive_376_, lean_object* v_ctorIdx_377_, lean_object* v_t_378_, lean_object* v_h_379_, lean_object* v_k_380_){
_start:
{
uint8_t v_t_boxed_381_; lean_object* v_res_382_; 
v_t_boxed_381_ = lean_unbox(v_t_378_);
v_res_382_ = lp_FiniteQuantum_SurfaceTopology_ctorElim(v_motive_376_, v_ctorIdx_377_, v_t_boxed_381_, v_h_379_, v_k_380_);
lean_dec(v_k_380_);
lean_dec(v_ctorIdx_377_);
return v_res_382_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim___redArg(lean_object* v_Disk_383_){
_start:
{
lean_inc(v_Disk_383_);
return v_Disk_383_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim___redArg___boxed(lean_object* v_Disk_384_){
_start:
{
lean_object* v_res_385_; 
v_res_385_ = lp_FiniteQuantum_SurfaceTopology_Disk_elim___redArg(v_Disk_384_);
lean_dec(v_Disk_384_);
return v_res_385_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim(lean_object* v_motive_386_, uint8_t v_t_387_, lean_object* v_h_388_, lean_object* v_Disk_389_){
_start:
{
lean_inc(v_Disk_389_);
return v_Disk_389_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Disk_elim___boxed(lean_object* v_motive_390_, lean_object* v_t_391_, lean_object* v_h_392_, lean_object* v_Disk_393_){
_start:
{
uint8_t v_t_boxed_394_; lean_object* v_res_395_; 
v_t_boxed_394_ = lean_unbox(v_t_391_);
v_res_395_ = lp_FiniteQuantum_SurfaceTopology_Disk_elim(v_motive_390_, v_t_boxed_394_, v_h_392_, v_Disk_393_);
lean_dec(v_Disk_393_);
return v_res_395_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___redArg(lean_object* v_Cylinder_396_){
_start:
{
lean_inc(v_Cylinder_396_);
return v_Cylinder_396_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___redArg___boxed(lean_object* v_Cylinder_397_){
_start:
{
lean_object* v_res_398_; 
v_res_398_ = lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___redArg(v_Cylinder_397_);
lean_dec(v_Cylinder_397_);
return v_res_398_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim(lean_object* v_motive_399_, uint8_t v_t_400_, lean_object* v_h_401_, lean_object* v_Cylinder_402_){
_start:
{
lean_inc(v_Cylinder_402_);
return v_Cylinder_402_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Cylinder_elim___boxed(lean_object* v_motive_403_, lean_object* v_t_404_, lean_object* v_h_405_, lean_object* v_Cylinder_406_){
_start:
{
uint8_t v_t_boxed_407_; lean_object* v_res_408_; 
v_t_boxed_407_ = lean_unbox(v_t_404_);
v_res_408_ = lp_FiniteQuantum_SurfaceTopology_Cylinder_elim(v_motive_403_, v_t_boxed_407_, v_h_405_, v_Cylinder_406_);
lean_dec(v_Cylinder_406_);
return v_res_408_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim___redArg(lean_object* v_Torus_409_){
_start:
{
lean_inc(v_Torus_409_);
return v_Torus_409_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim___redArg___boxed(lean_object* v_Torus_410_){
_start:
{
lean_object* v_res_411_; 
v_res_411_ = lp_FiniteQuantum_SurfaceTopology_Torus_elim___redArg(v_Torus_410_);
lean_dec(v_Torus_410_);
return v_res_411_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim(lean_object* v_motive_412_, uint8_t v_t_413_, lean_object* v_h_414_, lean_object* v_Torus_415_){
_start:
{
lean_inc(v_Torus_415_);
return v_Torus_415_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_Torus_elim___boxed(lean_object* v_motive_416_, lean_object* v_t_417_, lean_object* v_h_418_, lean_object* v_Torus_419_){
_start:
{
uint8_t v_t_boxed_420_; lean_object* v_res_421_; 
v_t_boxed_420_ = lean_unbox(v_t_417_);
v_res_421_ = lp_FiniteQuantum_SurfaceTopology_Torus_elim(v_motive_416_, v_t_boxed_420_, v_h_418_, v_Torus_419_);
lean_dec(v_Torus_419_);
return v_res_421_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_SurfaceTopology_ofNat(lean_object* v_n_422_){
_start:
{
lean_object* v___x_423_; uint8_t v___x_424_; 
v___x_423_ = lean_unsigned_to_nat(0u);
v___x_424_ = lean_nat_dec_le(v_n_422_, v___x_423_);
if (v___x_424_ == 0)
{
lean_object* v___x_425_; uint8_t v___x_426_; 
v___x_425_ = lean_unsigned_to_nat(1u);
v___x_426_ = lean_nat_dec_le(v_n_422_, v___x_425_);
if (v___x_426_ == 0)
{
uint8_t v___x_427_; 
v___x_427_ = 2;
return v___x_427_;
}
else
{
uint8_t v___x_428_; 
v___x_428_ = 1;
return v___x_428_;
}
}
else
{
uint8_t v___x_429_; 
v___x_429_ = 0;
return v___x_429_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_SurfaceTopology_ofNat___boxed(lean_object* v_n_430_){
_start:
{
uint8_t v_res_431_; lean_object* v_r_432_; 
v_res_431_ = lp_FiniteQuantum_SurfaceTopology_ofNat(v_n_430_);
lean_dec(v_n_430_);
v_r_432_ = lean_box(v_res_431_);
return v_r_432_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_instDecidableEqSurfaceTopology(uint8_t v_x_433_, uint8_t v_y_434_){
_start:
{
lean_object* v___x_435_; lean_object* v___x_436_; uint8_t v___x_437_; 
v___x_435_ = lp_FiniteQuantum_SurfaceTopology_ctorIdx(v_x_433_);
v___x_436_ = lp_FiniteQuantum_SurfaceTopology_ctorIdx(v_y_434_);
v___x_437_ = lean_nat_dec_eq(v___x_435_, v___x_436_);
lean_dec(v___x_436_);
lean_dec(v___x_435_);
return v___x_437_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instDecidableEqSurfaceTopology___boxed(lean_object* v_x_438_, lean_object* v_y_439_){
_start:
{
uint8_t v_x_13__boxed_440_; uint8_t v_y_14__boxed_441_; uint8_t v_res_442_; lean_object* v_r_443_; 
v_x_13__boxed_440_ = lean_unbox(v_x_438_);
v_y_14__boxed_441_ = lean_unbox(v_y_439_);
v_res_442_ = lp_FiniteQuantum_instDecidableEqSurfaceTopology(v_x_13__boxed_440_, v_y_14__boxed_441_);
v_r_443_ = lean_box(v_res_442_);
return v_r_443_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr(uint8_t v_x_453_, lean_object* v_prec_454_){
_start:
{
lean_object* v___y_456_; lean_object* v___y_463_; lean_object* v___y_470_; 
switch(v_x_453_)
{
case 0:
{
lean_object* v___x_476_; uint8_t v___x_477_; 
v___x_476_ = lean_unsigned_to_nat(1024u);
v___x_477_ = lean_nat_dec_le(v___x_476_, v_prec_454_);
if (v___x_477_ == 0)
{
lean_object* v___x_478_; 
v___x_478_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_456_ = v___x_478_;
goto v___jp_455_;
}
else
{
lean_object* v___x_479_; 
v___x_479_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_456_ = v___x_479_;
goto v___jp_455_;
}
}
case 1:
{
lean_object* v___x_480_; uint8_t v___x_481_; 
v___x_480_ = lean_unsigned_to_nat(1024u);
v___x_481_ = lean_nat_dec_le(v___x_480_, v_prec_454_);
if (v___x_481_ == 0)
{
lean_object* v___x_482_; 
v___x_482_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_463_ = v___x_482_;
goto v___jp_462_;
}
else
{
lean_object* v___x_483_; 
v___x_483_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_463_ = v___x_483_;
goto v___jp_462_;
}
}
default: 
{
lean_object* v___x_484_; uint8_t v___x_485_; 
v___x_484_ = lean_unsigned_to_nat(1024u);
v___x_485_ = lean_nat_dec_le(v___x_484_, v_prec_454_);
if (v___x_485_ == 0)
{
lean_object* v___x_486_; 
v___x_486_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__6);
v___y_470_ = v___x_486_;
goto v___jp_469_;
}
else
{
lean_object* v___x_487_; 
v___x_487_ = lean_obj_once(&lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7, &lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7_once, _init_lp_FiniteQuantum_instReprTrichotomyClass_repr___closed__7);
v___y_470_ = v___x_487_;
goto v___jp_469_;
}
}
}
v___jp_455_:
{
lean_object* v___x_457_; lean_object* v___x_458_; uint8_t v___x_459_; lean_object* v___x_460_; lean_object* v___x_461_; 
v___x_457_ = ((lean_object*)(lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__1));
lean_inc(v___y_456_);
v___x_458_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_458_, 0, v___y_456_);
lean_ctor_set(v___x_458_, 1, v___x_457_);
v___x_459_ = 0;
v___x_460_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_460_, 0, v___x_458_);
lean_ctor_set_uint8(v___x_460_, sizeof(void*)*1, v___x_459_);
v___x_461_ = l_Repr_addAppParen(v___x_460_, v_prec_454_);
return v___x_461_;
}
v___jp_462_:
{
lean_object* v___x_464_; lean_object* v___x_465_; uint8_t v___x_466_; lean_object* v___x_467_; lean_object* v___x_468_; 
v___x_464_ = ((lean_object*)(lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__3));
lean_inc(v___y_463_);
v___x_465_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_465_, 0, v___y_463_);
lean_ctor_set(v___x_465_, 1, v___x_464_);
v___x_466_ = 0;
v___x_467_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_467_, 0, v___x_465_);
lean_ctor_set_uint8(v___x_467_, sizeof(void*)*1, v___x_466_);
v___x_468_ = l_Repr_addAppParen(v___x_467_, v_prec_454_);
return v___x_468_;
}
v___jp_469_:
{
lean_object* v___x_471_; lean_object* v___x_472_; uint8_t v___x_473_; lean_object* v___x_474_; lean_object* v___x_475_; 
v___x_471_ = ((lean_object*)(lp_FiniteQuantum_instReprSurfaceTopology_repr___closed__5));
lean_inc(v___y_470_);
v___x_472_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_472_, 0, v___y_470_);
lean_ctor_set(v___x_472_, 1, v___x_471_);
v___x_473_ = 0;
v___x_474_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_474_, 0, v___x_472_);
lean_ctor_set_uint8(v___x_474_, sizeof(void*)*1, v___x_473_);
v___x_475_ = l_Repr_addAppParen(v___x_474_, v_prec_454_);
return v___x_475_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_instReprSurfaceTopology_repr___boxed(lean_object* v_x_488_, lean_object* v_prec_489_){
_start:
{
uint8_t v_x_173__boxed_490_; lean_object* v_res_491_; 
v_x_173__boxed_490_ = lean_unbox(v_x_488_);
v_res_491_ = lp_FiniteQuantum_instReprSurfaceTopology_repr(v_x_173__boxed_490_, v_prec_489_);
lean_dec(v_prec_489_);
return v_res_491_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_betti1__of__topology(uint8_t v_topo_494_){
_start:
{
switch(v_topo_494_)
{
case 0:
{
lean_object* v___x_495_; 
v___x_495_ = lean_unsigned_to_nat(0u);
return v___x_495_;
}
case 1:
{
lean_object* v___x_496_; 
v___x_496_ = lean_unsigned_to_nat(1u);
return v___x_496_;
}
default: 
{
lean_object* v___x_497_; 
v___x_497_ = lean_unsigned_to_nat(2u);
return v___x_497_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_betti1__of__topology___boxed(lean_object* v_topo_498_){
_start:
{
uint8_t v_topo_boxed_499_; lean_object* v_res_500_; 
v_topo_boxed_499_ = lean_unbox(v_topo_498_);
v_res_500_ = lp_FiniteQuantum_betti1__of__topology(v_topo_boxed_499_);
return v_res_500_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_toric__distance(lean_object* v_rows_501_, lean_object* v_cols_502_){
_start:
{
uint8_t v___x_503_; 
v___x_503_ = lean_nat_dec_le(v_rows_501_, v_cols_502_);
if (v___x_503_ == 0)
{
lean_inc(v_cols_502_);
return v_cols_502_;
}
else
{
lean_inc(v_rows_501_);
return v_rows_501_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_toric__distance___boxed(lean_object* v_rows_504_, lean_object* v_cols_505_){
_start:
{
lean_object* v_res_506_; 
v_res_506_ = lp_FiniteQuantum_toric__distance(v_rows_504_, v_cols_505_);
lean_dec(v_cols_505_);
lean_dec(v_rows_504_);
return v_res_506_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_coset__weight__upper__bound___redArg(lean_object* v_n1_507_, lean_object* v_C_508_, lean_object* v_w_509_, lean_object* v_alpha_510_){
_start:
{
lean_object* v_d0_511_; lean_object* v___x_512_; lean_object* v___x_513_; lean_object* v___x_514_; 
v_d0_511_ = lean_ctor_get(v_C_508_, 0);
lean_inc_ref(v_d0_511_);
lean_dec_ref(v_C_508_);
v___x_512_ = lean_apply_1(v_d0_511_, v_alpha_510_);
lean_inc(v_n1_507_);
v___x_513_ = lean_alloc_closure((void*)(lp_FiniteQuantum_F2Vec_add___boxed), 4, 3);
lean_closure_set(v___x_513_, 0, v_n1_507_);
lean_closure_set(v___x_513_, 1, v_w_509_);
lean_closure_set(v___x_513_, 2, v___x_512_);
v___x_514_ = lp_FiniteQuantum_F2Vec_weight(v_n1_507_, v___x_513_);
return v___x_514_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_coset__weight__upper__bound(lean_object* v_n0_515_, lean_object* v_n1_516_, lean_object* v_n2_517_, lean_object* v_C_518_, lean_object* v_w_519_, lean_object* v_alpha_520_){
_start:
{
lean_object* v___x_521_; 
v___x_521_ = lp_FiniteQuantum_coset__weight__upper__bound___redArg(v_n1_516_, v_C_518_, v_w_519_, v_alpha_520_);
return v___x_521_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_coset__weight__upper__bound___boxed(lean_object* v_n0_522_, lean_object* v_n1_523_, lean_object* v_n2_524_, lean_object* v_C_525_, lean_object* v_w_526_, lean_object* v_alpha_527_){
_start:
{
lean_object* v_res_528_; 
v_res_528_ = lp_FiniteQuantum_coset__weight__upper__bound(v_n0_522_, v_n1_523_, v_n2_524_, v_C_525_, v_w_526_, v_alpha_527_);
lean_dec(v_n2_524_);
lean_dec(v_n0_522_);
return v_res_528_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_MajoranaCore(uint8_t builtin) {
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
