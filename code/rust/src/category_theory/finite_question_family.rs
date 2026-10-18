
use crate::finite_report_descent::{DescentError, FiniteReportPresheaf};
use crate::finite_report_query::{ReportQueryProblem, ReportQueryRefusal};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Debug;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum QuestionFamilyError {
    RowWidth {
        row: usize,
        expected: usize,
        actual: usize,
    },
    MapLength {
        expected: usize,
        actual: usize,
    },
    ImageOutsideTarget {
        source: usize,
        image: usize,
    },
    WorkLimit,
    Report(ReportQueryRefusal<usize>),
    Descent(DescentError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QuestionQuotient<A> {
    pub profiles: Vec<Vec<A>>,
    pub class_of: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteQuestionFamily<A> {
    question_count: usize,
    answers: Vec<Vec<A>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QuestionReportSite<A> {
    presheaf: FiniteReportPresheaf,
    profiles: BTreeMap<u64, Vec<Vec<A>>>,
}

impl<A> QuestionReportSite<A> {
    pub fn presheaf(&self) -> &FiniteReportPresheaf {
        &self.presheaf
    }
    pub fn profiles(&self) -> &BTreeMap<u64, Vec<Vec<A>>> {
        &self.profiles
    }
}

pub fn factor_tables<R: Ord + Clone + Debug, A: Ord + Clone + Debug>(
    report: &[R],
    query: &[A],
) -> Result<ReportQueryProblem<usize, R, A>, QuestionFamilyError> {
    if report.len() != query.len() {
        return Err(QuestionFamilyError::MapLength {
            expected: query.len(),
            actual: report.len(),
        });
    }
    let source: Vec<_> = (0..query.len()).collect();
    let reports: Vec<_> = report
        .iter()
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    let queries: Vec<_> = query
        .iter()
        .cloned()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    ReportQueryProblem::new(
        &source,
        &reports,
        &queries,
        &report.iter().cloned().enumerate().collect::<Vec<_>>(),
        &query.iter().cloned().enumerate().collect::<Vec<_>>(),
    )
    .map_err(QuestionFamilyError::Report)
}

impl<A: Ord + Clone + Debug> FiniteQuestionFamily<A> {
    pub fn new(question_count: usize, answers: Vec<Vec<A>>) -> Result<Self, QuestionFamilyError> {
        for (row, values) in answers.iter().enumerate() {
            if values.len() != question_count {
                return Err(QuestionFamilyError::RowWidth {
                    row,
                    expected: question_count,
                    actual: values.len(),
                });
            }
        }
        Ok(Self {
            question_count,
            answers,
        })
    }

    pub fn answers(&self) -> &[Vec<A>] {
        &self.answers
    }
    pub fn question_count(&self) -> usize {
        self.question_count
    }

    pub fn quotient(&self) -> QuestionQuotient<A> {
        let profiles: Vec<_> = self
            .answers
            .iter()
            .cloned()
            .collect::<BTreeSet<_>>()
            .into_iter()
            .collect();
        let ids: BTreeMap<_, _> = profiles
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, p)| (p, i))
            .collect();
        let class_of = self.answers.iter().map(|row| ids[row]).collect();
        QuestionQuotient { profiles, class_of }
    }

    pub fn verify_quotient(&self, candidate: &QuestionQuotient<A>) -> bool {
        *candidate == self.quotient()
    }

    pub fn factor_report<R: Ord + Clone + Debug>(
        &self,
        report: &[R],
    ) -> Result<ReportQueryProblem<usize, R, Vec<A>>, QuestionFamilyError> {
        factor_tables(report, &self.answers)
    }

    pub fn descend_operation<B: Ord + Clone + Debug>(
        &self,
        target: &FiniteQuestionFamily<B>,
        images: &[Option<usize>],
    ) -> Result<ReportQueryProblem<usize, usize, Option<usize>>, QuestionFamilyError> {
        if images.len() != self.answers.len() {
            return Err(QuestionFamilyError::MapLength {
                expected: self.answers.len(),
                actual: images.len(),
            });
        }
        let target_classes = target.quotient().class_of;
        let query = images
            .iter()
            .enumerate()
            .map(|(source, image)| match image {
                None => Ok(None),
                Some(i) => target_classes
                    .get(*i)
                    .copied()
                    .map(Some)
                    .ok_or(QuestionFamilyError::ImageOutsideTarget { source, image: *i }),
            })
            .collect::<Result<Vec<_>, _>>()?;
        factor_tables(&self.quotient().class_of, &query)
    }

    pub fn descend_composition<B: Ord + Clone + Debug, C: Ord + Clone + Debug>(
        &self,
        right: &FiniteQuestionFamily<B>,
        target: &FiniteQuestionFamily<C>,
        images: &[Option<usize>],
    ) -> Result<ReportQueryProblem<usize, (usize, usize), Option<usize>>, QuestionFamilyError> {
        let expected = self
            .answers
            .len()
            .checked_mul(right.answers.len())
            .ok_or(QuestionFamilyError::WorkLimit)?;
        if images.len() != expected {
            return Err(QuestionFamilyError::MapLength {
                expected,
                actual: images.len(),
            });
        }
        let left_classes = self.quotient().class_of;
        let right_classes = right.quotient().class_of;
        let reports: Vec<_> = left_classes
            .iter()
            .flat_map(|&l| right_classes.iter().map(move |&r| (l, r)))
            .collect();
        let classes = target.quotient().class_of;
        let query = images
            .iter()
            .enumerate()
            .map(|(source, image)| match image {
                None => Ok(None),
                Some(i) => classes
                    .get(*i)
                    .copied()
                    .map(Some)
                    .ok_or(QuestionFamilyError::ImageOutsideTarget { source, image: *i }),
            })
            .collect::<Result<Vec<_>, _>>()?;
        factor_tables(&reports, &query)
    }

    pub fn report_site(
        &self,
        contexts: &BTreeSet<u64>,
        work_limit: usize,
    ) -> Result<QuestionReportSite<A>, QuestionFamilyError> {
        if self.question_count > 64 {
            return Err(QuestionFamilyError::Descent(DescentError::CarrierTooLarge));
        }
        let full = if self.question_count == 64 {
            u64::MAX
        } else {
            (1u64 << self.question_count) - 1
        };
        for &context in contexts {
            if context & !full != 0 {
                return Err(QuestionFamilyError::Descent(
                    DescentError::ContextOutsideCarrier { context },
                ));
            }
        }
        let c = contexts.len();
        let work = c
            .checked_add(self.question_count)
            .and_then(|x| x.checked_mul(c))
            .and_then(|x| x.checked_mul(c))
            .and_then(|x| x.checked_mul(self.answers.len().max(1)))
            .ok_or(QuestionFamilyError::WorkLimit)?;
        if work > work_limit {
            return Err(QuestionFamilyError::WorkLimit);
        }
        let mut profiles = BTreeMap::new();
        for &context in contexts {
            let projected: Vec<Vec<A>> = self
                .answers
                .iter()
                .map(|row| {
                    row.iter()
                        .enumerate()
                        .filter(|(i, _)| context & (1u64 << i) != 0)
                        .map(|(_, a)| a.clone())
                        .collect()
                })
                .collect();
            profiles.insert(
                context,
                if context == full {
                    projected
                } else {
                    projected
                        .into_iter()
                        .collect::<BTreeSet<_>>()
                        .into_iter()
                        .collect()
                },
            );
        }
        let counts = profiles.iter().map(|(&c, ps)| (c, ps.len())).collect();
        let mut restrictions = BTreeMap::new();
        for (&source, source_profiles) in &profiles {
            for (&target, target_profiles) in &profiles {
                if source & target != target {
                    continue;
                }
                if source == target {
                    restrictions.insert((source, target), (0..source_profiles.len()).collect());
                    continue;
                }
                let ids: BTreeMap<_, _> = target_profiles
                    .iter()
                    .cloned()
                    .enumerate()
                    .map(|(i, p)| (p, i))
                    .collect();
                let positions: Vec<_> = (0..self.question_count)
                    .filter(|i| source & (1u64 << i) != 0)
                    .collect();
                let table = source_profiles
                    .iter()
                    .map(|row| {
                        let projected: Vec<_> = positions
                            .iter()
                            .zip(row)
                            .filter(|(i, _)| target & (1u64 << **i) != 0)
                            .map(|(_, a)| a.clone())
                            .collect();
                        ids.get(&projected)
                            .copied()
                            .ok_or(QuestionFamilyError::Descent(
                                DescentError::RestrictionTargetOutsideReports { source, target },
                            ))
                    })
                    .collect::<Result<_, _>>()?;
                restrictions.insert((source, target), table);
            }
        }
        let presheaf = FiniteReportPresheaf::new(self.question_count, counts, restrictions)
            .map_err(QuestionFamilyError::Descent)?;
        Ok(QuestionReportSite { presheaf, profiles })
    }
}
