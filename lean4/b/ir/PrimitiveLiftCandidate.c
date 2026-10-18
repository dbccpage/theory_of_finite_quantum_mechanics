// Lean compiler output
// Module: PrimitiveLiftCandidate
// Imports: public import Init public meta import Init public import PrimitiveTerminalPacket
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
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableMatch__1PropLtNatFalse(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableMatch__1PropLtNatFalse___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableStrictly__improves(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableStrictly__improves___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_ctor_object lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*3 + 0, .m_other = 3, .m_tag = 0}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult___closed__0_value;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rollback(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw___redArg(lean_object* v_C_1_, lean_object* v_x_2_){
_start:
{
uint8_t v___x_3_; uint8_t v___x_4_; lean_object* v___x_5_; lean_object* v___x_6_; 
v___x_3_ = 1;
v___x_4_ = 0;
lean_inc(v_x_2_);
v___x_5_ = lp_FiniteQuantum_OmegaCore_PrimitiveTerminalPacket_packetFor___redArg(v_C_1_, v_x_2_, v___x_3_, v___x_4_);
v___x_6_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_6_, 0, v_x_2_);
lean_ctor_set(v___x_6_, 1, v___x_5_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw(lean_object* v_00_u03b1_7_, lean_object* v_00_u03b2_8_, lean_object* v_P_9_, lean_object* v_C_10_, lean_object* v_x_11_){
_start:
{
lean_object* v___x_12_; 
v___x_12_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw___redArg(v_C_10_, v_x_11_);
return v___x_12_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw___boxed(lean_object* v_00_u03b1_13_, lean_object* v_00_u03b2_14_, lean_object* v_P_15_, lean_object* v_C_16_, lean_object* v_x_17_){
_start:
{
lean_object* v_res_18_; 
v_res_18_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rawCarrierFromRaw(v_00_u03b1_13_, v_00_u03b2_14_, v_P_15_, v_C_16_, v_x_17_);
lean_dec_ref(v_P_15_);
return v_res_18_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableMatch__1PropLtNatFalse(lean_object* v_x1_19_, lean_object* v_x2_20_){
_start:
{
uint8_t v___x_21_; 
v___x_21_ = 0;
if (lean_obj_tag(v_x1_19_) == 0)
{
return v___x_21_;
}
else
{
if (lean_obj_tag(v_x2_20_) == 0)
{
return v___x_21_;
}
else
{
lean_object* v_val_22_; lean_object* v_val_23_; uint8_t v___x_24_; 
v_val_22_ = lean_ctor_get(v_x1_19_, 0);
v_val_23_ = lean_ctor_get(v_x2_20_, 0);
v___x_24_ = lean_nat_dec_lt(v_val_23_, v_val_22_);
return v___x_24_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableMatch__1PropLtNatFalse___boxed(lean_object* v_x1_25_, lean_object* v_x2_26_){
_start:
{
uint8_t v_res_27_; lean_object* v_r_28_; 
v_res_27_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableMatch__1PropLtNatFalse(v_x1_25_, v_x2_26_);
lean_dec(v_x2_26_);
lean_dec(v_x1_25_);
v_r_28_ = lean_box(v_res_27_);
return v_r_28_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableStrictly__improves(lean_object* v_p1_29_, lean_object* v_g1_30_, lean_object* v_x1_31_, lean_object* v_p2_32_, lean_object* v_g2_33_, lean_object* v_x2_34_){
_start:
{
uint8_t v___x_35_; 
v___x_35_ = lean_nat_dec_lt(v_p2_32_, v_p1_29_);
if (v___x_35_ == 0)
{
uint8_t v___x_36_; uint8_t v___x_37_; uint8_t v___x_38_; 
v___x_36_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableMatch__1PropLtNatFalse(v_x1_31_, v_x2_34_);
v___x_37_ = lean_nat_dec_eq(v_g2_33_, v_g1_30_);
v___x_38_ = lean_nat_dec_eq(v_p2_32_, v_p1_29_);
if (v___x_38_ == 0)
{
goto v___jp_39_;
}
else
{
uint8_t v___x_40_; 
v___x_40_ = lean_nat_dec_lt(v_g2_33_, v_g1_30_);
if (v___x_40_ == 0)
{
goto v___jp_39_;
}
else
{
return v___x_40_;
}
}
v___jp_39_:
{
if (v___x_38_ == 0)
{
return v___x_38_;
}
else
{
if (v___x_37_ == 0)
{
return v___x_37_;
}
else
{
return v___x_36_;
}
}
}
}
else
{
return v___x_35_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableStrictly__improves___boxed(lean_object* v_p1_41_, lean_object* v_g1_42_, lean_object* v_x1_43_, lean_object* v_p2_44_, lean_object* v_g2_45_, lean_object* v_x2_46_){
_start:
{
uint8_t v_res_47_; lean_object* v_r_48_; 
v_res_47_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableStrictly__improves(v_p1_41_, v_g1_42_, v_x1_43_, v_p2_44_, v_g2_45_, v_x2_46_);
lean_dec(v_x2_46_);
lean_dec(v_g2_45_);
lean_dec(v_p2_44_);
lean_dec(v_x1_43_);
lean_dec(v_g1_42_);
lean_dec(v_p1_41_);
v_r_48_ = lean_box(v_res_47_);
return v_r_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult(lean_object* v_p__before_52_, lean_object* v_g__before_53_){
_start:
{
lean_object* v___x_54_; 
v___x_54_ = ((lean_object*)(lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult___closed__0));
return v___x_54_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult___boxed(lean_object* v_p__before_55_, lean_object* v_g__before_56_){
_start:
{
lean_object* v_res_57_; 
v_res_57_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_adjoinRepairGeneratorResult(v_p__before_55_, v_g__before_56_);
lean_dec(v_g__before_56_);
lean_dec(v_p__before_55_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_rollback(lean_object* v_p__before_58_, lean_object* v_g__before_59_, lean_object* v_x__before_60_, lean_object* v_res_61_){
_start:
{
lean_object* v_phi__after_62_; lean_object* v_gamma__after_63_; lean_object* v_xi__after_64_; uint8_t v___x_65_; 
v_phi__after_62_ = lean_ctor_get(v_res_61_, 0);
v_gamma__after_63_ = lean_ctor_get(v_res_61_, 1);
v_xi__after_64_ = lean_ctor_get(v_res_61_, 2);
v___x_65_ = lp_FiniteQuantum_OmegaCore_PrimitiveLiftCandidate_instDecidableStrictly__improves(v_p__before_58_, v_g__before_59_, v_x__before_60_, v_phi__after_62_, v_gamma__after_63_, v_xi__after_64_);
if (v___x_65_ == 0)
{
lean_object* v___x_67_; uint8_t v_isShared_68_; uint8_t v_isSharedCheck_72_; 
v_isSharedCheck_72_ = !lean_is_exclusive(v_res_61_);
if (v_isSharedCheck_72_ == 0)
{
lean_object* v_unused_73_; lean_object* v_unused_74_; lean_object* v_unused_75_; 
v_unused_73_ = lean_ctor_get(v_res_61_, 2);
lean_dec(v_unused_73_);
v_unused_74_ = lean_ctor_get(v_res_61_, 1);
lean_dec(v_unused_74_);
v_unused_75_ = lean_ctor_get(v_res_61_, 0);
lean_dec(v_unused_75_);
v___x_67_ = v_res_61_;
v_isShared_68_ = v_isSharedCheck_72_;
goto v_resetjp_66_;
}
else
{
lean_dec(v_res_61_);
v___x_67_ = lean_box(0);
v_isShared_68_ = v_isSharedCheck_72_;
goto v_resetjp_66_;
}
v_resetjp_66_:
{
lean_object* v___x_70_; 
if (v_isShared_68_ == 0)
{
lean_ctor_set(v___x_67_, 2, v_x__before_60_);
lean_ctor_set(v___x_67_, 1, v_g__before_59_);
lean_ctor_set(v___x_67_, 0, v_p__before_58_);
v___x_70_ = v___x_67_;
goto v_reusejp_69_;
}
else
{
lean_object* v_reuseFailAlloc_71_; 
v_reuseFailAlloc_71_ = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(v_reuseFailAlloc_71_, 0, v_p__before_58_);
lean_ctor_set(v_reuseFailAlloc_71_, 1, v_g__before_59_);
lean_ctor_set(v_reuseFailAlloc_71_, 2, v_x__before_60_);
v___x_70_ = v_reuseFailAlloc_71_;
goto v_reusejp_69_;
}
v_reusejp_69_:
{
return v___x_70_;
}
}
}
else
{
lean_dec(v_x__before_60_);
lean_dec(v_g__before_59_);
lean_dec(v_p__before_58_);
return v_res_61_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_PrimitiveTerminalPacket(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_PrimitiveLiftCandidate(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_FiniteQuantum_PrimitiveTerminalPacket(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
