//! Conservative source-AST observation, not Sonar cognitive conformance.
use serde_json::json;
use syn::visit::{self, Visit};

#[derive(Default)]
struct Flow {
    weighted: usize,
    ccn: usize,
    depth: usize,
    nesting: usize,
    macros: Vec<String>,
}
impl<'a> Visit<'a> for Flow {
    fn visit_expr(&mut self, node: &'a syn::Expr) {
        let nested = matches!(
            node,
            syn::Expr::If(_)
                | syn::Expr::ForLoop(_)
                | syn::Expr::While(_)
                | syn::Expr::Loop(_)
                | syn::Expr::Match(_)
                | syn::Expr::Closure(_)
        );
        let branch = nested
            || matches!(node, syn::Expr::Try(_))
            || matches!(node, syn::Expr::Binary(b) if matches!(b.op, syn::BinOp::And(_) | syn::BinOp::Or(_)));
        if branch {
            self.weighted += 1 + self.depth;
            self.ccn += 1;
        }
        if nested {
            self.depth += 1;
            self.nesting = self.nesting.max(self.depth);
        }
        visit::visit_expr(self, node);
        if nested {
            self.depth -= 1;
        }
    }
    fn visit_macro(&mut self, node: &'a syn::Macro) {
        let name = node.path.segments.last().unwrap().ident.to_string();
        if name == "matches" {
            let alternatives = node
                .tokens
                .clone()
                .into_iter()
                .filter(|t| matches!(t,proc_macro2::TokenTree::Punct(p) if p.as_char()=='|'))
                .count();
            self.weighted += (1 + alternatives) * (1 + self.depth);
            self.ccn += 1 + alternatives;
        } else if !["format", "write", "file"].contains(&name.as_str()) {
            self.macros.push(name);
        }
    }
}

fn report(name: String, block: &syn::Block) -> serde_json::Value {
    let mut flow = Flow::default();
    flow.visit_block(block);
    json!({"name":name,"ast_decision_upper_bound":flow.ccn+1,"weighted_control_upper_bound":flow.weighted,"control_nesting":flow.nesting,"unsupported_macros":flow.macros})
}

fn main() {
    let file = std::env::args().nth(1).expect("explicit source argument");
    let source = std::fs::read_to_string(&file).expect("source readable");
    let parsed = syn::parse_file(&source).expect("complete Rust AST");
    let mut rows = Vec::new();
    for item in parsed.items {
        match item {
            syn::Item::Fn(f) => rows.push(report(f.sig.ident.to_string(), &f.block)),
            syn::Item::Impl(i) => {
                for entry in i.items {
                    if let syn::ImplItem::Fn(f) = entry {
                        rows.push(report(f.sig.ident.to_string(), &f.block));
                    }
                }
            }
            _ => (),
        }
    }
    println!(
        "{}",
        json!({"source":file,"functions":rows,"scope":"Calibrated conservative Rust syntax observer, includes fallible ? edges and matches alternatives. Not Sonar conformance, expanded macro semantics, or a runtime/grade measurement."})
    );
}
