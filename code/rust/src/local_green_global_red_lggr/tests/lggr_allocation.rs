//! Standalone allocation-order regression binary.
//! The observer is armed only around a call on the current test thread.
//! Allocation requests always delegate to System: no deliberate panic or abort.
//! Unsafe code is confined to forwarding GlobalAlloc's contracts unchanged.

use std::alloc::{GlobalAlloc, Layout, System};
use std::cell::Cell;

use num_rational::BigRational;
use omega_linear_algebra::backend::basic_matrix::BasicMatrix;
use tfqm_local_green_global_red_lggr::lggr_v::{
    check_soundness, verify_unsoundness_witness, LggrSoundnessError, MAX_LGGR_CELLS,
};

thread_local! {
    static ARMED: Cell<bool> = const { Cell::new(false) };
    static MAX_SINGLE: Cell<usize> = const { Cell::new(0) };
}

#[test]
fn witness_verifier_refuses_an_oversized_product_profile() {
    let one = BigRational::from_integer(1.into());
    let d = BasicMatrix::from_row_major(1, 65, vec![one.clone(); 65]).unwrap();
    let q = BasicMatrix::from_row_major(65, 1, vec![one.clone(); 65]).unwrap();
    assert_eq!(
        verify_unsoundness_witness(&d, &q, &vec![one; 65]).unwrap_err(),
        LggrSoundnessError::BudgetUnknown {
            cells: 4225,
            limit: MAX_LGGR_CELLS
        }
    );
}

fn observe(size: usize) {
    // Constant TLS initializers do not allocate. try_with also tolerates TLS
    // teardown; never format, log, panic or allocate in this allocator path.
    let _ = ARMED.try_with(|armed| {
        if armed.get() {
            let _ = MAX_SINGLE.try_with(|maximum| maximum.set(maximum.get().max(size)));
        }
    });
}

struct ProbeAllocator;

// SAFETY: Every allocation operation forwards its unchanged pointer/layout contract to System.
unsafe impl GlobalAlloc for ProbeAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        observe(layout.size());
        // SAFETY: Forward the caller's valid GlobalAlloc arguments unchanged.
        unsafe { System.alloc(layout) }
    }
    unsafe fn alloc_zeroed(&self, layout: Layout) -> *mut u8 {
        observe(layout.size());
        // SAFETY: Forward the caller's valid GlobalAlloc arguments unchanged.
        unsafe { System.alloc_zeroed(layout) }
    }
    unsafe fn realloc(&self, ptr: *mut u8, old: Layout, size: usize) -> *mut u8 {
        observe(size);
        // SAFETY: Forward the caller's valid GlobalAlloc arguments unchanged.
        unsafe { System.realloc(ptr, old, size) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        // SAFETY: Forward the caller's valid GlobalAlloc arguments unchanged.
        unsafe { System.dealloc(ptr, layout) }
    }
}

#[global_allocator]
static ALLOCATOR: ProbeAllocator = ProbeAllocator;

struct Disarm;
impl Drop for Disarm {
    fn drop(&mut self) {
        ARMED.with(|armed| armed.set(false));
    }
}

fn measure<T>(operation: impl FnOnce() -> T) -> (T, usize) {
    MAX_SINGLE.with(|maximum| maximum.set(0));
    ARMED.with(|armed| armed.set(true));
    let disarm = Disarm;
    let result = operation();
    drop(disarm);
    (result, MAX_SINGLE.with(Cell::get))
}

#[test]
fn oversize_output_refuses_before_the_old_dense_allocation() {
    // All construction and assertions occur while unarmed. Only this thread's
    // measured call is observed, even if the Rust harness has other threads.
    let one = BigRational::from_integer(1.into());
    let d = BasicMatrix::from_row_major(1, 65, vec![one.clone(); 65]).unwrap();
    let q = BasicMatrix::from_row_major(65, 1, vec![one; 65]).unwrap();
    let allowed_single_allocation = MAX_LGGR_CELLS * std::mem::size_of::<BigRational>();

    // Bounded positive control: 4225 entries is deliberately small. This proves
    // the probe observes the old multiplication mechanism, not a synthetic OOM.
    let (product, old_maximum) = measure(|| q.mul(&d));
    assert_eq!(product.as_ref().unwrap().shape(), (65, 65));
    assert!(old_maximum > allowed_single_allocation);
    drop(product);

    let (result, maximum) = measure(|| check_soundness(&d, &q));
    assert_eq!(
        result.unwrap_err(),
        LggrSoundnessError::BudgetUnknown {
            cells: 4225,
            limit: MAX_LGGR_CELLS,
        }
    );
    assert!(
        maximum <= allowed_single_allocation,
        "output refusal followed an oversized allocation request"
    );
}

#[test]
fn zero_image_refusal_precedes_observation_vector_allocation() {
    let zero = BigRational::from_integer(0.into());
    let one = BigRational::from_integer(1.into());
    let d = BasicMatrix::from_row_major(1, 1, vec![zero.clone()]).unwrap();
    let q =
        BasicMatrix::from_row_major(MAX_LGGR_CELLS, 1, vec![zero.clone(); MAX_LGGR_CELLS]).unwrap();
    let output_bytes = MAX_LGGR_CELLS * std::mem::size_of::<BigRational>();
    let (positive, observed) = measure(|| q.checked_mul_vec_with_limit(&[zero], MAX_LGGR_CELLS));
    assert_eq!(positive.unwrap().len(), MAX_LGGR_CELLS);
    assert!(
        observed >= output_bytes,
        "positive control missed the observation vector"
    );
    let (result, observed) = measure(|| verify_unsoundness_witness(&d, &q, &[one]));
    assert_eq!(result, Ok(false));
    assert!(
        observed < output_bytes,
        "zero-image refusal allocated Q(Dv)"
    );
}
