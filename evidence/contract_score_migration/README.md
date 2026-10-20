# Contract and scoring-history migration evidence

9,874 tracked legacy companions were consolidated into 7,142 combined YAML files, including registry contracts and historical evidence. The index preserves every original name, SHA-256 and byte length. `verification.json` confirms exact original bytes and consistent readable/history views. No Rust or Lean source changes are present in the diff.

The final checks passed: 15 migration/atlas tests, 4 QM policy tests, 15 foundation policy tests, 9 negative schema controls, atlas synchronization and 177 prompt collections. Earlier failed test runs are retained separately. Historical continuation controls initially stopped at the changed helper (and then changed dependencies); individual guard predicates are now tested directly, while the complete production guard still rejects the old helper epoch. These are policy-unit tests, not new executions or acceptance of historical mutation campaigns.

`receipt.json` binds the logs and tool. Mathematical claims and imported scoring grades were not independently revalidated or promoted by this storage migration. See `docs/CONTRACT_SCORING_HISTORY.md` for the schema and historical record reader.
