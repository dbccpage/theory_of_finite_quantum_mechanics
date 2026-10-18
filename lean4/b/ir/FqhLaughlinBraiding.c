// Lean compiler output
// Module: FqhLaughlinBraiding
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FqhLaughlinBraiding_laughlin__m;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FqhLaughlinBraiding_monodromyPhaseNumerator;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FqhLaughlinBraiding_fqhCochainCurvature;
static lean_object* _init_lp_FiniteQuantum_FqhLaughlinBraiding_laughlin__m(void){
_start:
{
lean_object* v___x_1_; 
v___x_1_ = lean_unsigned_to_nat(3u);
return v___x_1_;
}
}
static lean_object* _init_lp_FiniteQuantum_FqhLaughlinBraiding_monodromyPhaseNumerator(void){
_start:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(2u);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FqhLaughlinBraiding_fqhCochainCurvature(void){
_start:
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(2u);
return v___x_3_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_FqhLaughlinBraiding(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FqhLaughlinBraiding_laughlin__m = _init_lp_FiniteQuantum_FqhLaughlinBraiding_laughlin__m();
lean_mark_persistent(lp_FiniteQuantum_FqhLaughlinBraiding_laughlin__m);
lp_FiniteQuantum_FqhLaughlinBraiding_monodromyPhaseNumerator = _init_lp_FiniteQuantum_FqhLaughlinBraiding_monodromyPhaseNumerator();
lean_mark_persistent(lp_FiniteQuantum_FqhLaughlinBraiding_monodromyPhaseNumerator);
lp_FiniteQuantum_FqhLaughlinBraiding_fqhCochainCurvature = _init_lp_FiniteQuantum_FqhLaughlinBraiding_fqhCochainCurvature();
lean_mark_persistent(lp_FiniteQuantum_FqhLaughlinBraiding_fqhCochainCurvature);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
