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

def challenge(subject):
    body=VALIDATION if Path(subject['path']).stem=='validation' else ARROW
    return '\n#[cfg(test)] mod independent_record_tests { use super::*;\n'+body+'\n}\n'
