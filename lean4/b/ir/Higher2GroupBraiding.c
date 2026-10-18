// Lean compiler output
// Module: Higher2GroupBraiding
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
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
lean_object* lean_nat_abs(lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0;
static lean_once_cell_t lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_oneFormQuantumDoubleHolonomy(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_oneFormQuantumDoubleHolonomy___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherTwoDoubleHolonomy(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherTwoDoubleHolonomy___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherDefectMass(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherDefectMass___boxed(lean_object*);
static lean_object* _init_lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_obj_once(&lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0, &lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0_once, _init_lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0);
v___x_4_ = lean_int_neg(v___x_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy(uint8_t v_isTrivial_5_, uint8_t v_oddLinking_6_){
_start:
{
if (v_isTrivial_5_ == 0)
{
if (v_oddLinking_6_ == 0)
{
lean_object* v___x_7_; 
v___x_7_ = lean_obj_once(&lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0, &lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0_once, _init_lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0);
return v___x_7_;
}
else
{
lean_object* v___x_8_; 
v___x_8_ = lean_obj_once(&lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__1, &lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__1_once, _init_lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__1);
return v___x_8_;
}
}
else
{
lean_object* v___x_9_; 
v___x_9_ = lean_obj_once(&lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0, &lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0_once, _init_lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___closed__0);
return v___x_9_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy___boxed(lean_object* v_isTrivial_10_, lean_object* v_oddLinking_11_){
_start:
{
uint8_t v_isTrivial_boxed_12_; uint8_t v_oddLinking_boxed_13_; lean_object* v_res_14_; 
v_isTrivial_boxed_12_ = lean_unbox(v_isTrivial_10_);
v_oddLinking_boxed_13_ = lean_unbox(v_oddLinking_11_);
v_res_14_ = lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy(v_isTrivial_boxed_12_, v_oddLinking_boxed_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_oneFormQuantumDoubleHolonomy(uint8_t v_isTrivial_15_, uint8_t v_oddLinking_16_){
_start:
{
lean_object* v___x_17_; 
v___x_17_ = lp_FiniteQuantum_Higher2GroupBraiding_surfaceLoopHolonomy(v_isTrivial_15_, v_oddLinking_16_);
return v___x_17_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_oneFormQuantumDoubleHolonomy___boxed(lean_object* v_isTrivial_18_, lean_object* v_oddLinking_19_){
_start:
{
uint8_t v_isTrivial_boxed_20_; uint8_t v_oddLinking_boxed_21_; lean_object* v_res_22_; 
v_isTrivial_boxed_20_ = lean_unbox(v_isTrivial_18_);
v_oddLinking_boxed_21_ = lean_unbox(v_oddLinking_19_);
v_res_22_ = lp_FiniteQuantum_Higher2GroupBraiding_oneFormQuantumDoubleHolonomy(v_isTrivial_boxed_20_, v_oddLinking_boxed_21_);
return v_res_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherTwoDoubleHolonomy(lean_object* v_bareHol_23_){
_start:
{
lean_object* v___x_24_; lean_object* v___x_25_; 
v___x_24_ = lean_nat_abs(v_bareHol_23_);
v___x_25_ = lean_nat_mul(v___x_24_, v___x_24_);
lean_dec(v___x_24_);
return v___x_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherTwoDoubleHolonomy___boxed(lean_object* v_bareHol_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_FiniteQuantum_Higher2GroupBraiding_higherTwoDoubleHolonomy(v_bareHol_26_);
lean_dec(v_bareHol_26_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherDefectMass(lean_object* v_normVal_28_){
_start:
{
lean_object* v___x_29_; uint8_t v___x_30_; 
v___x_29_ = lean_unsigned_to_nat(0u);
v___x_30_ = lean_nat_dec_lt(v___x_29_, v_normVal_28_);
if (v___x_30_ == 0)
{
lean_object* v___x_31_; 
v___x_31_ = lean_unsigned_to_nat(1u);
return v___x_31_;
}
else
{
return v___x_29_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Higher2GroupBraiding_higherDefectMass___boxed(lean_object* v_normVal_32_){
_start:
{
lean_object* v_res_33_; 
v_res_33_ = lp_FiniteQuantum_Higher2GroupBraiding_higherDefectMass(v_normVal_32_);
lean_dec(v_normVal_32_);
return v_res_33_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_Higher2GroupBraiding(uint8_t builtin) {
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
