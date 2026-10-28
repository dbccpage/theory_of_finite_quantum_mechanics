# Vendored engine crates

**AuthorityEffect:** None. This folder is a third-party dependency of `code/rust`. It adds no result.

`code/rust` depends on these 33 Rust crates through plain path dependencies, so the workspace builds from a clean checkout without private sources. They are vendored here the way a crates.io dependency would be: outside the governed populations (`code/**`, `lean4/**`), so the contract-score floor in [`governance/`](../../governance/README.md) does not apply to them and they carry no companions or baseline entries.

## Provenance

The crates are copies of an upstream engine workspace at commit `4c8143035817782907c1023b6ff95949843abcb2`. Each directory below names its upstream crate directory by the first 12 hex digits of the SHA-256 of its upstream path.

| Crate directory | Upstream crate |
| --- | --- |
| `constants` | `upstream:sha256:f289cda5fc5e` |
| `engine_category_theory` | `upstream:sha256:1246209de165` |
| `engine_certifiers` | `upstream:sha256:8de04daf813f` |
| `engine_combinatorics` | `upstream:sha256:2784b7434a4d` |
| `engine_contracts` | `upstream:sha256:d73c387ac13a` |
| `engine_finite_probability` | `upstream:sha256:b66ac5e4336d` |
| `engine_functional` | `upstream:sha256:ea33f5dc3230` |
| `engine_fusion_categories` | `upstream:sha256:fd211d10b5b2` |
| `engine_general_relativity` | `upstream:sha256:47a873b6e952` |
| `engine_holonomy` | `upstream:sha256:c2e1e74c132f` |
| `engine_homology` | `upstream:sha256:1fca423dacdb` |
| `engine_homotopy_type_theory` | `upstream:sha256:f4a594dc9ded` |
| `engine_kernel` | `upstream:sha256:7db13328d5ba` |
| `engine_lie_theory` | `upstream:sha256:d63ba5b81a64` |
| `engine_lifts` | `upstream:sha256:c41c460d9d60` |
| `engine_local_green_global_red_lggr` | `upstream:sha256:41ff14e6ea4f` |
| `engine_majorana` | `upstream:sha256:ec61e75305f3` |
| `engine_measurement` | `upstream:sha256:2c8c946a95f2` |
| `engine_number_theory` | `upstream:sha256:07fbae171e50` |
| `engine_operad_theory` | `upstream:sha256:b6f3d836aa6d` |
| `engine_pipelines` | `upstream:sha256:21bf937cc80b` |
| `engine_policy` | `upstream:sha256:4d349d31dc6a` |
| `engine_prompt_evolution` | `upstream:sha256:5a146f093cfb` |
| `engine_quantum_physics` | `upstream:sha256:0f215ffd5d44` |
| `engine_replay` | `upstream:sha256:1506e46e658c` |
| `engine_runtime` | `upstream:sha256:50f19d545841` |
| `engine_solvers` | `upstream:sha256:f32ef28a74bc` |
| `engine_state` | `upstream:sha256:5fb98272739b` |
| `engine_symbol_host_runtime` | `upstream:sha256:109aa0e4899c` |
| `engine_types` | `upstream:sha256:cb668ba60424` |
| `engine_wdp` | `upstream:sha256:3b389bc5656d` |
| `engine_wire_primitives` | `upstream:sha256:28c2492731fd` |
| `linear_algebra` | `upstream:sha256:60d055f3b030` |
The package in `engine_local_green_global_red_lggr` is named `engine_epk`.

## License

These crates keep their upstream license, the PolyForm Noncommercial License 1.0.0 ([`LICENSE`](LICENSE), SPDX `PolyForm-Noncommercial-1.0.0`). They are **not** covered by the repository's Apache-2.0 license. Noncommercial use is free; commercial use needs a separate licence from the copyright holder named in `LICENSE`.

## Local changes

The copies differ from upstream only as follows.

1. **Names.** Crate names lost the upstream prefix and now start with `engine_` (`constants` and `linear_algebra` keep their names); four crates got descriptive names (`engine_runtime`, `engine_symbol_host_runtime`, `engine_wire_primitives`, `engine_prompt_evolution`). Directory names equal crate names.
2. **Paths.** Paths that pointed into the upstream repository now point into this tree: the contract corpus read by the `engine_contracts` build script (`engine_contracts/corpus`), its test fixtures (`engine_contracts/fixtures`) and the pinned PO-000 receipt (`engine_wire_primitives/receipts`). The `engine_state` custody records keep their upstream storage paths byte-exact; one helper (`storage_location` in `tests/engine_state/support/upstream_history.rs`) maps them to this tree.
3. **Naming clean-up.** Persona and product names in code and comments were replaced by neutral ones (for example coordinator, sealed residual, symbol host, wire, fold engine), and 11 files were renamed to match. Only names declared as types, functions, modules or constants were renamed; serialized enum variants, struct fields and string literals were left unchanged so that wire formats, schema ids and hashed fixtures stay byte-exact. Repository links and absolute paths naming private sources were replaced by hash markers.

## Building and testing

```
cd vendor/engine
cargo build --workspace
cargo test --workspace --no-fail-fast
```

Against the upstream workspace at the same commit (488 test binaries, run one by one):

| | passed | failed |
| --- | --- | --- |
| upstream | 8,626 | 24 |
| vendored here | 8,604 | 46 |

The same eight test targets fail to compile in both (they read upstream files outside the crates or use APIs that have since changed). The 22 extra failures are all repository self-audits that read the upstream repository layout or its contract corpus, which names the upstream crates: `engine_contracts` (`binding_audit`, `certificate_promotion_firewall`, `contract_projections`, `ddc_file_contract_gate`, `functional_boundary`, `governance_validator`, `math_contract_gate`, `rust_file_contract_gate`), `engine_certifiers` (`paper_claim_traceability`, `phi1_conformance`) and `engine_functional` (`dependency_boundary`). One timing test in `engine_solvers` (`bounded_l1_allocation`) failed once under parallel load and passes when rerun. No mathematical test changed outcome.
