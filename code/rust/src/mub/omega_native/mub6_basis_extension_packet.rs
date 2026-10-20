
use num_rational::BigRational;
use num_traits::Zero;
use serde::Serialize;
use sha2::{Digest, Sha256};

use omega_wdp::ddc::{FiniteDiagnostic, FiniteLambdaLedger};

use crate::omega_native::exact::d6_exact_curvature_cochain::{
    abs_sq, basis_closure, canonical_triple_exact, curvature_c2, inner,
    is_mutually_unbiased_triple_exact, ExactVec, BASIS_COUNT, COLUMN_COUNT, D,
};
use crate::omega_native::exact::mub6_cover_run::CoverCertificate;
use omega_number_theory::cyclotomic::Cyc24;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ResidualDefinition {
    DAbs,
    DSq,
}

pub struct CandidateExtensionReport {
    pub residual: Vec<Cyc24>,
    pub d_sq: Cyc24,
    pub cross_overlap_cleared: bool,
    pub candidate_is_unitary_basis: bool,
    pub extends: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnitaryBasis6 {
    columns: [ExactVec; D],
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum BasisAdmissionError {
    ColumnCount { got: usize },
    NotOrthonormal,
    EmptyFixedTuple,
}

pub fn try_unitary_basis6(columns: &[ExactVec]) -> Result<UnitaryBasis6, BasisAdmissionError> {
    if columns.len() != D {
        return Err(BasisAdmissionError::ColumnCount { got: columns.len() });
    }
    let one = Cyc24::rat(omega_number_theory::rational::ri(1));
    let zero = Cyc24::zero();
    for i in 0..D {
        for j in 0..D {
            let got = inner(&columns[i], &columns[j]);
            let want = if i == j { &one } else { &zero };
            if &got != want {
                return Err(BasisAdmissionError::NotOrthonormal);
            }
        }
    }
    Ok(UnitaryBasis6 {
        columns: std::array::from_fn(|i| columns[i].clone()),
    })
}

pub fn basis_extension_residual(fixed: &[ExactVec], candidate: &[ExactVec]) -> Vec<Cyc24> {
    let target = Cyc24::rat(
        omega_number_theory::rational::ri(1) / omega_number_theory::rational::ri(D as i64),
    );
    let mut out = Vec::with_capacity(fixed.len() * candidate.len());
    for e in fixed {
        for u in candidate {
            out.push(abs_sq(&inner(e, u)).sub(&target));
        }
    }
    out
}

pub fn d_sq(residual: &[Cyc24]) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for r in residual {
        acc = acc.add(&r.mul(r));
    }
    acc
}

pub fn cross_overlap_cleared(residual: &[Cyc24]) -> bool {
    residual.iter().all(|r| r.is_zero())
}

pub fn evaluate_candidate(fixed: &[ExactVec], candidate: &[ExactVec]) -> CandidateExtensionReport {
    let residual = basis_extension_residual(fixed, candidate);
    let squared = d_sq(&residual);
    let cleared = cross_overlap_cleared(&residual);
    let unitary = try_unitary_basis6(candidate).is_ok();
    let extends = !fixed.is_empty() && unitary && residual.len() == fixed.len() * D && cleared;
    CandidateExtensionReport {
        residual,
        d_sq: squared,
        cross_overlap_cleared: cleared,
        candidate_is_unitary_basis: unitary,
        extends,
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum PsiTerminal {
    OpenResidual,
    ExactCoverDischarged,
}

#[derive(Debug, Clone, Serialize)]
pub struct FixedTuplePsiCertificate {
    pub certificate_id: String,
    pub dimension: usize,
    pub residual_definition_id: ResidualDefinition,
    pub candidate_basis_domain: &'static str,
    pub zero_set_bridge_holds: bool,
    pub candidate_extends: bool,
    pub lower_bound_obligation: &'static str,
    pub terminal: PsiTerminal,
    pub refuses_global_promotion: bool,
    pub firewall: &'static str,
}

pub fn fixed_tuple_certificate(
    certificate_id: impl Into<String>,
    fixed: &[ExactVec],
    candidate: &[ExactVec],
) -> FixedTuplePsiCertificate {
    let report = evaluate_candidate(fixed, candidate);
    let zero_set_bridge_holds = report.candidate_is_unitary_basis
        && !fixed.is_empty()
        && report.extends == report.d_sq.is_zero();
    FixedTuplePsiCertificate {
        certificate_id: certificate_id.into(),
        dimension: D,
        residual_definition_id: ResidualDefinition::DSq,
        candidate_basis_domain: if report.candidate_is_unitary_basis {
            "U(6)"
        } else {
            "refused: candidate is not a unitary basis of C^6"
        },
        zero_set_bridge_holds,
        candidate_extends: report.extends,
        lower_bound_obligation:
            "exact/interval/PSD lower bound D(T,U) >= epsilon > 0 over all U in U(6)",
        terminal: PsiTerminal::OpenResidual,
        refuses_global_promotion: true,
        firewall: "diagnostic only; stated region only; not 'no four MUBs'; mints no authority",
    }
}

pub fn standard_basis() -> Vec<ExactVec> {
    (0..D)
        .map(|j| {
            let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
            v[j] = Cyc24::rat(omega_number_theory::rational::ri(1));
            v
        })
        .collect()
}


fn hex(bytes: &[u8]) -> String {
    use std::fmt::Write;
    let mut s = String::with_capacity(bytes.len() * 2);
    for b in bytes {
        let _ = write!(&mut s, "{b:02x}");
    }
    s
}

fn hash_exact_vecs(label: &str, vecs: &[ExactVec]) -> String {
    let mut h = Sha256::new();
    h.update(label.as_bytes());
    h.update(b"|");
    h.update((vecs.len() as u64).to_le_bytes());
    for v in vecs {
        for c in v.iter() {
            for q in c.a.iter() {
                h.update(q.numer().to_string().as_bytes());
                h.update(b"/");
                h.update(q.denom().to_string().as_bytes());
                h.update(b";");
            }
            h.update(b"|");
        }
        h.update(b"\n");
    }
    hex(&h.finalize())
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ArithmeticMode {
    Exact,
    Interval,
    PsdSos,
}

#[derive(Debug, Clone, Serialize)]
pub struct ReplayCheck {
    pub name: String,
    pub passed: bool,
    pub detail: String,
}

impl ReplayCheck {
    fn new(name: &str, passed: bool, detail: &str) -> Self {
        Self {
            name: name.to_string(),
            passed,
            detail: detail.to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct ReplayOutcome {
    pub ok: bool,
    pub checks: Vec<ReplayCheck>,
}

fn mub6_descent_ledger() -> FiniteLambdaLedger {
    let d = FiniteDiagnostic::new(1, 0);
    FiniteLambdaLedger::new(d, Vec::new(), d)
}

#[derive(Debug, Clone, Serialize)]
pub struct Mub6OdpInstance {
    pub certificate_id: String,
    pub dimension: usize,
    pub tuple_source: &'static str,
    pub tuple_hash: String,
    pub field_model: &'static str,
    pub fixed_vector_count: usize,
    pub basis_count: usize,
    pub tuple_is_exact_mu_triple: bool,
    pub c2_curvature_target: &'static str,
    pub zerorel_statement: &'static str,
    pub gamma2_bianchi_closes: bool,
    pub residual_definition_id: ResidualDefinition,
    pub observer_norm_declaration: &'static str,
    pub phi_object: &'static str,
    pub lower_bound_epsilon: Option<&'static str>,
    pub lower_bound_certificate: &'static str,
    pub arithmetic_mode: ArithmeticMode,
    pub zerorel_preservation_statement: &'static str,
    pub replay_hash: String,
    pub dda_phi1_gamma2: (u64, u64),
    pub dda_descent_certified: bool,
    pub terminal: PsiTerminal,
    pub refuses_global_promotion: bool,
    pub firewall: &'static str,
}

const SEALED_FIELD_MODEL: &str = "Q(zeta_24) exact cyclotomic (Cyc24)";
const SEALED_CURVATURE_TARGET: &str = "1/6";

fn sealed_replay_hash(tuple_hash: &str) -> String {
    let mut hr = Sha256::new();
    hr.update(b"mub6-odp-replay-v2|");
    hr.update(D.to_string().as_bytes());
    hr.update(b"|");
    hr.update(SEALED_FIELD_MODEL.as_bytes());
    hr.update(b"|");
    hr.update(COLUMN_COUNT.to_string().as_bytes());
    hr.update(b"|");
    hr.update(BASIS_COUNT.to_string().as_bytes());
    hr.update(b"|DSq|Exact|");
    hr.update(SEALED_CURVATURE_TARGET.as_bytes());
    hr.update(b"|");
    hr.update(tuple_hash.as_bytes());
    hr.update(b"|OpenResidual");
    hex(&hr.finalize())
}

impl Mub6OdpInstance {
    pub fn instantiate_t0(certificate_id: impl Into<String>) -> Self {
        let t0 = canonical_triple_exact();
        let tuple_is_exact_mu_triple = is_mutually_unbiased_triple_exact(&t0);
        let tuple_hash = hash_exact_vecs("mub6-T0-canonical", &t0);

        let gamma2_bianchi_closes = standard_basis().iter().all(|v| {
            basis_closure(&curvature_c2(&t0, v))
                .iter()
                .all(Cyc24::is_zero)
        });

        let ledger = mub6_descent_ledger();
        let dda_descent_certified = ledger.require_chained().is_ok();

        let replay_hash = sealed_replay_hash(&tuple_hash);

        Self {
            certificate_id: certificate_id.into(),
            dimension: D,
            tuple_source: "canonical_triple_T0 (Weyl-Heisenberg, qubit (x) qutrit)",
            tuple_hash,
            field_model: SEALED_FIELD_MODEL,
            fixed_vector_count: COLUMN_COUNT,
            basis_count: BASIS_COUNT,
            tuple_is_exact_mu_triple,
            c2_curvature_target: SEALED_CURVATURE_TARGET,
            zerorel_statement:
                "for all i,j: |<e_i, U_j>|^2 = 1/6 (every basis-extension residual vanishes exactly)",
            gamma2_bianchi_closes,
            residual_definition_id: ResidualDefinition::DSq,
            observer_norm_declaration: "D_abs = sum_ij |r_ij| (l1 observer residual)",
            phi_object:
                "Psi_basis(T) = min_{U in U(6)} D_T(U) (basis-level, attained on compact U(6))",
            lower_bound_epsilon: None,
            lower_bound_certificate:
                "schema OPEN; canonical reduction cover => no fourth MU basis = MUB.FiniteBasisCover.{no_fourth_basis_of_cover, psi_basis_pos_of_no_mu_vector} (Lean). For T0 the exact complete vector cover discharges it: see discharge_t0_with_vector_cover; the moduli (all-triples) cover is the open frontier",
            arithmetic_mode: ArithmeticMode::Exact,
            zerorel_preservation_statement:
                "extends(U) <=> D_sq(T,U)=0 <=> all r_ij=0; preserved under d0 gauge (phase / relabel / representation-preserving rewrites)",
            replay_hash,
            dda_phi1_gamma2: (ledger.initial.phi1, ledger.initial.gamma2),
            dda_descent_certified,
            terminal: PsiTerminal::OpenResidual,
            refuses_global_promotion: true,
            firewall:
                "diagnostic only; stated region only; not 'no four MUBs in C^6'; not about MUB(n); mints no authority",
        }
    }

    fn sealed_semantic_payload_matches(&self) -> bool {
        let counts_ok = self.dimension == D
            && self.field_model == SEALED_FIELD_MODEL
            && self.fixed_vector_count == COLUMN_COUNT
            && self.basis_count == BASIS_COUNT;
        let mode_ok = self.residual_definition_id == ResidualDefinition::DSq
            && self.arithmetic_mode == ArithmeticMode::Exact
            && self.c2_curvature_target == SEALED_CURVATURE_TARGET
            && self.terminal == PsiTerminal::OpenResidual;
        counts_ok && mode_ok
    }

    fn dda_descent_remains_open(&self) -> bool {
        let ledger = mub6_descent_ledger();
        ledger.require_chained().is_err()
            && ledger.initial.is_obstructed()
            && !self.dda_descent_certified
            && self.dda_phi1_gamma2 == (ledger.initial.phi1, ledger.initial.gamma2)
    }

    pub fn replay(&self) -> ReplayOutcome {
        let mut checks = Vec::new();
        let t0 = canonical_triple_exact();

        checks.push(ReplayCheck::new(
            "carrier_exact_mu_triple",
            is_mutually_unbiased_triple_exact(&t0) && self.tuple_is_exact_mu_triple,
            "T0 orthonormal within each basis and |<.,.>|^2 = 1/6 across, exactly over Cyc24",
        ));

        let tuple_hash = hash_exact_vecs("mub6-T0-canonical", &t0);
        let replay_hash = sealed_replay_hash(&tuple_hash);
        checks.push(ReplayCheck::new(
            "tuple_hash_matches",
            tuple_hash == self.tuple_hash,
            "recomputed SHA-256 of the exact tuple encoding equals the recorded tuple_hash",
        ));
        checks.push(ReplayCheck::new(
            "replay_hash_matches",
            replay_hash == self.replay_hash,
            "recomputed digest of the sealed mathematical payload equals replay_hash",
        ));
        checks.push(ReplayCheck::new(
            "sealed_semantic_payload",
            self.sealed_semantic_payload_matches(),
            "dimension, field, counts, residual, arithmetic mode, curvature target, and terminal match the carrier",
        ));

        let gamma2 = standard_basis().iter().all(|v| {
            basis_closure(&curvature_c2(&t0, v))
                .iter()
                .all(Cyc24::is_zero)
        });
        checks.push(ReplayCheck::new(
            "gamma2_bianchi_closes",
            gamma2 && self.gamma2_bianchi_closes,
            "sum_{i in basis} omega_i(v) = ||v||^2 - 1 = 0 on unit vectors (closed survivor, ENC-1131)",
        ));

        let report = evaluate_candidate(&t0, &standard_basis());
        checks.push(ReplayCheck::new(
            "zero_set_bridge",
            report.candidate_is_unitary_basis && report.extends == report.d_sq.is_zero(),
            "on an admitted unitary basis, extends(U) iff D_sq(T,U) = 0 (exact over Cyc24)",
        ));

        checks.push(ReplayCheck::new(
            "dda_descent_open",
            self.dda_descent_remains_open(),
            "FiniteLambdaLedger::require_chained fails (LambdaDidNotResolve): descent not certified",
        ));

        checks.push(ReplayCheck::new(
            "terminal_open_residual",
            self.terminal == PsiTerminal::OpenResidual
                && self.refuses_global_promotion
                && self.lower_bound_epsilon.is_none(),
            "terminal = OpenResidual; no Psi_basis>0 lower bound; refuses global promotion",
        ));

        let ok = checks.iter().all(|c| c.passed);
        ReplayOutcome { ok, checks }
    }
}


pub const T0_VECTOR_COVER_PATH: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/omega_mub/artifacts/gauge_fixed_5_torus_cover_certificate_20260620.json"
);

pub const T0_COVER_REGION: &str = "gauge_fixed_5_torus";

pub fn admit_t0_cover_summary(cover: &CoverCertificate) -> Result<BigRational, String> {
    if cover.region_label != T0_COVER_REGION {
        return Err(format!(
            "cover region '{}' is not the canonical T0 carrier '{T0_COVER_REGION}'",
            cover.region_label
        ));
    }
    if !cover.complete || cover.uncertified != 0 || cover.certified == 0 {
        return Err(format!(
            "cover summary is not a nonempty complete certificate (complete={}, certified={}, uncertified={})",
            cover.complete, cover.certified, cover.uncertified
        ));
    }
    let raw = cover
        .min_gap
        .as_deref()
        .ok_or_else(|| "cover has no exact min_gap tightness witness".to_string())?;
    let gap = raw
        .parse::<BigRational>()
        .map_err(|error| format!("min_gap '{raw}' is not an exact rational: {error}"))?;
    if gap <= BigRational::zero() {
        return Err(format!("min_gap {gap} is not strictly positive"));
    }
    Ok(gap)
}

pub fn load_t0_vector_cover() -> Result<CoverCertificate, String> {
    let raw = std::fs::read_to_string(T0_VECTOR_COVER_PATH)
        .map_err(|e| format!("read {T0_VECTOR_COVER_PATH}: {e}"))?;
    serde_json::from_str(&raw).map_err(|e| format!("parse cover certificate: {e}"))
}

#[derive(Debug, Clone, Serialize)]
pub struct Mub6CoverDischarge {
    pub instance: Mub6OdpInstance,
    pub cover: CoverCertificate,
    pub vector_no_go_discharged: bool,
    pub basis_no_go_via_bridge: bool,
    pub terminal: PsiTerminal,
    pub lean_bridge_vector: &'static str,
    pub lean_bridge_basis: &'static str,
    pub trust_anchor: &'static str,
    pub firewall: &'static str,
}

pub fn discharge_t0_with_vector_cover() -> Result<Mub6CoverDischarge, String> {
    let cover = load_t0_vector_cover()?;
    let _gap = admit_t0_cover_summary(&cover)?;
    Ok(Mub6CoverDischarge {
        instance: Mub6OdpInstance::instantiate_t0("mub6-odp-T0-cover-summary"),
        cover,
        vector_no_go_discharged: false,
        basis_no_go_via_bridge: false,
        terminal: PsiTerminal::OpenResidual,
        lean_bridge_vector: "MUB.FiniteVectorCover.no_fourth_mu_vector_T0_of_cover",
        lean_bridge_basis: "MUB.FiniteBasisCover.psi_basis_pos_of_no_mu_vector",
        trust_anchor:
            "summary record only: region identity and a strictly positive exact min_gap were parsed; the boxes were not replayed, so the Lean bridge hypotheses are not established",
        firewall:
            "fixed triple T0 only; stated region only; the moduli (all-triples) cover is the open frontier (ENC-1147); mints no authority",
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, COLUMN_COUNT};

    fn inv_sqrt6() -> Cyc24 {
        let one = Cyc24::rat(omega_number_theory::rational::ri(1));
        let two = Cyc24::rat(omega_number_theory::rational::ri(2));
        let sqrt3 = two.mul(&Cyc24::zeta24(8)).add(&one).mul(&Cyc24::zeta24(18));
        let sqrt2 = Cyc24::zeta24(3).add(&Cyc24::zeta24(-3));
        sqrt2.mul(&sqrt3).inv()
    }

    #[test]
    fn standard_basis_does_not_extend_the_canonical_triple() {
        let t0 = canonical_triple_exact();
        let report = evaluate_candidate(&t0, &standard_basis());
        assert_eq!(report.residual.len(), COLUMN_COUNT * D);
        assert!(
            !report.extends,
            "the standard basis is basis B1 of T0, not a fourth MU basis"
        );
        assert!(
            !report.d_sq.is_zero(),
            "a non-extending candidate has D_sq > 0 (nonzero)"
        );
    }

    #[test]
    fn zero_set_bridge_holds_extends_iff_d_sq_zero() {
        let t0 = canonical_triple_exact();
        for cand in [standard_basis(), t0.clone()[0..D].to_vec()] {
            let report = evaluate_candidate(&t0, &cand);
            assert!(report.candidate_is_unitary_basis);
            assert_eq!(report.extends, report.d_sq.is_zero());
            assert_eq!(report.extends, report.cross_overlap_cleared);
        }
    }

    #[test]
    fn certificate_refuses_global_promotion() {
        let t0 = canonical_triple_exact();
        let cert = fixed_tuple_certificate("mub6-pilot-T0-std", &t0, &standard_basis());
        assert!(cert.zero_set_bridge_holds);
        assert!(cert.refuses_global_promotion);
        assert_eq!(cert.terminal, PsiTerminal::OpenResidual);
        assert_eq!(cert.dimension, 6);
        assert!(!cert.candidate_extends);
    }

    #[test]
    fn odp_instance_replays_green_and_seals_open_residual() {
        let inst = Mub6OdpInstance::instantiate_t0("mub6-odp-T0");
        assert_eq!(inst.dimension, 6);
        assert_eq!(inst.fixed_vector_count, 18);
        assert!(inst.tuple_is_exact_mu_triple);
        assert!(
            inst.gamma2_bianchi_closes,
            "Bianchi closure must vanish exactly (Gamma2 = 0)"
        );
        assert!(
            inst.lower_bound_epsilon.is_none(),
            "no Psi_basis > 0 lower bound is claimed"
        );
        assert_eq!(inst.terminal, PsiTerminal::OpenResidual);
        assert!(inst.refuses_global_promotion);
        assert!(
            !inst.dda_descent_certified,
            "the discrete DDA descent must NOT be certified (OpenResidual)"
        );
        assert_eq!(
            inst.dda_phi1_gamma2,
            (1, 0),
            "closed survivor (gamma2 = 0), obstructed (phi1 > 0)"
        );

        let outcome = inst.replay();
        let failed: Vec<&str> = outcome
            .checks
            .iter()
            .filter(|c| !c.passed)
            .map(|c| c.name.as_str())
            .collect();
        assert!(outcome.ok, "replay failed checks: {failed:?}");
        assert!(outcome
            .checks
            .iter()
            .any(|c| c.name == "dda_descent_open" && c.passed));
    }

    #[test]
    fn tuple_hash_and_replay_hash_are_content_stable() {
        let a = Mub6OdpInstance::instantiate_t0("a");
        let b = Mub6OdpInstance::instantiate_t0("b");
        assert_eq!(a.tuple_hash, b.tuple_hash);
        assert_eq!(a.replay_hash, b.replay_hash);
        assert_eq!(a.tuple_hash.len(), 64, "SHA-256 hex is 64 chars");
    }

    #[test]
    fn dda_ledger_refuses_to_chain_for_open_residual() {
        let ledger = mub6_descent_ledger();
        assert!(ledger.initial.is_obstructed());
        assert!(
            ledger.require_chained().is_err(),
            "no resolving lambda is licensed; the chain must fail (OpenResidual)"
        );
    }

    #[test]
    fn t0_vector_cover_loads_complete_and_exact() {
        let cover = load_t0_vector_cover().expect("committed cover artifact loads");
        assert!(cover.complete, "the cover is complete");
        assert_eq!(cover.uncertified, 0, "no uncertified residue");
        assert_eq!(cover.certified, 910_338);
        assert!(
            cover.min_gap.is_some(),
            "exact rational tightness witness present"
        );
    }

    #[test]
    fn cover_summary_does_not_discharge_the_no_go() {
        let d = discharge_t0_with_vector_cover().expect("canonical summary parses");
        assert!(!d.vector_no_go_discharged);
        assert!(!d.basis_no_go_via_bridge);
        assert_eq!(d.terminal, PsiTerminal::OpenResidual);
        assert_eq!(d.instance.terminal, PsiTerminal::OpenResidual);
        assert!(d.lean_bridge_basis.contains("FiniteBasisCover"));
        assert!(d.firewall.contains("stated region only"));
        assert!(d.trust_anchor.contains("not replayed"));
    }

    #[test]
    fn empty_or_rank_deficient_candidate_is_not_an_extending_basis() {
        let t0 = canonical_triple_exact();
        let empty = evaluate_candidate(&t0, &[]);
        assert!(empty.residual.is_empty());
        assert!(empty.d_sq.is_zero());
        assert!(empty.cross_overlap_cleared);
        assert!(!empty.candidate_is_unitary_basis);
        assert!(!empty.extends);

        let flat = inv_sqrt6();
        let column: ExactVec = std::array::from_fn(|_| flat.clone());
        let repeated = vec![column; D];
        let rank_one = evaluate_candidate(&standard_basis(), &repeated);
        assert!(
            rank_one.cross_overlap_cleared,
            "every column is unbiased to the standard basis, so every supplied residual vanishes"
        );
        assert!(!rank_one.candidate_is_unitary_basis);
        assert!(!rank_one.extends);
        let cert = fixed_tuple_certificate("rank-one", &standard_basis(), &repeated);
        assert!(!cert.candidate_extends);
        assert_eq!(
            cert.candidate_basis_domain,
            "refused: candidate is not a unitary basis of C^6"
        );
    }

    #[test]
    fn replay_rejects_a_mutated_semantic_field_and_a_mutated_digest() {
        let mut inst = Mub6OdpInstance::instantiate_t0("mub6-odp-T0");
        assert!(inst.replay().ok);
        inst.dimension = 10;
        assert!(!inst.replay().ok);
        inst.dimension = D;
        inst.replay_hash = "corrupted".to_string();
        assert!(!inst.replay().ok);
        inst.replay_hash = sealed_replay_hash(&inst.tuple_hash);
        inst.c2_curvature_target = "1/10";
        assert!(!inst.replay().ok);
        inst.c2_curvature_target = SEALED_CURVATURE_TARGET;
        inst.field_model = "Q";
        assert!(!inst.replay().ok);
    }

    #[test]
    fn cover_summary_rejects_nonpositive_or_unparsed_gaps() {
        let mut cover = load_t0_vector_cover().expect("artifact");
        for raw in ["0", "-1", "not-a-rational"] {
            cover.min_gap = Some(raw.to_string());
            assert!(admit_t0_cover_summary(&cover).is_err(), "{raw}");
        }
        cover.min_gap = Some("1/6".to_string());
        cover.certified = 0;
        assert!(admit_t0_cover_summary(&cover).is_err());
        cover.certified = 1;
        cover.region_label = "other-region".to_string();
        assert!(admit_t0_cover_summary(&cover).is_err());
    }
}
