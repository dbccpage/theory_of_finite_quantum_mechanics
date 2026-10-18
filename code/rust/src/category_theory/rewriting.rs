//! Checked finite globular rewriting data. AuthorityEffect: None.
//!
//! The legacy Infinity names denote finite declarations, not an admitted
//! infinity-category. Admission checks names, generating rules, composable
//! nonempty paths, parallel 2-cell boundaries, higher globular boundaries,
//! and exact truncation. Formal inverse paths are admitted as path syntax.
//! Directed termination and local confluence use forward 1-cells only.
//! Termination certificates carry an independently checked decreasing rank.
//! No higher composition, coherence theorem or HoTT interpretation is claimed.

use std::collections::{BTreeMap, BTreeSet};
use std::sync::Arc;

// ═══════════════════════════════════════════════════════════════════════════
// 0-cells: Terms
// ═══════════════════════════════════════════════════════════════════════════

/// A term in the rewriting system. Identified by name.
#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Term(pub String);

impl Term {
    pub fn new(name: &str) -> Self {
        Self(name.into())
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// n-cells: RewriteCell
// ═══════════════════════════════════════════════════════════════════════════

/// An untrusted n-cell record in finite globular rewriting data.
///
/// - level 0: a term (0-cell)
/// - level 1: a rewrite step t ⟹ t' (1-cell)
/// - level 2: a rewrite equivalence between two 1-cell paths (2-cell)
/// - level n: coherence between (n-1)-cells
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct RewriteCell {
    /// The cell name (for audit/reference).
    pub name: String,
    /// Dimensional level: 0 = term, 1 = rewrite, 2 = equivalence, ...
    pub level: usize,
    /// Source (n-1)-cell name. Empty for 0-cells.
    pub source: Option<String>,
    /// Target (n-1)-cell name. Empty for 0-cells.
    pub target: Option<String>,
    /// The rewrite rule that generates this cell (if any).
    pub rule: Option<String>,
}

impl RewriteCell {
    /// Create a 0-cell (term).
    pub fn term(name: &str) -> Self {
        Self {
            name: name.into(),
            level: 0,
            source: None,
            target: None,
            rule: None,
        }
    }

    /// Create a 1-cell (rewrite step).
    pub fn rewrite(name: &str, from: &str, to: &str, rule: &str) -> Self {
        Self {
            name: name.into(),
            level: 1,
            source: Some(from.into()),
            target: Some(to.into()),
            rule: Some(rule.into()),
        }
    }

    /// Create an n-cell (higher coherence).
    pub fn higher(name: &str, level: usize, from: &str, to: &str) -> Self {
        Self {
            name: name.into(),
            level,
            source: Some(from.into()),
            target: Some(to.into()),
            rule: None,
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// RewriteRule
// ═══════════════════════════════════════════════════════════════════════════

/// A generating rewrite rule: lhs ⟹ rhs.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RewriteRule {
    pub name: String,
    pub lhs: String,
    pub rhs: String,
}

impl RewriteRule {
    pub fn new(name: &str, lhs: &str, rhs: &str) -> Self {
        Self {
            name: name.into(),
            lhs: lhs.into(),
            rhs: rhs.into(),
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// RewritePath — a composite 1-cell
// ═══════════════════════════════════════════════════════════════════════════

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PathStep {
    Forward(String),
    Inverse(String),
}

/// A rewrite path: a sequence of 1-cells composed end-to-end.
///
/// source(path) = source(steps[0])
/// target(path) = target(steps[last])
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RewritePath {
    pub name: String,
    pub steps: Vec<PathStep>,
}

impl RewritePath {
    /// A candidate path with a default name separate from its generating cell.
    /// Admission still rejects collisions with caller-chosen names.
    pub fn single(cell_name: &str) -> Self {
        Self {
            name: format!("path:{cell_name}"),
            steps: vec![PathStep::Forward(cell_name.into())],
        }
    }

    pub fn named_single(path_name: &str, cell_name: &str) -> Self {
        Self {
            name: path_name.into(),
            steps: vec![PathStep::Forward(cell_name.into())],
        }
    }

    pub fn compose(name: &str, steps: Vec<PathStep>) -> Self {
        Self {
            name: name.into(),
            steps,
        }
    }

    pub fn len(&self) -> usize {
        self.steps.len()
    }

    pub fn is_empty(&self) -> bool {
        self.steps.is_empty()
    }

    pub fn inverse(&self, new_name: &str) -> Self {
        let mut rev_steps = self.steps.clone();
        rev_steps.reverse();
        let inverted = rev_steps
            .into_iter()
            .map(|step| match step {
                PathStep::Forward(s) => PathStep::Inverse(s),
                PathStep::Inverse(s) => PathStep::Forward(s),
            })
            .collect();
        Self {
            name: new_name.into(),
            steps: inverted,
        }
    }

    pub fn concat(&self, other: &Self, new_name: &str) -> Self {
        let mut new_steps = self.steps.clone();
        new_steps.extend(other.steps.clone());
        Self {
            name: new_name.into(),
            steps: new_steps,
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Normal Form Witness
// ═══════════════════════════════════════════════════════════════════════════

/// Owned evidence of no outgoing forward 1-cell in one admitted finite system.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NormalFormWitness {
    term: String,
    system: Arc<ValidatedInfinityRewriteSystem>,
}

impl NormalFormWitness {
    pub fn term(&self) -> &str {
        &self.term
    }
    pub fn system(&self) -> &ValidatedInfinityRewriteSystem {
        &self.system
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// InfinityRewriteSystem — the main structure
// ═══════════════════════════════════════════════════════════════════════════

/// Candidate finite globular rewriting data, with a legacy type name.
///
/// Contains cells at all declared levels, rewrite rules, and
/// composition/homotopy data.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InfinityRewriteSystem {
    pub name: String,
    /// All cells, keyed by name.
    pub cells: BTreeMap<String, RewriteCell>,
    /// Generating rewrite rules (produce 1-cells).
    pub rules: Vec<RewriteRule>,
    /// Declared rewrite paths (composite 1-cells).
    pub paths: Vec<RewritePath>,
    /// 2-cells: homotopies between paths. Key = 2-cell name.
    /// The 2-cell's source/target are path names.
    pub homotopies: BTreeMap<String, (String, String)>,
    /// Maximum declared cell level.
    pub truncation_level: usize,
}

impl InfinityRewriteSystem {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.into(),
            cells: BTreeMap::new(),
            rules: Vec::new(),
            paths: Vec::new(),
            homotopies: BTreeMap::new(),
            truncation_level: 0,
        }
    }

    pub fn add_term(&mut self, name: &str) {
        self.cells.insert(name.into(), RewriteCell::term(name));
    }

    pub fn add_rule(&mut self, rule_name: &str, lhs: &str, rhs: &str) {
        self.rules.push(RewriteRule::new(rule_name, lhs, rhs));
        let cell = RewriteCell::rewrite(rule_name, lhs, rhs, rule_name);
        self.cells.insert(rule_name.into(), cell);
        if self.truncation_level < 1 {
            self.truncation_level = 1;
        }
    }

    pub fn add_path(&mut self, path: RewritePath) {
        self.paths.push(path);
    }

    pub fn add_homotopy(&mut self, name: &str, path_a: &str, path_b: &str) {
        let cell = RewriteCell::higher(name, 2, path_a, path_b);
        self.cells.insert(name.into(), cell);
        self.homotopies
            .insert(name.into(), (path_a.into(), path_b.into()));
        if self.truncation_level < 2 {
            self.truncation_level = 2;
        }
    }

    pub fn add_higher_cell(&mut self, name: &str, level: usize, from: &str, to: &str) {
        let cell = RewriteCell::higher(name, level, from, to);
        self.cells.insert(name.into(), cell);
        if self.truncation_level < level {
            self.truncation_level = level;
        }
    }

    pub fn cells_at_level(&self, level: usize) -> Vec<&RewriteCell> {
        self.cells.values().filter(|c| c.level == level).collect()
    }

    pub fn terms(&self) -> Vec<&RewriteCell> {
        self.cells_at_level(0)
    }

    pub fn rewrites(&self) -> Vec<&RewriteCell> {
        self.cells_at_level(1)
    }

    /// Raw syntactic diagnostic: a level-0 key with no outgoing 1-cell.
    /// This does not attest admission of the surrounding declaration.
    pub fn is_normal_form(&self, term: &str) -> bool {
        self.is_term(term)
            && !self
                .rewrites()
                .iter()
                .any(|r| r.source.as_deref() == Some(term))
    }

    fn is_term(&self, term: &str) -> bool {
        self.cells.get(term).is_some_and(|cell| cell.level == 0)
    }

    /// Admission precedes witness creation; caller-owned declarations are cloned.
    pub fn normal_form_witness(
        &self,
        term: &str,
    ) -> Result<Option<NormalFormWitness>, Vec<RewriteError>> {
        Ok(ValidatedInfinityRewriteSystem::validate(self.clone())?.normal_form_witness(term))
    }

    /// Boundary of a nonempty, composable formal path. A dangling boundary or
    /// a step with the wrong dimension returns None, even on raw declarations.
    pub fn path_boundary(&self, path: &RewritePath) -> Option<(String, String)> {
        let (first, rest) = path.steps.split_first()?;
        let (source, mut target) = self.step_boundary(first)?;
        for step in rest {
            let (next_source, next_target) = self.step_boundary(step)?;
            if target != next_source {
                return None;
            }
            target = next_target;
        }
        Some((source, target))
    }

    fn step_boundary(&self, step: &PathStep) -> Option<(String, String)> {
        let (name, inverse) = match step {
            PathStep::Forward(name) => (name, false),
            PathStep::Inverse(name) => (name, true),
        };
        let cell = self.cells.get(name)?;
        let (source, target) = self.rewrite_boundary(cell)?;
        if inverse {
            Some((target, source))
        } else {
            Some((source, target))
        }
    }

    fn rewrite_boundary(&self, cell: &RewriteCell) -> Option<(String, String)> {
        if cell.level != 1 {
            return None;
        }
        let source = cell.source.as_ref()?;
        let target = cell.target.as_ref()?;
        if !self.is_term(source) || !self.is_term(target) {
            return None;
        }
        Some((source.clone(), target.clone()))
    }

    pub fn whisker_left(
        &mut self,
        name: &str,
        path: &str,
        homotopy: &str,
    ) -> Result<(), Vec<RewriteError>> {
        let next = self.whisker_candidate(name, path, homotopy, true)?;
        *self = next;
        Ok(())
    }

    pub fn whisker_right(
        &mut self,
        name: &str,
        homotopy: &str,
        path: &str,
    ) -> Result<(), Vec<RewriteError>> {
        let next = self.whisker_candidate(name, path, homotopy, false)?;
        *self = next;
        Ok(())
    }

    fn named_path(&self, name: &str) -> Result<&RewritePath, Vec<RewriteError>> {
        self.paths
            .iter()
            .find(|p| p.name == name)
            .ok_or_else(|| vec![problem(RewriteInvariant::Path, name)])
    }

    fn homotopy_paths(
        &self,
        name: &str,
    ) -> Result<(&RewritePath, &RewritePath), Vec<RewriteError>> {
        let (a, b) = self
            .homotopies
            .get(name)
            .ok_or_else(|| vec![problem(RewriteInvariant::Homotopy, name)])?;
        Ok((self.named_path(a)?, self.named_path(b)?))
    }

    fn require_join(
        &self,
        first: &RewritePath,
        second: &RewritePath,
    ) -> Result<(), Vec<RewriteError>> {
        let a = self
            .path_boundary(first)
            .ok_or_else(|| vec![problem(RewriteInvariant::Path, &first.name)])?;
        let b = self
            .path_boundary(second)
            .ok_or_else(|| vec![problem(RewriteInvariant::Path, &second.name)])?;
        if a.1 != b.0 {
            return Err(vec![problem(RewriteInvariant::Composition, &first.name)]);
        }
        Ok(())
    }

    fn whisker_candidate(
        &self,
        name: &str,
        path: &str,
        homotopy: &str,
        left: bool,
    ) -> Result<Self, Vec<RewriteError>> {
        validate_records(self)?;
        let (a, b) = self.homotopy_paths(homotopy)?;
        let p = self.named_path(path)?;
        let (first, second) = if left { (p, a) } else { (a, p) };
        self.require_join(first, second)?;
        let pa = whiskered_path(p, a, left);
        let pb = whiskered_path(p, b, left);
        self.extend_whiskered_homotopy(name, pa, pb)
    }

    fn extend_whiskered_homotopy(
        &self,
        name: &str,
        pa: RewritePath,
        pb: RewritePath,
    ) -> Result<Self, Vec<RewriteError>> {
        let mut names = vec![name, pa.name.as_str()];
        if pa != pb {
            names.push(&pb.name);
        }
        self.reserve_names(&names)?;
        let mut next = self.clone();
        next.add_path(pa.clone());
        if pa != pb {
            next.add_path(pb.clone());
        }
        next.add_homotopy(name, &pa.name, &pb.name);
        validate_records(&next)?;
        Ok(next)
    }

    fn reserve_names(&self, names: &[&str]) -> Result<(), Vec<RewriteError>> {
        let mut seen: BTreeSet<&str> = self.cells.keys().map(String::as_str).collect();
        seen.extend(self.paths.iter().map(|p| p.name.as_str()));
        for name in names {
            if name.trim().is_empty() || !seen.insert(name) {
                return Err(vec![problem(RewriteInvariant::Name, name)]);
            }
        }
        Ok(())
    }
}

fn whiskered_path(path: &RewritePath, branch: &RewritePath, left: bool) -> RewritePath {
    let (first, second) = if left { (path, branch) } else { (branch, path) };
    first.concat(second, &format!("{}_{}", first.name, second.name))
}

/// Admission and analysis failure classes. Candidate records are not certificates.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RewriteInvariant {
    Name,
    CellKey,
    Term,
    Rule,
    Edge,
    Path,
    Homotopy,
    GlobularBoundary,
    Truncation,
    Composition,
    NonJoinable,
    Cycle,
    RankDomain,
    RankDescent,
    Capacity,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RewriteError {
    pub invariant: RewriteInvariant,
    pub subject: String,
}

impl std::fmt::Display for RewriteError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}: {}", self.invariant, self.subject)
    }
}
impl std::error::Error for RewriteError {}

fn problem(invariant: RewriteInvariant, subject: &str) -> RewriteError {
    RewriteError {
        invariant,
        subject: subject.into(),
    }
}

/// Immutable, owned admission of finite globular data. Does not claim a complete
/// infinity-category. All graph certificates and witnesses retain this context.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedInfinityRewriteSystem {
    declared: InfinityRewriteSystem,
}

impl ValidatedInfinityRewriteSystem {
    pub fn validate(sys: InfinityRewriteSystem) -> Result<Self, Vec<RewriteError>> {
        validate_records(&sys)?;
        Ok(Self { declared: sys })
    }
    pub fn declared(&self) -> &InfinityRewriteSystem {
        &self.declared
    }

    pub fn normal_form_witness(&self, term: &str) -> Option<NormalFormWitness> {
        if !self.declared.is_normal_form(term) {
            return None;
        }
        Some(NormalFormWitness {
            term: term.into(),
            system: Arc::new(self.clone()),
        })
    }
    pub fn termination_certificate(&self) -> Result<TerminationCertificate, RewriteError> {
        let ranks = ForwardGraph::new(self).decreasing_ranks()?;
        self.admit_termination_ranks(ranks)
    }
    /// Separate checker: exact term domain and strict descent on every edge.
    /// No topological-sort result is trusted by this admission path.
    pub fn admit_termination_ranks(
        &self,
        ranks: BTreeMap<String, usize>,
    ) -> Result<TerminationCertificate, RewriteError> {
        check_rank_domain(self, &ranks)?;
        check_rank_descent(self, &ranks)?;
        Ok(TerminationCertificate {
            system: Arc::new(self.clone()),
            ranks,
        })
    }
    pub fn whisker_left(
        &self,
        name: &str,
        path: &str,
        homotopy: &str,
    ) -> Result<Self, Vec<RewriteError>> {
        Self::validate(
            self.declared
                .whisker_candidate(name, path, homotopy, true)?,
        )
    }
    pub fn whisker_right(
        &self,
        name: &str,
        homotopy: &str,
        path: &str,
    ) -> Result<Self, Vec<RewriteError>> {
        Self::validate(
            self.declared
                .whisker_candidate(name, path, homotopy, false)?,
        )
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TerminationCertificate {
    system: Arc<ValidatedInfinityRewriteSystem>,
    ranks: BTreeMap<String, usize>,
}
impl TerminationCertificate {
    pub fn system(&self) -> &ValidatedInfinityRewriteSystem {
        &self.system
    }
    pub fn ranks(&self) -> &BTreeMap<String, usize> {
        &self.ranks
    }
}

fn check_rank_domain(
    sys: &ValidatedInfinityRewriteSystem,
    ranks: &BTreeMap<String, usize>,
) -> Result<(), RewriteError> {
    let terms = sys
        .declared
        .cells
        .iter()
        .filter(|(_, c)| c.level == 0)
        .map(|(name, _)| name);
    if !ranks.keys().eq(terms) {
        return Err(problem(RewriteInvariant::RankDomain, &sys.declared.name));
    }
    Ok(())
}

fn check_rank_descent(
    sys: &ValidatedInfinityRewriteSystem,
    ranks: &BTreeMap<String, usize>,
) -> Result<(), RewriteError> {
    for edge in sys.declared.rewrites() {
        let (source, target) = cell_ends(edge)?;
        let a = ranks
            .get(source)
            .ok_or_else(|| problem(RewriteInvariant::RankDomain, source))?;
        let b = ranks
            .get(target)
            .ok_or_else(|| problem(RewriteInvariant::RankDomain, target))?;
        if a <= b {
            return Err(problem(RewriteInvariant::RankDescent, &edge.name));
        }
    }
    Ok(())
}

fn validate_records(sys: &InfinityRewriteSystem) -> Result<(), Vec<RewriteError>> {
    let mut errors = check_names(sys);
    errors.extend(check_rules(sys));
    let rules: RuleIndex<'_> = sys.rules.iter().map(|r| (r.name.as_str(), r)).collect();
    for (key, cell) in &sys.cells {
        if let Err(err) = check_cell(sys, &rules, key, cell) {
            errors.push(err);
        }
    }
    errors.extend(check_paths(sys));
    errors.extend(check_homotopies(sys));
    let max_level = sys.cells.values().map(|cell| cell.level).max().unwrap_or(0);
    if sys.truncation_level != max_level {
        errors.push(problem(RewriteInvariant::Truncation, &sys.name));
    }
    if errors.is_empty() {
        Ok(())
    } else {
        Err(errors)
    }
}

fn check_names(sys: &InfinityRewriteSystem) -> Vec<RewriteError> {
    let mut errors = Vec::new();
    let mut names = BTreeSet::new();
    if sys.name.trim().is_empty() {
        errors.push(problem(RewriteInvariant::Name, &sys.name));
    }
    for name in sys.cells.keys().chain(sys.paths.iter().map(|p| &p.name)) {
        if name.trim().is_empty() || !names.insert(name) {
            errors.push(problem(RewriteInvariant::Name, name));
        }
    }
    errors
}

fn check_rules(sys: &InfinityRewriteSystem) -> Vec<RewriteError> {
    let mut seen = BTreeSet::new();
    let mut errors = Vec::new();
    for rule in &sys.rules {
        if rule.name.trim().is_empty() || !seen.insert(&rule.name) {
            errors.push(problem(RewriteInvariant::Rule, &rule.name));
        }
        if let Err(err) = check_rule(sys, rule) {
            errors.push(err);
        }
    }
    errors
}

fn check_rule(sys: &InfinityRewriteSystem, rule: &RewriteRule) -> Result<(), RewriteError> {
    require_term(sys, &rule.lhs)?;
    require_term(sys, &rule.rhs)?;
    let cell = sys
        .cells
        .get(&rule.name)
        .ok_or_else(|| problem(RewriteInvariant::Rule, &rule.name))?;
    if cell.level != 1
        || cell.rule.as_deref() != Some(&rule.name)
        || cell.source.as_deref() != Some(&rule.lhs)
        || cell.target.as_deref() != Some(&rule.rhs)
    {
        return Err(problem(RewriteInvariant::Rule, &rule.name));
    }
    Ok(())
}

fn require_term(sys: &InfinityRewriteSystem, name: &str) -> Result<(), RewriteError> {
    if !sys.is_term(name) {
        return Err(problem(RewriteInvariant::Term, name));
    }
    Ok(())
}

fn cell_ends(cell: &RewriteCell) -> Result<(&str, &str), RewriteError> {
    let source = cell
        .source
        .as_deref()
        .ok_or_else(|| problem(RewriteInvariant::GlobularBoundary, &cell.name))?;
    let target = cell
        .target
        .as_deref()
        .ok_or_else(|| problem(RewriteInvariant::GlobularBoundary, &cell.name))?;
    Ok((source, target))
}

type RuleIndex<'a> = BTreeMap<&'a str, &'a RewriteRule>;

fn check_cell(
    sys: &InfinityRewriteSystem,
    rules: &RuleIndex<'_>,
    key: &str,
    cell: &RewriteCell,
) -> Result<(), RewriteError> {
    if key != cell.name {
        return Err(problem(RewriteInvariant::CellKey, key));
    }
    match cell.level {
        0 => check_term(cell),
        1 => check_edge(sys, rules, cell),
        2 => check_two_cell(sys, cell),
        _ => check_higher_cell(sys, cell),
    }
}

fn check_term(cell: &RewriteCell) -> Result<(), RewriteError> {
    if cell.source.is_some() || cell.target.is_some() || cell.rule.is_some() {
        return Err(problem(RewriteInvariant::Term, &cell.name));
    }
    Ok(())
}

fn check_edge(
    sys: &InfinityRewriteSystem,
    rules: &RuleIndex<'_>,
    cell: &RewriteCell,
) -> Result<(), RewriteError> {
    let (source, target) = cell_ends(cell)?;
    require_term(sys, source)?;
    require_term(sys, target)?;
    let rule = cell
        .rule
        .as_deref()
        .and_then(|name| rules.get(name))
        .ok_or_else(|| problem(RewriteInvariant::Rule, &cell.name))?;
    if rule.lhs != source || rule.rhs != target {
        return Err(problem(RewriteInvariant::Edge, &cell.name));
    }
    Ok(())
}

fn check_two_cell(sys: &InfinityRewriteSystem, cell: &RewriteCell) -> Result<(), RewriteError> {
    let (source, target) = cell_ends(cell)?;
    let expected: (String, String) = (source.into(), target.into());
    if cell.rule.is_some() || sys.homotopies.get(&cell.name) != Some(&expected) {
        return Err(problem(RewriteInvariant::Homotopy, &cell.name));
    }
    let a = sys
        .named_path(source)
        .map_err(|_| problem(RewriteInvariant::Path, source))?;
    let b = sys
        .named_path(target)
        .map_err(|_| problem(RewriteInvariant::Path, target))?;
    let bound = sys
        .path_boundary(a)
        .ok_or_else(|| problem(RewriteInvariant::Path, source))?;
    if Some(bound) != sys.path_boundary(b) {
        return Err(problem(RewriteInvariant::GlobularBoundary, &cell.name));
    }
    Ok(())
}

fn check_higher_cell(sys: &InfinityRewriteSystem, cell: &RewriteCell) -> Result<(), RewriteError> {
    let (source, target) = cell_ends(cell)?;
    let a = sys
        .cells
        .get(source)
        .ok_or_else(|| problem(RewriteInvariant::GlobularBoundary, source))?;
    let b = sys
        .cells
        .get(target)
        .ok_or_else(|| problem(RewriteInvariant::GlobularBoundary, target))?;
    check_higher_dimension(cell, a, b)?;
    if a.source != b.source || a.target != b.target {
        return Err(problem(RewriteInvariant::GlobularBoundary, &cell.name));
    }
    Ok(())
}

fn check_higher_dimension(
    cell: &RewriteCell,
    a: &RewriteCell,
    b: &RewriteCell,
) -> Result<(), RewriteError> {
    let expected = cell
        .level
        .checked_sub(1)
        .ok_or_else(|| problem(RewriteInvariant::GlobularBoundary, &cell.name))?;
    if cell.rule.is_some() || a.level != expected || b.level != expected {
        return Err(problem(RewriteInvariant::GlobularBoundary, &cell.name));
    }
    Ok(())
}

fn check_paths(sys: &InfinityRewriteSystem) -> Vec<RewriteError> {
    sys.paths
        .iter()
        .filter(|p| sys.path_boundary(p).is_none())
        .map(|p| problem(RewriteInvariant::Path, &p.name))
        .collect()
}

fn check_homotopies(sys: &InfinityRewriteSystem) -> Vec<RewriteError> {
    let mut errors = Vec::new();
    for name in sys.homotopies.keys() {
        if !sys.cells.get(name).is_some_and(|c| c.level == 2) {
            errors.push(problem(RewriteInvariant::Homotopy, name));
        }
    }
    errors
}

/// Forward finite graph only. Inverse path syntax and homotopies cannot change
/// directed reduction, termination or directed local confluence.
struct ForwardGraph<'a> {
    adjacent: BTreeMap<&'a str, BTreeSet<&'a str>>,
}

impl<'a> ForwardGraph<'a> {
    fn new(sys: &'a ValidatedInfinityRewriteSystem) -> Self {
        let mut adjacent: BTreeMap<_, BTreeSet<_>> = sys
            .declared
            .terms()
            .iter()
            .map(|c| (c.name.as_str(), BTreeSet::new()))
            .collect();
        for cell in sys.declared.rewrites() {
            if let (Some(source), Some(target)) = (cell.source.as_deref(), cell.target.as_deref()) {
                adjacent.entry(source).or_default().insert(target);
            }
        }
        Self { adjacent }
    }
    fn reachable(&self, start: &'a str) -> BTreeSet<&'a str> {
        let mut reached = BTreeSet::new();
        let mut stack = vec![start];
        while let Some(node) = stack.pop() {
            if !reached.insert(node) {
                continue;
            }
            if let Some(next) = self.adjacent.get(node) {
                stack.extend(next.iter().copied());
            }
        }
        reached
    }
    fn check_pair(&self, source: &str, a: &'a str, b: &'a str) -> Option<RewriteError> {
        let left = self.reachable(a);
        let right = self.reachable(b);
        if !left.is_disjoint(&right) {
            return None;
        }
        Some(problem(
            RewriteInvariant::NonJoinable,
            &format!("{source}: {a}, {b}"),
        ))
    }
    fn check_fork(&self, source: &str, targets: &BTreeSet<&'a str>) -> Vec<RewriteError> {
        let mut errors = Vec::new();
        for (i, a) in targets.iter().enumerate() {
            for b in targets.iter().skip(i + 1) {
                if let Some(err) = self.check_pair(source, a, b) {
                    errors.push(err);
                }
            }
        }
        errors
    }
    fn confluence_errors(&self) -> Vec<RewriteError> {
        let mut errors = Vec::new();
        for (source, targets) in &self.adjacent {
            errors.extend(self.check_fork(source, targets));
        }
        errors
    }
    /// Kahn's algorithm uses an explicit work set, never recursion. O(V+E)
    /// graph visits with BTreeMap/BTreeSet logarithmic lookup factors.
    fn decreasing_ranks(&self) -> Result<BTreeMap<String, usize>, RewriteError> {
        let mut indegree = self.indegrees()?;
        let mut ready: BTreeSet<_> = indegree
            .iter()
            .filter(|(_, n)| **n == 0)
            .map(|(v, _)| *v)
            .collect();
        let mut order = Vec::new();
        while let Some(node) = ready.pop_first() {
            order.push(node);
            self.drain_edges(node, &mut indegree, &mut ready)?;
        }
        if order.len() != self.adjacent.len() {
            return Err(problem(RewriteInvariant::Cycle, "forward graph"));
        }
        Ok(order
            .into_iter()
            .rev()
            .enumerate()
            .map(|(rank, node)| (node.into(), rank))
            .collect())
    }
    fn indegrees(&self) -> Result<BTreeMap<&'a str, usize>, RewriteError> {
        let mut counts: BTreeMap<_, usize> = self.adjacent.keys().map(|node| (*node, 0)).collect();
        for targets in self.adjacent.values() {
            for target in targets {
                let count = counts
                    .get_mut(target)
                    .ok_or_else(|| problem(RewriteInvariant::Term, target))?;
                *count = count
                    .checked_add(1)
                    .ok_or_else(|| problem(RewriteInvariant::Capacity, target))?;
            }
        }
        Ok(counts)
    }
    fn drain_edges(
        &self,
        node: &str,
        indegree: &mut BTreeMap<&'a str, usize>,
        ready: &mut BTreeSet<&'a str>,
    ) -> Result<(), RewriteError> {
        let Some(targets) = self.adjacent.get(node) else {
            return Ok(());
        };
        for target in targets {
            let count = indegree
                .get_mut(target)
                .ok_or_else(|| problem(RewriteInvariant::Term, target))?;
            *count = count
                .checked_sub(1)
                .ok_or_else(|| problem(RewriteInvariant::Capacity, target))?;
            if *count == 0 {
                ready.insert(target);
            }
        }
        Ok(())
    }
}

/// Raw entry points fail closed on malformed declarations before graph analysis.
pub fn check_local_confluence(sys: &InfinityRewriteSystem) -> Vec<RewriteError> {
    match ValidatedInfinityRewriteSystem::validate(sys.clone()) {
        Ok(checked) => ForwardGraph::new(&checked).confluence_errors(),
        Err(errors) => errors,
    }
}

pub fn check_termination(sys: &InfinityRewriteSystem) -> Vec<RewriteError> {
    match ValidatedInfinityRewriteSystem::validate(sys.clone()) {
        Ok(checked) => checked
            .termination_certificate()
            .err()
            .into_iter()
            .collect(),
        Err(errors) => errors,
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InfinityCategorySummary {
    pub n_terms: usize,
    pub n_rewrites: usize,
    pub n_homotopies: usize,
    pub n_higher_cells: usize,
    pub truncation_level: usize,
    pub is_locally_confluent: bool,
    pub is_terminating: bool,
}

pub fn summarize(
    sys: &InfinityRewriteSystem,
) -> Result<InfinityCategorySummary, Vec<RewriteError>> {
    let checked = ValidatedInfinityRewriteSystem::validate(sys.clone())?;
    Ok(InfinityCategorySummary {
        n_terms: sys.terms().len(),
        n_rewrites: sys.rewrites().len(),
        n_homotopies: sys.homotopies.len(),
        n_higher_cells: sys.cells.values().filter(|c| c.level > 2).count(),
        truncation_level: sys.truncation_level,
        is_locally_confluent: ForwardGraph::new(&checked).confluence_errors().is_empty(),
        is_terminating: checked.termination_certificate().is_ok(),
    })
}

// ═══════════════════════════════════════════════════════════════════════════
// Tests
// ═══════════════════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    fn arrow_system() -> InfinityRewriteSystem {
        let mut sys = InfinityRewriteSystem::new("arrow");
        sys.add_term("a");
        sys.add_term("b");
        sys.add_rule("r", "a", "b");
        sys.add_path(RewritePath::named_single("p", "r"));
        sys
    }

    #[test]
    fn default_single_path_names_do_not_collide_with_their_cells() {
        let mut sys = arrow_system();
        let path = RewritePath::single("r");
        assert_ne!(path.name, "r");
        assert_eq!(sys.path_boundary(&path), Some(("a".into(), "b".into())));
        sys.add_path(path);
        assert!(ValidatedInfinityRewriteSystem::validate(sys).is_ok());
    }

    #[test]
    fn admission_rejects_inconsistent_cell_and_rule_records() {
        let base = arrow_system();
        let mut cases = Vec::new();
        let mut sys = base.clone();
        sys.cells.get_mut("a").unwrap().source = Some("b".into());
        cases.push(("term boundary", sys));
        let mut sys = base.clone();
        sys.cells.get_mut("a").unwrap().rule = Some("r".into());
        cases.push(("term rule", sys));
        let mut sys = base.clone();
        sys.cells.get_mut("r").unwrap().name = "different".into();
        cases.push(("map key", sys));
        let mut sys = base.clone();
        sys.cells.get_mut("r").unwrap().rule = Some("missing".into());
        cases.push(("missing rule", sys));
        let mut sys = base.clone();
        sys.rules[0].lhs = "b".into();
        cases.push(("rule boundary", sys));
        let mut sys = base.clone();
        sys.rules.push(sys.rules[0].clone());
        cases.push(("duplicate rule", sys));
        let mut sys = base.clone();
        sys.rules.push(RewriteRule::new("ghost", "a", "b"));
        cases.push(("missing generated cell", sys));
        let mut sys = base.clone();
        sys.cells
            .insert("extra".into(), RewriteCell::rewrite("extra", "b", "a", "r"));
        cases.push(("extra edge contradicts its rule", sys));
        for (reason, sys) in cases {
            assert!(
                ValidatedInfinityRewriteSystem::validate(sys).is_err(),
                "admitted {reason}"
            );
        }
    }

    #[test]
    fn all_name_path_and_truncation_boundaries_reject_bad_candidates() {
        let base = arrow_system();
        let mut cases = Vec::new();
        let mut sys = base.clone();
        sys.name.clear();
        cases.push(sys);
        let mut sys = base.clone();
        sys.add_term(" ");
        cases.push(sys);
        let mut sys = base.clone();
        sys.paths.push(sys.paths[0].clone());
        cases.push(sys);
        let mut sys = base.clone();
        sys.paths[0].name = "a".into();
        cases.push(sys);
        let mut sys = base.clone();
        sys.paths[0].steps.clear();
        cases.push(sys);
        let mut sys = base.clone();
        sys.paths[0].steps = vec![PathStep::Forward("a".into())];
        cases.push(sys);
        let mut sys = base.clone();
        sys.paths[0].steps = vec![PathStep::Forward("missing".into())];
        cases.push(sys);
        let mut sys = base.clone();
        sys.cells.get_mut("r").unwrap().source = None;
        cases.push(sys);
        let mut sys = base.clone();
        sys.cells.get_mut("r").unwrap().target = None;
        cases.push(sys);
        let mut sys = base.clone();
        sys.truncation_level = 0;
        cases.push(sys);
        let mut sys = base.clone();
        sys.add_higher_cell("h", usize::MAX, "missing", "missing");
        cases.push(sys);
        let mut sys = base;
        sys.add_higher_cell("h", 2, "p", "p");
        cases.push(sys);
        for (i, sys) in cases.into_iter().enumerate() {
            assert!(
                ValidatedInfinityRewriteSystem::validate(sys).is_err(),
                "boundary {i}"
            );
        }
    }

    #[test]
    fn admission_binds_two_cells_and_homotopy_data_in_both_directions() {
        let mut base = arrow_system();
        base.add_homotopy("h", "p", "p");
        let mut missing_map = base.clone();
        missing_map.homotopies.clear();
        assert!(ValidatedInfinityRewriteSystem::validate(missing_map).is_err());
        let mut missing_cell = base.clone();
        missing_cell.cells.remove("h");
        missing_cell.truncation_level = 1;
        assert!(ValidatedInfinityRewriteSystem::validate(missing_cell).is_err());
        let mut mismatch = base;
        mismatch.add_path(RewritePath::named_single("q", "r"));
        mismatch
            .homotopies
            .insert("h".into(), ("q".into(), "q".into()));
        assert!(ValidatedInfinityRewriteSystem::validate(mismatch).is_err());
    }

    #[test]
    fn inverse_paths_cannot_prove_directed_local_confluence() {
        let mut sys = InfinityRewriteSystem::new("fork");
        for term in ["a", "b", "c"] {
            sys.add_term(term);
        }
        sys.add_rule("ab", "a", "b");
        sys.add_rule("ac", "a", "c");
        sys.add_path(RewritePath::named_single("p", "ab"));
        sys.add_path(RewritePath::compose(
            "q",
            vec![
                PathStep::Forward("ac".into()),
                PathStep::Inverse("ac".into()),
                PathStep::Forward("ab".into()),
            ],
        ));
        sys.add_homotopy("h", "p", "q");
        assert!(ValidatedInfinityRewriteSystem::validate(sys.clone()).is_ok());
        assert!(
            !check_local_confluence(&sys).is_empty(),
            "b and c have no common forward reduct"
        );
    }

    fn graph_system(edges: &[[bool; 3]; 3]) -> InfinityRewriteSystem {
        let mut sys = InfinityRewriteSystem::new("three vertices");
        for i in 0..3 {
            sys.add_term(&i.to_string());
        }
        for (i, row) in edges.iter().enumerate() {
            for (j, edge) in row.iter().enumerate() {
                if *edge {
                    sys.add_rule(&format!("e{i}{j}"), &i.to_string(), &j.to_string());
                }
            }
        }
        sys
    }

    /// Independent boolean Floyd-Warshall oracle, including cycles of length 1.
    fn closure(mut relation: [[bool; 3]; 3]) -> [[bool; 3]; 3] {
        for k in 0..3 {
            for i in 0..3 {
                for j in 0..3 {
                    relation[i][j] |= relation[i][k] && relation[k][j];
                }
            }
        }
        relation
    }

    fn oracle_locally_confluent(edges: &[[bool; 3]; 3], mut reach: [[bool; 3]; 3]) -> bool {
        for i in 0..3 {
            reach[i][i] = true;
        }
        for row in edges {
            for a in 0..3 {
                for b in 0..3 {
                    if row[a] && row[b] && !(0..3).any(|j| reach[a][j] && reach[b][j]) {
                        return false;
                    }
                }
            }
        }
        true
    }

    #[test]
    fn all_512_directed_graphs_match_independent_matrix_oracles() {
        for mask in 0u16..512 {
            let mut edges = [[false; 3]; 3];
            for (i, row) in edges.iter_mut().enumerate() {
                for (j, edge) in row.iter_mut().enumerate() {
                    *edge = mask & (1 << (3 * i + j)) != 0;
                }
            }
            let sys = graph_system(&edges);
            let checked = ValidatedInfinityRewriteSystem::validate(sys.clone()).unwrap();
            let reach = closure(edges);
            let terminating = (0..3).all(|i| !reach[i][i]);
            assert_eq!(
                checked.termination_certificate().is_ok(),
                terminating,
                "graph {mask}"
            );
            let summary = summarize(&sys).unwrap();
            assert_eq!(summary.is_terminating, terminating);
            assert_eq!(
                summary.is_locally_confluent,
                oracle_locally_confluent(&edges, reach),
                "graph {mask}"
            );
            for (i, row) in edges.iter().enumerate() {
                let witness = checked.normal_form_witness(&i.to_string());
                assert_eq!(witness.is_some(), !row.iter().any(|v| *v));
                if let Some(witness) = witness {
                    assert_eq!(witness.term(), i.to_string());
                    assert_eq!(witness.system(), &checked);
                }
            }
        }
    }

    #[test]
    fn rank_checker_rejects_forged_domains_and_non_decreasing_edges() {
        let checked = ValidatedInfinityRewriteSystem::validate(arrow_system()).unwrap();
        let good = BTreeMap::from([("a".into(), usize::MAX), ("b".into(), 0)]);
        let certificate = checked.admit_termination_ranks(good.clone()).unwrap();
        assert_eq!(certificate.ranks(), &good);
        assert_eq!(certificate.system(), &checked);
        for bad in [
            BTreeMap::from([("a".into(), 0), ("b".into(), 0)]),
            BTreeMap::from([("a".into(), 0), ("b".into(), 1)]),
        ] {
            assert_eq!(
                checked.admit_termination_ranks(bad).unwrap_err().invariant,
                RewriteInvariant::RankDescent
            );
        }
        let mut missing = good.clone();
        missing.remove("a");
        let mut extra = good;
        extra.insert("outside".into(), 1);
        for bad in [missing, extra] {
            assert_eq!(
                checked.admit_termination_ranks(bad).unwrap_err().invariant,
                RewriteInvariant::RankDomain
            );
        }
    }

    #[test]
    fn malformed_declarations_do_not_produce_summaries_or_witnesses() {
        let mut sys = arrow_system();
        sys.cells.remove("b");
        assert!(sys.path_boundary(&sys.paths[0]).is_none());
        assert!(summarize(&sys).is_err());
        assert!(sys.normal_form_witness("a").is_err());
        assert!(!check_termination(&sys).is_empty());
        assert!(!check_local_confluence(&sys).is_empty());
        let empty = InfinityRewriteSystem::new("empty");
        let checked = ValidatedInfinityRewriteSystem::validate(empty).unwrap();
        assert!(checked
            .termination_certificate()
            .unwrap()
            .ranks()
            .is_empty());
        assert!(checked.normal_form_witness("outside").is_none());
    }

    #[test]
    fn globular_parallelism_and_dimensions_are_admitted_at_every_level() {
        let mut sys = arrow_system();
        sys.add_homotopy("h", "p", "p");
        sys.add_homotopy("k", "p", "p");
        sys.add_higher_cell("coherence", 3, "h", "k");
        assert!(ValidatedInfinityRewriteSystem::validate(sys.clone()).is_ok());
        let mut wrong_dimension = sys.clone();
        wrong_dimension.cells.get_mut("coherence").unwrap().level = usize::MAX;
        wrong_dimension.truncation_level = usize::MAX;
        assert!(ValidatedInfinityRewriteSystem::validate(wrong_dimension).is_err());
        sys.add_path(RewritePath::compose(
            "back",
            vec![PathStep::Inverse("r".into())],
        ));
        sys.cells.get_mut("k").unwrap().source = Some("back".into());
        sys.cells.get_mut("k").unwrap().target = Some("back".into());
        sys.homotopies
            .insert("k".into(), ("back".into(), "back".into()));
        assert!(ValidatedInfinityRewriteSystem::validate(sys).is_err());
        let mut nonparallel = arrow_system();
        nonparallel.add_path(RewritePath::compose(
            "back",
            vec![PathStep::Inverse("r".into())],
        ));
        nonparallel.add_homotopy("bad", "p", "back");
        assert!(ValidatedInfinityRewriteSystem::validate(nonparallel).is_err());
    }

    fn whisker_system() -> InfinityRewriteSystem {
        let mut sys = arrow_system();
        sys.add_term("x");
        sys.add_term("y");
        sys.add_rule("before", "x", "a");
        sys.add_rule("after", "b", "y");
        sys.add_path(RewritePath::named_single("prefix", "before"));
        sys.add_path(RewritePath::named_single("suffix", "after"));
        sys.add_homotopy("h", "p", "p");
        sys
    }

    #[test]
    fn whiskering_preserves_admission_and_failure_is_atomic() {
        let mut raw = whisker_system();
        let checked = ValidatedInfinityRewriteSystem::validate(raw.clone()).unwrap();
        let witness = checked.normal_form_witness("y").unwrap();
        let ranks = checked.termination_certificate().unwrap();
        raw.cells.clear(); // caller changes cannot alter certificates or witnesses
        assert!(witness.system().declared().cells.contains_key("y"));
        assert_eq!(ranks.system(), &checked);
        let left = checked.whisker_left("left", "prefix", "h").unwrap();
        assert_eq!(left.declared().paths.len(), 4); // reflexive homotopy reuses its path
        let right = checked.whisker_right("right", "h", "suffix").unwrap();
        let both = left.whisker_right("both", "left", "suffix").unwrap();
        assert!(right.termination_certificate().is_ok());
        assert!(both.termination_certificate().is_ok());
        let mut different = whisker_system();
        different.add_path(RewritePath::named_single("q", "r"));
        different.add_homotopy("parallel", "p", "q");
        assert!(different
            .whisker_left("distinct", "prefix", "parallel")
            .is_ok());
        for (name, path, homotopy) in [
            ("h", "prefix", "h"),
            ("new", "suffix", "h"),
            ("new", "missing", "h"),
            ("new", "prefix", "missing"),
            (" ", "prefix", "h"),
        ] {
            let mut raw = whisker_system();
            let before = raw.clone();
            assert!(raw.whisker_left(name, path, homotopy).is_err());
            assert_eq!(raw, before);
        }
        let mut collision = whisker_system();
        collision.add_path(RewritePath::named_single("prefix_p", "r"));
        let before = collision.clone();
        assert!(collision.whisker_left("new", "prefix", "h").is_err());
        assert_eq!(collision, before);
    }

    #[test]
    fn termination_on_a_long_chain_uses_no_recursive_call_stack() {
        let mut sys = InfinityRewriteSystem::new("long");
        for i in 0..20_000 {
            sys.add_term(&i.to_string());
        }
        for i in 1..20_000 {
            sys.add_rule(&format!("r{i}"), &(i - 1).to_string(), &i.to_string());
        }
        let checked = ValidatedInfinityRewriteSystem::validate(sys).unwrap();
        let cert = checked.termination_certificate().unwrap();
        assert_eq!(cert.ranks()["0"], 19_999);
        assert_eq!(cert.ranks()["19999"], 0);
    }

    #[test]
    fn valid_system_passes() {
        let mut sys = InfinityRewriteSystem::new("trivial");
        sys.add_term("a");
        sys.add_term("b");
        sys.add_rule("r1", "a", "b");

        let path = RewritePath::named_single("p1", "r1");
        sys.add_path(path.clone());
        sys.add_homotopy("h1", "p1", "p1");

        let validated = ValidatedInfinityRewriteSystem::validate(sys);
        assert!(validated.is_ok(), "{:?}", validated.err());
    }

    #[test]
    fn invalid_path_fails() {
        let mut sys = InfinityRewriteSystem::new("bad");
        sys.add_term("a");
        sys.add_term("b");
        sys.add_term("c");
        sys.add_rule("r1", "a", "b");
        sys.add_rule("r2", "c", "b"); // Note: c -> b

        // This path is broken because r1 goes to b, but r2 starts at c
        let path = RewritePath::compose(
            "p_bad",
            vec![
                PathStep::Forward("r1".into()),
                PathStep::Forward("r2".into()),
            ],
        );
        sys.add_path(path);

        let validated = ValidatedInfinityRewriteSystem::validate(sys);
        assert!(validated.is_err());
    }

    #[test]
    fn inverse_path_composes() {
        let mut sys = InfinityRewriteSystem::new("inv");
        sys.add_term("a");
        sys.add_term("b");
        sys.add_term("c");
        sys.add_rule("r1", "a", "b");
        sys.add_rule("r2", "b", "c");

        let fwd = RewritePath::compose(
            "p1",
            vec![
                PathStep::Forward("r1".into()),
                PathStep::Forward("r2".into()),
            ],
        );
        let inv = fwd.inverse("p1_inv");

        sys.add_path(fwd);
        sys.add_path(inv.clone());

        let bound = sys.path_boundary(&inv);
        assert_eq!(bound, Some(("c".into(), "a".into())));
    }
}
