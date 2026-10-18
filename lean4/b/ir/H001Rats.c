// Lean compiler output
// Module: H001Rats
// Imports: public import Init public meta import Init public import HWKernel
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
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_preQSetoid;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mkQ(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mkQ___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pneg(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_phalf;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_addPre(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_addPre___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mulPre(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mulPre___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fadd(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fadd___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fmul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fmul___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fneg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___lam__0___boxed(lean_object*);
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___lam__0___boxed, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__0_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fadd___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__1 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__1_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fmul___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__2 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__2_value;
static const lean_closure_object lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fneg, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__3 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__4;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_uniformHalf(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_uniformHalf___boxed(lean_object*);
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_preQSetoid(void){
_start:
{
lean_object* v___x_1_; 
v___x_1_ = lean_box(0);
return v___x_1_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mkQ(lean_object* v_x_2_){
_start:
{
lean_inc_ref(v_x_2_);
return v_x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mkQ___boxed(lean_object* v_x_3_){
_start:
{
lean_object* v_res_4_; 
v_res_4_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mkQ(v_x_3_);
lean_dec_ref(v_x_3_);
return v_res_4_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0(void){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; 
v___x_5_ = lean_unsigned_to_nat(1u);
v___x_6_ = lean_nat_to_int(v___x_5_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt(lean_object* v_n_7_){
_start:
{
lean_object* v___x_8_; lean_object* v___x_9_; 
v___x_8_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0);
v___x_9_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_9_, 0, v_n_7_);
lean_ctor_set(v___x_9_, 1, v___x_8_);
return v___x_9_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0(void){
_start:
{
lean_object* v___x_10_; lean_object* v___x_11_; 
v___x_10_ = lean_unsigned_to_nat(0u);
v___x_11_ = lean_nat_to_int(v___x_10_);
return v___x_11_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__1(void){
_start:
{
lean_object* v___x_12_; lean_object* v___x_13_; 
v___x_12_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0);
v___x_13_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt(v___x_12_);
return v___x_13_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero(void){
_start:
{
lean_object* v___x_14_; 
v___x_14_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__1);
return v___x_14_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone___closed__0(void){
_start:
{
lean_object* v___x_15_; lean_object* v___x_16_; 
v___x_15_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0);
v___x_16_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt(v___x_15_);
return v___x_16_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone(void){
_start:
{
lean_object* v___x_17_; 
v___x_17_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone___closed__0);
return v___x_17_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__0(void){
_start:
{
lean_object* v___x_18_; lean_object* v___x_19_; 
v___x_18_ = lean_unsigned_to_nat(2u);
v___x_19_ = lean_nat_to_int(v___x_18_);
return v___x_19_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1(void){
_start:
{
lean_object* v___x_20_; lean_object* v___x_21_; lean_object* v___x_22_; 
v___x_20_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__0);
v___x_21_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0);
v___x_22_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_22_, 0, v___x_21_);
lean_ctor_set(v___x_22_, 1, v___x_20_);
return v___x_22_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half(void){
_start:
{
lean_object* v___x_23_; 
v___x_23_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1);
return v___x_23_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd(lean_object* v_x_24_, lean_object* v_y_25_){
_start:
{
lean_object* v_num_26_; lean_object* v_den_27_; lean_object* v_num_28_; lean_object* v_den_29_; lean_object* v___x_31_; uint8_t v_isShared_32_; uint8_t v_isSharedCheck_40_; 
v_num_26_ = lean_ctor_get(v_x_24_, 0);
v_den_27_ = lean_ctor_get(v_x_24_, 1);
v_num_28_ = lean_ctor_get(v_y_25_, 0);
v_den_29_ = lean_ctor_get(v_y_25_, 1);
v_isSharedCheck_40_ = !lean_is_exclusive(v_y_25_);
if (v_isSharedCheck_40_ == 0)
{
v___x_31_ = v_y_25_;
v_isShared_32_ = v_isSharedCheck_40_;
goto v_resetjp_30_;
}
else
{
lean_inc(v_den_29_);
lean_inc(v_num_28_);
lean_dec(v_y_25_);
v___x_31_ = lean_box(0);
v_isShared_32_ = v_isSharedCheck_40_;
goto v_resetjp_30_;
}
v_resetjp_30_:
{
lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_38_; 
v___x_33_ = lean_int_mul(v_num_26_, v_den_29_);
v___x_34_ = lean_int_mul(v_num_28_, v_den_27_);
lean_dec(v_num_28_);
v___x_35_ = lean_int_add(v___x_33_, v___x_34_);
lean_dec(v___x_34_);
lean_dec(v___x_33_);
v___x_36_ = lean_int_mul(v_den_27_, v_den_29_);
lean_dec(v_den_29_);
if (v_isShared_32_ == 0)
{
lean_ctor_set(v___x_31_, 1, v___x_36_);
lean_ctor_set(v___x_31_, 0, v___x_35_);
v___x_38_ = v___x_31_;
goto v_reusejp_37_;
}
else
{
lean_object* v_reuseFailAlloc_39_; 
v_reuseFailAlloc_39_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_39_, 0, v___x_35_);
lean_ctor_set(v_reuseFailAlloc_39_, 1, v___x_36_);
v___x_38_ = v_reuseFailAlloc_39_;
goto v_reusejp_37_;
}
v_reusejp_37_:
{
return v___x_38_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd___boxed(lean_object* v_x_41_, lean_object* v_y_42_){
_start:
{
lean_object* v_res_43_; 
v_res_43_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd(v_x_41_, v_y_42_);
lean_dec_ref(v_x_41_);
return v_res_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul(lean_object* v_x_44_, lean_object* v_y_45_){
_start:
{
lean_object* v_num_46_; lean_object* v_den_47_; lean_object* v_num_48_; lean_object* v_den_49_; lean_object* v___x_51_; uint8_t v_isShared_52_; uint8_t v_isSharedCheck_58_; 
v_num_46_ = lean_ctor_get(v_x_44_, 0);
v_den_47_ = lean_ctor_get(v_x_44_, 1);
v_num_48_ = lean_ctor_get(v_y_45_, 0);
v_den_49_ = lean_ctor_get(v_y_45_, 1);
v_isSharedCheck_58_ = !lean_is_exclusive(v_y_45_);
if (v_isSharedCheck_58_ == 0)
{
v___x_51_ = v_y_45_;
v_isShared_52_ = v_isSharedCheck_58_;
goto v_resetjp_50_;
}
else
{
lean_inc(v_den_49_);
lean_inc(v_num_48_);
lean_dec(v_y_45_);
v___x_51_ = lean_box(0);
v_isShared_52_ = v_isSharedCheck_58_;
goto v_resetjp_50_;
}
v_resetjp_50_:
{
lean_object* v___x_53_; lean_object* v___x_54_; lean_object* v___x_56_; 
v___x_53_ = lean_int_mul(v_num_46_, v_num_48_);
lean_dec(v_num_48_);
v___x_54_ = lean_int_mul(v_den_47_, v_den_49_);
lean_dec(v_den_49_);
if (v_isShared_52_ == 0)
{
lean_ctor_set(v___x_51_, 1, v___x_54_);
lean_ctor_set(v___x_51_, 0, v___x_53_);
v___x_56_ = v___x_51_;
goto v_reusejp_55_;
}
else
{
lean_object* v_reuseFailAlloc_57_; 
v_reuseFailAlloc_57_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_57_, 0, v___x_53_);
lean_ctor_set(v_reuseFailAlloc_57_, 1, v___x_54_);
v___x_56_ = v_reuseFailAlloc_57_;
goto v_reusejp_55_;
}
v_reusejp_55_:
{
return v___x_56_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul___boxed(lean_object* v_x_59_, lean_object* v_y_60_){
_start:
{
lean_object* v_res_61_; 
v_res_61_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul(v_x_59_, v_y_60_);
lean_dec_ref(v_x_59_);
return v_res_61_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pneg(lean_object* v_x_62_){
_start:
{
lean_object* v_num_63_; lean_object* v_den_64_; lean_object* v___x_66_; uint8_t v_isShared_67_; uint8_t v_isSharedCheck_72_; 
v_num_63_ = lean_ctor_get(v_x_62_, 0);
v_den_64_ = lean_ctor_get(v_x_62_, 1);
v_isSharedCheck_72_ = !lean_is_exclusive(v_x_62_);
if (v_isSharedCheck_72_ == 0)
{
v___x_66_ = v_x_62_;
v_isShared_67_ = v_isSharedCheck_72_;
goto v_resetjp_65_;
}
else
{
lean_inc(v_den_64_);
lean_inc(v_num_63_);
lean_dec(v_x_62_);
v___x_66_ = lean_box(0);
v_isShared_67_ = v_isSharedCheck_72_;
goto v_resetjp_65_;
}
v_resetjp_65_:
{
lean_object* v___x_68_; lean_object* v___x_70_; 
v___x_68_ = lean_int_neg(v_num_63_);
lean_dec(v_num_63_);
if (v_isShared_67_ == 0)
{
lean_ctor_set(v___x_66_, 0, v___x_68_);
v___x_70_ = v___x_66_;
goto v_reusejp_69_;
}
else
{
lean_object* v_reuseFailAlloc_71_; 
v_reuseFailAlloc_71_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_71_, 0, v___x_68_);
lean_ctor_set(v_reuseFailAlloc_71_, 1, v_den_64_);
v___x_70_ = v_reuseFailAlloc_71_;
goto v_reusejp_69_;
}
v_reusejp_69_:
{
return v___x_70_;
}
}
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero___closed__0(void){
_start:
{
lean_object* v___x_73_; lean_object* v___x_74_; lean_object* v___x_75_; 
v___x_73_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0);
v___x_74_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero___closed__0);
v___x_75_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_75_, 0, v___x_74_);
lean_ctor_set(v___x_75_, 1, v___x_73_);
return v___x_75_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero(void){
_start:
{
lean_object* v___x_76_; 
v___x_76_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero___closed__0);
return v___x_76_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone___closed__0(void){
_start:
{
lean_object* v___x_77_; lean_object* v___x_78_; 
v___x_77_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_ofInt___closed__0);
v___x_78_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_78_, 0, v___x_77_);
lean_ctor_set(v___x_78_, 1, v___x_77_);
return v___x_78_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone(void){
_start:
{
lean_object* v___x_79_; 
v___x_79_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone___closed__0);
return v___x_79_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_phalf(void){
_start:
{
lean_object* v___x_80_; 
v___x_80_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half___closed__1);
return v___x_80_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_addPre(lean_object* v_a_81_, lean_object* v_y_82_){
_start:
{
lean_object* v___x_83_; 
v___x_83_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd(v_a_81_, v_y_82_);
return v___x_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_addPre___boxed(lean_object* v_a_84_, lean_object* v_y_85_){
_start:
{
lean_object* v_res_86_; 
v_res_86_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_addPre(v_a_84_, v_y_85_);
lean_dec_ref(v_a_84_);
return v_res_86_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mulPre(lean_object* v_a_87_, lean_object* v_y_88_){
_start:
{
lean_object* v___x_89_; 
v___x_89_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul(v_a_87_, v_y_88_);
return v___x_89_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mulPre___boxed(lean_object* v_a_90_, lean_object* v_y_91_){
_start:
{
lean_object* v_res_92_; 
v_res_92_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_mulPre(v_a_90_, v_y_91_);
lean_dec_ref(v_a_90_);
return v_res_92_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fadd(lean_object* v_x_93_, lean_object* v_y_94_){
_start:
{
lean_object* v___x_95_; 
v___x_95_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_padd(v_x_93_, v_y_94_);
return v___x_95_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fadd___boxed(lean_object* v_x_96_, lean_object* v_y_97_){
_start:
{
lean_object* v_res_98_; 
v_res_98_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fadd(v_x_96_, v_y_97_);
lean_dec(v_x_96_);
return v_res_98_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fmul(lean_object* v_x_99_, lean_object* v_y_100_){
_start:
{
lean_object* v___x_101_; 
v___x_101_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pmul(v_x_99_, v_y_100_);
return v___x_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fmul___boxed(lean_object* v_x_102_, lean_object* v_y_103_){
_start:
{
lean_object* v_res_104_; 
v_res_104_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fmul(v_x_102_, v_y_103_);
lean_dec(v_x_102_);
return v_res_104_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fneg(lean_object* v_x_105_){
_start:
{
lean_object* v___x_106_; 
v___x_106_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pneg(v_x_105_);
return v___x_106_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___lam__0(lean_object* v___y_107_){
_start:
{
lean_inc(v___y_107_);
return v___y_107_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___lam__0___boxed(lean_object* v___y_108_){
_start:
{
lean_object* v_res_109_; 
v_res_109_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___lam__0(v___y_108_);
lean_dec(v___y_108_);
return v_res_109_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__4(void){
_start:
{
lean_object* v___f_114_; lean_object* v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; lean_object* v___x_118_; lean_object* v___x_119_; lean_object* v___x_120_; 
v___f_114_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__0));
v___x_115_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone;
v___x_116_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero;
v___x_117_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__3));
v___x_118_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__2));
v___x_119_ = ((lean_object*)(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__1));
v___x_120_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_120_, 0, v___x_119_);
lean_ctor_set(v___x_120_, 1, v___x_118_);
lean_ctor_set(v___x_120_, 2, v___x_117_);
lean_ctor_set(v___x_120_, 3, v___x_116_);
lean_ctor_set(v___x_120_, 4, v___x_115_);
lean_ctor_set(v___x_120_, 5, v___f_114_);
return v___x_120_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack(void){
_start:
{
lean_object* v___x_121_; 
v___x_121_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__4, &lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__4_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack___closed__4);
return v___x_121_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_uniformHalf(uint8_t v_x_122_){
_start:
{
lean_object* v___x_123_; 
v___x_123_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half;
return v___x_123_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_uniformHalf___boxed(lean_object* v_x_124_){
_start:
{
uint8_t v_x_4__boxed_125_; lean_object* v_res_126_; 
v_x_4__boxed_125_ = lean_unbox(v_x_124_);
v_res_126_ = lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_uniformHalf(v_x_4__boxed_125_);
return v_res_126_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H001Rats(uint8_t builtin) {
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
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_preQSetoid = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_preQSetoid();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_preQSetoid);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fzero);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fone);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_half);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pzero);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_pone);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_phalf = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_phalf();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_phalf);
lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H001Rats_fracPack);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
