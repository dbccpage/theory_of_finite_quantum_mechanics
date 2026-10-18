//! Crate-wide float census.
//!
//! Walks every `.rs` file under this crate. A hit is a float type, a float
//! literal, or a float conversion (`to_f64`, `as f64`/`as f32`, an `f32`/`f64`
//! path). A hit is `deciding-path` when a comparison that contains it sits in
//! a function that also names a certificate, completeness, or MUB(6) claim
//! bit. Every other hit is `diagnostic-isolated`. A skipped file or a
//! deciding-path hit fails.
//!
//! AuthorityEffect: None
//! Firewall Line: NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no authority

use std::fs;
use std::path::{Path, PathBuf};

use syn::spanned::Spanned;
use syn::visit::Visit;

const VERDICT_IDENTS: &[&str] = &[
    "gate_a_pass",
    "gate_b_pass",
    "mub6_equals_3",
    "mub6_at_most_3",
    "global_solution",
    "verified_certificate",
    "real_spectrum_gluing_passed",
    "archimedean_norm_bound_certified",
    "all_cells_certified",
    "complete",
    "is_complete",
    "solved",
];

#[derive(Clone, Debug, PartialEq, Eq)]
struct Hit {
    line: usize,
    kind: String,
    disposition: &'static str,
}

struct FnFrame {
    verdict: bool,
}

struct Census {
    hits: Vec<RawHit>,
    fns: Vec<FnFrame>,
    stack: Vec<usize>,
    in_compare: u32,
    in_format: u32,
}

struct RawHit {
    line: usize,
    kind: String,
    comparison: bool,
    formatting: bool,
    fn_index: Option<usize>,
}

impl Census {
    fn record(&mut self, line: usize, kind: String) {
        self.hits.push(RawHit {
            line,
            kind,
            comparison: self.in_compare > 0,
            formatting: self.in_format > 0,
            fn_index: self.stack.last().copied(),
        });
    }
}

fn last_ident(path: &syn::Path) -> String {
    path.segments
        .last()
        .map(|seg| seg.ident.to_string())
        .unwrap_or_default()
}

fn path_has_float(path: &syn::Path) -> Option<&'static str> {
    for seg in &path.segments {
        match seg.ident.to_string().as_str() {
            "f64" => return Some("f64"),
            "f32" => return Some("f32"),
            _ => {}
        }
    }
    None
}

fn type_float(ty: &syn::Type) -> Option<&'static str> {
    let syn::Type::Path(path) = ty else {
        return None;
    };
    path_has_float(&path.path)
}

fn is_cmp(op: &syn::BinOp) -> bool {
    matches!(
        op,
        syn::BinOp::Lt(_)
            | syn::BinOp::Gt(_)
            | syn::BinOp::Le(_)
            | syn::BinOp::Ge(_)
            | syn::BinOp::Eq(_)
            | syn::BinOp::Ne(_)
    )
}

fn is_format_macro(name: &str) -> bool {
    matches!(
        name,
        "format" | "println" | "eprintln" | "print" | "write" | "writeln" | "panic" | "format_args"
    )
}

impl<'ast> Visit<'ast> for Census {
    fn visit_item_fn(&mut self, node: &'ast syn::ItemFn) {
        self.fns.push(FnFrame { verdict: false });
        self.stack.push(self.fns.len() - 1);
        syn::visit::visit_item_fn(self, node);
        self.stack.pop();
    }

    fn visit_impl_item_fn(&mut self, node: &'ast syn::ImplItemFn) {
        self.fns.push(FnFrame { verdict: false });
        self.stack.push(self.fns.len() - 1);
        syn::visit::visit_impl_item_fn(self, node);
        self.stack.pop();
    }

    fn visit_ident(&mut self, ident: &'ast syn::Ident) {
        if let Some(index) = self.stack.last().copied() {
            if VERDICT_IDENTS.contains(&ident.to_string().as_str()) {
                self.fns[index].verdict = true;
            }
        }
    }

    fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
        if let Some(name) = path_has_float(&node.path) {
            self.record(node.path.span().start().line, format!("float type {name}"));
        }
        syn::visit::visit_type_path(self, node);
    }

    fn visit_expr_path(&mut self, node: &'ast syn::ExprPath) {
        if let Some(name) = path_has_float(&node.path) {
            self.record(
                node.path.span().start().line,
                format!("float conversion std::{name}"),
            );
        }
        syn::visit::visit_expr_path(self, node);
    }

    fn visit_lit_float(&mut self, node: &'ast syn::LitFloat) {
        self.record(node.span().start().line, format!("float literal {node}"));
        syn::visit::visit_lit_float(self, node);
    }

    fn visit_expr_method_call(&mut self, node: &'ast syn::ExprMethodCall) {
        let comparing = node.method == "partial_cmp";
        if comparing {
            self.in_compare += 1;
        }
        if node.method == "to_f64" {
            self.record(
                node.method.span().start().line,
                "float conversion to_f64".to_string(),
            );
        }
        syn::visit::visit_expr_method_call(self, node);
        if comparing {
            self.in_compare -= 1;
        }
    }

    fn visit_expr_cast(&mut self, node: &'ast syn::ExprCast) {
        if let Some(name) = type_float(&node.ty) {
            self.record(
                node.span().start().line,
                format!("float conversion as {name}"),
            );
        }
        syn::visit::visit_expr_cast(self, node);
    }

    fn visit_expr_binary(&mut self, node: &'ast syn::ExprBinary) {
        let comparing = is_cmp(&node.op);
        if comparing {
            self.in_compare += 1;
        }
        syn::visit::visit_expr_binary(self, node);
        if comparing {
            self.in_compare -= 1;
        }
    }

    fn visit_item_use(&mut self, node: &'ast syn::ItemUse) {
        record_use_tree(self, &node.tree, node.span().start().line);
        syn::visit::visit_item_use(self, node);
    }

    fn visit_macro(&mut self, node: &'ast syn::Macro) {
        let name = last_ident(&node.path);
        let formatting = is_format_macro(&name);
        if formatting {
            self.in_format += 1;
        }
        record_macro_tokens(self, node);
        syn::visit::visit_macro(self, node);
        if formatting {
            self.in_format -= 1;
        }
    }
}

fn record_use_tree(census: &mut Census, tree: &syn::UseTree, line: usize) {
    match tree {
        syn::UseTree::Path(path) => {
            let name = path.ident.to_string();
            if name == "f64" || name == "f32" {
                census.record(line, format!("float conversion std::{name}"));
            }
            record_use_tree(census, &path.tree, line);
        }
        syn::UseTree::Name(name) => {
            let name = name.ident.to_string();
            if name == "f64" || name == "f32" {
                census.record(line, format!("float conversion std::{name}"));
            }
        }
        syn::UseTree::Rename(rename) => {
            let name = rename.ident.to_string();
            if name == "f64" || name == "f32" {
                census.record(line, format!("float conversion std::{name}"));
            }
        }
        syn::UseTree::Glob(_) => {}
        syn::UseTree::Group(group) => {
            for item in &group.items {
                record_use_tree(census, item, line);
            }
        }
    }
}

fn record_macro_tokens(census: &mut Census, node: &syn::Macro) {
    let line = node.span().start().line;
    let text = node.tokens.to_string();
    if text.contains("to_f64") {
        census.record(line, "float conversion to_f64".to_string());
    }
    if text.contains("as f64") {
        census.record(line, "float conversion as f64".to_string());
    }
    if text.contains("as f32") {
        census.record(line, "float conversion as f32".to_string());
    }
    if text.split(|c: char| !c.is_ascii_alphanumeric() && c != '_').any(|tok| tok == "f64")
    {
        census.record(line, "float conversion std::f64".to_string());
    }
    if text.split(|c: char| !c.is_ascii_alphanumeric() && c != '_').any(|tok| tok == "f32")
    {
        census.record(line, "float conversion std::f32".to_string());
    }
    for tok in text.split(|c: char| c.is_whitespace() || matches!(c, ',' | '(' | ')' | '{' | '}' | '[' | ']'))
    {
        if looks_like_float_literal(tok) {
            census.record(line, format!("float literal {tok}"));
        }
    }
}

fn looks_like_float_literal(tok: &str) -> bool {
    let trimmed = tok.trim_end_matches("f64").trim_end_matches("f32");
    if trimmed.is_empty() || trimmed.chars().all(|c| c.is_ascii_digit()) {
        return false;
    }
    trimmed.parse::<f64>().is_ok() && (trimmed.contains('.') || trimmed.contains('e') || trimmed.contains('E'))
}

fn census_source(source: &str) -> Vec<Hit> {
    let tree = syn::parse_file(source).expect("source parses");
    let mut census = Census {
        hits: Vec::new(),
        fns: Vec::new(),
        stack: Vec::new(),
        in_compare: 0,
        in_format: 0,
    };
    census.visit_file(&tree);
    census
        .hits
        .into_iter()
        .map(|hit| {
            let verdict = hit
                .fn_index
                .map(|index| census.fns[index].verdict)
                .unwrap_or(false);
            let disposition = if hit.comparison && !hit.formatting && verdict {
                "deciding-path"
            } else {
                "diagnostic-isolated"
            };
            Hit {
                line: hit.line,
                kind: hit.kind,
                disposition,
            }
        })
        .collect()
}

fn rust_files(root: &Path) -> Vec<PathBuf> {
    let mut files = Vec::new();
    for dir in [root.join("src"), root.join("../tests/omega_mub")] {
        walk(&dir, &mut files);
    }
    files.sort();
    files
}

fn walk(dir: &Path, files: &mut Vec<PathBuf>) {
    let entries = fs::read_dir(dir).unwrap_or_else(|err| panic!("read {}: {err}", dir.display()));
    for entry in entries {
        let entry = entry.expect("dir entry");
        let path = entry.path();
        if path.is_dir() {
            walk(&path, files);
        } else if path.extension().and_then(|ext| ext.to_str()) == Some("rs") {
            files.push(path);
        }
    }
}

fn render_census(root: &Path) -> String {
    let mut out = String::new();
    let mut deciding = 0usize;
    let mut hits_total = 0usize;
    let files = rust_files(root);
    for path in &files {
        let rel = path.strip_prefix(root).unwrap_or(path);
        let source = fs::read_to_string(path)
            .unwrap_or_else(|err| panic!("read {}: {err}", path.display()));
        let hits = census_source(&source);
        out.push_str(&format!("FILE {}\n", rel.display()));
        if hits.is_empty() {
            out.push_str("  (no float hits)\n");
        }
        for hit in &hits {
            hits_total += 1;
            if hit.disposition == "deciding-path" {
                deciding += 1;
            }
            out.push_str(&format!(
                "  L{} {} {}\n",
                hit.line, hit.kind, hit.disposition
            ));
        }
    }
    out.push_str(&format!(
        "SUMMARY files={} hits={} deciding={}\n",
        files.len(),
        hits_total,
        deciding
    ));
    out
}

#[test]
fn the_census_flags_a_synthetic_hidden_float_as_deciding_path() {
    let found = census_source(
        "fn sneak(estimate: f64) -> bool { let gate_a_pass = estimate > 0.0; gate_a_pass }\n",
    );
    assert!(
        found.iter().any(|hit| hit.kind.contains("f64")),
        "synthetic float must be flagged: {found:?}"
    );
    assert!(
        found.iter().any(|hit| hit.disposition == "deciding-path"),
        "a float comparison that sets gate_a_pass is deciding-path: {found:?}"
    );
}

#[test]
fn the_census_keeps_a_printout_float_diagnostic() {
    let found = census_source("fn show(x: f64) { println!(\"{x}\"); }\n");
    assert!(!found.is_empty());
    assert!(found.iter().all(|hit| hit.disposition == "diagnostic-isolated"));
}

#[test]
fn every_rust_file_is_censused_and_no_deciding_path_float_remains() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"));
    let files = rust_files(root);
    assert!(files.len() > 4, "the walk must cover more than the old four-module list");
    let rendered = render_census(root);
    println!("{rendered}");
    if let Ok(path) = std::env::var("MUB_FLOAT_CENSUS_OUT") {
        let dest = PathBuf::from(path);
        if let Some(parent) = dest.parent() {
            fs::create_dir_all(parent).expect("census directory");
        }
        fs::write(&dest, &rendered).expect("write census");
    }
    assert!(rendered.contains("SUMMARY"));
    let deciding = rendered.matches("deciding-path").count();
    assert_eq!(deciding, 0, "deciding-path hits remain; see MUB_FLOAT_CENSUS_OUT");
}
