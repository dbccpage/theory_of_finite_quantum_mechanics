// Lean compiler output
// Module: WorldRebitHiddenDirection
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
lean_object* lean_int_neg(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_toCtorIdx(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqQ9AuthorityEffect(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqQ9AuthorityEffect___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqRebitCoord(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqRebitCoord___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqJointCoord(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqJointCoord___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqLocalSymBasis(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqLocalSymBasis___boxed(lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord___boxed(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry(uint8_t, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productEntry(uint8_t, uint8_t, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productEntry___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productMatrixEntry(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productMatrixEntry___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(lean_object*, lean_object*, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_frobeniusInner(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_matrixMulEntry(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_matrixMulEntry___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pPlusScaled(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pPlusScaled___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pMinusScaled(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pMinusScaled___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoMinusScaled(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoMinusScaled___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_trace4(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___redArg(uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter(lean_object*, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_toCtorIdx(lean_object* v_x_1_){
_start:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_ofNat(lean_object* v_n_3_){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = lean_box(0);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_ofNat___boxed(lean_object* v_n_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_Q9AuthorityEffect_ofNat(v_n_5_);
lean_dec(v_n_5_);
return v_res_6_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqQ9AuthorityEffect(lean_object* v_x_7_, lean_object* v_y_8_){
_start:
{
uint8_t v___x_9_; 
v___x_9_ = 1;
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqQ9AuthorityEffect___boxed(lean_object* v_x_10_, lean_object* v_y_11_){
_start:
{
uint8_t v_res_12_; lean_object* v_r_13_; 
v_res_12_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqQ9AuthorityEffect(v_x_10_, v_y_11_);
v_r_13_ = lean_box(v_res_12_);
return v_r_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx(uint8_t v_x_14_){
_start:
{
if (v_x_14_ == 0)
{
lean_object* v___x_15_; 
v___x_15_ = lean_unsigned_to_nat(0u);
return v___x_15_;
}
else
{
lean_object* v___x_16_; 
v___x_16_ = lean_unsigned_to_nat(1u);
return v___x_16_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx___boxed(lean_object* v_x_17_){
_start:
{
uint8_t v_x_boxed_18_; lean_object* v_res_19_; 
v_x_boxed_18_ = lean_unbox(v_x_17_);
v_res_19_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx(v_x_boxed_18_);
return v_res_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_toCtorIdx(uint8_t v_x_20_){
_start:
{
lean_object* v___x_21_; 
v___x_21_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx(v_x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_toCtorIdx___boxed(lean_object* v_x_22_){
_start:
{
uint8_t v_x_4__boxed_23_; lean_object* v_res_24_; 
v_x_4__boxed_23_ = lean_unbox(v_x_22_);
v_res_24_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_toCtorIdx(v_x_4__boxed_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___redArg(lean_object* v_k_25_){
_start:
{
lean_inc(v_k_25_);
return v_k_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___redArg___boxed(lean_object* v_k_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___redArg(v_k_26_);
lean_dec(v_k_26_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim(lean_object* v_motive_28_, lean_object* v_ctorIdx_29_, uint8_t v_t_30_, lean_object* v_h_31_, lean_object* v_k_32_){
_start:
{
lean_inc(v_k_32_);
return v_k_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim___boxed(lean_object* v_motive_33_, lean_object* v_ctorIdx_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_k_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorElim(v_motive_33_, v_ctorIdx_34_, v_t_boxed_38_, v_h_36_, v_k_37_);
lean_dec(v_k_37_);
lean_dec(v_ctorIdx_34_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___redArg(lean_object* v_zero_40_){
_start:
{
lean_inc(v_zero_40_);
return v_zero_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___redArg___boxed(lean_object* v_zero_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___redArg(v_zero_41_);
lean_dec(v_zero_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_zero_46_){
_start:
{
lean_inc(v_zero_46_);
return v_zero_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_zero_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_zero_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_zero_50_);
lean_dec(v_zero_50_);
return v_res_52_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___redArg(lean_object* v_one_53_){
_start:
{
lean_inc(v_one_53_);
return v_one_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___redArg___boxed(lean_object* v_one_54_){
_start:
{
lean_object* v_res_55_; 
v_res_55_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___redArg(v_one_54_);
lean_dec(v_one_54_);
return v_res_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim(lean_object* v_motive_56_, uint8_t v_t_57_, lean_object* v_h_58_, lean_object* v_one_59_){
_start:
{
lean_inc(v_one_59_);
return v_one_59_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim___boxed(lean_object* v_motive_60_, lean_object* v_t_61_, lean_object* v_h_62_, lean_object* v_one_63_){
_start:
{
uint8_t v_t_boxed_64_; lean_object* v_res_65_; 
v_t_boxed_64_ = lean_unbox(v_t_61_);
v_res_65_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_one_elim(v_motive_60_, v_t_boxed_64_, v_h_62_, v_one_63_);
lean_dec(v_one_63_);
return v_res_65_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ofNat(lean_object* v_n_66_){
_start:
{
lean_object* v___x_67_; uint8_t v___x_68_; 
v___x_67_ = lean_unsigned_to_nat(0u);
v___x_68_ = lean_nat_dec_le(v_n_66_, v___x_67_);
if (v___x_68_ == 0)
{
uint8_t v___x_69_; 
v___x_69_ = 1;
return v___x_69_;
}
else
{
uint8_t v___x_70_; 
v___x_70_ = 0;
return v___x_70_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ofNat___boxed(lean_object* v_n_71_){
_start:
{
uint8_t v_res_72_; lean_object* v_r_73_; 
v_res_72_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ofNat(v_n_71_);
lean_dec(v_n_71_);
v_r_73_ = lean_box(v_res_72_);
return v_r_73_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqRebitCoord(uint8_t v_x_74_, uint8_t v_y_75_){
_start:
{
lean_object* v___x_76_; lean_object* v___x_77_; uint8_t v___x_78_; 
v___x_76_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx(v_x_74_);
v___x_77_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_RebitCoord_ctorIdx(v_y_75_);
v___x_78_ = lean_nat_dec_eq(v___x_76_, v___x_77_);
lean_dec(v___x_77_);
lean_dec(v___x_76_);
return v___x_78_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqRebitCoord___boxed(lean_object* v_x_79_, lean_object* v_y_80_){
_start:
{
uint8_t v_x_13__boxed_81_; uint8_t v_y_14__boxed_82_; uint8_t v_res_83_; lean_object* v_r_84_; 
v_x_13__boxed_81_ = lean_unbox(v_x_79_);
v_y_14__boxed_82_ = lean_unbox(v_y_80_);
v_res_83_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqRebitCoord(v_x_13__boxed_81_, v_y_14__boxed_82_);
v_r_84_ = lean_box(v_res_83_);
return v_r_84_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx(uint8_t v_x_85_){
_start:
{
switch(v_x_85_)
{
case 0:
{
lean_object* v___x_86_; 
v___x_86_ = lean_unsigned_to_nat(0u);
return v___x_86_;
}
case 1:
{
lean_object* v___x_87_; 
v___x_87_ = lean_unsigned_to_nat(1u);
return v___x_87_;
}
case 2:
{
lean_object* v___x_88_; 
v___x_88_ = lean_unsigned_to_nat(2u);
return v___x_88_;
}
default: 
{
lean_object* v___x_89_; 
v___x_89_ = lean_unsigned_to_nat(3u);
return v___x_89_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx___boxed(lean_object* v_x_90_){
_start:
{
uint8_t v_x_boxed_91_; lean_object* v_res_92_; 
v_x_boxed_91_ = lean_unbox(v_x_90_);
v_res_92_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx(v_x_boxed_91_);
return v_res_92_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_toCtorIdx(uint8_t v_x_93_){
_start:
{
lean_object* v___x_94_; 
v___x_94_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx(v_x_93_);
return v___x_94_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_toCtorIdx___boxed(lean_object* v_x_95_){
_start:
{
uint8_t v_x_4__boxed_96_; lean_object* v_res_97_; 
v_x_4__boxed_96_ = lean_unbox(v_x_95_);
v_res_97_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_toCtorIdx(v_x_4__boxed_96_);
return v_res_97_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___redArg(lean_object* v_k_98_){
_start:
{
lean_inc(v_k_98_);
return v_k_98_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___redArg___boxed(lean_object* v_k_99_){
_start:
{
lean_object* v_res_100_; 
v_res_100_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___redArg(v_k_99_);
lean_dec(v_k_99_);
return v_res_100_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim(lean_object* v_motive_101_, lean_object* v_ctorIdx_102_, uint8_t v_t_103_, lean_object* v_h_104_, lean_object* v_k_105_){
_start:
{
lean_inc(v_k_105_);
return v_k_105_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim___boxed(lean_object* v_motive_106_, lean_object* v_ctorIdx_107_, lean_object* v_t_108_, lean_object* v_h_109_, lean_object* v_k_110_){
_start:
{
uint8_t v_t_boxed_111_; lean_object* v_res_112_; 
v_t_boxed_111_ = lean_unbox(v_t_108_);
v_res_112_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorElim(v_motive_106_, v_ctorIdx_107_, v_t_boxed_111_, v_h_109_, v_k_110_);
lean_dec(v_k_110_);
lean_dec(v_ctorIdx_107_);
return v_res_112_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___redArg(lean_object* v_zeroZero_113_){
_start:
{
lean_inc(v_zeroZero_113_);
return v_zeroZero_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___redArg___boxed(lean_object* v_zeroZero_114_){
_start:
{
lean_object* v_res_115_; 
v_res_115_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___redArg(v_zeroZero_114_);
lean_dec(v_zeroZero_114_);
return v_res_115_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim(lean_object* v_motive_116_, uint8_t v_t_117_, lean_object* v_h_118_, lean_object* v_zeroZero_119_){
_start:
{
lean_inc(v_zeroZero_119_);
return v_zeroZero_119_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim___boxed(lean_object* v_motive_120_, lean_object* v_t_121_, lean_object* v_h_122_, lean_object* v_zeroZero_123_){
_start:
{
uint8_t v_t_boxed_124_; lean_object* v_res_125_; 
v_t_boxed_124_ = lean_unbox(v_t_121_);
v_res_125_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroZero_elim(v_motive_120_, v_t_boxed_124_, v_h_122_, v_zeroZero_123_);
lean_dec(v_zeroZero_123_);
return v_res_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___redArg(lean_object* v_zeroOne_126_){
_start:
{
lean_inc(v_zeroOne_126_);
return v_zeroOne_126_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___redArg___boxed(lean_object* v_zeroOne_127_){
_start:
{
lean_object* v_res_128_; 
v_res_128_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___redArg(v_zeroOne_127_);
lean_dec(v_zeroOne_127_);
return v_res_128_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim(lean_object* v_motive_129_, uint8_t v_t_130_, lean_object* v_h_131_, lean_object* v_zeroOne_132_){
_start:
{
lean_inc(v_zeroOne_132_);
return v_zeroOne_132_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim___boxed(lean_object* v_motive_133_, lean_object* v_t_134_, lean_object* v_h_135_, lean_object* v_zeroOne_136_){
_start:
{
uint8_t v_t_boxed_137_; lean_object* v_res_138_; 
v_t_boxed_137_ = lean_unbox(v_t_134_);
v_res_138_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_zeroOne_elim(v_motive_133_, v_t_boxed_137_, v_h_135_, v_zeroOne_136_);
lean_dec(v_zeroOne_136_);
return v_res_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___redArg(lean_object* v_oneZero_139_){
_start:
{
lean_inc(v_oneZero_139_);
return v_oneZero_139_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___redArg___boxed(lean_object* v_oneZero_140_){
_start:
{
lean_object* v_res_141_; 
v_res_141_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___redArg(v_oneZero_140_);
lean_dec(v_oneZero_140_);
return v_res_141_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim(lean_object* v_motive_142_, uint8_t v_t_143_, lean_object* v_h_144_, lean_object* v_oneZero_145_){
_start:
{
lean_inc(v_oneZero_145_);
return v_oneZero_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim___boxed(lean_object* v_motive_146_, lean_object* v_t_147_, lean_object* v_h_148_, lean_object* v_oneZero_149_){
_start:
{
uint8_t v_t_boxed_150_; lean_object* v_res_151_; 
v_t_boxed_150_ = lean_unbox(v_t_147_);
v_res_151_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneZero_elim(v_motive_146_, v_t_boxed_150_, v_h_148_, v_oneZero_149_);
lean_dec(v_oneZero_149_);
return v_res_151_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___redArg(lean_object* v_oneOne_152_){
_start:
{
lean_inc(v_oneOne_152_);
return v_oneOne_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___redArg___boxed(lean_object* v_oneOne_153_){
_start:
{
lean_object* v_res_154_; 
v_res_154_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___redArg(v_oneOne_153_);
lean_dec(v_oneOne_153_);
return v_res_154_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim(lean_object* v_motive_155_, uint8_t v_t_156_, lean_object* v_h_157_, lean_object* v_oneOne_158_){
_start:
{
lean_inc(v_oneOne_158_);
return v_oneOne_158_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim___boxed(lean_object* v_motive_159_, lean_object* v_t_160_, lean_object* v_h_161_, lean_object* v_oneOne_162_){
_start:
{
uint8_t v_t_boxed_163_; lean_object* v_res_164_; 
v_t_boxed_163_ = lean_unbox(v_t_160_);
v_res_164_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_oneOne_elim(v_motive_159_, v_t_boxed_163_, v_h_161_, v_oneOne_162_);
lean_dec(v_oneOne_162_);
return v_res_164_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ofNat(lean_object* v_n_165_){
_start:
{
lean_object* v___x_166_; uint8_t v___x_167_; 
v___x_166_ = lean_unsigned_to_nat(1u);
v___x_167_ = lean_nat_dec_le(v_n_165_, v___x_166_);
if (v___x_167_ == 0)
{
lean_object* v___x_168_; uint8_t v___x_169_; 
v___x_168_ = lean_unsigned_to_nat(2u);
v___x_169_ = lean_nat_dec_le(v_n_165_, v___x_168_);
if (v___x_169_ == 0)
{
uint8_t v___x_170_; 
v___x_170_ = 3;
return v___x_170_;
}
else
{
uint8_t v___x_171_; 
v___x_171_ = 2;
return v___x_171_;
}
}
else
{
lean_object* v___x_172_; uint8_t v___x_173_; 
v___x_172_ = lean_unsigned_to_nat(0u);
v___x_173_ = lean_nat_dec_le(v_n_165_, v___x_172_);
if (v___x_173_ == 0)
{
uint8_t v___x_174_; 
v___x_174_ = 1;
return v___x_174_;
}
else
{
uint8_t v___x_175_; 
v___x_175_ = 0;
return v___x_175_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ofNat___boxed(lean_object* v_n_176_){
_start:
{
uint8_t v_res_177_; lean_object* v_r_178_; 
v_res_177_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ofNat(v_n_176_);
lean_dec(v_n_176_);
v_r_178_ = lean_box(v_res_177_);
return v_r_178_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqJointCoord(uint8_t v_x_179_, uint8_t v_y_180_){
_start:
{
lean_object* v___x_181_; lean_object* v___x_182_; uint8_t v___x_183_; 
v___x_181_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx(v_x_179_);
v___x_182_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_JointCoord_ctorIdx(v_y_180_);
v___x_183_ = lean_nat_dec_eq(v___x_181_, v___x_182_);
lean_dec(v___x_182_);
lean_dec(v___x_181_);
return v___x_183_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqJointCoord___boxed(lean_object* v_x_184_, lean_object* v_y_185_){
_start:
{
uint8_t v_x_13__boxed_186_; uint8_t v_y_14__boxed_187_; uint8_t v_res_188_; lean_object* v_r_189_; 
v_x_13__boxed_186_ = lean_unbox(v_x_184_);
v_y_14__boxed_187_ = lean_unbox(v_y_185_);
v_res_188_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqJointCoord(v_x_13__boxed_186_, v_y_14__boxed_187_);
v_r_189_ = lean_box(v_res_188_);
return v_r_189_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx(uint8_t v_x_190_){
_start:
{
switch(v_x_190_)
{
case 0:
{
lean_object* v___x_191_; 
v___x_191_ = lean_unsigned_to_nat(0u);
return v___x_191_;
}
case 1:
{
lean_object* v___x_192_; 
v___x_192_ = lean_unsigned_to_nat(1u);
return v___x_192_;
}
default: 
{
lean_object* v___x_193_; 
v___x_193_ = lean_unsigned_to_nat(2u);
return v___x_193_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx___boxed(lean_object* v_x_194_){
_start:
{
uint8_t v_x_boxed_195_; lean_object* v_res_196_; 
v_x_boxed_195_ = lean_unbox(v_x_194_);
v_res_196_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx(v_x_boxed_195_);
return v_res_196_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_toCtorIdx(uint8_t v_x_197_){
_start:
{
lean_object* v___x_198_; 
v___x_198_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx(v_x_197_);
return v___x_198_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_toCtorIdx___boxed(lean_object* v_x_199_){
_start:
{
uint8_t v_x_4__boxed_200_; lean_object* v_res_201_; 
v_x_4__boxed_200_ = lean_unbox(v_x_199_);
v_res_201_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_toCtorIdx(v_x_4__boxed_200_);
return v_res_201_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___redArg(lean_object* v_k_202_){
_start:
{
lean_inc(v_k_202_);
return v_k_202_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___redArg___boxed(lean_object* v_k_203_){
_start:
{
lean_object* v_res_204_; 
v_res_204_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___redArg(v_k_203_);
lean_dec(v_k_203_);
return v_res_204_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim(lean_object* v_motive_205_, lean_object* v_ctorIdx_206_, uint8_t v_t_207_, lean_object* v_h_208_, lean_object* v_k_209_){
_start:
{
lean_inc(v_k_209_);
return v_k_209_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim___boxed(lean_object* v_motive_210_, lean_object* v_ctorIdx_211_, lean_object* v_t_212_, lean_object* v_h_213_, lean_object* v_k_214_){
_start:
{
uint8_t v_t_boxed_215_; lean_object* v_res_216_; 
v_t_boxed_215_ = lean_unbox(v_t_212_);
v_res_216_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorElim(v_motive_210_, v_ctorIdx_211_, v_t_boxed_215_, v_h_213_, v_k_214_);
lean_dec(v_k_214_);
lean_dec(v_ctorIdx_211_);
return v_res_216_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___redArg(lean_object* v_zeroDiagonal_217_){
_start:
{
lean_inc(v_zeroDiagonal_217_);
return v_zeroDiagonal_217_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___redArg___boxed(lean_object* v_zeroDiagonal_218_){
_start:
{
lean_object* v_res_219_; 
v_res_219_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___redArg(v_zeroDiagonal_218_);
lean_dec(v_zeroDiagonal_218_);
return v_res_219_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim(lean_object* v_motive_220_, uint8_t v_t_221_, lean_object* v_h_222_, lean_object* v_zeroDiagonal_223_){
_start:
{
lean_inc(v_zeroDiagonal_223_);
return v_zeroDiagonal_223_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim___boxed(lean_object* v_motive_224_, lean_object* v_t_225_, lean_object* v_h_226_, lean_object* v_zeroDiagonal_227_){
_start:
{
uint8_t v_t_boxed_228_; lean_object* v_res_229_; 
v_t_boxed_228_ = lean_unbox(v_t_225_);
v_res_229_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_zeroDiagonal_elim(v_motive_224_, v_t_boxed_228_, v_h_226_, v_zeroDiagonal_227_);
lean_dec(v_zeroDiagonal_227_);
return v_res_229_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___redArg(lean_object* v_oneDiagonal_230_){
_start:
{
lean_inc(v_oneDiagonal_230_);
return v_oneDiagonal_230_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___redArg___boxed(lean_object* v_oneDiagonal_231_){
_start:
{
lean_object* v_res_232_; 
v_res_232_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___redArg(v_oneDiagonal_231_);
lean_dec(v_oneDiagonal_231_);
return v_res_232_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim(lean_object* v_motive_233_, uint8_t v_t_234_, lean_object* v_h_235_, lean_object* v_oneDiagonal_236_){
_start:
{
lean_inc(v_oneDiagonal_236_);
return v_oneDiagonal_236_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim___boxed(lean_object* v_motive_237_, lean_object* v_t_238_, lean_object* v_h_239_, lean_object* v_oneDiagonal_240_){
_start:
{
uint8_t v_t_boxed_241_; lean_object* v_res_242_; 
v_t_boxed_241_ = lean_unbox(v_t_238_);
v_res_242_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_oneDiagonal_elim(v_motive_237_, v_t_boxed_241_, v_h_239_, v_oneDiagonal_240_);
lean_dec(v_oneDiagonal_240_);
return v_res_242_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___redArg(lean_object* v_plusProjectorScaled_243_){
_start:
{
lean_inc(v_plusProjectorScaled_243_);
return v_plusProjectorScaled_243_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___redArg___boxed(lean_object* v_plusProjectorScaled_244_){
_start:
{
lean_object* v_res_245_; 
v_res_245_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___redArg(v_plusProjectorScaled_244_);
lean_dec(v_plusProjectorScaled_244_);
return v_res_245_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim(lean_object* v_motive_246_, uint8_t v_t_247_, lean_object* v_h_248_, lean_object* v_plusProjectorScaled_249_){
_start:
{
lean_inc(v_plusProjectorScaled_249_);
return v_plusProjectorScaled_249_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim___boxed(lean_object* v_motive_250_, lean_object* v_t_251_, lean_object* v_h_252_, lean_object* v_plusProjectorScaled_253_){
_start:
{
uint8_t v_t_boxed_254_; lean_object* v_res_255_; 
v_t_boxed_254_ = lean_unbox(v_t_251_);
v_res_255_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_plusProjectorScaled_elim(v_motive_250_, v_t_boxed_254_, v_h_252_, v_plusProjectorScaled_253_);
lean_dec(v_plusProjectorScaled_253_);
return v_res_255_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ofNat(lean_object* v_n_256_){
_start:
{
lean_object* v___x_257_; uint8_t v___x_258_; 
v___x_257_ = lean_unsigned_to_nat(0u);
v___x_258_ = lean_nat_dec_le(v_n_256_, v___x_257_);
if (v___x_258_ == 0)
{
lean_object* v___x_259_; uint8_t v___x_260_; 
v___x_259_ = lean_unsigned_to_nat(1u);
v___x_260_ = lean_nat_dec_le(v_n_256_, v___x_259_);
if (v___x_260_ == 0)
{
uint8_t v___x_261_; 
v___x_261_ = 2;
return v___x_261_;
}
else
{
uint8_t v___x_262_; 
v___x_262_ = 1;
return v___x_262_;
}
}
else
{
uint8_t v___x_263_; 
v___x_263_ = 0;
return v___x_263_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ofNat___boxed(lean_object* v_n_264_){
_start:
{
uint8_t v_res_265_; lean_object* v_r_266_; 
v_res_265_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ofNat(v_n_264_);
lean_dec(v_n_264_);
v_r_266_ = lean_box(v_res_265_);
return v_r_266_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqLocalSymBasis(uint8_t v_x_267_, uint8_t v_y_268_){
_start:
{
lean_object* v___x_269_; lean_object* v___x_270_; uint8_t v___x_271_; 
v___x_269_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx(v_x_267_);
v___x_270_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_LocalSymBasis_ctorIdx(v_y_268_);
v___x_271_ = lean_nat_dec_eq(v___x_269_, v___x_270_);
lean_dec(v___x_270_);
lean_dec(v___x_269_);
return v___x_271_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqLocalSymBasis___boxed(lean_object* v_x_272_, lean_object* v_y_273_){
_start:
{
uint8_t v_x_13__boxed_274_; uint8_t v_y_14__boxed_275_; uint8_t v_res_276_; lean_object* v_r_277_; 
v_x_13__boxed_274_ = lean_unbox(v_x_272_);
v_y_14__boxed_275_ = lean_unbox(v_y_273_);
v_res_276_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqLocalSymBasis(v_x_13__boxed_274_, v_y_14__boxed_275_);
v_r_277_ = lean_box(v_res_276_);
return v_r_277_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(uint8_t v_x_278_){
_start:
{
switch(v_x_278_)
{
case 2:
{
uint8_t v___x_279_; 
v___x_279_ = 1;
return v___x_279_;
}
case 3:
{
uint8_t v___x_280_; 
v___x_280_ = 1;
return v___x_280_;
}
default: 
{
uint8_t v___x_281_; 
v___x_281_ = 0;
return v___x_281_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord___boxed(lean_object* v_x_282_){
_start:
{
uint8_t v_x_28__boxed_283_; uint8_t v_res_284_; lean_object* v_r_285_; 
v_x_28__boxed_283_ = lean_unbox(v_x_282_);
v_res_284_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_x_28__boxed_283_);
v_r_285_ = lean_box(v_res_284_);
return v_r_285_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(uint8_t v_x_286_){
_start:
{
switch(v_x_286_)
{
case 1:
{
uint8_t v___x_287_; 
v___x_287_ = 1;
return v___x_287_;
}
case 3:
{
uint8_t v___x_288_; 
v___x_288_ = 1;
return v___x_288_;
}
default: 
{
uint8_t v___x_289_; 
v___x_289_ = 0;
return v___x_289_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord___boxed(lean_object* v_x_290_){
_start:
{
uint8_t v_x_28__boxed_291_; uint8_t v_res_292_; lean_object* v_r_293_; 
v_x_28__boxed_291_ = lean_unbox(v_x_290_);
v_res_292_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_x_28__boxed_291_);
v_r_293_ = lean_box(v_res_292_);
return v_r_293_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0(void){
_start:
{
lean_object* v___x_294_; lean_object* v___x_295_; 
v___x_294_ = lean_unsigned_to_nat(0u);
v___x_295_ = lean_nat_to_int(v___x_294_);
return v___x_295_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1(void){
_start:
{
lean_object* v___x_296_; lean_object* v___x_297_; 
v___x_296_ = lean_unsigned_to_nat(1u);
v___x_297_ = lean_nat_to_int(v___x_296_);
return v___x_297_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__2(void){
_start:
{
lean_object* v___x_298_; lean_object* v___x_299_; 
v___x_298_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1);
v___x_299_ = lean_int_neg(v___x_298_);
return v___x_299_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry(uint8_t v_x_300_, uint8_t v_x_301_){
_start:
{
if (v_x_300_ == 0)
{
if (v_x_301_ == 0)
{
goto v___jp_302_;
}
else
{
lean_object* v___x_304_; 
v___x_304_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__2, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__2_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__2);
return v___x_304_;
}
}
else
{
if (v_x_301_ == 0)
{
lean_object* v___x_305_; 
v___x_305_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1);
return v___x_305_;
}
else
{
goto v___jp_302_;
}
}
v___jp_302_:
{
lean_object* v___x_303_; 
v___x_303_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0);
return v___x_303_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___boxed(lean_object* v_x_306_, lean_object* v_x_307_){
_start:
{
uint8_t v_x_66__boxed_308_; uint8_t v_x_67__boxed_309_; lean_object* v_res_310_; 
v_x_66__boxed_308_ = lean_unbox(v_x_306_);
v_x_67__boxed_309_ = lean_unbox(v_x_307_);
v_res_310_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry(v_x_66__boxed_308_, v_x_67__boxed_309_);
return v_res_310_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(uint8_t v_row_311_, uint8_t v_column_312_){
_start:
{
uint8_t v___x_313_; uint8_t v___x_314_; lean_object* v___x_315_; uint8_t v___x_316_; uint8_t v___x_317_; lean_object* v___x_318_; lean_object* v___x_319_; 
v___x_313_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_row_311_);
v___x_314_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_column_312_);
v___x_315_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry(v___x_313_, v___x_314_);
v___x_316_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_row_311_);
v___x_317_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_column_312_);
v___x_318_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry(v___x_316_, v___x_317_);
v___x_319_ = lean_int_mul(v___x_315_, v___x_318_);
lean_dec(v___x_318_);
lean_dec(v___x_315_);
return v___x_319_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry___boxed(lean_object* v_row_320_, lean_object* v_column_321_){
_start:
{
uint8_t v_row_boxed_322_; uint8_t v_column_boxed_323_; lean_object* v_res_324_; 
v_row_boxed_322_ = lean_unbox(v_row_320_);
v_column_boxed_323_ = lean_unbox(v_column_321_);
v_res_324_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(v_row_boxed_322_, v_column_boxed_323_);
return v_res_324_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry(uint8_t v_x_325_, uint8_t v_x_326_, uint8_t v_x_327_){
_start:
{
switch(v_x_325_)
{
case 0:
{
if (v_x_326_ == 0)
{
if (v_x_327_ == 0)
{
goto v___jp_328_;
}
else
{
goto v___jp_330_;
}
}
else
{
goto v___jp_330_;
}
}
case 1:
{
if (v_x_326_ == 1)
{
if (v_x_327_ == 1)
{
goto v___jp_328_;
}
else
{
goto v___jp_330_;
}
}
else
{
goto v___jp_330_;
}
}
default: 
{
lean_object* v___x_332_; 
v___x_332_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1);
return v___x_332_;
}
}
v___jp_328_:
{
lean_object* v___x_329_; 
v___x_329_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1);
return v___x_329_;
}
v___jp_330_:
{
lean_object* v___x_331_; 
v___x_331_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0);
return v___x_331_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry___boxed(lean_object* v_x_333_, lean_object* v_x_334_, lean_object* v_x_335_){
_start:
{
uint8_t v_x_78__boxed_336_; uint8_t v_x_79__boxed_337_; uint8_t v_x_80__boxed_338_; lean_object* v_res_339_; 
v_x_78__boxed_336_ = lean_unbox(v_x_333_);
v_x_79__boxed_337_ = lean_unbox(v_x_334_);
v_x_80__boxed_338_ = lean_unbox(v_x_335_);
v_res_339_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry(v_x_78__boxed_336_, v_x_79__boxed_337_, v_x_80__boxed_338_);
return v_res_339_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productEntry(uint8_t v_left_340_, uint8_t v_right_341_, uint8_t v_row_342_, uint8_t v_column_343_){
_start:
{
uint8_t v___x_344_; uint8_t v___x_345_; lean_object* v___x_346_; uint8_t v___x_347_; uint8_t v___x_348_; lean_object* v___x_349_; lean_object* v___x_350_; 
v___x_344_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_row_342_);
v___x_345_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_column_343_);
v___x_346_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry(v_left_340_, v___x_344_, v___x_345_);
v___x_347_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_row_342_);
v___x_348_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_column_343_);
v___x_349_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_localBasisEntry(v_right_341_, v___x_347_, v___x_348_);
v___x_350_ = lean_int_mul(v___x_346_, v___x_349_);
lean_dec(v___x_349_);
lean_dec(v___x_346_);
return v___x_350_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productEntry___boxed(lean_object* v_left_351_, lean_object* v_right_352_, lean_object* v_row_353_, lean_object* v_column_354_){
_start:
{
uint8_t v_left_boxed_355_; uint8_t v_right_boxed_356_; uint8_t v_row_boxed_357_; uint8_t v_column_boxed_358_; lean_object* v_res_359_; 
v_left_boxed_355_ = lean_unbox(v_left_351_);
v_right_boxed_356_ = lean_unbox(v_right_352_);
v_row_boxed_357_ = lean_unbox(v_row_353_);
v_column_boxed_358_ = lean_unbox(v_column_354_);
v_res_359_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_productEntry(v_left_boxed_355_, v_right_boxed_356_, v_row_boxed_357_, v_column_boxed_358_);
return v_res_359_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productMatrixEntry(lean_object* v_left_360_, lean_object* v_right_361_, uint8_t v_row_362_, uint8_t v_column_363_){
_start:
{
uint8_t v___x_364_; uint8_t v___x_365_; lean_object* v___x_366_; lean_object* v___x_367_; lean_object* v___x_368_; uint8_t v___x_369_; uint8_t v___x_370_; lean_object* v___x_371_; lean_object* v___x_372_; lean_object* v___x_373_; lean_object* v___x_374_; 
v___x_364_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_row_362_);
v___x_365_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_leftCoord(v_column_363_);
v___x_366_ = lean_box(v___x_364_);
v___x_367_ = lean_box(v___x_365_);
v___x_368_ = lean_apply_2(v_left_360_, v___x_366_, v___x_367_);
v___x_369_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_row_362_);
v___x_370_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rightCoord(v_column_363_);
v___x_371_ = lean_box(v___x_369_);
v___x_372_ = lean_box(v___x_370_);
v___x_373_ = lean_apply_2(v_right_361_, v___x_371_, v___x_372_);
v___x_374_ = lean_int_mul(v___x_368_, v___x_373_);
lean_dec(v___x_373_);
lean_dec(v___x_368_);
return v___x_374_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_productMatrixEntry___boxed(lean_object* v_left_375_, lean_object* v_right_376_, lean_object* v_row_377_, lean_object* v_column_378_){
_start:
{
uint8_t v_row_boxed_379_; uint8_t v_column_boxed_380_; lean_object* v_res_381_; 
v_row_boxed_379_ = lean_unbox(v_row_377_);
v_column_boxed_380_ = lean_unbox(v_column_378_);
v_res_381_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_productMatrixEntry(v_left_375_, v_right_376_, v_row_boxed_379_, v_column_boxed_380_);
return v_res_381_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(lean_object* v_left_382_, lean_object* v_right_383_, uint8_t v_x_384_){
_start:
{
switch(v_x_384_)
{
case 0:
{
lean_object* v___x_385_; lean_object* v___x_386_; lean_object* v___x_387_; lean_object* v___x_388_; lean_object* v___x_389_; lean_object* v___x_390_; lean_object* v___x_391_; uint8_t v___x_392_; lean_object* v___x_393_; lean_object* v___x_394_; lean_object* v___x_395_; lean_object* v___x_396_; lean_object* v___x_397_; lean_object* v___x_398_; lean_object* v___x_399_; lean_object* v___x_400_; uint8_t v___x_401_; lean_object* v___x_402_; lean_object* v___x_403_; lean_object* v___x_404_; lean_object* v___x_405_; lean_object* v___x_406_; lean_object* v___x_407_; lean_object* v___x_408_; lean_object* v___x_409_; uint8_t v___x_410_; lean_object* v___x_411_; lean_object* v___x_412_; lean_object* v___x_413_; lean_object* v___x_414_; lean_object* v___x_415_; lean_object* v___x_416_; lean_object* v___x_417_; lean_object* v___x_418_; 
v___x_385_ = lean_box(v_x_384_);
v___x_386_ = lean_box(v_x_384_);
lean_inc_ref_n(v_left_382_, 3);
v___x_387_ = lean_apply_2(v_left_382_, v___x_385_, v___x_386_);
v___x_388_ = lean_box(v_x_384_);
v___x_389_ = lean_box(v_x_384_);
lean_inc_ref_n(v_right_383_, 3);
v___x_390_ = lean_apply_2(v_right_383_, v___x_388_, v___x_389_);
v___x_391_ = lean_int_mul(v___x_387_, v___x_390_);
lean_dec(v___x_390_);
lean_dec(v___x_387_);
v___x_392_ = 1;
v___x_393_ = lean_box(v_x_384_);
v___x_394_ = lean_box(v___x_392_);
v___x_395_ = lean_apply_2(v_left_382_, v___x_393_, v___x_394_);
v___x_396_ = lean_box(v_x_384_);
v___x_397_ = lean_box(v___x_392_);
v___x_398_ = lean_apply_2(v_right_383_, v___x_396_, v___x_397_);
v___x_399_ = lean_int_mul(v___x_395_, v___x_398_);
lean_dec(v___x_398_);
lean_dec(v___x_395_);
v___x_400_ = lean_int_add(v___x_391_, v___x_399_);
lean_dec(v___x_399_);
lean_dec(v___x_391_);
v___x_401_ = 2;
v___x_402_ = lean_box(v_x_384_);
v___x_403_ = lean_box(v___x_401_);
v___x_404_ = lean_apply_2(v_left_382_, v___x_402_, v___x_403_);
v___x_405_ = lean_box(v_x_384_);
v___x_406_ = lean_box(v___x_401_);
v___x_407_ = lean_apply_2(v_right_383_, v___x_405_, v___x_406_);
v___x_408_ = lean_int_mul(v___x_404_, v___x_407_);
lean_dec(v___x_407_);
lean_dec(v___x_404_);
v___x_409_ = lean_int_add(v___x_400_, v___x_408_);
lean_dec(v___x_408_);
lean_dec(v___x_400_);
v___x_410_ = 3;
v___x_411_ = lean_box(v_x_384_);
v___x_412_ = lean_box(v___x_410_);
v___x_413_ = lean_apply_2(v_left_382_, v___x_411_, v___x_412_);
v___x_414_ = lean_box(v_x_384_);
v___x_415_ = lean_box(v___x_410_);
v___x_416_ = lean_apply_2(v_right_383_, v___x_414_, v___x_415_);
v___x_417_ = lean_int_mul(v___x_413_, v___x_416_);
lean_dec(v___x_416_);
lean_dec(v___x_413_);
v___x_418_ = lean_int_add(v___x_409_, v___x_417_);
lean_dec(v___x_417_);
lean_dec(v___x_409_);
return v___x_418_;
}
case 1:
{
uint8_t v___x_419_; lean_object* v___x_420_; lean_object* v___x_421_; lean_object* v___x_422_; lean_object* v___x_423_; lean_object* v___x_424_; lean_object* v___x_425_; lean_object* v___x_426_; lean_object* v___x_427_; lean_object* v___x_428_; lean_object* v___x_429_; lean_object* v___x_430_; lean_object* v___x_431_; lean_object* v___x_432_; lean_object* v___x_433_; lean_object* v___x_434_; uint8_t v___x_435_; lean_object* v___x_436_; lean_object* v___x_437_; lean_object* v___x_438_; lean_object* v___x_439_; lean_object* v___x_440_; lean_object* v___x_441_; lean_object* v___x_442_; lean_object* v___x_443_; uint8_t v___x_444_; lean_object* v___x_445_; lean_object* v___x_446_; lean_object* v___x_447_; lean_object* v___x_448_; lean_object* v___x_449_; lean_object* v___x_450_; lean_object* v___x_451_; lean_object* v___x_452_; 
v___x_419_ = 0;
v___x_420_ = lean_box(v_x_384_);
v___x_421_ = lean_box(v___x_419_);
lean_inc_ref_n(v_left_382_, 3);
v___x_422_ = lean_apply_2(v_left_382_, v___x_420_, v___x_421_);
v___x_423_ = lean_box(v_x_384_);
v___x_424_ = lean_box(v___x_419_);
lean_inc_ref_n(v_right_383_, 3);
v___x_425_ = lean_apply_2(v_right_383_, v___x_423_, v___x_424_);
v___x_426_ = lean_int_mul(v___x_422_, v___x_425_);
lean_dec(v___x_425_);
lean_dec(v___x_422_);
v___x_427_ = lean_box(v_x_384_);
v___x_428_ = lean_box(v_x_384_);
v___x_429_ = lean_apply_2(v_left_382_, v___x_427_, v___x_428_);
v___x_430_ = lean_box(v_x_384_);
v___x_431_ = lean_box(v_x_384_);
v___x_432_ = lean_apply_2(v_right_383_, v___x_430_, v___x_431_);
v___x_433_ = lean_int_mul(v___x_429_, v___x_432_);
lean_dec(v___x_432_);
lean_dec(v___x_429_);
v___x_434_ = lean_int_add(v___x_426_, v___x_433_);
lean_dec(v___x_433_);
lean_dec(v___x_426_);
v___x_435_ = 2;
v___x_436_ = lean_box(v_x_384_);
v___x_437_ = lean_box(v___x_435_);
v___x_438_ = lean_apply_2(v_left_382_, v___x_436_, v___x_437_);
v___x_439_ = lean_box(v_x_384_);
v___x_440_ = lean_box(v___x_435_);
v___x_441_ = lean_apply_2(v_right_383_, v___x_439_, v___x_440_);
v___x_442_ = lean_int_mul(v___x_438_, v___x_441_);
lean_dec(v___x_441_);
lean_dec(v___x_438_);
v___x_443_ = lean_int_add(v___x_434_, v___x_442_);
lean_dec(v___x_442_);
lean_dec(v___x_434_);
v___x_444_ = 3;
v___x_445_ = lean_box(v_x_384_);
v___x_446_ = lean_box(v___x_444_);
v___x_447_ = lean_apply_2(v_left_382_, v___x_445_, v___x_446_);
v___x_448_ = lean_box(v_x_384_);
v___x_449_ = lean_box(v___x_444_);
v___x_450_ = lean_apply_2(v_right_383_, v___x_448_, v___x_449_);
v___x_451_ = lean_int_mul(v___x_447_, v___x_450_);
lean_dec(v___x_450_);
lean_dec(v___x_447_);
v___x_452_ = lean_int_add(v___x_443_, v___x_451_);
lean_dec(v___x_451_);
lean_dec(v___x_443_);
return v___x_452_;
}
case 2:
{
uint8_t v___x_453_; lean_object* v___x_454_; lean_object* v___x_455_; lean_object* v___x_456_; lean_object* v___x_457_; lean_object* v___x_458_; lean_object* v___x_459_; lean_object* v___x_460_; uint8_t v___x_461_; lean_object* v___x_462_; lean_object* v___x_463_; lean_object* v___x_464_; lean_object* v___x_465_; lean_object* v___x_466_; lean_object* v___x_467_; lean_object* v___x_468_; lean_object* v___x_469_; lean_object* v___x_470_; lean_object* v___x_471_; lean_object* v___x_472_; lean_object* v___x_473_; lean_object* v___x_474_; lean_object* v___x_475_; lean_object* v___x_476_; lean_object* v___x_477_; uint8_t v___x_478_; lean_object* v___x_479_; lean_object* v___x_480_; lean_object* v___x_481_; lean_object* v___x_482_; lean_object* v___x_483_; lean_object* v___x_484_; lean_object* v___x_485_; lean_object* v___x_486_; 
v___x_453_ = 0;
v___x_454_ = lean_box(v_x_384_);
v___x_455_ = lean_box(v___x_453_);
lean_inc_ref_n(v_left_382_, 3);
v___x_456_ = lean_apply_2(v_left_382_, v___x_454_, v___x_455_);
v___x_457_ = lean_box(v_x_384_);
v___x_458_ = lean_box(v___x_453_);
lean_inc_ref_n(v_right_383_, 3);
v___x_459_ = lean_apply_2(v_right_383_, v___x_457_, v___x_458_);
v___x_460_ = lean_int_mul(v___x_456_, v___x_459_);
lean_dec(v___x_459_);
lean_dec(v___x_456_);
v___x_461_ = 1;
v___x_462_ = lean_box(v_x_384_);
v___x_463_ = lean_box(v___x_461_);
v___x_464_ = lean_apply_2(v_left_382_, v___x_462_, v___x_463_);
v___x_465_ = lean_box(v_x_384_);
v___x_466_ = lean_box(v___x_461_);
v___x_467_ = lean_apply_2(v_right_383_, v___x_465_, v___x_466_);
v___x_468_ = lean_int_mul(v___x_464_, v___x_467_);
lean_dec(v___x_467_);
lean_dec(v___x_464_);
v___x_469_ = lean_int_add(v___x_460_, v___x_468_);
lean_dec(v___x_468_);
lean_dec(v___x_460_);
v___x_470_ = lean_box(v_x_384_);
v___x_471_ = lean_box(v_x_384_);
v___x_472_ = lean_apply_2(v_left_382_, v___x_470_, v___x_471_);
v___x_473_ = lean_box(v_x_384_);
v___x_474_ = lean_box(v_x_384_);
v___x_475_ = lean_apply_2(v_right_383_, v___x_473_, v___x_474_);
v___x_476_ = lean_int_mul(v___x_472_, v___x_475_);
lean_dec(v___x_475_);
lean_dec(v___x_472_);
v___x_477_ = lean_int_add(v___x_469_, v___x_476_);
lean_dec(v___x_476_);
lean_dec(v___x_469_);
v___x_478_ = 3;
v___x_479_ = lean_box(v_x_384_);
v___x_480_ = lean_box(v___x_478_);
v___x_481_ = lean_apply_2(v_left_382_, v___x_479_, v___x_480_);
v___x_482_ = lean_box(v_x_384_);
v___x_483_ = lean_box(v___x_478_);
v___x_484_ = lean_apply_2(v_right_383_, v___x_482_, v___x_483_);
v___x_485_ = lean_int_mul(v___x_481_, v___x_484_);
lean_dec(v___x_484_);
lean_dec(v___x_481_);
v___x_486_ = lean_int_add(v___x_477_, v___x_485_);
lean_dec(v___x_485_);
lean_dec(v___x_477_);
return v___x_486_;
}
default: 
{
uint8_t v___x_487_; lean_object* v___x_488_; lean_object* v___x_489_; lean_object* v___x_490_; lean_object* v___x_491_; lean_object* v___x_492_; lean_object* v___x_493_; lean_object* v___x_494_; uint8_t v___x_495_; lean_object* v___x_496_; lean_object* v___x_497_; lean_object* v___x_498_; lean_object* v___x_499_; lean_object* v___x_500_; lean_object* v___x_501_; lean_object* v___x_502_; lean_object* v___x_503_; uint8_t v___x_504_; lean_object* v___x_505_; lean_object* v___x_506_; lean_object* v___x_507_; lean_object* v___x_508_; lean_object* v___x_509_; lean_object* v___x_510_; lean_object* v___x_511_; lean_object* v___x_512_; lean_object* v___x_513_; lean_object* v___x_514_; lean_object* v___x_515_; lean_object* v___x_516_; lean_object* v___x_517_; lean_object* v___x_518_; lean_object* v___x_519_; lean_object* v___x_520_; 
v___x_487_ = 0;
v___x_488_ = lean_box(v_x_384_);
v___x_489_ = lean_box(v___x_487_);
lean_inc_ref_n(v_left_382_, 3);
v___x_490_ = lean_apply_2(v_left_382_, v___x_488_, v___x_489_);
v___x_491_ = lean_box(v_x_384_);
v___x_492_ = lean_box(v___x_487_);
lean_inc_ref_n(v_right_383_, 3);
v___x_493_ = lean_apply_2(v_right_383_, v___x_491_, v___x_492_);
v___x_494_ = lean_int_mul(v___x_490_, v___x_493_);
lean_dec(v___x_493_);
lean_dec(v___x_490_);
v___x_495_ = 1;
v___x_496_ = lean_box(v_x_384_);
v___x_497_ = lean_box(v___x_495_);
v___x_498_ = lean_apply_2(v_left_382_, v___x_496_, v___x_497_);
v___x_499_ = lean_box(v_x_384_);
v___x_500_ = lean_box(v___x_495_);
v___x_501_ = lean_apply_2(v_right_383_, v___x_499_, v___x_500_);
v___x_502_ = lean_int_mul(v___x_498_, v___x_501_);
lean_dec(v___x_501_);
lean_dec(v___x_498_);
v___x_503_ = lean_int_add(v___x_494_, v___x_502_);
lean_dec(v___x_502_);
lean_dec(v___x_494_);
v___x_504_ = 2;
v___x_505_ = lean_box(v_x_384_);
v___x_506_ = lean_box(v___x_504_);
v___x_507_ = lean_apply_2(v_left_382_, v___x_505_, v___x_506_);
v___x_508_ = lean_box(v_x_384_);
v___x_509_ = lean_box(v___x_504_);
v___x_510_ = lean_apply_2(v_right_383_, v___x_508_, v___x_509_);
v___x_511_ = lean_int_mul(v___x_507_, v___x_510_);
lean_dec(v___x_510_);
lean_dec(v___x_507_);
v___x_512_ = lean_int_add(v___x_503_, v___x_511_);
lean_dec(v___x_511_);
lean_dec(v___x_503_);
v___x_513_ = lean_box(v_x_384_);
v___x_514_ = lean_box(v_x_384_);
v___x_515_ = lean_apply_2(v_left_382_, v___x_513_, v___x_514_);
v___x_516_ = lean_box(v_x_384_);
v___x_517_ = lean_box(v_x_384_);
v___x_518_ = lean_apply_2(v_right_383_, v___x_516_, v___x_517_);
v___x_519_ = lean_int_mul(v___x_515_, v___x_518_);
lean_dec(v___x_518_);
lean_dec(v___x_515_);
v___x_520_ = lean_int_add(v___x_512_, v___x_519_);
lean_dec(v___x_519_);
lean_dec(v___x_512_);
return v___x_520_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner___boxed(lean_object* v_left_521_, lean_object* v_right_522_, lean_object* v_x_523_){
_start:
{
uint8_t v_x_344__boxed_524_; lean_object* v_res_525_; 
v_x_344__boxed_524_ = lean_unbox(v_x_523_);
v_res_525_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(v_left_521_, v_right_522_, v_x_344__boxed_524_);
return v_res_525_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_frobeniusInner(lean_object* v_left_526_, lean_object* v_right_527_){
_start:
{
uint8_t v___x_528_; lean_object* v___x_529_; uint8_t v___x_530_; lean_object* v___x_531_; lean_object* v___x_532_; uint8_t v___x_533_; lean_object* v___x_534_; lean_object* v___x_535_; uint8_t v___x_536_; lean_object* v___x_537_; lean_object* v___x_538_; 
v___x_528_ = 0;
lean_inc_ref_n(v_right_527_, 3);
lean_inc_ref_n(v_left_526_, 3);
v___x_529_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(v_left_526_, v_right_527_, v___x_528_);
v___x_530_ = 1;
v___x_531_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(v_left_526_, v_right_527_, v___x_530_);
v___x_532_ = lean_int_add(v___x_529_, v___x_531_);
lean_dec(v___x_531_);
lean_dec(v___x_529_);
v___x_533_ = 2;
v___x_534_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(v_left_526_, v_right_527_, v___x_533_);
v___x_535_ = lean_int_add(v___x_532_, v___x_534_);
lean_dec(v___x_534_);
lean_dec(v___x_532_);
v___x_536_ = 3;
v___x_537_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rowInner(v_left_526_, v_right_527_, v___x_536_);
v___x_538_ = lean_int_add(v___x_535_, v___x_537_);
lean_dec(v___x_537_);
lean_dec(v___x_535_);
return v___x_538_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(uint8_t v_row_539_, uint8_t v_column_540_){
_start:
{
uint8_t v___x_541_; 
v___x_541_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_instDecidableEqJointCoord(v_row_539_, v_column_540_);
if (v___x_541_ == 0)
{
lean_object* v___x_542_; 
v___x_542_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__0);
return v___x_542_;
}
else
{
lean_object* v___x_543_; 
v___x_543_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_jEntry___closed__1);
return v___x_543_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry___boxed(lean_object* v_row_544_, lean_object* v_column_545_){
_start:
{
uint8_t v_row_boxed_546_; uint8_t v_column_boxed_547_; lean_object* v_res_548_; 
v_row_boxed_546_ = lean_unbox(v_row_544_);
v_column_boxed_547_ = lean_unbox(v_column_545_);
v_res_548_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(v_row_boxed_546_, v_column_boxed_547_);
return v_res_548_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_matrixMulEntry(lean_object* v_left_549_, lean_object* v_right_550_, uint8_t v_row_551_, uint8_t v_column_552_){
_start:
{
uint8_t v___x_553_; lean_object* v___x_554_; lean_object* v___x_555_; lean_object* v___x_556_; lean_object* v___x_557_; lean_object* v___x_558_; lean_object* v___x_559_; lean_object* v___x_560_; uint8_t v___x_561_; lean_object* v___x_562_; lean_object* v___x_563_; lean_object* v___x_564_; lean_object* v___x_565_; lean_object* v___x_566_; lean_object* v___x_567_; lean_object* v___x_568_; lean_object* v___x_569_; uint8_t v___x_570_; lean_object* v___x_571_; lean_object* v___x_572_; lean_object* v___x_573_; lean_object* v___x_574_; lean_object* v___x_575_; lean_object* v___x_576_; lean_object* v___x_577_; lean_object* v___x_578_; uint8_t v___x_579_; lean_object* v___x_580_; lean_object* v___x_581_; lean_object* v___x_582_; lean_object* v___x_583_; lean_object* v___x_584_; lean_object* v___x_585_; lean_object* v___x_586_; lean_object* v___x_587_; 
v___x_553_ = 0;
v___x_554_ = lean_box(v_row_551_);
v___x_555_ = lean_box(v___x_553_);
lean_inc_ref_n(v_left_549_, 3);
v___x_556_ = lean_apply_2(v_left_549_, v___x_554_, v___x_555_);
v___x_557_ = lean_box(v___x_553_);
v___x_558_ = lean_box(v_column_552_);
lean_inc_ref_n(v_right_550_, 3);
v___x_559_ = lean_apply_2(v_right_550_, v___x_557_, v___x_558_);
v___x_560_ = lean_int_mul(v___x_556_, v___x_559_);
lean_dec(v___x_559_);
lean_dec(v___x_556_);
v___x_561_ = 1;
v___x_562_ = lean_box(v_row_551_);
v___x_563_ = lean_box(v___x_561_);
v___x_564_ = lean_apply_2(v_left_549_, v___x_562_, v___x_563_);
v___x_565_ = lean_box(v___x_561_);
v___x_566_ = lean_box(v_column_552_);
v___x_567_ = lean_apply_2(v_right_550_, v___x_565_, v___x_566_);
v___x_568_ = lean_int_mul(v___x_564_, v___x_567_);
lean_dec(v___x_567_);
lean_dec(v___x_564_);
v___x_569_ = lean_int_add(v___x_560_, v___x_568_);
lean_dec(v___x_568_);
lean_dec(v___x_560_);
v___x_570_ = 2;
v___x_571_ = lean_box(v_row_551_);
v___x_572_ = lean_box(v___x_570_);
v___x_573_ = lean_apply_2(v_left_549_, v___x_571_, v___x_572_);
v___x_574_ = lean_box(v___x_570_);
v___x_575_ = lean_box(v_column_552_);
v___x_576_ = lean_apply_2(v_right_550_, v___x_574_, v___x_575_);
v___x_577_ = lean_int_mul(v___x_573_, v___x_576_);
lean_dec(v___x_576_);
lean_dec(v___x_573_);
v___x_578_ = lean_int_add(v___x_569_, v___x_577_);
lean_dec(v___x_577_);
lean_dec(v___x_569_);
v___x_579_ = 3;
v___x_580_ = lean_box(v_row_551_);
v___x_581_ = lean_box(v___x_579_);
v___x_582_ = lean_apply_2(v_left_549_, v___x_580_, v___x_581_);
v___x_583_ = lean_box(v___x_579_);
v___x_584_ = lean_box(v_column_552_);
v___x_585_ = lean_apply_2(v_right_550_, v___x_583_, v___x_584_);
v___x_586_ = lean_int_mul(v___x_582_, v___x_585_);
lean_dec(v___x_585_);
lean_dec(v___x_582_);
v___x_587_ = lean_int_add(v___x_578_, v___x_586_);
lean_dec(v___x_586_);
lean_dec(v___x_578_);
return v___x_587_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_matrixMulEntry___boxed(lean_object* v_left_588_, lean_object* v_right_589_, lean_object* v_row_590_, lean_object* v_column_591_){
_start:
{
uint8_t v_row_boxed_592_; uint8_t v_column_boxed_593_; lean_object* v_res_594_; 
v_row_boxed_592_ = lean_unbox(v_row_590_);
v_column_boxed_593_ = lean_unbox(v_column_591_);
v_res_594_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_matrixMulEntry(v_left_588_, v_right_589_, v_row_boxed_592_, v_column_boxed_593_);
return v_res_594_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pPlusScaled(uint8_t v_row_595_, uint8_t v_column_596_){
_start:
{
lean_object* v___x_597_; lean_object* v___x_598_; lean_object* v___x_599_; 
v___x_597_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(v_row_595_, v_column_596_);
v___x_598_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(v_row_595_, v_column_596_);
v___x_599_ = lean_int_add(v___x_597_, v___x_598_);
lean_dec(v___x_598_);
lean_dec(v___x_597_);
return v___x_599_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pPlusScaled___boxed(lean_object* v_row_600_, lean_object* v_column_601_){
_start:
{
uint8_t v_row_boxed_602_; uint8_t v_column_boxed_603_; lean_object* v_res_604_; 
v_row_boxed_602_ = lean_unbox(v_row_600_);
v_column_boxed_603_ = lean_unbox(v_column_601_);
v_res_604_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_pPlusScaled(v_row_boxed_602_, v_column_boxed_603_);
return v_res_604_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pMinusScaled(uint8_t v_row_605_, uint8_t v_column_606_){
_start:
{
lean_object* v___x_607_; lean_object* v___x_608_; lean_object* v___x_609_; 
v___x_607_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(v_row_605_, v_column_606_);
v___x_608_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(v_row_605_, v_column_606_);
v___x_609_ = lean_int_sub(v___x_607_, v___x_608_);
lean_dec(v___x_608_);
lean_dec(v___x_607_);
return v___x_609_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_pMinusScaled___boxed(lean_object* v_row_610_, lean_object* v_column_611_){
_start:
{
uint8_t v_row_boxed_612_; uint8_t v_column_boxed_613_; lean_object* v_res_614_; 
v_row_boxed_612_ = lean_unbox(v_row_610_);
v_column_boxed_613_ = lean_unbox(v_column_611_);
v_res_614_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_pMinusScaled(v_row_boxed_612_, v_column_boxed_613_);
return v_res_614_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0(void){
_start:
{
lean_object* v___x_615_; lean_object* v___x_616_; 
v___x_615_ = lean_unsigned_to_nat(4u);
v___x_616_ = lean_nat_to_int(v___x_615_);
return v___x_616_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1(void){
_start:
{
lean_object* v___x_617_; lean_object* v___x_618_; 
v___x_617_ = lean_unsigned_to_nat(2u);
v___x_618_ = lean_nat_to_int(v___x_617_);
return v___x_618_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled(uint8_t v_row_619_, uint8_t v_column_620_){
_start:
{
lean_object* v___x_621_; lean_object* v___x_622_; lean_object* v___x_623_; lean_object* v___x_624_; lean_object* v___x_625_; lean_object* v___x_626_; lean_object* v___x_627_; 
v___x_621_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0);
v___x_622_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(v_row_619_, v_column_620_);
v___x_623_ = lean_int_mul(v___x_621_, v___x_622_);
lean_dec(v___x_622_);
v___x_624_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1);
v___x_625_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(v_row_619_, v_column_620_);
v___x_626_ = lean_int_mul(v___x_624_, v___x_625_);
lean_dec(v___x_625_);
v___x_627_ = lean_int_add(v___x_623_, v___x_626_);
lean_dec(v___x_626_);
lean_dec(v___x_623_);
return v___x_627_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___boxed(lean_object* v_row_628_, lean_object* v_column_629_){
_start:
{
uint8_t v_row_boxed_630_; uint8_t v_column_boxed_631_; lean_object* v_res_632_; 
v_row_boxed_630_ = lean_unbox(v_row_628_);
v_column_boxed_631_ = lean_unbox(v_column_629_);
v_res_632_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled(v_row_boxed_630_, v_column_boxed_631_);
return v_res_632_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoMinusScaled(uint8_t v_row_633_, uint8_t v_column_634_){
_start:
{
lean_object* v___x_635_; lean_object* v___x_636_; lean_object* v___x_637_; lean_object* v___x_638_; lean_object* v___x_639_; lean_object* v___x_640_; lean_object* v___x_641_; 
v___x_635_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__0);
v___x_636_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_identityEntry(v_row_633_, v_column_634_);
v___x_637_ = lean_int_mul(v___x_635_, v___x_636_);
lean_dec(v___x_636_);
v___x_638_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1, &lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___closed__1);
v___x_639_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry(v_row_633_, v_column_634_);
v___x_640_ = lean_int_mul(v___x_638_, v___x_639_);
lean_dec(v___x_639_);
v___x_641_ = lean_int_sub(v___x_637_, v___x_640_);
lean_dec(v___x_640_);
lean_dec(v___x_637_);
return v___x_641_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoMinusScaled___boxed(lean_object* v_row_642_, lean_object* v_column_643_){
_start:
{
uint8_t v_row_boxed_644_; uint8_t v_column_boxed_645_; lean_object* v_res_646_; 
v_row_boxed_644_ = lean_unbox(v_row_642_);
v_column_boxed_645_ = lean_unbox(v_column_643_);
v_res_646_ = lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoMinusScaled(v_row_boxed_644_, v_column_boxed_645_);
return v_res_646_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_RebitQ9_trace4(lean_object* v_matrix_647_){
_start:
{
uint8_t v___x_648_; lean_object* v___x_649_; lean_object* v___x_650_; lean_object* v___x_651_; uint8_t v___x_652_; lean_object* v___x_653_; lean_object* v___x_654_; lean_object* v___x_655_; lean_object* v___x_656_; uint8_t v___x_657_; lean_object* v___x_658_; lean_object* v___x_659_; lean_object* v___x_660_; lean_object* v___x_661_; uint8_t v___x_662_; lean_object* v___x_663_; lean_object* v___x_664_; lean_object* v___x_665_; lean_object* v___x_666_; 
v___x_648_ = 0;
v___x_649_ = lean_box(v___x_648_);
v___x_650_ = lean_box(v___x_648_);
lean_inc_ref_n(v_matrix_647_, 3);
v___x_651_ = lean_apply_2(v_matrix_647_, v___x_649_, v___x_650_);
v___x_652_ = 1;
v___x_653_ = lean_box(v___x_652_);
v___x_654_ = lean_box(v___x_652_);
v___x_655_ = lean_apply_2(v_matrix_647_, v___x_653_, v___x_654_);
v___x_656_ = lean_int_add(v___x_651_, v___x_655_);
lean_dec(v___x_655_);
lean_dec(v___x_651_);
v___x_657_ = 2;
v___x_658_ = lean_box(v___x_657_);
v___x_659_ = lean_box(v___x_657_);
v___x_660_ = lean_apply_2(v_matrix_647_, v___x_658_, v___x_659_);
v___x_661_ = lean_int_add(v___x_656_, v___x_660_);
lean_dec(v___x_660_);
lean_dec(v___x_656_);
v___x_662_ = 3;
v___x_663_ = lean_box(v___x_662_);
v___x_664_ = lean_box(v___x_662_);
v___x_665_ = lean_apply_2(v_matrix_647_, v___x_663_, v___x_664_);
v___x_666_ = lean_int_add(v___x_661_, v___x_665_);
lean_dec(v___x_665_);
lean_dec(v___x_661_);
return v___x_666_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___redArg(uint8_t v_x_667_, lean_object* v_h__1_668_, lean_object* v_h__2_669_, lean_object* v_h__3_670_, lean_object* v_h__4_671_){
_start:
{
switch(v_x_667_)
{
case 0:
{
lean_object* v___x_672_; lean_object* v___x_673_; 
lean_dec(v_h__4_671_);
lean_dec(v_h__3_670_);
lean_dec(v_h__2_669_);
v___x_672_ = lean_box(0);
v___x_673_ = lean_apply_1(v_h__1_668_, v___x_672_);
return v___x_673_;
}
case 1:
{
lean_object* v___x_674_; lean_object* v___x_675_; 
lean_dec(v_h__4_671_);
lean_dec(v_h__3_670_);
lean_dec(v_h__1_668_);
v___x_674_ = lean_box(0);
v___x_675_ = lean_apply_1(v_h__2_669_, v___x_674_);
return v___x_675_;
}
case 2:
{
lean_object* v___x_676_; lean_object* v___x_677_; 
lean_dec(v_h__4_671_);
lean_dec(v_h__2_669_);
lean_dec(v_h__1_668_);
v___x_676_ = lean_box(0);
v___x_677_ = lean_apply_1(v_h__3_670_, v___x_676_);
return v___x_677_;
}
default: 
{
lean_object* v___x_678_; lean_object* v___x_679_; 
lean_dec(v_h__3_670_);
lean_dec(v_h__2_669_);
lean_dec(v_h__1_668_);
v___x_678_ = lean_box(0);
v___x_679_ = lean_apply_1(v_h__4_671_, v___x_678_);
return v___x_679_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___redArg___boxed(lean_object* v_x_680_, lean_object* v_h__1_681_, lean_object* v_h__2_682_, lean_object* v_h__3_683_, lean_object* v_h__4_684_){
_start:
{
uint8_t v_x_42__boxed_685_; lean_object* v_res_686_; 
v_x_42__boxed_685_ = lean_unbox(v_x_680_);
v_res_686_ = lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___redArg(v_x_42__boxed_685_, v_h__1_681_, v_h__2_682_, v_h__3_683_, v_h__4_684_);
return v_res_686_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter(lean_object* v_motive_687_, uint8_t v_x_688_, lean_object* v_h__1_689_, lean_object* v_h__2_690_, lean_object* v_h__3_691_, lean_object* v_h__4_692_){
_start:
{
switch(v_x_688_)
{
case 0:
{
lean_object* v___x_693_; lean_object* v___x_694_; 
lean_dec(v_h__4_692_);
lean_dec(v_h__3_691_);
lean_dec(v_h__2_690_);
v___x_693_ = lean_box(0);
v___x_694_ = lean_apply_1(v_h__1_689_, v___x_693_);
return v___x_694_;
}
case 1:
{
lean_object* v___x_695_; lean_object* v___x_696_; 
lean_dec(v_h__4_692_);
lean_dec(v_h__3_691_);
lean_dec(v_h__1_689_);
v___x_695_ = lean_box(0);
v___x_696_ = lean_apply_1(v_h__2_690_, v___x_695_);
return v___x_696_;
}
case 2:
{
lean_object* v___x_697_; lean_object* v___x_698_; 
lean_dec(v_h__4_692_);
lean_dec(v_h__2_690_);
lean_dec(v_h__1_689_);
v___x_697_ = lean_box(0);
v___x_698_ = lean_apply_1(v_h__3_691_, v___x_697_);
return v___x_698_;
}
default: 
{
lean_object* v___x_699_; lean_object* v___x_700_; 
lean_dec(v_h__3_691_);
lean_dec(v_h__2_690_);
lean_dec(v_h__1_689_);
v___x_699_ = lean_box(0);
v___x_700_ = lean_apply_1(v_h__4_692_, v___x_699_);
return v___x_700_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter___boxed(lean_object* v_motive_701_, lean_object* v_x_702_, lean_object* v_h__1_703_, lean_object* v_h__2_704_, lean_object* v_h__3_705_, lean_object* v_h__4_706_){
_start:
{
uint8_t v_x_61__boxed_707_; lean_object* v_res_708_; 
v_x_61__boxed_707_ = lean_unbox(v_x_702_);
v_res_708_ = lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_leftCoord_match__1_splitter(v_motive_701_, v_x_61__boxed_707_, v_h__1_703_, v_h__2_704_, v_h__3_705_, v_h__4_706_);
return v_res_708_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___redArg(uint8_t v_x_709_, uint8_t v_x_710_, lean_object* v_h__1_711_, lean_object* v_h__2_712_, lean_object* v_h__3_713_, lean_object* v_h__4_714_){
_start:
{
if (v_x_709_ == 0)
{
lean_dec(v_h__4_714_);
lean_dec(v_h__3_713_);
if (v_x_710_ == 0)
{
lean_object* v___x_715_; lean_object* v___x_716_; 
lean_dec(v_h__2_712_);
v___x_715_ = lean_box(0);
v___x_716_ = lean_apply_1(v_h__1_711_, v___x_715_);
return v___x_716_;
}
else
{
lean_object* v___x_717_; lean_object* v___x_718_; 
lean_dec(v_h__1_711_);
v___x_717_ = lean_box(0);
v___x_718_ = lean_apply_1(v_h__2_712_, v___x_717_);
return v___x_718_;
}
}
else
{
lean_dec(v_h__2_712_);
lean_dec(v_h__1_711_);
if (v_x_710_ == 0)
{
lean_object* v___x_719_; lean_object* v___x_720_; 
lean_dec(v_h__4_714_);
v___x_719_ = lean_box(0);
v___x_720_ = lean_apply_1(v_h__3_713_, v___x_719_);
return v___x_720_;
}
else
{
lean_object* v___x_721_; lean_object* v___x_722_; 
lean_dec(v_h__3_713_);
v___x_721_ = lean_box(0);
v___x_722_ = lean_apply_1(v_h__4_714_, v___x_721_);
return v___x_722_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___redArg___boxed(lean_object* v_x_723_, lean_object* v_x_724_, lean_object* v_h__1_725_, lean_object* v_h__2_726_, lean_object* v_h__3_727_, lean_object* v_h__4_728_){
_start:
{
uint8_t v_x_46__boxed_729_; uint8_t v_x_47__boxed_730_; lean_object* v_res_731_; 
v_x_46__boxed_729_ = lean_unbox(v_x_723_);
v_x_47__boxed_730_ = lean_unbox(v_x_724_);
v_res_731_ = lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___redArg(v_x_46__boxed_729_, v_x_47__boxed_730_, v_h__1_725_, v_h__2_726_, v_h__3_727_, v_h__4_728_);
return v_res_731_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter(lean_object* v_motive_732_, uint8_t v_x_733_, uint8_t v_x_734_, lean_object* v_h__1_735_, lean_object* v_h__2_736_, lean_object* v_h__3_737_, lean_object* v_h__4_738_){
_start:
{
if (v_x_733_ == 0)
{
lean_dec(v_h__4_738_);
lean_dec(v_h__3_737_);
if (v_x_734_ == 0)
{
lean_object* v___x_739_; lean_object* v___x_740_; 
lean_dec(v_h__2_736_);
v___x_739_ = lean_box(0);
v___x_740_ = lean_apply_1(v_h__1_735_, v___x_739_);
return v___x_740_;
}
else
{
lean_object* v___x_741_; lean_object* v___x_742_; 
lean_dec(v_h__1_735_);
v___x_741_ = lean_box(0);
v___x_742_ = lean_apply_1(v_h__2_736_, v___x_741_);
return v___x_742_;
}
}
else
{
lean_dec(v_h__2_736_);
lean_dec(v_h__1_735_);
if (v_x_734_ == 0)
{
lean_object* v___x_743_; lean_object* v___x_744_; 
lean_dec(v_h__4_738_);
v___x_743_ = lean_box(0);
v___x_744_ = lean_apply_1(v_h__3_737_, v___x_743_);
return v___x_744_;
}
else
{
lean_object* v___x_745_; lean_object* v___x_746_; 
lean_dec(v_h__3_737_);
v___x_745_ = lean_box(0);
v___x_746_ = lean_apply_1(v_h__4_738_, v___x_745_);
return v___x_746_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter___boxed(lean_object* v_motive_747_, lean_object* v_x_748_, lean_object* v_x_749_, lean_object* v_h__1_750_, lean_object* v_h__2_751_, lean_object* v_h__3_752_, lean_object* v_h__4_753_){
_start:
{
uint8_t v_x_68__boxed_754_; uint8_t v_x_69__boxed_755_; lean_object* v_res_756_; 
v_x_68__boxed_754_ = lean_unbox(v_x_748_);
v_x_69__boxed_755_ = lean_unbox(v_x_749_);
v_res_756_ = lp_FiniteQuantum___private_WorldRebitHiddenDirection_0__OmegaWorld_RebitQ9_jEntry_match__1_splitter(v_motive_747_, v_x_68__boxed_754_, v_x_69__boxed_755_, v_h__1_750_, v_h__2_751_, v_h__3_752_, v_h__4_753_);
return v_res_756_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness___closed__0(void){
_start:
{
lean_object* v___x_757_; lean_object* v___x_758_; lean_object* v___x_759_; 
v___x_757_ = lean_box(0);
v___x_758_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_RebitQ9_deltaEntry___boxed), 2, 0);
v___x_759_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_759_, 0, v___x_758_);
lean_ctor_set(v___x_759_, 1, v___x_757_);
return v___x_759_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness(void){
_start:
{
lean_object* v___x_760_; 
v___x_760_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness___closed__0);
return v___x_760_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness___closed__0(void){
_start:
{
lean_object* v___x_761_; lean_object* v___x_762_; lean_object* v___x_763_; lean_object* v___x_764_; lean_object* v___x_765_; 
v___x_761_ = lean_box(0);
v___x_762_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoMinusScaled___boxed), 2, 0);
v___x_763_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPlusScaled___boxed), 2, 0);
v___x_764_ = lean_unsigned_to_nat(16u);
v___x_765_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_765_, 0, v___x_764_);
lean_ctor_set(v___x_765_, 1, v___x_763_);
lean_ctor_set(v___x_765_, 2, v___x_762_);
lean_ctor_set(v___x_765_, 3, v___x_761_);
return v___x_765_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness(void){
_start:
{
lean_object* v___x_766_; 
v___x_766_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness___closed__0, &lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness___closed__0);
return v___x_766_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldRebitHiddenDirection(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness = _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_RebitQ9_hiddenDirectionWitness);
lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness = _init_lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_RebitQ9_rhoPairWitness);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
