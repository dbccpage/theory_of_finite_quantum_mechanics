# GTH-LANG-LIMITS

Stage: [GENESIS_TO_HIGHER](../stages/GENESIS_TO_HIGHER.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let S be a theory in classical first-order logic with a primitive recursive coding of its syntax. Write code(psi) for the code of a sentence psi and num(n) for the numeral of a natural number n. Assume (i) consistency: there is no sentence psi such that S derives both psi and the negation of psi. Assume (ii) a primitive recursive relation Proof such that psi is a theorem of S exactly when Proof(p, code(psi)) holds for some natural number p, and Proof is represented at standard numerals: for all natural numbers p and s, S derives the sentence expressing Proof(num(p), num(s)) when the relation holds and derives its negation when the relation fails. Assume (iii) that S derives every true Delta_0 sentence of this coding; that the substitution function subst, sending the code of a formula with one free variable and a number n to the code of the sentence obtained by substituting num(n) for that variable, is represented in S; that the primitive recursive function neg on codes, with neg(code(psi)) equal to code(the negation of psi), is represented in S; and that for each standard natural number n, S derives both that every w with w \< num(n) equals one of num(0), ..., num(n-1), and that every w satisfies w \< num(n) or w = num(n) or num(n) \< w. Then there is a sentence phi such that S derives neither phi nor the negation of phi. The diagonal lemma from representation of subst supplies, for the negation of the Rosser formula RosserProv(v) given by existence of a u such that Proof(u, v) and such that Proof(w, neg(v)) fails for every w \< u, a sentence phi such that S derives the biconditional of phi and the negation of RosserProv(num(code(phi))). If S derives phi, a standard derivation code p, clause (i), numeral-wise representation of Proof, and the schema that every number below num(p) equals one of num(0), ..., num(p-1), yield a derivation of RosserProv(num(code(phi))) and then of the negation of phi. If S derives the negation of phi, a least standard derivation code q of that negation, numeral-wise representation of Proof, the same bounded schema at q, and the schema that every number is below num(q), equal to num(q), or above num(q), yield a derivation of the negation of RosserProv(num(code(phi))) and then of phi. Either case contradicts (i). Separately, drop (i) and (ii) and keep (iii): if a formula Tr(x) is such that S derives the biconditional of Tr(num(code(psi))) and psi for every sentence psi, the same diagonal lemma applied to the negation of Tr supplies a sentence lambda for which those biconditionals yield a derivation of both lambda and its negation, so S is inconsistent. Both conclusions use only the hypotheses just stated and classical first-order logic.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The two limit statements are conditional on the hypotheses in the statement. The priced admission language is not defined and is not shown to meet (i), (ii) or (iii). Nothing is formalised in Lean. Admitting a later theory is a priced import record, not a derivation from the core.

## Source status

Prose under hypotheses (i), (ii) and (iii) in the statement. Those hypotheses do not mention the priced admission language. No Lean declaration.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/34_genesis_to_higher/tfq_2411_gth_lang_limits.md`

- file: [dag/derivations/34_genesis_to_higher/tfq_2411_gth_lang_limits.md](../../../dag/derivations/34_genesis_to_higher/tfq_2411_gth_lang_limits.md)
- sha256 (`lf-normalised`): `f3cacf7def8669f89c34d66b990c349adc4a7ba0583c0c63c3ff9c39d93fd6db`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2411
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/gth_lang_limits.md`

- file: [dag/derivations/independent/gth_lang_limits.md](../../../dag/derivations/independent/gth_lang_limits.md)
- sha256 (`lf-normalised`): `2087165479a8aaf31b5578d806870c619657b6c5350ee477b8098fdb0a72609a`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:book:Tarski-1935-Wahrheitsbegriff-Studia-Philosophica-1`
- `external:doi:10.1007/BF01700692`
- `external:doi:10.2307/2269028`

## Routes

Incoming (1):

- `GTH-R-GTH-LANG-LIMITS` `RECORD_PARENT`: [GTH-LANG-IMPORT](GTH-LANG-IMPORT.md) (OPEN)

Outgoing (1):

- `OPS-R-AXIS2-META-CARRIER` `GAP_NO_DERIVATION`: [OPS-AXIS2-META-CARRIER](OPS-AXIS2-META-CARRIER.md) (IMPORTED_ASSUMPTION)
