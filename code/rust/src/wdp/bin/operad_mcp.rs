
use std::fs;
use std::io::{self, BufRead, Write};
use engine_wdp::ddc::parser::DdcTapeParser;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};

#[derive(Debug, Deserialize)]
struct JsonRpcRequest {
    #[allow(dead_code)]
    jsonrpc: String,
    id: Option<Value>,
    method: String,
    #[serde(default)]
    params: Option<Value>,
}

#[derive(Debug, Serialize)]
struct JsonRpcResponse {
    jsonrpc: &'static str,
    #[serde(skip_serializing_if = "Option::is_none")]
    id: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    result: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<Value>,
}

fn handle_initialize(id: Option<Value>) -> JsonRpcResponse {
    JsonRpcResponse {
        jsonrpc: "2.0",
        id,
        result: Some(json!({
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "omega-operad-mcp",
                "version": "0.1.0"
            }
        })),
        error: None,
    }
}

fn handle_tools_list(id: Option<Value>) -> JsonRpcResponse {
    JsonRpcResponse {
        jsonrpc: "2.0",
        id,
        result: Some(json!({
            "tools": [
                {
                    "name": "operad_parse_ddc_tape",
                    "description": "Parses a DDC event tape, verifies hash-chain integrity, enforces 8-letter candidate runtime laws, and computes exact rational residual contraction receipts.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "tape_path": {
                                "type": "string",
                                "description": "Absolute or relative path to ddc.jsonl"
                            },
                            "tape_content": {
                                "type": "string",
                                "description": "Raw JSONL content string to parse directly"
                            }
                        }
                    }
                },
                {
                    "name": "operad_verify_laws",
                    "description": "Verifies candidate algebraic runtime laws (alphabet, terminal absorption, and exact monotonic repair) on a set of DDC action records.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "records_json": {
                                "type": "string",
                                "description": "JSON array of DDC step records"
                            }
                        },
                        "required": ["records_json"]
                    }
                }
            ]
        })),
        error: None,
    }
}

fn handle_tools_call(id: Option<Value>, params: Option<Value>) -> JsonRpcResponse {
    let p = match params {
        Some(Value::Object(map)) => map,
        _ => {
            return JsonRpcResponse {
                jsonrpc: "2.0",
                id,
                result: None,
                error: Some(json!({
                    "code": -32602,
                    "message": "Invalid params"
                })),
            };
        }
    };

    let tool_name = p.get("name").and_then(|v| v.as_str()).unwrap_or("");
    let arguments = p.get("arguments").cloned().unwrap_or(json!({}));

    match tool_name {
        "operad_parse_ddc_tape" => {
            let content = if let Some(raw) = arguments.get("tape_content").and_then(|v| v.as_str()) {
                raw.to_string()
            } else if let Some(path_str) = arguments.get("tape_path").and_then(|v| v.as_str()) {
                match fs::read_to_string(path_str) {
                    Ok(c) => c,
                    Err(e) => {
                        return JsonRpcResponse {
                            jsonrpc: "2.0",
                            id,
                            result: Some(json!({
                                "content": [{
                                    "type": "text",
                                    "text": format!("Error reading tape file '{}': {e}", path_str)
                                }],
                                "isError": true
                            })),
                            error: None,
                        };
                    }
                }
            } else {
                return JsonRpcResponse {
                    jsonrpc: "2.0",
                    id,
                    result: Some(json!({
                        "content": [{
                            "type": "text",
                            "text": "Either 'tape_path' or 'tape_content' must be provided."
                        }],
                        "isError": true
                    })),
                    error: None,
                };
            };

            match DdcTapeParser::parse_jsonl(&content) {
                Ok(receipt) => {
                    let receipt_str = serde_json::to_string_pretty(&receipt).unwrap();
                    JsonRpcResponse {
                        jsonrpc: "2.0",
                        id,
                        result: Some(json!({
                            "content": [{
                                "type": "text",
                                "text": receipt_str
                            }],
                            "isError": !receipt.ddc_laws_valid || !receipt.hash_chain_valid
                        })),
                        error: None,
                    }
                }
                Err(refusal) => {
                    let refusal_str = serde_json::to_string_pretty(&json!({
                        "status": "REFUSAL",
                        "code": refusal.code,
                        "message": refusal.message,
                        "locus": refusal.locus,
                        "authority_effect": "None"
                    }))
                    .unwrap();
                    JsonRpcResponse {
                        jsonrpc: "2.0",
                        id,
                        result: Some(json!({
                            "content": [{
                                "type": "text",
                                "text": refusal_str
                            }],
                            "isError": true
                        })),
                        error: None,
                    }
                }
            }
        }
        "operad_verify_laws" => {
            let records_str = arguments
                .get("records_json")
                .and_then(|v| v.as_str())
                .unwrap_or("[]");
            let records_val: Result<Vec<Value>, _> = serde_json::from_str(records_str);
            match records_val {
                Ok(records) => match DdcTapeParser::parse_records(&records) {
                    Ok(receipt) => JsonRpcResponse {
                        jsonrpc: "2.0",
                        id,
                        result: Some(json!({
                            "content": [{
                                "type": "text",
                                "text": serde_json::to_string_pretty(&json!({
                                    "ddc_laws_valid": receipt.ddc_laws_valid,
                                    "law_violations": receipt.law_violations,
                                    "tape_str": receipt.tape_str,
                                    "residual_effect": receipt.residual_effect,
                                    "residual_delta": receipt.residual_delta
                                })).unwrap()
                            }]
                        })),
                        error: None,
                    },
                    Err(refusal) => JsonRpcResponse {
                        jsonrpc: "2.0",
                        id,
                        result: Some(json!({
                            "content": [{
                                "type": "text",
                                "text": format!("Refusal: {refusal}")
                            }],
                            "isError": true
                        })),
                        error: None,
                    },
                },
                Err(e) => JsonRpcResponse {
                    jsonrpc: "2.0",
                    id,
                    result: Some(json!({
                        "content": [{
                            "type": "text",
                            "text": format!("JSON parse error in records_json: {e}")
                        }],
                        "isError": true
                    })),
                    error: None,
                },
            }
        }
        _ => JsonRpcResponse {
            jsonrpc: "2.0",
            id,
            result: None,
            error: Some(json!({
                "code": -32601,
                "message": format!("Tool not found: {tool_name}")
            })),
        },
    }
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut stdout = io::stdout();

    for line in stdin.lock().lines() {
        let raw = match line {
            Ok(l) => l,
            Err(e) => {
                eprintln!("Error reading stdin line: {e}");
                break;
            }
        };

        let trimmed = raw.trim();
        if trimmed.is_empty() {
            continue;
        }

        let req: JsonRpcRequest = match serde_json::from_str(trimmed) {
            Ok(r) => r,
            Err(e) => {
                let err_resp = JsonRpcResponse {
                    jsonrpc: "2.0",
                    id: None,
                    result: None,
                    error: Some(json!({
                        "code": -32700,
                        "message": format!("Parse error: {e}")
                    })),
                };
                writeln!(stdout, "{}", serde_json::to_string(&err_resp).unwrap())?;
                stdout.flush()?;
                continue;
            }
        };

        let resp = match req.method.as_str() {
            "initialize" => Some(handle_initialize(req.id)),
            "notifications/initialized" => None,
            "tools/list" => Some(handle_tools_list(req.id)),
            "tools/call" => Some(handle_tools_call(req.id, req.params)),
            "ping" => Some(JsonRpcResponse {
                jsonrpc: "2.0",
                id: req.id,
                result: Some(json!({})),
                error: None,
            }),
            _ => Some(JsonRpcResponse {
                jsonrpc: "2.0",
                id: req.id,
                result: None,
                error: Some(json!({
                    "code": -32601,
                    "message": format!("Method not found: {}", req.method)
                })),
            }),
        };

        if let Some(r) = resp {
            writeln!(stdout, "{}", serde_json::to_string(&r).unwrap())?;
            stdout.flush()?;
        }
    }

    Ok(())
}
