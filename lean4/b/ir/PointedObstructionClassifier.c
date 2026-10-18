// Lean compiler output
// Module: PointedObstructionClassifier
// Imports: public import Init public meta import Init public import PrimitiveDifference
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
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_ObstructionStatus_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_instDecidableEqObstructionStatus(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_instDecidableEqObstructionStatus___boxed(lean_object*, lean_object*);
static const lean_string_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 40, .m_capacity = 40, .m_length = 39, .m_data = "OmegaCore.ObstructionStatus.exactRepair"};
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__0_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__0_value)}};
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__1 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__1_value;
static const lean_string_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 47, .m_capacity = 47, .m_length = 46, .m_data = "OmegaCore.ObstructionStatus.stabilizedSurvivor"};
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__2 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__2_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__2_value)}};
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__3 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__3_value;
static const lean_string_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 44, .m_capacity = 44, .m_length = 43, .m_data = "OmegaCore.ObstructionStatus.openObstruction"};
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__4 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__4_value;
static const lean_ctor_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__4_value)}};
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__5 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__5_value;
static lean_once_cell_t lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6;
static lean_once_cell_t lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaCore_instReprObstructionStatus___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus___closed__0_value;
LEAN_EXPORT const lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus = (const lean_object*)&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus___closed__0_value;
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx(uint8_t v_x_1_){
_start:
{
switch(v_x_1_)
{
case 0:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
case 1:
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(1u);
return v___x_3_;
}
default: 
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(2u);
return v___x_4_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx___boxed(lean_object* v_x_5_){
_start:
{
uint8_t v_x_boxed_6_; lean_object* v_res_7_; 
v_x_boxed_6_ = lean_unbox(v_x_5_);
v_res_7_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx(v_x_boxed_6_);
return v_res_7_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_toCtorIdx(uint8_t v_x_8_){
_start:
{
lean_object* v___x_9_; 
v___x_9_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx(v_x_8_);
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_toCtorIdx___boxed(lean_object* v_x_10_){
_start:
{
uint8_t v_x_4__boxed_11_; lean_object* v_res_12_; 
v_x_4__boxed_11_ = lean_unbox(v_x_10_);
v_res_12_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_toCtorIdx(v_x_4__boxed_11_);
return v_res_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___redArg(lean_object* v_k_13_){
_start:
{
lean_inc(v_k_13_);
return v_k_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___redArg___boxed(lean_object* v_k_14_){
_start:
{
lean_object* v_res_15_; 
v_res_15_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___redArg(v_k_14_);
lean_dec(v_k_14_);
return v_res_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim(lean_object* v_motive_16_, lean_object* v_ctorIdx_17_, uint8_t v_t_18_, lean_object* v_h_19_, lean_object* v_k_20_){
_start:
{
lean_inc(v_k_20_);
return v_k_20_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim___boxed(lean_object* v_motive_21_, lean_object* v_ctorIdx_22_, lean_object* v_t_23_, lean_object* v_h_24_, lean_object* v_k_25_){
_start:
{
uint8_t v_t_boxed_26_; lean_object* v_res_27_; 
v_t_boxed_26_ = lean_unbox(v_t_23_);
v_res_27_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorElim(v_motive_21_, v_ctorIdx_22_, v_t_boxed_26_, v_h_24_, v_k_25_);
lean_dec(v_k_25_);
lean_dec(v_ctorIdx_22_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___redArg(lean_object* v_exactRepair_28_){
_start:
{
lean_inc(v_exactRepair_28_);
return v_exactRepair_28_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___redArg___boxed(lean_object* v_exactRepair_29_){
_start:
{
lean_object* v_res_30_; 
v_res_30_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___redArg(v_exactRepair_29_);
lean_dec(v_exactRepair_29_);
return v_res_30_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim(lean_object* v_motive_31_, uint8_t v_t_32_, lean_object* v_h_33_, lean_object* v_exactRepair_34_){
_start:
{
lean_inc(v_exactRepair_34_);
return v_exactRepair_34_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim___boxed(lean_object* v_motive_35_, lean_object* v_t_36_, lean_object* v_h_37_, lean_object* v_exactRepair_38_){
_start:
{
uint8_t v_t_boxed_39_; lean_object* v_res_40_; 
v_t_boxed_39_ = lean_unbox(v_t_36_);
v_res_40_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_exactRepair_elim(v_motive_35_, v_t_boxed_39_, v_h_37_, v_exactRepair_38_);
lean_dec(v_exactRepair_38_);
return v_res_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___redArg(lean_object* v_stabilizedSurvivor_41_){
_start:
{
lean_inc(v_stabilizedSurvivor_41_);
return v_stabilizedSurvivor_41_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___redArg___boxed(lean_object* v_stabilizedSurvivor_42_){
_start:
{
lean_object* v_res_43_; 
v_res_43_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___redArg(v_stabilizedSurvivor_42_);
lean_dec(v_stabilizedSurvivor_42_);
return v_res_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim(lean_object* v_motive_44_, uint8_t v_t_45_, lean_object* v_h_46_, lean_object* v_stabilizedSurvivor_47_){
_start:
{
lean_inc(v_stabilizedSurvivor_47_);
return v_stabilizedSurvivor_47_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim___boxed(lean_object* v_motive_48_, lean_object* v_t_49_, lean_object* v_h_50_, lean_object* v_stabilizedSurvivor_51_){
_start:
{
uint8_t v_t_boxed_52_; lean_object* v_res_53_; 
v_t_boxed_52_ = lean_unbox(v_t_49_);
v_res_53_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_stabilizedSurvivor_elim(v_motive_48_, v_t_boxed_52_, v_h_50_, v_stabilizedSurvivor_51_);
lean_dec(v_stabilizedSurvivor_51_);
return v_res_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___redArg(lean_object* v_openObstruction_54_){
_start:
{
lean_inc(v_openObstruction_54_);
return v_openObstruction_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___redArg___boxed(lean_object* v_openObstruction_55_){
_start:
{
lean_object* v_res_56_; 
v_res_56_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___redArg(v_openObstruction_55_);
lean_dec(v_openObstruction_55_);
return v_res_56_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim(lean_object* v_motive_57_, uint8_t v_t_58_, lean_object* v_h_59_, lean_object* v_openObstruction_60_){
_start:
{
lean_inc(v_openObstruction_60_);
return v_openObstruction_60_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim___boxed(lean_object* v_motive_61_, lean_object* v_t_62_, lean_object* v_h_63_, lean_object* v_openObstruction_64_){
_start:
{
uint8_t v_t_boxed_65_; lean_object* v_res_66_; 
v_t_boxed_65_ = lean_unbox(v_t_62_);
v_res_66_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_openObstruction_elim(v_motive_61_, v_t_boxed_65_, v_h_63_, v_openObstruction_64_);
lean_dec(v_openObstruction_64_);
return v_res_66_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_ObstructionStatus_ofNat(lean_object* v_n_67_){
_start:
{
lean_object* v___x_68_; uint8_t v___x_69_; 
v___x_68_ = lean_unsigned_to_nat(0u);
v___x_69_ = lean_nat_dec_le(v_n_67_, v___x_68_);
if (v___x_69_ == 0)
{
lean_object* v___x_70_; uint8_t v___x_71_; 
v___x_70_ = lean_unsigned_to_nat(1u);
v___x_71_ = lean_nat_dec_le(v_n_67_, v___x_70_);
if (v___x_71_ == 0)
{
uint8_t v___x_72_; 
v___x_72_ = 2;
return v___x_72_;
}
else
{
uint8_t v___x_73_; 
v___x_73_ = 1;
return v___x_73_;
}
}
else
{
uint8_t v___x_74_; 
v___x_74_ = 0;
return v___x_74_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionStatus_ofNat___boxed(lean_object* v_n_75_){
_start:
{
uint8_t v_res_76_; lean_object* v_r_77_; 
v_res_76_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ofNat(v_n_75_);
lean_dec(v_n_75_);
v_r_77_ = lean_box(v_res_76_);
return v_r_77_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_instDecidableEqObstructionStatus(uint8_t v_x_78_, uint8_t v_y_79_){
_start:
{
lean_object* v___x_80_; lean_object* v___x_81_; uint8_t v___x_82_; 
v___x_80_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx(v_x_78_);
v___x_81_ = lp_FiniteQuantum_OmegaCore_ObstructionStatus_ctorIdx(v_y_79_);
v___x_82_ = lean_nat_dec_eq(v___x_80_, v___x_81_);
lean_dec(v___x_81_);
lean_dec(v___x_80_);
return v___x_82_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_instDecidableEqObstructionStatus___boxed(lean_object* v_x_83_, lean_object* v_y_84_){
_start:
{
uint8_t v_x_13__boxed_85_; uint8_t v_y_14__boxed_86_; uint8_t v_res_87_; lean_object* v_r_88_; 
v_x_13__boxed_85_ = lean_unbox(v_x_83_);
v_y_14__boxed_86_ = lean_unbox(v_y_84_);
v_res_87_ = lp_FiniteQuantum_OmegaCore_instDecidableEqObstructionStatus(v_x_13__boxed_85_, v_y_14__boxed_86_);
v_r_88_ = lean_box(v_res_87_);
return v_r_88_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6(void){
_start:
{
lean_object* v___x_98_; lean_object* v___x_99_; 
v___x_98_ = lean_unsigned_to_nat(2u);
v___x_99_ = lean_nat_to_int(v___x_98_);
return v___x_99_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7(void){
_start:
{
lean_object* v___x_100_; lean_object* v___x_101_; 
v___x_100_ = lean_unsigned_to_nat(1u);
v___x_101_ = lean_nat_to_int(v___x_100_);
return v___x_101_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr(uint8_t v_x_102_, lean_object* v_prec_103_){
_start:
{
lean_object* v___y_105_; lean_object* v___y_112_; lean_object* v___y_119_; 
switch(v_x_102_)
{
case 0:
{
lean_object* v___x_125_; uint8_t v___x_126_; 
v___x_125_ = lean_unsigned_to_nat(1024u);
v___x_126_ = lean_nat_dec_le(v___x_125_, v_prec_103_);
if (v___x_126_ == 0)
{
lean_object* v___x_127_; 
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6, &lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6_once, _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6);
v___y_105_ = v___x_127_;
goto v___jp_104_;
}
else
{
lean_object* v___x_128_; 
v___x_128_ = lean_obj_once(&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7, &lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7_once, _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7);
v___y_105_ = v___x_128_;
goto v___jp_104_;
}
}
case 1:
{
lean_object* v___x_129_; uint8_t v___x_130_; 
v___x_129_ = lean_unsigned_to_nat(1024u);
v___x_130_ = lean_nat_dec_le(v___x_129_, v_prec_103_);
if (v___x_130_ == 0)
{
lean_object* v___x_131_; 
v___x_131_ = lean_obj_once(&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6, &lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6_once, _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6);
v___y_112_ = v___x_131_;
goto v___jp_111_;
}
else
{
lean_object* v___x_132_; 
v___x_132_ = lean_obj_once(&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7, &lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7_once, _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7);
v___y_112_ = v___x_132_;
goto v___jp_111_;
}
}
default: 
{
lean_object* v___x_133_; uint8_t v___x_134_; 
v___x_133_ = lean_unsigned_to_nat(1024u);
v___x_134_ = lean_nat_dec_le(v___x_133_, v_prec_103_);
if (v___x_134_ == 0)
{
lean_object* v___x_135_; 
v___x_135_ = lean_obj_once(&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6, &lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6_once, _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__6);
v___y_119_ = v___x_135_;
goto v___jp_118_;
}
else
{
lean_object* v___x_136_; 
v___x_136_ = lean_obj_once(&lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7, &lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7_once, _init_lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__7);
v___y_119_ = v___x_136_;
goto v___jp_118_;
}
}
}
v___jp_104_:
{
lean_object* v___x_106_; lean_object* v___x_107_; uint8_t v___x_108_; lean_object* v___x_109_; lean_object* v___x_110_; 
v___x_106_ = ((lean_object*)(lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__1));
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
v___x_113_ = ((lean_object*)(lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__3));
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
v___jp_118_:
{
lean_object* v___x_120_; lean_object* v___x_121_; uint8_t v___x_122_; lean_object* v___x_123_; lean_object* v___x_124_; 
v___x_120_ = ((lean_object*)(lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___closed__5));
lean_inc(v___y_119_);
v___x_121_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_121_, 0, v___y_119_);
lean_ctor_set(v___x_121_, 1, v___x_120_);
v___x_122_ = 0;
v___x_123_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_123_, 0, v___x_121_);
lean_ctor_set_uint8(v___x_123_, sizeof(void*)*1, v___x_122_);
v___x_124_ = l_Repr_addAppParen(v___x_123_, v_prec_103_);
return v___x_124_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr___boxed(lean_object* v_x_137_, lean_object* v_prec_138_){
_start:
{
uint8_t v_x_177__boxed_139_; lean_object* v_res_140_; 
v_x_177__boxed_139_ = lean_unbox(v_x_137_);
v_res_140_ = lp_FiniteQuantum_OmegaCore_instReprObstructionStatus_repr(v_x_177__boxed_139_, v_prec_138_);
lean_dec(v_prec_138_);
return v_res_140_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg(lean_object* v_C_143_, lean_object* v_q_144_){
_start:
{
lean_object* v_Phi_145_; lean_object* v_Gamma_146_; lean_object* v___x_147_; lean_object* v___x_148_; uint8_t v___x_149_; 
v_Phi_145_ = lean_ctor_get(v_C_143_, 0);
lean_inc_ref(v_Phi_145_);
v_Gamma_146_ = lean_ctor_get(v_C_143_, 1);
lean_inc_ref(v_Gamma_146_);
lean_dec_ref(v_C_143_);
lean_inc(v_q_144_);
v___x_147_ = lean_apply_1(v_Phi_145_, v_q_144_);
v___x_148_ = lean_unsigned_to_nat(0u);
v___x_149_ = lean_nat_dec_eq(v___x_147_, v___x_148_);
lean_dec(v___x_147_);
if (v___x_149_ == 0)
{
lean_object* v___x_150_; uint8_t v___x_151_; 
v___x_150_ = lean_apply_1(v_Gamma_146_, v_q_144_);
v___x_151_ = lean_nat_dec_eq(v___x_150_, v___x_148_);
lean_dec(v___x_150_);
if (v___x_151_ == 0)
{
uint8_t v___x_152_; 
v___x_152_ = 2;
return v___x_152_;
}
else
{
uint8_t v___x_153_; 
v___x_153_ = 1;
return v___x_153_;
}
}
else
{
uint8_t v___x_154_; 
lean_dec_ref(v_Gamma_146_);
lean_dec(v_q_144_);
v___x_154_ = 0;
return v___x_154_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg___boxed(lean_object* v_C_155_, lean_object* v_q_156_){
_start:
{
uint8_t v_res_157_; lean_object* v_r_158_; 
v_res_157_ = lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg(v_C_155_, v_q_156_);
v_r_158_ = lean_box(v_res_157_);
return v_r_158_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize(lean_object* v_Q_159_, lean_object* v_C_160_, lean_object* v_q_161_){
_start:
{
uint8_t v___x_162_; 
v___x_162_ = lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___redArg(v_C_160_, v_q_161_);
return v___x_162_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize___boxed(lean_object* v_Q_163_, lean_object* v_C_164_, lean_object* v_q_165_){
_start:
{
uint8_t v_res_166_; lean_object* v_r_167_; 
v_res_166_ = lp_FiniteQuantum_OmegaCore_ObstructionClassifier_terminalize(v_Q_163_, v_C_164_, v_q_165_);
v_r_167_ = lean_box(v_res_166_);
return v_r_167_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveDifference(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PointedObstructionClassifier(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveDifference(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
