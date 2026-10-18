// Lean compiler output
// Module: H003ReversibilityGate
// Imports: public import Init public meta import Init public import HWKernel
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
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggle(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggle___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggleRev___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggle___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggleRev___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggleRev___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggleRev = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggleRev___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H003_collapse(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H003_collapse___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggle(uint8_t v_q_1_){
_start:
{
if (v_q_1_ == 0)
{
uint8_t v___x_2_; 
v___x_2_ = 1;
return v___x_2_;
}
else
{
uint8_t v___x_3_; 
v___x_3_ = 0;
return v___x_3_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggle___boxed(lean_object* v_q_4_){
_start:
{
uint8_t v_q_boxed_5_; uint8_t v_res_6_; lean_object* v_r_7_; 
v_q_boxed_5_ = lean_unbox(v_q_4_);
v_res_6_ = lp_FiniteQuantum_FableHilbertWalk20260819_H003_toggle(v_q_boxed_5_);
v_r_7_ = lean_box(v_res_6_);
return v_r_7_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H003_collapse(uint8_t v_x_10_){
_start:
{
uint8_t v___x_11_; 
v___x_11_ = 0;
return v___x_11_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H003_collapse___boxed(lean_object* v_x_12_){
_start:
{
uint8_t v_x_4__boxed_13_; uint8_t v_res_14_; lean_object* v_r_15_; 
v_x_4__boxed_13_ = lean_unbox(v_x_12_);
v_res_14_ = lp_FiniteQuantum_FableHilbertWalk20260819_H003_collapse(v_x_4__boxed_13_);
v_r_15_ = lean_box(v_res_14_);
return v_r_15_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_HWKernel(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
