
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; import-bundle TOY-MECH.";


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ImportSlot {
    Spectral,
    Monoidal,
    LocalTomography,
    ObU1,
    BornGleason,
    Instruments,
    NonCommuting,
}

impl ImportSlot {
    pub const ALL: [ImportSlot; 7] = [
        ImportSlot::Spectral,
        ImportSlot::Monoidal,
        ImportSlot::LocalTomography,
        ImportSlot::ObU1,
        ImportSlot::BornGleason,
        ImportSlot::Instruments,
        ImportSlot::NonCommuting,
    ];

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

pub type Zi = (i64, i64);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompositionKind {
    Tensor,
    DirectSum,
    None,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PhaseKind {
    ComplexU1,
    RealOnly,
    None,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BornKind {
    Quadratic,
    Linear,
    Absent,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteImportHost {
    pub id: &'static str,
    pub drop_note: &'static str,
    pub matrix_2x2: [[Zi; 2]; 2],
    pub dim_a: usize,
    pub dim_b: usize,
    pub composition: CompositionKind,
    pub phase: PhaseKind,
    pub local_param_a: usize,
    pub local_param_b: usize,
    pub joint_param: usize,
    pub born: BornKind,
    pub has_instrument_update: bool,
    pub amplitudes: Vec<Zi>,
    pub eigenvalues: [i64; 2],
    pub projectors_diag: [[i64; 2]; 2],
    pub observables: [[[i64; 2]; 2]; 2],
}

impl FiniteImportHost {
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

    pub fn is_hermitian(&self) -> bool {
        let m = &self.matrix_2x2;
        for i in 0..2 {
            for j in 0..2 {
                let (a, b) = m[i][j];
                let (c, d) = m[j][i];
                if a != c || b != -d {
                    return false;
                }
            }
        }
        true
    }

    fn has_real_diagonal_matrix(&self) -> bool {
        let m = &self.matrix_2x2;
        m[0][1] == (0, 0) && m[1][0] == (0, 0) && m[0][0].1 == 0 && m[1][1].1 == 0
    }

    fn has_orthogonal_projectors_diag(&self) -> bool {
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        p0[0] + p1[0] == 1 && p0[1] + p1[1] == 1 && p0[0] * p1[0] == 0 && p0[1] * p1[1] == 0
    }

    pub fn spectral_reconstructs(&self) -> bool {
        if !self.is_hermitian()
            || !self.has_real_diagonal_matrix()
            || !self.has_orthogonal_projectors_diag()
        {
            return false;
        }
        let m = &self.matrix_2x2;
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        let r0 = self.eigenvalues[0] * p0[0] + self.eigenvalues[1] * p1[0];
        let r1 = self.eigenvalues[0] * p0[1] + self.eigenvalues[1] * p1[1];
        m[0][0].0 == r0 && m[1][1].0 == r1
    }

    pub fn monoidal_holds(&self) -> bool {
        self.composition == CompositionKind::Tensor
            && self.dim_a >= 1
            && self.dim_b >= 1
            && self.dim_a.saturating_mul(self.dim_b) >= 2
    }

    pub fn local_tomography_holds(&self) -> bool {
        self.local_param_a > 0
            && self.local_param_b > 0
            && self.joint_param > 0
            && self.local_param_a.saturating_mul(self.local_param_b) == self.joint_param
    }

    pub fn phase_group(&self) -> &'static [Zi] {
        match self.phase {
            PhaseKind::ComplexU1 => &[(1, 0), (0, 1), (-1, 0), (0, -1)],
            PhaseKind::RealOnly => &[(1, 0), (-1, 0)],
            PhaseKind::None => &[(1, 0)],
        }
    }

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

    pub fn born_gleason_holds(&self) -> bool {
        if self.born != BornKind::Quadratic {
            return false;
        }
        if self.amplitudes.is_empty() {
            return false;
        }
        let mass: i64 = self
            .amplitudes
            .iter()
            .map(|&(re, im)| re * re + im * im)
            .sum();
        mass > 0
    }

    pub fn instruments_hold(&self) -> bool {
        if !self.has_instrument_update || !self.has_orthogonal_projectors_diag() {
            return false;
        }
        let p0 = self.projectors_diag[0];
        let p1 = self.projectors_diag[1];
        [p0[0], p0[1], p1[0], p1[1]]
            .into_iter()
            .all(|v| v == 0 || v == 1)
    }

    pub fn noncommuting_holds(&self) -> bool {
        let [a, b] = self.observables;
        let symmetric = |m: [[i64; 2]; 2]| m[0][1] == m[1][0];
        if !symmetric(a) || !symmetric(b) {
            return false;
        }
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
        observables: [[[0, 1], [1, 0]], [[1, 0], [0, -1]]],
    }
}

pub fn countermodel_drop_spectral() -> FiniteImportHost {
    FiniteImportHost {
        id: "cm_drop_spectral",
        drop_note: "Non-Hermitian nilpotent Jordan block is not unitarily diagonalizable; spectral reconstruction fails.",
        matrix_2x2: [[(0, 0), (1, 0)], [(0, 0), (0, 0)]],
        dim_a: 2,
        dim_b: 2,
        composition: CompositionKind::Tensor,
        phase: PhaseKind::ComplexU1,
        local_param_a: 4,
        local_param_b: 4,
        joint_param: 16,
        born: BornKind::Quadratic,
        has_instrument_update: true,
        amplitudes: vec![(1, 1), (0, 0)],
        eigenvalues: [0, 0],
        projectors_diag: [[1, 0], [0, 1]],
        observables: [[[0, 1], [1, 0]], [[1, 0], [0, -1]]],
    }
}

pub fn countermodel_drop_monoidal() -> FiniteImportHost {
    let mut h = herm_diag_host(
        "cm_drop_monoidal",
        "Composition is direct sum (dim 2+3=5), not tensor (dim 2·3=6); monoidal tensor import absent.",
        [1, -1],
        CompositionKind::DirectSum,
        PhaseKind::ComplexU1,
        4,
        9,
        36,
        BornKind::Quadratic,
        true,
        vec![(1, 0), (0, 1)],
    );
    h.dim_a = 2;
    h.dim_b = 3;
    h
}

pub fn countermodel_drop_local_tomography() -> FiniteImportHost {
    herm_diag_host(
        "cm_drop_local_tomography",
        "Complex U(1) phase present, but joint param count 15 ≠ 4·4=16 (LT identity fails).",
        [1, 0],
        CompositionKind::Tensor,
        PhaseKind::ComplexU1,
        4,
        4,
        15,
        BornKind::Quadratic,
        true,
        vec![(1, 1), (0, 0)],
    )
}

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
        vec![(1, 0), (1, 0)],
    )
}

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
        false,
        vec![(0, 1), (1, 0)],
    )
}

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


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SpectralWitness {
    pub eigenvalues: [i64; 2],
    pub projectors_diag: [[i64; 2]; 2],
}

impl SpectralWitness {
    pub fn computational(eigenvalues: [i64; 2]) -> Self {
        Self {
            eigenvalues,
            projectors_diag: [[1, 0], [0, 1]],
        }
    }

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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObU1Witness {
    pub amplitudes: Vec<Zi>,
}

impl ObU1Witness {
    pub fn validates(&self) -> bool {
        self.amplitudes.iter().any(|&(re, im)| re != 0 || im != 0)
            && self.amplitudes.iter().any(|&(_, im)| im != 0)
    }
}

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

    pub fn masses(&self) -> Vec<i64> {
        self.amplitudes
            .iter()
            .map(|&(re, im)| re * re + im * im)
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstrumentsWitness {
    pub projectors_diag: [[i64; 2]; 2],
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

    pub fn luders_update(&self, outcome: usize) -> Option<[i64; 2]> {
        if !self.validates() || outcome > 1 {
            return None;
        }
        let p = self.projectors_diag[outcome];
        Some([self.prior_diag[0] * p[0], self.prior_diag[1] * p[1]])
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NonCommutingWitness {
    pub observables: [[[i64; 2]; 2]; 2],
}

impl NonCommutingWitness {
    pub fn pauli_xz() -> Self {
        Self {
            observables: [[[0, 1], [1, 0]], [[1, 0], [0, -1]]],
        }
    }

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
    pub fn empty() -> Self {
        Self::default()
    }

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

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SpectralCalculus {
    pub eigenvalues: [i64; 2],
    pub reconstructed_diag: [i64; 2],
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MonoidalTensor {
    pub dim_a: usize,
    pub dim_b: usize,
    pub joint_dim: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TomographyProtocol {
    pub local_param_a: usize,
    pub local_param_b: usize,
    pub joint_param: usize,
    pub identity_holds: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PhaseCarrier {
    pub amplitudes: Vec<Zi>,
    pub has_nontrivial_u1: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BornRule {
    pub masses: Vec<i64>,
    pub total_mass: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstrumentMap {
    pub prior_diag: [i64; 2],
    pub post_outcome_0: [i64; 2],
    pub post_outcome_1: [i64; 2],
}

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

pub fn build_tomography(bundle: &ImportBundle) -> Result<TomographyProtocol, MissingImport> {
    let w = require_local_tomography(bundle)?;
    Ok(TomographyProtocol {
        local_param_a: w.local_param_a,
        local_param_b: w.local_param_b,
        joint_param: w.joint_param,
        identity_holds: true,
    })
}

pub fn build_phase_carrier(bundle: &ImportBundle) -> Result<PhaseCarrier, MissingImport> {
    let w = require_ob_u1(bundle)?;
    Ok(PhaseCarrier {
        amplitudes: w.amplitudes.clone(),
        has_nontrivial_u1: true,
    })
}

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

pub fn authority_fence() -> &'static str {
    AUTHORITY_FENCE
}



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

    fn id_core(self) -> Option<&'static str> {
        match self {
            FrozenSlotId::ObU1 => Some("OB-U1"),
            FrozenSlotId::ObBorn => Some("OB-BORN"),
            FrozenSlotId::ObSpectral => Some("OB-SPECTRAL"),
            FrozenSlotId::ObInstrument => Some("OB-INSTRUMENT"),
            FrozenSlotId::ObCompose => Some("OB-COMPOSE"),
            FrozenSlotId::ObConvex => Some("OB-CONVEX"),
            FrozenSlotId::ObNoncomm => Some("OB-NONCOMM"),
            _ => None,
        }
    }

    pub fn id(self) -> &'static str {
        if let Some(s) = self.id_core() {
            return s;
        }
        match self {
            FrozenSlotId::ObUnitary => "OB-UNITARY",
            FrozenSlotId::ObHerm => "OB-HERM",
            FrozenSlotId::ObL2Readout => "OB-L2-READOUT",
            FrozenSlotId::ObCoherence => "OB-COHERENCE",
            FrozenSlotId::ObStats => "OB-STATS",
            FrozenSlotId::ObClone => "OB-CLONE",
            _ => unreachable!(),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CarrierClass {
    ClassicalSimplex,
    RealQuantum,
    ComplexQuantum,
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

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SlotEvidence {
    IndependentWithCountermodel {
        host_id: &'static str,
        carrier_class: CarrierClass,
    },
    EntailedBy { by: FrozenSlotId, why: &'static str },
    DeclaredNotModelled { needs: &'static str },
}

fn frozen_slot_modeled_evidence(slot: FrozenSlotId) -> Option<SlotEvidence> {
    match slot {
        FrozenSlotId::ObSpectral => Some(independent_with("cm_drop_spectral")),
        FrozenSlotId::ObCompose => Some(independent_with("cm_drop_monoidal")),
        FrozenSlotId::ObU1 => Some(independent_with("cm_drop_ob_u1")),
        FrozenSlotId::ObBorn => Some(independent_with("cm_drop_born_gleason")),
        FrozenSlotId::ObInstrument => Some(independent_with("cm_drop_instruments")),
        FrozenSlotId::ObHerm => Some(SlotEvidence::EntailedBy {
            by: FrozenSlotId::ObSpectral,
            why: "spectral_reconstructs() returns false unless is_hermitian(); no host \
                  can fail OB-HERM while admitting OB-SPECTRAL, so the two cannot both \
                  sit in a drop-one independence basis",
        }),
        FrozenSlotId::ObNoncomm => Some(independent_with("cm_drop_noncommuting")),
        _ => None,
    }
}

pub fn frozen_slot_evidence(slot: FrozenSlotId) -> SlotEvidence {
    if let Some(ev) = frozen_slot_modeled_evidence(slot) {
        return ev;
    }
    let needs = match slot {
        FrozenSlotId::ObConvex => {
            "a state-space field distinguishing a simplex from a general convex body"
        }
        FrozenSlotId::ObUnitary => {
            "a dynamics field separating unitary evolution from the stochastic shadow"
        }
        FrozenSlotId::ObL2Readout => {
            "an l2-readout field split from OB-BORN; the freeze says merge or split \
                    ONLY BY THEOREM, and no such theorem exists yet"
        }
        FrozenSlotId::ObCoherence => {
            "off-diagonal / Kraus-agreement dynamics; the freeze already expects \
                    underdetermination here"
        }
        FrozenSlotId::ObStats => "an exchange-statistics field (multi-particle carrier)",
        FrozenSlotId::ObClone => "a cloning-map field; may be derivable rather than imported",
        _ => unreachable!(),
    };
    SlotEvidence::DeclaredNotModelled { needs }
}

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

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ImportBasis {
    FrozenDeclared,
    Modelled,
    DropOneIndependent,
    ModelledLtNestedUnderU1,
}

pub fn basis_cardinality(basis: ImportBasis) -> usize {
    match basis {
        ImportBasis::FrozenDeclared => FrozenSlotId::ALL.len(),
        ImportBasis::Modelled => ImportSlot::ALL.len(),
        ImportBasis::DropOneIndependent => independent_slots().len(),
        ImportBasis::ModelledLtNestedUnderU1 => ImportSlot::ALL.len() - 1,
    }
}

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


    #[test]
    fn w619_frozen_registry_has_thirteen_slots() {
        assert_eq!(FrozenSlotId::ALL.len(), 13);
        assert_eq!(ImportSlot::ALL.len(), 7);
        let mut ids: Vec<&str> = FrozenSlotId::ALL.iter().map(|s| s.id()).collect();
        ids.sort_unstable();
        ids.dedup();
        assert_eq!(ids.len(), 13, "frozen slot ids must be distinct");
    }

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

    #[test]
    fn w619_hermiticity_guard_is_redundant_entailment_is_structural() {
        let base = countermodel_drop_instruments();
        let vals: [i64; 3] = [0, 1, -1];
        for a_re in vals {
            for a_im in vals {
                for d_re in vals {
                    for d_im in vals {
                        let mut h = base.clone();
                        h.matrix_2x2 = [[(a_re, a_im), (0, 0)], [(0, 0), (d_re, d_im)]];
                        h.eigenvalues = [a_re, d_re];
                        h.projectors_diag = [[1, 0], [0, 1]];
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

    #[test]
    fn w619_canonical_n_is_basis_relative() {
        assert_eq!(basis_cardinality(ImportBasis::FrozenDeclared), 13);
        assert_eq!(basis_cardinality(ImportBasis::Modelled), 7);
        assert_eq!(basis_cardinality(ImportBasis::DropOneIndependent), 6);
        assert_eq!(basis_cardinality(ImportBasis::ModelledLtNestedUnderU1), 6);
        assert_ne!(
            basis_cardinality(ImportBasis::FrozenDeclared),
            basis_cardinality(ImportBasis::DropOneIndependent),
            "quoting the declared count as N is the defect"
        );
    }

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
        assert!(countermodel_drop_local_tomography().ob_u1_holds());
        assert!(countermodel_drop_ob_u1().local_tomography_holds());
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
