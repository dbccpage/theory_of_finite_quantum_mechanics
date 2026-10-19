//! Generic callback adapters, finite algebra observations and Maybe transport.
//! AuthorityEffect: None. Monad/Eq/Clone are caller contracts, not checked laws.
//! Samples establish only their evaluated observations; empty samples are vacuous.
//! Callback purity, termination, panic/drop behavior and external effects remain
//! caller boundaries. Marker/printer adapters do not construct a category in D.

use std::fmt::Debug;

/// A trait representing types as objects in a category.
pub trait Obj: Clone + Debug + 'static {}

// Blanket implementation for all suitable types
impl<T> Obj for T where T: Clone + Debug + 'static {}

// --------------------------------------------------
// MONAD DEFINITION IN A CATEGORY (Endofunctor with unit and multiplication)
// We work in the category of sets (Set) for simplicity.
// A monad is (T, η, μ) where:
//   T: Set → Set (endofunctor)
//   η: Id → T  (unit)
//   μ: T² → T (multiplication)

/// A monad-shaped interface over Rust types and functions.
/// Implementations must separately justify the mathematical monad laws.
pub trait Monad {
    /// Type constructor: for any type `A`, T<A> is the "wrapped" type.
    type T<A: Obj>: Obj;

    /// Unit (return / pure): A → T<A>
    fn unit<A: Obj>(x: A) -> Self::T<A>;

    /// Bind operation (derived from join and fmap)
    fn bind<A: Obj, B: Obj>(ta: Self::T<A>, f: impl Fn(A) -> Self::T<B>) -> Self::T<B>;

    /// Join (multiplication): T<T<A>> → T<A>
    fn join<A: Obj>(tta: Self::T<Self::T<A>>) -> Self::T<A> {
        Self::bind(tta, |x| x)
    }

    /// fmap: (A → B) → (T<A> → T<B>)
    fn fmap<A: Obj, B: Obj>(f: impl Fn(A) -> B, ta: Self::T<A>) -> Self::T<B>;
}

// --------------------------------------------------
// EILENBERG-MOORE ALGEBRA FOR A MONAD

/// An unchecked candidate action for a monad-like interface `M`.
/// An Eilenberg–Moore algebra is a pair (A, h)
/// where:
///   A: object (carrier)
///   h: T<A> → A  (action morphism)
/// satisfying two laws; this public callback record does not enforce them:
///   1. h ∘ T(h) = h ∘ μ_A     (associativity)
///   2. h ∘ η_A = id_A          (unit law)
pub struct EMAlgebra<M: Monad, A: Obj> {
    pub carrier: Phantom<A>, // Just to carry type info
    pub action: Box<dyn Fn(M::T<A>) -> A>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AlgebraLaw {
    Unit,
    Associativity,
    Morphism,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LawCheckError {
    NonPreservingClone { law: AlgebraLaw, index: usize },
    Violated { law: AlgebraLaw, index: usize },
}

/// Counts of supplied observations, not an exhaustive-domain certificate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AlgebraSampleCheck {
    pub unit_samples: usize,
    pub associativity_samples: usize,
}

fn checked_clone<T: Clone + Eq>(
    value: &T,
    law: AlgebraLaw,
    index: usize,
) -> Result<T, LawCheckError> {
    let copy = value.clone();
    if copy != *value {
        return Err(LawCheckError::NonPreservingClone { law, index });
    }
    Ok(copy)
}

// We use a phantom to avoid storing data
#[derive(Debug, Clone)]
pub struct Phantom<T>(std::marker::PhantomData<T>);
impl<T> Phantom<T> {
    fn new() -> Self {
        Phantom(std::marker::PhantomData)
    }
}

impl<M: Monad, A: Obj> EMAlgebra<M, A> {
    /// No domain was supplied, so this legacy method establishes no laws.
    /// False means unverified here, not a mathematical counterexample.
    #[deprecated(
        note = "No input domain: always unverified. Use check_samples for finite observations."
    )]
    pub fn verify_laws(&self) -> bool
    where
        A: Clone + Eq,
        M::T<A>: Clone + Eq,
        M::T<M::T<A>>: Clone,
    {
        false
    }

    /// Evaluate unit samples first, then associativity samples, in caller order.
    /// Clone must preserve each shared input under the supplied Eq contract.
    /// Success covers these observations only, even if both vectors are empty.
    pub fn check_samples(
        &self,
        unit_samples: Vec<A>,
        associativity_samples: Vec<M::T<M::T<A>>>,
    ) -> Result<AlgebraSampleCheck, LawCheckError>
    where
        A: Eq,
        M::T<M::T<A>>: Eq,
    {
        let observed = AlgebraSampleCheck {
            unit_samples: unit_samples.len(),
            associativity_samples: associativity_samples.len(),
        };
        for (index, value) in unit_samples.into_iter().enumerate() {
            let copy = checked_clone(&value, AlgebraLaw::Unit, index)?;
            if (self.action)(M::unit::<A>(copy)) != value {
                return Err(LawCheckError::Violated {
                    law: AlgebraLaw::Unit,
                    index,
                });
            }
        }
        for (index, value) in associativity_samples.into_iter().enumerate() {
            let copy = checked_clone(&value, AlgebraLaw::Associativity, index)?;
            let left = (self.action)(M::fmap::<M::T<A>, A>(|ta| (self.action)(ta), copy));
            let right = (self.action)(M::join::<A>(value));
            if left != right {
                return Err(LawCheckError::Violated {
                    law: AlgebraLaw::Associativity,
                    index,
                });
            }
        }
        Ok(observed)
    }
}

// --------------------------------------------------
// CATEGORY OF EILENBERG-MOORE ALGEBRAS

/// A morphism between two EM algebras (A, h) and (B, k) is a function f: A → B
/// such that f ∘ h = k ∘ T(f). This record stores an unchecked candidate.
pub struct AlgebraMorphism<M: Monad, A: Obj, B: Obj> {
    f: Box<dyn Fn(A) -> B>,
    _phantom: Phantom<(M, A, B)>,
}

impl<M: Monad, A: Obj, B: Obj> std::fmt::Debug for AlgebraMorphism<M, A, B> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("AlgebraMorphism").finish()
    }
}

impl<M: Monad, A: Obj, B: Obj> AlgebraMorphism<M, A, B> {
    pub fn new(f: impl Fn(A) -> B + 'static) -> Self {
        Self {
            f: Box::new(f),
            _phantom: Phantom(std::marker::PhantomData),
        }
    }

    /// Without a supplied domain no preservation law has been established.
    #[deprecated(
        note = "No input domain: always unverified. Use check_samples for finite observations."
    )]
    pub fn respects_algebras(&self, _dom: &EMAlgebra<M, A>, _cod: &EMAlgebra<M, B>) -> bool
    where
        A: Clone,
        B: Clone + Eq,
        M::T<A>: Clone,
        M::T<B>: Clone,
    {
        false
    }

    /// Count successful supplied preservation observations; no exhaustive claim.
    pub fn check_samples(
        &self,
        dom: &EMAlgebra<M, A>,
        cod: &EMAlgebra<M, B>,
        samples: Vec<M::T<A>>,
    ) -> Result<usize, LawCheckError>
    where
        B: Eq,
        M::T<A>: Eq,
    {
        let count = samples.len();
        for (index, value) in samples.into_iter().enumerate() {
            let copy = checked_clone(&value, AlgebraLaw::Morphism, index)?;
            let left = (self.f)((dom.action)(copy));
            let right = (cod.action)(M::fmap::<A, B>(&self.f, value));
            if left != right {
                return Err(LawCheckError::Violated {
                    law: AlgebraLaw::Morphism,
                    index,
                });
            }
        }
        Ok(count)
    }
}

// --------------------------------------------------
// FREE FORGETFUL ADJUNCTION AND MONAD DERIVATION

/// Marker for the intended forgetful role. `map` only builds a label printer;
/// it does not extract a carrier value or establish a categorical functor.
#[derive(Debug)]
pub struct ForgetfulFunctor<M: Monad>(Phantom<M>);

impl<M: Monad> Default for ForgetfulFunctor<M> {
    fn default() -> Self {
        Self::new()
    }
}

impl<M: Monad> ForgetfulFunctor<M> {
    pub fn new() -> Self {
        Self(Phantom::new())
    }

    /// Return a fixed carrier-description printer, not a carrier object or map.
    pub fn map<A: Obj + 'static>(&self, alg: &EMAlgebra<M, A>) -> Box<dyn Fn() -> String> {
        // We can't return A directly due to typing, so we return a printer
        let _ = alg;
        Box::new(|| "Carrier type A".to_string())
    }
}

/// Free algebra functor F: C → EM(M)
/// For any object A, gives the free algebra (T<A>, μ_A)
#[derive(Debug)]
pub struct FreeAlgebraFunctor<M: Monad>(Phantom<M>);

impl<M: Monad> Default for FreeAlgebraFunctor<M> {
    fn default() -> Self {
        Self::new()
    }
}

impl<M: Monad> FreeAlgebraFunctor<M> {
    pub fn new() -> Self {
        Self(Phantom::new())
    }

    /// Construct the join action; algebra laws require a lawful supplied Monad.
    pub fn map<A: Obj>(&self) -> EMAlgebra<M, M::T<A>>
    where
        M::T<M::T<A>>: 'static,
        M::T<A>: 'static,
    {
        EMAlgebra {
            carrier: Phantom::new(),
            action: Box::new(|tta: M::T<M::T<A>>| M::join(tta)),
        }
    }
}

// --------------------------------------------------
// COMPARISON FUNCTOR K: C^T → D
// In the canonical case: K: EM(M) → D where M arises from adjunction C ⇄ D

/// Type-parameter marker for a proposed comparison role in D.
/// `map` returns descriptive metadata, not an object or categorical functor.
#[derive(Debug)]
pub struct ComparisonFunctor<M: Monad, DObj: Obj> {
    _phantom: Phantom<(M, DObj)>,
}

impl<M: Monad, DObj: Obj> Default for ComparisonFunctor<M, DObj> {
    fn default() -> Self {
        Self::new()
    }
}

impl<M: Monad, DObj: Obj> ComparisonFunctor<M, DObj> {
    pub fn new() -> Self {
        Self {
            _phantom: Phantom::new(),
        }
    }

    /// Return a fixed descriptive label; no object or actual comparison map in D.
    pub fn map<A: Obj + 'static>(&self, _alg: &EMAlgebra<M, A>) -> &'static str {
        "Object in D (via comparison)" // Descriptive metadata only.
    }
}

// --------------------------------------------------
// EXAMPLE: Maybe Monad (Partiality)

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Maybe<T> {
    Just(T),
    Nothing,
}

// NOTE: `Maybe<T>` satisfies `Obj` via the blanket impl when `T: Obj`.

#[derive(Debug)]
pub struct MaybeMonad;
impl Monad for MaybeMonad {
    type T<A: Obj> = Maybe<A>;

    fn unit<A: Obj>(x: A) -> Self::T<A> {
        Maybe::Just(x)
    }

    fn bind<A: Obj, B: Obj>(ta: Maybe<A>, f: impl Fn(A) -> Maybe<B>) -> Maybe<B> {
        match ta {
            Maybe::Just(x) => f(x),
            Maybe::Nothing => Maybe::Nothing,
        }
    }

    fn fmap<A: Obj, B: Obj>(f: impl Fn(A) -> B, ta: Maybe<A>) -> Maybe<B> {
        Self::bind(ta, |a| Self::unit(f(a)))
    }
}

// Example: Trivial algebra on bool: collapse Maybe<bool> to bool
// Define: h(Just b) = b, h(Nothing) = false
#[cfg(test)]
fn bool_algebra() -> EMAlgebra<MaybeMonad, bool> {
    EMAlgebra {
        carrier: Phantom::new(),
        action: Box::new(|mb: Maybe<bool>| match mb {
            Maybe::Just(b) => b,
            Maybe::Nothing => false,
        }),
    }
}

// --------------------------------------------------
// TESTS

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_free_algebra() {
        let free_functor = FreeAlgebraFunctor::<MaybeMonad>::new();
        let free_alg: EMAlgebra<MaybeMonad, Maybe<i32>> = free_functor.map::<i32>();

        // The action should be `join`: Maybe<Maybe<i32>> → Maybe<i32>
        let tta = Maybe::Just(Maybe::Just(42));
        let result = (free_alg.action)(tta);
        assert_eq!(result, Maybe::Just(42));
    }

    #[test]
    fn test_bool_algebra() {
        let alg = bool_algebra();
        let true_val = (alg.action)(Maybe::Just(true));
        let false_val = (alg.action)(Maybe::Just(false));
        let nothing_val = (alg.action)(Maybe::Nothing);

        assert!(true_val);
        assert!(!false_val);
        assert!(!nothing_val);
    }

    #[test]
    fn test_comparison_functor() {
        let comp = ComparisonFunctor::<MaybeMonad, ()>::new();
        let alg = bool_algebra();
        let result = comp.map(&alg);
        assert_eq!(result, "Object in D (via comparison)");
    }
}
