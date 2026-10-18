//! Binary CLI: Execute exact Szöllősi B6 and Tao S6 MU triad compatibility search and emit receipts.
//!
//! AuthorityEffect: None

use omega_mub::omega_native::exact::szollosi_triad_solver::{
    emit_receipt_files, execute_szollosi_triad_search,
};

fn main() {
    println!("=== Running Szöllősi & Tao MU Triad Compatibility Solver ===");
    println!("AuthorityEffect: None");
    println!("Firewall: stated region only; mints no authority");

    let receipt = execute_szollosi_triad_search();
    println!("Tao S6 CHM verified: {}", receipt.tao_s6_verification.is_chm);
    println!(
        "Discrete Szöllősi CHM points found: {} / {}",
        receipt.valid_szollosi_discrete_chm_count,
        receipt.total_discrete_parameter_tuples_evaluated
    );
    println!("Tao vs Tao MU triads: {}", receipt.tao_vs_tao_mu_triads_found);
    println!(
        "Tao vs Szöllősi MU triads: {}",
        receipt.tao_vs_szollosi_mu_triads_found
    );
    println!(
        "Szöllősi vs Szöllősi MU triads: {}",
        receipt.szollosi_vs_szollosi_mu_triads_found
    );
    println!("Obstruction summary: {}", receipt.obstruction_summary);
    println!("Terminal status: {}", receipt.terminal_status);

    match emit_receipt_files(&receipt) {
        Ok(paths) => {
            for p in paths {
                println!("Emitted receipt artifact: {}", p.display());
            }
        }
        Err(err) => {
            eprintln!("Error emitting receipts: {err}");
            std::process::exit(1);
        }
    }

    match serde_json::to_string_pretty(&receipt) {
        Ok(json) => println!("{json}"),
        Err(err) => {
            eprintln!("Serialization error: {err}");
            std::process::exit(1);
        }
    }
}
