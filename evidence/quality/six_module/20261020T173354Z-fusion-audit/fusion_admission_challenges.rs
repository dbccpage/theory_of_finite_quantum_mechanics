#[cfg(test)]
mod admission_review {
    use super::*;
    use std::alloc::{GlobalAlloc,Layout,System};
    use std::sync::atomic::{AtomicBool,AtomicUsize,Ordering};

    // The runner executes exactly one test thread, so the guarded interval has
    // no other test allocations. Only this test fixture installs instrumentation.
    static MONITOR:AtomicBool=AtomicBool::new(false);
    static ALLOCATIONS:AtomicUsize=AtomicUsize::new(0);
    struct ObservedAllocator;
    unsafe impl GlobalAlloc for ObservedAllocator {
        unsafe fn alloc(&self,layout:Layout)->*mut u8 {
            if MONITOR.load(Ordering::Relaxed) {ALLOCATIONS.fetch_add(1,Ordering::Relaxed);}
            unsafe {System.alloc(layout)}
        }
        unsafe fn dealloc(&self,p:*mut u8,layout:Layout) {unsafe {System.dealloc(p,layout)}}
        unsafe fn realloc(&self,p:*mut u8,layout:Layout,size:usize)->*mut u8 {
            if MONITOR.load(Ordering::Relaxed) {ALLOCATIONS.fetch_add(1,Ordering::Relaxed);}
            unsafe {System.realloc(p,layout,size)}
        }
    }
    #[global_allocator]
    static ALLOCATOR:ObservedAllocator=ObservedAllocator;

    fn allocations<T>(call:impl FnOnce()->T)->(T,usize) {
        ALLOCATIONS.store(0,Ordering::Relaxed);MONITOR.store(true,Ordering::Relaxed);
        let result=call();MONITOR.store(false,Ordering::Relaxed);
        (result,ALLOCATIONS.load(Ordering::Relaxed))
    }
    #[test]
    fn rank_admission_precedes_name_and_array_allocations() {
        let (result,count)=allocations(||FusionTable::new(MAX_RANK+1,vec![]));
        assert!(matches!(result,Err(FusionError::RankOutOfRange{rank:33,max:32})));assert_eq!(count,0,"names allocated before rank refusal");
        let data=[[[0u64;33];33];33];
        let (result,count)=allocations(||FusionTable::from_array(data));
        assert!(matches!(result,Err(FusionError::RankOutOfRange{rank:33,max:32})));assert_eq!(count,0,"array flattened before rank refusal");
    }
    #[test]
    fn cyclic_group_admission_precedes_names() {
        let (result,count)=allocations(||FusionRing::z_n(MAX_RANK+1));
        assert!(matches!(result,Err(FusionError::RankOutOfRange{rank:33,max:32})));assert_eq!(count,0);
    }
    #[test]
    fn su2_maximum_is_typed_refusal() {assert!(FusionRing::su2_level(usize::MAX).is_err());}
}
