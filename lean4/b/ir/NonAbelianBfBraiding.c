// Lean compiler output
// Module: NonAbelianBfBraiding
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
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_borromean3LoopCommutator___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_borromean3LoopCommutator(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_quantumDoubleTraceNorm(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_quantumDoubleTraceNorm___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_defectMass(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_defectMass___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_borromean3LoopCommutator___redArg(lean_object* v_alg_1_, lean_object* v_b1_2_, lean_object* v_b2_3_){
_start:
{
lean_object* v_mul_4_; lean_object* v_inv_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v_mul_4_ = lean_ctor_get(v_alg_1_, 0);
lean_inc_n(v_mul_4_, 3);
v_inv_5_ = lean_ctor_get(v_alg_1_, 1);
lean_inc_n(v_inv_5_, 2);
lean_dec_ref(v_alg_1_);
lean_inc(v_b2_3_);
lean_inc(v_b1_2_);
v___x_6_ = lean_apply_2(v_mul_4_, v_b1_2_, v_b2_3_);
v___x_7_ = lean_apply_1(v_inv_5_, v_b1_2_);
v___x_8_ = lean_apply_2(v_mul_4_, v___x_6_, v___x_7_);
v___x_9_ = lean_apply_1(v_inv_5_, v_b2_3_);
v___x_10_ = lean_apply_2(v_mul_4_, v___x_8_, v___x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_borromean3LoopCommutator(lean_object* v_G_11_, lean_object* v_alg_12_, lean_object* v_b1_13_, lean_object* v_b2_14_){
_start:
{
lean_object* v___x_15_; 
v___x_15_ = lp_FiniteQuantum_NonAbelianBfBraiding_borromean3LoopCommutator___redArg(v_alg_12_, v_b1_13_, v_b2_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_quantumDoubleTraceNorm(lean_object* v_re_16_, lean_object* v_im_17_){
_start:
{
lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; 
v___x_18_ = lean_nat_mul(v_re_16_, v_re_16_);
v___x_19_ = lean_nat_mul(v_im_17_, v_im_17_);
v___x_20_ = lean_nat_add(v___x_18_, v___x_19_);
lean_dec(v___x_19_);
lean_dec(v___x_18_);
return v___x_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_quantumDoubleTraceNorm___boxed(lean_object* v_re_21_, lean_object* v_im_22_){
_start:
{
lean_object* v_res_23_; 
v_res_23_ = lp_FiniteQuantum_NonAbelianBfBraiding_quantumDoubleTraceNorm(v_re_21_, v_im_22_);
lean_dec(v_im_22_);
lean_dec(v_re_21_);
return v_res_23_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_defectMass(lean_object* v_normVal_24_){
_start:
{
lean_object* v___x_25_; uint8_t v___x_26_; 
v___x_25_ = lean_unsigned_to_nat(0u);
v___x_26_ = lean_nat_dec_lt(v___x_25_, v_normVal_24_);
if (v___x_26_ == 0)
{
lean_object* v___x_27_; 
v___x_27_ = lean_unsigned_to_nat(1u);
return v___x_27_;
}
else
{
return v___x_25_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_NonAbelianBfBraiding_defectMass___boxed(lean_object* v_normVal_28_){
_start:
{
lean_object* v_res_29_; 
v_res_29_ = lp_FiniteQuantum_NonAbelianBfBraiding_defectMass(v_normVal_28_);
lean_dec(v_normVal_28_);
return v_res_29_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_NonAbelianBfBraiding(uint8_t builtin) {
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
