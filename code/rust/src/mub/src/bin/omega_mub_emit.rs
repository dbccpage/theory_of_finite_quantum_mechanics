use std::{fs, path::PathBuf, process::ExitCode};

use omega_mub::omega_native::exact::mub6_collar_solver;
use omega_mub::omega_native::exact::mub6_deltoid_cusp_asymptotics;
use omega_mub::omega_native::exact::mub6_frame_potential;
use omega_mub::omega_native::exact::mub6_hyper_gramian;
use omega_mub::omega_native::exact::mub6_quad_sdp;
use serde::Serialize;

struct EmitJob {
    name: &'static str,
    usage: &'static str,
    artifact: &'static str,
    report: fn() -> Result<Vec<u8>, String>,
}

fn encode<T: Serialize>(value: &T) -> Result<Vec<u8>, String> {
    serde_json::to_vec_pretty(value).map_err(|error| error.to_string())
}

fn jobs() -> Vec<EmitJob> {
    vec![
        EmitJob {
            name: "collar",
            usage: "collar",
            artifact: "mub_karlsson_collar_cover.json",
            report: || encode(&mub6_collar_solver::solve_karlsson_collar_cover(2)),
        },
        EmitJob {
            name: "frame-potential",
            usage: "frame-potential",
            artifact: "mub_frame_potential.json",
            report: || encode(&mub6_frame_potential::solve_frame_potential_certificate()),
        },
        EmitJob {
            name: "hyper-gramian",
            usage: "hyper-gramian",
            artifact: "mub_hyper_gramian_sdp.json",
            report: || encode(&mub6_hyper_gramian::solve_hyper_gramian_certificate()),
        },
        EmitJob {
            name: "quad-incompatibility",
            usage: "quad-incompatibility",
            artifact: "mub_quad_sdp_certificate.json",
            report: || encode(&mub6_quad_sdp::solve_quad_sdp_certificate()),
        },
        EmitJob {
            name: "deltoid-cusp",
            usage: "deltoid-cusp",
            artifact: "mub_deltoid_cusps.json",
            report: || encode(&mub6_deltoid_cusp_asymptotics::solve_deltoid_cusp_asymptotics()),
        },
    ]
}

fn emit(bytes: &[u8], artifact: &str) -> Result<(), String> {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..");
    for dir in [
        root.join("artifacts"),
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts"),
    ] {
        fs::create_dir_all(&dir).map_err(|error| error.to_string())?;
        fs::write(dir.join(artifact), bytes).map_err(|error| error.to_string())?;
    }
    Ok(())
}

fn job_usage_names(jobs: &[EmitJob]) -> String {
    let mut parts = Vec::new();
    for job in jobs {
        parts.push(job.usage);
    }
    parts.join("|")
}

fn find_emit_job(jobs: Vec<EmitJob>, command: &str) -> Result<Option<EmitJob>, String> {
    if command == "--help" || command == "-h" {
        let names = job_usage_names(&jobs);
        println!("usage: omega_mub_emit <{names}> [--emit | --output PATH]");
        return Ok(None);
    }
    for job in jobs {
        if job.name == command {
            return Ok(Some(job));
        }
    }
    Err(format!("unknown diagnostic: {command}"))
}

fn parse_emit_flags(
    args: &mut std::iter::Skip<std::env::Args>,
    usage: &str,
) -> Result<Option<(bool, Option<PathBuf>)>, String> {
    let mut write_artifacts = false;
    let mut output = None;
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--emit" => write_artifacts = true,
            "--output" => output = Some(PathBuf::from(args.next().ok_or("--output needs a path")?)),
            "--help" | "-h" => {
                println!("usage: omega_mub_emit {usage} [--emit | --output PATH]");
                return Ok(None);
            }
            _ => return Err(format!("unknown argument: {arg}")),
        }
    }
    if write_artifacts && output.is_some() {
        return Err("choose --emit or --output".into());
    }
    Ok(Some((write_artifacts, output)))
}

fn write_or_emit_bytes(
    bytes: &[u8],
    artifact: &str,
    write_artifacts: bool,
    output: Option<PathBuf>,
) -> Result<(), String> {
    if let Some(path) = output {
        fs::write(path, bytes).map_err(|error| error.to_string())?;
    } else if write_artifacts {
        emit(bytes, artifact)?;
    }
    Ok(())
}

fn run() -> Result<(), String> {
    let all_jobs = jobs();
    let mut args = std::env::args().skip(1);
    let Some(command) = args.next() else {
        let names = job_usage_names(&all_jobs);
        return Err(format!("usage: omega_mub_emit <{names}> [--emit | --output PATH]"));
    };
    let Some(job) = find_emit_job(all_jobs, &command)? else {
        return Ok(());
    };
    let Some((write_artifacts, output)) = parse_emit_flags(&mut args, job.usage)? else {
        return Ok(());
    };
    let bytes = (job.report)()?;
    write_or_emit_bytes(&bytes, job.artifact, write_artifacts, output)?;
    println!("{}", String::from_utf8(bytes).map_err(|error| error.to_string())?);
    Ok(())
}

fn main() -> ExitCode {
    if let Err(error) = run() {
        eprintln!("{error}");
        return ExitCode::from(1);
    }
    ExitCode::from(0)
}
