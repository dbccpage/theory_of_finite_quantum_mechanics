"""Raw named-equation/flag inventory and checked metadata update controls."""

REGRESSION = '#[test] fn declared_max_level_is_refused_without_mutation_or_panic(){let mut c=Condensation::new("X","Y","s","r");c.coherence_level=usize::MAX;let before=c.clone();let result=std::panic::catch_unwind(std::panic::AssertUnwindSafe(||{let _=c.add_witness("next",true);}));assert!(result.is_ok(),"public raw max level must not overflow");assert_eq!(c,before);}'


ORIGINAL_VALIDATOR = 'fn original_validate_condensation(\n    cond: &Condensation,\n    compositions: &BTreeMap<(String, String), String>,\n    identity_map: &BTreeMap<String, String>,\n) -> Vec<String> {\n    let mut violations = Vec::new();\n\n    // Level 0: r ∘ s = id_Y\n    let rs_key = (cond.section.clone(), cond.retraction.clone());\n    let id_y = identity_map.get(&cond.retract);\n    match (compositions.get(&rs_key), id_y) {\n        (Some(v), Some(id)) if v == id => {}\n        (Some(v), Some(id)) => {\n            violations.push(format!(\n                "Condensation level 0: r ∘ s = {} but id_Y = {}",\n                v, id\n            ));\n        }\n        _ => {\n            violations.push("Condensation level 0: r ∘ s or id_Y not defined".into());\n        }\n    }\n\n    // Level 0: s ∘ r produces some endomorphism e of X\n    let sr_key = (cond.retraction.clone(), cond.section.clone());\n    let e = compositions.get(&sr_key);\n    match e {\n        Some(e_mor) => {\n            // Level 1: e ∘ e = e (idempotent)\n            let ee_key = (e_mor.clone(), e_mor.clone());\n            match compositions.get(&ee_key) {\n                Some(ee) if ee == e_mor => {}\n                Some(ee) => {\n                    violations.push(format!(\n                        "Condensation level 1: e ∘ e = {} but e = {} (not idempotent)",\n                        ee, e_mor\n                    ));\n                }\n                None => {\n                    violations.push(format!(\n                        "Condensation level 1: e ∘ e not defined for e = {}",\n                        e_mor\n                    ));\n                }\n            }\n        }\n        None => {\n            violations.push("Condensation level 0: s ∘ r not defined".into());\n        }\n    }\n\n    // Check coherence witnesses\n    for w in &cond.witnesses {\n        if w.level > 0 && !w.verified {\n            violations.push(format!(\n                "Condensation level {}: witness \'{}\' not verified",\n                w.level, w.description\n            ));\n        }\n    }\n\n    violations\n}\n'


ORACLES = r'''
#[test] fn checked_updates_and_caller_flags(){
 for label in ["","λ\0","base splitting data: r, s, X, Y"]{for verified in [false,true]{
  assert_eq!(CoherenceWitness::new(usize::MAX,label),CoherenceWitness{level:usize::MAX,description:label.into(),verified:false});
  assert_eq!(CoherenceWitness::verified(0,label),CoherenceWitness{level:0,description:label.into(),verified:true});
  for level in [0,1,7,usize::MAX-1,usize::MAX]{let mut c=Condensation::new("X","Y","s","r");assert_eq!((&*c.carrier,&*c.retract,&*c.section,&*c.retraction),("X","Y","s","r"));assert_eq!(c.coherence_level,0);assert_eq!(c.witnesses,vec![CoherenceWitness::new(0,"base splitting data: r, s, X, Y")]);c.coherence_level=level;let before=c.clone();let result=c.add_witness(label,verified);if level==usize::MAX{assert_eq!(result,Err(CoherenceLevelOverflow));assert_eq!(c,before);}else{assert_eq!(result,Ok(()));assert_eq!(c.coherence_level,level+1);let mut expected=before.witnesses;expected.push(CoherenceWitness{level:level+1,description:label.into(),verified});assert_eq!(c.witnesses,expected);}}
 }}
 for mask in 0usize..216{let mut n=mask;let mut c=Condensation::new("","λ","s","r");c.witnesses.clear();let mut expected_max=0;let mut all=true;for _ in 0..3{let state=n%6;n/=6;let level=[0,1,usize::MAX][state/2];let flag=state%2==1;c.witnesses.push(CoherenceWitness{level,description:"flag".into(),verified:flag});if flag{expected_max=expected_max.max(level);}else{all=false;}}assert_eq!(c.max_verified_level(),expected_max);assert_eq!(c.fully_verified(),all);}
 let mut c=Condensation::new("","","","");c.witnesses.clear();assert_eq!(c.max_verified_level(),0);assert!(c.fully_verified());
}
fn expected_flags(c:&Condensation)->Vec<String>{c.witnesses.iter().filter(|w|w.level!=0&&!w.verified).map(|w|format!("Condensation level {}: witness '{}' not verified",w.level,w.description)).collect()}
#[test] fn independent_defined_observations_and_order(){
 let choices=[None,Some("e"),Some("id"),Some("bad")];
 for &rs in &choices{for &identity in &choices{for &sr in &choices{for &ee in &choices{
  let mut c=Condensation::new("unchecked-carrier","Y","s","r");c.coherence_level=usize::MAX;c.witnesses=vec![CoherenceWitness::new(0,"base ignored"),CoherenceWitness::new(8,"λ\0"),CoherenceWitness::verified(1,"asserted"),CoherenceWitness::new(8,"duplicate")];
  let mut table=BTreeMap::new();if let Some(v)=rs{table.insert(("s".into(),"r".into()),v.into());}if let Some(v)=sr{table.insert(("r".into(),"s".into()),v.into());if let Some(w)=ee{table.insert((v.into(),v.into()),w.into());}}
  let identities: BTreeMap<_,_>=identity.map(|v|("Y".into(),v.into())).into_iter().collect();let mut errors=Vec::new();
  match(rs,identity){(Some(x),Some(y)) if x==y=>{},(Some(x),Some(y))=>errors.push(format!("Condensation level 0: r ∘ s = {} but id_Y = {}",x,y)),_=>errors.push("Condensation level 0: r ∘ s or id_Y not defined".into())}
  if let Some(e)=sr{if let Some(out)=ee{if out!=e{errors.push(format!("Condensation level 1: e ∘ e = {} but e = {} (not idempotent)",out,e));}}else{errors.push(format!("Condensation level 1: e ∘ e not defined for e = {}",e));}}else{errors.push("Condensation level 0: s ∘ r not defined".into());}
  errors.extend(expected_flags(&c));assert_eq!(validate_condensation(&c,&table,&identities),errors);assert_eq!(validate_condensation(&c,&table,&identities),original_validate_condensation(&c,&table,&identities));
 }}}}
}
#[test] fn literal_aliases_and_inventory_not_completeness(){
 let names=["","s","λ\0"];let mut records=Vec::new();
 for &s in &names{for &r in &names{for &e in &names{for mask in 0usize..16{
  let mut c=Condensation::new("unchecked-carrier","Y",s,r);c.witnesses.clear();let mut table=BTreeMap::new();if mask&1!=0{table.insert((s.into(),r.into()),"id".into());}if mask&2!=0{table.insert((r.into(),s.into()),e.into());}if mask&4!=0{table.insert((e.into(),e.into()),e.into());}let ids=if mask&8!=0{BTreeMap::from([("Y".into(),"id".into())])}else{BTreeMap::new()};assert_eq!(validate_condensation(&c,&table,&ids),original_validate_condensation(&c,&table,&ids));records.push(c);
 }}}}
 let table=BTreeMap::from([(("s".into(),"r".into()),"id".into()),(("r".into(),"s".into()),"e".into()),(("e".into(),"e".into()),"e".into())]);let ids=BTreeMap::from([("Y".into(),"id".into())]);
 for end in [0,1,2,records.len()]{let mut expected=Vec::new();for c in &records[..end]{let errors=original_validate_condensation(c,&table,&ids);if !errors.is_empty(){expected.push(format!("{} → {} ({})",c.carrier,c.retract,errors.join("; ")));}}let status=check_infinity_cauchy(&records[..end],&table,&ids);if expected.is_empty(){assert_eq!(status,InfinityCauchyStatus::Complete);}else{assert_eq!(status,InfinityCauchyStatus::Incomplete{unsplit_condensations:expected});}}
 let c=Condensation::new("not-admitted","Y","s","r");assert!(!c.fully_verified());assert!(validate_condensation(&c,&table,&ids).is_empty());assert_eq!(check_infinity_cauchy(&[c],&table,&ids),InfinityCauchyStatus::Complete);
}
'''


def challenge(subject):
    extra = '' if subject.get('probe') else ORIGINAL_VALIDATOR+ORACLES
    return '\n#[cfg(test)] mod independent_condensation_tests {use super::*;\n'+REGRESSION+extra+'\n}\n'
