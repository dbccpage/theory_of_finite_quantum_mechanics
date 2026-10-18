/*
// grothendieck_construction.rs
// The Grothendieck Construction: Category of Elements and Fibrations

use std::collections::HashMap;
use std::fmt::Debug;
use std::hash::{Hash, Hasher};
use std::rc::Rc;

use crate::core::Category;
use crate::arrow::Morph;
use crate::arrow::Obj;

/// A set-valued functor F: C → Set
/// Represented as a trait object to allow dynamic mapping.
pub trait SetValuedFunctor<C: Category> {
    type Element: Obj;

    /// Apply F to an object in C, returning the set (as Vec of elements)
    fn obj_map(&self, c: &C::Obj) -> Vec<Self::Element>;

    /// Apply F to a morphism f: A → B in C
    /// Returns function F(f): F(A) → F(B) as a map over elements
    fn morph_map(&self, f: &Morph<C::Obj, C::Obj>, x: &Self::Element) -> Option<Self::Element>;
}

/// Object in the category of elements ∫F
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ElementObj<CObj: Obj, E: Obj> {
    pub base: CObj, // c : C
    pub elem: E,    // x ∈ F(c)
}

impl<CObj: Obj, E: Obj> Obj for ElementObj<CObj, E> {}

/// Morphism in ∫F: (c, x) → (d, y)
/// Given by f: c → d in C such that F(f)(x) = y
#[derive(Debug, Clone)]
pub struct ElementMorph<CObj: Obj, E: Obj> {
    pub domain: ElementObj<CObj, E>,
    pub codomain: ElementObj<CObj, E>,
    pub base_morph: Morph<CObj, CObj>, // f: c → d
}

impl<CObj: Obj, E: Obj> PartialEq for ElementMorph<CObj, E> {
    fn eq(&self, other: &Self) -> bool {
        self.domain == other.domain && self.codomain == other.codomain
    }
}
impl<CObj: Obj, E: Obj> Eq for ElementMorph<CObj, E> {}
impl<CObj: Obj, E: Obj> Hash for ElementMorph<CObj, E> {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.domain.hash(state);
        self.codomain.hash(state);
    }
}

/// Category of Elements ∫F
pub struct CategoryOfElements<C: Category, F: SetValuedFunctor<C>> {
    category: C,
    functor: F,
    _phantom: std::marker::PhantomData<(C, F)>,
}

impl<C, F> CategoryOfElements<C, F>
where
    C: Category,
    F: SetValuedFunctor<C>,
{
    pub fn new(category: C, functor: F) -> Self {
        Self {
            category,
            functor,
            _phantom: std::marker::PhantomData,
        }
    }

    /// Check if a morphism is valid in ∫F
    pub fn is_valid_morphism(&self, morph: &ElementMorph<C::Obj, F::Element>) -> bool {
        // Base morphism must exist
        let f = &morph.base_morph;
        if f.from != morph.domain.base || f.to != morph.codomain.base {
            return false;
        }

        // Must satisfy F(f)(x) = y
        match self.functor.morph_map(f, &morph.domain.elem) {
            Some(image) => image == morph.codomain.elem,
            None => false,
        }
    }

    /// Construct a morphism if valid
    pub fn morph(
        &self,
        domain: ElementObj<C::Obj, F::Element>,
        codomain: ElementObj<C::Obj, F::Element>,
        base_morph: Morph<C::Obj, C::Obj>,
    ) -> Option<ElementMorph<C::Obj, F::Element>> {
        let morph = ElementMorph {
            domain: domain.clone(),
            codomain: codomain.clone(),
            base_morph: base_morph.clone(),
        };
        if self.is_valid_morphism(&morph) {
            Some(morph)
        } else {
            None
        }
    }
}

impl<C, F> Category for CategoryOfElements<C, F>
where
    C: Category,
    F: SetValuedFunctor<C>,
    C::Obj: Clone + Eq,
    F::Element: Clone + Eq,
{
    type Obj = ElementObj<C::Obj, F::Element>;

    fn compose<A, B, D>(f: &Morph<A, B>, g: &Morph<B, D>) -> Option<Morph<A, D>>
    where
        A: Obj,
        B: Obj,
        D: Obj,
    {
        // Cast to concrete types
        let f_elem =
            unsafe { std::mem::transmute::<&Morph<A, B>, &ElementMorph<C::Obj, F::Element>>(f) };
        let g_elem =
            unsafe { std::mem::transmute::<&Morph<B, D>, &ElementMorph<C::Obj, F::Element>>(g) };

        if f_elem.codomain != g_elem.domain {
            return None;
        }

        let base_composed = C::compose(&f_elem.base_morph, &g_elem.base_morph)?;
        let composed = ElementMorph {
            domain: f_elem.domain.clone(),
            codomain: g_elem.codomain.clone(),
            base_morph: base_composed,
        };

        Some(Morph {
            from: unsafe { std::mem::transmute_copy(&composed.domain) },
            to: unsafe { std::mem::transmute_copy(&composed.codomain) },
            _phantom: Rc::new(()),
        })
    }

    fn id(x: Self::Obj) -> Morph<Self::Obj, Self::Obj> {
        let base_id = C::id(x.base.clone());
        Morph {
            from: x.clone(),
            to: x,
            _phantom: Rc::new(()),
        }
    }
}

// ===============================================
// GROTHENDIECK FIBRATION

/*
impl<C, F> Fibration for CategoryOfElements<C, F>
where
    C: Category,
    F: SetValuedFunctor<C>,
    C::Obj: Clone + Eq,
    F::Element: Clone + Eq + Hash,
{
    type TotalObj = ElementObj<C::Obj, F::Element>;
    type BaseObj = C::Obj;

    fn proj_obj(&self, e: &Self::TotalObj) -> Self::BaseObj {
        e.base.clone()
    }

    /// Cartesian lift: given u: I → J in C, and an object (J, y) in ∫F,
    /// lift to (I, x) → (J, y) where x must satisfy F(u)(x) = y
    /// But cartesian lift must be *universal* — so we require x such that
    /// for any v: K → I and z with F(u∘v)(z) = y, there is unique lift.
    ///
    /// In ∫F, cartesian morphisms are precisely those where
    /// the underlying F(u)(x) = y and x is "universal" — i.e., **any** preimage suffices,
    /// but we pick one if exists.
    ///
    /// Actually: **all pullbacks along u are cartesian** in ∫F.
    fn cartesian_lift(
        &self,
        u: &Morph<Self::BaseObj, Self::BaseObj>,
        e: &Self::TotalObj,
    ) -> Option<(Morph<Self::TotalObj, Self::TotalObj>, Self::TotalObj)> {
        // e = (J, y), u: I → J
        // We want x ∈ F(I) such that F(u)(x) = y
        let candidates = self.functor.obj_map(&u.from);
        for x in candidates {
            if let Some(image) = self.functor.morph_map(u, &x) {
                if image == e.elem {
                    let domain = ElementObj {
                        base: u.from.clone(),
                        elem: x,
                    };
                    let phi = ElementMorph {
                        domain: domain.clone(),
                        codomain: e.clone(),
                        base_morph: u.clone(),
                    };
                    let morph = Morph {
                        from: domain.clone(),
                        to: e.clone(),
                        _phantom: Rc::new(()),
                    };
                    return Some((morph, domain));
                }
            }
        }
        None
    }
}

impl<C, F> Opfibration for CategoryOfElements<C, F>
where
    C: Category,
    F: SetValuedFunctor<C>,
    C::Obj: Clone + Eq,
    F::Element: Clone + Eq,
{
    type TotalObj = ElementObj<C::Obj, F::Element>;
    type BaseObj = C::Obj;

    fn proj_obj(&self, e: &Self::TotalObj) -> Self::BaseObj {
        e.base.clone()
    }

    /// Cocartesian lift: given u: I → J and (I, x), find (I, x) → (J, y)
    /// such that y = F(u)(x), if defined
    fn cocartesian_lift(
        &self,
        u: &Morph<Self::BaseObj, Self::BaseObj>,
        e: &Self::TotalObj,
    ) -> Option<(Morph<Self::TotalObj, Self::TotalObj>, Self::TotalObj)> {
        let y = self.functor.morph_map(u, &e.elem)?;
        let codomain = ElementObj {
            base: u.to.clone(),
            elem: y,
        };
        let morph = Morph {
            from: e.clone(),
            to: codomain.clone(),
            _phantom: Rc::new(()),
        };
        Some((morph, codomain))
    }
}
*/

// ===============================================
// Example: Presheaf of Colors over a Category

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Node {
    A,
    B,
}

impl Obj for Node {}

pub struct BaseCategory<O: Obj> {
    pub _phantom: std::marker::PhantomData<O>,
}

impl Category for BaseCategory<Node> {
    type Obj = Node;

    fn compose<A: Obj, B: Obj, C: Obj>(f: &Morph<A, B>, g: &Morph<B, C>) -> Option<Morph<A, C>> {
        // Safety: only one object type
        let f_node = unsafe { std::mem::transmute_copy::<A, Node>(&f.from) };
        let f_to = unsafe { std::mem::transmute_copy::<B, Node>(&f.to) };
        let g_from = unsafe { std::mem::transmute_copy::<B, Node>(&g.from) };
        let g_to = unsafe { std::mem::transmute_copy::<C, Node>(&g.to) };

        if f_to == g_from {
            Some(Morph {
                from: unsafe { std::mem::transmute_copy(&f_node) },
                to: unsafe { std::mem::transmute_copy(&g_to) },
                _phantom: Rc::new(()),
            })
        } else {
            None
        }
    }

    fn id(x: Node) -> Morph<Node, Node> {
        Morph {
            from: x.clone(),
            to: x,
            _phantom: Rc::new(()),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Color {
    Red,
    Blue,
    Green,
}

impl Obj for Color {}

// Functor F: C → Set, where F(A) = {Red, Blue}, F(B) = {Green}
// and F(f: A → B) sends Red → Green, Blue → Green

pub struct ColorFunctor;

impl SetValuedFunctor<BaseCategory<Node>> for ColorFunctor {
    type Element = Color;

    fn obj_map(&self, c: &Node) -> Vec<Color> {
        match c {
            Node::A => vec![Color::Red, Color::Blue],
            Node::B => vec![Color::Green],
        }
    }

    fn morph_map(&self, f: &Morph<Node, Node>, x: &Color) -> Option<Color> {
        // Only one non-id morphism: A → B
        if f.from == Node::A && f.to == Node::B {
            match x {
                Color::Red | Color::Blue => Some(Color::Green),
                _ => None,
            }
        } else {
            None // No other morphisms defined
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /*
    #[test]
    fn test_grothendieck_cartesian_lift() {
        let base = BaseCategory {
            _phantom: std::marker::PhantomData,
        };
        let functor = ColorFunctor;
        let fib = CategoryOfElements::new(base, functor);

        let b_green = ElementObj {
            base: Node::B,
            elem: Color::Green,
        };

        let u = Morph {
            from: Node::A,
            to: Node::B,
            _phantom: Rc::new(()),
        };

        let result = fib.cartesian_lift(&u, &b_green);
        assert!(result.is_some());
        let (lift, domain) = result.unwrap();

        assert_eq!(lift.to, b_green);
        assert!(matches!(domain.elem, Color::Red | Color::Blue));
        assert_eq!(domain.base, Node::A);
    }

    #[test]
    fn test_grothendieck_cocartesian_lift() {
        let base = BaseCategory {
            _phantom: std::marker::PhantomData,
        };
        let functor = ColorFunctor;
        let opfib = CategoryOfElements::new(base, functor);

        let a_red = ElementObj {
            base: Node::A,
            elem: Color::Red,
        };

        let u = Morph {
            from: Node::A,
            to: Node::B,
            _phantom: Rc::new(()),
        };

        let result = opfib.cocartesian_lift(&u, &a_red);
        assert!(result.is_some());
        let (lift, codomain) = result.unwrap();

        assert_eq!(lift.from, a_red);
        assert_eq!(codomain.elem, Color::Green);
        assert_eq!(codomain.base, Node::B);
    }
    */
}


*/
