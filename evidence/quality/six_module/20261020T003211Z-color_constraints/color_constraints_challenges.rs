#[cfg(test)]
mod independent_color_checks {
    use super::*;
    use num_traits::One;

    fn oracle(vertices: usize, edges: &[(usize,usize)], colors: usize, forbidden: &BTreeSet<(usize,usize)>) -> MinimumColorViolations {
        let mut choices = Vec::new();
        for rank in 0..colors.pow(vertices as u32) {
            let mut digits = rank;
            let mut coloring = vec![0;vertices];
            for digit in coloring.iter_mut().rev() { *digit = digits % colors; digits /= colors; }
            let violations = edges.iter().enumerate().filter_map(|(index,&(u,v))| {
                let left = coloring[u]; let right = coloring[v];
                forbidden.iter().any(|&(a,b)| (a==left && b==right)||(a==right && b==left)).then_some(index)
            }).collect::<Vec<_>>();
            choices.push((violations.len(),rank,MinimumColorViolations {coloring,violated_edges:violations}));
        }
        choices.sort_by_key(|(count,rank,_)| (*count,*rank));
        choices.remove(0).2
    }

    #[test]
    fn all_small_graph_and_literal_forbidden_sets_match_global_minimum() {
        for colors in 1usize..=3 {
            let max_vertices = if colors==3 {2} else {3};
            for vertices in 0..=max_vertices {
                let pairs = (0..vertices).flat_map(|u| (u..vertices).map(move |v|(u,v))).collect::<Vec<_>>();
                for graph in 0..(1usize << pairs.len()) {
                    let edges = pairs.iter().enumerate().filter_map(|(i,&edge)| (graph & (1<<i)!=0).then_some(edge)).collect::<Vec<_>>();
                    for mask in 0..(1usize << (colors*colors)) {
                        let forbidden = (0..colors*colors).filter_map(|i| (mask & (1<<i)!=0).then_some((i/colors,i%colors))).collect::<BTreeSet<_>>();
                        let count = colors.pow(vertices as u32); let checks = count*edges.len();
                        let expected = oracle(vertices,&edges,colors,&forbidden);
                        assert_eq!(minimum_color_violations(vertices,&edges,colors,&forbidden,count,checks).unwrap(),expected);
                        if checks>0 {
                            assert_eq!(minimum_color_violations(vertices,&edges,colors,&forbidden,count,checks-1).unwrap_err(),
                                ColorConstraintError::Enumeration(CombinatoricsError::BudgetExceeded {
                                    what:"coloring edge checks",requested:BigUint::from(checks),limit:checks-1}));
                        }
                    }
                }
            }
        }
    }

    #[test]
    fn duplicate_oriented_edges_and_first_tie_are_literal() {
        for edges in [vec![(0,1),(1,0),(0,1)],vec![(0,0),(1,1),(0,1)],vec![(1,0),(0,0)]] {
            for mask in 0..16usize {
                let forbidden = (0..4).filter_map(|i|(mask&(1<<i)!=0).then_some((i/2,i%2))).collect();
                assert_eq!(minimum_color_violations(2,&edges,2,&forbidden,4,4*edges.len()).unwrap(),oracle(2,&edges,2,&forbidden));
            }
        }
        let all_pairs = BTreeSet::from([(0,0),(0,1),(1,0),(1,1)]);
        assert_eq!(minimum_color_violations(2,&[(0,1)],2,&all_pairs,4,4).unwrap(),
            MinimumColorViolations {coloring:vec![0,0],violated_edges:vec![0]});
    }

    #[test]
    fn failure_priority_exact_work_and_maximum_scalar_cases() {
        let invalid = BTreeSet::from([(usize::MAX,0)]);
        assert_eq!(minimum_color_violations(0,&[(usize::MAX,0)],0,&invalid,0,0).unwrap_err(),ColorConstraintError::EmptyPalette {colors:0});
        assert_eq!(minimum_color_violations(1,&[(0,0),(1,0)],2,&invalid,0,0).unwrap_err(),ColorConstraintError::Endpoint {index:1});
        assert_eq!(minimum_color_violations(1,&[],2,&BTreeSet::from([(1,3),(2,0)]),0,0).unwrap_err(),ColorConstraintError::Color {left:1,right:3,colors:2});
        assert!(matches!(minimum_color_violations(usize::MAX,&[],1,&BTreeSet::new(),1,0),Err(ColorConstraintError::Enumeration(CombinatoricsError::BudgetExceeded {what:"Cartesian word width",..}))));
        assert!(matches!(minimum_color_violations(1,&[],2,&BTreeSet::new(),1,0),Err(ColorConstraintError::Enumeration(CombinatoricsError::BudgetExceeded {what:"Cartesian words",..}))));
        let maximum = usize::MAX;
        assert_eq!(minimum_color_violations(1,&[(0,0),(0,0)],maximum,&BTreeSet::new(),maximum,maximum).unwrap_err(),
            ColorConstraintError::Enumeration(CombinatoricsError::BudgetExceeded {what:"coloring edge checks",requested:BigUint::from(maximum)*BigUint::from(2u8),limit:maximum}));
        assert_eq!(minimum_color_violations(1,&[(0,0)],maximum,&BTreeSet::from([(0,0)]),maximum,maximum).unwrap(),
            MinimumColorViolations {coloring:vec![1],violated_edges:vec![]});
        assert_eq!(minimum_color_violations(0,&[],1,&BTreeSet::new(),1,0).unwrap(),MinimumColorViolations {coloring:vec![],violated_edges:vec![]});
        assert_eq!(color_at(&[0],1,7),Err(ColorConstraintError::Endpoint {index:7}));
        let error = ColorConstraintError::Enumeration(CombinatoricsError::BudgetExceeded {what:"x",requested:BigUint::one(),limit:0});
        assert_eq!(error.violated_invariant(),"emitted cardinality stays inside the caller budget");
        assert_eq!(error.measured_parameters(),vec![("what","x".into()),("requested","1".into()),("limit","0".into())]);
        assert_eq!(ColorConstraintError::Endpoint {index:2}.measured_parameters(),vec![("index","2".into())]);
        assert_eq!(ColorConstraintError::Color {left:3,right:4,colors:2}.measured_parameters(),vec![("left","3".into()),("right","4".into()),("colors","2".into())]);
    }
}
