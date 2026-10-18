// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)
use theory_of_finite_qm::entropy_solver::generate_c750_b01_parity_receipt;

fn main() {
    let receipt =
        generate_c750_b01_parity_receipt().expect("Failed to generate C750 B01 parity receipt");
    let json_str =
        serde_json::to_string_pretty(&receipt).expect("Failed to serialize parity receipt");
    println!("{}", json_str);
}
