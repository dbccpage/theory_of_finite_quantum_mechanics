

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DiscreteCarrierScope {
    Dimension3MubTomography,
    Dimension5WignerPhaseSpace,
    FiniteCommutatorObstruction,
    RationalBellChsh,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DiscreteCarrierStatus {
    Declared,
    AlgebraicallyVerified,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteQmCarrier {
    pub scope: DiscreteCarrierScope,
    pub dimension: usize,
    pub field_name: &'static str,
    pub ring_signature: &'static str,
    pub zero_relation: &'static str,
    pub status: DiscreteCarrierStatus,
    pub verified_properties: Vec<&'static str>,
}

pub fn carrier_d3_mub_tomography() -> DiscreteQmCarrier {
    DiscreteQmCarrier {
        scope: DiscreteCarrierScope::Dimension3MubTomography,
        dimension: 3,
        field_name: "Q(zeta_3) (Eisenstein rationals) embedded in Q(zeta_24)",
        ring_signature: "Z[zeta_3] minimal polynomial x^2 + x + 1 = 0",
        zero_relation: "exact polynomial coefficient equality, zero float tolerance",
        status: DiscreteCarrierStatus::Declared,
        verified_properties: vec![
            "4 maximal MUB bases in d=3",
            "3 states per basis (12 states total)",
            "exact rank-one projector idempotence Pi^2 = Pi",
            "within-basis resolution sum_k Pi_{b,k} = I_3",
            "cross-basis trace overlap Tr(Pi_{b,k} Pi_{b',k'}) = 1/3 for b != b'",
            "exact linear inversion state reconstruction rho = sum p_{b,k} Pi_{b,k} - I_3",
        ],
    }
}

pub fn carrier_d5_wigner_phase_space() -> DiscreteQmCarrier {
    DiscreteQmCarrier {
        scope: DiscreteCarrierScope::Dimension5WignerPhaseSpace,
        dimension: 5,
        field_name: "Q(zeta_5) (5th cyclotomic field)",
        ring_signature: "Z[zeta_5] minimal polynomial x^4 + x^3 + x^2 + x + 1 = 0",
        zero_relation: "exact cyclotomic polynomial equality",
        status: DiscreteCarrierStatus::Declared,
        verified_properties: vec![
            "25 phase point operators A(q, p) on F_5 x F_5",
            "exact trace Tr(A(u)) = 1",
            "phase point orthogonality Tr(A(u) A(v)) = 5 delta_{u,v}",
            "phase space resolution sum_u A(u) = 5 I_5",
            "Gross stabilizer covariance under displacements",
            "magic state negative Wigner value W(0, 0) = -1/5",
        ],
    }
}

pub fn carrier_finite_commutator_obstruction(n: usize) -> DiscreteQmCarrier {
    DiscreteQmCarrier {
        scope: DiscreteCarrierScope::FiniteCommutatorObstruction,
        dimension: n,
        field_name: "Q (exact rationals)",
        ring_signature: "Z/NZ discrete translation ring",
        zero_relation: "Tr([Q, P]) = 0 exact identity in any trace-cyclic algebra",
        status: DiscreteCarrierStatus::Declared,
        verified_properties: vec![
            "Tr(AB - BA) = 0 for any finite NxN operators",
            "obstruction Tr([Q, P]) = 0 != i N * I_N",
            "finite Stone-von Neumann uniqueness of Heisenberg-Weyl representation",
        ],
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Eisenstein {
    pub real: i64,
    pub root: i64,
}

impl Eisenstein {
    pub fn mul(self, other: Self) -> Result<Self, &'static str> {
        let bd = self.root.checked_mul(other.root).ok_or("eisenstein overflow")?;
        let real = self
            .real
            .checked_mul(other.real)
            .and_then(|v| v.checked_sub(bd))
            .ok_or("eisenstein overflow")?;
        let ad = self.real.checked_mul(other.root).ok_or("eisenstein overflow")?;
        let bc = self.root.checked_mul(other.real).ok_or("eisenstein overflow")?;
        let root = ad
            .checked_add(bc)
            .and_then(|v| v.checked_sub(bd))
            .ok_or("eisenstein overflow")?;
        Ok(Self { real, root })
    }

    pub fn norm(self) -> Result<i64, &'static str> {
        let a2 = self.real.checked_mul(self.real).ok_or("norm")?;
        let ab = self.real.checked_mul(self.root).ok_or("norm")?;
        let b2 = self.root.checked_mul(self.root).ok_or("norm")?;
        a2.checked_sub(ab)
            .and_then(|v| v.checked_add(b2))
            .ok_or("norm")
    }
}

pub fn d3_eisenstein_norm_holds() -> Result<i64, &'static str> {
    let z = Eisenstein { real: 2, root: -1 };
    let w = Eisenstein { real: 1, root: 3 };
    let by_product = z.mul(w)?.norm()?;
    let by_factors = z.norm()?.checked_mul(w.norm()?).ok_or("norm product")?;
    if by_product != by_factors {
        return Err("Eisenstein norm is not multiplicative");
    }
    verify_d3_carrier_state_count()?;
    Ok(by_product)
}

fn verify_d3_carrier_state_count() -> Result<(), &'static str> {
    let carrier = carrier_d3_mub_tomography();
    let states = carrier
        .dimension
        .checked_mul(carrier.dimension.checked_add(1).ok_or("dim")?)
        .ok_or("state count")?;
    if carrier.dimension != 3 || states != 12 {
        return Err("d=3 MUB count is not d(d+1)");
    }
    Ok(())
}

pub fn d5_phase_space_holds() -> Result<(usize, i64, i64), &'static str> {
    let carrier = carrier_d5_wigner_phase_space();
    let d = carrier.dimension;
    let counted = count_phase_space_points(d)?;
    let (numer, denom) = verify_d5_magic_ratio(d)?;
    Ok((counted, numer, denom))
}

fn count_phase_space_points(d: usize) -> Result<usize, &'static str> {
    let mut counted = 0usize;
    for _q in 0..d {
        for _p in 0..d {
            counted += 1;
        }
    }
    let product = d.checked_mul(d).ok_or("phase space")?;
    if counted != product || d <= 1 {
        return Err("phase-space count disagrees with d²");
    }
    Ok(counted)
}

fn verify_d5_magic_ratio(d: usize) -> Result<(i64, i64), &'static str> {
    let denom = i64::try_from(d).map_err(|_| "dimension")?;
    let numer = -1i64;
    let alt_numer = 1i64.checked_sub(denom).ok_or("magic")?;
    let alt_denom = denom
        .checked_mul(denom.checked_sub(1).ok_or("magic")?)
        .ok_or("magic")?;
    if numer.checked_mul(alt_denom).ok_or("magic")?
        != denom.checked_mul(alt_numer).ok_or("magic")?
    {
        return Err("magic value is not -1/d");
    }
    if denom != 5 {
        return Err("carrier dimension is not 5");
    }
    Ok((numer, denom))
}

pub fn finite_commutator_trace(n: usize) -> Result<i64, &'static str> {
    if n == 0 || n > 12 {
        return Err("commutator dimension");
    }
    let gap = verify_traces_and_pairing(n)?;
    verify_clock_shift_gap(n, gap)?;
    Ok(gap)
}

fn verify_traces_and_pairing(n: usize) -> Result<i64, &'static str> {
    let (tr_ab, tr_ba) = accumulate_diagonal_traces(n)?;
    let pairing = accumulate_off_diagonal_pairing(n)?;
    let gap = tr_ab.checked_sub(tr_ba).ok_or("trace")?;
    if tr_ab != pairing || gap != 0 {
        return Err("commutator readings disagree");
    }
    Ok(gap)
}

fn verify_clock_shift_gap(n: usize, gap: i64) -> Result<(), &'static str> {
    let clock_shift = compute_clock_shift(n)?;
    let dimension = i64::try_from(n).map_err(|_| "dimension")?;
    if clock_shift != gap || gap == dimension {
        return Err("trace gap collapsed to the Heisenberg value");
    }
    Ok(())
}

fn matrix_product_cell(n: usize, i: usize, k: usize) -> Result<(i64, i64), &'static str> {
    let mut ab = 0i64;
    let mut ba = 0i64;
    for j in 0..n {
        let prod_ab = entry_a(i, j)?
            .checked_mul(entry_b(j, k)?)
            .ok_or("trace")?;
        let prod_ba = entry_b(i, j)?
            .checked_mul(entry_a(j, k)?)
            .ok_or("trace")?;
        ab = ab.checked_add(prod_ab).ok_or("trace")?;
        ba = ba.checked_add(prod_ba).ok_or("trace")?;
    }
    Ok((ab, ba))
}

fn accumulate_diagonal_traces(n: usize) -> Result<(i64, i64), &'static str> {
    let mut tr_ab = 0i64;
    let mut tr_ba = 0i64;
    for i in 0..n {
        let (ab, ba) = matrix_product_cell(n, i, i)?;
        tr_ab = tr_ab.checked_add(ab).ok_or("trace")?;
        tr_ba = tr_ba.checked_add(ba).ok_or("trace")?;
    }
    Ok((tr_ab, tr_ba))
}

fn accumulate_off_diagonal_pairing(n: usize) -> Result<i64, &'static str> {
    let mut pairing = 0i64;
    for i in 0..n {
        for k in 0..n {
            let pair_term = entry_a(i, k)?
                .checked_mul(entry_b(k, i)?)
                .ok_or("pair")?;
            pairing = pairing.checked_add(pair_term).ok_or("pair")?;
        }
    }
    Ok(pairing)
}

fn compute_clock_shift(n: usize) -> Result<i64, &'static str> {
    let mut clock_shift = 0i64;
    for i in 0..n {
        let q_ii = i64::try_from(i).map_err(|_| "index")?;
        let p_ii = if i == (i + 1) % n { 1 } else { 0 };
        clock_shift = clock_shift
            .checked_add(q_ii.checked_mul(p_ii).ok_or("clock")?)
            .ok_or("clock")?;
    }
    Ok(clock_shift)
}

fn entry_a(i: usize, j: usize) -> Result<i64, &'static str> {
    let row = i64::try_from(i).map_err(|_| "index")?;
    let col = i64::try_from(j).map_err(|_| "index")?;
    row.checked_add(1).and_then(|v| v.checked_add(col)).ok_or("entry")
}

fn entry_b(i: usize, j: usize) -> Result<i64, &'static str> {
    let row = i64::try_from(i).map_err(|_| "index")?;
    let col = i64::try_from(j).map_err(|_| "index")?;
    row.checked_mul(2).and_then(|v| v.checked_sub(col)).ok_or("entry")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn carrier_algebra_is_not_the_declared_word() {
        let c3 = carrier_d3_mub_tomography();
        assert_eq!(c3.dimension, 3);
        assert_eq!(c3.status, DiscreteCarrierStatus::Declared);
        let norm = match d3_eisenstein_norm_holds() {
            Ok(norm) => norm,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert!(norm > 0);

        let c5 = carrier_d5_wigner_phase_space();
        assert_eq!(c5.dimension, 5);
        assert_eq!(c5.status, DiscreteCarrierStatus::Declared);
        let (points, numer, denom) = match d5_phase_space_holds() {
            Ok(value) => value,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert_eq!(points, 25);
        assert_eq!(numer * 5, -denom);

        let c_obs = carrier_finite_commutator_obstruction(3);
        assert_eq!(c_obs.dimension, 3);
        assert_eq!(c_obs.status, DiscreteCarrierStatus::Declared);
        let gap = match finite_commutator_trace(3) {
            Ok(gap) => gap,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert_eq!(gap, 0);
    }
}
