use engine_number_theory::cyclotomic_field::Cyclotomic;
use engine_number_theory::rational::rq;
use engine_number_theory::real_embedding::RealEmbeddings;
use engine_quantum_physics::embedding_relativity::{
    born_weights, conductor_5_witness, conductor_8_witness, galois_born_weights,
    positivity_under_embeddings, PositivityError,
};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Block03VerificationReceipt {
    pub real_embeddings_of_target_field: usize,
    pub embedding_relative_mixed_witness_conductor: usize,
    pub embedding_relative_witness_matrix: String,
    pub conductor_5_positive_classes: Vec<usize>,
    pub conductor_8_positive_classes: Vec<usize>,
    pub galois_covariance_of_born_probabilities: bool,
    pub galois_covariance_fixture_conductor: usize,
    pub galois_automorphisms_checked: usize,
    pub preferred_embedding_imported: bool,
}

pub fn run_block_03_verification() -> Result<Block03VerificationReceipt, PositivityError> {
    let e = RealEmbeddings::new(120)?;
    let p5 = positivity_under_embeddings(&conductor_5_witness()?)?;
    let p8 = positivity_under_embeddings(&conductor_8_witness()?)?;
    let zeta = Cyclotomic::<120>::zeta(1);
    let amplitudes = [
        Cyclotomic::<120>::one().add(&zeta).scale(&rq(1, 2)),
        Cyclotomic::<120>::one().sub(&zeta).scale(&rq(1, 2)),
    ];
    let weights = born_weights(&amplitudes);
    let automorphisms = e
        .classes()
        .iter()
        .flat_map(|&k| [k as i64, -(k as i64)])
        .collect::<Vec<_>>();
    let mut covariance = weights[0].add(&weights[1]) == Cyclotomic::<120>::one();
    for &k in &automorphisms {
        let transformed_weights = weights
            .iter()
            .map(|p| p.galois(k))
            .collect::<Result<Vec<_>, _>>()?;
        covariance &= galois_born_weights(&amplitudes, k)? == transformed_weights;
    }
    Ok(Block03VerificationReceipt {
        real_embeddings_of_target_field: e.count(),
        embedding_relative_mixed_witness_conductor: 5,
        embedding_relative_witness_matrix: "diag(2*(zeta_5+zeta_5^-1)-1, 2-2*(zeta_5+zeta_5^-1))"
            .into(),
        conductor_5_positive_classes: p5
            .into_iter()
            .filter_map(|(k, positive)| positive.then_some(k))
            .collect(),
        conductor_8_positive_classes: p8
            .into_iter()
            .filter_map(|(k, positive)| positive.then_some(k))
            .collect(),
        galois_covariance_of_born_probabilities: covariance,
        galois_covariance_fixture_conductor: 120,
        galois_automorphisms_checked: automorphisms.len(),
        preferred_embedding_imported: true,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_full_block_03_verification() {
        let r = run_block_03_verification().unwrap();
        assert_eq!(r.real_embeddings_of_target_field, 16);
        assert_eq!(r.conductor_5_positive_classes, vec![1]);
        assert_eq!(r.conductor_8_positive_classes, vec![1]);
        assert!(r.galois_covariance_of_born_probabilities);
        assert_eq!(r.galois_covariance_fixture_conductor, 120);
        assert_eq!(r.galois_automorphisms_checked, 32);
    }
}
