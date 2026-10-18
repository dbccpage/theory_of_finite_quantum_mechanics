use serde::{Deserialize, Serialize};
use std::fmt;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/types.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: sha256 and blake3 packet identities are 32-byte lowercase hex strings and AuthorityEffect admits only None";
pub const AUTHORITY_EFFECT_TEXT: &str = "AuthorityEffect: None";
pub const DIGEST_HEX_WIDTH: usize = 64;
pub const MUTATION_KILLS: u32 = 0;

const EMPTY_SHA256: &str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
const EMPTY_BLAKE3: &str = "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262";

#[derive(
    Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize, Default,
)]
pub enum AuthorityEffect {
    #[default]
    None,
}

impl fmt::Display for AuthorityEffect {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::None => write!(f, "None"),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum IdentityError {
    Width { hex_len: usize, expected: usize },
    NonHex { index: usize },
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, IdentityError> {
    if token == "true" || token == "false" {
        return Err(IdentityError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(IdentityError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, IdentityError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(IdentityError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(IdentityError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(IdentityError::Overflow)?;
    }
    Ok(value)
}

pub fn sha256_digest(bytes: &[u8]) -> String {
    use sha2::{Digest, Sha256};
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    hex::encode(hasher.finalize())
}

pub fn blake3_digest(bytes: &[u8]) -> String {
    let hash = blake3::hash(bytes);
    hash.to_hex().to_string()
}

fn is_lower_hex(byte: u8) -> bool {
    byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte)
}

pub fn certify_lower_hex(hex_text: &str) -> Result<(), IdentityError> {
    if hex_text.len() != DIGEST_HEX_WIDTH {
        return Err(IdentityError::Width {
            hex_len: hex_text.len(),
            expected: DIGEST_HEX_WIDTH,
        });
    }
    for (index, byte) in hex_text.bytes().enumerate() {
        if !is_lower_hex(byte) {
            return Err(IdentityError::NonHex { index });
        }
    }
    Ok(())
}

pub fn certify_sha256(bytes: &[u8]) -> Result<String, IdentityError> {
    let hex_text = sha256_digest(bytes);
    certify_lower_hex(&hex_text)?;
    Ok(hex_text)
}

pub fn certify_blake3(bytes: &[u8]) -> Result<String, IdentityError> {
    let hex_text = blake3_digest(bytes);
    certify_lower_hex(&hex_text)?;
    Ok(hex_text)
}

pub fn certify_authority(effect: AuthorityEffect) -> Result<&'static str, IdentityError> {
    match effect {
        AuthorityEffect::None => Ok(AUTHORITY_EFFECT_TEXT),
    }
}

pub fn empty_sha256_vector() -> &'static str {
    EMPTY_SHA256
}

pub fn empty_blake3_vector() -> &'static str {
    EMPTY_BLAKE3
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn show(error: impl std::fmt::Debug) -> String {
        format!("{error:?}")
    }

    #[test]
    fn unit_empty_digests_match_known_vectors() -> Result<(), String> {
        empty_digests().and_then(|(sha, blake)| unit_vectors(sha, blake))
    }

    fn empty_digests() -> Result<(String, String), String> {
        let sha = certify_sha256(b"").map_err(show)?;
        let blake = certify_blake3(b"").map_err(show)?;
        Ok((sha, blake))
    }

    fn unit_vectors(sha: String, blake: String) -> Result<(), String> {
        need(sha == EMPTY_SHA256, "sha256 empty")?;
        need(blake == EMPTY_BLAKE3, "blake3 empty")?;
        need(sha.len() == DIGEST_HEX_WIDTH, "width")
    }

    #[test]
    fn integration_distinct_algorithms_separate_abc() -> Result<(), String> {
        abc_digests().and_then(|(sha, blake)| integration_abc(sha, blake))
    }

    fn abc_digests() -> Result<(String, String), String> {
        let sha = certify_sha256(b"abc").map_err(show)?;
        let blake = certify_blake3(b"abc").map_err(show)?;
        Ok((sha, blake))
    }

    fn integration_abc(sha: String, blake: String) -> Result<(), String> {
        need(sha != blake, "separation")?;
        need(
            sha == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            "sha abc",
        )?;
        integration_hex(&sha, &blake)
    }

    fn integration_hex(sha: &str, blake: &str) -> Result<(), String> {
        certify_lower_hex(sha).map_err(show)?;
        certify_lower_hex(blake).map_err(show)?;
        Ok(())
    }

    #[test]
    fn e2e_authority_and_packet_identity_are_sealed() -> Result<(), String> {
        e2e_values().and_then(|(effect, packet)| e2e_seal(effect, packet))
    }

    fn e2e_values() -> Result<(&'static str, String), String> {
        let effect = certify_authority(AuthorityEffect::None).map_err(show)?;
        let packet = certify_sha256(b"wdp-packet").map_err(show)?;
        Ok((effect, packet))
    }

    fn e2e_seal(effect: &str, packet: String) -> Result<(), String> {
        need(effect == AUTHORITY_EFFECT_TEXT, "authority")?;
        need(AuthorityEffect::None.to_string() == "None", "display")?;
        e2e_text(packet.len())
    }

    fn e2e_text(packet_len: usize) -> Result<(), String> {
        need(packet_len == 64, "packet")?;
        need(ORIGIN.contains("code/rust/src/wdp/types.rs"), "origin")?;
        need(CLAIM.contains("AuthorityEffect"), "claim")
    }

    #[test]
    fn negative_refuses_width_uppercase_float_and_boolean() -> Result<(), String> {
        need(
            matches!(
                certify_lower_hex("abcd"),
                Err(IdentityError::Width { hex_len: 4, expected: 64 })
            ),
            "width",
        )?;
        let mut upper = EMPTY_SHA256.to_string();
        upper.replace_range(0..1, "E");
        need(
            matches!(certify_lower_hex(&upper), Err(IdentityError::NonHex { index: 0 })),
            "upper",
        )?;
        need(
            admit_exact_integer("1.5") == Err(IdentityError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("false") == Err(IdentityError::BooleanAsNumber),
            "bool",
        )?;
        need(admit_exact_integer("64") == Ok(64), "integer")?;
        Ok(())
    }
}
