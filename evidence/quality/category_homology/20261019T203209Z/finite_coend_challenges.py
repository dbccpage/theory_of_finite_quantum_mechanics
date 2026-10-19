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


def challenge(subject):
    return '\n#[cfg(test)] mod independent_coend_tests {use super::*;\n'+REGRESSION+'\n}\n'
