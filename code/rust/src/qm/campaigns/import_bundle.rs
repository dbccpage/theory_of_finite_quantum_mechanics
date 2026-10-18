//! Import independence (Target 13) and import sufficiency (Target 14).
//!
//! **Target 13:** one concrete finite countermodel per import slot — data carriers,
//! not a Boolean flag matrix. `OB-U1` and `LocalTomography` are **separate** rows
//! (not a coupled `BUNDLE-U1-LT` slot).
//!
//! **Target 14:** `ImportBundle` holds optional typed **witnesses**;
//! `build_downstream` constructs downstream structures only from those witnesses
//! (Boolean pathway coverage alone is insufficient).
//!
//! AuthorityEffect: None. Not PROVED. Not GlobalGreen. TOY-MECH finite hosts only.

/// Fence string (proposal).
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; import-bundle TOY-MECH.";

// ---------------------------------------------------------------------------
// Target 13 — import slots and finite hosts
// ---------------------------------------------------------------------------

/// Named freeze-import slots for the independence basis (minimum six).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ImportSlot {
    /// Finite spectral theorem / Hermitian diagonalization.
    Spectral,
    /// Monoidal tensor composition (⊗, not ⊕ / bare product alone).
    Monoidal,
    /// Composite-system local tomography (param identity / reconstructibility).
    LocalTomography,
    /// Complex / U(1) phase carrier (`OB-U1`).
    ObU1,
    /// Born quadratic uniqueness / Gleason-style frame function.
    BornGleason,
    /// Instrument / Lüders state-update map (not readout alone).
    Instruments,
    /// A NON-COMMUTING observable algebra (`OB-NONCOMM`).
    ///
    /// Added 2026-08-04 (R2-C9). Round 1 produced the separating pair
    /// (`X = [[0,1],[1,0]]`, `Z = [[1,0],[0,-1]]` — symmetric on the same
    /// carrier, `XZ ≠ ZX`) but left the slot `DeclaredNotModelled` because
    /// `FiniteImportHost` carried no observable-algebra field. It does now.
    NonCommuting,
}

impl ImportSlot {
    /// Canonical enumeration order for the independence basis.
    pub const ALL: [ImportSlot; 7] = [
        ImportSlot::Spectral,
        ImportSlot::Monoidal,
        ImportSlot::LocalTomography,
        ImportSlot::ObU1,
        ImportSlot::BornGleason,
        ImportSlot::Instruments,
        ImportSlot::NonCommuting,
    ];

    /// Stable string id.
    pub fn id(self) -> &'static str {
        match self {
            ImportSlot::Spectral => "Spectral",
            ImportSlot::Monoidal => "Monoidal",
            ImportSlot::LocalTomography => "LocalTomography",
            ImportSlot::ObU1 => "OB-U1",
            ImportSlot::BornGleason => "BornGleason",
            ImportSlot::Instruments => "Instruments",
            ImportSlot::NonCommuting => "NonCommuting",
        }
    }
}

/// Integer complex entry \(a + bi\).
pub type Zi = (i64, i64);

/// Declared composition law on a finite host.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompositionKind {
    /// Tensor product: \(\dim(AB)=\dim A\cdot\dim B\).
    Tensor,
    /// Direct sum only: \(\dim(A\oplus B)=\dim A+\dim B\) (not monoidal tensor).
    DirectSum,
    /// No composition structure declared.
    None,
}

/// Phase-carrier kind on the host.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PhaseKind {
    /// Continuous \(U(1)\) acts on complex amplitudes.
    ComplexU1,
    /// Real amplitudes only (no complex phase fiber).
    RealOnly,
    /// No phase structure at all.
    None,
}

/// Born / frame-function selection on the host.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BornKind {
    /// Quadratic Born: \(p \propto |c|^2\).
    Quadratic,
    /// Linear (non-Gleason) readout: \(p \propto |c|\) (absolute, integer proxy).
    Linear,
    /// No probability selection declared.
    Absent,
}

/// Concrete finite host data used to **evaluate** import predicates.
///
/// Slot admission is derived from these fields by the predicate functions
/// below, not from a hand-written bool row. Three slots are computed from
/// matrix and count data: Spectral, LocalTomography and NonCommuting. The other
/// four read a declaration: Monoidal the composition kind, OB-U1 the phase
/// kind (which fixes the phase group; the fiber is then computed on the
/// amplitudes), BornGleason the Born kind, and Instruments the update flag. The
/// independence countermodels for those four slots therefore differ from an
/// admitting host by a declaration, not by computed structure: they show the
/// declarations are independent, and derive no absence of structure.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteImportHost {
    /// Stable countermodel / host id.
    pub id: &'static str,
    /// Human-readable failure description for the dropped slot.
    pub drop_note: &'static str,
    /// \(2\times 2\) matrix over \(\mathbb{Z}[i]\) (row-major) for spectral checks.
    pub matrix_2x2: [[Zi; 2]; 2],
    /// Factor dimensions for composition / tomography.
    pub dim_a: usize,
    pub dim_b: usize,
    /// Declared composition law.
    pub composition: CompositionKind,
    /// Phase structure.
    pub phase: PhaseKind,
    /// Theory-specific density / state parameter counts (unnormalized incl. trace).
    /// Local tomography identity: `local_param_a * local_param_b == joint_param`.
    pub local_param_a: usize,
    pub local_param_b: usize,
    pub joint_param: usize,
    /// Born selection kind.
    pub born: BornKind,
    /// Whether a Lüders / instrument update map is present (not readout alone).
    pub has_instrument_update: bool,
    /// Sample amplitudes \((re, im)\) on a single factor (length = `dim_a`).
    pub amplitudes: Vec<Zi>,
    /// Spectral eigenvalues used when the matrix is reconstructible (else ignored).
    pub eigenvalues: [i64; 2],
    /// Rank-1 spectral projectors (diagonal toy) when spectral holds.
    pub projectors_diag: [[i64; 2]; 2],
    /// Two real-symmetric 2x2 integer observables on the SAME carrier.
    ///
    /// The `OB-NONCOMM` witness. Real-symmetric (not complex Hermitian) keeps
    /// the datum exact over `i64` while still being a legitimate observable
    /// algebra; non-commutativity is the property under test and does not need
    /// complex entries to exhibit.
    pub observables: [[[i64; 2]; 2]; 2],
}

impl FiniteImportHost {
    /// Which carrier class this host's declared parameter counts describe.
    ///
    /// Decided by comparing `(local_param_a, local_param_b, joint_param)`
    /// against the canonical counts for the host's own `(dim_a, dim_b)`. This
    /// is what makes independence evidence scopeable: a witness carrying
    /// simplex counts is evidence about classical carriers, whatever the rest
    /// of its fields are named.
    pub fn carrier_class(&self) -> CarrierClass {
        let (da, db) = (self.dim_a, self.dim_b);
        let joint = da * db;
        let declared = (self.local_param_a, self.local_param_b, self.joint_param);
        if declared == (da, db, joint) {
            CarrierClass::ClassicalSimplex
        } else if declared
            == (
                da * (da + 1) / 2,
                db * (db + 1) / 2,
                joint * (joint + 1) / 2,
            )
        {
            CarrierClass::RealQuantum
        } else if declared == (da * da, db * db, joint * joint) {
            CarrierClass::ComplexQuantum
        } else {
            CarrierClass::Unrecognised
        }
    }

    /// Hermitian: \(M_{ij} = \overline{M_{ji}}\).
    pub fn is_hermitian(&self) -> bool {
        let m = &self.matrix_2x2;
        for i in 0..2 {
            for j in 0..2 {
                let (a, b) = m[i][j];
                let (c, d) = m[j][i];
                // conjugate of m[j][i] is (c, -d)
                if a != c || b != -d {
                    return false;
                }
            }
        }
        true
    }

    /// Spectral reconstruction for diagonal real-symmetric toy:
    /// \(M = \lambda_0 P_0 + \lambda_1 P_1\) with diagonal projectors.
    pub fn spectral_reconstructs(&self) -> bool {
        if !self.is_hermitian() {
            return false;
        }
        // Only diagonal real entries in this finite toy calculus.
        let m = &self.matrix_2x2;
        if m[0][1] != (0, 0) || m[1][0] != (0, 0) {
            // Off-diagonal Hermitian (e.g. Pauli-X) needs a fuller spectral host;
            // treat non-diagonal as spectral-fail in this finite diagonal toy.
            return false;
        }
        if m[0][0].1 != 0 || m[1][1].1 != 0 {
            return false;
        }
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        // Projectors: diagonal 0/1, orthogonal, sum to I.
        if p0[0] + p1[0] != 1 || p0[1] + p1[1] != 1 {
            return false;
        }
        if p0[0] * p1[0] != 0 || p0[1] * p1[1] != 0 {
            return false;
        }
        let r0 = self.eigenvalues[0] * p0[0] + self.eigenvalues[1] * p1[0];
        let r1 = self.eigenvalues[0] * p0[1] + self.eigenvalues[1] * p1[1];
        m[0][0].0 == r0 && m[1][1].0 == r1
    }

    /// Monoidal tensor declared with dimension law \(\dim A\cdot\dim B\).
    pub fn monoidal_holds(&self) -> bool {
        self.composition == CompositionKind::Tensor
            && self.dim_a >= 1
            && self.dim_b >= 1
            && self.dim_a.saturating_mul(self.dim_b) >= 2
    }

    /// Composite local tomography param identity (theory-relative).
    pub fn local_tomography_holds(&self) -> bool {
        self.local_param_a > 0
            && self.local_param_b > 0
            && self.joint_param > 0
            && self.local_param_a.saturating_mul(self.local_param_b) == self.joint_param
    }

    /// The finite phase group of the declared phase kind, as Gaussian units:
    /// `{1, i, -1, -i}` for `ComplexU1`, `{1, -1}` for `RealOnly`, `{1}` for `None`.
    /// A declaration: the host's amplitudes do not determine it.
    pub fn phase_group(&self) -> &'static [Zi] {
        match self.phase {
            PhaseKind::ComplexU1 => &[(1, 0), (0, 1), (-1, 0), (0, -1)],
            PhaseKind::RealOnly => &[(1, 0), (-1, 0)],
            PhaseKind::None => &[(1, 0)],
        }
    }

    /// `OB-U1`: some phase of the declared group other than `+1` and `-1` moves
    /// the host's amplitude vector while keeping every quadratic weight — a
    /// phase fiber beyond signs, computed on the amplitudes. Real amplitudes
    /// suffice under `ComplexU1` (`i` moves any nonzero vector); no amplitude,
    /// imaginary or not, gives the fiber under `RealOnly`.
    pub fn ob_u1_holds(&self) -> bool {
        let times = |u: Zi, (re, im): Zi| (u.0 * re - u.1 * im, u.0 * im + u.1 * re);
        let weight = |(re, im): Zi| re * re + im * im;
        self.phase_group().iter().any(|&u| {
            u != (1, 0)
                && u != (-1, 0)
                && self.amplitudes.iter().any(|&a| times(u, a) != a)
                && self
                    .amplitudes
                    .iter()
                    .all(|&a| weight(times(u, a)) == weight(a))
        })
    }

    /// Born–Gleason quadratic selection.
    pub fn born_gleason_holds(&self) -> bool {
        if self.born != BornKind::Quadratic {
            return false;
        }
        if self.amplitudes.is_empty() {
            return false;
        }
        // Quadratic mass sum proxy Σ(re²+im²) > 0.
        let mass: i64 = self
            .amplitudes
            .iter()
            .map(|&(re, im)| re * re + im * im)
            .sum();
        mass > 0
    }

    /// Instrument / Lüders update: update flag + projector algebra.
    ///
    /// Intentionally **not** gated on full spectral reconstruction of `matrix_2x2`,
    /// so Spectral and Instruments can fail independently (separate countermodel rows).
    pub fn instruments_hold(&self) -> bool {
        if !self.has_instrument_update {
            return false;
        }
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        let sum_ok = p0[0] + p1[0] == 1 && p0[1] + p1[1] == 1;
        let orth_ok = p0[0] * p1[0] == 0 && p0[1] * p1[1] == 0;
        let idemp_ok = (p0[0] == 0 || p0[0] == 1)
            && (p0[1] == 0 || p0[1] == 1)
            && (p1[0] == 0 || p1[0] == 1)
            && (p1[1] == 0 || p1[1] == 1);
        sum_ok && orth_ok && idemp_ok
    }

    /// `OB-NONCOMM`: the host carries two observables that are symmetric on the
    /// same carrier and do NOT commute.
    ///
    /// Both conjuncts are load-bearing. Symmetry alone is not an observable
    /// algebra, and a non-commuting pair of non-observables witnesses nothing:
    /// dropping either check makes a host with a commuting pair, or with
    /// non-symmetric matrices, wrongly admit the slot.
    pub fn noncommuting_holds(&self) -> bool {
        let [a, b] = self.observables;
        let symmetric = |m: [[i64; 2]; 2]| m[0][1] == m[1][0];
        if !symmetric(a) || !symmetric(b) {
            return false;
        }
        // AB - BA, computed entrywise; nonzero somewhere == non-commuting.
        let mut differs = false;
        for i in 0..2 {
            for j in 0..2 {
                let ab: i64 = (0..2).map(|k| a[i][k] * b[k][j]).sum();
                let ba: i64 = (0..2).map(|k| b[i][k] * a[k][j]).sum();
                if ab != ba {
                    differs = true;
                }
            }
        }
        differs
    }

    /// Evaluate whether this host admits a given import slot (data-derived).
    pub fn admits(&self, slot: ImportSlot) -> bool {
        match slot {
            ImportSlot::Spectral => self.spectral_reconstructs(),
            ImportSlot::Monoidal => self.monoidal_holds(),
            ImportSlot::LocalTomography => self.local_tomography_holds(),
            ImportSlot::ObU1 => self.ob_u1_holds(),
            ImportSlot::BornGleason => self.born_gleason_holds(),
            ImportSlot::Instruments => self.instruments_hold(),
            ImportSlot::NonCommuting => self.noncommuting_holds(),
        }
    }

    /// True iff the host fails `drop` and admits every other enumerated slot.
    pub fn fails_exactly(&self, drop: ImportSlot) -> bool {
        if self.admits(drop) {
            return false;
        }
        ImportSlot::ALL
            .iter()
            .filter(|&&s| s != drop)
            .all(|&s| self.admits(s))
    }
}

// ---------------------------------------------------------------------------
// Concrete countermodels (one per slot; OB-U1 ⊥ LocalTomography)
// ---------------------------------------------------------------------------

fn herm_diag_host(
    id: &'static str,
    drop_note: &'static str,
    evals: [i64; 2],
    composition: CompositionKind,
    phase: PhaseKind,
    local_a: usize,
    local_b: usize,
    joint: usize,
    born: BornKind,
    instrument: bool,
    amplitudes: Vec<Zi>,
) -> FiniteImportHost {
    // Diagonal Hermitian: diag(λ0, λ1); projectors |0⟩⟨0|, |1⟩⟨1|.
    FiniteImportHost {
        id,
        drop_note,
        matrix_2x2: [[(evals[0], 0), (0, 0)], [(0, 0), (evals[1], 0)]],
        dim_a: 2,
        dim_b: 2,
        composition,
        phase,
        local_param_a: local_a,
        local_param_b: local_b,
        joint_param: joint,
        born,
        has_instrument_update: instrument,
        amplitudes,
        eigenvalues: evals,
        projectors_diag: [[1, 0], [0, 1]],
        // Cycle-7 separating pair: X and Z, symmetric on the
        // same carrier, XZ != ZX. Every host that is not the
        // OB-NONCOMM countermodel must ADMIT the slot, or it
        // would fail two slots and break its own fails_exactly.
        observables: [[[0, 1], [1, 0]], [[1, 0], [0, -1]]],
    }
}

/// Countermodel: Spectral fails (non-Hermitian Jordan block); other slots hold.
///
/// Instruments stay independent of spectral reconstruction: they only need the
/// Lüders update flag + projector algebra (see `instruments_hold`).
pub fn countermodel_drop_spectral() -> FiniteImportHost {
    FiniteImportHost {
        id: "cm_drop_spectral",
        drop_note: "Non-Hermitian nilpotent Jordan block is not unitarily diagonalizable; spectral reconstruction fails.",
        matrix_2x2: [[(0, 0), (1, 0)], [(0, 0), (0, 0)]],
        dim_a: 2,
        dim_b: 2,
        composition: CompositionKind::Tensor,
        phase: PhaseKind::ComplexU1,
        // Complex unnormalized density params: d^2 = 4 per qubit factor; joint 16.
        local_param_a: 4,
        local_param_b: 4,
        joint_param: 16,
        born: BornKind::Quadratic,
        has_instrument_update: true,
        amplitudes: vec![(1, 1), (0, 0)],
        eigenvalues: [0, 0],
        projectors_diag: [[1, 0], [0, 1]],
        // Cycle-7 separating pair: X and Z, symmetric on the
        // same carrier, XZ != ZX. Every host that is not the
        // OB-NONCOMM countermodel must ADMIT the slot, or it
        // would fail two slots and break its own fails_exactly.
        observables: [[[0, 1], [1, 0]], [[1, 0], [0, -1]]],
    }
}

/// Countermodel: Monoidal fails (direct-sum composition only; dims 2⊕3).
pub fn countermodel_drop_monoidal() -> FiniteImportHost {
    let mut h = herm_diag_host(
        "cm_drop_monoidal",
        "Composition is direct sum (dim 2+3=5), not tensor (dim 2·3=6); monoidal tensor import absent.",
        [1, -1],
        CompositionKind::DirectSum,
        PhaseKind::ComplexU1,
        4,
        9, // dim_b=3 → d^2=9 for a 3-level complex factor toy param
        36,
        BornKind::Quadratic,
        true,
        vec![(1, 0), (0, 1)],
    );
    h.dim_a = 2;
    h.dim_b = 3;
    // Fix LT identity for declared params: 4*9=36 holds independently of composition kind.
    h
}

/// Countermodel: LocalTomography fails; **OB-U1 still holds** (phase-without-LT).
///
/// Complex phase fiber on single-system amplitudes, but composite param identity
/// fails: \(4\cdot 4 \neq 15\) (outside-registry joint restriction).
pub fn countermodel_drop_local_tomography() -> FiniteImportHost {
    herm_diag_host(
        "cm_drop_local_tomography",
        "Complex U(1) phase present, but joint param count 15 ≠ 4·4=16 (LT identity fails).",
        [1, 0],
        CompositionKind::Tensor,
        PhaseKind::ComplexU1,
        4,
        4,
        15, // breaks LT; OB-U1 still true via ComplexU1 + imag amp
        BornKind::Quadratic,
        true,
        vec![(1, 1), (0, 0)],
    )
}

/// Countermodel: OB-U1 fails; **LocalTomography still holds** (LT-without-phase).
///
/// Real amplitudes only; classical / real param identity \(2\cdot 2 = 4\).
pub fn countermodel_drop_ob_u1() -> FiniteImportHost {
    herm_diag_host(
        "cm_drop_ob_u1",
        "Real amplitudes only (RealOnly); no complex U(1) phase carrier. LT identity 2·2=4 holds.",
        [1, -1],
        CompositionKind::Tensor,
        PhaseKind::RealOnly,
        2,
        2,
        4,
        BornKind::Quadratic,
        true,
        vec![(1, 0), (1, 0)], // real nonzero; no imag
    )
}

/// Countermodel: BornGleason fails (linear frame function, not quadratic).
pub fn countermodel_drop_born_gleason() -> FiniteImportHost {
    herm_diag_host(
        "cm_drop_born_gleason",
        "Probability selection is linear in |c| (not quadratic Born); Gleason uniqueness absent.",
        [1, 0],
        CompositionKind::Tensor,
        PhaseKind::ComplexU1,
        4,
        4,
        16,
        BornKind::Linear,
        true,
        vec![(1, 0), (0, 1)],
    )
}

/// Countermodel: Instruments fail (readout / projectors only; no Lüders update).
pub fn countermodel_drop_instruments() -> FiniteImportHost {
    herm_diag_host(
        "cm_drop_instruments",
        "Spectral projectors exist for readout, but no Lüders / instrument state-update map.",
        [1, -1],
        CompositionKind::Tensor,
        PhaseKind::ComplexU1,
        4,
        4,
        16,
        BornKind::Quadratic,
        false, // no instrument update
        vec![(0, 1), (1, 0)],
    )
}

/// Countermodel: `OB-NONCOMM` fails — the observable algebra is COMMUTATIVE.
///
/// Everything else is the fully-admitting configuration, so this host isolates
/// exactly one slot. The observables are `Z` and `2Z`: both symmetric, both on
/// the same carrier, and they commute. That is a classical (simultaneously
/// diagonalizable) observable algebra — a finite host can have spectral
/// calculus, tensor composition, local tomography, a U(1) phase, Born and
/// Lüders, and still have nothing non-commuting in it.
pub fn countermodel_drop_noncommuting() -> FiniteImportHost {
    let mut h = herm_diag_host(
        "cm_drop_noncommuting",
        "Observable algebra is commutative: Z and 2Z are symmetric on the same          carrier but ZZ' = Z'Z, so no non-commuting pair exists.",
        [1, -1],
        CompositionKind::Tensor,
        PhaseKind::ComplexU1,
        4,
        4,
        16,
        BornKind::Quadratic,
        true,
        vec![(0, 1), (1, 0)],
    );
    h.observables = [[[1, 0], [0, -1]], [[2, 0], [0, -2]]];
    h
}

/// All independence countermodels: one concrete host per slot, in `ImportSlot::ALL` order.
pub fn independence_countermodels() -> [(ImportSlot, FiniteImportHost); 7] {
    [
        (ImportSlot::Spectral, countermodel_drop_spectral()),
        (ImportSlot::Monoidal, countermodel_drop_monoidal()),
        (
            ImportSlot::LocalTomography,
            countermodel_drop_local_tomography(),
        ),
        (ImportSlot::ObU1, countermodel_drop_ob_u1()),
        (ImportSlot::BornGleason, countermodel_drop_born_gleason()),
        (ImportSlot::Instruments, countermodel_drop_instruments()),
        (ImportSlot::NonCommuting, countermodel_drop_noncommuting()),
    ]
}

// ---------------------------------------------------------------------------
// Target 14 — ImportBundle, witnesses, build_downstream
// ---------------------------------------------------------------------------

/// Witness that a finite spectral calculus is imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SpectralWitness {
    /// Hermitian diagonal matrix entries (real parts of diagonal).
    pub eigenvalues: [i64; 2],
    /// Diagonal projectors \(P_0,P_1\).
    pub projectors_diag: [[i64; 2]; 2],
}

impl SpectralWitness {
    /// Standard computational-basis spectral witness for diag(λ0, λ1).
    pub fn computational(eigenvalues: [i64; 2]) -> Self {
        Self {
            eigenvalues,
            projectors_diag: [[1, 0], [0, 1]],
        }
    }

    /// Validate projector algebra + reconstruction of diag(λ).
    pub fn validates(&self) -> bool {
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        if p0[0] + p1[0] != 1 || p0[1] + p1[1] != 1 {
            return false;
        }
        if p0[0] * p1[0] != 0 || p0[1] * p1[1] != 0 {
            return false;
        }
        let r0 = self.eigenvalues[0] * p0[0] + self.eigenvalues[1] * p1[0];
        let r1 = self.eigenvalues[0] * p0[1] + self.eigenvalues[1] * p1[1];
        r0 == self.eigenvalues[0] && r1 == self.eigenvalues[1]
    }
}

/// Witness that monoidal tensor composition is imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MonoidalWitness {
    pub dim_a: usize,
    pub dim_b: usize,
}

impl MonoidalWitness {
    pub fn validates(&self) -> bool {
        self.dim_a >= 1
            && self.dim_b >= 1
            && self.dim_a.saturating_mul(self.dim_b) == self.dim_a * self.dim_b
            && self.dim_a * self.dim_b >= 1
    }

    pub fn joint_dim(&self) -> usize {
        self.dim_a.saturating_mul(self.dim_b)
    }
}

/// Witness that composite local tomography is imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalTomographyWitness {
    pub local_param_a: usize,
    pub local_param_b: usize,
    pub joint_param: usize,
}

impl LocalTomographyWitness {
    pub fn validates(&self) -> bool {
        self.local_param_a > 0
            && self.local_param_b > 0
            && self.local_param_a.saturating_mul(self.local_param_b) == self.joint_param
    }
}

/// Witness that the complex \(U(1)\) phase carrier (`OB-U1`) is imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObU1Witness {
    /// Sample amplitudes with at least one imaginary component.
    pub amplitudes: Vec<Zi>,
}

impl ObU1Witness {
    pub fn validates(&self) -> bool {
        self.amplitudes.iter().any(|&(re, im)| re != 0 || im != 0)
            && self.amplitudes.iter().any(|&(_, im)| im != 0)
    }
}

/// Witness that Born–Gleason quadratic selection is imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BornGleasonWitness {
    pub amplitudes: Vec<Zi>,
}

impl BornGleasonWitness {
    pub fn validates(&self) -> bool {
        let mass: i64 = self
            .amplitudes
            .iter()
            .map(|&(re, im)| re * re + im * im)
            .sum();
        mass > 0
    }

    /// Quadratic Born masses \(\lvert c_i\rvert^2\).
    pub fn masses(&self) -> Vec<i64> {
        self.amplitudes
            .iter()
            .map(|&(re, im)| re * re + im * im)
            .collect()
    }
}

/// Witness that an instrument / Lüders update is imported.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstrumentsWitness {
    /// Diagonal projectors for a two-outcome Lüders update.
    pub projectors_diag: [[i64; 2]; 2],
    /// Prior diagonal populations (classical shadow).
    pub prior_diag: [i64; 2],
}

impl InstrumentsWitness {
    pub fn validates(&self) -> bool {
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        p0[0] + p1[0] == 1
            && p0[1] + p1[1] == 1
            && p0[0] * p1[0] == 0
            && p0[1] * p1[1] == 0
            && self.prior_diag.iter().all(|&x| x >= 0)
            && self.prior_diag[0] + self.prior_diag[1] > 0
    }

    /// Lüders / Bayesian sector update for outcome 0 or 1.
    pub fn luders_update(&self, outcome: usize) -> Option<[i64; 2]> {
        if !self.validates() || outcome > 1 {
            return None;
        }
        let p = self.projectors_diag[outcome];
        Some([self.prior_diag[0] * p[0], self.prior_diag[1] * p[1]])
    }
}

/// Witness that a NON-COMMUTING observable algebra is imported (`OB-NONCOMM`).
///
/// Added 2026-08-04 (R2-C9) so the slot is modelled on BOTH surfaces: as an
/// independence datum on `FiniteImportHost`, and as bundle evidence here. A slot
/// present in one and absent from the other is exactly the `DeclaredNotModelled`
/// half-state this cycle exists to remove.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NonCommutingWitness {
    /// Two real-symmetric 2x2 integer observables on the same carrier.
    pub observables: [[[i64; 2]; 2]; 2],
}

impl NonCommutingWitness {
    /// The cycle-7 separating pair: `X = [[0,1],[1,0]]`, `Z = [[1,0],[0,-1]]`.
    pub fn pauli_xz() -> Self {
        Self {
            observables: [[[0, 1], [1, 0]], [[1, 0], [0, -1]]],
        }
    }

    /// Symmetric on the same carrier AND non-commuting. Both conjuncts are
    /// load-bearing; see `FiniteImportHost::noncommuting_holds`.
    pub fn validates(&self) -> bool {
        let [a, b] = self.observables;
        let symmetric = |m: [[i64; 2]; 2]| m[0][1] == m[1][0];
        if !symmetric(a) || !symmetric(b) {
            return false;
        }
        (0..2).any(|i| {
            (0..2).any(|j| {
                let ab: i64 = (0..2).map(|k| a[i][k] * b[k][j]).sum();
                let ba: i64 = (0..2).map(|k| b[i][k] * a[k][j]).sum();
                ab != ba
            })
        })
    }
}

/// Declared import bundle: each slot is present only with a typed witness object.
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct ImportBundle {
    pub spectral: Option<SpectralWitness>,
    pub monoidal: Option<MonoidalWitness>,
    pub local_tomography: Option<LocalTomographyWitness>,
    pub ob_u1: Option<ObU1Witness>,
    pub born_gleason: Option<BornGleasonWitness>,
    pub instruments: Option<InstrumentsWitness>,
    pub noncommuting: Option<NonCommutingWitness>,
}

impl ImportBundle {
    /// Empty bundle (all imports absent).
    pub fn empty() -> Self {
        Self::default()
    }

    /// Full finite TOY bundle with every witness present and valid.
    pub fn full_toy() -> Self {
        Self {
            spectral: Some(SpectralWitness::computational([1, -1])),
            monoidal: Some(MonoidalWitness { dim_a: 2, dim_b: 2 }),
            local_tomography: Some(LocalTomographyWitness {
                local_param_a: 4,
                local_param_b: 4,
                joint_param: 16,
            }),
            ob_u1: Some(ObU1Witness {
                amplitudes: vec![(1, 1), (0, 0)],
            }),
            born_gleason: Some(BornGleasonWitness {
                amplitudes: vec![(1, 0), (0, 1)],
            }),
            instruments: Some(InstrumentsWitness {
                projectors_diag: [[1, 0], [0, 1]],
                prior_diag: [3, 1],
            }),
            noncommuting: Some(NonCommutingWitness::pauli_xz()),
        }
    }

    /// Whether a slot has a **present and validating** witness.
    pub fn has_valid(&self, slot: ImportSlot) -> bool {
        match slot {
            ImportSlot::Spectral => self.spectral.as_ref().is_some_and(|w| w.validates()),
            ImportSlot::Monoidal => self.monoidal.as_ref().is_some_and(|w| w.validates()),
            ImportSlot::LocalTomography => self
                .local_tomography
                .as_ref()
                .is_some_and(|w| w.validates()),
            ImportSlot::ObU1 => self.ob_u1.as_ref().is_some_and(|w| w.validates()),
            ImportSlot::BornGleason => self.born_gleason.as_ref().is_some_and(|w| w.validates()),
            ImportSlot::Instruments => self.instruments.as_ref().is_some_and(|w| w.validates()),
            ImportSlot::NonCommuting => self.noncommuting.as_ref().is_some_and(|w| w.validates()),
        }
    }
}

/// Missing (or invalid) import required by a downstream constructor.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MissingImport {
    Spectral,
    Monoidal,
    LocalTomography,
    ObU1,
    BornGleason,
    Instruments,
}

impl MissingImport {
    pub fn slot(self) -> ImportSlot {
        match self {
            MissingImport::Spectral => ImportSlot::Spectral,
            MissingImport::Monoidal => ImportSlot::Monoidal,
            MissingImport::LocalTomography => ImportSlot::LocalTomography,
            MissingImport::ObU1 => ImportSlot::ObU1,
            MissingImport::BornGleason => ImportSlot::BornGleason,
            MissingImport::Instruments => ImportSlot::Instruments,
        }
    }
}

/// Finite spectral calculus built from a spectral witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SpectralCalculus {
    pub eigenvalues: [i64; 2],
    pub reconstructed_diag: [i64; 2],
}

/// Monoidal tensor structure built from a monoidal witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MonoidalTensor {
    pub dim_a: usize,
    pub dim_b: usize,
    pub joint_dim: usize,
}

/// Tomography protocol built from a local-tomography witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TomographyProtocol {
    pub local_param_a: usize,
    pub local_param_b: usize,
    pub joint_param: usize,
    /// True when the witness identity holds (always for a successful build).
    pub identity_holds: bool,
}

/// Phase carrier built from an OB-U1 witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PhaseCarrier {
    pub amplitudes: Vec<Zi>,
    pub has_nontrivial_u1: bool,
}

/// Born rule built from a Born–Gleason witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BornRule {
    pub masses: Vec<i64>,
    pub total_mass: i64,
}

/// Instrument map built from an instruments witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstrumentMap {
    pub prior_diag: [i64; 2],
    pub post_outcome_0: [i64; 2],
    pub post_outcome_1: [i64; 2],
}

/// Downstream structures constructible only when the required imports are present.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DownstreamStructures {
    pub spectral: SpectralCalculus,
    pub monoidal: MonoidalTensor,
    pub tomography: TomographyProtocol,
    pub phase_carrier: PhaseCarrier,
    pub born_rule: BornRule,
    pub instrument_map: InstrumentMap,
}

fn require_spectral(bundle: &ImportBundle) -> Result<&SpectralWitness, MissingImport> {
    match &bundle.spectral {
        Some(w) if w.validates() => Ok(w),
        _ => Err(MissingImport::Spectral),
    }
}

fn require_monoidal(bundle: &ImportBundle) -> Result<&MonoidalWitness, MissingImport> {
    match &bundle.monoidal {
        Some(w) if w.validates() => Ok(w),
        _ => Err(MissingImport::Monoidal),
    }
}

fn require_local_tomography(
    bundle: &ImportBundle,
) -> Result<&LocalTomographyWitness, MissingImport> {
    match &bundle.local_tomography {
        Some(w) if w.validates() => Ok(w),
        _ => Err(MissingImport::LocalTomography),
    }
}

fn require_ob_u1(bundle: &ImportBundle) -> Result<&ObU1Witness, MissingImport> {
    match &bundle.ob_u1 {
        Some(w) if w.validates() => Ok(w),
        _ => Err(MissingImport::ObU1),
    }
}

fn require_born_gleason(bundle: &ImportBundle) -> Result<&BornGleasonWitness, MissingImport> {
    match &bundle.born_gleason {
        Some(w) if w.validates() => Ok(w),
        _ => Err(MissingImport::BornGleason),
    }
}

fn require_instruments(bundle: &ImportBundle) -> Result<&InstrumentsWitness, MissingImport> {
    match &bundle.instruments {
        Some(w) if w.validates() => Ok(w),
        _ => Err(MissingImport::Instruments),
    }
}

/// Build tomography **only** from a local-tomography witness object.
///
/// Cannot succeed from Boolean “pathway covered” flags alone.
pub fn build_tomography(bundle: &ImportBundle) -> Result<TomographyProtocol, MissingImport> {
    let w = require_local_tomography(bundle)?;
    Ok(TomographyProtocol {
        local_param_a: w.local_param_a,
        local_param_b: w.local_param_b,
        joint_param: w.joint_param,
        identity_holds: true,
    })
}

/// Build the phase carrier **only** from an OB-U1 witness object.
pub fn build_phase_carrier(bundle: &ImportBundle) -> Result<PhaseCarrier, MissingImport> {
    let w = require_ob_u1(bundle)?;
    Ok(PhaseCarrier {
        amplitudes: w.amplitudes.clone(),
        has_nontrivial_u1: true,
    })
}

/// Construct all downstream structures from the declared import bundle.
///
/// Each field is built from the corresponding witness data (not from flags).
/// Returns `Err(MissingImport::*)` for the first missing/invalid required import.
pub fn build_downstream(bundle: &ImportBundle) -> Result<DownstreamStructures, MissingImport> {
    let sw = require_spectral(bundle)?;
    let mw = require_monoidal(bundle)?;
    let ltw = require_local_tomography(bundle)?;
    let uw = require_ob_u1(bundle)?;
    let bw = require_born_gleason(bundle)?;
    let iw = require_instruments(bundle)?;

    let spectral = SpectralCalculus {
        eigenvalues: sw.eigenvalues,
        reconstructed_diag: [
            sw.eigenvalues[0] * sw.projectors_diag[0][0]
                + sw.eigenvalues[1] * sw.projectors_diag[1][0],
            sw.eigenvalues[0] * sw.projectors_diag[0][1]
                + sw.eigenvalues[1] * sw.projectors_diag[1][1],
        ],
    };

    let monoidal = MonoidalTensor {
        dim_a: mw.dim_a,
        dim_b: mw.dim_b,
        joint_dim: mw.joint_dim(),
    };

    let tomography = TomographyProtocol {
        local_param_a: ltw.local_param_a,
        local_param_b: ltw.local_param_b,
        joint_param: ltw.joint_param,
        identity_holds: true,
    };

    let phase_carrier = PhaseCarrier {
        amplitudes: uw.amplitudes.clone(),
        has_nontrivial_u1: true,
    };

    let masses = bw.masses();
    let total_mass: i64 = masses.iter().sum();
    let born_rule = BornRule { masses, total_mass };

    let post0 = iw.luders_update(0).ok_or(MissingImport::Instruments)?;
    let post1 = iw.luders_update(1).ok_or(MissingImport::Instruments)?;
    let instrument_map = InstrumentMap {
        prior_diag: iw.prior_diag,
        post_outcome_0: post0,
        post_outcome_1: post1,
    };

    Ok(DownstreamStructures {
        spectral,
        monoidal,
        tomography,
        phase_carrier,
        born_rule,
        instrument_map,
    })
}

/// Authority fence (never mints PROVED / GlobalGreen).
pub fn authority_fence() -> &'static str {
    AUTHORITY_FENCE
}

// ---------------------------------------------------------------------------
// Unit tests (crate-local)
// ---------------------------------------------------------------------------

// ═════════════════════════════════════════════════════════════════════════════
// W6.19 — the thirteen frozen slots, entailment, and a basis-relative N
// ═════════════════════════════════════════════════════════════════════════════
//
// `ImportSlot` above models SIX slots and gives each a drop-one countermodel.
// The Wave-0 freeze (`finite_l1_qm_freeze_20260730.md` v0.1, section 4) names
// **thirteen**. Seven were absent from this module entirely — and an absent slot
// reads as "nothing exists here", which is a stronger and falser statement than
// "a toy exists" or "this one is entailed".
//
// This section makes every frozen slot carry explicit evidence, and reports a
// **basis-relative** cardinality instead of a bare `N`.

/// Every `OB-*` slot named by the Wave-0 freeze v0.1 section 4.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum FrozenSlotId {
    ObU1,
    ObBorn,
    ObSpectral,
    ObInstrument,
    ObCompose,
    ObConvex,
    ObNoncomm,
    ObUnitary,
    ObHerm,
    ObL2Readout,
    ObCoherence,
    ObStats,
    ObClone,
}

impl FrozenSlotId {
    /// The freeze's enumeration. Thirteen, not six.
    pub const ALL: [FrozenSlotId; 13] = [
        FrozenSlotId::ObU1,
        FrozenSlotId::ObBorn,
        FrozenSlotId::ObSpectral,
        FrozenSlotId::ObInstrument,
        FrozenSlotId::ObCompose,
        FrozenSlotId::ObConvex,
        FrozenSlotId::ObNoncomm,
        FrozenSlotId::ObUnitary,
        FrozenSlotId::ObHerm,
        FrozenSlotId::ObL2Readout,
        FrozenSlotId::ObCoherence,
        FrozenSlotId::ObStats,
        FrozenSlotId::ObClone,
    ];

    pub fn id(self) -> &'static str {
        match self {
            FrozenSlotId::ObU1 => "OB-U1",
            FrozenSlotId::ObBorn => "OB-BORN",
            FrozenSlotId::ObSpectral => "OB-SPECTRAL",
            FrozenSlotId::ObInstrument => "OB-INSTRUMENT",
            FrozenSlotId::ObCompose => "OB-COMPOSE",
            FrozenSlotId::ObConvex => "OB-CONVEX",
            FrozenSlotId::ObNoncomm => "OB-NONCOMM",
            FrozenSlotId::ObUnitary => "OB-UNITARY",
            FrozenSlotId::ObHerm => "OB-HERM",
            FrozenSlotId::ObL2Readout => "OB-L2-READOUT",
            FrozenSlotId::ObCoherence => "OB-COHERENCE",
            FrozenSlotId::ObStats => "OB-STATS",
            FrozenSlotId::ObClone => "OB-CLONE",
        }
    }
}

/// Which carrier class a host's declared parameter counts actually describe.
///
/// **Computed** from `(dim_a, dim_b, local_param_a, local_param_b,
/// joint_param)` against the canonical counts — never declared by hand. It
/// exists because independence evidence is only meaningful *relative to a
/// carrier class*: a host carrying classical simplex counts witnesses nothing
/// about real-quantum carriers, and a registry that cannot say so overstates
/// its own scope.
///
/// At `dim_a = dim_b = 1` all three families coincide at `(1, 1, 1)` and the
/// classical reading wins; that dimension is degenerate and separates nothing.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CarrierClass {
    /// Simplex counts: local `d`, joint `d_a * d_b`.
    ClassicalSimplex,
    /// Real-symmetric counts: local `d(d+1)/2`, joint `D(D+1)/2` for `D = d_a d_b`.
    RealQuantum,
    /// Complex Hermitian counts: local `d^2`, joint `D^2`.
    ComplexQuantum,
    /// The declared counts match none of the recognised carrier classes.
    Unrecognised,
}

impl CarrierClass {
    pub fn id(self) -> &'static str {
        match self {
            CarrierClass::ClassicalSimplex => "classical-simplex",
            CarrierClass::RealQuantum => "real-quantum",
            CarrierClass::ComplexQuantum => "complex-quantum",
            CarrierClass::Unrecognised => "unrecognised",
        }
    }
}

/// What the drop-one engine can actually say about a frozen slot.
///
/// The three cases are deliberately distinct. Collapsing `EntailedBy` into
/// `DeclaredNotModelled` would hide a **proved** structural fact; treating
/// `DeclaredNotModelled` as a failure would invent evidence that does not exist.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SlotEvidence {
    /// A concrete host fails exactly this slot and admits every other modelled
    /// slot: drop-one independent, with the witness named **and scoped**.
    ///
    /// `carrier_class` is the class the witness's own parameter counts put it
    /// in. Independence established by a `ClassicalSimplex` host is evidence
    /// about classical carriers only; a consumer must not read it as
    /// independence over quantum carriers.
    IndependentWithCountermodel {
        host_id: &'static str,
        carrier_class: CarrierClass,
    },
    /// **Provably not drop-one independent.** Another slot entails it, so no host
    /// can fail this one alone — it cannot sit in an independence basis alongside
    /// its entailer.
    EntailedBy { by: FrozenSlotId, why: &'static str },
    /// Named in the freeze; no field of [`FiniteImportHost`] models it yet.
    /// Explicitly *not* a claim that the slot is empty or derivable.
    DeclaredNotModelled { needs: &'static str },
}

/// Evidence for each frozen slot, as of cycle 9.
///
/// The `OB-SPECTRAL ⟹ OB-HERM` entailment is not an opinion:
/// [`FiniteImportHost::spectral_reconstructs`] returns `false` whenever
/// [`FiniteImportHost::is_hermitian`] is `false`, so a host that drops `OB-HERM`
/// necessarily drops `OB-SPECTRAL` too.
pub fn frozen_slot_evidence(slot: FrozenSlotId) -> SlotEvidence {
    match slot {
        FrozenSlotId::ObSpectral => independent_with("cm_drop_spectral"),
        FrozenSlotId::ObCompose => independent_with("cm_drop_monoidal"),
        FrozenSlotId::ObU1 => independent_with("cm_drop_ob_u1"),
        FrozenSlotId::ObBorn => independent_with("cm_drop_born_gleason"),
        FrozenSlotId::ObInstrument => independent_with("cm_drop_instruments"),
        FrozenSlotId::ObHerm => SlotEvidence::EntailedBy {
            by: FrozenSlotId::ObSpectral,
            why: "spectral_reconstructs() returns false unless is_hermitian(); no host \
                  can fail OB-HERM while admitting OB-SPECTRAL, so the two cannot both \
                  sit in a drop-one independence basis",
        },
        // R2-C9 (2026-08-04): promoted from DeclaredNotModelled. The blocker was
        // never the mathematics — round 1 already had the separating pair
        // X=[[0,1],[1,0]], Z=[[1,0],[0,-1]] in hermitian_spectral (cycle 7,
        // axiom A17). It was that FiniteImportHost carried no observable-algebra
        // field, so nothing could be evaluated. It now has `observables`, and the
        // slot has a predicate, a bundle witness, and a drop-one countermodel
        // whose independence is MEASURED by `fails_exactly`, not asserted.
        FrozenSlotId::ObNoncomm => independent_with("cm_drop_noncommuting"),
        FrozenSlotId::ObConvex => SlotEvidence::DeclaredNotModelled {
            needs: "a state-space field distinguishing a simplex from a general convex body",
        },
        FrozenSlotId::ObUnitary => SlotEvidence::DeclaredNotModelled {
            needs: "a dynamics field separating unitary evolution from the stochastic shadow",
        },
        FrozenSlotId::ObL2Readout => SlotEvidence::DeclaredNotModelled {
            needs: "an l2-readout field split from OB-BORN; the freeze says merge or split \
                    ONLY BY THEOREM, and no such theorem exists yet",
        },
        FrozenSlotId::ObCoherence => SlotEvidence::DeclaredNotModelled {
            needs: "off-diagonal / Kraus-agreement dynamics; the freeze already expects \
                    underdetermination here",
        },
        FrozenSlotId::ObStats => SlotEvidence::DeclaredNotModelled {
            needs: "an exchange-statistics field (multi-particle carrier)",
        },
        FrozenSlotId::ObClone => SlotEvidence::DeclaredNotModelled {
            needs: "a cloning-map field; may be derivable rather than imported",
        },
    }
}

/// Build scoped independence evidence by **looking the host up and computing**
/// its carrier class, rather than declaring a scope alongside the id.
///
/// An id with no registered host yields `Unrecognised`, which is the honest
/// answer: nothing was measured.
fn independent_with(host_id: &'static str) -> SlotEvidence {
    let carrier_class = independence_countermodels()
        .iter()
        .map(|(_, host)| host)
        .find(|host| host.id == host_id)
        .map(|host| host.carrier_class())
        .unwrap_or(CarrierClass::Unrecognised);
    SlotEvidence::IndependentWithCountermodel {
        host_id,
        carrier_class,
    }
}

/// Slots with a verified drop-one countermodel.
///
/// **Scope warning.** This returns slots with *some* countermodel, regardless of
/// its carrier class. Use [`independent_slots_over`] when the question is
/// independence over a particular class of carrier.
pub fn independent_slots() -> Vec<FrozenSlotId> {
    FrozenSlotId::ALL
        .into_iter()
        .filter(|&s| {
            matches!(
                frozen_slot_evidence(s),
                SlotEvidence::IndependentWithCountermodel { .. }
            )
        })
        .collect()
}

/// Slots whose drop-one countermodel lies in the given carrier class.
///
/// This is the query a consumer actually needs: "is `OB-U1` independent *over
/// quantum carriers*?" is a different question from "does some host drop it?",
/// and before the scope was recorded the registry could not tell them apart.
pub fn independent_slots_over(carrier_class: CarrierClass) -> Vec<FrozenSlotId> {
    FrozenSlotId::ALL
        .into_iter()
        .filter(|&s| {
            matches!(
                frozen_slot_evidence(s),
                SlotEvidence::IndependentWithCountermodel { carrier_class: c, .. }
                    if c == carrier_class
            )
        })
        .collect()
}

/// A named import basis, so a bare number is never quoted without its referent.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ImportBasis {
    /// Every `OB-*` id named by the Wave-0 freeze v0.1 section 4.
    FrozenDeclared,
    /// Slots this module models with a predicate over [`FiniteImportHost`].
    Modelled,
    /// Slots with a verified drop-one countermodel — the only reading of `N`
    /// that means "independent".
    DropOneIndependent,
    /// `Modelled` with the `LocalTomography` residue folded back under `OB-U1`,
    /// as the freeze's non-double-count caveat requires until a split is proved.
    ModelledLtNestedUnderU1,
}

/// **The canonical `N` is basis-relative.**
///
/// Five values circulate in the estate (3, 5, 7, 8, 9) with no reconciling
/// artifact. They are not competing answers to one question — they count
/// different things. Quoting `N` without naming its basis is the actual defect.
pub fn basis_cardinality(basis: ImportBasis) -> usize {
    match basis {
        ImportBasis::FrozenDeclared => FrozenSlotId::ALL.len(),
        ImportBasis::Modelled => ImportSlot::ALL.len(),
        ImportBasis::DropOneIndependent => independent_slots().len(),
        ImportBasis::ModelledLtNestedUnderU1 => ImportSlot::ALL.len() - 1,
    }
}

/// The freeze's own caveat, kept next to the code it constrains.
///
/// `OB-COMPOSE` row: the local-tomography / global-field-uniqueness residue stays
/// **nested under `OB-U1`** until a Wave-6 independence argument splits it, and
/// must not be double-counted under both ids.
///
/// This module *does* provide the two countermodels such a split needs
/// (`countermodel_drop_local_tomography` keeps `OB-U1`;
/// `countermodel_drop_ob_u1` keeps LT). But the Lean side records the pair as
/// **COUPLED** on the NamedLift registry, with `SPLIT-OUTSIDE-REGISTRY` still
/// OPEN. Rust and Lean therefore disagree, and the disagreement is recorded
/// rather than silently resolved in either direction.
pub const LT_U1_SPLIT_DISPUTED: &str =
    "LocalTomography vs OB-U1: the WITNESS is INVALIDATED for a real-quantum \
     reading; COUPLING on quantum carriers remains OPEN (narrowed 2026-08-05 \
     under review of PR #1894). What is established: `cm_drop_ob_u1` declares \
     parameter counts (2,2,4), which `FiniteImportHost::carrier_class()` \
     computes as CLASSICAL-SIMPLEX, and a classical composite has local \
     tomography trivially. The real-quantum counts at the same dimensions are \
     (3,3,10) (Sym(R^2)=3, Sym(R^4)=10) and 3*3 = 9 != 10, so under a \
     real-quantum reading the same host fails LocalTomography as well and is \
     therefore NOT a drop-one witness for OB-U1. What is NOT established: the \
     implication QuantumCarrier(H) AND NOT OB-U1(H) => NOT LT(H). That would \
     need a validated carrier-class invariant tying phase, state space, effect \
     space, observables, Born rule and composition together, or an exhaustion \
     over a precisely bounded licensed model universe. Substituting three count \
     fields by hand and observing two predicates fail invalidates ONE witness; \
     it does not quantify over hosts. The registry now records carrier scope \
     (see `CarrierClass`), so OB-U1 independence reads as CLASSICAL-SIMPLEX \
     scoped rather than unqualified. SPLIT-OUTSIDE-REGISTRY stays OPEN for the \
     classical carrier, where the split is real, and QUANTUM-CARRIER-COUPLING \
     is OPEN. Do not quote a split N for a quantum carrier, and do not quote \
     this as a coupling theorem. AuthorityEffect None.";

/// Slots whose *meaning* changed in cycles 6–8 and which must be re-priced
/// against the new statements rather than their earlier descriptions.
pub const REPRICED_BY_CYCLES_6_TO_8: [(&str, &str); 3] = [
    (
        "OB-BORN",
        "Cycle 6: routes through BornSelectionImport = GleasonAbsoluteDim3Plus OR \
         BuschPovmFrameAbsolute. Gleason is fenced to dim >= 3, so at the estate's \
         working dimension d=2 the Busch/POVM route is FORCED.",
    ),
    (
        "OB-SPECTRAL",
        "Cycle 7: reclassified [OPEN] -> [UNDERIVABLE over Q]. A rational Hermitian \
         matrix can have irrational eigenvalues at n=2, so this is a priced import \
         (an algebraic extension), not a pending algorithm.",
    ),
    (
        "OB-COMPOSE",
        "Cycle 4: local tomography restated as a spanning theorem; the real failure is \
         witnessed by Delta = J (x) J, generator of the skew-skew sector, with \
         deficiency C(m,2)*C(n,2).",
    ),
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fence_is_none() {
        assert!(authority_fence().contains("AuthorityEffect None"));
    }

    // --- W6.19: the thirteen frozen slots ----------------------------------

    /// The freeze names thirteen slots; this module modelled six, and models
    /// SEVEN since R2-C9 added `OB-NONCOMM`. The remaining six are not merely
    /// unproved — they are **absent**, which reads as "nothing exists".
    ///
    /// The frozen count stays 13. Modelling a slot does not create one.
    #[test]
    fn w619_frozen_registry_has_thirteen_slots() {
        assert_eq!(FrozenSlotId::ALL.len(), 13);
        assert_eq!(ImportSlot::ALL.len(), 7);
        let mut ids: Vec<&str> = FrozenSlotId::ALL.iter().map(|s| s.id()).collect();
        ids.sort_unstable();
        ids.dedup();
        assert_eq!(ids.len(), 13, "frozen slot ids must be distinct");
    }

    /// **No silent omissions.** Every frozen slot carries explicit evidence.
    #[test]
    fn w619_every_frozen_slot_has_explicit_evidence() {
        for s in FrozenSlotId::ALL {
            match frozen_slot_evidence(s) {
                SlotEvidence::IndependentWithCountermodel {
                    host_id,
                    carrier_class,
                } => {
                    assert!(!host_id.is_empty(), "{} names no host", s.id());
                    assert_ne!(
                        carrier_class,
                        CarrierClass::Unrecognised,
                        "{} names a host whose carrier class could not be computed",
                        s.id()
                    );
                }
                SlotEvidence::EntailedBy { why, .. } => {
                    assert!(!why.is_empty(), "{} gives no entailment reason", s.id())
                }
                SlotEvidence::DeclaredNotModelled { needs } => {
                    assert!(
                        !needs.is_empty(),
                        "{} says nothing about what it needs",
                        s.id()
                    )
                }
            }
        }
    }

    /// **The load-bearing negative result.** `spectral_reconstructs` returns false
    /// whenever `is_hermitian` is false, so dropping `OB-HERM` necessarily drops
    /// `OB-SPECTRAL`: no host fails `OB-HERM` alone. The frozen thirteen are
    /// therefore **not** a drop-one independence basis.
    /// Exhaustive sweep over 729 hosts establishing `spectral ⟹ hermitian`.
    ///
    /// An earlier version of this test only ranged over the six countermodels,
    /// where `spectral_reconstructs` is false for *other* reasons anyway. It
    /// survived deleting the `is_hermitian()` guard — i.e. it could not fail for
    /// its stated reason. This version varies both diagonal imaginary parts and
    /// both off-diagonals, and carries anti-vacuity counters so the sweep cannot
    /// pass by exercising only one side.
    #[test]
    fn w619_spectral_entails_hermiticity_exhaustively() {
        let base = countermodel_drop_instruments();
        let vals: [i64; 3] = [0, 1, -1];
        let (mut saw_spectral, mut saw_non_hermitian, mut checked) = (0usize, 0usize, 0usize);

        for a_re in vals {
            for a_im in vals {
                for d_re in vals {
                    for d_im in vals {
                        for b_re in vals {
                            for c_re in vals {
                                let mut h = base.clone();
                                h.matrix_2x2 =
                                    [[(a_re, a_im), (b_re, 0)], [(c_re, 0), (d_re, d_im)]];
                                h.eigenvalues = [a_re, d_re];
                                h.projectors_diag = [[1, 0], [0, 1]];
                                checked += 1;
                                let spec = h.spectral_reconstructs();
                                let herm = h.is_hermitian();
                                if spec {
                                    saw_spectral += 1;
                                }
                                if !herm {
                                    saw_non_hermitian += 1;
                                }
                                assert!(
                                    !spec || herm,
                                    "spectral without hermitian at {:?}",
                                    h.matrix_2x2
                                );
                            }
                        }
                    }
                }
            }
        }

        assert_eq!(checked, 729);
        assert!(saw_spectral > 0, "sweep never admitted spectral — vacuous");
        assert!(
            saw_non_hermitian > 0,
            "sweep contained no non-Hermitian host — vacuous"
        );

        assert!(matches!(
            frozen_slot_evidence(FrozenSlotId::ObHerm),
            SlotEvidence::EntailedBy {
                by: FrozenSlotId::ObSpectral,
                ..
            }
        ));
    }

    /// **Code finding.** The explicit `is_hermitian()` guard at the top of
    /// `spectral_reconstructs` is *redundant*: the later conditions already force
    /// Hermiticity (both off-diagonals zero and both diagonals real ⟹ Hermitian).
    ///
    /// So the entailment `OB-SPECTRAL ⟹ OB-HERM` is structural, not an artifact
    /// of one early return — which is a stronger statement than "there is a
    /// guard". Recorded rather than silently deleting the guard.
    #[test]
    fn w619_hermiticity_guard_is_redundant_entailment_is_structural() {
        let base = countermodel_drop_instruments();
        let vals: [i64; 3] = [0, 1, -1];
        for a_re in vals {
            for a_im in vals {
                for d_re in vals {
                    for d_im in vals {
                        let mut h = base.clone();
                        // zero off-diagonals; vary only the diagonal imaginary parts
                        h.matrix_2x2 = [[(a_re, a_im), (0, 0)], [(0, 0), (d_re, d_im)]];
                        h.eigenvalues = [a_re, d_re];
                        h.projectors_diag = [[1, 0], [0, 1]];
                        // With zero off-diagonals, Hermitian <=> both diagonals real.
                        assert_eq!(
                            h.is_hermitian(),
                            a_im == 0 && d_im == 0,
                            "hermiticity should reduce to real diagonals here"
                        );
                    }
                }
            }
        }
    }

    /// Hermiticity alone does **not** buy spectral decomposability — cycle 7's
    /// golden matrix `[[1,1],[1,0]]` is Hermitian and non-diagonal. The
    /// entailment runs one way only, so `OB-SPECTRAL` stays genuinely
    /// independent. Without this the entailment could be a collapse of both.
    #[test]
    fn w619_entailment_is_one_directional() {
        let mut h = countermodel_drop_spectral();
        h.matrix_2x2 = [[(1, 0), (1, 0)], [(1, 0), (0, 0)]];
        assert!(h.is_hermitian(), "golden witness must be Hermitian");
        assert!(
            !h.spectral_reconstructs(),
            "Hermitian must NOT imply spectral: that would collapse the slots"
        );
    }

    /// **`N` is basis-relative.** The five circulating values count different
    /// things; none of them is "the" answer.
    #[test]
    fn w619_canonical_n_is_basis_relative() {
        assert_eq!(basis_cardinality(ImportBasis::FrozenDeclared), 13);
        assert_eq!(basis_cardinality(ImportBasis::Modelled), 7);
        // R2-C9: OB-NONCOMM adds a verified drop-one countermodel, 5 -> 6.
        assert_eq!(basis_cardinality(ImportBasis::DropOneIndependent), 6);
        assert_eq!(basis_cardinality(ImportBasis::ModelledLtNestedUnderU1), 6);
        assert_ne!(
            basis_cardinality(ImportBasis::FrozenDeclared),
            basis_cardinality(ImportBasis::DropOneIndependent),
            "quoting the declared count as N is the defect"
        );
    }

    /// Each independent slot's named host really does fail exactly that slot.
    /// Guards the registry against naming a host that does not do what it claims.
    #[test]
    fn w619_named_hosts_actually_fail_exactly_their_slot() {
        let pairs: [(FrozenSlotId, ImportSlot); 5] = [
            (FrozenSlotId::ObSpectral, ImportSlot::Spectral),
            (FrozenSlotId::ObCompose, ImportSlot::Monoidal),
            (FrozenSlotId::ObU1, ImportSlot::ObU1),
            (FrozenSlotId::ObBorn, ImportSlot::BornGleason),
            (FrozenSlotId::ObInstrument, ImportSlot::Instruments),
        ];
        let models = independence_countermodels();
        for (frozen, modelled) in pairs {
            let SlotEvidence::IndependentWithCountermodel { host_id, .. } =
                frozen_slot_evidence(frozen)
            else {
                panic!("{} should be independent", frozen.id());
            };
            let host = models
                .iter()
                .map(|(_, h)| h)
                .find(|h| h.id == host_id)
                .unwrap_or_else(|| panic!("no host named {host_id}"));
            assert!(
                host.fails_exactly(modelled),
                "{host_id} does not fail exactly {}",
                modelled.id()
            );
        }
    }

    /// The three slots whose meaning changed in cycles 6–8 are recorded, so the
    /// ledger is re-priced against the new statements rather than the old ones.
    #[test]
    fn w619_repriced_slots_are_recorded() {
        assert_eq!(REPRICED_BY_CYCLES_6_TO_8.len(), 3);
        let ids: Vec<&str> = REPRICED_BY_CYCLES_6_TO_8.iter().map(|(i, _)| *i).collect();
        assert!(ids.contains(&"OB-BORN"));
        assert!(ids.contains(&"OB-SPECTRAL"));
        assert!(ids.contains(&"OB-COMPOSE"));
        assert!(REPRICED_BY_CYCLES_6_TO_8[0].1.contains("Busch"));
        assert!(REPRICED_BY_CYCLES_6_TO_8[1].1.contains("UNDERIVABLE"));
    }

    /// The LT ↔ OB-U1 split is disputed between Rust and Lean; the dispute is
    /// recorded rather than resolved by fiat in either direction.
    #[test]
    fn w619_lt_u1_split_is_adjudicated_as_coupled() {
        let verdict = LT_U1_SPLIT_DISPUTED
            .split_whitespace()
            .collect::<Vec<_>>()
            .join(" ");
        assert!(verdict.contains("the WITNESS is INVALIDATED"));
        assert!(verdict.contains("COUPLING on quantum carriers remains OPEN"));
        assert!(
            verdict.contains("What is NOT established"),
            "the verdict must state its own limit"
        );
        assert!(
            !verdict.contains("ADJUDICATED"),
            "the coupling was not adjudicated"
        );
        assert!(LT_U1_SPLIT_DISPUTED.contains("SPLIT-OUTSIDE-REGISTRY"));
        // The hosts behave exactly as before; the adjudication is about what that
        // behaviour MEANS, not about changing it.
        assert!(countermodel_drop_local_tomography().ob_u1_holds());
        assert!(countermodel_drop_ob_u1().local_tomography_holds());
        // ...and the reason the second one holds is that its counts are CLASSICAL.
        let h = countermodel_drop_ob_u1();
        assert_eq!((h.local_param_a, h.local_param_b, h.joint_param), (2, 2, 4));
    }

    #[test]
    fn seven_slots_enumerated() {
        assert_eq!(ImportSlot::ALL.len(), 7);
        assert_eq!(ImportSlot::NonCommuting.id(), "NonCommuting");
        assert_eq!(ImportSlot::ObU1.id(), "OB-U1");
        assert_eq!(ImportSlot::LocalTomography.id(), "LocalTomography");
    }

    #[test]
    fn instruments_uncoupled_from_jordan_spectral() {
        let h = countermodel_drop_spectral();
        assert!(!h.spectral_reconstructs());
        assert!(h.instruments_hold());
        assert!(h.fails_exactly(ImportSlot::Spectral));
    }

    /// OB-U1 reads the declared phase kind and computes the fiber on the
    /// amplitudes: real amplitudes suffice under `ComplexU1`, imaginary ones do
    /// not help under `RealOnly`, and a zero vector has no fiber.
    #[test]
    fn ob_u1_computes_the_fiber_of_the_declared_phase_group() {
        let mut host = countermodel_drop_ob_u1();
        assert!(!host.ob_u1_holds());
        host.amplitudes = vec![(0, 1), (1, 1)];
        assert!(!host.ob_u1_holds());
        host.phase = PhaseKind::ComplexU1;
        host.amplitudes = vec![(1, 0), (2, 0)];
        assert!(host.ob_u1_holds());
        host.amplitudes = vec![(0, 0), (0, 0)];
        assert!(!host.ob_u1_holds());
        assert_eq!(host.phase_group().len(), 4);
    }

    /// The four declaration-read slots: restoring the one dropped declaration
    /// makes each countermodel admit every slot, so its failure rests on that
    /// declaration alone.
    #[test]
    fn declaration_slots_fail_by_their_declaration_alone() {
        let restore: [(ImportSlot, fn(&mut FiniteImportHost)); 4] = [
            (ImportSlot::Monoidal, |h| {
                h.composition = CompositionKind::Tensor
            }),
            (ImportSlot::ObU1, |h| h.phase = PhaseKind::ComplexU1),
            (ImportSlot::BornGleason, |h| h.born = BornKind::Quadratic),
            (ImportSlot::Instruments, |h| h.has_instrument_update = true),
        ];
        for (slot, fix) in restore {
            let (_, mut host) = independence_countermodels()
                .into_iter()
                .find(|(s, _)| *s == slot)
                .unwrap();
            assert!(host.fails_exactly(slot), "{slot:?}");
            fix(&mut host);
            assert!(ImportSlot::ALL.iter().all(|&s| host.admits(s)), "{slot:?}");
        }
    }
}
