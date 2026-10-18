//! CLI adapter; all computation is shared with the Python extension.
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let target = args.get(1).map(String::as_str).unwrap_or("--all");
    let result = if target == "--qm122" {
        theory_of_finite_qm::suites::run("qm122", &serde_json::Value::Null)
    } else {
        theory_of_finite_qm::legacy_suites::run_legacy_target_with_args(target, &args)
    };
    match result {
        Ok(value) => println!("{}", serde_json::to_string_pretty(&value).unwrap()),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}
