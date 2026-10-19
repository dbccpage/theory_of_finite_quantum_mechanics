"""Independent finite functor/category admission oracles. AuthorityEffect: None."""
from pathlib import Path

FUNCTOR=r'''
fn cycle(n:usize)->ValidatedFiniteCategory{
 let mut c=crate::finite_category::DeclaredFiniteCategory::new(&format!("C{n}"));for a in 0..n{c.add_morphism(&a.to_string(),"*","*");}c.set_identity("*","0");for a in 0..n{for b in 0..n{c.set_composition(&a.to_string(),&b.to_string(),&((a+b)%n).to_string());}}ValidatedFiniteCategory::try_new(c).unwrap()
}
fn c3c2(values:[usize;3])->DeclaredFiniteFunctor{let mut f=DeclaredFiniteFunctor::new("F","C3","C2");f.map_object("*","*");for (i,v) in values.iter().enumerate(){f.map_morphism(&i.to_string(),&v.to_string());}f}
#[test]fn admission_matches_all_cyclic_maps_and_preserves_owned_endpoints(){
 let c3=cycle(3);let c2=cycle(2);for bits in 0..8{let v=[bits&1,(bits>>1)&1,(bits>>2)&1];let expected=v==[0,0,0];let raw=c3c2(v);let saved=raw.clone();let admitted=ValidatedFiniteFunctor::try_new(raw,c3.clone(),c2.clone());assert_eq!(admitted.is_ok(),expected);if let Ok(f)=admitted{assert_eq!(f.declared(),&saved);assert_eq!(f.source(),&c3);assert_eq!(f.target(),&c2);assert_eq!(f.on_object("*"),Some("*"));for a in ["0","1","2"]{assert_eq!(f.on_morphism(a),Some("0"));}assert_eq!(f.on_object("missing"),None);assert_eq!(f.on_morphism("missing"),None);let mut changed=f.declared().clone();changed.object_map.clear();assert_eq!(f.declared(),&saved);assert_eq!(f,f.clone());}}
 let empty=ValidatedFiniteCategory::try_new(crate::finite_category::DeclaredFiniteCategory::new("empty")).unwrap();assert!(ValidatedFiniteFunctor::try_new(DeclaredFiniteFunctor::new("empty functor","empty","empty"),empty.clone(),empty).is_ok());
}
#[test]fn admission_has_exact_failures_and_precedence_for_every_map_and_binding_boundary(){
 let a=cycle(3);let b=cycle(2);let valid=c3c2([0,0,0]);let attempt=|f|ValidatedFiniteFunctor::try_new(f,a.clone(),b.clone());
 let mut f=valid.clone();f.name=" \t".into();f.source_category="wrong".into();assert_eq!(attempt(f),Err(FunctorAdmissionError::Name));
 for source in [true,false]{let mut f=valid.clone();if source{f.source_category="wrong".into();}else{f.target_category="wrong".into();}assert_eq!(attempt(f),Err(FunctorAdmissionError::CategoryBinding));}
 for extra in [false,true]{let mut f=valid.clone();if extra{f.map_object("extra","*");}else{f.object_map.clear();}assert_eq!(attempt(f),Err(FunctorAdmissionError::MappingDomain{kind:"objects"}));let mut f=valid.clone();if extra{f.map_morphism("extra","0");}else{f.morphism_map.remove("1");}assert_eq!(attempt(f),Err(FunctorAdmissionError::MappingDomain{kind:"morphisms"}));}
 let mut f=valid.clone();f.map_object("*","unknown");assert_eq!(attempt(f),Err(FunctorAdmissionError::UnknownImage{kind:"objects",image:"unknown".into()}));let mut f=valid.clone();f.map_morphism("1","unknown");assert_eq!(attempt(f),Err(FunctorAdmissionError::UnknownImage{kind:"morphisms",image:"unknown".into()}));
 assert_eq!(attempt(c3c2([1,0,0])),Err(FunctorAdmissionError::Identity{object:"*".into()}));assert_eq!(attempt(c3c2([0,1,0])),Err(FunctorAdmissionError::Composition{first:"1".into(),second:"2".into()}));
 let w=crate::finite_category_builder::DeclaredFiniteCategoryBuilder::walking_arrow("W","A","B","f").build_validated().unwrap();for image in ["id_A","id_B"]{let mut f=DeclaredFiniteFunctor::new("bad","W","W");for x in ["A","B"]{f.map_object(x,x);}for x in ["id_A","id_B"]{f.map_morphism(x,x);}f.map_morphism("f",image);assert_eq!(ValidatedFiniteFunctor::try_new(f,w.clone(),w.clone()),Err(FunctorAdmissionError::Boundary{morphism:"f".into()}));}
}
#[test]fn shared_borrowed_lookup_is_exact_for_asymmetric_unicode_and_missing_pairs(){
 let names=["","a","aa","z","é"];let mut table=CompositionTable::new();for (i,a) in names.iter().enumerate(){for (j,b) in names.iter().enumerate(){if (i+2*j)%3==0{table.insert((a.to_string(),b.to_string()),format!("{i}:{j}"));}}}
 let view=CompositionLookup::new(&table);assert_eq!(view.rows.len(),table.len());for a in names.into_iter().chain(["missing"]){for b in names.into_iter().chain(["absent"]){assert_eq!(view.compose(a,b),table.get(&(a.into(),b.into())).map(String::as_str));}}assert_eq!(CompositionLookup::new(&CompositionTable::new()).compose("",""),None);
}
#[test]fn raw_maps_and_legacy_identity_totality_diagnostics_keep_literal_scope(){
 let mut f=DeclaredFiniteFunctor::new("raw","C","D");assert_eq!((f.name.as_str(),f.source_category.as_str(),f.target_category.as_str()),("raw","C","D"));assert!(f.object_map.is_empty()&&f.morphism_map.is_empty());assert_eq!(f.on_object("A"),None);assert_eq!(f.on_morphism("A"),None);f.map_object("A","wrong");f.map_object("A","X");f.map_morphism("m","wrong");f.map_morphism("m","image");assert_eq!(f.on_object("A"),Some("X"));assert_eq!(f.on_morphism("m"),Some("image"));assert_eq!(f.object_map.len(),1);assert_eq!(f.morphism_map.len(),1);
 assert_eq!(check_identity_law(&f),vec!["Identity law: F(id_A) is not defined"]);f.map_morphism("id_A","bad");assert_eq!(check_identity_law(&f),vec!["Identity law violated at A: F(id_A) = bad but expected id_X"]);f.map_morphism("id_A","id_X");assert!(check_identity_law(&f).is_empty());
 assert_eq!(check_object_totality(&f,&["B","A","B"]),vec!["Object totality: B is not mapped by functor raw","Object totality: B is not mapped by functor raw"]);assert_eq!(check_morphism_totality(&f,&["z","m","z"]),vec!["Morphism totality: z is not mapped by functor raw","Morphism totality: z is not mapped by functor raw"]);assert!(check_object_totality(&f,&[]).is_empty());assert!(check_morphism_totality(&f,&[]).is_empty());
 let blank=DeclaredFiniteFunctor::new("","","");assert!(check_identity_law(&blank).is_empty());assert_eq!(f,f.clone());assert!(format!("{:?}",f).contains("raw"));
}
#[test]fn supplied_composition_diagnostics_cover_all_presence_and_result_cases(){
 for present in 0..16{for different in [false,true]{let mut f=DeclaredFiniteFunctor::new("F","C","D");if present&1!=0{f.map_morphism("f","Ff");}if present&2!=0{f.map_morphism("g","Fg");}if present&4!=0{f.map_morphism("gf","Fgf");}let mut table=CompositionTable::new();if present&8!=0{table.insert(("Ff".into(),"Fg".into()),if different{"other"}else{"Fgf"}.into());}
 let expected=if present&1==0{vec!["Composition law: F(f) is not defined"]}else if present&2==0{vec!["Composition law: F(g) is not defined"]}else if present&4==0{vec!["Composition law: F(gf) is not defined"]}else if present&8==0{vec!["Composition law: F(g)∘F(f) = Fg∘Ff not in target composition table"]}else if different{vec!["Composition law violated: F(g∘f) = Fgf but F(g)∘F(f) = other"]}else{vec![]};assert_eq!(check_composition_law(&f,&[("f","g","gf")],&table),expected);assert!(check_composition_law(&f,&[],&table).is_empty());}}
}
#[test]fn supplied_boundaries_cover_all_missing_and_independent_endpoint_failures(){
 for present in 0..16{for wrong in 0..4{let mut f=DeclaredFiniteFunctor::new("F","C","D");if present&1!=0{f.map_morphism("f","Ff");}if present&2!=0{f.map_object("A","X");}if present&4!=0{f.map_object("B","Y");}let mut table=BTreeMap::new();if present&8!=0{table.insert("Ff".into(),(if wrong&1!=0{"badS"}else{"X"}.into(),if wrong&2!=0{"badT"}else{"Y"}.into()));}
 let expected=if present&1==0{vec!["Boundary preservation: F(f) is not defined"]}else if present&2==0{vec!["Boundary preservation: F(A) is not defined"]}else if present&4==0{vec!["Boundary preservation: F(B) is not defined"]}else if present&8==0{vec!["Boundary preservation: target boundary for F(f) = Ff is not defined"]}else{let mut v=vec![];if wrong&1!=0{v.push("Boundary preservation violated for f: src(F(f)) = badS, expected F(src(f)) = X");}if wrong&2!=0{v.push("Boundary preservation violated for f: tgt(F(f)) = badT, expected F(tgt(f)) = Y");}v};assert_eq!(check_boundary_preservation(&f,&[("f","A","B")],&table),expected);assert!(check_boundary_preservation(&f,&[],&table).is_empty());}}
}
'''

VALIDATOR=r'''
fn walking()->DeclaredFiniteCategory{crate::finite_category_builder::DeclaredFiniteCategoryBuilder::walking_arrow("W","A","B","f").build()}
#[test]fn all_unital_three_element_tables_match_numeric_associativity_oracle(){
 for encoded in 0..81{let mut n=encoded;let mut matrix=[[0usize;3];3];for a in 0..3{matrix[0][a]=a;matrix[a][0]=a;}for a in 1..3{for b in 1..3{matrix[a][b]=n%3;n/=3;}}
 let mut expected=true;for a in 0..3{for b in 0..3{for c in 0..3{if matrix[matrix[a][b]][c]!=matrix[a][matrix[b][c]]{expected=false;}}}}
 let mut raw=DeclaredFiniteCategory::new("table");for a in 0..3{raw.add_morphism(&a.to_string(),"*","*");}raw.set_identity("*","0");for a in 0..3{for b in 0..3{raw.set_composition(&a.to_string(),&b.to_string(),&matrix[a][b].to_string());}}
 let saved=raw.clone();let report=validate_finite_category(&raw);assert_eq!(report.all_passed(),expected,"table={encoded}");assert_eq!(check_associativity(&raw).is_empty(),expected);assert_eq!(raw,saved);assert!(check_object_references(&raw).is_empty());assert!(check_nonempty_names(&raw).is_empty());assert!(check_identity_totality(&raw).is_empty());assert!(check_identity_laws(&raw).is_empty());assert!(check_composition_totality(&raw).is_empty());assert!(check_composition_closure(&raw).is_empty());assert!(check_composition_boundaries(&raw).is_empty());
 }
}
#[test]fn exact_typed_unit_severity_and_all_local_reference_refusals(){
 let w=walking();assert!(validate_finite_category(&w).all_passed());let unit=FiniteCategoryValidation::ObjectReference;
 let mut c=w.clone();c.morphisms.get_mut("f").unwrap().name="different".into();let v=check_object_references(&c);assert_eq!(v.len(),1);assert_eq!(v[0].unit,ValidationUnit::FiniteCategory(unit));assert_eq!(v[0].location,ValidationLocation::Morphism("f".into()));assert_eq!(v[0].severity,ValidationSeverity::Error);assert_eq!(v[0].message,"Morphism key f does not match declared name different");
 for source in [true,false]{let mut c=w.clone();if source{c.morphisms.get_mut("f").unwrap().source="unknown".into();}else{c.morphisms.get_mut("f").unwrap().target="unknown".into();}let v=check_object_references(&c);assert_eq!(v.len(),1);assert!(v[0].message.contains(if source{"unknown source"}else{"unknown target"}));}
 let mut c=w.clone();c.identities.insert("unknown".into(),"id_A".into());assert_eq!(check_object_references(&c).len(),1);
 let mut c=w.clone();c.name=" \t".into();c.objects.insert(" ".into());c.morphisms.insert("".into(),crate::finite_category::DeclaredMorphism::new("","A","B"));let v=check_nonempty_names(&c);assert_eq!(v.len(),3);assert_eq!(v[0].message,"Empty category name");assert_eq!(v[1].message,"Empty object name declared");assert_eq!(v[2].message,"Empty morphism name declared");
 let mut c=w.clone();c.identities.remove("A");assert_eq!(check_identity_totality(&c).len(),1);let mut c=w.clone();c.identities.insert("A".into(),"missing".into());assert_eq!(check_identity_totality(&c).len(),1);let mut c=w.clone();c.identities.insert("A".into(),"f".into());assert_eq!(check_identity_totality(&c).len(),1);
}
#[test]fn composition_domain_closure_boundary_and_unit_failures_are_distinct(){
 let w=walking();for key in [("id_A","f"),("f","id_B")]{let mut c=w.clone();c.compositions.remove(&(key.0.into(),key.1.into()));assert_eq!(check_identity_laws(&c).len(),1);assert_eq!(check_composition_totality(&c).len(),1);let v=check_identity_laws(&c);assert_eq!(v[0].unit,ValidationUnit::FiniteCategory(FiniteCategoryValidation::IdentityLaw));}
 let mut c=w.clone();c.set_composition("id_A","f","id_A");assert_eq!(check_identity_laws(&c).len(),1);assert_eq!(check_composition_boundaries(&c).len(),1);
 for (first,second,result) in [("missing","f","f"),("id_A","missing","f"),("id_A","f","missing")]{let mut c=w.clone();c.set_composition(first,second,result);assert_eq!(check_composition_closure(&c).len(),1);assert!(!validate_finite_category(&c).all_passed());}
 let mut c=w.clone();c.set_composition("f","f","f");assert_eq!(check_composition_boundaries(&c).len(),1);let mut c=w.clone();c.set_composition("id_A","f","id_B");assert_eq!(check_composition_boundaries(&c).len(),1);
 let empty=DeclaredFiniteCategory::new("empty");let lookup=CompositionLookup::new(&empty.compositions);assert!(associativity_at(&lookup,"f","g","h").is_some());assert!(validate_finite_category(&empty).all_passed());assert_eq!(validate_finite_category(&w).target_name,"W");assert_eq!(validate_finite_category(&w).results.len(),8);
}
'''

def challenge(subject):
    body=FUNCTOR if Path(subject['path']).stem=='cat_functor' else VALIDATOR
    return '\n#[cfg(test)] mod independent_admission_tests { use super::*;\n'+body+'\n}\n'
