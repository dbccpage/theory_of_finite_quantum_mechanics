//! Exact Reader/State/Writer arrow combinators. AuthorityEffect: None.
//! Callback termination and panic behavior remain the caller's trust boundary.
//! Errors discard returned state/logs; callback side effects are not rolled back.
//! Fan-out sends `Clone::clone` to the left callback and the original to the right.

use std::sync::Arc;

// ----------------------------------------------------------------------------
// Core Types
// ----------------------------------------------------------------------------

// Ctx: Configuration / Global Constants (Reader)
#[derive(Clone, Debug)]
pub struct Ctx {
    pub common_constants: Vec<num_rational::BigRational>,
    pub threshold: num_rational::BigRational,
}

// St: State (Accumulated suggestions, local symbol table)
#[derive(Clone, Debug, Default)]
pub struct St {
    pub suggestions: Vec<String>,
}

// Writer: Accumulated Violations
#[derive(Clone, Debug)]
pub struct Violation {
    pub rule_id: String,
    pub msg: String,
    pub severity: String,
}

pub type Writer = Vec<Violation>;
pub type ArrowResult<B> = Result<(Writer, St, B), anyhow::Error>;

pub type Arrow<A, B> = Arc<dyn Fn(&Ctx, St, A) -> ArrowResult<B> + Send + Sync>;

pub enum Either<L, R> {
    Left(L),
    Right(R),
}

// ----------------------------------------------------------------------------
// Combinators
// ----------------------------------------------------------------------------

pub fn arr<A, B, F>(f: F) -> Arrow<A, B>
where
    A: 'static + Send + Sync,
    B: 'static + Send + Sync,
    F: Fn(A) -> B + Send + Sync + 'static,
{
    Arc::new(move |_ctx, st, a| Ok((vec![], st, f(a))))
}

pub fn compose<A, B, C>(k1: Arrow<A, B>, k2: Arrow<B, C>) -> Arrow<A, C>
where
    A: 'static + Send + Sync,
    B: 'static + Send + Sync,
    C: 'static + Send + Sync,
{
    Arc::new(move |ctx, st, a| {
        let (mut w1, st1, b) = k1(ctx, st, a)?;
        let (w2, st2, c) = k2(ctx, st1, b)?;
        w1.extend(w2);
        Ok((w1, st2, c))
    })
}

pub fn tell<A>(v: Violation) -> Arrow<A, A>
where
    A: 'static + Clone + Send + Sync,
{
    Arc::new(move |_ctx, st, a| Ok((vec![v.clone()], st, a)))
}

// Lift a pure input transformation, as in arr; preserve state and emit no log.
pub fn map_input<A, B, F>(f: F) -> Arrow<A, B>
where
    A: 'static + Send + Sync,
    B: 'static + Send + Sync,
    F: Fn(A) -> B + Send + Sync + 'static,
{
    Arc::new(move |_ctx, st, a| Ok((vec![], st, f(a))))
}

// Fan-out: apply two arrows to the same input, combine their outputs
pub fn fanout<A, B, C>(ab: Arrow<A, B>, ac: Arrow<A, C>) -> Arrow<A, (B, C)>
where
    A: Clone + 'static + Send + Sync,
    B: 'static + Send + Sync,
    C: 'static + Send + Sync,
{
    Arc::new(move |ctx, st, a| {
        let (mut w1, st1, b) = ab(ctx, st, a.clone())?;
        let (w2, st2, c) = ac(ctx, st1, a)?;
        w1.extend(w2);
        Ok((w1, st2, (b, c)))
    })
}

// Split: apply two arrows to a pair, produce a pair
pub fn split<A, B, C, D>(f1: Arrow<A, B>, f2: Arrow<C, D>) -> Arrow<(A, C), (B, D)>
where
    A: 'static + Send + Sync,
    B: 'static + Send + Sync,
    C: 'static + Send + Sync,
    D: 'static + Send + Sync,
{
    Arc::new(move |ctx, st, (a, c)| {
        let (mut w1, st, b) = f1(ctx, st, a)?;
        let (w2, st, d) = f2(ctx, st, c)?;
        w1.extend(w2);
        Ok((w1, st, (b, d)))
    })
}

// Choice: apply either the left or right arrow depending on an Either value
pub fn choice<A, B, C>(f: Arrow<A, C>, g: Arrow<B, C>) -> Arrow<Either<A, B>, C>
where
    A: 'static + Send + Sync,
    B: 'static + Send + Sync,
    C: 'static + Send + Sync,
{
    Arc::new(move |ctx, st, input| match input {
        Either::Left(a) => f(ctx, st, a),
        Either::Right(b) => g(ctx, st, b),
    })
}
