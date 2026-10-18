use omega_mub::omega_native::exact::mub6_szollosi_executable::ExecutableQuartetSystem;
use std::{
    env, fs,
    path::{Path, PathBuf},
    process::ExitCode,
};

fn resolve_output(path: &Path) -> Result<PathBuf, String> {
    if path.exists() {
        return fs::canonicalize(path).map_err(|e| e.to_string());
    }
    let parent = path
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."));
    Ok(fs::canonicalize(parent)
        .map_err(|e| e.to_string())?
        .join(path.file_name().ok_or("output filename is required")?))
}

fn run() -> Result<(), String> {
    let args: Vec<_> = env::args().skip(1).collect();
    let inspect = args.len() == 6
        && args[0] == "--inspect-system"
        && args[2] == "--coefficients"
        && args[4] == "--receipt";
    let linear = args.len() == 7
        && args[0] == "--contract-system"
        && args[2] == "--coefficients"
        && args[4] == "--full-box-linear"
        && args[5] == "--receipt";
    let request = args.len() == 8
        && args[0] == "--contract-system"
        && args[2] == "--coefficients"
        && args[4] == "--request"
        && args[6] == "--receipt";
    if !inspect && !linear && !request {
        return Err("usage: mub6_smale_sentry --inspect-system <system.json> --coefficients <lean-coefficients.json> --receipt <output.json>; or --contract-system <system.json> --coefficients <lean-coefficients.json> (--full-box-linear | --request <request.json>) --receipt <output.json>".into());
    }
    let input_path = fs::canonicalize(&args[1]).map_err(|e| e.to_string())?;
    let coefficient_path = fs::canonicalize(&args[3]).map_err(|e| e.to_string())?;
    let output_index = if inspect {
        5
    } else if linear {
        6
    } else {
        7
    };
    let output = resolve_output(Path::new(&args[output_index]))?;
    let request_path = if request {
        Some(fs::canonicalize(&args[5]).map_err(|e| e.to_string())?)
    } else {
        None
    };
    if output == input_path || output == coefficient_path || request_path.as_ref() == Some(&output)
    {
        return Err("output path must differ from every input".into());
    }
    let bytes = fs::read(&input_path).map_err(|e| e.to_string())?;
    let coefficients = fs::read(&coefficient_path).map_err(|e| e.to_string())?;
    let system = ExecutableQuartetSystem::from_bytes(&bytes).map_err(|e| e.to_string())?;
    let (json, summary) = if inspect {
        let receipt = system
            .inspect_full_box(&coefficients)
            .map_err(|e| e.to_string())?;
        let summary = format!(
            "{}: {} equations, {} sparse terms, {} checked coefficient rows, {} probe comparisons",
            receipt.status,
            receipt.equation_count,
            receipt.sparse_terms,
            receipt.checked_coefficient_rows,
            receipt.parity_scalar_comparisons
        );
        (
            serde_json::to_string_pretty(&receipt).map_err(|e| e.to_string())?,
            summary,
        )
    } else {
        let receipt = if let Some(path) = request_path {
            system.contract_from_bytes(&coefficients, &fs::read(path).map_err(|e| e.to_string())?)
        } else {
            system.contract_full_box_linear(&coefficients)
        }
        .map_err(|e| e.to_string())?;
        let summary=format!("{}: {} coefficient rows, {} images, {} preconditioner entries, {} contracted coordinates; excluded coordinate {:?}",receipt.status,receipt.checked_coefficient_rows,receipt.images.len(),receipt.nonzero_preconditioner_entries,receipt.contracted_coordinates.len(),receipt.excluded_coordinate);
        (
            serde_json::to_string_pretty(&receipt).map_err(|e| e.to_string())?,
            summary,
        )
    };
    fs::write(&output, json + "\n").map_err(|e| e.to_string())?;
    println!("{summary}");
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("{error}");
            ExitCode::FAILURE
        }
    }
}
