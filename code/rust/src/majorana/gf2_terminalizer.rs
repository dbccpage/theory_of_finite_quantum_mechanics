
use serde::{Deserialize, Serialize};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; not physical Majorana; GF(2) diagnostic only.";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum GF2ScheduleStatus {
    Exact,
    ClosedResidual,
    OpenObstruction,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct GF2Matrix {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<Vec<u8>>,
}

impl GF2Matrix {
    pub fn zeros(rows: usize, cols: usize) -> Self {
        Self {
            rows,
            cols,
            data: vec![vec![0; cols]; rows],
        }
    }

    pub fn from_data(data: Vec<Vec<u8>>) -> Self {
        let rows = data.len();
        let cols = data.iter().map(Vec::len).max().unwrap_or(0);
        let mut normalized = Vec::with_capacity(rows);
        for row in data {
            let mut out = vec![0u8; cols];
            for (col, val) in row.into_iter().enumerate() {
                out[col] = val % 2;
            }
            normalized.push(out);
        }
        Self {
            rows,
            cols,
            data: normalized,
        }
    }

    pub fn matmul(&self, rhs: &GF2Matrix) -> Result<GF2Matrix, String> {
        if self.cols != rhs.rows {
            return Err(format!(
                "Shape mismatch for GF(2) matmul: ({}, {}) x ({}, {})",
                self.rows, self.cols, rhs.rows, rhs.cols
            ));
        }
        let mut result = GF2Matrix::zeros(self.rows, rhs.cols);
        for i in 0..self.rows {
            for j in 0..rhs.cols {
                let mut sum = 0u8;
                for k in 0..self.cols {
                    sum ^= self.data[i][k] & rhs.data[k][j];
                }
                result.data[i][j] = sum & 1;
            }
        }
        Ok(result)
    }

    pub fn is_zero(&self) -> bool {
        self.data.iter().all(|row| row.iter().all(|&v| v == 0))
    }

    fn find_pivot_row(&self, start_row: usize, col: usize) -> Option<usize> {
        for r in start_row..self.rows {
            if self.data[r][col] == 1 {
                return Some(r);
            }
        }
        None
    }

    fn xor_row(&mut self, target: usize, source: usize) {
        for c in 0..self.cols {
            self.data[target][c] ^= self.data[source][c];
        }
    }

    fn eliminate_column(&mut self, pivot_row: usize, col: usize) {
        for r in 0..self.rows {
            if r != pivot_row && self.data[r][col] == 1 {
                self.xor_row(r, pivot_row);
            }
        }
    }

    pub fn rref(&self) -> (usize, GF2Matrix) {
        let mut mat = self.clone();
        let mut rank = 0;
        let mut col = 0;

        while rank < mat.rows && col < mat.cols {
            if let Some(p_row) = mat.find_pivot_row(rank, col) {
                mat.data.swap(rank, p_row);
                mat.eliminate_column(rank, col);
                rank += 1;
            }
            col += 1;
        }
        (rank, mat)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Gf2ScheduleReceipt {
    pub certificate_tag: String,
    pub status: GF2ScheduleStatus,
    pub d0_rank: usize,
    pub d1_rank: usize,
    pub q1_dimension: usize,
    pub boundary_valid: bool,
    pub authority_effect: String,
}

pub struct Gf2CocycleClassifier;

impl Gf2CocycleClassifier {
    pub fn verify_boundary(d0: &GF2Matrix, d1: &GF2Matrix) -> bool {
        match d1.matmul(d0) {
            Ok(prod) => prod.is_zero(),
            Err(_) => false,
        }
    }

    pub fn classify(
        d0: &GF2Matrix,
        d1: &GF2Matrix,
        syndrome: &[u8],
    ) -> Result<Gf2ScheduleReceipt, String> {
        if syndrome.len() != d0.rows {
            return Err(format!(
                "Syndrome dimension {} does not match d0 rows {}",
                syndrome.len(),
                d0.rows
            ));
        }

        let boundary_valid = Self::verify_boundary(d0, d1);
        if !boundary_valid {
            return Err("Boundary operator validation failed: d1 * d0 != 0 mod 2".into());
        }

        let (rank_d0, _) = d0.rref();
        let (rank_d1, _) = d1.rref();

        let mut d1_syndrome = vec![0u8; d1.rows];
        for i in 0..d1.rows {
            let mut sum = 0u8;
            for j in 0..d1.cols {
                sum ^= d1.data[i][j] & (syndrome[j] % 2);
            }
            d1_syndrome[i] = sum & 1;
        }

        let is_closed = d1_syndrome.iter().all(|&v| v == 0);

        let mut augmented = vec![vec![0u8; d0.cols + 1]; d0.rows];
        for r in 0..d0.rows {
            for c in 0..d0.cols {
                augmented[r][c] = d0.data[r][c];
            }
            augmented[r][d0.cols] = syndrome[r] % 2;
        }
        let aug_mat = GF2Matrix::from_data(augmented);
        let (aug_rank, _) = aug_mat.rref();

        let status = if aug_rank == rank_d0 {
            GF2ScheduleStatus::Exact
        } else if is_closed {
            GF2ScheduleStatus::ClosedResidual
        } else {
            GF2ScheduleStatus::OpenObstruction
        };

        let ker_d1 = d1.cols.saturating_sub(rank_d1);
        let q1_dim = ker_d1.saturating_sub(rank_d0);

        Ok(Gf2ScheduleReceipt {
            certificate_tag: "omega.majorana-gf2-receipt.v1".into(),
            status,
            d0_rank: rank_d0,
            d1_rank: rank_d1,
            q1_dimension: q1_dim,
            boundary_valid,
            authority_effect: "None".into(),
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cyclotomic16Element {
    pub coeffs: [i64; 8],
}

impl Cyclotomic16Element {
    pub fn zero() -> Self {
        Self { coeffs: [0; 8] }
    }

    pub fn one() -> Self {
        let mut c = [0; 8];
        c[0] = 1;
        Self { coeffs: c }
    }

    pub fn from_scalar(val: i64) -> Self {
        let mut c = [0; 8];
        c[0] = val;
        Self { coeffs: c }
    }

    pub fn checked_mul(&self, rhs: &Self) -> Option<Self> {
        let mut raw = [0i64; 16];
        for i in 0..8 {
            for j in 0..8 {
                raw[i + j] = raw[i + j].checked_add(self.coeffs[i].checked_mul(rhs.coeffs[j])?)?;
            }
        }
        let mut res = [0i64; 8];
        for k in 0..8 {
            res[k] = raw[k].checked_sub(raw[k + 8])?;
        }
        Some(Self { coeffs: res })
    }

    pub fn zeta() -> Self {
        let mut c = [0; 8];
        c[1] = 1;
        Self { coeffs: c }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gf2_matrix_boundary_and_terminalization() {
        let d0_data = vec![
            vec![1, 1, 0],
            vec![0, 1, 1],
            vec![1, 0, 1],
        ];
        let d0 = GF2Matrix::from_data(d0_data);

        let d1_data = vec![
            vec![1, 1, 1],
        ];
        let d1 = GF2Matrix::from_data(d1_data);

        assert!(Gf2CocycleClassifier::verify_boundary(&d0, &d1));

        let exact_syndrome = vec![1, 1, 0];
        let cert_exact = Gf2CocycleClassifier::classify(&d0, &d1, &exact_syndrome).unwrap();
        assert_eq!(cert_exact.status, GF2ScheduleStatus::Exact);
        assert_eq!(cert_exact.certificate_tag, "omega.majorana-gf2-receipt.v1");

        let open_syndrome = vec![1, 0, 0];
        let cert_open = Gf2CocycleClassifier::classify(&d0, &d1, &open_syndrome).unwrap();
        assert_eq!(cert_open.status, GF2ScheduleStatus::OpenObstruction);
    }

    #[test]
    fn ragged_rows_are_rectangular_and_do_not_panic() {
        let matrix = GF2Matrix::from_data(vec![vec![1], vec![1, 1, 3]]);
        assert_eq!(matrix.rows, 2);
        assert_eq!(matrix.cols, 3);
        assert_eq!(matrix.data[0], vec![1, 0, 0]);
        assert_eq!(matrix.data[1], vec![1, 1, 1]);
        let (rank, _) = matrix.rref();
        assert_eq!(rank, 2);
        let wide = GF2Matrix::from_data(vec![vec![1, 0], vec![1]]);
        let product = wide.matmul(&GF2Matrix::zeros(2, 1)).unwrap();
        assert_eq!(product.data, vec![vec![0], vec![0]]);
    }

    #[test]
    fn test_cyclotomic16_arithmetic() {
        let one = Cyclotomic16Element::one();
        let prod = one.checked_mul(&one).unwrap();
        assert_eq!(prod, one);

        let mut zeta4 = Cyclotomic16Element::zero();
        zeta4.coeffs[4] = 1;
        let zeta8 = zeta4.checked_mul(&zeta4).unwrap();
        assert_eq!(zeta8.coeffs[0], -1);
    }

    #[test]
    fn zeta_has_order_sixteen() {
        let zeta = Cyclotomic16Element::zeta();
        let mut power = Cyclotomic16Element::one();
        let mut order = None;
        for k in 1..=16 {
            power = power.checked_mul(&zeta).unwrap();
            if power == Cyclotomic16Element::one() {
                order = Some(k);
                break;
            }
        }
        assert_eq!(order, Some(16));
    }

    #[test]
    fn coefficient_overflow_is_refused() {
        let big = Cyclotomic16Element::from_scalar(i64::MAX / 2 + 1);
        assert_eq!(big.checked_mul(&Cyclotomic16Element::from_scalar(2)), None);
        assert_eq!(
            Cyclotomic16Element::from_scalar(3).checked_mul(&Cyclotomic16Element::from_scalar(-4)),
            Some(Cyclotomic16Element::from_scalar(-12))
        );
    }
}
