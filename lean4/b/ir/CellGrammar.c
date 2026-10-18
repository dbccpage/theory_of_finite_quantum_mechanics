// Lean compiler output
// Module: CellGrammar
// Imports: public import Init public meta import Init public import CochainWindow
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___redArg(lean_object* v_dual_1_){
_start:
{
lean_object* v_d0Carrier_2_; lean_object* v_d1Carrier_3_; lean_object* v_d2Carrier_4_; lean_object* v_d0_5_; lean_object* v_d1_6_; lean_object* v___x_7_; 
v_d0Carrier_2_ = lean_ctor_get(v_dual_1_, 0);
v_d1Carrier_3_ = lean_ctor_get(v_dual_1_, 1);
v_d2Carrier_4_ = lean_ctor_get(v_dual_1_, 2);
v_d0_5_ = lean_ctor_get(v_dual_1_, 3);
v_d1_6_ = lean_ctor_get(v_dual_1_, 4);
lean_inc(v_d1_6_);
lean_inc(v_d0_5_);
lean_inc_ref(v_d2Carrier_4_);
lean_inc_ref(v_d1Carrier_3_);
lean_inc_ref(v_d0Carrier_2_);
v___x_7_ = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(v___x_7_, 0, v_d0Carrier_2_);
lean_ctor_set(v___x_7_, 1, v_d1Carrier_3_);
lean_ctor_set(v___x_7_, 2, v_d2Carrier_4_);
lean_ctor_set(v___x_7_, 3, v_d0_5_);
lean_ctor_set(v___x_7_, 4, v_d1_6_);
return v___x_7_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___redArg___boxed(lean_object* v_dual_8_){
_start:
{
lean_object* v_res_9_; 
v_res_9_ = lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___redArg(v_dual_8_);
lean_dec_ref(v_dual_8_);
return v_res_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow(lean_object* v_C0_10_, lean_object* v_C1_11_, lean_object* v_C2_12_, lean_object* v_D0_13_, lean_object* v_D1_14_, lean_object* v_D2_15_, lean_object* v_chain_16_, lean_object* v_dual_17_){
_start:
{
lean_object* v___x_18_; 
v___x_18_ = lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___redArg(v_dual_17_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow___boxed(lean_object* v_C0_19_, lean_object* v_C1_20_, lean_object* v_C2_21_, lean_object* v_D0_22_, lean_object* v_D1_23_, lean_object* v_D2_24_, lean_object* v_chain_25_, lean_object* v_dual_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_FiniteQuantum_OmegaCore_CellGrammar_toWindow(v_C0_19_, v_C1_20_, v_C2_21_, v_D0_22_, v_D1_23_, v_D2_24_, v_chain_25_, v_dual_26_);
lean_dec_ref(v_dual_26_);
lean_dec_ref(v_chain_25_);
return v_res_27_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_CochainWindow(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_CellGrammar(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_CochainWindow(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
