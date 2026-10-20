#[cfg(test)]
mod boundary_review {
    use super::*;

    #[test]
    fn five_actual_providers_and_surface_compose() {
        assert_eq!(certify_partition(),Ok(5));assert_eq!(certify_factorial(),Ok(120));
        assert_eq!(certify_mub(),Ok(6));assert_eq!(certify_fano(),Ok(7));assert_eq!(certify_affine(),Ok(12));
        let got=surface_certificate().unwrap();
        assert_eq!((got.partition_four,got.factorial_five,got.mub_bases,got.fano_lines,got.affine_lines),(5,120,6,7,12));
        assert_eq!(got,finish_surface(5,120).unwrap());
    }

    #[test]
    fn exact_scalar_check_and_diagnostic_operands() {
        assert_eq!(refuse_partition_witness(5),Ok(()));
        for value in [0,1,4,6,119,120,u64::MAX] {
            assert_eq!(refuse_partition_witness(value),Err(SurfaceError {invariant:"p(4)=5",parameters:format!("witness={value}")}));
        }
    }

    #[test]
    fn finish_is_a_private_assembler_and_records_are_raw() {
        for (p,f) in [(0,0),(4,119),(u64::MAX,u64::MAX)] {
            let record=finish_surface(p,f).unwrap();
            assert_eq!((record.partition_four,record.factorial_five),(p,f));
            assert_eq!((record.mub_bases,record.fano_lines,record.affine_lines),(6,7,12));
        }
        let original=surface_certificate().unwrap();let mut copied=original.clone();copied.affine_lines=0;
        assert_eq!(original.affine_lines,12);assert_ne!(original,copied);
    }
}
