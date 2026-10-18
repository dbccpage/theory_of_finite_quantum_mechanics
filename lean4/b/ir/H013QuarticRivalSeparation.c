// Lean compiler output
// Module: H013QuarticRivalSeparation
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
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* l_Int_pow(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_normSq(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_normSq___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quadReadout(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quadReadout___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quartReadout(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quartReadout___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_psi;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot(lean_object* v_u_1_, lean_object* v_v_2_){
_start:
{
lean_object* v_x_3_; lean_object* v_y_4_; lean_object* v_x_5_; lean_object* v_y_6_; lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_9_; 
v_x_3_ = lean_ctor_get(v_u_1_, 0);
v_y_4_ = lean_ctor_get(v_u_1_, 1);
v_x_5_ = lean_ctor_get(v_v_2_, 0);
v_y_6_ = lean_ctor_get(v_v_2_, 1);
v___x_7_ = lean_int_mul(v_x_3_, v_x_5_);
v___x_8_ = lean_int_mul(v_y_4_, v_y_6_);
v___x_9_ = lean_int_add(v___x_7_, v___x_8_);
lean_dec(v___x_8_);
lean_dec(v___x_7_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot___boxed(lean_object* v_u_10_, lean_object* v_v_11_){
_start:
{
lean_object* v_res_12_; 
v_res_12_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot(v_u_10_, v_v_11_);
lean_dec_ref(v_v_11_);
lean_dec_ref(v_u_10_);
return v_res_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_normSq(lean_object* v_u_13_){
_start:
{
lean_object* v___x_14_; 
v___x_14_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot(v_u_13_, v_u_13_);
return v___x_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_normSq___boxed(lean_object* v_u_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_normSq(v_u_15_);
lean_dec_ref(v_u_15_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quadReadout(lean_object* v_u_17_, lean_object* v_v_18_){
_start:
{
lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___x_19_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot(v_u_17_, v_v_18_);
v___x_20_ = lean_unsigned_to_nat(2u);
v___x_21_ = l_Int_pow(v___x_19_, v___x_20_);
lean_dec(v___x_19_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quadReadout___boxed(lean_object* v_u_22_, lean_object* v_v_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quadReadout(v_u_22_, v_v_23_);
lean_dec_ref(v_v_23_);
lean_dec_ref(v_u_22_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quartReadout(lean_object* v_u_25_, lean_object* v_v_26_){
_start:
{
lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; 
v___x_27_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_dot(v_u_25_, v_v_26_);
v___x_28_ = lean_unsigned_to_nat(4u);
v___x_29_ = l_Int_pow(v___x_27_, v___x_28_);
lean_dec(v___x_27_);
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quartReadout___boxed(lean_object* v_u_30_, lean_object* v_v_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_quartReadout(v_u_30_, v_v_31_);
lean_dec_ref(v_v_31_);
lean_dec_ref(v_u_30_);
return v_res_32_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_unsigned_to_nat(5u);
v___x_34_ = lean_nat_to_int(v___x_33_);
return v___x_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1(void){
_start:
{
lean_object* v___x_35_; lean_object* v___x_36_; 
v___x_35_ = lean_unsigned_to_nat(0u);
v___x_36_ = lean_nat_to_int(v___x_35_);
return v___x_36_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2(void){
_start:
{
lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_37_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1);
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0);
v___x_39_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_39_, 0, v___x_38_);
lean_ctor_set(v___x_39_, 1, v___x_37_);
return v___x_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1(void){
_start:
{
lean_object* v___x_40_; 
v___x_40_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2);
return v___x_40_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2___closed__0(void){
_start:
{
lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_41_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__0);
v___x_42_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__1);
v___x_43_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_43_, 0, v___x_42_);
lean_ctor_set(v___x_43_, 1, v___x_41_);
return v___x_43_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2(void){
_start:
{
lean_object* v___x_44_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2___closed__0);
return v___x_44_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0(void){
_start:
{
lean_object* v___x_45_; lean_object* v___x_46_; 
v___x_45_ = lean_unsigned_to_nat(3u);
v___x_46_ = lean_nat_to_int(v___x_45_);
return v___x_46_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1(void){
_start:
{
lean_object* v___x_47_; lean_object* v___x_48_; 
v___x_47_ = lean_unsigned_to_nat(4u);
v___x_48_ = lean_nat_to_int(v___x_47_);
return v___x_48_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__2(void){
_start:
{
lean_object* v___x_49_; lean_object* v___x_50_; lean_object* v___x_51_; 
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1);
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0);
v___x_51_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_51_, 0, v___x_50_);
lean_ctor_set(v___x_51_, 1, v___x_49_);
return v___x_51_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1(void){
_start:
{
lean_object* v___x_52_; 
v___x_52_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__2);
return v___x_52_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__0(void){
_start:
{
lean_object* v___x_53_; lean_object* v___x_54_; 
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__1);
v___x_54_ = lean_int_neg(v___x_53_);
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__1(void){
_start:
{
lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; 
v___x_55_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1___closed__0);
v___x_56_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__0);
v___x_57_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_57_, 0, v___x_56_);
lean_ctor_set(v___x_57_, 1, v___x_55_);
return v___x_57_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2(void){
_start:
{
lean_object* v___x_58_; 
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2___closed__1);
return v___x_58_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_psi(void){
_start:
{
lean_object* v___x_59_; 
v___x_59_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1___closed__2);
return v___x_59_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H013QuarticRivalSeparation(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e1);
lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_e2);
lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p1);
lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_p2);
lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_psi = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_psi();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H013QuarticSeparation_psi);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
