//! Thin PyO3 bridge exposing the Rust operad kernel to Python.
//!
//! AuthorityEffect: None.

#[cfg(feature = "python")]
use pyo3::exceptions::{PyRuntimeError, PyValueError};
#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use serde::Serialize;

#[cfg(feature = "python")]
use crate::foundation::colour::OperadColour;
#[cfg(feature = "python")]
use crate::foundation::operation::OperationId;
#[cfg(feature = "python")]
use crate::foundation::planar_tree::PlanarTree;

#[cfg(feature = "python")]
#[pyclass(name = "OperadColour")]
#[derive(Clone)]
pub struct PyOperadColour {
    pub inner: OperadColour,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyOperadColour {
    #[new]
    pub fn new(name: String) -> PyResult<Self> {
        OperadColour::new(name)
            .map(|inner| Self { inner })
            .map_err(|e| PyValueError::new_err(e))
    }

    #[getter]
    pub fn name(&self) -> &str {
        self.inner.as_str()
    }

    pub fn __repr__(&self) -> String {
        format!("OperadColour('{}')", self.inner.as_str())
    }

    pub fn __str__(&self) -> String {
        self.inner.to_string()
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "OperationId")]
#[derive(Clone)]
pub struct PyOperationId {
    pub inner: OperationId,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyOperationId {
    #[new]
    pub fn new(name: String) -> PyResult<Self> {
        OperationId::new(name)
            .map(|inner| Self { inner })
            .map_err(|e| PyValueError::new_err(e))
    }

    #[staticmethod]
    pub fn identity_for(colour: &PyOperadColour) -> Self {
        Self {
            inner: OperationId::identity_for(&colour.inner),
        }
    }

    #[getter]
    pub fn name(&self) -> &str {
        self.inner.as_str()
    }

    pub fn __repr__(&self) -> String {
        format!("OperationId('{}')", self.inner.as_str())
    }
}

#[cfg(feature = "python")]
#[pyclass(name = "PlanarTree")]
#[derive(Clone)]
pub struct PyPlanarTree {
    pub inner: PlanarTree,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyPlanarTree {
    #[getter]
    pub fn term_hash(&self) -> String {
        self.inner.term_hash()
    }

    #[getter]
    pub fn arity(&self) -> usize {
        self.inner.arity()
    }
}

#[cfg(feature = "python")]
#[pyfunction]
pub fn authority_effect() -> &'static str {
    "None"
}

#[cfg(feature = "python")]
#[pyfunction]
pub fn package_info(py: Python<'_>) -> PyResult<Py<PyAny>> {
    #[derive(Serialize)]
    struct Info {
        name: &'static str,
        version: &'static str,
        authority_effect: &'static str,
        pyo3_accelerated: bool,
    }
    let info = Info {
        name: "omega_operad_theory",
        version: "0.1.0",
        authority_effect: "None",
        pyo3_accelerated: true,
    };
    let encoded = serde_json::to_string(&info)
        .map_err(|e| PyRuntimeError::new_err(format!("serialization error: {e}")))?;
    py.import("json")?
        .call_method1("loads", (encoded,))
        .map(|v| v.unbind())
}

#[cfg(feature = "python")]
#[pymodule]
pub fn omega_operad_theory_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyOperadColour>()?;
    m.add_class::<PyOperationId>()?;
    m.add_class::<PyPlanarTree>()?;
    m.add_function(wrap_pyfunction!(authority_effect, m)?)?;
    m.add_function(wrap_pyfunction!(package_info, m)?)?;
    Ok(())
}
