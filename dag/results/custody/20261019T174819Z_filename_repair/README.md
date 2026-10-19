# PFP custody and protocol repair

The current 177-prompt validator now has zero errors, and all 12 staged-protocol tests pass. The actual starting 398 errors were 177 stale prompt hashes, 220 stale paper bindings (144 distinct papers), and one stale file-only Majorana source pin. Both previous protocol issues are repaired: corpus custody is checked through exact predecessor/successor records, and the Bell target test resolves the semantic node ID through the index instead of relying on uppercase filenames.

The original prompt audit, all current prompt text and paper text, and every existing staged/review artifact remain byte-identical. All 177 canonical operad presentations, targets and stage histories are preserved. The only canonical operad edit advances one file-only source-lead hash and appends explicit predecessor/current provenance for an upstream additive public-re-export change. Its scope remains source_lead_only/file_only_no_symbol; this is not a Rust implementation or theorem validation.

The new custody ledger binds 177 prompts and 144 papers to exact historical and current snapshots. All 654 whole-filename-token replacements and 144 explicit CRLF-to-LF conversions reproduce the current bytes exactly; other content or numerical changes are rejected. Both versions are checked against their declared Git commits. Historical pins and the historical audit are retained, not silently rewritten or waived.

Adversarial tests reject changed values even with forged current hashes, forged predecessors that do not match the original pin, rollbacks, missing snapshots/entries, wrong tasks, incomplete use coverage, duplicate keys, floats, Boolean digests, arbitrary substitutions and path escapes. The re-export review separately rejects removed/redirected exports and changed source bodies. Earlier failed validator/protocol receipts and the two rejected constructor source versions remain retained; their diagnostics are not presented as passing checks.

Measured verification: {"after_custody_errors": 0, "authority_effect": "None", "before_custody_errors": 398, "custody_tests_per_mode": 18, "modes": ["normal", "Python -O"], "protocol_tests_per_mode": 12, "review": {"added_Majorana_public_exports": 22, "authority_effect": "None", "canonical_operad_presentations_preserved": 177, "historical_and_current_git_blob_bindings_checked": 642, "preserved_existing_file_count": 12375, "scope": "Literal byte/provenance and limited public-re-export checks. No numerical, mathematical, implementation or authority claim is promoted.", "source_review_negative_controls_rejected": 3, "source_review_positive_control": "accepted"}, "scope": "Current corpus custody and protocol repair. Earlier failure receipts remain historical. Read-only replay checks retained exact certificates; no Rust/Lean compiler or mathematical campaign completion is claimed.", "sealed_twenty_run_replay": {"exact_records": 62, "rejected_P4_mutations": 1524, "retained_failed_checkpoints": 1, "runs": 20, "scope": "Read-only replay; saved native/kernel receipts checked, compilers not rerun.", "unique_named_prompt_anchors": 31}, "validated_prompts": 177}.

Normal and optimized Python each run the full validator, 12 protocol tests, 18 custody tests and the sealed twenty-run replay. The replay checks exact saved certificates and compiler receipts; it does not recompile Rust or Lean. This repair changes no Rust/Lean implementation, numerical certificate, quantum theorem claim or full-operad coherence obligation. These historical limitations remain open.

Live checks from repository root:

    py -3.9 -X utf8 dag/pfp/validate_prompts.py
    py -3.9 -X utf8 dag/pfp/test_staged_prompts.py -v
    py -3.9 -X utf8 dag/pfp/test_custody.py -v
    py -3.9 -X utf8 -O dag/pfp/test_custody.py -v

The source/snapshot custody checker is portable and needs no live Git history. The retained construction/review tools additionally inspect historical Git objects and refuse to overwrite their receipts. AuthorityEffect: None.
