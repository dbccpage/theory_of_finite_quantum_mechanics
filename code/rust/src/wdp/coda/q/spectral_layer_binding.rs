//! Cross-layer binding note: finite Hermitian *operator* spectral layer ↔ Q membrane.
//!
//! **Does not** re-implement or rewrite [`crate::coda::spectral_membrane`].
//! **Does not** depend on `omega_quantum_physics` (dependency firewall / layering).
//!
//! | Surface | Crate path | Role |
//! |---|---|---|
//! | Exact spectral *certificate* membrane | `crate::coda::q::spectral_membrane` | Binds a finite refinement tower + convergence certificate into continuum-debt / Q admission terminals. Evidence ceiling ShapeOnly; authority None. |
//! | Finite Hermitian *operator* spectral face | `omega_quantum_physics::hermitian_spectral` | Finite-`n` algebraic spectrum with exact root isolation and multiplicities, rational eigenspace decomposition, and explicit `ScalarCarrier` hypotheses. AuthorityEffect None; no continuum claim. |
//!
//! Binding contract (documentation only):
//! 1. Neither surface mints authority above `AuthorityEffect::None` / `AuthorityEffectLevel::None`.
//! 2. Neither surface constructs a continuum object; residual / debt routes remain explicit.
//! 3. Operator eigen-decomposition (hermitian_spectral) is **not** a substitute for a
//!    `ConvergenceCertificate` at the membrane; membrane decisions stay certificate-driven.
//! 4. Float / demo carriers on the operator face are non-exact and cannot pay membrane certificates.
//!
//! `hermitian_spectral::algebraic_spectrum` computes the general finite spectrum.
//! A full projector decomposition in the original scalar field remains a
//! separate representability question when the eigenvalues require an extension.

/// Stable path string for the operator spectral face (for logs / residual ledgers).
pub const OPERATOR_SPECTRAL_LAYER_PATH: &str = "omega_quantum_physics::hermitian_spectral";

/// Stable path string for the Q spectral certificate membrane.
pub const CERTIFICATE_SPECTRAL_MEMBRANE_PATH: &str = "crate::coda::q::spectral_membrane";

/// Binding fence: both layers declare AuthorityEffect None and no continuum object.
pub const SPECTRAL_LAYER_BINDING_FENCE: &str = "AuthorityEffect None on both faces; \
    hermitian_spectral is finite operator spectral; spectral_membrane is certificate admission; \
    neither mints continuum objects; Float64Demo is non-exact/experimental on the operator face.";

/// Returns the binding fence (never mints authority).
pub fn spectral_layer_binding_fence() -> &'static str {
    SPECTRAL_LAYER_BINDING_FENCE
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fence_declares_none_and_no_continuum() {
        let f = spectral_layer_binding_fence();
        assert!(f.contains("AuthorityEffect None"));
        assert!(f.contains("neither mints continuum"));
        assert!(OPERATOR_SPECTRAL_LAYER_PATH.contains("hermitian_spectral"));
        assert!(CERTIFICATE_SPECTRAL_MEMBRANE_PATH.contains("spectral_membrane"));
    }
}
