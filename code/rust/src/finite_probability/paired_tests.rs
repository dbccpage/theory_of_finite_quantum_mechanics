
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

fn default_authority_effect() -> String {
    "None".to_string()
}

pub fn binom(n: u64, k: u64) -> BigInt {
    if k > n {
        return BigInt::zero();
    }
    if k == 0 || k == n {
        return BigInt::one();
    }
    let k = k.min(n - k);
    let mut c = BigInt::one();
    for i in 1..=k {
        c = (c * BigInt::from(n - i + 1)) / BigInt::from(i);
    }
    c
}

pub fn mcnemar_exact(b: u64, c: u64) -> BigRational {
    let n = b + c;
    if n == 0 {
        return BigRational::one();
    }
    let min_bc = b.min(c);
    let mut sum = BigInt::zero();
    for i in 0..=min_bc {
        sum += binom(n, i);
    }

    let two_sided_sum = BigInt::from(2) * sum;
    let denom = BigInt::from(2).pow(n as u32);

    let p = BigRational::new(two_sided_sum, denom);
    if p > BigRational::one() {
        BigRational::one()
    } else {
        p
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct McNemarReportV1 {
    pub b: u64,
    pub c: u64,
    pub discordant_total: u64,
    pub p_value_exact: String,
    pub p_value_num: String,
    pub p_value_denom: String,
    #[serde(default = "default_authority_effect")]
    pub authority_effect: String,
}

pub fn evaluate_mcnemar(b: u64, c: u64) -> McNemarReportV1 {
    let p = mcnemar_exact(b, c);
    McNemarReportV1 {
        b,
        c,
        discordant_total: b + c,
        p_value_exact: format!("{}/{}", p.numer(), p.denom()),
        p_value_num: p.numer().to_string(),
        p_value_denom: p.denom().to_string(),
        authority_effect: default_authority_effect(),
    }
}
