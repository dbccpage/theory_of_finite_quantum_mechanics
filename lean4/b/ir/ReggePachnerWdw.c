// Lean compiler output
// Module: ReggePachnerWdw
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
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_sumDeficits(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_sumDeficits___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_evaluateH__Wdw(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_evaluateH__Wdw___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_sumDeficits(lean_object* v_x_1_){
_start:
{
if (lean_obj_tag(v_x_1_) == 0)
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
else
{
lean_object* v_head_3_; lean_object* v_tail_4_; lean_object* v___x_5_; lean_object* v___x_6_; 
v_head_3_ = lean_ctor_get(v_x_1_, 0);
v_tail_4_ = lean_ctor_get(v_x_1_, 1);
v___x_5_ = lp_FiniteQuantum_ReggePachnerWdw_sumDeficits(v_tail_4_);
v___x_6_ = lean_nat_add(v_head_3_, v___x_5_);
lean_dec(v___x_5_);
return v___x_6_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_sumDeficits___boxed(lean_object* v_x_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_FiniteQuantum_ReggePachnerWdw_sumDeficits(v_x_7_);
lean_dec(v_x_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_evaluateH__Wdw(lean_object* v_v_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_FiniteQuantum_ReggePachnerWdw_sumDeficits(v_v_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_ReggePachnerWdw_evaluateH__Wdw___boxed(lean_object* v_v_11_){
_start:
{
lean_object* v_res_12_; 
v_res_12_ = lp_FiniteQuantum_ReggePachnerWdw_evaluateH__Wdw(v_v_11_);
lean_dec(v_v_11_);
return v_res_12_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_ReggePachnerWdw(uint8_t builtin) {
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
