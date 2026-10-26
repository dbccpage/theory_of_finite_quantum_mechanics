// Executable finite evidence; AuthorityEffect: None.
use serde::{Deserialize, Serialize};
use crate::error::WdpError;
use std::collections::{BTreeMap, HashSet, VecDeque};
use crate::genesis_observer::{HistoryMemory, WordTransducer};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum FunctionalClass {
    O1Only,
    O2 { name: String, first: Vec<usize>, second: Vec<usize> },
    OutsideO1,
}

pub fn classify_observer(
    memory: &HistoryMemory,
    profiles: &[String],
    contexts: &[(&str, &WordTransducer)],
) -> Result<FunctionalClass, WdpError> {
    HistoryMemory::new(memory.transitions.clone(), memory.initial)?;
    for (_, rho) in contexts { rho.validate_memory(memory)?; }
    if profiles.len() != memory.transitions.len() {
        return Err(WdpError::InvalidInput { detail: "one profile per memory state is required".into() });
    }
    let mut reached = HashSet::new();
    let mut q = VecDeque::new();
    reached.insert(memory.initial);
    q.push_back(memory.initial);

    while let Some(curr) = q.pop_front() {
        for &target in &memory.transitions[curr] {
            if !reached.contains(&target) {
                reached.insert(target);
                q.push_back(target);
            }
        }
    }

    let reached_profiles: HashSet<&str> = reached.iter().map(|&x| profiles[x].as_str()).collect();
    let o1 = reached_profiles.len() > 1;

    for (name, rho) in contexts {
        let first_out = memory.run(&rho.prefix_words);
        let first = (memory.initial, rho.initial, first_out);
        let mut witnesses = BTreeMap::new();
        witnesses.insert(first, Vec::new());
        let mut queue = VecDeque::new();
        queue.push_back(first);
        let mut images: BTreeMap<String, (String, Vec<usize>)> = BTreeMap::new();

        while let Some(vertex) = queue.pop_front() {
            let (source, control, output) = vertex;
            let word = witnesses.get(&vertex).unwrap().clone();
            let source_prof = profiles[source].clone();
            let final_slice: &[usize] = if control < rho.final_words.len() { &rho.final_words[control] } else { &[] };
            let img_state = memory.run_from(final_slice, output);
            let img_prof = profiles[img_state].clone();

            if let Some((prev_img, prev_word)) = images.get(&source_prof) {
                if *prev_img != img_prof {
                    return Ok(FunctionalClass::O2 {
                        name: (*name).to_string(),
                        first: prev_word.clone(),
                        second: word,
                    });
                }
            } else {
                images.insert(source_prof, (img_prof, word.clone()));
            }

            for d in 0..rho.state_transitions[0].len() {
                let emit_slice = &rho.emit[control][d];
                let next_out = memory.run_from(emit_slice, output);
                let target = (memory.transitions[source][d], rho.state_transitions[control][d], next_out);
                if !witnesses.contains_key(&target) {
                    let mut next_w = word.clone();
                    next_w.push(d);
                    witnesses.insert(target, next_w);
                    queue.push_back(target);
                }
            }
        }
    }

    Ok(if o1 {
        FunctionalClass::O1Only
    } else {
        FunctionalClass::OutsideO1
    })
}
