//! Genesis to universal computation: exact semi-Thue engine, bounded-regime reachability
//! decider, and the Turing-machine-to-rewriting encoding with step simulation.
//!
//! AuthorityEffect: None.
//!
//! Scope fence. Everything here is a finite, exact computation on explicit inputs. The words are
//! sequences of marks; a rule rewrites a factor of a word, which is a one-hole context plus a
//! replacement. The bounded decider answers reachability only inside a declared word-length bound
//! and says so when the bound is exceeded. The Turing machine encoding mirrors the Lean module
//! `lean4/GenesisCompTM.lean` (marks `lend`, `rend`, state marks, tape marks) for machines given
//! in the `Turing.TM0` form (one move or one write per transition). Nothing here claims a
//! physical Church-Turing thesis, derives the identity convention, or supplies unbounded blanks:
//! the blank supply is the explicit growth of the word at the right and left ends.
//!
//! This file has no dependencies beyond `std`, so it is both a module of the `tfqm_wdp` crate and
//! the root of the standalone crate `tfqm_genesis_tm` in `code/rust/src/genesis_tm`.

use std::collections::{BTreeMap, BTreeSet, VecDeque};

/// A mark of the alphabet.
pub type Mark = u32;
/// A word over the marks.
pub type Word = Vec<Mark>;

/// Errors of the engine.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TmError {
    /// The start word is already longer than the declared bound.
    StartOutsideBound { len: usize, bound: usize },
    /// A mark outside the declared alphabet size appeared.
    MarkOutOfRange(Mark),
    /// A word is not the encoding of any configuration.
    NotAConfiguration,
    /// A simulation check failed.
    Mismatch(String),
}

/// A rewriting rule `lhs -> rhs`; an empty `lhs` matches at every position.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Rule {
    pub lhs: Word,
    pub rhs: Word,
}

/// A semi-Thue system: a finite list of rules.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Srs {
    pub rules: Vec<Rule>,
}

impl Srs {
    pub fn new(rules: Vec<Rule>) -> Self {
        Srs { rules }
    }

    /// Every redex of `w`: pairs `(position, rule index)` in increasing order.
    pub fn redexes(&self, w: &[Mark]) -> Vec<(usize, usize)> {
        let mut out = Vec::new();
        for pos in 0..=w.len() {
            for (ri, r) in self.rules.iter().enumerate() {
                if w[pos..].starts_with(&r.lhs) {
                    out.push((pos, ri));
                }
            }
        }
        out
    }

    /// Apply rule `ri` at position `pos`; the caller guarantees the redex.
    pub fn apply(&self, w: &[Mark], pos: usize, ri: usize) -> Word {
        let r = &self.rules[ri];
        let mut out = Vec::with_capacity(w.len() + r.rhs.len());
        out.extend_from_slice(&w[..pos]);
        out.extend_from_slice(&r.rhs);
        out.extend_from_slice(&w[pos + r.lhs.len()..]);
        out
    }

    /// The set of one-step rewrites of `w` (the relation `Step` of the Lean module).
    pub fn successors(&self, w: &[Mark]) -> BTreeSet<Word> {
        self.redexes(w).into_iter().map(|(p, r)| self.apply(w, p, r)).collect()
    }

    /// No rule applies.
    pub fn is_irreducible(&self, w: &[Mark]) -> bool {
        self.redexes(w).is_empty()
    }

    /// Letter map: rename every mark through `f` (the analogue of Genesis `Step.rename`).
    pub fn map_marks(&self, f: impl Fn(Mark) -> Mark) -> Srs {
        Srs::new(
            self.rules
                .iter()
                .map(|r| Rule {
                    lhs: r.lhs.iter().map(|&m| f(m)).collect(),
                    rhs: r.rhs.iter().map(|&m| f(m)).collect(),
                })
                .collect(),
        )
    }
}

/// Verdict of the bounded decider on "is `target` reachable from `start`?".
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Verdict {
    /// `target` is reachable inside the bound, hence reachable.
    Reachable,
    /// The bounded search is closed (no reachable word has a step leaving the bound) and the
    /// target was not found: `target` is not reachable at all.
    Unreachable,
    /// A word reached inside the bound has a step to a word longer than the bound, so the bounded
    /// search cannot settle the unbounded question. The witness step is returned.
    BoundExceeded { from: Word, to: Word },
}

/// The set of words reachable from `start` with every intermediate word of length at most
/// `bound`, together with the first step found that leaves the bound (breadth-first order).
pub fn reach_set_bounded(
    srs: &Srs,
    start: &[Mark],
    bound: usize,
) -> Result<(BTreeSet<Word>, Option<(Word, Word)>), TmError> {
    if start.len() > bound {
        return Err(TmError::StartOutsideBound { len: start.len(), bound });
    }
    let mut seen: BTreeSet<Word> = BTreeSet::new();
    let mut queue: VecDeque<Word> = VecDeque::new();
    let mut exceeded: Option<(Word, Word)> = None;
    seen.insert(start.to_vec());
    queue.push_back(start.to_vec());
    while let Some(w) = queue.pop_front() {
        for next in srs.successors(&w) {
            if next.len() > bound {
                if exceeded.is_none() {
                    exceeded = Some((w.clone(), next));
                }
            } else if seen.insert(next.clone()) {
                queue.push_back(next);
            }
        }
    }
    Ok((seen, exceeded))
}

/// The bounded reachability decider (the explicit procedure behind `decideReachB`/`verdict`).
pub fn decide_reach(
    srs: &Srs,
    start: &[Mark],
    target: &[Mark],
    bound: usize,
) -> Result<Verdict, TmError> {
    let (seen, exceeded) = reach_set_bounded(srs, start, bound)?;
    if seen.contains(target) {
        return Ok(Verdict::Reachable);
    }
    Ok(match exceeded {
        None => Verdict::Unreachable,
        Some((from, to)) => Verdict::BoundExceeded { from, to },
    })
}

/// Number of words of length at most `bound` over `k` marks: `1 + k + ... + k^bound`.
pub fn config_space_size(k: u64, bound: u32) -> u64 {
    (0..=bound).map(|i| k.pow(i)).sum()
}

// ---------------------------------------------------------------------------------------------
// Turing machines in the `TM0` form and their encoding
// ---------------------------------------------------------------------------------------------

/// Head direction.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Dir {
    Left,
    Right,
}

/// A `TM0` statement: either write a symbol or move.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Stmt {
    Write(u32),
    Move(Dir),
}

/// A machine: symbol `0` is the blank; a missing transition halts.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Machine {
    pub n_states: u32,
    pub n_symbols: u32,
    pub delta: BTreeMap<(u32, u32), (u32, Stmt)>,
}

/// A configuration: state, left cells (nearest first), scanned symbol, right cells (nearest first).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Config {
    pub state: u32,
    pub left: Vec<u32>,
    pub head: u32,
    pub right: Vec<u32>,
}

impl Config {
    /// Strip the trailing (far) blanks of both sides: the canonical form of the blank-padded tape.
    pub fn normalized(&self) -> Config {
        let mut left = self.left.clone();
        let mut right = self.right.clone();
        while left.last() == Some(&0) {
            left.pop();
        }
        while right.last() == Some(&0) {
            right.pop();
        }
        Config { state: self.state, left, head: self.head, right }
    }

    /// The initial configuration on `input`: head on the first cell, state `0`.
    pub fn init(input: &[u32]) -> Config {
        match input.split_first() {
            None => Config { state: 0, left: vec![], head: 0, right: vec![] },
            Some((&h, rest)) => Config { state: 0, left: vec![], head: h, right: rest.to_vec() },
        }
    }

    /// The tape from the far left to the far right, trailing blanks stripped on both sides.
    pub fn tape(&self) -> Vec<u32> {
        let n = self.normalized();
        let mut t: Vec<u32> = n.left.iter().rev().cloned().collect();
        t.push(n.head);
        t.extend(n.right.iter());
        while t.last() == Some(&0) {
            t.pop();
        }
        t
    }
}

/// One machine step, mirroring `Turing.TM0.step` and `Turing.Tape.move`/`write`.
pub fn tm_step(m: &Machine, c: &Config) -> Option<Config> {
    let &(q2, stmt) = m.delta.get(&(c.state, c.head))?;
    let mut n = c.clone();
    n.state = q2;
    match stmt {
        Stmt::Write(b) => n.head = b,
        Stmt::Move(Dir::Right) => {
            let new_head = if n.right.is_empty() { 0 } else { n.right.remove(0) };
            n.left.insert(0, c.head);
            n.head = new_head;
        }
        Stmt::Move(Dir::Left) => {
            let new_head = if n.left.is_empty() { 0 } else { n.left.remove(0) };
            n.right.insert(0, c.head);
            n.head = new_head;
        }
    }
    Some(n)
}

/// Mark numbering of the encoding: `0` is `lend`, `1` is `rend`, `2 + a` is tape symbol `a`,
/// `2 + n_symbols + q` is state `q`.
#[derive(Debug, Clone, Copy)]
pub struct Marks {
    pub n_symbols: u32,
    pub n_states: u32,
}

impl Marks {
    pub const LEND: Mark = 0;
    pub const REND: Mark = 1;
    pub fn of(m: &Machine) -> Marks {
        Marks { n_symbols: m.n_symbols, n_states: m.n_states }
    }
    pub fn sym(&self, a: u32) -> Mark {
        2 + a
    }
    pub fn st(&self, q: u32) -> Mark {
        2 + self.n_symbols + q
    }
    /// Total number of marks: `|symbols| + |states| + 2`.
    pub fn count(&self) -> u32 {
        self.n_symbols + self.n_states + 2
    }
}

/// Configuration word `lend . left (far to near) . q . a . right (near to far) . rend`.
pub fn encode(m: &Machine, c: &Config) -> Word {
    let k = Marks::of(m);
    let mut w = vec![Marks::LEND];
    w.extend(c.left.iter().rev().map(|&a| k.sym(a)));
    w.push(k.st(c.state));
    w.push(k.sym(c.head));
    w.extend(c.right.iter().map(|&a| k.sym(a)));
    w.push(Marks::REND);
    w
}

/// Decode a configuration word to its normalized configuration; `None` if the word is not of the
/// configuration shape.
pub fn decode(m: &Machine, w: &[Mark]) -> Option<Config> {
    let k = Marks::of(m);
    let first_st = 2 + k.n_symbols;
    if w.first() != Some(&Marks::LEND) || w.last() != Some(&Marks::REND) || w.len() < 4 {
        return None;
    }
    let inner = &w[1..w.len() - 1];
    let is_st = |x: Mark| x >= first_st && x < first_st + k.n_states;
    let is_sym = |x: Mark| x >= 2 && x < first_st;
    let pos = inner.iter().position(|&x| is_st(x))?;
    if inner.iter().filter(|&&x| is_st(x)).count() != 1 || pos + 1 >= inner.len() {
        return None;
    }
    if !inner.iter().enumerate().all(|(i, &x)| i == pos || is_sym(x)) {
        return None;
    }
    let state = inner[pos] - first_st;
    let head = inner[pos + 1] - 2;
    let left: Vec<u32> = inner[..pos].iter().rev().map(|&x| x - 2).collect();
    let right: Vec<u32> = inner[pos + 2..].iter().map(|&x| x - 2).collect();
    Some(Config { state, left, head, right }.normalized())
}

/// The rewriting rules of a machine (the Lean `Rules`): write, right, right-end, left, left-end.
pub fn rules_of(m: &Machine) -> Srs {
    let k = Marks::of(m);
    let mut rules = Vec::new();
    for (&(q, a), &(q2, stmt)) in &m.delta {
        match stmt {
            Stmt::Write(b) => rules.push(Rule {
                lhs: vec![k.st(q), k.sym(a)],
                rhs: vec![k.st(q2), k.sym(b)],
            }),
            Stmt::Move(Dir::Right) => {
                for c in 0..m.n_symbols {
                    rules.push(Rule {
                        lhs: vec![k.st(q), k.sym(a), k.sym(c)],
                        rhs: vec![k.sym(a), k.st(q2), k.sym(c)],
                    });
                }
                rules.push(Rule {
                    lhs: vec![k.st(q), k.sym(a), Marks::REND],
                    rhs: vec![k.sym(a), k.st(q2), k.sym(0), Marks::REND],
                });
            }
            Stmt::Move(Dir::Left) => {
                for c in 0..m.n_symbols {
                    rules.push(Rule {
                        lhs: vec![k.sym(c), k.st(q), k.sym(a)],
                        rhs: vec![k.st(q2), k.sym(c), k.sym(a)],
                    });
                }
                rules.push(Rule {
                    lhs: vec![Marks::LEND, k.st(q), k.sym(a)],
                    rhs: vec![Marks::LEND, k.st(q2), k.sym(0), k.sym(a)],
                });
            }
        }
    }
    Srs::new(rules)
}

/// Check one-step simulation in both directions on the encoding of `c`: the rewrite successors of
/// `encode(c)` are exactly the encoding of the machine step, or none when the machine halts.
pub fn check_step_simulation(m: &Machine, srs: &Srs, c: &Config) -> Result<(), TmError> {
    let w = encode(m, c);
    let succ = srs.successors(&w);
    match tm_step(m, c) {
        None => {
            if succ.is_empty() {
                Ok(())
            } else {
                Err(TmError::Mismatch(format!("halted config {:?} has rewrites", c)))
            }
        }
        Some(c2) => {
            if succ.len() != 1 {
                return Err(TmError::Mismatch(format!("{} successors for {:?}", succ.len(), c)));
            }
            let w2 = succ.into_iter().next().unwrap();
            let d = decode(m, &w2).ok_or(TmError::NotAConfiguration)?;
            if d == c2.normalized() {
                Ok(())
            } else {
                Err(TmError::Mismatch(format!("{:?} -> {:?} but machine gives {:?}", c, d, c2)))
            }
        }
    }
}

/// Run machine and rewriting side by side, checking every step; returns the final configuration
/// and the number of steps, or `None` if `max_steps` is reached.
pub fn run_both(
    m: &Machine,
    c0: &Config,
    max_steps: usize,
) -> Result<Option<(Config, usize)>, TmError> {
    let srs = rules_of(m);
    let mut c = c0.clone();
    let mut w = encode(m, &c);
    for step in 0..=max_steps {
        check_step_simulation(m, &srs, &c)?;
        match tm_step(m, &c) {
            None => {
                if !srs.is_irreducible(&w) {
                    return Err(TmError::Mismatch("halted word is reducible".into()));
                }
                return Ok(Some((c, step)));
            }
            Some(c2) => {
                let succ = srs.successors(&w);
                w = succ.into_iter().next().unwrap();
                c = decode(m, &w).ok_or(TmError::NotAConfiguration)?;
                if c != c2.normalized() {
                    return Err(TmError::Mismatch("decoded step differs".into()));
                }
            }
        }
    }
    Ok(None)
}

// ---------------------------------------------------------------------------------------------
// Example machines (TM0 form)
// ---------------------------------------------------------------------------------------------

fn machine(n_states: u32, n_symbols: u32, t: &[((u32, u32), (u32, Stmt))]) -> Machine {
    Machine { n_states, n_symbols, delta: t.iter().cloned().collect() }
}

/// Binary incrementer, least significant bit first, blank read as 0. States: `0` carry,
/// `1` move-after-write, `2` halt. Symbols: `0` blank/zero, `1` one.
pub fn incrementer() -> Machine {
    use Dir::Right;
    use Stmt::{Move, Write};
    machine(
        3,
        2,
        &[
            ((0, 1), (1, Write(0))),
            ((1, 0), (0, Move(Right))),
            ((1, 1), (0, Move(Right))),
            ((0, 0), (2, Write(1))),
        ],
    )
}

/// The two-state two-symbol busy beaver champion, with each of its transitions split into a write
/// step and a move step as the `TM0` form requires. Starting on the blank tape it halts with four
/// ones after twelve `TM0` steps (six steps of the usual presentation).
pub fn busy_beaver_2() -> Machine {
    use Dir::{Left, Right};
    use Stmt::{Move, Write};
    // states: 0 A, 1 B, 2 H, 3 A0 then R to B, 4 A1 then L to B, 5 B0 then L to A, 6 B1 then R to H
    machine(
        7,
        2,
        &[
            ((0, 0), (3, Write(1))),
            ((3, 0), (1, Move(Right))),
            ((3, 1), (1, Move(Right))),
            ((0, 1), (4, Write(1))),
            ((4, 0), (1, Move(Left))),
            ((4, 1), (1, Move(Left))),
            ((1, 0), (5, Write(1))),
            ((5, 0), (0, Move(Left))),
            ((5, 1), (0, Move(Left))),
            ((1, 1), (6, Write(1))),
            ((6, 0), (2, Move(Right))),
            ((6, 1), (2, Move(Right))),
        ],
    )
}

/// A non-halting machine that moves right forever: every step needs one more fresh blank mark.
pub fn right_runner() -> Machine {
    machine(
        1,
        2,
        &[((0, 0), (0, Stmt::Move(Dir::Right))), ((0, 1), (0, Stmt::Move(Dir::Right)))],
    )
}

// ---------------------------------------------------------------------------------------------
// Genesis event semantics (custody mirror of the sealed events) and contexts
// ---------------------------------------------------------------------------------------------

/// A Genesis regime (mirror of the sealed `Regime`).
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Regime {
    pub data: usize,
    pub forms: Vec<usize>,
    pub insts: Vec<(usize, Vec<usize>)>,
    pub rules: Vec<usize>,
    pub reqs: Vec<(usize, usize)>,
}

/// A sealed Genesis event (mirror of the sealed `Event`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Event {
    Supply(usize),
    AdmitDatum,
    AdmitForm(usize),
    AdmitInst(usize, Vec<usize>),
    AdmitRuleAll(usize),
    Impose(usize, usize),
}

fn insert_new<T: PartialEq + Clone>(l: &[T], a: T) -> Vec<T> {
    let mut v = l.to_vec();
    if !v.contains(&a) {
        v.push(a);
    }
    v
}

/// The sealed step function: `None` refuses the event.
pub fn step_e(r: &Regime, e: &Event) -> Option<Regime> {
    let mut n = r.clone();
    match e {
        Event::Supply(_) => Some(n),
        Event::AdmitDatum => {
            n.data += 1;
            Some(n)
        }
        Event::AdmitForm(a) => {
            if *a >= 1 {
                n.forms.push(*a);
                Some(n)
            } else {
                None
            }
        }
        Event::AdmitInst(f, args) => {
            if *f < r.forms.len() && args.len() == r.forms[*f] && args.iter().all(|&x| x < r.data)
            {
                n.insts = insert_new(&r.insts, (*f, args.clone()));
                Some(n)
            } else {
                None
            }
        }
        Event::AdmitRuleAll(f) => {
            if *f < r.forms.len() {
                n.rules = insert_new(&r.rules, *f);
                Some(n)
            } else {
                None
            }
        }
        Event::Impose(i, j) => {
            if i < j && *j < r.data {
                n.reqs = insert_new(&r.reqs, (*i, *j));
                Some(n)
            } else {
                None
            }
        }
    }
}

/// Replay a history of events from a base regime.
pub fn replay_e(h: &[Event], base: &Regime) -> Option<Regime> {
    let mut r = base.clone();
    for e in h {
        r = step_e(&r, e)?;
    }
    Some(r)
}

/// Datum `i` is told apart from datum `j` by a unary form instance (mirror of `UnarySep`).
pub fn unary_sep(r: &Regime, i: usize, j: usize) -> bool {
    (0..r.forms.len()).any(|f| {
        r.forms[f] == 1 && (r.insts.contains(&(f, vec![i])) != r.insts.contains(&(f, vec![j])))
    })
}

/// Neither direction is told apart (mirror of `Collapsed`).
pub fn collapsed(r: &Regime, i: usize, j: usize) -> bool {
    !unary_sep(r, i, j) && !unary_sep(r, j, i)
}

/// Every two distinct admitted marks are told apart (mirror of `PairwiseSeparated`).
pub fn pairwise_separated(r: &Regime) -> bool {
    (0..r.data).all(|i| (0..r.data).all(|j| i == j || unary_sep(r, i, j)))
}

/// The canonical regime on `n` marks: `n` data, `n-1` unary forms, instance `(i,[i])`.
pub fn canonical_regime(n: usize) -> Regime {
    let k = n.saturating_sub(1);
    Regime {
        data: n,
        forms: vec![1; k],
        insts: (0..k).map(|i| (i, vec![i])).collect(),
        rules: vec![],
        reqs: vec![],
    }
}

/// The history of the cost-two shape of the first separation (one unary form, one instance).
pub fn first_separation_history() -> Vec<Event> {
    vec![
        Event::AdmitDatum,
        Event::AdmitDatum,
        Event::AdmitForm(1),
        Event::AdmitInst(0, vec![0]),
        Event::Impose(0, 1),
    ]
}

/// A Genesis context: a tuple of slots, `None` being a hole.
pub type GCtx = Vec<Option<usize>>;

/// All contexts of arity `a` over data `0..n` with at least one hole.
pub fn contexts(n: usize, a: usize) -> Vec<GCtx> {
    let mut all: Vec<GCtx> = vec![vec![]];
    for _ in 0..a {
        let mut next = Vec::new();
        for c in &all {
            let mut with_hole = c.clone();
            with_hole.push(None);
            next.push(with_hole);
            for d in 0..n {
                let mut with_datum = c.clone();
                with_datum.push(Some(d));
                next.push(with_datum);
            }
        }
        all = next;
    }
    all.into_iter().filter(|c| c.iter().any(Option::is_none)).collect()
}

/// Plug a datum into every hole.
pub fn plug1(d: usize, c: &GCtx) -> Vec<usize> {
    c.iter().map(|o| o.unwrap_or(d)).collect()
}

// ---------------------------------------------------------------------------------------------
// Binary coding of a finite alphabet
// ---------------------------------------------------------------------------------------------

/// Width of the fixed-length binary code of an alphabet of `card` marks: `ceil(log2 card) + 1`.
pub fn code_width(card: usize) -> usize {
    let mut clog = 0usize;
    while (1usize << clog) < card {
        clog += 1;
    }
    clog + 1
}

/// Code a word over `0..card` as bits, least significant bit first, `code_width` bits per letter.
pub fn encode_binary(card: usize, w: &[usize]) -> Vec<bool> {
    let k = code_width(card);
    w.iter().flat_map(|&a| (0..k).map(move |j| (a >> j) & 1 == 1)).collect()
}

/// Decode; `None` if the length is not a multiple of the width or a chunk is out of range.
pub fn decode_binary(card: usize, bits: &[bool]) -> Option<Vec<usize>> {
    let k = code_width(card);
    if bits.len() % k != 0 {
        return None;
    }
    bits.chunks(k)
        .map(|ch| {
            let v = ch.iter().enumerate().fold(0usize, |acc, (j, &b)| acc | ((b as usize) << j));
            if v < card {
                Some(v)
            } else {
                None
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn lsb(n: u64, width: usize) -> Vec<u32> {
        (0..width).map(|j| ((n >> j) & 1) as u32).collect()
    }

    fn lsb_value(t: &[u32]) -> u64 {
        t.iter().enumerate().map(|(j, &b)| (b as u64) << j).sum()
    }

    #[test]
    fn srs_rewrites_a_factor_in_context() {
        // ab -> ba on marks {0,1}: 0 = a, 1 = b
        let srs = Srs::new(vec![Rule { lhs: vec![0, 1], rhs: vec![1, 0] }]);
        let s = srs.successors(&[0, 0, 1, 1]);
        assert_eq!(s.len(), 1);
        assert!(s.contains(&vec![0, 1, 0, 1]));
        // two redexes
        let s2 = srs.successors(&[0, 1, 0, 1]);
        assert_eq!(s2.len(), 2);
        assert!(srs.is_irreducible(&[1, 1, 0, 0]));
    }

    #[test]
    fn empty_lhs_inserts_at_every_position() {
        let srs = Srs::new(vec![Rule { lhs: vec![], rhs: vec![7] }]);
        assert_eq!(srs.redexes(&[1, 2]).len(), 3);
        assert_eq!(srs.successors(&[1, 2]).len(), 3);
    }

    #[test]
    fn letter_map_commutes_with_steps() {
        let srs = Srs::new(vec![Rule { lhs: vec![0, 1], rhs: vec![1, 1, 0] }]);
        let f = |m: Mark| m + 10;
        let mapped = srs.map_marks(f);
        let w = vec![0, 0, 1, 1];
        let lhs: BTreeSet<Word> =
            srs.successors(&w).into_iter().map(|x| x.iter().map(|&m| f(m)).collect()).collect();
        let wm: Word = w.iter().map(|&m| f(m)).collect();
        assert_eq!(lhs, mapped.successors(&wm));
    }

    #[test]
    fn bounded_decider_is_exact_on_a_closed_system() {
        // ab -> ba is length preserving: the bounded search is closed at the start length.
        let srs = Srs::new(vec![Rule { lhs: vec![0, 1], rhs: vec![1, 0] }]);
        let start = vec![0, 0, 1, 1];
        let (seen, exceeded) = reach_set_bounded(&srs, &start, 4).unwrap();
        assert!(exceeded.is_none());
        assert_eq!(seen.len(), 6); // all arrangements of two a's and two b's
        assert_eq!(decide_reach(&srs, &start, &[1, 1, 0, 0], 4), Ok(Verdict::Reachable));
        assert_eq!(decide_reach(&srs, &start, &[1, 0, 1, 0], 4), Ok(Verdict::Reachable));
        // b's never move back: unreachable is a complete answer because the search is closed
        assert_eq!(decide_reach(&srs, &[1, 1, 0, 0], &start, 4), Ok(Verdict::Unreachable));
        assert!(seen.len() as u64 <= config_space_size(2, 4));
    }

    #[test]
    fn bounded_decider_reports_bound_exceeded() {
        // a -> aa grows forever
        let srs = Srs::new(vec![Rule { lhs: vec![0], rhs: vec![0, 0] }]);
        for bound in 1..=12usize {
            match decide_reach(&srs, &[0], &[1], bound).unwrap() {
                Verdict::BoundExceeded { from, to } => {
                    assert_eq!(from.len(), bound);
                    assert_eq!(to.len(), bound + 1);
                }
                other => panic!("expected BoundExceeded, got {:?}", other),
            }
        }
        // the target is found when it fits
        assert_eq!(decide_reach(&srs, &[0], &[0, 0, 0], 5), Ok(Verdict::Reachable));
    }

    #[test]
    fn start_outside_bound_is_refused() {
        let srs = Srs::default();
        assert!(matches!(
            decide_reach(&srs, &[0, 0, 0], &[0], 2),
            Err(TmError::StartOutsideBound { len: 3, bound: 2 })
        ));
    }

    #[test]
    fn config_space_size_matches_enumeration() {
        // all words of length <= 3 over 2 marks: 1 + 2 + 4 + 8
        assert_eq!(config_space_size(2, 3), 15);
        assert_eq!(config_space_size(3, 2), 13);
    }

    #[test]
    fn encode_decode_roundtrip_with_padding() {
        let m = incrementer();
        let c = Config { state: 1, left: vec![1, 0, 1], head: 1, right: vec![0, 1] };
        let w = encode(&m, &c);
        assert_eq!(decode(&m, &w), Some(c.normalized()));
        let padded = Config { state: 1, left: vec![1, 0, 1, 0, 0], head: 1, right: vec![0, 1, 0] };
        assert_eq!(decode(&m, &encode(&m, &padded)), Some(c.normalized()));
        assert_eq!(decode(&m, &[0, 1]), None);
    }

    #[test]
    fn incrementer_matches_machine_for_all_small_inputs() {
        let m = incrementer();
        for n in 0u64..=40 {
            for pad in 0..3 {
                let width = (64 - n.leading_zeros()) as usize + pad;
                let input = lsb(n, width);
                let (fin, steps) = run_both(&m, &Config::init(&input), 400).unwrap().unwrap();
                // each carried one costs two steps (write, move); the final write costs one
                let carries = n.trailing_ones() as usize;
                // the head ends on the cell where the carry stopped; read the tape from cell 0
                let mut cells: Vec<u32> = fin.left.clone();
                cells.resize(cells.len().max(carries), 0);
                let mut tape: Vec<u32> = cells[..carries].iter().rev().cloned().collect();
                tape.push(fin.head);
                tape.extend(fin.right.iter());
                assert_eq!(lsb_value(&tape), n + 1, "n = {n}");
                assert_eq!(steps, 2 * carries + 1, "n = {n}");
            }
        }
    }

    #[test]
    fn busy_beaver_2_matches_machine() {
        let m = busy_beaver_2();
        let (fin, steps) = run_both(&m, &Config::init(&[]), 100).unwrap().unwrap();
        assert_eq!(steps, 12);
        assert_eq!(fin.tape().iter().filter(|&&b| b == 1).count(), 4);
        assert_eq!(fin.state, 2);
    }

    #[test]
    fn halted_word_is_irreducible_and_unique_decoding() {
        let m = busy_beaver_2();
        let srs = rules_of(&m);
        let (fin, _) = run_both(&m, &Config::init(&[]), 100).unwrap().unwrap();
        assert!(srs.is_irreducible(&encode(&m, &fin)));
    }

    #[test]
    fn right_runner_is_refused_by_every_bounded_decider() {
        let m = right_runner();
        let srs = rules_of(&m);
        let start = encode(&m, &Config::init(&[]));
        assert_eq!(start.len(), 4);
        let target = vec![Marks::LEND, Marks::REND]; // never reached
        for bound in 4..=24usize {
            match decide_reach(&srs, &start, &target, bound).unwrap() {
                Verdict::BoundExceeded { from, to } => {
                    assert_eq!(to.len(), bound + 1);
                    assert_eq!(from.len(), bound);
                }
                other => panic!("bound {bound}: expected BoundExceeded, got {:?}", other),
            }
        }
        // inside the bound it reaches each word of the run
        let (seen, _) = reach_set_bounded(&srs, &start, 10).unwrap();
        assert_eq!(seen.len(), 7); // lengths 4..=10, one word each
    }

    #[test]
    fn step_simulation_holds_on_every_small_configuration() {
        let m = busy_beaver_2();
        let srs = rules_of(&m);
        // exhaustive over states, scanned symbols and tapes of length at most 3 on each side
        let tapes: Vec<Vec<u32>> = (0..=3usize)
            .flat_map(|len| (0..(1u32 << len)).map(move |bits| (0..len).map(|j| (bits >> j) & 1).collect()))
            .collect();
        let mut checked = 0;
        for q in 0..m.n_states {
            for h in 0..m.n_symbols {
                for l in &tapes {
                    for r in &tapes {
                        let c = Config { state: q, left: l.clone(), head: h, right: r.clone() };
                        check_step_simulation(&m, &srs, &c).unwrap();
                        checked += 1;
                    }
                }
            }
        }
        assert_eq!(checked, 7 * 2 * 15 * 15);
    }

    #[test]
    fn rule_count_is_per_transition_shape() {
        let m = incrementer();
        let srs = rules_of(&m);
        // 2 write rules; 2 right transitions with 2 + 1 rules each
        assert_eq!(srs.rules.len(), 2 + 2 * 3);
        assert_eq!(Marks::of(&m).count(), 2 + 3 + 2);
    }

    #[test]
    fn first_separation_replays_and_admission_is_uncapped() {
        let r = replay_e(&first_separation_history(), &Regime::default()).unwrap();
        assert_eq!(
            r,
            Regime {
                data: 2,
                forms: vec![1],
                insts: vec![(0, vec![0])],
                rules: vec![],
                reqs: vec![(0, 1)]
            }
        );
        for k in [0usize, 1, 7, 1000] {
            let h = vec![Event::AdmitDatum; k];
            assert_eq!(replay_e(&h, &Regime::default()).unwrap().data, k);
        }
        // supply is a no-op
        let s = replay_e(&[Event::Supply(5), Event::Supply(9)], &Regime::default()).unwrap();
        assert_eq!(s, Regime::default());
        // a refused event
        assert!(step_e(&Regime::default(), &Event::AdmitForm(0)).is_none());
    }

    #[test]
    fn separated_alphabets_and_collapse() {
        for n in 0usize..=8 {
            assert!(pairwise_separated(&canonical_regime(n)), "n = {n}");
        }
        let two_bare = Regime { data: 2, ..Regime::default() };
        assert!(collapsed(&two_bare, 0, 1));
        let first = replay_e(&first_separation_history(), &Regime::default()).unwrap();
        assert!(pairwise_separated(&first));
        assert!(!collapsed(&first, 0, 1));
    }

    #[test]
    fn context_count_formula_and_one_hole_splits() {
        for n in 0usize..=4 {
            for a in 1usize..=5 {
                let cs = contexts(n, a);
                assert_eq!(cs.len(), (n + 1).pow(a as u32) - n.pow(a as u32), "n={n} a={a}");
                let one: Vec<&GCtx> =
                    cs.iter().filter(|c| c.iter().filter(|o| o.is_none()).count() == 1).collect();
                let expect = if n == 0 { if a == 1 { 1 } else { 0 } } else { a * n.pow(a as u32 - 1) };
                assert_eq!(one.len(), expect, "one-hole n={n} a={a}");
                // each one-hole context is (u, hole, v) and plugs d to u d v
                for c in one {
                    let i = c.iter().position(Option::is_none).unwrap();
                    let u: Vec<usize> = c[..i].iter().map(|o| o.unwrap()).collect();
                    let v: Vec<usize> = c[i + 1..].iter().map(|o| o.unwrap()).collect();
                    let mut expect_word = u.clone();
                    expect_word.push(99);
                    expect_word.extend(v);
                    assert_eq!(plug1(99, c), expect_word);
                }
            }
        }
    }

    #[test]
    fn binary_coding_roundtrips_and_is_injective() {
        for card in 1usize..=9 {
            let k = code_width(card);
            assert!(card < (1usize << k));
            let mut seen = BTreeSet::new();
            for len in 0..=3usize {
                let total = card.pow(len as u32);
                for idx in 0..total {
                    let mut w = Vec::new();
                    let mut x = idx;
                    for _ in 0..len {
                        w.push(x % card);
                        x /= card;
                    }
                    let bits = encode_binary(card, &w);
                    assert_eq!(bits.len(), k * len);
                    assert_eq!(decode_binary(card, &bits), Some(w.clone()));
                    assert!(seen.insert(bits), "collision for card {card}");
                }
            }
        }
        assert_eq!(code_width(1), 1);
        assert_eq!(code_width(2), 2);
        assert_eq!(code_width(3), 3);
        assert_eq!(code_width(5), 4);
        assert_eq!(decode_binary(3, &[true, true, false]), None); // 3 is out of range
        assert_eq!(decode_binary(3, &[true]), None);
    }
}
