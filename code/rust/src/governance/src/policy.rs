//! `governance/policy.json` and `governance/baseline.json`: the single source of
//! truth for the floor, the source populations ("build kinds"), the exclusions,
//! the companion naming rule, pinned boilerplate and the grandfather list.
//!
//! Cost: parsing is linear in the file; [`glob_match`] is O(P x S) (no backtracking);
//! [`Policy::spec_for`] tries each population's globs once.

use std::collections::BTreeMap;
use std::fmt;
use std::path::Path;

use serde_json::{Map, Value};

use super::score::{Floor, Grade, Level};

/// Repository-relative location of the policy file.
pub const POLICY_PATH: &str = "governance/policy.json";
/// Repository-relative location of the baseline file.
pub const BASELINE_PATH: &str = "governance/baseline.json";
/// Schema identifier of the policy file.
pub const POLICY_SCHEMA: &str = "tfqm.governance-policy.v1";
/// Schema identifier of the baseline file.
pub const BASELINE_SCHEMA: &str = "tfqm.governance-baseline.v1";
/// Environment variable that selects the build-time mode.
pub const MODE_ENV: &str = "TFQM_GOVERNANCE";

/// The language family of a governed source ("build kind").
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ArtifactKind {
    /// Rust source, built by cargo.
    Rust,
    /// Python source.
    Python,
    /// Lean 4 source, built by lake.
    Lean,
    /// SQL scripts.
    Sql,
    /// Any other declared population.
    Other,
}

impl ArtifactKind {
    /// Parse the `kind` key of a policy population.
    pub fn from_key(key: &str) -> Option<ArtifactKind> {
        match key {
            "rust" => Some(ArtifactKind::Rust),
            "python" => Some(ArtifactKind::Python),
            "lean" => Some(ArtifactKind::Lean),
            "sql" => Some(ArtifactKind::Sql),
            "other" => Some(ArtifactKind::Other),
            _ => None,
        }
    }

    /// The policy key of this kind.
    pub fn key(self) -> &'static str {
        match self {
            ArtifactKind::Rust => "rust",
            ArtifactKind::Python => "python",
            ArtifactKind::Lean => "lean",
            ArtifactKind::Sql => "sql",
            ArtifactKind::Other => "other",
        }
    }
}

/// Paths removed from every population.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Exclusions {
    /// A path is excluded when any of its `/`-separated components equals one of these.
    pub path_parts: Vec<String>,
    /// A path is excluded when it matches one of these globs.
    pub path_globs: Vec<String>,
}

impl Exclusions {
    /// True when the repository-relative posix path is excluded.
    pub fn excludes(&self, rel_path: &str) -> bool {
        rel_path.split('/').any(|part| self.path_parts.iter().any(|p| p == part))
            || self.path_globs.iter().any(|glob| glob_match(glob, rel_path))
    }
}

/// Per-language source selection: which globs form a population and what is excluded.
pub trait ArtifactKindSpec {
    /// The build kind of the population.
    fn kind(&self) -> ArtifactKind;
    /// The language label that score records must carry (for example `Lean 4`).
    fn language(&self) -> &str;
    /// Globs over repository-relative posix paths.
    fn source_globs(&self) -> &[String];
    /// Exclusions applied after the globs.
    fn exclusions(&self) -> &Exclusions;
    /// True when the path belongs to this population.
    fn admits(&self, rel_path: &str) -> bool {
        !self.exclusions().excludes(rel_path) && self.source_globs().iter().any(|glob| glob_match(glob, rel_path))
    }
}

/// One population declared in the policy file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PopulationSpec {
    kind: ArtifactKind,
    language: String,
    globs: Vec<String>,
    exclusions: Exclusions,
}

impl ArtifactKindSpec for PopulationSpec {
    fn kind(&self) -> ArtifactKind {
        self.kind
    }
    fn language(&self) -> &str {
        &self.language
    }
    fn source_globs(&self) -> &[String] {
        &self.globs
    }
    fn exclusions(&self) -> &Exclusions {
        &self.exclusions
    }
}

/// How companions are named and which schemas they carry.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CompanionRules {
    /// Companion file suffix, `.contract.score.yaml`.
    pub suffix: String,
    /// `schema_version` of the companion document.
    pub document_schema: String,
    /// `schema_version` of a current score record.
    pub score_schema: String,
    /// Source suffixes whose stems may collide in one directory.
    pub collision_suffixes: Vec<String>,
}

/// A byte-pinned boilerplate file that needs no companion of its own.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PinnedBoilerplate {
    /// Paths the pin applies to.
    pub glob: String,
    /// The only admitted SHA-256 of such a file.
    pub sha256: String,
    /// Repository-relative path of the canonical template.
    pub template: String,
    /// Why the file is exempt.
    pub reason: String,
}

/// A reviewed support artifact may use L1..L3, while still requiring D or better.
/// The exception applies only to one exact repository path and source digest.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SupportException {
    /// Exact source digest admitted by the review.
    pub sha256: String,
    /// One of build_registration, regression_test, or source_archive.
    pub category: String,
    /// User authorization and artifact-specific rationale.
    pub reason: String,
}

/// The parsed `governance/policy.json`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Policy {
    /// The acceptance floor.
    pub floor: Floor,
    /// Companion naming and schemas.
    pub companion: CompanionRules,
    /// Source populations, one per build kind.
    pub populations: Vec<PopulationSpec>,
    /// Global exclusions.
    pub exclusions: Exclusions,
    /// Boilerplate admitted by exact bytes.
    pub pinned_boilerplate: Vec<PinnedBoilerplate>,
    /// Environment variable that selects the build-time mode.
    pub mode_env: String,
    /// Exact-byte support exceptions; all companion integrity checks still apply.
    pub support_exceptions: BTreeMap<String, SupportException>,
}

impl Policy {
    /// Parse and validate the policy text.
    pub fn from_json(text: &str) -> Result<Policy, PolicyError> {
        let value: Value = serde_json::from_str(text).map_err(|e| PolicyError::Json(e.to_string()))?;
        let root = value.as_object().ok_or(PolicyError::Field { field: "$".into(), expected: "an object".into() })?;
        check_header(root)?;
        let exclusions = parse_exclusions(root)?;
        Ok(Policy {
            floor: parse_floor(root)?,
            companion: parse_companion(root)?,
            populations: parse_populations(root, &exclusions)?,
            pinned_boilerplate: parse_pins(root)?,
            mode_env: parse_mode_env(root)?,
            support_exceptions: parse_support_exceptions(root)?,
            exclusions,
        })
    }

    /// Read and parse a policy file.
    pub fn load(path: &Path) -> Result<Policy, PolicyError> {
        Policy::from_json(&read(path)?)
    }

    /// The population a repository-relative path belongs to, if any.
    pub fn spec_for(&self, rel_path: &str) -> Option<&PopulationSpec> {
        self.populations.iter().find(|spec| spec.admits(rel_path))
    }

    /// The pin that admits this path, if its glob matches.
    pub fn pinned_for(&self, rel_path: &str) -> Option<&PinnedBoilerplate> {
        self.pinned_boilerplate.iter().find(|pin| glob_match(&pin.glob, rel_path))
    }

    /// Use the support floor only for a reviewed path at its exact source bytes.
    pub fn floor_for(&self, path: &str, digest: &str) -> Floor {
        match self.support_exceptions.get(path) {
            Some(pin) if pin.sha256 == digest => Floor { min_level: Level::L1, min_grade: self.floor.min_grade.max(Grade::D) },
            _ => self.floor,
        }
    }

    /// The companion path of a source. A stem shared with a sibling source of another
    /// collision suffix (for example `m.py` and `m.rs`) is qualified by the full name.
    pub fn companion_path(&self, rel_path: &str, exists: impl Fn(&str) -> bool) -> String {
        let (dir, name) = rel_path.rsplit_once('/').map_or(("", rel_path), |(d, n)| (d, n));
        let (stem, ext) = name.rsplit_once('.').map_or((name, ""), |(s, e)| (s, e));
        let sibling = |suffix: &String| {
            let candidate = format!("{}{stem}{suffix}", prefix(dir));
            suffix.trim_start_matches('.') != ext && exists(&candidate)
        };
        let base = if self.companion.collision_suffixes.iter().any(sibling) { name } else { stem };
        format!("{}{base}{}", prefix(dir), self.companion.suffix)
    }
}

fn prefix(dir: &str) -> String {
    if dir.is_empty() {
        String::new()
    } else {
        format!("{dir}/")
    }
}

/// The schema id and the level and grade orders, which must equal this crate's enums.
fn check_header(root: &Map<String, Value>) -> Result<(), PolicyError> {
    expect_schema(root, POLICY_SCHEMA)?;
    check_order(root, "level_order", &Level::ALL.map(Level::as_str))?;
    check_order(root, "grade_order", &Grade::ALL.map(Grade::as_str))
}

fn parse_support_exceptions(root: &Map<String, Value>) -> Result<BTreeMap<String, SupportException>, PolicyError> {
    let Some(value) = root.get("support_exceptions") else { return Ok(BTreeMap::new()) };
    let entries = value.as_object().ok_or_else(|| field("support_exceptions", "an object"))?;
    entries.iter().map(|(path, value)| support_exception(path, value).map(|pin| (path.clone(), pin))).collect()
}

fn support_exception(path: &str, value: &Value) -> Result<SupportException, PolicyError> {
    if path.contains(['*', '?', ':', '\\']) || path.split('/').any(|p| p.is_empty() || p == "." || p == "..") {
        return Err(field("support_exceptions.path", "an exact relative POSIX path without wildcards"));
    }
    let item = value.as_object().ok_or_else(|| field("support_exceptions[]", "an object"))?;
    let sha256 = string(item, "sha256")?;
    let category = string(item, "category")?;
    let reason = string(item, "reason")?;
    if !is_sha256(sha256) || reason.trim().is_empty() {
        return Err(field("support_exceptions[]", "a valid source digest and nonempty review reason"));
    }
    if !matches!(category, "build_registration" | "regression_test" | "source_archive") {
        return Err(field("support_exceptions.category", "build_registration, regression_test or source_archive"));
    }
    Ok(SupportException { sha256: sha256.into(), category: category.into(), reason: reason.into() })
}

fn parse_floor(root: &Map<String, Value>) -> Result<Floor, PolicyError> {
    let floor = object(root, "floor")?;
    Ok(Floor {
        min_level: string(floor, "min_level")?.parse().map_err(|_| field("floor.min_level", "L1..L5"))?,
        min_grade: string(floor, "min_grade")?.parse().map_err(|_| field("floor.min_grade", "a grade"))?,
    })
}

fn parse_companion(root: &Map<String, Value>) -> Result<CompanionRules, PolicyError> {
    let companion = object(root, "companion")?;
    Ok(CompanionRules {
        suffix: string(companion, "suffix")?.to_owned(),
        document_schema: string(companion, "document_schema")?.to_owned(),
        score_schema: string(companion, "score_schema")?.to_owned(),
        collision_suffixes: strings(companion, "collision_suffixes")?,
    })
}

fn parse_exclusions(root: &Map<String, Value>) -> Result<Exclusions, PolicyError> {
    let exclusions = object(root, "exclusions")?;
    Ok(Exclusions { path_parts: strings(exclusions, "path_parts")?, path_globs: strings(exclusions, "path_globs")? })
}

fn parse_populations(root: &Map<String, Value>, exclusions: &Exclusions) -> Result<Vec<PopulationSpec>, PolicyError> {
    let populations = array(root, "populations")?.iter().map(|item| population(item, exclusions)).collect::<Result<Vec<_>, _>>()?;
    if populations.is_empty() {
        return Err(field("populations", "at least one population"));
    }
    Ok(populations)
}

fn parse_pins(root: &Map<String, Value>) -> Result<Vec<PinnedBoilerplate>, PolicyError> {
    array(root, "pinned_boilerplate")?.iter().map(pinned).collect()
}

fn parse_mode_env(root: &Map<String, Value>) -> Result<String, PolicyError> {
    let env = string(object(root, "enforcement")?, "env")?;
    if env == MODE_ENV {
        Ok(env.to_owned())
    } else {
        Err(field("enforcement.env", MODE_ENV))
    }
}

fn population(item: &Value, exclusions: &Exclusions) -> Result<PopulationSpec, PolicyError> {
    let item = item.as_object().ok_or_else(|| field("populations[]", "an object"))?;
    let key = string(item, "kind")?;
    let kind = ArtifactKind::from_key(key).ok_or_else(|| field("populations[].kind", "rust, python, lean, sql or other"))?;
    let globs = strings(item, "globs")?;
    if globs.is_empty() {
        return Err(field("populations[].globs", "at least one glob"));
    }
    Ok(PopulationSpec { kind, language: string(item, "language")?.to_owned(), globs, exclusions: exclusions.clone() })
}

fn pinned(item: &Value) -> Result<PinnedBoilerplate, PolicyError> {
    let item = item.as_object().ok_or_else(|| field("pinned_boilerplate[]", "an object"))?;
    let sha256 = string(item, "sha256")?;
    if !is_sha256(sha256) {
        return Err(field("pinned_boilerplate[].sha256", "64 lower-case hex digits"));
    }
    Ok(PinnedBoilerplate {
        glob: string(item, "glob")?.to_owned(),
        sha256: sha256.to_owned(),
        template: string(item, "template")?.to_owned(),
        reason: string(item, "reason")?.to_owned(),
    })
}

/// One grandfathered source: its bytes at baseline time and the deficit then.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BaselineEntry {
    /// SHA-256 of the source bytes when the entry was recorded.
    pub sha256: String,
    /// Rule code of the first violation at that time.
    pub deficit: String,
    /// Required justification for any entry added after the initial baseline.
    pub reason: Option<String>,
}

/// The grandfather list `governance/baseline.json`, keyed by repository-relative path.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Baseline {
    /// Entries in path order.
    pub entries: BTreeMap<String, BaselineEntry>,
}

impl Baseline {
    /// Parse and validate the baseline text.
    pub fn from_json(text: &str) -> Result<Baseline, PolicyError> {
        let value: Value = serde_json::from_str(text).map_err(|e| PolicyError::Json(e.to_string()))?;
        let root = value.as_object().ok_or_else(|| field("$", "an object"))?;
        expect_schema(root, BASELINE_SCHEMA)?;
        let entries = object(root, "entries")?
            .iter()
            .map(|(path, entry)| baseline_entry(path, entry).map(|e| (path.clone(), e)))
            .collect::<Result<BTreeMap<_, _>, _>>()?;
        Ok(Baseline { entries })
    }

    /// Read and parse a baseline file.
    pub fn load(path: &Path) -> Result<Baseline, PolicyError> {
        Baseline::from_json(&read(path)?)
    }

    /// True when the path is listed with exactly these bytes.
    pub fn grandfathers(&self, rel_path: &str, sha256: &str) -> bool {
        self.entries.get(rel_path).is_some_and(|entry| entry.sha256 == sha256)
    }

    /// Deterministic text: one entry per line, sorted by path, LF endings.
    pub fn to_json_text(&self) -> String {
        let mut by_deficit: BTreeMap<&str, usize> = BTreeMap::new();
        for entry in self.entries.values() {
            let slot = by_deficit.entry(entry.deficit.as_str()).or_insert(0);
            *slot = slot.saturating_add(1);
        }
        let summary: Map<String, Value> = by_deficit.into_iter().map(|(k, v)| (k.to_owned(), Value::from(v))).collect();
        let mut out = String::new();
        out.push_str("{\n");
        out.push_str(&format!("  \"schema_version\": {},\n", Value::from(BASELINE_SCHEMA)));
        out.push_str("  \"AuthorityEffect\": \"None\",\n");
        out.push_str(&format!("  \"policy\": {},\n", Value::from(POLICY_PATH)));
        out.push_str("  \"rule\": \"Grandfather list. An entry exempts one source only while its bytes keep this sha256. Entries may only be removed; governance-check baseline --write --allow-add --reason is the only way to add one, and CI rejects added entries without a reason.\",\n");
        out.push_str(&format!("  \"summary\": {{\"entries\": {}, \"by_deficit\": {}}},\n", self.entries.len(), Value::Object(summary)));
        let lines: Vec<String> = self.entries.iter().map(|(path, entry)| format!("    {}: {}", Value::from(path.as_str()), entry_json(entry))).collect();
        if lines.is_empty() {
            out.push_str("  \"entries\": {}\n}\n");
        } else {
            out.push_str(&format!("  \"entries\": {{\n{}\n  }}\n}}\n", lines.join(",\n")));
        }
        out
    }
}

fn baseline_entry(path: &str, entry: &Value) -> Result<BaselineEntry, PolicyError> {
    let entry = entry.as_object().ok_or_else(|| field("entries.*", "an object"))?;
    let sha256 = string(entry, "sha256")?;
    if !is_sha256(sha256) {
        return Err(PolicyError::Field { field: format!("entries.{path}.sha256"), expected: "64 lower-case hex digits".into() });
    }
    let reason = entry.get("reason").and_then(Value::as_str).map(str::to_owned);
    Ok(BaselineEntry { sha256: sha256.to_owned(), deficit: string(entry, "deficit")?.to_owned(), reason })
}

fn entry_json(entry: &BaselineEntry) -> Value {
    let mut fields = Map::new();
    fields.insert("sha256".into(), Value::from(entry.sha256.as_str()));
    fields.insert("deficit".into(), Value::from(entry.deficit.as_str()));
    if let Some(reason) = &entry.reason {
        fields.insert("reason".into(), Value::from(reason.as_str()));
    }
    Value::Object(fields)
}

/// A failure to read or validate a governance data file. Fields name the file or
/// key at fault and the underlying message or the expected shape.
#[allow(missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PolicyError {
    /// The file could not be read.
    Io { path: String, message: String },
    /// The text is not JSON.
    Json(String),
    /// A field is missing or has the wrong shape.
    Field { field: String, expected: String },
}

impl fmt::Display for PolicyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PolicyError::Io { path, message } => write!(f, "cannot read {path}: {message}"),
            PolicyError::Json(message) => write!(f, "invalid JSON: {message}"),
            PolicyError::Field { field, expected } => write!(f, "field {field}: expected {expected}"),
        }
    }
}

impl std::error::Error for PolicyError {}

fn field(name: &str, expected: &str) -> PolicyError {
    PolicyError::Field { field: name.to_owned(), expected: expected.to_owned() }
}

fn read(path: &Path) -> Result<String, PolicyError> {
    std::fs::read_to_string(path).map_err(|e| PolicyError::Io { path: path.display().to_string(), message: e.to_string() })
}

fn expect_schema(root: &Map<String, Value>, schema: &str) -> Result<(), PolicyError> {
    if string(root, "schema_version")? == schema {
        Ok(())
    } else {
        Err(field("schema_version", schema))
    }
}

fn check_order(root: &Map<String, Value>, key: &str, expected: &[&str]) -> Result<(), PolicyError> {
    let found = strings(root, key)?;
    if found.iter().map(String::as_str).eq(expected.iter().copied()) {
        Ok(())
    } else {
        Err(field(key, &expected.join(" < ")))
    }
}

fn object<'a>(map: &'a Map<String, Value>, key: &str) -> Result<&'a Map<String, Value>, PolicyError> {
    map.get(key).and_then(Value::as_object).ok_or_else(|| field(key, "an object"))
}

fn array<'a>(map: &'a Map<String, Value>, key: &str) -> Result<&'a Vec<Value>, PolicyError> {
    map.get(key).and_then(Value::as_array).ok_or_else(|| field(key, "an array"))
}

fn string<'a>(map: &'a Map<String, Value>, key: &str) -> Result<&'a str, PolicyError> {
    map.get(key).and_then(Value::as_str).ok_or_else(|| field(key, "a string"))
}

fn strings(map: &Map<String, Value>, key: &str) -> Result<Vec<String>, PolicyError> {
    array(map, key)?
        .iter()
        .map(|v| v.as_str().map(str::to_owned).ok_or_else(|| field(key, "an array of strings")))
        .collect()
}

/// True for exactly 64 lower-case hexadecimal digits.
pub fn is_sha256(text: &str) -> bool {
    text.len() == 64 && text.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

/// Match a `/`-separated path against a glob: `**` spans zero or more whole
/// components, `*` any run of characters within one component, `?` one character.
///
/// Cost: O(P x S) for P pattern components and S path components, each component
/// comparison O(p x s) in characters; no backtracking.
pub fn glob_match(pattern: &str, path: &str) -> bool {
    let pattern: Vec<&str> = pattern.split('/').collect();
    let path: Vec<&str> = path.split('/').collect();
    wildcard(&pattern, &path, |p| *p == "**", |p, s| match_component(p, s))
}

fn match_component(pattern: &str, text: &str) -> bool {
    let pattern: Vec<char> = pattern.chars().collect();
    let text: Vec<char> = text.chars().collect();
    wildcard(&pattern, &text, |c| *c == '*', |c, t| *c == '?' || c == t)
}

/// Wildcard matching by dynamic programming. `row[j]` holds whether the pattern
/// read so far matches `text[..j]`; a star element matches any run of text
/// elements, any other element exactly one element accepted by `single`.
fn wildcard<P, T>(pattern: &[P], text: &[T], is_star: impl Fn(&P) -> bool, single: impl Fn(&P, &T) -> bool) -> bool {
    let mut row: Vec<bool> = std::iter::once(true).chain(text.iter().map(|_| false)).collect();
    for element in pattern {
        row = if is_star(element) {
            prefix_or(&row)
        } else {
            std::iter::once(false).chain(row.iter().zip(text).map(|(&reached, item)| reached && single(element, item))).collect()
        };
    }
    row.last() == Some(&true)
}

/// `out[j]` is true when any of `row[..=j]` is: a star may consume any run.
fn prefix_or(row: &[bool]) -> Vec<bool> {
    row.iter()
        .scan(false, |seen, &reached| {
            *seen = *seen || reached;
            Some(*seen)
        })
        .collect()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
pub(crate) mod tests {
    use super::*;

    pub(crate) const POLICY: &str = r#"{
      "schema_version": "tfqm.governance-policy.v1",
      "level_order": ["L1","L2","L3","L4","L5"],
      "grade_order": ["E","D","C","B","A","A+"],
      "floor": {"min_level": "L4", "min_grade": "D"},
      "companion": {"suffix": ".contract.score.yaml", "document_schema": "tfqm.contract-score.v1",
                    "score_schema": "2.0.0", "collision_suffixes": [".py", ".rs", ".lean"]},
      "populations": [
        {"kind": "rust", "language": "Rust", "globs": ["code/**/*.rs"]},
        {"kind": "python", "language": "Python", "globs": ["code/**/*.py"]},
        {"kind": "lean", "language": "Lean 4", "globs": ["lean4/**/*.lean"]}
      ],
      "exclusions": {"path_parts": ["target", "__pycache__", ".lake"],
                     "path_globs": ["dag/results/**", "papers/**/archive/**"]},
      "pinned_boilerplate": [{"glob": "code/rust/**/build.rs",
        "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        "template": "governance/hook/build.rs", "reason": "hook"}],
      "enforcement": {"env": "TFQM_GOVERNANCE"}
    }"#;

    pub(crate) fn policy() -> Policy {
        Policy::from_json(POLICY).unwrap()
    }

    #[test]
    fn policy_parses_floor_and_populations() {
        let p = policy();
        assert_eq!(p.floor, Floor { min_level: Level::L4, min_grade: Grade::D });
        assert_eq!(p.populations.len(), 3);
        assert_eq!(p.spec_for("code/rust/src/x/lib.rs").map(|s| s.kind()), Some(ArtifactKind::Rust));
        assert_eq!(p.spec_for("code/python/a.py").map(|s| s.language().to_owned()), Some("Python".into()));
        assert_eq!(p.spec_for("lean4/A/B.lean").map(|s| s.kind()), Some(ArtifactKind::Lean));
        assert!(p.spec_for("code/rust/target/debug/x.rs").is_none());
        assert!(p.spec_for("scripts/x.py").is_none());
        assert!(p.spec_for("lean4/.lake/packages/m/M.lean").is_none());
        assert!(p.spec_for("code/rust/Cargo.toml").is_none());
        assert_eq!(p.mode_env, "TFQM_GOVERNANCE");
        assert!(p.pinned_for("code/rust/src/a/build.rs").is_some());
        assert!(p.pinned_for("code/rust/src/a/lib.rs").is_none());
    }

    #[test]
    fn policy_rejects_wrong_orders_and_shapes() {
        let swapped = POLICY.replace(r#"["E","D","C","B","A","A+"]"#, r#"["D","E","C","B","A","A+"]"#);
        assert!(matches!(Policy::from_json(&swapped), Err(PolicyError::Field { field, .. }) if field == "grade_order"));
        let bad_level = POLICY.replace(r#""min_level": "L4""#, r#""min_level": "L9""#);
        assert!(matches!(Policy::from_json(&bad_level), Err(PolicyError::Field { field, .. }) if field == "floor.min_level"));
        let bad_grade = POLICY.replace(r#""min_grade": "D""#, r#""min_grade": "F""#);
        assert!(matches!(Policy::from_json(&bad_grade), Err(PolicyError::Field { field, .. }) if field == "floor.min_grade"));
        let bad_schema = POLICY.replace("tfqm.governance-policy.v1", "v0");
        assert!(matches!(Policy::from_json(&bad_schema), Err(PolicyError::Field { field, .. }) if field == "schema_version"));
        assert!(matches!(Policy::from_json("{"), Err(PolicyError::Json(_))));
        assert!(matches!(Policy::from_json("[]"), Err(PolicyError::Field { .. })));
        let bad_kind = POLICY.replace(r#""kind": "lean""#, r#""kind": "cobol""#);
        assert!(matches!(Policy::from_json(&bad_kind), Err(PolicyError::Field { field, .. }) if field == "populations[].kind"));
        let bad_pin = POLICY.replace("0000000000000000000000000000000000000000000000000000000000000000", "XYZ");
        assert!(matches!(Policy::from_json(&bad_pin), Err(PolicyError::Field { field, .. }) if field == "pinned_boilerplate[].sha256"));
        let no_globs = POLICY.replace(r#""globs": ["lean4/**/*.lean"]"#, r#""globs": []"#);
        assert!(matches!(Policy::from_json(&no_globs), Err(PolicyError::Field { field, .. }) if field == "populations[].globs"));
        let no_pops = POLICY.replace(r#""populations": ["#, r#""populations": [], "x": ["#);
        assert!(matches!(Policy::from_json(&no_pops), Err(PolicyError::Field { field, .. }) if field == "populations"));
        let int_globs = POLICY.replace(r#""path_parts": ["target", "__pycache__", ".lake"]"#, r#""path_parts": [1]"#);
        assert!(matches!(Policy::from_json(&int_globs), Err(PolicyError::Field { field, .. }) if field == "path_parts"));
        let bad_env = POLICY.replace(r#""env": "TFQM_GOVERNANCE""#, r#""env": "OTHER""#);
        assert!(matches!(Policy::from_json(&bad_env), Err(PolicyError::Field { field, .. }) if field == "enforcement.env"));
        assert!(PolicyError::Json("x".into()).to_string().contains("invalid JSON"));
        assert!(Policy::load(Path::new("no/such/policy.json")).is_err());
    }

    #[test]
    fn globs() {
        assert!(glob_match("code/**/*.rs", "code/a.rs"));
        assert!(glob_match("code/**/*.rs", "code/rust/src/a/b.rs"));
        assert!(!glob_match("code/**/*.rs", "code/rust/src/a/b.rs.bak"));
        assert!(!glob_match("code/**/*.rs", "lean4/a.rs"));
        assert!(!glob_match("code/**/*.rs", "code"));
        assert!(glob_match("papers/**/archive/**", "papers/x/y/archive/z.py"));
        assert!(glob_match("papers/**/archive/**", "papers/archive/z.py"));
        assert!(!glob_match("papers/**/archive/**", "papers/x/archived/z.py"));
        assert!(glob_match("dag/results/**", "dag/results/a/b.py"));
        assert!(!glob_match("dag/results/**", "dag/resultsx/a.py"));
        assert!(glob_match("a/?.rs", "a/b.rs"));
        assert!(!glob_match("a/?.rs", "a/bc.rs"));
        assert!(!glob_match("a/?.rs", "a/.rs"));
        assert!(glob_match("a/*", "a/"));
        assert!(glob_match("*", "x"));
        assert!(!glob_match("*", "x/y"));
        assert!(glob_match("**", "x/y"));
        assert!(!glob_match("a/b", "a"));
        assert!(glob_match("a/**/b/**/c", "a/x/b/y/z/c"));
        assert!(!glob_match("a/**/b/**/c", "a/x/c"));
        assert!(glob_match("*.contract.*", "m.contract.score.yaml"));
        assert!(glob_match("ÃƒÂ©?/*", "ÃƒÂ©x/ÃƒÂ¼.py"), "? and * work on characters");
        // Pathological patterns stay polynomial (no backtracking blow-up).
        let long = "a".repeat(200);
        assert!(!glob_match(&format!("{}b", "*a".repeat(30)), &long));
        assert!(!glob_match(&format!("{}/x", "**/".repeat(30)), &vec!["a"; 60].join("/")));
    }

    #[test]
    fn exclusions_and_populations_use_any_glob() {
        let ex = Exclusions { path_parts: vec!["target".into()], path_globs: vec!["x/**".into(), "y/**".into()] };
        assert!(ex.excludes("y/a.rs"), "one matching glob of several suffices");
        assert!(ex.excludes("x/a.rs"));
        assert!(ex.excludes("z/target/a.rs"));
        assert!(!ex.excludes("z/a.rs"));
        let spec = PopulationSpec { kind: ArtifactKind::Rust, language: "Rust".into(), globs: vec!["a/**/*.rs".into(), "b/**/*.rs".into()], exclusions: ex };
        assert!(spec.admits("b/m.rs"), "one matching glob of several suffices");
        assert!(spec.admits("a/m.rs"));
        assert!(!spec.admits("y/m.rs"));
        assert!(!spec.admits("c/m.rs"));
    }

    #[test]
    fn companion_naming_follows_collision_rule() {
        let p = policy();
        let none = |_: &str| false;
        assert_eq!(p.companion_path("code/a/m.rs", none), "code/a/m.contract.score.yaml");
        assert_eq!(p.companion_path("top.py", none), "top.contract.score.yaml");
        let twin = |c: &str| c == "code/a/m.py";
        assert_eq!(p.companion_path("code/a/m.rs", twin), "code/a/m.rs.contract.score.yaml");
        // The source itself is not its own sibling.
        let itself = |c: &str| c == "code/a/m.rs";
        assert_eq!(p.companion_path("code/a/m.rs", itself), "code/a/m.contract.score.yaml");
    }

    #[test]
    fn baseline_round_trip_and_grandfathering() {
        let sha = "a".repeat(64);
        let mut b = Baseline::default();
        b.entries.insert("code/x.rs".into(), BaselineEntry { sha256: sha.clone(), deficit: "COMPLETENESS".into(), reason: None });
        b.entries.insert("code/y.py".into(), BaselineEntry { sha256: "b".repeat(64), deficit: "MISSING_COMPANION".into(), reason: Some("why".into()) });
        let text = b.to_json_text();
        assert_eq!(Baseline::from_json(&text).unwrap(), b);
        assert!(text.contains("\"entries\": 2"));
        assert!(b.grandfathers("code/x.rs", &sha));
        assert!(!b.grandfathers("code/x.rs", &"c".repeat(64)));
        assert!(!b.grandfathers("code/z.rs", &sha));
        let empty = Baseline::default().to_json_text();
        assert_eq!(Baseline::from_json(&empty).unwrap(), Baseline::default());
        let bad = text.replace(&sha, "nothex");
        assert!(matches!(Baseline::from_json(&bad), Err(PolicyError::Field { field, .. }) if field == "entries.code/x.rs.sha256"));
        assert!(matches!(Baseline::from_json("{\"schema_version\": \"x\"}"), Err(PolicyError::Field { .. })));
        assert!(Baseline::load(Path::new("no/such/baseline.json")).is_err());
    }

    #[test]
    fn sha_shape() {
        assert!(is_sha256(&"0123456789abcdef".repeat(4)));
        assert!(!is_sha256(&"0123456789ABCDEF".repeat(4)));
        assert!(!is_sha256(&"g".repeat(64)));
        assert!(!is_sha256(&"a".repeat(63)));
    }

    #[test]
    fn kind_keys_round_trip() {
        for kind in [ArtifactKind::Rust, ArtifactKind::Python, ArtifactKind::Lean, ArtifactKind::Sql, ArtifactKind::Other] {
            assert_eq!(ArtifactKind::from_key(kind.key()), Some(kind));
        }
        assert_eq!(ArtifactKind::from_key("go"), None);
    }
    #[test]
    fn support_exceptions_are_exact_and_fail_closed() {
        let mut value: Value = serde_json::from_str(POLICY).unwrap();
        let pin = serde_json::json!({"sha256": "a".repeat(64), "category": "regression_test", "reason": "reviewed fixture"});
        value["support_exceptions"] = serde_json::json!({"code/test.py": pin});
        let policy = Policy::from_json(&value.to_string()).unwrap();
        assert_eq!(policy.floor_for("code/test.py", &"a".repeat(64)).min_level, Level::L1);
        assert_eq!(policy.floor_for("code/test.py", &"b".repeat(64)), policy.floor);
        assert_eq!(policy.floor_for("code/other.py", &"a".repeat(64)), policy.floor);
        for path in ["../test.py", "/test.py", "code/*.py", "C:/test.py", "code//test.py"] {
            value["support_exceptions"] = serde_json::json!({path: pin});
            assert!(Policy::from_json(&value.to_string()).is_err(), "{path}");
        }
    }

    #[test]
    fn support_exception_requires_review_metadata() {
        for (key, bad) in [("sha256", "bad"), ("category", "runtime"), ("reason", " ")] {
            let mut value: Value = serde_json::from_str(POLICY).unwrap();
            let mut pin = serde_json::json!({"sha256": "a".repeat(64), "category": "regression_test", "reason": "review"});
            pin[key] = Value::String(bad.into());
            value["support_exceptions"] = serde_json::json!({"code/test.py": pin});
            assert!(Policy::from_json(&value.to_string()).is_err(), "{key}");
        }
    }

}
