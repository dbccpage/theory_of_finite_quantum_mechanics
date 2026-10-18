// Lean compiler output
// Module: WorldLiftExhaustion
// Imports: public import Init public meta import Init public import WorldPresentation
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_LiftRefusal_toCtorIdx(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_LiftRefusal_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_LiftRefusal_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqLiftRefusal(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqLiftRefusal___boxed(lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_requireExhaustion(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_LiftRefusal_toCtorIdx(lean_object* v_x_1_){
_start:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_LiftRefusal_ofNat(lean_object* v_n_3_){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = lean_box(0);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_LiftRefusal_ofNat___boxed(lean_object* v_n_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_FiniteQuantum_OmegaWorld_LiftRefusal_ofNat(v_n_5_);
lean_dec(v_n_5_);
return v_res_6_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_instDecidableEqLiftRefusal(lean_object* v_x_7_, lean_object* v_y_8_){
_start:
{
uint8_t v___x_9_; 
v___x_9_ = 1;
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_instDecidableEqLiftRefusal___boxed(lean_object* v_x_10_, lean_object* v_y_11_){
_start:
{
uint8_t v_res_12_; lean_object* v_r_13_; 
v_res_12_ = lp_FiniteQuantum_OmegaWorld_instDecidableEqLiftRefusal(v_x_10_, v_y_11_);
v_r_13_ = lean_box(v_res_12_);
return v_r_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg(lean_object* v_receipt_16_){
_start:
{
if (lean_obj_tag(v_receipt_16_) == 0)
{
lean_object* v___x_17_; 
v___x_17_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg___closed__0));
return v___x_17_;
}
else
{
lean_object* v_val_18_; lean_object* v___x_20_; uint8_t v_isShared_21_; uint8_t v_isSharedCheck_25_; 
v_val_18_ = lean_ctor_get(v_receipt_16_, 0);
v_isSharedCheck_25_ = !lean_is_exclusive(v_receipt_16_);
if (v_isSharedCheck_25_ == 0)
{
v___x_20_ = v_receipt_16_;
v_isShared_21_ = v_isSharedCheck_25_;
goto v_resetjp_19_;
}
else
{
lean_inc(v_val_18_);
lean_dec(v_receipt_16_);
v___x_20_ = lean_box(0);
v_isShared_21_ = v_isSharedCheck_25_;
goto v_resetjp_19_;
}
v_resetjp_19_:
{
lean_object* v___x_23_; 
if (v_isShared_21_ == 0)
{
v___x_23_ = v___x_20_;
goto v_reusejp_22_;
}
else
{
lean_object* v_reuseFailAlloc_24_; 
v_reuseFailAlloc_24_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v_reuseFailAlloc_24_, 0, v_val_18_);
v___x_23_ = v_reuseFailAlloc_24_;
goto v_reusejp_22_;
}
v_reusejp_22_:
{
return v___x_23_;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_requireExhaustion(lean_object* v_State_26_, lean_object* v_Move_27_, lean_object* v_receipt_28_){
_start:
{
lean_object* v___x_29_; 
v___x_29_ = lp_FiniteQuantum_OmegaWorld_requireExhaustion___redArg(v_receipt_28_);
return v___x_29_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_WorldPresentation(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldLiftExhaustion(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_WorldPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
