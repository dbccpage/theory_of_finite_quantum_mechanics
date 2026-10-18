//! The PROVED/GlobalGreen fence, discharged structurally.
//!
//! A carrier in this crate cannot mint authority. `CertifiedAuthority` is
//! defined in `omega_types`, and its sole constructor demands a matching
//! `DescentWitness` and an `IsAuth` token. Code here can only call what it can
//! name, and it can name `CertifiedAuthority` only if this crate depends on
//! `omega_types` directly, or if some crate on its dependency path publicly
//! re-exports the type, the `authority` module or the crate root. This test
//! forbids both, so the property belongs to the build graph and the sources it
//! compiles, not to a convention anyone has to honour.
//!
//! Until 2026-09-28 the fence forbade `omega_types` anywhere in the dependency
//! closure. The crate now depends on `omega_solvers`, whose exact weighted-`L1`
//! solver proposes the `Phi1` certificates that `omega_functional` replays, and
//! `omega_solvers` depends on `omega_types` for its own diagnostics. The closure
//! condition could no longer hold, so it was narrowed to what it protected:
//! `omega_types` is linked but never nameable. A direct dependency on it, or a
//! new public re-export that exposes the type, still turns this test red. The
//! test keeps its name because contract bindings cite it.
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

use std::collections::{BTreeMap, BTreeSet, VecDeque};
use std::path::{Path, PathBuf};

/// The crate that defines `CertifiedAuthority`.
const AUTHORITY_CRATE: &str = "omega_types";

/// The type no carrier here may name, and the module that holds it.
const AUTHORITY_TYPE: &str = "CertifiedAuthority";
const AUTHORITY_MODULE: &str = "authority";

/// A public re-export from `AUTHORITY_CRATE` that the scan must find, so that
/// a scanner which reads nothing cannot pass for a clean closure.
const MUST_SEE_REEXPORT: (&str, &str) = ("omega_solvers", "MAX_DETECTOR_SAFE_MAGNITUDE");

/// Pinned so that re-homing the type cannot quietly make this fence vacuous.
const AUTHORITY_TYPE_DECL: &str = "pub struct CertifiedAuthority";

/// Reached only through `omega_functional`, never directly. A traversal that
/// stopped at direct dependencies would fail here rather than satisfy the
/// negative assertion below for the wrong reason.
const MUST_REACH: &[&str] = &["omega_kernel"];

/// Every carrier's fence opens with this. The tail after it is per-module.
const FENCE_PREFIX: &str = "AuthorityEffect None; not PROVED; not GlobalGreen;";

const CLAIM_WORDS: &[&str] = &["PROVED", "GlobalGreen"];
const NEGATORS: &[&str] = &["no", "not", "never", "without"];

fn assert_certified_authority_unreachable(root: &Path) {
    assert_authority_type_still_lives();

    let reachable = path_dependency_closure(&root);
    for required in MUST_REACH {
        assert!(
            reachable.contains_key(*required),
            "{required} must appear in the closure; its absence means the walk \
             is broken, not that the fence holds: {:?}",
            reachable.keys()
        );
    }

    let direct = direct_dependency_names(&root);
    assert!(
        !direct.iter().any(|name| name == AUTHORITY_CRATE),
        "this crate depends on {AUTHORITY_CRATE} directly, so CertifiedAuthority \
         is nameable here and the PROVED/GlobalGreen fence is no longer \
         structural: {direct:?}"
    );

    let reexports = authority_reexports(&reachable);
    let (sentinel_crate, sentinel_item) = MUST_SEE_REEXPORT;
    assert!(
        reexports
            .iter()
            .any(|(krate, item)| krate == sentinel_crate && item.contains(sentinel_item)),
        "the re-export scan did not find {sentinel_crate}'s {sentinel_item}; the \
         scan is broken, not clean: {reexports:?}"
    );
    for (krate, item) in &reexports {
        assert!(
            !exposes_authority(item),
            "{krate} publicly exposes `{item}`, which makes {AUTHORITY_TYPE} \
             nameable from this crate"
        );
    }

    assert_no_fence_claims_authority(&root.join("src"));
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
fn assert_authority_type_still_lives() {
    let source = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../../omega_engine/crates_rs/omega_types/src/authority.rs");
    let text =
        std::fs::read_to_string(&source).unwrap_or_else(|err| panic!("read {source:?}: {err}"));
    assert!(
        text.contains(AUTHORITY_TYPE_DECL),
        "{AUTHORITY_TYPE_DECL} is no longer in {source:?}; this fence is \
         guarding a crate that no longer defines the type, so AUTHORITY_CRATE \
         needs repointing"
    );
}

/// Package names of this crate's own path dependencies, in every section.
fn direct_dependency_names(root: &Path) -> Vec<String> {
    let manifest = std::fs::read_to_string(root.join("Cargo.toml")).expect("read root manifest");
    let mut in_dependencies = false;
    let mut names = Vec::new();
    for line in manifest.lines() {
        let line = line.trim();
        if line.starts_with('[') {
            in_dependencies = line.contains("dependencies");
            continue;
        }
        if in_dependencies && !line.starts_with('#') {
            if let Some((name, _)) = line.split_once('=') {
                names.push(quoted_value(line, "package").unwrap_or_else(|| name.trim().to_owned()));
            }
        }
    }
    names
}

/// Every public `use`, `extern crate` or `type` item in the closure's sources,
/// outside the authority crate itself, that names the authority crate or type,
/// as (crate, whitespace-normalized item).
fn authority_reexports(closure: &BTreeMap<String, PathBuf>) -> Vec<(String, String)> {
    let mut out = Vec::new();
    for (name, dir) in closure {
        if name == AUTHORITY_CRATE {
            continue;
        }
        let mut stack = vec![dir.join("src")];
        while let Some(path) = stack.pop() {
            let Ok(entries) = std::fs::read_dir(&path) else {
                continue;
            };
            for entry in entries.flatten() {
                let file = entry.path();
                if file.is_dir() {
                    stack.push(file);
                    continue;
                }
                if file.extension().and_then(|e| e.to_str()) != Some("rs") {
                    continue;
                }
                let Ok(text) = std::fs::read_to_string(&file) else {
                    continue;
                };
                for item in public_items(&text) {
                    if names_word(&item, AUTHORITY_CRATE) || item.contains(AUTHORITY_TYPE) {
                        out.push((name.clone(), item));
                    }
                }
            }
        }
    }
    out
}

/// `pub use ...;`, `pub extern crate ...;` and `pub type ...;` items, each read
/// up to its semicolon and whitespace-normalized.
fn public_items(text: &str) -> Vec<String> {
    let mut out = Vec::new();
    for keyword in ["pub use ", "pub extern crate ", "pub type "] {
        let mut rest = text;
        while let Some(at) = rest.find(keyword) {
            let tail = &rest[at..];
            let end = tail.find(';').map_or(tail.len(), |e| e + 1);
            out.push(tail[..end].split_whitespace().collect::<Vec<_>>().join(" "));
            rest = &tail[end..];
        }
    }
    out
}

fn is_ident_char(c: char) -> bool {
    c.is_alphanumeric() || c == '_'
}

/// Whether `word` occurs in `text` as a whole identifier.
fn names_word(text: &str, word: &str) -> bool {
    text.match_indices(word).any(|(at, _)| {
        let before = text[..at].chars().next_back();
        let after = text[at + word.len()..].chars().next();
        !before.is_some_and(is_ident_char) && !after.is_some_and(is_ident_char)
    })
}

/// A public item exposes the authority type when it names the type, or when it
/// re-exports the authority crate's root, a glob of it, or its `authority`
/// module. Named items such as constants or diagnostics are fine.
fn exposes_authority(item: &str) -> bool {
    if item.contains(AUTHORITY_TYPE) {
        return true;
    }
    item.match_indices(AUTHORITY_CRATE).any(|(at, _)| {
        let after = &item[at + AUTHORITY_CRATE.len()..];
        if item[..at].chars().next_back().is_some_and(is_ident_char)
            || after.chars().next().is_some_and(is_ident_char)
        {
            return false;
        }
        let Some(path) = after.strip_prefix("::") else {
            // The crate root itself: `pub use omega_types;`, `... as x;`.
            return true;
        };
        path.split(|c: char| matches!(c, '{' | '}' | ',' | ';') || c.is_whitespace())
            .filter(|token| !token.is_empty() && !token.ends_with("::"))
            .any(|token| {
                let leaf = token.rsplit("::").next().unwrap_or(token);
                leaf == "*" || leaf == "self" || leaf == AUTHORITY_MODULE
            })
    })
}

/// Path dependencies reachable from `root`, by package name, with directories.
fn path_dependency_closure(root: &Path) -> BTreeMap<String, PathBuf> {
    let mut seen = BTreeSet::new();
    let mut names = BTreeMap::new();
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
                names.insert(name, dir.clone());
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
    let native = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    assert_certified_authority_unreachable(&native);
    assert_certified_authority_unreachable(
        &native.join("../../../omega_engine/crates_rs/omega_quantum_physics"),
    );
}

#[test]
fn the_exposure_rule_separates_named_items_from_the_authority_surface() {
    for exposing in [
        "pub use omega_types::CertifiedAuthority;",
        "pub use omega_types::*;",
        "pub use omega_types;",
        "pub extern crate omega_types;",
        "pub use omega_types as types;",
        "pub use omega_types::authority;",
        "pub use omega_types::authority::{self, AuthorityEffect};",
        "pub use omega_types::{prime, authority};",
        "pub type Minted = CertifiedAuthority;",
    ] {
        assert!(
            exposes_authority(exposing),
            "{exposing} should expose the type"
        );
    }
    for named in [
        "pub use omega_types::{ DETECTOR_CAPACITY_COMPARISON_TOLERANCE, MAX_DETECTOR_SAFE_MAGNITUDE, };",
        "pub use omega_types::authority::AuthorityEffect;",
        "pub use omega_types::prime::CanContinueResult;",
        "pub use omega_types_extra::*;",
    ] {
        assert!(!exposes_authority(named), "{named} names items only");
    }
    assert!(names_word("pub use omega_types::X;", AUTHORITY_CRATE));
    assert!(!names_word(
        "pub use omega_types_extra::X;",
        AUTHORITY_CRATE
    ));

    // A dev-dependency on the authority crate is a direct edge the walk sees.
    let manifest = "[package]\nname = \"x\"\n[dev-dependencies]\nomega_types = { path = \"../omega_types\" }\n";
    assert_eq!(
        path_dependencies(manifest, true),
        vec!["../omega_types".to_owned()]
    );
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let types_manifest = std::fs::read_to_string(
        root.join("../../../omega_engine/crates_rs/omega_types/Cargo.toml"),
    )
    .expect("read the authority crate's manifest");
    assert_eq!(
        package_name(&types_manifest).as_deref(),
        Some(AUTHORITY_CRATE)
    );
}
