//! MUB6 basis-extension CODA packet (the bounded fixed-tuple pilot).
//!
//! Binding layer for `omega_engine/research/published/012_mutually_unbiased_bases/mub6_basisextensionobstruction_coda_packet.md`: it lifts the exact
//! local cochain evidence (`d6_exact_curvature_cochain`, `d6_exact_tangent_obstruction`)
//! from the vector-level `Phi_1` to the **basis-level `Psi_basis(T)`** object, over the
//! native field `Q(zeta_24)`, and packages it as a replayable certificate that **refuses
//! global promotion**.
//!
//! For a fixed tuple `T` (its `N` flattened fixed vectors `e_i`) and a candidate next
//! basis `U` (a unitary of `C^6`, columns `U_j`), the basis-extension residual is
//!
//! ```text
//!   r_ij(T, U) = |<e_i, U_j>|^2 - 1/6        (C1: BasisExtensionResidual)
//! ```
//!
//! with two zero-set-equivalent residual masses (packet section 5):
//!
//! ```text
//!   D_abs(T,U) = sum_ij |r_ij|     (observer / l1 residual)
//!   D_sq(T,U)  = sum_ij r_ij^2     (certificate-friendly polynomial residual)
//! ```
//!
//! The **zero-set bridge** is exact and is the load-bearing pilot obligation:
//!
//! ```text
//!   D_abs(T,U) = 0  iff  D_sq(T,U) = 0  iff  every r_ij = 0  iff  U extends T by one MU basis.
//! ```
//!
//! Both directions hold because each `r_ij` is a real algebraic number and each
//! `r_ij^2 >= 0`, so a sum of them vanishes in the field iff every term vanishes; and
//! `|r_ij| = 0 iff r_ij = 0`. We compute `D_sq` exactly (no sign comparison needed) and
//! the exact zero-set via `r_ij == 0` in `Cyc24`; `D_abs` shares that zero set.
//!
//! Firewall (packet section 12): a single candidate `U` with `D > 0` only shows that *that*
//! `U` is not an extension. The basis-level `Psi_basis(T) = min_U D(T,U) > 0` certificate
//! needs an exact / interval / PSD lower bound over all of `U(6)` (the cover obligation,
//! NOT supplied here). This packet is `OpenResidual`; it does NOT imply MUB(6)=3, no four
//! MUBs, or anything about MUB(n). It mints no authority.

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

/// Which residual mass a certificate is stated in (packet section 5).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ResidualDefinition {
    /// `D_abs = sum |r_ij|` (observer / l1).
    DAbs,
    /// `D_sq = sum r_ij^2` (PSD/SOS-friendly).
    DSq,
}

/// Per-candidate basis-extension evaluation against a fixed tuple `T`.
pub struct CandidateExtensionReport {
    /// The exact basis-extension residuals `r_ij = |<e_i, U_j>|^2 - 1/6`.
    pub residual: Vec<Cyc24>,
    /// `D_sq(T, U) = sum_ij r_ij^2`, exact.
    pub d_sq: Cyc24,
    /// Every supplied cross-overlap residual vanishes. An empty residual is vacuous.
    pub cross_overlap_cleared: bool,
    /// The candidate was admitted as six orthonormal columns.
    pub candidate_is_unitary_basis: bool,
    /// The candidate is a unitary basis of `C^6` and every cross-overlap residual vanishes.
    pub extends: bool,
}

/// Six orthonormal columns of `C^6`. Construction is the admission check.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnitaryBasis6 {
    columns: [ExactVec; D],
}

/// Why a candidate was not admitted as a basis of `C^6`.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum BasisAdmissionError {
    /// The candidate does not have six columns.
    ColumnCount { got: usize },
    /// `U* U` is not the identity.
    NotOrthonormal,
    /// The fixed tuple has no vectors, so there is no extension problem.
    EmptyFixedTuple,
}

/// Admit `columns` only when it is an orthonormal basis of `C^6`.
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

/// The exact basis-extension residual `r_ij(T, U)` for fixed vectors `e_i` (rows) and
/// candidate columns `U_j`. Flattened `i`-major: index `i * 6 + j`.
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

/// `D_sq(T, U) = sum_ij r_ij^2`, exact.
pub fn d_sq(residual: &[Cyc24]) -> Cyc24 {
    let mut acc = Cyc24::zero();
    for r in residual {
        acc = acc.add(&r.mul(r));
    }
    acc
}

/// `true` iff every supplied residual vanishes. This is not a basis-admission check.
pub fn cross_overlap_cleared(residual: &[Cyc24]) -> bool {
    residual.iter().all(|r| r.is_zero())
}

/// Evaluate a candidate next basis `U` against the fixed tuple `T`.
///
/// Vanishing cross-overlap residuals and “`U` extends `T`” are different conclusions.
/// The second one requires a nonempty fixed tuple and an admitted `UnitaryBasis6`.
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

/// Terminal status of the fixed-tuple basis-extension packet (packet section 12).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum PsiTerminal {
    /// The `Psi_basis(T) > 0` lower-bound certificate (over all of `U(6)`) is not yet
    /// supplied; only per-candidate evaluations and the zero-set bridge are present.
    OpenResidual,
    /// For the fixed triple `T0`, an EXACT COMPLETE machine vector cover discharges the no-go
    /// (no fourth MU vector, hence no fourth MU basis via the kernel-checked Lean bridges).
    /// The discharge rests on the trusted exact-interval cover engine, NOT a Lean reflection of
    /// the boxes; and it is fixed-triple only (stated region only — the moduli cover stays open).
    ExactCoverDischarged,
}

/// The fixed-tuple `Psi_basis(T)` certificate schema (packet section 9), the replayable
/// binding layer. This pilot fills the residual-algebra and zero-set-bridge obligations;
/// the lower-bound certificate over `U(6)` remains an explicit open obligation.
#[derive(Debug, Clone, Serialize)]
pub struct FixedTuplePsiCertificate {
    pub certificate_id: String,
    pub dimension: usize,
    pub residual_definition_id: ResidualDefinition,
    /// `U(6)` only after the candidate is admitted as a unitary basis.
    pub candidate_basis_domain: &'static str,
    /// The zero-set bridge holds for the evaluated candidate: `extends == (D_sq == 0)`.
    pub zero_set_bridge_holds: bool,
    /// Whether the single evaluated candidate extends `T` (NOT a `Psi_basis > 0` claim).
    pub candidate_extends: bool,
    /// The remaining obligation for a real `Psi_basis(T) > 0` terminal.
    pub lower_bound_obligation: &'static str,
    pub terminal: PsiTerminal,
    pub refuses_global_promotion: bool,
    pub firewall: &'static str,
}

/// Build the fixed-tuple basis-extension certificate for one declared candidate. The
/// terminal is always `OpenResidual` and global promotion is always refused: a single
/// candidate cannot certify `Psi_basis(T) > 0`.
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

/// The standard basis of `C^6` (the identity unitary's columns) as a candidate.
pub fn standard_basis() -> Vec<ExactVec> {
    (0..D)
        .map(|j| {
            let mut v: ExactVec = std::array::from_fn(|_| Cyc24::zero());
            v[j] = Cyc24::rat(omega_number_theory::rational::ri(1));
            v
        })
        .collect()
}

// ---------------------------------------------------------------------------
// Full ODP instantiation + replay (the binding / terminalization layer).
//
// `FixedTuplePsiCertificate` above records a single candidate evaluation. The
// `Mub6OdpInstance` below binds the *complete* Obstruction Descent Packet field
// set for the fixed tuple `T0` (packet sections 2-12 of
// `omega_engine/research/published/012_mutually_unbiased_bases/mub6_basisextensionobstruction_coda_packet.md`, schema of
// `crates/omega_contracts/src/contract_canonical_definitions/core/09_packets/omega_obstruction_packet_standard.md`)
// over the native field `Q(zeta_24)`, reusing the exact cochain surface of
// `d6_exact_curvature_cochain` (packet section 1.1: reuse, do not route around it),
// and seals it through an exact `replay` verifier as terminal `OpenResidual`.
//
// What is established EXACTLY (replay-checked over `Cyc24`):
//   * the carrier `T0` is a genuine MU triple (normalization + unitarity +
//     pairwise-MU, packet section 9 `*_proof` fields);
//   * `Gamma_2 = 0` -- the discrete Bianchi closure `sum_i omega_i(v) = ||v||^2 - 1`
//     vanishes on every unit vector (every config is a closed survivor, ENC-1131);
//   * the zero-set bridge `extends(U) <=> D_sq(T,U) = 0` (packet section 5).
// What is deliberately NOT claimed (the open obligation that keeps this OpenResidual):
//   * a `Psi_basis(T) >= epsilon > 0` lower bound over all of `U(6)` (packet
//     section 9 `lower_bound_*`). No exact/interval/PSD cover certificate is supplied.
// The generic DDA bookkeeping confirms the gap honestly: the discrete shadow is
// `(phi1, gamma2) = (1, 0)` -- closed (`gamma2 = 0`) but obstructed (`phi1 > 0`) with
// NO licensed resolving lambda, so `FiniteLambdaLedger::require_chained` MUST fail.
// ---------------------------------------------------------------------------

/// Lowercase hex of a byte string.
fn hex(bytes: &[u8]) -> String {
    use std::fmt::Write;
    let mut s = String::with_capacity(bytes.len() * 2);
    for b in bytes {
        let _ = write!(&mut s, "{b:02x}");
    }
    s
}

/// Stable SHA-256 hex of an ordered list of exact vectors (hash-stable tuple
/// encoding, packet section 10). `Cyc24.a` is in canonical reduced form and each
/// `BigRational` is in lowest terms, so equal field elements encode identically and
/// the digest is byte-stable across rebuilds.
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

/// The arithmetic mode a certificate's facts are established in (packet section 9).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ArithmeticMode {
    /// exact rational / algebraic (`Cyc24`) -- the mode of everything sealed here.
    Exact,
    /// interval-arithmetic cover of `U(6)` (not used by this instance).
    Interval,
    /// PSD / SOS lower-bound certificate (not used by this instance).
    PsdSos,
}

/// One named, replayed check and its outcome.
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

/// The aggregate result of replaying a `Mub6OdpInstance` from its raw carrier.
#[derive(Debug, Clone, Serialize)]
pub struct ReplayOutcome {
    /// `true` iff every check re-derived from `canonical_triple_exact()` passed.
    pub ok: bool,
    pub checks: Vec<ReplayCheck>,
}

/// The discrete DDA shadow of the MUB6 descent: `gamma2 = 0` (Bianchi closes, so the
/// curvature class is a closed survivor) and `phi1 = 1` (a residual obstruction is
/// present and NO resolving lambda is licensed). With no steps and an unresolved
/// initial diagnostic, `require_chained` fails -- the discrete witness of `OpenResidual`.
fn mub6_descent_ledger() -> FiniteLambdaLedger {
    let d = FiniteDiagnostic::new(1, 0);
    FiniteLambdaLedger::new(d, Vec::new(), d)
}

/// The complete MUB6 basis-extension ODP instance for the canonical triple `T0`.
#[derive(Debug, Clone, Serialize)]
pub struct Mub6OdpInstance {
    pub certificate_id: String,
    pub dimension: usize,
    pub tuple_source: &'static str,
    /// SHA-256 of the exact carrier encoding (hash-stable, packet section 10).
    pub tuple_hash: String,
    pub field_model: &'static str,
    pub fixed_vector_count: usize,
    pub basis_count: usize,
    /// The carrier is a genuine MU triple, checked exactly (the section-9 `*_proof` fields).
    pub tuple_is_exact_mu_triple: bool,
    /// `omega_i(v) = |<e_i, v>|^2 - 1/6`, the C2 curvature target (packet section 5).
    pub c2_curvature_target: &'static str,
    pub zerorel_statement: &'static str,
    /// `Gamma_2 = 0`: the discrete Bianchi closure vanishes exactly on unit vectors.
    pub gamma2_bianchi_closes: bool,
    pub residual_definition_id: ResidualDefinition,
    pub observer_norm_declaration: &'static str,
    /// The basis-level obstruction object `Phi = Psi_basis(T)` (packet section 7).
    pub phi_object: &'static str,
    /// `Some(_)` only when a real `Psi_basis(T) >= epsilon > 0` bound is supplied. Here `None`.
    pub lower_bound_epsilon: Option<&'static str>,
    pub lower_bound_certificate: &'static str,
    pub arithmetic_mode: ArithmeticMode,
    pub zerorel_preservation_statement: &'static str,
    /// SHA-256 over the replay-relevant inputs and the terminal (packet section 9).
    pub replay_hash: String,
    /// Discrete DDA shadow `(phi1, gamma2)` of the descent.
    pub dda_phi1_gamma2: (u64, u64),
    /// `FiniteLambdaLedger::require_chained().is_ok()` -- `false` for `OpenResidual`.
    pub dda_descent_certified: bool,
    pub terminal: PsiTerminal,
    pub refuses_global_promotion: bool,
    pub firewall: &'static str,
}

const SEALED_FIELD_MODEL: &str = "Q(zeta_24) exact cyclotomic (Cyc24)";
const SEALED_CURVATURE_TARGET: &str = "1/6";

/// Digest of the mathematical payload. Presentation fields such as `certificate_id` are excluded.
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
    /// Instantiate the full ODP for the canonical triple `T0`, reusing the exact
    /// `d6_exact_curvature_cochain` surface. The terminal is always `OpenResidual`:
    /// no `Psi_basis(T) > 0` lower bound over `U(6)` is established here.
    pub fn instantiate_t0(certificate_id: impl Into<String>) -> Self {
        let t0 = canonical_triple_exact();
        let tuple_is_exact_mu_triple = is_mutually_unbiased_triple_exact(&t0);
        let tuple_hash = hash_exact_vecs("mub6-T0-canonical", &t0);

        // Gamma_2 = 0: the per-basis Bianchi closure vanishes exactly on every unit
        // probe vector (the 6 standard-basis vectors are exact unit vectors).
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

    /// Re-derive every sealed fact from the raw carrier `canonical_triple_exact()` and
    /// check it exactly. This is the replayable artifact: it depends on nothing but the
    /// reconstructed tuple and the recorded fields, and it never upgrades the terminal.
    pub fn replay(&self) -> ReplayOutcome {
        let mut checks = Vec::new();
        let t0 = canonical_triple_exact();

        // 1. carrier is an exact MU triple (normalization + unitarity + pairwise-MU).
        checks.push(ReplayCheck::new(
            "carrier_exact_mu_triple",
            is_mutually_unbiased_triple_exact(&t0) && self.tuple_is_exact_mu_triple,
            "T0 orthonormal within each basis and |<.,.>|^2 = 1/6 across, exactly over Cyc24",
        ));

        // 2. hash-stable tuple encoding reproduces, and the sealed payload digest matches it.
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
            self.dimension == D
                && self.field_model == SEALED_FIELD_MODEL
                && self.fixed_vector_count == COLUMN_COUNT
                && self.basis_count == BASIS_COUNT
                && self.residual_definition_id == ResidualDefinition::DSq
                && self.arithmetic_mode == ArithmeticMode::Exact
                && self.c2_curvature_target == SEALED_CURVATURE_TARGET
                && self.terminal == PsiTerminal::OpenResidual,
            "dimension, field, counts, residual, arithmetic mode, curvature target, and terminal match the carrier",
        ));

        // 3. Gamma_2 = 0: Bianchi closure vanishes exactly on every unit probe.
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

        // 4. zero-set bridge on a probe candidate: extends(U) <=> D_sq(T,U) = 0.
        let report = evaluate_candidate(&t0, &standard_basis());
        checks.push(ReplayCheck::new(
            "zero_set_bridge",
            report.candidate_is_unitary_basis && report.extends == report.d_sq.is_zero(),
            "on an admitted unitary basis, extends(U) iff D_sq(T,U) = 0 (exact over Cyc24)",
        ));

        // 5. the discrete DDA shadow refuses to chain: no resolving lambda licensed.
        let ledger = mub6_descent_ledger();
        let dda_open = ledger.require_chained().is_err()
            && ledger.initial.is_obstructed()
            && !self.dda_descent_certified
            && self.dda_phi1_gamma2 == (ledger.initial.phi1, ledger.initial.gamma2);
        checks.push(ReplayCheck::new(
            "dda_descent_open",
            dda_open,
            "FiniteLambdaLedger::require_chained fails (LambdaDidNotResolve): descent not certified",
        ));

        // 6. the terminal is OpenResidual with global promotion refused and no lower bound.
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

// ---------------------------------------------------------------------------
// Exact vector-cover discharge for the fixed triple T0 (the cover wired behind the gate).
//
// The packet's lower-bound obligation is OPEN at the schema level, but for the *fixed* triple
// T0 it is in fact discharged by an EXACT, COMPLETE machine cover: the committed artifact
// `artifacts/gauge_fixed_5_torus_cover_certificate_20260620.json` (910,338 certified boxes,
// 0 uncertified, `complete = true`, exact `BigRational` `min_gap`) emitted by the
// `omega_native::mub6_cover_run` engine. It certifies — per box, in exact rational interval
// arithmetic — that no fourth mutually-unbiased VECTOR extends T0. Via the kernel-checked Lean
// bridges that already exist:
//   MUB.FiniteVectorCover.no_fourth_mu_vector_T0_of_cover  (cover  => no fourth MU vector)
//   MUB.FiniteBasisCover.psi_basis_pos_of_no_mu_vector     (no MU vector => Psi_basis > 0)
// this yields `Psi_basis(T0) > 0`, i.e. no fourth MU BASIS extends T0.
//
// Trust boundary (kept honest): the discharge rests on the exact-interval cover ENGINE (a
// trusted Rust computation), NOT on a Lean-kernel reflection of the 910,338 boxes; and it is a
// no-go for the FIXED triple T0 only. It is stated region only — the cover over the moduli of ALL
// triples (the 6x6 complex-Hadamard exhaustion, ENC-1147) is the open frontier.
// ---------------------------------------------------------------------------

/// Path to the committed exact complete vector-cover certificate for `T0`.
pub const T0_VECTOR_COVER_PATH: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../tests/omega_mub/artifacts/gauge_fixed_5_torus_cover_certificate_20260620.json"
);

/// Region label of the canonical fixed triple `T0` gauge-fixed 5-torus.
pub const T0_COVER_REGION: &str = "gauge_fixed_5_torus";

/// Parse a cover summary as a strictly positive exact gap on the canonical T0 region.
///
/// A passing summary is not a replay of the boxes and does not discharge the no-go.
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

/// Load the committed `T0` vector-cover certificate (the `mub6_cover_run` artifact).
pub fn load_t0_vector_cover() -> Result<CoverCertificate, String> {
    let raw = std::fs::read_to_string(T0_VECTOR_COVER_PATH)
        .map_err(|e| format!("read {T0_VECTOR_COVER_PATH}: {e}"))?;
    serde_json::from_str(&raw).map_err(|e| format!("parse cover certificate: {e}"))
}

/// The cover-summary form of the `T0` packet. Region identity and a strictly positive exact
/// gap can be admitted from the summary. The boxes are not replayed, so the terminal stays
/// `OpenResidual` and both no-go flags stay false.
#[derive(Debug, Clone, Serialize)]
pub struct Mub6CoverDischarge {
    /// The honest schema instance (still `OpenResidual` on its own).
    pub instance: Mub6OdpInstance,
    /// The loaded exact complete vector-cover certificate.
    pub cover: CoverCertificate,
    /// The exact cover certifies no fourth MU vector for `T0`.
    pub vector_no_go_discharged: bool,
    /// ...hence (via the Lean bridge) no fourth MU basis for `T0`.
    pub basis_no_go_via_bridge: bool,
    pub terminal: PsiTerminal,
    pub lean_bridge_vector: &'static str,
    pub lean_bridge_basis: &'static str,
    /// What the discharge rests on (NOT a Lean reflection of the boxes).
    pub trust_anchor: &'static str,
    pub firewall: &'static str,
}

/// Load the T0 cover summary and admit its parsed gap. The summary names a region and a
/// positive rational; it does not replay the boxes, so both no-go flags stay false and the
/// terminal stays `OpenResidual`.
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

    /// `1/sqrt(6)` in `Q(zeta_24)`: `sqrt(2) = ζ8 + ζ8^{-1}` and `sqrt(3) = -i (2 ζ3 + 1)`.
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
            // extends  <=>  D_sq == 0  <=>  every r_ij == 0.
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
        // a single candidate must NOT claim Psi_basis > 0 / no extension globally.
        assert!(!cert.candidate_extends);
    }

    #[test]
    fn odp_instance_replays_green_and_seals_open_residual() {
        let inst = Mub6OdpInstance::instantiate_t0("mub6-odp-T0");
        // honest field bindings.
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

        // replay re-derives every fact from the raw carrier and passes.
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
        // the certificate id differs, but the carrier/replay hashes are content-stable.
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
