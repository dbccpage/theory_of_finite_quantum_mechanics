
use std::path::PathBuf;

use omega_mub::deep_run::run_deep_mub;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let crate_root = match args.as_slice() {
        [_] => PathBuf::from(env!("CARGO_MANIFEST_DIR")),
        [_, flag, dir] if flag == "--crate-root" => PathBuf::from(dir),
        _ => {
            eprintln!("usage: mub_deep_run [--crate-root <dir>]");
            std::process::exit(2);
        }
    };

    let report = run_deep_mub(&crate_root);
    match serde_json::to_string_pretty(&report) {
        Ok(json) => println!("{json}"),
        Err(error) => {
            eprintln!("failed to serialize MUB deep-run report: {error}");
            std::process::exit(1);
        }
    }
}
