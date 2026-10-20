use std::alloc::{GlobalAlloc, Layout, System};
use std::cell::Cell;
use tfqm_homotopy_type_theory::substitution::{shift, substitute, Term, TermLimits, Token};
thread_local! {
    static WATCH: Cell<Option<(usize,usize)>> = const { Cell::new(None) };
    static OBSERVED: Cell<bool> = const { Cell::new(false) };
}
struct Observer;
fn record(size: usize, align: usize) {
    let _ = WATCH.try_with(|w| {
        if w.get() == Some((size, align)) {
            let _ = OBSERVED.try_with(|f| f.set(true));
        }
    });
}
unsafe impl GlobalAlloc for Observer {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 {
        record(l.size(), l.align());
        unsafe { System.alloc(l) }
    }
    unsafe fn alloc_zeroed(&self, l: Layout) -> *mut u8 {
        record(l.size(), l.align());
        unsafe { System.alloc_zeroed(l) }
    }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) {
        unsafe { System.dealloc(p, l) }
    }
    unsafe fn realloc(&self, p: *mut u8, l: Layout, s: usize) -> *mut u8 {
        record(s, l.align());
        unsafe { System.realloc(p, l, s) }
    }
}
#[global_allocator]
static ALLOCATOR: Observer = Observer;
struct Reset;
impl Drop for Reset {
    fn drop(&mut self) {
        WATCH.with(|w| w.set(None));
    }
}
fn observe<T>(count: usize, f: impl FnOnce() -> T) -> (T, bool) {
    let l = Layout::array::<Token>(count).unwrap();
    OBSERVED.with(|v| v.set(false));
    WATCH.with(|w| w.set(Some((l.size(), l.align()))));
    let reset = Reset;
    let output = f();
    drop(reset);
    (output, OBSERVED.with(Cell::get))
}
fn term(tokens: Vec<Token>) -> Term {
    Term::try_new(tokens, TermLimits::default()).unwrap()
}
#[test]
fn observation_positive_control() {
    for count in [1, 2] {
        let (v, seen) = observe(count, || Vec::<Token>::with_capacity(count));
        assert!(seen);
        drop(v);
    }
}
#[test]
fn shift_refuses_variable_underflow_before_output_allocation() {
    let input = term(vec![Token::Var(0)]);
    let (result, seen) = observe(1, || shift(&input, -1, 0, TermLimits::default()));
    assert!(result.is_err());
    assert!(!seen, "shift allocated output before checking underflow");
}
#[test]
fn substitution_refuses_lift_overflow_before_output_allocation() {
    let input = term(vec![Token::Lambda, Token::Var(1)]);
    let argument = term(vec![Token::Var(usize::MAX)]);
    let (result, seen) = observe(2, || {
        substitute(&input, 0, &argument, TermLimits::default())
    });
    assert!(result.is_err());
    assert!(
        !seen,
        "substitution allocated output before checking replacement lift"
    );
}
