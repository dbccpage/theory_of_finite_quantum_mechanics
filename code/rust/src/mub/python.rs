//! Thin PyO3 face for Jupyter / reviewer notebooks.
//!
//! **SSOT of math remains Rust.** This module only serializes existing
//! assessments and runtime receipts to Python dicts. It does not reimplement
//! cyclotomic arithmetic, covers, SOS, or certificates in Python.
//!
//! Enable with features: `python` (and `extension-module` for a cdylib wheel).

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use serde::Serialize;

use crate::omega_native::float_check::d10_wall_status::current_d10_wall_status;
use crate::omega_native::exact::extension::{
    attempt_full_mub6_from_pinned_t0, attempt_general_mub_n, attempt_mub10,
};
use crate::primitive_map::{assess_d6_pinned_wall, assess_general_mub_n};
use crate::runtime_adapter::evaluate_mub6_json;

#[derive(Serialize)]
struct Mub6PyReceipt {
    terminal: String,
    authority_effect: String,
    cover_discharged: bool,
    tuple_hash: String,
    replay_hash: String,
}

fn to_py_dict(py: Python<'_>, value: &impl Serialize) -> PyResult<Py<PyAny>> {
    let encoded = serde_json::to_string(value).map_err(|error| {
        PyRuntimeError::new_err(format!("could not serialize omega_mub receipt: {error}"))
    })?;
    py.import("json")?
        .call_method1("loads", (encoded,))
        .map(|value| value.unbind())
}

/// Always `"None"` — this surface mints no authority.
#[pyfunction]
fn authority_effect() -> &'static str {
    "None"
}

/// Crate identity for notebooks.
#[pyfunction]
fn package_info(py: Python<'_>) -> PyResult<Py<PyAny>> {
    #[derive(Serialize)]
    struct Info {
        name: &'static str,
        math_ssot: &'static str,
        authority_effect: &'static str,
        note: &'static str,
    }
    to_py_dict(
        py,
        &Info {
            name: "omega_mub",
            math_ssot: "rust",
            authority_effect: "None",
            note: "Thin PyO3 adapter only; no Python math core.",
        },
    )
}

#[pyfunction]
fn assess_general_mub_n_py(py: Python<'_>) -> PyResult<Py<PyAny>> {
    to_py_dict(py, &assess_general_mub_n())
}

#[pyfunction]
#[pyo3(signature = (global_certificate_replayed=false))]
fn assess_d6_pinned_wall_py(
    py: Python<'_>,
    global_certificate_replayed: bool,
) -> PyResult<Py<PyAny>> {
    to_py_dict(py, &assess_d6_pinned_wall(global_certificate_replayed))
}

#[pyfunction]
#[pyo3(signature = (upper_bound_replayed=false))]
fn extension_verdict_full_mub6_py(
    py: Python<'_>,
    upper_bound_replayed: bool,
) -> PyResult<Py<PyAny>> {
    to_py_dict(py, &attempt_full_mub6_from_pinned_t0(upper_bound_replayed))
}

#[pyfunction]
fn extension_verdict_mub10_py(py: Python<'_>) -> PyResult<Py<PyAny>> {
    to_py_dict(py, &attempt_mub10())
}

#[pyfunction]
fn extension_verdict_general_mub_n_py(py: Python<'_>) -> PyResult<Py<PyAny>> {
    to_py_dict(py, &attempt_general_mub_n())
}

#[pyfunction]
fn d10_wall_status_py(py: Python<'_>) -> PyResult<Py<PyAny>> {
    to_py_dict(py, &current_d10_wall_status())
}

/// Exact runtime adapter: JSON request string → receipt dict.
///
/// Example request:
/// `{"evidence":{"kind":"fixed_t0","cover_discharged":false}}`
#[pyfunction]
fn evaluate_mub6_request_py(py: Python<'_>, request_json: &str) -> PyResult<Py<PyAny>> {
    match evaluate_mub6_json(request_json.as_bytes()) {
        Ok(eval) => {
            let receipt = Mub6PyReceipt {
                terminal: format!("{:?}", eval.terminal()),
                authority_effect: if eval.authority_effect().is_none() {
                    "None".to_string()
                } else {
                    format!("{:?}", eval.authority_effect())
                },
                cover_discharged: eval.cover_discharged(),
                tuple_hash: eval.tuple_hash().to_string(),
                replay_hash: eval.replay_hash().to_string(),
            };
            to_py_dict(py, &receipt)
        }
        Err(error) => {
            #[derive(Serialize)]
            struct ErrReceipt {
                terminal: String,
                authority_effect: &'static str,
                error: String,
            }
            to_py_dict(
                py,
                &ErrReceipt {
                    terminal: format!("{:?}", error.terminal()),
                    authority_effect: "None",
                    error: error.to_string(),
                },
            )
        }
    }
}

/// Root Python extension module (`import omega_mub`).
#[pymodule]
fn omega_mub(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(authority_effect, module)?)?;
    module.add_function(wrap_pyfunction!(package_info, module)?)?;
    module.add_function(wrap_pyfunction!(assess_general_mub_n_py, module)?)?;
    module.add_function(wrap_pyfunction!(assess_d6_pinned_wall_py, module)?)?;
    module.add_function(wrap_pyfunction!(extension_verdict_full_mub6_py, module)?)?;
    module.add_function(wrap_pyfunction!(extension_verdict_mub10_py, module)?)?;
    module.add_function(wrap_pyfunction!(
        extension_verdict_general_mub_n_py,
        module
    )?)?;
    module.add_function(wrap_pyfunction!(d10_wall_status_py, module)?)?;
    module.add_function(wrap_pyfunction!(evaluate_mub6_request_py, module)?)?;

    // Friendly aliases matching notebook docs (no `_py` suffix).
    module.add(
        "assess_general_mub_n",
        module.getattr("assess_general_mub_n_py")?,
    )?;
    module.add(
        "assess_d6_pinned_wall",
        module.getattr("assess_d6_pinned_wall_py")?,
    )?;
    module.add(
        "extension_verdict_full_mub6",
        module.getattr("extension_verdict_full_mub6_py")?,
    )?;
    module.add(
        "extension_verdict_mub10",
        module.getattr("extension_verdict_mub10_py")?,
    )?;
    module.add(
        "extension_verdict_general_mub_n",
        module.getattr("extension_verdict_general_mub_n_py")?,
    )?;
    module.add("d10_wall_status", module.getattr("d10_wall_status_py")?)?;
    module.add(
        "evaluate_mub6_request",
        module.getattr("evaluate_mub6_request_py")?,
    )?;

    Ok(())
}
