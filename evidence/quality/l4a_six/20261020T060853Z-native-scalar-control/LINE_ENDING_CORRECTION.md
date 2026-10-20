AuthorityEffect: None.

The original runner read exact item text but Windows translated LF to CRLF when writing its executable harness. The source and harness hashes remain accurate, and the overflow observation remains valid, but the old description of physical byte-for-byte item copying was too strong. A later corrected native-scalar-control receipt reads and writes bytes explicitly. This note preserves the original evidence without rewriting its runner, logs or receipt.
