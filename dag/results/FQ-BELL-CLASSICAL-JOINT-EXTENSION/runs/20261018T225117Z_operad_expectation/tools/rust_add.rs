
/// Nullary generator, with rows ordered by the A0,A1,B0,B1 bit mask.
pub fn response_products() -> [[i32; 4]; 16] {
    std::array::from_fn(|mask| {
        let [a0, a1, b0, b1] = std::array::from_fn(|j| if mask & (1 << j) == 0 { -1 } else { 1 });
        [a0*b0, a0*b1, a1*b0, a1*b1]
    })
}

fn canonical(q: &Q) -> bool {
    q.denom().is_positive() && q.numer().gcd(q.denom()).is_one()
}

fn joint_weights(weights: &[Q]) -> Result<(), JointBellError> {
    if weights.len() != 16 { return Err(JointBellError::WrongCarrier); }
    for (i, q) in weights.iter().enumerate() {
        if !canonical(q) { return Err(JointBellError::InvalidRational(i)); }
        if q.is_negative() { return Err(JointBellError::NegativeWeight(i)); }
    }
    if weights.iter().cloned().sum::<Q>() != Q::one() { return Err(JointBellError::NotNormalized); }
    Ok(())
}

/// Binary generator on a single joint law and an arbitrary exact Q^4 table.
/// The Bell bound requires response_products(), rather than an arbitrary table.
pub fn joint_expectation(weights: &[Q], responses: &[[Q; 4]]) -> Result<[Q; 4], JointBellError> {
    joint_weights(weights)?;
    if responses.len() != 16 { return Err(JointBellError::WrongResponseCarrier); }
    for (i, row) in responses.iter().enumerate() {
        for (j, q) in row.iter().enumerate() {
            if !canonical(q) { return Err(JointBellError::InvalidResponseRational(i, j)); }
        }
    }
    Ok(std::array::from_fn(|j| weights.iter().zip(responses).map(|(p,row)| p*&row[j]).sum()))
}

/// Unary generator. A scalar value alone is not a Bell certificate.
pub fn chsh_linear(e: &[Q; 4]) -> Result<Q, JointBellError> {
    for (j,q) in e.iter().enumerate() {
        if !canonical(q) { return Err(JointBellError::InvalidResponseRational(0,j)); }
    }
    Ok(&e[0]+&e[1]+&e[2]-&e[3])
}

/// Independently recompute every field; does not call the certificate producer.
pub fn verify_joint_certificate(weights: &[Q], certificate: &JointBellCertificate) -> Result<(), JointBellError> {
    joint_weights(weights)?;
    if certificate.correlators.iter().chain([
        &certificate.chsh, &certificate.positive_score_mass, &certificate.negative_score_mass,
        &certificate.lower_slack, &certificate.upper_slack,
    ]).any(|q| !canonical(q)) { return Err(JointBellError::CertificateMismatch); }
    let products = response_products();
    let e: [Q;4] = std::array::from_fn(|j| (0..16).map(|m| &weights[m]*Q::from_integer(products[m][j].into())).sum());
    let mut plus=Q::zero();let mut minus=Q::zero();
    for (m,row) in products.iter().enumerate() {
        if row[0]+row[1]+row[2]-row[3] == 2 { plus+=&weights[m]; } else { minus+=&weights[m]; }
    }
    let s=&e[0]+&e[1]+&e[2]-&e[3];let two=Q::from_integer(2.into());
    let independent=JointBellCertificate { correlators:e,lower_slack:&two+&s,upper_slack:&two-&s,
        chsh:s,positive_score_mass:plus,negative_score_mass:minus };
    if *certificate != independent { return Err(JointBellError::CertificateMismatch); }
    Ok(())
}

#[cfg(test)]
mod operad_tests {
    use super::*;
    fn q(n:i64,d:i64)->Q { Q::new(n.into(),d.into()) }
    #[test]
    fn generic_linearity_and_bell_composition() {
        let law:Vec<Q>=(1..=16).map(|i|q(i,136)).collect();
        let table:Vec<[Q;4]>=(0..16).map(|i|std::array::from_fn(|j|q((i+1)*(j as i64-2),i+j as i64+3))).collect();
        let left=chsh_linear(&joint_expectation(&law,&table).unwrap()).unwrap();
        let right:Q=law.iter().zip(&table).map(|(p,row)|p*chsh_linear(row).unwrap()).sum();
        assert_eq!(left,right);
        let products:Vec<[Q;4]>=response_products().iter().map(|row|row.map(|n|q(n.into(),1))).collect();
        let c=certify_joint_law(&law).unwrap();
        assert_eq!(joint_expectation(&law,&products).unwrap(),c.correlators);
        assert_eq!(chsh_linear(&c.correlators).unwrap(),c.chsh);
        assert_eq!(chsh_linear(&joint_expectation(&law,&vec![[q(2,1),q(2,1),q(2,1),q(2,1)];16]).unwrap()).unwrap(),q(4,1));
    }
    #[test]
    fn malformed_response_and_certificate_are_rejected_before_arithmetic() {
        let law=vec![q(1,16);16];let mut table=vec![[q(1,1),q(1,1),q(1,1),q(1,1)];16];
        assert_eq!(joint_expectation(&law,&table[..15]),Err(JointBellError::WrongResponseCarrier));
        table[7][2]=Q::new_raw(1.into(),0.into());
        assert_eq!(joint_expectation(&law,&table),Err(JointBellError::InvalidResponseRational(7,2)));
        let mut c=certify_joint_law(&law).unwrap();c.chsh=Q::new_raw(1.into(),0.into());
        assert_eq!(verify_joint_certificate(&law,&c),Err(JointBellError::CertificateMismatch));
    }
    #[test]
    fn each_forged_component_is_rejected_and_all_mixtures_are_accepted() {
        let law=vec![q(1,16);16];let c=certify_joint_law(&law).unwrap();
        verify_joint_certificate(&law,&c).unwrap();
        for k in 0..9 {
            let mut bad=c.clone();
            match k {0..=3=>bad.correlators[k]+=q(1,1),4=>bad.chsh+=q(1,1),5=>bad.positive_score_mass+=q(1,1),
                6=>bad.negative_score_mass+=q(1,1),7=>bad.lower_slack+=q(1,1),_=>bad.upper_slack+=q(1,1)}
            assert_eq!(verify_joint_certificate(&law,&bad),Err(JointBellError::CertificateMismatch));
        }
        for i in 0..16 {for j in 0..16 {for p in [q(1,7),q(2,5),q(11,13)] {
            let mut law=vec![Q::zero();16];law[i]+=&p;law[j]+=Q::one()-p;
            verify_joint_certificate(&law,&certify_joint_law(&law).unwrap()).unwrap();
        }}}
    }
}
