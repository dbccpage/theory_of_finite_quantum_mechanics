//! Staged exact scalar/matrix boundary allocation observations. AuthorityEffect: None.
//! Matching a layout is a finite fixture observation, not a global memory bound.
use std::alloc::{GlobalAlloc, Layout, System};
use std::cell::Cell;
use theory_of_finite_qm::linear_algebra::basic_matrix::{
    BasicMatrix, CheckedMatrixError, MatrixError, OperationLimits,
};
use theory_of_finite_qm::linear_algebra::scalars::{q, Q};
thread_local! {
    static WATCH: Cell<Option<(usize, usize)>> = const { Cell::new(None) };
    static OBSERVED: Cell<bool> = const { Cell::new(false) };
    static ALLOCATION_COUNT: Cell<usize> = const { Cell::new(0) };
}
struct WatchingAllocator;
fn record(size: usize, align: usize) {
    let _ = WATCH.try_with(|watch| {
        if watch.get() == Some((size, align)) {
            let _ = OBSERVED.try_with(|flag| flag.set(true));
            let _ = ALLOCATION_COUNT.try_with(|count| count.set(count.get() + 1));
        }
    });
}
unsafe impl GlobalAlloc for WatchingAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        record(layout.size(), layout.align());
        // SAFETY: Forward the unchanged allocation/deallocation contract to System.
        unsafe { System.alloc(layout) }
    }
    unsafe fn alloc_zeroed(&self, layout: Layout) -> *mut u8 {
        record(layout.size(), layout.align());
        // SAFETY: Forward the unchanged allocation/deallocation contract to System.
        unsafe { System.alloc_zeroed(layout) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        // SAFETY: Forward the unchanged allocation/deallocation contract to System.
        unsafe { System.dealloc(ptr, layout) }
    }
    unsafe fn realloc(&self, ptr: *mut u8, layout: Layout, size: usize) -> *mut u8 {
        record(size, layout.align());
        // SAFETY: Forward the unchanged allocation/deallocation contract to System.
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
    ALLOCATION_COUNT.with(|count| count.set(0));
    WATCH.with(|watch| watch.set(Some((layout.size(), layout.align()))));
    let reset = ResetWatch;
    let output = operation();
    drop(reset);
    (output, OBSERVED.with(Cell::get))
}

#[test]
fn constant_polynomial_uses_one_output_buffer_without_a_discarded_product() {
    let matrix = BasicMatrix::from_row_major(2, 2, vec![q(1); 4]).unwrap();
    let coefficients = [q(2)];
    let (result, observed) = observe(4, || {
        theory_of_finite_qm::linear_algebra::char_poly::evaluate_polynomial_at_matrix(
            &coefficients,
            &matrix,
        )
    });
    assert_eq!(result.unwrap().as_slice(), &[q(2), q(0), q(0), q(2)]);
    assert!(observed, "the output buffer was not observed");
    assert_eq!(
        ALLOCATION_COUNT.with(Cell::get),
        1,
        "constant evaluation allocated a redundant full output buffer"
    );
}

#[test]
fn observer_positive_control_detects_the_output_layout() {
    let (matrix, observed) = observe(4096, || BasicMatrix::<Q>::zero(4096, 1));
    assert!(matrix.is_ok());
    assert!(observed);
}
#[test]
fn matrix_and_vector_arithmetic_refuse_both_raw_roles_before_output_reservation() {
    let zero = BasicMatrix::from_row_major(4096, 1, vec![q(0); 4096]).unwrap();
    let row = BasicMatrix::from_row_major(1, 4096, vec![q(0); 4096]).unwrap();
    let bad = BasicMatrix::from_row_major(1, 1, vec![Q::new_raw(1.into(), 0.into())]).unwrap();
    let (left, allocated) = observe(4096, || bad.mul(&row));
    assert!(matches!(left, Err(CheckedMatrixError::Scalar(_))));
    assert!(!allocated);
    let (right, allocated) = observe(4096, || zero.mul(&bad));
    assert!(matches!(right, Err(CheckedMatrixError::Scalar(_))));
    assert!(!allocated);
    let (vector, allocated) = observe(4096, || zero.mul_vec(bad.as_slice()));
    assert!(matches!(vector, Err(CheckedMatrixError::Scalar(_))));
    assert!(!allocated);
}
#[test]
fn element_and_work_admission_precedes_domain_validation_and_allocation() {
    let bad = BasicMatrix::from_row_major(1, 1, vec![Q::new_raw(1.into(), 0.into())]).unwrap();
    let row = BasicMatrix::from_row_major(1, 4096, vec![q(0); 4096]).unwrap();
    let (limited, allocated) = observe(4096, || {
        bad.checked_mul_with_limits(
            &row,
            OperationLimits {
                max_elements: 4095,
                max_scalar_ops: usize::MAX,
            },
        )
    });
    assert!(matches!(
        limited,
        Err(CheckedMatrixError::Matrix(
            MatrixError::AllocationLimitExceeded {
                requested: 4096,
                limit: 4095
            }
        ))
    ));
    assert!(!allocated);
    let (limited, allocated) = observe(4096, || {
        bad.checked_mul_with_limits(
            &row,
            OperationLimits {
                max_elements: 4096,
                max_scalar_ops: 8191,
            },
        )
    });
    assert!(matches!(
        limited,
        Err(CheckedMatrixError::Matrix(
            MatrixError::OperationLimitExceeded {
                requested: 8192,
                limit: 8191
            }
        ))
    ));
    assert!(!allocated);
}
