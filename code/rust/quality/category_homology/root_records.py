"""Independent specifications for literal root records; not categorical laws.

AuthorityEffect: None. Oracles are hand-stated field, tag, list and rational
boundary rules. Faults are designated valid changes, dispatched separately.
"""
from pathlib import Path
import json

ORACLES = {
"morphism": r'''
#[test] fn boundary_category_and_payload() {
 let tags=["", "x", "y", " x ", "λ\0"];
 for a in tags {for b in tags {for c in tags {for d in tags {
  let first=SkillMorphism::new("f", "a", a,b,"authority","ceiling","first");
  let next=SkillMorphism::new("g",c,"z",d,"other","other","second");
  assert_eq!(first.contract_id,"urn:omega:math:morphism:v0.1.0");
  assert_eq!((&first.morphism_id,&first.domain_id,&first.codomain_id,&first.category_id,&first.governance_authority,&first.evidence_ceiling,&first.description),
             (&"f".to_string(),&"a".to_string(),&a.to_string(),&b.to_string(),&"authority".to_string(),&"ceiling".to_string(),&"first".to_string()));
  let saved=first.clone(); let saved_next=next.clone(); let result=first.compose(&next);
  assert_eq!(result.is_some(), a==c && b==d);
  if let Some(r)=result {assert_eq!(r,SkillMorphism{contract_id:"urn:omega:math:morphism:v0.1.0".into(),morphism_id:"f >> g".into(),domain_id:"a".into(),codomain_id:"z".into(),category_id:b.into(),governance_authority:"authority".into(),evidence_ceiling:"ceiling".into(),description:"Composite morphism of f and g".into()});}
  assert_eq!(first,saved);assert_eq!(next,saved_next);
 }}}}
}
#[derive(Debug)] struct Echo;
impl MorphismTrait<String,String> for Echo {fn domain(&self)->&String{unreachable!()} fn codomain(&self)->&String{unreachable!()} fn id(&self)->&str{"id"} fn category_id(&self)->&str{"C"} fn evaluate(&self,x:&String)->String{x.clone()}}
#[test] fn signature_only() {let e=Echo; assert_eq!(e.evaluate(&"literal".into()),"literal");assert_eq!(e.id(),"id");assert_eq!(e.category_id(),"C");}
''',
"agent_functor": r'''
#[test] fn literal_relabeling() {
 for name in ["","agent", "[]:\0λ"] {for target in ["","D", " D "] {for affiliation in ["","council"] {
  let a=AgentFunctor::new(name,"source",target,"role",affiliation,vec!["skill".into(),"skill".into()],"desc");
  assert_eq!(a,AgentFunctor{contract_id:"urn:omega:math:functor:v0.1.0".into(),name:name.into(),source_category_id:"source".into(),target_category_id:target.into(),primary_role:"role".into(),council_affiliation:affiliation.into(),supported_skills:vec!["skill".into(),"skill".into()],description:"desc".into()});
  for raw in ["","f", "[]:\0λ"] {
   let m=crate::morphism::SkillMorphism{contract_id:"custom".into(),morphism_id:raw.into(),domain_id:"x".into(),codomain_id:"y".into(),category_id:"foreign".into(),governance_authority:"other".into(),evidence_ceiling:"scoped".into(),description:"raw".into()};
   let saved=m.clone();let saved_a=a.clone();let result=a.map_skill_morphism(&m);
   assert_eq!(result,crate::morphism::SkillMorphism{contract_id:"custom".into(),morphism_id:format!("{}[{}]",name,raw),domain_id:format!("{}:x",name),codomain_id:format!("{}:y",name),category_id:target.into(),governance_authority:affiliation.into(),evidence_ceiling:"scoped".into(),description:format!("Skill morphism {} lifted by Agent Functor {}",raw,name)});
   assert_eq!(m,saved);assert_eq!(a,saved_a);
  }
 }}}
}
#[derive(Debug)] struct Echo;
impl FunctorTrait<String,String,String,String> for Echo {fn source_category_id(&self)->&str{"C"} fn target_category_id(&self)->&str{"D"} fn map_object(&self,x:&String)->String{x.clone()} fn map_morphism(&self,x:&String)->String{x.clone()}}
#[test] fn trait_signature() {let e=Echo;assert_eq!(e.map_object(&"x".into()),"x");assert_eq!(e.map_morphism(&"f".into()),"f");assert_eq!(e.source_category_id(),"C");assert_eq!(e.target_category_id(),"D");}
''',
"bridges": r'''
#[test] fn declared_inventory() {
 for a in [""," source ","λ\0"] {for b in ["","target"] {for c in ["","map"] {
  let mut x=BridgeEvidence::new(a,b,c);assert_eq!((&*x.source_discipline,&*x.target_discipline,&*x.map_name), (a,b,c));assert!(x.laws_preserved.is_empty());
  for label in ["","identity","identity","λ\0"] {x.preserve_law(label);}
  assert_eq!(x.laws_preserved,vec!["","identity","identity","λ\0"]);
  let mut copy=x.clone();copy.preserve_law("extra");assert_eq!(x.laws_preserved.len(),4);assert_eq!(copy.laws_preserved.len(),5);
 }}}
}
struct Echo; impl StructurePreservingMap for Echo {type Domain=String;type Codomain=String;fn map(&self,x:&String)->String{x.clone()}}
#[test] fn trait_signature() {assert_eq!(Echo.map(&"x".into()),"x");}
''',
"hott_topos_bridge": r'''
#[test] fn ordered_missing_labels() {
 let tags=[""," \t\n","\u{2003}"," x ","\0λ"];
 for a in tags {for b in tags {for c in tags {
  let mut x=HottJudgmentInterpretation::new(a,b,c); assert_eq!((&*x.judgment,&*x.context_object,&*x.semantic_object),(a,b,c));assert!(x.evidence.is_empty());
  for item in ["","proof","proof"] {x.add_evidence(item);}
  let mut expected=vec![];
  if [""," \t\n","\u{2003}"].contains(&a){expected.push("HoTT judgment is empty".to_string());}
  if [""," \t\n","\u{2003}"].contains(&b){expected.push("Context object is empty".to_string());}
  if [""," \t\n","\u{2003}"].contains(&c){expected.push("Semantic object is empty".to_string());}
  let saved=x.clone();assert_eq!(x.validate(),expected);assert_eq!(x,saved);assert_eq!(x.evidence,vec!["","proof","proof"]);
 }}}
}
''',
"mssn_functor_bridge": r'''
#[test] fn declaration_only() {for a in ["","lift","λ\0"] {for b in ["","forget"," adjoint "] {
 let x=MssnFunctorBridge::new(a,b);assert_eq!((&*x.lift_functor,&*x.forget_functor),(a,b));
 assert_eq!(x.evidence,super::super::bridges::BridgeEvidence{source_discipline:"MSSN".into(),target_discipline:"category".into(),map_name:format!("{} adjoint {}",a,b),laws_preserved:vec!["lift/forget boundary".into()]});
}}}
''',
"simplicial_hott_bridge": r'''
#[test] fn raw_threshold() {for a in ["","simplex","λ\0"] {for b in ["","path"] {
 let mut x=SimplicialPathWitness::new(a,b);assert_eq!((&*x.simplex,&*x.hott_path),(a,b));assert!(x.coherence_cells.is_empty());
 for n in 0..=5 {x.coherence_cells=vec![String::new();n];for level in [0,1,2,3,4,5,6,usize::MAX] {let expected=match n {0=>level==0,1=>level==0||level==1,_=>level<=n};assert_eq!(x.is_coherent_at_level(level),expected);} }
}}}
''',
"topos_hott_model": r'''
#[test] fn raw_presence_only() {for name in ["","model","λ\0"] {
 let mut x=ToposHottModel::new(name);assert_eq!(x.name,name);assert!(x.universes.is_empty() && x.identity_type_interpretations.is_empty() && x.truncation_modalities.is_empty());
 for mask in 0..8 {x.universes=if mask&1!=0 {vec!["".into()]} else {vec![]};x.identity_type_interpretations=if mask&2!=0 {vec!["".into(),"".into()]} else {vec![]};x.truncation_modalities=if mask&4!=0 {vec!["unchecked".into()]} else {vec![]};
 let expected=match mask&3 {0=>vec![format!("Model {} has no universe interpretation",name),format!("Model {} has no identity type interpretation",name)],1=>vec![format!("Model {} has no identity type interpretation",name)],2=>vec![format!("Model {} has no universe interpretation",name)],_=>vec![]};
 let saved=x.clone();assert_eq!(x.validate_minimal_model(),expected);assert_eq!(x,saved);
 }
}}
''',
"zeta_functor": r'''
#[test] fn stored_product_not_arithmetic() {for numerator in [-2,0,2] {for denominator in [-2,0,2] {
 let q=num_rational::BigRational::new_raw(numerator.into(),denominator.into());let raw=vec!["".into(),"same".into(),"same".into(),"λ\0".into()];let x=ZetaFunctorWitness::new(raw.clone(),q);
 assert_eq!(x.primitive_orbits,raw);assert_eq!(x.finite_euler_product.numer(),&numerator.into());assert_eq!(x.finite_euler_product.denom(),&denominator.into());
 let copy=x.clone();assert_eq!(copy.finite_euler_product.numer(),x.finite_euler_product.numer());assert_eq!(copy.finite_euler_product.denom(),x.finite_euler_product.denom());
}}}
''',
"density_matrix_functor": r'''
#[test] fn defined_nonnegative_mass() {for label in [""," \t\n","\u{2003}"," x ","\0λ"] {for n in [-2,0,2] {for d in [-2,0,2] {
 let q=num_rational::BigRational::new_raw(n.into(),d.into());let result=DensityMatrixFunctorWitness::new(label,q);
 if [""," \t\n","\u{2003}"].contains(&label) {assert_eq!(result.unwrap_err(),"empty residual label");}
 else if d<=0 || n<0 {assert_eq!(result.unwrap_err(),"weight must be a defined nonnegative rational");}
 else {let x=result.unwrap();assert_eq!(x.residual_label(),label);assert_eq!(x.rank_one_weight().numer(),&n.into());assert_eq!(x.rank_one_weight().denom(),&d.into());assert_eq!(x.clone(),x);}
}}}}
''',
"category_contract_alignment": r'''
#[test] fn explicit_local_table() {
 let expected=[("Category","category","M0"),("Functor","functor","M0"),("NaturalTransformation","natural_transformation","M0"),("Adjunction","adjunction","M1"),("Monad","monad","M1"),("Operad","operad","M1"),("Limit","limit","M1"),("Colimit","colimit","M1"),("Coend","coend","M2"),("End","end","M2")];
 let constants=[CONTRACT_CATEGORY,CONTRACT_FUNCTOR,CONTRACT_NATURAL_TRANSFORMATION,CONTRACT_ADJUNCTION,CONTRACT_MONAD,CONTRACT_OPERAD,CONTRACT_LIMIT,CONTRACT_COLIMIT,CONTRACT_COEND,CONTRACT_END];
 let mut records=CategoryContractBinding::default_category_bindings();assert_eq!(records.len(),10);
 for (i,(concept,stem,stratum)) in expected.iter().enumerate() {let urn=format!("urn:omega:math:{}:v0.1.0",stem);assert_eq!(constants[i],urn);assert_eq!(records[i],CategoryContractBinding{concept_name:concept.to_string(),contract_urn:urn,mechanization_stratum:stratum.to_string(),is_active:true});}
 records[0].concept_name.clear();assert_eq!(CategoryContractBinding::default_category_bindings()[0].concept_name,"Category");
}
'''
}


def challenge(subject):
    if Path(subject['path']).stem == 'family_category':
        from family_challenges import challenge as family_challenge
        return family_challenge(subject)
    if Path(subject['path']).stem == 'finite_path':
        from path_challenges import challenge as path_challenge
        return path_challenge(subject)
    if Path(subject['path']).stem == 'finite_partial_structure':
        from partial_structure_challenges import challenge as partial_structure_challenge
        return partial_structure_challenge(subject)
    if Path(subject['path']).stem == 'finite_moore':
        from moore_challenges import challenge as moore_challenge
        return moore_challenge(subject)
    if Path(subject['path']).stem == 'finite_continuation':
        from continuation_challenges import challenge as continuation_challenge
        return continuation_challenge(subject)
    if Path(subject['path']).stem == 'finite_profunctor':
        from finite_profunctor_challenges import challenge as profunctor_challenge
        return profunctor_challenge(subject)
    if subject.get('catalog_modules') is not None:
        from root_catalog_challenges import challenge as catalog_challenge
        return catalog_challenge(subject)
    if Path(subject['path']).stem == 'condensation':
        from finite_condensation_challenges import challenge as condensation_challenge
        return condensation_challenge(subject)
    if Path(subject['path']).stem == 'coend':
        from finite_coend_challenges import challenge as coend_challenge
        return coend_challenge(subject)
    if Path(subject['path']).stem == 'cauchy':
        from finite_cauchy_challenges import challenge as cauchy_challenge
        return cauchy_challenge(subject)
    if Path(subject['path']).stem == 'finite_groupoid':
        from finite_groupoid_challenges import challenge as groupoid_challenge
        return groupoid_challenge(subject)
    if Path(subject['path']).stem == 'dagger':
        from finite_dagger_challenges import challenge as dagger_challenge
        return dagger_challenge(subject)
    if Path(subject['path']).stem == 'finite_trace':
        from finite_trace_challenges import challenge as trace_challenge
        return trace_challenge(subject)
    if Path(subject['path']).stem == 'finite_independence':
        from independence import challenge as swap_challenge
        return swap_challenge(subject)
    if Path(subject['path']).stem == 'finite_simulation':
        from simulation import challenge as simulation_challenge
        return simulation_challenge(subject)
    if Path(subject['path']).stem == 'finite_joint_carrier':
        from joint_carrier import challenge as joint_challenge
        return joint_challenge(subject)
    if Path(subject['path']).stem == 'grothendieck_construction':
        from archival_inventory import challenge as archival_challenge
        return archival_challenge(subject)
    if Path(subject['path']).stem in ('natural_trans','natural_trans_composition'):
        from natural_transformations import challenge as naturality_challenge
        return naturality_challenge(subject)
    if Path(subject['path']).stem in ('cat_functor','finite_category_validation','functor_composition'):
        from functor_certificates import challenge as admission_challenge
        return admission_challenge(subject)
    if Path(subject['path']).stem in ('validation','arrow','finite_category_builder','eilenberg_moore','lawvere','higher_functor'):
        from category_diagnostics import challenge as diagnostics_challenge
        return diagnostics_challenge(subject)
    return '\n#[cfg(test)] mod independent_record_tests { use super::*;\n'+ORACLES[Path(subject['path']).stem]+'\n}\n'


def variants(subject, source):
    for index, (needle, replacement) in enumerate(subject['faults']):
        if source.count(needle) != 1:
            raise ValueError('Ambiguous fault: '+subject['path']+' '+needle)
        yield str(index),source.replace(needle,replacement,1),needle,replacement
