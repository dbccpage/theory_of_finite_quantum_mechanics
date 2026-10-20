use std::alloc::{GlobalAlloc, Layout, System};
use std::cell::Cell;
use tfqm_homotopy_type_theory::a_infinity::{AlgebraLimits, StrictAInfinity};
thread_local! {static WATCH:Cell<bool>=const{Cell::new(false)};static SEEN:Cell<bool>=const{Cell::new(false)};}
struct Observer;
fn record(size: usize, align: usize) {
    let _ = WATCH.try_with(|w| {
        if w.get() && size == 4 && align == 2 {
            let _ = SEEN.try_with(|s| s.set(true));
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
        WATCH.with(|w| w.set(false));
    }
}
fn observe<T>(f: impl FnOnce() -> T) -> (T, bool) {
    SEEN.with(|s| s.set(false));
    WATCH.with(|w| w.set(true));
    let reset = Reset;
    let value = f();
    drop(reset);
    (value, SEEN.with(Cell::get))
}
fn algebra() -> StrictAInfinity {
    StrictAInfinity::try_new(
        2,
        vec![0, 0],
        vec![0; 4],
        vec![0; 8],
        AlgebraLimits::default(),
    )
    .unwrap()
}
#[test]
fn positive_control_observes_the_output_layout() {
    let (v, seen) = observe(|| Vec::<u16>::with_capacity(2));
    assert!(seen);
    drop(v);
}
#[test]
fn invalid_coefficient_precedes_output_allocation() {
    let a = algebra();
    let (r, seen) = observe(|| a.evaluate(&[&[2, 0]], AlgebraLimits::default()));
    assert!(r.is_err());
    assert!(!seen);
}
#[test]
fn invalid_shape_precedes_output_allocation() {
    let a = algebra();
    let (r, seen) = observe(|| a.evaluate(&[&[0]], AlgebraLimits::default()));
    assert!(r.is_err());
    assert!(!seen);
}
#[test]
fn work_refusal_precedes_output_allocation() {
    let a = algebra();
    let (r, seen) = observe(|| {
        a.evaluate(
            &[&[0, 0]],
            AlgebraLimits {
                max_field_operations: 7,
                ..AlgebraLimits::default()
            },
        )
    });
    assert!(r.is_err());
    assert!(!seen);
}
