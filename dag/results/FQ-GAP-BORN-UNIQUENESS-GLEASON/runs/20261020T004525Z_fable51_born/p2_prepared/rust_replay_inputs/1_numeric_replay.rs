// Exact, bounded i128 replay of the frozen public 2x2 symmetric matrix wire.
use std::{env,fs};
#[derive(Clone,Copy,Debug,PartialEq,Eq)] struct Q{i:i128,d:i128}
fn gcd(mut a:i128,mut b:i128)->i128{while b!=0{let r=a%b;a=b;b=r;}a.abs()}
impl Q{
 fn new(i:i128,d:i128)->Self{assert!(d!=0,"zero denominator");let s=if d<0{-1}else{1};let g=gcd(i,d);Self{i:i.checked_mul(s).expect("bounded overflow")/g,d:d.checked_mul(s).expect("bounded overflow")/g}}
 fn int(i:i128)->Self{Self::new(i,1)}
 fn parse(s:&str)->Self{let a:Vec<_>=s.split('/').collect();let q=Self::new(a[0].parse().unwrap(),if a.len()==2{a[1].parse().unwrap()}else{1});assert!(a.len()<=2 && q.text()==s,"canonical wire");q}
 fn add(self,b:Self)->Self{Self::new(self.i.checked_mul(b.d).unwrap().checked_add(b.i.checked_mul(self.d).unwrap()).unwrap(),self.d.checked_mul(b.d).unwrap())}
 fn neg(self)->Self{Self::new(self.i.checked_neg().unwrap(),self.d)}
 fn sub(self,b:Self)->Self{self.add(b.neg())}
 fn mul(self,b:Self)->Self{Self::new(self.i.checked_mul(b.i).unwrap(),self.d.checked_mul(b.d).unwrap())}
 fn le(self,b:Self)->bool{self.i.checked_mul(b.d).unwrap()<=b.i.checked_mul(self.d).unwrap()}
 fn text(self)->String{if self.d==1{format!("{}",self.i)}else{format!("{}/{}",self.i,self.d)}}
}
type M=[Q;3];
fn add(a:M,b:M)->M{[a[0].add(b[0]),a[1].add(b[1]),a[2].add(b[2])]}
fn sub(a:M,b:M)->M{[a[0].sub(b[0]),a[1].sub(b[1]),a[2].sub(b[2])]}
fn psd(a:M)->bool{a[0].i>=0 && a[2].i>=0 && a[0].mul(a[2]).sub(a[1].mul(a[1])).i>=0}
fn effect(a:M)->bool{psd(a)&&psd(sub([Q::int(1),Q::int(0),Q::int(1)],a))}
fn trace(a:M,r:M)->Q{a[0].mul(r[0]).add(Q::int(2).mul(a[1]).mul(r[1])).add(a[2].mul(r[2]))}
fn binary(x:Q,y:Q)->Q{assert!(x.i!=0 || y.i!=0);let p=x.mul(y);Q::int(if p.i>0{1}else if p.i<0{0}else if y.i==0{1}else{0})}
fn replay(line:&str)->String{
 let f:Vec<_>=line.split('\t').collect();assert!(f.len()>=12);let a=[Q::parse(f[1]),Q::parse(f[2]),Q::parse(f[3])];let b=[Q::parse(f[4]),Q::parse(f[5]),Q::parse(f[6])];let e=Q::parse(f[7]);assert!(Q::int(0).le(e)&&e.le(Q::int(1)));let u=[e,Q::int(0),e];let d=sub(a,b);
 let (va,vb)=if f[8]=="trace"{assert_eq!(f.len(),12);let rho=[Q::parse(f[9]),Q::parse(f[10]),Q::parse(f[11])];(trace(a,rho),trace(b,rho))}else{assert_eq!(f[8],"binary_ray_restriction");assert_eq!(f.len(),13);(binary(Q::parse(f[9]),Q::parse(f[10])),binary(Q::parse(f[11]),Q::parse(f[12])))};
 let diff=va.sub(vb);format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",f[0],effect(a),effect(b),psd(add(d,u)),psd(sub(u,d)),va.text(),vb.text(),e.neg().le(diff)&&diff.le(e))
}
fn main(){let a:Vec<_>=env::args().collect();assert_eq!(a.len(),2);let s=fs::read_to_string(&a[1]).unwrap();for l in s.lines(){println!("{}",replay(l));}}
#[cfg(test)]mod tests{use super::*;
 #[test]fn exact_normalization(){assert_eq!(Q::new(-6,-8).text(),"3/4");assert_eq!(Q::parse("1/3").add(Q::parse("1/6")).text(),"1/2");}
 #[test]fn determinant_controls(){assert!(psd([Q::int(1),Q::int(1),Q::int(1)]));assert!(!psd([Q::int(1),Q::int(2),Q::int(1)]));assert!(!psd([Q::int(0),Q::int(1),Q::int(1)]));}
 #[test]fn effect_boundary(){assert!(effect([Q::int(1),Q::int(0),Q::int(0)]));assert!(!effect([Q::int(2),Q::int(0),Q::int(0)]));}
 #[test]fn sign_and_axis_ray_controls(){assert_eq!(binary(Q::int(1),Q::int(0)),Q::int(1));assert_eq!(binary(Q::int(2),Q::int(-1)),Q::int(0));assert_eq!(binary(Q::int(0),Q::int(1)),Q::int(0));}
 #[test]#[should_panic]fn denominator_refusal(){Q::new(1,0);}
 #[test]#[should_panic]fn noncanonical_refusal(){Q::parse("2/4");}
 #[test]#[should_panic]fn zero_ray_refusal(){binary(Q::int(0),Q::int(0));}
 #[test]#[should_panic]fn overflow_refusal(){Q::int(i128::MAX).mul(Q::int(2));}
}