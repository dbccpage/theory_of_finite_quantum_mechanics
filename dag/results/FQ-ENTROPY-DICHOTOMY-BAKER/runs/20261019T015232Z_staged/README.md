# Algebraic entropy and exact series stage

The source theorem proves entropy zero iff pure and strict positivity for mixed finite algebraic spectra. Transcendence is conditional on the explicit BakerCitedInput argument; no native flag discharges it. Natural logarithms are used. Five exact rational spectra retain common-denominator integer weights, integer Renyi power sums of orders2,3,4 and all rational series terms/endpoints/widths. Zero-weight terms contribute zero without evaluating log0. The small-eigenvalue case retains its actual wider interval.

For 0<p<=1 set t=(p-1)/(p+1), so -1<t<=0. The compiled Mathlib log series gives log(p)=2 sum_{k>=0} t^(2k+1)/(2k+1), using log((1+t)/(1-t))=log(p). Every omitted term is nonpositive. Its absolute tail is at most 2 |t|^(2N+1)/((2N+1)(1-t^2)), since 1/(2k+1)<=1/(2N+1) for k>=N and the remaining absolute powers form a geometric series. Thus S_N-R_N<=log(p)<=S_N and -p*S_N<=-p*log(p)<=-p*S_N+p*R_N. The exact native endpoints implement this argument. The finite-tail/rational-array transport is not yet formalized in Lean; the infinite-series identity is a separately named compiled anchor.

The compiled cancellation log4-2log2=0 blocks replacing the nonzero-linear-form hypothesis by nonzero coefficients.

Every executed checkpoint retains an operad delta, source/candidate bindings and actual host results. This is local file-based PFP execution, not an external-provider transcript. No whole-repository or hosted-CI success is claimed. Awaiting the requested batch review. AuthorityEffect: None.
