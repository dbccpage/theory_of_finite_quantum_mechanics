use omega_quantum_physics::toric_code::ToricCode;
#[test]
fn toric_code_two_by_two_reproduces_the_regression_stabilizers() {
    let t = ToricCode::new(2, 2).unwrap();
    for g in finite_qm_native::campaigns::toric::ToricCode2x2::star_operators()
        .iter()
        .chain(finite_qm_native::campaigns::toric::ToricCode2x2::plaquette_operators().iter())
    {
        assert!(t.code().in_stabilizer_group(g).unwrap());
    }
}
