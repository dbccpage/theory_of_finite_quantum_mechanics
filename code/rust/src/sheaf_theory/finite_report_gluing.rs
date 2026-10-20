
use omega_category_theory::finite_report_descent::{DescentError, FiniteReportPresheaf};
use omega_category_theory::finite_report_query::{
    ReportQueryDecision, ReportQueryProblem, ReportQueryRefusal,
};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GluingRefusal<C, P, V> {
    DuplicateTargetPoint { point: P },
    DuplicateAlphabetValue { value: V },
    DuplicateContext { context: C },
    DuplicateContextPoint { context: C, point: P },
    ContextOutsideTarget { context: C, point: P },
    UnknownContext { context: C },
    DuplicateSection { context: C },
    MissingSection { context: C },
    DuplicateAssignment { context: C, point: P },
    SectionDomainMismatch { context: C, point: P },
    OutsideValueAlphabet { context: C, point: P },
    IncompleteCoverage { missing_points: BTreeSet<P> },
}

impl<C: fmt::Debug, P: fmt::Debug, V: fmt::Debug> fmt::Display for GluingRefusal<C, P, V> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

impl<C: fmt::Debug, P: fmt::Debug, V: fmt::Debug> std::error::Error for GluingRefusal<C, P, V> {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FunctionCover<C, P, V> {
    target: BTreeSet<P>,
    contexts: BTreeMap<C, BTreeSet<P>>,
    alphabet: BTreeSet<V>,
}

pub type LocalSections<C, P, V> = BTreeMap<C, BTreeMap<P, V>>;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FunctionGlueDecision<C, P, V> {
    UniqueFunctionGlue {
        global: BTreeMap<P, V>,
        containing_context: BTreeMap<P, C>,
    },
    Incompatible {
        left: C,
        right: C,
        point: P,
        left_value: V,
        right_value: V,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FunctionGlueReplayFailure {
    GlobalDomainMismatch,
    GlobalValueOutsideAlphabet,
    RestrictionMismatch,
    ContainingContextMismatch,
    IncompatibleWitnessInvalid,
}

fn collect_unique_target<C, P: Ord + Clone, V>(
    target: &[P],
) -> Result<BTreeSet<P>, GluingRefusal<C, P, V>> {
    let mut t = BTreeSet::new();
    for p in target {
        if !t.insert(p.clone()) {
            return Err(GluingRefusal::DuplicateTargetPoint { point: p.clone() });
        }
    }
    Ok(t)
}

fn collect_unique_alphabet<C, P, V: Ord + Clone>(
    alphabet: &[V],
) -> Result<BTreeSet<V>, GluingRefusal<C, P, V>> {
    let mut a = BTreeSet::new();
    for v in alphabet {
        if !a.insert(v.clone()) {
            return Err(GluingRefusal::DuplicateAlphabetValue { value: v.clone() });
        }
    }
    Ok(a)
}

fn collect_context_domain<C: Clone, P: Ord + Clone, V>(
    c: &C,
    pts: &[P],
    target: &BTreeSet<P>,
) -> Result<BTreeSet<P>, GluingRefusal<C, P, V>> {
    let mut dom = BTreeSet::new();
    for p in pts {
        if !target.contains(p) {
            return Err(GluingRefusal::ContextOutsideTarget {
                context: c.clone(),
                point: p.clone(),
            });
        }
        if !dom.insert(p.clone()) {
            return Err(GluingRefusal::DuplicateContextPoint {
                context: c.clone(),
                point: p.clone(),
            });
        }
    }
    Ok(dom)
}

impl<C, P, V> FunctionCover<C, P, V>
where
    C: Ord + Clone + fmt::Debug,
    P: Ord + Clone + fmt::Debug,
    V: Ord + Clone + fmt::Debug,
{
    pub fn new(
        target: &[P],
        contexts: &[(C, Vec<P>)],
        alphabet: &[V],
    ) -> Result<Self, GluingRefusal<C, P, V>> {
        let t = collect_unique_target(target)?;
        let a = collect_unique_alphabet(alphabet)?;
        let mut cs = BTreeMap::new();
        for (c, pts) in contexts {
            let dom = collect_context_domain(c, pts, &t)?;
            if cs.insert(c.clone(), dom).is_some() {
                return Err(GluingRefusal::DuplicateContext { context: c.clone() });
            }
        }
        Ok(Self {
            target: t,
            contexts: cs,
            alphabet: a,
        })
    }

    pub fn target(&self) -> &BTreeSet<P> {
        &self.target
    }

    pub fn contexts(&self) -> &BTreeMap<C, BTreeSet<P>> {
        &self.contexts
    }

    pub fn union(&self) -> BTreeSet<P> {
        self.contexts.values().flatten().cloned().collect()
    }

    pub fn admit_sections(
        &self,
        sections: &[(C, Vec<(P, V)>)],
    ) -> Result<LocalSections<C, P, V>, GluingRefusal<C, P, V>> {
        let mut out: LocalSections<C, P, V> = BTreeMap::new();
        for (c, rows) in sections {
            let Some(dom) = self.contexts.get(c) else {
                return Err(GluingRefusal::UnknownContext { context: c.clone() });
            };
            if out.contains_key(c) {
                return Err(GluingRefusal::DuplicateSection { context: c.clone() });
            }
            let table = self.admit_section_rows(c, dom, rows)?;
            out.insert(c.clone(), table);
        }
        if let Some(c) = self.contexts.keys().find(|c| !out.contains_key(*c)) {
            return Err(GluingRefusal::MissingSection { context: c.clone() });
        }
        Ok(out)
    }

    fn admit_section_rows(
        &self,
        c: &C,
        dom: &BTreeSet<P>,
        rows: &[(P, V)],
    ) -> Result<BTreeMap<P, V>, GluingRefusal<C, P, V>> {
        let mut table = BTreeMap::new();
        for (p, v) in rows {
            if !dom.contains(p) {
                return Err(GluingRefusal::SectionDomainMismatch {
                    context: c.clone(),
                    point: p.clone(),
                });
            }
            if !self.alphabet.contains(v) {
                return Err(GluingRefusal::OutsideValueAlphabet {
                    context: c.clone(),
                    point: p.clone(),
                });
            }
            if table.insert(p.clone(), v.clone()).is_some() {
                return Err(GluingRefusal::DuplicateAssignment {
                    context: c.clone(),
                    point: p.clone(),
                });
            }
        }
        for p in dom {
            if !table.contains_key(p) {
                return Err(GluingRefusal::SectionDomainMismatch {
                    context: c.clone(),
                    point: p.clone(),
                });
            }
        }
        Ok(table)
    }

    pub fn glue_on_union(
        &self,
        sections: &[(C, Vec<(P, V)>)],
    ) -> Result<FunctionGlueDecision<C, P, V>, GluingRefusal<C, P, V>> {
        let locals = self.admit_sections(sections)?;
        Ok(Self::glue_admitted(&locals))
    }

    pub fn glue_on_target(
        &self,
        sections: &[(C, Vec<(P, V)>)],
    ) -> Result<FunctionGlueDecision<C, P, V>, GluingRefusal<C, P, V>> {
        let union = self.union();
        let missing: BTreeSet<P> = self.target.difference(&union).cloned().collect();
        if !missing.is_empty() {
            return Err(GluingRefusal::IncompleteCoverage {
                missing_points: missing,
            });
        }
        self.glue_on_union(sections)
    }

    fn glue_admitted(locals: &LocalSections<C, P, V>) -> FunctionGlueDecision<C, P, V> {
        if let Some(incompat) = Self::find_incompatibility(locals) {
            return incompat;
        }
        let mut global = BTreeMap::new();
        let mut containing_context = BTreeMap::new();
        for (c, s) in locals {
            for (p, v) in s {
                if !global.contains_key(p) {
                    global.insert(p.clone(), v.clone());
                    containing_context.insert(p.clone(), c.clone());
                }
            }
        }
        FunctionGlueDecision::UniqueFunctionGlue {
            global,
            containing_context,
        }
    }

    fn find_incompatibility(
        locals: &LocalSections<C, P, V>,
    ) -> Option<FunctionGlueDecision<C, P, V>> {
        let entries: Vec<(&C, &BTreeMap<P, V>)> = locals.iter().collect();
        for (i, (ci, si)) in entries.iter().enumerate() {
            for (cj, sj) in entries.iter().skip(i + 1) {
                if let Some((p, vi, vj)) = Self::first_section_mismatch(si, sj) {
                    return Some(FunctionGlueDecision::Incompatible {
                        left: (*ci).clone(),
                        right: (*cj).clone(),
                        point: p,
                        left_value: vi,
                        right_value: vj,
                    });
                }
            }
        }
        None
    }

    fn first_section_mismatch(
        si: &BTreeMap<P, V>,
        sj: &BTreeMap<P, V>,
    ) -> Option<(P, V, V)> {
        for (p, vi) in si {
            if let Some(vj) = sj.get(p) {
                if vi != vj {
                    return Some((p.clone(), vi.clone(), vj.clone()));
                }
            }
        }
        None
    }

    pub fn verify_function_glue(
        &self,
        sections: &[(C, Vec<(P, V)>)],
        decision: &FunctionGlueDecision<C, P, V>,
    ) -> Result<(), FunctionGlueReplayFailure> {
        let Ok(locals) = self.admit_sections(sections) else {
            return Err(FunctionGlueReplayFailure::RestrictionMismatch);
        };
        match decision {
            FunctionGlueDecision::UniqueFunctionGlue {
                global,
                containing_context,
            } => self.verify_unique_function_glue(&locals, global, containing_context),
            FunctionGlueDecision::Incompatible {
                left,
                right,
                point,
                left_value,
                right_value,
            } => Self::verify_incompatible_function_glue(
                &locals,
                left,
                right,
                point,
                left_value,
                right_value,
            ),
        }
    }

    fn verify_unique_function_glue(
        &self,
        locals: &LocalSections<C, P, V>,
        global: &BTreeMap<P, V>,
        containing_context: &BTreeMap<P, C>,
    ) -> Result<(), FunctionGlueReplayFailure> {
        let union = self.union();
        let dom: BTreeSet<P> = global.keys().cloned().collect();
        if dom != union {
            return Err(FunctionGlueReplayFailure::GlobalDomainMismatch);
        }
        if global.values().any(|v| !self.alphabet.contains(v)) {
            return Err(FunctionGlueReplayFailure::GlobalValueOutsideAlphabet);
        }
        Self::verify_local_restrictions(locals, global)?;
        self.verify_containing_contexts(&union, containing_context)
    }

    fn verify_local_restrictions(
        locals: &LocalSections<C, P, V>,
        global: &BTreeMap<P, V>,
    ) -> Result<(), FunctionGlueReplayFailure> {
        for s in locals.values() {
            for (p, v) in s {
                if global.get(p) != Some(v) {
                    return Err(FunctionGlueReplayFailure::RestrictionMismatch);
                }
            }
        }
        Ok(())
    }

    fn verify_containing_contexts(
        &self,
        union: &BTreeSet<P>,
        containing_context: &BTreeMap<P, C>,
    ) -> Result<(), FunctionGlueReplayFailure> {
        let witness_dom: BTreeSet<P> = containing_context.keys().cloned().collect();
        if witness_dom != *union {
            return Err(FunctionGlueReplayFailure::ContainingContextMismatch);
        }
        for (p, c) in containing_context {
            let Some(dom) = self.contexts.get(c) else {
                return Err(FunctionGlueReplayFailure::ContainingContextMismatch);
            };
            if !dom.contains(p) {
                return Err(FunctionGlueReplayFailure::ContainingContextMismatch);
            }
        }
        Ok(())
    }

    fn verify_incompatible_function_glue(
        locals: &LocalSections<C, P, V>,
        left: &C,
        right: &C,
        point: &P,
        left_value: &V,
        right_value: &V,
    ) -> Result<(), FunctionGlueReplayFailure> {
        let left_matches = locals.get(left).and_then(|s| s.get(point)) == Some(left_value);
        let right_matches = locals.get(right).and_then(|s| s.get(point)) == Some(right_value);
        if left != right && left_value != right_value && left_matches && right_matches {
            Ok(())
        } else {
            Err(FunctionGlueReplayFailure::IncompatibleWitnessInvalid)
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct RejectedGlobalRow {
    pub global: usize,
    pub context: u64,
    pub actual: usize,
    pub expected: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PresheafGlueReceipt {
    UniquePresheafGlue {
        global: usize,
        rejected_global_rows: Vec<RejectedGlobalRow>,
    },
    NoGlobalExtension {
        matching_family: Vec<usize>,
        rejected_global_rows: Vec<RejectedGlobalRow>,
    },
    Ambiguous {
        matching_family: Vec<usize>,
        first: usize,
        second: usize,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PresheafReplayFailure {
    Descent(DescentError),
    WrongVerdict,
    RejectionTableIncomplete,
    RejectionRowFalse,
    AmbiguityWitnessInvalid,
}

fn restriction(presheaf: &FiniteReportPresheaf, source: u64, target: u64, s: usize) -> Option<usize> {
    presheaf
        .restrictions()
        .get(&(source, target))
        .and_then(|table| table.get(s))
        .copied()
}

fn first_rejected_row(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    g: usize,
) -> Option<RejectedGlobalRow> {
    for (&c, &expected) in cover.iter().zip(locals) {
        if let Some(actual) = restriction(presheaf, target, c, g) {
            if actual != expected {
                return Some(RejectedGlobalRow {
                    global: g,
                    context: c,
                    actual,
                    expected,
                });
            }
        }
    }
    None
}

fn rejection_rows(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    skip: Option<usize>,
) -> Vec<RejectedGlobalRow> {
    let count = presheaf.report_counts().get(&target).copied().unwrap_or(0);
    let mut rows = Vec::new();
    for g in 0..count {
        if Some(g) != skip {
            if let Some(row) = first_rejected_row(presheaf, target, cover, locals, g) {
                rows.push(row);
            }
        }
    }
    rows
}

pub fn classify_presheaf_gluing(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
) -> Result<PresheafGlueReceipt, DescentError> {
    let fiber = presheaf.descent_fiber(target, cover, locals)?;
    Ok(match fiber.global_sections.as_slice() {
        [] => PresheafGlueReceipt::NoGlobalExtension {
            matching_family: locals.to_vec(),
            rejected_global_rows: rejection_rows(presheaf, target, cover, locals, None),
        },
        [g] => PresheafGlueReceipt::UniquePresheafGlue {
            global: *g,
            rejected_global_rows: rejection_rows(presheaf, target, cover, locals, Some(*g)),
        },
        [first, second, ..] => PresheafGlueReceipt::Ambiguous {
            matching_family: locals.to_vec(),
            first: *first,
            second: *second,
        },
    })
}

fn restricts_correctly(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    g: usize,
) -> bool {
    for (&c, &l) in cover.iter().zip(locals) {
        if restriction(presheaf, target, c, g) != Some(l) {
            return false;
        }
    }
    true
}

fn row_is_valid_rejection(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    r: &RejectedGlobalRow,
) -> bool {
    let mut in_cover = false;
    for (&c, &l) in cover.iter().zip(locals) {
        if c == r.context && l == r.expected {
            in_cover = true;
            break;
        }
    }
    in_cover
        && r.actual != r.expected
        && restriction(presheaf, target, r.context, r.global) == Some(r.actual)
}

fn check_rejection_rows(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    count: usize,
    rows: &[RejectedGlobalRow],
    skip: Option<usize>,
) -> Result<(), PresheafReplayFailure> {
    for r in rows {
        if !row_is_valid_rejection(presheaf, target, cover, locals, r) {
            return Err(PresheafReplayFailure::RejectionRowFalse);
        }
    }
    let excluded: BTreeSet<usize> = rows.iter().map(|r| r.global).collect();
    for g in 0..count {
        if Some(g) != skip && !excluded.contains(&g) {
            return Err(PresheafReplayFailure::RejectionTableIncomplete);
        }
    }
    Ok(())
}

pub fn verify_presheaf_receipt(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    receipt: &PresheafGlueReceipt,
) -> Result<(), PresheafReplayFailure> {
    presheaf
        .descent_fiber(target, cover, locals)
        .map_err(PresheafReplayFailure::Descent)?;
    let count = presheaf.report_counts().get(&target).copied().unwrap_or(0);
    match receipt {
        PresheafGlueReceipt::UniquePresheafGlue {
            global,
            rejected_global_rows,
        } => {
            if *global >= count || !restricts_correctly(presheaf, target, cover, locals, *global) {
                return Err(PresheafReplayFailure::WrongVerdict);
            }
            check_rejection_rows(
                presheaf,
                target,
                cover,
                locals,
                count,
                rejected_global_rows,
                Some(*global),
            )
        }
        PresheafGlueReceipt::NoGlobalExtension {
            matching_family,
            rejected_global_rows,
        } => {
            if matching_family.as_slice() != locals {
                return Err(PresheafReplayFailure::WrongVerdict);
            }
            check_rejection_rows(
                presheaf,
                target,
                cover,
                locals,
                count,
                rejected_global_rows,
                None,
            )
        }
        PresheafGlueReceipt::Ambiguous {
            matching_family,
            first,
            second,
        } => verify_ambiguous_presheaf_receipt(
            presheaf,
            target,
            cover,
            locals,
            count,
            matching_family,
            *first,
            *second,
        ),
    }
}

fn verify_ambiguous_presheaf_receipt(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
    count: usize,
    matching_family: &[usize],
    first: usize,
    second: usize,
) -> Result<(), PresheafReplayFailure> {
    let valid_indices = first != second && first < count && second < count;
    if matching_family != locals
        || !valid_indices
        || !restricts_correctly(presheaf, target, cover, locals, first)
        || !restricts_correctly(presheaf, target, cover, locals, second)
    {
        return Err(PresheafReplayFailure::AmbiguityWitnessInvalid);
    }
    Ok(())
}

pub fn history_erasure_decision<H, E, Q>(
    histories: &[H],
    endpoints: &[E],
    query_values: &[Q],
    endpoint_rows: &[(H, E)],
    query_rows: &[(H, Q)],
) -> Result<ReportQueryDecision<H, E, Q>, ReportQueryRefusal<H>>
where
    H: Ord + Clone + fmt::Debug,
    E: Ord + Clone + fmt::Debug,
    Q: Ord + Clone + fmt::Debug,
{
    let problem =
        ReportQueryProblem::new(histories, endpoints, query_values, endpoint_rows, query_rows)?;
    Ok(problem.decide())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn function_cover_glues_compatible_sections_and_detects_incompatibility_and_refusals() {
        let cover = FunctionCover::new(
            &[1u8, 2, 3],
            &[('A', vec![1u8, 2]), ('B', vec![2u8, 3])],
            &[0u8, 1],
        )
        .unwrap();

        let compatible = vec![
            ('A', vec![(1u8, 0u8), (2, 1)]),
            ('B', vec![(2u8, 1u8), (3, 0)]),
        ];
        let glued = cover.glue_on_target(&compatible).unwrap();
        assert!(matches!(glued, FunctionGlueDecision::UniqueFunctionGlue { .. }));
        cover.verify_function_glue(&compatible, &glued).unwrap();

        let incompatible = vec![
            ('A', vec![(1u8, 0u8), (2, 1)]),
            ('B', vec![(2u8, 0u8), (3, 0)]),
        ];
        let conflict = cover.glue_on_target(&incompatible).unwrap();
        assert_eq!(
            conflict,
            FunctionGlueDecision::Incompatible {
                left: 'A',
                right: 'B',
                point: 2,
                left_value: 1,
                right_value: 0,
            }
        );
        cover.verify_function_glue(&incompatible, &conflict).unwrap();

        let dup_err = FunctionCover::new(&[1u8, 1], &[('A', vec![1u8])], &[0u8]).unwrap_err();
        assert_eq!(dup_err, GluingRefusal::DuplicateTargetPoint { point: 1 });
    }
}

