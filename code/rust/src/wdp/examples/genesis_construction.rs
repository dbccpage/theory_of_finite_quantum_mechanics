use engine_wire_primitives::{event::Event, mark::Mark};
use engine_wdp::genesis_construction::{
    cycle_construction, verify_history_report, GenesisConstruction,
};
use serde_json::json;

fn run() -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let pre = GenesisConstruction::pre_genesis();
    let seed = GenesisConstruction::from_literal_seed()?;
    let cycle = cycle_construction(["<a>", "<ab>", "<c>"])?;
    let cycle_report = cycle.homology()?;
    verify_history_report(cycle.history(), &cycle_report)?;
    let filled = cycle.advance(Event::AdmitInst(2, vec![Mark(0), Mark(1), Mark(2)]))?;
    let filled_report = filled.homology()?;
    verify_history_report(filled.history(), &filled_report)?;
    Ok(json!({
        "schema": "wdp.genesis-construction.v1",
        "pre_genesis": {"events": pre.history().len(), "admitted_data": pre.regime().n_data()},
        "literal_seed": {"event": seed.history()[0].to_string(), "admitted_data": seed.regime().n_data()},
        "history": filled.history().iter().map(ToString::to_string).collect::<Vec<_>>(),
        "cycle": {"event_count": cycle.history().len(), "homology": cycle_report},
        "filled_triangle": {"event_count": filled.history().len(), "homology": filled_report},
        "construction_choices": [
            "deduplicating canonical primitive admission",
            "arity-k admitted instances interpreted as (k-1)-simplices",
            "signed rational chains through omega_homology",
            "explicit final face admission changes the first homology"
        ],
        "authority_effect": "None"
    }))
}

fn main() {
    match run().and_then(|value| Ok(serde_json::to_string_pretty(&value)?)) {
        Ok(output) => println!("{output}"),
        Err(error) => {
            eprintln!("construction failed: {error}");
            std::process::exit(1);
        }
    }
}
