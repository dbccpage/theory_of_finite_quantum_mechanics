//! Fock space CAR algebra, Jordan-Wigner signs, discrete fermionic Hamiltonians,
//! and exact Trotter path-sum expansions over Q.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};

/// Occupation bitmask representation of a many-body state with spin up and down.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct FockState {
    pub up_mask: u32,
    pub down_mask: u32,
}

impl FockState {
    pub const fn new(up_mask: u32, down_mask: u32) -> Self {
        Self { up_mask, down_mask }
    }

    pub fn count_up(&self) -> u32 {
        self.up_mask.count_ones()
    }

    pub fn count_down(&self) -> u32 {
        self.down_mask.count_ones()
    }

    pub fn total_particles(&self) -> u32 {
        self.count_up() + self.count_down()
    }

    pub fn is_occupied(&self, site: usize, spin: Spin) -> bool {
        match spin {
            Spin::Up => (self.up_mask & (1 << site)) != 0,
            Spin::Down => (self.down_mask & (1 << site)) != 0,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Spin {
    Up,
    Down,
}

/// Compute Jordan-Wigner sign (-1)^p when hopping or moving between site1 and site2 in a given mask.
/// p is the number of occupied sites strictly between min(site1, site2) and max(site1, site2).
pub fn jordan_wigner_hop_sign(mask: u32, site1: usize, site2: usize) -> i64 {
    let (low, high) = if site1 < site2 {
        (site1, site2)
    } else {
        (site2, site1)
    };
    if high <= low + 1 {
        return 1;
    }
    let mask_between = (mask >> (low + 1)) & ((1 << (high - low - 1)) - 1);
    if mask_between.count_ones() % 2 == 1 {
        -1
    } else {
        1
    }
}

/// Number of occupied sites strictly before `site` in `mask`.
pub fn preceding_count(mask: u32, site: usize) -> u32 {
    if site == 0 {
        0
    } else {
        let below = (1u32 << site) - 1;
        (mask & below).count_ones()
    }
}

/// Fermionic annihilation operator c_{site, spin} |state>.
/// Returns None if the site is not occupied, or Some((sign, new_state)).
pub fn car_annihilate(state: FockState, site: usize, spin: Spin) -> Option<(i64, FockState)> {
    match spin {
        Spin::Up => {
            if (state.up_mask & (1 << site)) == 0 {
                None
            } else {
                let p = preceding_count(state.up_mask, site);
                let sign = if p % 2 == 1 { -1 } else { 1 };
                let next_up = state.up_mask ^ (1 << site);
                Some((sign, FockState::new(next_up, state.down_mask)))
            }
        }
        Spin::Down => {
            if (state.down_mask & (1 << site)) == 0 {
                None
            } else {
                // All up particles precede down particles in standard CAR ordering.
                let p = state.count_up() + preceding_count(state.down_mask, site);
                let sign = if p % 2 == 1 { -1 } else { 1 };
                let next_down = state.down_mask ^ (1 << site);
                Some((sign, FockState::new(state.up_mask, next_down)))
            }
        }
    }
}

/// Fermionic creation operator c_{site, spin}^\dagger |state>.
/// Returns None if the site is already occupied, or Some((sign, new_state)).
pub fn car_create(state: FockState, site: usize, spin: Spin) -> Option<(i64, FockState)> {
    match spin {
        Spin::Up => {
            if (state.up_mask & (1 << site)) != 0 {
                None
            } else {
                let p = preceding_count(state.up_mask, site);
                let sign = if p % 2 == 1 { -1 } else { 1 };
                let next_up = state.up_mask | (1 << site);
                Some((sign, FockState::new(next_up, state.down_mask)))
            }
        }
        Spin::Down => {
            if (state.down_mask & (1 << site)) != 0 {
                None
            } else {
                let p = state.count_up() + preceding_count(state.down_mask, site);
                let sign = if p % 2 == 1 { -1 } else { 1 };
                let next_down = state.down_mask | (1 << site);
                Some((sign, FockState::new(state.up_mask, next_down)))
            }
        }
    }
}

/// Hopping operator c_{dst}^\dagger c_{src} acting on state.
pub fn car_hop(state: FockState, src: usize, dst: usize, spin: Spin) -> Option<(i64, FockState)> {
    let (ann_sign, interim) = car_annihilate(state, src, spin)?;
    let (cre_sign, final_state) = car_create(interim, dst, spin)?;
    Some((ann_sign * cre_sign, final_state))
}

/// Finite undirected lattice for fermionic models.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FermionicLattice {
    pub num_sites: usize,
    pub edges: Vec<(usize, usize)>,
}

impl FermionicLattice {
    pub fn new(num_sites: usize, edges: Vec<(usize, usize)>) -> Result<Self, &'static str> {
        if num_sites == 0 {
            return Err("num_sites must be positive");
        }
        let mut clean = Vec::new();
        for (u, v) in edges {
            if u >= num_sites || v >= num_sites {
                return Err("edge endpoint out of range");
            }
            if u == v {
                return Err("self-loops are not allowed in simple hopping lattice");
            }
            let edge = if u < v { (u, v) } else { (v, u) };
            if !clean.contains(&edge) {
                clean.push(edge);
            }
        }
        clean.sort_unstable();
        Ok(Self {
            num_sites,
            edges: clean,
        })
    }

    pub fn linear_chain(n: usize, periodic: bool) -> Result<Self, &'static str> {
        if n == 0 {
            return Err("chain length must be positive");
        }
        let mut edges = Vec::new();
        for i in 0..(n.saturating_sub(1)) {
            edges.push((i, i + 1));
        }
        if periodic && n > 2 {
            edges.push((n - 1, 0));
        }
        Self::new(n, edges)
    }

    pub fn triangle() -> Self {
        Self::new(3, vec![(0, 1), (1, 2), (0, 2)]).unwrap()
    }

    pub fn square_plaquette() -> Self {
        Self::new(4, vec![(0, 1), (1, 2), (2, 3), (3, 0)]).unwrap()
    }

    /// 2D rectangular grid of `rows x cols` sites, optionally with periodic boundary conditions.
    pub fn rectangular_grid(rows: usize, cols: usize, periodic: bool) -> Result<Self, &'static str> {
        if rows == 0 || cols == 0 {
            return Err("grid dimensions must be positive");
        }
        let num_sites = rows * cols;
        let idx = |r: usize, c: usize| r * cols + c;
        let mut edges = Vec::new();
        for r in 0..rows {
            for c in 0..cols {
                if c + 1 < cols {
                    edges.push((idx(r, c), idx(r, c + 1)));
                } else if periodic && cols > 2 {
                    edges.push((idx(r, c), idx(r, 0)));
                }
                if r + 1 < rows {
                    edges.push((idx(r, c), idx(r + 1, c)));
                } else if periodic && rows > 2 {
                    edges.push((idx(r, c), idx(0, c)));
                }
            }
        }
        Self::new(num_sites, edges)
    }

    /// 2-leg frustrated triangular ladder with `rungs` rungs (`2 * rungs` sites).
    pub fn triangular_ladder(rungs: usize) -> Result<Self, &'static str> {
        if rungs < 2 {
            return Err("triangular ladder requires at least 2 rungs");
        }
        let num_sites = 2 * rungs;
        let mut edges = Vec::new();
        for i in 0..rungs {
            let top = 2 * i;
            let bot = 2 * i + 1;
            edges.push((top, bot));
            if i + 1 < rungs {
                let next_top = 2 * (i + 1);
                let next_bot = 2 * (i + 1) + 1;
                edges.push((top, next_top));
                edges.push((bot, next_bot));
                edges.push((top, next_bot));
            }
        }
        Self::new(num_sites, edges)
    }
}

/// Exact Discrete Fermionic Hubbard Hamiltonian matrix over Q.
#[derive(Clone, Debug)]
pub struct DiscreteFermionicHamiltonian {
    pub lattice: FermionicLattice,
    pub t: BigRational,
    pub u: BigRational,
    pub mu: BigRational,
    pub num_up: usize,
    pub num_down: usize,
    pub basis: Vec<FockState>,
    pub matrix: Vec<Vec<BigRational>>,
}

impl DiscreteFermionicHamiltonian {
    pub fn new(
        lattice: FermionicLattice,
        t: BigRational,
        u: BigRational,
        mu: BigRational,
        num_up: usize,
        num_down: usize,
    ) -> Result<Self, &'static str> {
        if num_up > lattice.num_sites || num_down > lattice.num_sites {
            return Err("particle count exceeds lattice site capacity");
        }
        if num_up + num_down == 0 {
            return Err("physical sector must have at least one particle");
        }
        let basis = Self::build_basis(lattice.num_sites, num_up, num_down);
        let matrix = Self::build_hamiltonian(&lattice, &t, &u, &mu, &basis);
        Ok(Self {
            lattice,
            t,
            u,
            mu,
            num_up,
            num_down,
            basis,
            matrix,
        })
    }

    fn build_basis(num_sites: usize, num_up: usize, num_down: usize) -> Vec<FockState> {
        let mut up_masks = Vec::new();
        let total_masks = 1u32 << num_sites;
        for mask in 0..total_masks {
            if mask.count_ones() as usize == num_up {
                up_masks.push(mask);
            }
        }
        let mut down_masks = Vec::new();
        for mask in 0..total_masks {
            if mask.count_ones() as usize == num_down {
                down_masks.push(mask);
            }
        }
        let mut basis = Vec::with_capacity(up_masks.len() * down_masks.len());
        for &u_m in &up_masks {
            for &d_m in &down_masks {
                basis.push(FockState::new(u_m, d_m));
            }
        }
        basis
    }

    fn build_hamiltonian(
        lattice: &FermionicLattice,
        t: &BigRational,
        u: &BigRational,
        mu: &BigRational,
        basis: &[FockState],
    ) -> Vec<Vec<BigRational>> {
        let dim = basis.len();
        let mut mat = vec![vec![BigRational::zero(); dim]; dim];
        let mut index_map = std::collections::HashMap::new();
        for (i, state) in basis.iter().enumerate() {
            index_map.insert(*state, i);
        }

        for (i, state) in basis.iter().enumerate() {
            // Diagonal on-site interaction U * n_up * n_down - mu * (n_up + n_down)
            let mut double_occ = 0i64;
            for s in 0..lattice.num_sites {
                if state.is_occupied(s, Spin::Up) && state.is_occupied(s, Spin::Down) {
                    double_occ += 1;
                }
            }
            let total_n = (state.total_particles()) as i64;
            let diag = u * BigRational::from(BigInt::from(double_occ))
                - mu * BigRational::from(BigInt::from(total_n));
            mat[i][i] = &mat[i][i] + diag;

            // Off-diagonal hopping: -t \sum_<i,j> (c_i^\dagger c_j + h.c.)
            for &(src_site, dst_site) in &lattice.edges {
                for (src, dst) in [(src_site, dst_site), (dst_site, src_site)] {
                    // Spin Up hopping
                    if let Some((sign, next_state)) = car_hop(*state, src, dst, Spin::Up) {
                        if let Some(&j) = index_map.get(&next_state) {
                            let hop_contrib = -t * BigRational::from(BigInt::from(sign));
                            mat[j][i] = &mat[j][i] + hop_contrib;
                        }
                    }
                    // Spin Down hopping
                    if let Some((sign, next_state)) = car_hop(*state, src, dst, Spin::Down) {
                        if let Some(&j) = index_map.get(&next_state) {
                            let hop_contrib = -t * BigRational::from(BigInt::from(sign));
                            mat[j][i] = &mat[j][i] + hop_contrib;
                        }
                    }
                }
            }
        }
        mat
    }

    /// Exact Euler transfer matrix T = I - dtau * H over Q.
    pub fn exact_transfer_matrix(&self, dtau: &BigRational) -> Vec<Vec<BigRational>> {
        let dim = self.matrix.len();
        let mut t_mat = vec![vec![BigRational::zero(); dim]; dim];
        for i in 0..dim {
            for j in 0..dim {
                let delta = if i == j {
                    BigRational::one()
                } else {
                    BigRational::zero()
                };
                t_mat[i][j] = delta - dtau * &self.matrix[i][j];
            }
        }
        t_mat
    }

    /// Exact Trotter partition functions and average fermion sign over Q.
    pub fn compute_partition_functions(
        &self,
        beta: &BigRational,
        trotter_steps: usize,
    ) -> Result<PartitionReceipt, &'static str> {
        if trotter_steps == 0 {
            return Err("trotter_steps must be positive");
        }
        if beta <= &BigRational::zero() {
            return Err("beta must be positive");
        }
        let dtau = beta / BigRational::from(BigInt::from(trotter_steps));
        let dim = self.matrix.len();
        let t_ferm = self.exact_transfer_matrix(&dtau);

        let mut t_bos = vec![vec![BigRational::zero(); dim]; dim];
        for i in 0..dim {
            for j in 0..dim {
                t_bos[i][j] = t_ferm[i][j].abs();
            }
        }

        let mut p_ferm = t_ferm.clone();
        let mut p_bos = t_bos.clone();

        for _ in 1..trotter_steps {
            p_ferm = mat_mul(&p_ferm, &t_ferm);
            p_bos = mat_mul(&p_bos, &t_bos);
        }

        let mut z_ferm = BigRational::zero();
        let mut z_bos = BigRational::zero();
        for i in 0..dim {
            z_ferm = z_ferm + &p_ferm[i][i];
            z_bos = z_bos + &p_bos[i][i];
        }

        let avg_sign = if z_bos.is_zero() {
            BigRational::zero()
        } else {
            &z_ferm / &z_bos
        };

        Ok(PartitionReceipt {
            trotter_steps,
            dim,
            z_fermionic: z_ferm,
            z_bosonic: z_bos,
            average_sign: avg_sign,
        })
    }

    /// Enumerate all non-zero closed cyclic Euler paths and compute exact signed amplitudes.
    pub fn generate_sample_paths(
        &self,
        beta: &BigRational,
        trotter_steps: usize,
    ) -> Result<Vec<EulerPath>, &'static str> {
        if trotter_steps == 0 {
            return Err("trotter_steps must be positive");
        }
        let dtau = beta / BigRational::from(BigInt::from(trotter_steps));
        let t = self.exact_transfer_matrix(&dtau);
        let dim = self.matrix.len();
        let mut paths = Vec::new();

        // Recursively or iteratively generate paths
        let mut stack = Vec::new();
        for start_idx in 0..dim {
            stack.push((vec![start_idx], BigRational::one()));
            while let Some((seq, current_weight)) = stack.pop() {
                let step = seq.len();
                let last = *seq.last().unwrap();
                if step == trotter_steps {
                    // Close the cycle to start_idx
                    let hop_amp = &t[start_idx][last];
                    let total_amp = &current_weight * hop_amp;
                    if !total_amp.is_zero() {
                        let mut closed = seq.clone();
                        closed.push(start_idx);
                        let sign = if total_amp > BigRational::zero() {
                            1
                        } else {
                            -1
                        };
                        paths.push(EulerPath {
                            path_indices: closed,
                            signed_amplitude: total_amp.clone(),
                            abs_weight: total_amp.abs(),
                            parity_sign: sign,
                            is_cancelling: sign < 0,
                        });
                    }
                } else {
                    for next_idx in 0..dim {
                        let hop_amp = &t[next_idx][last];
                        if !hop_amp.is_zero() {
                            let next_weight = &current_weight * hop_amp;
                            let mut next_seq = seq.clone();
                            next_seq.push(next_idx);
                            stack.push((next_seq, next_weight));
                        }
                    }
                }
            }
        }

        Ok(paths)
    }
}

fn mat_mul(a: &[Vec<BigRational>], b: &[Vec<BigRational>]) -> Vec<Vec<BigRational>> {
    let n = a.len();
    let mut c = vec![vec![BigRational::zero(); n]; n];
    for i in 0..n {
        for k in 0..n {
            if a[i][k].is_zero() {
                continue;
            }
            for j in 0..n {
                let term = &a[i][k] * &b[k][j];
                c[i][j] = &c[i][j] + term;
            }
        }
    }
    c
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct PartitionReceipt {
    pub trotter_steps: usize,
    pub dim: usize,
    pub z_fermionic: BigRational,
    pub z_bosonic: BigRational,
    pub average_sign: BigRational,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct EulerPath {
    pub path_indices: Vec<usize>,
    pub signed_amplitude: BigRational,
    pub abs_weight: BigRational,
    pub parity_sign: i64,
    pub is_cancelling: bool,
}

pub mod rational_str_serde {
    use num_rational::BigRational;
    use serde::{self, Deserialize, Deserializer, Serializer};
    use std::str::FromStr;

    pub fn serialize<S>(value: &BigRational, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(&value.to_string())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<BigRational, D::Error>
    where
        D: Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        BigRational::from_str(&s).map_err(serde::de::Error::custom)
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FockLatticeScalingRow {
    pub label: String,
    pub num_sites: usize,
    pub num_edges: usize,
    pub num_up: usize,
    pub num_down: usize,
    pub fock_dim: usize,
    pub trotter_steps: usize,
    #[serde(with = "rational_str_serde")]
    pub z_fermionic: BigRational,
    #[serde(with = "rational_str_serde")]
    pub z_bosonic: BigRational,
    #[serde(with = "rational_str_serde")]
    pub average_sign: BigRational,
    pub has_sign_cancellation: bool,
}

/// Serialize `FockLatticeScalingRow` slice to canonical 2-space pretty JSON with LF line endings.
pub fn fock_scaling_to_canonical_json(rows: &[FockLatticeScalingRow]) -> Result<String, String> {
    serde_json::to_string_pretty(rows).map_err(|e| e.to_string())
}

/// Deserialize `FockLatticeScalingRow` vector from canonical JSON string.
pub fn fock_scaling_from_canonical_json(
    json_str: &str,
) -> Result<Vec<FockLatticeScalingRow>, String> {
    serde_json::from_str(json_str).map_err(|e| e.to_string())
}

/// Finite lattice scaling benchmark for exact Fock-space partition functions across
/// 1D chains/rings, 2D rectangular grids, and frustrated triangular ladders up to N = 8 sites.
pub fn benchmark_fock_lattice_scaling(
    beta: &BigRational,
    trotter_steps: usize,
) -> Result<Vec<FockLatticeScalingRow>, &'static str> {
    let specs: Vec<(&str, FermionicLattice, usize, usize, BigRational)> = vec![
        ("triangle_3", FermionicLattice::triangle(), 2, 0, BigRational::zero()),
        ("square_4", FermionicLattice::square_plaquette(), 2, 0, BigRational::zero()),
        (
            "ring_5_frustrated",
            FermionicLattice::linear_chain(5, true)?,
            2,
            0,
            BigRational::zero(),
        ),
        (
            "chain_6_open",
            FermionicLattice::linear_chain(6, false)?,
            3,
            0,
            BigRational::zero(),
        ),
        (
            "ladder_2x3_rect",
            FermionicLattice::rectangular_grid(2, 3, false)?,
            2,
            1,
            BigRational::from(BigInt::from(2)),
        ),
        (
            "triangular_ladder_6",
            FermionicLattice::triangular_ladder(3)?,
            2,
            0,
            BigRational::zero(),
        ),
        (
            "ring_7_frustrated",
            FermionicLattice::linear_chain(7, true)?,
            2,
            0,
            BigRational::zero(),
        ),
        (
            "grid_2x4_rect",
            FermionicLattice::rectangular_grid(2, 4, false)?,
            2,
            0,
            BigRational::zero(),
        ),
        (
            "triangular_ladder_8",
            FermionicLattice::triangular_ladder(4)?,
            2,
            0,
            BigRational::zero(),
        ),
    ];

    let mut rows = Vec::with_capacity(specs.len());
    for (label, lattice, num_up, num_down, u_val) in specs {
        let num_sites = lattice.num_sites;
        let num_edges = lattice.edges.len();
        let ham = DiscreteFermionicHamiltonian::new(
            lattice,
            BigRational::one(),
            u_val,
            BigRational::zero(),
            num_up,
            num_down,
        )?;
        let receipt = ham.compute_partition_functions(beta, trotter_steps)?;
        let has_sign_cancellation = receipt.average_sign < BigRational::one();
        rows.push(FockLatticeScalingRow {
            label: label.to_string(),
            num_sites,
            num_edges,
            num_up,
            num_down,
            fock_dim: receipt.dim,
            trotter_steps,
            z_fermionic: receipt.z_fermionic,
            z_bosonic: receipt.z_bosonic,
            average_sign: receipt.average_sign,
            has_sign_cancellation,
        });
    }
    Ok(rows)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn car_anticommutation_relation_on_fock_states() {
        // Test {c_i, c_j^\dagger} = delta_ij and {c_i, c_j} = 0
        let state = FockState::new(0, 0); // Vacuum
        let (sign1, st1) = car_create(state, 0, Spin::Up).unwrap();
        assert_eq!(sign1, 1);
        assert_eq!(st1, FockState::new(1, 0));

        // c_1^\dagger c_0^\dagger |0>
        let (sign2, st2) = car_create(st1, 1, Spin::Up).unwrap();
        assert_eq!(sign2, -1);
        assert_eq!(st2, FockState::new(3, 0));

        // c_0^\dagger c_1^\dagger |0> has opposite sign (+1), confirming {c_0^\dagger, c_1^\dagger} = 0
        let (sign3, st3) = car_create(state, 1, Spin::Up).unwrap();
        assert_eq!(sign3, 1);
        let (sign4, st4) = car_create(st3, 0, Spin::Up).unwrap();
        assert_eq!(sign4, 1);
        assert_eq!(st4, st2);
        assert_eq!(sign2 + sign4, 0, "anticommutation of creation operators");
    }

    #[test]
    fn free_fermion_triangle_paths_and_cancellation() {
        // 3-site triangle with 2 spin-up fermions
        let lattice = FermionicLattice::triangle();
        let ham = DiscreteFermionicHamiltonian::new(
            lattice,
            BigRational::one(),
            BigRational::zero(),
            BigRational::zero(),
            2,
            0,
        )
        .unwrap();
        assert_eq!(ham.matrix.len(), 3); // C(3, 2) = 3 states

        let beta = BigRational::from(BigInt::from(2));
        let receipt = ham.compute_partition_functions(&beta, 3).unwrap();
        assert!(receipt.z_bosonic > BigRational::zero());

        let paths = ham.generate_sample_paths(&beta, 3).unwrap();
        assert!(!paths.is_empty());
        let has_cancelling = paths.iter().any(|p| p.is_cancelling);
        assert!(has_cancelling, "triangle geometry exhibits negative signed paths");
    }

    #[test]
    fn fock_lattice_scaling_benchmark_up_to_8_sites() {
        let beta = BigRational::from(BigInt::from(2));
        let rows = benchmark_fock_lattice_scaling(&beta, 3).unwrap();
        assert_eq!(rows.len(), 9);

        let expected_dims = [3usize, 6, 10, 20, 90, 15, 21, 28, 28];
        let expected_sites = [3usize, 4, 5, 6, 6, 6, 7, 8, 8];
        for (i, row) in rows.iter().enumerate() {
            assert_eq!(row.num_sites, expected_sites[i], "label={}", row.label);
            assert_eq!(row.fock_dim, expected_dims[i], "label={}", row.label);
            assert!(row.z_bosonic > BigRational::zero(), "label={}", row.label);
        }

        // Bipartite lattices at trotter_steps = 3 have no odd cycles of length 3, so every
        // 3-step closed walk traverses edges in cancelling pairs and has average_sign == 1.
        for bipartite in ["square_4", "chain_6_open", "grid_2x4_rect"] {
            let r = rows.iter().find(|row| row.label == bipartite).unwrap();
            assert_eq!(r.average_sign, BigRational::one(), "label={bipartite}");
            assert!(!r.has_sign_cancellation, "label={bipartite}");
        }

        // Frustrated non-bipartite lattices containing length-3 triangles (triangle_3,
        // triangular_ladder_6, triangular_ladder_8) exhibit sign cancellation at trotter_steps = 3.
        for frustrated in ["triangle_3", "triangular_ladder_6", "triangular_ladder_8"] {
            let r = rows.iter().find(|row| row.label == frustrated).unwrap();
            assert!(
                r.has_sign_cancellation,
                "expected sign cancellation on {frustrated}, got average_sign={}",
                r.average_sign
            );
        }
    }

    #[test]
    fn fock_lattice_scaling_matches_cross_language_json_fixture_bit_for_bit() {
        let beta = BigRational::from(BigInt::from(2));
        let rows = benchmark_fock_lattice_scaling(&beta, 3).unwrap();
        let serialized = fock_scaling_to_canonical_json(&rows).unwrap();
        let fixture = include_str!("fixtures/fock_lattice_scaling.json").replace("\r\n", "\n");
        assert_eq!(
            serialized.as_bytes(),
            fixture.as_bytes(),
            "Rust benchmark_fock_lattice_scaling JSON output drifted from cross-language fixture"
        );
        let round_trip = fock_scaling_from_canonical_json(&fixture).unwrap();
        assert_eq!(round_trip, rows);
    }
}
