// Lean compiler output
// Module: H017FiniteHilbertBoundary
// Imports: public import Init public meta import Init public import HWKernel public import Core public import H003ReversibilityGate public import H004FreeLinearization public import H005InnerProductAdmission public import H006PermutationUnitary public import H008PhaseBlindPresentation public import H009PhaseFiber public import H010InterferenceNonDescent public import H013BornPairingBoundary public import H014TensorCompositionBoundary public import H015IrreversibleFork public import H016ContinuousDynamicsFork
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
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H017_walkLedger___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 1, 1, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017_walkLedger___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H017_walkLedger___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017_walkLedger = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H017_walkLedger___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H017_AllDischarged(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017_AllDischarged___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H017_AllDischarged(lean_object* v_L_5_){
_start:
{
uint8_t v_permutation__isometry__envelope__flag_6_; 
v_permutation__isometry__envelope__flag_6_ = lean_ctor_get_uint8(v_L_5_, 0);
if (v_permutation__isometry__envelope__flag_6_ == 0)
{
return v_permutation__isometry__envelope__flag_6_;
}
else
{
uint8_t v_phase__fiber__nonempty_7_; 
v_phase__fiber__nonempty_7_ = lean_ctor_get_uint8(v_L_5_, 1);
if (v_phase__fiber__nonempty_7_ == 0)
{
return v_phase__fiber__nonempty_7_;
}
else
{
uint8_t v_interference__non__descent_8_; 
v_interference__non__descent_8_ = lean_ctor_get_uint8(v_L_5_, 2);
if (v_interference__non__descent_8_ == 0)
{
return v_interference__non__descent_8_;
}
else
{
uint8_t v_complex__phase__selected_9_; 
v_complex__phase__selected_9_ = lean_ctor_get_uint8(v_L_5_, 3);
if (v_complex__phase__selected_9_ == 0)
{
return v_complex__phase__selected_9_;
}
else
{
uint8_t v_born__uniqueness_10_; 
v_born__uniqueness_10_ = lean_ctor_get_uint8(v_L_5_, 4);
if (v_born__uniqueness_10_ == 0)
{
return v_born__uniqueness_10_;
}
else
{
uint8_t v_tensor__composition__forced_11_; 
v_tensor__composition__forced_11_ = lean_ctor_get_uint8(v_L_5_, 5);
if (v_tensor__composition__forced_11_ == 0)
{
return v_tensor__composition__forced_11_;
}
else
{
uint8_t v_channels__canonical_12_; 
v_channels__canonical_12_ = lean_ctor_get_uint8(v_L_5_, 6);
if (v_channels__canonical_12_ == 0)
{
return v_channels__canonical_12_;
}
else
{
uint8_t v_continuum__dynamics_13_; 
v_continuum__dynamics_13_ = lean_ctor_get_uint8(v_L_5_, 7);
return v_continuum__dynamics_13_;
}
}
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H017_AllDischarged___boxed(lean_object* v_L_14_){
_start:
{
uint8_t v_res_15_; lean_object* v_r_16_; 
v_res_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_H017_AllDischarged(v_L_14_);
lean_dec_ref(v_L_14_);
v_r_16_ = lean_box(v_res_15_);
return v_r_16_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_Core(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H006PermutationUnitary(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H008PhaseBlindPresentation(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H009PhaseFiber(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H010InterferenceNonDescent(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H013BornPairingBoundary(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H014TensorCompositionBoundary(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H015IrreversibleFork(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H016ContinuousDynamicsFork(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H017FiniteHilbertBoundary(uint8_t builtin) {
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
res = initialize_FiniteQuantum_Core(builtin);
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
res = initialize_FiniteQuantum_H006PermutationUnitary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H008PhaseBlindPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H009PhaseFiber(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H010InterferenceNonDescent(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H013BornPairingBoundary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H014TensorCompositionBoundary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H015IrreversibleFork(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H016ContinuousDynamicsFork(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
