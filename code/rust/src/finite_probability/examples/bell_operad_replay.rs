//! Replays the P0 public laws as exact rationals, emitting TSV for independent comparison.
//! Generated from the retained P0 inputs, with no expected certificate values.
use tfqm_finite_probability::bell_joint_extension::{certify_joint_law,verify_joint_certificate,joint_expectation,response_products,chsh_linear};
use num_bigint::BigInt;
use num_rational::BigRational as Q;
fn parse(s:&str)->Q { let (n,d)=s.split_once('/').unwrap_or((s,"1"));Q::new(n.parse::<BigInt>().unwrap(),d.parse::<BigInt>().unwrap()) }
fn emit(id:&str,raw:&[&str]) {
    let law:Vec<Q>=raw.iter().map(|s|parse(s)).collect();
    let c=certify_joint_law(&law).unwrap();verify_joint_certificate(&law,&c).unwrap();
    let table:Vec<[Q;4]>=response_products().iter().map(|r|r.map(|x|Q::from_integer(x.into()))).collect();
    assert_eq!(joint_expectation(&law,&table).unwrap(),c.correlators);
    assert_eq!(chsh_linear(&c.correlators).unwrap(),c.chsh);
    print!("{}",id);for x in c.correlators {print!("\t{}",x);}
    for x in [c.chsh,c.positive_score_mass,c.negative_score_mass,c.lower_slack,c.upper_slack] {print!("\t{}",x);}
    println!();
}
fn main(){
    emit("vertex_0", &["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_1", &["0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_2", &["0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_3", &["0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_4", &["0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_5", &["0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_6", &["0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_7", &["0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_8", &["0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_9", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0"]);
    emit("vertex_10", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0"]);
    emit("vertex_11", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0"]);
    emit("vertex_12", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0"]);
    emit("vertex_13", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0"]);
    emit("vertex_14", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0"]);
    emit("vertex_15", &["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1"]);
    emit("uniform", &["1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16", "1/16"]);
    emit("asymmetric", &["1/136", "1/68", "3/136", "1/34", "5/136", "3/68", "7/136", "1/17", "9/136", "5/68", "11/136", "3/34", "13/136", "7/68", "15/136", "2/17"]);
    emit("mixture_0_1", &["1/7", "6/7", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
    emit("mixture_3_10", &["0", "0", "0", "2/5", "0", "0", "0", "0", "0", "0", "3/5", "0", "0", "0", "0", "0"]);
    emit("mixture_5_14", &["0", "0", "0", "0", "0", "11/13", "0", "0", "0", "0", "0", "0", "0", "0", "2/13", "0"]);
    emit("large_denominator", &["10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003", "1/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]);
}
