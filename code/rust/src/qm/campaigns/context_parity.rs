//! Campaign module context_parity.
//!
//! Two commuting contexts on three bits, with parity-check rows
//! `(1,1,0)` and `(0,1,1)`. The syndrome is the matrix product and the
//! pairwise sums. A word is a codeword exactly when both readings vanish.

pub fn verify() -> Result<u8, &'static str> {
    let checks = [[1u8, 1, 0], [0, 1, 1]];
    let word = [1u8, 1, 0];
    let by_rows = syndrome(&checks, &word)?;
    let by_pairs = [word[0] ^ word[1], word[1] ^ word[2]];
    if by_rows != by_pairs {
        return Err("context parities disagree");
    }
    let codeword = [1u8, 1, 1];
    let clear = syndrome(&checks, &codeword)?;
    if clear != [0, 0] || by_rows == [0, 0] {
        return Err("parity did not separate the word from the code");
    }
    Ok(by_rows[0] ^ by_rows[1])
}

fn syndrome(checks: &[[u8; 3]; 2], word: &[u8; 3]) -> Result<[u8; 2], &'static str> {
    let mut out = [0u8; 2];
    for row in 0..2 {
        for col in 0..3 {
            if checks[row][col] > 1 || word[col] > 1 {
                return Err("bit was not in F2");
            }
            out[row] ^= checks[row][col] & word[col];
        }
    }
    Ok(out)
}
