
pub const OPEN_RESIDUAL_GENERAL_N: &str =
    "OPEN residual: general-n exact Hermitian spectral algorithm \
    (non-diagonal, n > 2) is unpaid; only diagonal (any finite n) and 2×2 charpoly-split \
    cases are implemented. AuthorityEffect None; no continuum claim.";
pub const SPECTRAL_OBSTRUCTION_IS_ALGEBRAIC_NOT_DIMENSIONAL: &str =
    "OB-SPECTRAL obstruction is ALGEBRAIC, not dimensional: a rational Hermitian \
     matrix may have irrational eigenvalues, so exact spectral decomposition over \
     the rationals fails already at n = 2. Paying OB-SPECTRAL means admitting an \
     algebraic extension as the scalar carrier. AuthorityEffect None.";
pub const SPECTRAL_OBSTRUCTION_SCOPE: &str =
    "OB-SPECTRAL at general n, SCOPED (narrowed 2026-08-05 under review of PR      #1894): the family is CONSTRUCTED for arbitrary n >= 2 and EXECUTED for      2 <= n <= 8. Within the executed range, the block-diagonal matrix with      leading block [[1,1],[1,0]] (charpoly x^2 - x - 1, discriminant 5, not a      perfect square) has NO exact rational spectral decomposition THROUGH THE      DECLARED BLOCK PATH, while the same construction with leading block      [[0,1],[1,0]] (discriminant 4, a perfect square) DOES decompose at the      same n through the same code path. The decisive property is the SQUARE      CLASS of the discriminant, not the dimension and not the shape. NOT      ESTABLISHED: that no rational spectral decomposition of the family exists      AT ALL for arbitrary n. That needs a proof that any rational spectral      decomposition of the block-diagonal family restricts to the nonsplitting      2x2 block; no such proof is mechanized here, and n > 8 is not executed.      Do not quote this as a universal theorem. AuthorityEffect None.";
pub const AXIOM_A17_OBSERVABLES: &str =
    "A17 (observables): a classical observable on the declared finite carrier is a \
     function sector -> Q; spectral decomposition is level-set indicator arithmetic; \
     the classical observable algebra is commutative by construction. \
     Non-commutativity is NOT derived from the carrier - it is the declared import \
     OB-NONCOMM. AuthorityEffect None.";

#[cfg(test)]
mod tests {
    use super::*;
    use omega_quantum_physics::hermitian_spectral::leading_block_structure;
    fn squish(text: &str) -> String {
        text.split_whitespace().collect::<Vec<_>>().join(" ")
    }
    #[test]
    fn general_n_scope_is_recorded_with_its_executed_range() {
        let scope = squish(SPECTRAL_OBSTRUCTION_SCOPE);
        assert!(scope.contains("CONSTRUCTED for arbitrary n >= 2"));
        assert!(scope.contains("EXECUTED for 2 <= n <= 8"));
        assert!(scope.contains("NOT ESTABLISHED"));
        assert!(scope.contains("SQUARE CLASS"));
        assert!(scope.contains("AuthorityEffect None"));
        assert!(scope.contains("Do not quote this as a universal theorem"));
        for n in 2..=8 {
            assert!(
                leading_block_structure(n).is_ok(),
                "n={n} is claimed executed"
            );
        }
    }
}
