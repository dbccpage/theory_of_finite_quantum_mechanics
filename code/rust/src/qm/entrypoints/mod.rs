//! Entrypoint suites and verification routines.

pub mod consolidate;
pub mod embeddings;
pub mod replay_receipts;
pub mod replay_review;
pub mod review_estate;
pub mod score_block;
pub mod verify_exec;

/// Walk the declared entrypoints. Each one must return `Ok` from its own check,
/// and the name list must be a set whose index mass is `n(n+1)/2`.
pub fn entrypoints_hold() -> Result<(), String> {
    const NAMES: &[&str] = &[
        "consolidate",
        "embeddings",
        "replay_receipts",
        "replay_review",
        "review_estate",
        "score_block",
        "verify_exec",
    ];
    let mut mass = 0u64;
    for (index, name) in NAMES.iter().enumerate() {
        if name.is_empty() || NAMES[..index].contains(name) {
            return Err("entrypoint name list is not a set".into());
        }
        mass += (index as u64) + 1;
    }
    let n = NAMES.len() as u64;
    if mass != n * (n + 1) / 2 {
        return Err("entrypoint index mass".into());
    }
    consolidate::run_consolidate()?;
    embeddings::run_embeddings()?;
    replay_receipts::run_replay_receipts()?;
    replay_review::run_replay_review()?;
    review_estate::run_review_estate()?;
    score_block::run_score_block()?;
    verify_exec::run_verify_exec()?;
    Ok(())
}
