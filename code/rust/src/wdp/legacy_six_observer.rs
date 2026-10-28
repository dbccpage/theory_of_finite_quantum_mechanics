use crate::legacy_observer_adapters::{
    adapt_finite_quotient, AdaptedObserver, AdapterError, SourceCustody,
};
use crate::observer::QuotientObserver;
use num_traits::Zero;
use tfqm_functional::phi1::{ExactPhi1Certificate, Phi1Functional};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SixObserverAdapter {
    presentation: AdaptedObserver,
    carrier: Vec<String>,
    terms: Vec<String>,
    receipts: Vec<ExactPhi1Certificate>,
    pair_receipts: Vec<Vec<ExactPhi1Certificate>>,
    relation: Vec<Vec<bool>>,
    terminal_labels: Vec<String>,
    terminalizer: Vec<usize>,
}
impl SixObserverAdapter {
    pub fn try_new(
        carrier: Vec<String>,
        terms: Vec<String>,
        receipts: Vec<ExactPhi1Certificate>,
        pair_receipts: Vec<Vec<ExactPhi1Certificate>>,
        relation: Vec<Vec<bool>>,
        terminal_labels: Vec<String>,
        terminalizer: Vec<usize>,
        custody: SourceCustody,
    ) -> Result<Self, AdapterError> {
        let n = terms.len();
        if n == 0
            || receipts.len() != n
            || pair_receipts.len() != n
            || relation.len() != n
            || pair_receipts.iter().any(|r| r.len() != n)
            || relation.iter().any(|r| r.len() != n)
            || terminalizer.len() != n
            || terminal_labels.is_empty()
            || terminalizer.iter().any(|&i| i >= terminal_labels.len())
            || terms
                .iter()
                .collect::<std::collections::BTreeSet<_>>()
                .len()
                != n
            || carrier
                .iter()
                .collect::<std::collections::BTreeSet<_>>()
                .len()
                != carrier.len()
        {
            return Err(AdapterError::MissingSemantics(
                "complete six-tuple finite domain",
            ));
        }
        let first = &receipts[0];
        if first.omega.len() != carrier.len() {
            return Err(AdapterError::InvalidEvaluatorDomain);
        }
        for c in &receipts {
            Phi1Functional::verify_exact_certificate(c.clone())
                .map_err(|_| AdapterError::InvalidEvaluatorDomain)?;
            if c.d0 != first.d0 || c.weights != first.weights {
                return Err(AdapterError::InvalidEvaluatorDomain);
            }
        }
        for i in 0..n {
            for j in 0..n {
                let c = &pair_receipts[i][j];
                let verified = Phi1Functional::verify_exact_certificate(c.clone())
                    .map_err(|_| AdapterError::InvalidEvaluatorDomain)?;
                if c.d0 != first.d0
                    || c.weights != first.weights
                    || c.omega
                        != receipts[i]
                            .omega
                            .iter()
                            .zip(&receipts[j].omega)
                            .map(|(a, b)| a - b)
                            .collect::<Vec<_>>()
                    || relation[i][j] != verified.value().is_zero()
                {
                    return Err(AdapterError::InvalidPresentation);
                }
                if receipts[i] == receipts[j] && terminalizer[i] != terminalizer[j] {
                    return Err(AdapterError::InvalidEvaluatorDomain);
                }
            }
        }
        let mut classes: Vec<Vec<String>> = Vec::new();
        let mut assigned = vec![false; n];
        for i in 0..n {
            if !assigned[i] {
                let mut class = Vec::new();
                for j in 0..n {
                    if relation[i][j] {
                        assigned[j] = true;
                        class.push(terms[j].clone());
                    }
                }
                classes.push(class);
            }
        }
        let quotient = QuotientObserver::new(
            terms.iter().cloned().collect(),
            classes
                .into_iter()
                .map(|c| c.into_iter().collect())
                .collect(),
            "independently certified p(x)-p(y) in image(d0)".into(),
        )
        .map_err(|_| AdapterError::InvalidPresentation)?;
        let presentation = adapt_finite_quotient(&quotient, custody)?;
        Ok(Self {
            presentation,
            carrier,
            terms,
            receipts,
            pair_receipts,
            relation,
            terminal_labels,
            terminalizer,
        })
    }
    pub fn presentation(&self) -> &AdaptedObserver {
        &self.presentation
    }
    pub fn carrier(&self) -> &[String] {
        &self.carrier
    }
    pub fn terms(&self) -> &[String] {
        &self.terms
    }
    pub fn receipts(&self) -> &[ExactPhi1Certificate] {
        &self.receipts
    }
    pub fn pair_receipts(&self) -> &[Vec<ExactPhi1Certificate>] {
        &self.pair_receipts
    }
    pub fn relation(&self) -> &[Vec<bool>] {
        &self.relation
    }
    pub fn terminal(&self, term: usize) -> Option<&str> {
        self.terminalizer
            .get(term)
            .map(|&i| self.terminal_labels[i].as_str())
    }
}
