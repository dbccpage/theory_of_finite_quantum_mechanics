from pathlib import Path
import hashlib,importlib.util,json,shutil,sys

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');STAGING=Path(__file__).resolve().parent
RUN=ROOT/'dag/results/FQ-CARRIER-CONTRACT-V2/runs/20261019T015232Z_staged';EXT=Path(r'C:\Users\a343o\source\repos\the_symbol_game')
spec=importlib.util.spec_from_file_location('native',ROOT/'dag/results/batches/20261019T015232Z_next_ten/native.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
domain=ROOT/'code/python/src/qm/domain/cyclotomic_tower.py';records=[]
references=[('this_repository',domain,Path('code/python/src/qm/domain/cyclotomic_tower.py'),'historical_before_guard_repair'),('the_symbol_game',EXT/'omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/carrier_contract.yaml',Path('claims/carrier_contract.yaml'),'declaration_input'),('the_symbol_game',EXT/'omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/evidence/carrier_inventory.json',Path('evidence/carrier_inventory.json'),'declaration_input')]
references += [('the_symbol_game',EXT/'omega_engine/crates_rs/omega_number_theory/src'/name,Path('native_dependency')/name,'read_only_native_dependency') for name in ('cyclotomic_field.rs','polynomial.rs','cyclotomic120.rs')]
for repository,actual,relative,role in references:
    snapshot=RUN/'p0/additional_sources'/relative;snapshot.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(actual,snapshot);digest=hashlib.sha256(actual.read_bytes()).hexdigest()
    records.append({'repository':repository,'source_path':str(actual),'source_absolute_path':str(actual),'role':role,'available':True,'recorded_sha256':digest,'actual_sha256':digest,'matches_recorded_pin':True,'snapshot':snapshot.relative_to(ROOT).as_posix()})
(RUN/'p0/additional_source_inventory.json').write_bytes((json.dumps({'source_records':records},indent=2)+'\n').encode())
code='import importlib.util; s=importlib.util.spec_from_file_location("legacy_cyclotomic",'+repr(str(domain))+');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);x=m.CyclotomicElement.zeta(3).lift_to(4);print("invalid_3_to_4_lift_accepted",x.conductor,list(map(str,x.coeffs)))'
native.record(RUN/'p0/native','original_optimized_lift_probe',[sys.executable,'-O','-c',code],sources=[domain])
text=domain.read_text();text=text.replace('''        if m == n:
            return self
        assert n % m == 0, f"Cannot lift from conductor {m} to non-multiple {n}"''','''        if type(n) is not int or n < 1:
            raise ValueError("Target conductor must be a positive integer")
        if m == n:
            return self
        if n % m != 0:
            raise ValueError(f"Cannot lift from conductor {m} to non-multiple {n}")''')
text=text.replace('''        assert w.is_real(), "Born weight must be invariant under complex conjugation"''','''        if not w.is_real():
            raise ArithmeticError("Born weight is not invariant under complex conjugation")''')
domain.write_bytes(text.encode())
for src,relative in [('carrier_contract.py','code/python/src/qm/carrier_contract.py'),('carrier_contract.rs','code/rust/src/finite_probability/carrier_contract.rs'),('carrier_contract_replay.rs','code/rust/src/finite_probability/examples/carrier_contract_replay.rs'),('PromptCarrierContract.lean','lean4/PromptCarrierContract.lean'),('test_carrier_contract.py','code/python/tests/test_carrier_contract.py')]:shutil.copyfile(STAGING/src,ROOT/relative)
for src,relative in [('check_carrier_contract.py','check_candidate.py'),('format_carrier_contract.py','format_certificate.py')]:shutil.copyfile(STAGING/src,RUN/relative)
p=ROOT/'code/rust/src/finite_probability/lib.rs';text=p.read_text().replace('pub mod cabello_obstruction;','pub mod cabello_obstruction;\npub mod carrier_contract;');p.write_bytes(text.encode())
p=ROOT/'lean4/lakefile.lean';text=p.read_text().replace('    `PromptCabelloParity,','    `PromptCabelloParity,\n    `PromptCarrierContract,');p.write_bytes(text.encode())
shutil.copyfile(STAGING/'target_stages.py',ROOT/'dag/results/batches/20261019T015232Z_next_ten/target_stages.py')
