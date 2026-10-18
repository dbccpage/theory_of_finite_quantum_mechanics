// Lean compiler output
// Module: Entanglement
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
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_schmidt__minor(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_schmidt__minor___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__0;
static lean_once_cell_t lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__1;
static lean_once_cell_t lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_bell__phi__plus;
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_reduced__marginal__a(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_reduced__marginal__a___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_local__flip__b(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_local__phase__b(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_schmidt__minor(lean_object* v_00_u03c8_1_){
_start:
{
lean_object* v_c00_2_; lean_object* v_c01_3_; lean_object* v_c10_4_; lean_object* v_c11_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v_c00_2_ = lean_ctor_get(v_00_u03c8_1_, 0);
v_c01_3_ = lean_ctor_get(v_00_u03c8_1_, 1);
v_c10_4_ = lean_ctor_get(v_00_u03c8_1_, 2);
v_c11_5_ = lean_ctor_get(v_00_u03c8_1_, 3);
v___x_6_ = lean_int_mul(v_c00_2_, v_c11_5_);
v___x_7_ = lean_int_mul(v_c01_3_, v_c10_4_);
v___x_8_ = lean_int_sub(v___x_6_, v___x_7_);
lean_dec(v___x_7_);
lean_dec(v___x_6_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_schmidt__minor___boxed(lean_object* v_00_u03c8_9_){
_start:
{
lean_object* v_res_10_; 
v_res_10_ = lp_FiniteQuantum_Entanglement_schmidt__minor(v_00_u03c8_9_);
lean_dec_ref(v_00_u03c8_9_);
return v_res_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__0(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_11_ = lean_unsigned_to_nat(1u);
v___x_12_ = lean_nat_to_int(v___x_11_);
return v___x_12_;
}
}
static lean_object* _init_lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__1(void){
_start:
{
lean_object* v___x_13_; lean_object* v___x_14_; 
v___x_13_ = lean_unsigned_to_nat(0u);
v___x_14_ = lean_nat_to_int(v___x_13_);
return v___x_14_;
}
}
static lean_object* _init_lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__2(void){
_start:
{
lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; 
v___x_15_ = lean_obj_once(&lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__1, &lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__1_once, _init_lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__1);
v___x_16_ = lean_obj_once(&lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__0, &lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__0_once, _init_lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__0);
v___x_17_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_17_, 0, v___x_16_);
lean_ctor_set(v___x_17_, 1, v___x_15_);
lean_ctor_set(v___x_17_, 2, v___x_15_);
lean_ctor_set(v___x_17_, 3, v___x_16_);
return v___x_17_;
}
}
static lean_object* _init_lp_FiniteQuantum_Entanglement_bell__phi__plus(void){
_start:
{
lean_object* v___x_18_; 
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__2, &lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__2_once, _init_lp_FiniteQuantum_Entanglement_bell__phi__plus___closed__2);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_reduced__marginal__a(lean_object* v_00_u03c8_19_){
_start:
{
lean_object* v_c00_20_; lean_object* v_c01_21_; lean_object* v_c10_22_; lean_object* v_c11_23_; lean_object* v___x_24_; lean_object* v___x_25_; lean_object* v___x_26_; lean_object* v___x_27_; lean_object* v___x_28_; lean_object* v___x_29_; lean_object* v___x_30_; 
v_c00_20_ = lean_ctor_get(v_00_u03c8_19_, 0);
v_c01_21_ = lean_ctor_get(v_00_u03c8_19_, 1);
v_c10_22_ = lean_ctor_get(v_00_u03c8_19_, 2);
v_c11_23_ = lean_ctor_get(v_00_u03c8_19_, 3);
v___x_24_ = lean_int_mul(v_c00_20_, v_c00_20_);
v___x_25_ = lean_int_mul(v_c01_21_, v_c01_21_);
v___x_26_ = lean_int_add(v___x_24_, v___x_25_);
lean_dec(v___x_25_);
lean_dec(v___x_24_);
v___x_27_ = lean_int_mul(v_c10_22_, v_c10_22_);
v___x_28_ = lean_int_mul(v_c11_23_, v_c11_23_);
v___x_29_ = lean_int_add(v___x_27_, v___x_28_);
lean_dec(v___x_28_);
lean_dec(v___x_27_);
v___x_30_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_30_, 0, v___x_26_);
lean_ctor_set(v___x_30_, 1, v___x_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_reduced__marginal__a___boxed(lean_object* v_00_u03c8_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_FiniteQuantum_Entanglement_reduced__marginal__a(v_00_u03c8_31_);
lean_dec_ref(v_00_u03c8_31_);
return v_res_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_local__flip__b(lean_object* v_00_u03c8_33_){
_start:
{
lean_object* v_c00_34_; lean_object* v_c01_35_; lean_object* v_c10_36_; lean_object* v_c11_37_; lean_object* v___x_39_; uint8_t v_isShared_40_; uint8_t v_isSharedCheck_44_; 
v_c00_34_ = lean_ctor_get(v_00_u03c8_33_, 0);
v_c01_35_ = lean_ctor_get(v_00_u03c8_33_, 1);
v_c10_36_ = lean_ctor_get(v_00_u03c8_33_, 2);
v_c11_37_ = lean_ctor_get(v_00_u03c8_33_, 3);
v_isSharedCheck_44_ = !lean_is_exclusive(v_00_u03c8_33_);
if (v_isSharedCheck_44_ == 0)
{
v___x_39_ = v_00_u03c8_33_;
v_isShared_40_ = v_isSharedCheck_44_;
goto v_resetjp_38_;
}
else
{
lean_inc(v_c11_37_);
lean_inc(v_c10_36_);
lean_inc(v_c01_35_);
lean_inc(v_c00_34_);
lean_dec(v_00_u03c8_33_);
v___x_39_ = lean_box(0);
v_isShared_40_ = v_isSharedCheck_44_;
goto v_resetjp_38_;
}
v_resetjp_38_:
{
lean_object* v___x_42_; 
if (v_isShared_40_ == 0)
{
lean_ctor_set(v___x_39_, 3, v_c10_36_);
lean_ctor_set(v___x_39_, 2, v_c11_37_);
lean_ctor_set(v___x_39_, 1, v_c00_34_);
lean_ctor_set(v___x_39_, 0, v_c01_35_);
v___x_42_ = v___x_39_;
goto v_reusejp_41_;
}
else
{
lean_object* v_reuseFailAlloc_43_; 
v_reuseFailAlloc_43_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_43_, 0, v_c01_35_);
lean_ctor_set(v_reuseFailAlloc_43_, 1, v_c00_34_);
lean_ctor_set(v_reuseFailAlloc_43_, 2, v_c11_37_);
lean_ctor_set(v_reuseFailAlloc_43_, 3, v_c10_36_);
v___x_42_ = v_reuseFailAlloc_43_;
goto v_reusejp_41_;
}
v_reusejp_41_:
{
return v___x_42_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Entanglement_local__phase__b(lean_object* v_00_u03c8_45_){
_start:
{
lean_object* v_c00_46_; lean_object* v_c01_47_; lean_object* v_c10_48_; lean_object* v_c11_49_; lean_object* v___x_51_; uint8_t v_isShared_52_; uint8_t v_isSharedCheck_58_; 
v_c00_46_ = lean_ctor_get(v_00_u03c8_45_, 0);
v_c01_47_ = lean_ctor_get(v_00_u03c8_45_, 1);
v_c10_48_ = lean_ctor_get(v_00_u03c8_45_, 2);
v_c11_49_ = lean_ctor_get(v_00_u03c8_45_, 3);
v_isSharedCheck_58_ = !lean_is_exclusive(v_00_u03c8_45_);
if (v_isSharedCheck_58_ == 0)
{
v___x_51_ = v_00_u03c8_45_;
v_isShared_52_ = v_isSharedCheck_58_;
goto v_resetjp_50_;
}
else
{
lean_inc(v_c11_49_);
lean_inc(v_c10_48_);
lean_inc(v_c01_47_);
lean_inc(v_c00_46_);
lean_dec(v_00_u03c8_45_);
v___x_51_ = lean_box(0);
v_isShared_52_ = v_isSharedCheck_58_;
goto v_resetjp_50_;
}
v_resetjp_50_:
{
lean_object* v___x_53_; lean_object* v___x_54_; lean_object* v___x_56_; 
v___x_53_ = lean_int_neg(v_c01_47_);
lean_dec(v_c01_47_);
v___x_54_ = lean_int_neg(v_c11_49_);
lean_dec(v_c11_49_);
if (v_isShared_52_ == 0)
{
lean_ctor_set(v___x_51_, 3, v___x_54_);
lean_ctor_set(v___x_51_, 1, v___x_53_);
v___x_56_ = v___x_51_;
goto v_reusejp_55_;
}
else
{
lean_object* v_reuseFailAlloc_57_; 
v_reuseFailAlloc_57_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v_reuseFailAlloc_57_, 0, v_c00_46_);
lean_ctor_set(v_reuseFailAlloc_57_, 1, v___x_53_);
lean_ctor_set(v_reuseFailAlloc_57_, 2, v_c10_48_);
lean_ctor_set(v_reuseFailAlloc_57_, 3, v___x_54_);
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
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_Entanglement(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_Entanglement_bell__phi__plus = _init_lp_FiniteQuantum_Entanglement_bell__phi__plus();
lean_mark_persistent(lp_FiniteQuantum_Entanglement_bell__phi__plus);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
