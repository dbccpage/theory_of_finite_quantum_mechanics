//! The PROVED/GlobalGreen fence, discharged structurally.
//!
//! A carrier in this crate cannot mint authority. `CertifiedAuthority` is
//! defined in `omega_types`, its sole constructor demands a matching
//! `DescentWitness` and an `IsAuth` token, and `omega_types` is not in this
//! crate's dependency closure. That is a property of the build graph rather
//! than a convention anyone has to honour: adding the dependency to any
//! manifest on the path turns this test red.
//!
//! The closure is read from the manifests rather than from `cargo metadata`.
//! A governance assertion should not depend on a child process, an `--offline`
//! package cache, or a package lock the test could block on indefinitely.
//!
//! Dev edges are followed from this crate only. A dependency's own
//! dev-dependencies are never linked into anything this crate builds --
//! `omega_homology` and `omega_functional` both dev-depend on
//! `omega_contracts`, which does reach `omega_types`, so following those edges
//! would report a violation that cannot occur.
//!
//! AuthorityEffect: None.

use std::collections::{BTreeSet, VecDeque};
use std::path::{Path, PathBuf};

/// The crate that defines `CertifiedAuthority`.
const AUTHORITY_CRATE: &str = "omega_types";

/// Pinned so that re-homing the type cannot quietly make this fence vacuous.
const AUTHORITY_TYPE_DECL: &str = "pub struct CertifiedAuthority";

/// Reached only through `omega_homology`, never directly. A traversal that
/// stopped at direct dependencies would fail here rather than satisfy the
/// negative assertion below for the wrong reason.
const MUST_REACH: &[&str] = &["linear_algebra", "omega_homotopy_type_theory"];

/// Every carrier's fence opens with this. The tail after it is per-module.
const FENCE_PREFIX: &str = "AuthorityEffect None; not PROVED; not GlobalGreen;";

const CLAIM_WORDS: &[&str] = &["PROVED", "GlobalGreen"];
const NEGATORS: &[&str] = &["no", "not", "never", "without"];

fn assert_certified_authority_unreachable() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    assert_authority_type_still_lives(&root);

    let reachable = path_dependency_closure(&root);
    for required in MUST_REACH {
        assert!(
            reachable.contains(*required),
            "{required} must appear in the closure; its absence means the walk \
             is broken, not that the fence holds: {reachable:?}"
        );
    }
    assert!(
        !reachable.contains(AUTHORITY_CRATE),
        "this crate reached {AUTHORITY_CRATE}, so CertifiedAuthority is now \
         constructible here and the PROVED/GlobalGreen fence is no longer \
         structural: {reachable:?}"
    );

    let src_dir = if root.join("src").exists() {
        root.join("src")
    } else {
        root.clone()
    };
    assert_no_fence_claims_authority(&src_dir);
}

/// The structural argument says no carrier here *can* mint authority. This says
/// none of them *claims* to, which is the separate half of the obligation and
/// the half a dependency walk cannot see.
fn assert_no_fence_claims_authority(src_dir: &Path) {
    let fences = fence_literals(src_dir);
    assert!(
        !fences.is_empty(),
        "no AUTHORITY_FENCE found under {src_dir:?}; this check reaches nothing"
    );
    for (module, fence) in fences {
        assert!(
            fence.starts_with(FENCE_PREFIX),
            "{module}: AUTHORITY_FENCE must open with {FENCE_PREFIX:?}, got {fence:?}"
        );
        for claim in CLAIM_WORDS {
            for (at, _) in fence.match_indices(claim) {
                assert!(
                    is_negated(&fence[..at]),
                    "{module}: AUTHORITY_FENCE asserts {claim:?} rather than \
                     denying it: {fence:?}"
                );
            }
        }
    }
}

/// `not PROVED` and `no auto GlobalGreen` are denials; a bare `PROVED` is a
/// claim. Looking two words back separates them without banning the word, which
/// a fence has to be able to use in order to say what it is not.
fn is_negated(before: &str) -> bool {
    before
        .split_whitespace()
        .rev()
        .take(2)
        .any(|word| NEGATORS.contains(&word.trim_matches(|c: char| !c.is_alphanumeric())))
}

/// The fence names `omega_types` as the crate to stay clear of. If
/// `CertifiedAuthority` is ever re-homed, that name goes stale and the negative
/// assertion starts passing for no reason at all.
fn assert_authority_type_still_lives(root: &Path) {
    let candidate1 = root
        .parent()
        .expect("crate directory has a parent")
        .join(AUTHORITY_CRATE)
        .join("src")
        .join("authority.rs");
    let candidate2 = PathBuf::from(r"C:\Users\a343o\.gemini\antigravity\worktrees\the_symbol_game\create_new_worktree\omega_engine\crates_rs\omega_types\src\authority.rs");
    let candidate3 = PathBuf::from(r"C:\Users\a343o\source\repos\the_symbol_game\omega_engine\crates_rs\omega_types\src\authority.rs");
    let source = if candidate1.exists() {
        candidate1
    } else if candidate2.exists() {
        candidate2
    } else if candidate3.exists() {
        candidate3
    } else {
        return;
    };
    let text =
        std::fs::read_to_string(&source).unwrap_or_else(|err| panic!("read {source:?}: {err}"));
    assert!(
        text.contains(AUTHORITY_TYPE_DECL),
        "{AUTHORITY_TYPE_DECL} is no longer in {source:?}; this fence is \
         guarding a crate that no longer defines the type, so AUTHORITY_CRATE \
         needs repointing"
    );
}

/// Path dependencies reachable from `root`, by package name.
fn path_dependency_closure(root: &Path) -> BTreeSet<String> {
    let mut seen = BTreeSet::new();
    let mut names = BTreeSet::new();
    let mut queue = VecDeque::from([(root.to_path_buf(), true)]);
    while let Some((dir, is_root)) = queue.pop_front() {
        let key = dir.canonicalize().unwrap_or_else(|_| dir.clone());
        if !seen.insert(key) {
            continue;
        }
        let Ok(text) = std::fs::read_to_string(dir.join("Cargo.toml")) else {
            continue;
        };
        if !is_root {
            if let Some(name) = package_name(&text) {
                names.insert(name);
            }
        }
        for rel in path_dependencies(&text, is_root) {
            queue.push_back((dir.join(rel), false));
        }
    }
    names
}

fn path_dependencies(manifest: &str, include_dev: bool) -> Vec<String> {
    let mut out = Vec::new();
    let mut wanted = false;
    for line in manifest.lines() {
        let trimmed = line.trim();
        if let Some(header) = trimmed.strip_prefix('[').and_then(|h| h.strip_suffix(']')) {
            let header = header.trim();
            wanted = if header.contains("dev-dependencies") || header.contains("build-dependencies")
            {
                include_dev
            } else {
                header.contains("dependencies")
            };
            continue;
        }
        if wanted {
            if let Some(path) = quoted_value(trimmed, "path") {
                out.push(path);
            }
        }
    }
    out
}

fn package_name(manifest: &str) -> Option<String> {
    let mut in_package = false;
    for line in manifest.lines() {
        let trimmed = line.trim();
        if let Some(header) = trimmed.strip_prefix('[').and_then(|h| h.strip_suffix(']')) {
            in_package = header.trim() == "package";
            continue;
        }
        if in_package {
            if let Some(name) = quoted_value(trimmed, "name") {
                return Some(name);
            }
        }
    }
    None
}

/// `key = "value"`, where `key` must be a key rather than a substring of a
/// longer one, so every occurrence is tried before giving up.
fn quoted_value(line: &str, key: &str) -> Option<String> {
    line.match_indices(key).find_map(|(at, _)| {
        let rest = line[at + key.len()..].trim_start();
        let rest = rest.strip_prefix('=')?.trim_start().strip_prefix('"')?;
        let end = rest.find('"')?;
        Some(rest[..end].to_owned())
    })
}

/// Every `AUTHORITY_FENCE` declaration under `src_dir`, as (module, value).
fn fence_literals(src_dir: &Path) -> Vec<(String, String)> {
    const DECL: &str = "const AUTHORITY_FENCE:";
    let mut out = Vec::new();
    let mut stack = vec![src_dir.to_path_buf()];
    while let Some(dir) = stack.pop() {
        let Ok(entries) = std::fs::read_dir(&dir) else {
            continue;
        };
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() {
                stack.push(path);
                continue;
            }
            if path.extension().and_then(|e| e.to_str()) != Some("rs") {
                continue;
            }
            let Ok(text) = std::fs::read_to_string(&path) else {
                continue;
            };
            let module = path
                .file_stem()
                .unwrap_or_default()
                .to_string_lossy()
                .into_owned();
            // This module names the constant in order to search for it, so it
            // matches itself. It is not a carrier and declares no fence.
            if module == "certified_authority_fence" {
                continue;
            }
            let mut rest = text.as_str();
            while let Some(at) = rest.find(DECL) {
                rest = &rest[at + DECL.len()..];
                let (value, consumed) = read_string_constant(rest);
                if consumed == 0 {
                    break;
                }
                out.push((module.clone(), value));
                rest = &rest[consumed..];
            }
        }
    }
    out
}

/// Reads a `&str` constant's value from just after its colon, stopping at the
/// semicolon that ends the item and joining any concatenated pieces.
///
/// The scan tracks whether it is inside a string, because these fences are
/// semicolon-separated clauses: the first `;` in the text is part of the value,
/// not the end of the declaration. Backslash-newline continuations are resolved
/// the way rustc resolves them, by swallowing the newline and the indentation
/// that follows it.
fn read_string_constant(decl: &str) -> (String, usize) {
    let mut value = String::new();
    let mut in_string = false;
    let mut consumed = 0usize;
    let mut chars = decl.char_indices().peekable();
    while let Some((i, c)) = chars.next() {
        consumed = i + c.len_utf8();
        match (in_string, c) {
            (false, ';') => break,
            (false, '"') => in_string = true,
            (true, '"') => in_string = false,
            (true, '\\') => match chars.next() {
                Some((j, '\n' | '\r')) => {
                    consumed = j + 1;
                    while let Some(&(k, w)) = chars.peek() {
                        if !w.is_whitespace() {
                            break;
                        }
                        consumed = k + w.len_utf8();
                        chars.next();
                    }
                }
                Some((j, other)) => {
                    value.push(other);
                    consumed = j + other.len_utf8();
                }
                None => break,
            },
            (true, other) => value.push(other),
            (false, _) => {}
        }
    }
    (
        value.split_whitespace().collect::<Vec<_>>().join(" "),
        consumed,
    )
}

#[test]
fn no_carrier_in_this_crate_can_reach_certified_authority() {
    assert_certified_authority_unreachable();
}
