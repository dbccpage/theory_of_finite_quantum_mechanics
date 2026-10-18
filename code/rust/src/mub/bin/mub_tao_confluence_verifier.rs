use omega_mub::omega_native::exact::mub6_tao_confluence;
use std::{
    fs,
    io::{self, Read},
    path::PathBuf,
};

fn run() -> Result<(), String> {
    let mut emit = false;
    let mut output = None;
    let mut check = false;
    let mut public = false;
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--emit" => emit = true,
            "--check-stdin" => check = true,
            "--public-input" => public = true,
            "--output" => output = Some(PathBuf::from(args.next().ok_or("--output needs a path")?)),
            "--help" | "-h" => {
                println!("usage: mub_tao_confluence_verifier [--emit | --output PATH | --check-stdin | --public-input]");
                return Ok(());
            }
            _ => return Err(format!("unknown argument: {arg}")),
        }
    }
    if [emit, output.is_some(), check, public]
        .iter()
        .filter(|v| **v)
        .count()
        > 1
    {
        return Err("choose one output or input mode".into());
    }
    if public {
        println!("{}", mub6_tao_confluence::pilot035_public_input());
        return Ok(());
    }
    if check {
        let mut raw = Vec::new();
        io::stdin()
            .take(65537)
            .read_to_end(&mut raw)
            .map_err(|e| e.to_string())?;
        if raw.len() > 65536 {
            return Err("candidate exceeds 65536 bytes".into());
        }
        let candidate = serde_json::from_slice(&raw).map_err(|e| e.to_string())?;
        let result = mub6_tao_confluence::check_pilot035_candidate(&candidate)?;
        println!(
            "{}",
            serde_json::to_string(&result).map_err(|e| e.to_string())?
        );
        return Ok(());
    }
    let report = mub6_tao_confluence::solve_tao_confluence();
    let bytes = serde_json::to_vec_pretty(&report).map_err(|e| e.to_string())?;
    if let Some(path) = output {
        fs::write(path, &bytes).map_err(|e| e.to_string())?;
    } else if emit {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..");
        for dir in [
            root.join("artifacts"),
            PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts"),
        ] {
            fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
            fs::write(dir.join("mub_tao_confluence_receipt.json"), &bytes)
                .map_err(|e| e.to_string())?;
        }
    }
    println!("{}", String::from_utf8(bytes).map_err(|e| e.to_string())?);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
