# PROD-KERNEL-NEXT-1

Goal id: PROD-KERNEL-NEXT-1

Selected scope for PROD-KERNEL-NEXT-1 is recorded in this note.

## Selected scope

Adapter mapping `witnessed_difference.receipts.Receipt` and `witnessed_difference.outcomes.Refused` onto the kernel contracts `ReceiptRecord` and `TypedRefusal` (`omega_engine_applications/wdp_products/kernel/adapter.py`), implementing the `ReceiptIssuer` protocol (`issue` and `verify`) over `make_receipt` and `verify_receipt` with exact parity tests (`omega_engine_applications/tests/test_kernel_adapter.py`).

## Hypotheses

H1. A reference WDP receipt (`witnessed_difference.receipts.Receipt`) carries six content fields (`subject`, `input_digest`, `output_digest`, `claim_ids`, `implementation_version`, `receipt_digest`) plus the fixed `authority_effect = AuthorityEffect.NONE`.

H2. `make_receipt` normalizes `claim_ids` to a nonempty, sorted, duplicate-free tuple of nonempty strings (`tuple(sorted(set(claim_ids)))`) before computing `receipt_digest = content_hash(body)`.

H3. `Refused(code, detail)` carries a lowercase snake_case `RefusalCode` and a nonempty detail string with `authority_effect = AuthorityEffect.NONE`, which maps onto `TypedRefusal(code=code.value, reason=detail, authority_effect="None")`.

## Derivation

1. **Receipt mapping (`to_receipt_record` and `from_receipt_record`)**:
   For any `Receipt` emitted by `make_receipt(subject, inputs, output, claim_ids, implementation_version=v)`:
   - `input_digest = content_hash(inputs)` and `output_digest = content_hash(output)` are 64-character lowercase hexadecimal SHA-256 digests.
   - `claim_ids = tuple(sorted(set(claim_ids)))` is strictly sorted and duplicate-free, satisfying the `ReceiptRecord` validator.
   - `to_receipt_record` maps all six fields plus `authority_effect="None"` into the frozen Pydantic `ReceiptRecord`, and `from_receipt_record` reconstructs the identical `Receipt` dataclass (`from_receipt_record(to_receipt_record(r)) == r`).

2. **Refusal mapping (`to_typed_refusal`)**:
   For any `Refused(code, detail)` returned by `make_receipt` or `verify_receipt`:
   - `to_typed_refusal` maps `code.value` to `TypedRefusal.code` and `detail` to `TypedRefusal.reason` with `authority_effect="None"`.

3. **Parity of `WdpReceiptIssuer.issue` and `WdpReceiptIssuer.verify`**:
   - On valid canonicalizable inputs and nonempty `claim_ids`, `WdpReceiptIssuer.issue` returns `to_receipt_record(make_receipt(...).value)`.
   - On empty `subject`, empty `claim_ids`, or non-canonicalizable inputs/outputs, `WdpReceiptIssuer.issue` returns `TypedRefusal(code="invalid_input", ...)`.
   - On `WdpReceiptIssuer.verify(record, inputs, output)`, unmodified artifacts return `True`; tampered `ReceiptRecord` fields return `TypedRefusal(code="receipt_mismatch", ...)`; modified `inputs` or `output` return `TypedRefusal(code="digest_mismatch", ...)`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not treat a content-bound receipt as a proof of semantic truth of the gated claim (`WDP-CH00-N03`, `WDP-CH15-N01`).
- It does not absorb the routing layer (`WDP-CH04-O01`) into the monograph.
