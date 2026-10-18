// Lean compiler output
// Module: H015DilationCount
// Imports: public import Init public meta import Init public import HWKernel public import H015IrreversibleFork
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilOf(uint8_t, uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilOf___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT;
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015DilationCount_0__FableHilbertWalk20260819_H015DilationCount_dilOf_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015DilationCount_0__FableHilbertWalk20260819_H015DilationCount_dilOf_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilOf(uint8_t v_flipF_1_, uint8_t v_flipT_2_, lean_object* v_x_3_){
_start:
{
lean_object* v_fst_4_; uint8_t v___x_5_; 
v_fst_4_ = lean_ctor_get(v_x_3_, 0);
v___x_5_ = lean_unbox(v_fst_4_);
if (v___x_5_ == 0)
{
if (v_flipF_1_ == 0)
{
return v_x_3_;
}
else
{
lean_object* v_snd_6_; lean_object* v___x_8_; uint8_t v_isShared_9_; uint8_t v_isSharedCheck_18_; 
lean_inc(v_fst_4_);
v_snd_6_ = lean_ctor_get(v_x_3_, 1);
v_isSharedCheck_18_ = !lean_is_exclusive(v_x_3_);
if (v_isSharedCheck_18_ == 0)
{
lean_object* v_unused_19_; 
v_unused_19_ = lean_ctor_get(v_x_3_, 0);
lean_dec(v_unused_19_);
v___x_8_ = v_x_3_;
v_isShared_9_ = v_isSharedCheck_18_;
goto v_resetjp_7_;
}
else
{
lean_inc(v_snd_6_);
lean_dec(v_x_3_);
v___x_8_ = lean_box(0);
v_isShared_9_ = v_isSharedCheck_18_;
goto v_resetjp_7_;
}
v_resetjp_7_:
{
uint8_t v___x_10_; 
v___x_10_ = lean_unbox(v_snd_6_);
lean_dec(v_snd_6_);
if (v___x_10_ == 0)
{
lean_object* v___x_11_; lean_object* v___x_13_; 
v___x_11_ = lean_box(v_flipF_1_);
if (v_isShared_9_ == 0)
{
lean_ctor_set(v___x_8_, 1, v___x_11_);
v___x_13_ = v___x_8_;
goto v_reusejp_12_;
}
else
{
lean_object* v_reuseFailAlloc_14_; 
v_reuseFailAlloc_14_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_14_, 0, v_fst_4_);
lean_ctor_set(v_reuseFailAlloc_14_, 1, v___x_11_);
v___x_13_ = v_reuseFailAlloc_14_;
goto v_reusejp_12_;
}
v_reusejp_12_:
{
return v___x_13_;
}
}
else
{
lean_object* v___x_16_; 
lean_inc(v_fst_4_);
if (v_isShared_9_ == 0)
{
lean_ctor_set(v___x_8_, 1, v_fst_4_);
v___x_16_ = v___x_8_;
goto v_reusejp_15_;
}
else
{
lean_object* v_reuseFailAlloc_17_; 
v_reuseFailAlloc_17_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_17_, 0, v_fst_4_);
lean_ctor_set(v_reuseFailAlloc_17_, 1, v_fst_4_);
v___x_16_ = v_reuseFailAlloc_17_;
goto v_reusejp_15_;
}
v_reusejp_15_:
{
return v___x_16_;
}
}
}
}
}
else
{
if (v_flipT_2_ == 0)
{
return v_x_3_;
}
else
{
lean_object* v_snd_20_; lean_object* v___x_22_; uint8_t v_isShared_23_; uint8_t v_isSharedCheck_33_; 
lean_inc(v_fst_4_);
v_snd_20_ = lean_ctor_get(v_x_3_, 1);
v_isSharedCheck_33_ = !lean_is_exclusive(v_x_3_);
if (v_isSharedCheck_33_ == 0)
{
lean_object* v_unused_34_; 
v_unused_34_ = lean_ctor_get(v_x_3_, 0);
lean_dec(v_unused_34_);
v___x_22_ = v_x_3_;
v_isShared_23_ = v_isSharedCheck_33_;
goto v_resetjp_21_;
}
else
{
lean_inc(v_snd_20_);
lean_dec(v_x_3_);
v___x_22_ = lean_box(0);
v_isShared_23_ = v_isSharedCheck_33_;
goto v_resetjp_21_;
}
v_resetjp_21_:
{
uint8_t v___x_24_; 
v___x_24_ = lean_unbox(v_snd_20_);
lean_dec(v_snd_20_);
if (v___x_24_ == 0)
{
lean_object* v___x_26_; 
lean_inc(v_fst_4_);
if (v_isShared_23_ == 0)
{
lean_ctor_set(v___x_22_, 1, v_fst_4_);
v___x_26_ = v___x_22_;
goto v_reusejp_25_;
}
else
{
lean_object* v_reuseFailAlloc_27_; 
v_reuseFailAlloc_27_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_27_, 0, v_fst_4_);
lean_ctor_set(v_reuseFailAlloc_27_, 1, v_fst_4_);
v___x_26_ = v_reuseFailAlloc_27_;
goto v_reusejp_25_;
}
v_reusejp_25_:
{
return v___x_26_;
}
}
else
{
uint8_t v___x_28_; lean_object* v___x_29_; lean_object* v___x_31_; 
v___x_28_ = 0;
v___x_29_ = lean_box(v___x_28_);
if (v_isShared_23_ == 0)
{
lean_ctor_set(v___x_22_, 1, v___x_29_);
v___x_31_ = v___x_22_;
goto v_reusejp_30_;
}
else
{
lean_object* v_reuseFailAlloc_32_; 
v_reuseFailAlloc_32_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_32_, 0, v_fst_4_);
lean_ctor_set(v_reuseFailAlloc_32_, 1, v___x_29_);
v___x_31_ = v_reuseFailAlloc_32_;
goto v_reusejp_30_;
}
v_reusejp_30_:
{
return v___x_31_;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilOf___boxed(lean_object* v_flipF_35_, lean_object* v_flipT_36_, lean_object* v_x_37_){
_start:
{
uint8_t v_flipF_boxed_38_; uint8_t v_flipT_boxed_39_; lean_object* v_res_40_; 
v_flipF_boxed_38_ = lean_unbox(v_flipF_35_);
v_flipT_boxed_39_ = lean_unbox(v_flipT_36_);
v_res_40_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilOf(v_flipF_boxed_38_, v_flipT_boxed_39_, v_x_37_);
return v_res_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(uint8_t v_flipF_41_, uint8_t v_flipT_42_){
_start:
{
lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___x_45_; lean_object* v___x_46_; 
v___x_43_ = lean_box(v_flipF_41_);
v___x_44_ = lean_box(v_flipT_42_);
v___x_45_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilOf___boxed), 3, 2);
lean_closure_set(v___x_45_, 0, v___x_43_);
lean_closure_set(v___x_45_, 1, v___x_44_);
lean_inc_ref(v___x_45_);
v___x_46_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_46_, 0, v___x_45_);
lean_ctor_set(v___x_46_, 1, v___x_45_);
return v___x_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips___boxed(lean_object* v_flipF_47_, lean_object* v_flipT_48_){
_start:
{
uint8_t v_flipF_boxed_49_; uint8_t v_flipT_boxed_50_; lean_object* v_res_51_; 
v_flipF_boxed_49_ = lean_unbox(v_flipF_47_);
v_flipT_boxed_50_ = lean_unbox(v_flipT_48_);
v_res_51_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(v_flipF_boxed_49_, v_flipT_boxed_50_);
return v_res_51_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF___closed__0(void){
_start:
{
uint8_t v___x_52_; lean_object* v___x_53_; 
v___x_52_ = 0;
v___x_53_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(v___x_52_, v___x_52_);
return v___x_53_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF(void){
_start:
{
lean_object* v___x_54_; 
v___x_54_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF___closed__0);
return v___x_54_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT___closed__0(void){
_start:
{
uint8_t v___x_55_; uint8_t v___x_56_; lean_object* v___x_57_; 
v___x_55_ = 1;
v___x_56_ = 0;
v___x_57_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(v___x_56_, v___x_55_);
return v___x_57_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT(void){
_start:
{
lean_object* v___x_58_; 
v___x_58_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT___closed__0);
return v___x_58_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF___closed__0(void){
_start:
{
uint8_t v___x_59_; uint8_t v___x_60_; lean_object* v___x_61_; 
v___x_59_ = 0;
v___x_60_ = 1;
v___x_61_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(v___x_60_, v___x_59_);
return v___x_61_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF(void){
_start:
{
lean_object* v___x_62_; 
v___x_62_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF___closed__0);
return v___x_62_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT___closed__0(void){
_start:
{
uint8_t v___x_63_; lean_object* v___x_64_; 
v___x_63_ = 1;
v___x_64_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_ofFlips(v___x_63_, v___x_63_);
return v___x_64_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT(void){
_start:
{
lean_object* v___x_65_; 
v___x_65_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT___closed__0);
return v___x_65_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015DilationCount_0__FableHilbertWalk20260819_H015DilationCount_dilOf_match__1_splitter___redArg(lean_object* v_x_66_, lean_object* v_h__1_67_, lean_object* v_h__2_68_){
_start:
{
lean_object* v_fst_69_; uint8_t v___x_70_; 
v_fst_69_ = lean_ctor_get(v_x_66_, 0);
v___x_70_ = lean_unbox(v_fst_69_);
if (v___x_70_ == 0)
{
lean_object* v_snd_71_; lean_object* v___x_72_; 
lean_dec(v_h__2_68_);
v_snd_71_ = lean_ctor_get(v_x_66_, 1);
lean_inc(v_snd_71_);
lean_dec_ref(v_x_66_);
v___x_72_ = lean_apply_1(v_h__1_67_, v_snd_71_);
return v___x_72_;
}
else
{
lean_object* v_snd_73_; lean_object* v___x_74_; 
lean_dec(v_h__1_67_);
v_snd_73_ = lean_ctor_get(v_x_66_, 1);
lean_inc(v_snd_73_);
lean_dec_ref(v_x_66_);
v___x_74_ = lean_apply_1(v_h__2_68_, v_snd_73_);
return v___x_74_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015DilationCount_0__FableHilbertWalk20260819_H015DilationCount_dilOf_match__1_splitter(lean_object* v_motive_75_, lean_object* v_x_76_, lean_object* v_h__1_77_, lean_object* v_h__2_78_){
_start:
{
lean_object* v_fst_79_; uint8_t v___x_80_; 
v_fst_79_ = lean_ctor_get(v_x_76_, 0);
v___x_80_ = lean_unbox(v_fst_79_);
if (v___x_80_ == 0)
{
lean_object* v_snd_81_; lean_object* v___x_82_; 
lean_dec(v_h__2_78_);
v_snd_81_ = lean_ctor_get(v_x_76_, 1);
lean_inc(v_snd_81_);
lean_dec_ref(v_x_76_);
v___x_82_ = lean_apply_1(v_h__1_77_, v_snd_81_);
return v___x_82_;
}
else
{
lean_object* v_snd_83_; lean_object* v___x_84_; 
lean_dec(v_h__1_77_);
v_snd_83_ = lean_ctor_get(v_x_76_, 1);
lean_inc(v_snd_83_);
lean_dec_ref(v_x_76_);
v___x_84_ = lean_apply_1(v_h__2_78_, v_snd_83_);
return v___x_84_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H015IrreversibleFork(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H015DilationCount(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H015IrreversibleFork(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFF);
lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilFT);
lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTF);
lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015DilationCount_dilTT);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
