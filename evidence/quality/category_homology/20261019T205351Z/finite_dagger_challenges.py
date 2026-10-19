"""Exact finite relations, two inverse equations and phase-specific refusals."""

ORACLE = r'''
fn tag(error:DaggerValidationError)->String{match error{
 DaggerValidationError::Budget=>"budget".into(),DaggerValidationError::Category(r)=>{assert!(!r.all_passed());"category".into()},DaggerValidationError::Domain=>"domain".into(),
 DaggerValidationError::MissingImage{morphism}=>format!("missing:{morphism}"),DaggerValidationError::Boundary{morphism}=>format!("boundary:{morphism}"),DaggerValidationError::Involution{morphism}=>format!("involution:{morphism}"),DaggerValidationError::Identity{object}=>format!("identity:{object}"),DaggerValidationError::Composition{first,second}=>format!("composition:{first}:{second}")}}
fn refuse(c:DeclaredFiniteCategory,d:BTreeMap<String,String>)->String{tag(DaggerStructure::try_new(c,d).unwrap_err())}
fn cyclic(n:usize)->(DeclaredFiniteCategory,BTreeMap<String,String>){let mut c=DeclaredFiniteCategory::new("C");for i in 0..n{c.add_morphism(&format!("p{i}"),"*","*");}c.set_identity("*","p0");for i in 0..n{for j in 0..n{c.set_composition(&format!("p{i}"),&format!("p{j}"),&format!("p{}",(i+j)%n));}}let d=(0..n).map(|i|(format!("p{i}"),format!("p{}",(n-i)%n))).collect();(c,d)}
fn relation_name(a:usize,b:usize,bits:usize)->String{format!("{a}{b}:{bits:02}")}
fn relations()->(DeclaredFiniteCategory,BTreeMap<String,String>,Vec<(usize,usize,usize)>){
 let mut c=DeclaredFiniteCategory::new("finite relations on1,2");let mut rows=Vec::new();let mut d=BTreeMap::new();
 for a in 1..=2{for b in 1..=2{for bits in 0..(1usize<<(a*b)){let name=relation_name(a,b,bits);c.add_morphism(&name,&a.to_string(),&b.to_string());rows.push((a,b,bits));
  let converse=(0..a).flat_map(|i|(0..b).map(move|j|(i,j))).fold(0,|v,(i,j)|v|(((bits>>(i*b+j))&1)<<(j*a+i)));d.insert(name,relation_name(b,a,converse));}}}
 for a in 1..=2{let id=(0..a).fold(0,|v,i|v|(1<<(i*a+i)));c.set_identity(&a.to_string(),&relation_name(a,a,id));}
 // Relational join is stated independently as Boolean existential membership.
 for &(a,b,f) in &rows{for &(b2,z,g) in &rows{if b!=b2{continue;}let mut product=0;for i in 0..a{for j in 0..z{let paths:Vec<_>=(0..b).filter(|&k|f&(1<<(i*b+k))!=0&&g&(1<<(k*z+j))!=0).collect();if !paths.is_empty(){product|=1<<(i*z+j);}}}c.set_composition(&relation_name(a,b,f),&relation_name(b,z,g),&relation_name(a,z,product));}}
 (c,d,rows)
}
#[test] fn concrete_relations_and_both_inverse_equations(){
 let (c,d,rows)=relations();let expected=c.clone();let saved=d.clone();let x=DaggerStructure::try_new(c,d).unwrap();assert_eq!(x.category().declared(),&expected);
 for (a,b,bits) in rows{let name=relation_name(a,b,bits);assert_eq!(x.dagger(&name),Some(saved[&name].as_str()));
  let rows_one=(0..a).all(|i|(0..b).filter(|&j|bits&(1<<(i*b+j))!=0).count()==1);let cols_one=(0..b).all(|j|(0..a).filter(|&i|bits&(1<<(i*b+j))!=0).count()==1);
  assert_eq!(x.is_unitary(&name),Some(a==b&&rows_one&&cols_one));assert_eq!(x.dagger(x.dagger(&name).unwrap()),Some(name.as_str()));
 }
 // A1->B2 injection has only the source round trip; its converse only the target.
 assert_eq!(x.is_unitary("12:01"),Some(false));assert_eq!(x.is_unitary("21:01"),Some(false));
 assert_eq!(x.is_unitary("unknown"),None);assert_eq!(x.dagger("unknown"),None);assert_eq!(x.clone(),x);
 let (empty,d)= (DeclaredFiniteCategory::new("empty"),BTreeMap::new());let e=DaggerStructure::try_new(empty,d).unwrap();assert_eq!(e.is_unitary(""),None);assert!(e.category().declared().objects.is_empty());
}
#[test] fn exact_phase_refusals(){
 let mut invalid=DeclaredFiniteCategory::new("invalid");invalid.add_object("A");assert_eq!(refuse(invalid,BTreeMap::new()),"category");
 let (c,d)=cyclic(3);let mut bad=d.clone();bad.remove("p1");assert_eq!(refuse(c.clone(),bad),"domain");let mut bad=d.clone();bad.remove("p1");bad.insert("extra".into(),"p0".into());assert_eq!(refuse(c.clone(),bad),"domain");
 let mut bad=d.clone();bad.insert("p0".into(),"missing".into());assert_eq!(refuse(c.clone(),bad),"missing:p0");
 let mut bad=d.clone();bad.insert("p2".into(),"p2".into());assert_eq!(refuse(c.clone(),bad),"involution:p1");
 let (c2,mut d2)=cyclic(2);d2.insert("p0".into(),"p1".into());d2.insert("p1".into(),"p0".into());assert_eq!(refuse(c2,d2),"identity:*");
 let mut walk=DeclaredFiniteCategory::new("walking");walk.add_identity("A","eA");walk.add_identity("B","eB");walk.add_morphism("f","A","B");for(f,g,h)in[("eA","eA","eA"),("eB","eB","eB"),("eA","f","f"),("f","eB","f")]{walk.set_composition(f,g,h);}
 let identity:BTreeMap<String,String>=["eA","eB","f"].into_iter().map(|f|(f.into(),f.into())).collect();
 assert_eq!(refuse(walk.clone(),identity.clone()),"boundary:f");
 let mut source_only=identity.clone();source_only.insert("eB".into(),"f".into());source_only.insert("f".into(),"eB".into());assert_eq!(refuse(walk.clone(),source_only),"boundary:eB");
 let mut target_only=identity;target_only.insert("eA".into(),"f".into());target_only.insert("f".into(),"eA".into());assert_eq!(refuse(walk,target_only),"boundary:eA");
 // Adjoined identity plus two left-zero elements: associative, noncommutative.
 let names=["e","a","b"];let mut left=DeclaredFiniteCategory::new("left zero with unit");for f in names{left.add_morphism(f,"*","*");}left.set_identity("*","e");for f in names{for g in names{let h=if f=="e"{g}else{f};left.set_composition(f,g,h);}}
 let identity=names.into_iter().map(|f|(f.into(),f.into())).collect();assert_eq!(refuse(left,identity),"composition:a:b");
 for error in [DaggerValidationError::Budget,DaggerValidationError::Domain,DaggerValidationError::MissingImage{morphism:"λ".into()},DaggerValidationError::Boundary{morphism:"f".into()},DaggerValidationError::Involution{morphism:"f".into()},DaggerValidationError::Identity{object:"A".into()},DaggerValidationError::Composition{first:"f".into(),second:"g".into()}]{let text=error.to_string();assert_eq!(text,format!("finite dagger validation refused: {error:?}"));assert!(std::error::Error::source(&error).is_none());}
}
#[test] fn budget_boundaries_precede_category_or_map(){
 for field in 0..3{let mut c=DeclaredFiniteCategory::new("budget");let boundary=if field==2{4096}else{64};
  for i in 0..boundary{match field{0=>{c.add_object(&format!("o{i}"));},1=>c.add_morphism(&format!("f{i}"),"A","A"),_=>c.set_composition(&format!("f{i}"),"g","h")}}
  assert!(admit_dagger_budget(&c).is_ok());
  match field{0=>{c.add_object("overflow");},1=>c.add_morphism("overflow","A","A"),_=>c.set_composition("overflow","g","h")}
  assert_eq!(tag(admit_dagger_budget(&c).unwrap_err()),"budget");assert_eq!(refuse(c,BTreeMap::new()),"budget");
 }
 let mut c=DeclaredFiniteCategory::new("discrete64");let mut d=BTreeMap::new();for i in 0..64{let o=format!("o{i}");let f=format!("e{i}");c.add_identity(&o,&f);c.set_composition(&f,&f,&f);d.insert(f.clone(),f);}assert!(DaggerStructure::try_new(c,d).is_ok());
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_dagger_tests {use super::*;\n'+ORACLE+'\n}\n'
