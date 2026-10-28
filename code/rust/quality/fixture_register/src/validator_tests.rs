use super::*;
use serde_json::{json, Value};

const ABC: &str = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";

fn example() -> Value {
    json!({"schema":"omega_mub.fixture_receipts.v1","authority_effect":"None","description":"fixture",
        "kinds":{"literal":"literal","by_construction":"construction","assumed_constant":"assumption","no_producer":"missing"},
        "fixtures":[{"path":"a.json","sha256":ABC,"evidence_kind":"fixture","kind":"literal","fields":["verdict"],
            "producer":"example.rs:1","literal_at":["example.rs:1"],"reason":"fixture","fixture_values":[]}]})
}

fn parse(value: Value) -> Result<Register, ReceiptError> {
    parse_register(&serde_json::to_vec(&value).unwrap())
}

#[test]
fn malformed_entry_cannot_be_success() {
    for key in [
        "path",
        "sha256",
        "kind",
        "evidence_kind",
        "fields",
        "reason",
        "literal_at",
    ] {
        let mut value = example();
        value["fixtures"][0].as_object_mut().unwrap().remove(key);
        assert!(
            matches!(parse(value), Err(ReceiptError::Json { .. })),
            "{key}"
        );
    }
    let mut value = example();
    value["fixtures"][0]["path"] = json!(23);
    assert!(matches!(parse(value), Err(ReceiptError::Json { .. })));
}

#[test]
fn duplicate_keys_unknown_fields_and_authority_refuse() {
    let encoded = serde_json::to_string(&example()).unwrap();
    let duplicate = encoded.replacen(
        "\"path\":\"a.json\"",
        "\"path\":\"a.json\",\"path\":\"b.json\"",
        1,
    );
    assert!(matches!(
        parse_register(duplicate.as_bytes()),
        Err(ReceiptError::Json { .. })
    ));
    for (key, bad) in [
        ("authority_effect", json!("PROVED")),
        ("schema", json!("other")),
    ] {
        let mut value = example();
        value[key] = bad;
        assert_eq!(
            parse(value).unwrap_err(),
            ReceiptError::Invalid("schema and authority ceiling")
        );
    }
    let mut value = example();
    value["certified"] = json!(true);
    assert!(matches!(parse(value), Err(ReceiptError::Json { .. })));
    let mut value = example();
    value["fixtures"][0]["certified"] = json!(true);
    assert!(matches!(parse(value), Err(ReceiptError::Json { .. })));
    let mut value = example();
    value["fixtures"][0]["kind"] = json!("computed");
    assert!(matches!(parse(value), Err(ReceiptError::Json { .. })));
}

#[test]
fn digest_change_missing_empty_and_owned_result() {
    let root = tempfile::tempdir().unwrap();
    let path = root.path().join("a.json");
    std::fs::write(&path, b"abc").unwrap();
    let result = verify_receipt(root.path(), "a.json", ABC).unwrap();
    assert_eq!(result.sha256(), ABC);
    assert_eq!(result.bytes(), 3);
    assert_eq!(result.recorded_path(), "a.json");
    assert!(result
        .resolved_path()
        .starts_with(root.path().canonicalize().unwrap()));
    std::fs::write(&path, b"abd").unwrap();
    assert!(matches!(
        verify_receipt(root.path(), "a.json", ABC),
        Err(ReceiptError::DigestMismatch { .. })
    ));
    assert_eq!(result.sha256(), ABC); // a past owned observation, never a live-file certificate
    std::fs::remove_file(&path).unwrap();
    assert!(matches!(
        verify_receipt(root.path(), "a.json", ABC),
        Err(ReceiptError::Io {
            kind: ErrorKind::NotFound,
            ..
        })
    ));
    std::fs::write(&path, b"").unwrap();
    assert_eq!(
        verify_receipt(
            root.path(),
            "a.json",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
        .unwrap()
        .bytes(),
        0
    );
    root.close().unwrap();
}

#[test]
fn path_device_and_shape_refusals() {
    let root = tempfile::tempdir().unwrap();
    for bad in [
        "", "/x", "../x", "x/../y", "x//y", "x/./y", "C:/x", "x\\y", "x\0y", "CON", "aux.txt",
        "LPT1.log", "x. ", "x.",
    ] {
        assert!(relative_path(bad).is_err(), "{bad:?}");
    }
    std::fs::create_dir(root.path().join("dir")).unwrap();
    assert_eq!(
        verify_receipt(root.path(), "dir", ABC).unwrap_err(),
        ReceiptError::Invalid("regular file required")
    );
    let file = root.path().join("file");
    std::fs::write(&file, b"").unwrap();
    assert_eq!(
        verify_receipt(&file, "x", ABC).unwrap_err(),
        ReceiptError::Invalid("directory root required")
    );
    root.close().unwrap();
}

#[test]
fn canonical_link_escape_refuses() {
    let root = tempfile::tempdir().unwrap();
    let outside = tempfile::tempdir().unwrap();
    std::fs::write(outside.path().join("a.json"), b"abc").unwrap();
    let link = root.path().join("link");
    #[cfg(windows)]
    {
        let status = std::process::Command::new("cmd")
            .args(["/C", "mklink", "/J"])
            .arg(&link)
            .arg(outside.path())
            .output()
            .unwrap();
        assert!(
            status.status.success(),
            "junction creation unavailable: {:?}",
            status
        );
    }
    #[cfg(unix)]
    std::os::unix::fs::symlink(outside.path(), &link).unwrap();
    assert_eq!(
        verify_receipt(root.path(), "link/a.json", ABC).unwrap_err(),
        ReceiptError::OutsideRoot
    );
    #[cfg(windows)]
    std::fs::remove_dir(&link).unwrap();
    #[cfg(unix)]
    std::fs::remove_file(&link).unwrap();
    root.close().unwrap();
    outside.close().unwrap();
}

#[test]
fn metadata_lists_digest_and_no_producer() {
    for bad in [
        "0".repeat(63),
        "0".repeat(65),
        "A".repeat(64),
        "g".repeat(64),
    ] {
        assert!(digest_text(&bad).is_err());
    }
    for (field, value) in [
        ("fields", json!([])),
        ("literal_at", json!([])),
        ("reason", json!(" ")),
        ("producer", json!(" ")),
        ("fixture_values", json!(["../outside"])),
        ("evidence_kind", json!("computed")),
    ] {
        let mut data = example();
        data["fixtures"][0][field] = value;
        assert!(parse(data).is_err(), "{field}");
    }
    let mut data = example();
    data["fixtures"][0]["kind"] = json!("no_producer");
    data["fixtures"][0]["literal_at"] = json!([]);
    data["fixtures"][0]["producer"] = Value::Null;
    assert_eq!(parse(data).unwrap().len(), 1);
    let mut data = example();
    data["fixtures"] = json!([]);
    assert!(parse(data).is_err());
    assert!(strings(&vec!["x".into(); MAX_LIST_ITEMS], false).is_ok());
    assert_eq!(
        strings(&vec!["x".into(); MAX_LIST_ITEMS + 1], false),
        Err(ReceiptError::Limit("list items"))
    );
    assert!(strings(&[" ".into()], false).is_err());
}

#[test]
fn projected_path_duplicates_refuse() {
    let mut data = example();
    let mut second = data["fixtures"][0].clone();
    data["fixtures"][0]["path"] = json!("omega_engine/crates_rs/tests/omega_mub/a.json");
    second["path"] = json!("code/rust/tests/mub/a.json");
    data["fixtures"].as_array_mut().unwrap().push(second);
    assert_eq!(
        parse(data).unwrap_err(),
        ReceiptError::Invalid("duplicate resolved receipt")
    );
}

#[test]
fn declared_size_and_stream_limits() {
    assert_eq!(
        (
            MAX_REGISTER_BYTES,
            MAX_RECEIPT_BYTES,
            MAX_TOTAL_BYTES,
            MAX_ENTRIES,
            MAX_LIST_ITEMS,
            MAX_PATH_BYTES,
            MAX_TEXT_BYTES
        ),
        (1 << 20, 16 << 20, 64 << 20, 4096, 128, 2048, 8192)
    );
    assert_eq!(
        parse_register(&vec![b' '; MAX_REGISTER_BYTES + 1]).unwrap_err(),
        ReceiptError::Limit("register bytes")
    );
    assert!(relative_path(&"x".repeat(MAX_PATH_BYTES)).is_ok());
    assert_eq!(
        relative_path(&"x".repeat(MAX_PATH_BYTES + 1)),
        Err(ReceiptError::Limit("path bytes"))
    );
    assert!(text(&"x".repeat(MAX_TEXT_BYTES)).is_ok());
    assert_eq!(
        text(&"x".repeat(MAX_TEXT_BYTES + 1)),
        Err(ReceiptError::Limit("text bytes"))
    );
    let root = tempfile::tempdir().unwrap();
    let path = root.path().join("bytes");
    std::fs::write(&path, b"abcd").unwrap();
    assert_eq!(
        read_bounded(File::open(&path).unwrap(), 3),
        Err(ReceiptError::Limit("receipt or total bytes"))
    );
    assert_eq!(read_bounded(File::open(&path).unwrap(), 4).unwrap().1, 4);
    assert_eq!(
        read_bounded(File::open(&path).unwrap(), 0),
        Err(ReceiptError::Limit("receipt or total bytes"))
    );
    root.close().unwrap();
}

#[test]
fn per_file_and_total_byte_caps_are_distinct() {
    let root = tempfile::tempdir().unwrap();
    let path = root.path().join("a.json");
    let file = File::create(&path).unwrap();
    file.set_len((MAX_RECEIPT_BYTES + 1) as u64).unwrap();
    drop(file);
    assert_eq!(
        verify_receipt(root.path(), "a.json", ABC).unwrap_err(),
        ReceiptError::Limit("receipt or total bytes")
    );
    File::options()
        .write(true)
        .open(&path)
        .unwrap()
        .set_len(MAX_RECEIPT_BYTES as u64)
        .unwrap();
    let expected = read_bounded(File::open(&path).unwrap(), MAX_RECEIPT_BYTES)
        .unwrap()
        .0;
    let mut data = example();
    data["fixtures"] = json!([]);
    for index in 0..5 {
        let name = format!("file{index}.json");
        std::fs::hard_link(&path, root.path().join(&name)).unwrap();
        let mut row = example()["fixtures"][0].clone();
        row["path"] = json!(name);
        row["sha256"] = json!(expected);
        data["fixtures"].as_array_mut().unwrap().push(row);
    }
    let failure = verify_register(root.path(), &parse(data).unwrap()).unwrap_err();
    assert_eq!(failure.entry, Some(4));
    assert_eq!(failure.cause, ReceiptError::Limit("receipt or total bytes"));
    root.close().unwrap();
}

#[test]
fn entry_count_limit_has_an_admitted_byte_envelope() {
    let mut data = example();
    let row = json!({"path":"p","sha256":ABC,"evidence_kind":"fixture","kind":"literal","fields":["v"],"literal_at":["x"],"reason":"r"});
    data["fixtures"] = json!([]);
    for i in 0..MAX_ENTRIES {
        let mut row = row.clone();
        row["path"] = json!(format!("p{i}"));
        data["fixtures"].as_array_mut().unwrap().push(row);
    }
    assert!(serde_json::to_vec(&data).unwrap().len() < MAX_REGISTER_BYTES);
    assert_eq!(parse(data.clone()).unwrap().len(), MAX_ENTRIES);
    let mut extra = row;
    extra["path"] = json!("extra");
    data["fixtures"].as_array_mut().unwrap().push(extra);
    assert!(serde_json::to_vec(&data).unwrap().len() < MAX_REGISTER_BYTES);
    assert_eq!(
        parse(data).unwrap_err(),
        ReceiptError::Limit("register entries")
    );
}

#[test]
fn indexed_failure_and_value_file_check() {
    let root = tempfile::tempdir().unwrap();
    std::fs::write(root.path().join("a.json"), b"abc").unwrap();
    let register = parse(example()).unwrap();
    assert!(!register.is_empty());
    assert_eq!(verify_register(root.path(), &register).unwrap().len(), 1);
    assert_eq!(
        verify_register(&root.path().join("absent-root"), &register)
            .unwrap_err()
            .entry,
        None
    );
    let mut data = example();
    data["fixtures"][0]["fixture_values"] = json!(["absent.json"]);
    let failure = verify_register(root.path(), &parse(data).unwrap()).unwrap_err();
    assert_eq!(failure.entry, Some(0));
    assert!(matches!(
        failure.cause,
        ReceiptError::Io {
            kind: ErrorKind::NotFound,
            ..
        }
    ));
    root.close().unwrap();
}

#[test]
fn compiled_candidate_binding() {
    let actual = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join(compiled_source())
        .canonicalize()
        .unwrap();
    if let Some(expected) = std::env::var_os("TFQM_EXPECTED_COMPILED_SOURCE") {
        assert_eq!(
            actual,
            PathBuf::from(expected).canonicalize().unwrap(),
            "stale compiled source binding"
        );
    }
    println!("COMPILED_SOURCE {}", actual.display());
}

#[test]
fn historical_paths_are_explicit_and_not_guessed() {
    assert_eq!(
        relocate("omega_engine/crates_rs/tests/omega_mub/a.json"),
        "code/rust/tests/mub/a.json"
    );
    assert_eq!(
        relocate("omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts/a.json"),
        "papers/core/mub6/artifacts/a.json"
    );
    assert_eq!(
        relocate("omega_engine/crates_rs/omega_mub/fixtures/a.json"),
        "code/rust/src/mub/fixtures/a.json"
    );
    assert_eq!(relocate("unrelated/a.json"), "unrelated/a.json");
}

#[test]
fn actual_register_custody_does_not_promote_fixtures() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .find(|p| p.join("SCORING.md").is_file() && p.join("scripts/contract_scores.py").is_file())
        .expect("repository markers");
    let raw = std::fs::read(
        root.join("code/rust/tests/mub/fixture_receipt_register_current.json"),
    )
    .unwrap();
    let register = parse_register(&raw).unwrap();
    let observations = verify_register(root, &register).unwrap();
    assert_eq!(observations.len(), register.len());
    let bytes: usize = observations.iter().map(VerifiedReceipt::bytes).sum();
    println!(
        "FIXTURE_CUSTODY {}",
        json!({"AuthorityEffect":"None","kind":"fixture-only","entries":observations.len(),"bytes":bytes,
        "observations":observations.iter().map(|v|json!({"recorded_path":v.recorded_path(),"resolved_path":v.resolved_path(),"sha256":v.sha256(),"bytes":v.bytes()})).collect::<Vec<_>>()})
    );
}

#[test]
fn annotated_receipts_preserve_history_and_fixture_status() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .find(|p| p.join("SCORING.md").is_file())
        .unwrap();
    let directory = root.join("code/rust/tests/mub");
    let history = std::fs::read(directory.join("fixture_receipt_register.json")).unwrap();
    let current = std::fs::read(directory.join("fixture_receipt_register_current.json")).unwrap();
    let transitions: Value = serde_json::from_slice(
        &std::fs::read(directory.join("fixture_receipt_transitions.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(transitions["authority_effect"], "None");
    assert_eq!(
        format!("{:x}", Sha256::digest(&history)),
        transitions["historical_register_sha256"]
    );
    assert_eq!(
        format!("{:x}", Sha256::digest(&current)),
        transitions["current_register_sha256"]
    );
    // Historical custody must still refuse the corrected current bytes.
    let historical = parse_register(&history).unwrap();
    assert!(matches!(
        verify_register(root, &historical).unwrap_err().cause,
        ReceiptError::DigestMismatch { .. }
    ));
    let original: Value = serde_json::from_slice(&history).unwrap();
    let mut updated: Value = serde_json::from_slice(&current).unwrap();
    let changes = transitions["transitions"].as_array().unwrap();
    assert_eq!(changes.len(), 4);
    let mut seen = HashSet::new();
    for change in changes {
        let path = change["path"].as_str().unwrap();
        assert!(seen.insert(path));
        verify_receipt(root, path, change["after_sha256"].as_str().unwrap()).unwrap();
        let snapshot = change["historical_snapshot"].as_str().unwrap();
        verify_receipt(root, snapshot, change["before_sha256"].as_str().unwrap()).unwrap();
        let mut annotated: Value =
            serde_json::from_slice(&std::fs::read(root.join(path)).unwrap()).unwrap();
        let old: Value =
            serde_json::from_slice(&std::fs::read(root.join(snapshot)).unwrap()).unwrap();
        let fields = change["added_fields"].as_object().unwrap();
        assert_eq!(fields.len(), 3);
        assert!(fields["certificate_status"]
            .as_str()
            .unwrap()
            .starts_with("NOT_A_CERTIFICATE:"));
        for key in [
            "certificate_status",
            "certificate_status_corrected",
            "certificate_status_note",
        ] {
            assert!(old.get(key).is_none());
            assert_eq!(
                annotated.as_object_mut().unwrap().remove(key).unwrap(),
                fields[key]
            );
        }
        assert_eq!(
            annotated, old,
            "only the documented warning fields may change"
        );
        let record = updated["fixtures"]
            .as_array_mut()
            .unwrap()
            .iter_mut()
            .find(|r| relocate(r["path"].as_str().unwrap()) == path)
            .unwrap();
        assert_eq!(record["sha256"], change["after_sha256"]);
        record["sha256"] = change["before_sha256"].clone();
    }
    updated["description"] = original["description"].clone();
    assert_eq!(
        updated, original,
        "fixture classification and all other records are preserved"
    );
}
