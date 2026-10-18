// Lean compiler output
// Module: H010InterferenceNonDescent
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H008PhaseBlindPresentation public import H009PhaseFiber
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind___redArg(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_mix(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_mix___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_readout(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_readout___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_psi2__mutated(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_psi2__mutated___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iWeights(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iWeights___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iMix(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iMix___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iReadout(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iReadout___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_mix(lean_object* v_v_1_, uint8_t v_q_2_){
_start:
{
uint8_t v___x_3_; 
v___x_3_ = 1;
if (v_q_2_ == 0)
{
lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v___x_4_ = lean_box(v_q_2_);
lean_inc_ref(v_v_1_);
v___x_5_ = lean_apply_1(v_v_1_, v___x_4_);
v___x_6_ = lean_box(v___x_3_);
v___x_7_ = lean_apply_1(v_v_1_, v___x_6_);
v___x_8_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(v___x_5_, v___x_7_);
lean_dec_ref(v___x_5_);
return v___x_8_;
}
else
{
uint8_t v___x_9_; lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; 
v___x_9_ = 0;
v___x_10_ = lean_box(v___x_9_);
lean_inc_ref(v_v_1_);
v___x_11_ = lean_apply_1(v_v_1_, v___x_10_);
v___x_12_ = lean_box(v___x_3_);
v___x_13_ = lean_apply_1(v_v_1_, v___x_12_);
v___x_14_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_13_);
v___x_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gadd(v___x_11_, v___x_14_);
lean_dec_ref(v___x_11_);
return v___x_15_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_mix___boxed(lean_object* v_v_16_, lean_object* v_q_17_){
_start:
{
uint8_t v_q_boxed_18_; lean_object* v_res_19_; 
v_q_boxed_18_ = lean_unbox(v_q_17_);
v_res_19_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_mix(v_v_16_, v_q_boxed_18_);
return v_res_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_readout(lean_object* v_v_20_, uint8_t v_a_21_){
_start:
{
lean_object* v___x_22_; lean_object* v___x_23_; lean_object* v___x_24_; 
v___x_22_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H010_mix___boxed), 2, 1);
lean_closure_set(v___x_22_, 0, v_v_20_);
v___x_23_ = lean_box(v_a_21_);
v___x_24_ = lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind___redArg(v___x_22_, v___x_23_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_readout___boxed(lean_object* v_v_25_, lean_object* v_a_26_){
_start:
{
uint8_t v_a_5__boxed_27_; lean_object* v_res_28_; 
v_a_5__boxed_27_ = lean_unbox(v_a_26_);
v_res_28_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_readout(v_v_25_, v_a_5__boxed_27_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_psi2__mutated(uint8_t v_q_29_){
_start:
{
lean_object* v___x_30_; 
v___x_30_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_psi2__mutated___boxed(lean_object* v_q_31_){
_start:
{
uint8_t v_q_boxed_32_; lean_object* v_res_33_; 
v_q_boxed_32_ = lean_unbox(v_q_31_);
v_res_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_psi2__mutated(v_q_boxed_32_);
return v_res_33_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0(void){
_start:
{
lean_object* v___x_34_; lean_object* v___x_35_; 
v___x_34_ = lean_unsigned_to_nat(1u);
v___x_35_ = lean_nat_to_int(v___x_34_);
return v___x_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1(uint8_t v_x_36_){
_start:
{
lean_object* v___x_37_; 
v___x_37_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0);
return v___x_37_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___boxed(lean_object* v_x_38_){
_start:
{
uint8_t v_x_12__boxed_39_; lean_object* v_res_40_; 
v_x_12__boxed_39_ = lean_unbox(v_x_38_);
v_res_40_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1(v_x_12__boxed_39_);
return v_res_40_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___closed__0(void){
_start:
{
lean_object* v___x_41_; lean_object* v___x_42_; 
v___x_41_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0);
v___x_42_ = lean_int_neg(v___x_41_);
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2(uint8_t v_q_43_){
_start:
{
if (v_q_43_ == 0)
{
lean_object* v___x_44_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi1___closed__0);
return v___x_44_;
}
else
{
lean_object* v___x_45_; 
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___closed__0);
return v___x_45_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2___boxed(lean_object* v_q_46_){
_start:
{
uint8_t v_q_boxed_47_; lean_object* v_res_48_; 
v_q_boxed_47_ = lean_unbox(v_q_46_);
v_res_48_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_iPsi2(v_q_boxed_47_);
return v_res_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iWeights(lean_object* v_v_49_, uint8_t v_q_50_){
_start:
{
lean_object* v___x_51_; lean_object* v___x_52_; lean_object* v___x_53_; 
v___x_51_ = lean_box(v_q_50_);
v___x_52_ = lean_apply_1(v_v_49_, v___x_51_);
v___x_53_ = lean_int_mul(v___x_52_, v___x_52_);
lean_dec(v___x_52_);
return v___x_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iWeights___boxed(lean_object* v_v_54_, lean_object* v_q_55_){
_start:
{
uint8_t v_q_boxed_56_; lean_object* v_res_57_; 
v_q_boxed_56_ = lean_unbox(v_q_55_);
v_res_57_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_iWeights(v_v_54_, v_q_boxed_56_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iMix(lean_object* v_v_58_, uint8_t v_q_59_){
_start:
{
uint8_t v___x_60_; 
v___x_60_ = 1;
if (v_q_59_ == 0)
{
lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; lean_object* v___x_65_; 
v___x_61_ = lean_box(v_q_59_);
lean_inc_ref(v_v_58_);
v___x_62_ = lean_apply_1(v_v_58_, v___x_61_);
v___x_63_ = lean_box(v___x_60_);
v___x_64_ = lean_apply_1(v_v_58_, v___x_63_);
v___x_65_ = lean_int_add(v___x_62_, v___x_64_);
lean_dec(v___x_64_);
lean_dec(v___x_62_);
return v___x_65_;
}
else
{
uint8_t v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; 
v___x_66_ = 0;
v___x_67_ = lean_box(v___x_66_);
lean_inc_ref(v_v_58_);
v___x_68_ = lean_apply_1(v_v_58_, v___x_67_);
v___x_69_ = lean_box(v___x_60_);
v___x_70_ = lean_apply_1(v_v_58_, v___x_69_);
v___x_71_ = lean_int_sub(v___x_68_, v___x_70_);
lean_dec(v___x_70_);
lean_dec(v___x_68_);
return v___x_71_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iMix___boxed(lean_object* v_v_72_, lean_object* v_q_73_){
_start:
{
uint8_t v_q_boxed_74_; lean_object* v_res_75_; 
v_q_boxed_74_ = lean_unbox(v_q_73_);
v_res_75_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_iMix(v_v_72_, v_q_boxed_74_);
return v_res_75_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iReadout(lean_object* v_v_76_, uint8_t v_a_77_){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; 
v___x_78_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H010_iMix___boxed), 2, 1);
lean_closure_set(v___x_78_, 0, v_v_76_);
v___x_79_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_iWeights(v___x_78_, v_a_77_);
return v___x_79_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H010_iReadout___boxed(lean_object* v_v_80_, lean_object* v_a_81_){
_start:
{
uint8_t v_a_5__boxed_82_; lean_object* v_res_83_; 
v_a_5__boxed_82_ = lean_unbox(v_a_81_);
v_res_83_ = lp_FiniteQuantum_FableHilbertWalk20260819_H010_iReadout(v_v_80_, v_a_5__boxed_82_);
return v_res_83_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H008PhaseBlindPresentation(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H009PhaseFiber(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H010InterferenceNonDescent(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H004FreeLinearization(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H008PhaseBlindPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H009PhaseFiber(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
