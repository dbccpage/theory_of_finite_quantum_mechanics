// Lean compiler output
// Module: H015CollapseDilations
// Imports: public import Init public meta import Init public import HWKernel public import H003ReversibilityGate
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
LEAN_EXPORT uint8_t lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_prepared;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colOf(uint8_t, uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colOf___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colInv(uint8_t, uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colInv___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF;
static lean_once_cell_t lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT;
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static uint8_t _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_prepared(void){
_start:
{
uint8_t v___x_1_; 
v___x_1_ = 0;
return v___x_1_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colOf(uint8_t v_swapP_2_, uint8_t v_swapU_3_, lean_object* v_x_4_){
_start:
{
lean_object* v_fst_5_; uint8_t v___x_6_; 
v_fst_5_ = lean_ctor_get(v_x_4_, 0);
v___x_6_ = lean_unbox(v_fst_5_);
if (v___x_6_ == 0)
{
lean_object* v_snd_7_; lean_object* v___x_9_; uint8_t v_isShared_10_; uint8_t v_isSharedCheck_20_; 
v_snd_7_ = lean_ctor_get(v_x_4_, 1);
v_isSharedCheck_20_ = !lean_is_exclusive(v_x_4_);
if (v_isSharedCheck_20_ == 0)
{
lean_object* v_unused_21_; 
v_unused_21_ = lean_ctor_get(v_x_4_, 0);
lean_dec(v_unused_21_);
v___x_9_ = v_x_4_;
v_isShared_10_ = v_isSharedCheck_20_;
goto v_resetjp_8_;
}
else
{
lean_inc(v_snd_7_);
lean_dec(v_x_4_);
v___x_9_ = lean_box(0);
v_isShared_10_ = v_isSharedCheck_20_;
goto v_resetjp_8_;
}
v_resetjp_8_:
{
uint8_t v___x_11_; 
v___x_11_ = lean_unbox(v_snd_7_);
if (v___x_11_ == 0)
{
lean_object* v___x_12_; lean_object* v___x_14_; 
v___x_12_ = lean_box(v_swapP_2_);
if (v_isShared_10_ == 0)
{
lean_ctor_set(v___x_9_, 1, v___x_12_);
lean_ctor_set(v___x_9_, 0, v_snd_7_);
v___x_14_ = v___x_9_;
goto v_reusejp_13_;
}
else
{
lean_object* v_reuseFailAlloc_15_; 
v_reuseFailAlloc_15_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_15_, 0, v_snd_7_);
lean_ctor_set(v_reuseFailAlloc_15_, 1, v___x_12_);
v___x_14_ = v_reuseFailAlloc_15_;
goto v_reusejp_13_;
}
v_reusejp_13_:
{
return v___x_14_;
}
}
else
{
lean_object* v___x_16_; lean_object* v___x_18_; 
v___x_16_ = lean_box(v_swapU_3_);
if (v_isShared_10_ == 0)
{
lean_ctor_set(v___x_9_, 1, v___x_16_);
lean_ctor_set(v___x_9_, 0, v_snd_7_);
v___x_18_ = v___x_9_;
goto v_reusejp_17_;
}
else
{
lean_object* v_reuseFailAlloc_19_; 
v_reuseFailAlloc_19_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_19_, 0, v_snd_7_);
lean_ctor_set(v_reuseFailAlloc_19_, 1, v___x_16_);
v___x_18_ = v_reuseFailAlloc_19_;
goto v_reusejp_17_;
}
v_reusejp_17_:
{
return v___x_18_;
}
}
}
}
else
{
lean_object* v_snd_22_; lean_object* v___x_24_; uint8_t v_isShared_25_; uint8_t v_isSharedCheck_41_; 
lean_inc(v_fst_5_);
v_snd_22_ = lean_ctor_get(v_x_4_, 1);
v_isSharedCheck_41_ = !lean_is_exclusive(v_x_4_);
if (v_isSharedCheck_41_ == 0)
{
lean_object* v_unused_42_; 
v_unused_42_ = lean_ctor_get(v_x_4_, 0);
lean_dec(v_unused_42_);
v___x_24_ = v_x_4_;
v_isShared_25_ = v_isSharedCheck_41_;
goto v_resetjp_23_;
}
else
{
lean_inc(v_snd_22_);
lean_dec(v_x_4_);
v___x_24_ = lean_box(0);
v_isShared_25_ = v_isSharedCheck_41_;
goto v_resetjp_23_;
}
v_resetjp_23_:
{
uint8_t v___x_26_; 
v___x_26_ = lean_unbox(v_snd_22_);
if (v___x_26_ == 0)
{
if (v_swapP_2_ == 0)
{
lean_object* v___x_28_; 
if (v_isShared_25_ == 0)
{
lean_ctor_set(v___x_24_, 1, v_fst_5_);
lean_ctor_set(v___x_24_, 0, v_snd_22_);
v___x_28_ = v___x_24_;
goto v_reusejp_27_;
}
else
{
lean_object* v_reuseFailAlloc_29_; 
v_reuseFailAlloc_29_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_29_, 0, v_snd_22_);
lean_ctor_set(v_reuseFailAlloc_29_, 1, v_fst_5_);
v___x_28_ = v_reuseFailAlloc_29_;
goto v_reusejp_27_;
}
v_reusejp_27_:
{
return v___x_28_;
}
}
else
{
lean_object* v___x_31_; 
lean_dec(v_fst_5_);
lean_inc(v_snd_22_);
if (v_isShared_25_ == 0)
{
lean_ctor_set(v___x_24_, 0, v_snd_22_);
v___x_31_ = v___x_24_;
goto v_reusejp_30_;
}
else
{
lean_object* v_reuseFailAlloc_32_; 
v_reuseFailAlloc_32_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_32_, 0, v_snd_22_);
lean_ctor_set(v_reuseFailAlloc_32_, 1, v_snd_22_);
v___x_31_ = v_reuseFailAlloc_32_;
goto v_reusejp_30_;
}
v_reusejp_30_:
{
return v___x_31_;
}
}
}
else
{
lean_dec(v_fst_5_);
if (v_swapU_3_ == 0)
{
lean_object* v___x_34_; 
lean_inc(v_snd_22_);
if (v_isShared_25_ == 0)
{
lean_ctor_set(v___x_24_, 0, v_snd_22_);
v___x_34_ = v___x_24_;
goto v_reusejp_33_;
}
else
{
lean_object* v_reuseFailAlloc_35_; 
v_reuseFailAlloc_35_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_35_, 0, v_snd_22_);
lean_ctor_set(v_reuseFailAlloc_35_, 1, v_snd_22_);
v___x_34_ = v_reuseFailAlloc_35_;
goto v_reusejp_33_;
}
v_reusejp_33_:
{
return v___x_34_;
}
}
else
{
uint8_t v___x_36_; lean_object* v___x_37_; lean_object* v___x_39_; 
v___x_36_ = 0;
v___x_37_ = lean_box(v___x_36_);
if (v_isShared_25_ == 0)
{
lean_ctor_set(v___x_24_, 1, v___x_37_);
lean_ctor_set(v___x_24_, 0, v_snd_22_);
v___x_39_ = v___x_24_;
goto v_reusejp_38_;
}
else
{
lean_object* v_reuseFailAlloc_40_; 
v_reuseFailAlloc_40_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_40_, 0, v_snd_22_);
lean_ctor_set(v_reuseFailAlloc_40_, 1, v___x_37_);
v___x_39_ = v_reuseFailAlloc_40_;
goto v_reusejp_38_;
}
v_reusejp_38_:
{
return v___x_39_;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colOf___boxed(lean_object* v_swapP_43_, lean_object* v_swapU_44_, lean_object* v_x_45_){
_start:
{
uint8_t v_swapP_boxed_46_; uint8_t v_swapU_boxed_47_; lean_object* v_res_48_; 
v_swapP_boxed_46_ = lean_unbox(v_swapP_43_);
v_swapU_boxed_47_ = lean_unbox(v_swapU_44_);
v_res_48_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colOf(v_swapP_boxed_46_, v_swapU_boxed_47_, v_x_45_);
return v_res_48_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colInv(uint8_t v_swapP_49_, uint8_t v_swapU_50_, lean_object* v_x_51_){
_start:
{
lean_object* v_fst_52_; uint8_t v___x_53_; 
v_fst_52_ = lean_ctor_get(v_x_51_, 0);
lean_inc(v_fst_52_);
v___x_53_ = lean_unbox(v_fst_52_);
if (v___x_53_ == 0)
{
if (v_swapP_49_ == 0)
{
lean_object* v_snd_54_; lean_object* v___x_56_; uint8_t v_isShared_57_; uint8_t v_isSharedCheck_61_; 
v_snd_54_ = lean_ctor_get(v_x_51_, 1);
v_isSharedCheck_61_ = !lean_is_exclusive(v_x_51_);
if (v_isSharedCheck_61_ == 0)
{
lean_object* v_unused_62_; 
v_unused_62_ = lean_ctor_get(v_x_51_, 0);
lean_dec(v_unused_62_);
v___x_56_ = v_x_51_;
v_isShared_57_ = v_isSharedCheck_61_;
goto v_resetjp_55_;
}
else
{
lean_inc(v_snd_54_);
lean_dec(v_x_51_);
v___x_56_ = lean_box(0);
v_isShared_57_ = v_isSharedCheck_61_;
goto v_resetjp_55_;
}
v_resetjp_55_:
{
lean_object* v___x_59_; 
if (v_isShared_57_ == 0)
{
lean_ctor_set(v___x_56_, 1, v_fst_52_);
lean_ctor_set(v___x_56_, 0, v_snd_54_);
v___x_59_ = v___x_56_;
goto v_reusejp_58_;
}
else
{
lean_object* v_reuseFailAlloc_60_; 
v_reuseFailAlloc_60_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_60_, 0, v_snd_54_);
lean_ctor_set(v_reuseFailAlloc_60_, 1, v_fst_52_);
v___x_59_ = v_reuseFailAlloc_60_;
goto v_reusejp_58_;
}
v_reusejp_58_:
{
return v___x_59_;
}
}
}
else
{
lean_object* v_snd_63_; lean_object* v___x_65_; uint8_t v_isShared_66_; uint8_t v_isSharedCheck_75_; 
v_snd_63_ = lean_ctor_get(v_x_51_, 1);
v_isSharedCheck_75_ = !lean_is_exclusive(v_x_51_);
if (v_isSharedCheck_75_ == 0)
{
lean_object* v_unused_76_; 
v_unused_76_ = lean_ctor_get(v_x_51_, 0);
lean_dec(v_unused_76_);
v___x_65_ = v_x_51_;
v_isShared_66_ = v_isSharedCheck_75_;
goto v_resetjp_64_;
}
else
{
lean_inc(v_snd_63_);
lean_dec(v_x_51_);
v___x_65_ = lean_box(0);
v_isShared_66_ = v_isSharedCheck_75_;
goto v_resetjp_64_;
}
v_resetjp_64_:
{
uint8_t v___x_67_; 
v___x_67_ = lean_unbox(v_snd_63_);
lean_dec(v_snd_63_);
if (v___x_67_ == 0)
{
lean_object* v___x_68_; lean_object* v___x_70_; 
v___x_68_ = lean_box(v_swapP_49_);
if (v_isShared_66_ == 0)
{
lean_ctor_set(v___x_65_, 1, v_fst_52_);
lean_ctor_set(v___x_65_, 0, v___x_68_);
v___x_70_ = v___x_65_;
goto v_reusejp_69_;
}
else
{
lean_object* v_reuseFailAlloc_71_; 
v_reuseFailAlloc_71_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_71_, 0, v___x_68_);
lean_ctor_set(v_reuseFailAlloc_71_, 1, v_fst_52_);
v___x_70_ = v_reuseFailAlloc_71_;
goto v_reusejp_69_;
}
v_reusejp_69_:
{
return v___x_70_;
}
}
else
{
lean_object* v___x_73_; 
lean_inc(v_fst_52_);
if (v_isShared_66_ == 0)
{
lean_ctor_set(v___x_65_, 1, v_fst_52_);
v___x_73_ = v___x_65_;
goto v_reusejp_72_;
}
else
{
lean_object* v_reuseFailAlloc_74_; 
v_reuseFailAlloc_74_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_74_, 0, v_fst_52_);
lean_ctor_set(v_reuseFailAlloc_74_, 1, v_fst_52_);
v___x_73_ = v_reuseFailAlloc_74_;
goto v_reusejp_72_;
}
v_reusejp_72_:
{
return v___x_73_;
}
}
}
}
}
else
{
if (v_swapU_50_ == 0)
{
lean_object* v_snd_77_; lean_object* v___x_79_; uint8_t v_isShared_80_; uint8_t v_isSharedCheck_84_; 
v_snd_77_ = lean_ctor_get(v_x_51_, 1);
v_isSharedCheck_84_ = !lean_is_exclusive(v_x_51_);
if (v_isSharedCheck_84_ == 0)
{
lean_object* v_unused_85_; 
v_unused_85_ = lean_ctor_get(v_x_51_, 0);
lean_dec(v_unused_85_);
v___x_79_ = v_x_51_;
v_isShared_80_ = v_isSharedCheck_84_;
goto v_resetjp_78_;
}
else
{
lean_inc(v_snd_77_);
lean_dec(v_x_51_);
v___x_79_ = lean_box(0);
v_isShared_80_ = v_isSharedCheck_84_;
goto v_resetjp_78_;
}
v_resetjp_78_:
{
lean_object* v___x_82_; 
if (v_isShared_80_ == 0)
{
lean_ctor_set(v___x_79_, 1, v_fst_52_);
lean_ctor_set(v___x_79_, 0, v_snd_77_);
v___x_82_ = v___x_79_;
goto v_reusejp_81_;
}
else
{
lean_object* v_reuseFailAlloc_83_; 
v_reuseFailAlloc_83_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_83_, 0, v_snd_77_);
lean_ctor_set(v_reuseFailAlloc_83_, 1, v_fst_52_);
v___x_82_ = v_reuseFailAlloc_83_;
goto v_reusejp_81_;
}
v_reusejp_81_:
{
return v___x_82_;
}
}
}
else
{
lean_object* v_snd_86_; lean_object* v___x_88_; uint8_t v_isShared_89_; uint8_t v_isSharedCheck_99_; 
v_snd_86_ = lean_ctor_get(v_x_51_, 1);
v_isSharedCheck_99_ = !lean_is_exclusive(v_x_51_);
if (v_isSharedCheck_99_ == 0)
{
lean_object* v_unused_100_; 
v_unused_100_ = lean_ctor_get(v_x_51_, 0);
lean_dec(v_unused_100_);
v___x_88_ = v_x_51_;
v_isShared_89_ = v_isSharedCheck_99_;
goto v_resetjp_87_;
}
else
{
lean_inc(v_snd_86_);
lean_dec(v_x_51_);
v___x_88_ = lean_box(0);
v_isShared_89_ = v_isSharedCheck_99_;
goto v_resetjp_87_;
}
v_resetjp_87_:
{
uint8_t v___x_90_; 
v___x_90_ = lean_unbox(v_snd_86_);
lean_dec(v_snd_86_);
if (v___x_90_ == 0)
{
lean_object* v___x_92_; 
lean_inc(v_fst_52_);
if (v_isShared_89_ == 0)
{
lean_ctor_set(v___x_88_, 1, v_fst_52_);
v___x_92_ = v___x_88_;
goto v_reusejp_91_;
}
else
{
lean_object* v_reuseFailAlloc_93_; 
v_reuseFailAlloc_93_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_93_, 0, v_fst_52_);
lean_ctor_set(v_reuseFailAlloc_93_, 1, v_fst_52_);
v___x_92_ = v_reuseFailAlloc_93_;
goto v_reusejp_91_;
}
v_reusejp_91_:
{
return v___x_92_;
}
}
else
{
uint8_t v___x_94_; lean_object* v___x_95_; lean_object* v___x_97_; 
v___x_94_ = 0;
v___x_95_ = lean_box(v___x_94_);
if (v_isShared_89_ == 0)
{
lean_ctor_set(v___x_88_, 1, v_fst_52_);
lean_ctor_set(v___x_88_, 0, v___x_95_);
v___x_97_ = v___x_88_;
goto v_reusejp_96_;
}
else
{
lean_object* v_reuseFailAlloc_98_; 
v_reuseFailAlloc_98_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_98_, 0, v___x_95_);
lean_ctor_set(v_reuseFailAlloc_98_, 1, v_fst_52_);
v___x_97_ = v_reuseFailAlloc_98_;
goto v_reusejp_96_;
}
v_reusejp_96_:
{
return v___x_97_;
}
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colInv___boxed(lean_object* v_swapP_101_, lean_object* v_swapU_102_, lean_object* v_x_103_){
_start:
{
uint8_t v_swapP_boxed_104_; uint8_t v_swapU_boxed_105_; lean_object* v_res_106_; 
v_swapP_boxed_104_ = lean_unbox(v_swapP_101_);
v_swapU_boxed_105_ = lean_unbox(v_swapU_102_);
v_res_106_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colInv(v_swapP_boxed_104_, v_swapU_boxed_105_, v_x_103_);
return v_res_106_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(uint8_t v_swapP_107_, uint8_t v_swapU_108_){
_start:
{
lean_object* v___x_109_; lean_object* v___x_110_; lean_object* v___x_111_; lean_object* v___x_112_; lean_object* v___x_113_; lean_object* v___x_114_; lean_object* v___x_115_; 
v___x_109_ = lean_box(v_swapP_107_);
v___x_110_ = lean_box(v_swapU_108_);
v___x_111_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colOf___boxed), 3, 2);
lean_closure_set(v___x_111_, 0, v___x_109_);
lean_closure_set(v___x_111_, 1, v___x_110_);
v___x_112_ = lean_box(v_swapP_107_);
v___x_113_ = lean_box(v_swapU_108_);
v___x_114_ = lean_alloc_closure((void*)(lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_colInv___boxed), 3, 2);
lean_closure_set(v___x_114_, 0, v___x_112_);
lean_closure_set(v___x_114_, 1, v___x_113_);
v___x_115_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_115_, 0, v___x_111_);
lean_ctor_set(v___x_115_, 1, v___x_114_);
return v___x_115_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps___boxed(lean_object* v_swapP_116_, lean_object* v_swapU_117_){
_start:
{
uint8_t v_swapP_boxed_118_; uint8_t v_swapU_boxed_119_; lean_object* v_res_120_; 
v_swapP_boxed_118_ = lean_unbox(v_swapP_116_);
v_swapU_boxed_119_ = lean_unbox(v_swapU_117_);
v_res_120_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(v_swapP_boxed_118_, v_swapU_boxed_119_);
return v_res_120_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF___closed__0(void){
_start:
{
uint8_t v___x_121_; lean_object* v___x_122_; 
v___x_121_ = 0;
v___x_122_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(v___x_121_, v___x_121_);
return v___x_122_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF(void){
_start:
{
lean_object* v___x_123_; 
v___x_123_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF___closed__0);
return v___x_123_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT___closed__0(void){
_start:
{
uint8_t v___x_124_; uint8_t v___x_125_; lean_object* v___x_126_; 
v___x_124_ = 1;
v___x_125_ = 0;
v___x_126_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(v___x_125_, v___x_124_);
return v___x_126_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT(void){
_start:
{
lean_object* v___x_127_; 
v___x_127_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT___closed__0);
return v___x_127_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF___closed__0(void){
_start:
{
uint8_t v___x_128_; uint8_t v___x_129_; lean_object* v___x_130_; 
v___x_128_ = 0;
v___x_129_ = 1;
v___x_130_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(v___x_129_, v___x_128_);
return v___x_130_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF(void){
_start:
{
lean_object* v___x_131_; 
v___x_131_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF___closed__0);
return v___x_131_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT___closed__0(void){
_start:
{
uint8_t v___x_132_; lean_object* v___x_133_; 
v___x_132_ = 1;
v___x_133_ = lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_ofSwaps(v___x_132_, v___x_132_);
return v___x_133_;
}
}
static lean_object* _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT(void){
_start:
{
lean_object* v___x_134_; 
v___x_134_ = lean_obj_once(&lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT___closed__0, &lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT___closed__0_once, _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT___closed__0);
return v___x_134_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___redArg(lean_object* v_x_135_, lean_object* v_h__1_136_, lean_object* v_h__2_137_, lean_object* v_h__3_138_, lean_object* v_h__4_139_){
_start:
{
lean_object* v_fst_140_; uint8_t v___x_141_; 
v_fst_140_ = lean_ctor_get(v_x_135_, 0);
v___x_141_ = lean_unbox(v_fst_140_);
if (v___x_141_ == 0)
{
lean_object* v_snd_142_; uint8_t v___x_143_; 
lean_dec(v_h__4_139_);
lean_dec(v_h__2_137_);
v_snd_142_ = lean_ctor_get(v_x_135_, 1);
v___x_143_ = lean_unbox(v_snd_142_);
if (v___x_143_ == 0)
{
lean_object* v___x_144_; lean_object* v___x_145_; 
lean_dec(v_h__3_138_);
v___x_144_ = lean_box(0);
v___x_145_ = lean_apply_1(v_h__1_136_, v___x_144_);
return v___x_145_;
}
else
{
lean_object* v___x_146_; lean_object* v___x_147_; 
lean_dec(v_h__1_136_);
v___x_146_ = lean_box(0);
v___x_147_ = lean_apply_1(v_h__3_138_, v___x_146_);
return v___x_147_;
}
}
else
{
lean_object* v_snd_148_; uint8_t v___x_149_; 
lean_dec(v_h__3_138_);
lean_dec(v_h__1_136_);
v_snd_148_ = lean_ctor_get(v_x_135_, 1);
v___x_149_ = lean_unbox(v_snd_148_);
if (v___x_149_ == 0)
{
lean_object* v___x_150_; lean_object* v___x_151_; 
lean_dec(v_h__4_139_);
v___x_150_ = lean_box(0);
v___x_151_ = lean_apply_1(v_h__2_137_, v___x_150_);
return v___x_151_;
}
else
{
lean_object* v___x_152_; lean_object* v___x_153_; 
lean_dec(v_h__2_137_);
v___x_152_ = lean_box(0);
v___x_153_ = lean_apply_1(v_h__4_139_, v___x_152_);
return v___x_153_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___redArg___boxed(lean_object* v_x_154_, lean_object* v_h__1_155_, lean_object* v_h__2_156_, lean_object* v_h__3_157_, lean_object* v_h__4_158_){
_start:
{
lean_object* v_res_159_; 
v_res_159_ = lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___redArg(v_x_154_, v_h__1_155_, v_h__2_156_, v_h__3_157_, v_h__4_158_);
lean_dec_ref(v_x_154_);
return v_res_159_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter(lean_object* v_motive_160_, lean_object* v_x_161_, lean_object* v_h__1_162_, lean_object* v_h__2_163_, lean_object* v_h__3_164_, lean_object* v_h__4_165_){
_start:
{
lean_object* v_fst_166_; uint8_t v___x_167_; 
v_fst_166_ = lean_ctor_get(v_x_161_, 0);
v___x_167_ = lean_unbox(v_fst_166_);
if (v___x_167_ == 0)
{
lean_object* v_snd_168_; uint8_t v___x_169_; 
lean_dec(v_h__4_165_);
lean_dec(v_h__2_163_);
v_snd_168_ = lean_ctor_get(v_x_161_, 1);
v___x_169_ = lean_unbox(v_snd_168_);
if (v___x_169_ == 0)
{
lean_object* v___x_170_; lean_object* v___x_171_; 
lean_dec(v_h__3_164_);
v___x_170_ = lean_box(0);
v___x_171_ = lean_apply_1(v_h__1_162_, v___x_170_);
return v___x_171_;
}
else
{
lean_object* v___x_172_; lean_object* v___x_173_; 
lean_dec(v_h__1_162_);
v___x_172_ = lean_box(0);
v___x_173_ = lean_apply_1(v_h__3_164_, v___x_172_);
return v___x_173_;
}
}
else
{
lean_object* v_snd_174_; uint8_t v___x_175_; 
lean_dec(v_h__3_164_);
lean_dec(v_h__1_162_);
v_snd_174_ = lean_ctor_get(v_x_161_, 1);
v___x_175_ = lean_unbox(v_snd_174_);
if (v___x_175_ == 0)
{
lean_object* v___x_176_; lean_object* v___x_177_; 
lean_dec(v_h__4_165_);
v___x_176_ = lean_box(0);
v___x_177_ = lean_apply_1(v_h__2_163_, v___x_176_);
return v___x_177_;
}
else
{
lean_object* v___x_178_; lean_object* v___x_179_; 
lean_dec(v_h__2_163_);
v___x_178_ = lean_box(0);
v___x_179_ = lean_apply_1(v_h__4_165_, v___x_178_);
return v___x_179_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter___boxed(lean_object* v_motive_180_, lean_object* v_x_181_, lean_object* v_h__1_182_, lean_object* v_h__2_183_, lean_object* v_h__3_184_, lean_object* v_h__4_185_){
_start:
{
lean_object* v_res_186_; 
v_res_186_ = lp_FiniteQuantum___private_H015CollapseDilations_0__FableHilbertWalk20260819_H015CollapseDilations_colOf_match__1_splitter(v_motive_180_, v_x_181_, v_h__1_182_, v_h__2_183_, v_h__3_184_, v_h__4_185_);
lean_dec_ref(v_x_181_);
return v_res_186_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_FiniteQuantum_HWKernel(uint8_t builtin);
lean_object* initialize_FiniteQuantum_H003ReversibilityGate(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_H015CollapseDilations(uint8_t builtin) {
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
res = initialize_FiniteQuantum_H003ReversibilityGate(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_prepared = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_prepared();
lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFF);
lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dFT);
lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTF);
lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT = _init_lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT();
lean_mark_persistent(lp_FiniteQuantum_FableHilbertWalk20260819_H015CollapseDilations_dTT);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
