use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::cabello_obstruction::certify;
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let n: usize = f[1].parse().unwrap();
        let m: usize = f[2].parse().unwrap();
        let cn: usize = f[3].parse().unwrap();
        let cm: usize = f[4].parse().unwrap();
        assert_eq!(f.len(), 5 + 4 * n + 4 * m + 16 + 4 + 4 * cm + cn);
        let mut k = 5;
        let rays = f[k..k + 4 * n]
            .chunks(4)
            .map(|r| r.iter().map(|x| x.parse::<i64>().unwrap()).collect())
            .collect();
        k += 4 * n;
        let frames = f[k..k + 4 * m]
            .chunks(4)
            .map(|r| r.iter().map(|x| x.parse::<usize>().unwrap()).collect())
            .collect();
        k += 4 * m;
        let raw = f[k..k + 16]
            .chunks(4)
            .map(|r| {
                r.iter()
                    .map(|x| Q::from_integer(x.parse::<i64>().unwrap().into()))
                    .collect()
            })
            .collect();
        k += 16;
        let v: [i64; 4] = f[k..k + 4]
            .iter()
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();
        k += 4;
        let ef = f[k..k + 4 * cm]
            .chunks(4)
            .map(|r| r.iter().map(|x| x.parse::<usize>().unwrap()).collect())
            .collect();
        k += 4 * cm;
        let ea = f[k..].iter().map(|x| x.parse::<i64>().unwrap()).collect();
        let c = certify(rays, frames, raw, v, ef, ea).unwrap();
        print!("parity_main");
        for x in c
            .parity_main
            .multipliers
            .iter()
            .chain(&c.parity_main.coefficients)
        {
            print!("\t{}", x);
        }
        println!(
            "\t{}\t{}\t{}",
            c.parity_main.rhs, c.parity_main.divisor, c.parity_main.remainder
        );
        print!("frame_counterexample\t{}", c.denominator);
        for q in c
            .normalized_matrix
            .iter()
            .flatten()
            .chain(&c.weights)
            .chain(&c.frame_sums)
        {
            print!("\t{}", q);
        }
        for x in &c.negative_vector {
            print!("\t{}", x);
        }
        print!("\t{}\t{}", c.raw_negative_value, c.negative_value);
        for x in &c.scaled_readout_remainders {
            print!("\t{}", x);
        }
        println!();
        print!("even_control");
        for x in c
            .even_control
            .multipliers
            .iter()
            .chain(&c.even_control.coefficients)
        {
            print!("\t{}", x);
        }
        print!(
            "\t{}\t{}\t{}",
            c.even_control.rhs, c.even_control.divisor, c.even_control.remainder
        );
        for x in c.even_assignment.iter().chain(&c.even_context_sums) {
            print!("\t{}", x);
        }
        println!();
    }
}
