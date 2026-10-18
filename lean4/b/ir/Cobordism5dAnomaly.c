// Lean compiler output
// Module: Cobordism5dAnomaly
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
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_nat_mod(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_nu5(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_nu5___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0;
static lean_once_cell_t lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_cobordismDefectMass(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_cobordismDefectMass___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusDoubledTrace(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusDoubledTrace___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_nu5(lean_object* v_c_1_){
_start:
{
lean_object* v_postnikov__arf_2_; lean_object* v_mixed__gravitational_3_; lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; 
v_postnikov__arf_2_ = lean_ctor_get(v_c_1_, 0);
v_mixed__gravitational_3_ = lean_ctor_get(v_c_1_, 1);
v___x_4_ = lean_nat_add(v_postnikov__arf_2_, v_mixed__gravitational_3_);
v___x_5_ = lean_unsigned_to_nat(2u);
v___x_6_ = lean_nat_mod(v___x_4_, v___x_5_);
lean_dec(v___x_4_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_nu5___boxed(lean_object* v_c_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_FiniteQuantum_Cobordism5dAnomaly_nu5(v_c_7_);
lean_dec_ref(v_c_7_);
return v_res_8_;
}
}
static lean_object* _init_lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0(void){
_start:
{
lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_9_ = lean_unsigned_to_nat(1u);
v___x_10_ = lean_nat_to_int(v___x_9_);
return v___x_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__1(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_11_ = lean_obj_once(&lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0, &lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0_once, _init_lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0);
v___x_12_ = lean_int_neg(v___x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy(lean_object* v_nu_13_){
_start:
{
lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; uint8_t v___x_17_; 
v___x_14_ = lean_unsigned_to_nat(2u);
v___x_15_ = lean_nat_mod(v_nu_13_, v___x_14_);
v___x_16_ = lean_unsigned_to_nat(0u);
v___x_17_ = lean_nat_dec_eq(v___x_15_, v___x_16_);
lean_dec(v___x_15_);
if (v___x_17_ == 0)
{
lean_object* v___x_18_; 
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__1, &lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__1_once, _init_lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__1);
return v___x_18_;
}
else
{
lean_object* v___x_19_; 
v___x_19_ = lean_obj_once(&lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0, &lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0_once, _init_lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0);
return v___x_19_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___boxed(lean_object* v_nu_20_){
_start:
{
lean_object* v_res_21_; 
v_res_21_ = lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy(v_nu_20_);
lean_dec(v_nu_20_);
return v_res_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_cobordismDefectMass(lean_object* v_hol_22_){
_start:
{
lean_object* v___x_23_; uint8_t v___x_24_; 
v___x_23_ = lean_obj_once(&lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0, &lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0_once, _init_lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy___closed__0);
v___x_24_ = lean_int_dec_eq(v_hol_22_, v___x_23_);
if (v___x_24_ == 0)
{
lean_object* v___x_25_; 
v___x_25_ = lean_unsigned_to_nat(2u);
return v___x_25_;
}
else
{
lean_object* v___x_26_; 
v___x_26_ = lean_unsigned_to_nat(0u);
return v___x_26_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_cobordismDefectMass___boxed(lean_object* v_hol_27_){
_start:
{
lean_object* v_res_28_; 
v_res_28_ = lp_FiniteQuantum_Cobordism5dAnomaly_cobordismDefectMass(v_hol_27_);
lean_dec(v_hol_27_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusDoubledTrace(lean_object* v_nu_29_){
_start:
{
lean_object* v___x_30_; 
v___x_30_ = lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusHolonomy(v_nu_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusDoubledTrace___boxed(lean_object* v_nu_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_FiniteQuantum_Cobordism5dAnomaly_mappingTorusDoubledTrace(v_nu_31_);
lean_dec(v_nu_31_);
return v_res_32_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_Cobordism5dAnomaly(uint8_t builtin) {
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
