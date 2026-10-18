// Lean compiler output
// Module: T4CharacterRemainder
// Imports: public import Init public meta import Init public import Std
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
lean_object* lean_string_length(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_emod(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_charEval(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_charEval___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary_decEq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary_decEq___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__0_value;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "remainderCharacters"};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__1 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__1_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__1_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__2 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__3 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__3_value;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__4 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__5 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__5_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__3_value),((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__5_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__6 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__6_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__7;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__8 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__8_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__8_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__9 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__9_value;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "znSoldAsU1"};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__10 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__10_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__10_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__11 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__11_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__12;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "piFromExactQ"};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__13 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__13_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__13_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__14 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__14_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__15;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "authorityEffectNone"};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__16 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__16_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__16_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__17 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__17_value;
static const lean_string_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__18 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__18_value;
static lean_once_cell_t lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__19_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__19;
static lean_once_cell_t lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__20_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__20;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__21 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__21_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__18_value)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__22 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__22_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OvernightT4_instReprScopeBoundary___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary___closed__0 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary = (const lean_object*)&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_OvernightT4_scopeBoundary___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 0, 0, 1, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_OvernightT4_scopeBoundary___closed__0 = (const lean_object*)&lp_FiniteQuantum_OvernightT4_scopeBoundary___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OvernightT4_scopeBoundary = (const lean_object*)&lp_FiniteQuantum_OvernightT4_scopeBoundary___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_charEval(lean_object* v_r_1_, lean_object* v_k_2_, lean_object* v_m_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; 
v___x_4_ = lean_int_mul(v_k_2_, v_r_1_);
v___x_5_ = lean_int_emod(v___x_4_, v_m_3_);
lean_dec(v___x_4_);
return v___x_5_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_charEval___boxed(lean_object* v_r_6_, lean_object* v_k_7_, lean_object* v_m_8_){
_start:
{
lean_object* v_res_9_; 
v_res_9_ = lp_FiniteQuantum_OvernightT4_charEval(v_r_6_, v_k_7_, v_m_8_);
lean_dec(v_m_8_);
lean_dec(v_k_7_);
lean_dec(v_r_6_);
return v_res_9_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary_decEq(lean_object* v_x_10_, lean_object* v_x_11_){
_start:
{
uint8_t v_remainderCharacters_12_; uint8_t v_znSoldAsU1_13_; uint8_t v_piFromExactQ_14_; uint8_t v_authorityEffectNone_15_; uint8_t v_remainderCharacters_16_; uint8_t v_znSoldAsU1_17_; uint8_t v_piFromExactQ_18_; uint8_t v_authorityEffectNone_19_; 
v_remainderCharacters_12_ = lean_ctor_get_uint8(v_x_10_, 0);
v_znSoldAsU1_13_ = lean_ctor_get_uint8(v_x_10_, 1);
v_piFromExactQ_14_ = lean_ctor_get_uint8(v_x_10_, 2);
v_authorityEffectNone_15_ = lean_ctor_get_uint8(v_x_10_, 3);
v_remainderCharacters_16_ = lean_ctor_get_uint8(v_x_11_, 0);
v_znSoldAsU1_17_ = lean_ctor_get_uint8(v_x_11_, 1);
v_piFromExactQ_18_ = lean_ctor_get_uint8(v_x_11_, 2);
v_authorityEffectNone_19_ = lean_ctor_get_uint8(v_x_11_, 3);
if (v_remainderCharacters_12_ == 0)
{
if (v_remainderCharacters_16_ == 0)
{
goto v___jp_23_;
}
else
{
return v_remainderCharacters_12_;
}
}
else
{
if (v_remainderCharacters_16_ == 0)
{
return v_remainderCharacters_16_;
}
else
{
goto v___jp_23_;
}
}
v___jp_20_:
{
if (v_authorityEffectNone_15_ == 0)
{
if (v_authorityEffectNone_19_ == 0)
{
uint8_t v___x_21_; 
v___x_21_ = 1;
return v___x_21_;
}
else
{
return v_authorityEffectNone_15_;
}
}
else
{
return v_authorityEffectNone_19_;
}
}
v___jp_22_:
{
if (v_piFromExactQ_14_ == 0)
{
if (v_piFromExactQ_18_ == 0)
{
goto v___jp_20_;
}
else
{
return v_piFromExactQ_14_;
}
}
else
{
if (v_piFromExactQ_18_ == 0)
{
return v_piFromExactQ_18_;
}
else
{
goto v___jp_20_;
}
}
}
v___jp_23_:
{
if (v_znSoldAsU1_13_ == 0)
{
if (v_znSoldAsU1_17_ == 0)
{
goto v___jp_22_;
}
else
{
return v_znSoldAsU1_13_;
}
}
else
{
if (v_znSoldAsU1_17_ == 0)
{
return v_znSoldAsU1_17_;
}
else
{
goto v___jp_22_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary_decEq___boxed(lean_object* v_x_24_, lean_object* v_x_25_){
_start:
{
uint8_t v_res_26_; lean_object* v_r_27_; 
v_res_26_ = lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary_decEq(v_x_24_, v_x_25_);
lean_dec_ref(v_x_25_);
lean_dec_ref(v_x_24_);
v_r_27_ = lean_box(v_res_26_);
return v_r_27_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary(lean_object* v_x_28_, lean_object* v_x_29_){
_start:
{
uint8_t v___x_30_; 
v___x_30_ = lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary_decEq(v_x_28_, v_x_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary___boxed(lean_object* v_x_31_, lean_object* v_x_32_){
_start:
{
uint8_t v_res_33_; lean_object* v_r_34_; 
v_res_33_ = lp_FiniteQuantum_OvernightT4_instDecidableEqScopeBoundary(v_x_31_, v_x_32_);
lean_dec_ref(v_x_32_);
lean_dec_ref(v_x_31_);
v_r_34_ = lean_box(v_res_33_);
return v_r_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_48_ = lean_unsigned_to_nat(23u);
v___x_49_ = lean_nat_to_int(v___x_48_);
return v___x_49_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__12(void){
_start:
{
lean_object* v___x_56_; lean_object* v___x_57_; 
v___x_56_ = lean_unsigned_to_nat(14u);
v___x_57_ = lean_nat_to_int(v___x_56_);
return v___x_57_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__15(void){
_start:
{
lean_object* v___x_61_; lean_object* v___x_62_; 
v___x_61_ = lean_unsigned_to_nat(16u);
v___x_62_ = lean_nat_to_int(v___x_61_);
return v___x_62_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__19(void){
_start:
{
lean_object* v___x_67_; lean_object* v___x_68_; 
v___x_67_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__0));
v___x_68_ = lean_string_length(v___x_67_);
return v___x_68_;
}
}
static lean_object* _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__20(void){
_start:
{
lean_object* v___x_69_; lean_object* v___x_70_; 
v___x_69_ = lean_obj_once(&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__19, &lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__19_once, _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__19);
v___x_70_ = lean_nat_to_int(v___x_69_);
return v___x_70_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg(lean_object* v_x_75_){
_start:
{
uint8_t v_remainderCharacters_76_; uint8_t v_znSoldAsU1_77_; uint8_t v_piFromExactQ_78_; uint8_t v_authorityEffectNone_79_; lean_object* v___x_80_; lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; uint8_t v___x_85_; lean_object* v___x_86_; lean_object* v___x_87_; lean_object* v___x_88_; lean_object* v___x_89_; lean_object* v___x_90_; lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; lean_object* v___x_94_; lean_object* v___x_95_; lean_object* v___x_96_; lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; lean_object* v___x_100_; lean_object* v___x_101_; lean_object* v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; lean_object* v___x_105_; lean_object* v___x_106_; lean_object* v___x_107_; lean_object* v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; lean_object* v___x_113_; lean_object* v___x_114_; lean_object* v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; lean_object* v___x_120_; lean_object* v___x_121_; lean_object* v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; lean_object* v___x_125_; 
v_remainderCharacters_76_ = lean_ctor_get_uint8(v_x_75_, 0);
v_znSoldAsU1_77_ = lean_ctor_get_uint8(v_x_75_, 1);
v_piFromExactQ_78_ = lean_ctor_get_uint8(v_x_75_, 2);
v_authorityEffectNone_79_ = lean_ctor_get_uint8(v_x_75_, 3);
v___x_80_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__5));
v___x_81_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__6));
v___x_82_ = lean_obj_once(&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__7, &lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__7_once, _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__7);
v___x_83_ = l_Bool_repr___redArg(v_remainderCharacters_76_);
v___x_84_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_84_, 0, v___x_82_);
lean_ctor_set(v___x_84_, 1, v___x_83_);
v___x_85_ = 0;
v___x_86_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_86_, 0, v___x_84_);
lean_ctor_set_uint8(v___x_86_, sizeof(void*)*1, v___x_85_);
v___x_87_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_87_, 0, v___x_81_);
lean_ctor_set(v___x_87_, 1, v___x_86_);
v___x_88_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__9));
v___x_89_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_89_, 0, v___x_87_);
lean_ctor_set(v___x_89_, 1, v___x_88_);
v___x_90_ = lean_box(1);
v___x_91_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_91_, 0, v___x_89_);
lean_ctor_set(v___x_91_, 1, v___x_90_);
v___x_92_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__11));
v___x_93_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_93_, 0, v___x_91_);
lean_ctor_set(v___x_93_, 1, v___x_92_);
v___x_94_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_94_, 0, v___x_93_);
lean_ctor_set(v___x_94_, 1, v___x_80_);
v___x_95_ = lean_obj_once(&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__12, &lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__12_once, _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__12);
v___x_96_ = l_Bool_repr___redArg(v_znSoldAsU1_77_);
v___x_97_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_97_, 0, v___x_95_);
lean_ctor_set(v___x_97_, 1, v___x_96_);
v___x_98_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_98_, 0, v___x_97_);
lean_ctor_set_uint8(v___x_98_, sizeof(void*)*1, v___x_85_);
v___x_99_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_99_, 0, v___x_94_);
lean_ctor_set(v___x_99_, 1, v___x_98_);
v___x_100_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_100_, 0, v___x_99_);
lean_ctor_set(v___x_100_, 1, v___x_88_);
v___x_101_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_101_, 0, v___x_100_);
lean_ctor_set(v___x_101_, 1, v___x_90_);
v___x_102_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__14));
v___x_103_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_103_, 0, v___x_101_);
lean_ctor_set(v___x_103_, 1, v___x_102_);
v___x_104_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_104_, 0, v___x_103_);
lean_ctor_set(v___x_104_, 1, v___x_80_);
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__15, &lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__15_once, _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__15);
v___x_106_ = l_Bool_repr___redArg(v_piFromExactQ_78_);
v___x_107_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_107_, 0, v___x_105_);
lean_ctor_set(v___x_107_, 1, v___x_106_);
v___x_108_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_108_, 0, v___x_107_);
lean_ctor_set_uint8(v___x_108_, sizeof(void*)*1, v___x_85_);
v___x_109_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_109_, 0, v___x_104_);
lean_ctor_set(v___x_109_, 1, v___x_108_);
v___x_110_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_110_, 0, v___x_109_);
lean_ctor_set(v___x_110_, 1, v___x_88_);
v___x_111_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_111_, 0, v___x_110_);
lean_ctor_set(v___x_111_, 1, v___x_90_);
v___x_112_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__17));
v___x_113_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_113_, 0, v___x_111_);
lean_ctor_set(v___x_113_, 1, v___x_112_);
v___x_114_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_114_, 0, v___x_113_);
lean_ctor_set(v___x_114_, 1, v___x_80_);
v___x_115_ = l_Bool_repr___redArg(v_authorityEffectNone_79_);
v___x_116_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_116_, 0, v___x_82_);
lean_ctor_set(v___x_116_, 1, v___x_115_);
v___x_117_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_117_, 0, v___x_116_);
lean_ctor_set_uint8(v___x_117_, sizeof(void*)*1, v___x_85_);
v___x_118_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_118_, 0, v___x_114_);
lean_ctor_set(v___x_118_, 1, v___x_117_);
v___x_119_ = lean_obj_once(&lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__20, &lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__20_once, _init_lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__20);
v___x_120_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__21));
v___x_121_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_121_, 0, v___x_120_);
lean_ctor_set(v___x_121_, 1, v___x_118_);
v___x_122_ = ((lean_object*)(lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___closed__22));
v___x_123_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_123_, 0, v___x_121_);
lean_ctor_set(v___x_123_, 1, v___x_122_);
v___x_124_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_124_, 0, v___x_119_);
lean_ctor_set(v___x_124_, 1, v___x_123_);
v___x_125_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_125_, 0, v___x_124_);
lean_ctor_set_uint8(v___x_125_, sizeof(void*)*1, v___x_85_);
return v___x_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg___boxed(lean_object* v_x_126_){
_start:
{
lean_object* v_res_127_; 
v_res_127_ = lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg(v_x_126_);
lean_dec_ref(v_x_126_);
return v_res_127_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr(lean_object* v_x_128_, lean_object* v_prec_129_){
_start:
{
lean_object* v___x_130_; 
v___x_130_ = lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___redArg(v_x_128_);
return v___x_130_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr___boxed(lean_object* v_x_131_, lean_object* v_prec_132_){
_start:
{
lean_object* v_res_133_; 
v_res_133_ = lp_FiniteQuantum_OvernightT4_instReprScopeBoundary_repr(v_x_131_, v_prec_132_);
lean_dec(v_prec_132_);
lean_dec_ref(v_x_131_);
return v_res_133_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Std(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_T4CharacterRemainder(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Std(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
