// Lean compiler output
// Module: H013FrameAdditivity
// Imports: public import Init public meta import Init public import HWKernel public import H004FreeLinearization public import H005InnerProductAdmission public import H008PhaseBlindPresentation public import H013BornPairingBoundary
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
lean_object* lean_int_add(lean_object*, lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_sqMod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_overlap(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_quadraticAlong(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_quarticAlong(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_frameTotal(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eFalse(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eFalse___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eTrue(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eTrue___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had0(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had0___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot0(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot0___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_sqMod(lean_object* v_z_1_){
_start:
{
lean_object* v___x_2_; lean_object* v___x_3_; lean_object* v_re_4_; 
lean_inc_ref(v_z_1_);
v___x_2_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gconj(v_z_1_);
v___x_3_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gmul(v___x_2_, v_z_1_);
lean_dec_ref(v___x_2_);
v_re_4_ = lean_ctor_get(v___x_3_, 0);
lean_inc(v_re_4_);
lean_dec_ref(v___x_3_);
return v_re_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_overlap(lean_object* v_e_5_, lean_object* v_00_u03c8_6_){
_start:
{
lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v___x_7_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_gaussPack;
v___x_8_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_enumBool;
v___x_9_ = lp_FiniteQuantum_FableHilbertWalk20260819_H005_sesq___redArg(v___x_7_, v___x_8_, v_e_5_, v_00_u03c8_6_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_quadraticAlong(lean_object* v_e_10_, lean_object* v_00_u03c8_11_){
_start:
{
lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_12_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_overlap(v_e_10_, v_00_u03c8_11_);
v___x_13_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_sqMod(v___x_12_);
return v___x_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_quarticAlong(lean_object* v_e_14_, lean_object* v_00_u03c8_15_){
_start:
{
lean_object* v_w_16_; lean_object* v___x_17_; 
v_w_16_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_quadraticAlong(v_e_14_, v_00_u03c8_15_);
v___x_17_ = lean_int_mul(v_w_16_, v_w_16_);
lean_dec(v_w_16_);
return v___x_17_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_frameTotal(lean_object* v_readout_18_, lean_object* v_e0_19_, lean_object* v_e1_20_, lean_object* v_00_u03c8_21_){
_start:
{
lean_object* v___x_22_; lean_object* v___x_23_; lean_object* v___x_24_; 
lean_inc_ref(v_readout_18_);
lean_inc_ref(v_00_u03c8_21_);
v___x_22_ = lean_apply_2(v_readout_18_, v_e0_19_, v_00_u03c8_21_);
v___x_23_ = lean_apply_2(v_readout_18_, v_e1_20_, v_00_u03c8_21_);
v___x_24_ = lean_int_add(v___x_22_, v___x_23_);
lean_dec(v___x_23_);
lean_dec(v___x_22_);
return v___x_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eFalse(uint8_t v_q_25_){
_start:
{
if (v_q_25_ == 0)
{
lean_object* v___x_26_; 
v___x_26_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_26_;
}
else
{
lean_object* v___x_27_; 
v___x_27_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_27_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eFalse___boxed(lean_object* v_q_28_){
_start:
{
uint8_t v_q_boxed_29_; lean_object* v_res_30_; 
v_q_boxed_29_ = lean_unbox(v_q_28_);
v_res_30_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eFalse(v_q_boxed_29_);
return v_res_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eTrue(uint8_t v_q_31_){
_start:
{
if (v_q_31_ == 0)
{
lean_object* v___x_32_; 
v___x_32_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gzero;
return v___x_32_;
}
else
{
lean_object* v___x_33_; 
v___x_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_33_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eTrue___boxed(lean_object* v_q_34_){
_start:
{
uint8_t v_q_boxed_35_; lean_object* v_res_36_; 
v_q_boxed_35_ = lean_unbox(v_q_34_);
v_res_36_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_eTrue(v_q_boxed_35_);
return v_res_36_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had0(uint8_t v_x_37_){
_start:
{
lean_object* v___x_38_; 
v___x_38_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had0___boxed(lean_object* v_x_39_){
_start:
{
uint8_t v_x_4__boxed_40_; lean_object* v_res_41_; 
v_x_4__boxed_40_ = lean_unbox(v_x_39_);
v_res_41_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had0(v_x_4__boxed_40_);
return v_res_41_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___closed__0(void){
_start:
{
lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_42_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
v___x_43_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_42_);
return v___x_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1(uint8_t v_q_44_){
_start:
{
if (v_q_44_ == 0)
{
lean_object* v___x_45_; 
v___x_45_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_45_;
}
else
{
lean_object* v___x_46_; 
v___x_46_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___closed__0);
return v___x_46_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1___boxed(lean_object* v_q_47_){
_start:
{
uint8_t v_q_boxed_48_; lean_object* v_res_49_; 
v_q_boxed_48_ = lean_unbox(v_q_47_);
v_res_49_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_had1(v_q_boxed_48_);
return v_res_49_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot0(uint8_t v_q_50_){
_start:
{
if (v_q_50_ == 0)
{
lean_object* v___x_51_; 
v___x_51_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_51_;
}
else
{
lean_object* v___x_52_; 
v___x_52_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
return v___x_52_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot0___boxed(lean_object* v_q_53_){
_start:
{
uint8_t v_q_boxed_54_; lean_object* v_res_55_; 
v_q_boxed_54_ = lean_unbox(v_q_53_);
v_res_55_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot0(v_q_boxed_54_);
return v_res_55_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___closed__0(void){
_start:
{
lean_object* v___x_56_; lean_object* v___x_57_; 
v___x_56_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gi;
v___x_57_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gneg(v___x_56_);
return v___x_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1(uint8_t v_q_58_){
_start:
{
if (v_q_58_ == 0)
{
lean_object* v___x_59_; 
v___x_59_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_GaussInt_gone;
return v___x_59_;
}
else
{
lean_object* v___x_60_; 
v___x_60_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___closed__0);
return v___x_60_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1___boxed(lean_object* v_q_61_){
_start:
{
uint8_t v_q_boxed_62_; lean_object* v_res_63_; 
v_q_boxed_62_ = lean_unbox(v_q_61_);
v_res_63_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013Frame_rot1(v_q_boxed_62_);
return v_res_63_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H005InnerProductAdmission(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H008PhaseBlindPresentation(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H013BornPairingBoundary(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H013FrameAdditivity(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H008PhaseBlindPresentation(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_H013BornPairingBoundary(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
