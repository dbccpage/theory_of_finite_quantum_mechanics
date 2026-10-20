
use serde::{Deserialize, Serialize};

use crate::complexes::ChainComplexGf2;
use crate::gf2_terminalizer::{
    GF2Matrix, GF2ScheduleStatus, Gf2CocycleClassifier, Gf2ScheduleReceipt,
};
use crate::repair_limit::{
    face_syndrome, hamming_weight, repair_capacity_t, syndrome_is_zero, RepairCapacityReceipt,
};
use crate::RECEIPT_TAG;

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; incomplete packets refuse; residual+logical after repair saturation is a declared-packet capacity wall only; not a physical no-go.";


#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PacketWallTerminal {
    Absorbed,
    ResidualInvisible,
    ResidualLogicallyVisible,
    Refused,
    Exact,
    ClosedResidual,
    OpenObstruction,
    IncompleteRefusal,
    CapacityWallHit,
}


#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DefectEvent {
    pub residual: Vec<u8>,
    pub weight: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RepairAction {
    pub proposed_weight: usize,
    pub within_capacity: Option<bool>,
}

#[derive(Debug, Clone)]
pub struct ToyRepairPacket {
    pub complex: Option<ChainComplexGf2>,
    pub defect: Option<DefectEvent>,
    pub declared_distance_d: Option<usize>,
    pub proposed_repair: Option<RepairAction>,
}

impl ToyRepairPacket {
    pub fn complete(complex: ChainComplexGf2, residual: Vec<u8>) -> Self {
        let weight = hamming_weight(&residual);
        Self {
            complex: Some(complex),
            defect: Some(DefectEvent { residual, weight }),
            declared_distance_d: None,
            proposed_repair: None,
        }
    }

    pub fn empty() -> Self {
        Self {
            complex: None,
            defect: None,
            declared_distance_d: None,
            proposed_repair: None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PacketWallReceipt {
    pub certificate_tag: String,
    pub terminal: PacketWallTerminal,
    pub schedule_status: Option<GF2ScheduleStatus>,
    pub face_syndrome_zero: Option<bool>,
    pub complex_name: Option<String>,
    pub residual_weight: Option<usize>,
    pub repair_capacity_t: Option<usize>,
    pub authority_effect: String,
    pub notes: String,
}

fn none_auth() -> String {
    "None".into()
}

fn incomplete_receipt(
    complex_name: Option<String>,
    residual_weight: Option<usize>,
    schedule_status: Option<GF2ScheduleStatus>,
    declared_distance_d: Option<usize>,
    notes: String,
) -> PacketWallReceipt {
    PacketWallReceipt {
        certificate_tag: "omega.majorana-packet-wall-receipt.v1".into(),
        terminal: PacketWallTerminal::IncompleteRefusal,
        schedule_status,
        face_syndrome_zero: None,
        complex_name,
        residual_weight,
        repair_capacity_t: declared_distance_d.map(repair_capacity_t),
        authority_effect: none_auth(),
        notes,
    }
}

fn classify_wall_terminal(
    status: GF2ScheduleStatus,
    weight: usize,
    declared_distance_d: Option<usize>,
    t_opt: Option<usize>,
) -> (PacketWallTerminal, String) {
    let capacity_hit = matches!(
        (t_opt, status),
        (Some(t), GF2ScheduleStatus::ClosedResidual) if weight > t
    );
    let terminal = if capacity_hit {
        PacketWallTerminal::CapacityWallHit
    } else {
        match status {
            GF2ScheduleStatus::Exact => PacketWallTerminal::Exact,
            GF2ScheduleStatus::ClosedResidual => PacketWallTerminal::ClosedResidual,
            GF2ScheduleStatus::OpenObstruction => PacketWallTerminal::OpenObstruction,
        }
    };
    let notes = match terminal {
        PacketWallTerminal::ClosedResidual => {
            "Local green (face syndrome 0) + ClosedResidual = LGGR diagnostic; Auth=None".into()
        }
        PacketWallTerminal::CapacityWallHit => format!(
            "Capacity wall: weight {} > t={} for declared d={:?}; silent logical class possible. Auth=None",
            weight,
            t_opt.unwrap_or(0),
            declared_distance_d
        ),
        PacketWallTerminal::Exact => "Exact coboundary class; Auth=None".into(),
        PacketWallTerminal::OpenObstruction => {
            "Open obstruction (detectable syndrome); Auth=None".into()
        }
        PacketWallTerminal::IncompleteRefusal => "refused".into(),
        _ => "diagnostic terminal; Auth=None".into(),
    };
    (terminal, notes)
}

pub fn terminalize_packet(packet: &ToyRepairPacket) -> PacketWallReceipt {
    let Some(complex) = &packet.complex else {
        return incomplete_receipt(
            None,
            None,
            None,
            packet.declared_distance_d,
            "IncompletePacket: missing complex".into(),
        );
    };
    let Some(defect) = &packet.defect else {
        return incomplete_receipt(
            Some(complex.name.into()),
            None,
            None,
            packet.declared_distance_d,
            "IncompletePacket: missing defect".into(),
        );
    };
    if !complex.verify_boundary() {
        return incomplete_receipt(
            Some(complex.name.into()),
            Some(defect.weight),
            None,
            packet.declared_distance_d,
            "IncompletePacket: boundary invalid (d1 d0 != 0); refused".into(),
        );
    }
    let cert = match Gf2CocycleClassifier::classify(&complex.d0, &complex.d1, &defect.residual) {
        Ok(c) => c,
        Err(e) => {
            return incomplete_receipt(
                Some(complex.name.into()),
                Some(defect.weight),
                None,
                packet.declared_distance_d,
                format!("IncompletePacket: terminalize refused: {e}"),
            );
        }
    };
    if cert.authority_effect != "None" {
        return incomplete_receipt(
            Some(complex.name.into()),
            Some(defect.weight),
            Some(cert.status),
            packet.declared_distance_d,
            format!(
                "authority wall: underlying receipt claimed {:?}; suppressed to None + refuse",
                cert.authority_effect
            ),
        );
    }

    let syn = face_syndrome(&complex.d1, &defect.residual).ok();
    let syn_zero = syn.as_ref().map(|s| syndrome_is_zero(s));
    let t_opt = packet.declared_distance_d.map(repair_capacity_t);
    let (terminal, notes) =
        classify_wall_terminal(cert.status, defect.weight, packet.declared_distance_d, t_opt);
    let _ = RECEIPT_TAG;

    PacketWallReceipt {
        certificate_tag: "omega.majorana-packet-wall-receipt.v1".into(),
        terminal,
        schedule_status: Some(cert.status),
        face_syndrome_zero: syn_zero,
        complex_name: Some(complex.name.into()),
        residual_weight: Some(defect.weight),
        repair_capacity_t: t_opt,
        authority_effect: none_auth(),
        notes,
    }
}

pub fn illustrative_p_pair() -> (f64, f64) {
    let p = 0.01_f64;
    let p_logical_shadow = p;
    (p, p_logical_shadow)
}

pub fn illustrative_suppression_regime(d: usize) -> &'static str {
    let t = repair_capacity_t(d);
    if t == 0 {
        "no_unique_correction_radius (t=0); CODE_DEMO only"
    } else {
        "finite_unique_correction_radius; CODE_DEMO only — not a physical threshold"
    }
}

pub fn wall_with_audit(
    complex: &ChainComplexGf2,
    residual: &[u8],
    max_weight: usize,
) -> Result<(RepairCapacityReceipt, PacketWallReceipt), String> {
    let audit = crate::repair_limit::audit_repair_capacity(complex, max_weight)?;
    let mut packet = ToyRepairPacket::complete(complex.clone(), residual.to_vec());
    packet.declared_distance_d = audit.d;
    Ok((audit, terminalize_packet(&packet)))
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CountRepairAction {
    pub action_id: String,
    pub cycle: usize,
    pub site: (usize, usize),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CountDefectEvent {
    pub defect_id: String,
    pub cycle: usize,
    pub site: (usize, usize),
    pub logical_witness_value: u8,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CountRepairPacket {
    pub name: String,
    pub seed: u64,
    pub carrier: Option<String>,
    pub lattice_size: Option<usize>,
    pub cycles: Option<usize>,
    pub correction_window: Option<usize>,
    pub c0_repair_actions: Option<Vec<CountRepairAction>>,
    pub c1_defect_events: Option<Vec<CountDefectEvent>>,
    pub d0_repair_map: Option<Vec<(String, String)>>,
    pub residual_proxy: Option<String>,
    pub logical_witness_proxy: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PacketMetrics {
    pub site_cycle_opportunities: usize,
    pub lambda_proj_count: usize,
    pub mu_repair_count: usize,
    pub residual_count: usize,
    pub logical_pairing_indicator: u8,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CountPacketReceipt {
    pub packet: String,
    pub seed: u64,
    pub terminal: PacketWallTerminal,
    pub metrics: Option<PacketMetrics>,
    pub residual_defect_ids: Vec<String>,
    pub declaration_errors: Vec<String>,
    pub reason: String,
    pub authority_effect: String,
}

fn inside_packet(cycle: usize, site: (usize, usize), cycles: usize, lattice: usize) -> bool {
    let (r, c) = site;
    cycle < cycles && r < lattice && c < lattice
}

fn is_blank_opt(field: &Option<String>) -> bool {
    field.as_ref().map(|s| s.is_empty()).unwrap_or(true)
}

fn is_positive_opt(field: Option<usize>) -> bool {
    matches!(field, Some(n) if n > 0)
}

fn validate_count_packet_scalars(packet: &CountRepairPacket, errors: &mut Vec<String>) {
    if is_blank_opt(&packet.carrier) {
        errors.push("carrier is undeclared".into());
    }
    if !is_positive_opt(packet.lattice_size) {
        errors.push("lattice_size must be a declared positive integer".into());
    }
    if !is_positive_opt(packet.cycles) {
        errors.push("cycles must be a declared positive integer".into());
    }
    if !is_positive_opt(packet.correction_window) {
        errors.push("correction_window must be a declared positive integer".into());
    }
}

fn validate_count_packet_declarations(packet: &CountRepairPacket) -> Vec<String> {
    let mut errors = Vec::new();
    validate_count_packet_scalars(packet, &mut errors);
    if packet.c0_repair_actions.is_none() {
        errors.push("C0 repair actions are undeclared".into());
    }
    if packet.c1_defect_events.is_none() {
        errors.push("C1 defect events are undeclared".into());
    }
    if packet.d0_repair_map.is_none() {
        errors.push("d0 repair map is undeclared".into());
    }
    if is_blank_opt(&packet.residual_proxy) {
        errors.push("residual proxy is undeclared".into());
    }
    if is_blank_opt(&packet.logical_witness_proxy) {
        errors.push("logical witness proxy is undeclared".into());
    }
    errors
}

fn has_unique_strs(items: &[&str]) -> bool {
    items.len() == items.iter().collect::<std::collections::BTreeSet<_>>().len()
}

fn validate_d0_repair_map(
    d0: &[(String, String)],
    action_ids: &[&str],
    defect_ids: &[&str],
    errors: &mut Vec<String>,
) {
    let mapped_defects: Vec<&str> = d0.iter().map(|(_, def)| def.as_str()).collect();
    if !has_unique_strs(&mapped_defects) {
        errors.push("d0 must not map multiple C0 actions to the same C1 event".into());
    }
    for (act, def) in d0 {
        if !action_ids.contains(&act.as_str()) {
            errors.push("d0 contains an undeclared C0 action".into());
        }
        if !defect_ids.contains(&def.as_str()) {
            errors.push("d0 contains an undeclared C1 defect event".into());
        }
    }
}

fn validate_actions_and_defects(
    actions: &[CountRepairAction],
    defects: &[CountDefectEvent],
    cycles: usize,
    lattice: usize,
    errors: &mut Vec<String>,
) {
    for a in actions {
        if !inside_packet(a.cycle, a.site, cycles, lattice) {
            errors.push(format!(
                "C0 action {} is outside the declared packet",
                a.action_id
            ));
        }
    }
    for d in defects {
        if !inside_packet(d.cycle, d.site, cycles, lattice) {
            errors.push(format!(
                "C1 event {} is outside the declared packet",
                d.defect_id
            ));
        }
        if d.logical_witness_value > 1 {
            errors.push(format!(
                "C1 event {} has a non-binary logical witness",
                d.defect_id
            ));
        }
    }
}

fn validate_count_packet(packet: &CountRepairPacket) -> Vec<String> {
    let mut errors = validate_count_packet_declarations(packet);
    if !errors.is_empty() {
        return errors;
    }

    let lattice = packet.lattice_size.unwrap();
    let cycles = packet.cycles.unwrap();
    let actions = packet.c0_repair_actions.as_ref().unwrap();
    let defects = packet.c1_defect_events.as_ref().unwrap();
    let d0 = packet.d0_repair_map.as_ref().unwrap();

    let action_ids: Vec<&str> = actions.iter().map(|a| a.action_id.as_str()).collect();
    let defect_ids: Vec<&str> = defects.iter().map(|d| d.defect_id.as_str()).collect();
    if !has_unique_strs(&action_ids) {
        errors.push("C0 action IDs must be unique".into());
    }
    if !has_unique_strs(&defect_ids) {
        errors.push("C1 defect IDs must be unique".into());
    }
    validate_d0_repair_map(d0, &action_ids, &defect_ids, &mut errors);
    validate_actions_and_defects(actions, defects, cycles, lattice, &mut errors);
    errors
}

pub fn terminalize_count_packet(packet: &CountRepairPacket) -> CountPacketReceipt {
    let errors = validate_count_packet(packet);
    if !errors.is_empty() {
        return CountPacketReceipt {
            packet: packet.name.clone(),
            seed: packet.seed,
            terminal: PacketWallTerminal::Refused,
            metrics: None,
            residual_defect_ids: Vec::new(),
            declaration_errors: errors,
            reason: "Incomplete or invalid declaration; refuse to infer a repair terminal.".into(),
            authority_effect: "None".into(),
        };
    }

    let lattice = packet.lattice_size.unwrap();
    let cycles = packet.cycles.unwrap();
    let actions = packet.c0_repair_actions.as_ref().unwrap();
    let defects = packet.c1_defect_events.as_ref().unwrap();
    let d0 = packet.d0_repair_map.as_ref().unwrap();

    let repaired: std::collections::BTreeSet<&str> =
        d0.iter().map(|(_, def)| def.as_str()).collect();
    let residual: Vec<&CountDefectEvent> = defects
        .iter()
        .filter(|d| !repaired.contains(d.defect_id.as_str()))
        .collect();
    let logical_pairing = if residual.iter().any(|d| d.logical_witness_value == 1) {
        1u8
    } else {
        0u8
    };
    let opportunities = lattice.saturating_mul(lattice).saturating_mul(cycles);

    let (terminal, reason) = if residual.is_empty() {
        (
            PacketWallTerminal::Absorbed,
            "Every declared C1 defect event lies in the declared finite d0 repair image.",
        )
    } else if logical_pairing == 0 {
        (
            PacketWallTerminal::ResidualInvisible,
            "Declared residual C1 events remain, but the toy logical witness proxy is zero.",
        )
    } else {
        (
            PacketWallTerminal::ResidualLogicallyVisible,
            "Repair image saturated on the declaration: residual C1 + nonzero logical witness remain (capacity wall on this finite packet).",
        )
    };

    CountPacketReceipt {
        packet: packet.name.clone(),
        seed: packet.seed,
        terminal,
        metrics: Some(PacketMetrics {
            site_cycle_opportunities: opportunities,
            lambda_proj_count: defects.len(),
            mu_repair_count: actions.len(),
            residual_count: residual.len(),
            logical_pairing_indicator: logical_pairing,
        }),
        residual_defect_ids: residual.iter().map(|d| d.defect_id.clone()).collect(),
        declaration_errors: Vec::new(),
        reason: reason.into(),
        authority_effect: "None".into(),
    }
}

pub fn demo_count_packet(
    name: &str,
    seed: u64,
    defect_count: usize,
    repair_count: usize,
    logically_visible_residual_indexes: &[usize],
) -> CountRepairPacket {
    let lattice = 3usize;
    let cycles = 4usize;
    let mut defects = Vec::new();
    for i in 0..defect_count {
        let cycle = i % cycles;
        let row = (i / cycles) % lattice;
        let col = (i / (cycles * lattice)) % lattice;
        defects.push(CountDefectEvent {
            defect_id: format!("e{i}"),
            cycle,
            site: (row, col),
            logical_witness_value: if logically_visible_residual_indexes.contains(&i) {
                1
            } else {
                0
            },
        });
    }
    let mut repairs = Vec::new();
    let mut d0 = Vec::new();
    let rmax = repair_count.min(defect_count);
    for i in 0..rmax {
        repairs.push(CountRepairAction {
            action_id: format!("a{i}"),
            cycle: defects[i].cycle,
            site: defects[i].site,
        });
        d0.push((format!("a{i}"), format!("e{i}")));
    }
    CountRepairPacket {
        name: name.into(),
        seed,
        carrier: Some("declared_binary_surface_code_proxy".into()),
        lattice_size: Some(lattice),
        cycles: Some(cycles),
        correction_window: Some(1),
        c0_repair_actions: Some(repairs),
        c1_defect_events: Some(defects),
        d0_repair_map: Some(d0),
        residual_proxy: Some(
            "unmapped C1 defect count normalized by declared site-cycle opportunities".into(),
        ),
        logical_witness_proxy: Some(
            "binary annotation on residual declared C1 defect events".into(),
        ),
    }
}

pub fn incomplete_count_packet() -> CountRepairPacket {
    CountRepairPacket {
        name: "incomplete_declaration".into(),
        seed: 404,
        carrier: Some("declared_binary_surface_code_proxy".into()),
        lattice_size: Some(3),
        cycles: Some(4),
        correction_window: Some(1),
        c0_repair_actions: None,
        c1_defect_events: Some(Vec::new()),
        d0_repair_map: None,
        residual_proxy: Some("unmapped C1".into()),
        logical_witness_proxy: Some("binary annotation".into()),
    }
}


#[derive(Debug, Clone)]
pub struct DiagnosticPacket {
    pub d0: Option<GF2Matrix>,
    pub d1: Option<GF2Matrix>,
    pub syndrome: Option<Vec<u8>>,
}

impl DiagnosticPacket {
    pub fn empty() -> Self {
        Self {
            d0: None,
            d1: None,
            syndrome: None,
        }
    }

    pub fn complete(d0: GF2Matrix, d1: GF2Matrix, syndrome: Vec<u8>) -> Self {
        Self {
            d0: Some(d0),
            d1: Some(d1),
            syndrome: Some(syndrome),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PacketRefusal {
    IncompletePacket { missing: &'static str },
    DimensionMismatch(String),
    Terminalize(String),
}

pub fn admit_or_refuse(packet: &DiagnosticPacket) -> Result<Gf2ScheduleReceipt, PacketRefusal> {
    let d0 = packet
        .d0
        .as_ref()
        .ok_or(PacketRefusal::IncompletePacket { missing: "d0" })?;
    let d1 = packet
        .d1
        .as_ref()
        .ok_or(PacketRefusal::IncompletePacket { missing: "d1" })?;
    let syndrome = packet
        .syndrome
        .as_ref()
        .ok_or(PacketRefusal::IncompletePacket {
            missing: "syndrome",
        })?;
    if syndrome.len() != d0.rows {
        return Err(PacketRefusal::DimensionMismatch(format!(
            "syndrome len {} != d0.rows {}",
            syndrome.len(),
            d0.rows
        )));
    }
    Gf2CocycleClassifier::classify(d0, d1, syndrome).map_err(PacketRefusal::Terminalize)
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::complexes::{
        exact_syndrome_example, surface_grid_2x2_torus, surface_open_single_edge_example,
        torus_logical_x_example, triangle,
    };
    use crate::gf2_terminalizer::GF2ScheduleStatus;

    #[test]
    fn incomplete_packet_refuses() {
        let r = terminalize_packet(&ToyRepairPacket::empty());
        assert_eq!(r.terminal, PacketWallTerminal::IncompleteRefusal);
        assert_eq!(r.authority_effect, "None");
        assert!(r.notes.contains("IncompletePacket"));

        let c = triangle();
        let missing_defect = ToyRepairPacket {
            complex: Some(c),
            defect: None,
            declared_distance_d: None,
            proposed_repair: None,
        };
        let r2 = terminalize_packet(&missing_defect);
        assert_eq!(r2.terminal, PacketWallTerminal::IncompleteRefusal);
        assert_eq!(r2.authority_effect, "None");
    }

    #[test]
    fn complete_torus_logical_closed_residual_auth_none() {
        let c = surface_grid_2x2_torus();
        let r = terminalize_packet(&ToyRepairPacket::complete(c, torus_logical_x_example()));
        assert_eq!(r.terminal, PacketWallTerminal::ClosedResidual);
        assert_eq!(r.authority_effect, "None");
        assert_eq!(r.face_syndrome_zero, Some(true));
    }

    #[test]
    fn single_edge_open() {
        let c = surface_grid_2x2_torus();
        let n = c.num_edges;
        let r = terminalize_packet(&ToyRepairPacket::complete(
            c,
            surface_open_single_edge_example(n),
        ));
        assert_eq!(r.terminal, PacketWallTerminal::OpenObstruction);
        assert_eq!(r.authority_effect, "None");
    }

    #[test]
    fn capacity_wall_on_logical_when_d_declared() {
        let c = surface_grid_2x2_torus();
        let mut p = ToyRepairPacket::complete(c, torus_logical_x_example());
        p.declared_distance_d = Some(2);
        let r = terminalize_packet(&p);
        assert_eq!(r.terminal, PacketWallTerminal::CapacityWallHit);
        assert_eq!(r.repair_capacity_t, Some(0));
        assert_eq!(r.authority_effect, "None");
    }

    #[test]
    fn count_packet_absorbed_and_capacity_wall() {
        let p = demo_count_packet("absorbed", 101, 3, 3, &[]);
        let r = terminalize_count_packet(&p);
        assert_eq!(r.terminal, PacketWallTerminal::Absorbed);
        assert_eq!(r.metrics.as_ref().unwrap().lambda_proj_count, 3);
        assert_eq!(r.metrics.as_ref().unwrap().mu_repair_count, 3);

        let p2 = demo_count_packet("wall", 303, 5, 2, &[4]);
        let r2 = terminalize_count_packet(&p2);
        assert_eq!(r2.terminal, PacketWallTerminal::ResidualLogicallyVisible);
        assert_eq!(r2.authority_effect, "None");

        let p3 = incomplete_count_packet();
        let r3 = terminalize_count_packet(&p3);
        assert_eq!(r3.terminal, PacketWallTerminal::Refused);
    }

    #[test]
    fn diagnostic_packet_gates() {
        assert!(matches!(
            admit_or_refuse(&DiagnosticPacket::empty()),
            Err(PacketRefusal::IncompletePacket { missing: "d0" })
        ));
        let c = triangle();
        let cert = admit_or_refuse(&DiagnosticPacket::complete(
            c.d0,
            c.d1,
            exact_syndrome_example(),
        ))
        .unwrap();
        assert_eq!(cert.status, GF2ScheduleStatus::Exact);
        assert_eq!(cert.q1_dimension, 0);
        let short = triangle();
        assert!(matches!(
            admit_or_refuse(&DiagnosticPacket::complete(short.d0, short.d1, vec![1, 0])),
            Err(PacketRefusal::DimensionMismatch(_))
        ));
    }

    #[test]
    fn illustrative_regime_splits_on_a_zero_radius() {
        assert_eq!(illustrative_p_pair(), (0.01, 0.01));
        assert_eq!(
            illustrative_suppression_regime(2),
            "no_unique_correction_radius (t=0); CODE_DEMO only"
        );
        assert_eq!(
            illustrative_suppression_regime(3),
            "finite_unique_correction_radius; CODE_DEMO only — not a physical threshold"
        );
    }
}
