// Lean compiler output
// Module: DualWitness
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
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_nat_abs(lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_trace__norm(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_trace__norm___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_dual__pairing(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_dual__pairing___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_SignVal_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_instDecidableEqSignVal(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_instDecidableEqSignVal___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 24, .m_capacity = 24, .m_length = 23, .m_data = "DualWitness.SignVal.Pos"};
static const lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 24, .m_capacity = 24, .m_length = 23, .m_data = "DualWitness.SignVal.Neg"};
static const lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__3_value;
static lean_once_cell_t lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4;
static lean_once_cell_t lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5;
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_DualWitness_instReprSignVal___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_DualWitness_instReprSignVal_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal___closed__0 = (const lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal = (const lean_object*)&lp_FiniteQuantum_DualWitness_instReprSignVal___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_mulSign(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_mulSign___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_row1__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_row1__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_row2__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_row2__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_row3__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_row3__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_col1__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_col1__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_col2__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_col2__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_col3__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_col3__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_total__row__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_total__row__prod___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_total__col__prod(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_total__col__prod___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_trace__norm(lean_object* v_d_1_){
_start:
{
lean_object* v_diff0_2_; lean_object* v_diff1_3_; lean_object* v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; 
v_diff0_2_ = lean_ctor_get(v_d_1_, 0);
v_diff1_3_ = lean_ctor_get(v_d_1_, 1);
v___x_4_ = lean_nat_abs(v_diff0_2_);
v___x_5_ = lean_nat_abs(v_diff1_3_);
v___x_6_ = lean_nat_add(v___x_4_, v___x_5_);
lean_dec(v___x_5_);
lean_dec(v___x_4_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_trace__norm___boxed(lean_object* v_d_7_){
_start:
{
lean_object* v_res_8_; 
v_res_8_ = lp_FiniteQuantum_DualWitness_trace__norm(v_d_7_);
lean_dec_ref(v_d_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_dual__pairing(lean_object* v_w_9_, lean_object* v_d_10_){
_start:
{
lean_object* v_w0_11_; lean_object* v_w1_12_; lean_object* v_diff0_13_; lean_object* v_diff1_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; 
v_w0_11_ = lean_ctor_get(v_w_9_, 0);
v_w1_12_ = lean_ctor_get(v_w_9_, 1);
v_diff0_13_ = lean_ctor_get(v_d_10_, 0);
v_diff1_14_ = lean_ctor_get(v_d_10_, 1);
v___x_15_ = lean_int_mul(v_w0_11_, v_diff0_13_);
v___x_16_ = lean_int_mul(v_w1_12_, v_diff1_14_);
v___x_17_ = lean_int_add(v___x_15_, v___x_16_);
lean_dec(v___x_16_);
lean_dec(v___x_15_);
return v___x_17_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_dual__pairing___boxed(lean_object* v_w_18_, lean_object* v_d_19_){
_start:
{
lean_object* v_res_20_; 
v_res_20_ = lp_FiniteQuantum_DualWitness_dual__pairing(v_w_18_, v_d_19_);
lean_dec_ref(v_d_19_);
lean_dec_ref(v_w_18_);
return v_res_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorIdx(uint8_t v_x_21_){
_start:
{
if (v_x_21_ == 0)
{
lean_object* v___x_22_; 
v___x_22_ = lean_unsigned_to_nat(0u);
return v___x_22_;
}
else
{
lean_object* v___x_23_; 
v___x_23_ = lean_unsigned_to_nat(1u);
return v___x_23_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorIdx___boxed(lean_object* v_x_24_){
_start:
{
uint8_t v_x_boxed_25_; lean_object* v_res_26_; 
v_x_boxed_25_ = lean_unbox(v_x_24_);
v_res_26_ = lp_FiniteQuantum_DualWitness_SignVal_ctorIdx(v_x_boxed_25_);
return v_res_26_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_toCtorIdx(uint8_t v_x_27_){
_start:
{
lean_object* v___x_28_; 
v___x_28_ = lp_FiniteQuantum_DualWitness_SignVal_ctorIdx(v_x_27_);
return v___x_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_toCtorIdx___boxed(lean_object* v_x_29_){
_start:
{
uint8_t v_x_4__boxed_30_; lean_object* v_res_31_; 
v_x_4__boxed_30_ = lean_unbox(v_x_29_);
v_res_31_ = lp_FiniteQuantum_DualWitness_SignVal_toCtorIdx(v_x_4__boxed_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim___redArg(lean_object* v_k_32_){
_start:
{
lean_inc(v_k_32_);
return v_k_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim___redArg___boxed(lean_object* v_k_33_){
_start:
{
lean_object* v_res_34_; 
v_res_34_ = lp_FiniteQuantum_DualWitness_SignVal_ctorElim___redArg(v_k_33_);
lean_dec(v_k_33_);
return v_res_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim(lean_object* v_motive_35_, lean_object* v_ctorIdx_36_, uint8_t v_t_37_, lean_object* v_h_38_, lean_object* v_k_39_){
_start:
{
lean_inc(v_k_39_);
return v_k_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ctorElim___boxed(lean_object* v_motive_40_, lean_object* v_ctorIdx_41_, lean_object* v_t_42_, lean_object* v_h_43_, lean_object* v_k_44_){
_start:
{
uint8_t v_t_boxed_45_; lean_object* v_res_46_; 
v_t_boxed_45_ = lean_unbox(v_t_42_);
v_res_46_ = lp_FiniteQuantum_DualWitness_SignVal_ctorElim(v_motive_40_, v_ctorIdx_41_, v_t_boxed_45_, v_h_43_, v_k_44_);
lean_dec(v_k_44_);
lean_dec(v_ctorIdx_41_);
return v_res_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___redArg(lean_object* v_Pos_47_){
_start:
{
lean_inc(v_Pos_47_);
return v_Pos_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___redArg___boxed(lean_object* v_Pos_48_){
_start:
{
lean_object* v_res_49_; 
v_res_49_ = lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___redArg(v_Pos_48_);
lean_dec(v_Pos_48_);
return v_res_49_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim(lean_object* v_motive_50_, uint8_t v_t_51_, lean_object* v_h_52_, lean_object* v_Pos_53_){
_start:
{
lean_inc(v_Pos_53_);
return v_Pos_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Pos_elim___boxed(lean_object* v_motive_54_, lean_object* v_t_55_, lean_object* v_h_56_, lean_object* v_Pos_57_){
_start:
{
uint8_t v_t_boxed_58_; lean_object* v_res_59_; 
v_t_boxed_58_ = lean_unbox(v_t_55_);
v_res_59_ = lp_FiniteQuantum_DualWitness_SignVal_Pos_elim(v_motive_54_, v_t_boxed_58_, v_h_56_, v_Pos_57_);
lean_dec(v_Pos_57_);
return v_res_59_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___redArg(lean_object* v_Neg_60_){
_start:
{
lean_inc(v_Neg_60_);
return v_Neg_60_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___redArg___boxed(lean_object* v_Neg_61_){
_start:
{
lean_object* v_res_62_; 
v_res_62_ = lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___redArg(v_Neg_61_);
lean_dec(v_Neg_61_);
return v_res_62_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim(lean_object* v_motive_63_, uint8_t v_t_64_, lean_object* v_h_65_, lean_object* v_Neg_66_){
_start:
{
lean_inc(v_Neg_66_);
return v_Neg_66_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_Neg_elim___boxed(lean_object* v_motive_67_, lean_object* v_t_68_, lean_object* v_h_69_, lean_object* v_Neg_70_){
_start:
{
uint8_t v_t_boxed_71_; lean_object* v_res_72_; 
v_t_boxed_71_ = lean_unbox(v_t_68_);
v_res_72_ = lp_FiniteQuantum_DualWitness_SignVal_Neg_elim(v_motive_67_, v_t_boxed_71_, v_h_69_, v_Neg_70_);
lean_dec(v_Neg_70_);
return v_res_72_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_SignVal_ofNat(lean_object* v_n_73_){
_start:
{
lean_object* v___x_74_; uint8_t v___x_75_; 
v___x_74_ = lean_unsigned_to_nat(0u);
v___x_75_ = lean_nat_dec_le(v_n_73_, v___x_74_);
if (v___x_75_ == 0)
{
uint8_t v___x_76_; 
v___x_76_ = 1;
return v___x_76_;
}
else
{
uint8_t v___x_77_; 
v___x_77_ = 0;
return v___x_77_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_SignVal_ofNat___boxed(lean_object* v_n_78_){
_start:
{
uint8_t v_res_79_; lean_object* v_r_80_; 
v_res_79_ = lp_FiniteQuantum_DualWitness_SignVal_ofNat(v_n_78_);
lean_dec(v_n_78_);
v_r_80_ = lean_box(v_res_79_);
return v_r_80_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_instDecidableEqSignVal(uint8_t v_x_81_, uint8_t v_y_82_){
_start:
{
lean_object* v___x_83_; lean_object* v___x_84_; uint8_t v___x_85_; 
v___x_83_ = lp_FiniteQuantum_DualWitness_SignVal_ctorIdx(v_x_81_);
v___x_84_ = lp_FiniteQuantum_DualWitness_SignVal_ctorIdx(v_y_82_);
v___x_85_ = lean_nat_dec_eq(v___x_83_, v___x_84_);
lean_dec(v___x_84_);
lean_dec(v___x_83_);
return v___x_85_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_instDecidableEqSignVal___boxed(lean_object* v_x_86_, lean_object* v_y_87_){
_start:
{
uint8_t v_x_13__boxed_88_; uint8_t v_y_14__boxed_89_; uint8_t v_res_90_; lean_object* v_r_91_; 
v_x_13__boxed_88_ = lean_unbox(v_x_86_);
v_y_14__boxed_89_ = lean_unbox(v_y_87_);
v_res_90_ = lp_FiniteQuantum_DualWitness_instDecidableEqSignVal(v_x_13__boxed_88_, v_y_14__boxed_89_);
v_r_91_ = lean_box(v_res_90_);
return v_r_91_;
}
}
static lean_object* _init_lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4(void){
_start:
{
lean_object* v___x_98_; lean_object* v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(2u);
v___x_99_ = lean_nat_to_int(v___x_98_);
return v___x_99_;
}
}
static lean_object* _init_lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5(void){
_start:
{
lean_object* v___x_100_; lean_object* v___x_101_; 
v___x_100_ = lean_unsigned_to_nat(1u);
v___x_101_ = lean_nat_to_int(v___x_100_);
return v___x_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr(uint8_t v_x_102_, lean_object* v_prec_103_){
_start:
{
lean_object* v___y_105_; lean_object* v___y_112_; 
if (v_x_102_ == 0)
{
lean_object* v___x_118_; uint8_t v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(1024u);
v___x_119_ = lean_nat_dec_le(v___x_118_, v_prec_103_);
if (v___x_119_ == 0)
{
lean_object* v___x_120_; 
v___x_120_ = lean_obj_once(&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4, &lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4_once, _init_lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4);
v___y_105_ = v___x_120_;
goto v___jp_104_;
}
else
{
lean_object* v___x_121_; 
v___x_121_ = lean_obj_once(&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5, &lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5_once, _init_lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5);
v___y_105_ = v___x_121_;
goto v___jp_104_;
}
}
else
{
lean_object* v___x_122_; uint8_t v___x_123_; 
v___x_122_ = lean_unsigned_to_nat(1024u);
v___x_123_ = lean_nat_dec_le(v___x_122_, v_prec_103_);
if (v___x_123_ == 0)
{
lean_object* v___x_124_; 
v___x_124_ = lean_obj_once(&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4, &lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4_once, _init_lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__4);
v___y_112_ = v___x_124_;
goto v___jp_111_;
}
else
{
lean_object* v___x_125_; 
v___x_125_ = lean_obj_once(&lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5, &lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5_once, _init_lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__5);
v___y_112_ = v___x_125_;
goto v___jp_111_;
}
}
v___jp_104_:
{
lean_object* v___x_106_; lean_object* v___x_107_; uint8_t v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; 
v___x_106_ = ((lean_object*)(lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__1));
lean_inc(v___y_105_);
v___x_107_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_107_, 0, v___y_105_);
lean_ctor_set(v___x_107_, 1, v___x_106_);
v___x_108_ = 0;
v___x_109_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_109_, 0, v___x_107_);
lean_ctor_set_uint8(v___x_109_, sizeof(void*)*1, v___x_108_);
v___x_110_ = l_Repr_addAppParen(v___x_109_, v_prec_103_);
return v___x_110_;
}
v___jp_111_:
{
lean_object* v___x_113_; lean_object* v___x_114_; uint8_t v___x_115_; lean_object* v___x_116_; lean_object* v___x_117_; 
v___x_113_ = ((lean_object*)(lp_FiniteQuantum_DualWitness_instReprSignVal_repr___closed__3));
lean_inc(v___y_112_);
v___x_114_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_114_, 0, v___y_112_);
lean_ctor_set(v___x_114_, 1, v___x_113_);
v___x_115_ = 0;
v___x_116_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_116_, 0, v___x_114_);
lean_ctor_set_uint8(v___x_116_, sizeof(void*)*1, v___x_115_);
v___x_117_ = l_Repr_addAppParen(v___x_116_, v_prec_103_);
return v___x_117_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_instReprSignVal_repr___boxed(lean_object* v_x_126_, lean_object* v_prec_127_){
_start:
{
uint8_t v_x_121__boxed_128_; lean_object* v_res_129_; 
v_x_121__boxed_128_ = lean_unbox(v_x_126_);
v_res_129_ = lp_FiniteQuantum_DualWitness_instReprSignVal_repr(v_x_121__boxed_128_, v_prec_127_);
lean_dec(v_prec_127_);
return v_res_129_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_mulSign(uint8_t v_x_132_, uint8_t v_x_133_){
_start:
{
if (v_x_132_ == 0)
{
return v_x_133_;
}
else
{
if (v_x_133_ == 0)
{
return v_x_132_;
}
else
{
uint8_t v___x_134_; 
v___x_134_ = 0;
return v___x_134_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_mulSign___boxed(lean_object* v_x_135_, lean_object* v_x_136_){
_start:
{
uint8_t v_x_23__boxed_137_; uint8_t v_x_24__boxed_138_; uint8_t v_res_139_; lean_object* v_r_140_; 
v_x_23__boxed_137_ = lean_unbox(v_x_135_);
v_x_24__boxed_138_ = lean_unbox(v_x_136_);
v_res_139_ = lp_FiniteQuantum_DualWitness_mulSign(v_x_23__boxed_137_, v_x_24__boxed_138_);
v_r_140_ = lean_box(v_res_139_);
return v_r_140_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_row1__prod(lean_object* v_s_141_){
_start:
{
uint8_t v_m11_142_; uint8_t v_m12_143_; uint8_t v_m13_144_; uint8_t v___x_145_; uint8_t v___x_146_; 
v_m11_142_ = lean_ctor_get_uint8(v_s_141_, 0);
v_m12_143_ = lean_ctor_get_uint8(v_s_141_, 1);
v_m13_144_ = lean_ctor_get_uint8(v_s_141_, 2);
v___x_145_ = lp_FiniteQuantum_DualWitness_mulSign(v_m11_142_, v_m12_143_);
v___x_146_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_145_, v_m13_144_);
return v___x_146_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_row1__prod___boxed(lean_object* v_s_147_){
_start:
{
uint8_t v_res_148_; lean_object* v_r_149_; 
v_res_148_ = lp_FiniteQuantum_DualWitness_row1__prod(v_s_147_);
lean_dec_ref(v_s_147_);
v_r_149_ = lean_box(v_res_148_);
return v_r_149_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_row2__prod(lean_object* v_s_150_){
_start:
{
uint8_t v_m21_151_; uint8_t v_m22_152_; uint8_t v_m23_153_; uint8_t v___x_154_; uint8_t v___x_155_; 
v_m21_151_ = lean_ctor_get_uint8(v_s_150_, 3);
v_m22_152_ = lean_ctor_get_uint8(v_s_150_, 4);
v_m23_153_ = lean_ctor_get_uint8(v_s_150_, 5);
v___x_154_ = lp_FiniteQuantum_DualWitness_mulSign(v_m21_151_, v_m22_152_);
v___x_155_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_154_, v_m23_153_);
return v___x_155_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_row2__prod___boxed(lean_object* v_s_156_){
_start:
{
uint8_t v_res_157_; lean_object* v_r_158_; 
v_res_157_ = lp_FiniteQuantum_DualWitness_row2__prod(v_s_156_);
lean_dec_ref(v_s_156_);
v_r_158_ = lean_box(v_res_157_);
return v_r_158_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_row3__prod(lean_object* v_s_159_){
_start:
{
uint8_t v_m31_160_; uint8_t v_m32_161_; uint8_t v_m33_162_; uint8_t v___x_163_; uint8_t v___x_164_; 
v_m31_160_ = lean_ctor_get_uint8(v_s_159_, 6);
v_m32_161_ = lean_ctor_get_uint8(v_s_159_, 7);
v_m33_162_ = lean_ctor_get_uint8(v_s_159_, 8);
v___x_163_ = lp_FiniteQuantum_DualWitness_mulSign(v_m31_160_, v_m32_161_);
v___x_164_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_163_, v_m33_162_);
return v___x_164_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_row3__prod___boxed(lean_object* v_s_165_){
_start:
{
uint8_t v_res_166_; lean_object* v_r_167_; 
v_res_166_ = lp_FiniteQuantum_DualWitness_row3__prod(v_s_165_);
lean_dec_ref(v_s_165_);
v_r_167_ = lean_box(v_res_166_);
return v_r_167_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_col1__prod(lean_object* v_s_168_){
_start:
{
uint8_t v_m11_169_; uint8_t v_m21_170_; uint8_t v_m31_171_; uint8_t v___x_172_; uint8_t v___x_173_; 
v_m11_169_ = lean_ctor_get_uint8(v_s_168_, 0);
v_m21_170_ = lean_ctor_get_uint8(v_s_168_, 3);
v_m31_171_ = lean_ctor_get_uint8(v_s_168_, 6);
v___x_172_ = lp_FiniteQuantum_DualWitness_mulSign(v_m11_169_, v_m21_170_);
v___x_173_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_172_, v_m31_171_);
return v___x_173_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_col1__prod___boxed(lean_object* v_s_174_){
_start:
{
uint8_t v_res_175_; lean_object* v_r_176_; 
v_res_175_ = lp_FiniteQuantum_DualWitness_col1__prod(v_s_174_);
lean_dec_ref(v_s_174_);
v_r_176_ = lean_box(v_res_175_);
return v_r_176_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_col2__prod(lean_object* v_s_177_){
_start:
{
uint8_t v_m12_178_; uint8_t v_m22_179_; uint8_t v_m32_180_; uint8_t v___x_181_; uint8_t v___x_182_; 
v_m12_178_ = lean_ctor_get_uint8(v_s_177_, 1);
v_m22_179_ = lean_ctor_get_uint8(v_s_177_, 4);
v_m32_180_ = lean_ctor_get_uint8(v_s_177_, 7);
v___x_181_ = lp_FiniteQuantum_DualWitness_mulSign(v_m12_178_, v_m22_179_);
v___x_182_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_181_, v_m32_180_);
return v___x_182_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_col2__prod___boxed(lean_object* v_s_183_){
_start:
{
uint8_t v_res_184_; lean_object* v_r_185_; 
v_res_184_ = lp_FiniteQuantum_DualWitness_col2__prod(v_s_183_);
lean_dec_ref(v_s_183_);
v_r_185_ = lean_box(v_res_184_);
return v_r_185_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_col3__prod(lean_object* v_s_186_){
_start:
{
uint8_t v_m13_187_; uint8_t v_m23_188_; uint8_t v_m33_189_; uint8_t v___x_190_; uint8_t v___x_191_; 
v_m13_187_ = lean_ctor_get_uint8(v_s_186_, 2);
v_m23_188_ = lean_ctor_get_uint8(v_s_186_, 5);
v_m33_189_ = lean_ctor_get_uint8(v_s_186_, 8);
v___x_190_ = lp_FiniteQuantum_DualWitness_mulSign(v_m13_187_, v_m23_188_);
v___x_191_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_190_, v_m33_189_);
return v___x_191_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_col3__prod___boxed(lean_object* v_s_192_){
_start:
{
uint8_t v_res_193_; lean_object* v_r_194_; 
v_res_193_ = lp_FiniteQuantum_DualWitness_col3__prod(v_s_192_);
lean_dec_ref(v_s_192_);
v_r_194_ = lean_box(v_res_193_);
return v_r_194_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_total__row__prod(lean_object* v_s_195_){
_start:
{
uint8_t v___x_196_; uint8_t v___x_197_; uint8_t v___x_198_; uint8_t v___x_199_; uint8_t v___x_200_; 
v___x_196_ = lp_FiniteQuantum_DualWitness_row1__prod(v_s_195_);
v___x_197_ = lp_FiniteQuantum_DualWitness_row2__prod(v_s_195_);
v___x_198_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_196_, v___x_197_);
v___x_199_ = lp_FiniteQuantum_DualWitness_row3__prod(v_s_195_);
v___x_200_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_198_, v___x_199_);
return v___x_200_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_total__row__prod___boxed(lean_object* v_s_201_){
_start:
{
uint8_t v_res_202_; lean_object* v_r_203_; 
v_res_202_ = lp_FiniteQuantum_DualWitness_total__row__prod(v_s_201_);
lean_dec_ref(v_s_201_);
v_r_203_ = lean_box(v_res_202_);
return v_r_203_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_DualWitness_total__col__prod(lean_object* v_s_204_){
_start:
{
uint8_t v___x_205_; uint8_t v___x_206_; uint8_t v___x_207_; uint8_t v___x_208_; uint8_t v___x_209_; 
v___x_205_ = lp_FiniteQuantum_DualWitness_col1__prod(v_s_204_);
v___x_206_ = lp_FiniteQuantum_DualWitness_col2__prod(v_s_204_);
v___x_207_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_205_, v___x_206_);
v___x_208_ = lp_FiniteQuantum_DualWitness_col3__prod(v_s_204_);
v___x_209_ = lp_FiniteQuantum_DualWitness_mulSign(v___x_207_, v___x_208_);
return v___x_209_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_DualWitness_total__col__prod___boxed(lean_object* v_s_210_){
_start:
{
uint8_t v_res_211_; lean_object* v_r_212_; 
v_res_211_ = lp_FiniteQuantum_DualWitness_total__col__prod(v_s_210_);
lean_dec_ref(v_s_210_);
v_r_212_ = lean_box(v_res_211_);
return v_r_212_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_DualWitness(uint8_t builtin) {
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
