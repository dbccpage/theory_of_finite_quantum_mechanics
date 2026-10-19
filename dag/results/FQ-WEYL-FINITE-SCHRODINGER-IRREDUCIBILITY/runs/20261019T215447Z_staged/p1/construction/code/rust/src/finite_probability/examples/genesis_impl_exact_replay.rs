use std::io::{self,BufRead};
fn main(){for line in io::stdin().lock().lines(){let line=line.unwrap();let mut parts=line.split("\t");let kind=parts.next().unwrap();let values=parts.map(String::from).collect::<Vec<_>>();let out=tfqm_finite_probability::genesis_impl_exact::evaluate(kind,&values);println!("{}\t{}",kind,out.join("\t"));}}
