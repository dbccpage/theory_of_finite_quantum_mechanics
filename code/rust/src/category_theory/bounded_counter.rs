//! Minimal finite-depth future-legality report for a nonnegative counter.
//!
//! Increment is always legal; decrement requires a positive count. At remaining
//! depth r, the report is min(count,r). Its r+1 classes distinguish exactly the
//! legal continuations of length at most r. Depth decreases after every event:
//! this is not a fixed-depth congruence for unrestricted continuation.
//! AuthorityEffect: None.

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum CounterEvent {
    Increment,
    Decrement,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum CounterBoundary {
    /// Native decrement guard fails within the admitted context depth.
    GuardRefusal,
    /// No answer is claimed about another event at depth zero.
    ContextExhausted,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CounterReportError {
    ClipExceedsDepth,
    DifferentDepths,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct CounterReport {
    remaining: usize,
    clipped: usize,
}

impl CounterReport {
    /// Construct from a bounded machine count. Bigger scalar owners may supply
    /// a checked clip through `try_from_clip`, without narrowing the raw count.
    pub fn from_count(remaining: usize, count: usize) -> Self {
        Self {
            remaining,
            clipped: count.min(remaining),
        }
    }

    pub fn try_from_clip(remaining: usize, clipped: usize) -> Result<Self, CounterReportError> {
        if clipped > remaining {
            return Err(CounterReportError::ClipExceedsDepth);
        }
        Ok(Self { remaining, clipped })
    }

    pub fn remaining(self) -> usize {
        self.remaining
    }
    pub fn clipped(self) -> usize {
        self.clipped
    }

    pub fn advance(self, event: CounterEvent) -> Result<Self, CounterBoundary> {
        let next = self
            .remaining
            .checked_sub(1)
            .ok_or(CounterBoundary::ContextExhausted)?;
        let clipped = match event {
            CounterEvent::Increment => {
                // Avoid overflow even when remaining == clipped == usize::MAX.
                if self.clipped >= next {
                    next
                } else {
                    self.clipped + 1
                }
            }
            CounterEvent::Decrement => self
                .clipped
                .checked_sub(1)
                .ok_or(CounterBoundary::GuardRefusal)?
                .min(next),
        };
        Ok(Self {
            remaining: next,
            clipped,
        })
    }

    /// Returns the first boundary met. A guard failure already observed within
    /// the budget stays a failure even if an unexecuted suffix is longer.
    pub fn observe(self, word: &[CounterEvent]) -> Result<Self, CounterBoundary> {
        word.iter()
            .try_fold(self, |state, &event| state.advance(event))
    }

    /// Number of consecutive decrements separating distinct classes at the
    /// same depth. No word is allocated. None means equivalent guarded futures.
    pub fn separating_removals(self, other: Self) -> Result<Option<usize>, CounterReportError> {
        if self.remaining != other.remaining {
            return Err(CounterReportError::DifferentDepths);
        }
        Ok((self.clipped != other.clipped).then(|| self.clipped.min(other.clipped) + 1))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn words(length: usize) -> Vec<Vec<CounterEvent>> {
        (0..(1usize << length))
            .map(|bits| (0..length).map(|i| if bits & (1 << i) == 0 {
                CounterEvent::Increment
            } else { CounterEvent::Decrement }).collect())
            .collect()
    }

    // Independent native-state model: it never stores or updates a clipped
    // report. u128 accommodates every tested usize count plus six increments.
    fn native(mut depth: usize, mut count: u128, word: &[CounterEvent])
        -> Result<(usize, usize), CounterBoundary>
    {
        for event in word {
            if depth == 0 { return Err(CounterBoundary::ContextExhausted); }
            if *event == CounterEvent::Decrement && count == 0 {
                return Err(CounterBoundary::GuardRefusal);
            }
            depth -= 1;
            match event {
                CounterEvent::Increment => count += 1,
                CounterEvent::Decrement => count -= 1,
            }
        }
        Ok((depth, usize::try_from(count.min(depth as u128)).unwrap()))
    }

    #[test]
    fn every_short_word_matches_native_count_and_first_boundary() {
        let counts: Vec<u128> = (0..10).chain([
            usize::MAX as u128 - 1, usize::MAX as u128,
            usize::MAX as u128 + 1,
        ]).collect();
        for depth in [0, 1, 2, 3, 4, 6, usize::MAX] {
            for &count in &counts {
                let clip = usize::try_from(count.min(depth as u128)).unwrap();
                let report = CounterReport::try_from_clip(depth, clip).unwrap();
                if let Ok(machine_count) = usize::try_from(count) {
                    assert_eq!(CounterReport::from_count(depth, machine_count), report);
                }
                for length in 0..=6 {
                    for word in words(length) {
                        let got = report.observe(&word).map(|value| (value.remaining(), value.clipped()));
                        assert_eq!(got, native(depth, count, &word),
                            "depth={depth}, count={count}, word={word:?}");
                    }
                }
            }
        }
    }

    #[test]
    fn admission_and_cross_depth_comparison_are_explicit_refusals() {
        for depth in [0, 1, 5, usize::MAX - 1] {
            assert_eq!(CounterReport::try_from_clip(depth, depth + 1),
                Err(CounterReportError::ClipExceedsDepth));
        }
        assert_eq!(CounterReport::from_count(0, 0).separating_removals(
            CounterReport::from_count(1, 0)), Err(CounterReportError::DifferentDepths));
        assert_eq!(CounterReport::from_count(1, 0).observe(&[
            CounterEvent::Decrement, CounterEvent::Increment]), Err(CounterBoundary::GuardRefusal));
        assert_eq!(CounterReport::from_count(0, 0).advance(CounterEvent::Decrement),
            Err(CounterBoundary::ContextExhausted));
    }

    #[test]
    fn separators_are_minimal_for_future_legality_not_final_report_values() {
        for depth in 0..=5 {
            for left in 0..=depth {
                for right in 0..=depth {
                    let first = CounterReport::try_from_clip(depth, left).unwrap();
                    let second = CounterReport::try_from_clip(depth, right).unwrap();
                    let witness = first.separating_removals(second).unwrap();
                    if left == right {
                        assert_eq!(witness, None);
                        continue;
                    }
                    let length = witness.expect("distinct future classes need a separator");
                    assert!(length > 0 && length <= depth);
                    let word = vec![CounterEvent::Decrement; length];
                    assert_ne!(first.observe(&word).map(|_| ()), second.observe(&word).map(|_| ()));
                    for shorter in 0..length {
                        for word in words(shorter) {
                            assert_eq!(first.observe(&word).map(|_| ()), second.observe(&word).map(|_| ()),
                                "a shorter word distinguished {left}, {right} at depth {depth}");
                        }
                    }
                }
            }
        }
    }

    #[test]
    fn maximum_native_depth_needs_no_word_allocation_or_wrapping() {
        let full = CounterReport::try_from_clip(usize::MAX, usize::MAX).unwrap();
        let below = CounterReport::try_from_clip(usize::MAX, usize::MAX - 1).unwrap();
        assert_eq!(full.separating_removals(below), Ok(Some(usize::MAX)));
        assert_eq!(full.separating_removals(full), Ok(None));
        let incremented = full.advance(CounterEvent::Increment).unwrap();
        assert_eq!(incremented.remaining(), usize::MAX - 1);
        assert_eq!(incremented.clipped(), usize::MAX - 1);
        assert_eq!(full.observe(&[]), Ok(full));
    }
}
