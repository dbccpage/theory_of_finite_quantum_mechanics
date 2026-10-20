use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::image_kernel::ExactRowReduction;
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
fn stage_graph(stage: usize) -> Result<(usize, Vec<(usize, usize)>), String> {
    const VERTICES: [usize; 9] = [0, 1, 2, 2, 1, 2, 3, 3, 3];
    const EDGES: [&[(usize, usize)]; 9] = [
        &[],
        &[],
        &[],
        &[(0, 1)],
        &[(0, 0)],
        &[(0, 1), (1, 0)],
        &[(0, 1), (1, 2)],
        &[(0, 1), (1, 2), (2, 0)],
        &[(0, 1), (1, 2), (2, 0)],
    ];
    let Some(&v) = VERTICES.get(stage) else {
        return Err("STAGE_OUT_OF_RANGE".into());
    };
    Ok((v, EDGES[stage].to_vec()))
}

fn count_vertex_automorphisms(vertices: usize, edges: &[(usize, usize)]) -> Result<usize, String> {
    let mut sorted_edges = edges.to_vec();
    sorted_edges.sort_unstable();
    let perms = permutations(vertices)?;
    let mut count = 0;
    for p in &perms {
        let mut image: Vec<_> = edges.iter().map(|&(a, b)| (p[a], p[b])).collect();
        image.sort_unstable();
        if image == sorted_edges {
            count += 1;
        }
    }
    Ok(count)
}

fn build_stage_boundary(
    vertices: usize,
    edges: &[(usize, usize)],
) -> Result<(Vec<Vec<Q>>, BasicMatrix<Q>), String> {
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
    Ok((boundary, d1))
}

fn compute_stage_betti(
    vertices: usize,
    edges_len: usize,
    stage: usize,
    d1: &BasicMatrix<Q>,
) -> Result<(usize, usize), String> {
    let c2 = usize::from(stage == 8);
    let d2_data = if c2 == 1 { vec![ri(1); 3] } else { vec![] };
    let d2 = BasicMatrix::from_row_major(edges_len, c2, d2_data).map_err(|e| e.to_string())?;
    let _complex = omega_homology::chain_complex::ChainComplex::new(
        vertices,
        edges_len,
        c2,
        d1.clone().into_provider().map_err(|e| e.to_string())?,
        d2.clone().into_provider().map_err(|e| e.to_string())?,
    )
    .map_err(|e| e.to_string())?;
    let rank = d1.rank().map_err(|e| e.to_string())?;
    let d2_rank = d2.rank().map_err(|e| e.to_string())?;
    Ok((vertices - rank, d2.rows() - rank - d2_rank))
}

pub fn carrier_stage(stage: usize) -> Result<CarrierStage, String> {
    let (vertices, edges) = stage_graph(stage)?;
    let (boundary, d1) = build_stage_boundary(vertices, &edges)?;
    let (betti_h0, betti_h1) = compute_stage_betti(vertices, edges.len(), stage, &d1)?;
    let vertex_automorphisms = count_vertex_automorphisms(vertices, &edges)?;
    let automorphism_order = vertex_automorphisms * if stage == 4 { 2 } else { 1 };
    Ok(CarrierStage {
        stage,
        vertices,
        edges,
        boundary,
        betti_h0,
        betti_h1,
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
    let gv = crate::linear_algebra::matrix::multiply_vector(g, v).map_err(|e| e.to_string())?;
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

fn is_basis_orthogonal_2(g: &BasicMatrix<G>) -> Result<bool, String> {
    Ok(form(g, &basis_vector(2, 0), &basis_vector(2, 1))?.is_zero())
}

fn diag_2_proportional(g1: &BasicMatrix<G>, g2: &BasicMatrix<G>) -> Result<bool, String> {
    let a = g1.get_ref(0, 0).map_err(|e| e.to_string())?;
    let d = g2.get_ref(1, 1).map_err(|e| e.to_string())?;
    let b = g1.get_ref(1, 1).map_err(|e| e.to_string())?;
    let c = g2.get_ref(0, 0).map_err(|e| e.to_string())?;
    Ok(a.mul(d) == b.mul(c))
}

fn both_orthogonal_and_unequal_on(
    g1: &BasicMatrix<G>,
    g2: &BasicMatrix<G>,
) -> Result<bool, String> {
    let o1 = is_basis_orthogonal_2(g1)?;
    let o2 = is_basis_orthogonal_2(g2)?;
    let on1 = basis_orthonormal(g1, 2)?;
    let on2 = basis_orthonormal(g2, 2)?;
    Ok(o1 && o2 && on1 && !on2)
}

fn gram_form_not_unique() -> Result<bool, String> {
    use crate::linear_algebra::matrix::diagonal;
    use crate::linear_algebra::ordered::hermitian_is_positive_definite as is_positive_definite;
    let g1 = diagonal(&[G::one(), G::one()]).map_err(|e| e.to_string())?;
    let g2 = diagonal(&[G::one(), G::from_ints(2, 0)]).map_err(|e| e.to_string())?;
    let proportional = diag_2_proportional(&g1, &g2)?;
    let pd_both = is_positive_definite(&g1).map_err(|e| e.to_string())?
        && is_positive_definite(&g2).map_err(|e| e.to_string())?;
    let orth_and_on = both_orthogonal_and_unequal_on(&g1, &g2)?;
    Ok(pd_both && !proportional && orth_and_on)
}

fn subset_is_orthonormal(
    identity: &BasicMatrix<G>,
    labels: usize,
    members: &[usize],
) -> Result<bool, String> {
    let mut orthonormal = true;
    for &a in members {
        for &b in members {
            let expected = if a == b { G::one() } else { G::zero() };
            let val = form(identity, &basis_vector(labels, a), &basis_vector(labels, b))?;
            orthonormal &= val == expected;
        }
    }
    Ok(orthonormal)
}

fn count_orthonormal_frames(
    identity: &BasicMatrix<G>,
    labels: usize,
    size: usize,
) -> Result<usize, String> {
    let mut count = 0;
    for subset in 0u32..(1u32 << labels) {
        let members: Vec<usize> = (0..labels).filter(|&q| (subset >> q) & 1 == 1).collect();
        if members.len() == size && subset_is_orthonormal(identity, labels, &members)? {
            count += 1;
        }
    }
    Ok(count)
}

fn two_label_dimension_below_three(labels: usize) -> Result<bool, String> {
    if labels > 16 {
        return Err("LABEL_BUDGET_EXCEEDED".into());
    }
    let identity = crate::linear_algebra::matrix::identity(labels).map_err(|e| e.to_string())?;
    let f_labels = count_orthonormal_frames(&identity, labels, labels)?;
    let f_three = count_orthonormal_frames(&identity, labels, 3)?;
    Ok(labels < 3 && f_labels == 1 && f_three == 0)
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

fn gauss_mat2(rows: [[(i64, i64); 2]; 2]) -> Result<BasicMatrix<G>, String> {
    crate::linear_algebra::matrix::from_rows(
        rows.iter()
            .map(|r| r.iter().map(|&(a, b)| G::from_ints(a, b)).collect())
            .collect(),
    )
    .map_err(|e| e.to_string())
}

fn matrices_anticommute(a: &BasicMatrix<G>, b: &BasicMatrix<G>) -> Result<bool, String> {
    use crate::linear_algebra::matrix as mx;
    let ab = mx::multiply(a, b).map_err(|e| e.to_string())?;
    let ba = mx::multiply(b, a).map_err(|e| e.to_string())?;
    let sum = mx::add(&ab, &ba).map_err(|e| e.to_string())?;
    mx::is_zero_matrix(&sum).map_err(|e| e.to_string())
}

fn is_pauli_like(
    r: &BasicMatrix<G>,
    x: &BasicMatrix<G>,
    z: &BasicMatrix<G>,
    identity: &BasicMatrix<G>,
) -> Result<bool, String> {
    use crate::linear_algebra::{involution as star, matrix as mx};
    let adj = star::adjoint(r).map_err(|e| e.to_string())?;
    let sq = mx::multiply(r, r).map_err(|e| e.to_string())?;
    let ax = matrices_anticommute(r, x)?;
    let az = matrices_anticommute(r, z)?;
    Ok(adj == *r && sq == *identity && ax && az)
}

fn check_real_pauli_candidate(
    code: i64,
    x: &BasicMatrix<G>,
    z: &BasicMatrix<G>,
    identity: &BasicMatrix<G>,
) -> Result<(usize, usize), String> {
    use crate::linear_algebra::matrix as mx;
    let p0 = code % 3 - 1;
    let p1 = (code / 3) % 3 - 1;
    let p2 = (code / 9) % 3 - 1;
    let r = gauss_mat2([[(p0, 0), (p1, 0)], [(p1, 0), (p2, 0)]])?;
    let full = usize::from(is_pauli_like(&r, x, z, identity)?);
    let sq = mx::multiply(&r, &r).map_err(|e| e.to_string())?;
    let az = matrices_anticommute(&r, z)?;
    let no_x = usize::from(sq == *identity && az);
    Ok((full, no_x))
}

fn build_pauli_xzy() -> Result<(BasicMatrix<G>, BasicMatrix<G>, BasicMatrix<G>), String> {
    let x = gauss_mat2([[(0, 0), (1, 0)], [(1, 0), (0, 0)]])?;
    let z = gauss_mat2([[(1, 0), (0, 0)], [(0, 0), (-1, 0)]])?;
    let y = gauss_mat2([[(0, 0), (0, -1)], [(0, 1), (0, 0)]])?;
    Ok((x, z, y))
}

fn pauli_y_requires_imaginary_coefficients() -> Result<bool, String> {
    use crate::linear_algebra::matrix as mx;
    let (x, z, y) = build_pauli_xzy()?;
    let identity = mx::identity(2).map_err(|e| e.to_string())?;
    let y_ok =
        is_pauli_like(&y, &x, &z, &identity)? && y.as_slice().iter().any(|e| !e.im.is_zero());
    let mut real_solutions = 0;
    let mut without_x = 0;
    for code in 0..27i64 {
        let (full, no_x) = check_real_pauli_candidate(code, &x, &z, &identity)?;
        real_solutions += full;
        without_x += no_x;
    }
    Ok(y_ok && real_solutions == 0 && without_x > 0)
}

fn build_perm_lift_2x2(p: &[usize]) -> Result<BasicMatrix<G>, String> {
    let mut lift = crate::linear_algebra::matrix::zeros::<G>(2, 2).map_err(|e| e.to_string())?;
    for (j, &image) in p.iter().enumerate() {
        lift.set(image, j, G::one()).map_err(|e| e.to_string())?;
    }
    Ok(lift)
}

fn is_isometry_2x2(m: &BasicMatrix<G>, identity: &BasicMatrix<G>) -> Result<bool, String> {
    use crate::linear_algebra::{involution as star, matrix as mx};
    let adj = star::adjoint(m).map_err(|e| e.to_string())?;
    let prod = mx::multiply(&adj, m).map_err(|e| e.to_string())?;
    Ok(prod == *identity)
}

fn build_iswap_2x2() -> Result<BasicMatrix<G>, String> {
    let mut i_swap = crate::linear_algebra::matrix::zeros(2, 2).map_err(|e| e.to_string())?;
    i_swap.set(0, 1, G::i()).map_err(|e| e.to_string())?;
    i_swap.set(1, 0, G::i()).map_err(|e| e.to_string())?;
    Ok(i_swap)
}

fn collect_reversible_lifts_2x2(
    reversible: &[Vec<usize>],
    identity: &BasicMatrix<G>,
) -> Result<(Vec<BasicMatrix<G>>, bool), String> {
    let mut lifts = Vec::with_capacity(reversible.len());
    let mut all_lifts_isometric = true;
    for p in reversible {
        let lift = build_perm_lift_2x2(p)?;
        all_lifts_isometric &= is_isometry_2x2(&lift, identity)?;
        lifts.push(lift);
    }
    Ok((lifts, all_lifts_isometric))
}

fn permutation_isometry_envelope_strict() -> Result<bool, String> {
    use crate::linear_algebra::matrix as mx;
    let reversible = permutations(2)?;
    let identity = mx::identity(2).map_err(|e| e.to_string())?;
    let (lifts, all_lifts_isometric) = collect_reversible_lifts_2x2(&reversible, &identity)?;
    let i_swap = build_iswap_2x2()?;
    let i_swap_iso = is_isometry_2x2(&i_swap, &identity)?;
    Ok(reversible.len() == 2 && all_lifts_isometric && i_swap_iso && !lifts.contains(&i_swap))
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

fn parse_carrier_and_update(input: &Value) -> Result<(PresentedCarrier, Vec<usize>), String> {
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
    Ok((carrier, update))
}

fn check_mix_scale_for_pair(ar: i64, ai: i64, br: i64, bi: i64) -> Result<bool, String> {
    let v = [G::from_ints(ar, ai), G::from_ints(br, bi)];
    let before: Q = phase_blind(&v)?.into_iter().sum();
    let after: Q = phase_blind(&mix(&v))?.into_iter().sum();
    Ok(after == ri(2) * before)
}

fn check_mix_scales_on_box() -> Result<(usize, bool), String> {
    let mut scale_checks = 0;
    let mut scales_preserved = true;
    for idx in 0..625i64 {
        let ar = (idx % 5) - 2;
        let ai = ((idx / 5) % 5) - 2;
        let br = ((idx / 25) % 5) - 2;
        let bi = ((idx / 125) % 5) - 2;
        scales_preserved &= check_mix_scale_for_pair(ar, ai, br, bi)?;
        scale_checks += 1;
    }
    Ok((scale_checks, scales_preserved))
}

fn verify_permutation_lifts_preserve_pairing() -> Result<bool, String> {
    let report_permutations = permutations(4)?;
    let x = [ri(2), ri(-1), ri(3), ri(4)];
    let y = [ri(7), ri(2), ri(-3), ri(1)];
    let expected: Q = x.iter().zip(&y).map(|(a, b)| a * b).sum();
    for p in &report_permutations {
        let lx: Vec<G> = p.iter().map(|&i| G::from_rational(x[i].clone())).collect();
        let ly: Vec<G> = p.iter().map(|&i| G::from_rational(y[i].clone())).collect();
        if gaussian_pairing(&lx, &ly)?.re != expected {
            return Ok(false);
        }
    }
    Ok(true)
}

fn build_power_comparisons() -> Vec<Value> {
    (1u32..=4)
        .map(|p| {
            let (basis_ratio, plus_ratio) = power_readout_ratios(p);
            json!({
                "power": p,
                "basis_ratio": format!("{}/{}", basis_ratio.numer(), basis_ratio.denom()),
                "plus_ratio": crate::qm::finite_witness::qstr(&plus_ratio),
                "uniform_scale_two": basis_ratio == plus_ratio
            })
        })
        .collect()
}

fn count_dilations(pairs: &[Vec<usize>]) -> (usize, usize) {
    let identity_dilations = pairs
        .iter()
        .filter(|p| (0..4).all(|x| p[x] / 2 == x / 2))
        .count();
    let collapse_dilations = pairs
        .iter()
        .filter(|p| (0..2).all(|q| p[q * 2] / 2 == 0))
        .count();
    (identity_dilations, collapse_dilations)
}

fn build_structural_checks(
    weights: &[Q],
    pushed: &[Q],
    w_a: &[Q],
    w_b: &[Q],
    mixed_a: &[Q],
    mixed_b: &[Q],
    scales_preserved: bool,
    identity_dilations: usize,
    collapse_dilations: usize,
    probabilities: &[Q],
) -> Result<Value, String> {
    let bool_maps: Vec<Vec<usize>> = (0..4).map(|m| vec![m & 1, (m >> 1) & 1]).collect();
    let no_half_step = bool_maps.iter().all(|p| (0..2).any(|q| p[p[q]] != 1 - q));
    let two_reversibles = bool_maps.iter().filter(|p| reversible(p)).count() == 2;
    let plus_i = G::from_ints(1, 1);
    let inv = plus_i.inv();
    let bell = [ri(1), ri(0), ri(0), ri(1)];
    let u = [ri(1), ri(0)];
    let v = [ri(0), ri(1)];
    let fixed_carrier = PresentedCarrier::new(vec![0, 0, 1, 1], 2)?;
    let report_weights = [ri(1), ri(4)];
    let lifted_weights: Vec<_> = fixed_carrier
        .report
        .iter()
        .map(|&i| report_weights[i].clone())
        .collect();
    let pushed_lifted = fixed_carrier.push_weights(&lifted_weights)?;
    let expected_double: Vec<_> = report_weights.iter().map(|x| x * ri(2)).collect();
    let bell_splits_fiber =
        fixed_carrier.report[0] == fixed_carrier.report[1] && bell[0] != bell[1];
    Ok(json!({
        "mass_preserved": weights.iter().cloned().sum::<Q>() == pushed.iter().cloned().sum::<Q>(),
        "integer_weights_at_declared_scale": integer_weights_at_declared_scale()?,
        "permutation_lifts_preserve_pairing": verify_permutation_lifts_preserve_pairing()?,
        "presentation_push_recovers_double": pushed_lifted == expected_double,
        "bell_not_along_presentation": bell_splits_fiber,
        "collapse_not_reversible": !reversible(&[0, 0]),
        "two_bool_reversibles": two_reversibles,
        "phase_fiber_equal": w_a == w_b,
        "mixing_separates_fiber": mixed_a != mixed_b,
        "mix_doubles_weight_on_enumerated_box": scales_preserved,
        "four_identity_dilations": identity_dilations == 4,
        "four_collapse_dilations": collapse_dilations == 4,
        "no_report_half_step": no_half_step,
        "gaussian_integer_nonunit": !inv.is_integer_ring_element() && plus_i.mul(&inv) == G::one(),
        "tensor_rival_disagrees": tensor2(&u, &v) != dump_right(&u, &v),
        "bell_nonproduct": !entanglement_determinant(&bell).is_zero(),
        "phase_extra_does_not_select_circle": phase_extra_does_not_select_circle(),
        "unit_total_pairing_rivals": unit_total_pairing_rivals()?,
        "fractional_half_weights": fractional_half_weights(),
        "pauli_y_requires_imaginary_coefficients": pauli_y_requires_imaginary_coefficients()?,
        "two_label_dimension_below_three": two_label_dimension_below_three(fixed_carrier.labels)?,
        "normalization": probabilities.iter().cloned().sum::<Q>() == ri(1),
        "gaussian_operator_composition_and_adjoint": gaussian_operator_checks()?,
        "permutation_isometry_envelope_strict": permutation_isometry_envelope_strict()?,
        "gram_form_not_unique": gram_form_not_unique()?,
        "self_adjoint_spectral_field_obstruction": crate::qm::entropy_bounds::splitting_degree_2(&ri(0), &ri(-2)) == 2
    }))
}

fn compute_fiber_mixing() -> Result<(Vec<Q>, Vec<Q>, Vec<Q>, Vec<Q>, usize, bool), String> {
    let a = [G::from_ints(1, 0), G::from_ints(1, 0)];
    let b = [G::from_ints(1, 0), G::from_ints(-1, 0)];
    let w_a = phase_blind(&a)?;
    let w_b = phase_blind(&b)?;
    let mixed_a = phase_blind(&mix(&a))?;
    let mixed_b = phase_blind(&mix(&b))?;
    let (scale_checks, scales_preserved) = check_mix_scales_on_box()?;
    Ok((w_a, w_b, mixed_a, mixed_b, scale_checks, scales_preserved))
}

pub fn run(input: &Value) -> Result<Value, String> {
    let (carrier, update) = parse_carrier_and_update(input)?;
    let descent = carrier.descend(&update)?;
    let weights = vec![rq(1, 2); carrier.report.len()];
    let pushed = carrier.push_weights(&weights)?;
    let pairs = permutations(4)?;
    let (identity_dilations, collapse_dilations) = count_dilations(&pairs);
    let (w_a, w_b, mixed_a, mixed_b, scale_checks, scales_preserved) = compute_fiber_mixing()?;
    let powers = build_power_comparisons();
    let stages = (0..=8).map(carrier_stage).collect::<Result<Vec<_>, _>>()?;
    let psi = [G::from_ints(1, 0), G::from_ints(0, 1), G::from_ints(1, -1)];
    let probabilities = born_probabilities(&psi)?;
    let checks = build_structural_checks(
        &weights,
        &pushed,
        &w_a,
        &w_b,
        &mixed_a,
        &mixed_b,
        scales_preserved,
        identity_dilations,
        collapse_dilations,
        &probabilities,
    )?;
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
fn verify_basis_columns(op: &GaussianOperator, a: &[Vec<G>]) -> Result<bool, String> {
    let n = a.len();
    let mut valid = true;
    for j in 0..n {
        let mut basis = vec![G::zero(); n];
        basis[j] = G::one();
        let column = op.apply(&basis)?;
        valid &= (0..n).all(|i| column[i] == a[i][j]);
    }
    Ok(valid)
}

fn check_operator_pairing_and_comp(op: &GaussianOperator, n: usize) -> Result<bool, String> {
    let v: Vec<_> = (0..n).map(|i| G::from_ints(i as i64, 1)).collect();
    let w: Vec<_> = (0..n).map(|i| G::from_ints(1, -(i as i64))).collect();
    let adj = op.adjoint();
    let comp_v = op.compose(&adj)?.apply(&v)?;
    let step_v = op.apply(&adj.apply(&v)?)?;
    let pair_lhs = gaussian_pairing(&op.apply(&v)?, &w)?;
    let pair_rhs = gaussian_pairing(&v, &adj.apply(&w)?)?;
    Ok(comp_v == step_v && pair_lhs == pair_rhs)
}

fn check_gaussian_operator_dim(n: usize) -> Result<bool, String> {
    let a: Vec<Vec<G>> = (0..n)
        .map(|i| {
            (0..n)
                .map(|j| G::from_ints((i + j) as i64, (i as i64) - (j as i64)))
                .collect()
        })
        .collect();
    let op = GaussianOperator::new(&a)?;
    let pair_ok = check_operator_pairing_and_comp(&op, n)?;
    let cols_ok = verify_basis_columns(&op, &a)?;
    Ok(pair_ok && cols_ok)
}

fn gaussian_operator_checks() -> Result<bool, String> {
    let valid_2 = check_gaussian_operator_dim(2)?;
    let valid_4 = check_gaussian_operator_dim(4)?;
    let h = GaussianOperator::new(&vec![
        vec![G::one(), G::one()],
        vec![G::one(), G::from_ints(-1, 0)],
    ])?;
    let twice = GaussianOperator::new(&vec![
        vec![G::from_ints(2, 0), G::zero()],
        vec![G::zero(), G::from_ints(2, 0)],
    ])?;
    let h_sq_ok = h.adjoint().compose(&h)? == twice;
    Ok(valid_2 && valid_4 && h_sq_ok)
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
        use crate::linear_algebra::ordered::hermitian_is_positive_definite as is_positive_definite;
        assert!(
            !is_positive_definite(&diagonal(&[G::one(), G::from_ints(-1, 0)]).unwrap()).unwrap()
        );
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
