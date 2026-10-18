//! Definite Horn certificate checking on an explicitly supplied finite theory.
//! Exact source equality binds certificates; neither acceptance nor non-entailment
//! supplies empirical premises or an authorization decision.

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
        let n = self.atoms.len();
        self.atoms
            .iter()
            .enumerate()
            .all(|(i, a)| !a.is_empty() && !self.atoms[..i].contains(a))
            && self.facts.iter().all(|&a| a < n)
            && self
                .rules
                .iter()
                .all(|r| r.conclusion < n && r.premises.iter().all(|&a| a < n))
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

pub fn check_proof(theory: &Theory, goal: usize, proof: &Proof) -> bool {
    if !theory.valid()
        || goal >= theory.atoms.len()
        || proof.goal != goal
        || &proof.theory != theory
    {
        return false;
    }
    for (i, step) in proof.steps.iter().enumerate() {
        if step.conclusion >= theory.atoms.len() {
            return false;
        }
        match step.rule {
            None => {
                if !theory.facts.contains(&step.conclusion) || !step.premises.is_empty() {
                    return false;
                }
            }
            Some(index) => {
                let Some(rule) = theory.rules.get(index) else {
                    return false;
                };
                if step.conclusion != rule.conclusion
                    || step.premises.len() != rule.premises.len()
                    || !step
                        .premises
                        .iter()
                        .zip(&rule.premises)
                        .all(|(&j, &a)| j < i && proof.steps[j].conclusion == a)
                {
                    return false;
                }
            }
        }
    }
    proof.steps.last().is_some_and(|s| s.conclusion == goal)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Countermodel {
    pub theory: Theory,
    pub goal: usize,
    pub values: Vec<bool>,
}

pub fn check_countermodel(theory: &Theory, goal: usize, model: &Countermodel) -> bool {
    theory.valid()
        && goal < theory.atoms.len()
        && model.goal == goal
        && &model.theory == theory
        && model.values.len() == theory.atoms.len()
        && !model.values[goal]
        && theory.facts.iter().all(|&a| model.values[a])
        && theory
            .rules
            .iter()
            .all(|r| !r.premises.iter().all(|&a| model.values[a]) || model.values[r.conclusion])
}
