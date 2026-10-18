// Lean compiler output
// Module: MubMinorChart
// Imports: public import Init public meta import Init public import Mathlib.Data.Complex.Basic public import Mathlib.LinearAlgebra.Matrix.ConjTranspose public import Mathlib.LinearAlgebra.Matrix.Determinant.Basic public import Mathlib.LinearAlgebra.Matrix.NonsingularInverse public import Mathlib.Tactic.FinCases public import Mathlib.Tactic.NormNum public import Mathlib.Tactic.Ring public import Mathlib.Tactic.Linarith
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
lean_object* l_Fin_cases___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_mathlib_Matrix_submatrix___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__1(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__2(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__33(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_MUB_MinorChart_columns___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_MUB_MinorChart_columns___lam__0___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__0 = (const lean_object*)&lp_FiniteQuantum_MUB_MinorChart_columns___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_MUB_MinorChart_columns___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_MUB_MinorChart_columns___lam__1___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__1 = (const lean_object*)&lp_FiniteQuantum_MUB_MinorChart_columns___closed__1_value;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__2;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__3;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__4;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__5;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__6;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__7;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__8;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__9;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__10;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__11_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__11;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__12;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__13_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__13;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__14_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__14;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__15_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__15;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__16_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__16;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__17;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__18_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__18;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__19_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__19;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__20_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__20;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__21_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__21;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__22_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__22;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__23_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__23;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__24_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__24;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__25_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__25;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__26_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__26;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__27_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__27;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__28_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__28;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__29_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__29;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__30_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__30;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__31_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__31;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__32_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__32;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__33_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__33;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__34_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__34;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__35_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__35;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__36_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__36;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__37_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__37;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__38_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__38;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__39_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__39;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__40_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__40;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__41_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__41;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__42_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__42;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__43_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__43;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__44_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__44;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__45_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__45;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__46_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__46;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__47_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__47;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__48_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__48;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__49_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__49;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__50_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__50;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__51_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__51;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__52_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__52;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__53_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__53;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__54_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__54;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__55_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__55;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__56_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__56;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__57_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__57;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__58_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__58;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__59_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__59;
static lean_once_cell_t lp_FiniteQuantum_MUB_MinorChart_columns___closed__60_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___closed__60;
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_minor___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_minor___lam__0___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_MUB_MinorChart_minor___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_MUB_MinorChart_minor___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_MUB_MinorChart_minor___closed__0 = (const lean_object*)&lp_FiniteQuantum_MUB_MinorChart_minor___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_minor(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_firstRows(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__0(lean_object* v___y_1_, lean_object* v___y_2_){
_start:
{
lean_internal_panic_unreachable();
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__0___boxed(lean_object* v___y_3_, lean_object* v___y_4_){
_start:
{
lean_object* v_res_5_; 
v_res_5_ = lp_FiniteQuantum_MUB_MinorChart_columns___lam__0(v___y_3_, v___y_4_);
lean_dec(v___y_4_);
lean_dec(v___y_3_);
return v_res_5_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__1(lean_object* v___y_6_){
_start:
{
lean_internal_panic_unreachable();
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__1___boxed(lean_object* v___y_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_FiniteQuantum_MUB_MinorChart_columns___lam__1(v___y_7_);
lean_dec(v___y_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__2(lean_object* v___x_9_, lean_object* v___f_10_, lean_object* v___y_11_){
_start:
{
lean_object* v___x_12_; 
v___x_12_ = l_Fin_cases___redArg(v___x_9_, v___f_10_, v___y_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed(lean_object* v___x_13_, lean_object* v___f_14_, lean_object* v___y_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_MUB_MinorChart_columns___lam__2(v___x_13_, v___f_14_, v___y_15_);
lean_dec(v___y_15_);
lean_dec(v___x_13_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__33(lean_object* v___f_17_, lean_object* v___f_18_, lean_object* v___y_19_, lean_object* v___y_20_){
_start:
{
lean_object* v___x_507__overap_21_; lean_object* v___x_22_; 
v___x_507__overap_21_ = l_Fin_cases___redArg(v___f_17_, v___f_18_, v___y_19_);
v___x_22_ = lean_apply_1(v___x_507__overap_21_, v___y_20_);
return v___x_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed(lean_object* v___f_23_, lean_object* v___f_24_, lean_object* v___y_25_, lean_object* v___y_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_FiniteQuantum_MUB_MinorChart_columns___lam__33(v___f_23_, v___f_24_, v___y_25_, v___y_26_);
lean_dec(v___y_25_);
lean_dec_ref(v___f_23_);
return v_res_27_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2(void){
_start:
{
lean_object* v___x_30_; lean_object* v___x_31_; lean_object* v___x_32_; 
v___x_30_ = lean_unsigned_to_nat(6u);
v___x_31_ = lean_unsigned_to_nat(0u);
v___x_32_ = lean_nat_mod(v___x_31_, v___x_30_);
return v___x_32_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; 
v___x_33_ = lean_unsigned_to_nat(6u);
v___x_34_ = lean_unsigned_to_nat(1u);
v___x_35_ = lean_nat_mod(v___x_34_, v___x_33_);
return v___x_35_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4(void){
_start:
{
lean_object* v___x_36_; lean_object* v___x_37_; lean_object* v___x_38_; 
v___x_36_ = lean_unsigned_to_nat(6u);
v___x_37_ = lean_unsigned_to_nat(2u);
v___x_38_ = lean_nat_mod(v___x_37_, v___x_36_);
return v___x_38_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__5(void){
_start:
{
lean_object* v___f_39_; lean_object* v___x_40_; lean_object* v___f_41_; 
v___f_39_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_columns___closed__1));
v___x_40_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_41_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_41_, 0, v___x_40_);
lean_closure_set(v___f_41_, 1, v___f_39_);
return v___f_41_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__6(void){
_start:
{
lean_object* v___f_42_; lean_object* v___x_43_; lean_object* v___f_44_; 
v___f_42_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__5, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__5_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__5);
v___x_43_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_44_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_44_, 0, v___x_43_);
lean_closure_set(v___f_44_, 1, v___f_42_);
return v___f_44_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__7(void){
_start:
{
lean_object* v___f_45_; lean_object* v___x_46_; lean_object* v___f_47_; 
v___f_45_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__6, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__6_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__6);
v___x_46_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_47_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_47_, 0, v___x_46_);
lean_closure_set(v___f_47_, 1, v___f_45_);
return v___f_47_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__8(void){
_start:
{
lean_object* v___x_48_; lean_object* v___x_49_; lean_object* v___x_50_; 
v___x_48_ = lean_unsigned_to_nat(6u);
v___x_49_ = lean_unsigned_to_nat(3u);
v___x_50_ = lean_nat_mod(v___x_49_, v___x_48_);
return v___x_50_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__9(void){
_start:
{
lean_object* v___f_51_; lean_object* v___x_52_; lean_object* v___f_53_; 
v___f_51_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_columns___closed__1));
v___x_52_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__8, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__8_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__8);
v___f_53_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_53_, 0, v___x_52_);
lean_closure_set(v___f_53_, 1, v___f_51_);
return v___f_53_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__10(void){
_start:
{
lean_object* v___f_54_; lean_object* v___x_55_; lean_object* v___f_56_; 
v___f_54_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__9, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__9_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__9);
v___x_55_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_56_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_56_, 0, v___x_55_);
lean_closure_set(v___f_56_, 1, v___f_54_);
return v___f_56_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__11(void){
_start:
{
lean_object* v___f_57_; lean_object* v___x_58_; lean_object* v___f_59_; 
v___f_57_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__10, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__10_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__10);
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_59_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_59_, 0, v___x_58_);
lean_closure_set(v___f_59_, 1, v___f_57_);
return v___f_59_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__12(void){
_start:
{
lean_object* v___f_60_; lean_object* v___x_61_; lean_object* v___f_62_; 
v___f_60_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__9, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__9_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__9);
v___x_61_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_62_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_62_, 0, v___x_61_);
lean_closure_set(v___f_62_, 1, v___f_60_);
return v___f_62_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__13(void){
_start:
{
lean_object* v___f_63_; lean_object* v___x_64_; lean_object* v___f_65_; 
v___f_63_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__12, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__12_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__12);
v___x_64_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_65_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_65_, 0, v___x_64_);
lean_closure_set(v___f_65_, 1, v___f_63_);
return v___f_65_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__14(void){
_start:
{
lean_object* v___f_66_; lean_object* v___x_67_; lean_object* v___f_68_; 
v___f_66_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__12, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__12_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__12);
v___x_67_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_68_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_68_, 0, v___x_67_);
lean_closure_set(v___f_68_, 1, v___f_66_);
return v___f_68_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__15(void){
_start:
{
lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; 
v___x_69_ = lean_unsigned_to_nat(6u);
v___x_70_ = lean_unsigned_to_nat(4u);
v___x_71_ = lean_nat_mod(v___x_70_, v___x_69_);
return v___x_71_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__16(void){
_start:
{
lean_object* v___f_72_; lean_object* v___x_73_; lean_object* v___f_74_; 
v___f_72_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_columns___closed__1));
v___x_73_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__15, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__15_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__15);
v___f_74_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_74_, 0, v___x_73_);
lean_closure_set(v___f_74_, 1, v___f_72_);
return v___f_74_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__17(void){
_start:
{
lean_object* v___f_75_; lean_object* v___x_76_; lean_object* v___f_77_; 
v___f_75_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__16, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__16_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__16);
v___x_76_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__8, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__8_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__8);
v___f_77_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_77_, 0, v___x_76_);
lean_closure_set(v___f_77_, 1, v___f_75_);
return v___f_77_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__18(void){
_start:
{
lean_object* v___f_78_; lean_object* v___x_79_; lean_object* v___f_80_; 
v___f_78_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__17, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__17_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__17);
v___x_79_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_80_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_80_, 0, v___x_79_);
lean_closure_set(v___f_80_, 1, v___f_78_);
return v___f_80_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__19(void){
_start:
{
lean_object* v___f_81_; lean_object* v___x_82_; lean_object* v___f_83_; 
v___f_81_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__17, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__17_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__17);
v___x_82_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_83_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_83_, 0, v___x_82_);
lean_closure_set(v___f_83_, 1, v___f_81_);
return v___f_83_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__20(void){
_start:
{
lean_object* v___f_84_; lean_object* v___x_85_; lean_object* v___f_86_; 
v___f_84_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__17, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__17_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__17);
v___x_85_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_86_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_86_, 0, v___x_85_);
lean_closure_set(v___f_86_, 1, v___f_84_);
return v___f_86_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__21(void){
_start:
{
lean_object* v___f_87_; lean_object* v___x_88_; lean_object* v___f_89_; 
v___f_87_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__16, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__16_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__16);
v___x_88_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_89_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_89_, 0, v___x_88_);
lean_closure_set(v___f_89_, 1, v___f_87_);
return v___f_89_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__22(void){
_start:
{
lean_object* v___f_90_; lean_object* v___x_91_; lean_object* v___f_92_; 
v___f_90_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__21, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__21_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__21);
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_92_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_92_, 0, v___x_91_);
lean_closure_set(v___f_92_, 1, v___f_90_);
return v___f_92_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__23(void){
_start:
{
lean_object* v___f_93_; lean_object* v___x_94_; lean_object* v___f_95_; 
v___f_93_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__21, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__21_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__21);
v___x_94_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_95_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_95_, 0, v___x_94_);
lean_closure_set(v___f_95_, 1, v___f_93_);
return v___f_95_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__24(void){
_start:
{
lean_object* v___f_96_; lean_object* v___x_97_; lean_object* v___f_98_; 
v___f_96_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__16, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__16_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__16);
v___x_97_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_98_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_98_, 0, v___x_97_);
lean_closure_set(v___f_98_, 1, v___f_96_);
return v___f_98_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__25(void){
_start:
{
lean_object* v___f_99_; lean_object* v___x_100_; lean_object* v___f_101_; 
v___f_99_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__24, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__24_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__24);
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_101_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_101_, 0, v___x_100_);
lean_closure_set(v___f_101_, 1, v___f_99_);
return v___f_101_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__26(void){
_start:
{
lean_object* v___x_102_; lean_object* v___x_103_; lean_object* v___x_104_; 
v___x_102_ = lean_unsigned_to_nat(6u);
v___x_103_ = lean_unsigned_to_nat(5u);
v___x_104_ = lean_nat_mod(v___x_103_, v___x_102_);
return v___x_104_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__27(void){
_start:
{
lean_object* v___f_105_; lean_object* v___x_106_; lean_object* v___f_107_; 
v___f_105_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_columns___closed__1));
v___x_106_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__26, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__26_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__26);
v___f_107_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_107_, 0, v___x_106_);
lean_closure_set(v___f_107_, 1, v___f_105_);
return v___f_107_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__28(void){
_start:
{
lean_object* v___f_108_; lean_object* v___x_109_; lean_object* v___f_110_; 
v___f_108_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__27, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__27_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__27);
v___x_109_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_110_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_110_, 0, v___x_109_);
lean_closure_set(v___f_110_, 1, v___f_108_);
return v___f_110_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__29(void){
_start:
{
lean_object* v___f_111_; lean_object* v___x_112_; lean_object* v___f_113_; 
v___f_111_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__28, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__28_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__28);
v___x_112_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_113_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_113_, 0, v___x_112_);
lean_closure_set(v___f_113_, 1, v___f_111_);
return v___f_113_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__30(void){
_start:
{
lean_object* v___f_114_; lean_object* v___x_115_; lean_object* v___f_116_; 
v___f_114_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__27, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__27_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__27);
v___x_115_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_116_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_116_, 0, v___x_115_);
lean_closure_set(v___f_116_, 1, v___f_114_);
return v___f_116_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__31(void){
_start:
{
lean_object* v___f_117_; lean_object* v___x_118_; lean_object* v___f_119_; 
v___f_117_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__30, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__30_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__30);
v___x_118_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_119_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_119_, 0, v___x_118_);
lean_closure_set(v___f_119_, 1, v___f_117_);
return v___f_119_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__32(void){
_start:
{
lean_object* v___f_120_; lean_object* v___x_121_; lean_object* v___f_122_; 
v___f_120_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__30, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__30_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__30);
v___x_121_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_122_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_122_, 0, v___x_121_);
lean_closure_set(v___f_122_, 1, v___f_120_);
return v___f_122_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__33(void){
_start:
{
lean_object* v___f_123_; lean_object* v___x_124_; lean_object* v___f_125_; 
v___f_123_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__27, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__27_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__27);
v___x_124_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__8, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__8_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__8);
v___f_125_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_125_, 0, v___x_124_);
lean_closure_set(v___f_125_, 1, v___f_123_);
return v___f_125_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__34(void){
_start:
{
lean_object* v___f_126_; lean_object* v___x_127_; lean_object* v___f_128_; 
v___f_126_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__33, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__33_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__33);
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_128_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_128_, 0, v___x_127_);
lean_closure_set(v___f_128_, 1, v___f_126_);
return v___f_128_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__35(void){
_start:
{
lean_object* v___f_129_; lean_object* v___x_130_; lean_object* v___f_131_; 
v___f_129_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__33, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__33_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__33);
v___x_130_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_131_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_131_, 0, v___x_130_);
lean_closure_set(v___f_131_, 1, v___f_129_);
return v___f_131_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__36(void){
_start:
{
lean_object* v___f_132_; lean_object* v___x_133_; lean_object* v___f_134_; 
v___f_132_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__33, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__33_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__33);
v___x_133_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_134_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_134_, 0, v___x_133_);
lean_closure_set(v___f_134_, 1, v___f_132_);
return v___f_134_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__37(void){
_start:
{
lean_object* v___f_135_; lean_object* v___x_136_; lean_object* v___f_137_; 
v___f_135_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__27, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__27_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__27);
v___x_136_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__15, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__15_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__15);
v___f_137_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_137_, 0, v___x_136_);
lean_closure_set(v___f_137_, 1, v___f_135_);
return v___f_137_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__38(void){
_start:
{
lean_object* v___f_138_; lean_object* v___x_139_; lean_object* v___f_140_; 
v___f_138_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__37, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__37_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__37);
v___x_139_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__8, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__8_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__8);
v___f_140_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_140_, 0, v___x_139_);
lean_closure_set(v___f_140_, 1, v___f_138_);
return v___f_140_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__39(void){
_start:
{
lean_object* v___f_141_; lean_object* v___f_142_; lean_object* v___f_143_; 
v___f_141_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_columns___closed__0));
v___f_142_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__38, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__38_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__38);
v___f_143_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_143_, 0, v___f_142_);
lean_closure_set(v___f_143_, 1, v___f_141_);
return v___f_143_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__40(void){
_start:
{
lean_object* v___f_144_; lean_object* v___x_145_; lean_object* v___f_146_; 
v___f_144_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__37, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__37_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__37);
v___x_145_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__4, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__4_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__4);
v___f_146_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_146_, 0, v___x_145_);
lean_closure_set(v___f_146_, 1, v___f_144_);
return v___f_146_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__41(void){
_start:
{
lean_object* v___f_147_; lean_object* v___f_148_; lean_object* v___f_149_; 
v___f_147_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__39, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__39_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__39);
v___f_148_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__40, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__40_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__40);
v___f_149_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_149_, 0, v___f_148_);
lean_closure_set(v___f_149_, 1, v___f_147_);
return v___f_149_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__42(void){
_start:
{
lean_object* v___f_150_; lean_object* v___f_151_; lean_object* v___f_152_; 
v___f_150_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__41, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__41_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__41);
v___f_151_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__34, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__34_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__34);
v___f_152_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_152_, 0, v___f_151_);
lean_closure_set(v___f_152_, 1, v___f_150_);
return v___f_152_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__43(void){
_start:
{
lean_object* v___f_153_; lean_object* v___f_154_; lean_object* v___f_155_; 
v___f_153_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__42, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__42_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__42);
v___f_154_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__20, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__20_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__20);
v___f_155_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_155_, 0, v___f_154_);
lean_closure_set(v___f_155_, 1, v___f_153_);
return v___f_155_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__44(void){
_start:
{
lean_object* v___f_156_; lean_object* v___x_157_; lean_object* v___f_158_; 
v___f_156_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__37, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__37_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__37);
v___x_157_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__3, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__3_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__3);
v___f_158_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_158_, 0, v___x_157_);
lean_closure_set(v___f_158_, 1, v___f_156_);
return v___f_158_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__45(void){
_start:
{
lean_object* v___f_159_; lean_object* v___f_160_; lean_object* v___f_161_; 
v___f_159_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__43, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__43_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__43);
v___f_160_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__44, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__44_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__44);
v___f_161_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_161_, 0, v___f_160_);
lean_closure_set(v___f_161_, 1, v___f_159_);
return v___f_161_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__46(void){
_start:
{
lean_object* v___f_162_; lean_object* v___f_163_; lean_object* v___f_164_; 
v___f_162_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__45, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__45_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__45);
v___f_163_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__35, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__35_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__35);
v___f_164_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_164_, 0, v___f_163_);
lean_closure_set(v___f_164_, 1, v___f_162_);
return v___f_164_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__47(void){
_start:
{
lean_object* v___f_165_; lean_object* v___f_166_; lean_object* v___f_167_; 
v___f_165_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__46, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__46_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__46);
v___f_166_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__19, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__19_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__19);
v___f_167_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_167_, 0, v___f_166_);
lean_closure_set(v___f_167_, 1, v___f_165_);
return v___f_167_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__48(void){
_start:
{
lean_object* v___f_168_; lean_object* v___f_169_; lean_object* v___f_170_; 
v___f_168_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__47, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__47_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__47);
v___f_169_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__32, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__32_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__32);
v___f_170_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_170_, 0, v___f_169_);
lean_closure_set(v___f_170_, 1, v___f_168_);
return v___f_170_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__49(void){
_start:
{
lean_object* v___f_171_; lean_object* v___f_172_; lean_object* v___f_173_; 
v___f_171_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__48, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__48_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__48);
v___f_172_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__22, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__22_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__22);
v___f_173_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_173_, 0, v___f_172_);
lean_closure_set(v___f_173_, 1, v___f_171_);
return v___f_173_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__50(void){
_start:
{
lean_object* v___f_174_; lean_object* v___f_175_; lean_object* v___f_176_; 
v___f_174_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__49, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__49_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__49);
v___f_175_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__13, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__13_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__13);
v___f_176_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_176_, 0, v___f_175_);
lean_closure_set(v___f_176_, 1, v___f_174_);
return v___f_176_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__51(void){
_start:
{
lean_object* v___f_177_; lean_object* v___x_178_; lean_object* v___f_179_; 
v___f_177_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__37, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__37_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__37);
v___x_178_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__2, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__2_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__2);
v___f_179_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__2___boxed), 3, 2);
lean_closure_set(v___f_179_, 0, v___x_178_);
lean_closure_set(v___f_179_, 1, v___f_177_);
return v___f_179_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__52(void){
_start:
{
lean_object* v___f_180_; lean_object* v___f_181_; lean_object* v___f_182_; 
v___f_180_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__50, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__50_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__50);
v___f_181_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__51, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__51_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__51);
v___f_182_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_182_, 0, v___f_181_);
lean_closure_set(v___f_182_, 1, v___f_180_);
return v___f_182_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__53(void){
_start:
{
lean_object* v___f_183_; lean_object* v___f_184_; lean_object* v___f_185_; 
v___f_183_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__52, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__52_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__52);
v___f_184_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__36, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__36_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__36);
v___f_185_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_185_, 0, v___f_184_);
lean_closure_set(v___f_185_, 1, v___f_183_);
return v___f_185_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__54(void){
_start:
{
lean_object* v___f_186_; lean_object* v___f_187_; lean_object* v___f_188_; 
v___f_186_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__53, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__53_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__53);
v___f_187_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__18, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__18_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__18);
v___f_188_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_188_, 0, v___f_187_);
lean_closure_set(v___f_188_, 1, v___f_186_);
return v___f_188_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__55(void){
_start:
{
lean_object* v___f_189_; lean_object* v___f_190_; lean_object* v___f_191_; 
v___f_189_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__54, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__54_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__54);
v___f_190_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__31, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__31_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__31);
v___f_191_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_191_, 0, v___f_190_);
lean_closure_set(v___f_191_, 1, v___f_189_);
return v___f_191_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__56(void){
_start:
{
lean_object* v___f_192_; lean_object* v___f_193_; lean_object* v___f_194_; 
v___f_192_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__55, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__55_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__55);
v___f_193_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__23, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__23_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__23);
v___f_194_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_194_, 0, v___f_193_);
lean_closure_set(v___f_194_, 1, v___f_192_);
return v___f_194_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__57(void){
_start:
{
lean_object* v___f_195_; lean_object* v___f_196_; lean_object* v___f_197_; 
v___f_195_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__56, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__56_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__56);
v___f_196_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__14, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__14_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__14);
v___f_197_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_197_, 0, v___f_196_);
lean_closure_set(v___f_197_, 1, v___f_195_);
return v___f_197_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__58(void){
_start:
{
lean_object* v___f_198_; lean_object* v___f_199_; lean_object* v___f_200_; 
v___f_198_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__57, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__57_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__57);
v___f_199_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__29, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__29_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__29);
v___f_200_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_200_, 0, v___f_199_);
lean_closure_set(v___f_200_, 1, v___f_198_);
return v___f_200_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__59(void){
_start:
{
lean_object* v___f_201_; lean_object* v___f_202_; lean_object* v___f_203_; 
v___f_201_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__58, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__58_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__58);
v___f_202_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__25, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__25_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__25);
v___f_203_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_203_, 0, v___f_202_);
lean_closure_set(v___f_203_, 1, v___f_201_);
return v___f_203_;
}
}
static lean_object* _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__60(void){
_start:
{
lean_object* v___f_204_; lean_object* v___f_205_; lean_object* v___f_206_; 
v___f_204_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__59, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__59_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__59);
v___f_205_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__11, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__11_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__11);
v___f_206_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___lam__33___boxed), 4, 2);
lean_closure_set(v___f_206_, 0, v___f_205_);
lean_closure_set(v___f_206_, 1, v___f_204_);
return v___f_206_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns(lean_object* v_a_207_, lean_object* v_a_208_){
_start:
{
lean_object* v___f_209_; lean_object* v___f_210_; lean_object* v___x_165__overap_211_; lean_object* v___x_212_; 
v___f_209_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__7, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__7_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__7);
v___f_210_ = lean_obj_once(&lp_FiniteQuantum_MUB_MinorChart_columns___closed__60, &lp_FiniteQuantum_MUB_MinorChart_columns___closed__60_once, _init_lp_FiniteQuantum_MUB_MinorChart_columns___closed__60);
v___x_165__overap_211_ = l_Fin_cases___redArg(v___f_209_, v___f_210_, v_a_207_);
v___x_212_ = lean_apply_1(v___x_165__overap_211_, v_a_208_);
return v___x_212_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_columns___boxed(lean_object* v_a_213_, lean_object* v_a_214_){
_start:
{
lean_object* v_res_215_; 
v_res_215_ = lp_FiniteQuantum_MUB_MinorChart_columns(v_a_213_, v_a_214_);
lean_dec(v_a_213_);
return v_res_215_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_minor___lam__0(lean_object* v___y_216_){
_start:
{
lean_inc(v___y_216_);
return v___y_216_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_minor___lam__0___boxed(lean_object* v___y_217_){
_start:
{
lean_object* v_res_218_; 
v_res_218_ = lp_FiniteQuantum_MUB_MinorChart_minor___lam__0(v___y_217_);
lean_dec(v___y_217_);
return v_res_218_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_minor(lean_object* v_A_220_, lean_object* v_s_221_, lean_object* v_a_222_, lean_object* v_a_223_){
_start:
{
lean_object* v___f_224_; lean_object* v___x_225_; lean_object* v___x_226_; 
v___f_224_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_minor___closed__0));
v___x_225_ = lean_alloc_closure((void*)(lp_FiniteQuantum_MUB_MinorChart_columns___boxed), 2, 1);
lean_closure_set(v___x_225_, 0, v_s_221_);
v___x_226_ = lp_mathlib_Matrix_submatrix___redArg(v_A_220_, v___f_224_, v___x_225_, v_a_222_, v_a_223_);
return v___x_226_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_MUB_MinorChart_firstRows(lean_object* v_H_227_, lean_object* v_a_228_, lean_object* v_a_229_){
_start:
{
lean_object* v___f_230_; lean_object* v___x_231_; 
v___f_230_ = ((lean_object*)(lp_FiniteQuantum_MUB_MinorChart_minor___closed__0));
v___x_231_ = lp_mathlib_Matrix_submatrix___redArg(v_H_227_, v___f_230_, v___f_230_, v_a_228_, v_a_229_);
return v___x_231_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Complex_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_LinearAlgebra_Matrix_ConjTranspose(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_LinearAlgebra_Matrix_Determinant_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_LinearAlgebra_Matrix_NonsingularInverse(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_FinCases(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_NormNum(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_Ring(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_Linarith(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_MubMinorChart(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Complex_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_LinearAlgebra_Matrix_ConjTranspose(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_LinearAlgebra_Matrix_Determinant_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_LinearAlgebra_Matrix_NonsingularInverse(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_FinCases(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_NormNum(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_Ring(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_Linarith(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
