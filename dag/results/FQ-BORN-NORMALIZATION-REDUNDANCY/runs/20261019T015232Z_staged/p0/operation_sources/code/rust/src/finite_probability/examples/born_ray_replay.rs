//! Exact weight-ray and amplitude-phase controls from public TSV inputs.
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::born_ray::{born_weights, certify, normalize};
fn parse(s: &str) -> Q {
    let (n, d) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(n.parse::<BigInt>().unwrap(), d.parse::<BigInt>().unwrap())
}
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let n: usize = f[2].parse().unwrap();
        let v: Vec<Q> = f[3..].iter().map(|s| parse(s)).collect();
        print!("{}", f[0]);
        if f[1] == "weights" {
            assert_eq!(v.len(), 2 * n + 1);
            let c = certify(&v[..n], &v[n..2 * n], &v[2 * n]).unwrap();
            print!("\t{}\t{}", c.left_sum, c.right_sum);
            for q in c
                .normalized
                .iter()
                .chain(&c.normalized_twice)
                .chain(&c.normalized_scaled)
            {
                print!("\t{}", q);
            }
            print!(
                "\t{}\t{}",
                if c.same_weight_ray { "true" } else { "false" },
                c.ray_scale
                    .map(|q| q.to_string())
                    .unwrap_or_else(|| "none".into())
            );
            if let Some((i, j, d)) = c.separating_minor {
                println!("\t{}\t{}\t{}", i, j, d);
            } else {
                println!("\tnone\tnone\tnone");
            }
        } else {
            assert_eq!(f[1], "amplitudes");
            assert_eq!(n, 2);
            assert_eq!(v.len(), 4 * n);
            let a: Vec<[Q; 2]> = v[..2 * n]
                .chunks(2)
                .map(|p| [p[0].clone(), p[1].clone()])
                .collect();
            let b: Vec<[Q; 2]> = v[2 * n..]
                .chunks(2)
                .map(|p| [p[0].clone(), p[1].clone()])
                .collect();
            let wa = born_weights(&a).unwrap();
            let wb = born_weights(&b).unwrap();
            for q in wa
                .iter()
                .chain(&wb)
                .chain(&normalize(&wa).unwrap())
                .chain(&normalize(&wb).unwrap())
            {
                print!("\t{}", q);
            }
            let re = &a[0][0] * &b[1][0]
                - &a[0][1] * &b[1][1]
                - (&a[1][0] * &b[0][0] - &a[1][1] * &b[0][1]);
            let im = &a[0][0] * &b[1][1] + &a[0][1] * &b[1][0]
                - (&a[1][0] * &b[0][1] + &a[1][1] * &b[0][0]);
            println!("\t{}\t{}", re, im);
        }
    }
}
