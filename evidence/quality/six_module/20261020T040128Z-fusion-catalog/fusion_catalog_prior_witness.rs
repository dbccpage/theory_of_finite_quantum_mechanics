#[cfg(test)]
mod catalog_review {
    use super::*;
    use omega_number_theory::rational::Rational;
    #[test]
    fn rational_phase_requires_no_extra_root_field() {
        let result=cyclic_pointed::<Rational>(3,3);
        assert!(result.is_ok(),"exp(2*pi*i*3*x*y/3) is always one; result: {result:?}");
    }
}
