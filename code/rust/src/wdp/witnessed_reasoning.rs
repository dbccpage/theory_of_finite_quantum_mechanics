pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/witnessed_reasoning.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a finite Horn proof is valid exactly when every step is a declared fact or an earlier application of a declared rule, and a countermodel falsifies the goal while keeping facts and rules";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ProofRefusal {
    InvalidTheory,
    GoalOutOfRange { goal: usize, atoms: usize },
    ProofGoal { proof_goal: usize, goal: usize },
    ForeignTheory,
    StepAtom { step: usize, conclusion: usize, atoms: usize },
    UndeclaredFact { step: usize, conclusion: usize },
    FactHasPremises { step: usize },
    MissingRule { step: usize, rule: usize },
    RuleConclusion { step: usize },
    PremiseCount { step: usize },
    PremiseOrder { step: usize, premise: usize },
    GoalUnreached,
    ModelLength { values: usize, atoms: usize },
    GoalNotFalse,
    FactFalse { atom: usize },
    RuleBroken { rule: usize },
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Rule {
    pub premises: Vec<usize>,
    pub conclusion: usize,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Theory {
    pub atoms: Vec<String>,
    pub facts: Vec<usize>,
    pub rules: Vec<Rule>,
}

impl Theory {
    pub fn valid(&self) -> bool {
        self.atoms_distinct() && self.facts_in_range() && self.rules_in_range()
    }

    fn atoms_distinct(&self) -> bool {
        self.atoms.iter().enumerate().all(|(index, atom)| {
            !atom.is_empty() && !self.atoms[..index].contains(atom)
        })
    }

    fn facts_in_range(&self) -> bool {
        self.facts.iter().all(|atom| atom < &self.atoms.len())
    }

    fn rules_in_range(&self) -> bool {
        self.rules.iter().all(|rule| {
            rule.conclusion < self.atoms.len()
                && rule.premises.iter().all(|atom| atom < &self.atoms.len())
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ProofStep {
    pub conclusion: usize,
    pub rule: Option<usize>,
    pub premises: Vec<usize>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Proof {
    pub theory: Theory,
    pub goal: usize,
    pub steps: Vec<ProofStep>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Countermodel {
    pub theory: Theory,
    pub goal: usize,
    pub values: Vec<bool>,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, ProofRefusal> {
    if token == "true" || token == "false" {
        return Err(ProofRefusal::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(ProofRefusal::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, ProofRefusal> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(ProofRefusal::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(ProofRefusal::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(ProofRefusal::Overflow)?;
    }
    Ok(value)
}

fn header_refusal(theory: &Theory, goal: usize, proof: &Proof) -> Option<ProofRefusal> {
    if !theory.valid() {
        return Some(ProofRefusal::InvalidTheory);
    }
    if goal >= theory.atoms.len() {
        return Some(ProofRefusal::GoalOutOfRange {
            goal,
            atoms: theory.atoms.len(),
        });
    }
    if proof.goal != goal {
        return Some(ProofRefusal::ProofGoal {
            proof_goal: proof.goal,
            goal,
        });
    }
    if &proof.theory != theory {
        return Some(ProofRefusal::ForeignTheory);
    }
    None
}

fn fact_refusal(theory: &Theory, step_index: usize, step: &ProofStep) -> Option<ProofRefusal> {
    if !theory.facts.contains(&step.conclusion) {
        return Some(ProofRefusal::UndeclaredFact {
            step: step_index,
            conclusion: step.conclusion,
        });
    }
    if !step.premises.is_empty() {
        return Some(ProofRefusal::FactHasPremises { step: step_index });
    }
    None
}

fn earlier_conclusion(proof: &Proof, step_index: usize, premise: usize) -> Option<usize> {
    if premise >= step_index {
        return None;
    }
    proof.steps.get(premise).map(|step| step.conclusion)
}

fn rule_refusal(
    theory: &Theory,
    proof: &Proof,
    step_index: usize,
    step: &ProofStep,
    rule_index: usize,
) -> Option<ProofRefusal> {
    let Some(rule) = theory.rules.get(rule_index) else {
        return Some(ProofRefusal::MissingRule {
            step: step_index,
            rule: rule_index,
        });
    };
    if step.conclusion != rule.conclusion {
        return Some(ProofRefusal::RuleConclusion { step: step_index });
    }
    if step.premises.len() != rule.premises.len() {
        return Some(ProofRefusal::PremiseCount { step: step_index });
    }
    let broken = step
        .premises
        .iter()
        .zip(&rule.premises)
        .find(|(&premise, &atom)| earlier_conclusion(proof, step_index, premise) != Some(atom));
    broken.map(|(&premise, _)| ProofRefusal::PremiseOrder {
        step: step_index,
        premise,
    })
}

fn step_refusal(
    theory: &Theory,
    proof: &Proof,
    step_index: usize,
    step: &ProofStep,
) -> Option<ProofRefusal> {
    if step.conclusion >= theory.atoms.len() {
        return Some(ProofRefusal::StepAtom {
            step: step_index,
            conclusion: step.conclusion,
            atoms: theory.atoms.len(),
        });
    }
    match step.rule {
        None => fact_refusal(theory, step_index, step),
        Some(rule) => rule_refusal(theory, proof, step_index, step, rule),
    }
}

pub fn explain_proof(theory: &Theory, goal: usize, proof: &Proof) -> Result<(), ProofRefusal> {
    if let Some(error) = header_refusal(theory, goal, proof) {
        return Err(error);
    }
    for (index, step) in proof.steps.iter().enumerate() {
        if let Some(error) = step_refusal(theory, proof, index, step) {
            return Err(error);
        }
    }
    match proof.steps.last() {
        Some(step) if step.conclusion == goal => Ok(()),
        _ => Err(ProofRefusal::GoalUnreached),
    }
}

pub fn check_proof(theory: &Theory, goal: usize, proof: &Proof) -> bool {
    explain_proof(theory, goal, proof).is_ok()
}

fn model_header<'a>(
    theory: &'a Theory,
    goal: usize,
    model: &'a Countermodel,
) -> Result<&'a [bool], ProofRefusal> {
    if !theory.valid() {
        return Err(ProofRefusal::InvalidTheory);
    }
    if goal >= theory.atoms.len() {
        return Err(ProofRefusal::GoalOutOfRange {
            goal,
            atoms: theory.atoms.len(),
        });
    }
    if model.goal != goal || &model.theory != theory {
        return Err(ProofRefusal::ForeignTheory);
    }
    if model.values.len() != theory.atoms.len() {
        return Err(ProofRefusal::ModelLength {
            values: model.values.len(),
            atoms: theory.atoms.len(),
        });
    }
    Ok(&model.values)
}

fn goal_is_false(values: &[bool], goal: usize) -> Result<(), ProofRefusal> {
    match values.get(goal) {
        Some(false) => Ok(()),
        _ => Err(ProofRefusal::GoalNotFalse),
    }
}

fn facts_hold(theory: &Theory, values: &[bool]) -> Result<(), ProofRefusal> {
    for atom in &theory.facts {
        match values.get(*atom) {
            Some(true) => {}
            _ => return Err(ProofRefusal::FactFalse { atom: *atom }),
        }
    }
    Ok(())
}

fn premise_value(values: &[bool], atom: usize) -> bool {
    matches!(values.get(atom), Some(true))
}

fn rule_holds(values: &[bool], rule: &Rule) -> bool {
    if !rule.premises.iter().all(|atom| premise_value(values, *atom)) {
        return true;
    }
    premise_value(values, rule.conclusion)
}

fn rules_hold(theory: &Theory, values: &[bool]) -> Result<(), ProofRefusal> {
    for (index, rule) in theory.rules.iter().enumerate() {
        if !rule_holds(values, rule) {
            return Err(ProofRefusal::RuleBroken { rule: index });
        }
    }
    Ok(())
}

pub fn explain_countermodel(
    theory: &Theory,
    goal: usize,
    model: &Countermodel,
) -> Result<(), ProofRefusal> {
    let values = model_header(theory, goal, model)?;
    goal_is_false(values, goal)?;
    facts_hold(theory, values)?;
    rules_hold(theory, values)
}

pub fn check_countermodel(theory: &Theory, goal: usize, model: &Countermodel) -> bool {
    explain_countermodel(theory, goal, model).is_ok()
}

pub fn authority_effect() -> &'static str {
    AUTHORITY_EFFECT
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn implication() -> Theory {
        Theory {
            atoms: vec!["P".to_string(), "Q".to_string()],
            facts: vec![0],
            rules: vec![Rule {
                premises: vec![0],
                conclusion: 1,
            }],
        }
    }

    fn modus_ponens() -> Proof {
        Proof {
            theory: implication(),
            goal: 1,
            steps: vec![
                ProofStep {
                    conclusion: 0,
                    rule: None,
                    premises: vec![],
                },
                ProofStep {
                    conclusion: 1,
                    rule: Some(0),
                    premises: vec![0],
                },
            ],
        }
    }

    #[test]
    fn unit_modus_ponens_is_valid_and_a_skipped_premise_is_not() -> Result<(), String> {
        let theory = implication();
        let proof = modus_ponens();
        need(check_proof(&theory, 1, &proof), "valid")?;
        let mut skipped = proof.clone();
        let _ = skipped.steps.remove(0);
        need(!check_proof(&theory, 1, &skipped), "skipped")?;
        need(
            matches!(
                explain_proof(&theory, 1, &skipped),
                Err(ProofRefusal::PremiseOrder { .. })
            ),
            "order",
        )?;
        Ok(())
    }

    #[test]
    fn integration_countermodel_keeps_an_open_atom_false() -> Result<(), String> {
        let theory = Theory {
            atoms: vec!["P".to_string(), "Q".to_string()],
            facts: vec![],
            rules: vec![],
        };
        let model = Countermodel {
            theory: theory.clone(),
            goal: 1,
            values: vec![false, false],
        };
        need(check_countermodel(&theory, 1, &model), "open")?;
        need(authority_effect() == AUTHORITY_EFFECT, "authority")?;
        Ok(())
    }

    #[test]
    fn e2e_valid_proof_and_refusing_countermodel_agree() -> Result<(), String> {
        let theory = implication();
        let proof = modus_ponens();
        let model = Countermodel {
            theory: theory.clone(),
            goal: 1,
            values: vec![true, false],
        };
        need(check_proof(&theory, 1, &proof), "proof")?;
        need(!check_countermodel(&theory, 1, &model), "rule")?;
        need(
            matches!(
                explain_countermodel(&theory, 1, &model),
                Err(ProofRefusal::RuleBroken { rule: 0 })
            ),
            "broken",
        )?;
        need(ORIGIN.contains("witnessed_reasoning.rs"), "origin")?;
        need(CLAIM.contains("Horn proof"), "claim")?;
        Ok(())
    }

    #[test]
    fn negative_refuses_invalid_theory_true_goal_float_and_boolean() -> Result<(), String> {
        let theory = Theory {
            atoms: vec!["".to_string()],
            facts: vec![],
            rules: vec![],
        };
        let proof = Proof {
            theory: theory.clone(),
            goal: 0,
            steps: vec![],
        };
        need(
            matches!(explain_proof(&theory, 0, &proof), Err(ProofRefusal::InvalidTheory)),
            "theory",
        )?;
        let open = Theory {
            atoms: vec!["Q".to_string()],
            facts: vec![],
            rules: vec![],
        };
        let affirmed = Countermodel {
            theory: open.clone(),
            goal: 0,
            values: vec![true],
        };
        need(
            matches!(
                explain_countermodel(&open, 0, &affirmed),
                Err(ProofRefusal::GoalNotFalse)
            ),
            "goal",
        )?;
        need(
            admit_exact_integer("1.0") == Err(ProofRefusal::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("false") == Err(ProofRefusal::BooleanAsNumber),
            "bool",
        )?;
        Ok(())
    }
}
