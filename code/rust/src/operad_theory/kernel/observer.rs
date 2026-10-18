
use serde_json::{json, Value};

use super::canonical::{canonical_id, require_identifier, sorted_unique};
use super::model::ModelError;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObserverDeclaration {
    pub regime: String,
    pub comparison_relation: String,
    pub allowed_lifts_and_gauges: Vec<String>,
    pub defect_definition: String,
    pub terminal_rule: String,
}

impl ObserverDeclaration {
    pub fn new(
        regime: &str,
        comparison_relation: &str,
        allowed_lifts_and_gauges: &[String],
        defect_definition: &str,
        terminal_rule: &str,
    ) -> Result<Self, ModelError> {
        Ok(Self {
            regime: require_identifier(regime, "regime")?,
            comparison_relation: require_identifier(comparison_relation, "comparison_relation")?,
            allowed_lifts_and_gauges: sorted_unique(
                allowed_lifts_and_gauges,
                "allowed_lifts_and_gauges",
            )?,
            defect_definition: require_identifier(defect_definition, "defect_definition")?,
            terminal_rule: require_identifier(terminal_rule, "terminal_rule")?,
        })
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "regime": self.regime,
            "comparison_relation": self.comparison_relation,
            "allowed_lifts_and_gauges": self.allowed_lifts_and_gauges,
            "defect_definition": self.defect_definition,
            "terminal_rule": self.terminal_rule,
        })
    }

    pub fn observer_id(&self) -> Result<String, ModelError> {
        Ok(canonical_id("omega.observer.v1", &self.to_canonical())?)
    }

    pub fn same_observer_as(&self, other: &ObserverDeclaration) -> Result<bool, ModelError> {
        Ok(self.observer_id()? == other.observer_id()?)
    }

    pub fn authority_effect(&self) -> &'static str {
        "None"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn lifts(values: &[&str]) -> Vec<String> {
        values.iter().map(|value| (*value).to_owned()).collect()
    }

    fn observer() -> ObserverDeclaration {
        ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &lifts(&["vertex-rephasing", "coefficient-extension"]),
            "l1-residual-mass",
            "strict-descent",
        )
        .expect("observer must build")
    }

    #[test]
    fn an_observer_id_is_a_domain_separated_digest() {
        let id = observer().observer_id().unwrap();
        assert!(id.starts_with("sha256:"));
        assert_eq!(id.len(), "sha256:".len() + 64);
    }

    #[test]
    fn the_same_rule_card_yields_the_same_id() {
        assert_eq!(observer().observer_id().unwrap(), observer().observer_id().unwrap());
        assert!(observer().same_observer_as(&observer()).unwrap());
    }

    #[test]
    fn listing_the_same_lifts_in_another_order_is_the_same_observer() {
        let reordered = ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &lifts(&["coefficient-extension", "vertex-rephasing"]),
            "l1-residual-mass",
            "strict-descent",
        )
        .unwrap();
        assert!(observer().same_observer_as(&reordered).unwrap());
    }

    #[test]
    fn changing_what_counts_as_a_defect_changes_the_observer() {
        let strongest = ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &lifts(&["vertex-rephasing", "coefficient-extension"]),
            "gamma2-curvature-mass",
            "strict-descent",
        )
        .unwrap();
        assert!(!observer().same_observer_as(&strongest).unwrap());
    }

    #[test]
    fn every_component_participates_in_the_identity() {
        let base = observer().observer_id().unwrap();
        let variants = [
            ObserverDeclaration::new(
                "rational-l1.v1",
                "exact-equality",
                &lifts(&["vertex-rephasing", "coefficient-extension"]),
                "l1-residual-mass",
                "strict-descent",
            ),
            ObserverDeclaration::new(
                "finite-f2-gauge.v1",
                "quotient-equality",
                &lifts(&["vertex-rephasing", "coefficient-extension"]),
                "l1-residual-mass",
                "strict-descent",
            ),
            ObserverDeclaration::new(
                "finite-f2-gauge.v1",
                "exact-equality",
                &lifts(&["vertex-rephasing"]),
                "l1-residual-mass",
                "strict-descent",
            ),
            ObserverDeclaration::new(
                "finite-f2-gauge.v1",
                "exact-equality",
                &lifts(&["vertex-rephasing", "coefficient-extension"]),
                "l1-residual-mass",
                "bounded-with-open-frontier",
            ),
        ];
        for variant in variants {
            assert_ne!(base, variant.unwrap().observer_id().unwrap());
        }
    }

    #[test]
    fn adding_a_permitted_lift_changes_the_observer() {
        let permissive = ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &lifts(&["vertex-rephasing", "coefficient-extension", "carrier-refinement"]),
            "l1-residual-mass",
            "strict-descent",
        )
        .unwrap();
        assert!(!observer().same_observer_as(&permissive).unwrap());
    }

    #[test]
    fn duplicate_lifts_are_refused_rather_than_silently_merged() {
        let duplicated = ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &lifts(&["vertex-rephasing", "vertex-rephasing"]),
            "l1-residual-mass",
            "strict-descent",
        );
        assert!(duplicated.is_err());
    }

    #[test]
    fn prose_is_refused_because_prose_does_not_compare() {
        assert!(ObserverDeclaration::new(
            "the finite F2 gauge regime",
            "exact-equality",
            &lifts(&["vertex-rephasing"]),
            "l1-residual-mass",
            "strict-descent",
        )
        .is_err());
    }

    #[test]
    fn an_incomplete_observer_is_refused() {
        assert!(ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &lifts(&["vertex-rephasing"]),
            "l1-residual-mass",
            "",
        )
        .is_err());
    }

    #[test]
    fn an_observer_with_no_permitted_lifts_is_admissible() {
        let rigid = ObserverDeclaration::new(
            "finite-f2-gauge.v1",
            "exact-equality",
            &[],
            "l1-residual-mass",
            "strict-descent",
        )
        .expect("an observer permitting no repairs is still an observer");
        assert!(!rigid.same_observer_as(&observer()).unwrap());
    }

    #[test]
    fn naming_the_rule_card_grants_nothing() {
        assert_eq!(observer().authority_effect(), "None");
    }

    #[test]
    fn the_domain_separates_observers_from_other_records() {
        let payload = observer().to_canonical();
        let as_observer = canonical_id("omega.observer.v1", &payload).unwrap();
        let as_something_else = canonical_id("omega.oewas.colour.v1", &payload).unwrap();
        assert_ne!(as_observer, as_something_else);
    }
}
