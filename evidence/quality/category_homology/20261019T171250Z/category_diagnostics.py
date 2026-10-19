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

EM_SAMPLES=EM_COUNTER+r'''
use std::rc::Rc;
use std::cell::Cell;
fn units()->Vec<Maybe<bool>>{vec![Maybe::Nothing,Maybe::Just(false),Maybe::Just(true)]}
fn nested()->Vec<Maybe<Maybe<Maybe<bool>>>>{vec![Maybe::Nothing,Maybe::Just(Maybe::Nothing),Maybe::Just(Maybe::Just(Maybe::Nothing)),Maybe::Just(Maybe::Just(Maybe::Just(false))),Maybe::Just(Maybe::Just(Maybe::Just(true)))]}
fn morph_inputs()->Vec<Maybe<Maybe<bool>>>{vec![Maybe::Nothing,Maybe::Just(Maybe::Nothing),Maybe::Just(Maybe::Just(false)),Maybe::Just(Maybe::Just(true))]}
#[test]fn explicit_samples_observe_valid_algebras_and_empty_scope(){
 let a=free_bool();assert!(!a.verify_laws());assert_eq!(a.check_samples(units(),nested()),Ok(AlgebraSampleCheck{unit_samples:3,associativity_samples:5}));assert_eq!(a.check_samples(vec![],vec![]),Ok(AlgebraSampleCheck{unit_samples:0,associativity_samples:0}));
 let id=AlgebraMorphism::<MaybeMonad,Maybe<bool>,Maybe<bool>>::new(|x|x);let b=free_bool();assert!(!id.respects_algebras(&a,&b));assert_eq!(id.check_samples(&a,&b,morph_inputs()),Ok(4));assert_eq!(id.check_samples(&a,&b,vec![]),Ok(0));
}
#[test]fn unit_associativity_and_morphism_counterexamples_have_exact_first_payloads(){
 let calls=Rc::new(Cell::new(0usize));let c=calls.clone();let mut a=free_bool();a.action=Box::new(move|_|{c.set(c.get()+1);Maybe::Nothing});assert_eq!(a.check_samples(vec![Maybe::Nothing,Maybe::Just(true)],nested()),Err(LawCheckError::Violated{law:AlgebraLaw::Unit,index:1}));assert_eq!(calls.get(),2);
 let mut a=free_bool();a.action=Box::new(|x|match x{Maybe::Nothing=>Maybe::Nothing,Maybe::Just(Maybe::Nothing)=>Maybe::Nothing,Maybe::Just(Maybe::Just(v))=>Maybe::Just(!v)});let passing=Maybe::Nothing;let failing=Maybe::Just(Maybe::Just(Maybe::Just(false)));assert_eq!(a.check_samples(vec![],vec![passing,failing]),Err(LawCheckError::Violated{law:AlgebraLaw::Associativity,index:1}));
 let dom=free_bool();let cod=free_bool();let m=AlgebraMorphism::<MaybeMonad,Maybe<bool>,Maybe<bool>>::new(bad_morphism);assert_eq!(m.check_samples(&dom,&cod,vec![Maybe::Just(Maybe::Just(true)),Maybe::Nothing]),Err(LawCheckError::Violated{law:AlgebraLaw::Morphism,index:1}));
}
#[derive(Debug)]struct IdMonad;
impl Monad for IdMonad{type T<A:Obj>=A;fn unit<A:Obj>(x:A)->A{x}fn bind<A:Obj,B:Obj>(a:A,f:impl Fn(A)->B)->B{f(a)}fn fmap<A:Obj,B:Obj>(f:impl Fn(A)->B,a:A)->B{f(a)}}
#[derive(Debug,PartialEq,Eq)]struct Odd(u8);impl Clone for Odd{fn clone(&self)->Self{Self(if self.0==0{0}else{self.0^1})}}
#[test]fn nonpreserving_clone_is_rejected_before_callback_evaluation(){
 for law in [AlgebraLaw::Unit,AlgebraLaw::Associativity]{let mut a=FreeAlgebraFunctor::<IdMonad>::new().map::<Odd>();a.action=Box::new(|_|panic!("clone refusal must precede action"));let (unit,assoc)=if law==AlgebraLaw::Unit{(vec![Odd(1)],vec![])}else{(vec![],vec![Odd(1)])};assert_eq!(a.check_samples(unit,assoc),Err(LawCheckError::NonPreservingClone{law,index:0}));}
 let mut a=FreeAlgebraFunctor::<IdMonad>::new().map::<Odd>();a.action=Box::new(|_|panic!("clone refusal must precede action"));let b=FreeAlgebraFunctor::<IdMonad>::new().map::<Odd>();let m=AlgebraMorphism::<IdMonad,Odd,Odd>::new(|_|panic!("clone refusal must precede morphism"));assert_eq!(m.check_samples(&a,&b,vec![Odd(1)]),Err(LawCheckError::NonPreservingClone{law:AlgebraLaw::Morphism,index:0}));
 let a=FreeAlgebraFunctor::<IdMonad>::new().map::<Odd>();let b=FreeAlgebraFunctor::<IdMonad>::new().map::<Odd>();
 assert_eq!(a.check_samples(vec![Odd(0),Odd(1)],vec![]),Err(LawCheckError::NonPreservingClone{law:AlgebraLaw::Unit,index:1}));
 assert_eq!(a.check_samples(vec![],vec![Odd(0),Odd(1)]),Err(LawCheckError::NonPreservingClone{law:AlgebraLaw::Associativity,index:1}));
 let id=AlgebraMorphism::<IdMonad,Odd,Odd>::new(|x|x);assert_eq!(id.check_samples(&a,&b,vec![Odd(0),Odd(1)]),Err(LawCheckError::NonPreservingClone{law:AlgebraLaw::Morphism,index:1}));
}
#[derive(Debug)]struct SwitchClone{value:bool,calls:Rc<Cell<usize>>}
impl PartialEq for SwitchClone{fn eq(&self,other:&Self)->bool{self.value==other.value}}impl Eq for SwitchClone{}
impl Clone for SwitchClone{fn clone(&self)->Self{let n=self.calls.get();self.calls.set(n+1);Self{value:if n==0{self.value}else{!self.value},calls:self.calls.clone()}}}
#[test]fn exactly_the_guarded_clone_enters_the_law(){
 let calls=Rc::new(Cell::new(0));let point=SwitchClone{value:false,calls:calls.clone()};let a=FreeAlgebraFunctor::<IdMonad>::new().map::<SwitchClone>();assert_eq!(a.check_samples(vec![point],vec![]),Ok(AlgebraSampleCheck{unit_samples:1,associativity_samples:0}));assert_eq!(calls.get(),1);
}
#[test]fn maybe_truth_tables_join_action_and_descriptive_adapters_are_literal(){
 for x in [false,true]{assert_eq!(MaybeMonad::unit(x),Maybe::Just(x));assert_eq!(MaybeMonad::bind(Maybe::Just(x),|v|Maybe::Just(!v)),Maybe::Just(!x));assert_eq!(MaybeMonad::fmap(|v|!v,Maybe::Just(x)),Maybe::Just(!x));}
 assert_eq!(MaybeMonad::bind::<bool,bool>(Maybe::Nothing,|_|panic!("Nothing must not call bind")),Maybe::Nothing);assert_eq!(MaybeMonad::fmap::<bool,bool>(|_|panic!("Nothing must not call fmap"),Maybe::Nothing),Maybe::Nothing);
 let free=FreeAlgebraFunctor::<MaybeMonad>::default().map::<bool>();for (input,expected) in [(Maybe::Nothing,Maybe::Nothing),(Maybe::Just(Maybe::Nothing),Maybe::Nothing),(Maybe::Just(Maybe::Just(false)),Maybe::Just(false)),(Maybe::Just(Maybe::Just(true)),Maybe::Just(true))]{assert_eq!(MaybeMonad::join(input.clone()),expected);assert_eq!((free.action)(input),expected);}
 let printer=ForgetfulFunctor::<MaybeMonad>::default().map(&free);assert_eq!(printer(),"Carrier type A");assert_eq!(ComparisonFunctor::<MaybeMonad,()>::default().map(&free),"Object in D (via comparison)");let m=AlgebraMorphism::<MaybeMonad,Maybe<bool>,Maybe<bool>>::new(|x|x);assert_eq!(format!("{:?}",m),"AlgebraMorphism");
}
'''

LAWVERE_COUNTER=r'''
#[test]fn overflowing_slot_is_reported_without_panicking_or_wrapping(){
 let mut t=LawvereTheory::new("raw");t.add_substitution("f",usize::MAX,"g","fg");
 let errors=check_substitution_associativity(&t,&[("f",usize::MAX,"g",1,"h")]);
 assert_eq!(errors,vec![format!("Substitution slot overflow: i={}, j=1",usize::MAX)]);
}
'''

LAWVERE_SAMPLES=LAWVERE_COUNTER+r'''
fn unary(name:&str)->OperationDecl{OperationDecl::new(name,vec!["S".into()],vec!["S".into()])}
#[test]fn raw_records_preserve_duplicates_overwrites_and_order(){
 let mut t=LawvereTheory::new("raw");assert_eq!(t.name,"raw");assert!(t.sorts.is_empty()&&t.operations.is_empty()&&t.equations.is_empty()&&t.substitution_table.is_empty()&&t.identities.is_empty());assert_eq!(t.cauchy_status,TheoryCauchyStatus::Complete);
 t.add_sort("S");t.add_sort("S");t.add_sort("Q");assert_eq!(t.sorts,vec!["S","S","Q"]);
 let op=unary("e");assert_eq!(op.name,"e");assert_eq!(op.input_sorts,vec!["S"]);assert_eq!(op.output_sorts,vec!["S"]);assert_eq!(op.arity(),1);assert_eq!(op.coarity(),1);assert_eq!(op,op.clone());assert_ne!(op,unary("other"));
 t.add_operation(op.clone());t.add_operation(op.clone());t.add_operation(OperationDecl::new("z",vec![],vec!["S".into(),"Q".into()]));assert_eq!(t.operations.len(),3);assert_eq!(t.operations_of_arity(1),vec![&op,&op]);assert_eq!(t.operations_of_arity(0)[0].name,"z");assert_eq!(t.operations[2].coarity(),2);assert!(t.operations_of_arity(2).is_empty());
 let eq=EquationDecl::new("eq","a","b");assert_eq!((eq.name.as_str(),eq.lhs.as_str(),eq.rhs.as_str()),("eq","a","b"));assert_eq!(eq,eq.clone());t.add_equation(eq.clone());t.add_equation(eq.clone());assert_eq!(t.equations,vec![eq.clone(),eq]);
 t.add_substitution("a",2,"b","old");t.add_substitution("a",2,"b","new");assert_eq!(t.substitute("a",2,"b"),Some("new"));assert_eq!(t.substitution_table.len(),1);assert_eq!(t.substitute("b",2,"a"),None);assert_eq!(t.substitute("a",1,"b"),None);let copy=t.clone();assert_eq!(copy.name,t.name);assert_eq!(copy.sorts,t.sorts);assert_eq!(copy.operations,t.operations);assert_eq!(copy.equations,t.equations);assert_eq!(copy.substitution_table,t.substitution_table);assert_eq!(copy.identities,t.identities);assert_eq!(copy.cauchy_status,t.cauchy_status);assert!(format!("{:?}",t).contains("raw"));
}
#[test]fn borrowed_lookup_matches_public_lookup_for_ordered_and_missing_keys(){
 let mut t=LawvereTheory::new("index");let names=["","a","aa","z","é"];for (n,outer) in names.iter().enumerate(){for (m,inner) in names.iter().enumerate(){for slot in [0,1,usize::MAX]{if (n+m)%2==0{t.add_substitution(outer,slot,inner,inner);}}}}
 let lookup=SubstitutionLookup::new(&t);assert_eq!(lookup.entries.len(),t.substitution_table.len());for outer in names.into_iter().chain(["missing"]){for inner in names.into_iter().chain(["absent"]){for slot in [0,1,2,usize::MAX]{assert_eq!(lookup.get(outer,slot,inner),t.substitute(outer,slot,inner));}}}
 assert_eq!(SubstitutionLookup::new(&LawvereTheory::new("empty")).get("",0,""),None);
}
#[test]fn supplied_associativity_cases_match_independent_presence_truth_table(){
 for mask in 0..16{for different in [false,true]{let mut t=LawvereTheory::new("cases");if mask&1!=0{t.add_substitution("g",3,"h","gh");}if mask&2!=0{t.add_substitution("f",2,"gh","L");}if mask&4!=0{t.add_substitution("f",2,"g","fg");}if mask&8!=0{t.add_substitution("fg",5,"h",if different{"R"}else{"L"});}
 let expected=if mask!=15{vec!["Substitution not defined for f=f, g=g, h=h".to_string()]}else if different{vec!["Substitution not associative: f=f, g=g, h=h: L≠R".to_string()]}else{vec![]};assert_eq!(check_substitution_associativity(&t,&[("f",2,"g",3,"h")]),expected,"mask={mask},different={different}");assert!(check_substitution_associativity(&t,&[]).is_empty());}}
 let mut t=LawvereTheory::new("max");t.add_substitution("g",0,"h","gh");t.add_substitution("f",usize::MAX,"gh","ok");t.add_substitution("f",usize::MAX,"g","fg");t.add_substitution("fg",usize::MAX,"h","ok");assert!(check_substitution_associativity(&t,&[("f",usize::MAX,"g",0,"h")]).is_empty());
 let errors=check_substitution_associativity(&t,&[("x",0,"y",0,"z"),("a",usize::MAX,"b",2,"c"),("f",usize::MAX,"g",0,"h"),("a",usize::MAX,"b",2,"c")]);assert_eq!(errors,vec!["Substitution not defined for f=x, g=y, h=z".to_string(),format!("Substitution slot overflow: i={}, j=2",usize::MAX),format!("Substitution slot overflow: i={}, j=2",usize::MAX)]);
}
#[test]fn split_inventory_matches_independent_two_name_matrix_oracle(){
 let names=["e","k"];for encoded in 0..81{let mut n=encoded;let mut table=[0usize;4];for value in &mut table{*value=n%3;n/=3;}
 for identity in 0..3{for shapes in 0..16{let shape=[shapes%4,shapes/4];let mut t=LawvereTheory::new("raw matrix");for e in 0..2{let (input,output)=match shape[e]{0=>(1,1),1=>(0,1),2=>(1,0),_=>(2,2)};t.add_operation(OperationDecl::new(names[e],vec!["S".into();input],vec!["S".into();output]));}if identity!=0{t.identities.insert("S".into(),names[identity-1].into());}
 for outer in 0..2{for inner in 0..2{let result=table[2*outer+inner];if result!=0{t.add_substitution(names[outer],0,names[inner],names[result-1]);}}}
 let mut expected=vec![];for e in 0..2{if shape[e]!=0||table[2*e+e]!=e+1{continue;}let mut split=false;for r in 0..2{for s in 0..2{if shape[r]!=2&&identity!=0&&table[2*s+r]==e+1&&table[2*r+s]==identity{split=true;}}}if !split{expected.push(names[e].to_string());}}
 let expected=if expected.is_empty(){TheoryCauchyStatus::Complete}else{TheoryCauchyStatus::Incomplete{unsplit_operations:expected}};assert_eq!(check_theory_cauchy(&t),expected,"table={encoded},id={identity},shapes={shapes}");assert_eq!(t.cauchy_status,TheoryCauchyStatus::Complete);
 }}}
}
#[test]fn raw_split_scope_order_duplicates_and_first_output_sort_are_literal(){
 let mut t=LawvereTheory::new("duplicates");t.add_operation(unary("z"));t.add_operation(unary("a"));t.add_operation(unary("z"));t.add_substitution("z",0,"z","z");t.add_substitution("a",0,"a","a");assert_eq!(check_theory_cauchy(&t),TheoryCauchyStatus::Incomplete{unsplit_operations:vec!["z".into(),"a".into(),"z".into()]});
 t.cauchy_status=TheoryCauchyStatus::Incomplete{unsplit_operations:vec!["stored".into()]};let before=t.cauchy_status.clone();t.operations.clear();assert_eq!(check_theory_cauchy(&t),TheoryCauchyStatus::Complete);assert_eq!(t.cauchy_status,before);
 let mut t=LawvereTheory::new("first output");t.add_operation(unary("e"));t.add_operation(OperationDecl::new("r",vec![],vec!["first".into(),"second".into()]));t.add_operation(OperationDecl::new("s",vec![],vec![]));t.add_substitution("e",0,"e","e");t.add_substitution("s",0,"r","e");t.add_substitution("r",0,"s","id");t.identities.insert("second".into(),"id".into());assert_eq!(check_theory_cauchy(&t),TheoryCauchyStatus::Incomplete{unsplit_operations:vec!["e".into()]});t.identities.insert("first".into(),"id".into());assert_eq!(check_theory_cauchy(&t),TheoryCauchyStatus::Complete);
}
'''

def challenge(subject):
    name=Path(subject['path']).stem
    body=(LAWVERE_COUNTER if subject.get('mode')=='counterexample' else LAWVERE_SAMPLES) if name=='lawvere' else (EM_COUNTER if subject.get('mode')=='counterexample' else EM_SAMPLES) if name=='eilenberg_moore' else VALIDATION if name=='validation' else BUILDER if name=='finite_category_builder' else ARROW
    allow='#[allow(deprecated)]' if name=='eilenberg_moore' else ''
    return '\n#[cfg(test)] '+allow+' mod independent_record_tests { use super::*;\n'+body+'\n}\n'
