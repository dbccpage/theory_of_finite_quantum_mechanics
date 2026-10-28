
use engine_wdp::prime_algos::prime_algorithm_0_conformance::{
    check_builtin_roster, ReceiptViolation, UNDECIDABLE_WITHOUT_PER_STEP_STATE,
};
use engine_wdp::prime_algos::rosetta::{rosetta_builtin_roster, RosterProvenance};

fn main() -> std::process::ExitCode {
    let r = rosetta_builtin_roster();

    println!("=== ROSETTA CROSS-DOMAIN REPORT ===");
    match &r.provenance {
        RosterProvenance::AllFixtureDriven => {
            println!("  provenance: FIXTURE-DRIVEN STRUCTURAL DEMO -- every adapter declares");
            println!("              its own cochain justification, masses and lift bits.");
        }
        RosterProvenance::Mixed { verifier_produced } => {
            println!(
                "  provenance: MIXED. Masses COMPUTED by a verifier for: {verifier_produced:?}"
            );
            println!("              Every other domain DECLARES its masses as constants;");
            println!("              their numbers are fixtures, their structure is real.");
        }
        RosterProvenance::AllVerifierProduced => {
            println!("  provenance: VERIFIER-PRODUCED -- every domain's masses were computed.");
        }
    }
    println!();

    println!(
        "{:<12} {:<14} {:<28} {:<20} {:>8} {:>8}",
        "DOMAIN", "TAPE", "RESIDUAL FAMILY", "TERMINAL", "PHI1", "GAMMA2"
    );
    for d in &r.domains {
        println!(
            "{:<12} {:<14} {:<28} {:<20} {:>8} {:>8}",
            d.domain,
            d.letter_tape,
            d.residual_family_label,
            d.terminal,
            d.phi1.map(|v| v.to_string()).unwrap_or_else(|| "-".into()),
            d.gamma2
                .map(|v| v.to_string())
                .unwrap_or_else(|| "-".into()),
        );
    }

    println!("\n--- shared structure ---");
    println!(
        "  every domain emits C, R and T : {}",
        r.shared_required_letters
    );
    println!("  alphabet closed (no strays)   : {}", r.alphabet_closed);
    println!(
        "  all receipts AuthorityEffect  : None = {}",
        r.authority_all_none
    );
    println!(
        "  Phi1 / Gamma2 kept separate   : {}",
        r.phi_gamma_separated
    );
    println!(
        "  literature only after terminal: {}",
        r.literature_always_after_terminal
    );
    println!(
        "  distinct residual families    : {}",
        r.residual_family_count
    );

    println!("\n--- pairwise letter-set Jaccard (x1000) ---");
    println!("  1000 = identical letter sets; 0 = disjoint.");
    let mut pairs: Vec<_> = r.pairwise_letter_jaccard_x1000.iter().collect();
    pairs.sort_by(|a, b| b.1.cmp(a.1));
    for (k, v) in pairs {
        println!("  {:<44} {:>5}", k, v);
    }

    println!("\n--- branch / terminal histograms ---");
    for (k, v) in &r.branch_histogram {
        println!("  branch   {:<28} {}", k, v);
    }
    for (k, v) in &r.terminal_histogram {
        println!("  terminal {:<28} {}", k, v);
    }

    println!("\n--- letter-law conformance ---");
    let checks = check_builtin_roster();
    let mut violating = 0usize;
    for c in &checks {
        let v = c.violations();
        if v.is_empty() {
            println!("  {:<12} no decidable violation (PARTIAL)", c.domain);
        } else {
            violating += 1;
            for viol in v {
                let label = match viol {
                    ReceiptViolation::TerminalizedOpenResidual { gamma2 } => {
                        format!("T sealed an open residual (gamma2={gamma2})")
                    }
                    other => format!("{other:?}"),
                };
                println!("  {:<12} VIOLATION: {}", c.domain, label);
            }
        }
    }
    println!(
        "\n  {} of {} domains violate a decidable letter law.",
        violating,
        checks.len()
    );

    println!("\n--- laws NOT decidable from a OEPRMALG0 receipt ---");
    println!("  (so no receipt above can be called conformant, only PARTIAL)");
    for law in UNDECIDABLE_WITHOUT_PER_STEP_STATE {
        println!("  - {law}");
    }

    println!("\nrosetta_smoke_pass = {}", r.rosetta_smoke_pass);
    println!("AuthorityEffect: None.");

    if violating > 0 {
        eprintln!(
            "\nrosetta_report: {violating} domain(s) violate a decidable letter law -> exit 1"
        );
        return std::process::ExitCode::FAILURE;
    }
    std::process::ExitCode::SUCCESS
}
