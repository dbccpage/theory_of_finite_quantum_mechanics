// Lean compiler output
// Module: FibonacciAnyonBraiding
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
LEAN_EXPORT lean_object* lp_po023_FibonacciAnyonBraiding_commutatorHolonomy___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_po023_FibonacciAnyonBraiding_commutatorHolonomy(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_po023_FibonacciAnyonBraiding_leakageMassNumerator;
LEAN_EXPORT lean_object* lp_po023_FibonacciAnyonBraiding_commutatorHolonomy___redArg(lean_object* v_B_1_){
_start:
{
lean_object* v_mul_2_; lean_object* v_inv_3_; lean_object* v_s1_4_; lean_object* v_s2_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v_mul_2_ = lean_ctor_get(v_B_1_, 0);
lean_inc_n(v_mul_2_, 3);
v_inv_3_ = lean_ctor_get(v_B_1_, 1);
lean_inc_n(v_inv_3_, 2);
v_s1_4_ = lean_ctor_get(v_B_1_, 3);
lean_inc_n(v_s1_4_, 2);
v_s2_5_ = lean_ctor_get(v_B_1_, 4);
lean_inc_n(v_s2_5_, 2);
lean_dec_ref(v_B_1_);
v___x_6_ = lean_apply_2(v_mul_2_, v_s1_4_, v_s2_5_);
v___x_7_ = lean_apply_1(v_inv_3_, v_s1_4_);
v___x_8_ = lean_apply_2(v_mul_2_, v___x_6_, v___x_7_);
v___x_9_ = lean_apply_1(v_inv_3_, v_s2_5_);
v___x_10_ = lean_apply_2(v_mul_2_, v___x_8_, v___x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_po023_FibonacciAnyonBraiding_commutatorHolonomy(lean_object* v_G_11_, lean_object* v_B_12_){
_start:
{
lean_object* v___x_13_; 
v___x_13_ = lp_po023_FibonacciAnyonBraiding_commutatorHolonomy___redArg(v_B_12_);
return v___x_13_;
}
}
static lean_object* _init_lp_po023_FibonacciAnyonBraiding_leakageMassNumerator(void){
_start:
{
lean_object* v___x_14_; 
v___x_14_ = lean_unsigned_to_nat(618u);
return v___x_14_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
void lean_initialize_runtime_module();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_po023_FibonacciAnyonBraiding(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize_runtime_module();
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_po023_FibonacciAnyonBraiding_leakageMassNumerator = _init_lp_po023_FibonacciAnyonBraiding_leakageMassNumerator();
lean_mark_persistent(lp_po023_FibonacciAnyonBraiding_leakageMassNumerator);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
