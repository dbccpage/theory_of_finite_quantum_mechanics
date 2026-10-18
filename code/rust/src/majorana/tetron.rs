//! Homology-correct tetron-array carriers on a surface.
//!
//! A tetron **is a 2-cell**: one superconducting island, four MZMs on its
//! boundary, total fermion parity pinned by charging energy. An `R x C` array
//! of tetrons therefore tiles a surface, and the array's cohomology is the
//! surface's.
//!
//! - `C^0` = MZMs. A 0-cochain is a per-MZM reference-frame bit.
//! - `C^1` = parity-measurement channels. A channel on MZMs `a, b` measures
//!   `i * gamma_a * gamma_b`; a 1-cochain is the per-channel parity residual.
//! - `C^2` = islands. The product of the four channel parities around an island
//!   has every gamma twice, so it is a fixed scalar: a constraint.
//!
//! Three topologies, three Betti numbers:
//!
//! ```text
//! disk      chi = 1   dim H^1 = 0    open linear array (control)
//! cylinder  chi = 0   dim H^1 = 1    tetron ring / H-junction ladder
//! torus     chi = 0   dim H^1 = 2    periodic array (class typing possible)
//! ```
//!
//! Adjacent islands share the boundary MZM their coupler acts through. That is
//! an idealization of a coupled tetron array, and it is what makes the array a
//! clean cell complex.
//!
//! Python dual face: `omega_engine/omega_engine_majorana/carriers/surface_carrier.py`.
//! The golden fixtures in [`crate::harmonic`] pin the two surfaces together.
//!
//! AuthorityEffect: None. Nothing here asserts physical Majorana modes.

use crate::complexes::ChainComplexGf2;
use crate::gf2_terminalizer::{GF2Matrix, Gf2CocycleClassifier};

/// Surface the tetron array is laid out on.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Topology {
    /// Open in both directions. `dim H^1 = 0`.
    Disk,
    /// Periodic in columns, open in rows. `dim H^1 = 1`.
    Cylinder,
    /// Periodic in both directions. `dim H^1 = 2`.
    Torus,
}

impl Topology {
    /// `dim H^1` predicted by the Euler characteristic.
    pub fn expected_dim_h1(self) -> usize {
        match self {
            Topology::Disk => 0,
            Topology::Cylinder => 1,
            Topology::Torus => 2,
        }
    }

    pub fn name(self) -> &'static str {
        match self {
            Topology::Disk => "tetron_disk",
            Topology::Cylinder => "tetron_cylinder",
            Topology::Torus => "tetron_torus",
        }
    }

    /// Hardware reading, carried into receipts.
    pub fn hardware_reading(self) -> &'static str {
        match self {
            Topology::Disk => "open tetron array; no protected logical parity error",
            Topology::Cylinder => "tetron ring / H-junction ladder; one logical parity class",
            Topology::Torus => "periodic tetron array; two independent logical parity classes",
        }
    }

    fn wraps(self) -> (bool, bool) {
        match self {
            Topology::Disk => (false, false),
            Topology::Cylinder => (false, true),
            Topology::Torus => (true, true),
        }
    }
}

/// Which family of logical string to build.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Axis {
    /// Every horizontal channel in one column slot. Non-exact on cylinder and torus.
    Column,
    /// Every vertical channel in one row slot. Non-exact on the torus only.
    Row,
}

/// Measured structure of a tetron-array carrier.
///
/// Every field except `expected_dim_h1` is computed from the built matrices.
#[derive(Debug, Clone)]
pub struct TetronReport {
    pub topology: Topology,
    pub rows: usize,
    pub cols: usize,
    pub num_mzm: usize,
    pub num_channels: usize,
    pub num_islands: usize,
    pub euler_characteristic: i64,
    pub rank_d0: usize,
    pub rank_d1: usize,
    pub graph_b1: usize,
    pub dim_h1: usize,
    pub expected_dim_h1: usize,
    /// Horizontal channel index by `(vertex_row, column_slot)`.
    pub horizontal: Vec<Vec<usize>>,
    /// Vertical channel index by `(row_slot, vertex_col)`.
    pub vertical: Vec<Vec<usize>>,
    pub authority_effect: &'static str,
}

impl TetronReport {
    pub fn homology_matches_prediction(&self) -> bool {
        self.dim_h1 == self.expected_dim_h1
    }
}

/// Build an `rows x cols` tetron array on `topology`.
///
/// Returns the complex and a report whose `dim_h1` is *measured*, not asserted.
///
/// # Errors
///
/// A periodic direction of extent 1 identifies a channel's two endpoints and
/// would emit a self-loop with zero boundary; that is refused rather than built.
pub fn build_tetron_array(
    rows: usize,
    cols: usize,
    topology: Topology,
) -> Result<(ChainComplexGf2, TetronReport), String> {
    if rows == 0 || cols == 0 {
        return Err("rows and cols must be >= 1".into());
    }
    let (wrap_r, wrap_c) = topology.wraps();
    if wrap_c && cols < 2 {
        return Err(format!(
            "{:?} is periodic in columns; cols must be >= 2 (got {})",
            topology, cols
        ));
    }
    if wrap_r && rows < 2 {
        return Err(format!(
            "{:?} is periodic in rows; rows must be >= 2 (got {})",
            topology, rows
        ));
    }

    let vrows = if wrap_r { rows } else { rows + 1 };
    let vcols = if wrap_c { cols } else { cols + 1 };
    let num_mzm = vrows * vcols;
    let mzm = |i: usize, j: usize| -> usize { (i % vrows) * vcols + (j % vcols) };

    let mut d0_rows: Vec<Vec<u8>> = Vec::new();
    let add_channel = |u: usize, v: usize, sink: &mut Vec<Vec<u8>>| -> usize {
        let mut row = vec![0u8; num_mzm];
        row[u] ^= 1;
        row[v] ^= 1;
        sink.push(row);
        sink.len() - 1
    };

    // Horizontal channel H(i, j) joins MZM (i, j) to (i, j+1).
    let h_span = if wrap_c { vcols } else { vcols - 1 };
    let mut horizontal = vec![vec![usize::MAX; h_span]; vrows];
    for (i, slots) in horizontal.iter_mut().enumerate() {
        for (j, slot) in slots.iter_mut().enumerate() {
            *slot = add_channel(mzm(i, j), mzm(i, j + 1), &mut d0_rows);
        }
    }

    // Vertical channel V(i, j) joins MZM (i, j) to (i+1, j).
    let v_span = if wrap_r { vrows } else { vrows - 1 };
    let mut vertical = vec![vec![usize::MAX; vcols]; v_span];
    for (i, slots) in vertical.iter_mut().enumerate() {
        for (j, slot) in slots.iter_mut().enumerate() {
            *slot = add_channel(mzm(i, j), mzm(i + 1, j), &mut d0_rows);
        }
    }

    let num_channels = d0_rows.len();

    // Island 2-cells: island (i, j) is bounded by H(i,j), V(i,j+1), H(i+1,j),
    // V(i,j) -- a 4-cycle, so d1 . d0 = 0 holds by construction.
    let mut d1_rows: Vec<Vec<u8>> = Vec::new();
    for i in 0..rows {
        for j in 0..cols {
            let mut row = vec![0u8; num_channels];
            let j_next = if wrap_c { (j + 1) % vcols } else { j + 1 };
            let i_next = if wrap_r { (i + 1) % vrows } else { i + 1 };
            row[horizontal[i][j]] ^= 1;
            row[vertical[i][j_next]] ^= 1;
            row[horizontal[i_next][j]] ^= 1;
            row[vertical[i][j]] ^= 1;
            d1_rows.push(row);
        }
    }
    let num_islands = d1_rows.len();

    let d0 = GF2Matrix::from_data(d0_rows);
    let d1 = GF2Matrix::from_data(d1_rows);
    let (rank_d0, _) = d0.rref();
    let (rank_d1, _) = d1.rref();
    let dim_h1 = (num_channels - rank_d1) - rank_d0;

    let complex = ChainComplexGf2 {
        name: topology.name(),
        d0,
        d1,
        num_vertices: num_mzm,
        num_edges: num_channels,
        num_faces: num_islands,
    };
    if !Gf2CocycleClassifier::verify_boundary(&complex.d0, &complex.d1) {
        return Err("constructed carrier violates d1 . d0 = 0".into());
    }

    let report = TetronReport {
        topology,
        rows,
        cols,
        num_mzm,
        num_channels,
        num_islands,
        euler_characteristic: num_mzm as i64 - num_channels as i64 + num_islands as i64,
        rank_d0,
        rank_d1,
        graph_b1: num_channels - rank_d0,
        dim_h1,
        expected_dim_h1: topology.expected_dim_h1(),
        horizontal,
        vertical,
        authority_effect: "None",
    };
    Ok((complex, report))
}

/// An explicit closed 1-cochain generating a logical parity class.
///
/// [`Axis::Column`]: every horizontal channel in column slot `index`. Closed
/// because island `(i, index)` contains exactly `H(i, index)` and
/// `H(i+1, index)`. Non-exact on a torus and a cylinder.
///
/// [`Axis::Row`]: every vertical channel in row slot `index`. Non-exact on a
/// torus only -- on a cylinder it equals `d0 alpha` for `alpha = 1` on lattice
/// rows `<= index`.
///
/// Physically: a string of faulty channels crossing the array.
pub fn logical_class_representative(report: &TetronReport, axis: Axis, index: usize) -> Vec<u8> {
    let mut residual = vec![0u8; report.num_channels];
    match axis {
        Axis::Column => {
            let slot = index % report.horizontal[0].len();
            for row in &report.horizontal {
                residual[row[slot]] = 1;
            }
        }
        Axis::Row => {
            let slot = index % report.vertical.len();
            for &channel in &report.vertical[slot] {
                residual[channel] = 1;
            }
        }
    }
    residual
}

#[cfg(test)]
mod tests {
    use super::*;

    const ALL: [Topology; 3] = [Topology::Disk, Topology::Cylinder, Topology::Torus];

    #[test]
    fn cochain_relation_holds_everywhere() {
        for topology in ALL {
            for (rows, cols) in [(2usize, 2usize), (2, 3), (3, 3), (3, 4), (4, 4)] {
                let (complex, _) = build_tetron_array(rows, cols, topology).unwrap();
                assert!(
                    complex.verify_boundary(),
                    "d1 . d0 != 0 for {topology:?} {rows}x{cols}"
                );
            }
        }
    }

    #[test]
    fn dim_h1_is_the_topologys_betti_number() {
        for (topology, expected) in [
            (Topology::Disk, 0usize),
            (Topology::Cylinder, 1),
            (Topology::Torus, 2),
        ] {
            for (rows, cols) in [(2usize, 2usize), (2, 3), (3, 3), (3, 4), (4, 4)] {
                let (_, report) = build_tetron_array(rows, cols, topology).unwrap();
                assert_eq!(
                    report.dim_h1, expected,
                    "{topology:?} {rows}x{cols}: dim H^1 = {}, expected {expected}",
                    report.dim_h1
                );
                assert!(report.homology_matches_prediction());
            }
        }
    }

    #[test]
    fn dim_h1_agrees_with_the_euler_characteristic() {
        for topology in ALL {
            for (rows, cols) in [(2usize, 2usize), (3, 3), (3, 4)] {
                let (_, report) = build_tetron_array(rows, cols, topology).unwrap();
                let closed = topology == Topology::Torus;
                let predicted = (if closed { 2 } else { 1 }) - report.euler_characteristic;
                assert_eq!(
                    report.dim_h1 as i64, predicted,
                    "{topology:?} {rows}x{cols}"
                );
            }
        }
    }

    #[test]
    fn cell_counts_match_the_lattice() {
        let (_, disk) = build_tetron_array(2, 3, Topology::Disk).unwrap();
        assert_eq!(
            (disk.num_mzm, disk.num_channels, disk.num_islands),
            (12, 17, 6)
        );
        let (_, cyl) = build_tetron_array(2, 3, Topology::Cylinder).unwrap();
        assert_eq!((cyl.num_mzm, cyl.num_channels, cyl.num_islands), (9, 15, 6));
        let (_, tor) = build_tetron_array(2, 3, Topology::Torus).unwrap();
        assert_eq!((tor.num_mzm, tor.num_channels, tor.num_islands), (6, 12, 6));
    }

    #[test]
    fn degenerate_periodic_extents_are_refused() {
        // Kills: accepting a 1-row torus, and accepting a 1x1 disk without checking its cells.
        assert!(build_tetron_array(1, 1, Topology::Torus)
            .unwrap_err()
            .contains("columns"));
        assert!(build_tetron_array(2, 1, Topology::Torus)
            .unwrap_err()
            .contains("columns"));
        assert!(build_tetron_array(1, 2, Topology::Torus)
            .unwrap_err()
            .contains("rows"));
        assert!(build_tetron_array(1, 1, Topology::Cylinder)
            .unwrap_err()
            .contains("columns"));
        assert!(build_tetron_array(0, 3, Topology::Disk)
            .unwrap_err()
            .contains(">= 1"));
        let (_, disk) = build_tetron_array(1, 1, Topology::Disk).unwrap();
        assert_eq!(
            (disk.num_mzm, disk.num_channels, disk.num_islands, disk.dim_h1),
            (4, 4, 1, 0)
        );
        assert_eq!(disk.euler_characteristic, 1);
    }

    #[test]
    fn logical_generators_have_the_expected_weight() {
        let (_, report) = build_tetron_array(3, 4, Topology::Torus).unwrap();
        let column = logical_class_representative(&report, Axis::Column, 0);
        let row = logical_class_representative(&report, Axis::Row, 0);
        assert_eq!(column.iter().filter(|&&b| b == 1).count(), 3, "one per row");
        assert_eq!(row.iter().filter(|&&b| b == 1).count(), 4, "one per column");
    }

    #[test]
    fn logical_generators_are_closed() {
        for topology in ALL {
            let (complex, report) = build_tetron_array(3, 4, topology).unwrap();
            for axis in [Axis::Column, Axis::Row] {
                let residual = logical_class_representative(&report, axis, 0);
                let syndrome = crate::repair_limit::apply_d1(&complex.d1, &residual).unwrap();
                assert!(
                    syndrome.iter().all(|&b| b == 0),
                    "{topology:?} {axis:?} generator is not closed"
                );
            }
        }
    }
}
