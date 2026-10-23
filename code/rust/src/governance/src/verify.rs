//! The verifiers. Each checks one rule against a [`ContractDescriptor`] in a
//! [`Context`] and returns the first [`Violation`] it finds.
//!
//! | Verifier | Rule |
//! |---|---|
//! | [`SchemaVerifier`] | document and current score have the required shape and intact history bytes |
//! | [`BindingVerifier`] | contract and current score bind this source path and its current SHA-256 |
//! | [`CompletenessVerifier`] | no unassessed gate; composite and token agree with the gates |
//! | [`FloorVerifier`] | token meets the policy floor, unless grandfathered with unchanged bytes |
//!
//! Cost: each verifier is O(1) over the parsed descriptor (five gates, five binding fields).

use std::fmt;

use super::descriptor::ContractDescriptor;
use super::policy::{ArtifactKind, Baseline, Policy};
use super::score::{CompletedScore, ScoreClaim};

/// The rule a violation breaks; its code is what the baseline records as a deficit.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Rule {
    /// The source or companion could not be read.
    Io,
    /// No companion next to the source.
    MissingCompanion,
    /// The companion is not JSON.
    MalformedJson,
    /// Required keys, vocabulary or history integrity.
    Schema,
    /// Path or digest binding.
    Binding,
    /// Unassessed gate or inconsistent composite or token.
    Completeness,
    /// Below the acceptance floor.
    Floor,
}

impl Rule {
    /// Stable upper-case code.
    pub fn code(self) -> &'static str {
        match self {
            Rule::Io => "IO",
            Rule::MissingCompanion => "MISSING_COMPANION",
            Rule::MalformedJson => "MALFORMED_JSON",
            Rule::Schema => "SCHEMA",
            Rule::Binding => "BINDING",
            Rule::Completeness => "COMPLETENESS",
            Rule::Floor => "FLOOR",
        }
    }
}

/// A precise rule violation: which file, which rule, what was expected and found.
///
/// Fields: `path` is the file at fault, `field` the offending key, `expected` and
/// `found` the required and actual values, `message` an underlying error text.
#[allow(missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Violation {
    /// A file could not be read.
    Io { path: String, message: String },
    /// The source has no companion at the expected path.
    MissingCompanion { path: String, expected: String },
    /// The companion text is not a JSON object.
    MalformedJson { path: String, message: String },
    /// A field is absent or has an invalid value.
    Schema { path: String, field: String, expected: String, found: String },
    /// The companion binds other bytes or another path.
    Binding { path: String, field: String, expected: String, found: String },
    /// The score is incomplete or internally inconsistent.
    Completeness { path: String, field: String, expected: String, found: String },
    /// The score is below the floor.
    Floor { path: String, expected: String, found: String },
}

impl Violation {
    /// The rule this violation breaks.
    pub fn rule(&self) -> Rule {
        match self {
            Violation::Io { .. } => Rule::Io,
            Violation::MissingCompanion { .. } => Rule::MissingCompanion,
            Violation::MalformedJson { .. } => Rule::MalformedJson,
            Violation::Schema { .. } => Rule::Schema,
            Violation::Binding { .. } => Rule::Binding,
            Violation::Completeness { .. } => Rule::Completeness,
            Violation::Floor { .. } => Rule::Floor,
        }
    }

    /// The file the violation is about.
    pub fn path(&self) -> &str {
        match self {
            Violation::Io { path, .. }
            | Violation::MissingCompanion { path, .. }
            | Violation::MalformedJson { path, .. }
            | Violation::Schema { path, .. }
            | Violation::Binding { path, .. }
            | Violation::Completeness { path, .. }
            | Violation::Floor { path, .. } => path,
        }
    }
}

impl fmt::Display for Violation {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let code = self.rule().code();
        match self {
            Violation::Io { path, message } | Violation::MalformedJson { path, message } => write!(f, "{path}: [{code}] {message}"),
            Violation::MissingCompanion { path, expected } => write!(f, "{path}: [{code}] expected companion {expected}, found none"),
            Violation::Schema { path, field, expected, found }
            | Violation::Binding { path, field, expected, found }
            | Violation::Completeness { path, field, expected, found } => {
                write!(f, "{path}: [{code}] {field}: expected {expected}, found {found}")
            }
            Violation::Floor { path, expected, found } => write!(f, "{path}: [{code}] score: expected {expected}, found {found}"),
        }
    }
}

impl std::error::Error for Violation {}

/// The source file under verification.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SourceFile {
    /// Repository-relative posix path.
    pub rel_path: String,
    /// SHA-256 of its current bytes.
    pub sha256: String,
    /// Build kind of its population.
    pub kind: ArtifactKind,
    /// Language label score records must carry.
    pub language: String,
    /// Repository-relative path of its companion.
    pub companion: String,
}

/// Everything a verifier may consult besides the descriptor.
#[derive(Debug, Clone, Copy)]
pub struct Context<'a> {
    /// The policy in force.
    pub policy: &'a Policy,
    /// The grandfather list.
    pub baseline: &'a Baseline,
    /// The source being verified.
    pub source: &'a SourceFile,
}

/// One governance rule.
pub trait Verifier {
    /// Short name used in reports.
    fn name(&self) -> &'static str;
    /// Check the rule; `Err` carries the first violation found.
    fn verify(&self, ctx: &Context<'_>, d: &ContractDescriptor) -> Result<(), Violation>;
}

/// The verifiers in the order they run.
pub fn standard_verifiers() -> Vec<Box<dyn Verifier>> {
    vec![Box::new(SchemaVerifier), Box::new(BindingVerifier), Box::new(CompletenessVerifier), Box::new(FloorVerifier)]
}

fn schema(d: &ContractDescriptor, field: &str, expected: impl Into<String>, found: impl Into<String>) -> Violation {
    Violation::Schema { path: d.companion_path.clone(), field: field.to_owned(), expected: expected.into(), found: found.into() }
}

fn show(value: Option<&str>) -> String {
    value.map_or_else(|| "nothing".to_owned(), str::to_owned)
}

/// The document parses, carries the required keys, the policy's schemas and intact
/// current history entries, and the current score uses valid vocabulary.
#[derive(Debug, Clone, Copy, Default)]
pub struct SchemaVerifier;

impl Verifier for SchemaVerifier {
    fn name(&self) -> &'static str {
        "schema"
    }

    fn verify(&self, ctx: &Context<'_>, d: &ContractDescriptor) -> Result<(), Violation> {
        document_shape(ctx.policy, d)?;
        score_shape(ctx.policy, d)?;
        d.level()?;
        d.gate_grades()?;
        d.composite()?;
        d.token().map(|_| ())
    }
}

/// Schema, required keys and an intact current contract.
fn document_shape(policy: &Policy, d: &ContractDescriptor) -> Result<(), Violation> {
    let expected = policy.companion.document_schema.as_str();
    if d.document_schema.as_deref() != Some(expected) {
        return Err(schema(d, "schema_version", expected, show(d.document_schema.as_deref())));
    }
    if let Some(key) = d.missing_keys.first() {
        return Err(schema(d, key, "present", "absent"));
    }
    if !d.contract_view_ok {
        return Err(schema(d, "contract", "equal to the intact current_contract history record", "a differing or corrupt record"));
    }
    Ok(())
}

/// A current score entry with intact bytes, the policy's score schema and a completion flag.
fn score_shape(policy: &Policy, d: &ContractDescriptor) -> Result<(), Violation> {
    let score = d.current_score.as_ref().ok_or_else(|| schema(d, "current_scoring", "a digest naming a scoring_history entry", "no such entry"))?;
    if !score.digest_ok {
        return Err(schema(d, "scoring_history[current].raw_utf8", format!("bytes hashing to {}", score.digest), "different bytes or length"));
    }
    let expected = policy.companion.score_schema.as_str();
    if score.schema_version.as_deref() != Some(expected) {
        return Err(schema(d, "score.schema_version", expected, show(score.schema_version.as_deref())));
    }
    if score.is_complete.is_none() {
        return Err(schema(d, "is_complete", "a boolean", "absent or not boolean"));
    }
    Ok(())
}

/// The contract and the current score both bind this source's path and current
/// SHA-256, and the score declares the population's language.
#[derive(Debug, Clone, Copy, Default)]
pub struct BindingVerifier;

impl Verifier for BindingVerifier {
    fn name(&self) -> &'static str {
        "binding"
    }

    fn verify(&self, ctx: &Context<'_>, d: &ContractDescriptor) -> Result<(), Violation> {
        let source = ctx.source;
        let score = d.current_score.as_ref();
        let checks = [
            ("contract.artifact.path", source.rel_path.as_str(), d.artifact_path.as_deref()),
            ("contract.artifact.sha256", source.sha256.as_str(), d.artifact_sha256.as_deref()),
            ("score.artifact.path", source.rel_path.as_str(), score.and_then(|s| s.artifact_path.as_deref())),
            ("score.artifact.sha256", source.sha256.as_str(), score.and_then(|s| s.artifact_sha256.as_deref())),
            ("score.artifact.language", source.language.as_str(), score.and_then(|s| s.language.as_deref())),
        ];
        match checks.into_iter().find(|(_, expected, found)| Some(*expected) != *found) {
            Some((field, expected, found)) => Err(Violation::Binding {
                path: d.companion_path.clone(),
                field: field.to_owned(),
                expected: expected.to_owned(),
                found: show(found),
            }),
            None => Ok(()),
        }
    }
}

/// The current score is completed: `is_complete`, every gate graded, the composite
/// equal to the weakest gate, and the token equal to level plus composite.
#[derive(Debug, Clone, Copy, Default)]
pub struct CompletenessVerifier;

impl Verifier for CompletenessVerifier {
    fn name(&self) -> &'static str {
        "completeness"
    }

    fn verify(&self, _ctx: &Context<'_>, d: &ContractDescriptor) -> Result<(), Violation> {
        completed_score(d)?;
        Ok(())
    }
}

fn completed_score(d: &ContractDescriptor) -> Result<CompletedScore, Violation> {
    let claim = ScoreClaim {
        level: d.level()?,
        gates: d.gate_grades()?,
        is_complete: d.current_score.as_ref().and_then(|s| s.is_complete) == Some(true),
        composite: d.composite()?,
        token: d.token()?,
    };
    claim.validate().map_err(|error| {
        let (expected, found) = error.values();
        Violation::Completeness { path: d.companion_path.clone(), field: error.field().into(), expected, found }
    })
}

/// The token meets the floor, unless the baseline lists this path with these exact bytes.
#[derive(Debug, Clone, Copy, Default)]
pub struct FloorVerifier;

impl Verifier for FloorVerifier {
    fn name(&self) -> &'static str {
        "floor"
    }

    fn verify(&self, ctx: &Context<'_>, d: &ContractDescriptor) -> Result<(), Violation> {
        let completed = completed_score(d)?;
        if ctx.baseline.grandfathers(&ctx.source.rel_path, &ctx.source.sha256) {
            return Ok(());
        }
        let floor = ctx.policy.floor_for(&ctx.source.rel_path, &ctx.source.sha256);
        if completed.admitted_by(floor) {
            Ok(())
        } else {
            Err(Violation::Floor {
                path: d.companion_path.clone(),
                expected: format!("a completed token with {floor}"),
                found: completed.token().to_string(),
            })
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
mod tests {
    use super::*;
    use crate::descriptor::tests::{companion, score};
    use crate::policy::tests::policy;
    use crate::policy::BaselineEntry;

    const PATH: &str = "code/x.rs";

    fn source(sha: &str) -> SourceFile {
        SourceFile { rel_path: PATH.into(), sha256: sha.into(), kind: ArtifactKind::Rust, language: "Rust".into(), companion: "code/x.contract.score.yaml".into() }
    }

    fn run(text: &str, sha: &str, baseline: &Baseline) -> Result<(), Violation> {
        let policy = policy();
        let source = source(sha);
        let ctx = Context { policy: &policy, baseline, source: &source };
        let d = ContractDescriptor::parse(&source.companion, text)?;
        for verifier in standard_verifiers() {
            verifier.verify(&ctx, &d)?;
        }
        Ok(())
    }

    fn token_case(level: &str, grade: &str, token: &str) -> Result<(), Violation> {
        let sha = "a".repeat(64);
        let text = companion(PATH, &sha, score(PATH, &sha, level, [Some(grade); 5], Some(grade), Some(token), true));
        run(&text, &sha, &Baseline::default())
    }

    #[test]
    fn floor_pass_and_fail_cases() {
        assert_eq!(token_case("L4", "D", "L4D"), Ok(()));
        assert_eq!(token_case("L5", "A+", "L5A+"), Ok(()));
        assert_eq!(token_case("L4", "C", "L4C"), Ok(()));
        let e = token_case("L4", "E", "L4E").unwrap_err();
        assert_eq!(e.rule(), Rule::Floor);
        assert!(e.to_string().contains("found L4E"), "{e}");
        let e = token_case("L3", "A", "L3A").unwrap_err();
        assert_eq!(e.rule(), Rule::Floor);
        assert!(e.to_string().contains("level >= L4 and grade >= D"), "{e}");
    }

    #[test]
    fn null_gate_is_incomplete() {
        let sha = "a".repeat(64);
        let text = companion(PATH, &sha, score(PATH, &sha, "L4", [Some("C"), Some("C"), None, Some("C"), Some("C")], None, None, false));
        let e = run(&text, &sha, &Baseline::default()).unwrap_err();
        assert_eq!(e.rule(), Rule::Completeness);
        assert!(e.to_string().contains("unassessed G3"), "{e}");
    }

    #[test]
    fn inconsistent_composite_flag_or_token_is_incomplete() {
        let sha = "a".repeat(64);
        let case = |s| run(&companion(PATH, &sha, s), &sha, &Baseline::default()).unwrap_err();
        let e = case(score(PATH, &sha, "L4", [Some("C"), Some("B"), Some("B"), Some("B"), Some("B")], Some("B"), Some("L4B"), true));
        assert!(matches!(&e, Violation::Completeness { field, expected, found, .. } if field == "composite_grade" && expected == "C" && found == "B"), "{e}");
        let e = case(score(PATH, &sha, "L4", [Some("C"); 5], Some("C"), Some("L5C"), true));
        assert!(matches!(&e, Violation::Completeness { field, expected, .. } if field == "score_token" && expected == "L4C"), "{e}");
        let e = case(score(PATH, &sha, "L4", [Some("C"); 5], Some("C"), Some("L4C"), false));
        assert!(matches!(&e, Violation::Completeness { field, .. } if field == "is_complete"), "{e}");
        let e = case(score(PATH, &sha, "L4", [Some("C"); 5], Some("C"), None, true));
        assert!(matches!(&e, Violation::Completeness { field, found, .. } if field == "score_token" && found == "nothing"), "{e}");
    }

    #[test]
    fn binding_mismatch_names_the_field() {
        let old = "a".repeat(64);
        let new = "b".repeat(64);
        let text = companion(PATH, &old, score(PATH, &old, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        let e = run(&text, &new, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Binding { field, expected, found, .. } if field == "contract.artifact.sha256" && *expected == new && *found == old), "{e}");
        let text = companion("code/y.rs", &new, score(PATH, &new, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        let e = run(&text, &new, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Binding { field, .. } if field == "contract.artifact.path"), "{e}");
        let text = companion(PATH, &new, score(PATH, &old, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        let e = run(&text, &new, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Binding { field, .. } if field == "score.artifact.sha256"), "{e}");
        let mut s = score(PATH, &new, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true);
        s["artifact"]["language"] = "Python".into();
        let e = run(&companion(PATH, &new, s), &new, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Binding { field, .. } if field == "score.artifact.language"), "{e}");
        let s = score("code/z.rs", &new, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true);
        let e = run(&companion(PATH, &new, s), &new, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Binding { field, .. } if field == "score.artifact.path"), "{e}");
    }

    #[test]
    fn baseline_waives_floor_only_for_unchanged_bytes() {
        let sha = "a".repeat(64);
        let text = companion(PATH, &sha, score(PATH, &sha, "L2", [Some("B"); 5], Some("B"), Some("L2B"), true));
        let mut baseline = Baseline::default();
        baseline.entries.insert(PATH.into(), BaselineEntry { sha256: sha.clone(), deficit: "FLOOR".into(), reason: None });
        assert_eq!(run(&text, &sha, &baseline), Ok(()));
        // Same path, new bytes: grandfathering is lost and the floor applies.
        let changed = "c".repeat(64);
        let text = companion(PATH, &changed, score(PATH, &changed, "L2", [Some("B"); 5], Some("B"), Some("L2B"), true));
        let e = run(&text, &changed, &baseline).unwrap_err();
        assert_eq!(e.rule(), Rule::Floor);
    }

    #[test]
    fn schema_failures_are_specific() {
        let sha = "a".repeat(64);
        let good = companion(PATH, &sha, score(PATH, &sha, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        let mutate = |f: &dyn Fn(&mut serde_json::Value)| {
            let mut v: serde_json::Value = serde_json::from_str(&good).unwrap();
            f(&mut v);
            run(&v.to_string(), &sha, &Baseline::default()).unwrap_err()
        };
        let e = mutate(&|v| v["schema_version"] = "tfqm.contract-score.v0".into());
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "schema_version"), "{e}");
        let e = mutate(&|v| {
            v.as_object_mut().unwrap().remove("artifact");
        });
        assert!(matches!(&e, Violation::Schema { field, found, .. } if field == "artifact" && found == "absent"), "{e}");
        let e = mutate(&|v| {
            let doc = v.as_object_mut().unwrap();
            doc.remove("artifact");
            doc.remove("scoring_history");
        });
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "artifact"), "the first missing key is reported: {e}");
        let e = mutate(&|v| v["current_scoring"] = "0".repeat(64).into());
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "current_scoring"), "{e}");
        let e = mutate(&|v| v["scoring_history"][0]["bytes"] = 1.into());
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "scoring_history[current].raw_utf8"), "{e}");
        let e = mutate(&|v| v["contract"]["symbols"] = serde_json::json!([]));
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "contract"), "{e}");
        let old = score(PATH, &sha, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true);
        let mut v1 = old.clone();
        v1["schema_version"] = "1.0.0".into();
        let e = run(&companion(PATH, &sha, v1), &sha, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "score.schema_version"), "{e}");
        let mut no_flag = old;
        no_flag.as_object_mut().unwrap().remove("is_complete");
        let e = run(&companion(PATH, &sha, no_flag), &sha, &Baseline::default()).unwrap_err();
        assert!(matches!(&e, Violation::Schema { field, .. } if field == "is_complete"), "{e}");
    }

    #[test]
    fn violation_display_is_precise() {
        let v = Violation::Floor { path: "p".into(), expected: "x".into(), found: "L3A".into() };
        assert_eq!(v.to_string(), "p: [FLOOR] score: expected x, found L3A");
        assert_eq!(v.path(), "p");
        let m = Violation::MissingCompanion { path: "a.rs".into(), expected: "a.contract.score.yaml".into() };
        assert_eq!(m.to_string(), "a.rs: [MISSING_COMPANION] expected companion a.contract.score.yaml, found none");
        let io = Violation::Io { path: "q".into(), message: "gone".into() };
        assert_eq!(io.to_string(), "q: [IO] gone");
        assert_eq!(io.rule().code(), "IO");
        let names: Vec<&str> = standard_verifiers().iter().map(|v| v.name()).collect();
        assert_eq!(names, ["schema", "binding", "completeness", "floor"]);
    }
    #[test]
    fn support_pin_never_accepts_incomplete_or_grade_e() {
        let sha = "a".repeat(64);
        let mut policy = policy();
        policy.support_exceptions.insert(PATH.into(), crate::policy::SupportException {
            sha256: sha.clone(), category: "regression_test".into(), reason: "reviewed test".into(),
        });
        let source = source(&sha);
        let baseline = Baseline::default();
        let ctx = Context { policy: &policy, baseline: &baseline, source: &source };
        let good = companion(PATH, &sha, score(PATH, &sha, "L2", [Some("D"); 5], Some("D"), Some("L2D"), true));
        let d = ContractDescriptor::parse(&source.companion, &good).unwrap();
        assert_eq!(FloorVerifier.verify(&ctx, &d), Ok(()));
        let bad = companion(PATH, &sha, score(PATH, &sha, "L2", [Some("E"); 5], Some("E"), Some("L2E"), true));
        let d = ContractDescriptor::parse(&source.companion, &bad).unwrap();
        assert!(matches!(FloorVerifier.verify(&ctx, &d), Err(Violation::Floor { .. })));
        let bad = companion(PATH, &sha, score(PATH, &sha, "L2", [None; 5], None, None, false));
        let d = ContractDescriptor::parse(&source.companion, &bad).unwrap();
        assert!(matches!(FloorVerifier.verify(&ctx, &d), Err(Violation::Completeness { .. })));
    }

}
