//! `governance-check`: repository-wide contract governance for Rust, Python and Lean.
//!
//! ```text
//! governance-check [--root DIR] check [--changed-since REF]
//! governance-check [--root DIR] baseline [--write] [--initial | --allow-add --reason TEXT]
//! governance-check [--root DIR] explain PATH
//! governance-check [--root DIR] list
//! ```
//!
//! Exit status: 0 clean, 1 violations, 2 usage or configuration error. Cost: linear in the
//! bytes of the sources checked (about 20 s for the full population in a debug build).

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic, clippy::arithmetic_side_effects)]

use std::collections::BTreeSet;
use std::path::PathBuf;
use std::process::ExitCode;

use governance::policy::{BASELINE_PATH, POLICY_PATH};
use governance::repo;
use governance::{
    verify_file, verify_paths, ArtifactKindSpec, Baseline, BaselineEntry, BindingVerifier, CompletenessVerifier, Context, ContractDescriptor,
    FloorVerifier, Outcome, Policy, SchemaVerifier, SourceFile, Verifier,
};

const USAGE: &str = "usage: governance-check [--root DIR] (check [--changed-since REF] | baseline [--write] [--initial | --allow-add --reason TEXT] | explain PATH | list)";

/// A parsed command line.
#[derive(Debug, Clone, PartialEq, Eq)]
enum Command {
    Check { changed_since: Option<String> },
    Baseline { write: bool, initial: bool, reason: Option<String> },
    Explain { path: String },
    List,
}

/// A failure that ends the run with status 2.
type Fatal = String;

fn parse_args(args: &[String]) -> Result<(Option<PathBuf>, Command), Fatal> {
    let (root, rest) = split_root(args)?;
    let (name, options) = rest.split_first().ok_or(USAGE)?;
    Ok((root, command_of(name, options)?))
}

/// Take `--root DIR` out of the arguments, wherever it appears.
fn split_root(args: &[String]) -> Result<(Option<PathBuf>, Vec<&str>), Fatal> {
    let mut root = None;
    let mut rest = Vec::new();
    let mut iter = args.iter();
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "--root" => root = Some(PathBuf::from(iter.next().ok_or("--root needs a directory")?)),
            other => rest.push(other),
        }
    }
    Ok((root, rest))
}

fn command_of(name: &str, options: &[&str]) -> Result<Command, Fatal> {
    match name {
        "check" => {
            only_known(options, &["--changed-since"])?;
            Ok(Command::Check { changed_since: value_of(options, "--changed-since")? })
        }
        "baseline" => baseline_command(options),
        "explain" => match options {
            [path] if !path.starts_with("--") => Ok(Command::Explain { path: path.replace('\\', "/") }),
            _ => Err("explain takes exactly one path".into()),
        },
        "list" if options.is_empty() => Ok(Command::List),
        _ => Err(USAGE.into()),
    }
}

fn only_known(options: &[&str], known: &[&str]) -> Result<(), Fatal> {
    match options.iter().find(|o| o.starts_with("--") && !known.contains(o)) {
        Some(bad) => Err(format!("unknown option {bad}")),
        None => Ok(()),
    }
}

fn baseline_command(options: &[&str]) -> Result<Command, Fatal> {
    only_known(options, &["--write", "--initial", "--allow-add", "--reason"])?;
    let reason = value_of(options, "--reason")?;
    if options.contains(&"--allow-add") != reason.is_some() {
        return Err("--allow-add and --reason TEXT must be given together".into());
    }
    Ok(Command::Baseline { write: options.contains(&"--write"), initial: options.contains(&"--initial"), reason })
}

fn value_of(options: &[&str], flag: &str) -> Result<Option<String>, Fatal> {
    match options.iter().position(|o| *o == flag) {
        None => Ok(None),
        Some(at) => match at.checked_add(1).and_then(|next| options.get(next)) {
            Some(value) if !value.starts_with("--") => Ok(Some((*value).to_owned())),
            _ => Err(format!("{flag} needs a value")),
        },
    }
}

struct Repo {
    root: PathBuf,
    policy: Policy,
    baseline: Baseline,
}

fn open(root: Option<PathBuf>, need_baseline: bool) -> Result<Repo, Fatal> {
    let root = match root {
        Some(root) => root,
        None => {
            let here = std::env::current_dir().map_err(|e| e.to_string())?;
            repo::find_root(&here).ok_or_else(|| format!("no {POLICY_PATH} above {}", here.display()))?
        }
    };
    let policy = Policy::load(&root.join(POLICY_PATH)).map_err(|e| format!("{POLICY_PATH}: {e}"))?;
    let baseline_file = root.join(BASELINE_PATH);
    let baseline = if baseline_file.is_file() || need_baseline {
        Baseline::load(&baseline_file).map_err(|e| format!("{BASELINE_PATH}: {e}"))?
    } else {
        Baseline::default()
    };
    Ok(Repo { root, policy, baseline })
}

/// Sources to verify for a set of changed paths: changed sources, and the sources
/// of changed companions. A change to the policy or baseline selects everything.
fn affected_sources(r: &Repo, changed: &[String]) -> Result<Vec<String>, Fatal> {
    if changed.iter().any(|p| p == POLICY_PATH || p == BASELINE_PATH) {
        return repo::population(&r.root, &r.policy).map_err(|e| e.to_string());
    }
    let mut out = BTreeSet::new();
    for path in changed {
        if r.policy.spec_for(path).is_some() && r.root.join(path).is_file() {
            out.insert(path.clone());
        } else if let Some(base) = path.strip_suffix(&r.policy.companion.suffix) {
            out.extend(sources_of_companion(r, path, base));
        }
    }
    Ok(out.into_iter().collect())
}

fn sources_of_companion(r: &Repo, companion: &str, base: &str) -> Vec<String> {
    let mut candidates = vec![base.to_owned()];
    candidates.extend(r.policy.companion.collision_suffixes.iter().map(|s| format!("{base}{s}")));
    candidates
        .into_iter()
        .filter(|c| r.policy.spec_for(c).is_some() && r.root.join(c).is_file())
        .filter(|c| r.policy.companion_path(c, |p| r.root.join(p).is_file()) == companion)
        .collect()
}

/// Baseline entries added (or re-pinned to new bytes) since `base` without a reason.
fn baseline_growth(r: &Repo, base: &str) -> Result<Vec<String>, Fatal> {
    let old = match repo::show_at(&r.root, base, BASELINE_PATH).map_err(|e| e.to_string())? {
        Some(text) => Baseline::from_json(&text).map_err(|e| format!("{BASELINE_PATH} at {base}: {e}"))?,
        None => {
            println!("note: no {BASELINE_PATH} at {base}; this change introduces the baseline");
            return Ok(Vec::new());
        }
    };
    let (problems, notes) = growth(&old, &r.baseline);
    for note in notes {
        println!("note: baseline entry added with reason: {note}");
    }
    Ok(problems)
}

/// Entries of `new` that are absent from `old` or pinned to other bytes: without a
/// reason they are problems, with one they are notes.
fn growth(old: &Baseline, new: &Baseline) -> (Vec<String>, Vec<String>) {
    let grown = new.entries.iter().filter(|(path, entry)| old.entries.get(*path).is_none_or(|prior| prior.sha256 != entry.sha256));
    let (with_reason, without): (Vec<_>, Vec<_>) = grown.partition(|(_, entry)| entry.reason.is_some());
    let problems = without.into_iter().map(|(path, _)| format!("{BASELINE_PATH}: [BASELINE_GROWTH] {path}: added without a reason")).collect();
    let notes = with_reason.into_iter().map(|(path, entry)| format!("{path}: {}", entry.reason.as_deref().unwrap_or_default())).collect();
    (problems, notes)
}

fn cmd_check(r: &Repo, changed_since: Option<&str>) -> Result<bool, Fatal> {
    let (paths, growth) = match changed_since {
        Some(reference) => {
            let base = repo::merge_base(&r.root, reference).map_err(|e| e.to_string())?;
            let changed = repo::changed_since(&r.root, reference).map_err(|e| e.to_string())?;
            println!("changed since {reference} ({base}): {} paths", changed.len());
            (affected_sources(r, &changed)?, baseline_growth(r, &base)?)
        }
        None => (repo::population(&r.root, &r.policy).map_err(|e| e.to_string())?, Vec::new()),
    };
    let report = verify_paths(&r.policy, &r.baseline, &r.root, &paths);
    print!("{report}");
    for problem in &growth {
        println!("{problem}");
    }
    let stale = stale_entries(r);
    if stale > 0 {
        println!("note: {stale} baseline entries name deleted files; `governance-check baseline --write` removes them");
    }
    Ok(report.is_clean() && growth.is_empty())
}

/// Baseline entries whose file no longer exists.
fn stale_entries(r: &Repo) -> usize {
    r.baseline.entries.keys().filter(|p| !r.root.join(p).is_file()).count()
}

fn cmd_baseline(r: &Repo, write: bool, initial: bool, reason: Option<&str>) -> Result<bool, Fatal> {
    if initial && (r.root.join(BASELINE_PATH).is_file() || reason.is_some()) {
        return Err("--initial only creates a missing baseline, without --allow-add".into());
    }
    let paths = repo::population(&r.root, &r.policy).map_err(|e| e.to_string())?;
    let plan = plan_baseline(r, &paths, initial || reason.is_some(), reason);
    println!(
        "baseline: {} entries ({} kept, {} added, {} removed); {} failing files not added",
        plan.next.entries.len(),
        plan.kept,
        plan.added,
        plan.removed,
        plan.refused.len()
    );
    for path in &plan.refused {
        println!("  not grandfathered: {path}");
    }
    if write {
        std::fs::write(r.root.join(BASELINE_PATH), plan.next.to_json_text()).map_err(|e| format!("{BASELINE_PATH}: {e}"))?;
        println!("wrote {BASELINE_PATH}");
    }
    Ok(true)
}

/// The recomputed baseline and how it differs from the current one.
#[derive(Debug, Default, PartialEq, Eq)]
struct BaselinePlan {
    next: Baseline,
    kept: usize,
    added: usize,
    removed: usize,
    refused: Vec<String>,
}

/// Keep failing files listed with unchanged bytes; add other failing files only
/// when `may_add`; everything else (passing, deleted or changed) leaves the list.
fn plan_baseline(r: &Repo, paths: &[String], may_add: bool, reason: Option<&str>) -> BaselinePlan {
    let raw = verify_paths(&r.policy, &Baseline::default(), &r.root, paths);
    let mut plan = BaselinePlan::default();
    for file in raw.failures() {
        let (Some(sha256), Some(first)) = (file.sha256.clone(), file.violations().first()) else { continue };
        let deficit = first.rule().code().to_owned();
        let path = file.path.clone();
        match r.baseline.entries.get(&path) {
            Some(old) if old.sha256 == sha256 => {
                plan.kept = plan.kept.saturating_add(1);
                plan.next.entries.insert(path, BaselineEntry { deficit, ..old.clone() });
            }
            _ if may_add => {
                plan.added = plan.added.saturating_add(1);
                plan.next.entries.insert(path, BaselineEntry { sha256, deficit, reason: reason.map(str::to_owned) });
            }
            _ => plan.refused.push(path),
        }
    }
    plan.removed = r.baseline.entries.keys().filter(|p| !plan.next.entries.contains_key(*p)).count();
    plan
}

fn cmd_explain(r: &Repo, path: &str) -> Result<bool, Fatal> {
    let spec = r.policy.spec_for(path).ok_or_else(|| format!("{path} is in no governed population of {POLICY_PATH}"))?;
    let file = verify_file(&r.policy, &r.baseline, &r.root, path).ok_or("not governed")?;
    let companion = r.policy.companion_path(path, |p| r.root.join(p).is_file());
    println!("source:    {path} ({:?}, {})", spec.kind(), spec.language());
    println!("sha256:    {}", file.sha256.as_deref().unwrap_or("unreadable"));
    println!("companion: {companion}{}", if r.root.join(&companion).is_file() { "" } else { " (missing)" });
    println!("baseline:  {:?}", file.baseline);
    if let (Some(sha256), Ok(text)) = (file.sha256.clone(), std::fs::read_to_string(r.root.join(&companion))) {
        explain_descriptor(r, path, &sha256, &companion, &text, spec.kind(), spec.language());
    }
    let ok = !file.failed();
    match &file.outcome {
        Outcome::Pass(token) => println!("outcome:   PASS {token}"),
        Outcome::Grandfathered => println!("outcome:   GRANDFATHERED (unchanged since the baseline)"),
        Outcome::Boilerplate => println!("outcome:   PINNED BOILERPLATE"),
        Outcome::Fail(violations) => {
            println!("outcome:   FAIL");
            for v in violations {
                println!("  {v}");
            }
        }
    }
    Ok(ok)
}

fn explain_descriptor(r: &Repo, path: &str, sha256: &str, companion: &str, text: &str, kind: governance::ArtifactKind, language: &str) {
    let d = match ContractDescriptor::parse(companion, text) {
        Ok(d) => d,
        Err(v) => return println!("descriptor: {v}"),
    };
    println!("contract:  {} ({} symbols, {} owned invariants)", d.contract_urn.as_deref().unwrap_or("no URN"), d.symbols.len(), d.owned_invariants.len());
    let token = d.token().ok().flatten().map_or_else(|| "none".to_owned(), |t| t.to_string());
    println!("token:     {token}");
    let source = SourceFile { rel_path: path.to_owned(), sha256: sha256.to_owned(), kind, language: language.to_owned(), companion: companion.to_owned() };
    let ctx = Context { policy: &r.policy, baseline: &r.baseline, source: &source };
    let verifiers: [&dyn Verifier; 4] = [&SchemaVerifier, &BindingVerifier, &CompletenessVerifier, &FloorVerifier];
    for verifier in verifiers {
        match verifier.verify(&ctx, &d) {
            Ok(()) => println!("  {:<12} ok", verifier.name()),
            Err(v) => println!("  {:<12} {v}", verifier.name()),
        }
    }
}


fn cmd_list(r: &Repo) -> Result<bool, Fatal> {
    for path in repo::population(&r.root, &r.policy).map_err(|e| e.to_string())? {
        println!("{path}");
    }
    Ok(true)
}

fn run(args: &[String]) -> Result<bool, Fatal> {
    let (root, command) = parse_args(args)?;
    let needs_baseline = !matches!(command, Command::Baseline { initial: true, .. } | Command::List);
    let r = open(root, needs_baseline)?;
    match command {
        Command::Check { changed_since } => cmd_check(&r, changed_since.as_deref()),
        Command::Baseline { write, initial, reason } => cmd_baseline(&r, write, initial, reason.as_deref()),
        Command::Explain { path } => cmd_explain(&r, &path),
        Command::List => cmd_list(&r),
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match run(&args) {
        Ok(true) => ExitCode::SUCCESS,
        Ok(false) => ExitCode::from(1),
        Err(message) => {
            eprintln!("governance-check: {message}");
            ExitCode::from(2)
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
mod tests {
    use super::*;

    fn args(text: &str) -> Vec<String> {
        text.split_whitespace().map(String::from).collect()
    }

    #[test]
    fn parses_commands() {
        assert_eq!(parse_args(&args("check")).unwrap(), (None, Command::Check { changed_since: None }));
        assert_eq!(
            parse_args(&args("--root /r check --changed-since origin/main")).unwrap(),
            (Some(PathBuf::from("/r")), Command::Check { changed_since: Some("origin/main".into()) })
        );
        assert_eq!(parse_args(&args("baseline")).unwrap().1, Command::Baseline { write: false, initial: false, reason: None });
        assert_eq!(
            parse_args(&args("baseline --write --allow-add --reason because")).unwrap().1,
            Command::Baseline { write: true, initial: false, reason: Some("because".into()) }
        );
        assert_eq!(parse_args(&args("baseline --write --initial")).unwrap().1, Command::Baseline { write: true, initial: true, reason: None });
        assert_eq!(parse_args(&args("explain code\\a.rs")).unwrap().1, Command::Explain { path: "code/a.rs".into() });
        assert_eq!(parse_args(&args("list")).unwrap().1, Command::List);
    }

    #[test]
    fn rejects_bad_command_lines() {
        for bad in ["", "frobnicate", "list extra", "explain", "explain a b", "explain --x", "check --changed-since", "check --changed-since --x",
                    "check --bogus", "baseline --allow-add", "baseline --reason x", "baseline --bogus", "--root"] {
            assert!(parse_args(&args(bad)).is_err(), "{bad:?}");
        }
    }

    use governance::descriptor::hex;
    use serde_json::json;
    use sha2::{Digest, Sha256};
    use std::fs;
    use std::path::Path;
    use std::process::Command as Proc;

    const POLICY: &str = r#"{"schema_version": "tfqm.governance-policy.v1",
      "level_order": ["L1","L2","L3","L4","L5"], "grade_order": ["E","D","C","B","A","A+"],
      "floor": {"min_level": "L4", "min_grade": "D"},
      "companion": {"suffix": ".contract.score.yaml", "document_schema": "tfqm.contract-score.v1", "score_schema": "2.0.0", "collision_suffixes": [".py", ".rs", ".lean"]},
      "populations": [{"kind": "rust", "language": "Rust", "globs": ["code/**/*.rs"]}, {"kind": "python", "language": "Python", "globs": ["code/**/*.py"]}],
      "exclusions": {"path_parts": ["target"], "path_globs": []},
      "pinned_boilerplate": [], "enforcement": {"env": "TFQM_GOVERNANCE"}}"#;

    struct Tmp(PathBuf);

    impl Drop for Tmp {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }

    fn tmp(tag: &str) -> Tmp {
        let dir = std::env::temp_dir().join(format!("tfqm-gov-bin-{}-{tag}", std::process::id()));
        let _ = fs::remove_dir_all(&dir);
        fs::create_dir_all(dir.join("governance")).unwrap();
        fs::write(dir.join(POLICY_PATH), POLICY).unwrap();
        fs::write(dir.join(BASELINE_PATH), Baseline::default().to_json_text()).unwrap();
        Tmp(dir)
    }

    fn write(root: &Path, rel: &str, bytes: &[u8]) -> String {
        let path = root.join(rel);
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        fs::write(&path, bytes).unwrap();
        hex(&Sha256::digest(bytes))
    }

    /// A source with a completed L4C companion.
    fn scored(root: &Path, rel: &str, companion: &str) {
        let sha = write(root, rel, format!("// {rel}\n").as_bytes());
        let gates = json!({"G1": "C", "G2": "C", "G3": "C", "G4": "C", "G5": "C"});
        write(root, companion, companion_doc(rel, &sha, gates, true).as_bytes());
    }

    /// A companion whose contract and score bind `sha`, with the given gates.
    fn companion_doc(rel: &str, sha: &str, gates: serde_json::Value, complete: bool) -> String {
        let artifact = json!({"path": rel, "sha256": sha, "language": "Rust"});
        let contract = json!({"artifact": artifact, "contract_urn": "urn:t"});
        let (composite, token) = if complete { (json!("C"), json!("L4C")) } else { (json!(null), json!(null)) };
        let score = json!({"schema_version": "2.0.0", "artifact": artifact, "level": "L4", "gates": gates,
                           "composite_grade": composite, "score_token": token, "is_complete": complete});
        let entry = |r: &serde_json::Value| {
            let raw = r.to_string();
            json!({"sha256": hex(&Sha256::digest(raw.as_bytes())), "bytes": raw.len(), "record": r, "raw_utf8": raw, "original_paths": []})
        };
        let (c, s) = (entry(&contract), entry(&score));
        json!({"schema_version": "tfqm.contract-score.v1", "artifact": rel, "contract": contract, "current_contract": c["sha256"],
               "current_scoring": s["sha256"], "contract_history": [c], "scoring_history": [s]})
        .to_string()
    }

    fn git(root: &Path, args: &[&str]) {
        let ok = Proc::new("git")
            .arg("-C")
            .arg(root)
            .args(["-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"])
            .args(args)
            .status()
            .unwrap();
        assert!(ok.success(), "git {args:?}");
    }

    #[test]
    fn affected_sources_maps_companions_back_to_sources() {
        let t = tmp("affected");
        scored(&t.0, "code/a.rs", "code/a.contract.score.yaml");
        write(&t.0, "code/m.py", b"x = 1\n");
        scored(&t.0, "code/m.rs", "code/m.rs.contract.score.yaml");
        let r = open(Some(t.0.clone()), true).unwrap();
        let changed: Vec<String> = ["code/a.contract.score.yaml", "code/m.rs.contract.score.yaml", "README.md", "code/gone.rs", "code/m.py"].map(String::from).to_vec();
        assert_eq!(affected_sources(&r, &changed).unwrap(), ["code/a.rs", "code/m.py", "code/m.rs"]);
        // The unqualified name is not m.rs's companion while a twin m.py exists.
        assert!(sources_of_companion(&r, "code/m.contract.score.yaml", "code/m").is_empty());
        assert!(cmd_explain(&r, "code/a.rs").unwrap());
        assert!(!cmd_explain(&r, "code/m.py").unwrap());
        assert!(cmd_explain(&r, "README.md").is_err());
    }

    #[test]
    fn baseline_growth_needs_a_reason() {
        let mut old = Baseline::default();
        let entry = |sha: &str, reason: Option<&str>| BaselineEntry { sha256: sha.repeat(64), deficit: "SCHEMA".into(), reason: reason.map(String::from) };
        old.entries.insert("code/a.rs".into(), entry("a", None));
        let mut new = old.clone();
        assert_eq!(growth(&old, &new), (vec![], vec![]));
        new.entries.insert("code/b.rs".into(), entry("b", None));
        new.entries.insert("code/c.rs".into(), entry("c", Some("agreed")));
        new.entries.insert("code/a.rs".into(), entry("d", None));
        let (problems, notes) = growth(&old, &new);
        assert_eq!(problems.len(), 2, "{problems:?}");
        assert!(problems.iter().all(|p| p.contains("[BASELINE_GROWTH]")));
        assert_eq!(notes, ["code/c.rs: agreed"]);
        new.entries.remove("code/b.rs");
        new.entries.insert("code/a.rs".into(), entry("a", None));
        assert!(growth(&old, &new).0.is_empty(), "removal is never growth");
    }

    #[test]
    fn baseline_plan_only_shrinks_without_allow_add() {
        let t = tmp("plan");
        let legacy = write(&t.0, "code/legacy.rs", b"// old\n");
        write(&t.0, "code/changed.rs", b"// changed\n");
        write(&t.0, "code/new.rs", b"// new\n");
        scored(&t.0, "code/fixed.rs", "code/fixed.contract.score.yaml");
        let mut baseline = Baseline::default();
        baseline.entries.insert("code/legacy.rs".into(), BaselineEntry { sha256: legacy, deficit: "X".into(), reason: Some("kept".into()) });
        baseline.entries.insert("code/changed.rs".into(), BaselineEntry { sha256: "0".repeat(64), deficit: "X".into(), reason: None });
        baseline.entries.insert("code/fixed.rs".into(), BaselineEntry { sha256: "1".repeat(64), deficit: "X".into(), reason: None });
        baseline.entries.insert("code/deleted.rs".into(), BaselineEntry { sha256: "2".repeat(64), deficit: "X".into(), reason: None });
        fs::write(t.0.join(BASELINE_PATH), baseline.to_json_text()).unwrap();
        let r = open(Some(t.0.clone()), true).unwrap();
        let paths: Vec<String> = ["code/changed.rs", "code/fixed.rs", "code/legacy.rs", "code/new.rs"].map(String::from).to_vec();
        let plan = plan_baseline(&r, &paths, false, None);
        assert_eq!(plan.next.entries.keys().collect::<Vec<_>>(), ["code/legacy.rs"]);
        let kept = plan.next.entries.get("code/legacy.rs").unwrap();
        assert_eq!((kept.deficit.as_str(), kept.reason.as_deref()), ("MISSING_COMPANION", Some("kept")));
        assert_eq!((plan.kept, plan.added, plan.removed), (1, 0, 3));
        assert_eq!(plan.refused, ["code/changed.rs", "code/new.rs"]);
        let plan = plan_baseline(&r, &paths, true, Some("why"));
        assert_eq!((plan.kept, plan.added, plan.removed), (1, 2, 2));
        assert_eq!(plan.next.entries.get("code/new.rs").unwrap().reason.as_deref(), Some("why"));
        assert!(plan.refused.is_empty());
    }

    #[test]
    fn end_to_end_with_git() {
        let t = tmp("e2e");
        scored(&t.0, "code/a.rs", "code/a.contract.score.yaml");
        git(&t.0, &["init", "-q", "-b", "main"]);
        git(&t.0, &["add", "-A"]);
        git(&t.0, &["commit", "-q", "-m", "base"]);
        let root = t.0.display().to_string();
        let run_cmd = |text: &str| run(&args(&format!("--root {root} {text}")));
        assert_eq!(run_cmd("check"), Ok(true));
        assert_eq!(run_cmd("check --changed-since main"), Ok(true));
        assert_eq!(run_cmd("list"), Ok(true));
        write(&t.0, "code/new.rs", b"// new\n");
        assert_eq!(run_cmd("check --changed-since main"), Ok(false), "a new uncontracted file fails");
        assert_eq!(run_cmd("check"), Ok(false));
        assert_eq!(run_cmd("baseline"), Ok(true), "a dry run never fails");
        assert_eq!(run_cmd("baseline --write --allow-add --reason test"), Ok(true));
        assert_eq!(run_cmd("check"), Ok(true), "grandfathered now");
        assert_eq!(run_cmd("check --changed-since main"), Ok(true), "the added entry has a reason");
        let mut b = Baseline::load(&t.0.join(BASELINE_PATH)).unwrap();
        b.entries.values_mut().for_each(|e| e.reason = None);
        fs::write(t.0.join(BASELINE_PATH), b.to_json_text()).unwrap();
        assert_eq!(run_cmd("check --changed-since main"), Ok(false), "growth without a reason fails");
        assert!(run_cmd("baseline --initial").is_err(), "--initial refuses to overwrite");
        assert!(run_cmd("check --changed-since no-such-ref").is_err());
    }

    #[test]
    fn open_needs_a_baseline_only_when_asked() {
        let t = tmp("open");
        fs::remove_file(t.0.join(BASELINE_PATH)).unwrap();
        git(&t.0, &["init", "-q", "-b", "main"]);
        assert!(open(Some(t.0.clone()), true).is_err(), "check and explain need the baseline");
        assert!(open(Some(t.0.clone()), false).unwrap().baseline.entries.is_empty());
        let root = t.0.display().to_string();
        let e = run(&args(&format!("--root {root} check"))).unwrap_err();
        assert!(e.contains(BASELINE_PATH), "{e}");
        assert_eq!(run(&args(&format!("--root {root} list"))), Ok(true), "list needs no baseline");
        let e = run(&args(&format!("--root {root} baseline --initial --allow-add --reason x"))).unwrap_err();
        assert!(e.contains("--initial"), "--initial takes no reason: {e}");
        assert_eq!(run(&args(&format!("--root {root} baseline --initial"))), Ok(true), "--initial without a baseline file is allowed");
    }

    #[test]
    fn baseline_deficit_is_the_first_violation_and_stale_entries_are_counted() {
        let t = tmp("deficit");
        let sha = write(&t.0, "code/d.rs", b"// d\n");
        // Bound to other bytes (BINDING) and with an unassessed gate (COMPLETENESS).
        let gates = json!({"G1": "C", "G2": null, "G3": "C", "G4": "C", "G5": "C"});
        write(&t.0, "code/d.contract.score.yaml", companion_doc("code/d.rs", &"0".repeat(64), gates, false).as_bytes());
        let mut baseline = Baseline::default();
        baseline.entries.insert("code/gone.rs".into(), BaselineEntry { sha256: "1".repeat(64), deficit: "X".into(), reason: None });
        baseline.entries.insert("code/d.rs".into(), BaselineEntry { sha256: sha, deficit: "X".into(), reason: None });
        fs::write(t.0.join(BASELINE_PATH), baseline.to_json_text()).unwrap();
        let r = open(Some(t.0.clone()), true).unwrap();
        assert_eq!(stale_entries(&r), 1, "only code/gone.rs is missing");
        let mut only_live = r.baseline.clone();
        only_live.entries.remove("code/gone.rs");
        assert_eq!(stale_entries(&Repo { root: t.0.clone(), policy: r.policy.clone(), baseline: only_live }), 0);
        let plan = plan_baseline(&r, &["code/d.rs".to_owned()], false, None);
        assert_eq!(plan.next.entries.get("code/d.rs").unwrap().deficit, "BINDING", "first of [BINDING, COMPLETENESS]");
    }

    #[test]
    fn a_policy_or_baseline_change_selects_the_whole_population() {
        let t = tmp("whole");
        scored(&t.0, "code/a.rs", "code/a.contract.score.yaml");
        write(&t.0, "code/b.py", b"x = 1\n");
        git(&t.0, &["init", "-q", "-b", "main"]);
        let r = open(Some(t.0.clone()), true).unwrap();
        for changed in [POLICY_PATH, BASELINE_PATH] {
            let with_other = [changed.to_owned(), "docs/readme.md".to_owned()];
            assert_eq!(affected_sources(&r, &with_other).unwrap(), ["code/a.rs", "code/b.py"], "{changed}");
        }
        assert!(affected_sources(&r, &["docs/readme.md".to_owned()]).unwrap().is_empty());
        assert_eq!(run(&args(&format!("--root {} list", t.0.display()))), Ok(true));
    }

    #[test]
    fn missing_root_is_fatal() {
        let dir = std::env::temp_dir().join(format!("tfqm-gov-cli-{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let e = run(&["--root".into(), dir.display().to_string(), "check".into()]).err().unwrap();
        assert!(e.contains(POLICY_PATH), "{e}");
        std::fs::remove_dir_all(&dir).unwrap();
    }
}
