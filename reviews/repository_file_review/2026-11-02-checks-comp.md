# File review: six computation fixtures

AuthorityEffect: None.

All lines of the six Python files and the logical contents/history of their six
adjacent JSON contracts were reviewed. The source and companion bytes matched
the isolated review worktree. Each script ran with Python 3.14.7 and
`-I -B -X utf8`, reporting zero failures. These are closed finite fixtures;
the corresponding broad computation questions remain open or conditional.

The source files below each receive **file score 3**: each is referenced in
historical review/replay records and can be composed into a shared independent
finite-fixture runner with a separately named case. Retain the original byte
history and update any affected references before removing a file; do not
claim that composition proves the wider node. The six adjacent companions each
receive **file score 4**, because a source-bound contract is required and its
current evidence/score needs repair. Their historical `L2D` scores are below
L4B. These small literal-processing fixtures are L1 under SCORING.md; a new
five-gate assessment remains incomplete.

| Source and SHA-256 | Specific finding and proposed composition |
|---|---|
| `comp-c2-step3-not-word-step.py` `d40b46d3aa9c0835f1270c0911119190c5c060e48e15e5b5bd8c4fcc967dfb7c` | Three list replacements and one merge map are bounded examples, not all Genesis Step3 states. Its `hole` helper records an invalid split but still returns a fabricated result; use a typed error and share the replacement primitive with the fixed-target case. |
| `comp-c3-no-fixed-bound.py` `8fd49bce8aa54691b24d4c86d1a207726f5ac49968ca1857d961c321c3c27dd0` | This no-rule, one-letter example checks a fixed bound of 1. Preserve that exact case; it is not a general normal-form search or an unbounded-reachability proof. |
| `comp-c6-tm0-output-form-open.py` `0ed7501663c23122f78cb22ed8551d249aeb51f7abab915b4f32e3bf5f85dc64` | A toy write-and-halt function and constant evaluator agree on a small grid. It is explicitly not the named machine or `Code.eval`; keep those boundaries. |
| `comp-c7-encoded-instance-reduction.py` `2a2a523c4912755c7cfd017c265ca6445e23c0767f8826c28751c3071c1cbf8d` | Two codes illustrate predicate composition. This does not establish a computable reduction or decide an infinite language. Its independent derivation-note evidence pin also no longer matches. |
| `comp-c7-fixed-target-open.py` `8c094e74169a3155e058fc0a98d3e9cf2c431f361fc4b391379869c7723a5b7f` | Two fixed erasures reach `[0]`; these are not the whole rule system. Its duplicate `hole` helper also returns a result after an invalid split. |
| `comp-c8-minimality-fence.py` `5551468b4857719c8cfa6986bf753c4c42953a54d00cdc916cca4bf9ea95c3dd` | Two literal marks and a blank establish one finite tape fixture, not a machine or a minimality theorem. Preserve the fixture while sharing the runner. |

In each companion, the current source digest matches, and all current and
historical JSON entry digests validate. However, the cited replay receipt in
**each of the six** no longer matches its recorded evidence hash. Preserve the
old entries and append new source-specific, byte-bound evidence and incomplete
scores; do not silently rewrite the historical receipts.

Five scripts execute at import and call `SystemExit`; only the C3 file has a
main guard. The fixtures can share a small domain-specific runner with named
case IDs and structured pass/failure values, while keeping any independent
oracle separate from the implementation under test. A direct adversarial
probe of both `hole` helpers passed `word=[9]`, `left=[]`, `lhs=[1]`,
`rhs=[0]`, `right=[]`: each printed a failed split but returned `[0]`. The
current CLI records that failure in a global counter and eventually exits
nonzero; callers of the helper can nevertheless receive an invalid result.
