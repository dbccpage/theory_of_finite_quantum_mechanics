
use crate::cayley_menger::simplex_volume_cayley_menger;

pub const DEFAULT_ANGLE_TOL: f64 = 1e-9;

pub fn triangle_angle_at(
    triangle: &[usize; 3],
    vertex: usize,
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<f64, String> {
    let (i, j, k) = (triangle[0], triangle[1], triangle[2]);
    let (p, q, opp) = if vertex == i {
        (j, k, get_length(j, k))
    } else if vertex == j {
        (i, k, get_length(i, k))
    } else if vertex == k {
        (i, j, get_length(i, j))
    } else {
        return Err(format!("Vertex {vertex} not in triangle {triangle:?}"));
    };

    let a = get_length(vertex, p).ok_or_else(|| format!("Missing length ({vertex}, {p})"))?;
    let b = get_length(vertex, q).ok_or_else(|| format!("Missing length ({vertex}, {q})"))?;
    let c = opp.ok_or_else(|| format!("Missing length ({p}, {q})"))?;

    let denom = 2.0 * a * b;
    if denom.abs() < DEFAULT_ANGLE_TOL {
        return Err("Degenerate triangle side length".to_string());
    }
    let cos_theta = ((a * a + b * b - c * c) / denom).clamp(-1.0, 1.0);
    Ok(cos_theta.acos())
}

pub fn tetrahedron_dihedral_angle_at_edge(
    tetrahedron: &[usize; 4],
    edge: (usize, usize),
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<f64, String> {
    let (e1, e2) = edge;
    let mut opp_verts = Vec::new();
    for &v in tetrahedron {
        if v != e1 && v != e2 {
            opp_verts.push(v);
        }
    }
    if opp_verts.len() != 2 {
        return Err(format!(
            "Edge {edge:?} does not belong to tetrahedron {tetrahedron:?}"
        ));
    }
    let w1 = opp_verts[0];
    let w2 = opp_verts[1];

    let ell = get_length(e1, e2).ok_or_else(|| format!("Missing edge length {edge:?}"))?;
    let _v_tet = simplex_volume_cayley_menger(tetrahedron, &get_length)?;
    let a1 = simplex_volume_cayley_menger(&[e1, e2, w1], &get_length)?;
    let a2 = simplex_volume_cayley_menger(&[e1, e2, w2], &get_length)?;

    if a1 < DEFAULT_ANGLE_TOL || a2 < DEFAULT_ANGLE_TOL {
        return Err("Degenerate triangle face area in tetrahedron".to_string());
    }

    let d12_sq = ell * ell;
    let d13 = get_length(e1, w1).ok_or("Missing length")?;
    let d23 = get_length(e2, w1).ok_or("Missing length")?;
    let d14 = get_length(e1, w2).ok_or("Missing length")?;
    let d24 = get_length(e2, w2).ok_or("Missing length")?;
    let d34 = get_length(w1, w2).ok_or("Missing length")?;

    let term1 = (d12_sq + d13 * d13 - d23 * d23) * (d12_sq + d14 * d14 - d24 * d24);
    let term2 = 2.0 * d12_sq * (d13 * d13 + d14 * d14 - d34 * d34);
    let num = term2 - term1;
    let denom = 16.0 * a1 * a2;

    let cos_theta = (num / denom).clamp(-1.0, 1.0);
    let theta = cos_theta.acos();

    if !theta.is_finite() {
        return Err("Non-finite dihedral angle computed".to_string());
    }
    Ok(theta)
}

pub fn pentachoron_dihedral_angle_at_triangle(
    four_simplex: &[usize; 5],
    triangle: &[usize; 3],
    get_length: impl Fn(usize, usize) -> Option<f64>,
) -> Result<f64, String> {
    let unique: std::collections::BTreeSet<_> = four_simplex.iter().copied().collect();
    let hinge: std::collections::BTreeSet<_> = triangle.iter().copied().collect();
    if unique.len() != 5 || hinge.len() != 3 || !hinge.is_subset(&unique) {
        return Err("invalid simplex or hinge vertex IDs".into());
    }
    let opposite: Vec<_> = unique.difference(&hinge).copied().collect();
    let origin = triangle[0];
    let vertices = [triangle[1], triangle[2], opposite[0], opposite[1]];
    let squared = |i, j| -> Result<f64, String> {
        let length = get_length(i, j).ok_or("missing edge length")?;
        if !length.is_finite() || length <= 0.0 || !(length * length).is_finite() {
            return Err("edge length must be finite and positive".into());
        }
        Ok(length * length)
    };
    let mut gram = [[0.0; 4]; 4];
    for i in 0..4 {
        gram[i][i] = squared(origin, vertices[i])?;
        for j in 0..i {
            let dot = (gram[i][i] + gram[j][j] - squared(vertices[i], vertices[j])?) / 2.0;
            gram[i][j] = dot;
            gram[j][i] = dot;
        }
    }
    let det = gram[0][0] * gram[1][1] - gram[0][1] * gram[0][1];
    if !det.is_finite() || det <= 0.0 {
        return Err("degenerate hinge".into());
    }
    let normal_dot = |i: usize, j: usize| {
        gram[i][j]
            - (gram[i][0] * (gram[1][1] * gram[j][0] - gram[0][1] * gram[j][1])
                + gram[i][1] * (gram[0][0] * gram[j][1] - gram[0][1] * gram[j][0]))
                / det
    };
    let aa = normal_dot(2, 2);
    let bb = normal_dot(3, 3);
    let ab = normal_dot(2, 3);
    let residual_det = aa * bb - ab * ab;
    if aa <= 0.0 || bb <= 0.0 || !residual_det.is_finite() || residual_det <= 0.0 {
        return Err("degenerate or non-Euclidean 4-simplex".into());
    }
    Ok((ab / (aa.sqrt() * bb.sqrt())).clamp(-1.0, 1.0).acos())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_regular_tetrahedron_dihedral_angle() {
        let side = 1.0;
        let get_len = |_: usize, _: usize| Some(side);
        let tet = [0, 1, 2, 3];
        let theta = tetrahedron_dihedral_angle_at_edge(&tet, (0, 1), get_len).unwrap();
        let expected = (1.0f64 / 3.0).acos();
        assert!((theta - expected).abs() < 1e-7);
    }
}
