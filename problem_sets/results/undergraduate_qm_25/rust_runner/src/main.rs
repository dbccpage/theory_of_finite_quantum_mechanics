// Generated from solution YAML by ../verify.py; edit the YAML, then rerun.
#![allow(dead_code, unused_imports)]
#[path = "../../../../../code/rust/src/linear_algebra/scalars.rs"]
mod scalars;
mod problem_01 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let a = G::from_integers(1,1); let b = G::from_integers(2,0);
    let total = a.norm_sq()+b.norm_sq();
    let p0 = a.norm_sq()/&total; let p1 = b.norm_sq()/&total;
    let mean = q(3)*&p1; let variance = q(9)*&p1-&mean*&mean;
    let ret = (&p0-&p1)*(&p0-&p1);
    json!({"p0":p0.to_string(),"p1":p1.to_string(),"mean_over_epsilon":mean.to_string(),
        "variance_over_epsilon2":variance.to_string(),"return_at_pi":ret.to_string()})
}

}
mod problem_02 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let hbar=q(1); let m=q(1); let sigma=q(1); let k0=qr(3,2).unwrap(); let t=q(2);
    let vp=&hbar*&hbar/(q(4)*&sigma*&sigma);
    let vx=&sigma*&sigma+&t*&t*&vp/(&m*&m);
    json!({"mean_x":(&hbar*&k0*&t/&m).to_string(),"mean_p":(&hbar*&k0).to_string(),
        "variance_x":vx.to_string(),"variance_p":vp.to_string(),"uncertainty_product_squared":(&vx*&vp).to_string()})
}

}
mod problem_03 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let d=[[q(2),q(-1),q(0)],[q(-1),q(2),q(-1)],[q(0),q(-1),q(2)]];
    let v=[q(1),q(0),q(-1)]; let mut residual=q(0);
    for i in 0..3 { let mut value=q(0); for j in 0..3 {value += &d[i][j]*&v[j];}
        let delta=value-q(2)*&v[i]; residual += &delta*&delta; }
    let det=&d[0][0]*(&d[1][1]*&d[2][2]-&d[1][2]*&d[2][1])-&d[0][1]*(&d[1][0]*&d[2][2]);
    let trace=&d[0][0]+&d[1][1]+&d[2][2];
    json!({"trace":trace.to_string(),"determinant":det.to_string(),"middle_mode_residual":residual.to_string(),
        "ground_probability_constant":qr(1,2).unwrap().to_string(),"inverse_pi_coefficient":q(1).to_string()})
}

}
mod problem_04 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let cross=q(-2)*(q(1)-qr(1,9).unwrap());
    json!({"x12_pi2_over_L":cross.to_string(),"gap_over_E1":(q(4)-q(1)).to_string(),
        "p_E1":qr(1,2).unwrap().to_string(),"p_E2":qr(1,2).unwrap().to_string()})
}

}
mod problem_05 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let z=qr(1,4).unwrap(); let y=qr(1,4).unwrap(); let p2=&z*&z+&y*&y;
    json!({"p2_over_pi2":p2.to_string(),"energy_fraction":(&z*&z/&p2).to_string(),
        "matching_coefficient_residual":(&z-&y).to_string()})
}

}
mod problem_06 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let kl=q(2); let kr=q(1); let r=(&kl-&kr)/(&kl+&kr); let t=q(2)*&kl/(&kl+&kr);
    let refl=&r*&r; let trans=&kr/&kl*&t*&t;
    json!({"r":r.to_string(),"t":t.to_string(),"R":refl.to_string(),"T":trans.to_string(),
        "flux":(&refl+&trans).to_string(),"value_residual":(q(1)+&r-&t).to_string(),
        "derivative_residual":(&kl*(q(1)-&r)-&kr*&t).to_string()})
}

}
mod problem_07 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let c=qr(5,4).unwrap(); let s=qr(3,4).unwrap();
    let a=G::new(c.clone(),q(0)).unwrap(); let b=G::new(q(0),-&s).unwrap();
    let cc=G::new(q(0),s.clone()).unwrap();
    let off=a.try_conj().unwrap().try_mul(&b).unwrap().try_sub(&cc.try_conj().unwrap().try_mul(&a).unwrap()).unwrap();
    let diag=&c*&c-&s*&s-q(1);
    let residual=q(2)*&diag*&diag+q(2)*off.norm_sq();
    let t=q(1)/(&c*&c); let r=&s*&s/(&c*&c);
    json!({"T":t.to_string(),"R":r.to_string(),"flux":(&t+&r).to_string(),"metric_residual":residual.to_string()})
}

}
mod problem_08 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let m=q(1); let hbar=q(1); let g=q(2); let k=&m*&g/(&hbar*&hbar);
    let energy=-&hbar*&hbar*&k*&k/(q(2)*&m);
    json!({"kappa":k.to_string(),"energy":energy.to_string(),"amplitude_squared":k.to_string(),
        "jump_residual_over_A":(q(-2)*&k+q(2)*&m*&g/(&hbar*&hbar)).to_string(),"normalization":(&k/&k).to_string()})
}

}
mod problem_09 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let n=[q(0),q(1),q(2),q(3)]; let aa=[q(1),q(2),q(3),q(0)];
    let comm:Vec<_>=(0..4).map(|i|&aa[i]-&n[i]).collect();
    let trace=comm.iter().fold(q(0),|s,x|s+x);
    json!({"interior_commutator":comm[0].to_string(),"top_commutator":comm[3].to_string(),
        "commutator_trace":trace.to_string(),"projected_top_energy":(&n[3]+qr(1,2).unwrap()).to_string(),
        "symmetrized_top_energy":((&aa[3]+&n[3])/q(2)).to_string()})
}

}
mod problem_10 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let lam=qr(1,10).unwrap(); let shifts:Vec<_>=(0_i64..2).map(|n| {
        let moment=q(n*(n-1)+(2*n+1)*(2*n+1)+(n+1)*(n+2));
        &lam*qr(1,4).unwrap()*moment }).collect();
    json!({"shift_0":shifts[0].to_string(),"shift_1":shifts[1].to_string(),
        "energy_0_first_order":(qr(1,2).unwrap()+&shifts[0]).to_string(),
        "energy_1_first_order":(qr(3,2).unwrap()+&shifts[1]).to_string()})
}

}
mod problem_11 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let p=qr(1,2).unwrap(); let l1=q(2); let l2=q(-2);
    let mean=&p*&l1+&p*&l2; let second=&p*&l1*&l1+&p*&l2*&l2;
    json!({"p_plus":p.to_string(),"p_minus":p.to_string(),"mean_L_over_hbar":mean.to_string(),
        "variance_L_over_hbar2":(&second-&mean*&mean).to_string(),"energy_over_unit":second.to_string()})
}

}
mod problem_12 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let e1=-qr(1,2).unwrap(); let e2=-qr(1,8).unwrap(); let e3=-qr(1,18).unwrap();
    let count:i64=(0_i64..3).map(|l|2*l+1).sum();
    json!({"E1_over_Hartree":e1.to_string(),"E2_over_Hartree":e2.to_string(),"E3_over_Hartree":e3.to_string(),
        "photon_over_Hartree":(&e2-&e1).to_string(),"n3_spatial_degeneracy":q(count).to_string()})
}

}
mod problem_13 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let v0=q(1); let v2=q(1); let norm=&v0*&v0+&v2*&v2;
    let vx=(&v0+&v2)*(&v0+&v2)/(q(2)*&norm);
    let vy=(&v0-&v2)*(&v0-&v2)/(q(2)*&norm); let vz=(&v0*&v0+&v2*&v2)/&norm;
    json!({"var_x_over_hbar2":vx.to_string(),"var_y_over_hbar2":vy.to_string(),"var_z_over_hbar2":vz.to_string(),
        "casimir_over_hbar2":(&vx+&vy+&vz).to_string(),"p_x_zero":vy.to_string()})
}

}
mod problem_14 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let a=G::new(qr(3,5).unwrap(),q(0)).unwrap(); let b=G::new(q(0),qr(4,5).unwrap()).unwrap();
    let cross=a.try_conj().unwrap().try_mul(&b).unwrap();
    let x=q(2)*cross.real(); let y=q(2)*cross.imag(); let z=a.norm_sq()-b.norm_sq();
    let vx=(q(1)-&x*&x)/q(4); let vy=(q(1)-&y*&y)/q(4); let vz=(q(1)-&z*&z)/q(4);
    json!({"bloch_x":x.to_string(),"bloch_y":y.to_string(),"bloch_z":z.to_string(),"p_plus_y":((q(1)+&y)/q(2)).to_string(),
        "var_x":vx.to_string(),"var_y":vy.to_string(),"var_z":vz.to_string(),"robertson_residual":(&vx*&vy-&z*&z/q(16)).to_string()})
}

}
mod problem_15 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let input=[q(1),q(0)]; let mid=[(&input[0]+&input[1])/q(2),(&input[0]+&input[1])/q(2)];
    let passed=&mid[0]*&mid[0]+&mid[1]*&mid[1]; let joint=&mid[1]*&mid[1];
    json!({"direct":(&input[1]*&input[1]).to_string(),"pass_x":passed.to_string(),
        "joint":joint.to_string(),"conditional_minus_z":(&joint/&passed).to_string()})
}

}
mod problem_16 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let phase=G::new(qr(3,5).unwrap(),qr(4,5).unwrap()).unwrap();
    let amp=G::from_integers(1,0).try_add(&phase).unwrap().try_div(&G::from_integers(2,0)).unwrap();
    json!({"phase_norm":phase.norm_sq().to_string(),"bloch_x":phase.real().to_string(),"bloch_y":phase.imag().to_string(),
        "p_plus_x":amp.norm_sq().to_string(),"p_minus_x":(q(1)-amp.norm_sq()).to_string(),"mean_Sy_over_hbar":(phase.imag()/q(2)).to_string()})
}

}
mod problem_17 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let tau=qr(3,4).unwrap(); let den=q(1)+&tau*&tau;
    let c=(q(1)-&tau*&tau)/&den; let s=q(2)*&tau/&den;
    let flip=G::new(q(0),-&s).unwrap().norm_sq(); let survive=G::new(c.clone(),q(0)).unwrap().norm_sq();
    json!({"c":c.to_string(),"s":s.to_string(),"flip":flip.to_string(),"survive":survive.to_string(),"total":(&flip+&survive).to_string()})
}

}
mod problem_18 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let a=qr(1,2).unwrap(); let b=-&a;
    let d0=&a*&a+&b*&b-&a; let d1=&a*&b+&b*&a-&b;
    let residual=q(2)*&d0*&d0+q(2)*&d1*&d1; let tr=q(2)*&a;
    json!({"singlet_E_over_J":((q(0)-qr(3,2).unwrap())/q(2)).to_string(),
        "triplet_E_over_J":((q(2)-qr(3,2).unwrap())/q(2)).to_string(),"singlet_trace":tr.to_string(),
        "triplet_trace":(q(4)-&tr).to_string(),"idempotence_residual":residual.to_string()})
}

}
mod problem_19 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let e1=q(1); let e2=q(4); let a=G::from_integers(1,0); let b=G::from_integers(-1,0);
    let norm=a.norm_sq()+b.norm_sq(); let coincidence=a.try_add(&b).unwrap().norm_sq()/&norm;
    json!({"boson_energy_over_E1":(q(2)*&e1).to_string(),"fermion_energy_over_E1":(&e1+&e2).to_string(),
        "energy_gap_over_E1":(&e2-&e1).to_string(),"determinant_norm_squared":norm.to_string(),"coincidence_factor":coincidence.to_string()})
}

}
mod problem_20 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let lam=qr(1,2).unwrap(); let low=q(1)-&lam*&lam/q(2); let high=q(3)+&lam*&lam/q(2);
    let residual=(q(1)-&low)*(q(3)-&low)-&lam*&lam;
    json!({"low_second_order":low.to_string(),"high_second_order":high.to_string(),"trace":(&low+&high).to_string(),
        "characteristic_residual":residual.to_string(),"first_order_mixing":(-&lam/q(2)).to_string()})
}

}
mod problem_21 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let e0=qr(-1,8).unwrap(); let w=qr(3,10).unwrap(); let low=&e0-&w; let high=&e0+&w;
    let mut residual=q(0);
    for (v,e) in [([q(1),q(1)],low.clone()),([q(1),q(-1)],high.clone())] {
        let d0=&e0*&v[0]-&w*&v[1]-&e*&v[0]; let d1=-&w*&v[0]+&e0*&v[1]-&e*&v[1];
        residual += &d0*&d0+&d1*&d1;
    }
    json!({"lower":low.to_string(),"upper":high.to_string(),"splitting":(&high-&low).to_string(),"eigenvector_residual":residual.to_string()})
}

}
mod problem_22 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let a=qr(3,4).unwrap(); let kinetic=&a*&a/q(2); let potential=-&a; let energy=&kinetic+&potential;
    let gap=&energy+qr(1,2).unwrap(); let delta=&a-q(1);
    json!({"kinetic":kinetic.to_string(),"potential":potential.to_string(),"trial_energy":energy.to_string(),
        "gap":gap.to_string(),"square_completion_residual":(&gap-&delta*&delta/q(2)).to_string(),"optimal_energy":(qr(1,2).unwrap()-q(1)).to_string()})
}

}
mod problem_23 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let n1=1_i64; let n3=3_i64;
    let p1=qr(32,(4-n1*n1)*(4-n1*n1)).unwrap(); let p3=qr(32,(4-n3*n3)*(4-n3*n3)).unwrap();
    json!({"p1_times_pi2":p1.to_string(),"p2":qr(1,2).unwrap().to_string(),"p3_times_pi2":p3.to_string(),
        "p4":q(0).to_string(),"new_ground_over_old_ground":qr(1,4).unwrap().to_string(),"mean_energy_over_old_ground":q(1).to_string()})
}

}
mod problem_24 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let v=[q(1),q(0),q(0),q(1)]; let norm=v.iter().fold(q(0),|s,x|s+x*x);
    let rho:Vec<Vec<_>>=v.iter().map(|a|v.iter().map(|b|a*b/&norm).collect()).collect();
    let red:Vec<Vec<_>>=(0..2).map(|a|(0..2).map(|c|(0..2).fold(q(0),|s,b|s+&rho[2*a+b][2*c+b])).collect()).collect();
    let mut global=q(0); let mut local=q(0);
    for i in 0..4 {for j in 0..4 {global += &rho[i][j]*&rho[j][i];}}
    for i in 0..2 {for j in 0..2 {local += &red[i][j]*&red[j][i];}}
    let xx=&rho[0][3]+&rho[1][2]+&rho[2][1]+&rho[3][0];
    let yy=-&rho[0][3]+&rho[1][2]+&rho[2][1]-&rho[3][0];
    let zz=&rho[0][0]-&rho[1][1]-&rho[2][2]+&rho[3][3];
    json!({"local_00":red[0][0].to_string(),"local_01":red[0][1].to_string(),"global_purity":global.to_string(),
        "local_purity":local.to_string(),"XX":xx.to_string(),"YY":yy.to_string(),"ZZ":zz.to_string()})
}

}
mod problem_25 {
use crate::scalars::{q, qr, GaussianRational as G, Semiring, Ring, Field, Involution};
use serde_json::{json, Value};
pub fn solve() -> Value {
    let phase=G::new(qr(3,5).unwrap(),qr(4,5).unwrap()).unwrap(); let one=G::from_integers(1,0); let two=G::from_integers(2,0);
    let a0=one.try_add(&phase).unwrap().try_div(&two).unwrap(); let a1=one.try_sub(&phase).unwrap().try_div(&two).unwrap();
    let p0=a0.norm_sq(); let p1=a1.norm_sq(); let half=qr(1,2).unwrap(); let dephased=&half*&half+&half*&half;
    json!({"phase_norm":phase.norm_sq().to_string(),"coherent_p0":p0.to_string(),"coherent_p1":p1.to_string(),
        "total":(&p0+&p1).to_string(),"dephased_p0":dephased.to_string(),"dephased_p1":dephased.to_string()})
}

}
fn main() {
let mut outputs = serde_json::Map::new();
outputs.insert("UQM-01".into(), problem_01::solve());
outputs.insert("UQM-02".into(), problem_02::solve());
outputs.insert("UQM-03".into(), problem_03::solve());
outputs.insert("UQM-04".into(), problem_04::solve());
outputs.insert("UQM-05".into(), problem_05::solve());
outputs.insert("UQM-06".into(), problem_06::solve());
outputs.insert("UQM-07".into(), problem_07::solve());
outputs.insert("UQM-08".into(), problem_08::solve());
outputs.insert("UQM-09".into(), problem_09::solve());
outputs.insert("UQM-10".into(), problem_10::solve());
outputs.insert("UQM-11".into(), problem_11::solve());
outputs.insert("UQM-12".into(), problem_12::solve());
outputs.insert("UQM-13".into(), problem_13::solve());
outputs.insert("UQM-14".into(), problem_14::solve());
outputs.insert("UQM-15".into(), problem_15::solve());
outputs.insert("UQM-16".into(), problem_16::solve());
outputs.insert("UQM-17".into(), problem_17::solve());
outputs.insert("UQM-18".into(), problem_18::solve());
outputs.insert("UQM-19".into(), problem_19::solve());
outputs.insert("UQM-20".into(), problem_20::solve());
outputs.insert("UQM-21".into(), problem_21::solve());
outputs.insert("UQM-22".into(), problem_22::solve());
outputs.insert("UQM-23".into(), problem_23::solve());
outputs.insert("UQM-24".into(), problem_24::solve());
outputs.insert("UQM-25".into(), problem_25::solve());
println!("{}", serde_json::to_string_pretty(&outputs).unwrap());
}
