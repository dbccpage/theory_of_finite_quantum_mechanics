//! Private provider storage with owned, fallible exact arithmetic.
//! Raw construction transports coefficients; arithmetic admits every input,
//! including entries unused by empty products. Limits count output scalar slots
//! and arithmetic calls, not bytes, bit growth, validation cost or elapsed time.
//! AuthorityEffect: None.
#![forbid(unsafe_code)]
use ::linear_algebra::backend::basic_matrix as storage;
use super::scalars::{Ring, ScalarError, Semiring};
pub use storage::{CheckedMatrixError, MatrixError, OperationLimits};
type ArithmeticResult<T> = Result<T, CheckedMatrixError<ScalarError>>;
pub const DEFAULT_LIMITS: OperationLimits = OperationLimits { max_elements:4096, max_scalar_ops:1_000_000 };

/// Shape-checked transport. No Deref or public provider escape is exposed.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(transparent)]
pub struct BasicMatrix<T>(storage::BasicMatrix<T>);
impl<T> BasicMatrix<T> {
    pub fn from_row_major(rows:usize,cols:usize,data:Vec<T>)->Result<Self,MatrixError> { storage::BasicMatrix::from_row_major(rows,cols,data).map(Self) }
    pub fn from_row_major_with_limit(rows:usize,cols:usize,data:Vec<T>,limit:usize)->Result<Self,MatrixError> { storage::BasicMatrix::from_row_major_with_limit(rows,cols,data,limit).map(Self) }
    pub fn try_from_fn<F:FnMut(usize,usize)->T>(rows:usize,cols:usize,f:F)->Result<Self,MatrixError> { storage::BasicMatrix::try_from_fn(rows,cols,f).map(Self) }
    pub fn try_from_fn_with_limit<F:FnMut(usize,usize)->T>(rows:usize,cols:usize,limit:usize,f:F)->Result<Self,MatrixError> { storage::BasicMatrix::try_from_fn_with_limit(rows,cols,limit,f).map(Self) }
    pub fn try_from_fn_result<F:FnMut(usize,usize)->Result<T,E>,E:From<MatrixError>>(rows:usize,cols:usize,f:F)->Result<Self,E> { storage::BasicMatrix::try_from_fn_result(rows,cols,f).map(Self) }
    pub fn try_from_fn_result_with_limit<F:FnMut(usize,usize)->Result<T,E>,E:From<MatrixError>>(rows:usize,cols:usize,limit:usize,f:F)->Result<Self,E> { storage::BasicMatrix::try_from_fn_result_with_limit(rows,cols,limit,f).map(Self) }
    pub fn rows(&self)->usize { self.0.rows() }
    pub fn cols(&self)->usize { self.0.cols() }
    pub fn shape(&self)->(usize,usize) { self.0.shape() }
    pub fn as_slice(&self)->&[T] { self.0.as_slice() }
    pub fn get_ref(&self,row:usize,col:usize)->Result<&T,MatrixError> { self.0.get_ref(row,col) }
    pub fn try_to_nalgebra(&self)->Result<nalgebra::DMatrix<T>,MatrixError> where T:nalgebra::Scalar { self.0.try_to_nalgebra() }
    pub fn try_from_nalgebra(m:&nalgebra::DMatrix<T>)->Result<Self,MatrixError> where T:nalgebra::Scalar { storage::BasicMatrix::try_from_nalgebra(m).map(Self) }
}
impl<T:Clone> BasicMatrix<T> {
    pub fn get(&self,row:usize,col:usize)->Result<T,MatrixError> { self.0.get(row,col) }
    pub fn set(&mut self,row:usize,col:usize,value:T)->Result<(),MatrixError> { self.0.set(row,col,value) }
    pub fn try_transpose(&self)->Result<Self,MatrixError> { self.0.try_transpose().map(Self) }
    pub fn try_map<U,E:From<MatrixError>,F:FnMut(&T)->Result<U,E>>(&self,f:F)->Result<BasicMatrix<U>,E> { self.0.try_map(f).map(BasicMatrix) }
}
fn scalar(e:ScalarError)->CheckedMatrixError<ScalarError> { CheckedMatrixError::Scalar(e) }
fn admit<T:Semiring>(values:&[T])->ArithmeticResult<()> {
    for value in values { value.validate().map_err(scalar)?; }
    Ok(())
}
fn preflight(rows:usize,cols:usize,inner:usize,limits:OperationLimits)->Result<usize,MatrixError> {
    let elements=super::element_count(rows,cols)?;
    let work=super::times(super::times(2,elements)?,inner)?;
    super::charge(limits,elements,work)?;
    Ok(elements)
}
impl<T:Semiring> BasicMatrix<T> {
    pub fn zero(rows:usize,cols:usize)->Result<Self,MatrixError> { Self::try_from_fn_with_limit(rows,cols,DEFAULT_LIMITS.max_elements,|_,_|T::zero()) }
    pub fn mul(&self,rhs:&Self)->ArithmeticResult<Self> { self.checked_mul(rhs) }
    pub fn mul_vec(&self,rhs:&[T])->ArithmeticResult<Vec<T>> { self.checked_mul_vec(rhs) }
    pub fn add(&self,rhs:&Self)->ArithmeticResult<Self> { self.checked_add(rhs) }
    pub fn checked_add(&self,rhs:&Self)->ArithmeticResult<Self> { self.checked_add_with_limit(rhs,DEFAULT_LIMITS.max_elements) }
    pub fn checked_add_with_limit(&self,rhs:&Self,limit:usize)->ArithmeticResult<Self> { self.zip(rhs,limit,|a,b|a.try_add(b)) }
    fn zip<F:FnMut(&T,&T)->Result<T,ScalarError>>(&self,rhs:&Self,limit:usize,mut f:F)->ArithmeticResult<Self> {
        if self.shape()!=rhs.shape() { return Err(MatrixError::DimensionMismatch{left:self.shape(),right:rhs.shape()}.into()); }
        super::charge(OperationLimits{max_elements:limit,max_scalar_ops:usize::MAX},self.as_slice().len(),0)?;
        admit(self.as_slice())?; admit(rhs.as_slice())?;
        let mut out=super::reserve(self.as_slice().len())?;
        for (a,b) in self.as_slice().iter().zip(rhs.as_slice()) { out.push(f(a,b).map_err(scalar)?); }
        Ok(Self::from_row_major(self.rows(),self.cols(),out)?)
    }
    pub fn checked_mul(&self,rhs:&Self)->ArithmeticResult<Self> { self.checked_mul_with_limits(rhs,DEFAULT_LIMITS) }
    pub fn checked_mul_with_limit(&self,rhs:&Self,limit:usize)->ArithmeticResult<Self> { self.checked_mul_with_limits(rhs,OperationLimits{max_elements:limit,max_scalar_ops:DEFAULT_LIMITS.max_scalar_ops}) }
    pub fn checked_mul_with_limits(&self,rhs:&Self,limits:OperationLimits)->ArithmeticResult<Self> {
        if self.cols()!=rhs.rows() { return Err(MatrixError::DimensionMismatch{left:self.shape(),right:rhs.shape()}.into()); }
        let count=preflight(self.rows(),rhs.cols(),self.cols(),limits)?;
        admit(self.as_slice())?; admit(rhs.as_slice())?;
        let mut out=super::reserve(count)?;
        for index in 0..count {
            let (r,c)=(index/rhs.cols(),index%rhs.cols());
            let mut sum=T::zero();
            for k in 0..self.cols() {
                let product=self.as_slice()[r*self.cols()+k].try_mul(&rhs.as_slice()[k*rhs.cols()+c]).map_err(scalar)?;
                sum=sum.try_add(&product).map_err(scalar)?;
            }
            out.push(sum);
        }
        Ok(Self::from_row_major(self.rows(),rhs.cols(),out)?)
    }
    pub fn checked_mul_vec(&self,rhs:&[T])->ArithmeticResult<Vec<T>> { self.checked_mul_vec_with_limits(rhs,DEFAULT_LIMITS) }
    pub fn checked_mul_vec_with_limit(&self,rhs:&[T],limit:usize)->ArithmeticResult<Vec<T>> { self.checked_mul_vec_with_limits(rhs,OperationLimits{max_elements:limit,max_scalar_ops:DEFAULT_LIMITS.max_scalar_ops}) }
    pub fn checked_mul_vec_with_limits(&self,rhs:&[T],limits:OperationLimits)->ArithmeticResult<Vec<T>> {
        if self.cols()!=rhs.len() { return Err(MatrixError::DimensionMismatch{left:self.shape(),right:(rhs.len(),1)}.into()); }
        let count=preflight(self.rows(),1,self.cols(),limits)?;
        admit(self.as_slice())?; admit(rhs)?;
        let mut out=super::reserve(count)?;
        for row in 0..count {
            let mut sum=T::zero();
            for (col,value) in rhs.iter().enumerate() {
                let product=self.as_slice()[row*self.cols()+col].try_mul(value).map_err(scalar)?;
                sum=sum.try_add(&product).map_err(scalar)?;
            }
            out.push(sum);
        }
        Ok(out)
    }
}
impl<T:Ring> BasicMatrix<T> {
    pub fn sub(&self,rhs:&Self)->ArithmeticResult<Self> { self.checked_sub(rhs) }
    pub fn checked_sub(&self,rhs:&Self)->ArithmeticResult<Self> { self.checked_sub_with_limit(rhs,DEFAULT_LIMITS.max_elements) }
    pub fn checked_sub_with_limit(&self,rhs:&Self,limit:usize)->ArithmeticResult<Self> { self.zip(rhs,limit,|a,b|a.try_sub(b)) }
}
