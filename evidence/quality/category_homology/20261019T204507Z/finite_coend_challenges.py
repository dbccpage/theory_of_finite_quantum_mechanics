"""Concrete unique-tag class-index regression, before and after repair."""

REGRESSION = r'''
#[test] fn class_labels_address_the_returned_partition() {
 let input=CoendInput{objects:vec!["A".into(),"B".into()],morphisms:vec![("f".into(),"A".into(),"B".into())],
  diagonal:BTreeMap::from([("A".into(),vec![10usize,11]),("B".into(),vec![12])]),
  forward_action:BTreeMap::from([("f".into(),vec![(0,0),(1,0)])]),backward_action:BTreeMap::from([("f".into(),vec![(0,0)])])};
 assert!(validate_coend_input(&input).is_empty());let out=DeclaredFiniteCoend::compute(&input);assert_eq!(out.classes.len(),1);
 for (tag,&class) in &out.class_of{assert!(class<out.classes.len(),"tag{tag:?} has class{class},but only{} returned classes",out.classes.len());assert!(out.classes[class].iter().any(|x|(&x.object,x.index)==(&tag.0,tag.1)));}
 assert_eq!(out.class_of[&("A".into(),0)],0);assert_eq!(out.class_of[&("A".into(),1)],0);assert_eq!(out.class_of[&("B".into(),0)],0);
}
'''


ORACLES = r'''
fn oracle(input:&CoendInput<usize>)->(Vec<Vec<TaggedDiagonal<usize>>>,BTreeMap<(String,usize),usize>,Vec<DinaturalityWitness>){
 let mut tags=Vec::new();
 for o in &input.objects{if let Some(values)=input.diagonal.get(o){for (i,&value) in values.iter().enumerate(){if !tags.iter().any(|x:&TaggedDiagonal<usize>|x.object==*o&&x.index==i){tags.push(TaggedDiagonal{object:o.clone(),index:i,value});}}}}
 let n=tags.len();let mut reach=vec![vec![false;n];n];for i in 0..n{reach[i][i]=true;}let mut witnesses=Vec::new();
 for (name,source,target) in &input.morphisms{if let (Some(f),Some(b))=(input.forward_action.get(name),input.backward_action.get(name)){for &(i,s) in f{for &(j,t) in b{if s!=t{continue;}let a=tags.iter().position(|x|x.object==*source&&x.index==i);let z=tags.iter().position(|x|x.object==*target&&x.index==j);if let (Some(a),Some(z))=(a,z){reach[a][z]=true;reach[z][a]=true;witnesses.push(DinaturalityWitness{morphism:name.clone(),source_object:source.clone(),target_object:target.clone(),forward_index:i,backward_index:j});}}}}}
 // Independent Boolean Floyd-Warshall closure, not the producer's graph/worklist.
 for k in 0..n{for i in 0..n{for j in 0..n{reach[i][j]|=reach[i][k]&&reach[k][j];}}}
 let mut classes:Vec<Vec<TaggedDiagonal<usize>>>=Vec::new();let mut labels=BTreeMap::new();let mut roots=Vec::new();
 for i in 0..n{let root=(0..n).find(|&j|reach[i][j]).unwrap();let class=if let Some(c)=roots.iter().position(|&r|r==root){c}else{roots.push(root);classes.push(Vec::new());classes.len()-1};labels.insert((tags[i].object.clone(),tags[i].index),class);classes[class].push(tags[i].clone());}
 (classes,labels,witnesses)
}
fn check_partition(input:&CoendInput<usize>){
 let out=DeclaredFiniteCoend::compute(input);let (classes,labels,witnesses)=oracle(input);
 assert_eq!(out.objects,input.objects);assert_eq!(out.contributions,input.diagonal);assert_eq!(out.classes,classes);assert_eq!(out.class_of,labels);assert_eq!(out.identifications,witnesses);
 for (tag,&c) in &out.class_of{assert!(c<out.classes.len());assert_eq!(out.classes[c].iter().filter(|x|x.object==tag.0&&x.index==tag.1).count(),1);}
 assert!(out.classes.iter().all(|c|!c.is_empty()));
}
fn graph_input(n:usize,edges:&[(usize,usize)])->CoendInput<usize>{
 let mut input=CoendInput{objects:vec!["A".into()],morphisms:Vec::new(),diagonal:BTreeMap::from([("A".into(),vec![7;n])]),forward_action:BTreeMap::new(),backward_action:BTreeMap::new()};
 for (k,&(a,b)) in edges.iter().enumerate(){let name=format!("e{k}");input.morphisms.push((name.clone(),"A".into(),"A".into()));input.forward_action.insert(name.clone(),vec![(a,usize::MAX)]);input.backward_action.insert(name,vec![(b,usize::MAX)]);}
 input
}
#[test] fn all_five_vertex_graphs_and_direction_orders(){
 let possible:Vec<_>=(0..5).flat_map(|i|(i+1..5).map(move|j|(i,j))).collect();
 for mask in 0usize..1024{let edges:Vec<_>=possible.iter().enumerate().filter_map(|(k,&e)|((mask>>k)&1==1).then_some(e)).collect();check_partition(&graph_input(5,&edges));let reversed:Vec<_>=edges.iter().rev().map(|&(a,b)|(b,a)).collect();check_partition(&graph_input(5,&reversed));}
 check_partition(&graph_input(0,&[]));check_partition(&graph_input(1,&[(0,0),(0,0)]));
}
#[test] fn matched_slots_duplicates_unknown_tags_and_metadata(){
 let atoms=[(0,0),(1,0),(0,1),(1,1),(9,0),(0,usize::MAX)];
 for a in 0..6{for b in 0..6{for c in 0..6{for d in 0..6{
  let input=CoendInput{objects:vec!["B".into(),"A".into(),"B".into(),"missing".into()],morphisms:vec![("f".into(),"A".into(),"B".into()),("f".into(),"A".into(),"B".into()),("absent".into(),"A".into(),"B".into()),("unknown".into(),"X".into(),"A".into())],diagonal:BTreeMap::from([("A".into(),vec![4,4]),("B".into(),vec![4,4]),("X".into(),vec![88])]),forward_action:BTreeMap::from([("f".into(),vec![atoms[a],atoms[b]]),("unknown".into(),vec![(0,0)])]),backward_action:BTreeMap::from([("f".into(),vec![atoms[c],atoms[d]]),("unknown".into(),vec![(0,0)])])};check_partition(&input);
 }}}}
 // Empty and Unicode/NUL labels are literal; repeated names retain one tag.
 let mut input=graph_input(2,&[]);input.objects=vec!["\0λ".into(),"".into(),"\0λ".into()];input.diagonal=BTreeMap::from([("\0λ".into(),vec![1,1]),("".into(),vec![1])]);check_partition(&input);
}
fn diagnostic_oracle(out:&DeclaredFiniteCoend<usize>,input:&CoendInput<usize>)->Vec<String>{
 let mut errors=Vec::new();for (name,source,target) in &input.morphisms{if let (Some(f),Some(b))=(input.forward_action.get(name),input.backward_action.get(name)){for &(i,s) in f{for &(j,t) in b{if s==t{match(out.class_of.get(&(source.clone(),i)),out.class_of.get(&(target.clone(),j))){(Some(x),Some(y)) if x==y=>{},(Some(x),Some(y))=>errors.push(format!("Dinaturality violated: {} and {} via morphism {} mapped to different classes ({} vs {})",i,j,name,x,y)),_=>errors.push(format!("Dinaturality: missing class mapping for elements involved in morphism {}",name))}}}}}}errors
}
#[test] fn diagnostics_compare_labels_only_and_presence_order(){
 let mut input=graph_input(3,&[(0,1),(1,2),(2,2)]);input.morphisms.push(("e0".into(),"A".into(),"A".into()));
 for mask in 0usize..64{let mut out=DeclaredFiniteCoend::compute(&input);out.class_of.clear();for i in 0..3{let state=(mask>>(i*2))&3;if state!=0{out.class_of.insert(("A".into(),i),[0,0,1,usize::MAX][state]);}}assert_eq!(check_dinaturality(&out,&input),diagnostic_oracle(&out,&input));}
 let mut forged=DeclaredFiniteCoend::compute(&input);for v in forged.class_of.values_mut(){*v=usize::MAX;}forged.classes.clear();assert!(check_dinaturality(&forged,&input).is_empty(),"local labels are not a certificate");
 input.objects=vec!["missing".into(),"missing".into(),"A".into()];input.morphisms=vec![("z".into(),"A".into(),"A".into()),("y".into(),"A".into(),"A".into())];input.forward_action.insert("y".into(),Vec::new());input.backward_action.insert("z".into(),Vec::new());
 assert_eq!(validate_coend_input(&input),vec!["Missing diagonal contribution for object missing","Missing diagonal contribution for object missing","Missing forward action for morphism z","Missing backward action for morphism y"]);
 input.forward_action.insert("z".into(),vec![(usize::MAX,0)]);input.backward_action.insert("y".into(),vec![(usize::MAX,0)]);assert_eq!(validate_coend_input(&input).len(),2);check_partition(&input);
}
#[test] fn iterative_long_reverse_chain(){
 let n=10000;let edges:Vec<_>=(0..n-1).map(|i|(i+1,i)).collect();let input=graph_input(n,&edges);let out=DeclaredFiniteCoend::compute(&input);
 assert_eq!(out.classes.len(),1);assert_eq!(out.classes[0].len(),n);assert_eq!(out.identifications.len(),n-1);assert!(out.class_of.values().all(|&x|x==0));for (i,x) in out.classes[0].iter().enumerate(){assert_eq!(x.index,i);}
}
#[test] fn payload_callbacks_only_required_clones(){
 use std::rc::Rc;use std::cell::Cell;use std::hash::{Hash,Hasher};
 struct Value{value:usize,clones:Rc<Cell<usize>>,compares:Rc<Cell<usize>>,hashes:Rc<Cell<usize>>}
 impl Clone for Value{fn clone(&self)->Self{self.clones.set(self.clones.get()+1);Self{value:self.value,clones:self.clones.clone(),compares:self.compares.clone(),hashes:self.hashes.clone()}}}
 impl PartialEq for Value{fn eq(&self,other:&Self)->bool{self.compares.set(self.compares.get()+1);self.value==other.value}}impl Eq for Value{}
 impl Hash for Value{fn hash<H:Hasher>(&self,state:&mut H){self.hashes.set(self.hashes.get()+1);self.value.hash(state);}}
 let clones=Rc::new(Cell::new(0));let compares=Rc::new(Cell::new(0));let hashes=Rc::new(Cell::new(0));let make=|value|Value{value,clones:clones.clone(),compares:compares.clone(),hashes:hashes.clone()};
 let input=CoendInput{objects:vec!["A".into(),"A".into()],morphisms:Vec::new(),diagonal:BTreeMap::from([("A".into(),vec![make(0),make(0)]),("extra".into(),vec![make(9)])]),forward_action:BTreeMap::new(),backward_action:BTreeMap::new()};
 let out=DeclaredFiniteCoend::compute(&input);assert_eq!(out.classes.len(),2);assert_eq!(out.classes[0][0].value.value,0);assert_eq!(out.contributions["extra"][0].value,9);assert_eq!(clones.get(),5);assert_eq!(compares.get(),0);assert_eq!(hashes.get(),0);
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_coend_tests {use super::*;\n'+REGRESSION+ORACLES+'\n}\n'
