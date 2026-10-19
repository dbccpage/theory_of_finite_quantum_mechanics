"""Raw named-equation/flag inventory and checked metadata update controls."""

REGRESSION = '#[test] fn declared_max_level_is_refused_without_mutation_or_panic(){let mut c=Condensation::new("X","Y","s","r");c.coherence_level=usize::MAX;let before=c.clone();let result=std::panic::catch_unwind(std::panic::AssertUnwindSafe(||{let _=c.add_witness("next",true);}));assert!(result.is_ok(),"public raw max level must not overflow");assert_eq!(c,before);}'


def challenge(subject):
    return '\n#[cfg(test)] mod independent_condensation_tests {use super::*;\n'+REGRESSION+'\n}\n'
