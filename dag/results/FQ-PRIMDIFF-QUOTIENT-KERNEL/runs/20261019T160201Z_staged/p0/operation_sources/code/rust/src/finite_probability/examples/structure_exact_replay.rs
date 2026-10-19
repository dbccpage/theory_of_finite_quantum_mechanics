use std::io::{self, BufRead};
fn main() {
    for line in io::stdin().lock().lines() {
        let f: Vec<String> = line.unwrap().split('\t').map(str::to_string).collect();
        let mut out = vec![f[0].clone()];
        out.extend(tfqm_finite_probability::structure_exact::evaluate(
            &f[0],
            &f[1..],
        ));
        println!("{}", out.join("\t"));
    }
}
