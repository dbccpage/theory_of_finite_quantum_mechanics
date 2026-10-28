//! Zero-float audit of the modules the per-target audits no longer read.
//!
//! Each `test_target_*` audit parses only its own module. The constants, the
//! 6x6 matrices, the firewall line and the binary field those modules used to
//! define locally now live in shared modules, so they are audited here.
//!
//! AuthorityEffect: None

use std::fs;
use std::path::Path;
use syn::visit::Visit;

const SHARED_MODULES: [&str; 4] = [
    "src/native/mub6_constants.rs",
    "src/native/mub6_firewall.rs",
    "src/native/mub6_matrix6.rs",
    "../omega_number_theory/src/binary_field.rs",
];

#[derive(Default)]
struct FloatAudit {
    found: Vec<String>,
}

impl<'ast> Visit<'ast> for FloatAudit {
    fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
        for seg in &node.path.segments {
            let ident = seg.ident.to_string();
            if ident == "f32" || ident == "f64" {
                self.found.push(format!("float type {ident}"));
            }
        }
        syn::visit::visit_type_path(self, node);
    }

    fn visit_lit_float(&mut self, node: &'ast syn::LitFloat) {
        self.found.push(format!("float literal {node}"));
        syn::visit::visit_lit_float(self, node);
    }
}

fn floats_in(source: &str) -> Vec<String> {
    let tree = syn::parse_file(source).expect("source parses");
    let mut audit = FloatAudit::default();
    audit.visit_file(&tree);
    audit.found
}

#[test]
fn shared_modules_contain_no_floats() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"));
    for module in SHARED_MODULES {
        let path = root.join(module);
        let source = fs::read_to_string(&path)
            .unwrap_or_else(|e| panic!("failed to read {}: {e}", path.display()));
        assert_eq!(floats_in(&source), Vec::<String>::new(), "{module}");
    }
}

#[test]
fn the_audit_flags_a_float_type_and_a_float_literal() {
    let found = floats_in("pub fn lipschitz_bound() -> f64 { 85.0 / 9.0 }");
    assert_eq!(
        found,
        vec!["float type f64", "float literal 85.0", "float literal 9.0"]
    );
}
