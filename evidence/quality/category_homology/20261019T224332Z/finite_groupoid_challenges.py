"""Explicit finite matrix groupoids, independent permutation arithmetic and split pairs."""

ORACLE = r'''
fn multiplication(n:usize)->Vec<Vec<usize>>{
 if n!=6{return (0..n).map(|i|(0..n).map(|j|(i+j)%n).collect()).collect();}
 let p=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
 (0..6).map(|i|(0..6).map(|j|p.iter().position(|k|(0..3).all(|x|k[x]==p[j][p[i][x]])).unwrap()).collect()).collect()
}
fn inverse_element(table:&[Vec<usize>],g:usize)->usize{(0..table.len()).find(|&i|table[g][i]==0&&table[i][g]==0).unwrap()}
fn preferred(n:usize)->usize{match n{6=>3,2=>1,_=>0}}
fn label(ci:usize,x:&str,y:&str,g:usize,n:usize)->String{let rank=match n{6=>[5,1,2,0,3,4][g],2=>[1,0][g],_=>0};format!("r{rank}_c{ci}_{x}>{y}")}
fn build(groups:&[(Vec<&str>,usize)])->(DeclaredFiniteCategory,BTreeMap<String,String>){
 let mut c=DeclaredFiniteCategory::new("matrix groupoids");let mut inv=BTreeMap::new();
 for (ci,(objects,n)) in groups.iter().enumerate(){let table=multiplication(*n);
  for x in objects{for y in objects{for g in 0..*n{let f=label(ci,x,y,g,*n);c.add_morphism(&f,x,y);inv.insert(f,label(ci,y,x,inverse_element(&table,g),*n));}}c.set_identity(x,&label(ci,x,x,0,*n));}
  for x in objects{for y in objects{for z in objects{for g in 0..*n{for h in 0..*n{c.set_composition(&label(ci,x,y,g,*n),&label(ci,y,z,h,*n),&label(ci,x,z,table[g][h],*n));}}}}}
 }(c,inv)
}
#[test] fn all_coordinates_nonabelian_and_disconnected(){
 let groups=vec![(vec!["b","a","d"],6),(vec!["y","c"],2),(vec!["q"],1)];let (c,inv)=build(&groups);assert_eq!(c.morphisms.len(),63);let saved=c.clone();let expected_inv=inv.clone();
 let g=ValidatedFiniteGroupoid::try_new(c,inv).unwrap();assert_eq!(g.category().declared(),&saved);let components=g.components().unwrap();assert_eq!(components.iter().map(|x|x.root.as_str()).collect::<Vec<_>>(),vec!["a","c","q"]);
 let coords=g.matrix_coordinates().unwrap();assert_eq!(coords.len(),63);let mut all_coordinate_values=BTreeSet::new();
 for (ci,(objects,n)) in groups.iter().enumerate(){let root=*objects.iter().min().unwrap();let component=&components[ci];assert_eq!(component.objects,objects.iter().map(|x|x.to_string()).collect());assert_eq!(component.isotropy,(0..*n).map(|h|label(ci,root,root,h,*n)).collect());
  for x in objects{let px=if *x==root{0}else{preferred(*n)};assert_eq!(component.connectors[*x],label(ci,root,x,px,*n));}
  let table=multiplication(*n);
  for x in objects{for y in objects{for a in 0..*n{let name=label(ci,x,y,a,*n);let px=if *x==root{0}else{preferred(*n)};let py=if *y==root{0}else{preferred(*n)};
   let h=table[table[px][a]][inverse_element(&table,py)];let got=&coords[&name];let expected=GroupoidMatrixCoordinate{component_root:root.to_string(),row_object:y.to_string(),column_object:x.to_string(),isotropy_arrow:label(ci,root,root,h,*n)};
   assert_eq!(got,&expected);assert!(all_coordinate_values.insert(got.clone()));assert_eq!(g.inverse(&name),Some(expected_inv[&name].as_str()));
   // Decode each coordinate using inverse(px),h,py, independently of name tables.
   assert_eq!(table[table[inverse_element(&table,px)][h]][py],a);
  }}}
 }
 // All composable pairs preserve the chosen-root group label under multiplication.
 for ((f,h),product) in &saved.compositions{let cf=&coords[f];let ch=&coords[h];let cp=&coords[product];assert_eq!(cf.row_object,ch.column_object);
  let normalized=saved.compose(&cf.isotropy_arrow,&ch.isotropy_arrow).unwrap();assert_eq!(normalized,cp.isotropy_arrow);assert_eq!(cp.row_object,ch.row_object);assert_eq!(cp.column_object,cf.column_object);
 }
 assert_eq!(g.is_connected_thin().unwrap(),false);assert_eq!(g.inverse("unknown"),None);assert_eq!(g.clone(),g);
}
fn split_pair(reverse_first:bool)->(DeclaredFiniteCategory,BTreeMap<String,String>){
 // Relational maps: s picks coordinate0 of B2, r its partial converse; e=s*r.
 let s=if reverse_first{"b_s"}else{"a_s"};let r=if reverse_first{"a_r"}else{"b_r"};let names=[("z_A","A","A"),("z_B","B","B"),(s,"A","B"),(r,"B","A"),("c_e","B","B")];
 let mut c=DeclaredFiniteCategory::new("split pair");for &(f,x,y) in &names{c.add_morphism(f,x,y);}c.set_identity("A","z_A");c.set_identity("B","z_B");
 for &(f,x,y) in &names{for &(g,x2,z) in &names{if y!=x2{continue;}let h=if f=="z_A"||f=="z_B"{g}else if g=="z_A"||g=="z_B"{f}else if x=="A"&&z=="A"{"z_A"}else if x=="A"{s}else if z=="A"{r}else{"c_e"};c.set_composition(f,g,h);}}
 let inv=names.iter().map(|&(f,_,_)|(f.to_string(),if f==s{r}else if f==r{s}else{f}.to_string())).collect();(c,inv)
}
#[test] fn both_inverse_guards_and_admission_context(){
 for reverse_first in [false,true]{let(c,d)=split_pair(reverse_first);let dagger=DaggerStructure::try_new(c.clone(),d.clone()).unwrap();let expected=if reverse_first{"a_r"}else{"a_s"};
  assert!(matches!(ValidatedFiniteGroupoid::try_from_dagger(dagger),Err(GroupoidError::Noninvertible{morphism})if morphism==expected));
  assert!(matches!(ValidatedFiniteGroupoid::try_new(c,d),Err(GroupoidError::Noninvertible{morphism})if morphism==expected));
 }
 let groups=vec![(vec!["z","a"],1)];let(c,d)=build(&groups);let g=ValidatedFiniteGroupoid::try_new(c,d).unwrap();assert!(g.is_connected_thin().unwrap());assert_eq!(g.components().unwrap()[0].root,"a");
 let(c,d)=build(&[(vec!["x"],2)]);assert!(!ValidatedFiniteGroupoid::try_new(c,d).unwrap().is_connected_thin().unwrap());
 let empty=ValidatedFiniteGroupoid::try_new(DeclaredFiniteCategory::new("empty"),BTreeMap::new()).unwrap();assert!(empty.components().unwrap().is_empty());assert!(empty.matrix_coordinates().unwrap().is_empty());assert!(!empty.is_connected_thin().unwrap());
 let mut invalid=DeclaredFiniteCategory::new("invalid");invalid.add_object("x");assert!(matches!(ValidatedFiniteGroupoid::try_new(invalid,BTreeMap::new()),Err(GroupoidError::Dagger(DaggerValidationError::Category(_)))));
 let mut huge=DeclaredFiniteCategory::new("budget");for i in 0..65{huge.add_object(&i.to_string());}assert!(matches!(ValidatedFiniteGroupoid::try_new(huge,BTreeMap::new()),Err(GroupoidError::Dagger(DaggerValidationError::Budget))));
 for error in [GroupoidError::MissingStructure,GroupoidError::Noninvertible{morphism:"λ".into()},GroupoidError::Dagger(DaggerValidationError::Domain)]{assert_eq!(error.to_string(),format!("finite groupoid refused: {error:?}"));assert!(std::error::Error::source(&error).is_none());}
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_groupoid_tests {use super::*;\n'+ORACLE+'\n}\n'
