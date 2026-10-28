use tfqm_mub::native::exact::mub6_tao_confluence;
use std::{
    fs,
    io::{self, Read},
    path::PathBuf,
};

struct ConfluenceCli {
    emit: bool,
    output: Option<PathBuf>,
    check: bool,
    public: bool,
}

fn count_true(flags: [bool; 4]) -> usize {
    let mut n = 0;
    for f in flags {
        if f {
            n += 1;
        }
    }
    n
}

fn parse_confluence_cli() -> Result<Option<ConfluenceCli>, String> {
    let mut cli = ConfluenceCli {
        emit: false,
        output: None,
        check: false,
        public: false,
    };
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--emit" => cli.emit = true,
            "--check-stdin" => cli.check = true,
            "--public-input" => cli.public = true,
            "--output" => {
                cli.output = Some(PathBuf::from(args.next().ok_or("--output needs a path")?));
            }
            "--help" | "-h" => {
                println!("usage: mub_tao_confluence_verifier [--emit | --output PATH | --check-stdin | --public-input]");
                return Ok(None);
            }
            _ => return Err(format!("unknown argument: {arg}")),
        }
    }
    if count_true([cli.emit, cli.output.is_some(), cli.check, cli.public]) > 1 {
        return Err("choose one output or input mode".into());
    }
    Ok(Some(cli))
}

fn check_stdin_candidate() -> Result<(), String> {
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
    Ok(())
}

fn write_confluence_targets(
    bytes: &[u8],
    emit: bool,
    output: Option<PathBuf>,
) -> Result<(), String> {
    if let Some(path) = output {
        fs::write(path, bytes).map_err(|e| e.to_string())?;
    } else if emit {
        let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..");
        for dir in [
            root.join("artifacts"),
            PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/mub/artifacts"),
        ] {
            fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
            fs::write(dir.join("mub_tao_confluence_receipt.json"), bytes)
                .map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}

fn run() -> Result<(), String> {
    let Some(cli) = parse_confluence_cli()? else {
        return Ok(());
    };
    if cli.public {
        println!("{}", mub6_tao_confluence::pilot035_public_input());
        return Ok(());
    }
    if cli.check {
        return check_stdin_candidate();
    }
    let report = mub6_tao_confluence::solve_tao_confluence();
    let bytes = serde_json::to_vec_pretty(&report).map_err(|e| e.to_string())?;
    write_confluence_targets(&bytes, cli.emit, cli.output)?;
    println!("{}", String::from_utf8(bytes).map_err(|e| e.to_string())?);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
