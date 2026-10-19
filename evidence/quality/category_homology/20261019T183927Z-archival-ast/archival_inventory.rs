//! Full syn item/attribute inventory for the recorded archival source prefix.
//! This is an auxiliary verifier, not the calibrated complexity tool or a
//! category-theory implementation. AuthorityEffect: None.
use std::{env, fs, path::Path, process::ExitCode};

const BOUNDARY: &str = "// TFQM_ARCHIVAL_REPLAY_BOUNDARY_20261019";

fn inspect(path: &Path) -> Result<serde_json::Value, String> {
    let source = fs::read_to_string(path).map_err(|e| format!("read: {e}"))?;
    let prefix = source.split_once(BOUNDARY)
        .ok_or_else(|| "missing recorded fixture boundary".to_string())?.0;
    let parsed = match syn::parse_file(prefix) {
        Ok(file) => file,
        Err(error) => return Ok(serde_json::json!({
            "valid_syntax":false,"input":path.to_string_lossy(),"error":error.to_string()
        })),
    };
    let kinds: Vec<_> = parsed.items.iter().map(|item| match item {
        syn::Item::Const(_) => "const", syn::Item::Enum(_) => "enum",
        syn::Item::Fn(_) => "fn", syn::Item::ForeignMod(_) => "foreign_mod",
        syn::Item::Impl(_) => "impl", syn::Item::Macro(_) => "macro",
        syn::Item::Mod(_) => "mod", syn::Item::Static(_) => "static",
        syn::Item::Struct(_) => "struct", syn::Item::Trait(_) => "trait",
        syn::Item::TraitAlias(_) => "trait_alias", syn::Item::Type(_) => "type",
        syn::Item::Union(_) => "union", syn::Item::Use(_) => "use",
        syn::Item::Verbatim(_) => "verbatim", _ => "other",
    }).collect();
    let non_doc = parsed.attrs.iter().filter(|attribute| !attribute.path().is_ident("doc")).count();
    Ok(serde_json::json!({"valid_syntax":true,"input":path.to_string_lossy(),
        "prefix_utf8_bytes":prefix.len(),"top_level_item_count":parsed.items.len(),
        "item_kinds":kinds,"inner_attribute_count":parsed.attrs.len(),
        "non_doc_inner_attributes":non_doc,"scope":"Source prefix only, before the appended native fixture. Top-level items include non-functions. No macro expansion or mathematical algorithm claim."}))
}

fn main() -> ExitCode {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 { eprintln!("expected source path and owned inventory directory"); return ExitCode::from(3); }
    let path = Path::new(&args[1]);
    let value = match inspect(path) {
        Ok(value) => value,
        Err(error) => { eprintln!("{error}"); return ExitCode::from(3); }
    };
    let Some(stem) = path.file_stem() else { return ExitCode::from(3); };
    let destination = Path::new(&args[2]).join(stem).with_extension("json");
    if let Err(error) = fs::write(destination, value.to_string()) {
        eprintln!("inventory write: {error}"); return ExitCode::from(3);
    }
    println!("{value}");
    if value["valid_syntax"] != true { return ExitCode::from(2); }
    if value["top_level_item_count"] == 0 && value["non_doc_inner_attributes"] == 0 {
        ExitCode::SUCCESS
    } else { ExitCode::from(1) }
}
