// Lean compiler output
// Module: H037FourQubitCssSurfaceCode
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
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
lean_object* l_Int_mul___boxed(lean_object*, lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_emod(lean_object*, lean_object*);
uint8_t lean_int_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H037_dot4_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H037_dot4_spec__0___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)l_Int_mul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1;
static const lean_array_object lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_array_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 246}, .m_size = 0, .m_capacity = 0, .m_data = {}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__2_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_szX;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxX;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxZ;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1X;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1Z;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2X;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2Z;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2X;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2Z;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__1;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H037_dot4_spec__0(lean_object* v_x_1_, lean_object* v_x_2_){
_start:
{
if (lean_obj_tag(v_x_2_) == 0)
{
return v_x_1_;
}
else
{
lean_object* v_head_3_; lean_object* v_tail_4_; lean_object* v___x_5_; 
v_head_3_ = lean_ctor_get(v_x_2_, 0);
v_tail_4_ = lean_ctor_get(v_x_2_, 1);
v___x_5_ = lean_int_add(v_x_1_, v_head_3_);
lean_dec(v_x_1_);
v_x_1_ = v___x_5_;
v_x_2_ = v_tail_4_;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H037_dot4_spec__0___boxed(lean_object* v_x_7_, lean_object* v_x_8_){
_start:
{
lean_object* v_res_9_; 
v_res_9_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H037_dot4_spec__0(v_x_7_, v_x_8_);
lean_dec(v_x_8_);
return v_res_9_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_11_ = lean_unsigned_to_nat(0u);
v___x_12_ = lean_nat_to_int(v___x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4(lean_object* v_a_15_, lean_object* v_b_16_){
_start:
{
lean_object* v___f_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; 
v___f_17_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__0));
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_19_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__2));
v___x_20_ = l___private_Init_Data_List_Impl_0__List_zipWithTR_go___redArg(v___f_17_, v_a_15_, v_b_16_, v___x_19_);
v___x_21_ = lp_FiniteQuantum_List_foldl___at___00FableHilbertWalk20260819_H037_dot4_spec__0(v___x_18_, v___x_20_);
lean_dec(v___x_20_);
return v___x_21_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__0(void){
_start:
{
lean_object* v___x_22_; lean_object* v___x_23_; 
v___x_22_ = lean_unsigned_to_nat(2u);
v___x_23_ = lean_nat_to_int(v___x_22_);
return v___x_23_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1(void){
_start:
{
lean_object* v___x_24_; lean_object* v___x_25_; 
v___x_24_ = lean_unsigned_to_nat(1u);
v___x_25_ = lean_nat_to_int(v___x_24_);
return v___x_25_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__2(void){
_start:
{
lean_object* v___x_26_; lean_object* v___x_27_; 
v___x_26_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_27_ = lean_int_neg(v___x_26_);
return v___x_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase(lean_object* v_x1_28_, lean_object* v_z1_29_, lean_object* v_x2_30_, lean_object* v_z2_31_){
_start:
{
lean_object* v___x_32_; lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_37_; uint8_t v___x_38_; 
v___x_32_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4(v_x1_28_, v_z2_31_);
v___x_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4(v_z1_29_, v_x2_30_);
v___x_34_ = lean_int_add(v___x_32_, v___x_33_);
lean_dec(v___x_33_);
lean_dec(v___x_32_);
v___x_35_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__0);
v___x_36_ = lean_int_emod(v___x_34_, v___x_35_);
lean_dec(v___x_34_);
v___x_37_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_38_ = lean_int_dec_eq(v___x_36_, v___x_37_);
lean_dec(v___x_36_);
if (v___x_38_ == 0)
{
lean_object* v___x_39_; 
v___x_39_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__2);
return v___x_39_;
}
else
{
lean_object* v___x_40_; 
v___x_40_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
return v___x_40_;
}
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0(void){
_start:
{
lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; 
v___x_41_ = lean_box(0);
v___x_42_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_43_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_43_, 0, v___x_42_);
lean_ctor_set(v___x_43_, 1, v___x_41_);
return v___x_43_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1(void){
_start:
{
lean_object* v___x_44_; lean_object* v___x_45_; lean_object* v___x_46_; 
v___x_44_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0);
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_46_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_46_, 0, v___x_45_);
lean_ctor_set(v___x_46_, 1, v___x_44_);
return v___x_46_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2(void){
_start:
{
lean_object* v___x_47_; lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_47_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1);
v___x_48_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_49_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_49_, 0, v___x_48_);
lean_ctor_set(v___x_49_, 1, v___x_47_);
return v___x_49_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__3(void){
_start:
{
lean_object* v___x_50_; lean_object* v___x_51_; lean_object* v___x_52_; 
v___x_50_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2);
v___x_51_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_52_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_52_, 0, v___x_51_);
lean_ctor_set(v___x_52_, 1, v___x_50_);
return v___x_52_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero(void){
_start:
{
lean_object* v___x_53_; 
v___x_53_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__3);
return v___x_53_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szX(void){
_start:
{
lean_object* v___x_54_; 
v___x_54_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0(void){
_start:
{
lean_object* v___x_55_; lean_object* v___x_56_; lean_object* v___x_57_; 
v___x_55_ = lean_box(0);
v___x_56_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_57_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_57_, 0, v___x_56_);
lean_ctor_set(v___x_57_, 1, v___x_55_);
return v___x_57_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__1(void){
_start:
{
lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; 
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0);
v___x_59_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_60_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_60_, 0, v___x_59_);
lean_ctor_set(v___x_60_, 1, v___x_58_);
return v___x_60_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__2(void){
_start:
{
lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; 
v___x_61_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__1);
v___x_62_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_63_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_63_, 0, v___x_62_);
lean_ctor_set(v___x_63_, 1, v___x_61_);
return v___x_63_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3(void){
_start:
{
lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; 
v___x_64_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__2);
v___x_65_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_66_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_66_, 0, v___x_65_);
lean_ctor_set(v___x_66_, 1, v___x_64_);
return v___x_66_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ(void){
_start:
{
lean_object* v___x_67_; 
v___x_67_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3);
return v___x_67_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxX(void){
_start:
{
lean_object* v___x_68_; 
v___x_68_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__3);
return v___x_68_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxZ(void){
_start:
{
lean_object* v___x_69_; 
v___x_69_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
return v___x_69_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1X(void){
_start:
{
lean_object* v___x_70_; 
v___x_70_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
return v___x_70_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0(void){
_start:
{
lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; 
v___x_71_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__1);
v___x_72_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_73_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_73_, 0, v___x_72_);
lean_ctor_set(v___x_73_, 1, v___x_71_);
return v___x_73_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1(void){
_start:
{
lean_object* v___x_74_; lean_object* v___x_75_; lean_object* v___x_76_; 
v___x_74_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0);
v___x_75_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_76_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_76_, 0, v___x_75_);
lean_ctor_set(v___x_76_, 1, v___x_74_);
return v___x_76_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z(void){
_start:
{
lean_object* v___x_77_; 
v___x_77_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1);
return v___x_77_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__0(void){
_start:
{
lean_object* v___x_78_; lean_object* v___x_79_; lean_object* v___x_80_; 
v___x_78_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__0);
v___x_79_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_80_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_80_, 0, v___x_79_);
lean_ctor_set(v___x_80_, 1, v___x_78_);
return v___x_80_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1(void){
_start:
{
lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; 
v___x_81_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__0);
v___x_82_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_83_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_83_, 0, v___x_82_);
lean_ctor_set(v___x_83_, 1, v___x_81_);
return v___x_83_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2(void){
_start:
{
lean_object* v___x_84_; lean_object* v___x_85_; lean_object* v___x_86_; 
v___x_84_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1);
v___x_85_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_86_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_86_, 0, v___x_85_);
lean_ctor_set(v___x_86_, 1, v___x_84_);
return v___x_86_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X(void){
_start:
{
lean_object* v___x_87_; 
v___x_87_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2);
return v___x_87_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1Z(void){
_start:
{
lean_object* v___x_88_; 
v___x_88_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
return v___x_88_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2X(void){
_start:
{
lean_object* v___x_89_; 
v___x_89_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
return v___x_89_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2Z(void){
_start:
{
lean_object* v___x_90_; 
v___x_90_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__2);
return v___x_90_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2X(void){
_start:
{
lean_object* v___x_91_; 
v___x_91_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__1);
return v___x_91_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2Z(void){
_start:
{
lean_object* v___x_92_; 
v___x_92_ = lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero;
return v___x_92_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0___closed__0(void){
_start:
{
lean_object* v___x_93_; lean_object* v___x_94_; lean_object* v___x_95_; 
v___x_93_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero___closed__2);
v___x_94_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_pauliPhase___closed__1);
v___x_95_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_95_, 0, v___x_94_);
lean_ctor_set(v___x_95_, 1, v___x_93_);
return v___x_95_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0(void){
_start:
{
lean_object* v___x_96_; 
v___x_96_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0___closed__0);
return v___x_96_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1___closed__0(void){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; lean_object* v___x_99_; 
v___x_97_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z___closed__0);
v___x_98_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_99_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_99_, 0, v___x_98_);
lean_ctor_set(v___x_99_, 1, v___x_97_);
return v___x_99_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1(void){
_start:
{
lean_object* v___x_100_; 
v___x_100_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1___closed__0);
return v___x_100_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2___closed__0(void){
_start:
{
lean_object* v___x_101_; lean_object* v___x_102_; lean_object* v___x_103_; 
v___x_101_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X___closed__1);
v___x_102_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_103_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_103_, 0, v___x_102_);
lean_ctor_set(v___x_103_, 1, v___x_101_);
return v___x_103_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2(void){
_start:
{
lean_object* v___x_104_; 
v___x_104_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2___closed__0);
return v___x_104_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__0(void){
_start:
{
lean_object* v___x_105_; lean_object* v___x_106_; lean_object* v___x_107_; 
v___x_105_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ___closed__0);
v___x_106_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_107_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_107_, 0, v___x_106_);
lean_ctor_set(v___x_107_, 1, v___x_105_);
return v___x_107_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__1(void){
_start:
{
lean_object* v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; 
v___x_108_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__0);
v___x_109_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_110_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_110_, 0, v___x_109_);
lean_ctor_set(v___x_110_, 1, v___x_108_);
return v___x_110_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__2(void){
_start:
{
lean_object* v___x_111_; lean_object* v___x_112_; lean_object* v___x_113_; 
v___x_111_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__1);
v___x_112_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_dot4___closed__1);
v___x_113_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v___x_113_, 0, v___x_112_);
lean_ctor_set(v___x_113_, 1, v___x_111_);
return v___x_113_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3(void){
_start:
{
lean_object* v___x_114_; 
v___x_114_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__2, &lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__2_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3___closed__2);
return v___x_114_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H037FourQubitCssSurfaceCode(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_zZero);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_szX = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szX();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_szX);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_szZ);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxX = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxX();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxX);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxZ = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxZ();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_sxZ);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1X = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1X();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1X);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl1Z);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1X);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1Z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1Z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl1Z);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2X = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2X();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2X);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2Z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2Z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_zl2Z);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2X = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2X();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2X);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2Z = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2Z();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xl2Z);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr0);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr1);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr2);
lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3 = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H037_xErr3);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
