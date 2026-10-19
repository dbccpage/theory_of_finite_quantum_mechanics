"""Explicit parameter/tag schema challenges, never inferred from source guards.

The policy supplies required fields, independent cases and constructor checks.
Only mutation-site uniqueness is derived from the assessed source text.
"""
import json


def challenge(record):
    new_check = record.get("new_label_check",
        'assert_eq!(TYPE::new("label\\0\\u{03b1}").label,"label\\0\\u{03b1}");')
    cases = []
    required = record["required_fields"]
    for values, parameter_error in record["parameter_cases"]:
        for mask in range(1 << len(required)):
            candidate = dict(values)
            candidate.update({field: "" if mask & (1 << index) else values.get(field, field + ":\u03b1\0")
                              for index, field in enumerate(required)})
            missing = next((field for field in required if candidate[field] == ""), None)
            expected = "empty " + missing if missing else parameter_error
            cases.append([candidate, expected])
    # Labels are literal byte strings: no accidental trim or theorem admission.
    for label in [" ", "\u03b1\0", "unverified mathematical declaration"]:
        candidate = dict(record["parameter_cases"][0][0])
        candidate.update({field: candidate.get(field, label) for field in required})
        cases.append([candidate, record["parameter_cases"][0][1]])
    data = json.dumps(json.dumps(cases, ensure_ascii=True))
    return r'''
#[cfg(test)] mod parameter_challenge {
    use super::*;
    #[test] fn independent_schema_cases_and_first_error() {
        let cases: Vec<(serde_json::Value, Option<String>)> = serde_json::from_str(CASES).unwrap();
        for (patch, expected) in cases {
            let mut raw = serde_json::to_value(TYPE::default()).unwrap();
            for (key, value) in patch.as_object().unwrap() { raw[key] = value.clone(); }
            let subject: TYPE = serde_json::from_value(raw.clone()).unwrap();
            let before = subject.clone();
            match (expected, subject.validate_shell()) {
                (None, Ok(())) => (),
                (Some(wanted), Err(ArithmosError::InvalidShape(actual))) => assert_eq!(actual,wanted),
                (wanted, actual) => panic!("expected {wanted:?}, got {actual:?}; raw={raw}"),
            }
            assert_eq!(subject,before);
            let decoded: TYPE = serde_json::from_value(serde_json::to_value(&subject).unwrap()).unwrap();
            assert_eq!(decoded,subject,"serde remains raw metadata, including rejected candidates");
        }
    }
    #[test] fn constructors_preserve_distinct_supplied_parameters() {
NEW_LABEL_CHECK
CONSTRUCTORS
    }
}
'''.replace("CASES", data).replace("NEW_LABEL_CHECK",new_check).replace("TYPE",record["type"]).replace("CONSTRUCTORS",record["constructor_checks"])


def variants(record, source):
    rows = []
    recipes = []
    for field in record["required_fields"]:
        recipes.extend([
            (field + "-skip",f"if self.{field}.is_empty() {{","if false {"),
            (field + "-diagnostic",f'"empty {field}".into()','"wrong field diagnostic".into()'),
        ])
    recipes.extend(record["faults"])
    for name, needle, replacement in recipes:
        if source.count(needle) != 1:
            raise ValueError("Nonunique designated parameter fault: " + record["path"] + ":" + name)
        rows.append((name,source.replace(needle,replacement,1),needle,replacement))
    # Observe new() directly; replace only its first label binding.
    needle, replacement = record.get("new_label_binding", ["label: label.into()", "label: String::new()"])
    if needle not in source:
        raise ValueError("Missing raw new-label assignment")
    rows.append(("new-label",source.replace(needle,replacement,1),needle,replacement))
    return rows
