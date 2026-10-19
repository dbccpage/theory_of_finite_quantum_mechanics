//! Read public pair inputs from stdin TSV; emit actual exact native decisions.
use std::io::{self,BufRead};
use num_bigint::BigInt;
use num_rational::BigRational as Q;
use tfqm_finite_probability::bell_separator_extension::{PairData,construct_extension};
fn parse(s:&str)->Q{let(n,d)=s.split_once('/').unwrap_or((s,"1"));Q::new(n.parse::<BigInt>().unwrap(),d.parse::<BigInt>().unwrap())}
fn main(){for line in io::stdin().lock().lines(){
    let line=line.unwrap();let fields:Vec<&str>=line.split('\t').collect();assert_eq!(fields.len(),17);
    let p:PairData=std::array::from_fn(|j|std::array::from_fn(|k|parse(fields[1+4*j+k])));
    let a=construct_extension(&p).unwrap();let status=if a.weights.is_some(){"extended"}else{"blocked"};print!("{}\t{}",fields[0],status);
    for q in a.analysis.lower.iter().chain(&a.analysis.upper).chain(&a.analysis.facets){print!("\t{}",q);}
    if let Some(weights)=a.weights {print!("\t{}",a.separator.unwrap());for t in a.triples.unwrap(){for q in t {print!("\t{}",q);}}for q in weights {print!("\t{}",q);}}
    else {print!("\t{}",a.violating_mask.unwrap());}
    println!();
}}
