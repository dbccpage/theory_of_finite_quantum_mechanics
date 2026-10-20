#[cfg(test)]
mod boundary_review {
    use super::*;

    #[test]
    fn complete_surface_matches_independent_small_witnesses() {
        let cert=e2e_surface().unwrap();
        let expected_partitions=[vec![4],vec![3,1],vec![2,2],vec![2,1,1],vec![1,1,1,1]];
        assert_eq!(cert.partition_four,expected_partitions.len() as u64);
        assert_eq!(cert.factorial_five,(1..=5u64).product());
        assert_eq!(cert.mub_bases,5+1);assert_eq!(cert.fano_lines,(7*6)/(3*2));
        assert_eq!(cert.affine_lines,(3*3*(3*3-1))/(3*(3-1)));
        assert_eq!(cert,surface_certificate().unwrap());
    }

    #[test]
    fn public_records_are_mutable_reports_not_admission_tokens() {
        let original=e2e_surface().unwrap();let mut forged=original.clone();
        forged.partition_four=0;forged.factorial_five=u64::MAX;forged.mub_bases=usize::MAX;
        assert_ne!(forged,original);assert_eq!(e2e_surface().unwrap(),original);
        let error=SurfaceError {invariant:"caller-provided",parameters:"raw".to_owned()};
        assert_eq!(error.clone(),error);
    }

    #[test]
    fn exported_partition_check_has_exact_boundary() {
        assert_eq!(crate_certificate::refuse_partition_witness(5),Ok(()));
        for value in [0,1,4,6,120,u64::MAX] {
            let error=crate_certificate::refuse_partition_witness(value).unwrap_err();
            assert_eq!(error.invariant,"p(4)=5");assert_eq!(error.parameters,format!("witness={value}"));
        }
    }
}
