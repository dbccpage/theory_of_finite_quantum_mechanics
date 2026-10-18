// Lean compiler output
// Module: PrimitiveAdmissibleRepair
// Imports: public import Init public meta import Init public import PrimitiveRepairWitness
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___redArg(lean_object* v_zeroClass_1_){
_start:
{
lean_inc(v_zeroClass_1_);
return v_zeroClass_1_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___redArg___boxed(lean_object* v_zeroClass_2_){
_start:
{
lean_object* v_res_3_; 
v_res_3_ = lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___redArg(v_zeroClass_2_);
lean_dec(v_zeroClass_2_);
return v_res_3_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair(lean_object* v_Q_4_, lean_object* v_zeroClass_5_, lean_object* v_x_6_){
_start:
{
lean_inc(v_zeroClass_5_);
return v_zeroClass_5_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair___boxed(lean_object* v_Q_7_, lean_object* v_zeroClass_8_, lean_object* v_x_9_){
_start:
{
lean_object* v_res_10_; 
v_res_10_ = lp_FiniteQuantum_OmegaCore_PrimitiveAdmissibleRepair_constantZeroRepair(v_Q_7_, v_zeroClass_8_, v_x_9_);
lean_dec(v_x_9_);
lean_dec(v_zeroClass_8_);
return v_res_10_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveRepairWitness(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PrimitiveAdmissibleRepair(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveRepairWitness(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
