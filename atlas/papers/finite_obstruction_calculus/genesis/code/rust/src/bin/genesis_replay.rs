//! Line-oriented paper reproduction interface, with no registry dependencies.
use std::io::{self, BufRead};
use omega_ooutwire_primitives::{admission::step, bounds::Bounds,
    canonical::{portable_key_v1, decode_portable_key_v1, encode_structural_key_v1},
    context::{contexts, plug}, event::Event, mark::{Mark, Pair}, measure::MeasureKind,
    minima::challenge3, profile::derivable, reading::readings, regime::Regime,
    replay::replay, token::Token};

fn nums(text: &str) -> Result<Vec<usize>, String> {
    if text.is_empty() { return Ok(vec![]); }
    text.split(',').map(|s| s.parse().map_err(|_| "invalid integer".into())).collect()
}

fn decode(line: &str) -> Result<Regime, String> {
    let parts: Vec<_> = line.split('|').collect();
    if parts.len() != 5 { return Err("expected five fields".into()); }
    let n: usize = parts[0].parse().map_err(|_| "invalid data count")?;
    // This interface has a small, explicit input population; the library APIs
    // retain their own resource contracts.
    if n > 8 { return Err("paper replay supports at most eight data".into()); }
    let mut r = Regime::genesis();
    let mut admit = |event| -> Result<(), String> {
        r = step(&r, &event).map_err(|e| e.to_string())?;
        Ok(())
    };
    for d in 0..n { admit(Event::AdmitDatum(Token::new(format!("d{d}"))))?; }
    let forms = nums(parts[1])?;
    if forms.len() > 8 || forms.iter().any(|&a| a > 7) {
        return Err("paper replay supports at most eight forms of arity at most seven".into());
    }
    for arity in forms { admit(Event::AdmitForm(arity))?; }
    if !parts[2].is_empty() {
        for row in parts[2].split(';') {
            let (form, args) = row.split_once(':').ok_or("invalid instance")?;
            admit(Event::AdmitInst(form.parse().map_err(|_| "invalid form")?,
                nums(args)?.into_iter().map(Mark).collect()))?;
        }
    }
    for form in nums(parts[3])? { admit(Event::AdmitRuleAll(form))?; }
    if !parts[4].is_empty() {
        for row in parts[4].split(';') {
            let (i, j) = row.split_once(':').ok_or("invalid requirement")?;
            admit(Event::Impose(Pair { i: Mark(i.parse().map_err(|_| "invalid endpoint")?),
                j: Mark(j.parse().map_err(|_| "invalid endpoint")?) }))?;
        }
    }
    Ok(r)
}

fn run(line: &str) -> Result<String, String> {
    if let Some(hex) = line.strip_prefix("wire:") {
        if hex.len() % 2 != 0 || !hex.is_ascii() { return Ok("REJECT".into()); }
        let bytes: Result<Vec<u8>, _> = (0..hex.len()).step_by(2)
            .map(|i| u8::from_str_radix(&hex[i..i + 2], 16)).collect();
        let Ok(bytes) = bytes else { return Ok("REJECT".into()); };
        return Ok(match decode_portable_key_v1(&bytes) {
            Ok(key) => encode_structural_key_v1(&key).map_err(|e| e.to_string())?
                .iter().map(|b| format!("{b:02x}")).collect(),
            Err(_) => "REJECT".into(),
        });
    }
    if line == "minima" {
        let mut rows = vec![];
        for reading in readings() {
            let base = replay(&reading.genesis).map_err(|e| e.to_string())?;
            for measure in [MeasureKind::Mu1, MeasureKind::Mu2] {
                let c = challenge3(&base, reading.target, measure, &Bounds::default());
                rows.push(format!("{},{},{},{},{},{}", reading.name,
                    if measure == MeasureKind::Mu1 { "mu1" } else { "mu2" },
                    c.cost.0, c.cost.1, c.valid_at_minimum, c.classes.len()));
            }
        }
        return Ok(rows.join(";"));
    }
    let r = decode(line)?;
    let key = portable_key_v1(&r, 100_000).map_err(|e| e.to_string())?;
    let hex: String = key.iter().map(|b| format!("{b:02x}")).collect();
    let ctxs = contexts(&r);
    let observations: Vec<String> = (0..r.n_data()).map(|d| ctxs.iter()
        .map(|c| if derivable(&r, &plug(c, Mark(d))) { '1' } else { '0' }).collect()).collect();
    Ok(format!("{hex}|{}|{}", ctxs.len(), observations.join(",")))
}

fn main() {
    for line in io::stdin().lock().lines() {
        match line.map_err(|e| e.to_string()).and_then(|line| run(&line)) {
            Ok(answer) => println!("{answer}"),
            Err(error) => { eprintln!("{error}"); std::process::exit(1); }
        }
    }
}
