//! The source observer-world five: (image(profile), contexts, histories, witnesses, grammar).
//! A finite closed history restriction is declared explicitly. It supplies neither
//! memory updates nor a grammar interpretation unless those maps are supplied.
use std::collections::BTreeSet;

use omega_category_theory::context_reflection::ContextSystem;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorldWitness {
    pub left: usize,
    pub right: usize,
    pub context: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteObserverWorldPacket {
    pub alphabet: Vec<String>,
    pub histories: Vec<Vec<usize>>,
    pub profiles: Vec<String>,
    pub presented_profiles: Vec<usize>,
    pub contexts: Vec<String>,
    /// Context-major maps on the complete declared history carrier.
    pub context_actions: Vec<Vec<usize>>,
    pub witnesses: Vec<WorldWitness>,
    pub grammar: Vec<String>,
    /// An optional explicit interpretation of every grammar expression.
    pub grammar_interpretation: Option<Vec<BTreeSet<usize>>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum WorldAdapterError {
    InvalidCarrier,
    InvalidContext,
    InvalidWitness,
    InvalidGrammar,
    MissingGrammarInterpretation,
    ReceiptMismatch,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObserverWorldReceipt {
    packet: FiniteObserverWorldPacket,
    context_system: ContextSystem,
}

fn valid_labels(labels: &[String]) -> bool {
    labels.iter().all(|label| !label.is_empty())
        && labels.iter().collect::<BTreeSet<_>>().len() == labels.len()
}

impl FiniteObserverWorldPacket {
    pub fn adapt(&self) -> Result<ObserverWorldReceipt, WorldAdapterError> {
        let n = self.histories.len();
        if n == 0
            || !valid_labels(&self.alphabet)
            || !valid_labels(&self.profiles)
            || self.histories.iter().collect::<BTreeSet<_>>().len() != n
            || self
                .histories
                .iter()
                .flatten()
                .any(|&d| d >= self.alphabet.len())
            || self.presented_profiles.len() != n
            || self
                .presented_profiles
                .iter()
                .any(|&p| p >= self.profiles.len())
            || self
                .presented_profiles
                .iter()
                .copied()
                .collect::<BTreeSet<_>>()
                .len()
                != self.profiles.len()
        {
            return Err(WorldAdapterError::InvalidCarrier);
        }
        if !valid_labels(&self.contexts)
            || self.context_actions.len() != self.contexts.len()
            || self
                .context_actions
                .iter()
                .any(|map| map.len() != n || map.iter().any(|&h| h >= n))
        {
            return Err(WorldAdapterError::InvalidContext);
        }
        if !valid_labels(&self.grammar)
            || self
                .grammar_interpretation
                .as_ref()
                .is_some_and(|interpretation| {
                    interpretation.len() != self.grammar.len()
                        || interpretation
                            .iter()
                            .flatten()
                            .any(|&p| p >= self.profiles.len())
                })
        {
            return Err(WorldAdapterError::InvalidGrammar);
        }
        let transitions = (0..n)
            .map(|h| self.context_actions.iter().map(|map| map[h]).collect())
            .collect();
        let system = ContextSystem::new(
            self.presented_profiles.clone(),
            transitions,
            self.contexts.len(),
        )
        .map_err(|_| WorldAdapterError::InvalidContext)?;
        for witness in &self.witnesses {
            if witness.left >= n || witness.right >= n || witness.context >= self.contexts.len() {
                return Err(WorldAdapterError::InvalidWitness);
            }
            let map = &self.context_actions[witness.context];
            if !system.related(witness.left, witness.right)
                || system.related(map[witness.left], map[witness.right])
            {
                return Err(WorldAdapterError::InvalidWitness);
            }
        }
        Ok(ObserverWorldReceipt {
            packet: self.clone(),
            context_system: system,
        })
    }
}

impl ObserverWorldReceipt {
    pub fn packet(&self) -> &FiniteObserverWorldPacket {
        &self.packet
    }
    pub fn context_system(&self) -> &ContextSystem {
        &self.context_system
    }

    /// Source facts require both declared grammar expressibility and forward
    /// context stability. Noncongruent contexts are retained on histories.
    pub fn facts(&self) -> Result<BTreeSet<BTreeSet<usize>>, WorldAdapterError> {
        let interpretation = self
            .packet
            .grammar_interpretation
            .as_ref()
            .ok_or(WorldAdapterError::MissingGrammarInterpretation)?;
        Ok(interpretation
            .iter()
            .filter(|subset| {
                self.packet.context_actions.iter().all(|map| {
                    self.packet
                        .presented_profiles
                        .iter()
                        .enumerate()
                        .all(|(h, p)| {
                            !subset.contains(p)
                                || subset.contains(&self.packet.presented_profiles[map[h]])
                        })
                })
            })
            .cloned()
            .collect())
    }

    pub fn verify_against(
        &self,
        packet: &FiniteObserverWorldPacket,
    ) -> Result<(), WorldAdapterError> {
        if self.packet != *packet || packet.adapt()? != *self {
            return Err(WorldAdapterError::ReceiptMismatch);
        }
        Ok(())
    }
}
