# DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL review

Four actual one-entry rational Kraus matrices are built from two Cayley unit vectors. Native sums recompute ΣKᵀK=I, ΣKρKᵀ and its population kernel, plus post-composition by bit flip. Identity and normalized dephasing have the same population shadow yet differ at coherent inputs. The source H018 mixMat is unnormalized, so it is not silently declared CPTP.

Supported: Exact Kraus completeness, channel outputs, stochastic kernel and same-diagonal distinct-output controls are retained; scalar Cayley and population conservation are kernel checked.

Remaining: Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel.

Historical source annotations and all stage bytes are preserved. No external provider dispatched. AuthorityEffect: None.
