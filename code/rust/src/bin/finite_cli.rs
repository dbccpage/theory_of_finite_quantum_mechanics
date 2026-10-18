fn main() {
    if let Err(error) = commutator_traces_agree() {
        eprintln!("{error}");
        std::process::exit(2);
    }
    let args: Vec<String> = std::env::args().collect();
    let target = args.get(1).map(String::as_str).unwrap_or("--all");
    let result = if target == "--qm122" {
        theory_of_finite_qm::suites::run("qm122", &serde_json::Value::Null)
    } else {
        theory_of_finite_qm::legacy_suites::run_legacy_target_with_args(target, &args)
    };
    match result {
        Ok(value) => match serde_json::to_string_pretty(&value) {
            Ok(json) => println!("{json}"),
            Err(error) => {
                eprintln!("{error}");
                std::process::exit(2);
            }
        },
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}

fn commutator_traces_agree() -> Result<(), String> {
    let a = [[1i64, 2, 3], [0, -1, 4], [5, 6, 1]];
    let b = [[2i64, 0, 1], [1, 3, -2], [0, 1, 2]];
    let tr_ab = trace_product(&a, &b)?;
    let tr_ba = trace_product(&b, &a)?;
    let pairing = frobenius(&a, &b)?;
    if tr_ab != tr_ba || tr_ab != pairing {
        return Err(format!(
            "commutator traces disagree: Tr(AB)={tr_ab}, Tr(BA)={tr_ba}, pairing={pairing}"
        ));
    }
    Ok(())
}

fn trace_product(left: &[[i64; 3]; 3], right: &[[i64; 3]; 3]) -> Result<i64, String> {
    let mut trace = 0i64;
    for i in 0..3 {
        let mut diagonal = 0i64;
        for k in 0..3 {
            diagonal = diagonal
                .checked_add(
                    left[i][k]
                        .checked_mul(right[k][i])
                        .ok_or("trace overflow")?,
                )
                .ok_or("trace overflow")?;
        }
        trace = trace.checked_add(diagonal).ok_or("trace overflow")?;
    }
    Ok(trace)
}

fn frobenius(left: &[[i64; 3]; 3], right: &[[i64; 3]; 3]) -> Result<i64, String> {
    let mut pairing = 0i64;
    for i in 0..3 {
        for j in 0..3 {
            pairing = pairing
                .checked_add(
                    left[i][j]
                        .checked_mul(right[j][i])
                        .ok_or("pairing overflow")?,
                )
                .ok_or("pairing overflow")?;
        }
    }
    Ok(pairing)
}
