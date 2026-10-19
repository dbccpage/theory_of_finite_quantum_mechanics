
#[cfg(test)]
mod tests {
    use super::*;
    fn q(n:i64,d:i64)->Q{Q::new(n.into(),d.into())}
    #[test]
    fn deterministic_and_non_grid_pair_mixtures_extend() {
        for i in 0..16 {for j in 0..16 {for fraction in [q(1,7),q(2,5)] {
            let mut law:[Q;16]=std::array::from_fn(|_|Q::zero());law[i]+=&fraction;law[j]+=Q::one()-fraction;
            let p=project_joint(&law).unwrap();let answer=construct_extension(&p).unwrap();verify_extension(&p,&answer.weights.unwrap()).unwrap();
        }}}
    }
    #[test]
    fn all_eight_PR_obstructions_include_nonstandard_facets() {
        for mask in FACET_MASKS {
            let p:PairData=std::array::from_fn(|j|if mask&(1<<j)==0 {[q(1,2),q(0,1),q(0,1),q(1,2)]} else {[q(0,1),q(1,2),q(1,2),q(0,1)]});
            let answer=construct_extension(&p).unwrap();assert!(answer.weights.is_none());assert_eq!(answer.violating_mask,Some(mask));
            let k=FACET_MASKS.iter().position(|m|*m==mask).unwrap();assert_eq!(answer.analysis.facets[k],q(4,1));
            if mask!=8 {assert!(answer.analysis.facets[4]<=q(2,1));}
        }
    }
    #[test]
    fn zero_separator_slices_and_nonunique_extensions() {
        let p:PairData=std::array::from_fn(|_|std::array::from_fn(|_|q(1,4)));
        let answer=construct_extension(&p).unwrap();assert_eq!(answer.separator,Some(Q::zero()));
        let weights=answer.weights.unwrap();assert!(weights.iter().any(Zero::is_zero));verify_extension(&p,&weights).unwrap();
        assert_ne!(weights,std::array::from_fn(|_|q(1,16)));
    }
    #[test]
    fn mismatched_separators_and_wrong_projection_are_refused() {
        let mut left:[Q;8]=std::array::from_fn(|_|Q::zero());let mut right=left.clone();left[0]=Q::one();right[1]=Q::one();
        assert_eq!(conditional_glue(&left,&right),Err(ExtensionError::SeparatorMismatch));
        let p:PairData=std::array::from_fn(|_|std::array::from_fn(|_|q(1,4)));
        let mut bad:[Q;16]=std::array::from_fn(|_|Q::zero());bad[0]=Q::one();
        assert_eq!(verify_extension(&p,&bad),Err(ExtensionError::ProjectionMismatch));
    }
    #[test]
    fn invalid_raw_rationals_and_incompatible_marginals_are_refused() {
        let p:PairData=std::array::from_fn(|_|std::array::from_fn(|_|q(1,4)));
        for raw in [Q::new_raw(1.into(),0.into()),Q::new_raw(2.into(),2.into()),Q::new_raw((-1).into(),(-1).into())] {
            let mut bad=p.clone();bad[0][0]=raw;assert_eq!(validate_pairs(&bad),Err(ExtensionError::InvalidLaw));
        }
        for row in [[q(1,2),q(1,2),q(0,1),q(0,1)],[q(1,2),q(0,1),q(1,2),q(0,1)]] {
            let mut bad=p.clone();bad[0]=row;assert_eq!(validate_pairs(&bad),Err(ExtensionError::IncompatibleMarginals));
        }
    }
    #[test]
    fn arbitrary_precision_and_separator_guard() {
        let d=num_bigint::BigInt::from(10u32).pow(100)+num_bigint::BigInt::from(3);
        let mut law:[Q;16]=std::array::from_fn(|_|Q::zero());law[15]=Q::new(1.into(),d);law[0]=Q::one()-&law[15];
        let p=project_joint(&law).unwrap();let answer=construct_extension(&p).unwrap();verify_extension(&p,&answer.weights.unwrap()).unwrap();
        let uniform:PairData=std::array::from_fn(|_|std::array::from_fn(|_|q(1,4)));
        assert_eq!(split_triple(&uniform,0,&q(3,4)),Err(ExtensionError::InvalidSeparator));
        assert_eq!(split_triple(&uniform,2,&q(1,4)),Err(ExtensionError::InvalidSeparator));
    }
}
