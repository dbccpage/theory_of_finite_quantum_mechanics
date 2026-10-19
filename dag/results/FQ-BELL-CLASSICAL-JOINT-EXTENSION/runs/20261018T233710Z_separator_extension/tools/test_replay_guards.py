import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUN=Path(__file__).resolve().parent.parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
replay=module('separator_replay',RUN/'replay.py')
checker=module('separator_checker',RUN/'check_candidate.py')


class ReplayGuardTests(unittest.TestCase):
    def test_empty_evidence_inventory_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'custody:empty_manifest'):replay.verify_inventory(Path(d),{'artifacts':[]})
    def test_artifact_path_escape_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'custody:path_escape'):replay.safe(Path(d),'../outside.txt')
    def test_raw_duplicate_and_float_json_are_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'candidate.json'
            for raw in [b'{"weights":[],"weights":["1"]}',b'{"value":0.5}']:
                p.write_bytes(raw)
                with self.assertRaisesRegex(ValueError,'G1_SCHEMA:'):checker.load(p)
    def test_corruption_is_refused_under_python_optimization(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'evidence.txt';p.write_bytes(b'original')
            manifest={'artifacts':[{'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}
            replay.verify_inventory(root,manifest);p.write_bytes(b'corrupted')
            source='import importlib.util,pathlib; s=importlib.util.spec_from_file_location("r",'+repr(str(RUN/'replay.py'))+'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.verify_inventory(pathlib.Path('+repr(str(root))+'),'+repr(manifest)+')'
            child=subprocess.run([sys.executable,'-O','-c',source],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertNotEqual(child.returncode,0);self.assertIn(b'custody:artifact:evidence.txt',child.stderr)


if __name__=='__main__':unittest.main()
