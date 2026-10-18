use omega_mub::omega_native::exact::mub6_quadratic_lift::QuadraticLift;
use std::{error::Error, fs, path::PathBuf};

fn run() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    if !(2..=3).contains(&args.len()) {
        return Err("usage: mub_quadratic_lift COEFFICIENTS.jsonl OUTPUT.json [BOX.json]".into());
    }
    let input = PathBuf::from(&args[0]);
    let output = PathBuf::from(&args[1]);
    if output.exists() {
        return Err("output already exists; choose a fresh output path".into());
    }
    let system = QuadraticLift::from_bytes(&fs::read(input)?)?;
    let receipt = if let Some(box_path) = args.get(2) {
        system.inspect_box_bytes(&fs::read(box_path)?)?
    } else {
        system.inspect_full_box()?
    };
    let mut bytes = serde_json::to_vec_pretty(&receipt)?;
    bytes.push(b'\n');
    use std::io::Write;
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
