// Lean compiler output
// Module: BornNormalization
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
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_trace(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_trace___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__1___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__00(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__00___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__11(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__11___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__01(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__01___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__10(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__10___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_trace(lean_object* v_00_u03c1_1_){
_start:
{
lean_object* v_a_2_; lean_object* v_d_3_; lean_object* v___x_4_; 
v_a_2_ = lean_ctor_get(v_00_u03c1_1_, 0);
v_d_3_ = lean_ctor_get(v_00_u03c1_1_, 1);
v___x_4_ = lean_nat_add(v_a_2_, v_d_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_trace___boxed(lean_object* v_00_u03c1_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_FiniteQuantum_BornNormalization_trace(v_00_u03c1_5_);
lean_dec_ref(v_00_u03c1_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__0(lean_object* v_00_u03c1_7_, lean_object* v_povm_8_){
_start:
{
lean_object* v_e0__a_9_; lean_object* v_e0__d_10_; lean_object* v_a_11_; lean_object* v_d_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; 
v_e0__a_9_ = lean_ctor_get(v_povm_8_, 0);
v_e0__d_10_ = lean_ctor_get(v_povm_8_, 1);
v_a_11_ = lean_ctor_get(v_00_u03c1_7_, 0);
v_d_12_ = lean_ctor_get(v_00_u03c1_7_, 1);
v___x_13_ = lean_nat_mul(v_e0__a_9_, v_a_11_);
v___x_14_ = lean_nat_mul(v_e0__d_10_, v_d_12_);
v___x_15_ = lean_nat_add(v___x_13_, v___x_14_);
lean_dec(v___x_14_);
lean_dec(v___x_13_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__0___boxed(lean_object* v_00_u03c1_16_, lean_object* v_povm_17_){
_start:
{
lean_object* v_res_18_; 
v_res_18_ = lp_FiniteQuantum_BornNormalization_born__outcome__0(v_00_u03c1_16_, v_povm_17_);
lean_dec_ref(v_povm_17_);
lean_dec_ref(v_00_u03c1_16_);
return v_res_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__1(lean_object* v_00_u03c1_19_, lean_object* v_povm_20_){
_start:
{
lean_object* v_e1__a_21_; lean_object* v_e1__d_22_; lean_object* v_a_23_; lean_object* v_d_24_; lean_object* v___x_25_; lean_object* v___x_26_; lean_object* v___x_27_; 
v_e1__a_21_ = lean_ctor_get(v_povm_20_, 2);
v_e1__d_22_ = lean_ctor_get(v_povm_20_, 3);
v_a_23_ = lean_ctor_get(v_00_u03c1_19_, 0);
v_d_24_ = lean_ctor_get(v_00_u03c1_19_, 1);
v___x_25_ = lean_nat_mul(v_e1__a_21_, v_a_23_);
v___x_26_ = lean_nat_mul(v_e1__d_22_, v_d_24_);
v___x_27_ = lean_nat_add(v___x_25_, v___x_26_);
lean_dec(v___x_26_);
lean_dec(v___x_25_);
return v___x_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_born__outcome__1___boxed(lean_object* v_00_u03c1_28_, lean_object* v_povm_29_){
_start:
{
lean_object* v_res_30_; 
v_res_30_ = lp_FiniteQuantum_BornNormalization_born__outcome__1(v_00_u03c1_28_, v_povm_29_);
lean_dec_ref(v_povm_29_);
lean_dec_ref(v_00_u03c1_28_);
return v_res_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__00(lean_object* v_00_u03c8_31_){
_start:
{
lean_object* v_c0_32_; lean_object* v___x_33_; 
v_c0_32_ = lean_ctor_get(v_00_u03c8_31_, 0);
v___x_33_ = lean_int_mul(v_c0_32_, v_c0_32_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__00___boxed(lean_object* v_00_u03c8_34_){
_start:
{
lean_object* v_res_35_; 
v_res_35_ = lp_FiniteQuantum_BornNormalization_proj__00(v_00_u03c8_34_);
lean_dec_ref(v_00_u03c8_34_);
return v_res_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__11(lean_object* v_00_u03c8_36_){
_start:
{
lean_object* v_c1_37_; lean_object* v___x_38_; 
v_c1_37_ = lean_ctor_get(v_00_u03c8_36_, 1);
v___x_38_ = lean_int_mul(v_c1_37_, v_c1_37_);
return v___x_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__11___boxed(lean_object* v_00_u03c8_39_){
_start:
{
lean_object* v_res_40_; 
v_res_40_ = lp_FiniteQuantum_BornNormalization_proj__11(v_00_u03c8_39_);
lean_dec_ref(v_00_u03c8_39_);
return v_res_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__01(lean_object* v_00_u03c8_41_){
_start:
{
lean_object* v_c0_42_; lean_object* v_c1_43_; lean_object* v___x_44_; 
v_c0_42_ = lean_ctor_get(v_00_u03c8_41_, 0);
v_c1_43_ = lean_ctor_get(v_00_u03c8_41_, 1);
v___x_44_ = lean_int_mul(v_c0_42_, v_c1_43_);
return v___x_44_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__01___boxed(lean_object* v_00_u03c8_45_){
_start:
{
lean_object* v_res_46_; 
v_res_46_ = lp_FiniteQuantum_BornNormalization_proj__01(v_00_u03c8_45_);
lean_dec_ref(v_00_u03c8_45_);
return v_res_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__10(lean_object* v_00_u03c8_47_){
_start:
{
lean_object* v_c0_48_; lean_object* v_c1_49_; lean_object* v___x_50_; 
v_c0_48_ = lean_ctor_get(v_00_u03c8_47_, 0);
v_c1_49_ = lean_ctor_get(v_00_u03c8_47_, 1);
v___x_50_ = lean_int_mul(v_c1_49_, v_c0_48_);
return v___x_50_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_BornNormalization_proj__10___boxed(lean_object* v_00_u03c8_51_){
_start:
{
lean_object* v_res_52_; 
v_res_52_ = lp_FiniteQuantum_BornNormalization_proj__10(v_00_u03c8_51_);
lean_dec_ref(v_00_u03c8_51_);
return v_res_52_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_BornNormalization(uint8_t builtin) {
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
