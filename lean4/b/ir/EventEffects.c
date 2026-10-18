// Lean compiler output
// Module: EventEffects
// Imports: public import Init public meta import Init public import PrimitiveDifference
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_EventEffects_replay___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_EventEffects_replay(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_EventEffects_0__OmegaCore_EventEffects_replay_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_EventEffects_0__OmegaCore_EventEffects_replay_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_EventEffects_replay___redArg(lean_object* v_step_1_, lean_object* v_x_2_, lean_object* v_x_3_){
_start:
{
if (lean_obj_tag(v_x_2_) == 0)
{
lean_dec(v_step_1_);
return v_x_3_;
}
else
{
lean_object* v_head_4_; lean_object* v_tail_5_; lean_object* v___x_6_; 
v_head_4_ = lean_ctor_get(v_x_2_, 0);
lean_inc(v_head_4_);
v_tail_5_ = lean_ctor_get(v_x_2_, 1);
lean_inc(v_tail_5_);
lean_dec_ref_known(v_x_2_, 2);
lean_inc(v_step_1_);
v___x_6_ = lean_apply_2(v_step_1_, v_head_4_, v_x_3_);
v_x_2_ = v_tail_5_;
v_x_3_ = v___x_6_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_EventEffects_replay(lean_object* v_Event_8_, lean_object* v_State_9_, lean_object* v_step_10_, lean_object* v_x_11_, lean_object* v_x_12_){
_start:
{
lean_object* v___x_13_; 
v___x_13_ = lp_FiniteQuantum_OmegaCore_EventEffects_replay___redArg(v_step_10_, v_x_11_, v_x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_EventEffects_0__OmegaCore_EventEffects_replay_match__1_splitter___redArg(lean_object* v_x_14_, lean_object* v_x_15_, lean_object* v_h__1_16_, lean_object* v_h__2_17_){
_start:
{
if (lean_obj_tag(v_x_14_) == 0)
{
lean_object* v___x_18_; 
lean_dec(v_h__2_17_);
v___x_18_ = lean_apply_1(v_h__1_16_, v_x_15_);
return v___x_18_;
}
else
{
lean_object* v_head_19_; lean_object* v_tail_20_; lean_object* v___x_21_; 
lean_dec(v_h__1_16_);
v_head_19_ = lean_ctor_get(v_x_14_, 0);
lean_inc(v_head_19_);
v_tail_20_ = lean_ctor_get(v_x_14_, 1);
lean_inc(v_tail_20_);
lean_dec_ref_known(v_x_14_, 2);
v___x_21_ = lean_apply_3(v_h__2_17_, v_head_19_, v_tail_20_, v_x_15_);
return v___x_21_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_EventEffects_0__OmegaCore_EventEffects_replay_match__1_splitter(lean_object* v_Event_22_, lean_object* v_State_23_, lean_object* v_motive_24_, lean_object* v_x_25_, lean_object* v_x_26_, lean_object* v_h__1_27_, lean_object* v_h__2_28_){
_start:
{
if (lean_obj_tag(v_x_25_) == 0)
{
lean_object* v___x_29_; 
lean_dec(v_h__2_28_);
v___x_29_ = lean_apply_1(v_h__1_27_, v_x_26_);
return v___x_29_;
}
else
{
lean_object* v_head_30_; lean_object* v_tail_31_; lean_object* v___x_32_; 
lean_dec(v_h__1_27_);
v_head_30_ = lean_ctor_get(v_x_25_, 0);
lean_inc(v_head_30_);
v_tail_31_ = lean_ctor_get(v_x_25_, 1);
lean_inc(v_tail_31_);
lean_dec_ref_known(v_x_25_, 2);
v___x_32_ = lean_apply_3(v_h__2_28_, v_head_30_, v_tail_31_, v_x_26_);
return v___x_32_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveDifference(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_EventEffects(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveDifference(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
