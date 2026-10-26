import Lake
open Lake DSL

package «mssn_presentation» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

@[default_target]
lean_lib «MssnPresentation» where
  roots := #[`MssnSyntax, `MssnSimplicialGauge, `MssnSmithNormalForm, `MssnQuantumTransfer, `MssnObstructionDetector, `MssnFiniteAlgebra]
