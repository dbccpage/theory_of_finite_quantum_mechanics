//! Raw operation/equation declarations and literal partial-table diagnostics.
//!
//! These records do not admit a Lawvere theory, profunctor, typed substitution
//! calculus or equation semantics. Names, sorts and stored status are caller data.
//! Associativity checks only the supplied cases under the documented slot formula;
//! the Cauchy diagnostic searches declared names for the two literal split entries.
//! Neither result establishes completeness of an underlying mathematical category.

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
/// An unchecked name and two ordered sort lists; duplicates are retained.
pub struct OperationDecl {
    pub name: String,
    pub input_sorts: Vec<String>,
    pub output_sorts: Vec<String>,
}

impl OperationDecl {
    pub fn new(name: &str, input_sorts: Vec<String>, output_sorts: Vec<String>) -> Self {
        Self {
            name: name.into(),
            input_sorts,
            output_sorts,
        }
    }

    pub fn arity(&self) -> usize {
        self.input_sorts.len()
    }

    pub fn coarity(&self) -> usize {
        self.output_sorts.len()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
/// Uninterpreted equation strings, not parsed or enforced equations.
pub struct EquationDecl {
    pub name: String,
    pub lhs: String,
    pub rhs: String,
}

impl EquationDecl {
    pub fn new(name: &str, lhs: &str, rhs: &str) -> Self {
        Self {
            name: name.into(),
            lhs: lhs.into(),
            rhs: rhs.into(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
/// Result of the declared-name split inventory, not a category-law certificate.
pub enum TheoryCauchyStatus {
    Complete,
    Incomplete { unsplit_operations: Vec<String> },
}

#[derive(Debug, Clone)]
/// Mutable raw records. Appends retain duplicates; table inserts overwrite keys.
/// `cauchy_status` is independent caller metadata, never updated by the checkers.
pub struct LawvereTheory {
    pub name: String,
    pub sorts: Vec<String>,
    pub operations: Vec<OperationDecl>,
    pub equations: Vec<EquationDecl>,
    pub substitution_table: BTreeMap<(String, usize, String), String>,
    pub identities: BTreeMap<String, String>, // sort -> identity operation
    pub cauchy_status: TheoryCauchyStatus,
}

impl LawvereTheory {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.into(),
            sorts: Vec::new(),
            operations: Vec::new(),
            equations: Vec::new(),
            substitution_table: BTreeMap::new(),
            identities: BTreeMap::new(),
            cauchy_status: TheoryCauchyStatus::Complete,
        }
    }

    pub fn add_sort(&mut self, sort: &str) {
        self.sorts.push(sort.into());
    }
    pub fn add_operation(&mut self, op: OperationDecl) {
        self.operations.push(op);
    }
    pub fn add_equation(&mut self, eq: EquationDecl) {
        self.equations.push(eq);
    }

    pub fn add_substitution(&mut self, outer: &str, slot: usize, inner: &str, result: &str) {
        self.substitution_table
            .insert((outer.into(), slot, inner.into()), result.into());
    }

    pub fn substitute(&self, outer: &str, slot: usize, inner: &str) -> Option<&str> {
        self.substitution_table
            .get(&(outer.into(), slot, inner.into()))
            .map(|s| s.as_str())
    }

    pub fn operations_of_arity(&self, arity: usize) -> Vec<&OperationDecl> {
        self.operations
            .iter()
            .filter(|op| op.arity() == arity)
            .collect()
    }
}

// BTreeMap iteration already orders these borrowed keys. Build once per diagnostic
// so nested searches avoid allocating two temporary String keys per lookup.
struct SubstitutionLookup<'a> {
    entries: Vec<((&'a str, usize, &'a str), &'a str)>,
}

impl<'a> SubstitutionLookup<'a> {
    fn new(theory: &'a LawvereTheory) -> Self {
        Self {
            entries: theory.substitution_table.iter()
                .map(|((outer, slot, inner), value)| ((outer.as_str(), *slot, inner.as_str()), value.as_str()))
                .collect(),
        }
    }

    fn get(&self, outer: &str, slot: usize, inner: &str) -> Option<&'a str> {
        self.entries.binary_search_by_key(&(outer, slot, inner), |(key, _)| *key)
            .ok().and_then(|index| self.entries.get(index)).map(|(_, value)| *value)
    }
}

/// Check h-in-g-in-f at slots j and i against g-in-f followed by h at i+j.
/// Each supplied case emits at most one diagnostic, in input order. Overflow is
/// refused before table lookup; absent entries (including both absent) fail.
/// No arity/sort admission is implied. O(S) borrowed index storage, O(C log S)
/// lookups for S table entries and C cases, plus returned diagnostic strings.
pub fn check_substitution_associativity(
    theory: &LawvereTheory,
    cases: &[(&str, usize, &str, usize, &str)],
) -> Vec<String> {
    let mut violations = Vec::new();
    let lookup = SubstitutionLookup::new(theory);
    for &(f, i, g, j, h) in cases {
        let Some(slot) = i.checked_add(j) else {
            violations.push(format!("Substitution slot overflow: i={}, j={}", i, j));
            continue;
        };
        let left = lookup.get(g, j, h).and_then(|gh| lookup.get(f, i, gh));
        let right = lookup.get(f, i, g).and_then(|fg| lookup.get(fg, slot, h));
        match (left, right) {
            (Some(l), Some(r)) if l == r => {}
            (Some(l), Some(r)) => violations.push(format!(
                "Substitution not associative: f={}, g={}, h={}: {}≠{}",
                f, g, h, l, r
            )),
            _ => violations.push(format!(
                "Substitution not defined for f={}, g={}, h={}",
                f, g, h
            )),
        }
    }
    violations
}

fn is_declared_idempotent(lookup: &SubstitutionLookup<'_>, op: &OperationDecl) -> bool {
    op.arity() == 1 && op.coarity() == 1 && lookup.get(&op.name, 0, &op.name) == Some(op.name.as_str())
}

fn splitting_pair(theory: &LawvereTheory, lookup: &SubstitutionLookup<'_>, name: &str,
                  r: &OperationDecl, s: &OperationDecl) -> bool {
    lookup.get(&s.name, 0, &r.name) == Some(name)
        && r.output_sorts.first().and_then(|sort| theory.identities.get(sort))
            .is_some_and(|identity| lookup.get(&r.name, 0, &s.name) == Some(identity.as_str()))
}

fn has_splitting(theory: &LawvereTheory, lookup: &SubstitutionLookup<'_>, name: &str) -> bool {
    theory.operations.iter().any(|r| {
        theory.operations.iter().any(|s| splitting_pair(theory, lookup, name, r, s))
    })
}

/// Inventory unary/co-unary self-idempotent names without a declared split pair.
/// Search all declared r,s, using only r's first output sort for its identity;
/// this deliberately retains raw-table behavior, not typed splitting admission.
/// Duplicates and input order are retained. No detected unsplit name is vacuous
/// `Complete`; neither this function nor its result updates stored status.
/// O(S) borrowed index plus O(N^3 log S) worst-case lookups for N operations.
pub fn check_theory_cauchy(theory: &LawvereTheory) -> TheoryCauchyStatus {
    let lookup = SubstitutionLookup::new(theory);
    let unsplit: Vec<String> = theory.operations.iter()
        .filter(|op| is_declared_idempotent(&lookup, op) && !has_splitting(theory, &lookup, &op.name))
        .map(|op| op.name.clone()).collect();
    if unsplit.is_empty() {
        TheoryCauchyStatus::Complete
    } else {
        TheoryCauchyStatus::Incomplete {
            unsplit_operations: unsplit,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn monoid_theory() {
        let mut t = LawvereTheory::new("Monoid");
        t.add_sort("M");
        t.add_operation(OperationDecl::new(
            "mul",
            vec!["M".into(), "M".into()],
            vec!["M".into()],
        ));
        t.add_operation(OperationDecl::new("unit", vec![], vec!["M".into()]));
        t.add_equation(EquationDecl::new(
            "assoc",
            "mul(mul(x,y),z)",
            "mul(x,mul(y,z))",
        ));
        assert_eq!(t.operations.len(), 2);
        assert_eq!(t.equations.len(), 1);
    }

    #[test]
    fn trivial_theory_cauchy() {
        let t = LawvereTheory::new("Empty");
        assert_eq!(check_theory_cauchy(&t), TheoryCauchyStatus::Complete);
    }
}
