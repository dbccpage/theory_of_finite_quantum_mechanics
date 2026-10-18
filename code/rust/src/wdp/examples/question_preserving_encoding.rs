//! JSON-only local driver for the bounded WDP encoding experiment.
use std::io::{self, Read};

use omega_wdp::question_preserving_encoding::{experiment, verify_cochain, verify_direct, Task};
use serde::Deserialize;
use serde_json::json;

#[derive(Deserialize)]
#[serde(tag = "action", rename_all = "snake_case", deny_unknown_fields)]
enum Request {
    Experiment,
    VerifyDirect { expected_task: Task, report: String },
    VerifyCochain { expected_task: Task, report: String },
}

fn main() {
    let mut input = String::new();
    if io::stdin().take(4097).read_to_string(&mut input).is_err() || input.len() > 4096 {
        eprintln!("request exceeds input contract");
        std::process::exit(2);
    }
    let request = match serde_json::from_str::<Request>(&input) {
        Ok(request) => request,
        Err(error) => {
            eprintln!("invalid request: {error}");
            std::process::exit(2);
        }
    };
    let result = match request {
        Request::Experiment => experiment(),
        Request::VerifyDirect {
            expected_task,
            report,
        } => verify_direct(expected_task, &report)
            .map(|accepted| json!({"accepted":accepted,"authority_effect":"None"})),
        Request::VerifyCochain {
            expected_task,
            report,
        } => verify_cochain(expected_task, &report)
            .map(|accepted| json!({"accepted":accepted,"authority_effect":"None"})),
    };
    match result {
        Ok(value) => println!("{}", serde_json::to_string(&value).expect("JSON value")),
        Err(refusal) => {
            println!("{}", json!({"refused":refusal,"authority_effect":"None"}));
            std::process::exit(2);
        }
    }
}
