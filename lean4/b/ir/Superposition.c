// Lean compiler output
// Module: Superposition
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
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_base__probabilities(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_Superposition_interference__capacity__sq___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Superposition_interference__capacity__sq___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__capacity__sq(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__capacity__sq___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_beam__splitter__prob0(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_beam__splitter__prob0___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_classical__prob__sum(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_classical__prob__sum___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_Superposition_interference__cross__term___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_Superposition_interference__cross__term___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__cross__term(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__cross__term___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_P(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_P___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i3(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i3___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_base__probabilities(lean_object* v_00_u03c8_1_){
_start:
{
lean_object* v_c0_2_; lean_object* v_c1_3_; lean_object* v___x_5_; uint8_t v_isShared_6_; uint8_t v_isSharedCheck_12_; 
v_c0_2_ = lean_ctor_get(v_00_u03c8_1_, 0);
v_c1_3_ = lean_ctor_get(v_00_u03c8_1_, 1);
v_isSharedCheck_12_ = !lean_is_exclusive(v_00_u03c8_1_);
if (v_isSharedCheck_12_ == 0)
{
v___x_5_ = v_00_u03c8_1_;
v_isShared_6_ = v_isSharedCheck_12_;
goto v_resetjp_4_;
}
else
{
lean_inc(v_c1_3_);
lean_inc(v_c0_2_);
lean_dec(v_00_u03c8_1_);
v___x_5_ = lean_box(0);
v_isShared_6_ = v_isSharedCheck_12_;
goto v_resetjp_4_;
}
v_resetjp_4_:
{
lean_object* v___x_7_; lean_object* v___x_8_; lean_object* v___x_10_; 
v___x_7_ = lean_int_mul(v_c0_2_, v_c0_2_);
lean_dec(v_c0_2_);
v___x_8_ = lean_int_mul(v_c1_3_, v_c1_3_);
lean_dec(v_c1_3_);
if (v_isShared_6_ == 0)
{
lean_ctor_set(v___x_5_, 1, v___x_8_);
lean_ctor_set(v___x_5_, 0, v___x_7_);
v___x_10_ = v___x_5_;
goto v_reusejp_9_;
}
else
{
lean_object* v_reuseFailAlloc_11_; 
v_reuseFailAlloc_11_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_11_, 0, v___x_7_);
lean_ctor_set(v_reuseFailAlloc_11_, 1, v___x_8_);
v___x_10_ = v_reuseFailAlloc_11_;
goto v_reusejp_9_;
}
v_reusejp_9_:
{
return v___x_10_;
}
}
}
}
static lean_object* _init_lp_FiniteQuantum_Superposition_interference__capacity__sq___closed__0(void){
_start:
{
lean_object* v___x_13_; lean_object* v___x_14_; 
v___x_13_ = lean_unsigned_to_nat(4u);
v___x_14_ = lean_nat_to_int(v___x_13_);
return v___x_14_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__capacity__sq(lean_object* v_00_u03c8_15_){
_start:
{
lean_object* v_c0_16_; lean_object* v_c1_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; lean_object* v___x_22_; 
v_c0_16_ = lean_ctor_get(v_00_u03c8_15_, 0);
v_c1_17_ = lean_ctor_get(v_00_u03c8_15_, 1);
v___x_18_ = lean_obj_once(&lp_FiniteQuantum_Superposition_interference__capacity__sq___closed__0, &lp_FiniteQuantum_Superposition_interference__capacity__sq___closed__0_once, _init_lp_FiniteQuantum_Superposition_interference__capacity__sq___closed__0);
v___x_19_ = lean_int_mul(v_c0_16_, v_c0_16_);
v___x_20_ = lean_int_mul(v___x_18_, v___x_19_);
lean_dec(v___x_19_);
v___x_21_ = lean_int_mul(v_c1_17_, v_c1_17_);
v___x_22_ = lean_int_mul(v___x_20_, v___x_21_);
lean_dec(v___x_21_);
lean_dec(v___x_20_);
return v___x_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__capacity__sq___boxed(lean_object* v_00_u03c8_23_){
_start:
{
lean_object* v_res_24_; 
v_res_24_ = lp_FiniteQuantum_Superposition_interference__capacity__sq(v_00_u03c8_23_);
lean_dec_ref(v_00_u03c8_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_beam__splitter__prob0(lean_object* v_00_u03c8_25_){
_start:
{
lean_object* v_c0_26_; lean_object* v_c1_27_; lean_object* v___x_28_; lean_object* v___x_29_; 
v_c0_26_ = lean_ctor_get(v_00_u03c8_25_, 0);
v_c1_27_ = lean_ctor_get(v_00_u03c8_25_, 1);
v___x_28_ = lean_int_add(v_c0_26_, v_c1_27_);
v___x_29_ = lean_int_mul(v___x_28_, v___x_28_);
lean_dec(v___x_28_);
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_beam__splitter__prob0___boxed(lean_object* v_00_u03c8_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_FiniteQuantum_Superposition_beam__splitter__prob0(v_00_u03c8_30_);
lean_dec_ref(v_00_u03c8_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_classical__prob__sum(lean_object* v_00_u03c8_32_){
_start:
{
lean_object* v_c0_33_; lean_object* v_c1_34_; lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_37_; 
v_c0_33_ = lean_ctor_get(v_00_u03c8_32_, 0);
v_c1_34_ = lean_ctor_get(v_00_u03c8_32_, 1);
v___x_35_ = lean_int_mul(v_c0_33_, v_c0_33_);
v___x_36_ = lean_int_mul(v_c1_34_, v_c1_34_);
v___x_37_ = lean_int_add(v___x_35_, v___x_36_);
lean_dec(v___x_36_);
lean_dec(v___x_35_);
return v___x_37_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_classical__prob__sum___boxed(lean_object* v_00_u03c8_38_){
_start:
{
lean_object* v_res_39_; 
v_res_39_ = lp_FiniteQuantum_Superposition_classical__prob__sum(v_00_u03c8_38_);
lean_dec_ref(v_00_u03c8_38_);
return v_res_39_;
}
}
static lean_object* _init_lp_FiniteQuantum_Superposition_interference__cross__term___closed__0(void){
_start:
{
lean_object* v___x_40_; lean_object* v___x_41_; 
v___x_40_ = lean_unsigned_to_nat(2u);
v___x_41_ = lean_nat_to_int(v___x_40_);
return v___x_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__cross__term(lean_object* v_00_u03c8_42_){
_start:
{
lean_object* v_c0_43_; lean_object* v_c1_44_; lean_object* v___x_45_; lean_object* v___x_46_; lean_object* v___x_47_; 
v_c0_43_ = lean_ctor_get(v_00_u03c8_42_, 0);
v_c1_44_ = lean_ctor_get(v_00_u03c8_42_, 1);
v___x_45_ = lean_obj_once(&lp_FiniteQuantum_Superposition_interference__cross__term___closed__0, &lp_FiniteQuantum_Superposition_interference__cross__term___closed__0_once, _init_lp_FiniteQuantum_Superposition_interference__cross__term___closed__0);
v___x_46_ = lean_int_mul(v___x_45_, v_c0_43_);
v___x_47_ = lean_int_mul(v___x_46_, v_c1_44_);
lean_dec(v___x_46_);
return v___x_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_interference__cross__term___boxed(lean_object* v_00_u03c8_48_){
_start:
{
lean_object* v_res_49_; 
v_res_49_ = lp_FiniteQuantum_Superposition_interference__cross__term(v_00_u03c8_48_);
lean_dec_ref(v_00_u03c8_48_);
return v_res_49_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_P(lean_object* v_x_50_){
_start:
{
lean_object* v___x_51_; 
v___x_51_ = lean_int_mul(v_x_50_, v_x_50_);
return v___x_51_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_P___boxed(lean_object* v_x_52_){
_start:
{
lean_object* v_res_53_; 
v_res_53_ = lp_FiniteQuantum_Superposition_P(v_x_52_);
lean_dec(v_x_52_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i3(lean_object* v_a_54_, lean_object* v_b_55_, lean_object* v_c_56_){
_start:
{
lean_object* v___x_57_; lean_object* v___x_58_; lean_object* v___x_59_; lean_object* v___x_60_; lean_object* v___x_61_; lean_object* v___x_62_; lean_object* v___x_63_; lean_object* v___x_64_; lean_object* v___x_65_; lean_object* v___x_66_; lean_object* v___x_67_; lean_object* v___x_68_; lean_object* v___x_69_; lean_object* v___x_70_; lean_object* v___x_71_; lean_object* v___x_72_; lean_object* v___x_73_; 
v___x_57_ = lean_int_add(v_a_54_, v_b_55_);
v___x_58_ = lean_int_add(v___x_57_, v_c_56_);
v___x_59_ = lean_int_mul(v___x_58_, v___x_58_);
lean_dec(v___x_58_);
v___x_60_ = lean_int_mul(v___x_57_, v___x_57_);
lean_dec(v___x_57_);
v___x_61_ = lean_int_add(v_b_55_, v_c_56_);
v___x_62_ = lean_int_mul(v___x_61_, v___x_61_);
lean_dec(v___x_61_);
v___x_63_ = lean_int_add(v___x_60_, v___x_62_);
lean_dec(v___x_62_);
lean_dec(v___x_60_);
v___x_64_ = lean_int_add(v_c_56_, v_a_54_);
v___x_65_ = lean_int_mul(v___x_64_, v___x_64_);
lean_dec(v___x_64_);
v___x_66_ = lean_int_add(v___x_63_, v___x_65_);
lean_dec(v___x_65_);
lean_dec(v___x_63_);
v___x_67_ = lean_int_sub(v___x_59_, v___x_66_);
lean_dec(v___x_66_);
lean_dec(v___x_59_);
v___x_68_ = lean_int_mul(v_a_54_, v_a_54_);
v___x_69_ = lean_int_mul(v_b_55_, v_b_55_);
v___x_70_ = lean_int_add(v___x_68_, v___x_69_);
lean_dec(v___x_69_);
lean_dec(v___x_68_);
v___x_71_ = lean_int_mul(v_c_56_, v_c_56_);
v___x_72_ = lean_int_add(v___x_70_, v___x_71_);
lean_dec(v___x_71_);
lean_dec(v___x_70_);
v___x_73_ = lean_int_add(v___x_67_, v___x_72_);
lean_dec(v___x_72_);
lean_dec(v___x_67_);
return v___x_73_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i3___boxed(lean_object* v_a_74_, lean_object* v_b_75_, lean_object* v_c_76_){
_start:
{
lean_object* v_res_77_; 
v_res_77_ = lp_FiniteQuantum_Superposition_sorkin__i3(v_a_74_, v_b_75_, v_c_76_);
lean_dec(v_c_76_);
lean_dec(v_b_75_);
lean_dec(v_a_74_);
return v_res_77_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i2(lean_object* v_a_78_, lean_object* v_b_79_){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; lean_object* v___x_82_; lean_object* v___x_83_; lean_object* v___x_84_; lean_object* v___x_85_; 
v___x_80_ = lean_int_add(v_a_78_, v_b_79_);
v___x_81_ = lean_int_mul(v___x_80_, v___x_80_);
lean_dec(v___x_80_);
v___x_82_ = lean_int_mul(v_a_78_, v_a_78_);
v___x_83_ = lean_int_mul(v_b_79_, v_b_79_);
v___x_84_ = lean_int_add(v___x_82_, v___x_83_);
lean_dec(v___x_83_);
lean_dec(v___x_82_);
v___x_85_ = lean_int_sub(v___x_81_, v___x_84_);
lean_dec(v___x_84_);
lean_dec(v___x_81_);
return v___x_85_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_Superposition_sorkin__i2___boxed(lean_object* v_a_86_, lean_object* v_b_87_){
_start:
{
lean_object* v_res_88_; 
v_res_88_ = lp_FiniteQuantum_Superposition_sorkin__i2(v_a_86_, v_b_87_);
lean_dec(v_b_87_);
lean_dec(v_a_86_);
return v_res_88_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_Superposition(uint8_t builtin) {
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
