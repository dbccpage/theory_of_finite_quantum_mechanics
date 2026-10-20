#[cfg(test)]
mod boundary_review {
    use super::*;

    #[test]
    fn shape_and_checked_integer_refusals() {
        assert_eq!(ray_orthogonality(&[vec![1, 1], vec![1]]), Err(FiniteGeometryError::DimensionMismatch { index: 1, expected: 2, found: 1 }));
        assert_eq!(dot(&[1], &[1, 0]), Err(FiniteGeometryError::DimensionMismatch { index: 1, expected: 1, found: 2 }));
        assert_eq!(dot(&[i64::MAX], &[2]), Err(FiniteGeometryError::DotOverflow { left: i64::MAX, right: 2 }));
        assert_eq!(dot(&[i64::MAX, 1, -1], &[1, 1, 1]), Err(FiniteGeometryError::DotOverflow { left: i64::MAX, right: 1 }));
        assert_eq!(dot(&[i64::MIN], &[-1]), Err(FiniteGeometryError::DotOverflow { left: i64::MIN, right: -1 }));
        assert_eq!(dot(&[i64::MAX, -1], &[1, 1]), Ok(i64::MAX - 1));
        assert_eq!(dot(&[i64::MIN, 1], &[1, 1]), Ok(i64::MIN + 1));
        let input = vec![vec![i64::MAX], vec![2]];
        let before = input.clone();
        assert!(ray_orthogonality(&input).is_err());
        assert_eq!(input, before);
    }

    #[test]
    fn allocation_and_work_admission() {
        assert_eq!(admit_product("test", 1024, 1024, MAX_GEOMETRY_CELLS), Ok(MAX_GEOMETRY_CELLS));
        assert!(matches!(admit_product("test", usize::MAX, 2, MAX_GEOMETRY_CELLS), Err(FiniteGeometryError::ResourceLimit { requested: usize::MAX, .. })));
        assert!(admit_product("test", 1024, 1025, MAX_GEOMETRY_CELLS).is_err());
        assert!(matches!(ray_orthogonality(&vec![vec![]; 1025]), Err(FiniteGeometryError::ResourceLimit { operation: "ray matrix cells", .. })));
        assert_eq!(ray_orthogonality(&vec![vec![]; 1024]).unwrap().len(), 1024);
        assert!(matches!(ray_orthogonality(&[vec![0; MAX_GEOMETRY_CELLS + 1]]), Err(FiniteGeometryError::ResourceLimit { operation: "ray input cells", .. })));
        assert!(matches!(ray_orthogonality(&vec![vec![0; 4096]; 128]), Err(FiniteGeometryError::ResourceLimit { operation: "ray dot terms", .. })));
        assert!(matches!(IncidenceStructure::new(usize::MAX, vec![vec![0, 1]; 3]), Err(FiniteGeometryError::ResourceLimit { .. })));
        assert!(matches!(IncidenceStructure::new(3000, vec![vec![0, 1]; 3]), Err(FiniteGeometryError::ResourceLimit { operation: "incidence pair checks", .. })));
        assert!(matches!(IncidenceStructure::new(3, vec![vec![0; MAX_GEOMETRY_CELLS + 1], vec![0, 1], vec![1, 2]]), Err(FiniteGeometryError::ResourceLimit { operation: "incidence entries", .. })));
        assert!(admit_incidence_entries(&[vec![0; MAX_GEOMETRY_CELLS]]).is_ok());
        assert!(matches!(IncidenceStructure::new(2, vec![vec![0]; 3]), Err(FiniteGeometryError::TooSmall)));
    }

    #[test]
    fn incidence_against_bitmask_oracle() {
        for n in [3usize, 4] {
            let masks: Vec<usize> = (0..1usize << n).filter(|x| x.count_ones() >= 2).collect();
            for a in &masks { for b in &masks { for c in &masks {
                let selected = [*a, *b, *c];
                let lines = selected.iter().map(|mask| (0..n).filter(|i| mask & (1 << i) != 0).collect()).collect();
                let geometry = IncidenceStructure::new(n, lines).unwrap();
                assert_eq!((geometry.num_points(), geometry.num_lines()), (n, 3));
                let mut counts = vec![];
                for p in 0..n { for q in p+1..n {
                    let mask = (1 << p) | (1 << q);
                    counts.push(selected.iter().filter(|line| **line & mask == mask).count());
                }}
                assert_eq!(geometry.is_partial_linear_space(), counts.iter().all(|x| *x <= 1));
                assert_eq!(geometry.is_linear_space(), counts.iter().all(|x| *x == 1));
                for p in 0..n {
                    let expected: Vec<usize> = (0..3).filter(|i| selected[*i] & (1 << p) != 0).collect();
                    assert_eq!(geometry.lines_on_point(p).unwrap(), expected);
                    for l in 0..3 { assert_eq!(geometry.is_incident(p, l).unwrap(), selected[l] & (1 << p) != 0); }
                }
                for i in 0..3 { for j in 0..3 {
                    let expected: Vec<usize> = (0..n).filter(|p| (selected[i] & selected[j]) & (1 << p) != 0).collect();
                    assert_eq!(geometry.line_intersection(i, j).unwrap(), expected);
                }}
            }}}
        }
    }

    #[test]
    fn fano_and_all_admitted_affine_orders() {
        let fano = fano_plane().unwrap();
        let got: BTreeSet<_> = (0..7).map(|l| fano.points_on_line(l).unwrap().iter().copied().collect::<Vec<_>>()).collect();
        let mut expected = BTreeSet::new();
        for a in 1..8 { for b in a+1..8 { for c in b+1..8 {
            if a ^ b ^ c == 0 { expected.insert(vec![a-1,b-1,c-1]); }
        }}}
        assert_eq!(got, expected);
        for p in [2, 3, 5, 7, 11, 13] {
            let plane = affine_plane_ag2(p).unwrap();
            assert_eq!((plane.num_points(), plane.num_lines()), (p*p, p*(p+1)));
            for l in 0..p*(p+1) {
                let expected: BTreeSet<_> = (0..p*p).filter(|point| {
                    let (x,y) = (point/p, point%p);
                    if l < p { x == l } else { (y + p*p - ((l-p)/p)*x) % p == (l-p)%p }
                }).collect();
                assert_eq!(plane.points_on_line(l).unwrap(), &expected);
            }
            assert!(plane.is_linear_space());
            for point in 0..p*p { assert_eq!(plane.lines_on_point(point).unwrap().len(), p+1); }
        }
        for p in [0, 1, 14, usize::MAX] { assert_eq!(affine_plane_ag2(p), Err(FiniteGeometryError::InvalidDimension)); }
        for p in [4, 6, 8, 9, 10, 12] { assert_eq!(affine_plane_ag2(p), Err(FiniteGeometryError::NotPrime(p))); }
    }

    #[test]
    fn ray_matrix_against_i128_polynomial() {
        assert_eq!(ray_orthogonality(&[]).unwrap(), Vec::<Vec<bool>>::new());
        for width in 0..=3u32 {
            let vectors: Vec<Vec<i64>> = (0..3usize.pow(width)).map(|mut code| {
                (0..width).map(|_| { let value = (code % 3) as i64 - 1; code /= 3; value }).collect()
            }).collect();
            let result = ray_orthogonality(&vectors).unwrap();
            for i in 0..vectors.len() { for j in 0..vectors.len() {
                let exact: i128 = (0..width as usize).map(|k| vectors[i][k] as i128 * vectors[j][k] as i128).sum();
                assert_eq!(result[i][j], i != j && exact == 0);
            }}
        }
    }

    #[test]
    fn error_boundaries_and_diagnostics() {
        let triangle = IncidenceStructure::new(3, vec![vec![0, 1, 0], vec![1, 2], vec![0, 2]]).unwrap();
        assert!(triangle.is_linear_space());
        assert_eq!(triangle.points_on_line(0).unwrap().len(), 2);
        assert_eq!(triangle.is_incident(3, 3), Err(FiniteGeometryError::PointOutOfBounds { point: 3, num_points: 3 }));
        assert_eq!(triangle.is_incident(0, 3), Err(FiniteGeometryError::LineOutOfBounds { line: 3, num_lines: 3 }));
        assert!(triangle.lines_on_point(3).is_err());
        assert!(triangle.line_intersection(0, 3).is_err());
        assert_eq!(IncidenceStructure::new(3, vec![vec![0, 0]; 3]), Err(FiniteGeometryError::DegenerateLine));
        assert_eq!(IncidenceStructure::new(3, vec![vec![0, 3]; 3]), Err(FiniteGeometryError::PointOutOfBounds { point: 3, num_points: 3 }));
        assert_eq!(mark_orthogonal_row(&mut [], &[], 0), Err(FiniteGeometryError::PointOutOfBounds { point: 0, num_points: 0 }));
        assert!(mark_pair(&mut [], &[], &[], 0, 0).is_err());
        assert!(write_cell(&mut [], 0, 0).is_err());
        assert!(write_cell(&mut [vec![]], 0, 0).is_err());
        let shape = FiniteGeometryError::DimensionMismatch { index: 2, expected: 3, found: 4 };
        assert_eq!(shape.violated_invariant(), "all vectors have the same coordinate dimension");
        assert_eq!(shape.measured_parameters(), vec![("index", "2".to_owned()), ("expected", "3".to_owned()), ("found", "4".to_owned())]);
        let budget = FiniteGeometryError::ResourceLimit { operation: "test", requested: 5, maximum: 4 };
        assert_eq!(budget.violated_invariant(), "geometry allocation and work remain within admitted budgets");
        assert_eq!(budget.measured_parameters(), vec![("operation", "test".to_owned()), ("requested", "5".to_owned()), ("maximum", "4".to_owned())]);
    }
}
