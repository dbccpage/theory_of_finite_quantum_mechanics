"""Finite literal-set admission challenges; no source-derived expected oracle."""
from pathlib import Path


def challenge(record):
    return Path(__file__).with_name("finite_set_oracle.rs").read_text(encoding="utf-8")


def variants(record, source):
    recipes = [
        ("label-domain", "if self.label.trim().is_empty() {", "if false {"),
        ("element-domain", "if e.trim().is_empty() {", "if false {"),
        ("duplicate", "if !seen.insert(e) {", "if { seen.insert(e); false } {"),
        ("cardinality-binding", "if n != self.elements.len() {", "if false {"),
        ("owned-admission", "        declared.validate_shell()?;", "        let _ = declared.validate_shell();"),
        ("serde-admission", '#[serde(try_from = "FiniteSet", into = "FiniteSet")]', '#[serde(into = "FiniteSet")]'),
        ("label-observer", "        &self.declared.label", '        ""'),
        ("element-observer", "        &self.declared.elements", "        &self.declared.elements[..0]"),
        ("cardinality-observer", "        self.declared.cardinality()", "        0"),
        ("membership", "self.declared.elements.iter().any(|e| e == value)", "self.declared.elements.iter().all(|e| e == value)"),
        ("new-optional-bound", "declared_cardinality: Some(0)", "declared_cardinality: None"),
        ("with-elements-bound", "declared_cardinality: Some(n)", "declared_cardinality: Some(0)"),
        ("first-empty-index", "FiniteSetError::EmptyElement { index: i }", "FiniteSetError::EmptyElement { index: i + 1 }"),
        ("first-duplicate-index", "FiniteSetError::DuplicateElement { index: i }", "FiniteSetError::DuplicateElement { index: i + 1 }"),
        ("cardinality-payload", "                    declared: n,", "                    declared: 0,"),
        ("display-label", 'f.write_str("empty label")', 'f.write_str("wrong label")'),
        ("display-empty", '"empty element tag at index {index}"', '"wrong element tag at index {index}"'),
        ("display-duplicate", '"duplicate element tag at index {index}"', '"wrong duplicate at index {index}"'),
        ("display-cardinality", '"declared_cardinality {declared} != elements.len() {actual}"', '"wrong cardinality {declared} {actual}"'),
        ("raw-cardinality", "        self.elements.len()", "        0"),
    ]
    rows = []
    for identifier, needle, replacement in recipes:
        if source.count(needle) != 1:
            raise ValueError("Nonunique finite-set fault: " + identifier)
        rows.append(("FS-" + identifier,source.replace(needle,replacement,1),needle,replacement))
    return rows
