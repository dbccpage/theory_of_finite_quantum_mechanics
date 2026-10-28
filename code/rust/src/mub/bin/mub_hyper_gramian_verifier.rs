use tfqm_mub::native::mub6_hyper_gramian;
use std::{fs, path::PathBuf};

fn parse_cli_args() -> Result<Option<(bool, Option<PathBuf>)>, String> {
    let mut emit = false;
    let mut output = None;
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--emit" => emit = true,
            "--output" => output = Some(PathBuf::from(args.next().ok_or("--output needs a path")?)),
            "--help" | "-h" => {
                println!("usage: mub_hyper_gramian_verifier [--emit | --output PATH]");
                return Ok(None);
            }
            _ => return Err(format!("unknown argument: {arg}")),
        }
    }
    if emit && output.is_some() {
        return Err("choose --emit or --output".into());
    }
    Ok(Some((emit, output)))
}

fn write_artifact_targets(bytes: &[u8], emit: bool, output: Option<PathBuf>) -> Result<(), String> {
    if let Some(path) = output {
        fs::write(path, bytes).map_err(|e| e.to_string())?;
    } else if emit {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..");
        for dir in [
            root.join("artifacts"),
            PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts"),
        ] {
            fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
            fs::write(dir.join("mub_hyper_gramian_sdp.json"), bytes).map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}

fn run() -> Result<(), String> {
    let Some((emit, output)) = parse_cli_args()? else {
        return Ok(());
    };
    let report = mub6_hyper_gramian::solve_hyper_gramian_certificate();
    let bytes = serde_json::to_vec_pretty(&report).map_err(|e| e.to_string())?;
    write_artifact_targets(&bytes, emit, output)?;
    println!("{}", String::from_utf8(bytes).map_err(|e| e.to_string())?);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
