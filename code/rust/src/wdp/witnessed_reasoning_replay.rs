//! Structural export of native certificates for independent Lean kernel replay.
//! The emitted theorem is about the explicit task literal. This exporter does
//! not assert a theorem about Rust execution or replace the Lean checker.

use crate::witnessed_reasoning::{Countermodel, Proof, Theory};

fn list(values: impl Iterator<Item = String>) -> String {
    format!("[{}]", values.collect::<Vec<_>>().join(", "))
}

fn text(value: &str) -> String {
    format!(
        "(String.ofList {})",
        list(
            value
                .chars()
                .map(|c| format!("(Char.ofNat {})", u32::from(c)))
        )
    )
}

pub fn theory_term(theory: &Theory) -> String {
    format!(
        "⟨{}, {}, {}⟩",
        list(theory.atoms.iter().map(|a| text(a))),
        list(theory.facts.iter().map(ToString::to_string)),
        list(theory.rules.iter().map(|r| format!(
            "⟨{}, {}⟩",
            list(r.premises.iter().map(ToString::to_string)),
            r.conclusion
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
    let steps = list(proof.steps.iter().map(|s| {
        let rule = s
            .rule
            .map_or_else(|| "none".to_owned(), |i| format!("(some {i})"));
        format!(
            "⟨{}, {}, {}⟩",
            s.conclusion,
            rule,
            list(s.premises.iter().map(ToString::to_string))
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
