// Lean compiler output
// Module: TraceZeroDuality
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
uint8_t lean_int_dec_lt(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_TraceZeroDuality_iabs___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_TraceZeroDuality_iabs___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_iabs(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_iabs___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_max2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_max2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_min2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_min2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_spread(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_spread___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_pairing(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_pairing___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1;
static lean_once_cell_t lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__2;
static lean_once_cell_t lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__3;
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_TraceZeroDuality_opNorm___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_TraceZeroDuality_opNorm___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_opNorm(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_opNorm___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalShift(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalShift___boxed(lean_object*);
static lean_object* _init_lp_FiniteQuantum_TraceZeroDuality_iabs___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(0u);
v___x_2_ = lean_nat_to_int(v___x_1_);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_iabs(lean_object* v_x_3_){
_start:
{
lean_object* v___x_4_; uint8_t v___x_5_; 
v___x_4_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_iabs___closed__0, &lp_FiniteQuantum_TraceZeroDuality_iabs___closed__0_once, _init_lp_FiniteQuantum_TraceZeroDuality_iabs___closed__0);
v___x_5_ = lean_int_dec_lt(v_x_3_, v___x_4_);
if (v___x_5_ == 0)
{
lean_inc(v_x_3_);
return v_x_3_;
}
else
{
lean_object* v___x_6_; 
v___x_6_ = lean_int_neg(v_x_3_);
return v___x_6_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_iabs___boxed(lean_object* v_x_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_FiniteQuantum_TraceZeroDuality_iabs(v_x_7_);
lean_dec(v_x_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_max2(lean_object* v_a_9_, lean_object* v_b_10_){
_start:
{
uint8_t v___x_11_; 
v___x_11_ = lean_int_dec_lt(v_a_9_, v_b_10_);
if (v___x_11_ == 0)
{
lean_inc(v_a_9_);
return v_a_9_;
}
else
{
lean_inc(v_b_10_);
return v_b_10_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_max2___boxed(lean_object* v_a_12_, lean_object* v_b_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_FiniteQuantum_TraceZeroDuality_max2(v_a_12_, v_b_13_);
lean_dec(v_b_13_);
lean_dec(v_a_12_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_min2(lean_object* v_a_15_, lean_object* v_b_16_){
_start:
{
uint8_t v___x_17_; 
v___x_17_ = lean_int_dec_lt(v_a_15_, v_b_16_);
if (v___x_17_ == 0)
{
lean_inc(v_b_16_);
return v_b_16_;
}
else
{
lean_inc(v_a_15_);
return v_a_15_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_min2___boxed(lean_object* v_a_18_, lean_object* v_b_19_){
_start:
{
lean_object* v_res_20_; 
v_res_20_ = lp_FiniteQuantum_TraceZeroDuality_min2(v_a_18_, v_b_19_);
lean_dec(v_b_19_);
lean_dec(v_a_18_);
return v_res_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_spread(lean_object* v_L_21_){
_start:
{
lean_object* v_l1_22_; lean_object* v_l2_23_; lean_object* v___x_24_; lean_object* v___x_25_; lean_object* v___x_26_; 
v_l1_22_ = lean_ctor_get(v_L_21_, 0);
v_l2_23_ = lean_ctor_get(v_L_21_, 1);
v___x_24_ = lp_FiniteQuantum_TraceZeroDuality_max2(v_l1_22_, v_l2_23_);
v___x_25_ = lp_FiniteQuantum_TraceZeroDuality_min2(v_l1_22_, v_l2_23_);
v___x_26_ = lean_int_sub(v___x_24_, v___x_25_);
lean_dec(v___x_25_);
lean_dec(v___x_24_);
return v___x_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_spread___boxed(lean_object* v_L_27_){
_start:
{
lean_object* v_res_28_; 
v_res_28_ = lp_FiniteQuantum_TraceZeroDuality_spread(v_L_27_);
lean_dec_ref(v_L_27_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_pairing(lean_object* v_L_29_, lean_object* v_x_30_){
_start:
{
lean_object* v_l1_31_; lean_object* v_l2_32_; lean_object* v_x1_33_; lean_object* v_x2_34_; lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_37_; 
v_l1_31_ = lean_ctor_get(v_L_29_, 0);
v_l2_32_ = lean_ctor_get(v_L_29_, 1);
v_x1_33_ = lean_ctor_get(v_x_30_, 0);
v_x2_34_ = lean_ctor_get(v_x_30_, 1);
v___x_35_ = lean_int_mul(v_l1_31_, v_x1_33_);
v___x_36_ = lean_int_mul(v_l2_32_, v_x2_34_);
v___x_37_ = lean_int_add(v___x_35_, v___x_36_);
lean_dec(v___x_36_);
lean_dec(v___x_35_);
return v___x_37_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_pairing___boxed(lean_object* v_L_38_, lean_object* v_x_39_){
_start:
{
lean_object* v_res_40_; 
v_res_40_ = lp_FiniteQuantum_TraceZeroDuality_pairing(v_L_38_, v_x_39_);
lean_dec_ref(v_x_39_);
lean_dec_ref(v_L_38_);
return v_res_40_;
}
}
static lean_object* _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0(void){
_start:
{
lean_object* v___x_41_; lean_object* v___x_42_; 
v___x_41_ = lean_unsigned_to_nat(1u);
v___x_42_ = lean_nat_to_int(v___x_41_);
return v___x_42_;
}
}
static lean_object* _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1(void){
_start:
{
lean_object* v___x_43_; lean_object* v___x_44_; 
v___x_43_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0);
v___x_44_ = lean_int_neg(v___x_43_);
return v___x_44_;
}
}
static lean_object* _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__2(void){
_start:
{
lean_object* v___x_45_; lean_object* v___x_46_; lean_object* v___x_47_; 
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1);
v___x_46_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0);
v___x_47_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_47_, 0, v___x_46_);
lean_ctor_set(v___x_47_, 1, v___x_45_);
return v___x_47_;
}
}
static lean_object* _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__3(void){
_start:
{
lean_object* v___x_48_; lean_object* v___x_49_; lean_object* v___x_50_; 
v___x_48_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__0);
v___x_49_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__1);
v___x_50_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_50_, 0, v___x_49_);
lean_ctor_set(v___x_50_, 1, v___x_48_);
return v___x_50_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2(lean_object* v_L_51_){
_start:
{
lean_object* v_l1_52_; lean_object* v_l2_53_; uint8_t v___x_54_; 
v_l1_52_ = lean_ctor_get(v_L_51_, 0);
v_l2_53_ = lean_ctor_get(v_L_51_, 1);
v___x_54_ = lean_int_dec_lt(v_l1_52_, v_l2_53_);
if (v___x_54_ == 0)
{
lean_object* v___x_55_; 
v___x_55_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__2, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__2_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__2);
return v___x_55_;
}
else
{
lean_object* v___x_56_; 
v___x_56_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__3, &lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__3_once, _init_lp_FiniteQuantum_TraceZeroDuality_optimalVec2___closed__3);
return v___x_56_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalVec2___boxed(lean_object* v_L_57_){
_start:
{
lean_object* v_res_58_; 
v_res_58_ = lp_FiniteQuantum_TraceZeroDuality_optimalVec2(v_L_57_);
lean_dec_ref(v_L_57_);
return v_res_58_;
}
}
static lean_object* _init_lp_FiniteQuantum_TraceZeroDuality_opNorm___closed__0(void){
_start:
{
lean_object* v___x_59_; lean_object* v___x_60_; 
v___x_59_ = lean_unsigned_to_nat(2u);
v___x_60_ = lean_nat_to_int(v___x_59_);
return v___x_60_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_opNorm(lean_object* v_L_61_, lean_object* v_c_62_){
_start:
{
lean_object* v_l1_63_; lean_object* v_l2_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; 
v_l1_63_ = lean_ctor_get(v_L_61_, 0);
v_l2_64_ = lean_ctor_get(v_L_61_, 1);
v___x_65_ = lean_obj_once(&lp_FiniteQuantum_TraceZeroDuality_opNorm___closed__0, &lp_FiniteQuantum_TraceZeroDuality_opNorm___closed__0_once, _init_lp_FiniteQuantum_TraceZeroDuality_opNorm___closed__0);
v___x_66_ = lean_int_mul(v___x_65_, v_l1_63_);
v___x_67_ = lean_int_sub(v___x_66_, v_c_62_);
lean_dec(v___x_66_);
v___x_68_ = lp_FiniteQuantum_TraceZeroDuality_iabs(v___x_67_);
lean_dec(v___x_67_);
v___x_69_ = lean_int_mul(v___x_65_, v_l2_64_);
v___x_70_ = lean_int_sub(v___x_69_, v_c_62_);
lean_dec(v___x_69_);
v___x_71_ = lp_FiniteQuantum_TraceZeroDuality_iabs(v___x_70_);
lean_dec(v___x_70_);
v___x_72_ = lp_FiniteQuantum_TraceZeroDuality_max2(v___x_68_, v___x_71_);
lean_dec(v___x_71_);
lean_dec(v___x_68_);
return v___x_72_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_opNorm___boxed(lean_object* v_L_73_, lean_object* v_c_74_){
_start:
{
lean_object* v_res_75_; 
v_res_75_ = lp_FiniteQuantum_TraceZeroDuality_opNorm(v_L_73_, v_c_74_);
lean_dec(v_c_74_);
lean_dec_ref(v_L_73_);
return v_res_75_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalShift(lean_object* v_L_76_){
_start:
{
lean_object* v_l1_77_; lean_object* v_l2_78_; lean_object* v___x_79_; 
v_l1_77_ = lean_ctor_get(v_L_76_, 0);
v_l2_78_ = lean_ctor_get(v_L_76_, 1);
v___x_79_ = lean_int_add(v_l1_77_, v_l2_78_);
return v___x_79_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_TraceZeroDuality_optimalShift___boxed(lean_object* v_L_80_){
_start:
{
lean_object* v_res_81_; 
v_res_81_ = lp_FiniteQuantum_TraceZeroDuality_optimalShift(v_L_80_);
lean_dec_ref(v_L_80_);
return v_res_81_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_TraceZeroDuality(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
