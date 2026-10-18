
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

use crate::cech::compute_cech_h1_obstruction;
use crate::empirical_presheaf::{
    summarize_descent, DescentSummary, EmpiricalError, EmpiricalModel, L1DefectReceipt,
    ObserverDraft, ObserverTuple, Scenario, SignallingWitness, Q, AUTHORITY_EFFECT,
    DEFAULT_PIVOT_BUDGET, MAX_GLOBAL_ASSIGNMENTS,
};
use crate::open_set::OpenSet;

pub fn rational_string(value: &Q) -> String {
    let value = value.reduced();
    if value.denom().is_one_value() {
        value.numer().to_string()
    } else {
        format!("{}/{}", value.numer(), value.denom())
    }
}

trait IsOneValue {
    fn is_one_value(&self) -> bool;
}
impl IsOneValue for num_bigint::BigInt {
    fn is_one_value(&self) -> bool {
        *self == num_bigint::BigInt::from(1)
    }
}

pub fn parse_rational(text: &str) -> Option<Q> {
    let (n, d) = match text.split_once('/') {
        Some((n, d)) => (n, d),
        None => (text, "1"),
    };
    let n: num_bigint::BigInt = n.trim().parse().ok()?;
    let d: num_bigint::BigInt = d.trim().parse().ok()?;
    if d.is_zero() {
        return None;
    }
    Some(Q::new(n, d))
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TableRow {
    pub context: usize,
    pub outcome: Vec<usize>,
    pub p: Q,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EpistemicError {
    Empirical(EmpiricalError),
    Signalling(SignallingWitness),
    RowShape { context: usize },
    DuplicateRow { context: usize, outcome: Vec<usize> },
    Cech(String),
    WitnessRejected(String),
}

impl fmt::Display for EpistemicError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "epistemic kernel refusal: {self:?}")
    }
}
impl std::error::Error for EpistemicError {}
impl From<EmpiricalError> for EpistemicError {
    fn from(e: EmpiricalError) -> Self {
        EpistemicError::Empirical(e)
    }
}

pub fn model_from_rows(
    arities: Vec<usize>,
    contexts: Vec<Vec<usize>>,
    rows: &[TableRow],
) -> Result<EmpiricalModel, EpistemicError> {
    let scenario = Scenario::new(arities, contexts)?;
    let mut distributions: Vec<Vec<Q>> = scenario
        .contexts()
        .iter()
        .map(|c| Ok(vec![Q::zero(); scenario.section_count(c)?]))
        .collect::<Result<_, EmpiricalError>>()?;
    let mut seen: Vec<Vec<bool>> = distributions.iter().map(|d| vec![false; d.len()]).collect();
    for row in rows {
        let context = scenario
            .contexts()
            .get(row.context)
            .ok_or(EmpiricalError::Context { index: row.context })?;
        if row.outcome.len() != context.len()
            || row.outcome.iter().zip(context).any(|(&o, &m)| o >= scenario.arities()[m])
        {
            return Err(EpistemicError::RowShape { context: row.context });
        }
        let k = scenario.index_of(context, &row.outcome);
        if seen[row.context][k] {
            return Err(EpistemicError::DuplicateRow { context: row.context, outcome: row.outcome.clone() });
        }
        seen[row.context][k] = true;
        distributions[row.context][k] = row.p.clone();
    }
    Ok(EmpiricalModel::new(scenario, distributions)?)
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ParityCut {
    pub contexts: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ParityStatus {
    NotParityModel { context: usize },
    Consistent { solution: Vec<usize> },
    Cut(ParityCut),
}

fn parity_of_support(model: &EmpiricalModel, c: usize) -> Result<Option<u8>, EmpiricalError> {
    let scenario = model.scenario();
    let context = &scenario.contexts()[c];
    if context.iter().any(|&m| scenario.arities()[m] != 2) {
        return Ok(None);
    }
    let support = model.support(c)?;
    if support.len() != 1usize << (context.len() - 1) {
        return Ok(None);
    }
    let mut parity = None;
    for k in support {
        let assignment = scenario.assignment_of(context, k);
        let p = (assignment.iter().sum::<usize>() % 2) as u8;
        match parity {
            None => parity = Some(p),
            Some(q) if q != p => return Ok(None),
            _ => {}
        }
    }
    Ok(parity)
}

fn bits(mask: u64) -> Vec<usize> {
    (0..64).filter(|&i| mask & (1u64 << i) != 0).collect()
}

fn context_symdiff(left: &BTreeSet<usize>, right: &BTreeSet<usize>) -> BTreeSet<usize> {
    left.symmetric_difference(right).copied().collect()
}

pub fn parity_analysis(model: &EmpiricalModel) -> Result<ParityStatus, EpistemicError> {
    let scenario = model.scenario();
    let n = scenario.measurement_count();
    let mut rows: Vec<(u64, u8, BTreeSet<usize>)> = Vec::new();
    for c in 0..scenario.contexts().len() {
        match parity_of_support(model, c)? {
            Some(p) => rows.push((scenario.context_mask(c), p, BTreeSet::from([c]))),
            None => return Ok(ParityStatus::NotParityModel { context: c }),
        }
    }
    let mut pivots: Vec<(u64, u8, BTreeSet<usize>)> = Vec::new();
    for mut row in rows {
        for (pv, prhs, pset) in &pivots {
            let pivot_bit = pv & pv.wrapping_neg();
            if row.0 & pivot_bit != 0 {
                row = (row.0 ^ pv, row.1 ^ prhs, context_symdiff(&row.2, pset));
            }
        }
        if row.0 == 0 {
            if row.1 == 1 {
                return Ok(ParityStatus::Cut(ParityCut {
                    contexts: row.2.into_iter().collect(),
                }));
            }
            continue;
        }
        let new_bit = row.0 & row.0.wrapping_neg();
        for p in pivots.iter_mut() {
            if p.0 & new_bit != 0 {
                p.0 ^= row.0;
                p.1 ^= row.1;
                p.2 = context_symdiff(&p.2, &row.2);
            }
        }
        pivots.push(row);
    }
    let mut solution = vec![0usize; n];
    for (vars, rhs, _) in pivots.iter().rev() {
        let pivot = vars.trailing_zeros() as usize;
        let rest: usize = bits(*vars).into_iter().filter(|&q| q != pivot).map(|q| solution[q]).sum::<usize>() % 2;
        solution[pivot] = (*rhs as usize + rest) % 2;
    }
    Ok(ParityStatus::Consistent { solution })
}


pub fn nerve_h1_dimension(model: &EmpiricalModel) -> Result<usize, EpistemicError> {
    let cover: Vec<OpenSet> = model
        .scenario()
        .contexts()
        .iter()
        .map(|c| OpenSet::new(c.iter().map(|m| format!("m{m}"))))
        .collect();
    let result = compute_cech_h1_obstruction(&cover, BTreeMap::new()).map_err(EpistemicError::Cech)?;
    Ok(result.dim_h1)
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LocalSection {
    pub context: usize,
    pub outcome: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GlobalSection {
    pub joint: Vec<Q>,
    pub nerve_h1_dim: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContextualObstruction {
    Strong {
        descent: DescentSummary,
        cocycle_class: Option<ParityCut>,
        nerve_h1_dim: usize,
        lp_dual_witness: L1DefectReceipt,
    },
    Logical {
        unextendable: LocalSection,
        nerve_h1_dim: usize,
        lp_dual_witness: L1DefectReceipt,
    },
    Probabilistic { lp_dual_witness: L1DefectReceipt, nerve_h1_dim: usize },
}

impl ContextualObstruction {
    pub fn lp_dual_witness(&self) -> &L1DefectReceipt {
        match self {
            ContextualObstruction::Strong { lp_dual_witness, .. }
            | ContextualObstruction::Logical { lp_dual_witness, .. }
            | ContextualObstruction::Probabilistic { lp_dual_witness, .. } => lp_dual_witness,
        }
    }
    pub fn nerve_h1_dim(&self) -> usize {
        match self {
            ContextualObstruction::Strong { nerve_h1_dim, .. }
            | ContextualObstruction::Logical { nerve_h1_dim, .. }
            | ContextualObstruction::Probabilistic { nerve_h1_dim, .. } => *nerve_h1_dim,
        }
    }
    pub fn kind(&self) -> &'static str {
        match self {
            ContextualObstruction::Strong { .. } => "Strong",
            ContextualObstruction::Logical { .. } => "Logical",
            ContextualObstruction::Probabilistic { .. } => "Probabilistic",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContextualityVerdict {
    GlobalSection(GlobalSection),
    Obstructed(ContextualObstruction),
}

impl ContextualityVerdict {
    pub fn into_result(self) -> Result<GlobalSection, ContextualObstruction> {
        match self {
            ContextualityVerdict::GlobalSection(g) => Ok(g),
            ContextualityVerdict::Obstructed(o) => Err(o),
        }
    }
    pub fn kind(&self) -> &'static str {
        match self {
            ContextualityVerdict::GlobalSection(_) => "GlobalSection",
            ContextualityVerdict::Obstructed(o) => o.kind(),
        }
    }
    pub fn nerve_h1_dim(&self) -> usize {
        match self {
            ContextualityVerdict::GlobalSection(g) => g.nerve_h1_dim,
            ContextualityVerdict::Obstructed(o) => o.nerve_h1_dim(),
        }
    }

    pub fn to_json(&self) -> serde_json::Value {
        use serde_json::{json, Value};
        let qs = |v: &[Q]| Value::Array(v.iter().map(|x| Value::String(rational_string(x))).collect());
        match self {
            ContextualityVerdict::GlobalSection(g) => json!({
                "verdict": "GlobalSection", "joint": qs(&g.joint), "nerve_h1_dim": g.nerve_h1_dim,
            }),
            ContextualityVerdict::Obstructed(o) => {
                let w = o.lp_dual_witness();
                let mut v = json!({
                    "verdict": o.kind(),
                    "nerve_h1_dim": o.nerve_h1_dim(),
                    "lp_dual_witness": {
                        "defect": rational_string(&w.defect),
                        "dual_witness": qs(&w.dual_witness),
                        "dual_offset": rational_string(&w.dual_offset),
                    },
                });
                match o {
                    ContextualObstruction::Strong { descent, cocycle_class, .. } => {
                        v["descent"] = json!({
                            "matching_families": descent.matching_families,
                            "no_global_extension": descent.no_global_extension,
                        });
                        v["cocycle_class"] = serde_json::to_value(cocycle_class).expect("serialises");
                    }
                    ContextualObstruction::Logical { unextendable, .. } => {
                        v["unextendable"] = serde_json::to_value(unextendable).expect("serialises");
                    }
                    ContextualObstruction::Probabilistic { .. } => {}
                }
                v
            }
        }
    }
}

pub fn verify_joint(model: &EmpiricalModel, joint: &[Q]) -> Result<(), EpistemicError> {
    let scenario = model.scenario();
    let all = scenario.all_positions();
    let total = scenario.section_count(&all)?;
    if joint.len() != total {
        return Err(EpistemicError::WitnessRejected("joint has the wrong length".into()));
    }
    if joint.iter().any(|p| *p < Q::zero()) {
        return Err(EpistemicError::WitnessRejected("joint has a negative entry".into()));
    }
    if joint.iter().sum::<Q>() != Q::from_integer(1.into()) {
        return Err(EpistemicError::WitnessRejected("joint is not normalised".into()));
    }
    for (c, context) in scenario.contexts().iter().enumerate() {
        let mut marginal = vec![Q::zero(); scenario.section_count(context)?];
        for (g, p) in joint.iter().enumerate() {
            let assignment = scenario.assignment_of(&all, g);
            let local = Scenario::restrict(&all, &assignment, context)
                .ok_or_else(|| EpistemicError::WitnessRejected("restriction failed".into()))?;
            marginal[scenario.index_of(context, &local)] += p;
        }
        if marginal != model.distributions()[c] {
            return Err(EpistemicError::WitnessRejected(format!("joint does not marginalise to context {c}")));
        }
    }
    Ok(())
}

pub fn evaluate_epistemic_contextuality(
    model: &EmpiricalModel,
    pivots: usize,
) -> Result<ContextualityVerdict, EpistemicError> {
    if let Some(witness) = model.signalling_witness()? {
        return Err(EpistemicError::Signalling(witness));
    }
    let nerve_h1_dim = nerve_h1_dimension(model)?;
    let receipt = model.l1_defect(pivots)?;
    if !model.verify_l1_defect(&receipt) {
        return Err(EpistemicError::WitnessRejected("L1 defect receipt failed replay".into()));
    }
    let globals = model.global_support()?;
    if globals.is_empty() {
        if receipt.defect.is_zero() {
            return Err(EpistemicError::WitnessRejected(
                "zero defect with empty global support is contradictory".into(),
            ));
        }
        let scenario = model.scenario();
        let cover: Vec<u64> = (0..scenario.contexts().len()).map(|c| scenario.context_mask(c)).collect();
        let classification =
            model.admissible_presheaf(&[])?.classify_cover(scenario.full_mask(), &cover, MAX_GLOBAL_ASSIGNMENTS)?;
        let descent = summarize_descent(&classification);
        if descent.unique + descent.ambiguous != 0 {
            return Err(EpistemicError::WitnessRejected(
                "descent found a global extension the support enumeration did not".into(),
            ));
        }
        let cocycle_class = match parity_analysis(model)? {
            ParityStatus::Cut(cut) => Some(cut),
            _ => None,
        };
        return Ok(ContextualityVerdict::Obstructed(ContextualObstruction::Strong {
            descent,
            cocycle_class,
            nerve_h1_dim,
            lp_dual_witness: receipt,
        }));
    }
    if let Some((context, k)) = model.logical_contextuality_witness()? {
        if receipt.defect.is_zero() {
            return Err(EpistemicError::WitnessRejected(
                "zero defect with an unextendable supported section is contradictory".into(),
            ));
        }
        let outcome = model.scenario().assignment_of(&model.scenario().contexts()[context], k);
        return Ok(ContextualityVerdict::Obstructed(ContextualObstruction::Logical {
            unextendable: LocalSection { context, outcome },
            nerve_h1_dim,
            lp_dual_witness: receipt,
        }));
    }
    if !receipt.defect.is_zero() {
        return Ok(ContextualityVerdict::Obstructed(ContextualObstruction::Probabilistic {
            lp_dual_witness: receipt,
            nerve_h1_dim,
        }));
    }
    let joint = receipt.coefficients.clone();
    verify_joint(model, &joint)?;
    Ok(ContextualityVerdict::GlobalSection(GlobalSection { joint, nerve_h1_dim }))
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundaryProjection {
    pub state_dim: usize,
    pub boundary_dim: usize,
}

impl BoundaryProjection {
    pub fn private_fiber_dim(&self) -> usize {
        self.state_dim - self.boundary_dim
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Terminal {
    Admitted,
    Refused { kind: String },
    LiftRequired { reason: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LedgerEntry {
    pub index: usize,
    pub command: String,
    pub terminal: Terminal,
    pub payload_json: String,
    pub previous_digest: String,
    pub digest: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ObserverError {
    BoundaryLargerThanState { state_dim: usize, boundary_dim: usize },
    TrivialPrivateFiber,
    EmptyCarrier,
    Undeclared(EmpiricalError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EpistemicObserver {
    pub name: String,
    pub tuple: ObserverTuple,
    pub carrier_arities: Vec<usize>,
    pub boundary: BoundaryProjection,
    pub ledger: Vec<LedgerEntry>,
}

impl EpistemicObserver {
    pub fn new(
        name: impl Into<String>,
        draft: ObserverDraft,
        carrier_arities: Vec<usize>,
        boundary: BoundaryProjection,
    ) -> Result<Self, ObserverError> {
        if boundary.boundary_dim > boundary.state_dim {
            return Err(ObserverError::BoundaryLargerThanState {
                state_dim: boundary.state_dim,
                boundary_dim: boundary.boundary_dim,
            });
        }
        if boundary.private_fiber_dim() == 0 {
            return Err(ObserverError::TrivialPrivateFiber);
        }
        if carrier_arities.is_empty() || carrier_arities.iter().any(|&k| k < 2) {
            return Err(ObserverError::EmptyCarrier);
        }
        let tuple = draft.declare().map_err(ObserverError::Undeclared)?;
        Ok(Self { name: name.into(), tuple, carrier_arities, boundary, ledger: Vec::new() })
    }

    pub fn authority_effect(&self) -> &'static str {
        AUTHORITY_EFFECT
    }

    pub fn private_fiber_dim(&self) -> usize {
        self.boundary.private_fiber_dim()
    }

    pub fn carries(&self, model: &EmpiricalModel) -> bool {
        let arities = model.scenario().arities();
        arities.len() <= self.carrier_arities.len()
            && arities.iter().zip(&self.carrier_arities).all(|(a, b)| a == b)
    }

    pub fn terminalize(&self, evaluation: &Result<ContextualityVerdict, EpistemicError>) -> Terminal {
        match evaluation {
            Ok(ContextualityVerdict::GlobalSection(_)) => Terminal::Admitted,
            Ok(ContextualityVerdict::Obstructed(o)) => Terminal::Refused { kind: o.kind().to_string() },
            Err(e) => Terminal::LiftRequired { reason: e.to_string() },
        }
    }

    pub fn evaluate_and_record(
        &mut self,
        command: impl Into<String>,
        model: &EmpiricalModel,
    ) -> Result<ContextualityVerdict, EpistemicError> {
        let evaluation = if self.carries(model) {
            evaluate_epistemic_contextuality(model, DEFAULT_PIVOT_BUDGET)
        } else {
            Err(EpistemicError::WitnessRejected("model outside the observer's carrier".into()))
        };
        self.record(command, &evaluation);
        evaluation
    }

    pub fn record(
        &mut self,
        command: impl Into<String>,
        evaluation: &Result<ContextualityVerdict, EpistemicError>,
    ) -> &LedgerEntry {
        let terminal = self.terminalize(evaluation);
        let payload_json = match evaluation {
            Ok(v) => v.to_json().to_string(),
            Err(e) => serde_json::json!({ "refusal": e.to_string() }).to_string(),
        };
        let previous_digest = self.ledger.last().map(|e| e.digest.clone()).unwrap_or_else(|| "0".repeat(64));
        let command = command.into();
        let digest = Self::entry_digest(&previous_digest, &command, &terminal, &payload_json);
        self.ledger.push(LedgerEntry {
            index: self.ledger.len(),
            command,
            terminal,
            payload_json,
            previous_digest,
            digest,
        });
        self.ledger.last().expect("just pushed")
    }

    fn entry_digest(previous: &str, command: &str, terminal: &Terminal, payload: &str) -> String {
        let terminal_token = match terminal {
            Terminal::Admitted => "Admitted".to_string(),
            Terminal::Refused { kind } => format!("Refused\n{kind}"),
            Terminal::LiftRequired { reason } => format!("LiftRequired\n{reason}"),
        };
        let mut hasher = Sha256::new();
        for field in [previous, command, &terminal_token, payload] {
            let bytes = field.as_bytes();
            hasher.update((bytes.len() as u64).to_be_bytes());
            hasher.update(bytes);
        }
        format!("{:x}", hasher.finalize())
    }

    pub fn verify_ledger(&self) -> Result<(), usize> {
        let mut previous = "0".repeat(64);
        for entry in &self.ledger {
            if entry.previous_digest != previous
                || Self::entry_digest(
                    &entry.previous_digest,
                    &entry.command,
                    &entry.terminal,
                    &entry.payload_json,
                ) != entry.digest
            {
                return Err(entry.index);
            }
            previous = entry.digest.clone();
        }
        Ok(())
    }

    pub fn complete_against(&self, pinned_tip: &str) -> bool {
        !pinned_tip.is_empty()
            && self.verify_ledger().is_ok()
            && self.ledger.last().map(|e| e.digest.as_str()) == Some(pinned_tip)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::empirical_presheaf::rational;

    fn q(n: i64, d: i64) -> Q {
        rational(n, d).expect("test rationals have nonzero denominators")
    }

    fn bell_rows(same: [Q; 4]) -> Vec<TableRow> {
        let mut rows = Vec::new();
        for (c, s) in same.iter().enumerate() {
            let half = q(1, 2);
            rows.push(TableRow { context: c, outcome: vec![0, 0], p: s * &half });
            rows.push(TableRow { context: c, outcome: vec![1, 1], p: s * &half });
            rows.push(TableRow { context: c, outcome: vec![0, 1], p: (q(1, 1) - s) * &half });
            rows.push(TableRow { context: c, outcome: vec![1, 0], p: (q(1, 1) - s) * &half });
        }
        rows
    }

    fn bell(same: [Q; 4]) -> EmpiricalModel {
        model_from_rows(vec![2; 4], vec![vec![0, 2], vec![0, 3], vec![1, 2], vec![1, 3]], &bell_rows(same)).unwrap()
    }

    fn one() -> Q {
        q(1, 1)
    }

    #[test]
    fn pr_box_is_strong_with_a_parity_cut() {
        let pr = bell([one(), one(), one(), q(0, 1)]);
        match evaluate_epistemic_contextuality(&pr, DEFAULT_PIVOT_BUDGET).unwrap() {
            ContextualityVerdict::Obstructed(ContextualObstruction::Strong { cocycle_class, nerve_h1_dim, descent, lp_dual_witness }) => {
                assert_eq!(cocycle_class, Some(ParityCut { contexts: vec![0, 1, 2, 3] }));
                assert_eq!(nerve_h1_dim, 1);
                assert_eq!(descent.unique + descent.ambiguous, 0);
                assert!(lp_dual_witness.defect > Q::zero());
            }
            other => panic!("{other:?}"),
        }
    }

    #[test]
    fn classical_mixture_has_a_verified_global_section_with_the_same_nerve() {
        let classical = bell([one(), one(), one(), one()]);
        match evaluate_epistemic_contextuality(&classical, DEFAULT_PIVOT_BUDGET).unwrap() {
            ContextualityVerdict::GlobalSection(g) => {
                assert_eq!(g.nerve_h1_dim, 1);
                assert_eq!(g.joint.iter().filter(|p| !p.is_zero()).count(), 2);
            }
            other => panic!("{other:?}"),
        }
    }

    #[test]
    fn near_tsirelson_is_probabilistically_contextual() {
        let m = bell([q(17, 20), q(17, 20), q(17, 20), q(3, 20)]);
        match evaluate_epistemic_contextuality(&m, DEFAULT_PIVOT_BUDGET).unwrap() {
            ContextualityVerdict::Obstructed(ContextualObstruction::Probabilistic { lp_dual_witness, .. }) => {
                assert!(lp_dual_witness.defect > Q::zero());
                assert!(m.verify_l1_defect(&lp_dual_witness));
            }
            other => panic!("{other:?}"),
        }
    }

    #[test]
    fn rational_strings_round_trip() {
        for s in ["0", "1", "-3", "17/20", "-5/7"] {
            assert_eq!(rational_string(&parse_rational(s).unwrap()), s);
        }
        assert_eq!(rational_string(&parse_rational("2/4").unwrap()), "1/2");
        assert!(parse_rational("1/0").is_none());
    }

    #[test]
    fn observer_refuses_a_trivial_private_fiber_and_chains_its_ledger() {
        let draft = || ObserverDraft {
            kernel: Some("support presheaf over the maximal-context cover".into()),
            admissibility: Some("noncontextual polytope".into()),
            norm: Some("L1".into()),
            terminal: Some("GlobalSection -> Admitted; obstruction -> Refused; refusal -> LiftRequired".into()),
            layer: Some("WDP-CH10-D01 diagnostic".into()),
        };
        let err = EpistemicObserver::new("flat", draft(), vec![2; 4], BoundaryProjection { state_dim: 3, boundary_dim: 3 }).unwrap_err();
        assert_eq!(err, ObserverError::TrivialPrivateFiber);
        let mut observer =
            EpistemicObserver::new("o", draft(), vec![2; 4], BoundaryProjection { state_dim: 3, boundary_dim: 2 }).unwrap();
        assert_eq!(observer.private_fiber_dim(), 1);
        let pr = bell([one(), one(), one(), q(0, 1)]);
        let v = observer.evaluate_and_record("evaluate pr", &pr).unwrap();
        assert!(matches!(v, ContextualityVerdict::Obstructed(_)));
        assert!(matches!(observer.ledger[0].terminal, Terminal::Refused { .. }));
        let tip = observer.ledger[0].digest.clone();
        assert!(observer.complete_against(&tip));
        assert!(observer.verify_ledger().is_ok());
        observer.ledger[0].command = "tampered".into();
        assert_eq!(observer.verify_ledger(), Err(0));
        assert!(!observer.complete_against(&tip));
    }
}
