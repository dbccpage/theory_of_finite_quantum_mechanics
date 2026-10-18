// Lean compiler output
// Module: BfLinkedFluxBraiding
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
lean_object* lean_int_mul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BfLinkedFluxBraiding_monodromyNumerator(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BfLinkedFluxBraiding_monodromyNumerator___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BfLinkedFluxBraiding_level2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BfLinkedFluxBraiding_level3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_BfLinkedFluxBraiding_monodromyNumerator(lean_object* v_q_1_, lean_object* v_p_2_, lean_object* v_lk_3_){
_start:
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; 
v___x_4_ = lean_nat_to_int(v_q_1_);
v___x_5_ = lean_nat_to_int(v_p_2_);
v___x_6_ = lean_int_mul(v___x_4_, v___x_5_);
lean_dec(v___x_5_);
lean_dec(v___x_4_);
v___x_7_ = lean_int_mul(v___x_6_, v_lk_3_);
lean_dec(v___x_6_);
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BfLinkedFluxBraiding_monodromyNumerator___boxed(lean_object* v_q_8_, lean_object* v_p_9_, lean_object* v_lk_10_){
_start:
{
lean_object* v_res_11_; 
v_res_11_ = lp_FiniteQuantum_BfLinkedFluxBraiding_monodromyNumerator(v_q_8_, v_p_9_, v_lk_10_);
lean_dec(v_lk_10_);
return v_res_11_;
}
}
static lean_object* _init_lp_FiniteQuantum_BfLinkedFluxBraiding_level2(void){
_start:
{
lean_object* v___x_12_; 
v___x_12_ = lean_unsigned_to_nat(2u);
return v___x_12_;
}
}
static lean_object* _init_lp_FiniteQuantum_BfLinkedFluxBraiding_level3(void){
_start:
{
lean_object* v___x_13_; 
v___x_13_ = lean_unsigned_to_nat(3u);
return v___x_13_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_BfLinkedFluxBraiding(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_BfLinkedFluxBraiding_level2 = _init_lp_FiniteQuantum_BfLinkedFluxBraiding_level2();
lean_mark_persistent(lp_FiniteQuantum_BfLinkedFluxBraiding_level2);
lp_FiniteQuantum_BfLinkedFluxBraiding_level3 = _init_lp_FiniteQuantum_BfLinkedFluxBraiding_level3();
lean_mark_persistent(lp_FiniteQuantum_BfLinkedFluxBraiding_level3);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
