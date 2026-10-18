//! Obstruction Episode Segmentation (U02).
//!
//! An ObstructionEpisodeV1 represents a sequence of DDC transitions beginning
//! when an obstruction is detected (Phi1 > 0 or Gamma2 > 0) and terminating
//! on resolution (Phi1 = 0 and Gamma2 = 0), explicit refusal (M), or terminalization (T).
//!
//! Invariant: An episode cannot close as RESOLVED if Gamma2 > 0, even if Phi1 == 0.
//! Gamma2 > 0 strictly classifies as OpenObstruction.
//! AuthorityEffect: None (const).

use crate::ddc::ddc_trace::DdcStepRowV1;
use serde::{Deserialize, Serialize};

fn default_authority_effect() -> String {
    "None".to_string()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum EpisodeStatus {
    OpenObstruction,
    Resolved,
    Refused,
    Terminalized,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ObstructionEpisodeV1 {
    pub episode_id: String,
    pub open_seq: u64,
    pub close_seq: Option<u64>,
    pub initial_phi1: u64,
    pub initial_gamma2: u64,
    pub terminal_phi1: Option<u64>,
    pub terminal_gamma2: Option<u64>,
    pub steps: Vec<DdcStepRowV1>,
    pub status: EpisodeStatus,
    pub ddc_word: String,
    #[serde(default = "default_authority_effect")]
    pub authority_effect: String,
}

pub struct EpisodeSegmenter {
    active_episode: Option<ObstructionEpisodeV1>,
    completed_episodes: Vec<ObstructionEpisodeV1>,
    episode_counter: u64,
}

impl Default for EpisodeSegmenter {
    fn default() -> Self {
        Self::new()
    }
}

impl EpisodeSegmenter {
    pub fn new() -> Self {
        Self {
            active_episode: None,
            completed_episodes: Vec::new(),
            episode_counter: 0,
        }
    }

    pub fn process_step(
        &mut self,
        step: &DdcStepRowV1,
        after_phi1: u64,
        after_gamma2: u64,
    ) {
        if self.active_episode.is_none() {
            // Check if obstruction opens
            if after_phi1 > 0 || after_gamma2 > 0 {
                let ep_id = format!("EP_{:06}", self.episode_counter);
                self.episode_counter += 1;
                let ep = ObstructionEpisodeV1 {
                    episode_id: ep_id,
                    open_seq: step.seq,
                    close_seq: None,
                    initial_phi1: after_phi1,
                    initial_gamma2: after_gamma2,
                    terminal_phi1: None,
                    terminal_gamma2: None,
                    steps: vec![step.clone()],
                    status: EpisodeStatus::OpenObstruction,
                    ddc_word: step.letter.clone(),
                    authority_effect: default_authority_effect(),
                };
                self.active_episode = Some(ep);
            }
            return;
        }

        // Active episode present
        let mut ep = self.active_episode.take().unwrap();
        ep.steps.push(step.clone());
        ep.ddc_word.push_str(&step.letter);

        // Closure checks:
        if step.letter == "M" {
            ep.status = EpisodeStatus::Refused;
            ep.close_seq = Some(step.seq);
            ep.terminal_phi1 = Some(after_phi1);
            ep.terminal_gamma2 = Some(after_gamma2);
            self.completed_episodes.push(ep);
        } else if step.letter == "T" {
            ep.status = EpisodeStatus::Terminalized;
            ep.close_seq = Some(step.seq);
            ep.terminal_phi1 = Some(after_phi1);
            ep.terminal_gamma2 = Some(after_gamma2);
            self.completed_episodes.push(ep);
        } else if after_phi1 == 0 && after_gamma2 == 0 {
            // Both obstructions discharged
            ep.status = EpisodeStatus::Resolved;
            ep.close_seq = Some(step.seq);
            ep.terminal_phi1 = Some(0);
            ep.terminal_gamma2 = Some(0);
            self.completed_episodes.push(ep);
        } else {
            // WITNESS DOMINANCE / INVARIANT:
            // If after_phi1 == 0 but after_gamma2 > 0, it DOES NOT RESOLVE!
            // It remains OpenObstruction.
            ep.status = EpisodeStatus::OpenObstruction;
            self.active_episode = Some(ep);
        }
    }

    pub fn completed_episodes(&self) -> &[ObstructionEpisodeV1] {
        &self.completed_episodes
    }

    pub fn active_episode(&self) -> Option<&ObstructionEpisodeV1> {
        self.active_episode.as_ref()
    }
}
