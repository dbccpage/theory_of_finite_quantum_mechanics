// Lean compiler output
// Module: H014TensorCompositionBoundary
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
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensor(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__0;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__0(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__1(lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__1___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumJoin(lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensorNonForcing___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*0 + 8, .m_other = 0, .m_tag = 0}, .m_objs = {LEAN_SCALAR_PTR_LITERAL(1, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensorNonForcing___closed__0 = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensorNonForcing___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensorNonForcing = (const lean_object*)&lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensorNonForcing___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H014_NonForcingDischarged(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_NonForcingDischarged___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_tensor(lean_object* v_u_1_, lean_object* v_v_2_, lean_object* v_p_3_){
_start:
{
lean_object* v_fst_4_; lean_object* v_snd_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v_fst_4_ = lean_ctor_get(v_p_3_, 0);
lean_inc(v_fst_4_);
v_snd_5_ = lean_ctor_get(v_p_3_, 1);
lean_inc(v_snd_5_);
lean_dec_ref(v_p_3_);
v___x_6_ = lean_apply_1(v_u_1_, v_fst_4_);
v___x_7_ = lean_apply_1(v_v_2_, v_snd_5_);
v___x_8_ = lean_int_mul(v___x_6_, v___x_7_);
lean_dec(v___x_7_);
lean_dec(v___x_6_);
return v___x_8_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__0(void){
_start:
{
lean_object* v___x_9_; lean_object* v___x_10_; 
v___x_9_ = lean_unsigned_to_nat(0u);
v___x_10_ = lean_nat_to_int(v___x_9_);
return v___x_10_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__1(void){
_start:
{
lean_object* v___x_11_; lean_object* v___x_12_; 
v___x_11_ = lean_unsigned_to_nat(1u);
v___x_12_ = lean_nat_to_int(v___x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell(lean_object* v_p_13_){
_start:
{
lean_object* v_fst_18_; uint8_t v___x_19_; 
v_fst_18_ = lean_ctor_get(v_p_13_, 0);
v___x_19_ = lean_unbox(v_fst_18_);
if (v___x_19_ == 0)
{
lean_object* v_snd_20_; uint8_t v___x_21_; 
v_snd_20_ = lean_ctor_get(v_p_13_, 1);
v___x_21_ = lean_unbox(v_snd_20_);
if (v___x_21_ == 0)
{
goto v___jp_16_;
}
else
{
goto v___jp_14_;
}
}
else
{
lean_object* v_snd_22_; uint8_t v___x_23_; 
v_snd_22_ = lean_ctor_get(v_p_13_, 1);
v___x_23_ = lean_unbox(v_snd_22_);
if (v___x_23_ == 0)
{
goto v___jp_14_;
}
else
{
goto v___jp_16_;
}
}
v___jp_14_:
{
lean_object* v___x_15_; 
v___x_15_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__0);
return v___x_15_;
}
v___jp_16_:
{
lean_object* v___x_17_; 
v___x_17_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__1, &lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__1_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___closed__1);
return v___x_17_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell___boxed(lean_object* v_p_24_){
_start:
{
lean_object* v_res_25_; 
v_res_25_ = lp_FiniteQuantum_FableHilbertWalk20260819_H014_bell(v_p_24_);
lean_dec_ref(v_p_24_);
return v_res_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__0(lean_object* v_w_26_, uint8_t v_a_27_){
_start:
{
lean_object* v___x_28_; lean_object* v___x_29_; lean_object* v___x_30_; 
v___x_28_ = lean_box(v_a_27_);
v___x_29_ = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(v___x_29_, 0, v___x_28_);
v___x_30_ = lean_apply_1(v_w_26_, v___x_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__0___boxed(lean_object* v_w_31_, lean_object* v_a_32_){
_start:
{
uint8_t v_a_boxed_33_; lean_object* v_res_34_; 
v_a_boxed_33_ = lean_unbox(v_a_32_);
v_res_34_ = lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__0(v_w_31_, v_a_boxed_33_);
return v_res_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__1(lean_object* v_w_35_, uint8_t v_b_36_){
_start:
{
lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; 
v___x_37_ = lean_box(v_b_36_);
v___x_38_ = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(v___x_38_, 0, v___x_37_);
v___x_39_ = lean_apply_1(v_w_35_, v___x_38_);
return v___x_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__1___boxed(lean_object* v_w_40_, lean_object* v_b_41_){
_start:
{
uint8_t v_b_boxed_42_; lean_object* v_res_43_; 
v_b_boxed_42_ = lean_unbox(v_b_41_);
v_res_43_ = lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__1(v_w_40_, v_b_boxed_42_);
return v_res_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit(lean_object* v_w_44_){
_start:
{
lean_object* v___f_45_; lean_object* v___f_46_; lean_object* v___x_47_; 
lean_inc_ref(v_w_44_);
v___f_45_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__0___boxed), 2, 1);
lean_closure_set(v___f_45_, 0, v_w_44_);
v___f_46_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumSplit___lam__1___boxed), 2, 1);
lean_closure_set(v___f_46_, 0, v_w_44_);
v___x_47_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_47_, 0, v___f_45_);
lean_ctor_set(v___x_47_, 1, v___f_46_);
return v___x_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_sumJoin(lean_object* v_p_48_, lean_object* v_x_49_){
_start:
{
if (lean_obj_tag(v_x_49_) == 0)
{
lean_object* v_a_50_; lean_object* v_fst_51_; lean_object* v___x_52_; 
v_a_50_ = lean_ctor_get(v_x_49_, 0);
lean_inc(v_a_50_);
lean_dec_ref_known(v_x_49_, 1);
v_fst_51_ = lean_ctor_get(v_p_48_, 0);
lean_inc(v_fst_51_);
lean_dec_ref(v_p_48_);
v___x_52_ = lean_apply_1(v_fst_51_, v_a_50_);
return v___x_52_;
}
else
{
lean_object* v_a_53_; lean_object* v_snd_54_; lean_object* v___x_55_; 
v_a_53_ = lean_ctor_get(v_x_49_, 0);
lean_inc(v_a_53_);
lean_dec_ref_known(v_x_49_, 1);
v_snd_54_ = lean_ctor_get(v_p_48_, 1);
lean_inc(v_snd_54_);
lean_dec_ref(v_p_48_);
v___x_55_ = lean_apply_1(v_snd_54_, v_a_53_);
return v___x_55_;
}
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H014_NonForcingDischarged(lean_object* v_P_60_){
_start:
{
uint8_t v_rival__embeds__components_61_; 
v_rival__embeds__components_61_ = lean_ctor_get_uint8(v_P_60_, 0);
if (v_rival__embeds__components_61_ == 0)
{
return v_rival__embeds__components_61_;
}
else
{
uint8_t v_rival__meets__same__interface_62_; 
v_rival__meets__same__interface_62_ = lean_ctor_get_uint8(v_P_60_, 1);
return v_rival__meets__same__interface_62_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H014_NonForcingDischarged___boxed(lean_object* v_P_63_){
_start:
{
uint8_t v_res_64_; lean_object* v_r_65_; 
v_res_64_ = lp_FiniteQuantum_FableHilbertWalk20260819_H014_NonForcingDischarged(v_P_63_);
lean_dec_ref(v_P_63_);
v_r_65_ = lean_box(v_res_64_);
return v_r_65_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H014TensorCompositionBoundary(uint8_t builtin) {
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
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
