
pub const DEFAULT_CM_TOL: f64 = 1e-9;

pub fn small_matrix_det(mut mat: Vec<Vec<f64>>) -> f64 {
    let n = mat.len();
    if n == 0 {
        return 1.0;
    }
    for row in &mat {
        if row.len() != n {
            return 0.0;
        }
    }

    let mut det = 1.0;
    for col in 0..n {
        let mut pivot_row = col;
        let mut max_val = mat[col][col].abs();
        for r in (col + 1)..n {
            if mat[r][col].abs() > max_val {
                max_val = mat[r][col].abs();
                pivot_row = r;
            }
        }

        if max_val < 1e-15 {
            return 0.0;
        }

        if pivot_row != col {
            mat.swap(pivot_row, col);
            det = -det;
        }

        let pivot = mat[col][col];
        det *= pivot;

        for r in (col + 1)..n {
            let factor = mat[r][col] / pivot;
            for c in col..n {
                mat[r][c] -= factor * mat[col][c];
            }
        }
    }

    det
}

pub fn matrix_cofactor(mat: &[Vec<f64>], row: usize, col: usize) -> f64 {
    let n = mat.len();
    if n <= 1 {
        return 1.0;
    }
    let mut sub = Vec::with_capacity(n - 1);
    for (r, r_vec) in mat.iter().enumerate() {
        if r == row {
            continue;
        }
        let mut row_sub = Vec::with_capacity(n - 1);
        for (c, &val) in r_vec.iter().enumerate() {
            if c == col {
                continue;
            }
            row_sub.push(val);
        }
        sub.push(row_sub);
    }
    let det = small_matrix_det(sub);
    if (row + col) % 2 == 1 {
        -det
    } else {
        det
    }
}

pub fn cayley_menger_matrix(
    vertices: &[usize],
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<Vec<Vec<f64>>, String> {
    let k = vertices.len();
    if k == 0 {
        return Err("Cannot construct Cayley-Menger matrix for empty vertex set".to_string());
    }

    let m = k + 1;
    let mut mat = vec![vec![0.0; m]; m];

    for i in 1..m {
        mat[0][i] = 1.0;
        mat[i][0] = 1.0;
    }

    for i in 0..k {
        for j in 0..k {
            if i != j {
                let u = vertices[i];
                let v = vertices[j];
                let len = get_length(u, v)
                    .ok_or_else(|| format!("Missing edge length between vertices {u} and {v}"))?;
                if len <= 0.0 || !len.is_finite() {
                    return Err(format!(
                        "Invalid non-positive edge length {len} between {u} and {v}"
                    ));
                }
                mat[i + 1][j + 1] = len * len;
            }
        }
    }

    Ok(mat)
}

pub fn cayley_menger_determinant(
    vertices: &[usize],
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<f64, String> {
    let mat = cayley_menger_matrix(vertices, get_length)?;
    Ok(small_matrix_det(mat))
}

pub fn simplex_volume_cayley_menger(
    vertices: &[usize],
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<f64, String> {
    let n = vertices.len().saturating_sub(1);
    if n == 0 {
        return Ok(1.0);
    }
    if n == 1 {
        let u = vertices[0];
        let v = vertices[1];
        let len = get_length(u, v).ok_or_else(|| format!("Missing edge length ({u}, {v})"))?;
        return Ok(len);
    }

    let det = cayley_menger_determinant(vertices, get_length)?;

    let mut factorial = 1.0;
    for i in 1..=n {
        factorial *= i as f64;
    }
    let denom = (2.0f64.powi(n as i32)) * (factorial * factorial);
    let sign = if (n + 1) % 2 == 1 { -1.0 } else { 1.0 };

    let vol_sq = (sign * det) / denom;
    if vol_sq < -DEFAULT_CM_TOL {
        return Err(format!(
            "Simplex on vertices {vertices:?} violates metric embedding (negative Cayley-Menger vol^2 = {vol_sq})"
        ));
    }
    Ok(vol_sq.max(0.0).sqrt())
}

#[derive(Debug, Clone, PartialEq)]
pub struct MetricPolytopeCheck {
    pub is_admissible: bool,
    pub triangle_inequality_violations: Vec<([usize; 3], String)>,
    pub cayley_menger_violations: Vec<(Vec<usize>, f64)>,
}

impl MetricPolytopeCheck {
    pub fn new() -> Self {
        Self {
            is_admissible: true,
            triangle_inequality_violations: Vec::new(),
            cayley_menger_violations: Vec::new(),
        }
    }
}

impl Default for MetricPolytopeCheck {
    fn default() -> Self {
        Self::new()
    }
}

pub fn check_metric_polytope_admissibility(
    triangles: &[[usize; 3]],
    tetrahedra: &[[usize; 4]],
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> MetricPolytopeCheck {
    let mut check = MetricPolytopeCheck::new();

    for &tri in triangles {
        let a = match get_length(tri[1], tri[2]) {
            Some(v) => v,
            None => continue,
        };
        let b = match get_length(tri[0], tri[2]) {
            Some(v) => v,
            None => continue,
        };
        let c = match get_length(tri[0], tri[1]) {
            Some(v) => v,
            None => continue,
        };

        if a + b <= c + DEFAULT_CM_TOL || a + c <= b + DEFAULT_CM_TOL || b + c <= a + DEFAULT_CM_TOL
        {
            check.triangle_inequality_violations.push((
                tri,
                format!("Lengths ({a}, {b}, {c}) violate triangle inequality"),
            ));
            check.is_admissible = false;
        }
    }

    for &tet in tetrahedra {
        match simplex_volume_cayley_menger(&tet, &get_length) {
            Ok(vol) if vol > DEFAULT_CM_TOL => {}
            Ok(vol) => {
                check.cayley_menger_violations.push((tet.to_vec(), vol));
                check.is_admissible = false;
            }
            Err(_) => {
                check.cayley_menger_violations.push((tet.to_vec(), -1.0));
                check.is_admissible = false;
            }
        }
    }

    check
}

pub fn simplex_volume_derivative_wrt_squared_edge(
    vertices: &[usize],
    u: usize,
    v: usize,
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<f64, String> {
    let n = vertices.len().saturating_sub(1);
    if n < 1 {
        return Err("Simplex must have dimension at least 1 to compute edge derivative".to_string());
    }

    let i = vertices
        .iter()
        .position(|&x| x == u)
        .ok_or_else(|| format!("Vertex {u} not found in simplex {vertices:?}"))?;
    let j = vertices
        .iter()
        .position(|&x| x == v)
        .ok_or_else(|| format!("Vertex {v} not found in simplex {vertices:?}"))?;

    if i == j {
        return Err(format!("Vertices u={u} and v={v} must be distinct"));
    }

    let vol = simplex_volume_cayley_menger(vertices, &get_length)?;
    if vol <= DEFAULT_CM_TOL {
        return Err(format!("Simplex has degenerate/non-positive volume {vol}"));
    }

    let mat = cayley_menger_matrix(vertices, &get_length)?;
    let cof = matrix_cofactor(&mat, i + 1, j + 1);

    let mut factorial = 1.0;
    for k in 1..=n {
        factorial *= k as f64;
    }
    let denom = (2.0f64.powi(n as i32)) * (factorial * factorial) * vol;
    let sign = if (n + 1) % 2 == 1 { -1.0 } else { 1.0 };

    Ok((sign * cof) / denom)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeMap;

    #[test]
    fn test_equilateral_triangle_cayley_menger() {
        let side = 2.0;
        let get_len = |_: usize, _: usize| Some(side);
        let vol = simplex_volume_cayley_menger(&[0, 1, 2], get_len).unwrap();
        let expected = (3.0f64.sqrt() / 4.0) * side * side;
        assert!((vol - expected).abs() < 1e-9);
    }

    #[test]
    fn test_regular_tetrahedron_cayley_menger() {
        let side = 1.0;
        let get_len = |_: usize, _: usize| Some(side);
        let vol = simplex_volume_cayley_menger(&[0, 1, 2, 3], get_len).unwrap();
        let expected = side.powi(3) / (6.0 * 2.0f64.sqrt());
        assert!((vol - expected).abs() < 1e-9);
    }

    #[test]
    fn test_triangle_inequality_rejection() {
        let triangles = [[0, 1, 2]];
        let tetrahedra = [];
        let mut map = BTreeMap::new();
        map.insert((0, 1), 1.0);
        map.insert((1, 2), 2.0);
        map.insert((0, 2), 10.0);
        let get_len = |u: usize, v: usize| {
            let key = if u < v { (u, v) } else { (v, u) };
            map.get(&key).copied()
        };

        let check = check_metric_polytope_admissibility(&triangles, &tetrahedra, get_len);
        assert!(!check.is_admissible);
        assert_eq!(check.triangle_inequality_violations.len(), 1);
    }

    #[test]
    fn test_simplex_volume_derivative_wrt_squared_edge() {
        let get_len = |u: usize, v: usize| {
            let key = if u < v { (u, v) } else { (v, u) };
            match key {
                (0, 1) => Some(3.0),
                (1, 2) => Some(4.0),
                (0, 2) => Some(5.0),
                _ => None,
            }
        };

        let d_anal = simplex_volume_derivative_wrt_squared_edge(&[0, 1, 2], 0, 1, get_len).unwrap();
        assert!((d_anal - 1.0 / 3.0).abs() < 1e-7);

        let eps = 1e-6;
        let s0 = 3.0f64 * 3.0;
        let l_plus = (s0 + eps).sqrt();
        let l_minus = (s0 - eps).sqrt();

        let get_len_plus = |u: usize, v: usize| {
            let key = if u < v { (u, v) } else { (v, u) };
            if key == (0, 1) {
                Some(l_plus)
            } else {
                get_len(u, v)
            }
        };
        let get_len_minus = |u: usize, v: usize| {
            let key = if u < v { (u, v) } else { (v, u) };
            if key == (0, 1) {
                Some(l_minus)
            } else {
                get_len(u, v)
            }
        };

        let a_plus = simplex_volume_cayley_menger(&[0, 1, 2], get_len_plus).unwrap();
        let a_minus = simplex_volume_cayley_menger(&[0, 1, 2], get_len_minus).unwrap();
        let d_num = (a_plus - a_minus) / (2.0 * eps);

        assert!((d_anal - d_num).abs() < 1e-6);
    }
}
