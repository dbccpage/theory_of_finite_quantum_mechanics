# S(n) off-image refusal completeness: note

**AuthorityEffect:** None. Proposal only. Written by a model thread against
`dbccpage/the_symbol_game` `origin/main` `8ac5da188` (merge of #1152,
2026-10-17); the prompt was written against `9ac0cd73d`. Every cited line was
re-checked at `8ac5da188`; none had moved.

## Scope

This note is about the pinned education `SnCarrier` model only:
`BasePresentation`, `sectionLift` and `retractionDownMap` in
`symmetric_group_presentations/lean4/SnCarrier.lean`. It says nothing about carrier cardinalities,
about OB-1, or about any S(n) tower beyond the five base shapes. The
"corrected cardinality theorem" half of WDP-P001-019 is not touched.

## Definitions (file:line)

- `GroundToken` (`SnSyntax.lean:27`): one field `raw : Unit`, so one value.
- `InnerBody` (`SnSyntax.lean:81`): `arrow src tgt | pair first second | glyphs gs`.
- `SectionLift` (`SnSyntax.lean:93`): `stage : Nat`, `body : InnerBody`.
- `SnPresentation` (`SnSyntax.lean:118`): `ground | supplied | relation | lift | retraction | nonDescent`.
- `BasePresentation` (`SnCarrier.lean:58`): `ground | supplied | relation`;
  `toPresentation` (`:64`) reads it back constructor by constructor.
- `sectionLift stage p` (`SnCarrier.lean:70`): five cases, each producing
  `.lift ⟨stage, body⟩` with body `.glyphs []`, `.glyphs [m]`,
  `.glyphs [f, s]`, `.arrow src tgt`, `.pair v0 v1`.
- `RetractOutcome` (`SnCarrier.lean:84`): `accepted p | nonDescent`.
- `retractionDownMap stage p` (`SnCarrier.lean:90`): matches `.lift l`, tests
  `l.stage == stage`, then the five bodies; everything else is `nonDescent`.
- Positive half already present: `SnTheorems.old_image_base`
  (`SnTheorems.lean:91`), `retractionDownMap n (sectionLift n p) = .accepted p.toPresentation`.

## Statements (all in `symmetric_group_presentations/lean4/SnOffImage.lean`, namespace `SnOffImage`)

1. `accepted_only_from_section (n p q) (h : retractionDownMap n p = .accepted q) : ∃ b, p = sectionLift n b ∧ q = b.toPresentation`.
2. `nonDescent_iff_off_image (n p) : retractionDownMap n p = .nonDescent ↔ ∀ b, p ≠ sectionLift n b`.
3. `sectionLift_injective (n b b') : sectionLift n b = sectionLift n b' → b = b'`.
4. `retraction_stage_strict (n m b) (hm : m ≠ n) : retractionDownMap n (sectionLift m b) = .nonDescent`.
5. `inImage (n p) : Bool` with `inImage_iff : inImage n p = true ↔ ∃ b, p = sectionLift n b`.

Together with the old-image law: on the image the retraction is a left
inverse of the section, off the image it refuses, and the image is decidable
from the syntax.

## Proof

**Main theorem.** Case on `p`. For the five non-`lift` constructors the
hypothesis reduces to `.nonDescent = .accepted q`, closed by constructor
disjointness. For `.lift ⟨s, body⟩`, decide `s = n` with `Nat.decEq`. If
`s ≠ n`, the `if` takes its `else` branch (`eq_of_beq` turns the Boolean
test into an equation) and the hypothesis is again a constructor clash. If
`s = n`, substitute, then case on `body`, and on the glyph list to depth
three. Each of the five accepted branches names its witness
(`.ground ⟨()⟩`, `.supplied ⟨a⟩`, `.relation (.pair ⟨a, b⟩)`,
`.relation (.cut ⟨src, tgt⟩)`, `.relation (.simplex ⟨v0, v1⟩)`); the first
conjunct is `rfl`, the second follows from injectivity of `.accepted`. The
list `a :: b :: c :: t''` falls to the wildcard arm and is a clash.

**Corollary 1.** Left to right: if `p = sectionLift n b` then the old-image
law gives `.accepted _ = .nonDescent`, a clash. Right to left: case on the
outcome; an `accepted` outcome would produce a witness by the main theorem,
contradicting the hypothesis.

**Corollary 2.** The left-inverse argument (the shape of the deposit's
abstract `old_image_injective`, `Paper001.lean:103`): apply the old-image law
to `b` and `b'`, rewrite with the hypothesis, and read off
`b.toPresentation = b'.toPresentation`; `toPresentation` is injective by
cases. The `ground` case rests on `GroundToken` having one value; that fact
enters where the old-image law reads `.ground ⟨()⟩` back as `.ground g`.

**Corollary 3.** By corollary 1 it is enough that `sectionLift m b` is no
`sectionLift n b'`; the stage projection `liftStage` sends them to `some m`
and `some n`, so equality would force `m = n`.

**Corollary 4.** `inImage` reads which outcome `retractionDownMap` produced;
both directions follow from the main theorem and the old-image law.

## Axioms, and one thing found on the way

`SnTheorems.old_image_base` depends on `Classical.choice`. The source is
`Nat.instLawfulBEq` (reached through `beq_self_eq_true` in its `simp only`
call), not anything in the model. This file does not reuse it:
`old_image_base'` re-derives the same statement through
`decide_eq_true rfl` and a two-line `ite` lemma proved by cases on the
`Decidable` instance. All six theorems then sit inside `{propext, Quot.sound}`;
`propext` is already carried by the definition `retractionDownMap` itself
(through `Nat.decEq`). No edit to `SnTheorems.lean` is proposed; the
observation is recorded here for Jeremy.

## Reused, and what remains open

Reused: the pinned definitions above and the shape of
`Paper001.old_image_injective`. The deposit's `off_image_not_implied`
(`Paper001.lean:111`) shows abstractly that a left inverse does not by itself
give off-image refusal; the present file shows it for this concrete model by
inspecting the retraction's cases.

Open, not addressed here: the corrected cardinality theorem of WDP-P001-019;
OB-1; any statement about `carrierCard`.

**Proposed wording for WDP-P001-019 (deposit untouched; Jeremy's decision):**
"Domain restriction mechanized in
`education/symmetric_group_presentations/lean4/SnOffImage.lean`
(`accepted_only_from_section`, `nonDescent_iff_off_image`); corrected
cardinality theorem remains open."

## Where "not yet attempted" was re-checked at `8ac5da188`

- `SnTheorems.lean`: no theorem has `.accepted` as a hypothesis, no
  injectivity of `sectionLift`, no `inImage` (grep `accepted\|injective\|inImage`).
- `symmetric_groups_and_minimal_symbol_systems/lean4/SnCarrierDischarge.lean`: two negative controls only;
  `Paper001.lean` has the abstract `old_image_injective` and
  `off_image_not_implied`, no theorem about `retractionDownMap`.
- `symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md:25` and `paper.md:197-203` still name the
  gap as open; `symmetric_group_presentations/curriculum.md:178-179` lists OB-1 open.
- WDP monograph (`/mnt/project-files/witnessed_difference_programme.md`):
  `retraction` occurs in R4 (abstract cochain carrier transport) and
  WDP-CH16 (chain contractions); no `sectionLift`, `old-image` or S(n)
  retraction statement.

## Receipts

Toolchain: Lean 4.34.0 (commit `293d5d0`), Lake 5.0.0, installed in the
cloud container from the GitHub release tarball
`lean-4.34.0-linux.tar.zst` (the elan host is blocked by the proxy).

```
$ cd education/symmetric_group_presentations/lean4
$ lake --version
Lake version 5.0.0-src+293d5d0 (Lean version 4.34.0)
$ lake build
✔ [2/6] Built SnSyntax
✔ [3/6] Built SnCarrier
✔ [4/6] Built SnTheorems
ℹ [5/6] Built SnOffImage
info: SnOffImage.lean:243:0: 'SnOffImage.old_image_base'' depends on axioms: [propext]
info: SnOffImage.lean:244:0: 'SnOffImage.accepted_only_from_section' depends on axioms: [propext, Quot.sound]
info: SnOffImage.lean:245:0: 'SnOffImage.nonDescent_iff_off_image' depends on axioms: [propext, Quot.sound]
info: SnOffImage.lean:246:0: 'SnOffImage.sectionLift_injective' depends on axioms: [propext]
info: SnOffImage.lean:247:0: 'SnOffImage.retraction_stage_strict' depends on axioms: [propext, Quot.sound]
info: SnOffImage.lean:248:0: 'SnOffImage.inImage_iff' depends on axioms: [propext, Quot.sound]
Build completed successfully (6 jobs).
exit status: 0
```

Tested scope: the four roots `SnSyntax`, `SnCarrier`, `SnTheorems`,
`SnOffImage` of package `sn_presentation`; no `sorry`, `admit`, `axiom`,
`unsafe`, `partial` or `native_decide` in the new file (grep). Thirteen
`decide` instance checks elaborate inside the file. For Jeremy on Windows,
from `symmetric_group_presentations/lean4/`: `lake build`, then read the six `#print axioms`
lines.

## Compaction envelope

- **Supports:** for the pinned `SnCarrier` model, `retractionDownMap n`
  accepts exactly the images of `sectionLift n`, the witness is unique, the
  stage test is exact, and membership in the image is decidable; axioms
  within `{propext, Quot.sound}`.
- **Does not support:** any carrier cardinality claim, OB-1, any S(n) stage
  beyond the five base shapes, any statement about the wire grammar or the
  Python codec, and any change to the sealed deposit.
- **Narrowest defensible claim:** in `symmetric_group_presentations/lean4/SnOffImage.lean`,
  compiled with Lean 4.34.0, `retractionDownMap n p = .accepted q` implies
  `∃ b, p = sectionLift n b ∧ q = b.toPresentation`.
- **Next test:** `cd education/symmetric_group_presentations/lean4 && lake build`
  on Jeremy's machine, confirming the six axiom lines above.
- **Changeset:** branch `claude/sn-off-image-refusal-vjruc5` from
  `8ac5da188`; files `symmetric_group_presentations/lean4/SnOffImage.lean` (new),
  `symmetric_group_presentations/lean4/lakefile.lean` (one root appended),
  `symmetric_group_presentations/curriculum.md` (one bullet added at Lesson 6),
  `symmetric_group_presentations/docs/off_image_refusal_note.md` (new).
