//! Native finite fixtures for lesson 720.24. No input parser or Python solver.
use linear_algebra::backend::basic_matrix::OperationLimits;
use num_bigint::BigInt;
use num_traits::One;
use omega_wdp::genesis_balance_transition::{BalanceVerdict, Source25BalanceProfile};
use omega_wdp::genesis_ongoing_adapter::{GenesisOngoingPacket, MarkedTriple};
use omega_wdp::genesis_source_execution::{Source25Change, Source25State, SourceRelation};
use serde_json::{json, Value};

fn state(faces: Vec<MarkedTriple>, one_arc: bool) -> Source25State {
    let mut r = vec![BigInt::one(); 16];
    if one_arc {
        r[8] += BigInt::one();
    }
    Source25State::try_new(GenesisOngoingPacket {
        terms: (0..4).map(|i| format!("t{i}")).collect(),
        r,
        s: vec![BigInt::one(); 16],
        filled: faces,
    })
    .expect("fixed native fixture")
}
fn raw(source: &Source25State) -> Value {
    let p = source.packet();
    json!({"terms":p.terms,
        "r":p.r.iter().map(ToString::to_string).collect::<Vec<_>>(),
        "s":p.s.iter().map(ToString::to_string).collect::<Vec<_>>(),
        "filled":p.filled.iter().map(|t| [t.x,t.y,t.z]).collect::<Vec<_>>()})
}
fn case(name: &str, source: Source25State, event: Source25Change) -> Value {
    let p = Source25BalanceProfile::new(source, event, OperationLimits::UNLIMITED)
        .expect("fixed enabled event");
    p.verify().expect("certificate replay");
    let counter = match p.verdict() {
        BalanceVerdict::Preserved(_) => Value::Null,
        BalanceVerdict::Obstructed(w) => {
            json!({"value":w.value().to_string(),"source":raw(w.source()),"target":raw(w.target())})
        }
    };
    json!({"name":name,"universal_preserves":matches!(p.verdict(),BalanceVerdict::Preserved(_)),
        "actual_before_balanced":p.actual_source_balanced(),"actual_after_balanced":p.actual_target_balanced(),
        "counterexample":counter,"source":raw(p.source()),"target":raw(p.target())})
}
fn main() {
    let face = MarkedTriple { x: 0, y: 1, z: 2 };
    let source = state(vec![face], false);
    let mut seven = vec![];
    for x in 0..4 {
        for y in x + 1..4 {
            for z in y + 1..4 {
                for t in [MarkedTriple { x, y, z }, MarkedTriple { x, y: z, z: y }] {
                    if t != face {
                        seven.push(t);
                    }
                }
            }
        }
    }
    seven.sort();
    let three = vec![
        MarkedTriple { x: 0, y: 1, z: 3 },
        MarkedTriple { x: 0, y: 2, z: 3 },
        MarkedTriple { x: 1, y: 2, z: 3 },
    ];
    let cases = vec![
        case("add_term", source.clone(), Source25Change::AddTerm),
        case(
            "add_forward",
            source.clone(),
            Source25Change::AddAssertion {
                relation: SourceRelation::R,
                x: 0,
                y: 1,
            },
        ),
        case(
            "add_reverse",
            source.clone(),
            Source25Change::AddAssertion {
                relation: SourceRelation::R,
                x: 1,
                y: 0,
            },
        ),
        case(
            "remove_forward",
            source.clone(),
            Source25Change::Remove {
                relation: SourceRelation::R,
                x: 0,
                y: 1,
            },
        ),
        case(
            "identify_touching",
            source.clone(),
            Source25Change::Identify { x: 0, y: 3 },
        ),
        case(
            "fill_three_faces",
            state(three, true),
            Source25Change::Fill { x: 0, y: 1, z: 2 },
        ),
        case(
            "fill_seven_faces",
            state(seven, false),
            Source25Change::Fill { x: 0, y: 1, z: 2 },
        ),
    ];
    let disabled_refused = Source25BalanceProfile::new(
        source,
        Source25Change::Fill { x: 0, y: 1, z: 2 },
        OperationLimits::UNLIMITED,
    )
    .is_err();
    println!(
        "{}",
        json!({"cases":cases,"disabled_fill_refused":disabled_refused,"authority_effect":"None"})
    );
}
