"""Designated finite Pi and terminal-unit faults; AuthorityEffect: None."""
from scalar_port_faults import block

def pi_recipes(source):
    entries = []
    def add(identity, prefix, before, after, mode="unit"):
        original = block(source, prefix)
        assert original.count(before) == 1, identity
        entries.append(dict(id=identity, before=original, after=original.replace(before, after, 1), mode=mode, outcome="unrun"))
    add("PI01-zero-fiber", "fn finite_pi_cardinality(", "if fibers.contains(&0) {", "if false {")
    add("PI02-cardinality-product", "fn finite_pi_cardinality(", ".checked_mul(*size)", ".checked_add(*size)")
    add("PI03-reference-limit", "    pub fn finite_model<'a>(", 'finite_pi_limit("reference bytes", bytes, limits.max_reference_bytes)?;', "")
    add("PI04-fiber-limit", "    pub fn finite_model<'a>(", 'finite_pi_limit("fibers", fiber_sizes.len(), limits.max_fibers)?;', "")
    add("PI05-cardinality-limit", "    pub fn finite_model<'a>(", 'finite_pi_limit("cardinality", cardinality, limits.max_cardinality)?;', "")
    add("PI06-admission-work", "    pub fn finite_model<'a>(", "finite_pi_work(fiber_sizes.len(), 4, limits.max_work)?;", "finite_pi_work(fiber_sizes.len(), 0, limits.max_work)?;")
    add("PI07-coordinate-boundary", "    fn admit_coordinates(", "if value >= size {", "if value > size {")
    add("PI08-empty-base", "fn finite_pi_cardinality(", "try_fold(1usize,", "try_fold(0usize,")
    add("PI09-rank-weight", "    pub fn rank(", "rank.checked_mul(size)", "rank.checked_add(size)")
    add("PI10-rank-arity", "    pub fn rank(", "self.arity(coordinates.len())?;", "")
    add("PI11-decode-arity", "    pub fn unrank_into(", "self.arity(output.len())?;", "")
    add("PI12-ordinal-boundary", "    pub fn unrank_into(", "if ordinal >= self.cardinality {", "if ordinal > self.cardinality {")
    add("PI13-output-digit", "    pub fn unrank_into(", "*slot = remaining % size;", "*slot = remaining / size;")
    add("PI14-output-quotient", "    pub fn unrank_into(", "remaining /= size;", "remaining %= size;")
    add("PI15-query-work", "    pub fn rank(", "finite_pi_work(self.fiber_sizes.len(), 6, self.limits.max_work)?;", "")
    add("PI16-model-privacy", "pub struct FinitePi<'a>", "    declaration: &'a PiType,\n    fiber_sizes: &'a [usize],\n    cardinality: usize,\n    limits: FinitePiLimits,", "    pub declaration: &'a PiType,\n    pub fiber_sizes: &'a [usize],\n    pub cardinality: usize,\n    pub limits: FinitePiLimits,", "doc")
    add("PI17-empty-product-query", "    pub fn rank(", "if self.cardinality == 0 {", "if false {")
    add("PI18-presentation-admission", "    pub fn finite_model<'a>(", "self.validate()?;", "")
    return entries


def unit_recipes(source):
    entries = []
    def add(identity, prefix, before, after, mode="unit"):
        original = block(source, prefix)
        assert original.count(before) == 1, identity
        entries.append(dict(id=identity, before=original, after=original.replace(before, after, 1), mode=mode, outcome="unrun"))
    model = "    pub fn terminal_model<'a>("
    admission = "fn admit_terminal_unit(" if "fn admit_terminal_unit(" in source else model
    add("UT01-object-admission", admission, "category.identity(terminal)?;", "")
    add("UT02-object-limit", admission, 'terminal_unit_limit("objects", category.object_count(), limits.max_objects)?;', "")
    add("UT03-arrow-limit", admission, 'terminal_unit_limit("arrows", category.arrows().len(), limits.max_arrows)?;', "")
    add("UT04-scan-work", admission, ".checked_mul(category.arrows().len())", ".checked_add(category.arrows().len())")
    uniqueness = block(source, "    if let Some((second, _)) = factors.next() {")
    add("UT05-factor-uniqueness", "fn terminal_unit_factor(", uniqueness, "")
    add("UT06-factor-existence", "fn terminal_unit_factor(", ".ok_or(TerminalUnitError::MissingFactor {\n            object: source,\n            terminal,\n        })?", ".unwrap_or(category.identity(source)?)")
    add("UT07-hom-direction", "fn terminal_unit_factor(", "category.hom(source, terminal)?", "category.hom(terminal, source)?")
    add("UT08-coherence-order", "    pub fn coherence(", "compose(arrow, target_factor)?", "compose(target_factor, arrow)?")
    add("UT09-coherence-equality", "    pub fn coherence(", "== self.factor(f.source)?", "!= self.factor(f.source)?")
    add("UT10-query-work", "    pub fn coherence(", ".checked_mul(2)", ".checked_mul(0)")
    add("UT11-reference-bytes", admission, 'terminal_unit_limit("reference bytes", bytes, limits.max_reference_bytes)?;', "")
    add("UT12-stored-policy", model, "            limits,\n        })", "            limits: TerminalUnitLimits::default(),\n        })")
    add("UT13-certificate-privacy", "pub struct TerminalUnit<'a>", "    declaration: &'a UnitType,\n    category: &'a FiniteCategory,\n    terminal: usize,\n    limits: TerminalUnitLimits,", "    pub declaration: &'a UnitType,\n    pub category: &'a FiniteCategory,\n    pub terminal: usize,\n    pub limits: TerminalUnitLimits,", "doc")
    add("UT14-presentation", model, "self.validate()?;", "")
    add("UT15-inclusive-limits", "fn terminal_unit_limit(", "if requested > limit {", "if requested >= limit {")
    add("UT16-factor-target", "    pub fn factor(", "terminal_unit_factor(self.category, source, self.terminal)", "terminal_unit_factor(self.category, source, source)")
    if ".checked_add(4)" in block(source, "    pub fn coherence("):
        add("UT17-transitive-read-cost", "    pub fn coherence(", ".checked_add(4)", ".checked_add(3)")
    return entries


