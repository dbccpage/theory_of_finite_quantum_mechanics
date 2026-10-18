
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use super::colour::OperadColour;

pub const ADMITTED_FINITE_COLOURS: &[&str] = &[
    "State", "Proof", "Receipt", "Audit", "Contract", "Ledger", "Code", "Paper", "Diagram", "Post",
];

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct SpanOperand {
    pub file_path: String,
    pub start_line: usize,
    pub end_line: usize,
    pub byte_offset: usize,
    pub byte_length: usize,
    pub colour: OperadColour,
    pub content_sha256: String,
    pub raw_text: String,
    pub role: String,
}

impl SpanOperand {
    pub fn new(
        file_path: impl Into<String>,
        start_line: usize,
        end_line: usize,
        byte_offset: usize,
        byte_length: usize,
        colour: OperadColour,
        content_sha256: impl Into<String>,
        raw_text: impl Into<String>,
        role: Option<String>,
    ) -> Result<Self, String> {
        let f_path = file_path.into();
        let text = raw_text.into();
        let sha = content_sha256.into();

        if start_line < 1 {
            return Err(format!("start_line must be >= 1, got {start_line}"));
        }
        if end_line < start_line {
            return Err(format!(
                "end_line ({end_line}) cannot precede start_line ({start_line})"
            ));
        }
        if text.as_bytes().starts_with(&[0xef, 0xbb, 0xbf]) {
            return Err("Span text contains forbidden UTF-8 BOM bytes".to_string());
        }

        Ok(Self {
            file_path: f_path,
            start_line,
            end_line,
            byte_offset,
            byte_length,
            colour,
            content_sha256: sha,
            raw_text: text,
            role: role.unwrap_or_else(|| "general".to_string()),
        })
    }

    pub fn from_raw_text(
        file_path: impl Into<String>,
        raw_text: impl Into<String>,
        colour: OperadColour,
        start_line: usize,
        end_line: usize,
        byte_offset: usize,
        role: Option<String>,
    ) -> Result<Self, String> {
        let text = raw_text.into();
        if text.as_bytes().starts_with(&[0xef, 0xbb, 0xbf]) {
            return Err("Span text contains forbidden UTF-8 BOM bytes".to_string());
        }

        let mut hasher = Sha256::new();
        hasher.update(text.as_bytes());
        let digest_hex = hex::encode(hasher.finalize());
        let byte_len = text.as_bytes().len();

        Self::new(
            file_path,
            start_line,
            end_line,
            byte_offset,
            byte_len,
            colour,
            digest_hex,
            text,
            role,
        )
    }

    pub fn verify_integrity(&self) -> bool {
        let mut hasher = Sha256::new();
        hasher.update(self.raw_text.as_bytes());
        let computed = hex::encode(hasher.finalize());
        computed == self.content_sha256 && self.byte_length == self.raw_text.as_bytes().len()
    }
}
