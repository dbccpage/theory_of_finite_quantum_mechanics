#[derive(Debug)] enum HomologicalError{InvalidDegree(i32)}
struct CochainComplex{c0_dim:usize,c1_dim:usize,c2_dim:usize}
impl CochainComplex{
    pub fn dim(&self, degree: usize) -> Result<usize, HomologicalError> {
        match degree {
            0 => Ok(self.c0_dim),
            1 => Ok(self.c1_dim),
            2 => Ok(self.c2_dim),
            _ => Err(HomologicalError::InvalidDegree(degree as i32)),
        }
    }
}
#[test] fn preserves_rejected_index(){let object=CochainComplex{c0_dim:1,c1_dim:0,c2_dim:0};let degree=4294967296usize;let Err(HomologicalError::InvalidDegree(got))=object.dim(degree) else {panic!("expected refusal")};assert_eq!(got.to_string(),degree.to_string(),"the rejected index must be preserved");}
