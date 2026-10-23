//! Repository access: locating the root, hashing files, discovering the source
//! population through git, the files changed since a reference, and the
//! sources of one cargo package for build scripts.
//!
//! Cost: linear in the number of listed paths (git output) or package files (directory walk);
//! hashing is linear in file size. Each git call is bounded by [`GIT_TIMEOUT`].

use std::fmt;
use std::fs;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::{Command, Output, Stdio};
use std::thread::{self, JoinHandle};
use std::time::{Duration, Instant};

use sha2::{Digest, Sha256};

use super::descriptor::hex;
use super::policy::{Policy, POLICY_PATH};

/// A failure to read the repository. Fields name the path or git command and the
/// underlying message.
#[allow(missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RepoError {
    /// A file or directory could not be read.
    Io { path: String, message: String },
    /// A git command failed, timed out or could not start.
    Git { command: String, message: String },
    /// Git reported a path or text that is not UTF-8 (shown lossily).
    NonUtf8(String),
}

impl fmt::Display for RepoError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RepoError::Io { path, message } => write!(f, "cannot read {path}: {message}"),
            RepoError::Git { command, message } => write!(f, "git {command} failed: {message}"),
            RepoError::NonUtf8(text) => write!(f, "not UTF-8: {text}"),
        }
    }
}

impl std::error::Error for RepoError {}

fn io_error(path: &Path, error: &std::io::Error) -> RepoError {
    RepoError::Io { path: path.display().to_string(), message: error.to_string() }
}

/// SHA-256 of a file's bytes, as lower-case hex.
pub fn sha256_file(path: &Path) -> Result<String, RepoError> {
    let bytes = fs::read(path).map_err(|e| io_error(path, &e))?;
    Ok(hex(&Sha256::digest(&bytes)))
}

/// The nearest ancestor of `start` (inclusive) that holds `governance/policy.json`.
pub fn find_root(start: &Path) -> Option<PathBuf> {
    start.ancestors().find(|dir| dir.join(POLICY_PATH).is_file()).map(Path::to_path_buf)
}

/// `path` relative to `root` with `/` separators, if it lies inside `root`.
pub fn rel_posix(root: &Path, path: &Path) -> Option<String> {
    let rel = path.strip_prefix(root).ok()?;
    let parts: Option<Vec<&str>> = rel.components().map(|c| c.as_os_str().to_str()).collect();
    parts.map(|p| p.join("/")).filter(|s| !s.is_empty())
}

/// Upper bound on one git command. All commands used here are local and read-only.
pub const GIT_TIMEOUT: Duration = Duration::from_secs(300);

/// Run `git -C root args` with no stdin, no terminal prompt and a deadline. At the
/// deadline git itself is killed; a process git started (an alias, a hook) is not.
fn run_git(root: &Path, args: &[&str], timeout: Duration) -> Result<Output, RepoError> {
    let command = args.join(" ");
    let fail = |message: String| RepoError::Git { command: command.clone(), message };
    let mut child = Command::new("git")
        .arg("-C")
        .arg(root)
        .args(args)
        .env("GIT_TERMINAL_PROMPT", "0")
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| fail(e.to_string()))?;
    let stdout = child.stdout.take().map(drain);
    let stderr = child.stderr.take().map(drain);
    let deadline = Instant::now().checked_add(timeout).ok_or_else(|| fail("timeout out of range".into()))?;
    let status = loop {
        if let Some(status) = child.try_wait().map_err(|e| fail(e.to_string()))? {
            break status;
        }
        if Instant::now() >= deadline {
            let _ = child.kill();
            let _ = child.wait();
            return Err(fail(format!("timed out after {} s", timeout.as_secs())));
        }
        thread::sleep(Duration::from_millis(2));
    };
    Ok(Output { status, stdout: collect(stdout), stderr: collect(stderr) })
}

/// Read a pipe to its end on a separate thread, so a full pipe cannot block the child.
fn drain(mut pipe: impl Read + Send + 'static) -> JoinHandle<Vec<u8>> {
    thread::spawn(move || {
        let mut bytes = Vec::new();
        let _ = pipe.read_to_end(&mut bytes);
        bytes
    })
}

fn collect(handle: Option<JoinHandle<Vec<u8>>>) -> Vec<u8> {
    handle.and_then(|h| h.join().ok()).unwrap_or_default()
}

fn git(root: &Path, args: &[&str]) -> Result<Vec<u8>, RepoError> {
    let output = run_git(root, args, GIT_TIMEOUT)?;
    if output.status.success() {
        Ok(output.stdout)
    } else {
        Err(RepoError::Git { command: args.join(" "), message: String::from_utf8_lossy(&output.stderr).trim().to_owned() })
    }
}

fn utf8(bytes: &[u8]) -> Result<String, RepoError> {
    String::from_utf8(bytes.to_vec()).map_err(|_| RepoError::NonUtf8(String::from_utf8_lossy(bytes).into_owned()))
}

/// NUL-separated git output as `/`-separated paths; a non-UTF-8 path is an error,
/// never a silently altered name.
fn nul_separated(bytes: &[u8]) -> Result<Vec<String>, RepoError> {
    bytes.split(|b| *b == 0).filter(|s| !s.is_empty()).map(|s| utf8(s).map(|p| p.replace('\\', "/"))).collect()
}

/// Tracked and ordinary untracked files that belong to a policy population and
/// exist on disk, sorted. This is the same discovery rule as
/// `scripts/score_scope_contracts.py`.
pub fn population(root: &Path, policy: &Policy) -> Result<Vec<String>, RepoError> {
    let listed = git(root, &["ls-files", "--cached", "--others", "--exclude-standard", "-z"])?;
    let mut paths: Vec<String> =
        nul_separated(&listed)?.into_iter().filter(|p| policy.spec_for(p).is_some() && root.join(p).is_file()).collect();
    paths.sort();
    paths.dedup();
    Ok(paths)
}

/// The merge base of `reference` and `HEAD`.
pub fn merge_base(root: &Path, reference: &str) -> Result<String, RepoError> {
    let out = git(root, &["merge-base", reference, "HEAD"])?;
    Ok(utf8(&out)?.trim().to_owned())
}

/// Paths changed between the merge base of `reference` and the working tree,
/// plus untracked files, sorted and deduplicated. Deleted paths are included.
pub fn changed_since(root: &Path, reference: &str) -> Result<Vec<String>, RepoError> {
    let base = merge_base(root, reference)?;
    let mut paths = nul_separated(&git(root, &["diff", "--name-only", "--no-renames", "-z", &base])?)?;
    paths.extend(nul_separated(&git(root, &["ls-files", "--others", "--exclude-standard", "-z"])?)?);
    paths.sort();
    paths.dedup();
    Ok(paths)
}

/// The text of `path` at revision `rev`, or `None` when it does not exist there.
pub fn show_at(root: &Path, rev: &str, path: &str) -> Result<Option<String>, RepoError> {
    let spec = format!("{rev}:{path}");
    if !run_git(root, &["cat-file", "-e", &spec], GIT_TIMEOUT)?.status.success() {
        return Ok(None);
    }
    utf8(&git(root, &["show", &spec])?).map(Some)
}

/// The `.rs` files of the cargo package at `manifest_dir`: everything under it
/// except nested packages (directories with their own `Cargo.toml`) and `target`.
pub fn package_sources(manifest_dir: &Path) -> Result<Vec<PathBuf>, RepoError> {
    let mut found = Vec::new();
    let mut pending = vec![manifest_dir.to_path_buf()];
    while let Some(dir) = pending.pop() {
        for path in entries_of(&dir)? {
            match classify(&path) {
                Entry::Descend => pending.push(path),
                Entry::Source => found.push(path),
                Entry::Skip => ()
            }
        }
    }
    found.sort();
    Ok(found)
}

enum Entry {
    Descend,
    Source,
    Skip,
}

/// Directories are descended unless they are a nested package, `target` or `.git`.
fn classify(path: &Path) -> Entry {
    let skipped_dir = path.join("Cargo.toml").is_file() || path.file_name().is_some_and(|n| n == "target" || n == ".git");
    match (path.is_dir(), skipped_dir) {
        (true, false) => Entry::Descend,
        (true, true) => Entry::Skip,
        (false, _) if path.extension().is_some_and(|e| e == "rs") => Entry::Source,
        (false, _) => Entry::Skip,
    }
}

fn entries_of(dir: &Path) -> Result<Vec<PathBuf>, RepoError> {
    fs::read_dir(dir)
        .map_err(|e| io_error(dir, &e))?
        .map(|entry| entry.map(|e| e.path()).map_err(|e| io_error(dir, &e)))
        .collect()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
pub(crate) mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};

    static NEXT: AtomicUsize = AtomicUsize::new(0);

    /// A fresh empty directory under the system temp dir.
    pub(crate) fn scratch(tag: &str) -> PathBuf {
        let n = NEXT.fetch_add(1, Ordering::SeqCst);
        let dir = std::env::temp_dir().join(format!("tfqm-gov-{}-{tag}-{n}", std::process::id()));
        let _ = fs::remove_dir_all(&dir);
        fs::create_dir_all(&dir).unwrap();
        dir
    }

    #[test]
    fn hashing_and_relative_paths() {
        let dir = scratch("hash");
        let file = dir.join("a.txt");
        fs::write(&file, b"abc").unwrap();
        assert_eq!(sha256_file(&file).unwrap(), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
        assert!(matches!(sha256_file(&dir.join("missing")), Err(RepoError::Io { .. })));
        assert_eq!(rel_posix(&dir, &dir.join("x").join("y.rs")).as_deref(), Some("x/y.rs"));
        assert_eq!(rel_posix(&dir, &dir), None);
        assert_eq!(rel_posix(&dir.join("x"), &dir), None);
        fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn root_is_found_upwards() {
        let dir = scratch("root");
        fs::create_dir_all(dir.join("governance")).unwrap();
        fs::write(dir.join(POLICY_PATH), b"{}").unwrap();
        let deep = dir.join("code").join("rust");
        fs::create_dir_all(&deep).unwrap();
        assert_eq!(find_root(&deep), Some(dir.clone()));
        assert_eq!(find_root(&std::env::temp_dir().join("tfqm-gov-no-such-root")), None);
        fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn package_sources_skip_nested_packages_and_target() {
        let dir = scratch("pkg");
        for p in ["src/lib.rs", "src/m/n.rs", "build.rs", "target/debug/x.rs", "src/inner/Cargo.toml", "src/inner/lib.rs", "src/notes.md"] {
            let path = dir.join(p);
            fs::create_dir_all(path.parent().unwrap()).unwrap();
            fs::write(path, b"").unwrap();
        }
        let found: Vec<String> = package_sources(&dir).unwrap().iter().map(|p| rel_posix(&dir, p).unwrap()).collect();
        assert_eq!(found, ["build.rs", "src/lib.rs", "src/m/n.rs"]);
        assert!(matches!(package_sources(&dir.join("absent")), Err(RepoError::Io { .. })));
        fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn git_errors_are_typed() {
        let dir = scratch("nogit");
        let e = merge_base(&dir, "no-such-ref").unwrap_err();
        assert!(matches!(&e, RepoError::Git { command, .. } if command.starts_with("merge-base")), "{e}");
        assert!(e.to_string().starts_with("git merge-base"));
        fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn nul_lists_normalise_separators_and_refuse_non_utf8() {
        assert_eq!(nul_separated(b"a\\b.rs\0c.py\0\0").unwrap(), ["a/b.rs", "c.py"]);
        assert!(nul_separated(b"").unwrap().is_empty());
        let e = nul_separated(b"ok.rs\0bad\xff.rs\0").unwrap_err();
        assert!(matches!(&e, RepoError::NonUtf8(text) if text.starts_with("bad")), "{e}");
        assert!(e.to_string().starts_with("not UTF-8"));
    }

    fn git_ok(root: &Path, args: &[&str]) {
        let mut full = vec!["-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"];
        full.extend_from_slice(args);
        git(root, &full).unwrap();
    }

    #[test]
    fn git_population_changes_and_history() {
        let dir = scratch("git");
        let policy = crate::policy::tests::policy();
        for (p, body) in [("code/a.rs", "a"), ("code/b.py", "b"), ("docs/x.md", "x"), ("code/gone.rs", "g")] {
            let path = dir.join(p);
            fs::create_dir_all(path.parent().unwrap()).unwrap();
            fs::write(path, body).unwrap();
        }
        git_ok(&dir, &["init", "-q", "-b", "main"]);
        git_ok(&dir, &["add", "-A"]);
        git_ok(&dir, &["commit", "-q", "-m", "base"]);
        fs::remove_file(dir.join("code/gone.rs")).unwrap();
        fs::write(dir.join("code/new.rs"), "n").unwrap();
        fs::write(dir.join("code/a.rs"), "a2").unwrap();
        assert_eq!(population(&dir, &policy).unwrap(), ["code/a.rs", "code/b.py", "code/new.rs"], "governed, existing files only");
        assert_eq!(changed_since(&dir, "main").unwrap(), ["code/a.rs", "code/gone.rs", "code/new.rs"]);
        assert_eq!(merge_base(&dir, "main").unwrap().len(), 40);
        assert_eq!(show_at(&dir, "main", "code/a.rs").unwrap().as_deref(), Some("a"));
        assert_eq!(show_at(&dir, "main", "code/new.rs").unwrap(), None);
        // A git alias that sleeps (run by git's own shell) must hit the deadline.
        let started = Instant::now();
        let slow = run_git(&dir, &["-c", "alias.nap=!sleep 1", "nap"], Duration::from_millis(50));
        assert!(matches!(&slow, Err(RepoError::Git { message, .. }) if message.contains("timed out")), "{slow:?}");
        assert!(started.elapsed() < Duration::from_secs(15), "the child is killed at the deadline");
        assert!(matches!(git(&dir, &["no-such-subcommand"]), Err(RepoError::Git { .. })));
        // This API promises to kill git itself, not a shell launched by an alias.
        // Own the test's deliberate one-second grandchild instead of leaking a
        // twenty-second sleeper (and inherited log handles) into the next test run.
        thread::sleep(Duration::from_millis(1200));
        fs::remove_dir_all(&dir).unwrap();
    }
}
