

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct FieldElement {
    pub coeffs: Vec<usize>,
}

impl FieldElement {
    pub fn is_zero(&self) -> bool {
        self.coeffs.iter().all(|coeff| *coeff == 0)
    }
}

#[derive(Debug, Clone)]
pub struct FiniteField {
    prime: usize,
    degree: usize,
    modulus_lower: Vec<usize>,
    elements: Vec<FieldElement>,
}

impl FiniteField {
    pub fn new(prime: usize, degree: usize, modulus_lower: Vec<usize>) -> Self {
        let elements = enumerate_elements(prime, degree);
        Self {
            prime,
            degree,
            modulus_lower,
            elements,
        }
    }

    pub fn with_first_irreducible(prime: usize, degree: usize) -> Option<Self> {
        if !is_prime(prime) || degree == 0 {
            return None;
        }
        checked_pow(prime, degree)?;
        let modulus_lower = find_irreducible_monic(prime, degree)?;
        Some(Self::new(prime, degree, modulus_lower))
    }

    pub fn prime_field(prime: usize) -> Option<Self> {
        Self::with_first_irreducible(prime, 1)
    }

    pub fn prime(&self) -> usize {
        self.prime
    }

    pub fn degree(&self) -> usize {
        self.degree
    }

    pub fn modulus_lower(&self) -> &[usize] {
        &self.modulus_lower
    }

    pub fn elements(&self) -> &[FieldElement] {
        &self.elements
    }

    pub fn order(&self) -> usize {
        self.elements.len()
    }

    pub fn zero(&self) -> FieldElement {
        FieldElement {
            coeffs: vec![0; self.degree],
        }
    }

    pub fn one(&self) -> FieldElement {
        self.base(1)
    }

    pub fn base(&self, value: usize) -> FieldElement {
        let mut coeffs = vec![0; self.degree];
        coeffs[0] = value % self.prime;
        FieldElement { coeffs }
    }

    pub fn add(&self, left: &FieldElement, right: &FieldElement) -> FieldElement {
        let coeffs = left
            .coeffs
            .iter()
            .zip(&right.coeffs)
            .map(|(a, b)| (a + b) % self.prime)
            .collect();
        FieldElement { coeffs }
    }

    pub fn sub(&self, left: &FieldElement, right: &FieldElement) -> FieldElement {
        let coeffs = left
            .coeffs
            .iter()
            .zip(&right.coeffs)
            .map(|(a, b)| (self.prime + a - b) % self.prime)
            .collect();
        FieldElement { coeffs }
    }

    pub fn mul(&self, left: &FieldElement, right: &FieldElement) -> FieldElement {
        let mut product = vec![0; 2 * self.degree - 1];
        for (i, a) in left.coeffs.iter().enumerate() {
            for (j, b) in right.coeffs.iter().enumerate() {
                product[i + j] = (product[i + j] + a * b) % self.prime;
            }
        }

        for degree in (self.degree..product.len()).rev() {
            let coeff = product[degree] % self.prime;
            if coeff == 0 {
                continue;
            }
            for lower_degree in 0..self.degree {
                let reduction = coeff * self.modulus_lower[lower_degree] % self.prime;
                let target = degree - self.degree + lower_degree;
                product[target] = (self.prime + product[target] - reduction) % self.prime;
            }
        }

        FieldElement {
            coeffs: product[..self.degree].to_vec(),
        }
    }

    pub fn pow(&self, base: &FieldElement, mut exponent: usize) -> FieldElement {
        let mut acc = self.base(1);
        let mut power = base.clone();
        while exponent > 0 {
            if exponent % 2 == 1 {
                acc = self.mul(&acc, &power);
            }
            exponent /= 2;
            if exponent > 0 {
                power = self.mul(&power, &power);
            }
        }
        acc
    }

    pub fn trace_value(&self, element: &FieldElement) -> Result<usize, String> {
        let mut sum = self.zero();
        let mut conjugate = element.clone();
        for _ in 0..self.degree {
            sum = self.add(&sum, &conjugate);
            conjugate = self.pow(&conjugate, self.prime);
        }
        if sum.coeffs.iter().skip(1).any(|coeff| *coeff != 0) {
            return Err(format!(
                "trace did not land in the base field for {:?}",
                element.coeffs
            ));
        }
        Ok(sum.coeffs[0])
    }
}

pub fn find_irreducible_monic(prime: usize, degree: usize) -> Option<Vec<usize>> {
    if !is_prime(prime) || degree == 0 {
        return None;
    }
    for mut index in 0..checked_pow(prime, degree)? {
        let mut lower = vec![0; degree];
        for coeff in &mut lower {
            *coeff = index % prime;
            index /= prime;
        }
        if lower[0] == 0 {
            continue;
        }
        if is_irreducible_monic(prime, &lower) {
            return Some(lower);
        }
    }
    None
}

pub fn is_irreducible_monic(prime: usize, lower: &[usize]) -> bool {
    let degree = lower.len();
    if !is_prime(prime) || degree == 0 || lower.iter().any(|&coeff| coeff >= prime) {
        return false;
    }
    if degree > 1 && lower[0] == 0 {
        return false;
    }
    let mut polynomial = lower.to_vec();
    polynomial.push(1);

    for divisor_degree in 1..=degree / 2 {
        let Some(divisor_count) = checked_pow(prime, divisor_degree) else {
            return false;
        };
        for mut index in 0..divisor_count {
            let mut divisor = vec![0; divisor_degree + 1];
            for coeff in divisor.iter_mut().take(divisor_degree) {
                *coeff = index % prime;
                index /= prime;
            }
            divisor[divisor_degree] = 1;
            if divisor[0] == 0 {
                continue;
            }
            if poly_mod(prime, &polynomial, &divisor)
                .iter()
                .all(|coeff| *coeff == 0)
            {
                return false;
            }
        }
    }

    true
}

fn poly_mod(prime: usize, polynomial: &[usize], divisor: &[usize]) -> Vec<usize> {
    let mut rem = polynomial.to_vec();
    let divisor_degree = divisor.len() - 1;
    debug_assert_eq!(divisor[divisor_degree], 1);

    while rem.len() >= divisor.len() {
        let coeff = *rem.last().expect("remainder has a leading term") % prime;
        if coeff != 0 {
            let offset = rem.len() - divisor.len();
            for (i, divisor_coeff) in divisor.iter().enumerate().take(divisor_degree) {
                let reduction = coeff * divisor_coeff % prime;
                rem[offset + i] = (prime + rem[offset + i] - reduction) % prime;
            }
        }
        rem.pop();
    }

    rem
}

fn enumerate_elements(prime: usize, degree: usize) -> Vec<FieldElement> {
    let order = checked_pow(prime, degree).expect("finite-field sample dimensions fit in usize");
    let mut elements = Vec::with_capacity(order);
    for mut index in 0..order {
        let mut coeffs = vec![0; degree];
        for coeff in &mut coeffs {
            *coeff = index % prime;
            index /= prime;
        }
        elements.push(FieldElement { coeffs });
    }
    elements
}

pub fn checked_pow(base: usize, exponent: usize) -> Option<usize> {
    let mut acc = 1usize;
    for _ in 0..exponent {
        acc = acc.checked_mul(base)?;
    }
    Some(acc)
}

pub fn is_prime(n: usize) -> bool {
    if n < 2 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    let mut d = 3;
    while d <= n / d {
        if n % d == 0 {
            return false;
        }
        d += 2;
    }
    true
}
