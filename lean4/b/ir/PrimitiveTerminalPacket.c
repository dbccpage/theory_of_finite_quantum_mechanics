// Lean compiler output
// Module: PrimitiveTerminalPacket
// Imports: public import Init public meta import Init public import PrimitiveRepairBoundary
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
uint8_t lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor(lean_object*, lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg(lean_object* v_C_1_, lean_object* v_q_2_, uint8_t v_boundary_3_, uint8_t v_hasCertificate_4_){
_start:
{
uint8_t v___x_5_; lean_object* v___x_6_; 
v___x_5_ = lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg(v_C_1_, v_q_2_);
v___x_6_ = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(v___x_6_, 0, v___x_5_);
lean_ctor_set_uint8(v___x_6_, 1, v_boundary_3_);
lean_ctor_set_uint8(v___x_6_, 2, v_hasCertificate_4_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg___boxed(lean_object* v_C_7_, lean_object* v_q_8_, lean_object* v_boundary_9_, lean_object* v_hasCertificate_10_){
_start:
{
uint8_t v_boundary_boxed_11_; uint8_t v_hasCertificate_boxed_12_; lean_object* v_res_13_; 
v_boundary_boxed_11_ = lean_unbox(v_boundary_9_);
v_hasCertificate_boxed_12_ = lean_unbox(v_hasCertificate_10_);
v_res_13_ = lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg(v_C_7_, v_q_8_, v_boundary_boxed_11_, v_hasCertificate_boxed_12_);
return v_res_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor(lean_object* v_Q_14_, lean_object* v_C_15_, lean_object* v_q_16_, uint8_t v_boundary_17_, uint8_t v_hasCertificate_18_){
_start:
{
lean_object* v___x_19_; 
v___x_19_ = lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg(v_C_15_, v_q_16_, v_boundary_17_, v_hasCertificate_18_);
return v___x_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___boxed(lean_object* v_Q_20_, lean_object* v_C_21_, lean_object* v_q_22_, lean_object* v_boundary_23_, lean_object* v_hasCertificate_24_){
_start:
{
uint8_t v_boundary_boxed_25_; uint8_t v_hasCertificate_boxed_26_; lean_object* v_res_27_; 
v_boundary_boxed_25_ = lean_unbox(v_boundary_23_);
v_hasCertificate_boxed_26_ = lean_unbox(v_hasCertificate_24_);
v_res_27_ = lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor(v_Q_20_, v_C_21_, v_q_22_, v_boundary_boxed_25_, v_hasCertificate_boxed_26_);
return v_res_27_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveRepairBoundary(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PrimitiveTerminalPacket(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveRepairBoundary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
