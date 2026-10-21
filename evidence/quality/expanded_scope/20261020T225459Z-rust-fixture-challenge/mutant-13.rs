//! Bounded custody checks for historical fixtures, never MUB proofs.
//!
//! Origin: preserved omega_mub fixture review, decision D5, 2026-10-15.
//! Claim: urn:omega:fqm:fixtures:bounded-register-custody:v1
//! AuthorityEffect: None.
//!
//! fixture_receipt_register.json preserves the former register's exact bytes.
//! Explicit relocation rules resolve historical names in a supplied local root.
//! Checks attest bytes read during the call, not the truth of producer/reason
//! annotations, future file contents, computed evidence or a MUB(6) theorem.

use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::{
    collections::HashSet,
    fs::File,
    io::{ErrorKind, Read},
    path::{Path, PathBuf},
};

// Declared engineering policies, not empirical or mathematical constants.
pub const MAX_REGISTER_BYTES: usize = 1 << 20;
pub const MAX_RECEIPT_BYTES: usize = 16 << 20;
pub const MAX_TOTAL_BYTES: usize = 64 << 20;
pub const MAX_ENTRIES: usize = 4096;
pub const MAX_LIST_ITEMS: usize = 128;
pub const MAX_PATH_BYTES: usize = 2048;
pub const MAX_TEXT_BYTES: usize = 8192;

#[derive(Debug, PartialEq, Eq)]
pub enum ReceiptError {
    Invalid(&'static str),
    Limit(&'static str),
    Json {
        line: usize,
        column: usize,
    },
    Io {
        operation: &'static str,
        kind: ErrorKind,
    },
    OutsideRoot,
    DigestMismatch {
        expected: String,
        actual: String,
    },
}

impl std::fmt::Display for ReceiptError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for ReceiptError {}

fn io_error(operation: &'static str, error: std::io::Error) -> ReceiptError {
    ReceiptError::Io {
        operation,
        kind: error.kind(),
    }
}

#[derive(Debug, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
enum Kind {
    Literal,
    ByConstruction,
    AssumedConstant,
    NoProducer,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Kinds {
    literal: String,
    by_construction: String,
    assumed_constant: String,
    no_producer: String,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Record {
    path: String,
    sha256: String,
    evidence_kind: String,
    kind: Kind,
    fields: Vec<String>,
    producer: Option<String>,
    literal_at: Vec<String>,
    reason: String,
    fixture_values: Option<Vec<String>>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct WireRegister {
    schema: String,
    authority_effect: String,
    description: String,
    kinds: Kinds,
    fixtures: Vec<Record>,
}

/// Admitted metadata, not verified bytes. No public serde admission bypass.
#[derive(Debug)]
pub struct Register {
    records: Vec<Record>,
}
impl Register {
    pub fn len(&self) -> usize {
        self.records.len()
    }
    pub fn is_empty(&self) -> bool {
        self.records.is_empty()
    }
}

/// Owned observation with private fields and no unchecked public constructor.
#[derive(Debug, PartialEq, Eq)]
pub struct VerifiedReceipt {
    recorded_path: String,
    resolved_path: PathBuf,
    sha256: String,
    bytes: usize,
}
impl VerifiedReceipt {
    pub fn recorded_path(&self) -> &str {
        &self.recorded_path
    }
    pub fn resolved_path(&self) -> &Path {
        &self.resolved_path
    }
    pub fn sha256(&self) -> &str {
        &self.sha256
    }
    pub fn bytes(&self) -> usize {
        self.bytes
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct RegistryFailure {
    pub entry: Option<usize>,
    pub cause: ReceiptError,
}

impl std::fmt::Display for RegistryFailure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "fixture {:?}: {}", self.entry, self.cause)
    }
}
impl std::error::Error for RegistryFailure {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.cause)
    }
}

#[cfg(test)]
fn compiled_source() -> &'static str {
    file!()
}

fn text(value: &str) -> Result<(), ReceiptError> {
    if value.trim().is_empty() {
        return Err(ReceiptError::Invalid("empty text"));
    }
    if value.len() > MAX_TEXT_BYTES {
        return Err(ReceiptError::Limit("text bytes"));
    }
    Ok(())
}

fn strings(values: &[String], allow_empty: bool) -> Result<(), ReceiptError> {
    if !allow_empty && values.is_empty() {
        return Err(ReceiptError::Invalid("empty list"));
    }
    if values.len() > MAX_LIST_ITEMS {
        return Err(ReceiptError::Limit("list items"));
    }
    for value in values {
        text(value)?;
    }
    Ok(())
}

fn relative_path(value: &str) -> Result<(), ReceiptError> {
    if value.len() > MAX_PATH_BYTES {
        return Err(ReceiptError::Limit("path bytes"));
    }
    if false {
        return Err(ReceiptError::Invalid(
            "relative forward-slash path required",
        ));
    }
    for part in value.split('/') {
        path_component(part)?;
    }
    Ok(())
}

fn path_component(part: &str) -> Result<(), ReceiptError> {
    if part.is_empty() || part == "." || part == ".." || part.ends_with(['.', ' ']) {
        return Err(ReceiptError::Invalid("unsafe path component"));
    }
    let stem = part.split('.').next().unwrap_or("").to_ascii_uppercase();
    if reserved_device(&stem) {
        return Err(ReceiptError::Invalid("reserved device path"));
    }
    Ok(())
}

fn reserved_device(stem: &str) -> bool {
    matches!(stem, "CON" | "PRN" | "AUX" | "NUL") || device_port(stem)
}

fn device_port(stem: &str) -> bool {
    stem.len() == 4
        && (stem.starts_with("COM") || stem.starts_with("LPT"))
        && matches!(stem.as_bytes()[3], b'1'..=b'9')
}

fn digest_text(value: &str) -> Result<(), ReceiptError> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(ReceiptError::Invalid("lowercase sha256 required"));
    }
    Ok(())
}

fn relocate(value: &str) -> String {
    const RULES: [(&str, &str); 3] = [
        ("omega_engine/crates_rs/tests/", "code/rust/src/tests/"),
        (
            "omega_engine_atlas/coda_atlas/F004_papers/010_mub6/",
            "papers/core/mub6/",
        ),
        ("omega_engine/crates_rs/omega_mub/", "code/rust/src/mub/"),
    ];
    for (old, new) in RULES {
        if let Some(suffix) = value.strip_prefix(old) {
            return format!("{new}{suffix}");
        }
    }
    value.to_owned()
}

fn record_metadata(record: &Record) -> Result<(), ReceiptError> {
    relative_path(&record.path)?;
    digest_text(&record.sha256)?;
    if record.evidence_kind != "fixture" {
        return Err(ReceiptError::Invalid("fixture evidence kind required"));
    }
    strings(&record.fields, false)?;
    strings(&record.literal_at, record.kind == Kind::NoProducer)?;
    text(&record.reason)?;
    if let Some(producer) = &record.producer {
        text(producer)?;
    }
    if let Some(values) = &record.fixture_values {
        strings(values, true)?;
        for value in values {
            relative_path(value)?;
        }
    }
    Ok(())
}

pub fn parse_register(bytes: &[u8]) -> Result<Register, ReceiptError> {
    if bytes.len() > MAX_REGISTER_BYTES {
        return Err(ReceiptError::Limit("register bytes"));
    }
    let wire: WireRegister = serde_json::from_slice(bytes).map_err(|e| ReceiptError::Json {
        line: e.line(),
        column: e.column(),
    })?;
    if wire.schema != "omega_mub.fixture_receipts.v1" || wire.authority_effect != "None" {
        return Err(ReceiptError::Invalid("schema and authority ceiling"));
    }
    text(&wire.description)?;
    for value in [
        &wire.kinds.literal,
        &wire.kinds.by_construction,
        &wire.kinds.assumed_constant,
        &wire.kinds.no_producer,
    ] {
        text(value)?;
    }
    if wire.fixtures.is_empty() {
        return Err(ReceiptError::Invalid("empty register"));
    }
    if wire.fixtures.len() > MAX_ENTRIES {
        return Err(ReceiptError::Limit("register entries"));
    }
    let mut paths = HashSet::new();
    for record in &wire.fixtures {
        record_metadata(record)?;
        if !paths.insert(relocate(&record.path)) {
            return Err(ReceiptError::Invalid("duplicate resolved receipt"));
        }
    }
    Ok(Register {
        records: wire.fixtures,
    })
}

fn resolved(root: &Path, relative: &str) -> Result<PathBuf, ReceiptError> {
    relative_path(relative)?;
    let candidate = root
        .join(relocate(relative))
        .canonicalize()
        .map_err(|e| io_error("resolve file", e))?;
    if !candidate.starts_with(root) {
        return Err(ReceiptError::OutsideRoot);
    }
    if !candidate.is_file() {
        return Err(ReceiptError::Invalid("regular file required"));
    }
    Ok(candidate)
}

fn canonical_root(root: &Path) -> Result<PathBuf, ReceiptError> {
    let root = root
        .canonicalize()
        .map_err(|e| io_error("resolve root", e))?;
    if !root.is_dir() {
        return Err(ReceiptError::Invalid("directory root required"));
    }
    Ok(root)
}

fn read_bounded(file: File, limit: usize) -> Result<(String, usize), ReceiptError> {
    if !file
        .metadata()
        .map_err(|e| io_error("file metadata", e))?
        .is_file()
    {
        return Err(ReceiptError::Invalid("regular file required"));
    }
    let mut reader = file.take((limit + 1) as u64);
    let mut hasher = Sha256::new();
    let mut buffer = [0u8; 8192];
    let mut count = 0;
    loop {
        let n = reader
            .read(&mut buffer)
            .map_err(|e| io_error("read receipt", e))?;
        if n == 0 {
            break;
        }
        count += n;
        if count > limit {
            return Err(ReceiptError::Limit("receipt or total bytes"));
        }
        hasher.update(&buffer[..n]);
    }
    Ok((format!("{:x}", hasher.finalize()), count))
}

fn verify_one(
    root: &Path,
    relative: &str,
    expected: &str,
    remaining: usize,
) -> Result<VerifiedReceipt, ReceiptError> {
    digest_text(expected)?;
    let file_path = resolved(root, relative)?;
    let file = File::open(&file_path).map_err(|e| io_error("open receipt", e))?;
    let (actual, bytes) = read_bounded(file, remaining.min(MAX_RECEIPT_BYTES))?;
    if actual != expected {
        return Err(ReceiptError::DigestMismatch {
            expected: expected.to_owned(),
            actual,
        });
    }
    Ok(VerifiedReceipt {
        recorded_path: relative.to_owned(),
        resolved_path: file_path,
        sha256: actual,
        bytes,
    })
}

pub fn verify_receipt(
    root: &Path,
    relative: &str,
    expected: &str,
) -> Result<VerifiedReceipt, ReceiptError> {
    verify_one(&canonical_root(root)?, relative, expected, MAX_TOTAL_BYTES)
}

/// Entire register succeeds or returns an indexed refusal, never partial success.
/// Trust: a local non-hostile filesystem. No guarantee against path replacement
/// races, hostile concurrent writes, OS failures or real-time blocking IO.
pub fn verify_register(
    root: &Path,
    register: &Register,
) -> Result<Vec<VerifiedReceipt>, RegistryFailure> {
    let root = canonical_root(root).map_err(|cause| RegistryFailure { entry: None, cause })?;
    let mut remaining = MAX_TOTAL_BYTES;
    let mut verified = Vec::new();
    for (index, record) in register.records.iter().enumerate() {
        let result = verify_record(&root, record, remaining).map_err(|cause| RegistryFailure {
            entry: Some(index),
            cause,
        })?;
        remaining -= result.bytes;
        verified.push(result);
    }
    Ok(verified)
}

fn verify_record(
    root: &Path,
    record: &Record,
    remaining: usize,
) -> Result<VerifiedReceipt, ReceiptError> {
    if let Some(values) = &record.fixture_values {
        for value in values {
            resolved(root, value)?;
        }
    }
    verify_one(root, &record.path, &record.sha256, remaining)
}

#[cfg(test)]
#[path = "../../../quality/fixture_register/src/validator_tests.rs"]
mod tests;
