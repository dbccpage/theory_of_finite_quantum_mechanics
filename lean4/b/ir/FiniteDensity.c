// Lean compiler output
// Module: FiniteDensity
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_trace(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_trace___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_born__expected__numerator(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_born__expected__numerator___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_trace(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_trace___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_born__expected__numerator(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_born__expected__numerator___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_mix__eigenvalues(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_mix__eigenvalues___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_trace(lean_object* v_d_1_){
_start:
{
lean_object* v_lambda0_2_; lean_object* v_lambda1_3_; lean_object* v___x_4_; 
v_lambda0_2_ = lean_ctor_get(v_d_1_, 0);
v_lambda1_3_ = lean_ctor_get(v_d_1_, 1);
v___x_4_ = lean_nat_add(v_lambda0_2_, v_lambda1_3_);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_trace___boxed(lean_object* v_d_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_trace(v_d_5_);
lean_dec_ref(v_d_5_);
return v_res_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_born__expected__numerator(lean_object* v_d_7_, lean_object* v_e_8_){
_start:
{
lean_object* v_lambda0_9_; lean_object* v_lambda1_10_; lean_object* v_coeff0_11_; lean_object* v_coeff1_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; 
v_lambda0_9_ = lean_ctor_get(v_d_7_, 0);
v_lambda1_10_ = lean_ctor_get(v_d_7_, 1);
v_coeff0_11_ = lean_ctor_get(v_e_8_, 0);
v_coeff1_12_ = lean_ctor_get(v_e_8_, 1);
v___x_13_ = lean_nat_mul(v_lambda0_9_, v_coeff0_11_);
v___x_14_ = lean_nat_mul(v_lambda1_10_, v_coeff1_12_);
v___x_15_ = lean_nat_add(v___x_13_, v___x_14_);
lean_dec(v___x_14_);
lean_dec(v___x_13_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_born__expected__numerator___boxed(lean_object* v_d_16_, lean_object* v_e_17_){
_start:
{
lean_object* v_res_18_; 
v_res_18_ = lp_FiniteQuantum_FromPrimitiveDifferenceToQuantumMechanics_FiniteDensity_born__expected__numerator(v_d_16_, v_e_17_);
lean_dec_ref(v_e_17_);
lean_dec_ref(v_d_16_);
return v_res_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_trace(lean_object* v_d_19_){
_start:
{
lean_object* v_lambda0_20_; lean_object* v_lambda1_21_; lean_object* v___x_22_; 
v_lambda0_20_ = lean_ctor_get(v_d_19_, 0);
v_lambda1_21_ = lean_ctor_get(v_d_19_, 1);
v___x_22_ = lean_nat_add(v_lambda0_20_, v_lambda1_21_);
return v___x_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_trace___boxed(lean_object* v_d_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_FiniteQuantum_FiniteDensity_trace(v_d_23_);
lean_dec_ref(v_d_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_born__expected__numerator(lean_object* v_d_25_, lean_object* v_e_26_){
_start:
{
lean_object* v_lambda0_27_; lean_object* v_lambda1_28_; lean_object* v_coeff0_29_; lean_object* v_coeff1_30_; lean_object* v___x_31_; lean_object* v___x_32_; lean_object* v___x_33_; 
v_lambda0_27_ = lean_ctor_get(v_d_25_, 0);
v_lambda1_28_ = lean_ctor_get(v_d_25_, 1);
v_coeff0_29_ = lean_ctor_get(v_e_26_, 0);
v_coeff1_30_ = lean_ctor_get(v_e_26_, 1);
v___x_31_ = lean_nat_mul(v_lambda0_27_, v_coeff0_29_);
v___x_32_ = lean_nat_mul(v_lambda1_28_, v_coeff1_30_);
v___x_33_ = lean_nat_add(v___x_31_, v___x_32_);
lean_dec(v___x_32_);
lean_dec(v___x_31_);
return v___x_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_born__expected__numerator___boxed(lean_object* v_d_34_, lean_object* v_e_35_){
_start:
{
lean_object* v_res_36_; 
v_res_36_ = lp_FiniteQuantum_FiniteDensity_born__expected__numerator(v_d_34_, v_e_35_);
lean_dec_ref(v_e_35_);
lean_dec_ref(v_d_34_);
return v_res_36_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_mix__eigenvalues(lean_object* v_dA_37_, lean_object* v_dB_38_, lean_object* v_wA_39_, lean_object* v_wB_40_){
_start:
{
lean_object* v_lambda0_41_; lean_object* v_lambda1_42_; lean_object* v_lambda0_43_; lean_object* v_lambda1_44_; lean_object* v___x_45_; lean_object* v___x_46_; lean_object* v___x_47_; lean_object* v___x_48_; lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; 
v_lambda0_41_ = lean_ctor_get(v_dA_37_, 0);
v_lambda1_42_ = lean_ctor_get(v_dA_37_, 1);
v_lambda0_43_ = lean_ctor_get(v_dB_38_, 0);
v_lambda1_44_ = lean_ctor_get(v_dB_38_, 1);
v___x_45_ = lean_nat_mul(v_wA_39_, v_lambda0_41_);
v___x_46_ = lean_nat_mul(v_wB_40_, v_lambda0_43_);
v___x_47_ = lean_nat_add(v___x_45_, v___x_46_);
lean_dec(v___x_46_);
lean_dec(v___x_45_);
v___x_48_ = lean_nat_mul(v_wA_39_, v_lambda1_42_);
v___x_49_ = lean_nat_mul(v_wB_40_, v_lambda1_44_);
v___x_50_ = lean_nat_add(v___x_48_, v___x_49_);
lean_dec(v___x_49_);
lean_dec(v___x_48_);
v___x_51_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_51_, 0, v___x_47_);
lean_ctor_set(v___x_51_, 1, v___x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FiniteDensity_mix__eigenvalues___boxed(lean_object* v_dA_52_, lean_object* v_dB_53_, lean_object* v_wA_54_, lean_object* v_wB_55_){
_start:
{
lean_object* v_res_56_; 
v_res_56_ = lp_FiniteQuantum_FiniteDensity_mix__eigenvalues(v_dA_52_, v_dB_53_, v_wA_54_, v_wB_55_);
lean_dec(v_wB_55_);
lean_dec(v_wA_54_);
lean_dec_ref(v_dB_53_);
lean_dec_ref(v_dA_52_);
return v_res_56_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_FiniteDensity(uint8_t builtin) {
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
