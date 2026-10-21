use std::io::{self, BufRead};

fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        if line.is_empty() {
            continue;
        }
        let out = tfqm_finite_probability::pfp_old_image_injective::replay(&line).expect("unknown public-input line");
        println!("{}", out);
    }
}
