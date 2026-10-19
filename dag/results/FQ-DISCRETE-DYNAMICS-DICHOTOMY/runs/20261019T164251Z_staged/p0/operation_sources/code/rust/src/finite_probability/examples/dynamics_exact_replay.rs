use std::io::{self, BufRead};
fn main() {
    for line in io::stdin().lock().lines() {
        let v: Vec<String> = line.unwrap().split('\t').map(str::to_string).collect();
        let mut out = vec![v[0].clone()];
        out.extend(tfqm_finite_probability::dynamics_exact::evaluate(
            &v[0],
            &v[1..],
        ));
        println!("{}", out.join("\t"));
    }
}
