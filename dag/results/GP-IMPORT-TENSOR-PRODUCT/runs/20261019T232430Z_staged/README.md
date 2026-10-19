# GP-IMPORT-TENSOR-PRODUCT

Tensor and dumpRight are actual bilinear maps from the source. DumpRight uses tag(i,j)=(i,false), which is not injective and collapses right labels. Compute both maps and full difference, preserving the strong Kronecker convention needed for uniqueness. Output layout: tensor4;dump4;difference4;norm_product;tensor_norm

Supported: Exact tensor/dumpRight and norm-multiplicativity arrays, with generic bilinearity and a basis-collision control in Lean.

Remaining: Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product.

Every executed checkpoint retains an operad delta, source/candidate bindings and actual host results. This is local file-based PFP execution, not an external-provider transcript. No whole-repository or hosted-CI success is claimed. Awaiting the requested batch review. AuthorityEffect: None.
