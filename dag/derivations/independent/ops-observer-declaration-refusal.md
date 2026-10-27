Status: AI-drafted, awaiting human review.

# OPS-OBSERVER-DECLARATION-REFUSAL

The node stays CONDITIONAL. This note records one five-field classifier for one Bell label. The comparison does not read a defect.

## Texts

The kernel text is "support presheaf over the maximal-context cover {0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2".

The admissibility text is "noncontextual polytope conv(A)".

The norm text is "L1".

The terminal text is "defect = 0 -> ExactRepair; defect > 0 and a support-level global section exists -> ClosedResidual; defect > 0 and none exists -> OpenObstruction".

The layer text is "WDP-CH10-D01 diagnostic".

The authority text on the accepted class is "None".

## Classification

A draft has five fields, in order: kernel, admissibility, norm, terminal, layer. Each field is either missing or a text.

Walk the fields in that order. A missing value, the empty string, or one space on the first such field is the undeclared class of that field. A text other than the empty string, one space, and that field's accepted text is the unsupported class of that field, and the class keeps the declared text. If every field holds its accepted text, the class is accepted.

The finite case checked here starts from the draft of the five accepted texts and replaces one field.

## What is proved

- Replacing one field of that draft by a missing value, the empty string, or one space yields the undeclared class of that field.
- Replacing one field by a text other than the empty string, one space, and that field's accepted text yields the unsupported class of that field and keeps the declared text.
- The draft of the five accepted texts is the accepted class.
- The authority text of that class is "None".

The Lean declarations are `blank_on_accepted`, `mismatch_on_accepted`, `accepted_draft_class`, and `accepted_authority` in `lean4/ObserverDeclarationRefusal.lean`.

## What is assumed

String equality and the five fixed texts. No new axiom is declared. The node status stays CONDITIONAL. The Rust evaluator and its source tests are not run here.

## What is open

A defect receipt, Unicode whitespace other than one space, the terminal token, the typed profile, and any kernel label other than this Bell label are outside this slice.
