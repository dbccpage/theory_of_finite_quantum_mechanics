
pub const OPERATOR_SPECTRAL_LAYER_PATH: &str = "engine_quantum_physics::hermitian_spectral";

pub const CERTIFICATE_SPECTRAL_MEMBRANE_PATH: &str = "crate::coda::q::spectral_membrane";

pub const SPECTRAL_LAYER_BINDING_FENCE: &str = "AuthorityEffect None on both faces; \
    hermitian_spectral is finite operator spectral; spectral_membrane is certificate admission; \
    neither mints continuum objects; Float64Demo is non-exact/experimental on the operator face.";

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
