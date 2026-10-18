// Lean compiler output
// Module: H048RichardsonErrorMitigation
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
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__3;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_noisy__eval(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_noisy__eval___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(1u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_unsigned_to_nat(2u);
v___x_4_ = lean_nat_to_int(v___x_3_);
return v___x_4_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__2(void){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; lean_object* v___x_7_; 
v___x_5_ = lean_box(0);
v___x_6_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1);
v___x_7_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_7_, 0, v___x_6_);
lean_ctor_set(v___x_7_, 1, v___x_5_);
return v___x_7_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__3(void){
_start:
{
lean_object* v___x_8_; lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_8_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__2);
v___x_9_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0);
v___x_10_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_10_, 0, v___x_9_);
lean_ctor_set(v___x_10_, 1, v___x_8_);
return v___x_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1(void){
_start:
{
lean_object* v___x_11_; 
v___x_11_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__3);
return v___x_11_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__0(void){
_start:
{
lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_12_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0);
v___x_13_ = lean_int_neg(v___x_12_);
return v___x_13_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1(void){
_start:
{
lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; 
v___x_14_ = lean_box(0);
v___x_15_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__0);
v___x_16_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_16_, 0, v___x_15_);
lean_ctor_set(v___x_16_, 1, v___x_14_);
return v___x_16_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__2(void){
_start:
{
lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; 
v___x_17_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1);
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1);
v___x_19_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_19_, 0, v___x_18_);
lean_ctor_set(v___x_19_, 1, v___x_17_);
return v___x_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1(void){
_start:
{
lean_object* v___x_20_; 
v___x_20_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__2);
return v___x_20_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0(void){
_start:
{
lean_object* v___x_21_; lean_object* v___x_22_; 
v___x_21_ = lean_unsigned_to_nat(3u);
v___x_22_ = lean_nat_to_int(v___x_21_);
return v___x_22_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__1(void){
_start:
{
lean_object* v___x_23_; lean_object* v___x_24_; lean_object* v___x_25_; 
v___x_23_ = lean_box(0);
v___x_24_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0);
v___x_25_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_25_, 0, v___x_24_);
lean_ctor_set(v___x_25_, 1, v___x_23_);
return v___x_25_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__2(void){
_start:
{
lean_object* v___x_26_; lean_object* v___x_27_; lean_object* v___x_28_; 
v___x_26_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__1);
v___x_27_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1);
v___x_28_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_28_, 0, v___x_27_);
lean_ctor_set(v___x_28_, 1, v___x_26_);
return v___x_28_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__3(void){
_start:
{
lean_object* v___x_29_; lean_object* v___x_30_; lean_object* v___x_31_; 
v___x_29_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__2);
v___x_30_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0);
v___x_31_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_31_, 0, v___x_30_);
lean_ctor_set(v___x_31_, 1, v___x_29_);
return v___x_31_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2(void){
_start:
{
lean_object* v___x_32_; 
v___x_32_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__3);
return v___x_32_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__0(void){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; 
v___x_33_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0);
v___x_34_ = lean_int_neg(v___x_33_);
return v___x_34_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__1(void){
_start:
{
lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_37_; 
v___x_35_ = lean_box(0);
v___x_36_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0);
v___x_37_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_37_, 0, v___x_36_);
lean_ctor_set(v___x_37_, 1, v___x_35_);
return v___x_37_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__2(void){
_start:
{
lean_object* v___x_38_; lean_object* v___x_39_; lean_object* v___x_40_; 
v___x_38_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__1);
v___x_39_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__0);
v___x_40_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_40_, 0, v___x_39_);
lean_ctor_set(v___x_40_, 1, v___x_38_);
return v___x_40_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__3(void){
_start:
{
lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_41_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__2);
v___x_42_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0);
v___x_43_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_43_, 0, v___x_42_);
lean_ctor_set(v___x_43_, 1, v___x_41_);
return v___x_43_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2(void){
_start:
{
lean_object* v___x_44_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2___closed__3);
return v___x_44_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0(void){
_start:
{
lean_object* v___x_45_; lean_object* v___x_46_; 
v___x_45_ = lean_unsigned_to_nat(4u);
v___x_46_ = lean_nat_to_int(v___x_45_);
return v___x_46_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__1(void){
_start:
{
lean_object* v___x_47_; lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_47_ = lean_box(0);
v___x_48_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0);
v___x_49_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_49_, 0, v___x_48_);
lean_ctor_set(v___x_49_, 1, v___x_47_);
return v___x_49_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__2(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; lean_object* v___x_52_; 
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__1);
v___x_51_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2___closed__0);
v___x_52_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_52_, 0, v___x_51_);
lean_ctor_set(v___x_52_, 1, v___x_50_);
return v___x_52_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__3(void){
_start:
{
lean_object* v___x_53_; lean_object* v___x_54_; lean_object* v___x_55_; 
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__2);
v___x_54_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__1);
v___x_55_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_55_, 0, v___x_54_);
lean_ctor_set(v___x_55_, 1, v___x_53_);
return v___x_55_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__4(void){
_start:
{
lean_object* v___x_56_; lean_object* v___x_57_; lean_object* v___x_58_; 
v___x_56_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__3);
v___x_57_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1___closed__0);
v___x_58_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_58_, 0, v___x_57_);
lean_ctor_set(v___x_58_, 1, v___x_56_);
return v___x_58_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3(void){
_start:
{
lean_object* v___x_59_; 
v___x_59_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__4);
return v___x_59_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__0(void){
_start:
{
lean_object* v___x_60_; lean_object* v___x_61_; 
v___x_60_ = lean_unsigned_to_nat(6u);
v___x_61_ = lean_nat_to_int(v___x_60_);
return v___x_61_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__1(void){
_start:
{
lean_object* v___x_62_; lean_object* v___x_63_; 
v___x_62_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__0);
v___x_63_ = lean_int_neg(v___x_62_);
return v___x_63_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__2(void){
_start:
{
lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; 
v___x_64_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1___closed__1);
v___x_65_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0);
v___x_66_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_66_, 0, v___x_65_);
lean_ctor_set(v___x_66_, 1, v___x_64_);
return v___x_66_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__3(void){
_start:
{
lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; 
v___x_67_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__2);
v___x_68_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__1);
v___x_69_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_69_, 0, v___x_68_);
lean_ctor_set(v___x_69_, 1, v___x_67_);
return v___x_69_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__4(void){
_start:
{
lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; 
v___x_70_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__3);
v___x_71_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3___closed__0);
v___x_72_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_72_, 0, v___x_71_);
lean_ctor_set(v___x_72_, 1, v___x_70_);
return v___x_72_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3(void){
_start:
{
lean_object* v___x_73_; 
v___x_73_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3___closed__4);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_noisy__eval(lean_object* v_E0_74_, lean_object* v_c1_75_, lean_object* v_c2_76_, lean_object* v_c3_77_, lean_object* v_lam_78_){
_start:
{
lean_object* v___x_79_; lean_object* v___x_80_; lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; lean_object* v___x_86_; lean_object* v___x_87_; 
v___x_79_ = lean_int_mul(v_c1_75_, v_lam_78_);
v___x_80_ = lean_int_add(v_E0_74_, v___x_79_);
lean_dec(v___x_79_);
v___x_81_ = lean_int_mul(v_c2_76_, v_lam_78_);
v___x_82_ = lean_int_mul(v___x_81_, v_lam_78_);
lean_dec(v___x_81_);
v___x_83_ = lean_int_add(v___x_80_, v___x_82_);
lean_dec(v___x_82_);
lean_dec(v___x_80_);
v___x_84_ = lean_int_mul(v_c3_77_, v_lam_78_);
v___x_85_ = lean_int_mul(v___x_84_, v_lam_78_);
lean_dec(v___x_84_);
v___x_86_ = lean_int_mul(v___x_85_, v_lam_78_);
lean_dec(v___x_85_);
v___x_87_ = lean_int_add(v___x_83_, v___x_86_);
lean_dec(v___x_86_);
lean_dec(v___x_83_);
return v___x_87_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H048_noisy__eval___boxed(lean_object* v_E0_88_, lean_object* v_c1_89_, lean_object* v_c2_90_, lean_object* v_c3_91_, lean_object* v_lam_92_){
_start:
{
lean_object* v_res_93_; 
v_res_93_ = lp_FiniteQuantum_FableHilbertWalk20260819_H048_noisy__eval(v_E0_88_, v_c1_89_, v_c2_90_, v_c3_91_, v_lam_92_);
lean_dec(v_lam_92_);
lean_dec(v_c3_91_);
lean_dec(v_c2_90_);
lean_dec(v_c1_89_);
lean_dec(v_E0_88_);
return v_res_93_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H048RichardsonErrorMitigation(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales1);
lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights1);
lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales2);
lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights2);
lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H048_scales3);
lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H048_weights3);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
