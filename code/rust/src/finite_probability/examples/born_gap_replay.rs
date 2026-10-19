use num_bigint::BigInt;
use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::born_gap::{dimension, frame, weak_contract};
fn q(s: &str) -> Q {
    let (n, d) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(n.parse::<BigInt>().unwrap(), d.parse::<BigInt>().unwrap())
}
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let mut out = vec![f[0].to_string(), f[1].to_string()];
        match f[0] {
            "weak" => {
                for x in weak_contract(
                    f[2..4].iter().map(|x| q(x)).collect(),
                    f[4..6].iter().map(|x| q(x)).collect(),
                )
                .unwrap()
                {
                    out.push(x.to_string());
                }
            }
            "dimension" => {
                let ls = f[2..].iter().map(|x| x.to_string()).collect::<Vec<_>>();
                let (a, b, c) = dimension(&ls).unwrap();
                out.extend([a.to_string(), b.to_string(), c.to_string()]);
            }
            "frame" => {
                let n: usize = f[2].parse().unwrap();
                assert_eq!(f.len(), 3 + n + 2 * n * n);
                let psi = f[3..3 + n].iter().map(|x| q(x)).collect();
                let mut at = 3 + n;
                let mut fs = vec![];
                for _ in 0..2 {
                    let mut a = vec![];
                    for _ in 0..n {
                        a.push(f[at..at + n].iter().map(|x| q(x)).collect());
                        at += n;
                    }
                    fs.push(a);
                }
                let c = frame(psi, fs).unwrap();
                out.push(c.dimension.to_string());
                for g in c.grams {
                    for r in g {
                        for x in r {
                            out.push(x.to_string());
                        }
                    }
                }
                for x in c.determinants {
                    out.push(x.to_string());
                }
                for rows in [c.quadratic, c.quartic] {
                    for row in rows {
                        for x in row {
                            out.push(x.to_string());
                        }
                    }
                }
                for x in c.quadratic_sums.into_iter().chain(c.quartic_sums) {
                    out.push(x.to_string());
                }
                out.push(c.deficit.to_string());
            }
            _ => panic!("unknown input"),
        };
        println!("{}", out.join("\t"));
    }
    println!("uniqueness_status\tNOT_DISCHARGED");
}
