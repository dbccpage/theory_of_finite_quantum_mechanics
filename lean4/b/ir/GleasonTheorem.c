// Lean compiler output
// Module: GleasonTheorem
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
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_GleasonTheorem_eval__quad___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_GleasonTheorem_eval__quad___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_GleasonTheorem_eval__quad(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_GleasonTheorem_eval__quad___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_GleasonTheorem_eval__quad___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(2u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GleasonTheorem_eval__quad(lean_object* v_q_3_, lean_object* v_x_4_, lean_object* v_y_5_){
_start:
{
lean_object* v_a_6_; lean_object* v_b_7_; lean_object* v_c_8_; lean_object* v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; 
v_a_6_ = lean_ctor_get(v_q_3_, 0);
v_b_7_ = lean_ctor_get(v_q_3_, 1);
v_c_8_ = lean_ctor_get(v_q_3_, 2);
v___x_9_ = lean_int_mul(v_x_4_, v_x_4_);
v___x_10_ = lean_int_mul(v_a_6_, v___x_9_);
lean_dec(v___x_9_);
v___x_11_ = lean_obj_once(&lp_FiniteQuantum_GleasonTheorem_eval__quad___closed__0, &lp_FiniteQuantum_GleasonTheorem_eval__quad___closed__0_once, _init_lp_FiniteQuantum_GleasonTheorem_eval__quad___closed__0);
v___x_12_ = lean_int_mul(v___x_11_, v_b_7_);
v___x_13_ = lean_int_mul(v_x_4_, v_y_5_);
v___x_14_ = lean_int_mul(v___x_12_, v___x_13_);
lean_dec(v___x_13_);
lean_dec(v___x_12_);
v___x_15_ = lean_int_add(v___x_10_, v___x_14_);
lean_dec(v___x_14_);
lean_dec(v___x_10_);
v___x_16_ = lean_int_mul(v_y_5_, v_y_5_);
v___x_17_ = lean_int_mul(v_c_8_, v___x_16_);
lean_dec(v___x_16_);
v___x_18_ = lean_int_add(v___x_15_, v___x_17_);
lean_dec(v___x_17_);
lean_dec(v___x_15_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_GleasonTheorem_eval__quad___boxed(lean_object* v_q_19_, lean_object* v_x_20_, lean_object* v_y_21_){
_start:
{
lean_object* v_res_22_; 
v_res_22_ = lp_FiniteQuantum_GleasonTheorem_eval__quad(v_q_19_, v_x_20_, v_y_21_);
lean_dec(v_y_21_);
lean_dec(v_x_20_);
lean_dec_ref(v_q_19_);
return v_res_22_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_GleasonTheorem(uint8_t builtin) {
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
