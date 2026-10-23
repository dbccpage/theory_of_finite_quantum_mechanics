# normal_forms

Authority effect: None.

This folder holds two things. `contracts/` is a set of normal-form contracts
imported unchanged from another project. `sql/` is the start of a relational
schema in ANSI SQL for this repository's own facts, which uses those contracts
as a design vocabulary and also stores them as rows.

The repository is meant to be relational. This is a first slice, not a finished
model. `sql/README.md` lists what is covered and what is not.

## What the imported contracts are

They are YAML contracts from the Symbol Game / Proposal Fidelity Protocol
project, copied from
`the_symbol_game/omega_engine_pfp/infrastructure/yaml/nf/`. Each one names an
anomaly it is meant to exclude, an invariant it preserves, what it does not
claim, and a terminal routing vocabulary (`Accept`, `Reject`, `Decompose`, and
so on). They are imported as written. This repository did not author them,
did not run the checkers they mention, and has not reviewed their mathematical
content. Their authority effect here is None.

### True normal forms versus extended contracts

The source README separates two kinds of contract:

* **True normal forms** (`qualifies_as_true_normal_form: true`): relational
  forms defined by project-join decomposition or by functional and multivalued
  dependencies: 1NF through 6NF, BCNF, ETNF, EKNF, RFNF, SKNF. A decomposition
  into one of them is meant to rejoin losslessly.
* **Extended or canonical form contracts** (`qualifies_as_extended_form: true`,
  `qualifies_as_true_normal_form: false`): contracts for anomaly exclusion,
  canonicalization, invariant preservation and terminal routing, where
  reconstruction is by a compilation pass, a witness or a boundary map and not
  by a flat relational join. The source README gives claim hygiene (EQNF) and
  proposal fidelity (PFNF) as examples.

Not every contract states which kind it is. `sql/universe.sql` records a
`category` for each, computed by the loader from the contract's own
`quadrilateral` flags and from `nf_domain_index.yaml`, with the value
`unstated` when neither says. In the imported set: 11 true normal forms, 10
extended form contracts, 23 contracts that say they are not true normal forms
without claiming the extended label, and 13 that say nothing. The source marks
DKNF `qualifies_as_true_normal_form: false`; that is the source's classification
and is kept as written.

## What was taken, and why

The selection was specified by name, not by reading each contract against this
repository.

* **All 25 contracts the source `index.yaml` lists as `active`.** These are the
  classical forms (1NF to 6NF, BCNF, DKNF, EKNF, ETNF, RFNF, SKNF), the `ddc`
  family (context boundary, dual witness, Hodge canonical, lift ledger, loss
  ledger, refusal receipt, terminal partition, trace Merkle), three `change`
  contracts, `nf.experimental.qm_classical` and `nf.operational.schema-totality`.
* **32 drafts judged near this repository's subject matter by name:**
  `nf.derivation.*` (10), `nf.evidence.*` (5), `nf.fsp.*` (2), `nf.coda.eqnf`
  (claim hygiene), `nf.pfp.pfnf`, `nf.mssn`, `nf.mssn.bqnf`, `nf.wdp.wdnf`,
  `nf.physics.schlafli_nf`, `nf.physics.bqnf_regge`, `nf.physics.bianchi_regge`,
  `nf.experimental.bell_contextuality`, `nf.classical.0nf`, `nf.classical.nf2`,
  `nf.query.spja`, `nf.bridge.wir_relvar`, `nf.cochain.dhnf`,
  `nf.cohomology.acnf`.
* **The golden files** from `_golden_nfs/` (`normal_form_contract_schema.yaml`,
  `normal_form_definitions.yaml`, `standard.yaml`, `normal_forms_schema.sql`),
  placed beside the contracts so that `schema_ref: ./normal_form_contract_schema.yaml`
  resolves. The source's `README.md` (as `SOURCE_README.md`), `index.yaml` and
  `nf_domain_index.yaml`.

In all, 64 of the 157 files in the source folder were copied: 57 contracts
(25 active and 32 draft), the 4 golden files, the 2 indexes and the README.
The other 93 were not copied. `contracts/PROVENANCE.json` lists each one with
a reason; by category: 55 contracts not on the requested list, 20 compiled
`.pyc` files, 5 demo data files, 4 images, 3 planning documents, 2 other
`bqnf/` variants, 2 runtime schema or catalog files, and 2 top-level SQL files
that are not the golden schema.

`nf.change.bqnf.fermion_sign` is in the `bqnf/` subfolder of the source. It is
copied flat into `contracts/` so its `schema_ref` resolves; PROVENANCE keeps its
original relative path.

## Bytes and provenance

Every copied file is byte-identical to its source. `contracts/PROVENANCE.json`
records, for each: the original absolute path, the relative source path, the
sha256, the size in bytes and the status in the source `index.yaml`. The
loader in `sql/` re-checks each contract's sha256 on every run, and
`.gitattributes` marks `normal_forms/contracts/**` as `-text` so that line-ending
conversion cannot change the bytes. The source files use LF line endings.

Known imperfections, left as they are:

* **Mojibake in `SOURCE_README.md`.** The em dash (U+2014) and en dash (U+2013)
  were encoded as UTF-8, decoded as Windows-1252 and encoded as UTF-8 again, so
  the file contains the three-character sequences U+00E2 U+20AC U+201D (12
  times: the front-matter title, the H1 and ten section headings) and
  U+00E2 U+20AC U+201C (once, in a bullet) where a dash was meant. Not
  corrected, because the file is a byte-identical copy.
* **Links that do not resolve here.** The source README links to files in its
  own tree (`../../13_normal_forms/...`, `nf_domain_index.py`) that were not
  copied.
* **One `schema_ref` that does not resolve.** `nf.experimental.qm_classical`
  has `schema_ref: ./_golden_nfs/normal_form_contract_schema.yaml`; the golden
  files are flat in `contracts/`, so that path is dangling.
* **Source `index.yaml` disagrees with two contracts.** `nf.classical.eknf` is
  `active` in the index but `draft` in its own `contract_status`;
  `nf.cohomology.acnf` is `draft` in the index (it also appears under
  `deprecated`) and `deprecated` in its own `contract_status`.
  `nf.operational.schema-totality` is `active` in the index but its identity
  block has no `contract_status`, `verification_status` or `theory_status`.
* **Statuses outside the source schema.** Two copied contracts
  (`nf.physics.bianchi_regge`, `nf.physics.bqnf_regge`) have
  `theory_status: admitted`, which is not in the source's own enum
  (`established`, `proposed`, `experimental`). The `nf_theory_status` table
  stores the value as written and has no check on it.

## Status of each contract, from the contracts themselves

`index` is the status in the source `index.yaml`. `contract_status`,
`verification_status` and `theory_status` are each contract's own
`identity` fields. `category` is the loader's rule described above.

How to read the fields. `verification_status: absent` means the contract names
no checker; `executable` means the source project says an executable check
exists. None of that code was copied here or run, and no imported contract has
`verification_status: machine_checked`. Contracts that cite Lean theorems or
checkers (for example the BCNF contract cites `is_bcnf_compliant` and
`bcnf_implies_3nf`) are citing the source project's files, which are not in
this repository. `theory_status: established` says the underlying theory is
textbook material in the source's view; it is not a statement that this
repository checked anything. Of the 57 contracts, 27 have `executable`, 29
have `absent`, and 1 has no value; 36 are `established`, 16 `proposed`, 2
`experimental`, 2 `admitted`, and 1 has no value.

| nf_id | short name | family | category | index | contract_status | verification_status | theory_status |
|---|---|---|---|---|---|---|---|
| `nf.change.bqnf.fermion_sign` | BQNF-FSIGN | change | unstated | active | active | executable | proposed |
| `nf.change.rational_quotient` | RATIONAL_QUOTIENT | change | unstated | active | active | executable | proposed |
| `nf.change.sign_switching` | SIGN_SWITCHING | change | unstated | active | active | executable | proposed |
| `nf.classical.1nf` | 1NF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.2nf` | 2NF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.3nf` | 3NF | shape | true_normal_form | active | active | executable | established |
| `nf.classical.4nf` | 4NF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.5nf` | 5NF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.6nf` | 6NF | shape | true_normal_form | active | active | executable | established |
| `nf.classical.bcnf` | BCNF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.dknf` | DKNF | shape | not_true_normal_form | active | active | absent | established |
| `nf.classical.eknf` | EKNF | shape | true_normal_form | active | draft | absent | established |
| `nf.classical.etnf` | ETNF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.rfnf` | RFNF | shape | true_normal_form | active | active | absent | established |
| `nf.classical.sknf` | SKNF | shape | true_normal_form | active | active | absent | established |
| `nf.ddc.context_boundary` | CBNF | topology | not_true_normal_form | active | active | executable | established |
| `nf.ddc.dual_witness` | DWNF | evidence | not_true_normal_form | active | active | executable | established |
| `nf.ddc.hodge_canonical` | HCNF | shape | not_true_normal_form | active | active | executable | established |
| `nf.ddc.lift_ledger` | LNLF | transport | not_true_normal_form | active | active | executable | established |
| `nf.ddc.loss_ledger` | LLNF | transport | not_true_normal_form | active | active | executable | established |
| `nf.ddc.refusal_receipt` | RRNF | evidence | not_true_normal_form | active | active | executable | established |
| `nf.ddc.terminal_partition` | TPNF | authority | not_true_normal_form | active | active | executable | established |
| `nf.ddc.trace_merkle` | TMNF | runtime | not_true_normal_form | active | active | executable | established |
| `nf.experimental.qm_classical` | QCNF | experimental | extended_form_contract | active | active | executable | experimental |
| `nf.operational.schema-totality` | SQL-TOTAL | evidence | not_true_normal_form | active | (absent) | (absent) | (absent) |
| `nf.bridge.wir_relvar` | WIR-Relvar Bridge | bridge | unstated | draft | draft | absent | proposed |
| `nf.classical.0nf` | 0NF | shape | not_true_normal_form | draft | draft | executable | established |
| `nf.classical.nf2` | NF2 | shape | not_true_normal_form | draft | draft | absent | proposed |
| `nf.cochain.dhnf` | DHNF | shape | extended_form_contract | draft | draft | absent | established |
| `nf.coda.eqnf` | EQNF | epistemic | extended_form_contract | draft | draft | executable | established |
| `nf.cohomology.acnf` | ACNF | experimental | extended_form_contract | draft | deprecated | absent | proposed |
| `nf.derivation.aonf` | AONF | derivation | unstated | draft | draft | executable | established |
| `nf.derivation.apnf` | APNF | derivation | unstated | draft | draft | absent | established |
| `nf.derivation.ignf` | IGNF | derivation | unstated | draft | draft | absent | established |
| `nf.derivation.irnf` | IRNF | derivation | unstated | draft | draft | absent | established |
| `nf.derivation.lsnf` | LSNF | derivation | unstated | draft | draft | absent | established |
| `nf.derivation.obnf` | OBNF | derivation | unstated | draft | draft | executable | established |
| `nf.derivation.pdnf` | PDNF | derivation | unstated | draft | draft | executable | established |
| `nf.derivation.rpnf` | RPNF | derivation | unstated | draft | draft | executable | established |
| `nf.derivation.scnf` | SCNF | derivation | unstated | draft | draft | executable | established |
| `nf.derivation.sernf` | SERNF | derivation | not_true_normal_form | draft | draft | executable | established |
| `nf.evidence.cdc` | CDCEF | evidence | not_true_normal_form | draft | draft | absent | proposed |
| `nf.evidence.certificate` | CertF | evidence | extended_form_contract | draft | draft | absent | proposed |
| `nf.evidence.ddanf` | DDANF | evidence | extended_form_contract | draft | draft | absent | proposed |
| `nf.evidence.loss_ledger` | LLF | evidence | extended_form_contract | draft | draft | absent | proposed |
| `nf.evidence.provenance` | ProvF | evidence | not_true_normal_form | draft | draft | absent | proposed |
| `nf.experimental.bell_contextuality` | BellCNF | experimental | not_true_normal_form | draft | draft | absent | experimental |
| `nf.fsp.bssnf` | BSS-NF | representation | extended_form_contract | draft | draft | absent | proposed |
| `nf.fsp.micnf` | MIC-NF | representation | extended_form_contract | draft | draft | absent | proposed |
| `nf.mssn` | MSSNF | shape | not_true_normal_form | draft | draft | executable | proposed |
| `nf.mssn.bqnf` | MSSN-BQNF | change | not_true_normal_form | draft | draft | executable | proposed |
| `nf.pfp.pfnf` | PFNF | coda | extended_form_contract | draft | draft | executable | established |
| `nf.physics.bianchi_regge` | RBNF | physics | not_true_normal_form | draft | draft | absent | admitted |
| `nf.physics.bqnf_regge` | BQNF-REGGE | physics | not_true_normal_form | draft | draft | absent | admitted |
| `nf.physics.schlafli_nf` | SIDNF | physics | not_true_normal_form | draft | draft | absent | established |
| `nf.query.spja` | SPJA | query | not_true_normal_form | draft | draft | executable | proposed |
| `nf.wdp.wdnf` | WDNF | derivation | not_true_normal_form | draft | draft | executable | established |

## How this repository uses them

Not yet beyond two things. `sql/universe.sql` is written so that each table is
in BCNF, with the one-attribute-per-relation tables labelled "6NF-style", and
`sql/test_universe.py` checks the lossless-join property the 6NF contract
describes on this repository's own DAG data. Neither step runs the imported
contracts' own checkers, and nothing here declares that this repository
satisfies a contract in the sense those contracts define. The contracts are also
loaded as rows (`nf_contract`, `nf_non_claim` and related tables) so that they
can be queried with the facts they describe.

## Layout

```
normal_forms/
  README.md                this file
  contracts/               imported, byte-identical
    PROVENANCE.json
    SOURCE_README.md  index.yaml  nf_domain_index.yaml
    normal_form_contract_schema.yaml  normal_form_definitions.yaml
    standard.yaml  normal_forms_schema.sql          (golden files)
    nf.*.yaml                                       (57 contracts)
  sql/
    universe.sql  load_universe.py  test_universe.py  README.md
```
