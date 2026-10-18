
use crate::braid_action::{BraidActionError, MajoranaBraidAction, MAX_BRAID_MODES};

pub const DEFAULT_MAX_COMPILED_STEPS: usize = 65_536;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MultiQubitOperation {
    Elementary { index: usize, inverse: bool },
    Phase { qubit: usize, inverse: bool },
    Hadamard { qubit: usize, inverse: bool },
    Cnot { control: usize, target: usize },
    Swap { first: usize, second: usize },
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum MultiQubitBraidError {
    #[error("num_qubits must be an integer >= 1 within the braid mode bound")]
    InvalidQubitCount,
    #[error("qubit={qubit} out of range [1, {num_qubits}]")]
    InvalidQubit { qubit: usize, num_qubits: usize },
    #[error("Control and target qubits must be distinct")]
    EqualControlTarget,
    #[error("Adjacent swap requires |q1 - q2| == 1")]
    NonAdjacentSwap,
    #[error("compiled braid word exceeds the declared limit of {limit} elementary steps")]
    StepLimit { limit: usize },
    #[error("braid word allocation failed")]
    Allocation,
    #[error(transparent)]
    Braid(#[from] BraidActionError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CompiledMultiQubitBraid {
    pub num_qubits: usize,
    pub gate_count: usize,
    pub steps: Vec<(usize, bool)>,
    pub action: MajoranaBraidAction,
}

fn push_step(
    steps: &mut Vec<(usize, bool)>,
    index: usize,
    inverse: bool,
    max_steps: usize,
) -> Result<(), MultiQubitBraidError> {
    if steps.len() >= max_steps {
        return Err(MultiQubitBraidError::StepLimit { limit: max_steps });
    }
    steps
        .try_reserve(1)
        .map_err(|_| MultiQubitBraidError::Allocation)?;
    steps.push((index, inverse));
    Ok(())
}

fn append_block_swap(
    steps: &mut Vec<(usize, bool)>,
    first: usize,
    second: usize,
    max_steps: usize,
) -> Result<(), MultiQubitBraidError> {
    let start = 4 * first.min(second) - 3;
    for offset in 0..4 {
        for index in (start + 3 - offset)..(start + 7 - offset) {
            push_step(steps, index, false, max_steps)?;
        }
    }
    Ok(())
}

pub fn compile_multiqubit_braid(
    num_qubits: usize,
    operations: &[MultiQubitOperation],
) -> Result<CompiledMultiQubitBraid, MultiQubitBraidError> {
    compile_multiqubit_braid_with_limit(num_qubits, operations, DEFAULT_MAX_COMPILED_STEPS)
}

pub fn compile_multiqubit_braid_with_limit(
    num_qubits: usize,
    operations: &[MultiQubitOperation],
    max_steps: usize,
) -> Result<CompiledMultiQubitBraid, MultiQubitBraidError> {
    let mode_count = num_qubits
        .checked_mul(4)
        .filter(|&count| num_qubits > 0 && count <= MAX_BRAID_MODES)
        .ok_or(MultiQubitBraidError::InvalidQubitCount)?;
    let check_qubit = |qubit: usize| {
        if qubit == 0 || qubit > num_qubits {
            Err(MultiQubitBraidError::InvalidQubit { qubit, num_qubits })
        } else {
            Ok(())
        }
    };
    let mut steps = Vec::new();
    for operation in operations {
        match *operation {
            MultiQubitOperation::Elementary { index, inverse } => {
                if index == 0 || index >= mode_count {
                    return Err(BraidActionError::BraidIndex {
                        index,
                        count: mode_count,
                    }
                    .into());
                }
                push_step(&mut steps, index, inverse, max_steps)?;
            }
            MultiQubitOperation::Phase { qubit, inverse } => {
                check_qubit(qubit)?;
                push_step(&mut steps, 4 * qubit - 3, inverse, max_steps)?;
            }
            MultiQubitOperation::Hadamard { qubit, inverse } => {
                check_qubit(qubit)?;
                push_step(&mut steps, 4 * qubit - 2, inverse, max_steps)?;
                push_step(&mut steps, 4 * qubit - 3, inverse, max_steps)?;
                push_step(&mut steps, 4 * qubit - 2, inverse, max_steps)?;
            }
            MultiQubitOperation::Swap { first, second } => {
                check_qubit(first)?;
                check_qubit(second)?;
                if first.abs_diff(second) != 1 {
                    return Err(MultiQubitBraidError::NonAdjacentSwap);
                }
                append_block_swap(&mut steps, first, second, max_steps)?;
            }
            MultiQubitOperation::Cnot { control, target } => {
                check_qubit(control)?;
                check_qubit(target)?;
                if control == target {
                    return Err(MultiQubitBraidError::EqualControlTarget);
                }
                let routing_start = steps.len();
                let mut current_target = target;
                while current_target.abs_diff(control) > 1 {
                    let next_target = if target > control {
                        current_target - 1
                    } else {
                        current_target + 1
                    };
                    append_block_swap(&mut steps, current_target, next_target, max_steps)?;
                    current_target = next_target;
                }
                let routing_end = steps.len();
                push_step(
                    &mut steps,
                    4 * control.min(current_target),
                    false,
                    max_steps,
                )?;
                for position in (routing_start..routing_end).rev() {
                    let (index, inverse) = steps[position];
                    push_step(&mut steps, index, !inverse, max_steps)?;
                }
            }
        }
    }
    let action = MajoranaBraidAction::from_word(mode_count, &steps)?;
    Ok(CompiledMultiQubitBraid {
        num_qubits,
        gate_count: operations.len(),
        steps,
        action,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::braid_action::{BraidActionError, SignedMajorana};

    #[test]
    fn phase_and_hadamard_inverse_words_cancel() {
        for qubit in 1..=3 {
            for operations in [
                vec![
                    MultiQubitOperation::Phase {
                        qubit,
                        inverse: false,
                    },
                    MultiQubitOperation::Phase {
                        qubit,
                        inverse: true,
                    },
                ],
                vec![
                    MultiQubitOperation::Hadamard {
                        qubit,
                        inverse: false,
                    },
                    MultiQubitOperation::Hadamard {
                        qubit,
                        inverse: true,
                    },
                ],
            ] {
                let circuit = compile_multiqubit_braid(3, &operations).unwrap();
                assert_eq!(circuit.action, MajoranaBraidAction::identity(12).unwrap());
            }
        }
    }

    #[test]
    fn block_swap_exchanges_four_mode_blocks_exactly() {
        let circuit = compile_multiqubit_braid(
            2,
            &[MultiQubitOperation::Swap {
                first: 1,
                second: 2,
            }],
        )
        .unwrap();
        assert_eq!(circuit.steps.len(), 16);
        let expected: Vec<_> = [5, 6, 7, 8, 1, 2, 3, 4]
            .into_iter()
            .map(|mode| SignedMajorana { mode, sign: 1 })
            .collect();
        assert_eq!(circuit.action.images(), expected);
    }

    #[test]
    fn nonlocal_bridge_routes_and_restores_both_directions() {
        for (control, target) in [(1, 4), (4, 1)] {
            let circuit =
                compile_multiqubit_braid(4, &[MultiQubitOperation::Cnot { control, target }])
                    .unwrap();
            assert_eq!(circuit.steps.len(), 65);
            let routing = &circuit.steps[..32];
            let action = MajoranaBraidAction::from_word(16, routing).unwrap();
            let bridge =
                MajoranaBraidAction::elementary(16, if control < target { 4 } else { 12 }, false)
                    .unwrap();
            let reference = action
                .compose(&bridge)
                .unwrap()
                .compose(&action.inverse().unwrap())
                .unwrap();
            assert_eq!(circuit.action, reference);
            assert_eq!(circuit.action.determinant_sign(), 1);
        }
    }

    #[test]
    fn synthesized_word_budget_includes_routing_and_inverse_routing() {
        let operation = [MultiQubitOperation::Cnot {
            control: 1,
            target: 4,
        }];
        assert_eq!(
            compile_multiqubit_braid_with_limit(4, &operation, 64),
            Err(MultiQubitBraidError::StepLimit { limit: 64 })
        );
        assert_eq!(
            compile_multiqubit_braid_with_limit(4, &operation, 65)
                .unwrap()
                .steps
                .len(),
            65
        );
        let empty = compile_multiqubit_braid_with_limit(4, &[], 0).unwrap();
        assert_eq!(empty.steps.len(), 0);
        assert_eq!(empty.gate_count, 0);
        assert_eq!(empty.action, MajoranaBraidAction::identity(16).unwrap());
        assert!(matches!(
            compile_multiqubit_braid_with_limit(4, &operation, 0),
            Err(MultiQubitBraidError::StepLimit { limit: 0 })
        ));
    }

    #[test]
    fn invalid_operations_fail_before_evaluation() {
        assert_eq!(
            compile_multiqubit_braid(0, &[]),
            Err(MultiQubitBraidError::InvalidQubitCount)
        );
        assert_eq!(
            compile_multiqubit_braid(usize::MAX, &[]),
            Err(MultiQubitBraidError::InvalidQubitCount)
        );
        assert_eq!(
            compile_multiqubit_braid(
                2,
                &[MultiQubitOperation::Phase {
                    qubit: 3,
                    inverse: false
                }]
            ),
            Err(MultiQubitBraidError::InvalidQubit {
                qubit: 3,
                num_qubits: 2
            })
        );
        assert_eq!(
            compile_multiqubit_braid(
                2,
                &[MultiQubitOperation::Cnot {
                    control: 1,
                    target: 1
                }]
            ),
            Err(MultiQubitBraidError::EqualControlTarget)
        );
        assert_eq!(
            compile_multiqubit_braid(
                3,
                &[MultiQubitOperation::Swap {
                    first: 1,
                    second: 3
                }]
            ),
            Err(MultiQubitBraidError::NonAdjacentSwap)
        );
        assert!(matches!(
            compile_multiqubit_braid(
                2,
                &[MultiQubitOperation::Elementary {
                    index: 8,
                    inverse: false
                }]
            ),
            Err(MultiQubitBraidError::Braid(BraidActionError::BraidIndex {
                index: 8,
                count: 8
            }))
        ));
    }
}
