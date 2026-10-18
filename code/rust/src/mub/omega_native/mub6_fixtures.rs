//! Fixture values: hard-coded inputs that omega_mub receipts use where no computation exists.
//!
//! Each file under `omega_mub/fixtures/` holds the literals, assumed constants and fixed
//! verdict flags of one module, each with its kind, the reason it is a fixture and the source file
//! that reads it. Code reads them through [`fixture_set!`] instead of embedding them, so every number
//! that stands in for a computation is listed outside the code. A value read from here is not
//! evidence for any MUB(6) statement. The files are embedded at compile time.
//!
//! AuthorityEffect: None.

use num_rational::BigRational;
use serde_json::Value;
use std::str::FromStr;

/// Schema every fixture file declares.
pub const SCHEMA: &str = "omega_mub.fixture_values.v1";

/// Kinds a fixture value may declare: a number written in place of a computation, a constant the
/// code assumes without derivation, or a verdict flag or status set without a check.
pub const KINDS: [&str; 3] = ["literal", "assumed_constant", "fixed_verdict"];

/// Value types a fixture may declare; each has one accessor on [`FixtureSet`].
pub const TYPES: [&str; 6] = ["rational", "float", "bool", "string", "integer", "count"];

/// One module's fixture values, parsed from its embedded JSON file.
pub struct FixtureSet {
    name: &'static str,
    values: serde_json::Map<String, Value>,
}

impl FixtureSet {
    /// Parses an embedded fixture file. The files are compile-time constants checked by the
    /// register test, so a malformed file stops the program instead of returning a value.
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

    /// A rational written as `"p/q"` or `"p"`.
    pub fn rational(&self, id: &str) -> BigRational {
        let text = self
            .value(id)
            .as_str()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a rational string", self.name));
        BigRational::from_str(text)
            .unwrap_or_else(|e| panic!("fixture {}.{id} = {text:?}: {e}", self.name))
    }

    /// A float, for code that already works in `f64`.
    pub fn float(&self, id: &str) -> f64 {
        self.value(id)
            .as_f64()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a number", self.name))
    }

    /// A boolean flag.
    pub fn flag(&self, id: &str) -> bool {
        self.value(id)
            .as_bool()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a boolean", self.name))
    }

    /// A string.
    pub fn text(&self, id: &str) -> String {
        self.value(id)
            .as_str()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a string", self.name))
            .to_string()
    }

    /// A signed integer.
    pub fn integer(&self, id: &str) -> i64 {
        self.value(id)
            .as_i64()
            .unwrap_or_else(|| panic!("fixture {}.{id} is not an integer", self.name))
    }

    /// An unsigned integer.
    pub fn count(&self, id: &str) -> usize {
        self.value(id)
            .as_u64()
            .and_then(|n| usize::try_from(n).ok())
            .unwrap_or_else(|| panic!("fixture {}.{id} is not a count", self.name))
    }
}

/// Checks the document shape: schema, authority, and for every value a type, a kind, a reason
/// and the `used_at` source file (relative to the crate) that reads it.
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
        if entry["reason"].as_str().map_or(true, |r| r.trim().is_empty()) {
            return Err(format!("{id}: no reason"));
        }
        if entry["used_at"].as_str().map_or(true, |r| r.trim().is_empty()) {
            return Err(format!("{id}: no used_at"));
        }
    }
    Ok(())
}

/// Declares `fn $func() -> &'static FixtureSet` reading `omega_mub/fixtures/$name.json`, embedded
/// at compile time and parsed once.
#[macro_export]
macro_rules! fixture_set {
    ($func:ident, $name:literal) => {
        fn $func() -> &'static $crate::omega_native::census::mub6_fixtures::FixtureSet {
            static SET: std::sync::OnceLock<$crate::omega_native::census::mub6_fixtures::FixtureSet> =
                std::sync::OnceLock::new();
            SET.get_or_init(|| {
                $crate::omega_native::census::mub6_fixtures::FixtureSet::parse(
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

    /// Each value names the source file that reads it; that file must load this fixture set and
    /// mention the value id, so a value no code reads cannot sit in a fixture file.
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
