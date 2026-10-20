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

struct SentrySpec {
    input: String,
    coefficients: String,
    output: String,
    request: Option<String>,
    inspect: bool,
}

fn is_inspect_args(args: &[String]) -> bool {
    args.len() == 6
        && args[0] == "--inspect-system"
        && args[2] == "--coefficients"
        && args[4] == "--receipt"
}

fn is_linear_args(args: &[String]) -> bool {
    args.len() == 7
        && args[0] == "--contract-system"
        && args[2] == "--coefficients"
        && args[4] == "--full-box-linear"
        && args[5] == "--receipt"
}

fn is_request_args(args: &[String]) -> bool {
    args.len() == 8
        && args[0] == "--contract-system"
        && args[2] == "--coefficients"
        && args[4] == "--request"
        && args[6] == "--receipt"
}

fn parse_sentry_command(args: &[String]) -> Result<SentrySpec, String> {
    if is_inspect_args(args) {
        return Ok(SentrySpec {
            input: args[1].clone(),
            coefficients: args[3].clone(),
            output: args[5].clone(),
            request: None,
            inspect: true,
        });
    }
    if is_linear_args(args) {
        return Ok(SentrySpec {
            input: args[1].clone(),
            coefficients: args[3].clone(),
            output: args[6].clone(),
            request: None,
            inspect: false,
        });
    }
    if is_request_args(args) {
        return Ok(SentrySpec {
            input: args[1].clone(),
            coefficients: args[3].clone(),
            output: args[7].clone(),
            request: Some(args[5].clone()),
            inspect: false,
        });
    }
    Err("usage: mub6_smale_sentry --inspect-system <system.json> --coefficients <lean-coefficients.json> --receipt <output.json>; or --contract-system <system.json> --coefficients <lean-coefficients.json> (--full-box-linear | --request <request.json>) --receipt <output.json>".into())
}

fn canonicalize_path(path: &str) -> Result<PathBuf, String> {
    fs::canonicalize(path).map_err(|e| e.to_string())
}

fn read_file_bytes(path: &Path) -> Result<Vec<u8>, String> {
    fs::read(path).map_err(|e| e.to_string())
}

fn run_inspect(
    system: &ExecutableQuartetSystem,
    coefficients: &[u8],
) -> Result<(String, String), String> {
    let receipt = system
        .inspect_full_box(coefficients)
        .map_err(|e| e.to_string())?;
    let summary = format!(
        "{}: {} equations, {} sparse terms, {} checked coefficient rows, {} probe comparisons",
        receipt.status,
        receipt.equation_count,
        receipt.sparse_terms,
        receipt.checked_coefficient_rows,
        receipt.parity_scalar_comparisons
    );
    let json = serde_json::to_string_pretty(&receipt).map_err(|e| e.to_string())?;
    Ok((json, summary))
}

fn run_contract(
    system: &ExecutableQuartetSystem,
    coefficients: &[u8],
    request_path: Option<&Path>,
) -> Result<(String, String), String> {
    let receipt = if let Some(path) = request_path {
        let req_bytes = read_file_bytes(path)?;
        system.contract_from_bytes(coefficients, &req_bytes)
    } else {
        system.contract_full_box_linear(coefficients)
    }
    .map_err(|e| e.to_string())?;
    let summary = format!(
        "{}: {} coefficient rows, {} images, {} preconditioner entries, {} contracted coordinates; excluded coordinate {:?}",
        receipt.status,
        receipt.checked_coefficient_rows,
        receipt.images.len(),
        receipt.nonzero_preconditioner_entries,
        receipt.contracted_coordinates.len(),
        receipt.excluded_coordinate
    );
    let json = serde_json::to_string_pretty(&receipt).map_err(|e| e.to_string())?;
    Ok((json, summary))
}

fn resolve_command_paths(
    spec: &SentrySpec,
) -> Result<(PathBuf, PathBuf, PathBuf, Option<PathBuf>), String> {
    let input_path = canonicalize_path(&spec.input)?;
    let coefficient_path = canonicalize_path(&spec.coefficients)?;
    let output = resolve_output(Path::new(&spec.output))?;
    let request_path = match &spec.request {
        Some(req) => Some(canonicalize_path(req)?),
        None => None,
    };
    if output == input_path || output == coefficient_path || request_path.as_ref() == Some(&output)
    {
        return Err("output path must differ from every input".into());
    }
    Ok((input_path, coefficient_path, output, request_path))
}

fn execute_sentry(
    system: &ExecutableQuartetSystem,
    coefficients: &[u8],
    inspect: bool,
    request_path: Option<&Path>,
) -> Result<(String, String), String> {
    if inspect {
        run_inspect(system, coefficients)
    } else {
        run_contract(system, coefficients, request_path)
    }
}

fn run() -> Result<(), String> {
    let args: Vec<_> = env::args().skip(1).collect();
    let spec = parse_sentry_command(&args)?;
    let (input_path, coefficient_path, output, request_path) = resolve_command_paths(&spec)?;
    let bytes = read_file_bytes(&input_path)?;
    let coefficients = read_file_bytes(&coefficient_path)?;
    let system = ExecutableQuartetSystem::from_bytes(&bytes).map_err(|e| e.to_string())?;
    let (json, summary) =
        execute_sentry(&system, &coefficients, spec.inspect, request_path.as_deref())?;
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
