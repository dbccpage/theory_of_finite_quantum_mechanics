// Lean compiler output
// Module: ChiralAnomalyInflow
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
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__R(lean_object*);
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__R___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__L(lean_object*);
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__L___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_chiralCochainCurvature(lean_object*);
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_chiralCochainCurvature___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__R(lean_object* v_s_1_){
_start:
{
lean_object* v_base__energy_2_; 
v_base__energy_2_ = lean_ctor_get(v_s_1_, 0);
lean_inc(v_base__energy_2_);
return v_base__energy_2_;
}
}
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__R___boxed(lean_object* v_s_3_){
_start:
{
lean_object* v_res_4_; 
v_res_4_ = lp_po023_ChiralAnomalyInflow_energy__R(v_s_3_);
lean_dec_ref(v_s_3_);
return v_res_4_;
}
}
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__L(lean_object* v_s_5_){
_start:
{
lean_object* v_base__energy_6_; lean_object* v_mu__5_7_; lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v_base__energy_6_ = lean_ctor_get(v_s_5_, 0);
v_mu__5_7_ = lean_ctor_get(v_s_5_, 1);
v___x_8_ = lean_unsigned_to_nat(2u);
v___x_9_ = lean_nat_mul(v___x_8_, v_mu__5_7_);
v___x_10_ = lean_nat_add(v_base__energy_6_, v___x_9_);
lean_dec(v___x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_energy__L___boxed(lean_object* v_s_11_){
_start:
{
lean_object* v_res_12_; 
v_res_12_ = lp_po023_ChiralAnomalyInflow_energy__L(v_s_11_);
lean_dec_ref(v_s_11_);
return v_res_12_;
}
}
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_chiralCochainCurvature(lean_object* v_s_13_){
_start:
{
lean_object* v_mu__5_14_; 
v_mu__5_14_ = lean_ctor_get(v_s_13_, 1);
lean_inc(v_mu__5_14_);
return v_mu__5_14_;
}
}
LEAN_EXPORT lean_object* lp_po023_ChiralAnomalyInflow_chiralCochainCurvature___boxed(lean_object* v_s_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_po023_ChiralAnomalyInflow_chiralCochainCurvature(v_s_15_);
lean_dec_ref(v_s_15_);
return v_res_16_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
void lean_initialize_runtime_module();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_po023_ChiralAnomalyInflow(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize_runtime_module();
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
