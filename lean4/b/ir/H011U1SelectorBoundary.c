// Lean compiler output
// Module: H011U1SelectorBoundary
// Imports: public import Init public meta import Init public import HWKernel public import H010InterferenceNonDescent
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
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H011_SelectorDischarged(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H011_SelectorDischarged___boxed(lean_object*);
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H011_qm062Route___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 1, 1, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H011_qm062Route___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H011_qm062Route___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H011_qm062Route = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H011_qm062Route___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H011_SelectorDischarged(lean_object* v_S_1_){
_start:
{
uint8_t v_phase__composition__law_2_; 
v_phase__composition__law_2_ = lean_ctor_get_uint8(v_S_1_, 0);
if (v_phase__composition__law_2_ == 0)
{
return v_phase__composition__law_2_;
}
else
{
uint8_t v_transport__functoriality_3_; 
v_transport__functoriality_3_ = lean_ctor_get_uint8(v_S_1_, 1);
if (v_transport__functoriality_3_ == 0)
{
return v_transport__functoriality_3_;
}
else
{
uint8_t v_carrier__connectedness_4_; 
v_carrier__connectedness_4_ = lean_ctor_get_uint8(v_S_1_, 2);
if (v_carrier__connectedness_4_ == 0)
{
return v_carrier__connectedness_4_;
}
else
{
uint8_t v_rival__excluded_5_; 
v_rival__excluded_5_ = lean_ctor_get_uint8(v_S_1_, 3);
return v_rival__excluded_5_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H011_SelectorDischarged___boxed(lean_object* v_S_6_){
_start:
{
uint8_t v_res_7_; lean_object* v_r_8_; 
v_res_7_ = lp_FiniteQuantum_FableHilbertWalk20260819_H011_SelectorDischarged(v_S_6_);
lean_dec_ref(v_S_6_);
v_r_8_ = lean_box(v_res_7_);
return v_r_8_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H010InterferenceNonDescent(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H011U1SelectorBoundary(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H010InterferenceNonDescent(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
