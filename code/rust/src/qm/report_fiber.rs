use crate::linear_algebra::basic_matrix::BasicMatrix;
use linear_algebra::image_kernel::ExactRowReduction;
use num_traits::Zero;
use omega_number_theory::cyclotomic::GaussianRat as G;
use omega_number_theory::rational::{ri, rq, Rational as Q};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct PresentedCarrier {
    report: Vec<usize>,
    labels: usize,
}

impl PresentedCarrier {
    pub fn new(report: Vec<usize>, labels: usize) -> Result<Self, String> {
        if report.len() > 4096 || labels > 4096 {
            return Err("CARRIER_BUDGET_EXCEEDED".into());
        }
        if report.iter().any(|&x| x >= labels) || (0..labels).any(|q| !report.contains(&q)) {
            return Err("REPORT_MUST_SURJECT_ON_DECLARED_LABELS".into());
        }
        Ok(Self { report, labels })
    }
    pub fn descend(&self, update: &[usize]) -> Result<Option<Vec<usize>>, String> {
        if update.len() != self.report.len() || update.iter().any(|&x| x >= self.report.len()) {
            return Err("INVALID_CARRIER_UPDATE".into());
        }
        let mut descended = vec![None; self.labels];
        for (x, &target) in update.iter().enumerate() {
            let label = self.report[x];
            let image = self.report[target];
            if descended[label].is_some_and(|old| old != image) {
                return Ok(None);
            }
            descended[label] = Some(image);
        }
        Ok(Some(descended.into_iter().map(Option::unwrap).collect()))
    }
    pub fn push_weights(&self, weights: &[Q]) -> Result<Vec<Q>, String> {
        if weights.len() != self.report.len() || weights.iter().any(|q| q < &Q::zero()) {
            return Err("NONNEGATIVE_CARRIER_WEIGHTS_REQUIRED".into());
        }
        let mut result = vec![Q::zero(); self.labels];
        for (x, w) in weights.iter().enumerate() {
            result[self.report[x]] += w;
        }
        Ok(result)
    }
}

pub fn reversible(update: &[usize]) -> bool {
    let mut sorted = update.to_vec();
    sorted.sort_unstable();
    sorted == (0..update.len()).collect::<Vec<_>>()
}

pub fn permutations(n: usize) -> Result<Vec<Vec<usize>>, String> {
    if n > 8 {
        return Err("PERMUTATION_BUDGET_EXCEEDED".into());
    }
    fn walk(n: usize, p: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
        if p.len() == n {
            out.push(p.clone());
            return;
        }
        for x in 0..n {
            if !p.contains(&x) {
                p.push(x);
                walk(n, p, out);
                p.pop();
            }
        }
    }
    let mut result = Vec::new();
    walk(n, &mut Vec::new(), &mut result);
    Ok(result)
}

pub fn phase_blind(amplitudes: &[G]) -> Result<Vec<Q>, String> {
    if amplitudes.len() > 4096 {
        return Err("AMPLITUDE_BUDGET_EXCEEDED".into());
    }
    if amplitudes.iter().any(|x| !x.is_integer_ring_element()) {
        return Err("GAUSSIAN_INTEGER_HOST_REQUIRED".into());
    }
    Ok(amplitudes.iter().map(G::norm_sq).collect())
}

pub fn mix(a: &[G; 2]) -> [G; 2] {
    [a[0].add(&a[1]), a[0].sub(&a[1])]
}

pub fn born_probabilities(amplitudes: &[G]) -> Result<Vec<Q>, String> {
    let weights = phase_blind(amplitudes)?;
    omega_functional::born_probabilities::BornProbabilities::from_weights(&weights)
        .map(|probabilities| probabilities.probabilities().to_vec())
        .map_err(|_| "ZERO_WEIGHT_STATE".into())
}

pub fn tensor2(u: &[Q; 2], v: &[Q; 2]) -> [Q; 4] {
    [&u[0] * &v[0], &u[0] * &v[1], &u[1] * &v[0], &u[1] * &v[1]]
}
pub fn dump_right(u: &[Q; 2], v: &[Q; 2]) -> [Q; 4] {
    [
        &u[0] * (&v[0] + &v[1]),
        Q::zero(),
        &u[1] * (&v[0] + &v[1]),
        Q::zero(),
    ]
}
pub fn entanglement_determinant(a: &[Q; 4]) -> Q {
    &a[0] * &a[3] - &a[1] * &a[2]
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct CarrierStage {
    pub stage: usize,
    pub vertices: usize,
    pub edges: Vec<(usize, usize)>,
    pub boundary: Vec<Vec<Q>>,
    pub betti_h0: usize,
    pub betti_h1: usize,
    pub automorphism_order: usize,
}
pub fn carrier_stage(stage: usize) -> Result<CarrierStage, String> {
    let (vertices, edges) = match stage {
        0 => (0, vec![]),
        1 => (1, vec![]),
        2 => (2, vec![]),
        3 => (2, vec![(0, 1)]),
        4 => (1, vec![(0, 0)]),
        5 => (2, vec![(0, 1), (1, 0)]),
        6 => (3, vec![(0, 1), (1, 2)]),
        7 => (3, vec![(0, 1), (1, 2), (2, 0)]),
        8 => (3, vec![(0, 1), (1, 2), (2, 0)]),
        _ => return Err("STAGE_OUT_OF_RANGE".into()),
    };
    let mut boundary = vec![vec![Q::zero(); edges.len()]; vertices];
    for (j, &(u, v)) in edges.iter().enumerate() {
        boundary[u][j] -= ri(1);
        boundary[v][j] += ri(1);
    }
    let d1 = BasicMatrix::from_row_major(
        vertices,
        edges.len(),
        boundary.iter().flatten().cloned().collect(),
    )
    .map_err(|e| e.to_string())?;
    let c2 = usize::from(stage == 8);
    let d2 = BasicMatrix::from_row_major(
        edges.len(),
        c2,
        if c2 == 1 { vec![ri(1); 3] } else { vec![] },
    )
    .map_err(|e| e.to_string())?;
    let _complex = omega_homology::chain_complex::ChainComplex::new(
        vertices,
        edges.len(),
        c2,
        d1.clone(),
        d2.clone(),
    )
    .map_err(|e| e.to_string())?;
    let rank = d1.rank().map_err(|e| e.to_string())?;
    let mut sorted_edges = edges.clone();
    sorted_edges.sort_unstable();
    let vertex_automorphisms = permutations(vertices)?
        .iter()
        .filter(|p| {
            let mut image: Vec<_> = edges.iter().map(|&(a, b)| (p[a], p[b])).collect();
            image.sort_unstable();
            image == sorted_edges
        })
        .count();
    let automorphism_order = vertex_automorphisms * if stage == 4 { 2 } else { 1 };
    Ok(CarrierStage {
        stage,
        vertices,
        edges: edges.clone(),
        boundary,
        betti_h0: vertices - rank,
        betti_h1: edges.len() - rank - d2.rank().map_err(|e| e.to_string())?,
        automorphism_order,
    })
}

fn binomial(n: usize, k: usize) -> Option<usize> {
    if k > n {
        return Some(0);
    }
    (0..k).try_fold(1usize, |acc, i| Some(acc.checked_mul(n - i)? / (i + 1)))
}

pub fn scaled_simplex(labels: usize, scale: usize) -> Result<Vec<Vec<usize>>, String> {
    let count = labels
        .checked_sub(1)
        .and_then(|k| binomial(scale.checked_add(k)?, k))
        .ok_or("SIMPLEX_NEEDS_A_LABEL")?;
    if count > 100_000 {
        return Err("SIMPLEX_BUDGET_EXCEEDED".into());
    }
    fn walk(labels: usize, left: usize, prefix: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
        if prefix.len() + 1 == labels {
            prefix.push(left);
            out.push(prefix.clone());
            prefix.pop();
            return;
        }
        for w in 0..=left {
            prefix.push(w);
            walk(labels, left - w, prefix, out);
            prefix.pop();
        }
    }
    let mut out = Vec::with_capacity(count);
    walk(labels, scale, &mut Vec::new(), &mut out);
    Ok(out)
}

fn integer_weights_at_declared_scale() -> Result<bool, String> {
    let (labels, scale) = (3, 10);
    let simplex = scaled_simplex(labels, scale)?;
    Ok(
        Some(simplex.len()) == binomial(scale + labels - 1, labels - 1)
            && simplex.contains(&vec![2, 3, 5])
            && !simplex
                .iter()
                .any(|w| w.iter().all(|&x| labels * x == scale)),
    )
}

fn basis_vector(n: usize, q: usize) -> Vec<G> {
    (0..n)
        .map(|i| if i == q { G::one() } else { G::zero() })
        .collect()
}

fn form(g: &BasicMatrix<G>, u: &[G], v: &[G]) -> Result<G, String> {
    let gv =
        crate::linear_algebra::matrix::multiply_vector(g, v).map_err(|e| e.to_string())?;
    crate::linear_algebra::involution::inner_product(u, &gv).map_err(|e| e.to_string())
}

fn basis_orthonormal(g: &BasicMatrix<G>, n: usize) -> Result<bool, String> {
    for a in 0..n {
        for b in 0..n {
            let expected = if a == b { G::one() } else { G::zero() };
            if form(g, &basis_vector(n, a), &basis_vector(n, b))? != expected {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

fn gram_form_not_unique() -> Result<bool, String> {
    use crate::linear_algebra::matrix::diagonal;
    use omega_quantum_physics::exact_hermitian::is_positive_definite;
    let g1 = diagonal(&[G::one(), G::one()]).map_err(|e| e.to_string())?;
    let g2 = diagonal(&[G::one(), G::from_ints(2, 0)]).map_err(|e| e.to_string())?;
    let orthogonal = |g| -> Result<bool, String> {
        Ok(form(g, &basis_vector(2, 0), &basis_vector(2, 1))?.is_zero())
    };
    let proportional = g1
        .get_ref(0, 0)
        .map_err(|e| e.to_string())?
        .mul(g2.get_ref(1, 1).map_err(|e| e.to_string())?)
        == g1
            .get_ref(1, 1)
            .map_err(|e| e.to_string())?
            .mul(g2.get_ref(0, 0).map_err(|e| e.to_string())?);
    Ok(is_positive_definite(&g1)
        && is_positive_definite(&g2)
        && orthogonal(&g1)?
        && orthogonal(&g2)?
        && !proportional
        && basis_orthonormal(&g1, 2)?
        && !basis_orthonormal(&g2, 2)?)
}

fn two_label_dimension_below_three(labels: usize) -> Result<bool, String> {
    let identity =
        crate::linear_algebra::matrix::identity(labels).map_err(|e| e.to_string())?;
    let frames = |size: usize| -> Result<usize, String> {
        let mut count = 0;
        for subset in 0u32..(1u32 << labels) {
            let members: Vec<usize> = (0..labels).filter(|&q| (subset >> q) & 1 == 1).collect();
            if members.len() != size {
                continue;
            }
            let mut orthonormal = true;
            for &a in &members {
                for &b in &members {
                    let expected = if a == b { G::one() } else { G::zero() };
                    orthonormal &= form(
                        &identity,
                        &basis_vector(labels, a),
                        &basis_vector(labels, b),
                    )? == expected;
                }
            }
            count += usize::from(orthonormal);
        }
        Ok(count)
    };
    if labels > 16 {
        return Err("LABEL_BUDGET_EXCEEDED".into());
    }
    Ok(labels < 3 && frames(labels)? == 1 && frames(3)? == 0)
}

fn unit_total_pairing_rivals() -> Result<bool, String> {
    let declared = |w: &[Q], e: &[Q]| &w[0] * &e[0] + &w[1] * &e[1];
    let swapped = |w: &[Q], e: &[Q]| &w[1] * &e[0] + &w[0] * &e[1];
    let unit = [ri(1), ri(1)];
    let mut shared = true;
    let mut nonnegative = true;
    for code in 0..81i64 {
        let part = |k: u32| code / 3i64.pow(k) % 3 - 1;
        let w = phase_blind(&[
            G::from_ints(part(0), part(1)),
            G::from_ints(part(2), part(3)),
        ])?;
        shared &= declared(&w, &unit) == swapped(&w, &unit);
        for e in 0..9i64 {
            let effect = [ri(e % 3), ri(e / 3)];
            nonnegative &= declared(&w, &effect) >= Q::zero() && swapped(&w, &effect) >= Q::zero();
        }
    }
    let w = phase_blind(&[G::from_ints(2, 0), G::from_ints(1, 0)])?;
    let false_indicator = [ri(1), ri(0)];
    Ok(shared
        && nonnegative
        && declared(&w, &false_indicator) == ri(4)
        && swapped(&w, &false_indicator) == ri(1))
}

fn closed_with_exponent_two<T: PartialEq>(
    group: &[T],
    mul: impl Fn(&T, &T) -> T,
    one: &T,
) -> (bool, bool) {
    let closed = group
        .iter()
        .all(|a| group.iter().all(|b| group.contains(&mul(a, b))));
    (closed, group.iter().all(|g| mul(g, g) == *one))
}

fn phase_extra_does_not_select_circle() -> bool {
    use omega_number_theory::cyclotomic::EisensteinRat as E;
    let signs = [G::one(), G::from_ints(-1, 0)];
    let units = [G::one(), G::i(), G::from_ints(-1, 0), G::from_ints(0, -1)];
    let cube_roots = [E::one(), E::zeta3(), E::zeta3_sq()];
    let (signs_closed, signs_two) = closed_with_exponent_two(&signs, G::mul, &G::one());
    let (units_closed, units_two) = closed_with_exponent_two(&units, G::mul, &G::one());
    let (roots_closed, roots_two) = closed_with_exponent_two(&cube_roots, E::mul, &E::one());
    signs_closed
        && units_closed
        && roots_closed
        && signs_two
        && !units_two
        && !roots_two
        && units.len() != cube_roots.len()
}

fn pauli_y_requires_imaginary_coefficients() -> Result<bool, String> {
    use crate::linear_algebra::{involution as star, matrix as mx};
    let m = |rows: [[(i64, i64); 2]; 2]| {
        mx::from_rows(
            rows.iter()
                .map(|r| r.iter().map(|&(a, b)| G::from_ints(a, b)).collect())
                .collect(),
        )
        .map_err(|e| e.to_string())
    };
    let x = m([[(0, 0), (1, 0)], [(1, 0), (0, 0)]])?;
    let z = m([[(1, 0), (0, 0)], [(0, 0), (-1, 0)]])?;
    let y = m([[(0, 0), (0, -1)], [(0, 1), (0, 0)]])?;
    let identity = mx::identity(2).map_err(|e| e.to_string())?;
    let anticommutes = |a: &BasicMatrix<G>, b: &BasicMatrix<G>| -> Result<bool, String> {
        let ab = mx::multiply(a, b).map_err(|e| e.to_string())?;
        let ba = mx::multiply(b, a).map_err(|e| e.to_string())?;
        Ok(mx::is_zero_matrix(
            &mx::add(&ab, &ba).map_err(|e| e.to_string())?,
        ))
    };
    let pauli_like = |r: &BasicMatrix<G>| -> Result<bool, String> {
        Ok(star::adjoint(r).map_err(|e| e.to_string())? == *r
            && mx::multiply(r, r).map_err(|e| e.to_string())? == identity
            && anticommutes(r, &x)?
            && anticommutes(r, &z)?)
    };
    let y_ok = pauli_like(&y)? && y.as_slice().iter().any(|e| !e.im.is_zero());
    let mut real_solutions = 0;
    let mut without_x = 0;
    for code in 0..27i64 {
        let part = |k: u32| code / 3i64.pow(k) % 3 - 1;
        let r = m([[(part(0), 0), (part(1), 0)], [(part(1), 0), (part(2), 0)]])?;
        real_solutions += usize::from(pauli_like(&r)?);
        without_x += usize::from(
            mx::multiply(&r, &r).map_err(|e| e.to_string())? == identity && anticommutes(&r, &z)?,
        );
    }
    Ok(y_ok && real_solutions == 0 && without_x > 0)
}

fn permutation_isometry_envelope_strict() -> Result<bool, String> {
    use crate::linear_algebra::{involution as star, matrix as mx};
    let reversible = permutations(2)?;
    let lifts = reversible
        .iter()
        .map(|p| {
            let mut lift = mx::zeros::<G>(2, 2).map_err(|e| e.to_string())?;
            for (j, &image) in p.iter().enumerate() {
                lift.set(image, j, G::one()).map_err(|e| e.to_string())?;
            }
            Ok(lift)
        })
        .collect::<Result<Vec<_>, String>>()?;
    let identity = mx::identity(2).map_err(|e| e.to_string())?;
    let isometry = |m: &BasicMatrix<G>| -> Result<bool, String> {
        Ok(
            mx::multiply(&star::adjoint(m).map_err(|e| e.to_string())?, m)
                .map_err(|e| e.to_string())?
                == identity,
        )
    };
    let mut i_swap = mx::zeros(2, 2).map_err(|e| e.to_string())?;
    i_swap.set(0, 1, G::i()).map_err(|e| e.to_string())?;
    i_swap.set(1, 0, G::i()).map_err(|e| e.to_string())?;
    let all_lifts_isometric = lifts
        .iter()
        .map(isometry)
        .collect::<Result<Vec<_>, _>>()?
        .into_iter()
        .all(|v| v);
    Ok(reversible.len() == 2
        && all_lifts_isometric
        && isometry(&i_swap)?
        && !lifts.contains(&i_swap))
}

fn fractional_half_weights() -> bool {
    let same = |(a, b): (i64, i64), (c, d): (i64, i64)| a * d == b * c;
    let add = |(a, b): (i64, i64), (c, d): (i64, i64)| (a * d + b * c, b * d);
    let half = (1, 2);
    same(add(half, half), (1, 1))
        && !same(half, (0, 1))
        && !same(half, (1, 1))
        && same(half, (2, 4))
        && rq(1, 2) + rq(1, 2) == ri(1)
}

fn power_readout_ratios(p: u32) -> (Q, Q) {
    let readout = |v: [i64; 2]| -> Q { v.iter().map(|x| ri(x.abs().pow(p))).sum() };
    let mix_real = |v: [i64; 2]| [v[0] + v[1], v[0] - v[1]];
    let (basis, plus) = ([1, 0], [1, 1]);
    (
        readout(mix_real(basis)) / readout(basis),
        readout(mix_real(plus)) / readout(plus),
    )
}

pub fn run(input: &Value) -> Result<Value, String> {
    let carrier = if input.get("report").is_some() {
        PresentedCarrier::new(
            serde_json::from_value(input["report"].clone()).map_err(|e| e.to_string())?,
            input["labels"].as_u64().ok_or("LABEL_COUNT_REQUIRED")? as usize,
        )?
    } else {
        PresentedCarrier::new(vec![0, 0, 1, 1], 2)?
    };
    let update = if input.get("update").is_some() {
        serde_json::from_value(input["update"].clone()).map_err(|e| e.to_string())?
    } else {
        (0..carrier.report.len()).collect::<Vec<_>>()
    };
    let descent = carrier.descend(&update)?;
    let weights = vec![rq(1, 2); carrier.report.len()];
    let pushed = carrier.push_weights(&weights)?;
    let pairs = permutations(4)?;
    let identity_dilations = pairs
        .iter()
        .filter(|p| (0..4).all(|x| p[x] / 2 == x / 2))
        .count();
    let collapse_dilations = pairs
        .iter()
        .filter(|p| (0..2).all(|q| p[q * 2] / 2 == 0))
        .count();
    let bool_maps: Vec<Vec<usize>> = (0..4).map(|m| vec![m & 1, (m >> 1) & 1]).collect();
    let no_half_step = bool_maps.iter().all(|p| (0..2).any(|q| p[p[q]] != 1 - q));
    let a = [G::from_ints(1, 0), G::from_ints(1, 0)];
    let b = [G::from_ints(1, 0), G::from_ints(-1, 0)];
    let w_a = phase_blind(&a)?;
    let w_b = phase_blind(&b)?;
    let mixed_a = phase_blind(&mix(&a))?;
    let mixed_b = phase_blind(&mix(&b))?;
    let plus_i = G::from_ints(1, 1);
    let inv = plus_i.inv();
    let mut scale_checks = 0;
    let mut scales_preserved = true;
    for ar in -2..=2 {
        for ai in -2..=2 {
            for br in -2..=2 {
                for bi in -2..=2 {
                    let v = [G::from_ints(ar, ai), G::from_ints(br, bi)];
                    let before: Q = phase_blind(&v)?.into_iter().sum();
                    let after: Q = phase_blind(&mix(&v))?.into_iter().sum();
                    scales_preserved &= after == ri(2) * before;
                    scale_checks += 1;
                }
            }
        }
    }
    let powers: Vec<Value> = (1u32..=4)
        .map(|p| {
            let (basis_ratio, plus_ratio) = power_readout_ratios(p);
            json!({"power":p,"basis_ratio":format!("{}/{}", basis_ratio.numer(), basis_ratio.denom()),
                   "plus_ratio":crate::qm::finite_witness::qstr(&plus_ratio),"uniform_scale_two":basis_ratio==plus_ratio})
        })
        .collect();
    let bell = [ri(1), ri(0), ri(0), ri(1)];
    let u = [ri(1), ri(0)];
    let v = [ri(0), ri(1)];
    let stages = (0..=8).map(carrier_stage).collect::<Result<Vec<_>, _>>()?;
    let psi = [G::from_ints(1, 0), G::from_ints(0, 1), G::from_ints(1, -1)];
    let probabilities = born_probabilities(&psi)?;
    let operators = gaussian_operator_checks()?;
    let report_permutations = permutations(4)?;
    let permutation_lifts = report_permutations.iter().all(|p| {
        let x = [ri(2), ri(-1), ri(3), ri(4)];
        let y = [ri(7), ri(2), ri(-3), ri(1)];
        let lift = |v: &[Q]| p.iter().map(|&i| v[i].clone()).collect::<Vec<_>>();
        gaussian_pairing(
            &lift(&x)
                .into_iter()
                .map(G::from_rational)
                .collect::<Vec<_>>(),
            &lift(&y)
                .into_iter()
                .map(G::from_rational)
                .collect::<Vec<_>>(),
        )
        .unwrap()
        .re == x.iter().zip(y).map(|(x, y)| x * y).sum::<Q>()
    });
    let fixed_carrier = PresentedCarrier::new(vec![0, 0, 1, 1], 2)?;
    let report_weights = vec![ri(1), ri(4)];
    let lifted_weights: Vec<_> = fixed_carrier
        .report
        .iter()
        .map(|&i| report_weights[i].clone())
        .collect();
    let bell_splits_fiber =
        fixed_carrier.report[0] == fixed_carrier.report[1] && bell[0] != bell[1];
    let checks = json!({
        "mass_preserved":weights.iter().cloned().sum::<Q>()==pushed.iter().cloned().sum::<Q>(),
        "integer_weights_at_declared_scale":integer_weights_at_declared_scale()?,
        "permutation_lifts_preserve_pairing":permutation_lifts,
        "presentation_push_recovers_double":fixed_carrier.push_weights(&lifted_weights)?==report_weights.iter().map(|x|x*ri(2)).collect::<Vec<_>>(),
        "bell_not_along_presentation":bell_splits_fiber,
        "collapse_not_reversible":!reversible(&[0,0]),
        "two_bool_reversibles":bool_maps.iter().filter(|p|reversible(p)).count()==2,
        "phase_fiber_equal":w_a==w_b,
        "mixing_separates_fiber":mixed_a!=mixed_b,
        "mix_doubles_weight_on_enumerated_box":scales_preserved,
        "four_identity_dilations":identity_dilations==4,
        "four_collapse_dilations":collapse_dilations==4,
        "no_report_half_step":no_half_step,
        "gaussian_integer_nonunit":!inv.is_integer_ring_element() && plus_i.mul(&inv)==G::one(),
        "tensor_rival_disagrees":tensor2(&u,&v)!=dump_right(&u,&v),
        "bell_nonproduct":!entanglement_determinant(&bell).is_zero(),
        "phase_extra_does_not_select_circle":phase_extra_does_not_select_circle(),
        "unit_total_pairing_rivals":unit_total_pairing_rivals()?,
        "fractional_half_weights":fractional_half_weights(),
        "pauli_y_requires_imaginary_coefficients":pauli_y_requires_imaginary_coefficients()?,
        "two_label_dimension_below_three":two_label_dimension_below_three(fixed_carrier.labels)?,
        "normalization":probabilities.iter().cloned().sum::<Q>()==ri(1),
        "gaussian_operator_composition_and_adjoint":operators,
        "permutation_isometry_envelope_strict":permutation_isometry_envelope_strict()?,
        "gram_form_not_unique":gram_form_not_unique()?,
        "self_adjoint_spectral_field_obstruction":crate::qm::entropy_bounds::splitting_degree_2(&ri(0),&ri(-2))==2
    });
    Ok(
        json!({"authority_effect":"None","scope":"finite witnesses; imported scalar/inner-product/tensor structure remains explicit",
        "carrier":carrier,"descended_update":descent,"pushed_weights":crate::qm::finite_witness::qvec(&pushed),
        "checks":checks,"stages":stages,"mixing":{"weights":crate::qm::finite_witness::qvec(&w_a),"mixed_first":crate::qm::finite_witness::qvec(&mixed_a),"mixed_second":crate::qm::finite_witness::qvec(&mixed_b),"enumerated_amplitude_vectors":scale_checks},
        "finite_power_comparison":powers,"born_probabilities":crate::qm::finite_witness::qvec(&probabilities),
        "identity_dilations":identity_dilations,"collapse_dilations":collapse_dilations,
        "remaining_imports":["complex_field_completion","spectral_theorem_over_C","Gleason_uniqueness","CPTP","Hilbert_tensor_uniqueness","circle_group","continuous_time"],
        "unassigned":["SUSY","Standard_Model_gauge"]}),
    )
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct GaussianOperator {
    matrix: BasicMatrix<G>,
}
impl GaussianOperator {
    pub fn new(rows: &[Vec<G>]) -> Result<Self, String> {
        let n = rows.len();
        if n == 0
            || n > 32
            || rows
                .iter()
                .any(|row| row.len() != n || row.iter().any(|z| !z.is_integer_ring_element()))
        {
            return Err("INVALID_GAUSSIAN_INTEGER_OPERATOR".into());
        }
        Ok(Self {
            matrix: BasicMatrix::from_row_major(n, n, rows.iter().flatten().cloned().collect())
                .map_err(|error| error.to_string())?,
        })
    }
    pub fn compose(&self, other: &Self) -> Result<Self, String> {
        Ok(Self {
            matrix: crate::linear_algebra::matrix::multiply(&self.matrix, &other.matrix)
                .map_err(|error| error.to_string())?,
        })
    }
    pub fn adjoint(&self) -> Self {
        Self {
            matrix: crate::linear_algebra::involution::adjoint(&self.matrix)
                .expect("adjoint preserves the private admitted finite shape"),
        }
    }
    pub fn apply(&self, vector: &[G]) -> Result<Vec<G>, String> {
        crate::linear_algebra::matrix::multiply_vector(&self.matrix, vector)
            .map_err(|error| error.to_string())
    }
}
pub fn gaussian_pairing(a: &[G], b: &[G]) -> Result<G, String> {
    if a.len() != b.len() || a.len() > 4096 {
        return Err("INVALID_PAIRING_DIMENSION".into());
    }
    Ok(a.iter()
        .zip(b)
        .fold(G::zero(), |s, (a, b)| s.add(&a.conj().mul(b))))
}
fn gaussian_operator_checks() -> Result<bool, String> {
    let mut valid = true;
    for n in [2, 4] {
        let a: Vec<Vec<G>> = (0..n)
            .map(|i| {
                (0..n)
                    .map(|j| G::from_ints((i + j) as i64, (i as i64) - (j as i64)))
                    .collect()
            })
            .collect();
        let op = GaussianOperator::new(&a)?;
        let v: Vec<_> = (0..n).map(|i| G::from_ints(i as i64, 1)).collect();
        let w: Vec<_> = (0..n).map(|i| G::from_ints(1, -(i as i64))).collect();
        valid &= op.compose(&op.adjoint())?.apply(&v)? == op.apply(&op.adjoint().apply(&v)?)?;
        valid &= gaussian_pairing(&op.apply(&v)?, &w)?
            == gaussian_pairing(&v, &op.adjoint().apply(&w)?)?;
        for j in 0..n {
            let mut basis = vec![G::zero(); n];
            basis[j] = G::one();
            let column = op.apply(&basis)?;
            valid &= (0..n).all(|i| column[i] == a[i][j]);
        }
    }
    let h = GaussianOperator::new(&vec![
        vec![G::one(), G::one()],
        vec![G::one(), G::from_ints(-1, 0)],
    ])?;
    let twice = GaussianOperator::new(&vec![
        vec![G::from_ints(2, 0), G::zero()],
        vec![G::zero(), G::from_ints(2, 0)],
    ])?;
    valid &= h.adjoint().compose(&h)? == twice;
    Ok(valid)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn report_descent_checks_every_fiber_member() {
        let c = PresentedCarrier::new(vec![0, 0, 1, 1], 2).unwrap();
        assert_eq!(c.descend(&[0, 2, 2, 3]).unwrap(), None);
        assert_eq!(c.descend(&[2, 3, 0, 1]).unwrap(), Some(vec![1, 0]));
        assert!(c.descend(&[4, 1, 2, 3]).is_err());
        assert!(c.push_weights(&[ri(-1), ri(1), ri(1), ri(1)]).is_err());
    }
    #[test]
    fn loops_parallel_edges_and_filled_face_are_distinct() {
        assert_eq!(
            (0..=5)
                .map(|s| carrier_stage(s).unwrap().automorphism_order)
                .collect::<Vec<_>>(),
            vec![1, 1, 2, 1, 2, 2]
        );
        assert_eq!(carrier_stage(4).unwrap().betti_h1, 1);
        assert_eq!(carrier_stage(5).unwrap().betti_h1, 1);
        assert_eq!(carrier_stage(7).unwrap().betti_h1, 1);
        assert_eq!(carrier_stage(8).unwrap().betti_h1, 0);
    }
    #[test]
    fn computed_checks_fail_where_their_property_fails() {
        let simplex = scaled_simplex(3, 9).unwrap();
        assert_eq!(Some(simplex.len()), binomial(11, 2));
        assert!(simplex.contains(&vec![3, 3, 3]));
        assert!(scaled_simplex(0, 3).is_err());
        assert!(scaled_simplex(8, 64).is_err());
        assert!(integer_weights_at_declared_scale().unwrap());
        use crate::linear_algebra::matrix::diagonal;
        use omega_quantum_physics::exact_hermitian::is_positive_definite;
        assert!(!is_positive_definite(
            &diagonal(&[G::one(), G::from_ints(-1, 0)]).unwrap()
        ));
        assert!(basis_orthonormal(&diagonal(&[G::one(), G::one()]).unwrap(), 2).unwrap());
        assert!(!basis_orthonormal(
            &diagonal(&[G::from_ints(2, 0), G::from_ints(2, 0)]).unwrap(),
            2
        )
        .unwrap());
        assert!(two_label_dimension_below_three(2).unwrap());
        assert!(!two_label_dimension_below_three(3).unwrap());
        let (closed, two) =
            closed_with_exponent_two(&[G::one(), G::from_ints(-1, 0)], G::mul, &G::one());
        assert!(closed && two);
        let (closed, two) = closed_with_exponent_two(&[G::one(), G::i()], G::mul, &G::one());
        assert!(!closed && !two);
        assert_eq!(power_readout_ratios(2), (ri(2), ri(2)));
        assert_eq!(power_readout_ratios(4), (ri(2), ri(8)));
        for check in [
            unit_total_pairing_rivals().unwrap(),
            phase_extra_does_not_select_circle(),
            pauli_y_requires_imaginary_coefficients().unwrap(),
            permutation_isometry_envelope_strict().unwrap(),
            fractional_half_weights(),
            gram_form_not_unique().unwrap(),
        ] {
            assert!(check);
        }
    }

    #[test]
    fn finite_witnesses_and_invalid_hosts() {
        let r = run(&Value::Null).unwrap();
        assert!(r["checks"].as_object().unwrap().values().all(|v| v == true));
        assert!(born_probabilities(&[G::zero()]).is_err());
        assert!(phase_blind(&[G::from_rational(rq(1, 2))]).is_err());
        assert!(PresentedCarrier::new(vec![0], 2).is_err());
    }
}
