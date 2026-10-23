// Executable finite evidence; AuthorityEffect: None.
use serde::{Deserialize, Serialize};
use std::io::{self, Read};
use wdp_finite_witness::genesis_observer::{DescentResult, HistoryMemory, WordTransducer};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Request {
    memory_transitions: Vec<Vec<usize>>,
    memory_initial: usize,
    transducer_transitions: Vec<Vec<usize>>,
    transducer_emit: Vec<Vec<Vec<usize>>>,
    transducer_initial: usize,
    prefix_words: Vec<usize>,
    final_words: Vec<Vec<usize>>,
}

#[derive(Serialize)]
struct Response {
    status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    kind: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    prefix: Option<Vec<usize>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    certificate: Option<Vec<Option<usize>>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    collision_first: Option<Vec<usize>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    collision_second: Option<Vec<usize>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    authority_effect: Option<String>,
}

fn main() {
    let mut buffer = String::new();
    if let Err(e) = io::stdin().read_to_string(&mut buffer) {
        let resp = Response {
            status: "REFUSE".into(),
            reason: Some(format!("Failed to read stdin: {}", e)),
            kind: None,
            prefix: None,
            certificate: None,
            collision_first: None,
            collision_second: None,
            authority_effect: None,
        };
        println!("{}", serde_json::to_string(&resp).unwrap());
        return;
    }

    let req: Request = match serde_json::from_str(&buffer) {
        Ok(r) => r,
        Err(e) => {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("JSON parse error: {}", e)),
                kind: None,
                prefix: None,
                certificate: None,
                collision_first: None,
                collision_second: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
    };

    let memory = match HistoryMemory::new(req.memory_transitions, req.memory_initial) {
        Ok(m) => m,
        Err(e) => {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("Memory error: {}", e)),
                kind: None,
                prefix: None,
                certificate: None,
                collision_first: None,
                collision_second: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
    };

    let transducer = match WordTransducer::new(
        req.transducer_transitions,
        req.transducer_emit,
        req.transducer_initial,
        req.prefix_words,
        req.final_words,
    ) {
        Ok(t) => t,
        Err(e) => {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("Transducer error: {}", e)),
                kind: None,
                prefix: None,
                certificate: None,
                collision_first: None,
                collision_second: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
    };

    match transducer.descent(&memory) {
        Ok(DescentResult::Map { prefix, certificate }) => {
            let resp = Response {
                status: "PASS".into(),
                reason: None,
                kind: Some("map".into()),
                prefix: Some(prefix),
                certificate: Some(certificate),
                collision_first: None,
                collision_second: None,
                authority_effect: Some("None".into()),
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
        }
        Ok(DescentResult::Collision { first, second }) => {
            let resp = Response {
                status: "PASS".into(),
                reason: None,
                kind: Some("collision".into()),
                prefix: None,
                certificate: None,
                collision_first: Some(first),
                collision_second: Some(second),
                authority_effect: Some("None".into()),
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
        }
        Err(error) => {
            println!("{}", serde_json::json!({"status": "REFUSE", "reason": error.to_string(), "authority_effect": "None"}));
        }
    }
}
