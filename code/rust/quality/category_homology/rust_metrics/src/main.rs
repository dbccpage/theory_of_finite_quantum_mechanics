//! Source AST metrics, not a semantic verifier. AuthorityEffect: None.
//!
//! CCN counts if/loop tests, non-default match arms and guards, let-else,
//! short-circuit boolean operators, and `?`. Cognitive upper bound adds
//! 1+control depth for branches/loops/matches, one per else/boolean/recursion,
//! and closure nesting. `?` is a linear typed early exit, not cognitive nesting.
//! Tests are excluded by cfg(test). Unknown macros remain explicitly opaque;
//! macro-free results and parsed standard formatting/vec macro arguments are
//! exact for this declared source metric. No compiler expansion is claimed.

use serde_json::{json, Value};
use std::{env, fs, process};
use syn::{parse::Parser, punctuated::Punctuated, spanned::Spanned, visit::Visit, *};

fn test_only(attrs: &[Attribute]) -> bool {
    attrs.iter().any(|a| {
        a.path().is_ident("test")
            || (a.path().is_ident("cfg")
                && a.parse_args::<Path>().is_ok_and(|p| p.is_ident("test")))
    })
}

#[derive(Default)]
struct Functions {
    records: Vec<Value>,
}

impl Functions {
    fn record(&mut self, signature: &Signature, block: &Block) {
        let mut flow = Flow {
            name: signature.ident.to_string(),
            ccn: 1,
            ..Flow::default()
        };
        flow.visit_block(block);
        self.records.push(json!({
            "name": flow.name, "line": signature.fn_token.span.start().line,
            "ccn": flow.ccn, "cognitive_upper_bound": flow.cognitive,
            "control_nesting": flow.max_depth, "opaque_macros": flow.opaque,
        }));
    }
}

impl<'ast> Visit<'ast> for Functions {
    fn visit_item(&mut self, node: &'ast Item) {
        let attrs = match node {
            Item::Fn(v) => &v.attrs,
            Item::Mod(v) => &v.attrs,
            Item::Impl(v) => &v.attrs,
            Item::Trait(v) => &v.attrs,
            _ => return syn::visit::visit_item(self, node),
        };
        if !test_only(attrs) {
            syn::visit::visit_item(self, node);
        }
    }
    fn visit_item_fn(&mut self, node: &'ast ItemFn) {
        if !test_only(&node.attrs) {
            self.record(&node.sig, &node.block);
            // Nested named functions have their own metric record.
            syn::visit::visit_item_fn(self, node);
        }
    }
    fn visit_impl_item_fn(&mut self, node: &'ast ImplItemFn) {
        if !test_only(&node.attrs) {
            self.record(&node.sig, &node.block);
            syn::visit::visit_impl_item_fn(self, node);
        }
    }
    fn visit_trait_item_fn(&mut self, node: &'ast TraitItemFn) {
        if !test_only(&node.attrs) {
            if let Some(body) = &node.default {
                self.record(&node.sig, body);
            }
            syn::visit::visit_trait_item_fn(self, node);
        }
    }
}

#[derive(Default)]
struct Flow {
    name: String,
    ccn: usize,
    cognitive: usize,
    depth: usize,
    max_depth: usize,
    opaque: Vec<String>,
}

impl Flow {
    fn enter(&mut self) {
        self.cognitive += 1 + self.depth;
        self.depth += 1;
        self.max_depth = self.max_depth.max(self.depth);
    }
    fn macro_arguments(&mut self, mac: &Macro) {
        let label = mac.path.segments.last().unwrap().ident.to_string();
        // These standard macros do not add hidden control to argument evaluation.
        let transparent = [
            "format",
            "format_args",
            "println",
            "print",
            "eprintln",
            "eprint",
            "vec",
            "write",
            "writeln",
        ];
        if transparent.contains(&label.as_str()) {
            let parser = Punctuated::<Expr, Token![,]>::parse_terminated;
            if let Ok(arguments) = parser.parse2(mac.tokens.clone()) {
                for argument in arguments {
                    self.visit_expr(&argument);
                }
                return;
            }
            if label == "vec" {
                // Parse the repeat form vec![value; count] as an array expression.
                let tokens = mac.tokens.clone();
                let group = proc_macro2::Group::new(proc_macro2::Delimiter::Bracket, tokens);
                if let Ok(array) = syn::parse2::<Expr>(proc_macro2::TokenTree::Group(group).into())
                {
                    self.visit_expr(&array);
                    return;
                }
            }
        }
        self.opaque
            .push(format!("{}:{}", label, mac.span().start().line));
    }
}

impl<'ast> Visit<'ast> for Flow {
    fn visit_item(&mut self, _: &'ast Item) {} // counted separately, never twice
    fn visit_expr_if(&mut self, node: &'ast ExprIf) {
        self.ccn += 1;
        self.enter();
        self.visit_expr(&node.cond);
        self.visit_block(&node.then_branch);
        self.depth -= 1;
        if let Some((_, other)) = &node.else_branch {
            self.cognitive += 1;
            // An else-if is a chain at the current depth, not another nested block.
            if matches!(&**other, Expr::If(_)) {
                self.visit_expr(other);
            } else {
                self.depth += 1;
                self.max_depth = self.max_depth.max(self.depth);
                self.visit_expr(other);
                self.depth -= 1;
            }
        }
    }
    fn visit_expr_for_loop(&mut self, node: &'ast ExprForLoop) {
        self.ccn += 1;
        self.enter();
        self.visit_expr(&node.expr);
        self.visit_block(&node.body);
        self.depth -= 1;
    }
    fn visit_expr_while(&mut self, node: &'ast ExprWhile) {
        self.ccn += 1;
        self.enter();
        self.visit_expr(&node.cond);
        self.visit_block(&node.body);
        self.depth -= 1;
    }
    fn visit_expr_loop(&mut self, node: &'ast ExprLoop) {
        self.ccn += 1;
        self.enter();
        self.visit_block(&node.body);
        self.depth -= 1;
    }
    fn visit_expr_match(&mut self, node: &'ast ExprMatch) {
        self.enter();
        self.visit_expr(&node.expr);
        for arm in &node.arms {
            self.ccn += pattern_decisions(&arm.pat);
            syn::visit::visit_arm(self, arm);
        }
        self.depth -= 1;
    }
    fn visit_pat_guard(&mut self, node: &'ast PatGuard) {
        self.cognitive += 1;
        syn::visit::visit_pat_guard(self, node);
    }
    fn visit_local(&mut self, node: &'ast Local) {
        if let Some(init) = &node.init {
            self.visit_expr(&init.expr);
            if let Some((_, branch)) = &init.diverge {
                self.ccn += 1;
                self.enter();
                self.visit_expr(branch);
                self.depth -= 1;
            }
        }
    }
    fn visit_expr_binary(&mut self, node: &'ast ExprBinary) {
        if matches!(node.op, BinOp::And(_) | BinOp::Or(_)) {
            self.ccn += 1;
            self.cognitive += 1;
        }
        syn::visit::visit_expr_binary(self, node);
    }
    fn visit_expr_try(&mut self, node: &'ast ExprTry) {
        self.ccn += 1;
        syn::visit::visit_expr_try(self, node);
    }
    fn visit_expr_closure(&mut self, node: &'ast ExprClosure) {
        self.depth += 1;
        self.max_depth = self.max_depth.max(self.depth);
        syn::visit::visit_expr_closure(self, node);
        self.depth -= 1;
    }
    fn visit_expr_call(&mut self, node: &'ast ExprCall) {
        if let Expr::Path(path) = &*node.func {
            if path
                .path
                .segments
                .last()
                .is_some_and(|s| s.ident == self.name)
            {
                self.cognitive += 1;
            }
        }
        syn::visit::visit_expr_call(self, node);
    }
    fn visit_expr_method_call(&mut self, node: &'ast ExprMethodCall) {
        if node.method == self.name {
            self.cognitive += 1;
        }
        syn::visit::visit_expr_method_call(self, node);
    }
    fn visit_macro(&mut self, mac: &'ast Macro) {
        self.macro_arguments(mac);
    }
}

fn pattern_decisions(pat: &Pat) -> usize {
    match pat {
        Pat::Wild(_) => 0,
        Pat::Guard(p) => 1 + pattern_decisions(&p.pat),
        Pat::Or(p) => p.cases.iter().map(pattern_decisions).sum(),
        Pat::Paren(p) => pattern_decisions(&p.pat),
        _ => 1,
    }
}

fn analyze(source: &str) -> Result<Vec<Value>> {
    let file = syn::parse_file(source)?;
    let mut collector = Functions::default();
    collector.visit_file(&file);
    Ok(collector.records)
}

fn main() {
    let mut records = serde_json::Map::new();
    for path in env::args().skip(1) {
        let source = fs::read_to_string(&path).unwrap_or_else(|err| {
            eprintln!("{path}: {err}");
            process::exit(1)
        });
        let result = analyze(&source).unwrap_or_else(|err| {
            eprintln!("{path}: {err}");
            process::exit(1)
        });
        records.insert(path, json!(result));
    }
    println!("{}", serde_json::to_string_pretty(&records).unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    fn one(source: &str) -> Value {
        analyze(source).unwrap().remove(0)
    }

    #[test]
    fn lifetimes_and_closures_are_functions_not_fake_boolean_operators() {
        let record = one("fn f<'a>(x: &'a str) { let k = || x; k(); }");
        assert_eq!(record["ccn"], 1);
        assert_eq!(record["cognitive_upper_bound"], 0);
        assert_eq!(record["control_nesting"], 1);
    }

    #[test]
    fn independent_hand_counted_control_tree() {
        let record =
            one("fn f(a: bool,b: bool) { for i in 0..2 { if a && b { while a { } } else { } } }");
        assert_eq!(record["ccn"], 5); // base + for + if + && + while
        assert_eq!(record["cognitive_upper_bound"], 8); // 1+2+3 + bool + else
        assert_eq!(record["control_nesting"], 3);
    }

    #[test]
    fn controls_inside_a_condition_keep_the_enclosing_control_depth() {
        let record = one("fn f(a:bool){ if (if a { true } else { false }) { } }");
        assert_eq!(record["ccn"], 3);
        assert_eq!(record["cognitive_upper_bound"], 4); // outer 1 + inner 2 + else
        assert_eq!(record["control_nesting"], 2);
    }

    #[test]
    fn match_guards_and_or_patterns_are_decisions() {
        let record = one("fn f(x:u8,b:bool) { match x { 1|2 if b => (), _ => () } }");
        assert_eq!(record["ccn"], 4);
        assert_eq!(record["cognitive_upper_bound"], 2);
    }

    #[test]
    fn let_else_and_try_are_explicit_exits() {
        let record =
            one("fn f(x:Option<u8>)->Option<u8>{ let Some(a)=x else{return None}; Some(x?+a) }");
        assert_eq!(record["ccn"], 3);
        assert_eq!(record["cognitive_upper_bound"], 1);
    }

    #[test]
    fn excludes_test_modules_and_keeps_trait_default_and_nested_functions() {
        let records = analyze("#[cfg(test)] mod tests { fn ignored(){} } trait T {fn absent(); fn default(){}} fn outer(){fn inner(){}} ").unwrap();
        assert_eq!(records.len(), 3);
        assert_eq!(records[1]["ccn"], 1);
    }

    #[test]
    fn formats_visit_argument_expressions_and_unknown_macros_are_opaque() {
        let record = one("fn f(a:bool){format!(\"{}\", if a {1}else{0}); mysterious!(if a {1});}");
        assert_eq!(record["ccn"], 2);
        assert_eq!(record["opaque_macros"], json!(["mysterious:1"]));
    }

    #[test]
    fn refuses_malformed_source() {
        assert!(analyze("fn broken(").is_err());
    }
}
