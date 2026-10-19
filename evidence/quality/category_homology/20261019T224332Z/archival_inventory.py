"""Native compiler plus full-item source-prefix inventory. AuthorityEffect: None."""
import json

BOUNDARY = '// TFQM_ARCHIVAL_REPLAY_BOUNDARY_20261019'

def challenge(subject):
    executable=json.dumps(subject['ast_binary'])
    destination=json.dumps(subject['ast_inventory_dir'])
    return '\n'+BOUNDARY+r'''
#[cfg(test)] mod independent_archival_inventory {
 #[test] fn archived_module_has_no_active_items() {
  let output=std::process::Command::new(AST_BINARY).args([file!(),INVENTORY_DIR]).output().expect("recorded AST verifier must execute");
  println!("ARCHIVAL_AST {}",String::from_utf8_lossy(&output.stdout));
  assert_eq!(output.status.code(),Some(0),"archival source must parse with no active items or non-doc attributes");
 }
 const AST_BINARY:&str=EXE;
 const INVENTORY_DIR:&str=DEST;
}
'''.replace('EXE',executable).replace('DEST',destination)
