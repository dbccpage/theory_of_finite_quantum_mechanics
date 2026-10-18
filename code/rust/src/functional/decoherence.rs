

use linear_algebra::backend::basic_matrix::BasicMatrix;
use omega_number_theory::cyclotomic::GaussianRat;

fn check_well_formed(matrix: &BasicMatrix<GaussianRat>) -> Result<(), DecoherenceError> {
    if matrix.rows() == 0 || matrix.cols() == 0 {
        return Err(DecoherenceError::Empty);
    }
    omega_kernel::resource_limits::OperationLimits::default()
        .check_dense_matrix(
            matrix.rows(),
            matrix.cols(),
            std::mem::size_of::<GaussianRat>(),
        )
        .map(|_| ())
        .map_err(|error| DecoherenceError::Algebra(error.to_string()))
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum DecoherenceError {
    #[error(transparent)]
    Operator(#[from] linear_algebra::exact_field::ExactFieldError),
    #[error("exact algebra refused: {0}")]
    Algebra(String),
    #[error("a history family needs at least one history")]
    Empty,
    #[error("the state is {rows}x{cols}, not square")]
    StateNotSquare { rows: usize, cols: usize },
    #[error("class operator {index} is not {dimension}x{dimension}")]
    ClassOperatorShape { index: usize, dimension: usize },
    #[error("history {index} is out of range for {count} histories")]
    HistoryOutOfRange { index: usize, count: usize },
    #[error("a sum rule needs two distinct histories, got {index} twice")]
    SameHistory { index: usize },
    #[error("history {index} lies in {classes} classes of the coarse-graining, not one")]
    NotAPartition { index: usize, classes: usize },
    #[error("class {class} of the coarse-graining is empty")]
    EmptyClass { class: usize },
    #[error("{steps} steps cannot carry {partitions} partitions")]
    StepCount { steps: usize, partitions: usize },
    #[error("partition {time} is empty")]
    EmptyPartition { time: usize },
    #[error(
        "member {index} of partition {time} is not a {dimension}x{dimension} Hermitian idempotent"
    )]
    NotProjector {
        time: usize,
        index: usize,
        dimension: usize,
    },
    #[error("members {first} and {second} of partition {time} are not orthogonal")]
    NotOrthogonal {
        time: usize,
        first: usize,
        second: usize,
    },
    #[error("partition {time} does not sum to the identity")]
    IncompletePartition { time: usize },
    #[error("more than {budget} histories")]
    HistoryBudget { budget: usize },
    #[error("Heisenberg picture refused: {0}")]
    Heisenberg(String),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DecoherenceFunctional {
    state: BasicMatrix<GaussianRat>,
    class_operators: Vec<BasicMatrix<GaussianRat>>,
    matrix: BasicMatrix<GaussianRat>,
}

impl DecoherenceFunctional {
    pub fn new(
        state: BasicMatrix<GaussianRat>,
        class_operators: Vec<BasicMatrix<GaussianRat>>,
    ) -> Result<Self, DecoherenceError> {
        check_well_formed(&state)?;
        for c in &class_operators {
            check_well_formed(c)?;
        }
        if class_operators.len() > 1024 || state.rows() > 256 {
            return Err(DecoherenceError::HistoryBudget { budget: 1024 });
        }
        if class_operators.is_empty() {
            return Err(DecoherenceError::Empty);
        }
        if state.rows() != state.cols() {
            return Err(DecoherenceError::StateNotSquare {
                rows: state.rows(),
                cols: state.cols(),
            });
        }
        let dimension = state.rows();
        if let Some(index) = class_operators
            .iter()
            .position(|c| c.rows() != dimension || c.cols() != dimension)
        {
            return Err(DecoherenceError::ClassOperatorShape { index, dimension });
        }
        let weighted: Vec<BasicMatrix<GaussianRat>> = class_operators
            .iter()
            .map(|c| {
                linear_algebra::exact_field::matrix::multiply_with_limits(
                    &(c),
                    &state,
                    linear_algebra::backend::basic_matrix::OperationLimits {
                        max_elements: 1 << 20,
                        max_scalar_ops: 1 << 24,
                    },
                )
                .expect("validated finite matrix shape and budget")
            })
            .collect();
        let m = class_operators.len();
        let mut matrix = linear_algebra::exact_field::matrix::zeros_with_limits::<GaussianRat>(
            m,
            m,
            linear_algebra::backend::basic_matrix::OperationLimits {
                max_elements: 1 << 20,
                max_scalar_ops: 1 << 24,
            },
        )
        .expect("validated finite matrix shape and budget");
        for (j, c_rho) in weighted.iter().enumerate() {
            for (k, c) in class_operators.iter().enumerate() {
                let entry = linear_algebra::exact_field::involution::hs_inner(c, c_rho)
                    .map_err(linear_algebra::exact_field::ExactFieldError::from)
                    .expect("class operators share one shape");
                (matrix)
                    .set(j, k, entry)
                    .expect("validated finite matrix shape and budget");
            }
        }
        Ok(Self {
            state,
            class_operators,
            matrix,
        })
    }

    pub fn matrix(&self) -> &BasicMatrix<GaussianRat> {
        &self.matrix
    }

    pub fn is_complete(&self) -> bool {
        let d = self.state.rows();
        let total = self.class_operators.iter().fold(
            linear_algebra::exact_field::matrix::zeros_with_limits::<GaussianRat>(
                d,
                d,
                linear_algebra::backend::basic_matrix::OperationLimits {
                    max_elements: 1 << 20,
                    max_scalar_ops: 1 << 24,
                },
            )
            .expect("validated finite matrix shape and budget"),
            |acc, c| {
                linear_algebra::exact_field::matrix::add(
                    &(acc),
                    &linear_algebra::exact_field::matrix::multiply_with_limits(
                        &(linear_algebra::exact_field::involution::adjoint(&(c))
                            .expect("validated finite matrix shape and budget")),
                        c,
                        linear_algebra::backend::basic_matrix::OperationLimits {
                            max_elements: 1 << 20,
                            max_scalar_ops: 1 << 24,
                        },
                    )
                    .expect("validated finite matrix shape and budget"),
                )
                .expect("validated finite matrix shape and budget")
            },
        );
        total
            == linear_algebra::exact_field::matrix::identity_with_limits::<GaussianRat>(
                d,
                linear_algebra::backend::basic_matrix::OperationLimits {
                    max_elements: 1 << 20,
                    max_scalar_ops: 1 << 24,
                },
            )
            .expect("validated finite matrix shape and budget")
    }

    fn check_index(&self, index: usize) -> Result<(), DecoherenceError> {
        let count = self.class_operators.len();
        if index >= count {
            return Err(DecoherenceError::HistoryOutOfRange { index, count });
        }
        Ok(())
    }

    pub fn coarse_grain(&self, classes: &[Vec<usize>]) -> Result<Self, DecoherenceError> {
        let count = self.class_operators.len();
        let mut membership = vec![0usize; count];
        for (class, members) in classes.iter().enumerate() {
            if members.is_empty() {
                return Err(DecoherenceError::EmptyClass { class });
            }
            for &index in members {
                self.check_index(index)?;
                membership[index] += 1;
            }
        }
        if let Some((index, &classes)) = membership.iter().enumerate().find(|&(_, &n)| n != 1) {
            return Err(DecoherenceError::NotAPartition { index, classes });
        }
        let d = self.state.rows();
        let coarse = classes
            .iter()
            .map(|members| {
                members.iter().fold(
                    linear_algebra::exact_field::matrix::zeros_with_limits::<GaussianRat>(
                        d,
                        d,
                        linear_algebra::backend::basic_matrix::OperationLimits {
                            max_elements: 1 << 20,
                            max_scalar_ops: 1 << 24,
                        },
                    )
                    .expect("validated finite matrix shape and budget"),
                    |acc, &j| {
                        linear_algebra::exact_field::matrix::add(&(acc), &self.class_operators[j])
                            .expect("validated finite matrix shape and budget")
                    },
                )
            })
            .collect();
        Self::new(self.state.clone(), coarse)
    }

    pub fn sum_rule_residual(&self, j: usize, k: usize) -> Result<GaussianRat, DecoherenceError> {
        self.check_index(j)?;
        self.check_index(k)?;
        if j == k {
            return Err(DecoherenceError::SameHistory { index: j });
        }
        let union = linear_algebra::exact_field::matrix::add(
            &self.class_operators[j],
            &self.class_operators[k],
        )
        .map_err(linear_algebra::exact_field::ExactFieldError::from)?;
        let union_weight = linear_algebra::exact_field::matrix::trace(
            &(linear_algebra::exact_field::matrix::multiply_with_limits(
                &(linear_algebra::exact_field::matrix::multiply_with_limits(
                    &(union),
                    &self.state,
                    linear_algebra::backend::basic_matrix::OperationLimits {
                        max_elements: 1 << 20,
                        max_scalar_ops: 1 << 24,
                    },
                )
                .expect("validated finite matrix shape and budget")),
                &linear_algebra::exact_field::involution::adjoint(&(union))
                    .expect("validated finite matrix shape and budget"),
                linear_algebra::backend::basic_matrix::OperationLimits {
                    max_elements: 1 << 20,
                    max_scalar_ops: 1 << 24,
                },
            )
            .expect("validated finite matrix shape and budget")),
        )
        .expect("validated finite matrix shape and budget");
        Ok(union_weight
            .sub(
                (self.matrix)
                    .get_ref(j, j)
                    .expect("validated finite matrix shape and budget"),
            )
            .sub(
                (self.matrix)
                    .get_ref(k, k)
                    .expect("validated finite matrix shape and budget"),
            ))
    }

    pub fn medium_decoherence_witness(&self) -> Option<(usize, usize)> {
        let m = self.class_operators.len();
        (0..m)
            .flat_map(|j| (j + 1..m).map(move |k| (j, k)))
            .find(|&(j, k)| {
                !(self.matrix)
                    .get_ref(j, k)
                    .expect("validated finite matrix shape and budget")
                    .is_zero()
                    || !(self.matrix)
                        .get_ref(k, j)
                        .expect("validated finite matrix shape and budget")
                        .is_zero()
            })
    }

    pub fn weak_decoherence_witness(&self) -> Option<(usize, usize)> {
        let m = self.class_operators.len();
        (0..m)
            .flat_map(|j| (j + 1..m).map(move |k| (j, k)))
            .find(|&(j, k)| {
                !self
                    .sum_rule_residual(j, k)
                    .expect("indices are in range and distinct")
                    .is_zero()
            })
    }
}

impl DecoherenceFunctional {
    pub fn tensor(&self, other: &Self) -> Result<Self, DecoherenceError> {
        use linear_algebra::exact_field::matrix::kronecker;
        if self
            .class_operators
            .len()
            .checked_mul(other.class_operators.len())
            .is_none_or(|n| n > 1024)
            || self
                .state
                .rows()
                .checked_mul(other.state.rows())
                .is_none_or(|n| n > 256)
        {
            return Err(DecoherenceError::HistoryBudget { budget: 1024 });
        }
        let tensor = |a: &BasicMatrix<GaussianRat>,
                      b: &BasicMatrix<GaussianRat>|
         -> Result<BasicMatrix<GaussianRat>, DecoherenceError> {
            let product = kronecker(
                &Ok::<_, linear_algebra::exact_field::ExactFieldError>((a).clone())?,
                &Ok::<_, linear_algebra::exact_field::ExactFieldError>((b).clone())?,
            )
            .map_err(|e| DecoherenceError::Algebra(e.to_string()))?;
            Ok((&product).clone())
        };
        let state = tensor(&self.state, &other.state)?;
        let mut classes = Vec::new();
        for a in &self.class_operators {
            for b in &other.class_operators {
                classes.push(tensor(a, b)?);
            }
        }
        Self::new(state, classes)
    }
    pub fn is_strongly_positive(&self) -> Result<bool, DecoherenceError> {
        Ok(linear_algebra::exact_field::ordered::hermitian_is_positive_semidefinite(&self.matrix)?)
    }
}
