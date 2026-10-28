use num_rational::BigRational;
use num_traits::Zero;
use tfqm_holonomy::signed_transport::{
    certify_signed_transport, SignedCoefficientGraph, SignedTransportCertificate,
};
use engine_number_theory::cyclotomic::GaussianRat;
use engine_quantum_physics::signed_sampling::{
    finite_transfer_partition, verify_real_hamiltonian_step, SignedWeightFamily,
};
use engine_wdp::genesis_computation::{
    NamedConfiguration, SourceBooleanPacket, SourceMachinePacket, SourcePrefix,
};
use engine_wdp::genesis_geometry::{
    chain_report, metric_report, sheaf_report, verify_source_incidence, ComplexPacket,
    MetricPacket, SheafPacket, SourceIncidenceState,
};
use serde::Deserialize;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::io::{self, Read};

#[derive(Deserialize)]
#[serde(tag = "operation", rename_all = "snake_case", deny_unknown_fields)]
enum NativeRequest {
    BooleanGraph {
        packet: SourceBooleanPacket,
    },
    MachinePrefix {
        packet: SourceMachinePacket,
        initial: NamedConfiguration,
        bound: usize,
        #[serde(default)]
        candidate: Option<SourcePrefix>,
    },
    SignedTransport {
        coefficients: Vec<Vec<String>>,
        #[serde(default)]
        certificate: Option<SignedTransportCertificate>,
    },
    SignedSampling {
        weights: Vec<String>,
        samples: usize,
        copies: usize,
    },
    HamiltonianTransfer {
        coefficients: Vec<Vec<String>>,
        step: String,
        slices: usize,
        samples: usize,
        copies: usize,
        amplitudes: Vec<[String; 2]>,
    },
    Chain {
        packet: ComplexPacket,
        source_state: SourceIncidenceState,
    },
    Sheaf {
        packet: SheafPacket,
    },
    Metric {
        packet: MetricPacket,
        source_state: SourceIncidenceState,
    },
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct MetricRequest {
    operation: String,
    packet: MetricPacket,
    source_state: SourceIncidenceState,
}

fn parse_request(input: &str) -> Result<NativeRequest, String> {
    let header: Value = serde_json::from_str(input).map_err(|e| e.to_string())?;
    if header.get("operation").and_then(Value::as_str) == Some("metric") {
        let wire: MetricRequest = serde_json::from_str(input).map_err(|e| e.to_string())?;
        if wire.operation != "metric" {
            return Err("metric operation discriminator changed".into());
        }
        Ok(NativeRequest::Metric {
            packet: wire.packet,
            source_state: wire.source_state,
        })
    } else {
        serde_json::from_str(input).map_err(|e| e.to_string())
    }
}

fn rational(text: &str) -> Result<BigRational, String> {
    let graph = SignedCoefficientGraph::from_strings(&[vec![text.to_string()]])
        .map_err(|e| e.to_string())?;
    Ok(graph.coefficients()[0][0].clone())
}

fn family_report(
    family: &SignedWeightFamily,
    samples: usize,
    copies: usize,
) -> Result<Value, String> {
    if copies > 1024 {
        return Err("independent-copy bound is 1024".into());
    }
    let copied = family
        .independent_copies(copies)
        .map_err(|e| e.to_string())?;
    let variance = family
        .iid_sign_mean_variance(samples)
        .map_err(|e| e.to_string())?;
    let relative = if family.signed_mass().is_zero() {
        None
    } else {
        Some(
            family
                .iid_relative_variance(samples)
                .map_err(|e| e.to_string())?
                .to_string(),
        )
    };
    Ok(json!({
        "signed_mass": family.signed_mass().to_string(),
        "absolute_mass": family.absolute_mass().to_string(),
        "average_sign": family.average_sign().to_string(),
        "iid_sign_mean_variance": variance.to_string(),
        "iid_relative_variance": relative,
        "relative_variance_status": if relative.is_some() {"defined"} else {"undefined_zero_signed_sum"},
        "independent_copies": copies,
        "product_average_sign": copied.average_sign().to_string(),
        "sampling_law": "iid draws from declared absolute-weight distribution",
    }))
}

fn execute(request: NativeRequest) -> Result<(&'static str, Value), String> {
    match request {
        NativeRequest::BooleanGraph { packet } => {
            if packet.arity > 12 {
                return Err("native Boolean graph arity bound is 12".into());
            }
            let checked = packet.admit().map_err(|e| format!("{e:?}"))?;
            let cnf = checked.graph_cnf();
            checked.verify_cnf(&cnf).map_err(|e| format!("{e:?}"))?;
            let clauses: Vec<_> = cnf
                .clauses
                .iter()
                .map(|c| {
                    c.iter()
                        .map(|l| {
                            json!({
                                "variable": l.variable, "positive": l.positive,
                            })
                        })
                        .collect::<Vec<_>>()
                })
                .collect();
            let rows = 1usize << packet.arity;
            let outputs = (0..rows)
                .map(|index| {
                    let inputs: Vec<_> = (0..packet.arity)
                        .map(|i| (index >> (packet.arity - 1 - i)) & 1)
                        .collect();
                    checked.readout(&inputs).map_err(|e| format!("{e:?}"))
                })
                .collect::<Result<Vec<_>, _>>()?;
            Ok((
                "boolean_graph",
                json!({
                    "outputs": outputs,
                    "cnf": {"variables": cnf.variables, "clauses": clauses},
                    "cnf_verified_on_all_assignments": true,
                }),
            ))
        }
        NativeRequest::MachinePrefix {
            packet,
            initial,
            bound,
            candidate,
        } => {
            if bound > 100_000 {
                return Err("native machine finite-prefix bound is 100000".into());
            }
            let checked = packet.admit().map_err(|e| format!("{e:?}"))?;
            let prefix = checked
                .execute(&initial, bound)
                .map_err(|e| format!("{e:?}"))?
                .export();
            checked
                .verify_prefix(&initial, bound, candidate.as_ref().unwrap_or(&prefix))
                .map_err(|e| format!("{e:?}"))?;
            Ok((
                "machine_prefix",
                json!({"prefix": prefix, "independent_replay": true}),
            ))
        }
        NativeRequest::SignedTransport {
            coefficients,
            certificate,
        } => {
            let graph =
                SignedCoefficientGraph::from_strings(&coefficients).map_err(|e| e.to_string())?;
            let cert = certificate.unwrap_or_else(|| certify_signed_transport(&graph));
            cert.verify(&graph).map_err(|e| e.to_string())?;
            Ok((
                "signed_transport",
                json!({"certificate": cert, "verified": true}),
            ))
        }
        NativeRequest::SignedSampling {
            weights,
            samples,
            copies,
        } => {
            let parsed = weights
                .iter()
                .map(|w| rational(w))
                .collect::<Result<Vec<_>, _>>()?;
            let family = SignedWeightFamily::try_new(&parsed).map_err(|e| e.to_string())?;
            Ok(("signed_sampling", family_report(&family, samples, copies)?))
        }
        NativeRequest::HamiltonianTransfer {
            coefficients,
            step,
            slices,
            samples,
            copies,
            amplitudes,
        } => {
            let graph =
                SignedCoefficientGraph::from_strings(&coefficients).map_err(|e| e.to_string())?;
            let step = rational(&step)?;
            let psi = amplitudes
                .iter()
                .map(|z| {
                    Ok(GaussianRat {
                        re: rational(&z[0])?,
                        im: rational(&z[1])?,
                    })
                })
                .collect::<Result<Vec<_>, String>>()?;
            let cert = certify_signed_transport(&graph);
            cert.verify(&graph).map_err(|e| e.to_string())?;
            let dynamics = verify_real_hamiltonian_step(graph.coefficients(), &step, &psi)
                .map_err(|e| e.to_string())?;
            let family =
                finite_transfer_partition(&graph, &step, slices).map_err(|e| e.to_string())?;
            let defect: Vec<Vec<_>> = (0..graph.dimension())
                .map(|i| {
                    (0..graph.dimension())
                        .map(|j| {
                            let z = dynamics
                                .euler_unitarity_defect
                                .get_ref(i, j)
                                .map_err(|e| format!("Euler defect entry refused: {e:?}"))?;
                            Ok([z.re.to_string(), z.im.to_string()])
                        })
                        .collect::<Result<Vec<_>, String>>()
                })
                .collect::<Result<Vec<_>, String>>()?;
            Ok((
                "hamiltonian_transfer",
                json!({
                    "original_coefficients": graph.canonical_coefficients(),
                    "transport_certificate": cert,
                    "hermitian": true,
                    "instantaneous_norm_rate": dynamics.norm_rate.to_string(),
                    "euler_unitarity_defect": defect,
                    "euler_defect_identity": "tau^2 H^2",
                    "partition": family_report(&family, samples, copies)?,
                    "transfer_law": "T=I-step*H; finite Tr(T^slices)",
                    "thermal_exponential": false,
                }),
            ))
        }
        NativeRequest::Chain {
            packet,
            source_state,
        } => {
            verify_source_incidence(&packet, &source_state).map_err(|e| format!("{e:?}"))?;
            let report = chain_report(&packet).map_err(|e| format!("{e:?}"))?;
            Ok((
                "chain",
                json!({"report": report, "source_incidence_verified": true}),
            ))
        }
        NativeRequest::Sheaf { packet } => {
            let report = sheaf_report(&packet).map_err(|e| format!("{e:?}"))?;
            let fibers: Vec<_> = report
                .matching_fibers
                .iter()
                .map(|f| {
                    json!({
                        "local_sections": f.local_sections,
                        "global_sections": f.global_sections,
                    })
                })
                .collect();
            Ok((
                "sheaf",
                json!({
                    "target": report.target, "cover": report.cover,
                    "matching_fibers": fibers,
                    "is_separated": report.is_separated,
                    "has_existence": report.has_existence,
                    "is_sheaf_cover": report.is_sheaf_cover,
                }),
            ))
        }
        NativeRequest::Metric {
            packet,
            source_state,
        } => {
            verify_source_incidence(&packet.complex, &source_state)
                .map_err(|e| format!("{e:?}"))?;
            let report = metric_report(&packet).map_err(|e| format!("{e:?}"))?;
            Ok((
                "metric",
                json!({"report": report, "source_incidence_verified": true, "angle_scope": "floating Euclidean diagnostics"}),
            ))
        }
    }
}

fn main() -> Result<(), String> {
    let mut input = String::new();
    io::stdin()
        .take(16 * 1024 * 1024 + 1)
        .read_to_string(&mut input)
        .map_err(|e| e.to_string())?;
    if input.len() > 16 * 1024 * 1024 {
        return Err("native input exceeds declared 16 MiB bound".into());
    }
    let request = parse_request(&input)?;
    let (operation, result) = execute(request)?;
    let request_sha256 = format!("{:x}", Sha256::digest(input.as_bytes()));
    println!(
        "{}",
        json!({
            "schema": "genesis-native-extension/v1",
            "authority_effect": "None",
            "operation": operation,
            "request_sha256": request_sha256,
            "result": result,
        })
    );
    Ok(())
}
