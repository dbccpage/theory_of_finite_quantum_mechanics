"""Inline catalog defaults/metadata only; canonical children are actual providers."""

TESTS = r'''
#[derive(Clone,Debug)]struct Morphism{value:u8,calls:std::rc::Rc<std::cell::Cell<usize>>}
impl PartialEq for Morphism{fn eq(&self,other:&Self)->bool{self.calls.set(self.calls.get()+1);self.value==other.value}}impl Eq for Morphism{}
struct Raw;
impl core::Category for Raw{type Ob=();type Mor=Morphism;
 fn identity<A>(_:&A)->Self::Mor{Morphism{value:99,calls:Default::default()}}
 fn compose<A,B,C>(_:&Self::Mor,_:&Self::Mor)->Option<Self::Mor>{None}}
impl core::MorphismEq for Raw{}
#[test]fn default_delegates_exactly_once_to_value_equality(){
 use super::core::MorphismEq;
 let calls=std::rc::Rc::new(std::cell::Cell::new(0));for a in 0..3{for b in 0..3{let left=Morphism{value:a,calls:calls.clone()};let right=Morphism{value:b,calls:calls.clone()};let before=calls.get();assert_eq!(Raw::morphism_eq::<(),String>(&left,&right),a==b);assert_eq!(calls.get(),before+1);}}
 assert_eq!(calls.get(),9);
}
#[test]fn labels_and_one_conversion_are_metadata(){
 use std::cell::Cell;use std::rc::Rc;
 struct Input{label:String,calls:Rc<Cell<usize>>}impl From<Input> for String{fn from(input:Input)->String{input.calls.set(input.calls.get()+1);input.label}}
 let calls=Rc::new(Cell::new(0));for label in [""," "," x\n","λ\0","not-a-proof"]{let before=calls.get();let value=witness::Witness::new(Input{label:label.into(),calls:calls.clone()});assert_eq!(value.name,label);assert_eq!(calls.get(),before+1);assert_eq!(value.clone(),value);let mut other=value.clone();other.name.push('!');assert_ne!(other,value);}
 assert_eq!(calls.get(),5);
}
#[test]fn traits_are_unchecked_signatures_and_error_payloads(){
 use super::core::Category;use law::Law;
 let id=Raw::identity(&"arbitrary");assert_eq!(id.value,99);assert!(Raw::compose::<(),(),()>(&id,&id).is_none(),"traits do not admit identity/category laws");
 impl monoidal_category::MonoidalCategory for Raw{type TensorProduct<A,B>=();fn unit()->Self::Ob{()}}
 impl braided_monoidal::BraidedMonoidalCategory for Raw{fn braiding<A,B>()->Self::Mor{Raw::identity(&())}}
 struct RawLaw;impl law::Law for RawLaw{type Subject=bool;fn check(s:&bool)->Result<witness::Witness,errors::ArithmosError>{if *s{Ok(witness::Witness::new("caller assertion"))}else{Err(errors::ArithmosError::PreconditionFailed("refused".into()))}}}
 assert_eq!(RawLaw::check(&true).unwrap().name,"caller assertion");assert_eq!(RawLaw::check(&false),Err(errors::ArithmosError::PreconditionFailed("refused".into())));
 for label in ["","λ\0"]{let values=[errors::ArithmosError::LawViolation(label.into()),errors::ArithmosError::PreconditionFailed(label.into()),errors::ArithmosError::InvalidShape(label.into())];assert_ne!(values[0],values[1]);assert_ne!(values[1],values[2]);for v in values{assert_eq!(v.clone(),v);}}
 // Rebound children retain canonical provider identity in this narrow adapter.
 assert_eq!(std::any::TypeId::of::<finite_continuation::PartialDynamics>(),std::any::TypeId::of::<crate::finite_continuation::PartialDynamics>());
 assert_eq!(std::any::TypeId::of::<errors::ArithmosError>(),std::any::TypeId::of::<errors::ArithmosError>());
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_catalog_tests {use super::*;\n'+TESTS+'\n}\n'
