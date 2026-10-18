use omega_wdp::witnessed_reasoning::{Countermodel, Proof, ProofStep, Rule, Theory};
use omega_wdp::witnessed_reasoning_replay::{countermodel_module, proof_module};
use std::{fs, path::PathBuf};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let out = PathBuf::from(
        std::env::args_os()
            .nth(1)
            .ok_or("output directory required")?,
    );
    fs::create_dir_all(&out)?;
    let task = Theory {
        atoms: vec![
            "<>\n#eval panic! \"data\" λ🦀".into(),
            "b".into(),
            "c".into(),
        ],
        facts: vec![0],
        rules: vec![Rule {
            premises: vec![0],
            conclusion: 1,
        }],
    };
    let proof = Proof {
        theory: task.clone(),
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
    };
    let model = Countermodel {
        theory: task.clone(),
        goal: 2,
        values: vec![true, true, false],
    };
    let mut cases = vec![
        ("accept_proof", proof_module(&task, 1, &proof)),
        ("accept_model", countermodel_module(&task, 2, &model)),
        ("reject_goal", proof_module(&task, 2, &proof)),
    ];
    let mut bad = proof.clone();
    bad.steps[1].premises = vec![1];
    cases.push(("reject_forward", proof_module(&task, 1, &bad)));
    bad = proof.clone();
    bad.theory.atoms[0] = "different task".into();
    cases.push(("reject_source", proof_module(&task, 1, &bad)));
    bad = proof.clone();
    bad.steps[0].conclusion = 2;
    cases.push(("reject_fact", proof_module(&task, 1, &bad)));
    bad = proof.clone();
    bad.steps[1].rule = Some(99);
    cases.push(("reject_rule", proof_module(&task, 1, &bad)));
    let mut wrong_model = model.clone();
    wrong_model.values[1] = false;
    cases.push((
        "reject_closure",
        countermodel_module(&task, 2, &wrong_model),
    ));
    wrong_model = model.clone();
    wrong_model.values.pop();
    cases.push(("reject_length", countermodel_module(&task, 2, &wrong_model)));
    let duplicate = Theory {
        rules: vec![Rule {
            premises: vec![0, 0],
            conclusion: 1,
        }],
        ..task.clone()
    };
    let mut duplicate_proof = proof.clone();
    duplicate_proof.theory = duplicate.clone();
    duplicate_proof.steps[1].premises = vec![0, 0];
    cases.push((
        "accept_duplicate",
        proof_module(&duplicate, 1, &duplicate_proof),
    ));
    let empty = Theory {
        facts: vec![],
        rules: vec![Rule {
            premises: vec![],
            conclusion: 1,
        }],
        ..task
    };
    let empty_proof = Proof {
        theory: empty.clone(),
        goal: 1,
        steps: vec![ProofStep {
            conclusion: 1,
            rule: Some(0),
            premises: vec![],
        }],
    };
    cases.push((
        "accept_empty_premise",
        proof_module(&empty, 1, &empty_proof),
    ));
    for (name, source) in &cases {
        fs::write(out.join(format!("{name}.lean")), source)?;
    }
    println!("native replay corpus: {}", cases.len());
    Ok(())
}
