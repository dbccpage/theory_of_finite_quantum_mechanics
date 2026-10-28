use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

use omega_wdp::ddc::agent_contract::{
    render_rust_bytes, verify_bytes, DdaGateReceipt,
};

fn flag(args: &[String], name: &str) -> Result<PathBuf, String> {
    args.windows(2)
        .find(|pair| pair[0] == name)
        .map(|pair| PathBuf::from(&pair[1]))
        .ok_or_else(|| format!("missing required {name} PATH"))
}

fn write_receipt(receipt: &DdaGateReceipt, output: Option<&Path>) -> Result<(), String> {
    let raw = serde_json::to_string_pretty(receipt)
        .map_err(|error| format!("serialize receipt: {error}"))?
        + "\n";
    if let Some(path) = output {
        fs::write(path, raw).map_err(|error| format!("write {}: {error}", path.display()))
    } else {
        print!("{raw}");
        Ok(())
    }
}

fn run() -> Result<(), String> {
    let args: Vec<String> = env::args().collect();
    let command = args.get(1).map(String::as_str).ok_or_else(|| {
        "usage: dda_gate verify|render-rust --work-packet PATH --proposal PATH".to_string()
    })?;
    let work_path = flag(&args, "--work-packet")?;
    let proposal_path = flag(&args, "--proposal")?;
    let work_raw =
        fs::read(&work_path).map_err(|error| format!("read {}: {error}", work_path.display()))?;
    let proposal_raw = fs::read(&proposal_path)
        .map_err(|error| format!("read {}: {error}", proposal_path.display()))?;

    match command {
        "verify" => {
            let receipt = verify_bytes(&work_raw, &proposal_raw)?;
            let receipt_path = args
                .windows(2)
                .find(|pair| pair[0] == "--receipt")
                .map(|pair| Path::new(&pair[1]));
            write_receipt(&receipt, receipt_path)
        }
        "render-rust" => {
            let output = flag(&args, "--output")?;
            let source = render_rust_bytes(&work_raw, &proposal_raw, &output)?;
            if let Some(parent) = output.parent() {
                fs::create_dir_all(parent)
                    .map_err(|error| format!("create {}: {error}", parent.display()))?;
            }
            fs::write(&output, source)
                .map_err(|error| format!("write {}: {error}", output.display()))
        }
        other => Err(format!(
            "unknown command {other:?}; expected verify|render-rust"
        )),
    }
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("dda_gate: {error}");
            ExitCode::from(2)
        }
    }
}
