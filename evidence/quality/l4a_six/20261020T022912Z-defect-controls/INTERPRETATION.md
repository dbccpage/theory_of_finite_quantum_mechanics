AuthorityEffect: None.

The two newly added boundary/coboundary controls did not reproduce a panic.
Their sealed findings contain the hypothesis that prompted the probe, not an
established failure. Live provider inspection at backend/basic_matrix.rs:657
shows fallible `reserve(self.rows)?` before enumeration. Both controls report
NO_PANIC_OBSERVED; this is finite evidence, not universal crash-freedom.

The Gaussian, sparse-capacity and undefined-float controls likewise did not
reproduce their earlier failure classes. The external provider's i64 exact-ring
overflow control did reproduce a panic. The sealed records and logs are kept
unchanged; scoring consumes the explicit reproduced booleans.
