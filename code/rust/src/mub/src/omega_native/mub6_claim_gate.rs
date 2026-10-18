
use crate::omega_native::exact::mub6_cover::EnclosedTriple;
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_interval_cover::VectorBox;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StatedRegionSeal {
    pub firewall: &'static str,
    pub authority_effect: &'static str,
    pub stated_region_certificate: bool,
    pub mub6_equals_3: bool,
    pub mub6_at_most_3: bool,
    pub global_solution: bool,
    pub verified_certificate: bool,
}

pub fn certificate_from_exact_only<T>(exact: Option<T>, _float_estimate: f64) -> Option<T> {
    exact
}

pub fn artifact_tries_to_mint_global(artifact_json: &str) -> bool {
    let stripped = artifact_json.replace(FIREWALL, "");
    if stripped.contains("MUB(6)=3")
        || stripped.contains("MUB(6)<=3")
        || stripped.contains("MUB(6) = 3")
        || stripped.contains("MUB(6) <= 3")
    {
        return true;
    }
    let Ok(value) = serde_json::from_str::<serde_json::Value>(artifact_json) else {
        return !artifact_json.trim().is_empty();
    };
    flag_is_true(&value, "global_solution")
        || flag_is_true(&value, "mub6_equals_3")
        || flag_is_true(&value, "mub6_at_most_3")
        || flag_is_true(&value, "solved")
        || flag_is_true(&value, "verified_certificate")
}

fn flag_is_true(value: &serde_json::Value, key: &str) -> bool {
    match value {
        serde_json::Value::Object(map) => {
            if matches!(map.get(key), Some(serde_json::Value::Bool(true))) {
                return true;
            }
            map.values().any(|child| flag_is_true(child, key))
        }
        serde_json::Value::Array(items) => items.iter().any(|child| flag_is_true(child, key)),
        _ => false,
    }
}

pub fn seal_vbox_certificate(
    exact: &EnclosedTriple,
    vbox: &VectorBox,
    artifact_json: &str,
    float_estimate: f64,
    planted_global_solution: bool,
) -> StatedRegionSeal {
    let exact_holds = exact.certify(vbox).is_some();
    let _hostile = (
        artifact_tries_to_mint_global(artifact_json),
        float_estimate,
        planted_global_solution,
    );
    StatedRegionSeal {
        firewall: FIREWALL,
        authority_effect: AUTHORITY_EFFECT,
        stated_region_certificate: exact_holds,
        mub6_equals_3: false,
        mub6_at_most_3: false,
        global_solution: false,
        verified_certificate: exact_holds,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::mub6_interval_cover::VectorBox;
    use omega_kernel::interval::Interval;
    use omega_number_theory::rational::ri;

    fn wide_box() -> VectorBox {
        std::array::from_fn(|_| Interval::new(ri(0), ri(1)))
    }

    #[test]
    fn a_huge_float_cannot_invent_an_exact_certificate() {
        assert!(certificate_from_exact_only(None::<u8>, 1.0e9).is_none());
        assert_eq!(certificate_from_exact_only(Some(7u8), -1.0e9), Some(7));
    }

    #[test]
    fn planted_flag_artifact_and_float_cannot_mint_a_global_claim() {
        let exact = EnclosedTriple::standard();
        let vbox = wide_box();
        let artifact = r#"{"global_solution":true,"mub6_equals_3":true,"solved":true,"verified_certificate":true,"claim":"MUB(6)=3"}"#;
        let hostile = seal_vbox_certificate(&exact, &vbox, artifact, 1.0e9, true);
        let quiet = seal_vbox_certificate(&exact, &vbox, "{}", -1.0e9, false);
        assert_eq!(hostile, quiet);
        assert_eq!(hostile.firewall, FIREWALL);
        assert_eq!(hostile.authority_effect, AUTHORITY_EFFECT);
        assert!(!hostile.mub6_equals_3);
        assert!(!hostile.mub6_at_most_3);
        assert!(!hostile.global_solution);
        assert_eq!(
            hostile.verified_certificate,
            exact.certify(&vbox).is_some()
        );
        assert!(artifact_tries_to_mint_global(artifact));
        assert!(!artifact_tries_to_mint_global(&format!(
            "{{\"firewall\":\"{FIREWALL}\"}}"
        )));
    }
}
