pub const ORIGIN: &str = "Origin: code/rust/src/category_theory/bounded_counter.rs";
pub const CLAIM: &str = "Claim: urn:tfqm:category-theory:bounded_counter:clip-does-not-exceed-remaining";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: &str = "killed=3;suite=require_agreement_eq_flip,fold_carrier_add_to_sub,refuse_empty_eq_flip";

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum CounterEvent {
    Increment,
    Decrement,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum CounterBoundary {
    GuardRefusal { invariant: &'static str, measured: usize },
    ContextExhausted { invariant: &'static str, measured: usize },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CounterReportError {
    ClipExceedsDepth { invariant: &'static str, measured: usize, bound: usize },
    DifferentDepths { invariant: &'static str, measured: usize, expected: usize },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CounterCertError {
    FloatRefused { invariant: &'static str, measured_len: usize },
    EmptyCarrier { invariant: &'static str, measured: usize },
    ClaimFailed { invariant: &'static str, measured: i64, expected: i64 },
    Overflow { invariant: &'static str, measured: i64 },
}

impl std::fmt::Display for CounterCertError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for CounterCertError {}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct CounterReport {
    remaining: usize,
    clipped: usize,
}

impl CounterReport {
    pub fn from_count(remaining: usize, count: usize) -> Self {
        Self {
            remaining,
            clipped: count.min(remaining),
        }
    }

    pub fn try_from_clip(remaining: usize, clipped: usize) -> Result<Self, CounterReportError> {
        if clipped > remaining {
            return Err(CounterReportError::ClipExceedsDepth {
                invariant: "bounded-counter-clip-within-remaining",
                measured: clipped,
                bound: remaining,
            });
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
        let next = match self.remaining.checked_sub(1) {
            Some(value) => value,
            None => {
                return Err(CounterBoundary::ContextExhausted {
                    invariant: "bounded-counter-remaining-before-advance",
                    measured: self.remaining,
                });
            }
        };
        let clipped = apply_event(self.clipped, next, event)?;
        Ok(Self {
            remaining: next,
            clipped,
        })
    }

    pub fn observe(self, word: &[CounterEvent]) -> Result<Self, CounterBoundary> {
        let mut state = self;
        for event in word {
            state = state.advance(*event)?;
        }
        Ok(state)
    }

    pub fn separating_removals(self, other: Self) -> Result<Option<usize>, CounterReportError> {
        if self.remaining != other.remaining {
            return Err(CounterReportError::DifferentDepths {
                invariant: "bounded-counter-separating-depths-equal",
                measured: self.remaining,
                expected: other.remaining,
            });
        }
        removal_index(self.clipped, other.clipped)
    }
}

fn apply_event(clipped: usize, next: usize, event: CounterEvent) -> Result<usize, CounterBoundary> {
    match event {
        CounterEvent::Increment => incremented(clipped, next),
        CounterEvent::Decrement => decremented(clipped, next),
    }
}

fn incremented(clipped: usize, next: usize) -> Result<usize, CounterBoundary> {
    if clipped >= next {
        return Ok(next);
    }
    match clipped.checked_add(1) {
        Some(value) => Ok(value),
        None => Err(CounterBoundary::GuardRefusal {
            invariant: "bounded-counter-increment-fits-usize",
            measured: clipped,
        }),
    }
}

fn decremented(clipped: usize, next: usize) -> Result<usize, CounterBoundary> {
    let reduced = match clipped.checked_sub(1) {
        Some(value) => value,
        None => {
            return Err(CounterBoundary::GuardRefusal {
                invariant: "bounded-counter-decrement-guard",
                measured: clipped,
            });
        }
    };
    Ok(reduced.min(next))
}

fn removal_index(left: usize, right: usize) -> Result<Option<usize>, CounterReportError> {
    if left == right {
        return Ok(None);
    }
    match left.min(right).checked_add(1) {
        Some(value) => Ok(Some(value)),
        None => Err(CounterReportError::ClipExceedsDepth {
            invariant: "bounded-counter-removal-index-fits-usize",
            measured: left,
            bound: right,
        }),
    }
}

fn refuse_empty(objects: usize) -> Result<(), CounterCertError> {
    if objects == 0 {
        return Err(CounterCertError::EmptyCarrier {
            invariant: "bounded-counter-carrier-nonempty",
            measured: objects,
        });
    }
    Ok(())
}

fn fold_carrier(measured: i64, objects: usize) -> Result<i64, CounterCertError> {
    let width = match i64::try_from(objects) {
        Ok(value) => value,
        Err(_) => {
            return Err(CounterCertError::Overflow {
                invariant: "bounded-counter-width-fits-i64",
                measured,
            });
        }
    };
    measured.checked_add(width).ok_or(CounterCertError::Overflow {
        invariant: "bounded-counter-folded-width-fits-i64",
        measured,
    })
}

pub fn require_agreement(measured: i64, expected: i64) -> Result<i64, CounterCertError> {
    if measured == expected {
        return Ok(measured);
    }
    Err(CounterCertError::ClaimFailed {
        invariant: "bounded-counter-width-doubles",
        measured,
        expected,
    })
}

fn expected_double(objects: usize) -> Result<i64, CounterCertError> {
    let width = match i64::try_from(objects) {
        Ok(value) => value,
        Err(_) => {
            return Err(CounterCertError::Overflow {
                invariant: "bounded-counter-double-fits-i64",
                measured: 0,
            });
        }
    };
    width.checked_add(width).ok_or(CounterCertError::Overflow {
        invariant: "bounded-counter-double-fits-i64",
        measured: width,
    })
}

pub fn depth_certificate(objects: usize) -> Result<i64, CounterCertError> {
    refuse_empty(objects)?;
    let measured = match i64::try_from(objects) {
        Ok(value) => value,
        Err(_) => {
            return Err(CounterCertError::Overflow {
                invariant: "bounded-counter-measured-width-fits-i64",
                measured: 0,
            });
        }
    };
    finish_depth(measured, objects)
}

fn finish_depth(measured: i64, objects: usize) -> Result<i64, CounterCertError> {
    let folded = fold_carrier(measured, objects)?;
    let expected = expected_double(objects)?;
    require_agreement(folded, expected)
}

fn text_has_byte(text: &str, target: u8) -> bool {
    for byte in text.bytes() {
        if byte == target {
            return true;
        }
    }
    false
}

fn text_refused(text: &str) -> bool {
    if text.is_empty() {
        return true;
    }
    if text_has_byte(text, 46) {
        return true;
    }
    if text_has_byte(text, 101) {
        return true;
    }
    if text_has_byte(text, 69) {
        return true;
    }
    false
}

fn split_sign(text: &str) -> (i64, &str) {
    if text.starts_with('-') {
        let rest = match text.get(1..) {
            Some(value) => value,
            None => "",
        };
        return (-1, rest);
    }
    (1, text)
}

fn digits_only(text: &str) -> bool {
    if text.is_empty() {
        return false;
    }
    for byte in text.bytes() {
        if !byte.is_ascii_digit() {
            return false;
        }
    }
    true
}

fn accumulate_digits(text: &str) -> Result<i64, CounterCertError> {
    let mut value = 0i64;
    for byte in text.bytes() {
        value = value.checked_mul(10).ok_or(CounterCertError::Overflow {
            invariant: "parsed-integer-fits-i64",
            measured: value,
        })?;
        let digit = i64::from(byte - 48);
        value = value.checked_add(digit).ok_or(CounterCertError::Overflow {
            invariant: "parsed-integer-fits-i64",
            measured: value,
        })?;
    }
    Ok(value)
}

pub fn parse_exact_i64(text: &str) -> Result<i64, CounterCertError> {
    if text_refused(text) {
        return Err(CounterCertError::FloatRefused {
            invariant: "public-boundary-refuses-binary64-text",
            measured_len: text.len(),
        });
    }
    let (sign, digits) = split_sign(text);
    if !digits_only(digits) {
        return Err(CounterCertError::FloatRefused {
            invariant: "public-boundary-refuses-non-integer-text",
            measured_len: text.len(),
        });
    }
    let magnitude = accumulate_digits(digits)?;
    magnitude.checked_mul(sign).ok_or(CounterCertError::Overflow {
        invariant: "parsed-signed-integer-fits-i64",
        measured: magnitude,
    })
}

pub fn checked_claim_sum(parts: &[i64]) -> Result<i64, CounterCertError> {
    let mut total = 0i64;
    for (index, part) in parts.iter().enumerate() {
        let measured = match i64::try_from(index) {
            Ok(value) => value,
            Err(_) => i64::MAX,
        };
        total = total.checked_add(*part).ok_or(CounterCertError::Overflow {
            invariant: "claim-sum-stays-in-i64",
            measured,
        })?;
    }
    Ok(total)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn show_cert(err: CounterCertError) -> String {
        format!("{err:?}")
    }

    fn show_report(err: CounterReportError) -> String {
        format!("{err:?}")
    }

    fn show_boundary(err: CounterBoundary) -> String {
        format!("{err:?}")
    }

    #[test]
    fn unit_depth_certificate_doubles() -> Result<(), String> {
        let width = depth_certificate(2).map_err(show_cert)?;
        if width != 4 {
            return Err(format!("width {width}"));
        }
        Ok(())
    }

    #[test]
    fn unit_clip_stays_inside_remaining() -> Result<(), String> {
        let report = CounterReport::try_from_clip(3, 1).map_err(show_report)?;
        if report.remaining() != 3 {
            return Err(format!("remaining {}", report.remaining()));
        }
        if report.clipped() != 1 {
            return Err(format!("clipped {}", report.clipped()));
        }
        Ok(())
    }

    fn advanced_report() -> Result<CounterReport, String> {
        let start = CounterReport::from_count(3, 0);
        start.advance(CounterEvent::Increment).map_err(show_boundary)
    }

    fn removal_of(stepped: CounterReport) -> Result<Option<usize>, String> {
        let other = CounterReport::try_from_clip(stepped.remaining(), 0).map_err(show_report)?;
        let removal = stepped.separating_removals(other).map_err(show_report)?;
        if stepped.clipped() != 1 {
            return Err(format!("clipped {}", stepped.clipped()));
        }
        Ok(removal)
    }

    #[test]
    fn integration_advance_then_separating_removal() -> Result<(), String> {
        let stepped = advanced_report()?;
        let removal = removal_of(stepped)?;
        if removal != Some(1) {
            return Err(format!("removal {removal:?}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_observe_word_clips_to_remaining() -> Result<(), String> {
        let start = CounterReport::from_count(3, 0);
        let word = [CounterEvent::Increment, CounterEvent::Increment];
        let end = start.observe(&word).map_err(show_boundary)?;
        if end.remaining() != 1 {
            return Err(format!("remaining {}", end.remaining()));
        }
        if end.clipped() != 1 {
            return Err(format!("clipped {}", end.clipped()));
        }
        Ok(())
    }

    #[test]
    fn negative_empty_carrier() -> Result<(), String> {
        let err = depth_certificate(0).map_err(show_cert);
        match err {
            Err(text) => {
                if !text.contains("bounded-counter-carrier-nonempty") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("empty carrier accepted".into()),
        }
    }

    #[test]
    fn negative_float_boundary() -> Result<(), String> {
        let err = parse_exact_i64("1.5").map_err(show_cert);
        match err {
            Err(text) => {
                if !text.contains("binary64") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("float accepted".into()),
        }
    }

    #[test]
    fn negative_claim_disagreement() -> Result<(), String> {
        let err = require_agreement(1, 2).map_err(show_cert);
        match err {
            Err(text) => {
                if !text.contains("bounded-counter-width-doubles") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("disagreement accepted".into()),
        }
    }

    #[test]
    fn negative_overflow_sum() -> Result<(), String> {
        let err = checked_claim_sum(&[i64::MAX, 1]).map_err(show_cert);
        match err {
            Err(text) => {
                if !text.contains("claim-sum-stays-in-i64") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("overflow accepted".into()),
        }
    }

    #[test]
    fn negative_clip_exceeds_depth() -> Result<(), String> {
        let err = CounterReport::try_from_clip(1, 2).map_err(show_report);
        match err {
            Err(text) => {
                if !text.contains("bounded-counter-clip-within-remaining") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("oversize clip accepted".into()),
        }
    }

    #[test]
    fn negative_different_depths() -> Result<(), String> {
        let left = CounterReport::try_from_clip(2, 1).map_err(show_report)?;
        let right = CounterReport::try_from_clip(1, 1).map_err(show_report)?;
        let err = left.separating_removals(right).map_err(show_report);
        match err {
            Err(text) => {
                if !text.contains("bounded-counter-separating-depths-equal") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("unequal depths accepted".into()),
        }
    }

    #[test]
    fn negative_guard_refusal() -> Result<(), String> {
        let start = CounterReport::from_count(2, 0);
        let err = start.advance(CounterEvent::Decrement).map_err(show_boundary);
        match err {
            Err(text) => {
                if !text.contains("bounded-counter-decrement-guard") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("empty decrement accepted".into()),
        }
    }

    #[test]
    fn negative_context_exhausted() -> Result<(), String> {
        let start = CounterReport::from_count(0, 0);
        let err = start.advance(CounterEvent::Increment).map_err(show_boundary);
        match err {
            Err(text) => {
                if !text.contains("bounded-counter-remaining-before-advance") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("exhausted advance accepted".into()),
        }
    }
}
