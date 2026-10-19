// Quadratic prefix oracle, independent of the production BTreeSet admission.
#[cfg(test)]
mod finite_literal_set_oracle {
    use super::*;

    fn expected(raw: &FiniteSet) -> Result<(), FiniteSetError> {
        if raw.label.chars().all(char::is_whitespace) {
            return Err(FiniteSetError::EmptyLabel);
        }
        for (index, tag) in raw.elements.iter().enumerate() {
            if tag.chars().all(char::is_whitespace) {
                return Err(FiniteSetError::EmptyElement { index });
            }
            if raw.elements[..index].contains(tag) {
                return Err(FiniteSetError::DuplicateElement { index });
            }
        }
        match raw.declared_cardinality {
            Some(declared) if declared != raw.elements.len() => {
                Err(FiniteSetError::CardinalityMismatch { declared, actual: raw.elements.len() })
            }
            _ => Ok(()),
        }
    }

    #[test]
    fn all_short_tag_words_match_independent_prefix_and_wire_admission() {
        let alphabet = ["", " ", "x", "y", " x ", "\u{2003}", "\0", "\u{e9}", "e\u{301}"];
        let labels = ["", " \u{2003}", "\0", " valid "];
        let mut checked = 0;
        for length in 0..=3u32 {
            for code in 0..9usize.pow(length) {
                let mut digits = code;
                let elements: Vec<String> = (0..length).map(|_| {
                    let tag = alphabet[digits % 9].to_owned(); digits /= 9; tag
                }).collect();
                for label in labels {
                    for declared in [None, Some(0), Some(elements.len()), Some(elements.len()+1), Some(usize::MAX)] {
                        let raw = FiniteSet { label:label.into(), elements:elements.clone(),
                            declared_cardinality:declared, notes:vec!["opaque\0note".into()] };
                        let before = raw.clone();
                        assert_eq!(raw.cardinality(),raw.elements.len());
                        let wanted = expected(&raw);
                        assert_eq!(raw.validate_shell(),wanted);
                        assert_eq!(raw,before,"validation borrows, never repairs raw data");
                        let result = ValidatedFiniteSet::try_from(raw.clone());
                        assert_eq!(result.as_ref().err(),wanted.as_ref().err());
                        if let Ok(admitted) = result {
                            assert_eq!(admitted.declared(),&raw);
                            assert_eq!(admitted.label(),raw.label);
                            assert_eq!(admitted.elements(),raw.elements);
                            assert_eq!(admitted.cardinality(),raw.elements.len());
                            for tag in alphabet {
                                assert_eq!(admitted.contains(tag),raw.elements.contains(&tag.to_owned()));
                            }
                            let detached: FiniteSet = admitted.clone().into();
                            assert_eq!(detached,raw);
                        }
                        let wire = serde_json::to_value(&raw).unwrap();
                        let decoded: FiniteSet = serde_json::from_value(wire.clone()).unwrap();
                        assert_eq!(decoded,raw,"raw wire data remains a candidate");
                        let admitted: Result<ValidatedFiniteSet,_> = serde_json::from_value(wire);
                        assert_eq!(admitted.is_ok(),wanted.is_ok(),"wire cannot bypass admission");
                        if let Ok(admitted) = admitted { assert_eq!(admitted.declared(),&raw); }
                        checked += 1;
                    }
                }
            }
        }
        assert_eq!(checked,16400);
    }

    #[test]
    fn constructors_ownership_and_literal_identity_are_preserved() {
        let raw = FiniteSet::new("empty");
        assert_eq!(raw.declared_cardinality,Some(0)); assert!(raw.elements.is_empty());
        let elements = vec!["x".into()," x ".into(),"\u{e9}".into(),"e\u{301}".into()];
        let mut raw = FiniteSet::with_elements("set\0",elements.clone());
        assert_eq!(raw.declared_cardinality,Some(4));
        let admitted = ValidatedFiniteSet::try_from(raw.clone()).unwrap();
        raw.elements.clear(); raw.label.clear(); raw.declared_cardinality=Some(0);
        assert_eq!(admitted.label(),"set\0"); assert_eq!(admitted.elements(),elements);
        assert_eq!(admitted.cardinality(),4);
        assert!(!admitted.contains("absent"));
        assert!(admitted.contains("x")); assert!(admitted.contains(" x "));
    }

    #[test]
    fn exact_error_payloads_display_and_formatter_refusal() {
        use std::fmt::Write as _;
        struct Refuse;
        impl std::fmt::Write for Refuse {
            fn write_str(&mut self, _: &str) -> std::fmt::Result { Err(std::fmt::Error) }
        }
        for (error, text) in [
            (FiniteSetError::EmptyLabel,"empty label"),
            (FiniteSetError::EmptyElement {index:7},"empty element tag at index 7"),
            (FiniteSetError::DuplicateElement {index:9},"duplicate element tag at index 9"),
            (FiniteSetError::CardinalityMismatch {declared:5,actual:3},"declared_cardinality 5 != elements.len() 3"),
        ] {
            assert_eq!(error.to_string(),text);
            assert!(write!(&mut Refuse,"{error}").is_err());
            let _: &dyn std::error::Error = &error;
        }
    }
}
