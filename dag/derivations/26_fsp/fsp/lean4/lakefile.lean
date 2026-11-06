import Lake
open Lake DSL

package «po023» where
  version := v!"1.0.0"

@[default_target]
lean_lib «FermionSignAll» where
  srcDir := "."
  roots := #[
    `FermionSignAll,
    `FermionSignCore,
    `GenesisFspBridge,
    `FermionGinCore,
    `HaltingQuotient,
    `MeronClusterInvolution,
    `MeronCharacter,
    `NormalFormLaws,
    `BqnfSignPacket,
    `FrustratedSpectrumObstruction,
    `NonAbelianGaugeSigns,
    `ReggePachnerWdw,
    `ChiralAnomalyInflow,
    `FqhLaughlinBraiding,
    `FibonacciAnyonBraiding,
    `IsingMajoranaBraiding,
    `BfLinkedFluxBraiding,
    `NonAbelianBfBraiding,
    `Higher2GroupBraiding,
    `Cobordism5dAnomaly,
    `InstantonDyonGas,
    `FoliatedFracton2Gauge
  ]
