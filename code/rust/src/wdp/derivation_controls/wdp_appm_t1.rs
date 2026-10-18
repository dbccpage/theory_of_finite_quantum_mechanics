//! Exact witness for the finite carrier in `derivation.md`.
//!
//! Sites are `(Z/4Z)^2`. Configurations are the two orientations of each
//! 4-cycle: 16 faces and 8 generator cycles. The selected hypotheses are
//! `A=1`, `s=+1`, and `m=(W_x+W_y) mod 2`. The partition is not the 1D trace 912.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub sites: i64,
    pub cycles: i64,
    pub faces: i64,
    pub generators: i64,
    pub orientations: i64,
    pub z: i64,
    pub n: i64,
    pub average_sign: (i64, i64),
    pub expectation: (i64, i64),
}

fn edge(a: (i32, i32), b: (i32, i32)) -> ((i32, i32), (i32, i32)) {
    if a <= b { (a, b) } else { (b, a) }
}

fn face(x: i32, y: i32) -> [((i32, i32), (i32, i32)); 4] {
    let mut edges = [
        edge((x, y), ((x + 1) % 4, y)),
        edge(((x + 1) % 4, y), ((x + 1) % 4, (y + 1) % 4)),
        edge(((x + 1) % 4, (y + 1) % 4), (x, (y + 1) % 4)),
        edge((x, (y + 1) % 4), (x, y)),
    ];
    edges.sort_unstable();
    edges
}

fn row(y: i32) -> [((i32, i32), (i32, i32)); 4] {
    let mut edges = [
        edge((0, y), (1, y)),
        edge((1, y), (2, y)),
        edge((2, y), (3, y)),
        edge((3, y), (0, y)),
    ];
    edges.sort_unstable();
    edges
}

fn col(x: i32) -> [((i32, i32), (i32, i32)); 4] {
    let mut edges = [
        edge((x, 0), (x, 1)),
        edge((x, 1), (x, 2)),
        edge((x, 2), (x, 3)),
        edge((x, 3), (x, 0)),
    ];
    edges.sort_unstable();
    edges
}

fn orbit_sums(meron_bit: i64) -> (i64, i64) {
    let mut partition = 0;
    let mut numerator = 0;
    for orientation in [0_i64, 1] {
        let weight = if (meron_bit * orientation) % 2 == 0 { 1 } else { -1 };
        let observable = if orientation == 0 { 1 } else { -1 };
        partition += weight;
        numerator += weight * observable;
    }
    (partition, numerator)
}

fn distinct(cycles: &[[((i32, i32), (i32, i32)); 4]]) -> bool {
    for i in 0..cycles.len() {
        for j in (i + 1)..cycles.len() {
            if cycles[i] == cycles[j] {
                return false;
            }
        }
    }
    true
}

pub fn witness() -> Witness {
    let mut faces = Vec::with_capacity(16);
    let mut generators = Vec::with_capacity(8);
    for x in 0..4 {
        for y in 0..4 {
            faces.push(face(x, y));
        }
    }
    for y in 0..4 {
        generators.push(row(y));
    }
    for x in 0..4 {
        generators.push(col(x));
    }
    let mut cycles = faces.clone();
    cycles.extend(generators.iter().copied());
    assert!(distinct(&cycles), "4-cycle edge sets are not distinct");
    let (face_partition, face_numerator) = orbit_sums(0);
    let (generator_partition, generator_numerator) = orbit_sums(1);
    let z = faces.len() as i64 * face_partition + generators.len() as i64 * generator_partition;
    let n = faces.len() as i64 * face_numerator + generators.len() as i64 * generator_numerator;
    let orientations = 2 * cycles.len() as i64;
    Witness {
        sites: 16,
        cycles: cycles.len() as i64,
        faces: faces.len() as i64,
        generators: generators.len() as i64,
        orientations,
        z,
        n,
        average_sign: (z / gcd(z, orientations), orientations / gcd(z, orientations)),
        expectation: (n / gcd(n, z), z / gcd(n, z)),
    }
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let rest = a % b;
        a = b;
        b = rest;
    }
    a
}

pub fn reject_pinned_scalar(value: i64) -> Result<(), &'static str> {
    if value == 912 {
        Err("the 1D trace 912 is not the partition of this carrier")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{col, face, reject_pinned_scalar, row, witness};

    #[test]
    fn origin_face_and_row_are_labelled() {
        assert_eq!(
            face(0, 0),
            [
                ((0, 0), (0, 1)),
                ((0, 0), (1, 0)),
                ((0, 1), (1, 1)),
                ((1, 0), (1, 1)),
            ]
        );
        assert_eq!(
            row(0),
            [
                ((0, 0), (1, 0)),
                ((0, 0), (3, 0)),
                ((1, 0), (2, 0)),
                ((2, 0), (3, 0)),
            ]
        );
        assert_eq!(
            col(0),
            [
                ((0, 0), (0, 1)),
                ((0, 0), (0, 3)),
                ((0, 1), (0, 2)),
                ((0, 2), (0, 3)),
            ]
        );
    }

    #[test]
    fn exact_partition_and_numerator() {
        let result = witness();
        assert_eq!(result.sites, 16);
        assert_eq!(result.cycles, 24);
        assert_eq!(result.faces, 16);
        assert_eq!(result.generators, 8);
        assert_eq!(result.orientations, 48);
        assert_eq!(result.z, 32);
        assert_eq!(result.n, 16);
        assert_eq!(result.average_sign, (2, 3));
        assert_eq!(result.expectation, (1, 2));
    }

    #[test]
    fn pinned_one_dimensional_trace_is_refused() {
        assert!(reject_pinned_scalar(912).is_err());
        assert!(reject_pinned_scalar(witness().z).is_ok());
    }
}
