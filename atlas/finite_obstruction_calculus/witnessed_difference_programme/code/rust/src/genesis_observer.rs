// Executable finite evidence; AuthorityEffect: None.
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, VecDeque};
use crate::error::WdpError;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HistoryMemory {
    pub transitions: Vec<Vec<usize>>,
    pub initial: usize,
}

impl HistoryMemory {
    pub fn new(transitions: Vec<Vec<usize>>, initial: usize) -> Result<Self, WdpError> {
        let n = transitions.len();
        if n == 0 {
            return Err(WdpError::InvalidInput { detail: "Empty state table".into() });
        }
        if initial >= n {
            return Err(WdpError::InvalidInput { detail: "Initial state out of range".into() });
        }
        let alphabet_len = transitions[0].len();
        for row in &transitions {
            if row.len() != alphabet_len {
                return Err(WdpError::InvalidInput { detail: "Ragged transition table".into() });
            }
            for &next in row {
                if next >= n {
                    return Err(WdpError::InvalidInput { detail: "Target state out of range".into() });
                }
            }
        }
        Ok(Self { transitions, initial })
    }

    pub fn run_from(&self, word: &[usize], start: usize) -> usize {
        let mut state = start;
        for &sym in word {
            state = self.transitions[state][sym];
        }
        state
    }

    pub fn run(&self, word: &[usize]) -> usize {
        self.run_from(word, self.initial)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct WordTransducer {
    pub state_transitions: Vec<Vec<usize>>,
    pub emit: Vec<Vec<Vec<usize>>>,
    pub initial: usize,
    pub prefix_words: Vec<usize>,
    pub final_words: Vec<Vec<usize>>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum DescentResult {
    Map { prefix: Vec<usize>, certificate: Vec<Option<usize>> },
    Collision { first: Vec<usize>, second: Vec<usize> },
}

impl WordTransducer {
    pub fn new(
        state_transitions: Vec<Vec<usize>>,
        emit: Vec<Vec<Vec<usize>>>,
        initial: usize,
        prefix_words: Vec<usize>,
        final_words: Vec<Vec<usize>>,
    ) -> Result<Self, WdpError> {
        let n = state_transitions.len();
        if n == 0 || initial >= n {
            return Err(WdpError::InvalidInput { detail: "Invalid state space".into() });
        }
        let k = state_transitions[0].len();
        if state_transitions.iter().any(|row| row.len() != k || row.iter().any(|&s| s >= n))
            || emit.len() != n || emit.iter().any(|row| row.len() != k)
            || final_words.len() != n
            || prefix_words.iter().chain(final_words.iter().flatten()).chain(emit.iter().flatten().flatten()).any(|&s| s >= k)
        {
            return Err(WdpError::InvalidInput { detail: "invalid transducer shape, state target, or output symbol".into() });
        }
        Ok(Self {
            state_transitions,
            emit,
            initial,
            prefix_words,
            final_words,
        })
    }

    pub fn apply(&self, word: &[usize]) -> Vec<usize> {
        let mut state = self.initial;
        let mut out = self.prefix_words.clone();
        for &sym in word {
            let next = self.state_transitions[state][sym];
            let emission = &self.emit[state][sym];
            out.extend_from_slice(emission);
            state = next;
        }
        if state < self.final_words.len() {
            out.extend_from_slice(&self.final_words[state]);
        }
        out
    }

    pub fn validate_memory(&self, memory: &HistoryMemory) -> Result<(), WdpError> {
        HistoryMemory::new(memory.transitions.clone(), memory.initial)?;
        Self::new(self.state_transitions.clone(), self.emit.clone(), self.initial, self.prefix_words.clone(), self.final_words.clone())?;
        if self.state_transitions[0].len() != memory.transitions[0].len() {
            return Err(WdpError::InvalidInput { detail: "transducer and memory alphabets differ".into() });
        }
        Ok(())
    }

    pub fn descent(&self, memory: &HistoryMemory) -> Result<DescentResult, WdpError> {
        self.validate_memory(memory)?;
        let k = self.state_transitions[0].len();
        let first_output = memory.run(&self.prefix_words);
        let first = (memory.initial, self.initial, first_output);

        let mut witnesses = BTreeMap::new();
        witnesses.insert(first, Vec::new());
        let mut queue = VecDeque::new();
        queue.push_back(first);
        let mut images: BTreeMap<usize, (usize, Vec<usize>)> = BTreeMap::new();

        while let Some(vertex) = queue.pop_front() {
            let (source, control, output) = vertex;
            let final_slice: &[usize] = if control < self.final_words.len() { &self.final_words[control] } else { &[] };
            let image = memory.run_from(final_slice, output);
            let word = witnesses.get(&vertex).unwrap().clone();

            if let Some((prev_image, prev_word)) = images.get(&source) {
                if *prev_image != image {
                    return Ok(DescentResult::Collision {
                        first: prev_word.clone(),
                        second: word,
                    });
                }
            } else {
                images.insert(source, (image, word.clone()));
            }

            for d in 0..k {
                let emit_slice = &self.emit[control][d];
                let next_output = memory.run_from(emit_slice, output);
                let next_vertex = (memory.transitions[source][d], self.state_transitions[control][d], next_output);
                if !witnesses.contains_key(&next_vertex) {
                    let mut next_word = word.clone();
                    next_word.push(d);
                    witnesses.insert(next_vertex, next_word);
                    queue.push_back(next_vertex);
                }
            }
        }

        let mut map_tuple = Vec::new();
        for s in 0..memory.transitions.len() {
            map_tuple.push(images.get(&s).map(|(img, _)| *img));
        }

        Ok(DescentResult::Map {
            prefix: self.prefix_words.clone(),
            certificate: map_tuple,
        })
    }
}
