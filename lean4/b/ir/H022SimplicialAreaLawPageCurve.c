// Lean compiler output
// Module: H022SimplicialAreaLawPageCurve
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
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_pow(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_bulk__microstates(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_bulk__microstates___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_boundary__microstates(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_boundary__microstates___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SchmidtRankCeiling_schmidt__rank__bound(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SchmidtRankCeiling_schmidt__rank__bound___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_CombinatorialPageCurve_page__entropy__4x(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_CombinatorialPageCurve_page__entropy__4x___boxed(lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(4u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_unsigned_to_nat(2u);
v___x_4_ = lean_nat_to_int(v___x_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area(lean_object* v_N_5_, lean_object* v_M__int_6_){
_start:
{
lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_7_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__0);
v___x_8_ = lean_nat_to_int(v_N_5_);
v___x_9_ = lean_int_mul(v___x_7_, v___x_8_);
lean_dec(v___x_8_);
v___x_10_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H022_SimplicialAreaLaw_boundary__area___closed__1);
v___x_11_ = lean_nat_to_int(v_M__int_6_);
v___x_12_ = lean_int_mul(v___x_10_, v___x_11_);
lean_dec(v___x_11_);
v___x_13_ = lean_int_sub(v___x_9_, v___x_12_);
lean_dec(v___x_12_);
lean_dec(v___x_9_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_bulk__microstates(lean_object* v_d_14_, lean_object* v_N_15_){
_start:
{
lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; 
v___x_16_ = lean_unsigned_to_nat(4u);
v___x_17_ = lean_nat_mul(v___x_16_, v_N_15_);
v___x_18_ = lean_nat_pow(v_d_14_, v___x_17_);
lean_dec(v___x_17_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_bulk__microstates___boxed(lean_object* v_d_19_, lean_object* v_N_20_){
_start:
{
lean_object* v_res_21_; 
v_res_21_ = lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_bulk__microstates(v_d_19_, v_N_20_);
lean_dec(v_N_20_);
lean_dec(v_d_19_);
return v_res_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_boundary__microstates(lean_object* v_d_22_, lean_object* v_A_23_){
_start:
{
lean_object* v___x_24_; 
v___x_24_ = lean_nat_pow(v_d_22_, v_A_23_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_boundary__microstates___boxed(lean_object* v_d_25_, lean_object* v_A_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_FiniteQuantum_FableHilbertWalk20260819_H022_MicrostateProjection_boundary__microstates(v_d_25_, v_A_26_);
lean_dec(v_A_26_);
lean_dec(v_d_25_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SchmidtRankCeiling_schmidt__rank__bound(lean_object* v_d_28_, lean_object* v_A__B_29_, lean_object* v_A__R_30_){
_start:
{
uint8_t v___x_31_; 
v___x_31_ = lean_nat_dec_le(v_A__B_29_, v_A__R_30_);
if (v___x_31_ == 0)
{
lean_object* v___x_32_; 
v___x_32_ = lean_nat_pow(v_d_28_, v_A__R_30_);
return v___x_32_;
}
else
{
lean_object* v___x_33_; 
v___x_33_ = lean_nat_pow(v_d_28_, v_A__B_29_);
return v___x_33_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_SchmidtRankCeiling_schmidt__rank__bound___boxed(lean_object* v_d_34_, lean_object* v_A__B_35_, lean_object* v_A__R_36_){
_start:
{
lean_object* v_res_37_; 
v_res_37_ = lp_FiniteQuantum_FableHilbertWalk20260819_H022_SchmidtRankCeiling_schmidt__rank__bound(v_d_34_, v_A__B_35_, v_A__R_36_);
lean_dec(v_A__R_36_);
lean_dec(v_A__B_35_);
lean_dec(v_d_34_);
return v_res_37_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_CombinatorialPageCurve_page__entropy__4x(lean_object* v_A__B_38_, lean_object* v_A__R_39_){
_start:
{
uint8_t v___x_40_; 
v___x_40_ = lean_nat_dec_le(v_A__B_38_, v_A__R_39_);
if (v___x_40_ == 0)
{
lean_inc(v_A__R_39_);
return v_A__R_39_;
}
else
{
lean_inc(v_A__B_38_);
return v_A__B_38_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H022_CombinatorialPageCurve_page__entropy__4x___boxed(lean_object* v_A__B_41_, lean_object* v_A__R_42_){
_start:
{
lean_object* v_res_43_; 
v_res_43_ = lp_FiniteQuantum_FableHilbertWalk20260819_H022_CombinatorialPageCurve_page__entropy__4x(v_A__B_41_, v_A__R_42_);
lean_dec(v_A__R_42_);
lean_dec(v_A__B_41_);
return v_res_43_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H022SimplicialAreaLawPageCurve(uint8_t builtin) {
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
