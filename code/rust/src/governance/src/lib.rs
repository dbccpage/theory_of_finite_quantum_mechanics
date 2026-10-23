//! Build-time contract governance for the Theory of Finite Quantum Mechanics.
//!
//! Every governed source (Rust and Python under `code/`, Lean under `lean4/`,
//! as declared in `governance/policy.json`) needs a `*.contract.score.yaml`
//! companion that binds its path and exact SHA-256 and carries a completed
//! SCORING.md score at or above the floor (level L4 and grade D). Sources listed
//! in `governance/baseline.json` with unchanged bytes are grandfathered.
//!
//! * [`verify_paths`] / [`verify_file`] run the [`verify::standard_verifiers`]
//!   over sources and return a [`Report`].
//! * [`verify_crate_contracts!`] is the one-line `build.rs` hook (see
//!   [`buildtime`]); the `governance-check` binary covers Python and Lean and CI.
//!
//! AuthorityEffect: None. A passing check certifies that a score record exists,
//! is well formed, binds the bytes and meets the floor. It does not certify that
//! the grades are deserved; that is the reviewer's reading of the cited evidence.
//!
//! Cost: [`verify_paths`] reads and hashes each source once and parses its companion
//! once, so it is linear in the bytes checked.

#![forbid(unsafe_code)]
#![deny(missing_docs)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic, clippy::arithmetic_side_effects)]

use std::fmt;
use std::fs;
use std::path::Path;

pub mod buildtime;
pub mod descriptor;
pub mod policy;
pub mod repo;
pub mod score;
pub mod verify;

pub use descriptor::ContractDescriptor;
pub use policy::{ArtifactKind, ArtifactKindSpec, Baseline, BaselineEntry, Policy, PolicyError};
pub use score::{Floor, Gate, GateGrades, Grade, Level, ScoreError, ScoreToken};
pub use verify::{
    BindingVerifier, CompletenessVerifier, Context, FloorVerifier, Rule, SchemaVerifier, SourceFile, Verifier, Violation,
};

/// One-line `build.rs` hook: verify the calling package's Rust sources.
///
/// ```ignore
/// fn main() {
///     governance::verify_crate_contracts!();
/// }
/// ```
///
/// It is a macro so that `CARGO_MANIFEST_DIR` and `CARGO_PKG_NAME` are expanded
/// in the calling package. Behaviour is chosen by `TFQM_GOVERNANCE`
/// (`off`, `warn` (default), `new`, `enforce`); see [`buildtime::Mode`].
#[macro_export]
macro_rules! verify_crate_contracts {
    () => {
        $crate::buildtime::run(::std::env!("CARGO_MANIFEST_DIR"), ::std::env!("CARGO_PKG_NAME"))
    };
}

/// Where a source stands with respect to the baseline.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BaselineStatus {
    /// Not listed: a new file (or one that has left the baseline).
    Absent,
    /// Listed with these exact bytes: grandfathered.
    Unchanged,
    /// Listed with other bytes: grandfathering lost.
    Changed,
}

/// The result for one source.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    /// A completed score at or above the floor binds the current bytes.
    Pass(ScoreToken),
    /// Listed in the baseline with unchanged bytes; not verified further.
    Grandfathered,
    /// Byte-identical to pinned boilerplate (for example the build hook).
    Boilerplate,
    /// At least one violation.
    Fail(Vec<Violation>),
}

/// The verification of one source.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FileReport {
    /// Repository-relative path.
    pub path: String,
    /// SHA-256 of the current bytes, when readable.
    pub sha256: Option<String>,
    /// Baseline status.
    pub baseline: BaselineStatus,
    /// Outcome.
    pub outcome: Outcome,
}

impl FileReport {
    /// True when the outcome is a failure.
    pub fn failed(&self) -> bool {
        matches!(self.outcome, Outcome::Fail(_))
    }

    /// The violations, empty unless failed.
    pub fn violations(&self) -> &[Violation] {
        match &self.outcome {
            Outcome::Fail(v) => v,
            _ => &[],
        }
    }
}

/// The verification of a set of sources.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Report {
    /// One entry per governed source checked, in input order.
    pub files: Vec<FileReport>,
}

impl Report {
    /// The failed files.
    pub fn failures(&self) -> impl Iterator<Item = &FileReport> {
        self.files.iter().filter(|f| f.failed())
    }

    /// True when nothing failed.
    pub fn is_clean(&self) -> bool {
        self.failures().next().is_none()
    }

    /// Number of files whose outcome satisfies `pred`.
    pub fn count(&self, pred: impl Fn(&Outcome) -> bool) -> usize {
        self.files.iter().filter(|f| pred(&f.outcome)).count()
    }

    /// One-line summary.
    pub fn summary(&self) -> String {
        format!(
            "checked {}: {} pass, {} grandfathered, {} boilerplate, {} failed",
            self.files.len(),
            self.count(|o| matches!(o, Outcome::Pass(_))),
            self.count(|o| matches!(o, Outcome::Grandfathered)),
            self.count(|o| matches!(o, Outcome::Boilerplate)),
            self.failures().count(),
        )
    }
}

impl fmt::Display for Report {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "{}", self.summary())?;
        for file in self.failures() {
            let status = match file.baseline {
                BaselineStatus::Absent => "new or not grandfathered",
                BaselineStatus::Changed => "grandfathering lost: bytes changed since the baseline",
                BaselineStatus::Unchanged => "grandfathered",
            };
            writeln!(f, "FAIL {} ({status})", file.path)?;
            file.violations().iter().try_for_each(|violation| writeln!(f, "  {violation}"))?;
        }
        Ok(())
    }
}

/// Verify one repository-relative source. `None` when the path is in no population.
pub fn verify_file(policy: &Policy, baseline: &Baseline, root: &Path, rel_path: &str) -> Option<FileReport> {
    let spec = policy.spec_for(rel_path)?;
    let report = |sha256: Option<String>, status, outcome| FileReport { path: rel_path.to_owned(), sha256, baseline: status, outcome };
    let sha256 = match repo::sha256_file(&root.join(rel_path)) {
        Ok(sha) => sha,
        Err(e) => {
            let violation = Violation::Io { path: rel_path.to_owned(), message: e.to_string() };
            return Some(report(None, BaselineStatus::Absent, Outcome::Fail(vec![violation])));
        }
    };
    let status = match baseline.entries.get(rel_path) {
        None => BaselineStatus::Absent,
        Some(entry) if entry.sha256 == sha256 => BaselineStatus::Unchanged,
        Some(_) => BaselineStatus::Changed,
    };
    if status == BaselineStatus::Unchanged {
        return Some(report(Some(sha256), status, Outcome::Grandfathered));
    }
    if policy.pinned_for(rel_path).is_some_and(|pin| pin.sha256 == sha256) {
        return Some(report(Some(sha256), status, Outcome::Boilerplate));
    }
    let companion = policy.companion_path(rel_path, |p| root.join(p).is_file());
    let source = SourceFile { rel_path: rel_path.to_owned(), sha256: sha256.clone(), kind: spec.kind(), language: spec.language().to_owned(), companion };
    let outcome = match check_source(policy, baseline, root, &source) {
        Ok(token) => Outcome::Pass(token),
        Err(violations) => Outcome::Fail(violations),
    };
    Some(report(Some(sha256), status, outcome))
}

/// Run the verifiers on one source with a known digest and companion path.
fn check_source(policy: &Policy, baseline: &Baseline, root: &Path, source: &SourceFile) -> Result<ScoreToken, Vec<Violation>> {
    let companion = root.join(&source.companion);
    if !companion.is_file() {
        return Err(vec![Violation::MissingCompanion { path: source.rel_path.clone(), expected: source.companion.clone() }]);
    }
    let text = fs::read_to_string(&companion).map_err(|e| vec![Violation::Io { path: source.companion.clone(), message: e.to_string() }])?;
    let descriptor = ContractDescriptor::parse(&source.companion, &text).map_err(|v| vec![v])?;
    let ctx = Context { policy, baseline, source };
    SchemaVerifier.verify(&ctx, &descriptor).map_err(|v| vec![v])?;
    let mut violations: Vec<Violation> = [BindingVerifier.verify(&ctx, &descriptor), CompletenessVerifier.verify(&ctx, &descriptor)]
        .into_iter()
        .filter_map(Result::err)
        .collect();
    if violations.iter().all(|v| v.rule() != Rule::Completeness) {
        violations.extend(FloorVerifier.verify(&ctx, &descriptor).err());
    }
    match (violations.is_empty(), descriptor.token()) {
        (true, Ok(Some(token))) => Ok(token),
        (true, _) => Err(vec![Violation::Completeness {
            path: source.companion.clone(),
            field: "score_token".into(),
            expected: "a completed token".into(),
            found: "nothing".into(),
        }]),
        (false, _) => Err(violations),
    }
}

/// Verify every governed source among `paths` (repository-relative, posix).
/// Paths outside every population are skipped.
pub fn verify_paths(policy: &Policy, baseline: &Baseline, root: &Path, paths: &[String]) -> Report {
    Report { files: paths.iter().filter_map(|p| verify_file(policy, baseline, root, p)).collect() }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
pub(crate) mod tests {
    use super::*;
    use crate::descriptor::tests::{companion, score};
    use crate::policy::tests::POLICY;
    use crate::repo::tests::scratch;
    use std::path::PathBuf;

    pub(crate) struct Repo {
        pub root: PathBuf,
        pub policy: Policy,
    }

    impl Repo {
        pub fn new(tag: &str) -> Repo {
            let root = scratch(tag);
            fs::create_dir_all(root.join("governance")).unwrap();
            let hook = b"fn main() {}\n";
            let hook_sha = crate::descriptor::hex(&<sha2::Sha256 as sha2::Digest>::digest(hook));
            let text = POLICY.replace(&"0".repeat(64), &hook_sha);
            fs::write(root.join("governance/policy.json"), &text).unwrap();
            fs::write(root.join("governance/baseline.json"), Baseline::default().to_json_text()).unwrap();
            Repo { root, policy: Policy::from_json(&text).unwrap() }
        }

        pub fn write(&self, rel: &str, bytes: &[u8]) -> String {
            let path = self.root.join(rel);
            fs::create_dir_all(path.parent().unwrap()).unwrap();
            fs::write(&path, bytes).unwrap();
            repo::sha256_file(&path).unwrap()
        }

        /// Write a source and a companion with the given token at the given level/grade.
        pub fn scored(&self, rel: &str, body: &[u8], level: &str, grade: &str) -> String {
            let sha = self.write(rel, body);
            let token = format!("{level}{grade}");
            let doc = companion(rel, &sha, score(rel, &sha, level, [Some(grade); 5], Some(grade), Some(&token), true));
            let comp = self.policy.companion_path(rel, |p| self.root.join(p).is_file());
            self.write(&comp, doc.as_bytes());
            sha
        }
    }

    impl Drop for Repo {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }

    #[test]
    fn outcomes_cover_pass_fail_grandfather_and_boilerplate() {
        let repo = Repo::new("lib");
        repo.scored("code/a.rs", b"pub fn a() {}\n", "L4", "C");
        repo.scored("code/low.rs", b"pub fn low() {}\n", "L3", "A");
        let legacy = repo.write("code/legacy.py", b"x = 1\n");
        repo.write("code/new.rs", b"pub fn n() {}\n");
        repo.write("code/rust/src/k/build.rs", b"fn main() {}\n");
        repo.write("code/rust/src/k/build2.rs", b"fn main() {}\n");
        repo.write("code/rust/src/j/build.rs", b"fn main() { /* edited */ }\n");
        let mut baseline = Baseline::default();
        baseline.entries.insert("code/legacy.py".into(), BaselineEntry { sha256: legacy, deficit: "MISSING_COMPANION".into(), reason: None });
        let paths: Vec<String> =
            ["code/a.rs", "code/low.rs", "code/legacy.py", "code/new.rs", "code/rust/src/k/build.rs", "code/rust/src/j/build.rs", "scripts/x.py", "README.md"]
                .map(String::from)
                .to_vec();
        let report = verify_paths(&repo.policy, &baseline, &repo.root, &paths);
        assert_eq!(report.files.len(), 6, "scripts/ and README are outside every population");
        let outcome = |p: &str| report.files.iter().find(|f| f.path == p).unwrap().outcome.clone();
        assert_eq!(outcome("code/a.rs"), Outcome::Pass("L4C".parse().unwrap()));
        assert!(matches!(outcome("code/low.rs"), Outcome::Fail(v) if v.len() == 1 && v[0].rule() == Rule::Floor));
        assert_eq!(outcome("code/legacy.py"), Outcome::Grandfathered);
        assert!(matches!(outcome("code/new.rs"), Outcome::Fail(v) if v[0].rule() == Rule::MissingCompanion));
        assert_eq!(outcome("code/rust/src/k/build.rs"), Outcome::Boilerplate);
        assert!(matches!(outcome("code/rust/src/j/build.rs"), Outcome::Fail(v) if v[0].rule() == Rule::MissingCompanion));
        assert!(!report.is_clean());
        assert_eq!(report.summary(), "checked 6: 1 pass, 1 grandfathered, 1 boilerplate, 3 failed");
        let text = report.to_string();
        assert!(text.contains("FAIL code/new.rs (new or not grandfathered)"), "{text}");
        assert!(text.contains("[MISSING_COMPANION] expected companion code/new.contract.score.yaml"), "{text}");
    }

    #[test]
    fn changed_bytes_lose_grandfathering() {
        let repo = Repo::new("changed");
        let old = repo.write("lean4/A.lean", b"theorem t : True := trivial\n");
        let mut baseline = Baseline::default();
        baseline.entries.insert("lean4/A.lean".into(), BaselineEntry { sha256: old, deficit: "MISSING_COMPANION".into(), reason: None });
        assert_eq!(verify_file(&repo.policy, &baseline, &repo.root, "lean4/A.lean").unwrap().outcome, Outcome::Grandfathered);
        repo.write("lean4/A.lean", b"theorem t : True := by trivial\n");
        let file = verify_file(&repo.policy, &baseline, &repo.root, "lean4/A.lean").unwrap();
        assert_eq!(file.baseline, BaselineStatus::Changed);
        assert!(file.failed());
        assert!(Report { files: vec![file] }.to_string().contains("grandfathering lost"));
    }

    #[test]
    fn malformed_companion_and_unreadable_source() {
        let repo = Repo::new("malformed");
        repo.write("code/m.rs", b"pub fn m() {}\n");
        repo.write("code/m.contract.score.yaml", b"{\"schema_version\": \"tfqm.contract-score.v1\" \"x\": 1}");
        let file = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/m.rs").unwrap();
        assert!(matches!(file.violations(), [Violation::MalformedJson { path, .. }] if path == "code/m.contract.score.yaml"));
        let gone = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/gone.rs").unwrap();
        assert!(matches!(gone.violations(), [Violation::Io { .. }]));
        assert_eq!(gone.sha256, None);
        let schema = repo.write("code/s.rs", b"pub fn s() {}\n");
        let doc = companion("code/s.rs", &schema, score("code/s.rs", &schema, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        repo.write("code/s.contract.score.yaml", doc.replace("tfqm.contract-score.v1", "other").as_bytes());
        let file = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/s.rs").unwrap();
        assert!(matches!(file.violations(), [Violation::Schema { field, .. }] if field == "schema_version"));
    }

    #[test]
    fn binding_and_completeness_are_both_reported() {
        let repo = Repo::new("both");
        let sha = repo.write("code/b.rs", b"pub fn b() {}\n");
        let stale = "f".repeat(64);
        let doc = companion("code/b.rs", &stale, score("code/b.rs", &sha, "L4", [Some("C"), None, Some("C"), Some("C"), Some("C")], None, None, false));
        repo.write("code/b.contract.score.yaml", doc.as_bytes());
        let file = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/b.rs").unwrap();
        let rules: Vec<Rule> = file.violations().iter().map(Violation::rule).collect();
        assert_eq!(rules, [Rule::Binding, Rule::Completeness], "floor is not repeated when completeness fails");
    }

    #[test]
    fn binding_failure_still_reports_the_floor() {
        let repo = Repo::new("bind-floor");
        let sha = repo.write("code/f.rs", b"pub fn f() {}\n");
        let stale = "f".repeat(64);
        let doc = companion("code/f.rs", &stale, score("code/f.rs", &sha, "L3", [Some("A"); 5], Some("A"), Some("L3A"), true));
        repo.write("code/f.contract.score.yaml", doc.as_bytes());
        let file = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/f.rs").unwrap();
        let rules: Vec<Rule> = file.violations().iter().map(Violation::rule).collect();
        assert_eq!(rules, [Rule::Binding, Rule::Floor]);
    }

    #[test]
    fn twin_sources_use_qualified_companions() {
        let repo = Repo::new("twin");
        repo.write("code/t.py", b"x = 1\n");
        repo.scored("code/t.rs", b"pub fn t() {}\n", "L4", "D");
        assert!(repo.root.join("code/t.rs.contract.score.yaml").is_file());
        let file = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/t.rs").unwrap();
        assert_eq!(file.outcome, Outcome::Pass("L4D".parse().unwrap()));
        let py = verify_file(&repo.policy, &Baseline::default(), &repo.root, "code/t.py").unwrap();
        assert!(matches!(py.violations(), [Violation::MissingCompanion { expected, .. }] if expected == "code/t.py.contract.score.yaml"));
    }
}
