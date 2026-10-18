// Lean compiler output
// Module: H008PhaseBlindPresentation
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H005InnerProductAdmission
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(lean_object*, lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
lean_object* l_List_reverse___redArg(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H008_totalWeight_spec__0___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_totalWeight___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_totalWeight(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H008_totalWeight_spec__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi1(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi1___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind___redArg(lean_object* v_v_1_, lean_object* v_q_2_){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v_re_6_; 
v___x_3_ = lean_apply_1(v_v_1_, v_q_2_);
lean_inc_ref(v___x_3_);
v___x_4_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(v___x_3_);
v___x_5_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(v___x_4_, v___x_3_);
lean_dec_ref(v___x_4_);
v_re_6_ = lean_ctor_get(v___x_5_, 0);
lean_inc(v_re_6_);
lean_dec_ref(v___x_5_);
return v_re_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind(lean_object* v_Q_7_, lean_object* v_v_8_, lean_object* v_q_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind___redArg(v_v_8_, v_q_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H008_totalWeight_spec__0___redArg(lean_object* v_v_11_, lean_object* v_a_12_, lean_object* v_a_13_){
_start:
{
if (lean_obj_tag(v_a_12_) == 0)
{
lean_object* v___x_14_; 
lean_dec_ref(v_v_11_);
v___x_14_ = l_List_reverse___redArg(v_a_13_);
return v___x_14_;
}
else
{
lean_object* v_head_15_; lean_object* v_tail_16_; lean_object* v___x_18_; uint8_t v_isShared_19_; uint8_t v_isSharedCheck_25_; 
v_head_15_ = lean_ctor_get(v_a_12_, 0);
v_tail_16_ = lean_ctor_get(v_a_12_, 1);
v_isSharedCheck_25_ = !lean_is_exclusive(v_a_12_);
if (v_isSharedCheck_25_ == 0)
{
v___x_18_ = v_a_12_;
v_isShared_19_ = v_isSharedCheck_25_;
goto v_resetjp_17_;
}
else
{
lean_inc(v_tail_16_);
lean_inc(v_head_15_);
lean_dec(v_a_12_);
v___x_18_ = lean_box(0);
v_isShared_19_ = v_isSharedCheck_25_;
goto v_resetjp_17_;
}
v_resetjp_17_:
{
lean_object* v___x_20_; lean_object* v___x_22_; 
lean_inc_ref(v_v_11_);
v___x_20_ = lp_FiniteQuantum_FableHilbertWalk20260819_H008_phaseBlind___redArg(v_v_11_, v_head_15_);
if (v_isShared_19_ == 0)
{
lean_ctor_set(v___x_18_, 1, v_a_13_);
lean_ctor_set(v___x_18_, 0, v___x_20_);
v___x_22_ = v___x_18_;
goto v_reusejp_21_;
}
else
{
lean_object* v_reuseFailAlloc_24_; 
v_reuseFailAlloc_24_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_24_, 0, v___x_20_);
lean_ctor_set(v_reuseFailAlloc_24_, 1, v_a_13_);
v___x_22_ = v_reuseFailAlloc_24_;
goto v_reusejp_21_;
}
v_reusejp_21_:
{
v_a_12_ = v_tail_16_;
v_a_13_ = v___x_22_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_totalWeight___redArg(lean_object* v_E_26_, lean_object* v_v_27_){
_start:
{
lean_object* v___x_28_; lean_object* v___x_29_; lean_object* v___x_30_; lean_object* v___x_31_; 
v___x_28_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
v___x_29_ = lean_box(0);
v___x_30_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H008_totalWeight_spec__0___redArg(v_v_27_, v_E_26_, v___x_29_);
v___x_31_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v___x_28_, v___x_30_);
return v___x_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_totalWeight(lean_object* v_Q_32_, lean_object* v_E_33_, lean_object* v_v_34_){
_start:
{
lean_object* v___x_35_; 
v___x_35_ = lp_FiniteQuantum_FableHilbertWalk20260819_H008_totalWeight___redArg(v_E_33_, v_v_34_);
return v___x_35_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H008_totalWeight_spec__0(lean_object* v_Q_36_, lean_object* v_v_37_, lean_object* v_a_38_, lean_object* v_a_39_){
_start:
{
lean_object* v___x_40_; 
v___x_40_ = lp_FiniteQuantum_List_mapTR_loop___at___00FableHilbertWalk20260819_H008_totalWeight_spec__0___redArg(v_v_37_, v_a_38_, v_a_39_);
return v___x_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi1(uint8_t v_q_41_){
_start:
{
lean_object* v___x_42_; 
v___x_42_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi1___boxed(lean_object* v_q_43_){
_start:
{
uint8_t v_q_boxed_44_; lean_object* v_res_45_; 
v_q_boxed_44_ = lean_unbox(v_q_43_);
v_res_45_ = lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi1(v_q_boxed_44_);
return v_res_45_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___closed__0(void){
_start:
{
lean_object* v___x_46_; lean_object* v___x_47_; 
v___x_46_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
v___x_47_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_46_);
return v___x_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2(uint8_t v_q_48_){
_start:
{
if (v_q_48_ == 0)
{
lean_object* v___x_49_; 
v___x_49_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_49_;
}
else
{
lean_object* v___x_50_; 
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___closed__0);
return v___x_50_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2___boxed(lean_object* v_q_51_){
_start:
{
uint8_t v_q_boxed_52_; lean_object* v_res_53_; 
v_q_boxed_52_ = lean_unbox(v_q_51_);
v_res_53_ = lp_FiniteQuantum_FableHilbertWalk20260819_H008_psi2(v_q_boxed_52_);
return v_res_53_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H008PhaseBlindPresentation(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H005InnerProductAdmission(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
