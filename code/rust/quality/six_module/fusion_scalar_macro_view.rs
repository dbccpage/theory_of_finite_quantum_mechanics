// Explicit macro substitution view for calibrated AST metrics only. Not compiled.
impl FusionScalar for Cyc5 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                10
            }
            fn primitive_root_of_unity() -> Self {
                {
    let z = Cyc5::zeta5(3);
    Cyc5::zero().sub(&z)
}
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc8 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                8
            }
            fn primitive_root_of_unity() -> Self {
                Cyc8::zeta8(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc12 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                12
            }
            fn primitive_root_of_unity() -> Self {
                Cyc12::zeta12(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc24 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                24
            }
            fn primitive_root_of_unity() -> Self {
                Cyc24::zeta24(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc28 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                28
            }
            fn primitive_root_of_unity() -> Self {
                Cyc28::zeta(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc44 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                44
            }
            fn primitive_root_of_unity() -> Self {
                Cyc44::zeta(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc52 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                52
            }
            fn primitive_root_of_unity() -> Self {
                Cyc52::zeta(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
impl FusionScalar for Cyc120 {
            fn to_rational(&self) -> Option<Rational> {
                constant_term(&self.a)
            }
            fn root_of_unity_order() -> u32 {
                120
            }
            fn primitive_root_of_unity() -> Self {
                Cyc120::zeta(1)
            }
            fn real_sign(&self) -> Option<Ordering> {
                cyclotomic_sign(&CyclotomicNumber::from(self))
            }
        }
