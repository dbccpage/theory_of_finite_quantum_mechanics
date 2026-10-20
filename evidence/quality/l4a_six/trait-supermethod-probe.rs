trait Parent { fn add(&self,rhs:&Self)->Self; }
trait Child:Parent {}
impl Parent for i64 { fn add(&self,rhs:&Self)->Self{self+rhs} }
fn main(){ let _ = Child::add(&1i64,&2i64); }
