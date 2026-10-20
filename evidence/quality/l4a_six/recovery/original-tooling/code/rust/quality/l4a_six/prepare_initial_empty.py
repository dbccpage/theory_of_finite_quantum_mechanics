"""Prepare the categorical dual of the challenged terminal model; never activate it.

AuthorityEffect: None. The independent least-element oracle is dualized too.
"""
import subprocess
from replay import ROOT, RUST, digest, write
from scalar_port_faults import block


def once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after, 1)


def main():
    previous = ROOT / "evidence/quality/l4a_six/20261020-unit-cost-candidate/unit_type.rs"
    text = previous.read_bytes().decode("utf8")
    text = text[text.index("// Finite categorical interpretation:"):]
    text = text.replace("TerminalUnit", "InitialEmpty").replace("terminal_unit", "initial_empty")
    text = text.replace("UnitType", "EmptyType").replace("terminal", "initial")
    text = text.replace("categorical unit", "categorical empty object")
    text = text.replace("references inhabited", "references uninhabited")
    text = text.replace("from the identity to the constant initial functor", "from the constant initial functor to the identity")
    text = text.replace("has no arrow to proposed initial object", "has no arrow from proposed initial object")
    text = text.replace("to the proposed initial", "from the proposed initial")
    helper = block(text, "fn initial_empty_factor(")
    changed = helper.replace("source", "target").replace("category.hom(target, initial)?", "category.hom(initial, target)?")
    text = once(text, helper, changed)
    factor = block(text, "    pub fn factor(")
    text = once(text, factor, factor.replace("source", "target"))
    admission = block(text, "fn admit_initial_empty(")
    start = admission.index("    let bytes =")
    stop = admission.index('    initial_empty_limit("reference bytes"')
    updated = admission[:start] + "    let bytes = declaration.id.len();\n" + admission[stop:]
    text = once(text, admission, updated)
    coherence = block(text, "    pub fn coherence(")
    replacement = coherence.replace("let target_factor = self.factor(f.target)?;", "let source_factor = self.factor(f.source)?;")
    replacement = replacement.replace("compose(arrow, target_factor)? == self.factor(f.source)?", "compose(source_factor, arrow)? == self.factor(f.target)?")
    text = once(text, coherence, replacement)
    text = text.replace("Check f ; !target = !source", "Check initial_to_source ; f = initial_to_target")
    text = text.replace("unique arrow from source to the chosen initial object", "unique arrow from the chosen initial object to target")
    text = text.replace("Invalid\n    /// source identifiers", "Invalid\n    /// target identifiers")
    text = text.replace("greatest_element_oracle", "least_element_oracle")
    text = text.replace("Hom(x, initial)", "Hom(initial, x)")
    text = text.replace("relation[source * objects + initial]", "relation[initial * objects + source]")
    text = text.replace("(source, initial)", "(initial, source)")
    declaration = block(text, "    fn declaration()")
    text = once(text, declaration, '    fn declaration() -> EmptyType { EmptyType { id: "0".into() } }')
    test = block(text, "    fn independent_limits_query_domains_and_utf8_names_are_checked()")
    test = test.replace("max_reference_bytes: 2,", "max_reference_bytes: 1,")
    test = test.replace("max_reference_bytes: 1,\n                ..exact", "max_reference_bytes: 0,\n                ..exact")
    test = test.replace("&category,\n                1,", "&category,\n                0,")
    test = test.replace("&category, 1,", "&category, 0,")
    test = test.replace('            unit_term_ref: "*".into(),\n', "")
    test = test.replace("max_reference_bytes: 3,", "max_reference_bytes: 2,")
    test = test.replace("requested: 3,\n                limit: 2", "requested: 2,\n                limit: 1")
    text = once(text, block(text, "    fn independent_limits_query_domains_and_utf8_names_are_checked()"), test)
    out = ROOT / "evidence/quality/l4a_six/20261020-empty-candidate"
    out.mkdir()
    original = RUST / "src/homotopy_type_theory/empty_type.rs"
    (out / "before.rs").write_bytes(original.read_bytes())
    target = out / "empty_type.rs"
    target.write_bytes(original.read_bytes() + b"\n" + text.encode("utf8"))
    result = subprocess.run(["rustfmt", "--edition", "2021", str(target)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    write(out / "candidate.json", {"AuthorityEffect": "None", "status": "staged_not_activated_or_graded",
        "source": original.relative_to(ROOT).as_posix(), "origin_sha256": digest(original), "candidate_sha256": digest(target),
        "dual_source": {"path": previous.relative_to(ROOT).as_posix(), "sha256": digest(previous)},
        "scope": "Finite categorical initial-object universal property, not arbitrary HoTT uninhabitance. Needs its own oracle, boundary faults and metrics before activation."})
    print(out, flush=True)


if __name__ == "__main__":
    main()
