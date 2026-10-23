# PLAN-WDP-RELEASE-CHECKS

Goal id: PLAN-WDP-RELEASE-CHECKS

AuthorityEffect: None.

## Selected scope

Revalidation control for `000_witnessed_difference_programme` release artifacts, statement snapshots, and CI/policy dispositions after the R1–R4 and E1–E12 corrections:

1. **Manuscript-to-TeX/PDF binding:** `witnessed_difference_programme.tex` begins with `% manuscript-sha256: <sha256>` matching the live `witnessed_difference_programme.md` bytes, and `witnessed_difference_programme.pdf` is present and non-empty.
2. **Rendered link hygiene:** Zero relative `\href{...}` targets in `witnessed_difference_programme.tex` end with `/`, preventing `hyperref` from appending `.pdf` to directory paths.
3. **Manifest & statement-snapshot custody:** `manifests/current_claim_evidence.json`, `manifests/release_manifest.json`, and `manifests/release_verification.json` carry `authority_effect == "None"` and `status == "PASS"`, while `DEC-WDP-REPIN` remains an explicit separate owner decision rather than a silent baseline overwrite.
4. **CI/policy disposition discipline:** Any check with `silent_baseline_refresh=True` or unrecorded policy failure is refused.

## Claims this note does not make

- It does not perform a silent trusted-baseline refresh (`DEC-WDP-REPIN`), claim blanket green hosted CI, grant publication clearance, or assign a DOI.
