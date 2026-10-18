
pub fn q4_saving_milli(hits: i64) -> i64 {
    hits * 1000 - 10_000 * 1 - 2000
}

pub fn q4_strict_benefit(hits: i64) -> bool {
    q4_saving_milli(hits) > 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn q4_worked_example_requires_at_least_thirteen_hits_for_strict_benefit() {
        for h in 0..=12 {
            assert!(!q4_strict_benefit(h));
        }
        assert_eq!(q4_saving_milli(12), 0);
        assert_eq!(q4_saving_milli(13), 1000);
        assert!(q4_strict_benefit(13));
    }
}
