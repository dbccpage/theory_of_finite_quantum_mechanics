//! Build-script support behind [`verify_crate_contracts!`](crate::verify_crate_contracts).
//!
//! A build script verifies the Rust sources of its own package, prints
//! `cargo:rerun-if-changed` for every source, existing companion and the two
//! governance files, and then acts on the mode in `TFQM_GOVERNANCE`:
//!
//! | Mode | Violations |
//! |---|---|
//! | `off` | ignored |
//! | `warn` (default, also when unset) | one `cargo:warning` each; the build continues |
//! | `new` | abort when a file outside the baseline fails; otherwise warn |
//! | `enforce` (CI) | abort with the full report |
//!
//! The default is `warn` because a new file can only earn its score after its
//! tests have run, which needs a successful build. CI runs `enforce` on every
//! pull request, so nothing below the floor merges.
//!
//! Cost: one directory walk of the package and one SHA-256 per source and companion.

use std::fmt;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

use super::policy::{Baseline, Policy, PolicyError, BASELINE_PATH, MODE_ENV, POLICY_PATH};
use super::repo::{self, RepoError};
use super::{verify_paths, BaselineStatus, Report};

/// What a build does with violations.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    /// Skip verification.
    Off,
    /// Report violations as cargo warnings.
    Warn,
    /// Abort for failing files outside the baseline; warn for the rest.
    New,
    /// Abort on any violation.
    Enforce,
}

impl Mode {
    /// Read the value of `TFQM_GOVERNANCE`; unset or empty means `warn`.
    pub fn parse(value: Option<&str>) -> Result<Mode, String> {
        match value.map(str::trim) {
            None | Some("") | Some("warn") => Ok(Mode::Warn),
            Some("off") => Ok(Mode::Off),
            Some("new") => Ok(Mode::New),
            Some("enforce") => Ok(Mode::Enforce),
            Some(other) => Err(format!("{MODE_ENV}={other:?} is not one of off, warn, new, enforce")),
        }
    }
}

/// Why a package could not be verified at all.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BuildError {
    /// No `governance/policy.json` above the package (for example a packaged crate).
    NoPolicy(String),
    /// The policy or baseline is invalid.
    Policy(PolicyError),
    /// The sources could not be read.
    Repo(RepoError),
}

impl fmt::Display for BuildError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            BuildError::NoPolicy(start) => write!(f, "no {POLICY_PATH} found above {start}"),
            BuildError::Policy(e) => write!(f, "governance data: {e}"),
            BuildError::Repo(e) => write!(f, "governance sources: {e}"),
        }
    }
}

impl std::error::Error for BuildError {}

/// The verification of one package.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PackageCheck {
    /// Repository root.
    pub root: PathBuf,
    /// Report over the package's Rust sources.
    pub report: Report,
    /// Files whose change must rerun the build script.
    pub rerun: Vec<PathBuf>,
}

/// Verify the Rust sources of the package at `manifest_dir`.
pub fn check_package(manifest_dir: &Path) -> Result<PackageCheck, BuildError> {
    let root = repo::find_root(manifest_dir).ok_or_else(|| BuildError::NoPolicy(manifest_dir.display().to_string()))?;
    let policy = Policy::load(&root.join(POLICY_PATH)).map_err(BuildError::Policy)?;
    let baseline = Baseline::load(&root.join(BASELINE_PATH)).map_err(BuildError::Policy)?;
    let sources = repo::package_sources(manifest_dir).map_err(BuildError::Repo)?;
    let rel: Vec<String> = sources.iter().filter_map(|p| repo::rel_posix(&root, p)).collect();
    let report = verify_paths(&policy, &baseline, &root, &rel);
    let mut rerun = vec![root.join(POLICY_PATH), root.join(BASELINE_PATH)];
    rerun.extend(watched_dirs(&sources));
    rerun.extend(sources);
    for file in &report.files {
        let companion = policy.companion_path(&file.path, |p| root.join(p).is_file());
        // A missing companion of a failing file is watched too, so creating it reruns.
        if root.join(&companion).is_file() || file.failed() {
            rerun.push(root.join(companion));
        }
    }
    Ok(PackageCheck { root, report, rerun })
}

/// Directories holding sources, so that adding a file reruns the build script.
/// Cargo scans a watched directory recursively, so a directory with a `target`
/// subdirectory (the workspace root) is not watched; its files are watched one by one.
fn watched_dirs(sources: &[PathBuf]) -> Vec<PathBuf> {
    let mut dirs: Vec<PathBuf> = sources.iter().filter_map(|s| s.parent()).filter(|d| !d.join("target").is_dir()).map(Path::to_path_buf).collect();
    dirs.sort();
    dirs.dedup();
    dirs
}

/// What the build does after a check.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Decision {
    /// Nothing to report.
    Silent,
    /// Print these lines as cargo warnings.
    Warn(Vec<String>),
    /// Abort the build with this report.
    Abort(String),
}

/// Apply the mode to a report.
pub fn decide(mode: Mode, report: &Report) -> Decision {
    if mode == Mode::Off || report.is_clean() {
        return Decision::Silent;
    }
    let new_failure = report.failures().any(|f| f.baseline == BaselineStatus::Absent);
    if mode == Mode::Enforce || (mode == Mode::New && new_failure) {
        return Decision::Abort(format!("contract governance ({MODE_ENV}={}):\n{report}", mode_name(mode)));
    }
    let mut lines = vec![format!("contract governance: {} (see governance/README.md; {MODE_ENV}=enforce makes this fatal)", report.summary())];
    lines.extend(report.failures().flat_map(|f| f.violations().iter().map(ToString::to_string)));
    Decision::Warn(lines)
}

fn mode_name(mode: Mode) -> &'static str {
    match mode {
        Mode::Off => "off",
        Mode::Warn => "warn",
        Mode::New => "new",
        Mode::Enforce => "enforce",
    }
}

/// The body of the build hook, writing cargo directives to `out`. `Err` carries
/// the report that must abort the build.
pub fn run_with(manifest_dir: &Path, package: &str, mode_value: Option<&str>, out: &mut dyn Write) -> io::Result<Result<(), String>> {
    writeln!(out, "cargo:rerun-if-env-changed={MODE_ENV}")?;
    let mode = match Mode::parse(mode_value) {
        Ok(mode) => mode,
        Err(message) => return Ok(Err(message)),
    };
    if mode == Mode::Off {
        return Ok(Ok(()));
    }
    match check_package(manifest_dir) {
        Ok(check) => emit(&check, mode, package, out),
        Err(error) if mode == Mode::Warn => {
            writeln!(out, "cargo:warning=contract governance skipped for {package}: {error}")?;
            Ok(Ok(()))
        }
        Err(error) => Ok(Err(format!("contract governance cannot verify {package}: {error}"))),
    }
}

/// Print the rerun directives and the warnings of a completed check.
fn emit(check: &PackageCheck, mode: Mode, package: &str, out: &mut dyn Write) -> io::Result<Result<(), String>> {
    for path in &check.rerun {
        writeln!(out, "cargo:rerun-if-changed={}", path.display())?;
    }
    match decide(mode, &check.report) {
        Decision::Silent => Ok(Ok(())),
        Decision::Warn(lines) => {
            for line in lines {
                writeln!(out, "cargo:warning={package}: {line}")?;
            }
            Ok(Ok(()))
        }
        Decision::Abort(report) => Ok(Err(report)),
    }
}

/// Entry point used by the macro: reads `TFQM_GOVERNANCE`, prints to stdout and
/// panics, failing the build, when the mode requires it. The panic is the
/// intended fail-closed behaviour of a build script, not an error path.
#[allow(clippy::panic)]
pub fn run(manifest_dir: &str, package: &str) {
    let mode = std::env::var(MODE_ENV).ok();
    let stdout = io::stdout();
    let mut lock = stdout.lock();
    match run_with(Path::new(manifest_dir), package, mode.as_deref(), &mut lock) {
        Ok(Ok(())) => {}
        Ok(Err(report)) => panic!("{report}"),
        Err(error) => panic!("contract governance could not write cargo directives: {error}"),
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
mod tests {
    use super::*;
    use crate::policy::BaselineEntry;
    use crate::tests::Repo;
    use std::fs;

    fn output(repo: &Repo, pkg: &str, mode: Option<&str>) -> (String, Result<(), String>) {
        let mut out = Vec::new();
        let result = run_with(&repo.root.join(pkg), "pkg", mode, &mut out).unwrap();
        (String::from_utf8(out).unwrap(), result)
    }

    #[test]
    fn modes_parse() {
        assert_eq!(Mode::parse(None), Ok(Mode::Warn));
        assert_eq!(Mode::parse(Some("")), Ok(Mode::Warn));
        assert_eq!(Mode::parse(Some(" enforce ")), Ok(Mode::Enforce));
        assert_eq!(Mode::parse(Some("new")), Ok(Mode::New));
        assert_eq!(Mode::parse(Some("off")), Ok(Mode::Off));
        assert!(Mode::parse(Some("strict")).unwrap_err().contains("off, warn, new, enforce"));
    }

    #[test]
    fn clean_package_emits_reruns_only() {
        let repo = Repo::new("bt-clean");
        repo.scored("code/rust/p/src/lib.rs", b"pub fn f() {}\n", "L4", "B");
        repo.write("code/rust/p/Cargo.toml", b"[package]\n");
        repo.write("code/rust/p/build.rs", b"fn main() {}\n");
        let (text, result) = output(&repo, "code/rust/p", Some("enforce"));
        assert_eq!(result, Ok(()));
        assert!(text.starts_with("cargo:rerun-if-env-changed=TFQM_GOVERNANCE\n"), "{text}");
        assert!(text.contains("governance"), "{text}");
        assert!(text.contains("lib.contract.score.yaml"), "{text}");
        assert!(text.contains("build.rs"), "{text}");
        assert!(!text.contains("cargo:warning"), "{text}");
        let watched = |text: &str, dir: &Path| text.lines().filter_map(|l| l.strip_prefix("cargo:rerun-if-changed=")).any(|p| Path::new(p) == dir);
        assert!(watched(&text, &repo.root.join("code/rust/p/src")), "source directory watched: {text}");
        assert!(watched(&text, &repo.root.join("code/rust/p")), "package directory watched: {text}");
        fs::create_dir_all(repo.root.join("code/rust/p/target")).unwrap();
        let (text, _) = output(&repo, "code/rust/p", Some("enforce"));
        assert!(!watched(&text, &repo.root.join("code/rust/p")), "a dir with target/ is not watched: {text}");
    }

    #[test]
    fn new_uncontracted_file_warns_by_default_and_aborts_when_enforced() {
        let repo = Repo::new("bt-new");
        repo.write("code/rust/p/Cargo.toml", b"[package]\n");
        repo.write("code/rust/p/src/lib.rs", b"pub fn f() {}\n");
        let (text, result) = output(&repo, "code/rust/p", None);
        assert_eq!(result, Ok(()));
        assert!(text.contains("cargo:warning=pkg: contract governance: checked 1: 0 pass, 0 grandfathered, 0 boilerplate, 1 failed"), "{text}");
        assert!(text.contains("cargo:warning=pkg: code/rust/p/src/lib.rs: [MISSING_COMPANION]"), "{text}");
        assert!(text.contains("lib.contract.score.yaml"), "the missing companion is watched: {text}");
        let (_, result) = output(&repo, "code/rust/p", Some("enforce"));
        let report = result.unwrap_err();
        assert!(report.contains("FAIL code/rust/p/src/lib.rs (new or not grandfathered)"), "{report}");
        let (_, result) = output(&repo, "code/rust/p", Some("new"));
        assert!(result.is_err());
        let (text, result) = output(&repo, "code/rust/p", Some("off"));
        assert_eq!((text.as_str(), result), ("cargo:rerun-if-env-changed=TFQM_GOVERNANCE\n", Ok(())));
        let (_, result) = output(&repo, "code/rust/p", Some("bogus"));
        assert!(result.unwrap_err().contains("bogus"));
    }

    #[test]
    fn new_mode_only_warns_for_changed_grandfathered_files() {
        let repo = Repo::new("bt-changed");
        repo.write("code/rust/p/Cargo.toml", b"[package]\n");
        repo.write("code/rust/p/src/lib.rs", b"pub fn f() {}\n");
        let mut baseline = Baseline::default();
        baseline.entries.insert("code/rust/p/src/lib.rs".into(), BaselineEntry { sha256: "e".repeat(64), deficit: "MISSING_COMPANION".into(), reason: None });
        fs::write(repo.root.join(BASELINE_PATH), baseline.to_json_text()).unwrap();
        let (text, result) = output(&repo, "code/rust/p", Some("new"));
        assert_eq!(result, Ok(()));
        assert!(text.contains("cargo:warning"), "{text}");
        assert!(output(&repo, "code/rust/p", Some("enforce")).1.is_err());
    }

    #[test]
    fn missing_or_broken_policy() {
        let dir = crate::repo::tests::scratch("bt-nopolicy");
        let mut out = Vec::new();
        assert_eq!(run_with(&dir, "pkg", None, &mut out).unwrap(), Ok(()));
        let text = String::from_utf8(out).unwrap();
        assert!(text.contains("cargo:warning=contract governance skipped for pkg: no governance/policy.json found above"), "{text}");
        let mut out = Vec::new();
        assert!(run_with(&dir, "pkg", Some("enforce"), &mut out).unwrap().unwrap_err().contains("cannot verify pkg"));
        assert!(matches!(check_package(&dir), Err(BuildError::NoPolicy(_))));
        fs::remove_dir_all(&dir).unwrap();
        let repo = Repo::new("bt-badpolicy");
        fs::write(repo.root.join(BASELINE_PATH), b"{").unwrap();
        let e = check_package(&repo.root).unwrap_err();
        assert!(matches!(e, BuildError::Policy(PolicyError::Json(_))));
        assert!(e.to_string().starts_with("governance data:"));
        fs::write(repo.root.join(BASELINE_PATH), Baseline::default().to_json_text()).unwrap();
        let e = check_package(&repo.root.join("absent")).unwrap_err();
        assert!(matches!(e, BuildError::Repo(_)), "{e}");
        assert!(e.to_string().starts_with("governance sources:"));
        fs::write(repo.root.join(POLICY_PATH), b"[]").unwrap();
        assert!(matches!(check_package(&repo.root), Err(BuildError::Policy(PolicyError::Field { .. }))));
    }

    #[test]
    fn new_mode_aborts_when_any_failure_is_new() {
        let repo = Repo::new("bt-mixed");
        let old = repo.write("code/old.rs", b"fn old() {}\n");
        repo.write("code/old.rs", b"fn old() { /* changed */ }\n");
        repo.write("code/new.rs", b"fn new() {}\n");
        let mut baseline = Baseline::default();
        baseline.entries.insert("code/old.rs".into(), BaselineEntry { sha256: old, deficit: "MISSING_COMPANION".into(), reason: None });
        let report = verify_paths(&repo.policy, &baseline, &repo.root, &["code/old.rs".to_owned(), "code/new.rs".to_owned()]);
        assert_eq!(report.failures().count(), 2);
        assert!(matches!(decide(Mode::New, &report), Decision::Abort(_)), "one new failure among others aborts");
        let only_changed = verify_paths(&repo.policy, &baseline, &repo.root, &["code/old.rs".to_owned()]);
        assert!(matches!(decide(Mode::New, &only_changed), Decision::Warn(_)));
    }

    #[test]
    fn decide_respects_mode() {
        assert_eq!(decide(Mode::Enforce, &Report::default()), Decision::Silent);
        let repo = Repo::new("bt-decide");
        repo.write("code/x.rs", b"fn x() {}\n");
        let report = verify_paths(&repo.policy, &Baseline::default(), &repo.root, &["code/x.rs".to_owned()]);
        assert_eq!(decide(Mode::Off, &report), Decision::Silent);
        assert!(matches!(decide(Mode::Warn, &report), Decision::Warn(lines) if lines.len() == 2));
        assert!(matches!(decide(Mode::New, &report), Decision::Abort(text) if text.contains("TFQM_GOVERNANCE=new")));
        assert!(matches!(decide(Mode::Enforce, &report), Decision::Abort(text) if text.contains("TFQM_GOVERNANCE=enforce")));
    }
}
