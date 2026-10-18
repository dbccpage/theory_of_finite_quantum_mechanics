// Lean compiler output
// Module: WorldCovariantWignerYanase
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
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_int_sub(lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
lean_object* lean_int_mul(lean_object*, lean_object*);
lean_object* lean_int_add(lean_object*, lean_object*);
lean_object* lean_int_neg(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_toCtorIdx(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqQ10AuthorityEffect(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqQ10AuthorityEffect___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqCoord2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqCoord2___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqFactorCoord4(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqFactorCoord4___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixAdd(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixAdd___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixSub(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixSub___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scaleMatrix(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scaleMatrix___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixTranspose(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixTranspose___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_trace2(lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_commutator(lean_object*, lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_commutator___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pZero(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pZero___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pOne(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pOne___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_dephaseZ(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_dephaseZ___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_gram2(lean_object*, uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_gram2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewNumerator(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator(lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRho(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRho___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRoot(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRoot___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputGramFactor(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputGramFactor___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputStateGramFactor(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputStateGramFactor___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___boxed(lean_object*, lean_object*);
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRootGram;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput___closed__0;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput;
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___redArg(uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter(lean_object*, uint8_t, uint8_t, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_closure_object lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_dephaseZ___boxed, .m_arity = 3, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__0 = (const lean_object*)&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__0_value;
static lean_once_cell_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__1;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness;
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_toCtorIdx(lean_object* v_x_1_){
_start:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_ofNat(lean_object* v_n_3_){
_start:
{
lean_object* v___x_4_; 
v___x_4_ = lean_box(0);
return v___x_4_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_ofNat___boxed(lean_object* v_n_5_){
_start:
{
lean_object* v_res_6_; 
v_res_6_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Q10AuthorityEffect_ofNat(v_n_5_);
lean_dec(v_n_5_);
return v_res_6_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqQ10AuthorityEffect(lean_object* v_x_7_, lean_object* v_y_8_){
_start:
{
uint8_t v___x_9_; 
v___x_9_ = 1;
return v___x_9_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqQ10AuthorityEffect___boxed(lean_object* v_x_10_, lean_object* v_y_11_){
_start:
{
uint8_t v_res_12_; lean_object* v_r_13_; 
v_res_12_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqQ10AuthorityEffect(v_x_10_, v_y_11_);
v_r_13_ = lean_box(v_res_12_);
return v_r_13_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx(uint8_t v_x_14_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx___boxed(lean_object* v_x_17_){
_start:
{
uint8_t v_x_boxed_18_; lean_object* v_res_19_; 
v_x_boxed_18_ = lean_unbox(v_x_17_);
v_res_19_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx(v_x_boxed_18_);
return v_res_19_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_toCtorIdx(uint8_t v_x_20_){
_start:
{
lean_object* v___x_21_; 
v___x_21_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx(v_x_20_);
return v___x_21_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_toCtorIdx___boxed(lean_object* v_x_22_){
_start:
{
uint8_t v_x_4__boxed_23_; lean_object* v_res_24_; 
v_x_4__boxed_23_ = lean_unbox(v_x_22_);
v_res_24_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_toCtorIdx(v_x_4__boxed_23_);
return v_res_24_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___redArg(lean_object* v_k_25_){
_start:
{
lean_inc(v_k_25_);
return v_k_25_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___redArg___boxed(lean_object* v_k_26_){
_start:
{
lean_object* v_res_27_; 
v_res_27_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___redArg(v_k_26_);
lean_dec(v_k_26_);
return v_res_27_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim(lean_object* v_motive_28_, lean_object* v_ctorIdx_29_, uint8_t v_t_30_, lean_object* v_h_31_, lean_object* v_k_32_){
_start:
{
lean_inc(v_k_32_);
return v_k_32_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim___boxed(lean_object* v_motive_33_, lean_object* v_ctorIdx_34_, lean_object* v_t_35_, lean_object* v_h_36_, lean_object* v_k_37_){
_start:
{
uint8_t v_t_boxed_38_; lean_object* v_res_39_; 
v_t_boxed_38_ = lean_unbox(v_t_35_);
v_res_39_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorElim(v_motive_33_, v_ctorIdx_34_, v_t_boxed_38_, v_h_36_, v_k_37_);
lean_dec(v_k_37_);
lean_dec(v_ctorIdx_34_);
return v_res_39_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___redArg(lean_object* v_zero_40_){
_start:
{
lean_inc(v_zero_40_);
return v_zero_40_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___redArg___boxed(lean_object* v_zero_41_){
_start:
{
lean_object* v_res_42_; 
v_res_42_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___redArg(v_zero_41_);
lean_dec(v_zero_41_);
return v_res_42_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim(lean_object* v_motive_43_, uint8_t v_t_44_, lean_object* v_h_45_, lean_object* v_zero_46_){
_start:
{
lean_inc(v_zero_46_);
return v_zero_46_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim___boxed(lean_object* v_motive_47_, lean_object* v_t_48_, lean_object* v_h_49_, lean_object* v_zero_50_){
_start:
{
uint8_t v_t_boxed_51_; lean_object* v_res_52_; 
v_t_boxed_51_ = lean_unbox(v_t_48_);
v_res_52_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_zero_elim(v_motive_47_, v_t_boxed_51_, v_h_49_, v_zero_50_);
lean_dec(v_zero_50_);
return v_res_52_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___redArg(lean_object* v_one_53_){
_start:
{
lean_inc(v_one_53_);
return v_one_53_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___redArg___boxed(lean_object* v_one_54_){
_start:
{
lean_object* v_res_55_; 
v_res_55_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___redArg(v_one_54_);
lean_dec(v_one_54_);
return v_res_55_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim(lean_object* v_motive_56_, uint8_t v_t_57_, lean_object* v_h_58_, lean_object* v_one_59_){
_start:
{
lean_inc(v_one_59_);
return v_one_59_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim___boxed(lean_object* v_motive_60_, lean_object* v_t_61_, lean_object* v_h_62_, lean_object* v_one_63_){
_start:
{
uint8_t v_t_boxed_64_; lean_object* v_res_65_; 
v_t_boxed_64_ = lean_unbox(v_t_61_);
v_res_65_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_one_elim(v_motive_60_, v_t_boxed_64_, v_h_62_, v_one_63_);
lean_dec(v_one_63_);
return v_res_65_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ofNat(lean_object* v_n_66_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ofNat___boxed(lean_object* v_n_71_){
_start:
{
uint8_t v_res_72_; lean_object* v_r_73_; 
v_res_72_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ofNat(v_n_71_);
lean_dec(v_n_71_);
v_r_73_ = lean_box(v_res_72_);
return v_r_73_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqCoord2(uint8_t v_x_74_, uint8_t v_y_75_){
_start:
{
lean_object* v___x_76_; lean_object* v___x_77_; uint8_t v___x_78_; 
v___x_76_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx(v_x_74_);
v___x_77_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_Coord2_ctorIdx(v_y_75_);
v___x_78_ = lean_nat_dec_eq(v___x_76_, v___x_77_);
lean_dec(v___x_77_);
lean_dec(v___x_76_);
return v___x_78_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqCoord2___boxed(lean_object* v_x_79_, lean_object* v_y_80_){
_start:
{
uint8_t v_x_13__boxed_81_; uint8_t v_y_14__boxed_82_; uint8_t v_res_83_; lean_object* v_r_84_; 
v_x_13__boxed_81_ = lean_unbox(v_x_79_);
v_y_14__boxed_82_ = lean_unbox(v_y_80_);
v_res_83_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqCoord2(v_x_13__boxed_81_, v_y_14__boxed_82_);
v_r_84_ = lean_box(v_res_83_);
return v_r_84_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx(uint8_t v_x_85_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx___boxed(lean_object* v_x_90_){
_start:
{
uint8_t v_x_boxed_91_; lean_object* v_res_92_; 
v_x_boxed_91_ = lean_unbox(v_x_90_);
v_res_92_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx(v_x_boxed_91_);
return v_res_92_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_toCtorIdx(uint8_t v_x_93_){
_start:
{
lean_object* v___x_94_; 
v___x_94_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx(v_x_93_);
return v___x_94_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_toCtorIdx___boxed(lean_object* v_x_95_){
_start:
{
uint8_t v_x_4__boxed_96_; lean_object* v_res_97_; 
v_x_4__boxed_96_ = lean_unbox(v_x_95_);
v_res_97_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_toCtorIdx(v_x_4__boxed_96_);
return v_res_97_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___redArg(lean_object* v_k_98_){
_start:
{
lean_inc(v_k_98_);
return v_k_98_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___redArg___boxed(lean_object* v_k_99_){
_start:
{
lean_object* v_res_100_; 
v_res_100_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___redArg(v_k_99_);
lean_dec(v_k_99_);
return v_res_100_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim(lean_object* v_motive_101_, lean_object* v_ctorIdx_102_, uint8_t v_t_103_, lean_object* v_h_104_, lean_object* v_k_105_){
_start:
{
lean_inc(v_k_105_);
return v_k_105_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim___boxed(lean_object* v_motive_106_, lean_object* v_ctorIdx_107_, lean_object* v_t_108_, lean_object* v_h_109_, lean_object* v_k_110_){
_start:
{
uint8_t v_t_boxed_111_; lean_object* v_res_112_; 
v_t_boxed_111_ = lean_unbox(v_t_108_);
v_res_112_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorElim(v_motive_106_, v_ctorIdx_107_, v_t_boxed_111_, v_h_109_, v_k_110_);
lean_dec(v_k_110_);
lean_dec(v_ctorIdx_107_);
return v_res_112_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___redArg(lean_object* v_a_113_){
_start:
{
lean_inc(v_a_113_);
return v_a_113_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___redArg___boxed(lean_object* v_a_114_){
_start:
{
lean_object* v_res_115_; 
v_res_115_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___redArg(v_a_114_);
lean_dec(v_a_114_);
return v_res_115_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim(lean_object* v_motive_116_, uint8_t v_t_117_, lean_object* v_h_118_, lean_object* v_a_119_){
_start:
{
lean_inc(v_a_119_);
return v_a_119_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim___boxed(lean_object* v_motive_120_, lean_object* v_t_121_, lean_object* v_h_122_, lean_object* v_a_123_){
_start:
{
uint8_t v_t_boxed_124_; lean_object* v_res_125_; 
v_t_boxed_124_ = lean_unbox(v_t_121_);
v_res_125_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_a_elim(v_motive_120_, v_t_boxed_124_, v_h_122_, v_a_123_);
lean_dec(v_a_123_);
return v_res_125_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___redArg(lean_object* v_b_126_){
_start:
{
lean_inc(v_b_126_);
return v_b_126_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___redArg___boxed(lean_object* v_b_127_){
_start:
{
lean_object* v_res_128_; 
v_res_128_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___redArg(v_b_127_);
lean_dec(v_b_127_);
return v_res_128_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim(lean_object* v_motive_129_, uint8_t v_t_130_, lean_object* v_h_131_, lean_object* v_b_132_){
_start:
{
lean_inc(v_b_132_);
return v_b_132_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim___boxed(lean_object* v_motive_133_, lean_object* v_t_134_, lean_object* v_h_135_, lean_object* v_b_136_){
_start:
{
uint8_t v_t_boxed_137_; lean_object* v_res_138_; 
v_t_boxed_137_ = lean_unbox(v_t_134_);
v_res_138_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_b_elim(v_motive_133_, v_t_boxed_137_, v_h_135_, v_b_136_);
lean_dec(v_b_136_);
return v_res_138_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___redArg(lean_object* v_c_139_){
_start:
{
lean_inc(v_c_139_);
return v_c_139_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___redArg___boxed(lean_object* v_c_140_){
_start:
{
lean_object* v_res_141_; 
v_res_141_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___redArg(v_c_140_);
lean_dec(v_c_140_);
return v_res_141_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim(lean_object* v_motive_142_, uint8_t v_t_143_, lean_object* v_h_144_, lean_object* v_c_145_){
_start:
{
lean_inc(v_c_145_);
return v_c_145_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim___boxed(lean_object* v_motive_146_, lean_object* v_t_147_, lean_object* v_h_148_, lean_object* v_c_149_){
_start:
{
uint8_t v_t_boxed_150_; lean_object* v_res_151_; 
v_t_boxed_150_ = lean_unbox(v_t_147_);
v_res_151_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_c_elim(v_motive_146_, v_t_boxed_150_, v_h_148_, v_c_149_);
lean_dec(v_c_149_);
return v_res_151_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___redArg(lean_object* v_d_152_){
_start:
{
lean_inc(v_d_152_);
return v_d_152_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___redArg___boxed(lean_object* v_d_153_){
_start:
{
lean_object* v_res_154_; 
v_res_154_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___redArg(v_d_153_);
lean_dec(v_d_153_);
return v_res_154_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim(lean_object* v_motive_155_, uint8_t v_t_156_, lean_object* v_h_157_, lean_object* v_d_158_){
_start:
{
lean_inc(v_d_158_);
return v_d_158_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim___boxed(lean_object* v_motive_159_, lean_object* v_t_160_, lean_object* v_h_161_, lean_object* v_d_162_){
_start:
{
uint8_t v_t_boxed_163_; lean_object* v_res_164_; 
v_t_boxed_163_ = lean_unbox(v_t_160_);
v_res_164_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_d_elim(v_motive_159_, v_t_boxed_163_, v_h_161_, v_d_162_);
lean_dec(v_d_162_);
return v_res_164_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ofNat(lean_object* v_n_165_){
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
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ofNat___boxed(lean_object* v_n_176_){
_start:
{
uint8_t v_res_177_; lean_object* v_r_178_; 
v_res_177_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ofNat(v_n_176_);
lean_dec(v_n_176_);
v_r_178_ = lean_box(v_res_177_);
return v_r_178_;
}
}
LEAN_EXPORT uint8_t lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqFactorCoord4(uint8_t v_x_179_, uint8_t v_y_180_){
_start:
{
lean_object* v___x_181_; lean_object* v___x_182_; uint8_t v___x_183_; 
v___x_181_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx(v_x_179_);
v___x_182_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_FactorCoord4_ctorIdx(v_y_180_);
v___x_183_ = lean_nat_dec_eq(v___x_181_, v___x_182_);
lean_dec(v___x_182_);
lean_dec(v___x_181_);
return v___x_183_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqFactorCoord4___boxed(lean_object* v_x_184_, lean_object* v_y_185_){
_start:
{
uint8_t v_x_13__boxed_186_; uint8_t v_y_14__boxed_187_; uint8_t v_res_188_; lean_object* v_r_189_; 
v_x_13__boxed_186_ = lean_unbox(v_x_184_);
v_y_14__boxed_187_ = lean_unbox(v_y_185_);
v_res_188_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_instDecidableEqFactorCoord4(v_x_13__boxed_186_, v_y_14__boxed_187_);
v_r_189_ = lean_box(v_res_188_);
return v_r_189_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixAdd(lean_object* v_left_190_, lean_object* v_right_191_, uint8_t v_row_192_, uint8_t v_column_193_){
_start:
{
lean_object* v___x_194_; lean_object* v___x_195_; lean_object* v___x_196_; lean_object* v___x_197_; lean_object* v___x_198_; lean_object* v___x_199_; lean_object* v___x_200_; 
v___x_194_ = lean_box(v_row_192_);
v___x_195_ = lean_box(v_column_193_);
v___x_196_ = lean_apply_2(v_left_190_, v___x_194_, v___x_195_);
v___x_197_ = lean_box(v_row_192_);
v___x_198_ = lean_box(v_column_193_);
v___x_199_ = lean_apply_2(v_right_191_, v___x_197_, v___x_198_);
v___x_200_ = lean_int_add(v___x_196_, v___x_199_);
lean_dec(v___x_199_);
lean_dec(v___x_196_);
return v___x_200_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixAdd___boxed(lean_object* v_left_201_, lean_object* v_right_202_, lean_object* v_row_203_, lean_object* v_column_204_){
_start:
{
uint8_t v_row_boxed_205_; uint8_t v_column_boxed_206_; lean_object* v_res_207_; 
v_row_boxed_205_ = lean_unbox(v_row_203_);
v_column_boxed_206_ = lean_unbox(v_column_204_);
v_res_207_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixAdd(v_left_201_, v_right_202_, v_row_boxed_205_, v_column_boxed_206_);
return v_res_207_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixSub(lean_object* v_left_208_, lean_object* v_right_209_, uint8_t v_row_210_, uint8_t v_column_211_){
_start:
{
lean_object* v___x_212_; lean_object* v___x_213_; lean_object* v___x_214_; lean_object* v___x_215_; lean_object* v___x_216_; lean_object* v___x_217_; lean_object* v___x_218_; 
v___x_212_ = lean_box(v_row_210_);
v___x_213_ = lean_box(v_column_211_);
v___x_214_ = lean_apply_2(v_left_208_, v___x_212_, v___x_213_);
v___x_215_ = lean_box(v_row_210_);
v___x_216_ = lean_box(v_column_211_);
v___x_217_ = lean_apply_2(v_right_209_, v___x_215_, v___x_216_);
v___x_218_ = lean_int_sub(v___x_214_, v___x_217_);
lean_dec(v___x_217_);
lean_dec(v___x_214_);
return v___x_218_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixSub___boxed(lean_object* v_left_219_, lean_object* v_right_220_, lean_object* v_row_221_, lean_object* v_column_222_){
_start:
{
uint8_t v_row_boxed_223_; uint8_t v_column_boxed_224_; lean_object* v_res_225_; 
v_row_boxed_223_ = lean_unbox(v_row_221_);
v_column_boxed_224_ = lean_unbox(v_column_222_);
v_res_225_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixSub(v_left_219_, v_right_220_, v_row_boxed_223_, v_column_boxed_224_);
return v_res_225_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scaleMatrix(lean_object* v_scalar_226_, lean_object* v_matrix_227_, uint8_t v_row_228_, uint8_t v_column_229_){
_start:
{
lean_object* v___x_230_; lean_object* v___x_231_; lean_object* v___x_232_; lean_object* v___x_233_; 
v___x_230_ = lean_box(v_row_228_);
v___x_231_ = lean_box(v_column_229_);
v___x_232_ = lean_apply_2(v_matrix_227_, v___x_230_, v___x_231_);
v___x_233_ = lean_int_mul(v_scalar_226_, v___x_232_);
lean_dec(v___x_232_);
return v___x_233_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scaleMatrix___boxed(lean_object* v_scalar_234_, lean_object* v_matrix_235_, lean_object* v_row_236_, lean_object* v_column_237_){
_start:
{
uint8_t v_row_boxed_238_; uint8_t v_column_boxed_239_; lean_object* v_res_240_; 
v_row_boxed_238_ = lean_unbox(v_row_236_);
v_column_boxed_239_ = lean_unbox(v_column_237_);
v_res_240_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scaleMatrix(v_scalar_234_, v_matrix_235_, v_row_boxed_238_, v_column_boxed_239_);
lean_dec(v_scalar_234_);
return v_res_240_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixTranspose(lean_object* v_matrix_241_, uint8_t v_row_242_, uint8_t v_column_243_){
_start:
{
lean_object* v___x_244_; lean_object* v___x_245_; lean_object* v___x_246_; 
v___x_244_ = lean_box(v_column_243_);
v___x_245_ = lean_box(v_row_242_);
v___x_246_ = lean_apply_2(v_matrix_241_, v___x_244_, v___x_245_);
return v___x_246_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixTranspose___boxed(lean_object* v_matrix_247_, lean_object* v_row_248_, lean_object* v_column_249_){
_start:
{
uint8_t v_row_boxed_250_; uint8_t v_column_boxed_251_; lean_object* v_res_252_; 
v_row_boxed_250_ = lean_unbox(v_row_248_);
v_column_boxed_251_ = lean_unbox(v_column_249_);
v_res_252_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixTranspose(v_matrix_247_, v_row_boxed_250_, v_column_boxed_251_);
return v_res_252_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul(lean_object* v_left_253_, lean_object* v_right_254_, uint8_t v_row_255_, uint8_t v_column_256_){
_start:
{
uint8_t v___x_257_; lean_object* v___x_258_; lean_object* v___x_259_; lean_object* v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; lean_object* v___x_263_; lean_object* v___x_264_; uint8_t v___x_265_; lean_object* v___x_266_; lean_object* v___x_267_; lean_object* v___x_268_; lean_object* v___x_269_; lean_object* v___x_270_; lean_object* v___x_271_; lean_object* v___x_272_; lean_object* v___x_273_; 
v___x_257_ = 0;
v___x_258_ = lean_box(v_row_255_);
v___x_259_ = lean_box(v___x_257_);
lean_inc_ref(v_left_253_);
v___x_260_ = lean_apply_2(v_left_253_, v___x_258_, v___x_259_);
v___x_261_ = lean_box(v___x_257_);
v___x_262_ = lean_box(v_column_256_);
lean_inc_ref(v_right_254_);
v___x_263_ = lean_apply_2(v_right_254_, v___x_261_, v___x_262_);
v___x_264_ = lean_int_mul(v___x_260_, v___x_263_);
lean_dec(v___x_263_);
lean_dec(v___x_260_);
v___x_265_ = 1;
v___x_266_ = lean_box(v_row_255_);
v___x_267_ = lean_box(v___x_265_);
v___x_268_ = lean_apply_2(v_left_253_, v___x_266_, v___x_267_);
v___x_269_ = lean_box(v___x_265_);
v___x_270_ = lean_box(v_column_256_);
v___x_271_ = lean_apply_2(v_right_254_, v___x_269_, v___x_270_);
v___x_272_ = lean_int_mul(v___x_268_, v___x_271_);
lean_dec(v___x_271_);
lean_dec(v___x_268_);
v___x_273_ = lean_int_add(v___x_264_, v___x_272_);
lean_dec(v___x_272_);
lean_dec(v___x_264_);
return v___x_273_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul___boxed(lean_object* v_left_274_, lean_object* v_right_275_, lean_object* v_row_276_, lean_object* v_column_277_){
_start:
{
uint8_t v_row_boxed_278_; uint8_t v_column_boxed_279_; lean_object* v_res_280_; 
v_row_boxed_278_ = lean_unbox(v_row_276_);
v_column_boxed_279_ = lean_unbox(v_column_277_);
v_res_280_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul(v_left_274_, v_right_275_, v_row_boxed_278_, v_column_boxed_279_);
return v_res_280_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_trace2(lean_object* v_matrix_281_){
_start:
{
uint8_t v___x_282_; lean_object* v___x_283_; lean_object* v___x_284_; lean_object* v___x_285_; uint8_t v___x_286_; lean_object* v___x_287_; lean_object* v___x_288_; lean_object* v___x_289_; lean_object* v___x_290_; 
v___x_282_ = 0;
v___x_283_ = lean_box(v___x_282_);
v___x_284_ = lean_box(v___x_282_);
lean_inc_ref(v_matrix_281_);
v___x_285_ = lean_apply_2(v_matrix_281_, v___x_283_, v___x_284_);
v___x_286_ = 1;
v___x_287_ = lean_box(v___x_286_);
v___x_288_ = lean_box(v___x_286_);
v___x_289_ = lean_apply_2(v_matrix_281_, v___x_287_, v___x_288_);
v___x_290_ = lean_int_add(v___x_285_, v___x_289_);
lean_dec(v___x_289_);
lean_dec(v___x_285_);
return v___x_290_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_commutator(lean_object* v_left_291_, lean_object* v_right_292_, uint8_t v_a_293_, uint8_t v_a_294_){
_start:
{
lean_object* v___x_295_; lean_object* v___x_296_; lean_object* v___x_297_; 
lean_inc_ref(v_right_292_);
lean_inc_ref(v_left_291_);
v___x_295_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul___boxed), 4, 2);
lean_closure_set(v___x_295_, 0, v_left_291_);
lean_closure_set(v___x_295_, 1, v_right_292_);
v___x_296_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul___boxed), 4, 2);
lean_closure_set(v___x_296_, 0, v_right_292_);
lean_closure_set(v___x_296_, 1, v_left_291_);
v___x_297_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixSub(v___x_295_, v___x_296_, v_a_293_, v_a_294_);
return v___x_297_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_commutator___boxed(lean_object* v_left_298_, lean_object* v_right_299_, lean_object* v_a_300_, lean_object* v_a_301_){
_start:
{
uint8_t v_a_7__boxed_302_; uint8_t v_a_8__boxed_303_; lean_object* v_res_304_; 
v_a_7__boxed_302_ = lean_unbox(v_a_300_);
v_a_8__boxed_303_ = lean_unbox(v_a_301_);
v_res_304_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_commutator(v_left_298_, v_right_299_, v_a_7__boxed_302_, v_a_8__boxed_303_);
return v_res_304_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0(void){
_start:
{
lean_object* v___x_305_; lean_object* v___x_306_; 
v___x_305_ = lean_unsigned_to_nat(1u);
v___x_306_ = lean_nat_to_int(v___x_305_);
return v___x_306_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1(void){
_start:
{
lean_object* v___x_307_; lean_object* v___x_308_; 
v___x_307_ = lean_unsigned_to_nat(0u);
v___x_308_ = lean_nat_to_int(v___x_307_);
return v___x_308_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2(uint8_t v_x_309_, uint8_t v_x_310_){
_start:
{
if (v_x_309_ == 0)
{
if (v_x_310_ == 0)
{
goto v___jp_311_;
}
else
{
goto v___jp_313_;
}
}
else
{
if (v_x_310_ == 1)
{
goto v___jp_311_;
}
else
{
goto v___jp_313_;
}
}
v___jp_311_:
{
lean_object* v___x_312_; 
v___x_312_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0);
return v___x_312_;
}
v___jp_313_:
{
lean_object* v___x_314_; 
v___x_314_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_314_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___boxed(lean_object* v_x_315_, lean_object* v_x_316_){
_start:
{
uint8_t v_x_54__boxed_317_; uint8_t v_x_55__boxed_318_; lean_object* v_res_319_; 
v_x_54__boxed_317_ = lean_unbox(v_x_315_);
v_x_55__boxed_318_ = lean_unbox(v_x_316_);
v_res_319_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2(v_x_54__boxed_317_, v_x_55__boxed_318_);
return v_res_319_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___closed__0(void){
_start:
{
lean_object* v___x_320_; lean_object* v___x_321_; 
v___x_320_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0);
v___x_321_ = lean_int_neg(v___x_320_);
return v___x_321_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable(uint8_t v_x_322_, uint8_t v_x_323_){
_start:
{
if (v_x_322_ == 0)
{
if (v_x_323_ == 0)
{
lean_object* v___x_326_; 
v___x_326_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0);
return v___x_326_;
}
else
{
goto v___jp_324_;
}
}
else
{
if (v_x_323_ == 1)
{
lean_object* v___x_327_; 
v___x_327_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___closed__0);
return v___x_327_;
}
else
{
goto v___jp_324_;
}
}
v___jp_324_:
{
lean_object* v___x_325_; 
v___x_325_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_325_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable___boxed(lean_object* v_x_328_, lean_object* v_x_329_){
_start:
{
uint8_t v_x_71__boxed_330_; uint8_t v_x_72__boxed_331_; lean_object* v_res_332_; 
v_x_71__boxed_330_ = lean_unbox(v_x_328_);
v_x_72__boxed_331_ = lean_unbox(v_x_329_);
v_res_332_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_zObservable(v_x_71__boxed_330_, v_x_72__boxed_331_);
return v_res_332_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pZero(uint8_t v_x_333_, uint8_t v_x_334_){
_start:
{
if (v_x_333_ == 0)
{
if (v_x_334_ == 0)
{
lean_object* v___x_337_; 
v___x_337_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0);
return v___x_337_;
}
else
{
goto v___jp_335_;
}
}
else
{
goto v___jp_335_;
}
v___jp_335_:
{
lean_object* v___x_336_; 
v___x_336_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_336_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pZero___boxed(lean_object* v_x_338_, lean_object* v_x_339_){
_start:
{
uint8_t v_x_44__boxed_340_; uint8_t v_x_45__boxed_341_; lean_object* v_res_342_; 
v_x_44__boxed_340_ = lean_unbox(v_x_338_);
v_x_45__boxed_341_ = lean_unbox(v_x_339_);
v_res_342_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pZero(v_x_44__boxed_340_, v_x_45__boxed_341_);
return v_res_342_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pOne(uint8_t v_x_343_, uint8_t v_x_344_){
_start:
{
if (v_x_343_ == 1)
{
if (v_x_344_ == 1)
{
lean_object* v___x_347_; 
v___x_347_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0);
return v___x_347_;
}
else
{
goto v___jp_345_;
}
}
else
{
goto v___jp_345_;
}
v___jp_345_:
{
lean_object* v___x_346_; 
v___x_346_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_346_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pOne___boxed(lean_object* v_x_348_, lean_object* v_x_349_){
_start:
{
uint8_t v_x_44__boxed_350_; uint8_t v_x_45__boxed_351_; lean_object* v_res_352_; 
v_x_44__boxed_350_ = lean_unbox(v_x_348_);
v_x_45__boxed_351_ = lean_unbox(v_x_349_);
v_res_352_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_pOne(v_x_44__boxed_350_, v_x_45__boxed_351_);
return v_res_352_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_dephaseZ(lean_object* v_matrix_353_, uint8_t v_x_354_, uint8_t v_x_355_){
_start:
{
if (v_x_354_ == 0)
{
if (v_x_355_ == 0)
{
lean_object* v___x_358_; lean_object* v___x_359_; lean_object* v___x_360_; 
v___x_358_ = lean_box(v_x_355_);
v___x_359_ = lean_box(v_x_355_);
v___x_360_ = lean_apply_2(v_matrix_353_, v___x_358_, v___x_359_);
return v___x_360_;
}
else
{
lean_dec_ref(v_matrix_353_);
goto v___jp_356_;
}
}
else
{
if (v_x_355_ == 1)
{
lean_object* v___x_361_; lean_object* v___x_362_; lean_object* v___x_363_; 
v___x_361_ = lean_box(v_x_355_);
v___x_362_ = lean_box(v_x_355_);
v___x_363_ = lean_apply_2(v_matrix_353_, v___x_361_, v___x_362_);
return v___x_363_;
}
else
{
lean_dec_ref(v_matrix_353_);
goto v___jp_356_;
}
}
v___jp_356_:
{
lean_object* v___x_357_; 
v___x_357_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_357_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_dephaseZ___boxed(lean_object* v_matrix_364_, lean_object* v_x_365_, lean_object* v_x_366_){
_start:
{
uint8_t v_x_51__boxed_367_; uint8_t v_x_52__boxed_368_; lean_object* v_res_369_; 
v_x_51__boxed_367_ = lean_unbox(v_x_365_);
v_x_52__boxed_368_ = lean_unbox(v_x_366_);
v_res_369_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_dephaseZ(v_matrix_364_, v_x_51__boxed_367_, v_x_52__boxed_368_);
return v_res_369_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___redArg(uint8_t v_x_370_, uint8_t v_x_371_, lean_object* v_h__1_372_, lean_object* v_h__2_373_, lean_object* v_h__3_374_){
_start:
{
if (v_x_370_ == 0)
{
lean_dec(v_h__2_373_);
if (v_x_371_ == 0)
{
lean_object* v___x_375_; lean_object* v___x_376_; 
lean_dec(v_h__3_374_);
v___x_375_ = lean_box(0);
v___x_376_ = lean_apply_1(v_h__1_372_, v___x_375_);
return v___x_376_;
}
else
{
lean_object* v___x_377_; lean_object* v___x_378_; lean_object* v___x_379_; 
lean_dec(v_h__1_372_);
v___x_377_ = lean_box(v_x_370_);
v___x_378_ = lean_box(v_x_371_);
v___x_379_ = lean_apply_4(v_h__3_374_, v___x_377_, v___x_378_, lean_box(0), lean_box(0));
return v___x_379_;
}
}
else
{
lean_dec(v_h__1_372_);
if (v_x_371_ == 1)
{
lean_object* v___x_380_; lean_object* v___x_381_; 
lean_dec(v_h__3_374_);
v___x_380_ = lean_box(0);
v___x_381_ = lean_apply_1(v_h__2_373_, v___x_380_);
return v___x_381_;
}
else
{
lean_object* v___x_382_; lean_object* v___x_383_; lean_object* v___x_384_; 
lean_dec(v_h__2_373_);
v___x_382_ = lean_box(v_x_370_);
v___x_383_ = lean_box(v_x_371_);
v___x_384_ = lean_apply_4(v_h__3_374_, v___x_382_, v___x_383_, lean_box(0), lean_box(0));
return v___x_384_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___redArg___boxed(lean_object* v_x_385_, lean_object* v_x_386_, lean_object* v_h__1_387_, lean_object* v_h__2_388_, lean_object* v_h__3_389_){
_start:
{
uint8_t v_x_36__boxed_390_; uint8_t v_x_37__boxed_391_; lean_object* v_res_392_; 
v_x_36__boxed_390_ = lean_unbox(v_x_385_);
v_x_37__boxed_391_ = lean_unbox(v_x_386_);
v_res_392_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___redArg(v_x_36__boxed_390_, v_x_37__boxed_391_, v_h__1_387_, v_h__2_388_, v_h__3_389_);
return v_res_392_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter(lean_object* v_motive_393_, uint8_t v_x_394_, uint8_t v_x_395_, lean_object* v_h__1_396_, lean_object* v_h__2_397_, lean_object* v_h__3_398_){
_start:
{
if (v_x_394_ == 0)
{
lean_dec(v_h__2_397_);
if (v_x_395_ == 0)
{
lean_object* v___x_399_; lean_object* v___x_400_; 
lean_dec(v_h__3_398_);
v___x_399_ = lean_box(0);
v___x_400_ = lean_apply_1(v_h__1_396_, v___x_399_);
return v___x_400_;
}
else
{
lean_object* v___x_401_; lean_object* v___x_402_; lean_object* v___x_403_; 
lean_dec(v_h__1_396_);
v___x_401_ = lean_box(v_x_394_);
v___x_402_ = lean_box(v_x_395_);
v___x_403_ = lean_apply_4(v_h__3_398_, v___x_401_, v___x_402_, lean_box(0), lean_box(0));
return v___x_403_;
}
}
else
{
lean_dec(v_h__1_396_);
if (v_x_395_ == 1)
{
lean_object* v___x_404_; lean_object* v___x_405_; 
lean_dec(v_h__3_398_);
v___x_404_ = lean_box(0);
v___x_405_ = lean_apply_1(v_h__2_397_, v___x_404_);
return v___x_405_;
}
else
{
lean_object* v___x_406_; lean_object* v___x_407_; lean_object* v___x_408_; 
lean_dec(v_h__2_397_);
v___x_406_ = lean_box(v_x_394_);
v___x_407_ = lean_box(v_x_395_);
v___x_408_ = lean_apply_4(v_h__3_398_, v___x_406_, v___x_407_, lean_box(0), lean_box(0));
return v___x_408_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter___boxed(lean_object* v_motive_409_, lean_object* v_x_410_, lean_object* v_x_411_, lean_object* v_h__1_412_, lean_object* v_h__2_413_, lean_object* v_h__3_414_){
_start:
{
uint8_t v_x_62__boxed_415_; uint8_t v_x_63__boxed_416_; lean_object* v_res_417_; 
v_x_62__boxed_415_ = lean_unbox(v_x_410_);
v_x_63__boxed_416_ = lean_unbox(v_x_411_);
v_res_417_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_identity2_match__1_splitter(v_motive_409_, v_x_62__boxed_415_, v_x_63__boxed_416_, v_h__1_412_, v_h__2_413_, v_h__3_414_);
return v_res_417_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___redArg(uint8_t v_x_418_, uint8_t v_x_419_, lean_object* v_h__1_420_, lean_object* v_h__2_421_){
_start:
{
if (v_x_418_ == 0)
{
if (v_x_419_ == 0)
{
lean_object* v___x_422_; lean_object* v___x_423_; 
lean_dec(v_h__2_421_);
v___x_422_ = lean_box(0);
v___x_423_ = lean_apply_1(v_h__1_420_, v___x_422_);
return v___x_423_;
}
else
{
lean_object* v___x_424_; lean_object* v___x_425_; lean_object* v___x_426_; 
lean_dec(v_h__1_420_);
v___x_424_ = lean_box(v_x_418_);
v___x_425_ = lean_box(v_x_419_);
v___x_426_ = lean_apply_3(v_h__2_421_, v___x_424_, v___x_425_, lean_box(0));
return v___x_426_;
}
}
else
{
lean_object* v___x_427_; lean_object* v___x_428_; lean_object* v___x_429_; 
lean_dec(v_h__1_420_);
v___x_427_ = lean_box(v_x_418_);
v___x_428_ = lean_box(v_x_419_);
v___x_429_ = lean_apply_3(v_h__2_421_, v___x_427_, v___x_428_, lean_box(0));
return v___x_429_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___redArg___boxed(lean_object* v_x_430_, lean_object* v_x_431_, lean_object* v_h__1_432_, lean_object* v_h__2_433_){
_start:
{
uint8_t v_x_28__boxed_434_; uint8_t v_x_29__boxed_435_; lean_object* v_res_436_; 
v_x_28__boxed_434_ = lean_unbox(v_x_430_);
v_x_29__boxed_435_ = lean_unbox(v_x_431_);
v_res_436_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___redArg(v_x_28__boxed_434_, v_x_29__boxed_435_, v_h__1_432_, v_h__2_433_);
return v_res_436_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter(lean_object* v_motive_437_, uint8_t v_x_438_, uint8_t v_x_439_, lean_object* v_h__1_440_, lean_object* v_h__2_441_){
_start:
{
if (v_x_438_ == 0)
{
if (v_x_439_ == 0)
{
lean_object* v___x_442_; lean_object* v___x_443_; 
lean_dec(v_h__2_441_);
v___x_442_ = lean_box(0);
v___x_443_ = lean_apply_1(v_h__1_440_, v___x_442_);
return v___x_443_;
}
else
{
lean_object* v___x_444_; lean_object* v___x_445_; lean_object* v___x_446_; 
lean_dec(v_h__1_440_);
v___x_444_ = lean_box(v_x_438_);
v___x_445_ = lean_box(v_x_439_);
v___x_446_ = lean_apply_3(v_h__2_441_, v___x_444_, v___x_445_, lean_box(0));
return v___x_446_;
}
}
else
{
lean_object* v___x_447_; lean_object* v___x_448_; lean_object* v___x_449_; 
lean_dec(v_h__1_440_);
v___x_447_ = lean_box(v_x_438_);
v___x_448_ = lean_box(v_x_439_);
v___x_449_ = lean_apply_3(v_h__2_441_, v___x_447_, v___x_448_, lean_box(0));
return v___x_449_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter___boxed(lean_object* v_motive_450_, lean_object* v_x_451_, lean_object* v_x_452_, lean_object* v_h__1_453_, lean_object* v_h__2_454_){
_start:
{
uint8_t v_x_50__boxed_455_; uint8_t v_x_51__boxed_456_; lean_object* v_res_457_; 
v_x_50__boxed_455_ = lean_unbox(v_x_451_);
v_x_51__boxed_456_ = lean_unbox(v_x_452_);
v_res_457_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pZero_match__1_splitter(v_motive_450_, v_x_50__boxed_455_, v_x_51__boxed_456_, v_h__1_453_, v_h__2_454_);
return v_res_457_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___redArg(uint8_t v_x_458_, uint8_t v_x_459_, lean_object* v_h__1_460_, lean_object* v_h__2_461_){
_start:
{
if (v_x_458_ == 1)
{
if (v_x_459_ == 1)
{
lean_object* v___x_462_; lean_object* v___x_463_; 
lean_dec(v_h__2_461_);
v___x_462_ = lean_box(0);
v___x_463_ = lean_apply_1(v_h__1_460_, v___x_462_);
return v___x_463_;
}
else
{
lean_object* v___x_464_; lean_object* v___x_465_; lean_object* v___x_466_; 
lean_dec(v_h__1_460_);
v___x_464_ = lean_box(v_x_458_);
v___x_465_ = lean_box(v_x_459_);
v___x_466_ = lean_apply_3(v_h__2_461_, v___x_464_, v___x_465_, lean_box(0));
return v___x_466_;
}
}
else
{
lean_object* v___x_467_; lean_object* v___x_468_; lean_object* v___x_469_; 
lean_dec(v_h__1_460_);
v___x_467_ = lean_box(v_x_458_);
v___x_468_ = lean_box(v_x_459_);
v___x_469_ = lean_apply_3(v_h__2_461_, v___x_467_, v___x_468_, lean_box(0));
return v___x_469_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___redArg___boxed(lean_object* v_x_470_, lean_object* v_x_471_, lean_object* v_h__1_472_, lean_object* v_h__2_473_){
_start:
{
uint8_t v_x_28__boxed_474_; uint8_t v_x_29__boxed_475_; lean_object* v_res_476_; 
v_x_28__boxed_474_ = lean_unbox(v_x_470_);
v_x_29__boxed_475_ = lean_unbox(v_x_471_);
v_res_476_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___redArg(v_x_28__boxed_474_, v_x_29__boxed_475_, v_h__1_472_, v_h__2_473_);
return v_res_476_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter(lean_object* v_motive_477_, uint8_t v_x_478_, uint8_t v_x_479_, lean_object* v_h__1_480_, lean_object* v_h__2_481_){
_start:
{
if (v_x_478_ == 1)
{
if (v_x_479_ == 1)
{
lean_object* v___x_482_; lean_object* v___x_483_; 
lean_dec(v_h__2_481_);
v___x_482_ = lean_box(0);
v___x_483_ = lean_apply_1(v_h__1_480_, v___x_482_);
return v___x_483_;
}
else
{
lean_object* v___x_484_; lean_object* v___x_485_; lean_object* v___x_486_; 
lean_dec(v_h__1_480_);
v___x_484_ = lean_box(v_x_478_);
v___x_485_ = lean_box(v_x_479_);
v___x_486_ = lean_apply_3(v_h__2_481_, v___x_484_, v___x_485_, lean_box(0));
return v___x_486_;
}
}
else
{
lean_object* v___x_487_; lean_object* v___x_488_; lean_object* v___x_489_; 
lean_dec(v_h__1_480_);
v___x_487_ = lean_box(v_x_478_);
v___x_488_ = lean_box(v_x_479_);
v___x_489_ = lean_apply_3(v_h__2_481_, v___x_487_, v___x_488_, lean_box(0));
return v___x_489_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter___boxed(lean_object* v_motive_490_, lean_object* v_x_491_, lean_object* v_x_492_, lean_object* v_h__1_493_, lean_object* v_h__2_494_){
_start:
{
uint8_t v_x_50__boxed_495_; uint8_t v_x_51__boxed_496_; lean_object* v_res_497_; 
v_x_50__boxed_495_ = lean_unbox(v_x_491_);
v_x_51__boxed_496_ = lean_unbox(v_x_492_);
v_res_497_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_pOne_match__1_splitter(v_motive_490_, v_x_50__boxed_495_, v_x_51__boxed_496_, v_h__1_493_, v_h__2_494_);
return v_res_497_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_gram2(lean_object* v_factor_498_, uint8_t v_row_499_, uint8_t v_column_500_){
_start:
{
uint8_t v___x_501_; lean_object* v___x_502_; lean_object* v___x_503_; lean_object* v___x_504_; lean_object* v___x_505_; lean_object* v___x_506_; lean_object* v___x_507_; lean_object* v___x_508_; uint8_t v___x_509_; lean_object* v___x_510_; lean_object* v___x_511_; lean_object* v___x_512_; lean_object* v___x_513_; lean_object* v___x_514_; lean_object* v___x_515_; lean_object* v___x_516_; lean_object* v___x_517_; uint8_t v___x_518_; lean_object* v___x_519_; lean_object* v___x_520_; lean_object* v___x_521_; lean_object* v___x_522_; lean_object* v___x_523_; lean_object* v___x_524_; lean_object* v___x_525_; lean_object* v___x_526_; uint8_t v___x_527_; lean_object* v___x_528_; lean_object* v___x_529_; lean_object* v___x_530_; lean_object* v___x_531_; lean_object* v___x_532_; lean_object* v___x_533_; lean_object* v___x_534_; lean_object* v___x_535_; 
v___x_501_ = 0;
v___x_502_ = lean_box(v___x_501_);
v___x_503_ = lean_box(v_row_499_);
lean_inc_ref_n(v_factor_498_, 7);
v___x_504_ = lean_apply_2(v_factor_498_, v___x_502_, v___x_503_);
v___x_505_ = lean_box(v___x_501_);
v___x_506_ = lean_box(v_column_500_);
v___x_507_ = lean_apply_2(v_factor_498_, v___x_505_, v___x_506_);
v___x_508_ = lean_int_mul(v___x_504_, v___x_507_);
lean_dec(v___x_507_);
lean_dec(v___x_504_);
v___x_509_ = 1;
v___x_510_ = lean_box(v___x_509_);
v___x_511_ = lean_box(v_row_499_);
v___x_512_ = lean_apply_2(v_factor_498_, v___x_510_, v___x_511_);
v___x_513_ = lean_box(v___x_509_);
v___x_514_ = lean_box(v_column_500_);
v___x_515_ = lean_apply_2(v_factor_498_, v___x_513_, v___x_514_);
v___x_516_ = lean_int_mul(v___x_512_, v___x_515_);
lean_dec(v___x_515_);
lean_dec(v___x_512_);
v___x_517_ = lean_int_add(v___x_508_, v___x_516_);
lean_dec(v___x_516_);
lean_dec(v___x_508_);
v___x_518_ = 2;
v___x_519_ = lean_box(v___x_518_);
v___x_520_ = lean_box(v_row_499_);
v___x_521_ = lean_apply_2(v_factor_498_, v___x_519_, v___x_520_);
v___x_522_ = lean_box(v___x_518_);
v___x_523_ = lean_box(v_column_500_);
v___x_524_ = lean_apply_2(v_factor_498_, v___x_522_, v___x_523_);
v___x_525_ = lean_int_mul(v___x_521_, v___x_524_);
lean_dec(v___x_524_);
lean_dec(v___x_521_);
v___x_526_ = lean_int_add(v___x_517_, v___x_525_);
lean_dec(v___x_525_);
lean_dec(v___x_517_);
v___x_527_ = 3;
v___x_528_ = lean_box(v___x_527_);
v___x_529_ = lean_box(v_row_499_);
v___x_530_ = lean_apply_2(v_factor_498_, v___x_528_, v___x_529_);
v___x_531_ = lean_box(v___x_527_);
v___x_532_ = lean_box(v_column_500_);
v___x_533_ = lean_apply_2(v_factor_498_, v___x_531_, v___x_532_);
v___x_534_ = lean_int_mul(v___x_530_, v___x_533_);
lean_dec(v___x_533_);
lean_dec(v___x_530_);
v___x_535_ = lean_int_add(v___x_526_, v___x_534_);
lean_dec(v___x_534_);
lean_dec(v___x_526_);
return v___x_535_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_gram2___boxed(lean_object* v_factor_536_, lean_object* v_row_537_, lean_object* v_column_538_){
_start:
{
uint8_t v_row_boxed_539_; uint8_t v_column_boxed_540_; lean_object* v_res_541_; 
v_row_boxed_539_ = lean_unbox(v_row_537_);
v_column_boxed_540_ = lean_unbox(v_column_538_);
v_res_541_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_gram2(v_factor_536_, v_row_boxed_539_, v_column_boxed_540_);
return v_res_541_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewNumerator(lean_object* v_root_542_, lean_object* v_observable_543_){
_start:
{
lean_object* v___x_544_; lean_object* v___x_545_; lean_object* v___x_546_; lean_object* v___x_547_; 
v___x_544_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_commutator___boxed), 4, 2);
lean_closure_set(v___x_544_, 0, v_root_542_);
lean_closure_set(v___x_544_, 1, v_observable_543_);
lean_inc_ref(v___x_544_);
v___x_545_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_matrixMul___boxed), 4, 2);
lean_closure_set(v___x_545_, 0, v___x_544_);
lean_closure_set(v___x_545_, 1, v___x_544_);
v___x_546_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_trace2(v___x_545_);
v___x_547_ = lean_int_neg(v___x_546_);
lean_dec(v___x_546_);
return v___x_547_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0(void){
_start:
{
lean_object* v___x_548_; lean_object* v___x_549_; 
v___x_548_ = lean_unsigned_to_nat(2u);
v___x_549_ = lean_nat_to_int(v___x_548_);
return v___x_549_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator(lean_object* v_rootScale_550_){
_start:
{
lean_object* v___x_551_; lean_object* v___x_552_; lean_object* v___x_553_; lean_object* v___x_554_; 
v___x_551_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0);
v___x_552_ = lean_nat_to_int(v_rootScale_550_);
v___x_553_ = lean_int_mul(v___x_551_, v___x_552_);
v___x_554_ = lean_int_mul(v___x_553_, v___x_552_);
lean_dec(v___x_552_);
lean_dec(v___x_553_);
return v___x_554_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__0(void){
_start:
{
lean_object* v___x_555_; lean_object* v___x_556_; 
v___x_555_ = lean_unsigned_to_nat(12u);
v___x_556_ = lean_nat_to_int(v___x_555_);
return v___x_556_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1(void){
_start:
{
lean_object* v___x_557_; lean_object* v___x_558_; 
v___x_557_ = lean_unsigned_to_nat(9u);
v___x_558_ = lean_nat_to_int(v___x_557_);
return v___x_558_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2(void){
_start:
{
lean_object* v___x_559_; lean_object* v___x_560_; 
v___x_559_ = lean_unsigned_to_nat(16u);
v___x_560_ = lean_nat_to_int(v___x_559_);
return v___x_560_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho(uint8_t v_x_561_, uint8_t v_x_562_){
_start:
{
if (v_x_561_ == 0)
{
if (v_x_562_ == 0)
{
lean_object* v___x_565_; 
v___x_565_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1);
return v___x_565_;
}
else
{
goto v___jp_563_;
}
}
else
{
if (v_x_562_ == 0)
{
goto v___jp_563_;
}
else
{
lean_object* v___x_566_; 
v___x_566_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2);
return v___x_566_;
}
}
v___jp_563_:
{
lean_object* v___x_564_; 
v___x_564_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__0);
return v___x_564_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___boxed(lean_object* v_x_567_, lean_object* v_x_568_){
_start:
{
uint8_t v_x_58__boxed_569_; uint8_t v_x_59__boxed_570_; lean_object* v_res_571_; 
v_x_58__boxed_569_ = lean_unbox(v_x_567_);
v_x_59__boxed_570_ = lean_unbox(v_x_568_);
v_res_571_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho(v_x_58__boxed_569_, v_x_59__boxed_570_);
return v_res_571_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRho(uint8_t v_x_572_, uint8_t v_x_573_){
_start:
{
if (v_x_572_ == 0)
{
if (v_x_573_ == 0)
{
lean_object* v___x_576_; 
v___x_576_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__1);
return v___x_576_;
}
else
{
goto v___jp_574_;
}
}
else
{
if (v_x_573_ == 1)
{
lean_object* v___x_577_; 
v___x_577_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___closed__2);
return v___x_577_;
}
else
{
goto v___jp_574_;
}
}
v___jp_574_:
{
lean_object* v___x_575_; 
v___x_575_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_575_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRho___boxed(lean_object* v_x_578_, lean_object* v_x_579_){
_start:
{
uint8_t v_x_61__boxed_580_; uint8_t v_x_62__boxed_581_; lean_object* v_res_582_; 
v_x_61__boxed_580_ = lean_unbox(v_x_578_);
v_x_62__boxed_581_ = lean_unbox(v_x_579_);
v_res_582_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRho(v_x_61__boxed_580_, v_x_62__boxed_581_);
return v_res_582_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRoot(uint8_t v_a_583_, uint8_t v_a_584_){
_start:
{
lean_object* v___x_585_; 
v___x_585_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho(v_a_583_, v_a_584_);
return v___x_585_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRoot___boxed(lean_object* v_a_586_, lean_object* v_a_587_){
_start:
{
uint8_t v_a_5__boxed_588_; uint8_t v_a_6__boxed_589_; lean_object* v_res_590_; 
v_a_5__boxed_588_ = lean_unbox(v_a_586_);
v_a_6__boxed_589_ = lean_unbox(v_a_587_);
v_res_590_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRoot(v_a_5__boxed_588_, v_a_6__boxed_589_);
return v_res_590_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0(void){
_start:
{
lean_object* v___x_591_; lean_object* v___x_592_; 
v___x_591_ = lean_unsigned_to_nat(3u);
v___x_592_ = lean_nat_to_int(v___x_591_);
return v___x_592_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1(void){
_start:
{
lean_object* v___x_593_; lean_object* v___x_594_; 
v___x_593_ = lean_unsigned_to_nat(4u);
v___x_594_ = lean_nat_to_int(v___x_593_);
return v___x_594_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot(uint8_t v_x_595_, uint8_t v_x_596_){
_start:
{
if (v_x_595_ == 0)
{
if (v_x_596_ == 0)
{
lean_object* v___x_599_; 
v___x_599_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0);
return v___x_599_;
}
else
{
goto v___jp_597_;
}
}
else
{
if (v_x_596_ == 1)
{
lean_object* v___x_600_; 
v___x_600_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1);
return v___x_600_;
}
else
{
goto v___jp_597_;
}
}
v___jp_597_:
{
lean_object* v___x_598_; 
v___x_598_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_598_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___boxed(lean_object* v_x_601_, lean_object* v_x_602_){
_start:
{
uint8_t v_x_65__boxed_603_; uint8_t v_x_66__boxed_604_; lean_object* v_res_605_; 
v_x_65__boxed_603_ = lean_unbox(v_x_601_);
v_x_66__boxed_604_ = lean_unbox(v_x_602_);
v_res_605_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot(v_x_65__boxed_603_, v_x_66__boxed_604_);
return v_res_605_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputGramFactor(uint8_t v_x_606_, uint8_t v_x_607_){
_start:
{
if (v_x_606_ == 0)
{
if (v_x_607_ == 0)
{
lean_object* v___x_608_; 
v___x_608_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0);
return v___x_608_;
}
else
{
lean_object* v___x_609_; 
v___x_609_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1);
return v___x_609_;
}
}
else
{
lean_object* v___x_610_; 
v___x_610_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_610_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputGramFactor___boxed(lean_object* v_x_611_, lean_object* v_x_612_){
_start:
{
uint8_t v_x_52__boxed_613_; uint8_t v_x_53__boxed_614_; lean_object* v_res_615_; 
v_x_52__boxed_613_ = lean_unbox(v_x_611_);
v_x_53__boxed_614_ = lean_unbox(v_x_612_);
v_res_615_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputGramFactor(v_x_52__boxed_613_, v_x_53__boxed_614_);
return v_res_615_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputStateGramFactor(uint8_t v_x_616_, uint8_t v_x_617_){
_start:
{
switch(v_x_616_)
{
case 0:
{
if (v_x_617_ == 0)
{
lean_object* v___x_620_; 
v___x_620_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0);
return v___x_620_;
}
else
{
goto v___jp_618_;
}
}
case 1:
{
if (v_x_617_ == 1)
{
lean_object* v___x_621_; 
v___x_621_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1);
return v___x_621_;
}
else
{
goto v___jp_618_;
}
}
default: 
{
goto v___jp_618_;
}
}
v___jp_618_:
{
lean_object* v___x_619_; 
v___x_619_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_619_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputStateGramFactor___boxed(lean_object* v_x_622_, lean_object* v_x_623_){
_start:
{
uint8_t v_x_66__boxed_624_; uint8_t v_x_67__boxed_625_; lean_object* v_res_626_; 
v_x_66__boxed_624_ = lean_unbox(v_x_622_);
v_x_67__boxed_625_ = lean_unbox(v_x_623_);
v_res_626_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputStateGramFactor(v_x_66__boxed_624_, v_x_67__boxed_625_);
return v_res_626_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___closed__0(void){
_start:
{
lean_object* v___x_627_; lean_object* v___x_628_; 
v___x_627_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0);
v___x_628_ = lean_int_neg(v___x_627_);
return v___x_628_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor(uint8_t v_x_629_, uint8_t v_x_630_){
_start:
{
switch(v_x_629_)
{
case 0:
{
if (v_x_630_ == 0)
{
lean_object* v___x_635_; 
v___x_635_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__0);
return v___x_635_;
}
else
{
goto v___jp_633_;
}
}
case 1:
{
if (v_x_630_ == 0)
{
lean_object* v___x_636_; 
v___x_636_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_skewDenominator___closed__0);
return v___x_636_;
}
else
{
lean_object* v___x_637_; 
v___x_637_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___closed__0);
return v___x_637_;
}
}
case 2:
{
if (v_x_630_ == 0)
{
goto v___jp_631_;
}
else
{
lean_object* v___x_638_; 
v___x_638_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___closed__1);
return v___x_638_;
}
}
default: 
{
if (v_x_630_ == 0)
{
goto v___jp_631_;
}
else
{
goto v___jp_633_;
}
}
}
v___jp_631_:
{
lean_object* v___x_632_; 
v___x_632_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__0);
return v___x_632_;
}
v___jp_633_:
{
lean_object* v___x_634_; 
v___x_634_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_identity2___closed__1);
return v___x_634_;
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___boxed(lean_object* v_x_639_, lean_object* v_x_640_){
_start:
{
uint8_t v_x_109__boxed_641_; uint8_t v_x_110__boxed_642_; lean_object* v_res_643_; 
v_x_109__boxed_641_ = lean_unbox(v_x_639_);
v_x_110__boxed_642_ = lean_unbox(v_x_640_);
v_res_643_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor(v_x_109__boxed_641_, v_x_110__boxed_642_);
return v_res_643_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0(void){
_start:
{
lean_object* v___x_644_; lean_object* v___x_645_; lean_object* v___x_646_; 
v___x_644_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputGramFactor___boxed), 2, 0);
v___x_645_ = lean_unsigned_to_nat(5u);
v___x_646_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_646_, 0, v___x_645_);
lean_ctor_set(v___x_646_, 1, v___x_644_);
return v___x_646_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram(void){
_start:
{
lean_object* v___x_647_; 
v___x_647_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0);
return v___x_647_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRootGram(void){
_start:
{
lean_object* v___x_648_; 
v___x_648_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram___closed__0);
return v___x_648_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram___closed__0(void){
_start:
{
lean_object* v___x_649_; lean_object* v___x_650_; lean_object* v___x_651_; 
v___x_649_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputStateGramFactor___boxed), 2, 0);
v___x_650_ = lean_unsigned_to_nat(5u);
v___x_651_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_651_, 0, v___x_650_);
lean_ctor_set(v___x_651_, 1, v___x_649_);
return v___x_651_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram(void){
_start:
{
lean_object* v___x_652_; 
v___x_652_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram___closed__0);
return v___x_652_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram___closed__0(void){
_start:
{
lean_object* v___x_653_; lean_object* v___x_654_; lean_object* v___x_655_; 
v___x_653_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGramFactor___boxed), 2, 0);
v___x_654_ = lean_unsigned_to_nat(5u);
v___x_655_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v___x_655_, 0, v___x_654_);
lean_ctor_set(v___x_655_, 1, v___x_653_);
return v___x_655_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram(void){
_start:
{
lean_object* v___x_656_; 
v___x_656_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram___closed__0);
return v___x_656_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput___closed__0(void){
_start:
{
lean_object* v___x_657_; lean_object* v___x_658_; lean_object* v___f_659_; lean_object* v___x_660_; lean_object* v___x_661_; 
v___x_657_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRootGram;
v___x_658_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram;
v___f_659_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRho___boxed), 2, 0);
v___x_660_ = lean_unsigned_to_nat(25u);
lean_inc_ref(v___f_659_);
v___x_661_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_661_, 0, v___x_660_);
lean_ctor_set(v___x_661_, 1, v___x_660_);
lean_ctor_set(v___x_661_, 2, v___f_659_);
lean_ctor_set(v___x_661_, 3, v___f_659_);
lean_ctor_set(v___x_661_, 4, v___x_658_);
lean_ctor_set(v___x_661_, 5, v___x_657_);
return v___x_661_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput(void){
_start:
{
lean_object* v___x_662_; 
v___x_662_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput___closed__0);
return v___x_662_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput___closed__0(void){
_start:
{
lean_object* v___x_663_; lean_object* v___x_664_; lean_object* v___x_665_; lean_object* v___x_666_; lean_object* v___x_667_; lean_object* v___x_668_; lean_object* v___x_669_; 
v___x_663_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram;
v___x_664_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram;
v___x_665_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRoot___boxed), 2, 0);
v___x_666_ = lean_alloc_closure((void*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRho___boxed), 2, 0);
v___x_667_ = lean_unsigned_to_nat(5u);
v___x_668_ = lean_unsigned_to_nat(25u);
v___x_669_ = lean_alloc_ctor(0, 6, 0);
lean_ctor_set(v___x_669_, 0, v___x_668_);
lean_ctor_set(v___x_669_, 1, v___x_667_);
lean_ctor_set(v___x_669_, 2, v___x_666_);
lean_ctor_set(v___x_669_, 3, v___x_665_);
lean_ctor_set(v___x_669_, 4, v___x_664_);
lean_ctor_set(v___x_669_, 5, v___x_663_);
return v___x_669_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput(void){
_start:
{
lean_object* v___x_670_; 
v___x_670_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput___closed__0, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput___closed__0_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput___closed__0);
return v___x_670_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___redArg(uint8_t v_x_671_, uint8_t v_x_672_, lean_object* v_h__1_673_, lean_object* v_h__2_674_, lean_object* v_h__3_675_, lean_object* v_h__4_676_){
_start:
{
if (v_x_671_ == 0)
{
lean_dec(v_h__4_676_);
lean_dec(v_h__3_675_);
if (v_x_672_ == 0)
{
lean_object* v___x_677_; lean_object* v___x_678_; 
lean_dec(v_h__2_674_);
v___x_677_ = lean_box(0);
v___x_678_ = lean_apply_1(v_h__1_673_, v___x_677_);
return v___x_678_;
}
else
{
lean_object* v___x_679_; lean_object* v___x_680_; 
lean_dec(v_h__1_673_);
v___x_679_ = lean_box(0);
v___x_680_ = lean_apply_1(v_h__2_674_, v___x_679_);
return v___x_680_;
}
}
else
{
lean_dec(v_h__2_674_);
lean_dec(v_h__1_673_);
if (v_x_672_ == 0)
{
lean_object* v___x_681_; lean_object* v___x_682_; 
lean_dec(v_h__4_676_);
v___x_681_ = lean_box(0);
v___x_682_ = lean_apply_1(v_h__3_675_, v___x_681_);
return v___x_682_;
}
else
{
lean_object* v___x_683_; lean_object* v___x_684_; 
lean_dec(v_h__3_675_);
v___x_683_ = lean_box(0);
v___x_684_ = lean_apply_1(v_h__4_676_, v___x_683_);
return v___x_684_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___redArg___boxed(lean_object* v_x_685_, lean_object* v_x_686_, lean_object* v_h__1_687_, lean_object* v_h__2_688_, lean_object* v_h__3_689_, lean_object* v_h__4_690_){
_start:
{
uint8_t v_x_46__boxed_691_; uint8_t v_x_47__boxed_692_; lean_object* v_res_693_; 
v_x_46__boxed_691_ = lean_unbox(v_x_685_);
v_x_47__boxed_692_ = lean_unbox(v_x_686_);
v_res_693_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___redArg(v_x_46__boxed_691_, v_x_47__boxed_692_, v_h__1_687_, v_h__2_688_, v_h__3_689_, v_h__4_690_);
return v_res_693_;
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter(lean_object* v_motive_694_, uint8_t v_x_695_, uint8_t v_x_696_, lean_object* v_h__1_697_, lean_object* v_h__2_698_, lean_object* v_h__3_699_, lean_object* v_h__4_700_){
_start:
{
if (v_x_695_ == 0)
{
lean_dec(v_h__4_700_);
lean_dec(v_h__3_699_);
if (v_x_696_ == 0)
{
lean_object* v___x_701_; lean_object* v___x_702_; 
lean_dec(v_h__2_698_);
v___x_701_ = lean_box(0);
v___x_702_ = lean_apply_1(v_h__1_697_, v___x_701_);
return v___x_702_;
}
else
{
lean_object* v___x_703_; lean_object* v___x_704_; 
lean_dec(v_h__1_697_);
v___x_703_ = lean_box(0);
v___x_704_ = lean_apply_1(v_h__2_698_, v___x_703_);
return v___x_704_;
}
}
else
{
lean_dec(v_h__2_698_);
lean_dec(v_h__1_697_);
if (v_x_696_ == 0)
{
lean_object* v___x_705_; lean_object* v___x_706_; 
lean_dec(v_h__4_700_);
v___x_705_ = lean_box(0);
v___x_706_ = lean_apply_1(v_h__3_699_, v___x_705_);
return v___x_706_;
}
else
{
lean_object* v___x_707_; lean_object* v___x_708_; 
lean_dec(v_h__3_699_);
v___x_707_ = lean_box(0);
v___x_708_ = lean_apply_1(v_h__4_700_, v___x_707_);
return v___x_708_;
}
}
}
}
LEAN_EXPORT lean_object* lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter___boxed(lean_object* v_motive_709_, lean_object* v_x_710_, lean_object* v_x_711_, lean_object* v_h__1_712_, lean_object* v_h__2_713_, lean_object* v_h__3_714_, lean_object* v_h__4_715_){
_start:
{
uint8_t v_x_68__boxed_716_; uint8_t v_x_69__boxed_717_; lean_object* v_res_718_; 
v_x_68__boxed_716_ = lean_unbox(v_x_710_);
v_x_69__boxed_717_ = lean_unbox(v_x_711_);
v_res_718_ = lp_FiniteQuantum___private_WorldCovariantWignerYanase_0__OmegaWorld_WignerYanaseQ10_inputRho_match__1_splitter(v_motive_709_, v_x_68__boxed_716_, v_x_69__boxed_717_, v_h__1_712_, v_h__2_713_, v_h__3_714_, v_h__4_715_);
return v_res_718_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__1(void){
_start:
{
lean_object* v___x_720_; lean_object* v___x_721_; lean_object* v___x_722_; lean_object* v___x_723_; lean_object* v___x_724_; 
v___x_720_ = lean_box(0);
v___x_721_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput;
v___x_722_ = lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput;
v___x_723_ = ((lean_object*)(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__0));
v___x_724_ = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(v___x_724_, 0, v___x_723_);
lean_ctor_set(v___x_724_, 1, v___x_722_);
lean_ctor_set(v___x_724_, 2, v___x_721_);
lean_ctor_set(v___x_724_, 3, v___x_720_);
return v___x_724_;
}
}
static lean_object* _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness(void){
_start:
{
lean_object* v___x_725_; 
v___x_725_ = lean_obj_once(&lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__1, &lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__1_once, _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness___closed__1);
return v___x_725_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_FiniteQuantum_WorldCovariantWignerYanase(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRhoGram);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRootGram = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRootGram();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_inputRootGram);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRhoGram);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_outputRootGram);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedInput);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_rootedOutput);
lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness = _init_lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness();
lean_mark_persistent(lp_FiniteQuantum_OmegaWorld_WignerYanaseQ10_scopedCovariantWignerYanaseWitness);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
