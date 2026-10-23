//! Wire adapter only: all Source-25 state admission and transitions use omega_wdp.
use num_bigint::BigInt;
use omega_wdp::genesis_ongoing_adapter::{GenesisOngoingPacket, MarkedTriple};
use omega_wdp::genesis_source_execution::{Source25Change, Source25Run, Source25State};
use omega_wdp::native_future_compression::{generate_bounded_future, BoundedFutureCensus};
use serde::Deserialize;
use serde_json::{json, Value};
use std::io::{self, Read, Write};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct StateWire {
    terms: Vec<String>,
    r: Vec<String>,
    s: Vec<String>,
    filled: Vec<[usize; 3]>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Request {
    initial: StateWire,
    changes: Vec<Source25Change>,
}

#[derive(Deserialize)]
enum QueryName {
    #[serde(rename = "bounded_future")]
    BoundedFuture,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct QueryRequest {
    query: QueryName,
}

enum InputRequest {
    Replay(Request),
    Query(QueryName),
}

enum Response {
    Replay(Value),
    Census(BoundedFutureCensus),
}

fn counts(values: Vec<String>) -> Result<Vec<BigInt>, String> {
    values
        .into_iter()
        .map(|text| {
            let n = text.parse::<BigInt>().map_err(|e| e.to_string())?;
            if n.to_string() != text {
                return Err("noncanonical integer".into());
            }
            Ok(n)
        })
        .collect()
}

fn wire(state: &Source25State) -> Value {
    let p = state.packet();
    json!({
        "terms": p.terms, "r": p.r.iter().map(ToString::to_string).collect::<Vec<_>>(),
        "s": p.s.iter().map(ToString::to_string).collect::<Vec<_>>(),
        "filled": p.filled.iter().map(|t| [t.x,t.y,t.z]).collect::<Vec<_>>(),
        "source_size": state.source_size().to_string(),
        "plain_state_cost": state.plain_state_cost().to_string(),
    })
}

fn replay(request: Request) -> Result<Value, String> {
    let input = request.initial;
    let initial = Source25State::try_new(GenesisOngoingPacket {
        terms: input.terms,
        r: counts(input.r)?,
        s: counts(input.s)?,
        filled: input
            .filled
            .into_iter()
            .map(|t| MarkedTriple {
                x: t[0],
                y: t[1],
                z: t[2],
            })
            .collect(),
    })
    .map_err(|e| e.to_string())?;
    let run = Source25Run::replay(initial, &request.changes).map_err(|e| e.to_string())?;
    let (terms, assertions) = run.addition_price();
    Ok(
        json!({"states": run.states().iter().map(wire).collect::<Vec<_>>(),
        "changes": run.changes(), "addition_price": [terms.to_string(),assertions.to_string()]}),
    )
}

/// An exact query is recognised first; anything else is parsed as a replay
/// request, so a malformed replay keeps serde's field-level refusal reason.
fn parse(text: &str) -> Result<InputRequest, String> {
    if let Ok(QueryRequest { query }) = serde_json::from_str::<QueryRequest>(text) {
        return Ok(InputRequest::Query(query));
    }
    serde_json::from_str::<Request>(text)
        .map(InputRequest::Replay)
        .map_err(|e| e.to_string())
}

fn dispatch(text: &str) -> Result<Response, String> {
    match parse(text)? {
        InputRequest::Replay(request) => replay(request).map(Response::Replay),
        InputRequest::Query(QueryName::BoundedFuture) => generate_bounded_future()
            .map(Response::Census)
            .map_err(|e| e.to_string()),
    }
}

fn main() {
    let mut text = String::new();
    let read = io::stdin().take(1_048_577).read_to_string(&mut text);
    let result = if read.is_err() || text.len() > 1_048_576 {
        Err("input unavailable or above one MiB bound".into())
    } else {
        dispatch(&text)
    };
    match result {
        Ok(Response::Replay(run)) => println!(
            "{}",
            json!({"schema":"wdp-source25-native-v1","status":"PASS","authority_effect":"None","run":run})
        ),
        Ok(Response::Census(census)) => {
            let mut output = io::stdout().lock();
            if serde_json::to_writer(&mut output, &census).is_err()
                || output.write_all(b"\n").is_err()
            {
                eprintln!("census output could not be written");
                std::process::exit(2);
            }
        }
        Err(reason) => {
            println!(
                "{}",
                json!({"schema":"wdp-source25-native-v1","status":"REFUSE","authority_effect":"None","reason":reason})
            );
            std::process::exit(2);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bounded_query_is_exact_and_replay_shape_stays_available() {
        assert!(matches!(
            parse(r#"{"query":"bounded_future"}"#),
            Ok(InputRequest::Query(QueryName::BoundedFuture))
        ));
        assert!(matches!(
            parse(r#"{"initial":{"terms":[],"r":[],"s":[],"filled":[]},"changes":[]}"#),
            Ok(InputRequest::Replay(_))
        ));
        for text in [
            r#"{}"#,
            r#"{"query":"unknown"}"#,
            r#"{"query":"bounded_future","extra":0}"#,
            r#"{"query":"bounded_future","query":"bounded_future"}"#,
            r#"{"query":"bounded_future","changes":[]}"#,
            r#"{"query":null}"#,
            r#"{"query":["bounded_future"]}"#,
            r#"{"query":"bounded_future"} {}"#,
        ] {
            assert!(parse(text).is_err(), "accepted {text}");
        }
    }

    #[test]
    fn malformed_replay_request_keeps_its_field_reason() {
        let reason = match parse(
            r#"{"initial":{"terms":[],"r":[],"s":[],"filled":[]},"chnages":[]}"#,
        ) {
            Err(reason) => reason,
            Ok(_) => panic!("accepted a misspelled replay field"),
        };
        assert!(reason.contains("unknown field `chnages`"), "{reason}");
    }
}
