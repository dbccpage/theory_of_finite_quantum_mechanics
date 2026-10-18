//! Exact witness for the 3D winding, linking, and character-orthogonality carrier in `derivation.md`.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub sites: i64,
    pub cycles: i64,
    pub plaquettes: i64,
    pub generators: i64,
    pub orientations: i64,
    pub z: i64,
    pub n: i64,
    pub average_sign: (i64, i64),
    pub expectation: (i64, i64),
    pub hopf_linking: i64,
    pub reversed_linking: i64,
    pub shifted_linking: i64,
    pub trivial_character_sum: i64,
    pub max_nontrivial_character_residual: i64,
}

type Point3 = (i32, i32, i32);
type Edge3 = (Point3, Point3);

fn edge(a: Point3, b: Point3) -> Edge3 {
    if a <= b { (a, b) } else { (b, a) }
}

fn sorted4(mut edges: [Edge3; 4]) -> [Edge3; 4] {
    edges.sort_unstable();
    edges
}

pub fn plaquettes_3d() -> Vec<[Edge3; 4]> {
    let mut out = Vec::with_capacity(192);
    for x in 0..4 {
        for y in 0..4 {
            for z in 0..4 {
                let xp = (x + 1) % 4;
                let yp = (y + 1) % 4;
                let zp = (z + 1) % 4;
                // xy plaquette
                out.push(sorted4([
                    edge((x, y, z), (xp, y, z)),
                    edge((xp, y, z), (xp, yp, z)),
                    edge((xp, yp, z), (x, yp, z)),
                    edge((x, yp, z), (x, y, z)),
                ]));
                // yz plaquette
                out.push(sorted4([
                    edge((x, y, z), (x, yp, z)),
                    edge((x, yp, z), (x, yp, zp)),
                    edge((x, yp, zp), (x, y, zp)),
                    edge((x, y, zp), (x, y, z)),
                ]));
                // zx plaquette
                out.push(sorted4([
                    edge((x, y, z), (x, y, zp)),
                    edge((x, y, zp), (xp, y, zp)),
                    edge((xp, y, zp), (xp, y, z)),
                    edge((xp, y, z), (x, y, z)),
                ]));
            }
        }
    }
    out
}

pub fn generators_3d() -> Vec<[Edge3; 4]> {
    let mut out = Vec::with_capacity(48);
    for a in 0..4 {
        for b in 0..4 {
            out.push(sorted4([
                edge((0, a, b), (1, a, b)),
                edge((1, a, b), (2, a, b)),
                edge((2, a, b), (3, a, b)),
                edge((3, a, b), (0, a, b)),
            ]));
            out.push(sorted4([
                edge((a, 0, b), (a, 1, b)),
                edge((a, 1, b), (a, 2, b)),
                edge((a, 2, b), (a, 3, b)),
                edge((a, 3, b), (a, 0, b)),
            ]));
            out.push(sorted4([
                edge((a, b, 0), (a, b, 1)),
                edge((a, b, 1), (a, b, 2)),
                edge((a, b, 2), (a, b, 3)),
                edge((a, b, 3), (a, b, 0)),
            ]));
        }
    }
    out
}

fn distinct(cycles: &[[Edge3; 4]]) -> bool {
    for i in 0..cycles.len() {
        for j in (i + 1)..cycles.len() {
            if cycles[i] == cycles[j] {
                return false;
            }
        }
    }
    true
}

pub fn linking_with_square_patch(directed_edges: &[(Point3, Point3)]) -> Result<i64, &'static str> {
    let mut total = 0_i64;
    for &(u, v) in directed_edges {
        for p in [u, v] {
            if p.2 == 0 && (0..=2).contains(&p.0) && (0..=2).contains(&p.1) {
                if p.0 == 0 || p.0 == 2 || p.1 == 0 || p.1 == 2 {
                    return Err("loop intersects boundary C1 of spanning square");
                }
            }
        }
        if u.0 == v.0 && u.1 == v.1 && (1..2).contains(&u.0) && (1..2).contains(&u.1) {
            if u.2 == 0 && v.2 == 1 {
                total += 1;
            } else if u.2 == 1 && v.2 == 0 {
                total -= 1;
            }
        }
    }
    Ok(total)
}

pub fn hopf_loop(shift_x: i32, reverse: bool) -> Vec<(Point3, Point3)> {
    let pts = [
        (1 + shift_x, 1, -1),
        (1 + shift_x, 1, 0),
        (1 + shift_x, 1, 1),
        (3 + shift_x, 1, 1),
        (3 + shift_x, 1, 0),
        (3 + shift_x, 1, -1),
    ];
    let mut edges = Vec::with_capacity(pts.len());
    for i in 0..pts.len() {
        let a = pts[i];
        let b = pts[(i + 1) % pts.len()];
        if reverse {
            edges.push((b, a));
        } else {
            edges.push((a, b));
        }
    }
    edges
}

pub fn parity_character_sum(kx: i32, ky: i32, kz: i32) -> i64 {
    let mut total = 0_i64;
    for x in 0..4 {
        for y in 0..4 {
            for z in 0..4 {
                let dot = kx * x + ky * y + kz * z;
                total += if dot.rem_euclid(2) == 0 { 1 } else { -1 };
            }
        }
    }
    total
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

pub fn witness() -> Witness {
    let plaq = plaquettes_3d();
    let gen = generators_3d();
    let mut all = plaq.clone();
    all.extend(gen.iter().copied());
    assert!(distinct(&all), "3D 4-cycle edge sets must be distinct");
    let z = plaq.len() as i64 * 2;
    let n = gen.len() as i64 * 2;
    let orientations = 2 * all.len() as i64;
    let g_sign = gcd(z, orientations);
    let g_exp = gcd(n, z);
    let mut max_nontrivial = 0_i64;
    for kx in 0..2 {
        for ky in 0..2 {
            for kz in 0..2 {
                if (kx, ky, kz) != (0, 0, 0) {
                    max_nontrivial = max_nontrivial.max(parity_character_sum(kx, ky, kz).abs());
                }
            }
        }
    }
    Witness {
        sites: 64,
        cycles: all.len() as i64,
        plaquettes: plaq.len() as i64,
        generators: gen.len() as i64,
        orientations,
        z,
        n,
        average_sign: (z / g_sign, orientations / g_sign),
        expectation: (n / g_exp, z / g_exp),
        hopf_linking: linking_with_square_patch(&hopf_loop(0, false)).unwrap(),
        reversed_linking: linking_with_square_patch(&hopf_loop(0, true)).unwrap(),
        shifted_linking: linking_with_square_patch(&hopf_loop(2, false)).unwrap(),
        trivial_character_sum: parity_character_sum(0, 0, 0),
        max_nontrivial_character_residual: max_nontrivial,
    }
}

pub fn reject_pinned_t3_string_only_claim(claim: &str) -> Result<(), &'static str> {
    if claim.contains("10^-25") || claim.contains("Dirac functional determinant") {
        Err("pinned string labels and 10^-25 residual are not derived from this 3D carrier")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{
        hopf_loop, linking_with_square_patch, reject_pinned_t3_string_only_claim, witness,
    };

    #[test]
    fn exact_3d_torus_cycles_and_linking() {
        let w = witness();
        assert_eq!(w.sites, 64);
        assert_eq!(w.cycles, 240);
        assert_eq!(w.plaquettes, 192);
        assert_eq!(w.generators, 48);
        assert_eq!(w.orientations, 480);
        assert_eq!(w.z, 384);
        assert_eq!(w.n, 96);
        assert_eq!(w.average_sign, (4, 5));
        assert_eq!(w.expectation, (1, 4));
        assert_eq!(w.hopf_linking, 1);
        assert_eq!(w.reversed_linking, -1);
        assert_eq!(w.shifted_linking, 0);
        assert_eq!(w.trivial_character_sum, 64);
        assert_eq!(w.max_nontrivial_character_residual, 0);
    }

    #[test]
    fn boundary_collision_and_pinned_claims_refuse() {
        let mut bad = hopf_loop(0, false);
        bad[0] = ((0, 0, 0), (0, 0, 1));
        assert!(linking_with_square_patch(&bad).is_err());
        assert!(reject_pinned_t3_string_only_claim("residual 10^-25").is_err());
    }
}
