# Redundant numeral checker review

AuthorityEffect: None. Retention labels do not assert perfection.

| File | Initial | Final | Disposition |
|---|---:|---:|---|
| `checks/independent/fq-gap-c500-original-targets.py` |3|1|Exact archive retained; duplicate executable removed|
| `checks/independent/fq-gap-custody-and-receipts.py` |3|1|Exact archive retained; duplicate executable removed|
| Two original-source text archives |new|5|Required review custody|

Every line of both scripts was reviewed and replayed in normal and optimized
Python before archival. The C500 checker reports `checks=8` but executes49
guards across9 static sites. Its raw affine helpers also admit booleans and
floats instead of enforcing the natural-number domain. The custody checker
repeats three closed numeral facts. Neither exposes a needed production API.

Their complete arithmetic already appears in the retained derivation notes
and the cited `OriginalTargetNumerals.lean` and `CustodyReceiptNumerals.lean`.
The actual C500 origin is OriginalTargetNumerals, not the differently scoped
PromptC500Ledger module. Source reading confirms the same affine endpoints,
clause counts/labels and three custody numeral facts. No new Lean build is
claimed, and these numeral facts do not close either scientific target.

No explicit filename reference or executable caller exists outside review
metadata. The overclaim scanner does include an optional node-id-derived
filename when it exists; it does not require that file. Its numeric-claim rule
skips these two OPEN nodes. Directory-wide static lint similarly discovers
existing files without requiring either name. The current DAG and evidence
map cite the retained Lean declarations rather than these Python scripts.

The obsolete implementations are preserved byte-for-byte as `.py.txt`
review inputs, together with original output, source hashes, observed guard
counts and consumer/origin custody. Their active copies are removed rather
than assigning L4B to literal arithmetic utilities. No historical contract is
discarded: neither original has a companion. All retained active code must
still satisfy the requested L4B floor. This retirement adds no new code file.

The separate postflight receipt verifies exact archives, absence of retired
paths, unchanged origins/DAG, and the existing scanner/static-analysis tests.
Review continues with `fq-gap-continuum-hilbert-lift.py`, followed by the
remaining Stone, tensor and U1 checks before later checks and code.
