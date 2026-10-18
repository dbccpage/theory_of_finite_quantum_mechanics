// Lean compiler output
// Module: CochainWindow
// Imports: public import Init public meta import Init public import PrimitiveDifference
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CochainWindow_repair___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CochainWindow_repair(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CochainWindow_repair___redArg(lean_object* v_window_1_, lean_object* v_omega_2_, lean_object* v_alpha_3_){
_start:
{
lean_object* v_c1_4_; lean_object* v_d0_5_; lean_object* v_add_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v_c1_4_ = lean_ctor_get(v_window_1_, 1);
lean_inc_ref(v_c1_4_);
v_d0_5_ = lean_ctor_get(v_window_1_, 3);
lean_inc(v_d0_5_);
lean_dec_ref(v_window_1_);
v_add_6_ = lean_ctor_get(v_c1_4_, 1);
lean_inc(v_add_6_);
lean_dec_ref(v_c1_4_);
v___x_7_ = lean_apply_1(v_d0_5_, v_alpha_3_);
v___x_8_ = lean_apply_2(v_add_6_, v_omega_2_, v___x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CochainWindow_repair(lean_object* v_C0_9_, lean_object* v_C1_10_, lean_object* v_C2_11_, lean_object* v_window_12_, lean_object* v_omega_13_, lean_object* v_alpha_14_){
_start:
{
lean_object* v___x_15_; 
v___x_15_ = lp_FiniteQuantum_OmegaCore_CochainWindow_repair___redArg(v_window_12_, v_omega_13_, v_alpha_14_);
return v___x_15_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveDifference(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_CochainWindow(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveDifference(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
