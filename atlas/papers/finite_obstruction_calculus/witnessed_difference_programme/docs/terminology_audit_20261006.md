# Manuscript terminology audit, 6 October 2026

The user requested removal of unexplained internal language and invented
standards from the main WDP manuscript. This audit concerns the editable
Markdown source, not an already exported PDF or deposited release.

## What the numbered source label meant

The label “Source-25” was an informal archive index for the twenty-fifth
derivation in `dbccpage/H3V7N5QF`, revision
`5d9488324ce976817987bd83a28d901371cfc073`:

- [Original paper](https://github.com/dbccpage/H3V7N5QF/blob/5d9488324ce976817987bd83a28d901371cfc073/paper/twentyfifth/paper.md), heading and opening findings, accessed lines 1–85.
- [Original implementation](https://github.com/dbccpage/H3V7N5QF/blob/5d9488324ce976817987bd83a28d901371cfc073/code/twentyfifth/state.py), opening specification and five edit cases, accessed lines 1–230.

Its state has a finite set of terms, two nonnegative integer relation-count
tables, and oriented filled triples. The five edits identify terms, remove
an assertion, fill a triple, add a term, or add an assertion. The number 25
has no mathematical force. The implementation explicitly distinguishes
given seed text from chosen readings: orientation, transport of triples
under identification, and ordering of offered edits are choices, not
standards. Those assumptions now appear with direct citations in P.7.

## Changes to public mathematical prose

| Previous wording | Descriptive wording or treatment |
|---|---|
| Source-25 / source-25 | Five-edit model, with its carrier, operations and original source defined in P.7 |
| source-23 | Two-relation model; its definition and source reference accompany L.5 |
| degree-one spine | Independent detector basis; unrelated Lean import “spine” becomes entry module |
| E-observation | Validated observation, retaining the existing explicit predicate |
| Imported standard | Cited result; external theorem hypotheses and sources remain |
| Gate E | Trotter-response check, with the exact finite counterexample described |
| Original six / operational ten / world five / normalized nine | Observer tuples described by their component counts and roles |
| AutoP / PTIR | Repository schema grammar / typed intermediate representation, described as software interfaces |
| receipt / contract in prose | Verification record / specification; literal API names and link paths remain exact |
| antibody in the new assignment | Reusable rejection rule, with its actual predicate and validity set supplied |

Stable claim identifiers are lookup keys for evidence, not standards. The
manuscript now says this explicitly. Existing implementation identifiers,
historical records, raw source archives, hashes and serialized schemas are
retained as literal evidence references rather than silently renamed.
Real mathematical terminology, such as a standard basis, Bayes' rule,
linear programming and Boyce–Codd normal form, is not an invented standard.

The research workflow itself contains internal policy names such as
`SPK-001` and `MSS-0`. They are repository workflow conventions, not external
mathematical standards, and are not imported into the new theorem or GLM
assignment as assumptions. The source manuscript's audit found no such
policy names asserted as standards. The user request takes precedence over
any suggestion to turn workflow vocabulary into mathematical foundations.

## Evidence boundaries

The source excerpts and original-byte hashes are retained in the research
source inventory. Changed headings keep compatibility anchors where a
renamed heading had an established link. No historical manifest was
regenerated to imply a new release; no PDF, archive or deposit was replaced.
The dirty main checkout was left untouched. The editable result is on
`codex/wdp-deep-derivations-20261006` in the isolated checkout.
