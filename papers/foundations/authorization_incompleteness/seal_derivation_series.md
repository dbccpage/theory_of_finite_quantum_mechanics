> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\seal_derivation_series.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Proposed SEAL-AIT derivation series

**Status:** design document.

**AuthorityEffect:** None.

This is a plan for future, separately sealed derivations. It does not
amend, reproduce, or import `19L57G1@sealed-derivation-v1`. Each entry
would need its own frozen inputs, proof gates, receipts, and terminal
claim ledger. The current live CODA directory holds only this research
plan and its small finite seed.

## Design rule

Each derivation may introduce exactly the structure its result needs.
For every lift, record:

1. the carrier and the previous invariant;
2. the supplied or admitted data;
3. the derived object;
4. a positive witness;
5. a countermodel or nonimplication witness;
6. the invariant that survives the lift;
7. the next unpriced structure.

No later step may claim that an earlier raw object selected its added
structure. This is the J011 discipline applied to authorization.

## Series map

```text
SEAL-AIT-00 Primitive Difference
  -> SEAL-AIT-01 Presentation and quotient
  -> SEAL-AIT-02 Proposal and semantic predicate
  -> SEAL-AIT-03 Evaluation and report adequacy
  -> SEAL-AIT-04 Replay and evidence custody
  -> SEAL-AIT-05 Authorization and terminal policy
  -> SEAL-AIT-06 Turing-computation boundary
  -> SEAL-AIT-07 Self-soundness boundary
  -> SEAL-AIT-08 LLM authorization corollary
```

## SEAL-AIT-00: Primitive Difference

**Starting point:** a carrier, two unequal marks, a Primitive Difference,
and the derived zero quotient. The current J011 support spine is a
locator, not this derivation.

**Invariant:** a raw distinction does not by itself choose a look,
report, section, dynamic, semantic predicate, or policy.

**Required proof:** two extensions with identical primitive data but
different validity predicates and terminal policies. The differences
must be visibly added, not smuggled in as consequences of the marks.

**Terminal nonclaim:** no computation, Turing machine, LLM, evaluator,
or authority has been derived.

## SEAL-AIT-01: Presentation and quotient

**Input:** SEAL-AIT-00 plus a declared observation/report map.

**Invariant:** the quotient records exactly what the declared report
identifies. A quotient map is not an arbitrary supplied report, and a
section is extra data.

**Required proof:** report fibers, quotient recovery, and a witness that
no unique section is selected. Reuse only a formally bound interface,
not a prose analogy to J011.

**Current in-tree bridge:** `AIT-PD1` now specializes the P0
factorization boundary to J011's actual `pdProj P` quotient. It is a
rooted current candidate, not the separately sealed derivation required
for this series step.

**Next unpriced structure:** semantic validity.

## SEAL-AIT-02: Proposal and semantic predicate

**Input:** report interface plus an independently declared contract
predicate `V` on proposals.

**Invariant:** proposal bytes, parser, semantic interpretation, and
validity predicate are distinct objects.

**Required proof:** two proposal interpretations with the same report
shape but distinct validity behavior; a declared semantic adapter is an
import, not a report-derived fact.

**Next unpriced structure:** an evaluator / decider.

## SEAL-AIT-03: Evaluation and report adequacy

**Input:** proposal, report, and validity predicate.

**Invariant:** total report-only authorization requires validity to be
constant on report fibers.

**Required proof:** the finite factorization theorem, a split-fiber
countermodel, and an adequate positive contract. The current AIT Lean
seed now closes one finite executable instance: full configuration is
adequate for the marked-cell contract, while the shared control-only
report is not.

**Next unpriced structure:** replay custody.

## SEAL-AIT-04: Replay and evidence custody

**Input:** a local evaluator and a result claim.

**Invariant:** replay is a relationship among frozen bytes, parser,
checker, environment, command, and output. A producer assertion that a
check passed is not the same object as a replay.

**Required proof:** a receipt schema, binding theorem or executable
verifier, and negative attacks for parser, checker, contract, version,
and hash substitution.

**Current bounded witness:** the AIT-G3 JSON packet, SHA-256 manifest,
PowerShell evaluator, mutation corpus, and Lean-backed replay satisfy
this step for one finite transition carrier. The packet keeps terminal
status open and declares rather than proves collision resistance,
evaluator correspondence, runtime integrity, and custody.

**Next unpriced structure:** independently controlled custody and a
terminal policy effect.

## SEAL-AIT-05: Authorization and terminal policy

**Input:** replayable evidence with declared scope.

**Invariant:** evaluation evidence does not itself grant a policy
effect. A terminal policy identifies what, if anything, a passing check
licenses.

**Required proof:** evidence and authority types remain distinct;
authorization records the policy owner, scope, and trust base; an
unbound receipt cannot cross the terminal boundary.

**Current abstract bridge:** AIT-G5c proves the terminalization
consequence only after a class-relative no-decider premise and allowed
acceptance-bit membership are supplied. A closed terminalizer that is
acceptance-sound and rejection-sound would then be acceptance-complete
and contradict that premise. Its finite Boolean fixture shows that closed
terminalization remains possible for a decidable local contract. This is
not an actual nondecidability, physical-externality, or custody result.

**Next unpriced structure:** global semantic completeness.

## SEAL-AIT-06: Turing-computation boundary

**Input:** the completed controlled tape/read/transition/halt series in
`controlled_turing_derivation_series.md`, a Turing-complete proposal
language, and a nontrivial extensional semantic property.

**Current position:** AIT-DTM0 closes only a direct finite-rule operational
seed: finite structured rules, a total mathematical tape, bounded execution,
and distinct halt/stuck/fuel results. It does not yet supply the
Turing-complete language, byte-level parser, extensional property, or
effective reduction required by this lift.

**Invariant:** Turing computation remains an adequate model of effective
procedure. It does not make arbitrary semantic authorization decidable.

**Required proof:** a Rice-theorem reduction showing that a total,
sound-and-complete global authorizer would decide the chosen property.
This is not a claim of hypercomputation or a correction to Turing's
model. The tape-control branch must separately establish that a blank is
a declared symbol, a read is syntactic selection, a halt is execution
terminality, and none of these selects a semantic contract or terminal
policy.

**Next unpriced structure:** the soundness of the authorizer's own
formal theory.

## SEAL-AIT-07: Self-soundness boundary

**Input:** a recursively axiomatized formal theory of the authorization
procedure.

**Invariant:** relative proof checking can be strong without yielding
an internal proof of the theory's own global consistency under the
second-incompleteness hypotheses.

**Required proof:** theory encoding, provability predicate,
representability conditions, and the exact consistency/reflection
statement. Any external meta-theory must be named as the next trust
boundary.

**Next unpriced structure:** an LLM deployment model.

## SEAL-AIT-08: LLM authorization corollary

**Input:** a formal LLM execution model with explicit tools and seeds.

**Invariant:** capability, fluency, and a self-generated explanation do
not turn a proposal source into a globally total semantic authorizer.

**Required proof:** map an LLM-only decision to the SEAL-AIT-06 model,
or show that it consumes an independent checker, semantic oracle, or
terminal policy. In the latter case, the LLM is not the sole
authorization source.

**Terminal result:** a bounded system may authorize relative to a named
trust boundary; no LLM-only total semantic authorization exists for the
arbitrary proposal class modeled in SEAL-AIT-06.

## What would make the series convincing

- Each derivation is independently replayable from frozen inputs.
- Each conclusion names its exact theorem and a countermodel boundary.
- Every new structure is either derived, declared, or labeled open.
- The LLM result is a corollary of the prior series, not a premise
  imported at the beginning.
- The final paper clearly distinguishes a local certificate from a
  global semantic guarantee.

**AuthorityEffect:** None.
