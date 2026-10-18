#![cfg(any())]

use super::term::Term;

pub fn shift(t: &mut Term, amount: isize, cutoff: usize) {
    match t {
        Term::Var(idx) => {
            if idx.0 >= cutoff {
                idx.0 = (idx.0 as isize + amount) as usize;
            }
        }
        Term::Pi {
            domain, codomain, ..
        } => {
            shift(domain, amount, cutoff);
            shift(codomain, amount, cutoff + 1);
        }
        Term::Lambda { body, .. } => {
            shift(body, amount, cutoff + 1);
        }
        Term::App { func, arg } => {
            shift(func, amount, cutoff);
            shift(arg, amount, cutoff);
        }
        Term::Sigma {
            fst_type, snd_type, ..
        } => {
            shift(fst_type, amount, cutoff);
            shift(snd_type, amount, cutoff + 1);
        }
        Term::Pair { fst, snd } => {
            shift(fst, amount, cutoff);
            shift(snd, amount, cutoff);
        }
        Term::Fst(e) | Term::Snd(e) | Term::Refl(e) | Term::NatSucc(e) => {
            shift(e, amount, cutoff);
        }
        Term::IdType { ty, lhs, rhs } => {
            shift(ty, amount, cutoff);
            shift(lhs, amount, cutoff);
            shift(rhs, amount, cutoff);
        }
        Term::Abort { ty, expr } => {
            shift(ty, amount, cutoff);
            shift(expr, amount, cutoff);
        }
        Term::BoolElim {
            ty,
            m_true,
            m_false,
            expr,
        } => {
            shift(ty, amount, cutoff);
            shift(m_true, amount, cutoff);
            shift(m_false, amount, cutoff);
            shift(expr, amount, cutoff);
        }
        Term::NatElim {
            ty,
            m_zero,
            m_succ,
            expr,
        } => {
            shift(ty, amount, cutoff);
            shift(m_zero, amount, cutoff);
            shift(m_succ, amount, cutoff);
            shift(expr, amount, cutoff);
        }
        Term::Free(_)
        | Term::Universe(_)
        | Term::UnitType
        | Term::UnitVal
        | Term::EmptyType
        | Term::BoolType
        | Term::BoolTrue
        | Term::BoolFalse
        | Term::NatType
        | Term::NatZero => {}
    }
}

pub fn substitute(t: &mut Term, index: usize, repl: &Term) {
    match t {
        Term::Var(idx) => {
            if idx.0 == index {
                *t = repl.clone();
            } else if idx.0 > index {
                idx.0 -= 1;
            }
        }
        Term::Pi {
            domain, codomain, ..
        } => {
            substitute(domain, index, repl);
            let mut repl_shifted = repl.clone();
            shift(&mut repl_shifted, 1, 0);
            substitute(codomain, index + 1, &repl_shifted);
        }
        Term::Lambda { body, .. } => {
            let mut repl_shifted = repl.clone();
            shift(&mut repl_shifted, 1, 0);
            substitute(body, index + 1, &repl_shifted);
        }
        Term::App { func, arg } => {
            substitute(func, index, repl);
            substitute(arg, index, repl);
        }
        Term::Sigma {
            fst_type, snd_type, ..
        } => {
            substitute(fst_type, index, repl);
            let mut repl_shifted = repl.clone();
            shift(&mut repl_shifted, 1, 0);
            substitute(snd_type, index + 1, &repl_shifted);
        }
        Term::Pair { fst, snd } => {
            substitute(fst, index, repl);
            substitute(snd, index, repl);
        }
        Term::Fst(e) | Term::Snd(e) | Term::Refl(e) | Term::NatSucc(e) => {
            substitute(e, index, repl);
        }
        Term::IdType { ty, lhs, rhs } => {
            substitute(ty, index, repl);
            substitute(lhs, index, repl);
            substitute(rhs, index, repl);
        }
        Term::Abort { ty, expr } => {
            substitute(ty, index, repl);
            substitute(expr, index, repl);
        }
        Term::BoolElim {
            ty,
            m_true,
            m_false,
            expr,
        } => {
            substitute(ty, index, repl);
            substitute(m_true, index, repl);
            substitute(m_false, index, repl);
            substitute(expr, index, repl);
        }
        Term::NatElim {
            ty,
            m_zero,
            m_succ,
            expr,
        } => {
            substitute(ty, index, repl);
            substitute(m_zero, index, repl);
            substitute(m_succ, index, repl);
            substitute(expr, index, repl);
        }
        Term::Free(_)
        | Term::Universe(_)
        | Term::UnitType
        | Term::UnitVal
        | Term::EmptyType
        | Term::BoolType
        | Term::BoolTrue
        | Term::BoolFalse
        | Term::NatType
        | Term::NatZero => {}
    }
}

pub fn instantiate(scope: &mut Term, arg: &Term) {
    let arg_shifted = arg.clone();
    substitute(scope, 0, &arg_shifted);
}
