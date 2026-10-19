//! Read explicit two-qubit inputs; emit computed values without expected answers.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::{pfp_exact::Matrix, rational_bell::certify};
fn parse(s: &str) -> Q {
    let (n, d) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(n.parse::<BigInt>().unwrap(), d.parse::<BigInt>().unwrap())
}
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let fields: Vec<_> = line.split('\t').collect();
        assert_eq!(fields.len(), 33);
        let values: Vec<Q> = fields[1..].iter().map(|s| parse(s)).collect();
        let rho: Matrix = values[..16].chunks(4).map(|r| r.to_vec()).collect();
        let mat = |start: usize| -> Matrix {
            values[start..start + 4]
                .chunks(2)
                .map(|r| r.to_vec())
                .collect()
        };
        let c = certify(&rho, &[mat(16), mat(20)], &[mat(24), mat(28)]).unwrap();
        print!("{}", fields[0]);
        for q in c.pairs.iter().flatten().chain(c.correlations.iter()) {
            print!("\t{}", q);
        }
        println!(
            "\t{}\t{}\t{}\t{}\t{}\t{}",
            c.chsh,
            c.minimum_probability,
            c.support_assignments,
            c.separator_lower,
            c.separator_upper,
            c.violating_mask
                .map(|m| m.to_string())
                .unwrap_or_else(|| "none".into())
        );
    }
}
