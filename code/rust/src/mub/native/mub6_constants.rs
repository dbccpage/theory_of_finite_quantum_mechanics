
use num_rational::BigRational;
use num_traits::ToPrimitive;
use tfqm_number_theory::rational::rq;

crate::fixture_set!(fixtures, "mub6_constants");

pub fn base_gap() -> BigRational {
    fixtures().rational("base_gap")
}

pub fn lipschitz_bound() -> BigRational {
    fixtures().rational("lipschitz_bound")
}

pub fn delta_certified() -> BigRational {
    fixtures().rational("delta_certified")
}

pub fn delta_crit() -> BigRational {
    base_gap() / lipschitz_bound()
}

pub fn certified_erosion() -> BigRational {
    lipschitz_bound() * delta_certified()
}

pub fn certified_margin() -> BigRational {
    base_gap() - certified_erosion()
}

pub fn circulation_gamma() -> BigRational {
    certified_margin() * rq(6, 1)
}

pub fn total_domain_volume() -> BigRational {
    fixtures().rational("total_domain_volume")
}

pub fn circulation_gamma_scaled(scale: i128) -> i128 {
    let gamma = circulation_gamma();
    let numer = gamma.numer().to_i128().expect("circulation gamma numerator fits i128");
    let denom = gamma.denom().to_i128().expect("circulation gamma denominator fits i128");
    (numer * scale).div_euclid(denom)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn derived_constants_match_the_recorded_values() {
        assert_eq!(delta_crit(), rq(37249, 850000));
        assert_eq!(certified_erosion(), rq(17, 1800));
        assert_eq!(certified_margin(), rq(12133, 30000));
        assert_eq!(circulation_gamma(), certified_margin() * rq(6, 1));
        assert_eq!(circulation_gamma(), rq(12133, 5000));
        assert_eq!(circulation_gamma_scaled(30000), 72798);
        assert_eq!(total_domain_volume(), rq(5001, 1000));
        assert!(delta_certified() < delta_crit());
    }
}
