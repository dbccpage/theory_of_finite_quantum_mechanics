from pathlib import Path
import json,re,hashlib,subprocess
B=Path(__file__).resolve().parents[1]
accepted={'ReconstructionArithmetic.lean':'base_reconstructionarithmetic','ClassicalExclusion.lean':'base_classicalexclusion','ReconstructionGeometry.lean':'base_interface_retry','CatalogueGeometry.lean':'helpers_02','ConcreteJordanProducts.lean':'products_04','ClassicalModel.lean':'classical_03','QubitModel.lean':'qubit_03','SupportedJordanCatalogue.lean':'catalogue_02','JordanConeSquares.lean':'cones_03','CatalogueApplications.lean':'applications_02'}
(B/'accepted_modules.json').write_text(json.dumps(accepted,indent=2)+'\n',encoding='utf-8')
names=[]
for source,label in accepted.items():
 d=B/'verification'/label;r=json.loads((d/'receipt.json').read_text(encoding='utf-8'))
 if r['exit_code']!=0:raise RuntimeError('Unaccepted compile: '+label)
 names += re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)",(d/'stdout.txt').read_text(encoding='utf-8'))
extra=['FiniteQM.SupportedJordanCatalogue.Entry','FiniteQM.SupportedJordanCatalogue.Entry.model_dim','FiniteQM.SupportedJordanCatalogue.Entry.model_rank','FiniteQM.SupportedJordanCatalogue.Entry.classical_geometry','FiniteQM.SupportedJordanCatalogue.Entry.qubit_geometry','FiniteQM.SupportedJordanCatalogue.Supported','FiniteQM.ConcreteJordanProducts.classicalMul','FiniteQM.ConcreteJordanProducts.classicalUnit','FiniteQM.ConcreteJordanProducts.classicalTrace','FiniteQM.ConcreteJordanProducts.classicalPositive','FiniteQM.ConcreteJordanProducts.spinMul','FiniteQM.ConcreteJordanProducts.spinUnit','FiniteQM.ConcreteJordanProducts.spinTrace','FiniteQM.ConcreteJordanProducts.spinPositive','FiniteQM.ConcreteJordanProducts.blochState','FiniteQM.ReconstructionGeometry.JordanBridge.classify']
source='import CatalogueApplications\n\n-- Exact types expose every implicit and explicit premise.\n'+'\n'.join('#check @'+n for n in names+extra)+'\n'
(B/'CatalogueSignatures.lean').write_text(source,encoding='utf-8')
print('Prepared exact signatures:',len(names+extra))