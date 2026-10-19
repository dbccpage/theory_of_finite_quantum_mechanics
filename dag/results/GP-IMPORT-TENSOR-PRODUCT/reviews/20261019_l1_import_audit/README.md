# GP-IMPORT-TENSOR-PRODUCT review

Tensor and dumpRight are actual bilinear maps from the source. DumpRight uses tag(i,j)=(i,false), which is not injective and collapses right labels. Compute both maps and full difference, preserving the strong Kronecker convention needed for uniqueness. Output layout: tensor4;dump4;difference4;norm_product;tensor_norm

Supported: Exact tensor/dumpRight and norm-multiplicativity arrays, with generic bilinearity and a basis-collision control in Lean.

Remaining: Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product.

Historical source annotations and all stage bytes are preserved. No external provider dispatched. AuthorityEffect: None.
