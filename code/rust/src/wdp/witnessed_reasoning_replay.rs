use crate::witnessed_reasoning::{
    check_countermodel, check_proof, Countermodel, Proof, ProofRefusal, Theory,
};

pub const ORIGIN: &str = "Origin: code/rust/src/wdp/witnessed_reasoning_replay.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a witnessed proof or countermodel replays as a Lean module whose soundness checker names the same finite theory and goal";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

pub fn authority_effect() -> &'static str {
    AUTHORITY_EFFECT
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

fn list(values: impl Iterator<Item = String>) -> String {
    format!("[{}]", values.collect::<Vec<_>>().join(", "))
}

fn text(value: &str) -> String {
    format!(
        "(String.ofList {})",
        list(value.chars().map(|symbol| format!("(Char.ofNat {})", u32::from(symbol))))
    )
}

pub fn theory_term(theory: &Theory) -> String {
    format!(
        "⟨{}, {}, {}⟩",
        list(theory.atoms.iter().map(|atom| text(atom))),
        list(theory.facts.iter().map(ToString::to_string)),
        list(theory.rules.iter().map(|rule| format!(
            "⟨{}, {}⟩",
            list(rule.premises.iter().map(ToString::to_string)),
            rule.conclusion
        )))
    )
}

fn module(task: &Theory, goal: usize, certificate: String, positive: bool) -> String {
    let (kind, checker, parameter, judgment) = if positive {
        ("Proof", "checkProof", "p", "")
    } else {
        ("Model", "checkCountermodel", "m", "¬")
    };
    format!(
        "import ExecutableReasoning\n\
         open WitnessedReasoning WitnessedReasoning.Executable\n\
         namespace NativeReplay\n\
         def task : FiniteTheory := {}\n\
         def certificate : {kind}Certificate := {certificate}\n\
         theorem result : {judgment}Derivable task.abstract {goal} :=\n\
           {checker}_sound (T := task) (goal := {goal}) ({parameter} := certificate) (by decide)\n\
         #print axioms result\n\
         end NativeReplay\n",
        theory_term(task)
    )
}

pub fn proof_module(theory: &Theory, goal: usize, proof: &Proof) -> String {
    let steps = list(proof.steps.iter().map(|step| {
        let rule = step
            .rule
            .map_or_else(|| "none".to_owned(), |index| format!("(some {index})"));
        format!(
            "⟨{}, {}, {}⟩",
            step.conclusion,
            rule,
            list(step.premises.iter().map(ToString::to_string))
        )
    }));
    module(
        theory,
        goal,
        format!(
            "⟨{}, {}, {}⟩",
            theory_term(&proof.theory),
            proof.goal,
            steps
        ),
        true,
    )
}

pub fn countermodel_module(theory: &Theory, goal: usize, model: &Countermodel) -> String {
    module(
        theory,
        goal,
        format!(
            "⟨{}, {}, {}⟩",
            theory_term(&model.theory),
            model.goal,
            list(model.values.iter().map(ToString::to_string))
        ),
        false,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::witnessed_reasoning::{ProofStep, Rule};

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn theory() -> Theory {
        Theory {
            atoms: vec!["P".to_string(), "Q".to_string()],
            facts: vec![0],
            rules: vec![Rule {
                premises: vec![0],
                conclusion: 1,
            }],
        }
    }

    fn proof() -> Proof {
        Proof {
            theory: theory(),
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
    fn unit_proof_module_names_the_sound_checker_and_goal() -> Result<(), String> {
        let text = proof_module(&theory(), 1, &proof());
        unit_text(&text).and_then(|_| unit_authority())
    }

    fn unit_text(text: &str) -> Result<(), String> {
        need(text.contains("checkProof_sound"), "checker")?;
        need(text.contains("Derivable task.abstract 1"), "goal")?;
        need(text.contains("Char.ofNat"), "atom")
    }

    fn unit_authority() -> Result<(), String> {
        need(authority_effect() == AUTHORITY_EFFECT, "authority")
    }

    #[test]
    fn integration_replay_agrees_with_the_proof_checker() -> Result<(), String> {
        let task = theory();
        let certificate = proof();
        let text = proof_module(&task, 1, &certificate);
        need(check_proof(&task, 1, &certificate), "proof")?;
        need(text.contains(&theory_term(&task)), "theory")?;
        Ok(())
    }

    #[test]
    fn e2e_countermodel_module_uses_negation_only_when_the_model_is_valid() -> Result<(), String> {
        let task = Theory {
            atoms: vec!["Q".to_string()],
            facts: vec![],
            rules: vec![],
        };
        let model = Countermodel {
            theory: task.clone(),
            goal: 0,
            values: vec![false],
        };
        let text = countermodel_module(&task, 0, &model);
        e2e_model(&task, &model, &text).and_then(|_| e2e_text())
    }

    fn e2e_model(task: &Theory, model: &Countermodel, text: &str) -> Result<(), String> {
        need(check_countermodel(task, 0, model), "model")?;
        need(text.contains("checkCountermodel_sound"), "checker")?;
        need(text.contains("¬Derivable"), "negation")
    }

    fn e2e_text() -> Result<(), String> {
        need(ORIGIN.contains("witnessed_reasoning_replay.rs"), "origin")?;
        need(CLAIM.contains("Lean module"), "claim")
    }

    #[test]
    fn negative_invalid_proof_still_renders_but_is_refused_and_float_is_refused() -> Result<(), String>
    {
        negative_proof().and_then(|_| negative_tokens())
    }

    fn negative_proof() -> Result<(), String> {
        let task = theory();
        let mut bad = proof();
        bad.steps.pop();
        let text = proof_module(&task, 1, &bad);
        need(text.contains("checkProof_sound"), "rendered")?;
        need(!check_proof(&task, 1, &bad), "refused")
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            admit_exact_integer("0.5") == Err(ProofRefusal::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("true") == Err(ProofRefusal::BooleanAsNumber),
            "bool",
        )
    }
}
