import «009_gg001_core»
import «gomc_04_observer_quotient_nonfaithfulness»

/-!
QM-facing wrapper for Paper 051 succession.

The theorem here says only that a local succession view can be green while an
extra global/QM readout remains red. It is an LGGR/factorization boundary, not
a derivation of QM from constitutive succession and not an authority path.
-/

namespace QM

namespace PaperGG001SuccessionBridge

structure AnnotatedCut (Cut QMeta : Type) where
  cut : Cut
  qmeta : QMeta

def localSuccessionView {Cut QMeta View : Type}
    (view : Cut -> View) : AnnotatedCut Cut QMeta -> View :=
  fun x => view x.cut

def qmHiddenReadout {Cut QMeta Hidden : Type}
    (hidden : Cut -> QMeta -> Hidden) : AnnotatedCut Cut QMeta -> Hidden :=
  fun x => hidden x.cut x.qmeta

theorem local_succession_green_qm_hidden_red_blocks_factor
    {Cut QMeta View Hidden : Type}
    (view : Cut -> View) (hidden : Cut -> QMeta -> Hidden)
    (x y : AnnotatedCut Cut QMeta)
    (hLocal : localSuccessionView view x = localSuccessionView view y)
    (hHidden : qmHiddenReadout hidden x ≠ qmHiddenReadout hidden y) :
    Not (GOMC04.FactorsThrough
        (localSuccessionView view)
        (fun z => (localSuccessionView view z, qmHiddenReadout hidden z))) := by
  exact
    GOMC04.joint_not_factor_of_hidden_separation
      (localSuccessionView view)
      (qmHiddenReadout hidden) x y hLocal hHidden

def chainLocalView : PaperGG001.Chain3 -> Bool
  | PaperGG001.Chain3.alpha => false
  | PaperGG001.Chain3.beta => true
  | PaperGG001.Chain3.gamma => true

def chainHiddenReadout : PaperGG001.Chain3 -> Unit -> PaperGG001.Chain3 :=
  fun c _ => c

def betaAnnotated : AnnotatedCut PaperGG001.Chain3 Unit where
  cut := PaperGG001.Chain3.beta
  qmeta := ()

def gammaAnnotated : AnnotatedCut PaperGG001.Chain3 Unit where
  cut := PaperGG001.Chain3.gamma
  qmeta := ()

theorem chain_local_succession_view_green :
    localSuccessionView chainLocalView betaAnnotated =
      localSuccessionView chainLocalView gammaAnnotated := by
  rfl

theorem chain_qm_hidden_readout_red :
    qmHiddenReadout chainHiddenReadout betaAnnotated ≠
      qmHiddenReadout chainHiddenReadout gammaAnnotated := by
  decide

theorem chain_local_green_qm_hidden_red :
    Not (GOMC04.FactorsThrough
        (localSuccessionView chainLocalView)
        (fun z => (localSuccessionView chainLocalView z,
          qmHiddenReadout chainHiddenReadout z))) := by
  exact
    local_succession_green_qm_hidden_red_blocks_factor
      chainLocalView chainHiddenReadout betaAnnotated gammaAnnotated
      chain_local_succession_view_green chain_qm_hidden_readout_red

end PaperGG001SuccessionBridge

end QM

#print axioms QM.PaperGG001SuccessionBridge.local_succession_green_qm_hidden_red_blocks_factor
#print axioms QM.PaperGG001SuccessionBridge.chain_local_green_qm_hidden_red
