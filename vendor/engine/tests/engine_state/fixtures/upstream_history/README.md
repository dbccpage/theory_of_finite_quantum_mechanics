# Historical source custody

AuthorityEffect: None.

These content-addressed files preserve only the AnomalonPy inputs needed by
the imported `engine_state` replay tests. They are not an active paper catalog,
current CODA execution receipts, or proof of a published claim.

`custody.json` binds every input to its source repository, full commit, original
case-sensitive path, Git blob object ID, exact raw SHA-256 and byte count.
Identical existing files are reused. The reader checks the raw bytes before
applying the explicitly recorded materialization. GTOC1 originally hashed three
Windows checkout files: the pinned LF blobs are converted to CRLF in memory,
then checked against the original historical receipt hashes. No other bytes
are transformed. The `.gitattributes` rules protect archived raw bytes.

The 22 paper/ledger coordinates in the central agreement contract have no
retrieved source at the inspected AnomalonPy revision. This census uses the
`02_core_evidence/published_series_coordinates.contract.yaml` definition that
Cargo compiles, rather than an older contract copy.
They remain `OPEN_UNAVAILABLE_SOURCE`. Unit tests require that exact unresolved
census and retain the strict matrix, source-hash and authority validators.
Synthetic observation flags do not discharge source replay or publication.
