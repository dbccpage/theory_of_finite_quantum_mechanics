// Contract governance hook; see governance/README.md. This file is byte-identical
// in every workspace package and pinned by SHA-256 in governance/policy.json.
fn main() {
    governance::verify_crate_contracts!();
}
