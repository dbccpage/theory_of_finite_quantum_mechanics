// Lean compiler output
// Module: H004FreeLinearization
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
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
lean_object* l_List_filterTR_loop___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_List_mapTR_loop___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(lean_object*, lean_object*);
extern lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vadd___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vadd(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_smul___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_smul(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueF2(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueF2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueInt(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueInt___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vadd___redArg(lean_object* v_P_1_, lean_object* v_u_2_, lean_object* v_v_3_, lean_object* v_q_4_){
_start:
{
lean_object* v_add_5_; lean_object* v___x_6_; lean_object* v___x_7_; lean_object* v___x_8_; 
v_add_5_ = lean_ctor_get(v_P_1_, 0);
lean_inc(v_add_5_);
lean_dec_ref(v_P_1_);
lean_inc(v_q_4_);
v___x_6_ = lean_apply_1(v_u_2_, v_q_4_);
v___x_7_ = lean_apply_1(v_v_3_, v_q_4_);
v___x_8_ = lean_apply_2(v_add_5_, v___x_6_, v___x_7_);
return v___x_8_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vadd(lean_object* v_K_9_, lean_object* v_Q_10_, lean_object* v_P_11_, lean_object* v_u_12_, lean_object* v_v_13_, lean_object* v_q_14_){
_start:
{
lean_object* v___x_15_; 
v___x_15_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_vadd___redArg(v_P_11_, v_u_12_, v_v_13_, v_q_14_);
return v___x_15_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_smul___redArg(lean_object* v_P_16_, lean_object* v_c_17_, lean_object* v_v_18_, lean_object* v_q_19_){
_start:
{
lean_object* v_mul_20_; lean_object* v___x_21_; lean_object* v___x_22_; 
v_mul_20_ = lean_ctor_get(v_P_16_, 1);
lean_inc(v_mul_20_);
lean_dec_ref(v_P_16_);
v___x_21_ = lean_apply_1(v_v_18_, v_q_19_);
v___x_22_ = lean_apply_2(v_mul_20_, v_c_17_, v___x_21_);
return v___x_22_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_smul(lean_object* v_K_23_, lean_object* v_Q_24_, lean_object* v_P_25_, lean_object* v_c_26_, lean_object* v_v_27_, lean_object* v_q_28_){
_start:
{
lean_object* v___x_29_; 
v___x_29_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_smul___redArg(v_P_25_, v_c_26_, v_v_27_, v_q_28_);
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___redArg(lean_object* v_P_30_){
_start:
{
lean_object* v_zero_31_; 
v_zero_31_ = lean_ctor_get(v_P_30_, 3);
lean_inc(v_zero_31_);
return v_zero_31_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___redArg___boxed(lean_object* v_P_32_){
_start:
{
lean_object* v_res_33_; 
v_res_33_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___redArg(v_P_32_);
lean_dec_ref(v_P_32_);
return v_res_33_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero(lean_object* v_K_34_, lean_object* v_Q_35_, lean_object* v_P_36_, lean_object* v_x_37_){
_start:
{
lean_object* v_zero_38_; 
v_zero_38_ = lean_ctor_get(v_P_36_, 3);
lean_inc(v_zero_38_);
return v_zero_38_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero___boxed(lean_object* v_K_39_, lean_object* v_Q_40_, lean_object* v_P_41_, lean_object* v_x_42_){
_start:
{
lean_object* v_res_43_; 
v_res_43_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_vzero(v_K_39_, v_Q_40_, v_P_41_, v_x_42_);
lean_dec(v_x_42_);
lean_dec_ref(v_P_41_);
return v_res_43_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg(lean_object* v_P_44_, lean_object* v_inst_45_, lean_object* v_q_46_, lean_object* v_x_47_){
_start:
{
lean_object* v___x_48_; uint8_t v___x_49_; 
v___x_48_ = lean_apply_2(v_inst_45_, v_q_46_, v_x_47_);
v___x_49_ = lean_unbox(v___x_48_);
if (v___x_49_ == 0)
{
lean_object* v_zero_50_; 
v_zero_50_ = lean_ctor_get(v_P_44_, 3);
lean_inc(v_zero_50_);
return v_zero_50_;
}
else
{
lean_object* v_one_51_; 
v_one_51_ = lean_ctor_get(v_P_44_, 4);
lean_inc(v_one_51_);
return v_one_51_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg___boxed(lean_object* v_P_52_, lean_object* v_inst_53_, lean_object* v_q_54_, lean_object* v_x_55_){
_start:
{
lean_object* v_res_56_; 
v_res_56_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg(v_P_52_, v_inst_53_, v_q_54_, v_x_55_);
lean_dec_ref(v_P_52_);
return v_res_56_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta(lean_object* v_K_57_, lean_object* v_Q_58_, lean_object* v_P_59_, lean_object* v_inst_60_, lean_object* v_q_61_, lean_object* v_x_62_){
_start:
{
lean_object* v___x_63_; 
v___x_63_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___redArg(v_P_59_, v_inst_60_, v_q_61_, v_x_62_);
return v___x_63_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___boxed(lean_object* v_K_64_, lean_object* v_Q_65_, lean_object* v_P_66_, lean_object* v_inst_67_, lean_object* v_q_68_, lean_object* v_x_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta(v_K_64_, v_Q_65_, v_P_66_, v_inst_67_, v_q_68_, v_x_69_);
lean_dec_ref(v_P_66_);
return v_res_70_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg___lam__0(lean_object* v_00_u03c4_71_, lean_object* v_inst_72_, lean_object* v_q_73_, lean_object* v_x_74_){
_start:
{
lean_object* v___x_75_; lean_object* v___x_76_; uint8_t v___x_77_; 
v___x_75_ = lean_apply_1(v_00_u03c4_71_, v_x_74_);
v___x_76_ = lean_apply_2(v_inst_72_, v___x_75_, v_q_73_);
v___x_77_ = lean_unbox(v___x_76_);
return v___x_77_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg___lam__0___boxed(lean_object* v_00_u03c4_78_, lean_object* v_inst_79_, lean_object* v_q_80_, lean_object* v_x_81_){
_start:
{
uint8_t v_res_82_; lean_object* v_r_83_; 
v_res_82_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg___lam__0(v_00_u03c4_78_, v_inst_79_, v_q_80_, v_x_81_);
v_r_83_ = lean_box(v_res_82_);
return v_r_83_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg(lean_object* v_P_84_, lean_object* v_inst_85_, lean_object* v_E_86_, lean_object* v_00_u03c4_87_, lean_object* v_v_88_, lean_object* v_q_89_){
_start:
{
lean_object* v___f_90_; lean_object* v___x_91_; lean_object* v___x_92_; lean_object* v___x_93_; lean_object* v___x_94_; 
v___f_90_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg___lam__0___boxed), 4, 3);
lean_closure_set(v___f_90_, 0, v_00_u03c4_87_);
lean_closure_set(v___f_90_, 1, v_inst_85_);
lean_closure_set(v___f_90_, 2, v_q_89_);
v___x_91_ = lean_box(0);
v___x_92_ = l_List_filterTR_loop___redArg(v___f_90_, v_E_86_, v___x_91_);
v___x_93_ = l_List_mapTR_loop___redArg(v_v_88_, v___x_92_, v___x_91_);
v___x_94_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_rsum___redArg(v_P_84_, v___x_93_);
return v___x_94_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush(lean_object* v_K_95_, lean_object* v_X_96_, lean_object* v_Q_97_, lean_object* v_P_98_, lean_object* v_inst_99_, lean_object* v_E_100_, lean_object* v_00_u03c4_101_, lean_object* v_v_102_, lean_object* v_q_103_){
_start:
{
lean_object* v___x_104_; 
v___x_104_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_linPush___redArg(v_P_98_, v_inst_99_, v_E_100_, v_00_u03c4_101_, v_v_102_, v_q_103_);
return v___x_104_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(lean_object* v_P_105_, uint8_t v_q_106_, uint8_t v_x_107_){
_start:
{
if (v_q_106_ == 0)
{
if (v_x_107_ == 0)
{
lean_object* v_one_108_; 
v_one_108_ = lean_ctor_get(v_P_105_, 4);
lean_inc(v_one_108_);
return v_one_108_;
}
else
{
lean_object* v_zero_109_; 
v_zero_109_ = lean_ctor_get(v_P_105_, 3);
lean_inc(v_zero_109_);
return v_zero_109_;
}
}
else
{
if (v_x_107_ == 0)
{
lean_object* v_zero_110_; 
v_zero_110_ = lean_ctor_get(v_P_105_, 3);
lean_inc(v_zero_110_);
return v_zero_110_;
}
else
{
lean_object* v_one_111_; 
v_one_111_ = lean_ctor_get(v_P_105_, 4);
lean_inc(v_one_111_);
return v_one_111_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg___boxed(lean_object* v_P_112_, lean_object* v_q_113_, lean_object* v_x_114_){
_start:
{
uint8_t v_q_boxed_115_; uint8_t v_x_boxed_116_; lean_object* v_res_117_; 
v_q_boxed_115_ = lean_unbox(v_q_113_);
v_x_boxed_116_ = lean_unbox(v_x_114_);
v_res_117_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(v_P_112_, v_q_boxed_115_, v_x_boxed_116_);
lean_dec_ref(v_P_112_);
return v_res_117_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0(lean_object* v_K_118_, lean_object* v_P_119_, uint8_t v_q_120_, uint8_t v_x_121_){
_start:
{
lean_object* v___x_122_; 
v___x_122_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(v_P_119_, v_q_120_, v_x_121_);
return v___x_122_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___boxed(lean_object* v_K_123_, lean_object* v_P_124_, lean_object* v_q_125_, lean_object* v_x_126_){
_start:
{
uint8_t v_q_boxed_127_; uint8_t v_x_boxed_128_; lean_object* v_res_129_; 
v_q_boxed_127_ = lean_unbox(v_q_125_);
v_x_boxed_128_ = lean_unbox(v_x_126_);
v_res_129_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0(v_K_123_, v_P_124_, v_q_boxed_127_, v_x_boxed_128_);
lean_dec_ref(v_P_124_);
return v_res_129_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueF2(uint8_t v_a_130_){
_start:
{
lean_object* v___x_131_; uint8_t v___x_132_; lean_object* v___x_133_; uint8_t v___x_134_; 
v___x_131_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_f2Pack;
v___x_132_ = 1;
v___x_133_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(v___x_131_, v___x_132_, v_a_130_);
v___x_134_ = lean_unbox(v___x_133_);
lean_dec(v___x_133_);
return v___x_134_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueF2___boxed(lean_object* v_a_135_){
_start:
{
uint8_t v_a_48__boxed_136_; uint8_t v_res_137_; lean_object* v_r_138_; 
v_a_48__boxed_136_ = lean_unbox(v_a_135_);
v_res_137_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueF2(v_a_48__boxed_136_);
v_r_138_ = lean_box(v_res_137_);
return v_r_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueInt(uint8_t v_a_139_){
_start:
{
lean_object* v___x_140_; uint8_t v___x_141_; lean_object* v___x_142_; 
v___x_140_ = lp_FiniteQuantum_FableHilbertWalk20260819_HWKernel_intPack;
v___x_141_ = 1;
v___x_142_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_delta___at___00FableHilbertWalk20260819_H004_deltaTrueF2_spec__0___redArg(v___x_140_, v___x_141_, v_a_139_);
return v___x_142_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueInt___boxed(lean_object* v_a_143_){
_start:
{
uint8_t v_a_14__boxed_144_; lean_object* v_res_145_; 
v_a_14__boxed_144_ = lean_unbox(v_a_143_);
v_res_145_ = lp_FiniteQuantum_FableHilbertWalk20260819_H004_deltaTrueInt(v_a_14__boxed_144_);
return v_res_145_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H004FreeLinearization(uint8_t builtin) {
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
