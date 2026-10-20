//! Bounded capture-avoiding operations on finite, untyped HoTT syntax.
//! AuthorityEffect: None. This is a syntax checker, not a typing/proof kernel.
//!
//! Prefix tokens encode one tree. Private binder depths are validated once;
//! transforms preserve that tree grammar and never recurse on user input.
//! Limits count tokens, UTF-8 free-name bytes and conservative token visits.
//! They do not bound allocator internals, process memory, parsing or elapsed time.
#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Token {
    Var(usize),
    Free(String),
    Universe(u32),
    UnitType,
    UnitVal,
    EmptyType,
    BoolType,
    BoolTrue,
    BoolFalse,
    NatType,
    NatZero,
    Pi,
    Lambda,
    App,
    Sigma,
    Pair,
    Fst,
    Snd,
    IdType,
    Refl,
    NatSucc,
    Abort,
    BoolElim,
    NatElim,
}
impl Token {
    fn arity(&self) -> usize {
        match self {
            Self::Lambda => 1,
            Self::Pi | Self::Sigma => 2,
            _ => self.nonbinding_arity(),
        }
    }
    fn nonbinding_arity(&self) -> usize {
        match self {
            Self::App | Self::Pair => 2,
            Self::IdType => 3,
            _ => self.eliminator_arity(),
        }
    }
    fn eliminator_arity(&self) -> usize {
        match self {
            Self::Fst | Self::Snd | Self::Refl | Self::NatSucc => 1,
            Self::Abort => 2,
            Self::BoolElim | Self::NatElim => 4,
            _ => 0,
        }
    }
    fn binds(&self, child: usize) -> bool {
        match self {
            Self::Lambda => child == 0,
            Self::Pi | Self::Sigma => child == 1,
            _ => false,
        }
    }
    fn payload_bytes(&self) -> usize {
        match self {
            Self::Free(name) => name.len(),
            _ => 0,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TermLimits {
    pub max_tokens: usize,
    pub max_name_bytes: usize,
    pub max_binder_depth: usize,
    pub max_token_visits: usize,
}
impl Default for TermLimits {
    fn default() -> Self {
        Self {
            max_tokens: 4096,
            max_name_bytes: 1_048_576,
            max_binder_depth: 1024,
            max_token_visits: 1_000_000,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SubstitutionError {
    EmptyTerm,
    TrailingToken {
        index: usize,
    },
    IncompleteTerm {
        pending: usize,
    },
    Limit {
        resource: &'static str,
        requested: usize,
        limit: usize,
    },
    CountOverflow,
    VariableOverflow {
        index: usize,
    },
    VariableUnderflow {
        index: usize,
    },
    CaptureRisk {
        index: usize,
        cutoff: usize,
    },
    AllocationFailed {
        elements: usize,
    },
}
impl std::fmt::Display for SubstitutionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for SubstitutionError {}
type Result<T> = std::result::Result<T, SubstitutionError>;

fn admit(resource: &'static str, requested: usize, limit: usize) -> Result<()> {
    if requested > limit {
        return Err(SubstitutionError::Limit {
            resource,
            requested,
            limit,
        });
    }
    Ok(())
}
fn reserve<T>(values: &mut Vec<T>, additional: usize) -> Result<()> {
    let elements = add(values.len(), additional)?;
    values
        .try_reserve_exact(additional)
        .map_err(|_| SubstitutionError::AllocationFailed { elements })
}
fn add(left: usize, right: usize) -> Result<usize> {
    left.checked_add(right)
        .ok_or(SubstitutionError::CountOverflow)
}
fn mul(left: usize, right: usize) -> Result<usize> {
    left.checked_mul(right)
        .ok_or(SubstitutionError::CountOverflow)
}

/// Immutable admitted prefix tree; there is no unchecked deserializer or setter.
/// ```compile_fail
/// use tfqm_homotopy_type_theory::substitution::{Term, Token};
/// let _ = Term { tokens: vec![Token::Var(0)], depths: vec![], name_bytes: 0 };
/// ```
/// ```
/// use tfqm_homotopy_type_theory::substitution::{Term, Token, TermLimits, substitute};
/// let limits = TermLimits::default();
/// let body = Term::try_new(vec![Token::Lambda, Token::Var(1)], limits)?;
/// let argument = Term::try_new(vec![Token::Var(0)], limits)?;
/// let result = substitute(&body, 0, &argument, limits)?;
/// assert_eq!(result.tokens(), &[Token::Lambda, Token::Var(1)]);
/// # Ok::<(), tfqm_homotopy_type_theory::substitution::SubstitutionError>(())
/// ```
#[derive(Debug, PartialEq, Eq)]
pub struct Term {
    tokens: Vec<Token>,
    depths: Vec<usize>,
    name_bytes: usize,
}
impl Term {
    pub fn try_new(tokens: Vec<Token>, limits: TermLimits) -> Result<Self> {
        if tokens.is_empty() {
            return Err(SubstitutionError::EmptyTerm);
        }
        admit("tokens", tokens.len(), limits.max_tokens)?;
        admit("token visits", tokens.len(), limits.max_token_visits)?;
        let (depths, name_bytes) = check_tree(&tokens, limits)?;
        Ok(Self {
            tokens,
            depths,
            name_bytes,
        })
    }
    pub fn tokens(&self) -> &[Token] {
        &self.tokens
    }
    pub fn binder_depths(&self) -> &[usize] {
        &self.depths
    }
    pub fn name_bytes(&self) -> usize {
        self.name_bytes
    }
}
fn check_tree(tokens: &[Token], limits: TermLimits) -> Result<(Vec<usize>, usize)> {
    let mut depths = Vec::new();
    reserve(&mut depths, tokens.len())?;
    let mut pending = Vec::new();
    reserve(&mut pending, tokens.len())?;
    pending.push(0usize);
    let mut bytes = 0;
    for (index, token) in tokens.iter().enumerate() {
        let depth = pending
            .pop()
            .ok_or(SubstitutionError::TrailingToken { index })?;
        depths.push(depth);
        bytes = add(bytes, token.payload_bytes())?;
        admit("name bytes", bytes, limits.max_name_bytes)?;
        push_children(&mut pending, token, depth, tokens.len() - index - 1, limits)?;
    }
    if !pending.is_empty() {
        return Err(SubstitutionError::IncompleteTerm {
            pending: pending.len(),
        });
    }
    Ok((depths, bytes))
}
fn push_children(
    pending: &mut Vec<usize>,
    token: &Token,
    depth: usize,
    remaining: usize,
    limits: TermLimits,
) -> Result<()> {
    let count = add(pending.len(), token.arity())?;
    // Every pending child needs a future token. Fail before exceeding the one
    // pending-buffer reservation, including on malformed branching prefixes.
    if count > remaining {
        return Err(SubstitutionError::IncompleteTerm {
            pending: count - remaining,
        });
    }
    for child in (0..token.arity()).rev() {
        let child_depth = add(depth, usize::from(token.binds(child)))?;
        admit("binder depth", child_depth, limits.max_binder_depth)?;
        pending.push(child_depth);
    }
    Ok(())
}

struct Output {
    tokens: Vec<Token>,
    depths: Vec<usize>,
    name_bytes: usize,
}
impl Output {
    fn new(count: usize, name_bytes: usize, limits: TermLimits) -> Result<Self> {
        admit("tokens", count, limits.max_tokens)?;
        admit("name bytes", name_bytes, limits.max_name_bytes)?;
        let mut output = Self {
            tokens: Vec::new(),
            depths: Vec::new(),
            name_bytes,
        };
        reserve(&mut output.tokens, count)?;
        reserve(&mut output.depths, count)?;
        Ok(output)
    }
    fn push(&mut self, token: &Token, variable: Option<usize>, depth: usize) -> Result<()> {
        let copied = match variable {
            Some(index) => Token::Var(index),
            None => copy_token(token)?,
        };
        self.tokens.push(copied);
        self.depths.push(depth);
        Ok(())
    }
    fn finish(self) -> Term {
        Term {
            tokens: self.tokens,
            depths: self.depths,
            name_bytes: self.name_bytes,
        }
    }
}
fn copy_token(token: &Token) -> Result<Token> {
    if let Token::Free(name) = token {
        let mut copied = String::new();
        copied
            .try_reserve_exact(name.len())
            .map_err(|_| SubstitutionError::AllocationFailed {
                elements: name.len(),
            })?;
        copied.push_str(name);
        return Ok(Token::Free(copied));
    }
    Ok(token.clone())
}
fn moved_variable(token: &Token, amount: isize, cutoff: usize) -> Result<Option<usize>> {
    let Token::Var(index) = token else {
        return Ok(None);
    };
    if *index < cutoff {
        return Ok(Some(*index));
    }
    let changed = if amount >= 0 {
        index
            .checked_add(amount.unsigned_abs())
            .ok_or(SubstitutionError::VariableOverflow { index: *index })?
    } else {
        index
            .checked_sub(amount.unsigned_abs())
            .ok_or(SubstitutionError::VariableUnderflow { index: *index })?
    };
    if changed < cutoff {
        return Err(SubstitutionError::CaptureRisk {
            index: *index,
            cutoff,
        });
    }
    Ok(Some(changed))
}

/// Shift free de Bruijn indices at/above cutoff. Negative underflow and shifts
/// below the active cutoff are refused to prevent variable capture;
/// no signed casts, wrapping or mutation of the admitted input occur.
pub fn shift(term: &Term, amount: isize, cutoff: usize, limits: TermLimits) -> Result<Term> {
    check_shift(term, amount, cutoff, limits)?;
    let mut output = Output::new(term.tokens.len(), term.name_bytes, limits)?;
    append_shifted(&mut output, term, amount, cutoff)?;
    Ok(output.finish())
}
fn check_shift(term: &Term, amount: isize, cutoff: usize, limits: TermLimits) -> Result<()> {
    admit(
        "token visits",
        mul(term.tokens.len(), 2)?,
        limits.max_token_visits,
    )?;
    for (token, depth) in term.tokens.iter().zip(&term.depths) {
        admit("binder depth", *depth, limits.max_binder_depth)?;
        moved_variable(token, amount, add(cutoff, *depth)?)?;
    }
    Ok(())
}
fn append_shifted(output: &mut Output, term: &Term, amount: isize, cutoff: usize) -> Result<()> {
    for (token, depth) in term.tokens.iter().zip(&term.depths) {
        output.push(
            token,
            moved_variable(token, amount, add(cutoff, *depth)?)?,
            *depth,
        )?;
    }
    Ok(())
}

fn is_target(token: &Token, index: usize, depth: usize) -> Result<bool> {
    match token {
        Token::Var(value) => Ok(*value == add(index, depth)?),
        _ => Ok(false),
    }
}
fn substituted_variable(token: &Token, index: usize, depth: usize) -> Result<Option<usize>> {
    match token {
        Token::Var(value) => Ok(Some(*value - usize::from(*value > add(index, depth)?))),
        _ => Ok(None),
    }
}
fn lifted_variable(token: &Token, lift: usize, depth: usize) -> Result<Option<usize>> {
    match token {
        Token::Var(value) if *value >= depth => {
            Ok(Some(value.checked_add(lift).ok_or(
                SubstitutionError::VariableOverflow { index: *value },
            )?))
        }
        Token::Var(value) => Ok(Some(*value)),
        _ => Ok(None),
    }
}
fn check_replacement(replacement: &Term, lift: usize, limits: TermLimits) -> Result<()> {
    for (token, depth) in replacement.tokens.iter().zip(&replacement.depths) {
        admit("binder depth", add(lift, *depth)?, limits.max_binder_depth)?;
        lifted_variable(token, lift, *depth)?;
    }
    Ok(())
}
fn replacement_count(term: &Term, index: usize, limits: TermLimits) -> Result<usize> {
    admit("token visits", term.tokens.len(), limits.max_token_visits)?;
    let mut count = 0usize;
    for (token, depth) in term.tokens.iter().zip(&term.depths) {
        admit("binder depth", *depth, limits.max_binder_depth)?;
        if is_target(token, index, *depth)? {
            count = add(count, 1)?;
        }
    }
    Ok(count)
}
fn check_substitution(
    term: &Term,
    index: usize,
    replacement: &Term,
    limits: TermLimits,
) -> Result<(usize, usize)> {
    let count = replacement_count(term, index, limits)?;
    let size = substitution_size(term, replacement, count)?;
    admit_substitution_size(&size, limits)?;
    for (token, depth) in term.tokens.iter().zip(&term.depths) {
        if is_target(token, index, *depth)? {
            check_replacement(replacement, *depth, limits)?;
        }
    }
    Ok((size.tokens, size.bytes))
}
struct SubstitutionSize {
    tokens: usize,
    bytes: usize,
    visits: usize,
}
fn substitution_size(term: &Term, replacement: &Term, count: usize) -> Result<SubstitutionSize> {
    let inserted = mul(count, replacement.tokens.len())?;
    let output_count = add(term.tokens.len() - count, inserted)?;
    let bytes = add(term.name_bytes, mul(count, replacement.name_bytes)?)?;
    let visits = add(mul(term.tokens.len(), 3)?, mul(inserted, 2)?)?;
    Ok(SubstitutionSize {
        tokens: output_count,
        bytes,
        visits,
    })
}
fn admit_substitution_size(size: &SubstitutionSize, limits: TermLimits) -> Result<()> {
    admit("tokens", size.tokens, limits.max_tokens)?;
    admit("name bytes", size.bytes, limits.max_name_bytes)?;
    admit("token visits", size.visits, limits.max_token_visits)
}
fn append_replacement(output: &mut Output, replacement: &Term, lift: usize) -> Result<()> {
    for (token, depth) in replacement.tokens.iter().zip(&replacement.depths) {
        output.push(
            token,
            lifted_variable(token, lift, *depth)?,
            add(lift, *depth)?,
        )?;
    }
    Ok(())
}

/// Replace variable index, lift free replacement variables under binders, and
/// decrement larger indices as the substituted variable leaves the context.
/// All arithmetic/domain/resource preflight completes before output allocation.
/// Work is O(n + occurrences*m), with n input and m replacement tokens.
pub fn substitute(
    term: &Term,
    index: usize,
    replacement: &Term,
    limits: TermLimits,
) -> Result<Term> {
    let (count, bytes) = check_substitution(term, index, replacement, limits)?;
    let mut output = Output::new(count, bytes, limits)?;
    for (token, depth) in term.tokens.iter().zip(&term.depths) {
        if is_target(token, index, *depth)? {
            append_replacement(&mut output, replacement, *depth)?;
        } else {
            output.push(token, substituted_variable(token, index, *depth)?, *depth)?;
        }
    }
    Ok(output.finish())
}

/// Instantiate the first context variable with the same checked substitution
/// rule. The supplied term is the scope body, without an outer Lambda token.
pub fn instantiate(scope: &Term, argument: &Term, limits: TermLimits) -> Result<Term> {
    substitute(scope, 0, argument, limits)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn term(tokens: Vec<Token>) -> Term {
        Term::try_new(tokens, TermLimits::default()).unwrap()
    }
    #[test]
    fn capture_avoidance_and_context_removal_have_literal_expected_tokens() {
        let body = term(vec![
            Token::Lambda,
            Token::App,
            Token::Var(1),
            Token::Var(0),
        ]);
        let replacement = term(vec![Token::Var(0)]);
        let result = substitute(&body, 0, &replacement, TermLimits::default()).unwrap();
        assert_eq!(
            result.tokens(),
            &[Token::Lambda, Token::App, Token::Var(1), Token::Var(0)]
        );
        let body = term(vec![
            Token::Pi,
            Token::Var(0),
            Token::App,
            Token::Var(1),
            Token::Var(2),
        ]);
        let result = substitute(&body, 0, &replacement, TermLimits::default()).unwrap();
        assert_eq!(
            result.tokens(),
            &[
                Token::Pi,
                Token::Var(0),
                Token::App,
                Token::Var(1),
                Token::Var(1)
            ]
        );
        assert_eq!(result.binder_depths(), &[0, 0, 1, 1, 1]);
    }
    #[test]
    fn malformed_prefix_and_all_limits_are_typed_and_inclusive() {
        let d = TermLimits::default();
        assert_eq!(
            Term::try_new(vec![], d).err(),
            Some(SubstitutionError::EmptyTerm)
        );
        assert_eq!(
            Term::try_new(vec![Token::UnitVal, Token::Var(0)], d).err(),
            Some(SubstitutionError::TrailingToken { index: 1 })
        );
        assert_eq!(
            Term::try_new(vec![Token::App, Token::Var(0)], d).err(),
            Some(SubstitutionError::IncompleteTerm { pending: 1 })
        );
        let t = term(vec![Token::Free("abc".into())]);
        let inclusive = TermLimits {
            max_tokens: 1,
            max_name_bytes: 3,
            max_binder_depth: 0,
            max_token_visits: 2,
        };
        assert_eq!(shift(&t, 0, 0, inclusive).unwrap(), t);
        assert!(shift(
            &t,
            0,
            0,
            TermLimits {
                max_token_visits: 1,
                ..inclusive
            }
        )
        .is_err());
        assert!(shift(
            &t,
            0,
            0,
            TermLimits {
                max_name_bytes: 2,
                ..inclusive
            }
        )
        .is_err());
        assert!(Term::try_new(
            vec![Token::Lambda, Token::Var(0)],
            TermLimits {
                max_binder_depth: 0,
                ..d
            }
        )
        .is_err());
        let t = term(vec![Token::App, Token::Var(0), Token::Var(0)]);
        let r = term(vec![Token::App, Token::Var(0), Token::Var(1)]);
        assert_eq!(
            substitute(&t, 0, &r, TermLimits { max_tokens: 6, ..d }).err(),
            Some(SubstitutionError::Limit {
                resource: "tokens",
                requested: 7,
                limit: 6
            })
        );
        assert_eq!(
            substitute(
                &t,
                0,
                &r,
                TermLimits {
                    max_tokens: 7,
                    max_token_visits: 21,
                    ..d
                }
            )
            .unwrap()
            .tokens()
            .len(),
            7
        );
        assert!(substitute(
            &t,
            0,
            &r,
            TermLimits {
                max_token_visits: 20,
                ..d
            }
        )
        .is_err());
    }
    #[test]
    fn machine_boundaries_refuse_without_signed_casts_or_input_mutation() {
        let d = TermLimits::default();
        let max = term(vec![Token::Var(usize::MAX)]);
        assert_eq!(
            shift(&max, 1, 0, d).err(),
            Some(SubstitutionError::VariableOverflow { index: usize::MAX })
        );
        let zero = term(vec![Token::Var(0)]);
        assert_eq!(
            shift(&zero, -1, 0, d).err(),
            Some(SubstitutionError::VariableUnderflow { index: 0 })
        );
        assert!(shift(&zero, isize::MIN, 0, d).is_err());
        let bound = term(vec![Token::Lambda, Token::Var(0)]);
        assert!(shift(&bound, 1, usize::MAX, d).is_err());
        assert_eq!(shift(&bound, -1, 0, d).unwrap(), bound);
        let body = term(vec![Token::Lambda, Token::Var(1)]);
        assert_eq!(
            shift(&body, -1, 0, d).err(),
            Some(SubstitutionError::CaptureRisk {
                index: 1,
                cutoff: 1
            })
        );
        let deeper = term(vec![Token::Lambda, Token::Var(2)]);
        assert_eq!(shift(&deeper, -1, 0, d).unwrap(), body);
        assert!(substitute(&body, 0, &max, d).is_err());
        assert_eq!(max.tokens(), &[Token::Var(usize::MAX)]);
        assert_eq!(body.tokens(), &[Token::Lambda, Token::Var(1)]);
    }
    #[test]
    fn replacement_name_bytes_are_inclusive_and_count_every_occurrence() {
        let d = TermLimits::default();
        let body = term(vec![Token::App, Token::Var(0), Token::Var(0)]);
        let replacement = term(vec![Token::Free("\u{1f52c}".into())]);
        let expected = [
            Token::App,
            Token::Free("\u{1f52c}".into()),
            Token::Free("\u{1f52c}".into()),
        ];
        let result = substitute(
            &body,
            0,
            &replacement,
            TermLimits {
                max_name_bytes: 8,
                ..d
            },
        )
        .unwrap();
        assert_eq!(result.tokens(), expected);
        assert_eq!(result.name_bytes(), 8);
        assert_eq!(
            substitute(
                &body,
                0,
                &replacement,
                TermLimits {
                    max_name_bytes: 7,
                    ..d
                }
            )
            .err(),
            Some(SubstitutionError::Limit {
                resource: "name bytes",
                requested: 8,
                limit: 7
            })
        );
    }
    #[test]
    fn deep_prefix_uses_no_recursive_production_traversal() {
        let mut tokens = vec![Token::Lambda; 1024];
        tokens.push(Token::Var(1024));
        let body = term(tokens);
        let r = term(vec![Token::UnitVal]);
        let result = substitute(&body, 0, &r, TermLimits::default()).unwrap();
        assert_eq!(result.tokens().last(), Some(&Token::UnitVal));
        assert_eq!(result.binder_depths().last(), Some(&1024));
    }
}

#[cfg(test)]
mod independent_tree_oracle {
    use super::*;
    #[derive(Clone, Debug)]
    enum Tree {
        V(usize),
        L(Box<Tree>),
        A(Box<Tree>, Box<Tree>),
        P(Box<Tree>, Box<Tree>),
    }
    fn tokens(t: &Tree, output: &mut Vec<Token>) {
        match t {
            Tree::V(i) => output.push(Token::Var(*i)),
            Tree::L(t) => {
                output.push(Token::Lambda);
                tokens(t, output);
            }
            Tree::A(a, b) => {
                output.push(Token::App);
                tokens(a, output);
                tokens(b, output);
            }
            Tree::P(a, b) => {
                output.push(Token::Pi);
                tokens(a, output);
                tokens(b, output);
            }
        }
    }
    fn flat(t: &Tree) -> Vec<Token> {
        let mut out = Vec::new();
        tokens(t, &mut out);
        out
    }
    fn lift(t: &Tree, offset: usize, cutoff: usize) -> Tree {
        match t {
            Tree::V(i) => Tree::V(*i + usize::from(*i >= cutoff) * offset),
            Tree::L(t) => Tree::L(Box::new(lift(t, offset, cutoff + 1))),
            Tree::A(a, b) => Tree::A(
                Box::new(lift(a, offset, cutoff)),
                Box::new(lift(b, offset, cutoff)),
            ),
            Tree::P(a, b) => Tree::P(
                Box::new(lift(a, offset, cutoff)),
                Box::new(lift(b, offset, cutoff + 1)),
            ),
        }
    }
    fn subst(t: &Tree, index: usize, r: &Tree) -> Tree {
        match t {
            Tree::V(i) if *i == index => r.clone(),
            Tree::V(i) => Tree::V(*i - usize::from(*i > index)),
            Tree::L(t) => Tree::L(Box::new(subst(t, index + 1, &lift(r, 1, 0)))),
            Tree::A(a, b) => Tree::A(Box::new(subst(a, index, r)), Box::new(subst(b, index, r))),
            Tree::P(a, b) => Tree::P(
                Box::new(subst(a, index, r)),
                Box::new(subst(b, index + 1, &lift(r, 1, 0))),
            ),
        }
    }
    fn lower(t: &Tree, amount: i128, cutoff: usize) -> Option<Tree> {
        match t {
            Tree::V(i) if *i < cutoff => Some(Tree::V(*i)),
            Tree::V(i) => {
                let changed = *i as i128 + amount;
                (changed >= cutoff as i128).then_some(Tree::V(changed as usize))
            }
            Tree::L(t) => Some(Tree::L(Box::new(lower(t, amount, cutoff + 1)?))),
            Tree::A(a, b) => Some(Tree::A(
                Box::new(lower(a, amount, cutoff)?),
                Box::new(lower(b, amount, cutoff)?),
            )),
            Tree::P(a, b) => Some(Tree::P(
                Box::new(lower(a, amount, cutoff)?),
                Box::new(lower(b, amount, cutoff + 1)?),
            )),
        }
    }
    fn sample_trees() -> Vec<Tree> {
        let leaves: Vec<_> = (0..4).map(Tree::V).collect();
        let mut all = leaves.clone();
        for a in &leaves {
            all.push(Tree::L(Box::new(a.clone())));
            for b in &leaves {
                all.push(Tree::A(Box::new(a.clone()), Box::new(b.clone())));
                all.push(Tree::P(Box::new(a.clone()), Box::new(b.clone())));
            }
        }
        let more: Vec<_> = all.iter().cloned().map(|a| Tree::L(Box::new(a))).collect();
        all.extend(more);
        all
    }
    #[test]
    fn finite_trees_match_separate_recursive_shift_and_substitution_oracle() {
        let trees = sample_trees();
        let d = TermLimits::default();
        for t in &trees {
            let input = Term::try_new(flat(t), d).unwrap();
            for cutoff in 0..3 {
                for amount in 0..3 {
                    assert_eq!(
                        shift(&input, amount as isize, cutoff, d).unwrap().tokens(),
                        flat(&lift(t, amount, cutoff))
                    );
                }
                for amount in [-2, -1] {
                    let actual = shift(&input, amount as isize, cutoff, d);
                    match lower(t, amount, cutoff) {
                        Some(expected) => assert_eq!(actual.unwrap().tokens(), flat(&expected)),
                        None => assert!(actual.is_err()),
                    }
                }
            }
            for r in &trees {
                let replacement = Term::try_new(flat(r), d).unwrap();
                for index in 0..3 {
                    let result = substitute(&input, index, &replacement, d).unwrap();
                    let expected = flat(&subst(t, index, r));
                    assert_eq!(result.tokens(), expected);
                    assert_eq!(Term::try_new(expected, d).unwrap(), result);
                }
            }
        }
        assert_eq!(trees.len(), 80);
    }
    #[test]
    fn every_operator_arity_and_binder_position_is_exercised() {
        let forms = [
            Token::UnitType,
            Token::UnitVal,
            Token::EmptyType,
            Token::BoolType,
            Token::BoolTrue,
            Token::BoolFalse,
            Token::NatType,
            Token::NatZero,
            Token::Universe(0),
            Token::Free("x".into()),
            Token::Lambda,
            Token::Fst,
            Token::Snd,
            Token::Refl,
            Token::NatSucc,
            Token::Pi,
            Token::App,
            Token::Sigma,
            Token::Pair,
            Token::Abort,
            Token::IdType,
            Token::BoolElim,
            Token::NatElim,
        ];
        let expected_arities = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 4, 4,
        ];
        for (form, arity) in forms.into_iter().zip(expected_arities) {
            let binds: Vec<_> = match form {
                Token::Lambda => vec![1],
                Token::Pi | Token::Sigma => vec![0, 1],
                _ => vec![0; arity],
            };
            let mut source = vec![form];
            source.extend(vec![Token::Var(0); arity]);
            let admitted = Term::try_new(source, TermLimits::default()).unwrap();
            assert_eq!(&admitted.binder_depths()[1..], binds);
        }
    }
}
