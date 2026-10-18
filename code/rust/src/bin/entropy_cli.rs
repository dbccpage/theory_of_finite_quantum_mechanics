// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)
use theory_of_finite_qm::entropy_solver::{generate_c750_b01_parity_receipt, ParityReceipt};

fn main() {
    let receipt = match generate_c750_b01_parity_receipt() {
        Ok(receipt) => receipt,
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    };
    if let Err(error) = audit_receipt(&receipt) {
        eprintln!("{error}");
        std::process::exit(1);
    }
    match serde_json::to_string_pretty(&receipt) {
        Ok(json) => println!("{json}"),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    }
}

/// The receipt's verified count is the number of systems whose byte parity
/// matched, and each purity string `n/d` lies in `(0, 1]` with `is_pure` iff
/// the reduced value is 1. Dimensions are summed from both ends.
fn audit_receipt(receipt: &ParityReceipt) -> Result<(), String> {
    if receipt.systems.len() != 8 {
        return Err(format!(
            "expected 8 systems, found {}",
            receipt.systems.len()
        ));
    }
    let matched = receipt
        .systems
        .values()
        .filter(|system| system.byte_parity_match)
        .count();
    if matched != receipt.total_systems_verified {
        return Err(format!(
            "verified count {} is not the matched-system count {matched}",
            receipt.total_systems_verified
        ));
    }
    let mut dimensions = 0usize;
    let mut dimensions_rev = 0usize;
    let mut ordered: Vec<_> = receipt.systems.values().collect();
    for system in &ordered {
        dimensions = dimensions
            .checked_add(system.dimension)
            .ok_or("dimension sum overflow")?;
        audit_purity(&system.purity_p2, system.is_pure, &system.system_id)?;
        if system.conductor == 0 {
            return Err(format!("{} has conductor 0", system.system_id));
        }
    }
    ordered.reverse();
    for system in &ordered {
        dimensions_rev = dimensions_rev
            .checked_add(system.dimension)
            .ok_or("dimension sum overflow")?;
    }
    if dimensions != dimensions_rev {
        return Err(format!(
            "dimension sums {dimensions} and {dimensions_rev} disagree"
        ));
    }
    Ok(())
}

fn audit_purity(text: &str, is_pure: bool, system: &str) -> Result<(), String> {
    let (numer, denom) = parse_ratio(text).map_err(|error| format!("{system}: {error}"))?;
    if denom <= 0 || numer < 0 || numer > denom {
        return Err(format!("{system}: purity {text} is outside (0, 1]"));
    }
    if numer == 0 {
        return Err(format!("{system}: purity is zero"));
    }
    let pure = numer == denom;
    if pure != is_pure {
        return Err(format!(
            "{system}: is_pure={is_pure} but purity {text} says {pure}"
        ));
    }
    Ok(())
}

fn parse_ratio(text: &str) -> Result<(i128, i128), String> {
    let mut parts = text.split('/');
    let numer = parts
        .next()
        .ok_or("purity missing numerator")?
        .parse::<i128>()
        .map_err(|_| "purity numerator is not an integer")?;
    let denom = parts
        .next()
        .ok_or("purity missing denominator")?
        .parse::<i128>()
        .map_err(|_| "purity denominator is not an integer")?;
    if parts.next().is_some() {
        return Err("purity has extra slashes".into());
    }
    if denom == 0 {
        return Err("purity denominator is zero".into());
    }
    Ok((numer, denom))
}
