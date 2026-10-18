use crate::cyclotomic::GaussianRat;
use crate::rational::Rational;
use linear_algebra::backend::basic_matrix::BasicMatrix;

pub fn regular_representation(z: &GaussianRat) -> BasicMatrix<Rational> {
    BasicMatrix::from_row_major(2, 2, vec![z.re.clone(), -&z.im, z.im.clone(), z.re.clone()])
        .expect("the regular field representation has four entries")
}
pub fn regular_coordinates(m: &BasicMatrix<Rational>) -> Option<GaussianRat> {
    if m.shape() != (2, 2) {
        return None;
    }
    let data = m.as_slice();
    (data[0] == data[3] && data[1] == -&data[2]).then(|| GaussianRat {
        re: data[0].clone(),
        im: data[2].clone(),
    })
}
