use crate::genesis_carrier::{
    CarrierError, CarrierRequest, PassageAnswer, PassageCarrier, PassageQuestion,
};
use crate::genesis_passage::PassageEvent;
use omega_category_theory::finite_joint_dynamics::{
    JointDynamics, JointDynamicsError, JointOperation,
};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Side {
    Left,
    Right,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LicenseInteraction {
    pub source: Side,
    pub question: PassageQuestion,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PassageJointRequest {
    pub left: CarrierRequest,
    pub right: CarrierRequest,
    pub pairs: Vec<(usize, usize)>,
    pub interactions: Vec<LicenseInteraction>,
    pub max_cells: usize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PassageJointError {
    Carrier(CarrierError),
    Joint(JointDynamicsError),
    InvalidRelation,
    NonBooleanInteraction,
    InteractionOutsideCarrier { row: usize, interaction: usize },
    WorkLimit,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PassageJoint {
    source: PassageJointRequest,
    left: PassageCarrier,
    right: PassageCarrier,
    joint: JointDynamics,
}
impl PassageJoint {
    pub fn build(request: &PassageJointRequest) -> Result<Self, PassageJointError> {
        let work = request
            .interactions
            .len()
            .checked_add(1)
            .and_then(|n| n.checked_mul(request.pairs.len()));
        if work.is_none_or(|n| n > request.max_cells) {
            return Err(PassageJointError::WorkLimit);
        }
        let left = PassageCarrier::build(&request.left).map_err(PassageJointError::Carrier)?;
        let right = PassageCarrier::build(&request.right).map_err(PassageJointError::Carrier)?;
        let ls = &left.certificate().states;
        let rs = &right.certificate().states;
        let pairs: BTreeMap<_, _> = request
            .pairs
            .iter()
            .copied()
            .enumerate()
            .map(|(i, p)| (p, i))
            .collect();
        if request.pairs.is_empty()
            || pairs.len() != request.pairs.len()
            || request
                .pairs
                .iter()
                .any(|&(l, r)| l >= ls.len() || r >= rs.len())
        {
            return Err(PassageJointError::InvalidRelation);
        }
        let left_ids: BTreeMap<_, _> = ls.iter().enumerate().map(|(i, s)| (s, i)).collect();
        let right_ids: BTreeMap<_, _> = rs.iter().enumerate().map(|(i, s)| (s, i)).collect();
        let mut operations: Vec<_> = (0..request.left.alphabet.len())
            .map(JointOperation::Left)
            .chain((0..request.right.alphabet.len()).map(JointOperation::Right))
            .collect();
        for (interaction, op) in request.interactions.iter().enumerate() {
            let mut targets = Vec::new();
            for (row, &(l, r)) in request.pairs.iter().enumerate() {
                let (source, target, ids) = match op.source {
                    Side::Left => (&ls[l], &rs[r], &right_ids),
                    Side::Right => (&rs[r], &ls[l], &left_ids),
                };
                let PassageAnswer::Bool(value) = op.question.answer(source) else {
                    return Err(PassageJointError::NonBooleanInteraction);
                };
                let event = PassageEvent::SetLicense(value);
                if !target.enabled(&event) {
                    targets.push(None);
                    continue;
                }
                let next = target.step(&event);
                let err = || PassageJointError::InteractionOutsideCarrier { row, interaction };
                let &id = ids.get(&next).ok_or_else(err)?;
                let pair = match op.source {
                    Side::Left => (l, id),
                    Side::Right => (id, r),
                };
                targets.push(Some(*pairs.get(&pair).ok_or_else(err)?));
            }
            operations.push(JointOperation::Interaction(targets));
        }
        let joint = JointDynamics::new(
            left.dynamics(),
            right.dynamics(),
            request.pairs.clone(),
            &operations,
            request.max_cells,
        )
        .map_err(PassageJointError::Joint)?;
        Ok(Self {
            source: request.clone(),
            left,
            right,
            joint,
        })
    }
    pub fn source(&self) -> &PassageJointRequest {
        &self.source
    }
    pub fn left(&self) -> &PassageCarrier {
        &self.left
    }
    pub fn right(&self) -> &PassageCarrier {
        &self.right
    }
    pub fn joint(&self) -> &JointDynamics {
        &self.joint
    }
}
