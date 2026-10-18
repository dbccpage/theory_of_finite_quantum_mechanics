// Lean compiler output
// Module: GroupParameter
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
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_SubgroupType_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 37, .m_capacity = 37, .m_length = 36, .m_data = "GroupParameter.SubgroupType.rotation"};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 34, .m_capacity = 34, .m_length = 33, .m_data = "GroupParameter.SubgroupType.boost"};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 42, .m_capacity = 42, .m_length = 41, .m_data = "GroupParameter.SubgroupType.timeEvolution"};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__5_value;
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6;
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_GroupParameter_instReprSubgroupType___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType___closed__0 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprSubgroupType___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_ParameterVerdict_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_instDecidableEqParameterVerdict(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instDecidableEqParameterVerdict___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 40, .m_capacity = 40, .m_length = 39, .m_data = "GroupParameter.ParameterVerdict.carried"};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 54, .m_capacity = 54, .m_length = 53, .m_data = "GroupParameter.ParameterVerdict.refusedTranscendental"};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 53, .m_capacity = 53, .m_length = 52, .m_data = "GroupParameter.ParameterVerdict.externallyInterfaced"};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__5_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_GroupParameter_instReprParameterVerdict___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict___closed__0 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict = (const lean_object*)&lp_FiniteQuantum_GroupParameter_instReprParameterVerdict___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__0 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__1 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__1_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_classifyGroupParameter(uint8_t, uint8_t, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_classifyGroupParameter___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0;
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_b1Numerator(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_b1Numerator___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0;
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1;
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_GroupParameter_pauliZ___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GroupParameter_pauliZ___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pauliZ(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pauliZ___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_GroupParameter_terminalOutcome___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 36, .m_capacity = 36, .m_length = 35, .m_data = "PARAMETERS_REFUSED_ELEMENTS_CARRIED"};
static const lean_object* lp_FiniteQuantum_GroupParameter_terminalOutcome___closed__0 = (const lean_object*)&lp_FiniteQuantum_GroupParameter_terminalOutcome___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_GroupParameter_terminalOutcome = (const lean_object*)&lp_FiniteQuantum_GroupParameter_terminalOutcome___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_inventoryTotalCount;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_inventoryCarriedCount;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_inventoryRefusedCount;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx(uint8_t v_x_1_){
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
default: 
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(2u);
return v___x_4_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx___boxed(lean_object* v_x_5_){
_start:
{
uint8_t v_x_boxed_6_; lean_object* v_res_7_; 
v_x_boxed_6_ = lean_unbox(v_x_5_);
v_res_7_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx(v_x_boxed_6_);
return v_res_7_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_toCtorIdx(uint8_t v_x_8_){
_start:
{
lean_object* v___x_9_; 
v___x_9_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx(v_x_8_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_toCtorIdx___boxed(lean_object* v_x_10_){
_start:
{
uint8_t v_x_4__boxed_11_; lean_object* v_res_12_; 
v_x_4__boxed_11_ = lean_unbox(v_x_10_);
v_res_12_ = lp_FiniteQuantum_GroupParameter_SubgroupType_toCtorIdx(v_x_4__boxed_11_);
return v_res_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___redArg(lean_object* v_k_13_){
_start:
{
lean_inc(v_k_13_);
return v_k_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___redArg___boxed(lean_object* v_k_14_){
_start:
{
lean_object* v_res_15_; 
v_res_15_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___redArg(v_k_14_);
lean_dec(v_k_14_);
return v_res_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim(lean_object* v_motive_16_, lean_object* v_ctorIdx_17_, uint8_t v_t_18_, lean_object* v_h_19_, lean_object* v_k_20_){
_start:
{
lean_inc(v_k_20_);
return v_k_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim___boxed(lean_object* v_motive_21_, lean_object* v_ctorIdx_22_, lean_object* v_t_23_, lean_object* v_h_24_, lean_object* v_k_25_){
_start:
{
uint8_t v_t_boxed_26_; lean_object* v_res_27_; 
v_t_boxed_26_ = lean_unbox(v_t_23_);
v_res_27_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ctorElim(v_motive_21_, v_ctorIdx_22_, v_t_boxed_26_, v_h_24_, v_k_25_);
lean_dec(v_k_25_);
lean_dec(v_ctorIdx_22_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___redArg(lean_object* v_rotation_28_){
_start:
{
lean_inc(v_rotation_28_);
return v_rotation_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___redArg___boxed(lean_object* v_rotation_29_){
_start:
{
lean_object* v_res_30_; 
v_res_30_ = lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___redArg(v_rotation_29_);
lean_dec(v_rotation_29_);
return v_res_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim(lean_object* v_motive_31_, uint8_t v_t_32_, lean_object* v_h_33_, lean_object* v_rotation_34_){
_start:
{
lean_inc(v_rotation_34_);
return v_rotation_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim___boxed(lean_object* v_motive_35_, lean_object* v_t_36_, lean_object* v_h_37_, lean_object* v_rotation_38_){
_start:
{
uint8_t v_t_boxed_39_; lean_object* v_res_40_; 
v_t_boxed_39_ = lean_unbox(v_t_36_);
v_res_40_ = lp_FiniteQuantum_GroupParameter_SubgroupType_rotation_elim(v_motive_35_, v_t_boxed_39_, v_h_37_, v_rotation_38_);
lean_dec(v_rotation_38_);
return v_res_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___redArg(lean_object* v_boost_41_){
_start:
{
lean_inc(v_boost_41_);
return v_boost_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___redArg___boxed(lean_object* v_boost_42_){
_start:
{
lean_object* v_res_43_; 
v_res_43_ = lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___redArg(v_boost_42_);
lean_dec(v_boost_42_);
return v_res_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim(lean_object* v_motive_44_, uint8_t v_t_45_, lean_object* v_h_46_, lean_object* v_boost_47_){
_start:
{
lean_inc(v_boost_47_);
return v_boost_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim___boxed(lean_object* v_motive_48_, lean_object* v_t_49_, lean_object* v_h_50_, lean_object* v_boost_51_){
_start:
{
uint8_t v_t_boxed_52_; lean_object* v_res_53_; 
v_t_boxed_52_ = lean_unbox(v_t_49_);
v_res_53_ = lp_FiniteQuantum_GroupParameter_SubgroupType_boost_elim(v_motive_48_, v_t_boxed_52_, v_h_50_, v_boost_51_);
lean_dec(v_boost_51_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___redArg(lean_object* v_timeEvolution_54_){
_start:
{
lean_inc(v_timeEvolution_54_);
return v_timeEvolution_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___redArg___boxed(lean_object* v_timeEvolution_55_){
_start:
{
lean_object* v_res_56_; 
v_res_56_ = lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___redArg(v_timeEvolution_55_);
lean_dec(v_timeEvolution_55_);
return v_res_56_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim(lean_object* v_motive_57_, uint8_t v_t_58_, lean_object* v_h_59_, lean_object* v_timeEvolution_60_){
_start:
{
lean_inc(v_timeEvolution_60_);
return v_timeEvolution_60_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim___boxed(lean_object* v_motive_61_, lean_object* v_t_62_, lean_object* v_h_63_, lean_object* v_timeEvolution_64_){
_start:
{
uint8_t v_t_boxed_65_; lean_object* v_res_66_; 
v_t_boxed_65_ = lean_unbox(v_t_62_);
v_res_66_ = lp_FiniteQuantum_GroupParameter_SubgroupType_timeEvolution_elim(v_motive_61_, v_t_boxed_65_, v_h_63_, v_timeEvolution_64_);
lean_dec(v_timeEvolution_64_);
return v_res_66_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_SubgroupType_ofNat(lean_object* v_n_67_){
_start:
{
lean_object* v___x_68_; uint8_t v___x_69_; 
v___x_68_ = lean_unsigned_to_nat(0u);
v___x_69_ = lean_nat_dec_le(v_n_67_, v___x_68_);
if (v___x_69_ == 0)
{
lean_object* v___x_70_; uint8_t v___x_71_; 
v___x_70_ = lean_unsigned_to_nat(1u);
v___x_71_ = lean_nat_dec_le(v_n_67_, v___x_70_);
if (v___x_71_ == 0)
{
uint8_t v___x_72_; 
v___x_72_ = 2;
return v___x_72_;
}
else
{
uint8_t v___x_73_; 
v___x_73_ = 1;
return v___x_73_;
}
}
else
{
uint8_t v___x_74_; 
v___x_74_ = 0;
return v___x_74_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_SubgroupType_ofNat___boxed(lean_object* v_n_75_){
_start:
{
uint8_t v_res_76_; lean_object* v_r_77_; 
v_res_76_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ofNat(v_n_75_);
lean_dec(v_n_75_);
v_r_77_ = lean_box(v_res_76_);
return v_r_77_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType(uint8_t v_x_78_, uint8_t v_y_79_){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; uint8_t v___x_82_; 
v___x_80_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx(v_x_78_);
v___x_81_ = lp_FiniteQuantum_GroupParameter_SubgroupType_ctorIdx(v_y_79_);
v___x_82_ = lean_nat_dec_eq(v___x_80_, v___x_81_);
lean_dec(v___x_81_);
lean_dec(v___x_80_);
return v___x_82_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType___boxed(lean_object* v_x_83_, lean_object* v_y_84_){
_start:
{
uint8_t v_x_13__boxed_85_; uint8_t v_y_14__boxed_86_; uint8_t v_res_87_; lean_object* v_r_88_; 
v_x_13__boxed_85_ = lean_unbox(v_x_83_);
v_y_14__boxed_86_ = lean_unbox(v_y_84_);
v_res_87_ = lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType(v_x_13__boxed_85_, v_y_14__boxed_86_);
v_r_88_ = lean_box(v_res_87_);
return v_r_88_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6(void){
_start:
{
lean_object* v___x_98_; lean_object* v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(2u);
v___x_99_ = lean_nat_to_int(v___x_98_);
return v___x_99_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7(void){
_start:
{
lean_object* v___x_100_; lean_object* v___x_101_; 
v___x_100_ = lean_unsigned_to_nat(1u);
v___x_101_ = lean_nat_to_int(v___x_100_);
return v___x_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr(uint8_t v_x_102_, lean_object* v_prec_103_){
_start:
{
lean_object* v___y_105_; lean_object* v___y_112_; lean_object* v___y_119_; 
switch(v_x_102_)
{
case 0:
{
lean_object* v___x_125_; uint8_t v___x_126_; 
v___x_125_ = lean_unsigned_to_nat(1024u);
v___x_126_ = lean_nat_dec_le(v___x_125_, v_prec_103_);
if (v___x_126_ == 0)
{
lean_object* v___x_127_; 
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6);
v___y_105_ = v___x_127_;
goto v___jp_104_;
}
else
{
lean_object* v___x_128_; 
v___x_128_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___y_105_ = v___x_128_;
goto v___jp_104_;
}
}
case 1:
{
lean_object* v___x_129_; uint8_t v___x_130_; 
v___x_129_ = lean_unsigned_to_nat(1024u);
v___x_130_ = lean_nat_dec_le(v___x_129_, v_prec_103_);
if (v___x_130_ == 0)
{
lean_object* v___x_131_; 
v___x_131_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6);
v___y_112_ = v___x_131_;
goto v___jp_111_;
}
else
{
lean_object* v___x_132_; 
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___y_112_ = v___x_132_;
goto v___jp_111_;
}
}
default: 
{
lean_object* v___x_133_; uint8_t v___x_134_; 
v___x_133_ = lean_unsigned_to_nat(1024u);
v___x_134_ = lean_nat_dec_le(v___x_133_, v_prec_103_);
if (v___x_134_ == 0)
{
lean_object* v___x_135_; 
v___x_135_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6);
v___y_119_ = v___x_135_;
goto v___jp_118_;
}
else
{
lean_object* v___x_136_; 
v___x_136_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___y_119_ = v___x_136_;
goto v___jp_118_;
}
}
}
v___jp_104_:
{
lean_object* v___x_106_; lean_object* v___x_107_; uint8_t v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; 
v___x_106_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__1));
lean_inc(v___y_105_);
v___x_107_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_107_, 0, v___y_105_);
lean_ctor_set(v___x_107_, 1, v___x_106_);
v___x_108_ = 0;
v___x_109_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_109_, 0, v___x_107_);
lean_ctor_set_uint8(v___x_109_, sizeof(void*)*1, v___x_108_);
v___x_110_ = l_Repr_addAppParen(v___x_109_, v_prec_103_);
return v___x_110_;
}
v___jp_111_:
{
lean_object* v___x_113_; lean_object* v___x_114_; uint8_t v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; 
v___x_113_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__3));
lean_inc(v___y_112_);
v___x_114_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_114_, 0, v___y_112_);
lean_ctor_set(v___x_114_, 1, v___x_113_);
v___x_115_ = 0;
v___x_116_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_116_, 0, v___x_114_);
lean_ctor_set_uint8(v___x_116_, sizeof(void*)*1, v___x_115_);
v___x_117_ = l_Repr_addAppParen(v___x_116_, v_prec_103_);
return v___x_117_;
}
v___jp_118_:
{
lean_object* v___x_120_; lean_object* v___x_121_; uint8_t v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; 
v___x_120_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__5));
lean_inc(v___y_119_);
v___x_121_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_121_, 0, v___y_119_);
lean_ctor_set(v___x_121_, 1, v___x_120_);
v___x_122_ = 0;
v___x_123_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_123_, 0, v___x_121_);
lean_ctor_set_uint8(v___x_123_, sizeof(void*)*1, v___x_122_);
v___x_124_ = l_Repr_addAppParen(v___x_123_, v_prec_103_);
return v___x_124_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___boxed(lean_object* v_x_137_, lean_object* v_prec_138_){
_start:
{
uint8_t v_x_177__boxed_139_; lean_object* v_res_140_; 
v_x_177__boxed_139_ = lean_unbox(v_x_137_);
v_res_140_ = lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr(v_x_177__boxed_139_, v_prec_138_);
lean_dec(v_prec_138_);
return v_res_140_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx(uint8_t v_x_143_){
_start:
{
switch(v_x_143_)
{
case 0:
{
lean_object* v___x_144_; 
v___x_144_ = lean_unsigned_to_nat(0u);
return v___x_144_;
}
case 1:
{
lean_object* v___x_145_; 
v___x_145_ = lean_unsigned_to_nat(1u);
return v___x_145_;
}
default: 
{
lean_object* v___x_146_; 
v___x_146_ = lean_unsigned_to_nat(2u);
return v___x_146_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx___boxed(lean_object* v_x_147_){
_start:
{
uint8_t v_x_boxed_148_; lean_object* v_res_149_; 
v_x_boxed_148_ = lean_unbox(v_x_147_);
v_res_149_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx(v_x_boxed_148_);
return v_res_149_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_toCtorIdx(uint8_t v_x_150_){
_start:
{
lean_object* v___x_151_; 
v___x_151_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx(v_x_150_);
return v___x_151_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_toCtorIdx___boxed(lean_object* v_x_152_){
_start:
{
uint8_t v_x_4__boxed_153_; lean_object* v_res_154_; 
v_x_4__boxed_153_ = lean_unbox(v_x_152_);
v_res_154_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_toCtorIdx(v_x_4__boxed_153_);
return v_res_154_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___redArg(lean_object* v_k_155_){
_start:
{
lean_inc(v_k_155_);
return v_k_155_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___redArg___boxed(lean_object* v_k_156_){
_start:
{
lean_object* v_res_157_; 
v_res_157_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___redArg(v_k_156_);
lean_dec(v_k_156_);
return v_res_157_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim(lean_object* v_motive_158_, lean_object* v_ctorIdx_159_, uint8_t v_t_160_, lean_object* v_h_161_, lean_object* v_k_162_){
_start:
{
lean_inc(v_k_162_);
return v_k_162_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim___boxed(lean_object* v_motive_163_, lean_object* v_ctorIdx_164_, lean_object* v_t_165_, lean_object* v_h_166_, lean_object* v_k_167_){
_start:
{
uint8_t v_t_boxed_168_; lean_object* v_res_169_; 
v_t_boxed_168_ = lean_unbox(v_t_165_);
v_res_169_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorElim(v_motive_163_, v_ctorIdx_164_, v_t_boxed_168_, v_h_166_, v_k_167_);
lean_dec(v_k_167_);
lean_dec(v_ctorIdx_164_);
return v_res_169_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___redArg(lean_object* v_carried_170_){
_start:
{
lean_inc(v_carried_170_);
return v_carried_170_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___redArg___boxed(lean_object* v_carried_171_){
_start:
{
lean_object* v_res_172_; 
v_res_172_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___redArg(v_carried_171_);
lean_dec(v_carried_171_);
return v_res_172_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim(lean_object* v_motive_173_, uint8_t v_t_174_, lean_object* v_h_175_, lean_object* v_carried_176_){
_start:
{
lean_inc(v_carried_176_);
return v_carried_176_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim___boxed(lean_object* v_motive_177_, lean_object* v_t_178_, lean_object* v_h_179_, lean_object* v_carried_180_){
_start:
{
uint8_t v_t_boxed_181_; lean_object* v_res_182_; 
v_t_boxed_181_ = lean_unbox(v_t_178_);
v_res_182_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_carried_elim(v_motive_177_, v_t_boxed_181_, v_h_179_, v_carried_180_);
lean_dec(v_carried_180_);
return v_res_182_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___redArg(lean_object* v_refusedTranscendental_183_){
_start:
{
lean_inc(v_refusedTranscendental_183_);
return v_refusedTranscendental_183_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___redArg___boxed(lean_object* v_refusedTranscendental_184_){
_start:
{
lean_object* v_res_185_; 
v_res_185_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___redArg(v_refusedTranscendental_184_);
lean_dec(v_refusedTranscendental_184_);
return v_res_185_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim(lean_object* v_motive_186_, uint8_t v_t_187_, lean_object* v_h_188_, lean_object* v_refusedTranscendental_189_){
_start:
{
lean_inc(v_refusedTranscendental_189_);
return v_refusedTranscendental_189_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim___boxed(lean_object* v_motive_190_, lean_object* v_t_191_, lean_object* v_h_192_, lean_object* v_refusedTranscendental_193_){
_start:
{
uint8_t v_t_boxed_194_; lean_object* v_res_195_; 
v_t_boxed_194_ = lean_unbox(v_t_191_);
v_res_195_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_refusedTranscendental_elim(v_motive_190_, v_t_boxed_194_, v_h_192_, v_refusedTranscendental_193_);
lean_dec(v_refusedTranscendental_193_);
return v_res_195_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___redArg(lean_object* v_externallyInterfaced_196_){
_start:
{
lean_inc(v_externallyInterfaced_196_);
return v_externallyInterfaced_196_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___redArg___boxed(lean_object* v_externallyInterfaced_197_){
_start:
{
lean_object* v_res_198_; 
v_res_198_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___redArg(v_externallyInterfaced_197_);
lean_dec(v_externallyInterfaced_197_);
return v_res_198_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim(lean_object* v_motive_199_, uint8_t v_t_200_, lean_object* v_h_201_, lean_object* v_externallyInterfaced_202_){
_start:
{
lean_inc(v_externallyInterfaced_202_);
return v_externallyInterfaced_202_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim___boxed(lean_object* v_motive_203_, lean_object* v_t_204_, lean_object* v_h_205_, lean_object* v_externallyInterfaced_206_){
_start:
{
uint8_t v_t_boxed_207_; lean_object* v_res_208_; 
v_t_boxed_207_ = lean_unbox(v_t_204_);
v_res_208_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_externallyInterfaced_elim(v_motive_203_, v_t_boxed_207_, v_h_205_, v_externallyInterfaced_206_);
lean_dec(v_externallyInterfaced_206_);
return v_res_208_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_ParameterVerdict_ofNat(lean_object* v_n_209_){
_start:
{
lean_object* v___x_210_; uint8_t v___x_211_; 
v___x_210_ = lean_unsigned_to_nat(0u);
v___x_211_ = lean_nat_dec_le(v_n_209_, v___x_210_);
if (v___x_211_ == 0)
{
lean_object* v___x_212_; uint8_t v___x_213_; 
v___x_212_ = lean_unsigned_to_nat(1u);
v___x_213_ = lean_nat_dec_le(v_n_209_, v___x_212_);
if (v___x_213_ == 0)
{
uint8_t v___x_214_; 
v___x_214_ = 2;
return v___x_214_;
}
else
{
uint8_t v___x_215_; 
v___x_215_ = 1;
return v___x_215_;
}
}
else
{
uint8_t v___x_216_; 
v___x_216_ = 0;
return v___x_216_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_ParameterVerdict_ofNat___boxed(lean_object* v_n_217_){
_start:
{
uint8_t v_res_218_; lean_object* v_r_219_; 
v_res_218_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ofNat(v_n_217_);
lean_dec(v_n_217_);
v_r_219_ = lean_box(v_res_218_);
return v_r_219_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_GroupParameter_instDecidableEqParameterVerdict(uint8_t v_x_220_, uint8_t v_y_221_){
_start:
{
lean_object* v___x_222_; lean_object* v___x_223_; uint8_t v___x_224_; 
v___x_222_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx(v_x_220_);
v___x_223_ = lp_FiniteQuantum_GroupParameter_ParameterVerdict_ctorIdx(v_y_221_);
v___x_224_ = lean_nat_dec_eq(v___x_222_, v___x_223_);
lean_dec(v___x_223_);
lean_dec(v___x_222_);
return v___x_224_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instDecidableEqParameterVerdict___boxed(lean_object* v_x_225_, lean_object* v_y_226_){
_start:
{
uint8_t v_x_13__boxed_227_; uint8_t v_y_14__boxed_228_; uint8_t v_res_229_; lean_object* v_r_230_; 
v_x_13__boxed_227_ = lean_unbox(v_x_225_);
v_y_14__boxed_228_ = lean_unbox(v_y_226_);
v_res_229_ = lp_FiniteQuantum_GroupParameter_instDecidableEqParameterVerdict(v_x_13__boxed_227_, v_y_14__boxed_228_);
v_r_230_ = lean_box(v_res_229_);
return v_r_230_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr(uint8_t v_x_240_, lean_object* v_prec_241_){
_start:
{
lean_object* v___y_243_; lean_object* v___y_250_; lean_object* v___y_257_; 
switch(v_x_240_)
{
case 0:
{
lean_object* v___x_263_; uint8_t v___x_264_; 
v___x_263_ = lean_unsigned_to_nat(1024u);
v___x_264_ = lean_nat_dec_le(v___x_263_, v_prec_241_);
if (v___x_264_ == 0)
{
lean_object* v___x_265_; 
v___x_265_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6);
v___y_243_ = v___x_265_;
goto v___jp_242_;
}
else
{
lean_object* v___x_266_; 
v___x_266_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___y_243_ = v___x_266_;
goto v___jp_242_;
}
}
case 1:
{
lean_object* v___x_267_; uint8_t v___x_268_; 
v___x_267_ = lean_unsigned_to_nat(1024u);
v___x_268_ = lean_nat_dec_le(v___x_267_, v_prec_241_);
if (v___x_268_ == 0)
{
lean_object* v___x_269_; 
v___x_269_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6);
v___y_250_ = v___x_269_;
goto v___jp_249_;
}
else
{
lean_object* v___x_270_; 
v___x_270_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___y_250_ = v___x_270_;
goto v___jp_249_;
}
}
default: 
{
lean_object* v___x_271_; uint8_t v___x_272_; 
v___x_271_ = lean_unsigned_to_nat(1024u);
v___x_272_ = lean_nat_dec_le(v___x_271_, v_prec_241_);
if (v___x_272_ == 0)
{
lean_object* v___x_273_; 
v___x_273_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__6);
v___y_257_ = v___x_273_;
goto v___jp_256_;
}
else
{
lean_object* v___x_274_; 
v___x_274_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___y_257_ = v___x_274_;
goto v___jp_256_;
}
}
}
v___jp_242_:
{
lean_object* v___x_244_; lean_object* v___x_245_; uint8_t v___x_246_; lean_object* v___x_247_; lean_object* v___x_248_; 
v___x_244_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__1));
lean_inc(v___y_243_);
v___x_245_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_245_, 0, v___y_243_);
lean_ctor_set(v___x_245_, 1, v___x_244_);
v___x_246_ = 0;
v___x_247_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_247_, 0, v___x_245_);
lean_ctor_set_uint8(v___x_247_, sizeof(void*)*1, v___x_246_);
v___x_248_ = l_Repr_addAppParen(v___x_247_, v_prec_241_);
return v___x_248_;
}
v___jp_249_:
{
lean_object* v___x_251_; lean_object* v___x_252_; uint8_t v___x_253_; lean_object* v___x_254_; lean_object* v___x_255_; 
v___x_251_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__3));
lean_inc(v___y_250_);
v___x_252_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_252_, 0, v___y_250_);
lean_ctor_set(v___x_252_, 1, v___x_251_);
v___x_253_ = 0;
v___x_254_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_254_, 0, v___x_252_);
lean_ctor_set_uint8(v___x_254_, sizeof(void*)*1, v___x_253_);
v___x_255_ = l_Repr_addAppParen(v___x_254_, v_prec_241_);
return v___x_255_;
}
v___jp_256_:
{
lean_object* v___x_258_; lean_object* v___x_259_; uint8_t v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; 
v___x_258_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___closed__5));
lean_inc(v___y_257_);
v___x_259_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_259_, 0, v___y_257_);
lean_ctor_set(v___x_259_, 1, v___x_258_);
v___x_260_ = 0;
v___x_261_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_261_, 0, v___x_259_);
lean_ctor_set_uint8(v___x_261_, sizeof(void*)*1, v___x_260_);
v___x_262_ = l_Repr_addAppParen(v___x_261_, v_prec_241_);
return v___x_262_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr___boxed(lean_object* v_x_275_, lean_object* v_prec_276_){
_start:
{
uint8_t v_x_173__boxed_277_; lean_object* v_res_278_; 
v_x_173__boxed_277_ = lean_unbox(v_x_275_);
v_res_278_ = lp_FiniteQuantum_GroupParameter_instReprParameterVerdict_repr(v_x_173__boxed_277_, v_prec_276_);
lean_dec(v_prec_276_);
return v_res_278_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_classifyGroupParameter(uint8_t v_st_287_, uint8_t v_isIdentity_288_, uint8_t v_entriesAlgebraic_289_, uint8_t v_hasNonzeroGen_290_){
_start:
{
uint8_t v___y_292_; uint8_t v___y_297_; uint8_t v___y_302_; 
if (v_isIdentity_288_ == 0)
{
uint8_t v___x_306_; uint8_t v___x_307_; 
v___x_306_ = 0;
v___x_307_ = lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType(v_st_287_, v___x_306_);
if (v___x_307_ == 0)
{
v___y_302_ = v___x_307_;
goto v___jp_301_;
}
else
{
v___y_302_ = v_entriesAlgebraic_289_;
goto v___jp_301_;
}
}
else
{
lean_object* v___x_308_; 
v___x_308_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__1));
return v___x_308_;
}
v___jp_291_:
{
if (v___y_292_ == 0)
{
lean_object* v___x_293_; 
v___x_293_ = lean_box(0);
return v___x_293_;
}
else
{
if (v_hasNonzeroGen_290_ == 0)
{
lean_object* v___x_294_; 
v___x_294_ = lean_box(0);
return v___x_294_;
}
else
{
lean_object* v___x_295_; 
v___x_295_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__0));
return v___x_295_;
}
}
}
v___jp_296_:
{
if (v___y_297_ == 0)
{
uint8_t v___x_298_; uint8_t v___x_299_; 
v___x_298_ = 2;
v___x_299_ = lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType(v_st_287_, v___x_298_);
if (v___x_299_ == 0)
{
v___y_292_ = v___x_299_;
goto v___jp_291_;
}
else
{
v___y_292_ = v_entriesAlgebraic_289_;
goto v___jp_291_;
}
}
else
{
lean_object* v___x_300_; 
v___x_300_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__0));
return v___x_300_;
}
}
v___jp_301_:
{
if (v___y_302_ == 0)
{
uint8_t v___x_303_; uint8_t v___x_304_; 
v___x_303_ = 1;
v___x_304_ = lp_FiniteQuantum_GroupParameter_instDecidableEqSubgroupType(v_st_287_, v___x_303_);
if (v___x_304_ == 0)
{
v___y_297_ = v___x_304_;
goto v___jp_296_;
}
else
{
v___y_297_ = v_entriesAlgebraic_289_;
goto v___jp_296_;
}
}
else
{
lean_object* v___x_305_; 
v___x_305_ = ((lean_object*)(lp_FiniteQuantum_GroupParameter_classifyGroupParameter___closed__0));
return v___x_305_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_classifyGroupParameter___boxed(lean_object* v_st_309_, lean_object* v_isIdentity_310_, lean_object* v_entriesAlgebraic_311_, lean_object* v_hasNonzeroGen_312_){
_start:
{
uint8_t v_st_boxed_313_; uint8_t v_isIdentity_boxed_314_; uint8_t v_entriesAlgebraic_boxed_315_; uint8_t v_hasNonzeroGen_boxed_316_; lean_object* v_res_317_; 
v_st_boxed_313_ = lean_unbox(v_st_309_);
v_isIdentity_boxed_314_ = lean_unbox(v_isIdentity_310_);
v_entriesAlgebraic_boxed_315_ = lean_unbox(v_entriesAlgebraic_311_);
v_hasNonzeroGen_boxed_316_ = lean_unbox(v_hasNonzeroGen_312_);
v_res_317_ = lp_FiniteQuantum_GroupParameter_classifyGroupParameter(v_st_boxed_313_, v_isIdentity_boxed_314_, v_entriesAlgebraic_boxed_315_, v_hasNonzeroGen_boxed_316_);
return v_res_317_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0(void){
_start:
{
lean_object* v___x_318_; lean_object* v___x_319_; 
v___x_318_ = lean_unsigned_to_nat(5u);
v___x_319_ = lean_nat_to_int(v___x_318_);
return v___x_319_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1(void){
_start:
{
lean_object* v___x_320_; lean_object* v___x_321_; 
v___x_320_ = lean_unsigned_to_nat(3u);
v___x_321_ = lean_nat_to_int(v___x_320_);
return v___x_321_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_b1Numerator(lean_object* v_i_322_, lean_object* v_j_323_){
_start:
{
lean_object* v_zero_328_; uint8_t v_isZero_329_; 
v_zero_328_ = lean_unsigned_to_nat(0u);
v_isZero_329_ = lean_nat_dec_eq(v_i_322_, v_zero_328_);
if (v_isZero_329_ == 1)
{
uint8_t v_isZero_330_; 
v_isZero_330_ = lean_nat_dec_eq(v_j_323_, v_zero_328_);
if (v_isZero_330_ == 1)
{
goto v___jp_324_;
}
else
{
lean_object* v_one_331_; lean_object* v_n_332_; uint8_t v_isZero_333_; 
v_one_331_ = lean_unsigned_to_nat(1u);
v_n_332_ = lean_nat_sub(v_j_323_, v_one_331_);
v_isZero_333_ = lean_nat_dec_eq(v_n_332_, v_zero_328_);
lean_dec(v_n_332_);
goto v___jp_326_;
}
}
else
{
lean_object* v_one_334_; lean_object* v_n_335_; uint8_t v_isZero_336_; uint8_t v_isZero_337_; 
v_one_334_ = lean_unsigned_to_nat(1u);
v_n_335_ = lean_nat_sub(v_i_322_, v_one_334_);
v_isZero_336_ = lean_nat_dec_eq(v_n_335_, v_zero_328_);
lean_dec(v_n_335_);
v_isZero_337_ = lean_nat_dec_eq(v_j_323_, v_zero_328_);
if (v_isZero_337_ == 1)
{
goto v___jp_326_;
}
else
{
lean_object* v_n_338_; uint8_t v_isZero_339_; 
v_n_338_ = lean_nat_sub(v_j_323_, v_one_334_);
v_isZero_339_ = lean_nat_dec_eq(v_n_338_, v_zero_328_);
lean_dec(v_n_338_);
goto v___jp_324_;
}
}
v___jp_324_:
{
lean_object* v___x_325_; 
v___x_325_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0, &lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0_once, _init_lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0);
return v___x_325_;
}
v___jp_326_:
{
lean_object* v___x_327_; 
v___x_327_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1, &lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1_once, _init_lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1);
return v___x_327_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_b1Numerator___boxed(lean_object* v_i_340_, lean_object* v_j_341_){
_start:
{
lean_object* v_res_342_; 
v_res_342_ = lp_FiniteQuantum_GroupParameter_b1Numerator(v_i_340_, v_j_341_);
lean_dec(v_j_341_);
lean_dec(v_i_340_);
return v_res_342_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0(void){
_start:
{
lean_object* v___x_343_; lean_object* v___x_344_; 
v___x_343_ = lean_unsigned_to_nat(0u);
v___x_344_ = lean_nat_to_int(v___x_343_);
return v___x_344_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1(void){
_start:
{
lean_object* v___x_345_; lean_object* v___x_346_; 
v___x_345_ = lean_unsigned_to_nat(4u);
v___x_346_ = lean_nat_to_int(v___x_345_);
return v___x_346_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__2(void){
_start:
{
lean_object* v___x_347_; lean_object* v___x_348_; 
v___x_347_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1, &lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1_once, _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1);
v___x_348_ = lean_int_neg(v___x_347_);
return v___x_348_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator(lean_object* v_i_349_, lean_object* v_j_350_){
_start:
{
lean_object* v_zero_355_; uint8_t v_isZero_356_; 
v_zero_355_ = lean_unsigned_to_nat(0u);
v_isZero_356_ = lean_nat_dec_eq(v_i_349_, v_zero_355_);
if (v_isZero_356_ == 1)
{
uint8_t v_isZero_357_; 
v_isZero_357_ = lean_nat_dec_eq(v_j_350_, v_zero_355_);
if (v_isZero_357_ == 1)
{
goto v___jp_351_;
}
else
{
lean_object* v_one_358_; lean_object* v_n_359_; uint8_t v_isZero_360_; 
v_one_358_ = lean_unsigned_to_nat(1u);
v_n_359_ = lean_nat_sub(v_j_350_, v_one_358_);
v_isZero_360_ = lean_nat_dec_eq(v_n_359_, v_zero_355_);
if (v_isZero_360_ == 1)
{
lean_object* v___x_361_; 
lean_dec(v_n_359_);
v___x_361_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__2, &lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__2_once, _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__2);
return v___x_361_;
}
else
{
lean_object* v_n_362_; uint8_t v_isZero_363_; 
v_n_362_ = lean_nat_sub(v_n_359_, v_one_358_);
lean_dec(v_n_359_);
v_isZero_363_ = lean_nat_dec_eq(v_n_362_, v_zero_355_);
lean_dec(v_n_362_);
goto v___jp_353_;
}
}
}
else
{
lean_object* v_one_364_; lean_object* v_n_365_; uint8_t v_isZero_366_; 
v_one_364_ = lean_unsigned_to_nat(1u);
v_n_365_ = lean_nat_sub(v_i_349_, v_one_364_);
v_isZero_366_ = lean_nat_dec_eq(v_n_365_, v_zero_355_);
if (v_isZero_366_ == 1)
{
uint8_t v_isZero_367_; 
lean_dec(v_n_365_);
v_isZero_367_ = lean_nat_dec_eq(v_j_350_, v_zero_355_);
if (v_isZero_367_ == 1)
{
lean_object* v___x_368_; 
v___x_368_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1, &lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1_once, _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__1);
return v___x_368_;
}
else
{
lean_object* v_n_369_; uint8_t v_isZero_370_; 
v_n_369_ = lean_nat_sub(v_j_350_, v_one_364_);
v_isZero_370_ = lean_nat_dec_eq(v_n_369_, v_zero_355_);
if (v_isZero_370_ == 1)
{
lean_dec(v_n_369_);
goto v___jp_351_;
}
else
{
lean_object* v_n_371_; uint8_t v_isZero_372_; 
v_n_371_ = lean_nat_sub(v_n_369_, v_one_364_);
lean_dec(v_n_369_);
v_isZero_372_ = lean_nat_dec_eq(v_n_371_, v_zero_355_);
lean_dec(v_n_371_);
goto v___jp_353_;
}
}
}
else
{
lean_object* v_n_373_; uint8_t v_isZero_374_; uint8_t v_isZero_375_; 
v_n_373_ = lean_nat_sub(v_n_365_, v_one_364_);
lean_dec(v_n_365_);
v_isZero_374_ = lean_nat_dec_eq(v_n_373_, v_zero_355_);
lean_dec(v_n_373_);
v_isZero_375_ = lean_nat_dec_eq(v_j_350_, v_zero_355_);
if (v_isZero_375_ == 1)
{
goto v___jp_353_;
}
else
{
lean_object* v_n_376_; uint8_t v_isZero_377_; 
v_n_376_ = lean_nat_sub(v_j_350_, v_one_364_);
v_isZero_377_ = lean_nat_dec_eq(v_n_376_, v_zero_355_);
if (v_isZero_377_ == 1)
{
lean_dec(v_n_376_);
goto v___jp_353_;
}
else
{
lean_object* v_n_378_; uint8_t v_isZero_379_; lean_object* v___x_380_; 
v_n_378_ = lean_nat_sub(v_n_376_, v_one_364_);
lean_dec(v_n_376_);
v_isZero_379_ = lean_nat_dec_eq(v_n_378_, v_zero_355_);
lean_dec(v_n_378_);
v___x_380_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0, &lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0_once, _init_lp_FiniteQuantum_GroupParameter_b1Numerator___closed__0);
return v___x_380_;
}
}
}
}
v___jp_351_:
{
lean_object* v___x_352_; 
v___x_352_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1, &lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1_once, _init_lp_FiniteQuantum_GroupParameter_b1Numerator___closed__1);
return v___x_352_;
}
v___jp_353_:
{
lean_object* v___x_354_; 
v___x_354_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0, &lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0_once, _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0);
return v___x_354_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pythRotNumerator___boxed(lean_object* v_i_381_, lean_object* v_j_382_){
_start:
{
lean_object* v_res_383_; 
v_res_383_ = lp_FiniteQuantum_GroupParameter_pythRotNumerator(v_i_381_, v_j_382_);
lean_dec(v_j_382_);
lean_dec(v_i_381_);
return v_res_383_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_pauliZ___closed__0(void){
_start:
{
lean_object* v___x_384_; lean_object* v___x_385_; 
v___x_384_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
v___x_385_ = lean_int_neg(v___x_384_);
return v___x_385_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pauliZ(lean_object* v_i_386_, lean_object* v_j_387_){
_start:
{
lean_object* v_zero_390_; uint8_t v_isZero_391_; 
v_zero_390_ = lean_unsigned_to_nat(0u);
v_isZero_391_ = lean_nat_dec_eq(v_i_386_, v_zero_390_);
if (v_isZero_391_ == 1)
{
uint8_t v_isZero_392_; 
v_isZero_392_ = lean_nat_dec_eq(v_j_387_, v_zero_390_);
if (v_isZero_392_ == 1)
{
lean_object* v___x_393_; 
v___x_393_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7, &lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7_once, _init_lp_FiniteQuantum_GroupParameter_instReprSubgroupType_repr___closed__7);
return v___x_393_;
}
else
{
lean_object* v_one_394_; lean_object* v_n_395_; uint8_t v_isZero_396_; 
v_one_394_ = lean_unsigned_to_nat(1u);
v_n_395_ = lean_nat_sub(v_j_387_, v_one_394_);
v_isZero_396_ = lean_nat_dec_eq(v_n_395_, v_zero_390_);
lean_dec(v_n_395_);
goto v___jp_388_;
}
}
else
{
lean_object* v_one_397_; lean_object* v_n_398_; uint8_t v_isZero_399_; uint8_t v_isZero_400_; 
v_one_397_ = lean_unsigned_to_nat(1u);
v_n_398_ = lean_nat_sub(v_i_386_, v_one_397_);
v_isZero_399_ = lean_nat_dec_eq(v_n_398_, v_zero_390_);
lean_dec(v_n_398_);
v_isZero_400_ = lean_nat_dec_eq(v_j_387_, v_zero_390_);
if (v_isZero_400_ == 1)
{
goto v___jp_388_;
}
else
{
lean_object* v_n_401_; uint8_t v_isZero_402_; lean_object* v___x_403_; 
v_n_401_ = lean_nat_sub(v_j_387_, v_one_397_);
v_isZero_402_ = lean_nat_dec_eq(v_n_401_, v_zero_390_);
lean_dec(v_n_401_);
v___x_403_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_pauliZ___closed__0, &lp_FiniteQuantum_GroupParameter_pauliZ___closed__0_once, _init_lp_FiniteQuantum_GroupParameter_pauliZ___closed__0);
return v___x_403_;
}
}
v___jp_388_:
{
lean_object* v___x_389_; 
v___x_389_ = lean_obj_once(&lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0, &lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0_once, _init_lp_FiniteQuantum_GroupParameter_pythRotNumerator___closed__0);
return v___x_389_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GroupParameter_pauliZ___boxed(lean_object* v_i_404_, lean_object* v_j_405_){
_start:
{
lean_object* v_res_406_; 
v_res_406_ = lp_FiniteQuantum_GroupParameter_pauliZ(v_i_404_, v_j_405_);
lean_dec(v_j_405_);
lean_dec(v_i_404_);
return v_res_406_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_inventoryTotalCount(void){
_start:
{
lean_object* v___x_409_; 
v___x_409_ = lean_unsigned_to_nat(18u);
return v___x_409_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_inventoryCarriedCount(void){
_start:
{
lean_object* v___x_410_; 
v___x_410_ = lean_unsigned_to_nat(3u);
return v___x_410_;
}
}
static lean_object* _init_lp_FiniteQuantum_GroupParameter_inventoryRefusedCount(void){
_start:
{
lean_object* v___x_411_; 
v___x_411_ = lean_unsigned_to_nat(15u);
return v___x_411_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_GroupParameter(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_GroupParameter_inventoryTotalCount = _init_lp_FiniteQuantum_GroupParameter_inventoryTotalCount();
lean_mark_persistent(lp_FiniteQuantum_GroupParameter_inventoryTotalCount);
lp_FiniteQuantum_GroupParameter_inventoryCarriedCount = _init_lp_FiniteQuantum_GroupParameter_inventoryCarriedCount();
lean_mark_persistent(lp_FiniteQuantum_GroupParameter_inventoryCarriedCount);
lp_FiniteQuantum_GroupParameter_inventoryRefusedCount = _init_lp_FiniteQuantum_GroupParameter_inventoryRefusedCount();
lean_mark_persistent(lp_FiniteQuantum_GroupParameter_inventoryRefusedCount);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
