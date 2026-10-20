//! Independent public-boundary allocation observations in a dedicated test binary.
//! Matching a layout is a finite fixture observation, not a global memory bound.
use std::alloc::{GlobalAlloc, Layout, System};
use std::cell::Cell;
use theory_of_finite_qm::homology::errors::HomologicalError;
use theory_of_finite_qm::homology::rank_certificate::{
    certify_rank, certify_rank_with_limits, RankLimits,
};
use theory_of_finite_qm::linear_algebra::{q, BasicMatrix, ExactFieldError, MatrixError, Q};

thread_local! {
    static WATCH: Cell<Option<(usize, usize)>> = const { Cell::new(None) };
    static OBSERVED: Cell<bool> = const { Cell::new(false) };
}
struct WatchingAllocator;
fn record(size: usize, align: usize) {
    let _ = WATCH.try_with(|watch| {
        if watch.get() == Some((size, align)) {
            let _ = OBSERVED.try_with(|flag| flag.set(true));
        }
    });
}
unsafe impl GlobalAlloc for WatchingAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        record(layout.size(), layout.align());
        unsafe { System.alloc(layout) }
    }
    unsafe fn alloc_zeroed(&self, layout: Layout) -> *mut u8 {
        record(layout.size(), layout.align());
        unsafe { System.alloc_zeroed(layout) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        unsafe { System.dealloc(ptr, layout) }
    }
    unsafe fn realloc(&self, ptr: *mut u8, layout: Layout, size: usize) -> *mut u8 {
        record(size, layout.align());
        unsafe { System.realloc(ptr, layout, size) }
    }
}
#[global_allocator]
static ALLOCATOR: WatchingAllocator = WatchingAllocator;
struct ResetWatch;
impl Drop for ResetWatch {
    fn drop(&mut self) {
        WATCH.with(|watch| watch.set(None));
    }
}
fn observe<T>(cells: usize, operation: impl FnOnce() -> T) -> (T, bool) {
    let layout = Layout::array::<Q>(cells).unwrap();
    OBSERVED.with(|flag| flag.set(false));
    WATCH.with(|watch| watch.set(Some((layout.size(), layout.align()))));
    let reset = ResetWatch;
    let output = operation();
    drop(reset);
    (output, OBSERVED.with(Cell::get))
}
fn input() -> BasicMatrix<Q> {
    BasicMatrix::from_row_major(1, 1, vec![q(2)]).unwrap()
}

#[test]
fn observer_detects_the_allocations_it_is_supposed_to_exclude() {
    for cells in [1, 2] {
        let (allocation, observed) = observe(cells, || Vec::<Q>::with_capacity(cells));
        assert!(observed, "layout observer did not see its positive control");
        drop(allocation);
    }
}

#[test]
fn producer_refuses_inverse_work_before_allocating_the_augmented_buffer() {
    let matrix = input();
    let (result, observed) = observe(2, || {
        certify_rank_with_limits(
            &matrix,
            RankLimits {
                max_matrix_cells: 2,
                max_scalar_operations: 5,
            },
        )
    });
    assert!(matches!(
        result,
        Err(HomologicalError::RankInverseFailed {
            source: ExactFieldError::Matrix(MatrixError::OperationLimitExceeded {
                requested: 11,
                limit: 5
            })
        })
    ));
    assert!(
        !observed,
        "inverse allocated its augmented Q buffer before work refusal"
    );
}

#[test]
fn checker_refuses_aggregate_work_before_allocating_identity_or_products() {
    let matrix = input();
    let certificate = certify_rank(&matrix).unwrap();
    let (result, observed) = observe(1, || {
        certificate.verify_against_with_limits(
            &matrix,
            RankLimits {
                max_matrix_cells: 1,
                max_scalar_operations: 0,
            },
        )
    });
    assert!(matches!(
        result,
        Err(HomologicalError::MatrixError(
            MatrixError::OperationLimitExceeded {
                requested: 6,
                limit: 0
            }
        ))
    ));
    assert!(
        !observed,
        "checker copied candidates or allocated before its aggregate work refusal"
    );
}
