use std::fs;
use std::path::Path;
use syn::visit::{self, Visit};
use syn::{Expr, ExprCall, ExprStruct, Path as SynPath};

fn rust_files(root: &Path, files: &mut Vec<std::path::PathBuf>) {
    for entry in fs::read_dir(root).unwrap() {
        let path = entry.unwrap().path();
        if path.is_dir() {
            rust_files(&path, files);
        } else if path.extension().and_then(|ext| ext.to_str()) == Some("rs") {
            files.push(path);
        }
    }
}

fn path_name(path: &SynPath) -> String {
    path.segments
        .iter()
        .map(|segment| segment.ident.to_string())
        .collect::<Vec<_>>()
        .join("::")
}

fn is_forbidden_call(name: &str) -> bool {
    name.contains("CertifiedAuthority::")
        || name.ends_with("certify_checked_packet")
        || name.ends_with("authority_from_outcome")
        || name.ends_with("DescentWitness::from_verified_replay")
}

#[derive(Default)]
struct AuthorityConstructorAudit {
    violations: Vec<String>,
}

impl<'ast> Visit<'ast> for AuthorityConstructorAudit {
    fn visit_expr_call(&mut self, call: &'ast ExprCall) {
        if let Expr::Path(path) = call.func.as_ref() {
            let name = path_name(&path.path);
            if is_forbidden_call(&name) {
                self.violations.push(name);
            }
        }
        visit::visit_expr_call(self, call);
    }

    fn visit_expr_struct(&mut self, expression: &'ast ExprStruct) {
        let name = path_name(&expression.path);
        if name == "AuthorizedLocalResult" || name.ends_with("::AuthorizedLocalResult") {
            self.violations.push(name);
        }
        visit::visit_expr_struct(self, expression);
    }
}

#[test]
fn runtime_adapter_imports_shared_types_without_importing_apache_semantics() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"));
    let adapter = fs::read_to_string(root.join("src/runtime_adapter.rs")).unwrap();
    assert!(adapter.contains("tfqm_wdp::coda::coda_gtla"));
    assert!(adapter.contains("engine_state::CodaTerminal"));
    assert!(adapter.contains("engine_contracts::mub_domain_ownership"));
    assert!(!adapter.contains("use mub::"));
    assert!(!adapter.contains("mub::apache"));
}

#[test]
fn neither_mub_rail_contains_an_authority_constructor_call() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"));
    let mut files = Vec::new();
    rust_files(&root.join("src"), &mut files);
    let mub_src = root.join("../mub/src");
    if mub_src.exists() {
        rust_files(&mub_src, &mut files);
    }

    let mut violations = Vec::new();
    for path in files {
        let source = fs::read_to_string(&path).unwrap();
        let syntax = syn::parse_file(&source)
            .unwrap_or_else(|error| panic!("cannot parse {}: {error}", path.display()));
        let mut audit = AuthorityConstructorAudit::default();
        audit.visit_file(&syntax);
        for constructor in audit.violations {
            violations.push(format!("{}: {constructor}", path.display()));
        }
    }
    assert!(
        violations.is_empty(),
        "authority constructor calls: {violations:?}"
    );
}

#[test]
fn ast_audit_does_not_treat_comment_markers_inside_strings_as_comments() {
    let source = r#"
        fn fixture() {
            let _url = "https://example.invalid/path";
            certify_checked_packet();
        }
    "#;
    let syntax = syn::parse_file(source).unwrap();
    let mut audit = AuthorityConstructorAudit::default();
    audit.visit_file(&syntax);
    assert_eq!(audit.violations, vec!["certify_checked_packet"]);
}

#[test]
fn crate_dependency_direction_preserves_the_quarantine() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"));
    let native_cargo = fs::read_to_string(root.join("Cargo.toml")).unwrap();
    // Optional compare lane only — crates/mub was deleted per quarantine policy.
    let apache_cargo_path = root.join("../mub/Cargo.toml");
    if apache_cargo_path.exists() {
        let apache_cargo = fs::read_to_string(apache_cargo_path).unwrap();
        assert!(!apache_cargo.contains("omega_mub"));
    }
    assert!(native_cargo.contains("default = []"));
}
