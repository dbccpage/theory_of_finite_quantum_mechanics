//! Writes the prompt 05 campaign receipt: the balanced table replay, its negative controls
//! and the exact checks of the campaign's local lemmas.
//!
//! AuthorityEffect: None

use omega_mub::omega_native::campaign::mub6_prompt05_campaign_checks::run_campaign_checks;
use std::{error::Error, fs, io::Write, path::PathBuf};

fn run() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    if args.len() != 2 {
        return Err(
            "usage: mub6_prompt05_campaign_checks BALANCED_COEFFICIENTS.jsonl OUTPUT.json".into(),
        );
    }
    let input = PathBuf::from(&args[0]);
    let output = PathBuf::from(&args[1]);
    if output.exists() {
        return Err("output already exists; choose a fresh output path".into());
    }
    let receipt = run_campaign_checks(&fs::read(input)?)?;
    let mut bytes = serde_json::to_vec_pretty(&receipt)?;
    bytes.push(b'\n');
    fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(output)?
        .write_all(&bytes)?;
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
