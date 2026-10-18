// Lean compiler output
// Module: GleasonRationalPlane
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
lean_object* l_Nat_cast___at___00Dyadic_toRat_spec__0(lean_object*);
lean_object* l_Rat_mul(lean_object*, lean_object*);
uint8_t l_Rat_blt(lean_object*, lean_object*);
uint8_t l_instDecidableEqRat_decEq(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___boxed(lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(0u);
v___x_2_ = l_Nat_cast___at___00Dyadic_toRat_spec__0(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_unsigned_to_nat(1u);
v___x_4_ = l_Nat_cast___at___00Dyadic_toRat_spec__0(v___x_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay(lean_object* v_x_5_, lean_object* v_y_6_){
_start:
{
lean_object* v___x_7_; lean_object* v___x_8_; uint8_t v___x_9_; 
v___x_7_ = lean_obj_once(&lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__0, &lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__0_once, _init_lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__0);
lean_inc_ref(v_y_6_);
v___x_8_ = l_Rat_mul(v_x_5_, v_y_6_);
lean_inc_ref(v___x_8_);
v___x_9_ = l_Rat_blt(v___x_7_, v___x_8_);
if (v___x_9_ == 0)
{
uint8_t v___x_10_; 
v___x_10_ = l_Rat_blt(v___x_8_, v___x_7_);
if (v___x_10_ == 0)
{
uint8_t v___x_11_; 
v___x_11_ = l_instDecidableEqRat_decEq(v_y_6_, v___x_7_);
lean_dec_ref(v_y_6_);
if (v___x_11_ == 0)
{
return v___x_7_;
}
else
{
lean_object* v___x_12_; 
v___x_12_ = lean_obj_once(&lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1, &lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1_once, _init_lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1);
return v___x_12_;
}
}
else
{
lean_dec_ref(v_y_6_);
return v___x_7_;
}
}
else
{
lean_object* v___x_13_; 
lean_dec_ref(v___x_8_);
lean_dec_ref(v_y_6_);
v___x_13_ = lean_obj_once(&lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1, &lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1_once, _init_lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___closed__1);
return v___x_13_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay___boxed(lean_object* v_x_14_, lean_object* v_y_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_FiniteQm_GleasonRationalPlane_binaryRay(v_x_14_, v_y_15_);
lean_dec_ref(v_x_14_);
return v_res_16_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_GleasonRationalPlane(uint8_t builtin) {
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
