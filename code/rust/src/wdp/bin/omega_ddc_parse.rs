
use std::env;
use std::fs;
use std::io::{self, Read};
use std::path::PathBuf;
use std::process::ExitCode;

use omega_wdp::ddc::parser::DdcTapeParser;

fn flag(args: &[String], name: &str) -> Option<PathBuf> {
    args.windows(2)
        .find(|pair| pair[0] == name)
        .map(|pair| PathBuf::from(&pair[1]))
}

fn has_flag(args: &[String], name: &str) -> bool {
    args.iter().any(|arg| arg == name)
}

fn print_usage() {
    eprintln!(
        "omega_ddc_parse: Sovereign Rust DDC Tape Parser & Contractivity Certifier\n\
         AuthorityEffect: None\n\n\
         Usage:\n\
           omega_ddc_parse --tape <PATH> [--output <RECEIPT_PATH>]\n\
           omega_ddc_parse --stdin [--output <RECEIPT_PATH>]\n"
    );
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || has_flag(&args, "--help") || has_flag(&args, "-h") {
        print_usage();
        return ExitCode::from(1);
    }

    let output_path = flag(&args, "--output");
    let content = if has_flag(&args, "--stdin") {
        let mut buffer = String::new();
        if let Err(e) = io::stdin().read_to_string(&mut buffer) {
            eprintln!("Error reading stdin: {e}");
            return ExitCode::from(2);
        }
        buffer
    } else if let Some(tape_path) = flag(&args, "--tape") {
        match fs::read_to_string(&tape_path) {
            Ok(c) => c,
            Err(e) => {
                eprintln!("Error reading tape file '{}': {e}", tape_path.display());
                return ExitCode::from(2);
            }
        }
    } else {
        print_usage();
        return ExitCode::from(1);
    };

    match DdcTapeParser::parse_jsonl(&content) {
        Ok(receipt) => {
            let json_str = match serde_json::to_string_pretty(&receipt) {
                Ok(s) => s,
                Err(e) => {
                    eprintln!("Error serializing receipt: {e}");
                    return ExitCode::from(2);
                }
            };
            if let Some(out_p) = output_path {
                if let Err(e) = fs::write(&out_p, &json_str) {
                    eprintln!("Error writing receipt to '{}': {e}", out_p.display());
                    return ExitCode::from(2);
                }
            } else {
                println!("{json_str}");
            }
            if receipt.ddc_laws_valid && receipt.hash_chain_valid {
                ExitCode::SUCCESS
            } else {
                ExitCode::from(3)
            }
        }
        Err(refusal) => {
            let refusal_json = serde_json::json!({
                "status": "REFUSAL",
                "code": refusal.code,
                "message": refusal.message,
                "locus": refusal.locus,
                "authority_effect": "None"
            });
            eprintln!("{}", serde_json::to_string_pretty(&refusal_json).unwrap());
            ExitCode::from(4)
        }
    }
}
