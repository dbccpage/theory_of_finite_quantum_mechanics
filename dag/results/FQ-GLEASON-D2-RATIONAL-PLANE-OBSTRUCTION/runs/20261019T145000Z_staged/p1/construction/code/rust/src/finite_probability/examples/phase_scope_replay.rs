use std::io::{self, BufRead};
use std::path::Path;
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let fs: Vec<String> = line.split('\t').map(str::to_string).collect();
        assert!(fs.len() >= 2);
        let mut out = vec![fs[0].clone()];
        out.extend(tfqm_finite_probability::phase_scope::evaluate(
            &fs[0],
            &fs[1..],
            Path::new("."),
        ));
        println!("{}", out.join("\t"));
    }
}
