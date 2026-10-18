// Lean compiler output
// Module: FermionSignCore
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
lean_object* lean_nat_to_int(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_instDecidableD2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_instDecidableD2___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_swap(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_swap___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_instDecidableD2__rev(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_instDecidableD2__rev___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_instDecidableS2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_instDecidableS2___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_instDecidableD2(uint8_t v_x_1_, uint8_t v_y_2_){
_start:
{
uint8_t v___x_3_; 
v___x_3_ = 0;
if (v_x_1_ == 0)
{
if (v_y_2_ == 0)
{
return v___x_3_;
}
else
{
return v_y_2_;
}
}
else
{
return v___x_3_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_instDecidableD2___boxed(lean_object* v_x_4_, lean_object* v_y_5_){
_start:
{
uint8_t v_x_boxed_6_; uint8_t v_y_boxed_7_; uint8_t v_res_8_; lean_object* v_r_9_; 
v_x_boxed_6_ = lean_unbox(v_x_4_);
v_y_boxed_7_ = lean_unbox(v_y_5_);
v_res_8_ = lp_FiniteQuantum_FermionSignTower_instDecidableD2(v_x_boxed_6_, v_y_boxed_7_);
v_r_9_ = lean_box(v_res_8_);
return v_r_9_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_swap(uint8_t v_b_10_){
_start:
{
if (v_b_10_ == 0)
{
uint8_t v___x_11_; 
v___x_11_ = 1;
return v___x_11_;
}
else
{
uint8_t v___x_12_; 
v___x_12_ = 0;
return v___x_12_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_swap___boxed(lean_object* v_b_13_){
_start:
{
uint8_t v_b_boxed_14_; uint8_t v_res_15_; lean_object* v_r_16_; 
v_b_boxed_14_ = lean_unbox(v_b_13_);
v_res_15_ = lp_FiniteQuantum_FermionSignTower_swap(v_b_boxed_14_);
v_r_16_ = lean_box(v_res_15_);
return v_r_16_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_instDecidableD2__rev(uint8_t v_x_17_, uint8_t v_y_18_){
_start:
{
uint8_t v___x_19_; uint8_t v___x_20_; uint8_t v___x_21_; 
v___x_19_ = lp_FiniteQuantum_FermionSignTower_swap(v_x_17_);
v___x_20_ = lp_FiniteQuantum_FermionSignTower_swap(v_y_18_);
v___x_21_ = lp_FiniteQuantum_FermionSignTower_instDecidableD2(v___x_19_, v___x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_instDecidableD2__rev___boxed(lean_object* v_x_22_, lean_object* v_y_23_){
_start:
{
uint8_t v_x_boxed_24_; uint8_t v_y_boxed_25_; uint8_t v_res_26_; lean_object* v_r_27_; 
v_x_boxed_24_ = lean_unbox(v_x_22_);
v_y_boxed_25_ = lean_unbox(v_y_23_);
v_res_26_ = lp_FiniteQuantum_FermionSignTower_instDecidableD2__rev(v_x_boxed_24_, v_y_boxed_25_);
v_r_27_ = lean_box(v_res_26_);
return v_r_27_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FermionSignTower_instDecidableS2(uint8_t v_x_28_, uint8_t v_y_29_){
_start:
{
uint8_t v___x_30_; uint8_t v___x_31_; 
v___x_30_ = lp_FiniteQuantum_FermionSignTower_instDecidableD2(v_y_29_, v_x_28_);
v___x_31_ = lp_FiniteQuantum_FermionSignTower_instDecidableD2(v_x_28_, v_y_29_);
if (v___x_31_ == 0)
{
return v___x_30_;
}
else
{
return v___x_31_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FermionSignTower_instDecidableS2___boxed(lean_object* v_x_32_, lean_object* v_y_33_){
_start:
{
uint8_t v_x_boxed_34_; uint8_t v_y_boxed_35_; uint8_t v_res_36_; lean_object* v_r_37_; 
v_x_boxed_34_ = lean_unbox(v_x_32_);
v_y_boxed_35_ = lean_unbox(v_y_33_);
v_res_36_ = lp_FiniteQuantum_FermionSignTower_instDecidableS2(v_x_boxed_34_, v_y_boxed_35_);
v_r_37_ = lean_box(v_res_36_);
return v_r_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__0(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_38_ = lean_unsigned_to_nat(0u);
v___x_39_ = lean_nat_to_int(v___x_38_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__1(void){
_start:
{
uint8_t v___x_40_; lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_40_ = 1;
v___x_41_ = lean_obj_once(&lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__0, &lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__0_once, _init_lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__0);
v___x_42_ = lean_unsigned_to_nat(2u);
v___x_43_ = lean_alloc_ctor(0, 3, 1);
lean_ctor_set(v___x_43_, 0, v___x_42_);
lean_ctor_set(v___x_43_, 1, v___x_42_);
lean_ctor_set(v___x_43_, 2, v___x_41_);
lean_ctor_set_uint8(v___x_43_, sizeof(void*)*3, v___x_40_);
return v___x_43_;
}
}
static lean_object* _init_lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket(void){
_start:
{
lean_object* v___x_44_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__1, &lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__1_once, _init_lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket___closed__1);
return v___x_44_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_FermionSignCore(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket = _init_lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket();
lean_mark_persistent(lp_FiniteQuantum_FermionSignTower_exactMeronCancellationPacket);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
