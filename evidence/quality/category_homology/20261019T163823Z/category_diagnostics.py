"""Independent metadata inventory and callback observation challenges.

AuthorityEffect: None. No diagnostic label is a mathematical certificate;
callback purity, termination, Clone laws and external effects are not assumed.
"""
from pathlib import Path

VALIDATION=r'''
fn issue(message:&str,severity:ValidationSeverity)->ValidationViolation{
 ValidationViolation::new(ValidationUnit::FiniteCategory(FiniteCategoryValidation::IdentityLaw),ValidationLocation::Object("object".into()),message,severity)
}
#[test]fn fields_and_report_flags_are_literal(){
 for name in [""," ","\0λ"]{
  let mut r=ValidationReport::new(name);assert_eq!(r.target_name,name);assert!(r.results.is_empty());assert!(r.typed_violations.is_empty());assert!(r.all_passed());assert_eq!(r.failure_count(),0);assert_eq!(r.violation_count(),0);
  let p=ValidationResult::pass(name);assert_eq!(p.unit,name);assert!(p.passed);assert!(p.violations.is_empty());r.add(p);
  let f=ValidationResult::fail(name,vec!["".into(),"raw".into()]);assert_eq!(f.unit,name);assert!(!f.passed);assert_eq!(f.violations,["","raw"]);r.add(f);assert_eq!(r.results.len(),2);assert!(!r.all_passed());assert_eq!(r.failure_count(),1);
 }
 for bits in 0..8usize{for typed in [false,true]{let results=(0..3).map(|i|ValidationResult{unit:i.to_string(),passed:bits&(1<<i)!=0,violations:vec!["untrusted message".into()]}).collect();let r=ValidationReport{target_name:"caller data".into(),results,typed_violations:if typed{vec![issue("typed",ValidationSeverity::Info)]}else{vec![]}};
  assert_eq!(r.all_passed(),bits==7&&!typed);assert_eq!(r.failure_count(),3-bits.count_ones() as usize);assert_eq!(r.violation_count(),usize::from(typed));
 }}
}
#[test]fn typed_projection_preserves_order_and_every_severity(){
 for severity in [ValidationSeverity::Error,ValidationSeverity::Warning,ValidationSeverity::Info]{
  let v=issue(" \0λ",severity);assert_eq!(v.unit,ValidationUnit::FiniteCategory(FiniteCategoryValidation::IdentityLaw));assert_eq!(v.location,ValidationLocation::Object("object".into()));assert_eq!(v.message," \0λ");assert_eq!(v.severity,severity);
  let mut r=ValidationReport::new("R");r.add_violation(v.clone());assert_eq!(r.results.len(),1);assert_eq!(r.results[0].unit,"FiniteCategory(IdentityLaw)");assert!(!r.results[0].passed);assert_eq!(r.results[0].violations,[" \0λ"]);assert_eq!(r.typed_violations,[v]);assert!(!r.all_passed());assert_eq!((r.failure_count(),r.violation_count()),(1,1));
 }
 let mut r=ValidationReport::new("R");r.add_typed("empty",vec![]);assert_eq!(r.results[0].unit,"empty");assert!(r.results[0].passed);assert!(r.results[0].violations.is_empty());assert!(r.typed_violations.is_empty());assert!(r.all_passed());
 let vs=vec![issue("first",ValidationSeverity::Warning),issue("",ValidationSeverity::Info),issue("last",ValidationSeverity::Error)];r.add_typed("batch",vs.clone());assert_eq!(r.results.len(),2);assert_eq!(r.results[1].unit,"batch");assert!(!r.results[1].passed);assert_eq!(r.results[1].violations,["first","","last"]);assert_eq!(r.typed_violations,vs);assert_eq!((r.failure_count(),r.violation_count()),(1,3));assert!(!r.all_passed());
 let mut clone=r.clone();clone.target_name.clear();clone.typed_violations.clear();clone.results.clear();assert_eq!(r.target_name,"R");assert_eq!(r.results.len(),2);assert_eq!(r.typed_violations.len(),3);
}
#[test]fn tagged_diagnostics_keep_data_and_distinct_keys(){
 let units=vec![ValidationUnit::FiniteCategory(FiniteCategoryValidation::ObjectReference),ValidationUnit::Functor(FunctorValidation::Name),ValidationUnit::NatTrans(NatTransValidation::Name),ValidationUnit::Adjunction(AdjunctionValidation::UnitNaturality),ValidationUnit::Profunctor(ProfunctorValidation::DimapIdentity),ValidationUnit::HigherFunctor(HigherFunctorValidation::TwoFunctorObjectMap),ValidationUnit::Coend(CoendValidation::Dinaturality),ValidationUnit::KanExtension(KanExtensionValidation::UniversalProperty),ValidationUnit::Cauchy(CauchyValidation::IdempotentSplitting),ValidationUnit::Monad(MonadValidation::UnitLeft),ValidationUnit::Condensation(CondensationValidation::BaseSplitting),ValidationUnit::Lawvere(LawvereValidation::ProductPreservation),ValidationUnit::Operad(OperadValidation::Associativity),ValidationUnit::Rewriting(RewritingValidation::LocalConfluence),ValidationUnit::Other("x".into()),ValidationUnit::Other("y".into())];
 assert_eq!(units.iter().cloned().collect::<std::collections::HashSet<_>>().len(),16);
 let locations=vec![ValidationLocation::Global,ValidationLocation::Object("x".into()),ValidationLocation::Morphism("x".into()),ValidationLocation::Named("x".into()),ValidationLocation::Boundary{morphism:"m".into(),source:"s".into(),target:"t".into()},ValidationLocation::Composition{first:"a".into(),second:"b".into(),composite:None},ValidationLocation::Composition{first:"a".into(),second:"b".into(),composite:Some("c".into())}];assert_eq!(locations.iter().cloned().collect::<std::collections::HashSet<_>>().len(),7);
 for unit in units{for location in &locations{let v=ValidationViolation::new(unit.clone(),location.clone(),"message",ValidationSeverity::Warning);assert_eq!(v.unit,unit);assert_eq!(&v.location,location);assert_eq!(v.message,"message");assert_eq!(v.severity,ValidationSeverity::Warning);assert_eq!(v.clone(),v);}}
}
'''

ARROW=r'''
use std::sync::Mutex;
#[derive(Debug)]struct Marker(&'static str);impl std::fmt::Display for Marker{fn fmt(&self,f:&mut std::fmt::Formatter<'_>)->std::fmt::Result{f.write_str(self.0)}}impl std::error::Error for Marker{}
type Trace=Arc<Mutex<Vec<String>>>;
fn ctx()->Ctx{Ctx{common_constants:vec![num_rational::BigRational::new_raw(2.into(),4.into())],threshold:num_rational::BigRational::new_raw(1.into(),0.into())}}
fn state()->St{St{suggestions:vec!["seed".into()]}}
fn action(label:&'static str,fail:bool,trace:Trace)->Arrow<String,String>{Arc::new(move|ctx,mut st,a|{
 assert_eq!(ctx.threshold.numer().to_string(),"1");assert_eq!(ctx.threshold.denom().to_string(),"0");assert_eq!(ctx.common_constants[0].numer().to_string(),"2");assert_eq!(ctx.common_constants[0].denom().to_string(),"4");
 trace.lock().unwrap().push(label.into());st.suggestions.push(format!("{}:{}",label,a));if fail{return Err(anyhow::Error::new(Marker(label)));}Ok((vec![Violation{rule_id:label.into(),msg:a.clone(),severity:"raw".into()}],st,format!("{}>{}",a,label)))})}
fn logs(w:&Writer)->Vec<(&str,&str,&str)>{w.iter().map(|v|(v.rule_id.as_str(),v.msg.as_str(),v.severity.as_str())).collect()}
#[test]fn lifts_and_tell_preserve_input_state_and_call_once(){
 for which in 0..2{let trace:Trace=Arc::new(Mutex::new(vec![]));let t=trace.clone();let f=move|a:String|{t.lock().unwrap().push("lift".into());format!("{}!",a)};let arrow=if which==0{arr(f)}else{map_input(f)};let(w,s,b)=arrow(&ctx(),state(),"x".into()).unwrap();assert!(w.is_empty());assert_eq!(s.suggestions,["seed"]);assert_eq!(b,"x!");assert_eq!(*trace.lock().unwrap(),["lift"]);}
 let v=Violation{rule_id:"rule".into(),msg:" \0λ".into(),severity:"Info".into()};let a=tell::<Odd>(v);let(w,s,b)=a(&ctx(),state(),Odd(7)).unwrap();assert_eq!(logs(&w),[("rule"," \0λ","Info")]);assert_eq!(s.suggestions,["seed"]);assert_eq!(b.0,7);
}
#[derive(Debug)]struct Odd(i64);impl Clone for Odd{fn clone(&self)->Self{Odd(self.0+100)}}
#[test]fn composition_threads_state_values_log_order_and_same_error(){
 for bad1 in [false,true]{for bad2 in [false,true]{let trace:Trace=Arc::new(Mutex::new(vec![]));let arrow=compose(action("L",bad1,trace.clone()),action("R",bad2,trace.clone()));let result=arrow(&ctx(),state(),"x".into());
 if bad1||bad2{let e=result.unwrap_err();assert_eq!(e.downcast_ref::<Marker>().unwrap().0,if bad1{"L"}else{"R"});}else{let(w,s,b)=result.unwrap();assert_eq!(logs(&w),[("L","x","raw"),("R","x>L","raw")]);assert_eq!(s.suggestions,["seed","L:x","R:x>L"]);assert_eq!(b,"x>L>R");}
 assert_eq!(*trace.lock().unwrap(),if bad1{vec!["L"]}else{vec!["L","R"]});
 }}
}
#[test]fn fanout_and_split_are_sequential_and_stop_after_first_error(){
 for kind in 0..2{for bad1 in [false,true]{for bad2 in [false,true]{let trace:Trace=Arc::new(Mutex::new(vec![]));let left=action("L",bad1,trace.clone());let right=action("R",bad2,trace.clone());let result=if kind==0{fanout(left,right)(&ctx(),state(),"x".into())}else{split(left,right)(&ctx(),state(),("x".into(),"y".into()))};
 if bad1||bad2{assert_eq!(result.unwrap_err().downcast_ref::<Marker>().unwrap().0,if bad1{"L"}else{"R"});}else{let(w,s,b)=result.unwrap();let second=if kind==0{"x"}else{"y"};assert_eq!(logs(&w),[("L","x","raw"),("R",second,"raw")]);assert_eq!(s.suggestions,vec!["seed".to_string(),"L:x".into(),format!("R:{}",second)]);assert_eq!(b,("x>L".to_string(),format!("{}>R",second)));}
 assert_eq!(*trace.lock().unwrap(),if bad1{vec!["L"]}else{vec!["L","R"]});
 }}}
 let left:Arrow<Odd,i64>=Arc::new(|_,s,a|Ok((vec![],s,a.0)));let right=left.clone();let(_,s,pair)=fanout(left,right)(&ctx(),state(),Odd(7)).unwrap();assert_eq!(pair,(107,7));assert_eq!(s.suggestions,["seed"]);
}
#[test]fn choice_only_runs_selected_branch_and_preserves_state(){
 for left in [false,true]{for fail in [false,true]{let trace:Trace=Arc::new(Mutex::new(vec![]));let a=choice(action("L",fail,trace.clone()),action("R",fail,trace.clone()));let selected=if left{"L"}else{"R"};let input=if left{Either::Left("x".into())}else{Either::Right("x".into())};let result=a(&ctx(),state(),input);
 if fail{assert_eq!(result.unwrap_err().downcast_ref::<Marker>().unwrap().0,selected);}else{let(w,s,b)=result.unwrap();assert_eq!(logs(&w),[(selected,"x","raw")]);assert_eq!(s.suggestions,vec!["seed".to_string(),format!("{}:x",selected)]);assert_eq!(b,format!("x>{}",selected));}assert_eq!(*trace.lock().unwrap(),[selected]);
 }}
}
'''

BUILDER=r'''
#[test]fn raw_fluent_routes_and_checked_identity_boundaries(){
 for name in ["","x","id_x","\0λ"]{
  let b=DeclaredFiniteCategoryBuilder::new(name);let c=b.clone().build();assert_eq!(c.name,name);assert!(c.objects.is_empty());assert!(c.morphisms.is_empty());assert!(c.identities.is_empty());assert!(c.compositions.is_empty());
  let c=b.object("extra").morphism("f","A","B").identity("C","i").composition("f","i","z").path_composition("i","f","w").build();assert!(c.has_object("extra"));assert_eq!(c.boundary_of("f"),Some(("A","B")));assert_eq!(c.boundary_of("i"),Some(("C","C")));assert_eq!(c.identity_of("C"),Some("i"));assert_eq!(c.compose("f","i"),Some("z"));assert_eq!(c.compose("i","f"),Some("w"));assert_eq!(c.name,name);
 }
 for object in ["","A","\0λ"]{for src in ["","A","\0λ"]{for tgt in ["","A","\0λ"]{
  let input=DeclaredFiniteCategoryBuilder::new("N").morphism("e",src,tgt);let result=input.identity_checked(object,"e");
  if src==object&&tgt==object{let c=result.unwrap().build();assert_eq!(c.boundary_of("e"),Some((src,tgt)));assert_eq!(c.identity_of(object),Some("e"));}else{assert_eq!(result.unwrap_err(),format!("Cannot set e as identity of {}: boundary is {} → {}",object,src,tgt));}
 }}}
 let c=DeclaredFiniteCategoryBuilder::new("N").identity_checked("A","fresh").unwrap().build();assert_eq!(c.boundary_of("fresh"),Some(("A","A")));assert_eq!(c.identity_of("A"),Some("fresh"));
 let c=DeclaredFiniteCategoryBuilder::new("N").identity_object("A").build();assert_eq!(c.boundary_of("id_A"),Some(("A","A")));assert_eq!(c.identity_of("A"),Some("id_A"));
}
#[test]fn identity_completion_matches_independent_snapshot_update_rules(){
 let possible=[("p","A","A"),("q","A","B"),("r","B","A"),("s","B","B")];
 for bits in 0..16usize{for ids in 0..4usize{
  let mut b=DeclaredFiniteCategoryBuilder::new("raw").object("A").object("B");if ids&1!=0{b=b.identity("A","iA");}if ids&2!=0{b=b.identity("B","iB");}
  for (i,(name,src,tgt)) in possible.iter().enumerate(){if bits&(1<<i)!=0{b=b.morphism(name,src,tgt);}}
  b=b.composition("iA","q","wrong").composition("unrelated","pair","keep");let before=b.clone().build();let mut expected=before.compositions.clone();
  for m in before.morphisms.values(){for (first,second) in [(before.identities.get(&m.source).map(String::as_str),Some(m.name.as_str())),(Some(m.name.as_str()),before.identities.get(&m.target).map(String::as_str))]{if let(Some(f),Some(g))=(first,second){expected.insert((f.to_string(),g.to_string()),m.name.clone());}}}
  let completed=b.identity_compositions();let actual=completed.clone().build();assert_eq!(actual.name,before.name);assert_eq!(actual.objects,before.objects);assert_eq!(actual.morphisms,before.morphisms);assert_eq!(actual.identities,before.identities);assert_eq!(actual.compositions,expected);assert_eq!(completed.identity_compositions().build().compositions,expected);
 }}
 // Publicly reachable stale identity bindings make last-write ordering observable.
 let c=DeclaredFiniteCategoryBuilder::new("collision").identity("A","e").identity("B","f").morphism("e","A","B").morphism("f","A","B").identity_compositions().build();assert_eq!(c.compose("e","f"),Some("f"));
}
#[test]fn walking_recipe_and_fresh_admission_keep_context(){
 let raw=DeclaredFiniteCategoryBuilder::walking_arrow("W","A","B","f").build();assert_eq!(raw.name,"W");assert_eq!(raw.objects.len(),2);assert_eq!(raw.morphisms.len(),3);assert_eq!(raw.boundary_of("f"),Some(("A","B")));assert_eq!(raw.identities.get("A").unwrap(),"id_A");assert_eq!(raw.identities.get("B").unwrap(),"id_B");
 let expected=std::collections::BTreeMap::from([(("id_A".to_string(),"id_A".to_string()),"id_A".to_string()),(("id_B".to_string(),"id_B".to_string()),"id_B".to_string()),(("id_A".to_string(),"f".to_string()),"f".to_string()),(("f".to_string(),"id_B".to_string()),"f".to_string())]);assert_eq!(raw.compositions,expected);
 let c=DeclaredFiniteCategoryBuilder::walking_arrow("W","A","B","f").build_validated().unwrap();assert_eq!(c.declared().name,"W");assert_eq!(c.declared().compositions,expected);assert_eq!(c.declared().boundary_of("f"),Some(("A","B")));
 let bad=DeclaredFiniteCategoryBuilder::new("bad").object("A").build_validated().unwrap_err();assert!(!bad.all_passed());assert!(bad.failure_count()>0);
 let raw_bad=DeclaredFiniteCategoryBuilder::new("raw").morphism("f","A","B").build();assert!(raw_bad.identities.is_empty());assert!(raw_bad.has_morphism("f"));
 let overwritten=DeclaredFiniteCategoryBuilder::new("raw").identity("A","e").morphism("e","A","B").identity_checked("A","e");assert!(overwritten.is_err());
}
'''

EM_COUNTER=r'''
fn free_bool()->EMAlgebra<MaybeMonad,Maybe<bool>>{FreeAlgebraFunctor::<MaybeMonad>::new().map::<bool>()}
fn bad_morphism(_:Maybe<bool>)->Maybe<bool>{Maybe::Just(true)}
#[test]fn false_unit_law_must_not_be_accepted_without_evaluation(){
 let mut algebra=free_bool();algebra.action=Box::new(|_|Maybe::Nothing);let a=Maybe::Just(true);assert_ne!((algebra.action)(MaybeMonad::unit(a.clone())),a);assert!(!algebra.verify_laws());
}
#[test]fn false_morphism_law_must_not_be_accepted_without_evaluation(){
 let dom=free_bool();let cod=free_bool();let morphism=AlgebraMorphism::<MaybeMonad,Maybe<bool>,Maybe<bool>>::new(bad_morphism);let input=Maybe::<Maybe<bool>>::Nothing;let left=bad_morphism((dom.action)(input.clone()));let right=(cod.action)(MaybeMonad::fmap(bad_morphism,input));assert_ne!(left,right);assert!(!morphism.respects_algebras(&dom,&cod));
}
'''

def challenge(subject):
    name=Path(subject['path']).stem
    body=EM_COUNTER if name=='eilenberg_moore' else VALIDATION if name=='validation' else BUILDER if name=='finite_category_builder' else ARROW
    return '\n#[cfg(test)] mod independent_record_tests { use super::*;\n'+body+'\n}\n'
