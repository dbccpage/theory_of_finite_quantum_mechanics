//! Lean 4 Source Scanner and Axiom Audit Engine (U17).
//!
//! Provides lexer-level source scanning for forbidden constructs (skipping comments and strings)
//! and parsed axiom policy auditing against `#print axioms` output.
//! AuthorityEffect: None.

use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const LEAN_SCAN_REPORT_SCHEMA: &str = "omega.symbol_game.lean_scan_report.v1";
pub const LEAN_VERIFICATION_RECEIPT_SCHEMA: &str = "omega.symbol_game.lean_verification_receipt.v1";

pub const DEFAULT_AXIOM_POLICY: &[&str] = &["propext", "Quot.sound"];

pub const DEFAULT_FORBIDDEN_CONSTRUCTS: &[&str] = &[
    // Kernel / soundness escapes.
    "sorry",
    "admit",
    "axiom",
    "unsafe",
    "partial",
    "implemented_by",
    "extern",
    "debug.skipKernelTC",
    // Metaprogramming surface that can register a command/term elaborator, a macro, or
    // new syntax, and thereby forge the `#print axioms` output this audit reads back.
    // Confirmed candidate bypass: an `elab_rules : command` shadowing `#print axioms`
    // prints a clean axiom line (`[propext, Quot.sound]`) while the real proof depends
    // on `Classical.choice`. Re-parsing the captured stdout cannot distinguish the two,
    // so the only sound source-level defence is to refuse the registration surface. A
    // proof of the required declarations never needs any of these. Each `_`-joined name
    // is listed in full because the lexer treats `_` as a word character, so banning
    // `elab` does not cover `elab_rules`, nor `command_elab` cover `builtin_command_elab`.
    "elab",
    "elab_rules",
    "macro",
    "macro_rules",
    "syntax",
    "declare_syntax_cat",
    "run_cmd",
    "initialize",
    "builtin_initialize",
    "command_elab",
    "term_elab",
    "builtin_command_elab",
    "builtin_term_elab",
];

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SourceFinding {
    pub file: String,
    pub line: usize,
    pub construct: String,
    pub snippet: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SourceFileEntry {
    pub file: String,
    pub content: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LeanScanRequest {
    pub sources: Vec<SourceFileEntry>,
    #[serde(default)]
    pub forbidden_constructs: Vec<String>,
    /// Judge-owned identifiers (e.g. a trusted-prelude namespace prefix) that a candidate
    /// source must never write. Attack A names only host-owned symbols in the obligation
    /// statement; the candidate cannot legitimately define or extend that namespace, so any
    /// whole-word occurrence (including a `.`-qualified head like `JudgePrelude.enc`) in a
    /// non-harness source is a shadow attempt and a finding. Default empty keeps older
    /// callers unchanged.
    #[serde(default)]
    pub reserved_identifiers: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct LeanScanReport {
    pub schema_version: String,
    pub authority_effect: String,
    pub findings: Vec<SourceFinding>,
    pub clean: bool,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct LeanAuditRequest {
    pub axioms_output: String,
    #[serde(default)]
    pub policy: Vec<String>,
    #[serde(default)]
    pub required_declarations: Vec<String>,
    #[serde(default)]
    pub build_success: bool,
    #[serde(default)]
    pub harness_elaborated: bool,
    #[serde(default)]
    pub forbidden_findings: Vec<SourceFinding>,
    /// Kernel-extracted axiom census per declaration (e.g. from `lean4checker` over the
    /// compiled `.olean`), independent of the `#print axioms` stdout. When present it is the
    /// authority: the parsed stdout is cross-checked against it, and any declaration whose
    /// text census differs from its kernel census is a forgery (B1) and fails closed. Policy
    /// is then enforced against the kernel census, not the re-parsed text. `None` keeps the
    /// legacy text-only path for callers that have no kernel extractor wired yet.
    #[serde(default)]
    pub kernel_axiom_census: Option<BTreeMap<String, Vec<String>>>,
    /// When true, a missing `kernel_axiom_census` fails closed instead of falling back to the
    /// text-only path. Lets an operator pin the stronger gate once the extractor is available.
    #[serde(default)]
    pub require_kernel_census: bool,
    /// Per-declaration verdict of the independent second checker (c041): the obligation `P` is
    /// re-elaborated in a clean file with no candidate import, and the submission constant's
    /// proved type is required to equal that clean type. `true` means equal. This closes Attack
    /// A, where the obligation statement named candidate-authored symbols so a nominally strong
    /// statement was trivially true. `None` keeps the legacy path (the harness still forces the
    /// term to the written statement, but the written statement's meaning is not clean-pinned).
    #[serde(default)]
    pub type_equality_by_declaration: Option<BTreeMap<String, bool>>,
    /// When true, a missing or incomplete `type_equality_by_declaration` fails closed.
    #[serde(default)]
    pub require_type_equality: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct LeanVerificationReceipt {
    pub schema_version: String,
    pub authority_effect: String,
    pub status: String, // "PASS" or "FAIL"
    pub build_success: bool,
    pub harness_elaborated: bool,
    pub axioms_by_declaration: BTreeMap<String, Vec<String>>,
    pub forbidden_findings: Vec<SourceFinding>,
    pub refusal_code: Option<String>,
    pub details: Option<String>,
}

/// Scan Lean 4 source files for forbidden constructs outside comments and strings.
///
/// `reserved` names judge-owned identifiers a candidate source must not write (Attack A
/// trusted-prelude ownership); pass an empty slice to disable that check.
pub fn scan_lean_sources(
    sources: &[SourceFileEntry],
    forbidden: &[String],
    reserved: &[String],
) -> LeanScanReport {
    let forbidden_list: Vec<&str> = if forbidden.is_empty() {
        DEFAULT_FORBIDDEN_CONSTRUCTS.to_vec()
    } else {
        forbidden.iter().map(|s| s.as_str()).collect()
    };
    let reserved_list: Vec<&str> = reserved.iter().map(|s| s.as_str()).collect();

    let mut findings = Vec::new();

    for entry in sources {
        scan_single_file(
            &entry.file,
            &entry.content,
            &forbidden_list,
            &reserved_list,
            &mut findings,
        );
    }

    findings.sort_by(|a, b| a.file.cmp(&b.file).then_with(|| a.line.cmp(&b.line)));

    let clean = findings.is_empty();
    LeanScanReport {
        schema_version: LEAN_SCAN_REPORT_SCHEMA.to_string(),
        authority_effect: "None".to_string(),
        findings,
        clean,
    }
}

fn scan_single_file(
    file: &str,
    content: &str,
    forbidden: &[&str],
    reserved: &[&str],
    findings: &mut Vec<SourceFinding>,
) {
    let mut chars = content.chars().peekable();
    let mut line = 1usize;
    let mut comment_depth = 0usize;
    let mut in_string = false;
    let mut in_line_comment = false;

    // Filtered code stream: (char, line_number)
    let mut code_stream: Vec<(char, usize)> = Vec::with_capacity(content.len());

    while let Some(c) = chars.next() {
        if in_line_comment {
            if c == '\n' {
                in_line_comment = false;
                line += 1;
                code_stream.push((' ', line));
            }
            continue;
        }

        if in_string {
            if c == '\\' {
                // Escaped char inside string
                if let Some(next_c) = chars.next() {
                    if next_c == '\n' {
                        line += 1;
                    }
                }
            } else if c == '"' {
                in_string = false;
            } else if c == '\n' {
                line += 1;
            }
            continue;
        }

        if comment_depth > 0 {
            if c == '/' && chars.peek() == Some(&'-') {
                chars.next();
                comment_depth += 1;
            } else if c == '-' && chars.peek() == Some(&'/') {
                chars.next();
                comment_depth -= 1;
            } else if c == '\n' {
                line += 1;
            }
            continue;
        }

        // Outside comments and strings
        if c == '-' && chars.peek() == Some(&'-') {
            chars.next();
            in_line_comment = true;
        } else if c == '/' && chars.peek() == Some(&'-') {
            chars.next();
            comment_depth = 1;
        } else if c == '"' {
            in_string = true;
        } else {
            if c == '\n' {
                line += 1;
            }
            code_stream.push((c, line));
        }
    }

    if code_stream.is_empty() {
        return;
    }

    let code_chars: Vec<char> = code_stream.iter().map(|(c, _)| *c).collect();
    let code_lines: Vec<usize> = code_stream.iter().map(|(_, l)| *l).collect();

    for &kw in forbidden {
        let kw_chars: Vec<char> = kw.chars().collect();
        let kw_len = kw_chars.len();
        if kw_len > code_chars.len() {
            continue;
        }

        for i in 0..=(code_chars.len() - kw_len) {
            if &code_chars[i..i + kw_len] == kw_chars.as_slice() {
                // Check word boundaries
                let prev_ok = if i == 0 {
                    true
                } else {
                    let prev = code_chars[i - 1];
                    !prev.is_alphanumeric() && prev != '_' && prev != '.'
                };

                let next_ok = if i + kw_len == code_chars.len() {
                    true
                } else {
                    let next = code_chars[i + kw_len];
                    !next.is_alphanumeric() && next != '_' && next != '.'
                };

                if prev_ok && next_ok {
                    let occurrence_line = code_lines[i];
                    // Build short snippet
                    let start = i.saturating_sub(15);
                    let end = (i + kw_len + 15).min(code_chars.len());
                    let snippet: String = code_chars[start..end].iter().collect();

                    findings.push(SourceFinding {
                        file: file.to_string(),
                        line: occurrence_line,
                        construct: kw.to_string(),
                        snippet: snippet.trim().to_string(),
                    });
                }
            }
        }
    }

    // Reserved judge-owned identifiers. The trailing boundary is `.`-permissive so a
    // namespace head (`JudgePrelude.enc`, `JudgePrelude.Target`) is caught, not only the
    // bare name: the candidate must not write the reserved namespace in any form. The
    // leading boundary is the same as forbidden tokens, so `MyJudgePrelude` does not match.
    for &name in reserved {
        let name_chars: Vec<char> = name.chars().collect();
        let name_len = name_chars.len();
        if name_len == 0 || name_len > code_chars.len() {
            continue;
        }
        for i in 0..=(code_chars.len() - name_len) {
            if &code_chars[i..i + name_len] == name_chars.as_slice() {
                let prev_ok = if i == 0 {
                    true
                } else {
                    let prev = code_chars[i - 1];
                    !prev.is_alphanumeric() && prev != '_' && prev != '.'
                };
                let next_ok = if i + name_len == code_chars.len() {
                    true
                } else {
                    let next = code_chars[i + name_len];
                    // `.` permitted: a qualified head is still a reference to the namespace.
                    (!next.is_alphanumeric() && next != '_') || next == '.'
                };
                if prev_ok && next_ok {
                    let occurrence_line = code_lines[i];
                    let start = i.saturating_sub(15);
                    let end = (i + name_len + 15).min(code_chars.len());
                    let snippet: String = code_chars[start..end].iter().collect();
                    findings.push(SourceFinding {
                        file: file.to_string(),
                        line: occurrence_line,
                        construct: format!("reserved:{name}"),
                        snippet: snippet.trim().to_string(),
                    });
                }
            }
        }
    }
}

/// Parse the text output of `#print axioms` in Lean 4.
pub fn parse_print_axioms(output: &str) -> BTreeMap<String, Vec<String>> {
    let mut map = BTreeMap::new();

    // Look for lines like:
    // 'decl_name' depends on axioms: [axiom1, axiom2]
    // 'decl_name' does not depend on any axioms
    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }

        if let Some(idx) = trimmed.find("does not depend on any axioms") {
            let prefix = trimmed[..idx].trim();
            if let Some(decl) = extract_decl_name(prefix) {
                map.insert(decl, Vec::new());
            }
        } else if let Some(idx) = trimmed.find("depends on axioms: [") {
            let prefix = trimmed[..idx].trim();
            if let Some(decl) = extract_decl_name(prefix) {
                let rest = &trimmed[idx + "depends on axioms: [".len()..];
                if let Some(end_bracket) = rest.find(']') {
                    let axioms_str = &rest[..end_bracket];
                    let axioms: Vec<String> = axioms_str
                        .split(',')
                        .map(|s| s.trim().to_string())
                        .filter(|s| !s.is_empty())
                        .collect();
                    map.insert(decl, axioms);
                }
            }
        }
    }

    map
}

fn extract_decl_name(s: &str) -> Option<String> {
    let s = s.trim();
    // Usually enclosed in quotes: 'decl_name' or decl_name
    if let Some(start) = s.rfind('\'') {
        let before = &s[..start];
        if let Some(first_quote) = before.rfind('\'') {
            return Some(before[first_quote + 1..].to_string());
        }
    }
    // Fallback: last word
    s.split_whitespace()
        .last()
        .map(|w| w.trim_matches('\'').to_string())
}

/// Run total audit over Lean verification components.
pub fn audit_lean_verification(req: &LeanAuditRequest) -> LeanVerificationReceipt {
    let axioms_by_decl = parse_print_axioms(&req.axioms_output);

    let allowed_axioms: BTreeSet<&str> = if req.policy.is_empty() {
        DEFAULT_AXIOM_POLICY.iter().cloned().collect()
    } else {
        req.policy.iter().map(|s| s.as_str()).collect()
    };

    if !req.build_success {
        return LeanVerificationReceipt {
            schema_version: LEAN_VERIFICATION_RECEIPT_SCHEMA.to_string(),
            authority_effect: "None".to_string(),
            status: "FAIL".to_string(),
            build_success: false,
            harness_elaborated: req.harness_elaborated,
            axioms_by_declaration: axioms_by_decl,
            forbidden_findings: req.forbidden_findings.clone(),
            refusal_code: Some("BUILD_FAILED".to_string()),
            details: Some("Lake package build failed".to_string()),
        };
    }

    if !req.harness_elaborated {
        return LeanVerificationReceipt {
            schema_version: LEAN_VERIFICATION_RECEIPT_SCHEMA.to_string(),
            authority_effect: "None".to_string(),
            status: "FAIL".to_string(),
            build_success: true,
            harness_elaborated: false,
            axioms_by_declaration: axioms_by_decl,
            forbidden_findings: req.forbidden_findings.clone(),
            refusal_code: Some("HARNESS_ELABORATION_FAILED".to_string()),
            details: Some("Verify.lean failed to elaborate against hidden statement".to_string()),
        };
    }

    if !req.forbidden_findings.is_empty() {
        return LeanVerificationReceipt {
            schema_version: LEAN_VERIFICATION_RECEIPT_SCHEMA.to_string(),
            authority_effect: "None".to_string(),
            status: "FAIL".to_string(),
            build_success: true,
            harness_elaborated: true,
            axioms_by_declaration: axioms_by_decl,
            forbidden_findings: req.forbidden_findings.clone(),
            refusal_code: Some("FORBIDDEN_CONSTRUCT_DETECTED".to_string()),
            details: Some(format!(
                "Detected {} forbidden construct(s) in sources",
                req.forbidden_findings.len()
            )),
        };
    }

    let fail = |axioms: &BTreeMap<String, Vec<String>>, code: &str, details: String| {
        LeanVerificationReceipt {
            schema_version: LEAN_VERIFICATION_RECEIPT_SCHEMA.to_string(),
            authority_effect: "None".to_string(),
            status: "FAIL".to_string(),
            build_success: true,
            harness_elaborated: true,
            axioms_by_declaration: axioms.clone(),
            forbidden_findings: req.forbidden_findings.clone(),
            refusal_code: Some(code.to_string()),
            details: Some(details),
        }
    };

    // Resolve the authoritative census. A kernel census (e.g. lean4checker over the compiled
    // .olean) is independent of the re-parseable `#print axioms` stdout, which a candidate can
    // forge by shadowing the command (confirmed B1). When present the kernel census governs;
    // when absent, the operator may require it (fail-closed) or fall back to the text census.
    let authoritative: BTreeMap<String, Vec<String>> =
        match (&req.kernel_axiom_census, req.require_kernel_census) {
            (Some(census), _) => census.clone(),
            (None, true) => {
                return fail(
                    &axioms_by_decl,
                    "KERNEL_CENSUS_MISSING",
                    "Kernel axiom census is required but was not supplied by the producer"
                        .to_string(),
                );
            }
            (None, false) => axioms_by_decl.clone(),
        };

    // Cross-check: every required declaration's parsed-text axiom set must match its kernel
    // census set exactly. A clean stdout over a Classical.choice proof is a forgery and the
    // disagreement is its signature, so it fails closed.
    if let Some(census) = &req.kernel_axiom_census {
        for decl in &req.required_declarations {
            let Some(kernel_axioms) = census.get(decl) else {
                return fail(
                    &authoritative,
                    "KERNEL_CENSUS_INCOMPLETE",
                    format!("Kernel census omits required declaration '{decl}'"),
                );
            };
            let text_set: BTreeSet<&str> = axioms_by_decl
                .get(decl)
                .map(|v| v.iter().map(String::as_str).collect())
                .unwrap_or_default();
            let kernel_set: BTreeSet<&str> =
                kernel_axioms.iter().map(String::as_str).collect();
            if text_set != kernel_set {
                return fail(
                    &authoritative,
                    "AXIOM_CENSUS_FORGED",
                    format!(
                        "Declaration '{decl}': #print axioms stdout census {text_set:?} \
                         disagrees with kernel census {kernel_set:?}"
                    ),
                );
            }
        }
    }

    // Type equality (Attack A): the second checker re-elaborates the obligation clean and
    // compares the submission constant's type to it. The gate enforces its verdict fail-closed.
    match (&req.type_equality_by_declaration, req.require_type_equality) {
        (None, true) => {
            return fail(
                &authoritative,
                "TYPE_EQUALITY_MISSING",
                "Clean-type equality verdict is required but was not supplied by the checker"
                    .to_string(),
            );
        }
        (Some(verdicts), _) => {
            for decl in &req.required_declarations {
                match verdicts.get(decl) {
                    None => {
                        return fail(
                            &authoritative,
                            "TYPE_EQUALITY_INCOMPLETE",
                            format!("Type-equality verdict omits required declaration '{decl}'"),
                        );
                    }
                    Some(false) => {
                        return fail(
                            &authoritative,
                            "TYPE_EQUALITY_MISMATCH",
                            format!(
                                "Declaration '{decl}' proved type differs from the clean \
                                 re-elaborated obligation type"
                            ),
                        );
                    }
                    Some(true) => {}
                }
            }
        }
        (None, false) => {}
    }

    // Check required declarations are present in the authoritative census.
    for req_decl in &req.required_declarations {
        if !authoritative.contains_key(req_decl) {
            return fail(
                &authoritative,
                "REQUIRED_DECLARATION_MISSING",
                format!("Required declaration '{req_decl}' was not checked in axioms"),
            );
        }
    }

    // Check axiom policy against the authoritative census.
    for (decl, axioms) in &authoritative {
        for ax in axioms {
            if !allowed_axioms.contains(ax.as_str()) {
                return fail(
                    &authoritative,
                    "AXIOM_POLICY_VIOLATION",
                    format!("Declaration '{decl}' uses unapproved axiom '{ax}' outside policy"),
                );
            }
        }
    }

    LeanVerificationReceipt {
        schema_version: LEAN_VERIFICATION_RECEIPT_SCHEMA.to_string(),
        authority_effect: "None".to_string(),
        status: "PASS".to_string(),
        build_success: true,
        harness_elaborated: true,
        axioms_by_declaration: authoritative,
        forbidden_findings: Vec::new(),
        refusal_code: None,
        details: None,
    }
}

// Origin: vendor/engine/engine_symbol_host_runtime/src/lean_verify.rs
// Claim: urn:omega:crates_rs:omega-symbol-game-runtime:lean-verify:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecordd2459c12 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecordd2459c12` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrord2459c12 {
    /// Refused because `admitted_items` was zero.
    EmptyAdmission,
    /// Refused because `capacity_bound` was zero.
    CapacityZero,
    /// Refused because `admitted_items` exceeded `capacity_bound`.
    ExceedsCapacity {
        /// Requested item count.
        admitted_items: u64,
        /// Declared maximum capacity.
        capacity_bound: u64,
    },
}

#[allow(dead_code, missing_docs)]
impl BoundaryErrord2459c12 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrord2459c12 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrord2459c12 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecordd2459c12 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrord2459c12> {
        if capacity_bound == 0 {
            return Err(BoundaryErrord2459c12::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrord2459c12::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrord2459c12::ExceedsCapacity {
                admitted_items,
                capacity_bound,
            });
        }
        Ok(Self {
            admitted_items,
            capacity_bound,
        })
    }

    /// Returns the admitted item count.
    pub const fn admitted_items(&self) -> u64 {
        self.admitted_items
    }

    /// Returns the declared capacity bound.
    pub const fn capacity_bound(&self) -> u64 {
        self.capacity_bound
    }

    /// Returns the remaining capacity (`capacity_bound - admitted_items`).
    pub const fn remaining_capacity(&self) -> u64 {
        self.capacity_bound.saturating_sub(self.admitted_items)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scanner_skips_comments_and_strings() {
        let code = r#"
-- This line comment mentions sorry and axiom
/- Block comment mentions sorry
   /- Nested block comment mentions unsafe and admit -/
   still in comment sorry
-/
def welcome : String := "this string mentions sorry and partial"
theorem real_thm : 1 = 1 := rfl
"#;
        let sources = vec![SourceFileEntry {
            file: "Test.lean".to_string(),
            content: code.to_string(),
        }];

        let report = scan_lean_sources(&sources, &[], &[]);
        assert!(report.clean, "Must be clean, found: {:?}", report.findings);
    }

    #[test]
    fn test_scanner_flags_real_sorry_and_axiom() {
        let code = r#"
axiom cheat : False
theorem bad : 2 + 2 = 5 := by
  sorry
"#;
        let sources = vec![SourceFileEntry {
            file: "Bad.lean".to_string(),
            content: code.to_string(),
        }];

        let report = scan_lean_sources(&sources, &[], &[]);
        assert!(!report.clean);
        assert_eq!(report.findings.len(), 2);
        assert_eq!(report.findings[0].construct, "axiom");
        assert_eq!(report.findings[1].construct, "sorry");
    }

    #[test]
    fn test_scanner_flags_axiom_report_forgery_surface() {
        // The confirmed B1 bypass: a candidate module shadows `#print axioms` with its
        // own command elaborator so the audit reads a forged clean line. The source must
        // be refused by the scan even though its proof term and the forged output look clean.
        let code = "import Lean\n\
            open Classical in\n\
            noncomputable def myThm : True := trivial\n\
            open Lean Elab Command in\n\
            elab_rules : command\n\
            \x20 | `(#print axioms $_id:ident) => do\n\
            \x20   logInfo \"'judge_check_1' does not depend on any axioms\"\n";
        let sources = vec![SourceFileEntry {
            file: "Discrete4DBianchiSpectralContraction.lean".to_string(),
            content: code.to_string(),
        }];
        let report = scan_lean_sources(&sources, &[], &[]);
        assert!(!report.clean, "elab_rules override must be flagged");
        assert!(
            report.findings.iter().any(|f| f.construct == "elab_rules"),
            "expected an elab_rules finding, got {:?}",
            report.findings
        );
    }

    #[test]
    fn test_scanner_flags_each_metaprogramming_construct() {
        for (kw, line) in [
            ("elab", "elab \"#x\" : command => pure ()"),
            ("macro", "macro \"#x\" : command => `(#check 1)"),
            ("macro_rules", "macro_rules | `(#x) => `(#check 1)"),
            ("syntax", "syntax \"#x\" : command"),
            ("declare_syntax_cat", "declare_syntax_cat myCat"),
            ("run_cmd", "run_cmd pure ()"),
            ("initialize", "initialize x : Nat <- pure 0"),
            ("builtin_initialize", "builtin_initialize y : Nat <- pure 0"),
            ("command_elab", "@[command_elab foo] def g := ()"),
            ("builtin_command_elab", "@[builtin_command_elab foo] def g := ()"),
            ("term_elab", "@[term_elab foo] def g := ()"),
            ("builtin_term_elab", "@[builtin_term_elab foo] def g := ()"),
        ] {
            let sources = vec![SourceFileEntry {
                file: "M.lean".to_string(),
                content: format!("{line}\n"),
            }];
            let report = scan_lean_sources(&sources, &[], &[]);
            assert!(
                report.findings.iter().any(|f| f.construct == kw),
                "construct {kw} must be flagged in {line:?}, got {:?}",
                report.findings
            );
        }
    }

    #[test]
    fn test_scanner_allows_ordinary_proof_identifiers() {
        // Word-boundary substrings of the banned keywords must stay clean, and a genuine
        // tactic/term proof of a real statement must still pass.
        let code = "theorem relabel_elaborated (p : Prop) : p -> p := fun h => h\n\
            def syntaxError : Nat := 0\n\
            def macroName : Nat := 0\n\
            theorem real_thm : 1 = 1 := by rfl\n";
        let sources = vec![SourceFileEntry {
            file: "Clean.lean".to_string(),
            content: code.to_string(),
        }];
        let report = scan_lean_sources(&sources, &[], &[]);
        assert!(report.clean, "clean proof flagged: {:?}", report.findings);
    }

    #[test]
    fn test_audit_clean_pass() {
        let output = "'judge_check_1' depends on axioms: [propext, Quot.sound]\n";
        let req = LeanAuditRequest {
            axioms_output: output.to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            forbidden_findings: vec![],
            ..Default::default()
        };

        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "PASS");
        assert!(receipt.refusal_code.is_none());
    }

    #[test]
    fn test_audit_axiom_violation() {
        let output = "'judge_check_1' depends on axioms: [propext, Quot.sound, Classical.choice]\n";
        let req = LeanAuditRequest {
            axioms_output: output.to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            forbidden_findings: vec![],
            ..Default::default()
        };

        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(
            receipt.refusal_code.as_deref(),
            Some("AXIOM_POLICY_VIOLATION")
        );
    }

    // --- Attack A: reserved judge-owned identifier shadow guard ---

    #[test]
    fn test_scanner_flags_reserved_identifier_and_qualified_head() {
        // The obligation statement names only host-owned `JudgePrelude.*` symbols. A candidate
        // source has no reason to write that namespace; doing so (bare or `.`-qualified) is a
        // shadow attempt (Attack A) and must be flagged.
        let code = "def JudgePrelude : Nat := 0\n\
            theorem t : JudgePrelude.Target := by trivial\n";
        let sources = vec![SourceFileEntry {
            file: "Candidate.lean".to_string(),
            content: code.to_string(),
        }];
        let report = scan_lean_sources(&sources, &[], &["JudgePrelude".to_string()]);
        assert!(!report.clean, "reserved identifier must be flagged");
        let hits: Vec<_> = report
            .findings
            .iter()
            .filter(|f| f.construct == "reserved:JudgePrelude")
            .collect();
        assert_eq!(hits.len(), 2, "bare and qualified head both flagged: {hits:?}");
    }

    #[test]
    fn test_scanner_reserved_respects_leading_word_boundary() {
        // A longer identifier that merely contains the reserved name as a tail/substring is
        // not a reference to the reserved namespace and stays clean.
        let code = "def MyJudgePrelude : Nat := 0\ndef prelude_helper : Nat := 1\n";
        let sources = vec![SourceFileEntry {
            file: "Candidate.lean".to_string(),
            content: code.to_string(),
        }];
        let report = scan_lean_sources(&sources, &[], &["JudgePrelude".to_string()]);
        assert!(report.clean, "lookalike flagged: {:?}", report.findings);
    }

    // --- B1: kernel census cross-check ---

    fn census(pairs: &[(&str, &[&str])]) -> BTreeMap<String, Vec<String>> {
        pairs
            .iter()
            .map(|(k, v)| (k.to_string(), v.iter().map(|s| s.to_string()).collect()))
            .collect()
    }

    #[test]
    fn test_forged_clean_stdout_over_dirty_kernel_is_refused() {
        // Forged B1: stdout reads clean while lean4checker reports Classical.choice.
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' does not depend on any axioms\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            kernel_axiom_census: Some(census(&[("judge_check_1", &["Classical.choice"])])),
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(receipt.refusal_code.as_deref(), Some("AXIOM_CENSUS_FORGED"));
    }

    #[test]
    fn test_kernel_census_is_policy_authority() {
        // Text and kernel agree on Classical.choice; policy forbids it; refused against census.
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' depends on axioms: [Classical.choice]\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            kernel_axiom_census: Some(census(&[("judge_check_1", &["Classical.choice"])])),
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(receipt.refusal_code.as_deref(), Some("AXIOM_POLICY_VIOLATION"));
    }

    #[test]
    fn test_honest_matching_census_passes() {
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' depends on axioms: [propext, Quot.sound]\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            kernel_axiom_census: Some(census(&[("judge_check_1", &["propext", "Quot.sound"])])),
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "PASS", "details: {:?}", receipt.details);
        assert!(receipt.refusal_code.is_none());
    }

    #[test]
    fn test_require_kernel_census_fails_closed_when_absent() {
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' does not depend on any axioms\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            require_kernel_census: true,
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(receipt.refusal_code.as_deref(), Some("KERNEL_CENSUS_MISSING"));
    }

    #[test]
    fn test_kernel_census_incomplete_is_refused() {
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' does not depend on any axioms\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            kernel_axiom_census: Some(census(&[("other_decl", &[])])),
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(receipt.refusal_code.as_deref(), Some("KERNEL_CENSUS_INCOMPLETE"));
    }

    // --- Attack A: clean-type equality verdict at the gate ---

    fn type_eq(pairs: &[(&str, bool)]) -> BTreeMap<String, bool> {
        pairs.iter().map(|(k, v)| (k.to_string(), *v)).collect()
    }

    #[test]
    fn test_type_equality_mismatch_is_refused() {
        // Attack A: the submission proved a weaker type than the clean obligation.
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' depends on axioms: [propext, Quot.sound]\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            type_equality_by_declaration: Some(type_eq(&[("judge_check_1", false)])),
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(receipt.refusal_code.as_deref(), Some("TYPE_EQUALITY_MISMATCH"));
    }

    #[test]
    fn test_require_type_equality_fails_closed_when_absent() {
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' depends on axioms: [propext, Quot.sound]\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            require_type_equality: true,
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "FAIL");
        assert_eq!(receipt.refusal_code.as_deref(), Some("TYPE_EQUALITY_MISSING"));
    }

    #[test]
    fn test_type_equality_true_passes() {
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' depends on axioms: [propext, Quot.sound]\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            type_equality_by_declaration: Some(type_eq(&[("judge_check_1", true)])),
            require_type_equality: true,
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "PASS", "details: {:?}", receipt.details);
    }

    #[test]
    fn test_legacy_text_only_path_unchanged_without_census() {
        // No census, not required: behaves exactly as before (text governs).
        let req = LeanAuditRequest {
            axioms_output: "'judge_check_1' depends on axioms: [propext, Quot.sound]\n".to_string(),
            policy: vec!["propext".into(), "Quot.sound".into()],
            required_declarations: vec!["judge_check_1".into()],
            build_success: true,
            harness_elaborated: true,
            ..Default::default()
        };
        let receipt = audit_lean_verification(&req);
        assert_eq!(receipt.status, "PASS");
    }
}

#[cfg(test)]
mod l4_boundary_tests_d2459c12 {
    // Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0
    use super::*;

    #[test]
    fn admits_within_capacity_and_refuses_overflow() {
        let admitted = BoundaryRecordd2459c12::try_admit(3, 8);
        assert!(admitted.is_ok());
        if let Ok(record) = admitted {
            assert_eq!(record.admitted_items(), 3);
            assert_eq!(record.capacity_bound(), 8);
            assert_eq!(record.remaining_capacity(), 5);
        }
        let at_cap = BoundaryRecordd2459c12::try_admit(8, 8);
        assert!(at_cap.is_ok());
        let overflow = BoundaryRecordd2459c12::try_admit(9, 8);
        assert!(overflow.is_err());
        let zero_items = BoundaryRecordd2459c12::try_admit(0, 8);
        assert!(zero_items.is_err());
        let zero_cap = BoundaryRecordd2459c12::try_admit(1, 0);
        assert!(zero_cap.is_err());
        assert_eq!(BoundaryErrord2459c12::EmptyAdmission.violated_invariant(), "admitted_items >= 1");
        assert_eq!(BoundaryErrord2459c12::CapacityZero.violated_invariant(), "capacity_bound >= 1");
    }
}
