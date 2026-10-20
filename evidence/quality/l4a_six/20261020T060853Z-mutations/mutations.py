"""Designated semantic challenges in an owned source snapshot; all outcomes retained.

AuthorityEffect: None. Does not certify unchallenged symbols or failure classes.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from replay import (ROOT, RUST, digest, write, inventory, snapshot, execute,
                    remove_owned, dependency_sources)
import subprocess


def candidates():
    lie = "lie_theory/lib.rs"
    lggr = "local_green_global_red_lggr/lggr_v.rs"
    holo = "holonomy/connection.rs"
    matrix = "holonomy/matrix.rs"
    scalar = "linear_algebra/scalars.rs"
    hashing = "homology/hashing.rs"
    smith = "linear_algebra/smith_form.rs"
    entropy = "linear_algebra/entropy_dichotomy.rs"
    quintic = "linear_algebra/quintic_split.rs"
    adequacy = "local_green_global_red_lggr/adequacy.rs"
    rank = "homology/rank_certificate.rs"
    substitution = "homotopy_type_theory/substitution.rs"
    nerve = "homotopy_type_theory/quasi_category.rs"
    # Each literal recipe is deliberately source-specific. No blind substitutions.
    recipes = [
        ("SL01-denominator-domain", lie, "if *a11.denom() == 0 || *a22.denom() == 0 {", "if false {"),
        ("SL02-sign", lie, "left == -right", "left == right"),
        ("SL03-old-overflow", lie, "    left == -right", "    num_traits::Zero::is_zero(&(a11 + a22))"),
        ("SL04-widening", lie, "i128::from(*a11.numer()) * i128::from(*a22.denom())", "i128::from(a11.numer().wrapping_mul(*a22.denom()))"),
        ("LG01-inclusive-budget", lggr, "if cells > MAX_LGGR_CELLS {", "if cells >= MAX_LGGR_CELLS {"),
        ("LG02-product-preflight", lggr, "    admit_cell_count(cells(q.rows(), d.cols())?)?;", ""),
        ("LG03-matrix-domain", lggr, '    admit_coefficients("D", d.as_slice())?;', ""),
        ("LG04-witness-domain", lggr, '    admit_coefficients("witness", witness)?;', ""),
        ("LG05-soundness-rank", lggr, "if qd_rank == d_rank {", "if qd_rank <= d_rank {"),
        ("LG06-witness-nonzero", lggr, "if !dv_nonzero {", "if false {"),
        ("HO01-missing-source", holo, "id: edge.source.clone(),", 'id: "wrong-source".into(),'),
        ("HO02-missing-target", holo, "id: edge.target.clone(),", 'id: "wrong-target".into(),'),
        ("SC01-zero-denominator", "linear_algebra/scalars.rs", "if d == 0 {", "if false {"),
        ("SC02-domain-zero", scalar, "if num_traits::Zero::is_zero(value.denom()) {", "if false {"),
        ("SC03-domain-negative", scalar, "if value.denom() < &BigInt::from(0) {", "if false {"),
        ("SC04-domain-reduced", scalar, "if value.numer() != reduced.numer() || value.denom() != reduced.denom() {", "if false {"),
        ("SC05-real-admission", scalar, "        validate_rational(&real)?;", ""),
        ("SC06-imag-admission", scalar, "        validate_rational(&imag)?;", ""),
        ("SC07-wire-fields", scalar, "#[serde(deny_unknown_fields)]", ""),
        ("SC08-component-privacy", scalar, "    real: Q,\n    imag: Q,\n}\n\nimpl GaussianRational", "    pub real: Q,\n    pub imag: Q,\n}\n\nimpl GaussianRational"),
        ("SC09-product-real", scalar, "real: &self.real * &rhs.real - &self.imag * &rhs.imag,", "real: &self.real * &rhs.real + &self.imag * &rhs.imag,"),
        ("SC10-product-imag", scalar, "imag: &self.real * &rhs.imag + &self.imag * &rhs.real,", "imag: &self.real * &rhs.imag - &self.imag * &rhs.real,"),
        ("SC11-norm-sign", scalar, "        &self.real * &self.real + &self.imag * &self.imag", "        &self.real * &self.real - &self.imag * &self.imag"),
        ("SC12-inverse-sign", scalar, "imag: -&self.imag / &n,", "imag: &self.imag / &n,"),
        ("SC13-inverse-zero", scalar, "if num_traits::Zero::is_zero(&n) {", "if false {"),
        ("SC14-hash-domain", scalar, "if num_traits::Zero::is_zero(val.denom()) {", "if false {"),
        ("SC15-hash-normalization", scalar, "    let reduced = val.reduced();", "    let reduced = val.clone();"),
        ("SC16-integer-endian", scalar, "value.to_signed_bytes_le()", "value.to_signed_bytes_be()"),
        ("SC17-hash-length", scalar, "    hasher.update(&(bytes.len() as u64).to_le_bytes());", ""),
        ("SC18-hash-denominator", scalar, "    hash_bigint(hasher, reduced.denom());", "    hash_bigint(hasher, reduced.numer());"),
        ("HS01-matrix-refusal", hashing, "for val in m.as_slice() {\n        hash_rational(&mut hasher, val)?;", "for val in m.as_slice() {\n        let _ = hash_rational(&mut hasher, val);"),
        ("HS02-vector-refusal", hashing, "for val in v {\n        hash_rational(&mut hasher, val)?;", "for val in v {\n        let _ = hash_rational(&mut hasher, val);"),
        ("HS03-weights-refusal", hashing, "        hash_rational(&mut hasher, w)?;", "        let _ = hash_rational(&mut hasher, w);"),
        ("HS04-graded-binding", hashing, "hash_vector(v)?.as_bytes()", "hash_vector(&[])?.as_bytes()"),
        ("SM01-workspace-inclusive", smith, "if cells > limit {", "if cells >= limit {"),
        ("SM02-pivot-limit", smith, "if iterations == limit {", "if false {"),
        ("SM03-bezout-transform", smith, "let right = -q2 * &*a + q1 * &*b;", "let right = q2 * &*a + q1 * &*b;"),
        ("SM04-row-repair-tracking", smith, "        add_integer_row(&mut self.u, k, i);", ""),
        ("SM05-identity-refusal", smith, "if borrowed_integer_product(&borrowed_integer_product(u, matrix)?, v)?.as_slice()\n        != d.as_slice()\n    {", "if false {"),
        ("SM06-gcd-normalization", smith, "if old_r < BigInt::from(0) {", "if false {"),
        ("SP01-inclusive-elements", smith, "if requested > limit {", "if requested >= limit {"),
        ("SP02-vector-budget", smith, "let mut result = sparse_zeros(self.rows, limit)?;", "let mut result = sparse_zeros(self.rows, usize::MAX)?;"),
        ("SP03-dense-budget", smith, "let mut data = sparse_zeros(total, limit)?;", "let mut data = sparse_zeros(total, usize::MAX)?;"),
        ("SP04-storage-accounting", smith, ".checked_mul(2)\n            .and_then(|n| n.checked_add(nonzero))", ".checked_mul(1)\n            .and_then(|n| n.checked_add(nonzero))"),
        ("SP05-storage-budget", smith, "        admit_sparse_elements(storage, limit)?;", "        admit_sparse_elements(storage, usize::MAX)?;"),
        ("SP06-product-sign", smith, "result[*row] += value * &v[j];", "result[*row] -= value * &v[j];"),
        ("SP07-dense-coordinates", smith, "data[row * self.cols + j] = value.clone();", "data[row * self.cols + j] = -value;"),
        ("SP08-column-coordinates", smith, "(index / matrix.cols(), value.clone())", "(index / matrix.cols(), -value)"),
        ("BF01-finite-admission", adequacy, "BigRational::from_float(value).ok_or(NonFiniteFloat)", "Ok(BigRational::from_float(value).unwrap_or_else(BigRational::zero))"),
        ("BF02-binary-value", adequacy, "BigRational::from_float(value).ok_or(NonFiniteFloat)", "BigRational::from_float(value.trunc()).ok_or(NonFiniteFloat)"),
        ("AN01-top-capacity", adequacy, "    check_top_capacity(evidence, &value, &tolerance)?;", ""),
        ("AN02-section-norm", adequacy, "    check_section_norm(evidence, &tolerance)?;", ""),
        ("AN03-witness-attainment", adequacy, "    check_witness_attainment(evidence, &value, &tolerance)?;", ""),
        ("AN04-residual-gate", adequacy, "    check_numerical_residual(evidence)?;", ""),
        ("AN05-threshold-band", adequacy, "    check_threshold_band(declaration, &value, &tolerance)\n}", "    Ok(())\n}"),
        ("RK01-coefficient-admission", rank, "    check_coefficients(matrix, candidate)?;", ""),
        ("RK02-shape-admission", rank, "    check_shapes(matrix, candidate, rank)?;", ""),
        ("RK03-identity-admission", rank, "    check_split_identities(matrix, candidate, rank, budget)", "    Ok(())"),
        ("RK04-zero-identity", rank, "if !matrix.as_slice().iter().all(num_traits::Zero::is_zero) {", "if false {"),
        ("RK05-matrix-binding", rank, "if self.matrix_hash != hash_matrix(matrix)? {", "if false {"),
        ("RK06-identity-equality", rank, "if left != right {", "if false {"),
        ("RK07-rank-dimension", rank, "if rank > m.rows().min(m.cols()) {", "if false {"),
        ("RK08-elimination-sign", rank, "*entry -= &factor * pivot_entry;", "*entry += &factor * pivot_entry;"),
        ("RK09-pivot-normalization", rank, "*value /= &pivot;", "*value *= &pivot;"),
        ("RK10-pivot-clearing", rank, "let factor = std::mem::replace(&mut target[col], q(0));", "let factor = std::mem::replace(&mut target[col], q(1));"),
        ("RK11-coordinate-extraction", rank, "self.data.truncate(rows * self.cols);", "self.data.truncate(0);"),
        ("RK12-inverse-extraction", rank, "if index % self.cols >= n {", "if index % self.cols < n {"),
        ("RK13-certificate-privacy", rank, "    matrix_hash: Hash256,\n    rank: usize,\n    candidate: RankCandidate,", "    pub matrix_hash: Hash256,\n    pub rank: usize,\n    pub candidate: RankCandidate,"),
        ("RB01-inclusive-cells", rank, "if count > self.limits.max_matrix_cells {", "if count >= self.limits.max_matrix_cells {"),
        ("RB02-inclusive-work", rank, "if requested > self.limits.max_scalar_operations {", "if requested >= self.limits.max_scalar_operations {"),
        ("RB03-work-refusal", rank, "if requested > self.limits.max_scalar_operations {", "if false {"),
        ("RB04-product-debit", rank, "    budget.charge(operations)\n}", "    Ok(())\n}"),
        ("RB05-cell-refusal", rank, "if count > self.limits.max_matrix_cells {", "if false {"),
        ("RB06-product-work", rank, ".and_then(|n| n.checked_mul(inner))\n        .and_then(|n| n.checked_mul(2))", ".and_then(|n| n.checked_mul(inner))\n        .and_then(|n| n.checked_mul(1))"),
        ("RB07-reduction-work", rank, "    rows.checked_mul(2)\n        .and_then(|n| n.checked_add(1))", "    rows.checked_mul(1)\n        .and_then(|n| n.checked_add(1))"),
        ("RP01-inverse-admission-order", rank, "    budget.charge(reduction_work(n, cols, n)?)?;\n    let mut workspace = RationalRows::augmented_identity(matrix, budget)?;", "    let mut workspace = RationalRows::augmented_identity(matrix, budget)?;\n    budget.charge(reduction_work(n, cols, n)?)?;"),
        ("RP02-checker-admission-order", rank, "    preflight_split_work(matrix, rank, budget)?;\n    let identity = identity(rank, budget)?;", "    let identity = identity(rank, budget)?;\n    preflight_split_work(matrix, rank, budget)?;"),
        ("RP03-checker-preflight", rank, "    preflight_split_work(matrix, rank, budget)?;", ""),
        ("RP04-checker-candidate-clone", rank, "        check_candidate(matrix, &self.candidate, &mut budget)", "        let copied = self.candidate.clone();\n        check_candidate(matrix, &copied, &mut budget)"),
        ("EN01-stdin-injection", entropy, '"--inject" if has_path =>', '"--inject" =>'),
        ("EN02-external-integer", entropy, 'k.parse().map_err(|_| "APPROXIMATION_K_INTEGER_REQUIRED")?', '0'),
        ("EN03-mode-binding", entropy, '"--verdict-only" => Ok(RawEntropyMode::Verdict),', '"--verdict-only" => Ok(RawEntropyMode::Characteristic),'),
        ("AD01-boundary-check", adequacy, "    check_structural_boundary(declaration, records, boundary, &mut failures);", ""),
        ("AD02-ledger-check", adequacy, "        check_structural_segments(record, ledger, boundary, failures);", ""),
        ("AD03-direction-check", adequacy, "        check_protected_direction(item, expected, failures);", ""),
        ("QC01-metadata-tag", quintic, 'certificate["schema"] != SCHEMA', 'certificate["schema"] == SCHEMA'),
        ("QC02-discriminant-binding", quintic, 'if element(&certificate["discriminant"], algebra.d)? != disc {', 'if element(&certificate["discriminant"], algebra.d)? == disc {'),
        ("QC03-group-binding", quintic, 'if certificate["galois_group"] != group {', 'if false {'),
        ("MX01-constructor-scalar", matrix, "        data.iter().try_for_each(ExactScalar::validate_exact)?;", ""),
        ("MX02-setter-scalar", matrix, "        value.validate_exact()?;\n        self.data[index] = value;", "        self.data[index] = value;"),
        ("MX03-decoder-admission", matrix, "Self::try_new(wire.rows, wire.cols, wire.data).map_err(serde::de::Error::custom)", "Ok(Self { rows: wire.rows, cols: wire.cols, data: wire.data })"),
        ("MX04-index-boundary", matrix, "if row >= self.rows || col >= self.cols {", "if row > self.rows || col > self.cols {"),
        ("MX05-inclusive-cells", matrix, "if requested > limits.max_cells {", "if requested >= limits.max_cells {"),
        ("MX06-inclusive-work", matrix, "if requested > limits.max_operations {", "if requested >= limits.max_operations {"),
        ("MX07-product-index", matrix, "other.at(k, c)", "other.at(c, k)"),
        ("MX08-determinant-sign", matrix, "                determinant = -determinant;", ""),
        ("MX09-rank-increment", matrix, "            rank += 1;", ""),
        ("MX10-inverse-block", matrix, "if index % self.cols >= n {", "if index % self.cols < n {"),
        ("MX11-complex-product", matrix, "im: add_ref(&mul_ref(&a.re, &b.im), &mul_ref(&a.im, &b.re)),", "im: sub_ref(&mul_ref(&a.re, &b.im), &mul_ref(&a.im, &b.re)),"),
        ("MX12-complex-zero-inverse", matrix, "if n_sq.is_zero() {\n            return Err(HolonomyError::ZeroDivision);", "if n_sq.is_zero() {\n            return Ok(Self::zero());"),
        ("MX13-rational-zero-inverse", matrix, "if self.is_zero() {\n            Err(HolonomyError::ZeroDivision)", "if self.is_zero() {\n            Ok(Self::zero())"),
        ("MX14-storage-privacy", matrix, "    rows: usize,\n    cols: usize,\n    data: Vec<T>,\n}\n\nimpl<T: ExactScalar>", "    pub rows: usize,\n    pub cols: usize,\n    pub data: Vec<T>,\n}\n\nimpl<T: ExactScalar>"),
        ("MX15-domain-seal", matrix, "mod sealed {", "pub mod sealed {"),
        ("MX16-borrow-privacy", matrix, "    value: &'a T,", "    pub value: &'a T,"),
        ("MX17-borrow-admission", matrix, "        value.validate_exact()?;\n        Ok(Self { value })", "        Ok(Self { value })"),
        ("MX18-input-admission", matrix, "        admit_cells(self.rows, self.cols, limits)?;\n        admit_cells(other.rows, other.cols, limits)?;", ""),
        ("SU01-inclusive-limits", substitution, "if requested > limit {", "if requested >= limit {"),
        ("SU02-prefix-root", substitution, ".ok_or(SubstitutionError::TrailingToken { index })?", ".unwrap_or(0)"),
        ("SU03-lambda-arity", substitution, "Self::Lambda => 1,", "Self::Lambda => 0,"),
        ("SU04-lambda-binding", substitution, "Self::Lambda => child == 0,", "Self::Lambda => false,"),
        ("SU05-dependent-arity", substitution, "Self::Pi | Self::Sigma => 2,", "Self::Pi | Self::Sigma => 1,"),
        ("SU06-shift-boundary", substitution, "if *index < cutoff {", "if *index <= cutoff {"),
        ("SU07-capture-refusal", substitution, "if changed < cutoff {", "if false {"),
        ("SU08-negative-shift", substitution, ".checked_sub(amount.unsigned_abs())", ".checked_add(amount.unsigned_abs())"),
        ("SU09-target-depth", substitution, "Ok(*value == add(index, depth)?)", "Ok(*value == index)"),
        ("SU10-context-removal", substitution, "usize::from(*value > add(index, depth)?)", "0"),
        ("SU11-replacement-lift", substitution, "Token::Var(value) if *value >= depth =>", "Token::Var(value) if false =>"),
        ("SU12-name-preservation", substitution, "copied.push_str(name);", 'copied.push_str("");'),
        ("SU13-work-accounting", substitution, "mul(term.tokens.len(), 3)?", "mul(term.tokens.len(), 2)?"),
        ("SU14-name-accounting", substitution, "mul(count, replacement.name_bytes)?", "replacement.name_bytes"),
        ("SU15-term-privacy", substitution, "    tokens: Vec<Token>,\n    depths: Vec<usize>,\n    name_bytes: usize,\n}\nimpl Term", "    pub tokens: Vec<Token>,\n    pub depths: Vec<usize>,\n    pub name_bytes: usize,\n}\nimpl Term"),
        ("SA01-shift-allocation-order", substitution, "    check_shift(term, amount, cutoff, limits)?;\n    let mut output = Output::new(term.tokens.len(), term.name_bytes, limits)?;", "    let mut output = Output::new(term.tokens.len(), term.name_bytes, limits)?;\n    check_shift(term, amount, cutoff, limits)?;"),
        ("SA02-substitution-allocation-order", substitution, "            check_replacement(replacement, *depth, limits)?;", ""),
        ("QN01-inclusive-limits", nerve, "if requested > limit {", "if requested >= limit {"),
        ("QN02-endpoint-admission", nerve, "        category.check_endpoints()?;", ""),
        ("QN03-identity-admission", nerve, "        category.check_identities()?;", ""),
        ("QN04-composition-admission", nerve, "        category.check_compositions()?;", ""),
        ("QN05-unit-laws", nerve, "        category.check_units()?;", ""),
        ("QN06-associativity", nerve, "        category.check_associativity()?;", ""),
        ("QN07-table-orientation", nerve, "self.composition[first * self.arrows.len() + second]\n            .ok_or", "self.composition[second * self.arrows.len() + first]\n            .ok_or"),
        ("QN08-composition-domain", nerve, "if f.target != g.source {\n            return Err(CategoryError::NotComposable { first, second });", "if false {\n            return Err(CategoryError::NotComposable { first, second });"),
        ("QN09-inner-face-order", nerve, "self.category\n                .compose(self.edges[index - 1], self.edges[index])?", "self.category\n                .compose(self.edges[index], self.edges[index - 1])?"),
        ("QN10-first-face-start", nerve, "return self.vertex(1);", "return Ok(self.start);"),
        ("QN11-degeneracy-object", nerve, "edges.push(self.category.identity(object)?);", "edges.push(self.category.identity(0)?);"),
        ("QN12-path-admission", nerve, "if arrow.source != current {", "if false {"),
        ("QN13-limit-refusal", nerve, "if requested > limit {", "if false {"),
        ("QN14-category-privacy", nerve, "    objects: usize,\n    arrows: Vec<Arrow>,\n    identities: Vec<usize>,\n    composition: Vec<Option<usize>>,\n    limits: CategoryLimits,", "    pub objects: usize,\n    pub arrows: Vec<Arrow>,\n    pub identities: Vec<usize>,\n    pub composition: Vec<Option<usize>>,\n    pub limits: CategoryLimits,"),
        ("QN15-face-boundary", nerve, "if self.edges.is_empty() || index > self.dimension() {", "if self.edges.is_empty() || index >= self.dimension() {"),
        ("QN16-work-accounting", nerve, "mul(mul(cells, arrows)?, 5)?", "mul(mul(cells, arrows)?, 4)?"),
        ("QN17-identity-index", nerve, ".get(object)\n            .copied()", ".get(0)\n            .copied()"),
        ("QN18-simplex-privacy", nerve, "    category: &'a FiniteCategory,\n    start: usize,\n    edges: Vec<usize>,", "    pub category: &'a FiniteCategory,\n    pub start: usize,\n    pub edges: Vec<usize>,"),
    ]
    for filename, field in (("empty_type", "id"), ("unit_type", "unit_term_ref"),
                            ("sum_type", "left_type_ref"), ("pi_type", "family_ref"),
                            ("sigma_type", "base_type_ref")):
        recipes.append(("HT-" + filename, "homotopy_type_theory/" + filename + ".rs",
                        f"if self.{field}.is_empty() {{", "if false {"))
    # The staged trial and integrated replay share literal fault definitions;
    # execution and grading remain separately source-bound receipts.
    from a_infinity_trial import recipes as algebra_recipes
    recipes.extend((identity, "homotopy_type_theory/a_infinity.rs", before, after)
                   for identity, before, after, _ in algebra_recipes())
    result = []
    for identity, source, before, after in recipes:
        package = {"lie_theory": "tfqm_lie_theory", "holonomy": "tfqm_holonomy",
                   "homotopy_type_theory": "tfqm_homotopy_type_theory",
                   "linear_algebra": "tfqm_homology_linear_audit",
                   "homology": "tfqm_homology_linear_audit",
                   "local_green_global_red_lggr": "tfqm_local_green_global_red_lggr"}[source.split("/")[0]]
        result.append({"id": identity, "source": "code/rust/src/" + source,
                       "snapshot_source": "src/" + source, "before": before, "after": after,
                       "package": package, "outcome": "unrun"})
    return result


def classify(run, output):
    if run["timed_out"]:
        return "inconclusive", "Cargo deadline expired; no kill is inferred."
    if run["exit_code"] == 0:
        return "survived", "Selected suite passed."
    log = (ROOT / run["log"]).read_text(encoding="utf-8")
    if "could not compile" in log or "error[E" in log:
        return "invalid", "Compiler rejected candidate; excluded from eligible denominator."
    if "test result: FAILED" in log:
        return "killed", "Rust test harness reported an assertion/test failure."
    return "inconclusive", "Unsuccessful process without decisive compiler or assertion attribution."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", action="append", help="Select one or more designated ID prefixes.")
    parser.add_argument("--min-free-gib", type=int, choices=(1, 2, 3), default=3,
                        help="Pre-command headroom, not a disk guarantee. One GiB is restricted to the smaller HoTT-only campaign.")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / (stamp + "-mutations")
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / (stamp + "-mutations")
    sources = inventory()
    write(output / "source_manifest.json", sources)
    shutil.copyfile(__file__, output / "mutations.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), output / "replay.py")
    shutil.copyfile(Path(__file__).with_name("a_infinity_trial.py"), output / "a_infinity_trial.py")
    entries = [c for c in candidates() if not args.prefix or c["id"].startswith(tuple(args.prefix))]
    if args.min_free_gib == 1 and any(e["package"] != "tfqm_homotopy_type_theory" for e in entries):
        parser.error("One-GiB headroom is restricted to HoTT-only campaigns")
    write(output / "mutations.json", entries)
    receipt = {"AuthorityEffect": "None", "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
               "versions": {n: subprocess.check_output([n, "--version"], text=True).strip() for n in ("cargo", "rustc")},
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "runner_sha256": digest(output / "mutations.py"),
               "execution_helper_sha256": digest(output / "replay.py"),
               "algebra_recipe_source_sha256": digest(output / "a_infinity_trial.py"),
               "baselines": [], "restored_baselines": [],
               "build_cache_disposals": [],
               "minimum_free_build_bytes": args.min_free_gib * 1024**3,
               "headroom_scope": "Pre-command admission only; external disk activity can change free space during a command.",
               "scope": "Designated semantic faults only; no whole-file or system score is inferred."}
    print(output, flush=True)
    try:
        snapshot(work)
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(command, cwd=work, text=True, capture_output=True)
        (output / "cargo_metadata.json").write_text(meta.stdout, encoding="utf-8")
        (output / "cargo_metadata_stderr.log").write_text(meta.stderr, encoding="utf-8")
        receipt["metadata_capture"] = {"command": command, "cwd": str(work), "exit_code": meta.returncode,
                                       "sha256": digest(output / "cargo_metadata.json"),
                                       "stderr_sha256": digest(output / "cargo_metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        packages = sorted({c["package"] for c in entries})
        common = ["--offline", "--target-dir", str(work / "build"), "--quiet"]

        def run_package(package, log, test_filter=None, doc_only=False, integration=None):
            if shutil.disk_usage(ROOT).free < args.min_free_gib * 1024**3:
                remove_owned(work / "build", work)
                receipt["build_cache_disposals"].append({"before_log": log.name,
                    "reason": f"Completed Cargo cache removed to recover {args.min_free_gib} GiB headroom."})
            if shutil.disk_usage(ROOT).free < args.min_free_gib * 1024**3:
                return {"started": False, "exit_code": None, "reason": f"Less than {args.min_free_gib} GiB free"}
            # Holonomy includes compile-fail API boundary controls. Cargo's
            # default test target also executes doctests; --tests excludes them.
            targets = [] if package in ("tfqm_holonomy", "tfqm_homology_linear_audit", "tfqm_homotopy_type_theory") else ["--tests"]
            if test_filter:
                targets = ["--lib"]
            if doc_only:
                targets = ["--doc"]
            if integration:
                targets = ["--test", integration]
            selected = [test_filter] if test_filter else []
            before = shutil.disk_usage(ROOT).free
            run = execute(["cargo", "test", *common, "-p", package, *targets, *selected], work, log)
            run["disk_observation"] = {"free_before": before, "free_after": shutil.disk_usage(ROOT).free,
                "completed_cache_file_bytes": sum(p.stat().st_size for p in (work / "build").rglob("*") if p.is_file()),
                "scope": "Endpoint observations only; not a peak-space or external-activity guarantee."}
            return run

        eligible_packages = set()
        for package in packages:
            baseline = run_package(package, output / (package + "-baseline.log"))
            receipt["baselines"].append({"package": package, **baseline})
            if baseline["exit_code"] == 0:
                eligible_packages.add(package)
            print("baseline", package, baseline["exit_code"], flush=True)
        for entry in entries:
            if entry["package"] not in eligible_packages:
                entry["reason"] = "Baseline unavailable or unsuccessful."
                continue
            path = work / entry["snapshot_source"]
            original = path.read_bytes()
            try:
                source = original.decode("utf-8")
                if source.count(entry["before"]) != 1:
                    entry.update(outcome="invalid", reason="Recipe must match exactly one source site.")
                    continue
                path.write_bytes(source.replace(entry["before"], entry["after"], 1).encode("utf-8"))
                entry["candidate_sha256"] = digest(path)
                # Untouched and restored baselines remain complete. During an
                # injection, run the smallest source boundary that discharges
                # the designated fault, including its matching API doctests.
                filter_by_source = {"linear_algebra/scalars.rs": "linear_algebra::scalars",
                                    "homology/hashing.rs": "homology",
                                    "linear_algebra/smith_form.rs": "linear_algebra::smith_form",
                                    "linear_algebra/entropy_dichotomy.rs": "cli_contract_tests",
                                    "linear_algebra/quintic_split.rs": "quintic_validation_challenges"}
                filter_by_source["homology/rank_certificate.rs"] = "homology::rank_certificate"
                filter_by_source["homotopy_type_theory/substitution.rs"] = "substitution::"
                filter_by_source["homotopy_type_theory/quasi_category.rs"] = "quasi_category::"
                filter_by_source["homotopy_type_theory/a_infinity.rs"] = "a_infinity::"
                selected = filter_by_source.get(entry["source"].removeprefix("code/rust/src/"))
                # Cargo's TESTNAME filter on a default test command may omit
                # doctests entirely. Select the doc target explicitly for this
                # compile-fail API boundary; do not recast an earlier survivor.
                doc_only = entry["id"] in ("SC08-component-privacy", "RK13-certificate-privacy", "SU15-term-privacy", "QN14-category-privacy", "QN18-simplex-privacy", "AI14-field-privacy", "AI15-algebra-privacy", "AI16-operation-privacy")
                integration = "rank_allocation" if entry["id"].startswith("RP") else None
                if entry["id"].startswith("SA"):
                    integration = "substitution_allocation"
                if entry["id"].startswith("AA"):
                    integration = "a_infinity_allocation"
                if doc_only or integration:
                    selected = None
                entry["test_filter"] = selected
                entry["doc_only"] = doc_only
                entry["integration_target"] = integration
                run = run_package(entry["package"], output / (entry["id"] + ".log"), selected, doc_only, integration)
                entry["run"] = run
                if run.get("started") is False:
                    entry.update(outcome="unrun", reason=run["reason"])
                else:
                    outcome, reason = classify(run, output)
                    entry.update(outcome=outcome, reason=reason)
                print(entry["id"], entry["outcome"], flush=True)
            finally:
                path.write_bytes(original)
                entry["source_restored"] = digest(path) == sources[entry["source"]]
                write(output / "mutations.json", entries)
        for package in packages:
            receipt["restored_baselines"].append({"package": package,
                **run_package(package, output / (package + "-restored.log"))})
        receipt["dependency_sources_unchanged"] = all(Path(p).is_file() and digest(Path(p)) == h
                                                      for p, h in dependencies.items())
        shutil.copyfile(work / "Cargo.lock", output / "Cargo.lock")
        shutil.copyfile(work / "Cargo.toml", output / "snapshot.Cargo.toml")
    finally:
        counts = Counter(e["outcome"] for e in entries)
        for outcome in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(outcome, 0)
        denominator = sum(counts[k] for k in ("killed", "survived", "inconclusive", "unrun"))
        receipt["accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        receipt["sources_unchanged"] = sources == inventory()
        write(output / "mutations.json", entries)
        receipt["mutations_sha256"] = digest(output / "mutations.json")
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(output / "receipt.json", receipt)
        print(receipt["accounting"], flush=True)


if __name__ == "__main__":
    main()
