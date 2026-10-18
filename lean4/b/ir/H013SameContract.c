// Lean compiler output
// Module: H013SameContract
// Imports: public import Init public meta import Init public import HWKernel public import H008PhaseBlindPresentation public import H013BornPairingBoundary
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind(lean_object*, lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013_pair___redArg(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_bornRule(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swapEffect(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swapEffect___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swappedRule(lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect(uint8_t v_x_3_){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___closed__0);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect___boxed(lean_object* v_x_5_){
_start:
{
uint8_t v_x_12__boxed_6_; lean_object* v_res_7_; 
v_x_12__boxed_6_ = lean_unbox(v_x_5_);
v_res_7_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_unitEffect(v_x_12__boxed_6_);
return v_res_7_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_bornRule(lean_object* v_v_8_, lean_object* v_e_9_){
_start:
{
lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_10_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
v___x_11_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind), 3, 2);
lean_closure_set(v___x_11_, 0, lean_box(0));
lean_closure_set(v___x_11_, 1, v_v_8_);
v___x_12_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013_pair___redArg(v___x_10_, v___x_11_, v_e_9_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swapEffect(lean_object* v_e_13_, uint8_t v_q_14_){
_start:
{
if (v_q_14_ == 0)
{
uint8_t v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; 
v___x_15_ = 1;
v___x_16_ = lean_box(v___x_15_);
v___x_17_ = lean_apply_1(v_e_13_, v___x_16_);
return v___x_17_;
}
else
{
uint8_t v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; 
v___x_18_ = 0;
v___x_19_ = lean_box(v___x_18_);
v___x_20_ = lean_apply_1(v_e_13_, v___x_19_);
return v___x_20_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swapEffect___boxed(lean_object* v_e_21_, lean_object* v_q_22_){
_start:
{
uint8_t v_q_boxed_23_; lean_object* v_res_24_; 
v_q_boxed_23_ = lean_unbox(v_q_22_);
v_res_24_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swapEffect(v_e_21_, v_q_boxed_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swappedRule(lean_object* v_v_25_, lean_object* v_e_26_){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; lean_object* v___x_30_; 
v___x_27_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
v___x_28_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind), 3, 2);
lean_closure_set(v___x_28_, 0, lean_box(0));
lean_closure_set(v___x_28_, 1, v_v_25_);
v___x_29_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H013Contract_swapEffect___boxed), 2, 1);
lean_closure_set(v___x_29_, 0, v_e_26_);
v___x_30_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013_pair___redArg(v___x_27_, v___x_28_, v___x_29_);
return v___x_30_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H008PhaseBlindPresentation(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H013BornPairingBoundary(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H013SameContract(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H008PhaseBlindPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H013BornPairingBoundary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
