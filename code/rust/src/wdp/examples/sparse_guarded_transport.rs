use engine_homology::permutohedral::{add_scaled, boundary, Cell, CellChain, ContractionLimits};
use engine_wdp::guarded_chain_transport::sparse::{
    verify_sparse_event_filling, SparseTransport, SparseTransportLimits,
};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::collections::BTreeMap;
use std::fs::{File, OpenOptions};
use std::io::{Read, Write};
use std::time::Instant;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;
const MAX_BYTES: u64 = 16 * 1024 * 1024;

#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Term {
    cell: Cell,
    coefficient: i64,
}

#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Certificate {
    schema: String,
    pairs: usize,
    capacity: usize,
    degree: usize,
    cycle: Vec<Term>,
    filling: Vec<Term>,
}

fn encode(chain: &CellChain) -> Vec<Term> {
    chain
        .iter()
        .map(|(cell, &coefficient)| Term {
            cell: cell.clone(),
            coefficient,
        })
        .collect()
}

fn decode(terms: &[Term]) -> Result<CellChain> {
    if terms.iter().any(|term| term.coefficient == 0)
        || terms.windows(2).any(|w| w[0].cell >= w[1].cell)
    {
        return Err("certificate terms must be nonzero, unique and sorted".into());
    }
    Ok(terms
        .iter()
        .map(|term| (term.cell.clone(), term.coefficient))
        .collect())
}

fn natural(text: &str) -> Result<usize> {
    if text.is_empty() || !text.bytes().all(|b| b.is_ascii_digit()) {
        return Err("parameters must be unsigned decimal integers".into());
    }
    Ok(text.parse()?)
}

fn problem(n: usize, degree: usize) -> Result<Cell> {
    if !(4..=128).contains(&n) || degree > 2 {
        return Err("demo requires 4 <= N <= 128 and 0 <= degree <= 2".into());
    }
    let (mut cell, used) = match degree {
        0 => (vec![vec![0, 2], vec![1], vec![3]], 4),
        1 => (vec![vec![0, 2], vec![1, 3]], 4),
        2 => (vec![vec![0, 2], vec![1, 4], vec![3, 5]], 6),
        _ => return Err("unsupported degree".into()),
    };
    cell.extend((used..2 * n).map(|label| vec![label]));
    Ok(cell)
}

fn run() -> Result<serde_json::Value> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() != 3 && args.len() != 5 {
        return Err("usage: sparse_guarded_transport demo N DEGREE [--certificate-out PATH] | verify N DEGREE --certificate PATH".into());
    }
    let n = natural(&args[1])?;
    let degree = natural(&args[2])?;
    let cell = problem(n, degree)?;
    let limits = ContractionLimits {
        max_labels: 2 * n,
        ..Default::default()
    };
    let cycle = boundary(&cell, limits)?;
    let original = BTreeMap::from([(cell, 1)]);
    match args[0].as_str() {
        "demo" => {
            if args.len() == 5 && args[3] != "--certificate-out" {
                return Err("demo expects optional --certificate-out PATH".into());
            }
            let start = Instant::now();
            let mut maps =
                SparseTransport::new_minimum_sweep(n, 3, limits, SparseTransportLimits::default())?;
            let reduced_filling = maps.project(&original, degree + 1)?;
            let reduced_cycle = maps.project(&cycle, degree)?;
            let projected_boundary = engine_homology::permutohedral::boundary_chain(
                &reduced_filling,
                n,
                degree + 1,
                limits,
            )?;
            if projected_boundary != reduced_cycle {
                return Err("projection chain-map identity failed".into());
            }
            let mut filling = maps.include(&reduced_filling, degree + 1)?;
            let homotopy = maps.homotopy(&cycle, degree)?;
            add_scaled(&mut filling, &homotopy, -1, limits)?;
            let construction_us = start.elapsed().as_micros();
            let start = Instant::now();
            verify_sparse_event_filling(n, 3, &cycle, &filling, degree, limits)?;
            let verify_us = start.elapsed().as_micros();
            let start = Instant::now();
            verify_sparse_event_filling(n, 3, &cycle, &original, degree, limits)?;
            let direct_baseline_verify_us = start.elapsed().as_micros();
            let certificate = Certificate {
                schema: "omega.wdp.sparse-filling-demo.v2".into(),
                pairs: n,
                capacity: 3,
                degree,
                cycle: encode(&cycle),
                filling: encode(&filling),
            };
            let bytes = serde_json::to_vec(&certificate)?;
            if bytes.len() as u64 > MAX_BYTES {
                return Err("certificate exceeds byte limit".into());
            }
            if args.len() == 5 {
                let mut file = OpenOptions::new()
                    .write(true)
                    .create_new(true)
                    .open(&args[4])?;
                file.write_all(&bytes)?;
                file.sync_all()?;
            }
            Ok(
                json!({"status":"PASS", "authority_effect":"None", "mode":"demo",
                "method":"minimum_sweep_v2", "pairs":n, "capacity":3, "degree":degree,
                "input_cycle_terms":cycle.len(), "reduced_cycle_terms":reduced_cycle.len(),
                "reduced_filling_terms":reduced_filling.len(), "native_filling_terms":filling.len(),
                "certificate_bytes":bytes.len(), "construction_microseconds":construction_us,
                "verification_microseconds":verify_us, "stats":maps.stats(),
                "direct_baseline":{"supplied_filling_terms":original.len(),
                    "verification_microseconds":direct_baseline_verify_us,
                    "scope":"explicit known filler for this fixture; no search required"},
                "ambient_enumeration":false}),
            )
        }
        "verify" => {
            if args.len() != 5 || args[3] != "--certificate" {
                return Err("verify requires --certificate PATH".into());
            }
            let mut bytes = Vec::new();
            File::open(&args[4])?
                .take(MAX_BYTES + 1)
                .read_to_end(&mut bytes)?;
            if bytes.len() as u64 > MAX_BYTES {
                return Err("certificate exceeds byte limit".into());
            }
            let supplied: Certificate = serde_json::from_slice(&bytes)?;
            if supplied.schema != "omega.wdp.sparse-filling-demo.v2"
                || supplied.pairs != n
                || supplied.capacity != 3
                || supplied.degree != degree
                || decode(&supplied.cycle)? != cycle
            {
                return Err(
                    "certificate does not match the independently supplied demo problem".into(),
                );
            }
            let filling = decode(&supplied.filling)?;
            let start = Instant::now();
            verify_sparse_event_filling(n, 3, &cycle, &filling, degree, limits)?;
            Ok(
                json!({"status":"PASS", "authority_effect":"None", "mode":"verify",
                "pairs":n,"degree":degree,"certificate_bytes":bytes.len(),
                "verification_microseconds":start.elapsed().as_micros(),
                "ambient_enumeration":false,"transport_constructor_called":false}),
            )
        }
        _ => Err("unknown command".into()),
    }
}

fn main() {
    match run() {
        Ok(report) => println!("{report}"),
        Err(error) => {
            eprintln!(
                "{}",
                json!({"status":"REFUSED","authority_effect":"None","error":error.to_string()})
            );
            std::process::exit(2);
        }
    }
}
