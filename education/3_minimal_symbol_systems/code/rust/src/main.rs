//! CLI Entrypoint for Stage 024 Pullback Monic Factorization Verifier.

use mssn_stage_024::Stage024Candidate;
use std::env;
use std::io::{self, Read};
use std::process::exit;

fn main() {
    let args: Vec<String> = env::args().collect();
    let packet = if args.len() > 1 {
        if args[1] == "-" || args[1] == "--stdin" {
            let mut buffer = String::new();
            if let Err(e) = io::stdin().read_to_string(&mut buffer) {
                eprintln!("Error reading stdin: {}", e);
                exit(1);
            }
            buffer
        } else {
            args[1..].join(" ")
        }
    } else {
        // Run demo packet by default when no arguments are provided
        let default_packet = "<stage024<sub<s0><s1>><amb<x0><x1><x2>><m<<s0><x0>><<s1><x1>>><truth<true><false>><true<true>><chi<<x0><true>><<x1><true>><<x2><false>>>>";
        println!("No input provided. Evaluating canonical demo packet:");
        println!("  {}", default_packet);
        match Stage024Candidate::parse_boundary_packet(default_packet) {
            Ok(cand) => match cand.verify() {
                Ok(receipt) => {
                    println!("{}", serde_json::to_string_pretty(&receipt).unwrap());
                    exit(0);
                }
                Err(e) => {
                    eprintln!("Verification failed: {}", e);
                    exit(2);
                }
            },
            Err(e) => {
                eprintln!("Packet parse error: {}", e);
                exit(3);
            }
        }
    };

    let p = packet.trim();
    match Stage024Candidate::parse_boundary_packet(p) {
        Ok(candidate) => match candidate.verify() {
            Ok(receipt) => {
                println!("{}", serde_json::to_string_pretty(&receipt).unwrap());
                exit(0);
            }
            Err(e) => {
                eprintln!("REJECT: {}", e);
                exit(2);
            }
        },
        Err(e) => {
            eprintln!("MALFORMED: {}", e);
            exit(3);
        }
    }
}
