"""Independent equation/pair masks plus frozen pre-refactor raw behavior."""

REFERENCE = r'''
fn reference_find_idempotents(
    endomorphisms: &[(&str, &str, bool)],
    compositions: &BTreeMap<(String, String), String>,
) -> Vec<(String, String)> {
    let mut idempotents = Vec::new();
    for &(mor, obj, is_id) in endomorphisms {
        if is_id {
            continue; // Identities are trivially idempotent, skip.
        }
        let key = (mor.to_string(), mor.to_string());
        if let Some(composed) = compositions.get(&key) {
            if composed == mor {
                idempotents.push((mor.to_string(), obj.to_string()));
            }
        }
    }
    idempotents
}

fn reference_check_idempotent_splits(
    idempotent: &str,
    carrier: &str,
    morphisms_to_carrier: &[(&str, &str)], // (morphism_name, source_object)
    morphisms_from_carrier: &[(&str, &str)], // (morphism_name, target_object)
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Option<IdempotentSplitting> {
    // Search for a splitting pair (s, r).
    for &(s, r_obj) in morphisms_to_carrier {
        for &(r, s_obj) in morphisms_from_carrier {
            if r_obj != s_obj {
                continue; // s and r must share the retract object R.
            }
            let retract = r_obj;

            // Check r ∘ s = id_R
            let rs_key = (s.to_string(), r.to_string());
            let id_r = identity_map.get(retract);
            let rs_ok = compositions
                .get(&rs_key)
                .and_then(|v| id_r.map(|id| v == id))
                .unwrap_or(false);

            // Check s ∘ r = e
            let sr_key = (r.to_string(), s.to_string());
            let sr_ok = compositions
                .get(&sr_key)
                .map(|v| v == idempotent)
                .unwrap_or(false);

            if rs_ok && sr_ok {
                return Some(IdempotentSplitting {
                    carrier: carrier.to_string(),
                    idempotent: idempotent.to_string(),
                    retract: retract.to_string(),
                    section: s.to_string(),
                    retraction: r.to_string(),
                });
            }
        }
    }
    None
}

fn reference_check_cauchy_completeness(
    endomorphisms: &[(&str, &str, bool)],
    compositions: &BTreeMap<(String, String), String>,
    morphisms_to: &BTreeMap<String, Vec<(String, String)>>, // target → [(mor, source)]
    morphisms_from: &BTreeMap<String, Vec<(String, String)>>, // source → [(mor, target)]
    identity_map: &BTreeMap<String, String>,
) -> CauchyStatus {
    let idempotents = reference_find_idempotents(endomorphisms, compositions);
    let mut unsplit = Vec::new();

    for (idem, carrier) in &idempotents {
        let to_carrier: Vec<(&str, &str)> = morphisms_to
            .get(carrier)
            .map(|v| v.iter().map(|(m, s)| (m.as_str(), s.as_str())).collect())
            .unwrap_or_default();
        let from_carrier: Vec<(&str, &str)> = morphisms_from
            .get(carrier)
            .map(|v| v.iter().map(|(m, t)| (m.as_str(), t.as_str())).collect())
            .unwrap_or_default();

        if reference_check_idempotent_splits(
            idem,
            carrier,
            &to_carrier,
            &from_carrier,
            compositions,
            identity_map,
        )
        .is_none()
        {
            unsplit.push(idem.clone());
        }
    }

    if unsplit.is_empty() {
        CauchyStatus::Complete
    } else {
        CauchyStatus::Incomplete {
            unsplit_idempotents: unsplit,
        }
    }
}

fn reference_validate_splitting(
    splitting: &IdempotentSplitting,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();

    // Check e ∘ e = e
    let ee_key = (splitting.idempotent.clone(), splitting.idempotent.clone());
    match compositions.get(&ee_key) {
        Some(v) if v == &splitting.idempotent => {}
        Some(v) => {
            violations.push(format!(
                "Not idempotent: {} ∘ {} = {} ≠ {}",
                splitting.idempotent, splitting.idempotent, v, splitting.idempotent
            ));
        }
        None => {
            violations.push(format!(
                "Composition {} ∘ {} not defined",
                splitting.idempotent, splitting.idempotent
            ));
        }
    }

    // Check r ∘ s = id_R
    let rs_key = (splitting.section.clone(), splitting.retraction.clone());
    let expected_id = identity_map.get(&splitting.retract);
    match (compositions.get(&rs_key), expected_id) {
        (Some(v), Some(id)) if v == id => {}
        (Some(v), Some(id)) => {
            violations.push(format!(
                "Retraction law failed: r ∘ s = {} but id_R = {}",
                v, id
            ));
        }
        _ => {
            violations.push("Retraction law: composition r ∘ s or id_R not defined".into());
        }
    }

    // Check s ∘ r = e
    let sr_key = (splitting.retraction.clone(), splitting.section.clone());
    match compositions.get(&sr_key) {
        Some(v) if v == &splitting.idempotent => {}
        Some(v) => {
            violations.push(format!(
                "Section law failed: s ∘ r = {} but e = {}",
                v, splitting.idempotent
            ));
        }
        None => {
            violations.push("Section law: composition s ∘ r not defined".into());
        }
    }

    violations
}
'''

ORACLE = r'''
fn raw()->IdempotentSplitting{IdempotentSplitting{carrier:"unchecked carrier".into(),idempotent:"e".into(),retract:"R".into(),section:"s".into(),retraction:"r".into()}}
#[test] fn all_three_equation_observations_and_historical_wrapper(){
 let values=[None,Some("e"),Some("I"),Some("wrong")];
 for ee in values{for rs in values{for sr in values{for id in values{
  let mut c=BTreeMap::new();let mut identities=BTreeMap::new();if let Some(v)=ee{c.insert(("e".into(),"e".into()),v.into());}if let Some(v)=rs{c.insert(("s".into(),"r".into()),v.into());}if let Some(v)=sr{c.insert(("r".into(),"s".into()),v.into());}if let Some(v)=id{identities.insert("R".into(),v.into());}
  let mut expected=Vec::new();if ee!=Some("e"){expected.push(match ee{None=>"Composition e ∘ e not defined".to_string(),Some(v)=>format!("Not idempotent: e ∘ e = {v} ≠ e")});}
  match (rs,id){(Some(a),Some(b))if a==b=>{},(Some(a),Some(b))=>expected.push(format!("Retraction law failed: r ∘ s = {a} but id_R = {b}")),_=>expected.push("Retraction law: composition r ∘ s or id_R not defined".into())};
  if sr!=Some("e"){expected.push(match sr{None=>"Section law: composition s ∘ r not defined".to_string(),Some(v)=>format!("Section law failed: s ∘ r = {v} but e = e")});}
  let candidate=raw();let copy=candidate.clone();let saved=(c.clone(),identities.clone());assert_eq!(validate_splitting(&candidate,&c,&identities),expected);assert_eq!(reference_validate_splitting(&candidate,&c,&identities),expected);
  let result=ValidatedIdempotentSplitting::try_new(candidate,&c,&identities);
  if expected.is_empty(){let wrapper=result.unwrap();assert_eq!(wrapper.declared(),&copy);let cloned=wrapper.clone();assert_eq!(cloned,wrapper);c.clear();identities.clear();assert_eq!(wrapper.declared(),&copy);assert_eq!(validate_splitting(wrapper.declared(),&c,&identities).len(),3);}else{assert_eq!(result.unwrap_err(),expected);assert_eq!((c,identities),saved);}
 }}}}
 let metadata=CauchyCompletion{original_objects:vec!["A".into(),"A".into()],added_objects:vec!["A".into()],splittings:vec![raw()]};let clone=metadata.clone();assert_eq!(clone.original_objects,metadata.original_objects);assert_eq!(clone.added_objects,metadata.added_objects);assert_eq!(clone.splittings,metadata.splittings);
}
#[test] fn exhaustive_pair_masks_and_ordered_unsplit_inventory(){
 let to=[("s2","R0"),("s0","R1"),("s1","R0")];let from=[("r1","R1"),("r0","R0"),("r2","R0")];
 for mask in 0..512usize{for identity_mask in 0..4usize{
  let mut c=BTreeMap::new();let mut identities=BTreeMap::new();for (i,(s,r)) in to.iter().enumerate(){for(j,(v,_))in from.iter().enumerate(){let bit=i*3+j;
   if mask&(1<<bit)!=0{c.insert((s.to_string(),v.to_string()),format!("ID_{r}"));c.insert((v.to_string(),s.to_string()),"e".into());}
   else if bit%2==0{c.insert((s.to_string(),v.to_string()),format!("ID_{r}"));c.insert((v.to_string(),s.to_string()),"wrong".into());}
   else{c.insert((v.to_string(),s.to_string()),"e".into());}
  }}if identity_mask&1!=0{identities.insert("R0".into(),"ID_R0".into());}if identity_mask&2!=0{identities.insert("R1".into(),"ID_R1".into());}
  // Valid candidate positions in the full3x3 array; mismatched retract labels
  // are excluded even when both table equations were supplied as true.
  let first=[1usize,2,3,7,8].into_iter().find(|&k|mask&(1<<k)!=0&&identity_mask&(if k==3{2}else{1})!=0);
  let expected=first.map(|k|IdempotentSplitting{carrier:"A".into(),idempotent:"e".into(),retract:to[k/3].1.into(),section:to[k/3].0.into(),retraction:from[k%3].0.into()});
  assert_eq!(check_idempotent_splits("e","A",&to,&from,&c,&identities),expected);assert_eq!(reference_check_idempotent_splits("e","A",&to,&from,&c,&identities),expected);
  let mut reversed_to=to;reversed_to.reverse();let mut reversed_from=from;reversed_from.reverse();assert_eq!(check_idempotent_splits("e","A",&reversed_to,&reversed_from,&c,&identities),reference_check_idempotent_splits("e","A",&reversed_to,&reversed_from,&c,&identities));
  c.insert(("e".into(),"e".into()),"e".into());c.insert(("x".into(),"x".into()),"x".into());
  let endos=[("e","A",false),("e","A",false),("x","B",false),("e","A",true)];let tos=BTreeMap::from([("A".into(),to.iter().map(|(m,r)|(m.to_string(),r.to_string())).collect())]);let froms=BTreeMap::from([("A".into(),from.iter().map(|(m,r)|(m.to_string(),r.to_string())).collect())]);
  let expected_status=CauchyStatus::Incomplete{unsplit_idempotents:if first.is_some(){vec!["x".into()]}else{vec!["e".into(),"e".into(),"x".into()]}};
  assert_eq!(check_cauchy_completeness(&endos,&c,&tos,&froms,&identities),expected_status);assert_eq!(reference_check_cauchy_completeness(&endos,&c,&tos,&froms,&identities),expected_status);
  assert_eq!(check_cauchy_completeness(&endos[..2],&c,&tos,&froms,&identities),if first.is_some(){CauchyStatus::Complete}else{CauchyStatus::Incomplete{unsplit_idempotents:vec!["e".into(),"e".into()]}});
 }}
}
#[test] fn flags_duplicates_aliases_and_vacuous_inventory(){
 let rows=[("e","A",false),("x","B",false),("e","other",false),("e","A",false),("","λ\0",false)];let cells=[None,Some("e"),Some("x"),Some("")];
 for ee in cells{for xx in cells{for empty in cells{for mask in 0..32usize{
  let mut c=BTreeMap::new();for(name,value)in[("e",ee),("x",xx),("",empty)]{if let Some(v)=value{c.insert((name.into(),name.into()),v.into());}}
  let input:Vec<_>=rows.iter().enumerate().map(|(i,&(m,o,_))|(m,o,mask&(1<<i)!=0)).collect();let expected:Vec<_>=input.iter().filter(|(m,_,identity)|!identity&&match *m{"e"=>ee==Some("e"),"x"=>xx==Some("x"),_=>empty==Some("")}).map(|(m,o,_)|(m.to_string(),o.to_string())).collect();
  assert_eq!(find_idempotents(&input,&c),expected);assert_eq!(reference_find_idempotents(&input,&c),expected);
 }}}}
 let mut c=BTreeMap::from([(("".into(),"".into()),"".into())]);let ids=BTreeMap::from([("".into(),"".into())]);let arbitrary=IdempotentSplitting{carrier:"not in a category".into(),idempotent:"".into(),retract:"".into(),section:"".into(),retraction:"".into()};
 assert!(ValidatedIdempotentSplitting::try_new(arbitrary.clone(),&c,&ids).is_ok());assert_eq!(check_idempotent_splits("","ghost",&[("","")],&[("","")],&c,&ids).unwrap().carrier,"ghost");c.clear();
 assert_eq!(check_cauchy_completeness(&[],&c,&BTreeMap::new(),&BTreeMap::new(),&ids),CauchyStatus::Complete);
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_cauchy_tests {use super::*;\n'+REFERENCE+ORACLE+'\n}\n'

