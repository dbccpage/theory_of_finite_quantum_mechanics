
pub mod consolidate;
pub mod embeddings;
pub mod replay_receipts;
pub mod replay_review;
pub mod review_estate;
pub mod score_block;
pub mod verify_exec;

fn verify_entrypoint_names(names: &[&str]) -> Result<(), String> {
    let mut mass = 0u64;
    for (index, name) in names.iter().enumerate() {
        if name.is_empty() || names[..index].contains(name) {
            return Err("entrypoint name list is not a set".into());
        }
        mass += (index as u64) + 1;
    }
    let n = names.len() as u64;
    if mass != n * (n + 1) / 2 {
        return Err("entrypoint index mass".into());
    }
    Ok(())
}

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
    verify_entrypoint_names(NAMES)?;
    consolidate::run_consolidate()?;
    embeddings::run_embeddings()?;
    replay_receipts::run_replay_receipts()?;
    replay_review::run_replay_review()?;
    review_estate::run_review_estate()?;
    score_block::run_score_block()?;
    verify_exec::run_verify_exec()?;
    Ok(())
}
