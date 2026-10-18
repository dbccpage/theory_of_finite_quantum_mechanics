
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

fn default_authority_effect() -> String {
    "None".to_string()
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DdcMotifLedgerV1 {
    pub total_words: usize,
    pub total_letters: usize,
    pub ngrams: BTreeMap<usize, BTreeMap<String, u64>>,
    #[serde(default = "default_authority_effect")]
    pub authority_effect: String,
}

impl Default for DdcMotifLedgerV1 {
    fn default() -> Self {
        Self {
            total_words: 0,
            total_letters: 0,
            ngrams: BTreeMap::new(),
            authority_effect: default_authority_effect(),
        }
    }
}

pub fn mine_ddc_ngrams(words: &[&str], max_n: usize) -> DdcMotifLedgerV1 {
    let mut ledger = DdcMotifLedgerV1 {
        total_words: words.len(),
        total_letters: 0,
        ngrams: BTreeMap::new(),
        authority_effect: default_authority_effect(),
    };

    let bound_n = max_n.min(6);

    for &word in words {
        let chars: Vec<char> = word.chars().collect();
        ledger.total_letters += chars.len();

        for n in 1..=bound_n {
            if chars.len() < n {
                continue;
            }
            let n_map = ledger.ngrams.entry(n).or_default();
            for window in chars.windows(n) {
                let ngram: String = window.iter().collect();
                *n_map.entry(ngram).or_insert(0) += 1;
            }
        }
    }

    ledger
}
