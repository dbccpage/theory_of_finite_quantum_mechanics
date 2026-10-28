
use num_rational::BigRational;
use serde_json::Value;
use std::str::FromStr;

pub const SCHEMA: &str = "omega_mub.fixture_values.v1";

pub const KINDS: [&str; 3] = ["literal", "assumed_constant", "fixed_verdict"];

pub const TYPES: [&str; 6] = ["rational", "float", "bool", "string", "integer", "count"];

pub struct FixtureSet {
    name: &'static str,
    values: serde_json::Map<String, Value>,
}

impl FixtureSet {
    pub fn parse(name: &'static str, json: &'static str) -> Self {
        let doc: Value = serde_json::from_str(json)
            .unwrap_or_else(|e| panic!("fixture file {name} is not valid JSON: {e}"));
        if let Err(defect) = check_document(&doc) {
            panic!("fixture file {name}: {defect}");
        }
        let values = doc["values"].as_object().cloned().unwrap_or_default();
        FixtureSet { name, values }
    }

    fn value(&self, id: &str) -> &Value {
        self.values
            .get(id)
            .map(|entry| &entry["value"])
            .unwrap_or_else(|| panic!("fixture {} has no value {id}", self.name))
    }

    pub fn rational(&self, id: &str) -> BigRational {
        let text = self
            .value(id)
            .as_str()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a rational string", self.name));
        BigRational::from_str(text)
            .unwrap_or_else(|e| panic!("fixture {}.{id} = {text:?}: {e}", self.name))
    }

    pub fn float(&self, id: &str) -> f64 {
        self.value(id)
            .as_f64()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a number", self.name))
    }

    pub fn flag(&self, id: &str) -> bool {
        self.value(id)
            .as_bool()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a boolean", self.name))
    }

    pub fn text(&self, id: &str) -> String {
        self.value(id)
            .as_str()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a string", self.name))
            .to_string()
    }

    pub fn integer(&self, id: &str) -> i64 {
        self.value(id)
            .as_i64()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not an integer", self.name))
    }

    pub fn count(&self, id: &str) -> usize {
        self.value(id)
            .as_u64()
            .and_then(|n| usize::try_from(n).ok())
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a count", self.name))
    }
}

fn is_blank_str(v: &Value) -> bool {
    v.as_str().map_or(true, |r| r.trim().is_empty())
}

fn check_fixture_entry(id: &str, entry: &Value) -> Result<(), String> {
    if entry.get("value").is_none() {
        return Err(format!("{id}: no value"));
    }
    let kind = entry["kind"].as_str().unwrap_or_default();
    if !KINDS.contains(&kind) {
        return Err(format!("{id}: kind {kind:?} is not one of {KINDS:?}"));
    }
    let ty = entry["type"].as_str().unwrap_or_default();
    if !TYPES.contains(&ty) {
        return Err(format!("{id}: type {ty:?} is not one of {TYPES:?}"));
    }
    if is_blank_str(&entry["reason"]) {
        return Err(format!("{id}: no reason"));
    }
    if is_blank_str(&entry["used_at"]) {
        return Err(format!("{id}: no used_at"));
    }
    Ok(())
}

pub fn check_document(doc: &Value) -> Result<(), String> {
    if doc["schema"] != SCHEMA {
        return Err(format!("schema is {}, expected {SCHEMA}", doc["schema"]));
    }
    if doc["authority_effect"] != "None" {
        return Err("authority_effect must be \"None\"".to_string());
    }
    if doc["module"].as_str().map_or(true, str::is_empty) {
        return Err("module is missing".to_string());
    }
    let values = doc["values"].as_object().ok_or("values is not an object")?;
    if values.is_empty() {
        return Err("values is empty".to_string());
    }
    for (id, entry) in values {
        check_fixture_entry(id, entry)?;
    }
    Ok(())
}

#[macro_export]
macro_rules! fixture_set {
    ($func:ident, $name:literal) => {
        fn $func() -> &'static $crate::native::census::mub6_fixtures::FixtureSet {
            static SET: std::sync::OnceLock<$crate::native::census::mub6_fixtures::FixtureSet> =
                std::sync::OnceLock::new();
            SET.get_or_init(|| {
                $crate::native::census::mub6_fixtures::FixtureSet::parse(
                    $name,
                    include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/fixtures/", $name, ".json")),
                )
            })
        }
    };
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;

    fn fixture_files() -> Vec<(String, Value)> {
        let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("fixtures");
        let mut files: Vec<(String, Value)> = std::fs::read_dir(&dir)
            .expect("fixtures directory")
            .filter_map(|e| e.ok().map(|e| e.path()))
            .filter(|p| p.extension().is_some_and(|x| x == "json"))
            .map(|p| {
                let stem = p.file_stem().unwrap().to_string_lossy().to_string();
                let doc = serde_json::from_slice(&std::fs::read(&p).unwrap())
                    .unwrap_or_else(|e| panic!("{stem}: {e}"));
                (stem, doc)
            })
            .collect();
        files.sort_by(|a, b| a.0.cmp(&b.0));
        files
    }

    #[test]
    fn every_fixture_file_is_well_formed() {
        let files = fixture_files();
        assert!(!files.is_empty());
        for (stem, doc) in &files {
            check_document(doc).unwrap_or_else(|d| panic!("{stem}: {d}"));
            assert_eq!(doc["module"], stem.as_str(), "module field matches the file stem");
            for (id, entry) in doc["values"].as_object().unwrap() {
                if let Some(text) = entry["value"].as_str() {
                    if entry["type"] == "rational" {
                        BigRational::from_str(text).unwrap_or_else(|e| panic!("{stem}.{id}: {e}"));
                    }
                }
            }
        }
    }

    #[test]
    fn every_fixture_value_is_read_where_it_says() {
        let root = Path::new(env!("CARGO_MANIFEST_DIR"));
        for (stem, doc) in fixture_files() {
            for (id, entry) in doc["values"].as_object().unwrap() {
                let used_at = entry["used_at"].as_str().unwrap();
                let source = std::fs::read_to_string(root.join(used_at))
                    .unwrap_or_else(|e| panic!("{stem}.{id}: used_at {used_at}: {e}"));
                assert!(
                    source.contains(&format!("\"{stem}\"")),
                    "{stem}.{id}: {used_at} does not load fixture set {stem}"
                );
                assert!(
                    source.contains(&format!("\"{id}\"")),
                    "{stem}.{id}: {used_at} does not read this value"
                );
            }
        }
    }

    #[test]
    fn check_rejects_missing_reason_kind_or_authority() {
        let good = serde_json::json!({
            "schema": SCHEMA, "authority_effect": "None", "module": "m",
            "values": {"x": {"value": "1/2", "type": "rational", "kind": "literal", "reason": "r", "used_at": "f.rs"}}
        });
        assert!(check_document(&good).is_ok());
        let mut no_reason = good.clone();
        no_reason["values"]["x"]["reason"] = Value::from("  ");
        assert!(check_document(&no_reason).is_err());
        let mut bad_kind = good.clone();
        bad_kind["values"]["x"]["kind"] = Value::from("computed");
        assert!(check_document(&bad_kind).is_err());
        let mut authority = good.clone();
        authority["authority_effect"] = Value::from("Granted");
        assert!(check_document(&authority).is_err());
        let mut no_site = good;
        no_site["values"]["x"]["used_at"] = Value::Null;
        assert!(check_document(&no_site).is_err());
    }

    #[test]
    #[should_panic(expected = "has no value")]
    fn reading_an_undeclared_value_stops() {
        let set = FixtureSet::parse(
            "m",
            r#"{"schema":"omega_mub.fixture_values.v1","authority_effect":"None","module":"m",
                "values":{"x":{"value":true,"type":"bool","kind":"fixed_verdict","reason":"r","used_at":"f.rs"}}}"#,
        );
        assert!(set.flag("x"));
        set.flag("y");
    }
}
