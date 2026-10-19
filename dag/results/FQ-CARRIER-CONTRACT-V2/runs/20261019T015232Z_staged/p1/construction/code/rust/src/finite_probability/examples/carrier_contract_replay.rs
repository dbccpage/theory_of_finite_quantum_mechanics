use num_bigint::BigInt;
use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::carrier_contract::{certify_sample, label_lcm};
fn q(s: &str) -> Q {
    let (n, d) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(n.parse::<BigInt>().unwrap(), d.parse::<BigInt>().unwrap())
}
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        if f[0] == "inventory" {
            let n: usize = f[1].parse().unwrap();
            assert_eq!(f.len(), 2 + 2 * n);
            let ids: Vec<usize> = f[2..2 + n].iter().map(|x| x.parse().unwrap()).collect();
            let cs: Vec<usize> = f[2 + n..].iter().map(|x| x.parse().unwrap()).collect();
            let mut distinct = cs.clone();
            distinct.sort();
            distinct.dedup();
            print!("inventory\t{}", label_lcm(&cs).unwrap());
            for x in ids.iter().chain(&cs).chain(&distinct) {
                print!("\t{}", x);
            }
            println!();
            continue;
        }
        let n: usize = f[1].parse().unwrap();
        let mid: usize = f[2].parse().unwrap();
        let target: usize = f[3].parse().unwrap();
        let d: usize = f[4].parse().unwrap();
        assert_eq!(f.len(), 5 + 2 * d);
        let c = certify_sample(
            n,
            mid,
            target,
            f[5..5 + d].iter().map(|x| q(x)).collect(),
            f[5 + d..].iter().map(|x| q(x)).collect(),
        )
        .unwrap();
        print!("{}\t{}\t{}\t{}", f[0], c.source, c.intermediate, c.target);
        for x in c.source_polynomial.iter().chain(&c.target_polynomial) {
            print!("\t{}", x);
        }
        for a in &c.arrays {
            for x in a {
                print!("\t{}", x);
            }
        }
        println!();
    }
    println!("declaration_boundary\tfalse\tDECLARED\tfalse\tfalse");
}
