// Lean compiler output
// Module: H015IrreversibleFork
// Imports: public import Init public meta import Init public import HWKernel public import H003ReversibilityGate public import H004FreeLinearization public import H005InnerProductAdmission
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil1(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil1(lean_object* v_x_1_){
_start:
{
lean_inc_ref(v_x_1_);
return v_x_1_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil1___boxed(lean_object* v_x_2_){
_start:
{
lean_object* v_res_3_; 
v_res_3_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil1(v_x_2_);
lean_dec_ref(v_x_2_);
return v_res_3_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015_dil2(lean_object* v_x_4_){
_start:
{
lean_object* v_snd_5_; uint8_t v___x_6_; 
v_snd_5_ = lean_ctor_get(v_x_4_, 1);
v___x_6_ = lean_unbox(v_snd_5_);
if (v___x_6_ == 0)
{
lean_object* v_fst_7_; lean_object* v___x_9_; uint8_t v_isShared_10_; uint8_t v_isSharedCheck_16_; 
v_fst_7_ = lean_ctor_get(v_x_4_, 0);
v_isSharedCheck_16_ = !lean_is_exclusive(v_x_4_);
if (v_isSharedCheck_16_ == 0)
{
lean_object* v_unused_17_; 
v_unused_17_ = lean_ctor_get(v_x_4_, 1);
lean_dec(v_unused_17_);
v___x_9_ = v_x_4_;
v_isShared_10_ = v_isSharedCheck_16_;
goto v_resetjp_8_;
}
else
{
lean_inc(v_fst_7_);
lean_dec(v_x_4_);
v___x_9_ = lean_box(0);
v_isShared_10_ = v_isSharedCheck_16_;
goto v_resetjp_8_;
}
v_resetjp_8_:
{
uint8_t v___x_11_; lean_object* v___x_12_; lean_object* v___x_14_; 
v___x_11_ = 1;
v___x_12_ = lean_box(v___x_11_);
if (v_isShared_10_ == 0)
{
lean_ctor_set(v___x_9_, 1, v___x_12_);
v___x_14_ = v___x_9_;
goto v_reusejp_13_;
}
else
{
lean_object* v_reuseFailAlloc_15_; 
v_reuseFailAlloc_15_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_15_, 0, v_fst_7_);
lean_ctor_set(v_reuseFailAlloc_15_, 1, v___x_12_);
v___x_14_ = v_reuseFailAlloc_15_;
goto v_reusejp_13_;
}
v_reusejp_13_:
{
return v___x_14_;
}
}
}
else
{
lean_object* v_fst_18_; lean_object* v___x_20_; uint8_t v_isShared_21_; uint8_t v_isSharedCheck_27_; 
v_fst_18_ = lean_ctor_get(v_x_4_, 0);
v_isSharedCheck_27_ = !lean_is_exclusive(v_x_4_);
if (v_isSharedCheck_27_ == 0)
{
lean_object* v_unused_28_; 
v_unused_28_ = lean_ctor_get(v_x_4_, 1);
lean_dec(v_unused_28_);
v___x_20_ = v_x_4_;
v_isShared_21_ = v_isSharedCheck_27_;
goto v_resetjp_19_;
}
else
{
lean_inc(v_fst_18_);
lean_dec(v_x_4_);
v___x_20_ = lean_box(0);
v_isShared_21_ = v_isSharedCheck_27_;
goto v_resetjp_19_;
}
v_resetjp_19_:
{
uint8_t v___x_22_; lean_object* v___x_23_; lean_object* v___x_25_; 
v___x_22_ = 0;
v___x_23_ = lean_box(v___x_22_);
if (v_isShared_21_ == 0)
{
lean_ctor_set(v___x_20_, 1, v___x_23_);
v___x_25_ = v___x_20_;
goto v_reusejp_24_;
}
else
{
lean_object* v_reuseFailAlloc_26_; 
v_reuseFailAlloc_26_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_26_, 0, v_fst_18_);
lean_ctor_set(v_reuseFailAlloc_26_, 1, v___x_23_);
v___x_25_ = v_reuseFailAlloc_26_;
goto v_reusejp_24_;
}
v_reusejp_24_:
{
return v___x_25_;
}
}
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H015IrreversibleFork(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H003ReversibilityGate(builtin);
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
