//! Explicit public rays/contexts in; computed complete census and witnesses out.
use std::io::{self, BufRead};
use tfqm_finite_probability::cabello_certificates::certify;
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let n: usize = f[1].parse().unwrap();
        let d: usize = f[2].parse().unwrap();
        let m: usize = f[3].parse().unwrap();
        let budget: usize = f[4].parse().unwrap();
        let radius: i64 = f[5].parse().unwrap();
        assert_eq!(f.len(), 6 + n * d + m * d);
        let rays = f[6..6 + n * d]
            .chunks(d)
            .map(|r| r.iter().map(|x| x.parse::<i64>().unwrap()).collect())
            .collect();
        let frames = f[6 + n * d..]
            .chunks(d)
            .map(|r| r.iter().map(|x| x.parse::<usize>().unwrap()).collect())
            .collect();
        let c = certify(rays, frames, budget, radius).unwrap();
        println!(
            "census\t{}\t{}\t{}\t{}\t{}\t{}",
            c.basis_supports_examined,
            c.incidence_rank,
            c.projector_span_rank,
            c.vertices.len(),
            c.at_minus_half,
            c.above_minus_quarter
        );
        for (i, v) in c.vertices.iter().enumerate() {
            print!("vertex_{}", i);
            for q in v.weights.iter().chain(v.representative.iter().flatten()) {
                print!("\t{}", q);
            }
            for x in v.negative_vector {
                print!("\t{}", x);
            }
            print!(
                "\t{}\t{}\t{}",
                v.quadratic_value, v.spectral_class, v.half_shift_determinant
            );
            for q in &v.quarter_shift_leading_minors {
                print!("\t{}", q);
            }
            print!("\t{}", v.denominator);
            for x in v.matrix_numerators.iter().chain(&v.weights_twice) {
                print!("\t{}", x);
            }
            println!("\t{}", v.negative_value_numerator);
        }
    }
}
