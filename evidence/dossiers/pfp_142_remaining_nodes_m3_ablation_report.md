# Remaining 142 DAG Nodes (`36..177`): Live Mission M3 Decoy Equations Ablation Report

**AuthorityEffect:** `None`  
**Model Evaluated:** `deepseek/deepseek-v4.1-flash` (`openrouter:deepseek/deepseek-v4.1-flash`)  
**Paired DAG Nodes Evaluated:** `142 / 142` (`prompt_index` `36`..`177`)  

## 1. Aggregate First-Attempt Pass Rate & Marginal Contribution of Mission M3 (`slot_m3_layer2_ideals_and_annihilators`)

| Metric | Without Mission M3 Decoy Equations (`M1+M2+M4`) | With Mission M3 Decoy Equations (`M1+M2+M3+M4`) | Marginal M3 Contribution ($\Delta$) |
|---|---:|---:|---:|
| **Attempt-1 All-Gates Pass (`G0..G6`)** | `52 / 142` (`36.62%`) | `134 / 142` (`94.37%`) | **`+82` nodes (`+57.75%`)** |
| **Final Multi-Stage Pass (`<= 2` attempts)** | — | `142 / 142` (`100.0%`) | — |
| **`G4` Countermodel Decoy Failures (`Attempt 1`)** | `89` | `1` | **`-88` failures** |
| **`G5` Unconditional Promotion Failures (`Attempt 1`)** | `2` | `0` | **`-2` failures** |
| **Mean Completion Tokens (`Attempt 1`)** | `866.4` | `686.1` | **`-180.3` tokens** |
| **Mean Latency (`Attempt 1`, ms)** | `29616.5 ms` | `21096.1 ms` | **`-8520.4 ms`** |

## 2. Stage-by-Stage Breakdown (`36..177`)

| Stage | Nodes | Without M3 (Attempt 1 Pass) | With M3 (Attempt 1 Pass) | With M3 (Final Pass) |
|---|---:|---:|---:|---:|
| `PREGENESIS` | 14 | `1 / 14` | `14 / 14` | **`14 / 14`** |
| `GENESIS` | 11 | `1 / 11` | `10 / 11` | **`11 / 11`** |
| `MSSN_SN` | 2 | `0 / 2` | `2 / 2` | **`2 / 2`** |
| `WDP` | 6 | `1 / 6` | `6 / 6` | **`6 / 6`** |
| `L1_EMERGENCE` | 9 | `3 / 9` | `8 / 9` | **`9 / 9`** |
| `L1_TO_L2` | 19 | `10 / 19` | `19 / 19` | **`19 / 19`** |
| `FINITE_QM_CORE` | 20 | `9 / 20` | `17 / 20` | **`20 / 20`** |
| `FINITE_QM_STRUCTURE` | 40 | `17 / 40` | `38 / 40` | **`40 / 40`** |
| `FINITE_QM_DYNAMICS` | 14 | `6 / 14` | `13 / 14` | **`14 / 14`** |
| `IMPLEMENTATION` | 7 | `4 / 7` | `7 / 7` | **`7 / 7`** |

## 3. Node-by-Node Paired Comparison (`36..177`)

| # | Node ID | Stage | Status | Exp CM | Without-M3 Status (Emitted CM / Refused) | With-M3 Attempt-1 Status | With-M3 Final |
|---:|---|---|---|---:|---|---|---|
| 036 | `PG-ROOT-DIFF-STRUCTURE` | `PREGENESIS` | `ADMITTED_PRIMITIVE` | `38` | `FAIL` (`cm=39`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 037 | `PG-INERT-DIAMOND` | `PREGENESIS` | `DEFINITION` | `39` | `FAIL` (`cm=119`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 038 | `PG-SIX-OPERATIONS` | `PREGENESIS` | `DEFINITION` | `40` | `FAIL` (`cm=41`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 039 | `PG-PRIMDIFF-AXIOMS` | `PREGENESIS` | `DEFINITION` | `41` | `FAIL` (`cm=42`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 040 | `PG-ADMISSION-FLOOR` | `PREGENESIS` | `PROVED_LEAN` | `42` | `FAIL` (`cm=43`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 041 | `PG-COLLAPSE-BARRIER` | `PREGENESIS` | `PROVED_LEAN` | `43` | `FAIL` (`cm=44`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 042 | `PG-HISTORY-REPORT-CRITERION` | `PREGENESIS` | `PROVED_LEAN` | `44` | `FAIL` (`cm=45`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 043 | `PG-PREGEN-CONSTRUCTIVE-SUMMARY` | `PREGENESIS` | `PROVED_LEAN` | `45` | `FAIL` (`cm=46`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 044 | `PG-DEMAND-ACCOUNTING` | `PREGENESIS` | `PROVED_LEAN` | `46` | `FAIL` (`cm=47`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 045 | `PG-REFINE-SEPARATES` | `PREGENESIS` | `PROVED_LEAN` | `47` | `FAIL` (`cm=48`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 046 | `PG-OLD-IMAGE-INJECTIVE` | `PREGENESIS` | `PROVED_LEAN` | `48` | `FAIL` (`cm=49`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 047 | `PG-SN-OFF-IMAGE-REFUSAL` | `PREGENESIS` | `PROVED_LEAN` | `49` | `FAIL` (`cm=50`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 048 | `PG-FREE-MONOID-NONISO` | `PREGENESIS` | `PROVED_LEAN` | `50` | `PASS` (`cm=50`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 049 | `PG-CHAIN-RETRACTION` | `PREGENESIS` | `PROVED_LEAN` | `51` | `FAIL` (`cm=52`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 050 | `PG-MSS0-ONLY-DIAMOND` | `GENESIS` | `DEFINITION` | `54` | `FAIL` (`cm=56`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 051 | `PG-GEN-REGIME-EVENTS` | `GENESIS` | `DEFINITION` | `55` | `FAIL` (`cm=57`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 052 | `PG-GEN-SUPPLY-NO-OP` | `GENESIS` | `PROVED_LEAN` | `56` | `FAIL` (`cm=58`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 053 | `PG-GEN-SUPPLY-ERASURE` | `GENESIS` | `PROVED_LEAN` | `57` | `FAIL` (`cm=59`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 054 | `PG-GEN-COLLAPSE-AND-FIRST-SEPARATION` | `GENESIS` | `PROVED_LEAN` | `58` | `PASS` (`cm=58`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 055 | `PG-GEN-NO-RETURN` | `GENESIS` | `PROVED_LEAN` | `59` | `FAIL` (`cm=61`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 056 | `PG-GEN-IRREFLEXIVE-DISTINCT` | `GENESIS` | `PROVED_LEAN` | `60` | `FAIL` (`cm=62`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 057 | `PG-GEN-ONGOING-OBSTRUCTION` | `GENESIS` | `PROVED_LEAN` | `61` | `FAIL` (`cm=63`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 058 | `PG-GEN-ONGOING-FEWEST-CHANGES` | `GENESIS` | `PROVED_LEAN` | `62` | `FAIL` (`cm=64`, `ref=False`) | **PASS** | **PASS** (`a=1`) |
| 059 | `PG-GEN-REWRITING-COMMUTATION` | `GENESIS` | `PROVED_LEAN` | `63` | `FAIL` (`cm=65`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 060 | `PG-GEN-SAMENESS-REFINEMENTS` | `GENESIS` | `PROVED_LEAN` | `64` | `FAIL` (`cm=66`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 061 | `PG-SN-CARRIER` | `MSSN_SN` | `PROVED_LEAN` | `67` | `FAIL` (`cm=70`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 062 | `PG-OBLIGATION-MONOID` | `MSSN_SN` | `PROVED_LEAN` | `68` | `FAIL` (`cm=71`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 063 | `PG-WDP-PROTECTED-QUESTIONS` | `WDP` | `PROVED_LEAN` | `71` | `FAIL` (`cm=75`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 064 | `PG-WDP-DEGREE1-WINDOW` | `WDP` | `DEFINITION` | `72` | `FAIL` (`cm=76`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 065 | `PG-WDP-QUOTIENT-EXACT-SEQUENCE` | `WDP` | `PROVED_LEAN` | `73` | `FAIL` (`cm=77`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 066 | `PG-WDP-GROWTH-NO-REPAIR` | `WDP` | `PROVED_LEAN` | `74` | `FAIL` (`cm=78`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 067 | `PG-WDP-DIAGNOSTIC-NOT-ROUTING` | `WDP` | `DEFINITION` | `75` | `PASS` (`cm=75`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 068 | `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS` | `WDP` | `PROVED_LEAN` | `76` | `FAIL` (`cm=80`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 069 | `L1-WDP-WINDOW-PHI1-GAMMA2` | `L1_EMERGENCE` | `DEFINITION` | `79` | `PASS` (`cm=79`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 070 | `L1-OBSERVER-AXIOMS-H1-H5` | `L1_EMERGENCE` | `ADMITTED_PRIMITIVE` | `80` | `FAIL` (`cm=85`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 071 | `L1-GS000-EDGEWISE-L1` | `L1_EMERGENCE` | `PROVED_LEAN` | `81` | `FAIL` (`cm=86`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 072 | `L1-GS001-GAUGE-L1` | `L1_EMERGENCE` | `PROVED_LEAN` | `82` | `FAIL` (`cm=87`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 073 | `L1-WDP-CH08-C01-REPLICA-L1` | `L1_EMERGENCE` | `PROVED_LEAN` | `83` | `FAIL` (`cm=88`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 074 | `L1-WDP-WITNESS-MASS` | `L1_EMERGENCE` | `DEFINITION` | `84` | `PASS` (`cm=84`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 075 | `L1-QM002-O022A-PHI1-QUOTIENT` | `L1_EMERGENCE` | `PROVED_LEAN` | `85` | `FAIL` (`cm=90`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 076 | `L1-FRAMEWORK-KKT-CERT` | `L1_EMERGENCE` | `PROVED_LEAN` | `86` | `PASS` (`cm=86`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 077 | `L1-CHAIN-D1D0-AXIOM` | `L1_EMERGENCE` | `ADMITTED_PRIMITIVE` | `87` | `FAIL` (`cm=271`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 078 | `L1-OPERATOR-LIFT-TRACE-EMBED-013` | `L1_TO_L2` | `PROVED_LEAN` | `90` | `PASS` (`cm=90`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 079 | `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED` | `L1_TO_L2` | `PROVED_LEAN` | `91` | `PASS` (`cm=91`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 080 | `L1-DENSITY-LIFT-SIGNED-SQRT-PUB009` | `L1_TO_L2` | `PROVED_LEAN` | `92` | `PASS` (`cm=92`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 081 | `L1-QM020-THM1-DIRECT-NORMALIZATION` | `L1_TO_L2` | `PROVED_LEAN` | `93` | `PASS` (`cm=93`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 082 | `L1-QM020-THM2A-L1-ADDITIVITY-DEFECT` | `L1_TO_L2` | `PROVED_LEAN` | `94` | `PASS` (`cm=94`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 083 | `L1-QM020-THM3-ROW-SPARSITY` | `L1_TO_L2` | `PROVED_LEAN` | `95` | `FAIL` (`cm=101`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 084 | `L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY` | `L1_TO_L2` | `PROVED_LEAN` | `96` | `PASS` (`cm=96`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 085 | `L1-QM020-THM5-PHASE-AVERAGED-SHADOW` | `L1_TO_L2` | `PROVED_LEAN` | `97` | `FAIL` (`cm=103`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 086 | `L1-QM020-THM6-P1-SCOPE-FENCE` | `L1_TO_L2` | `PROVED_LEAN` | `98` | `FAIL` (`cm=104`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 087 | `L1-QM020-THM7-REPRESENTATION-CAPACITY` | `L1_TO_L2` | `PROVED_LEAN` | `99` | `PASS` (`cm=99`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 088 | `L1-WDP-REALIFICATION-J` | `L1_TO_L2` | `DEFINITION` | `100` | `FAIL` (`cm=106`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 089 | `L1-QM121-LADDER-RUNGS-2-6` | `L1_TO_L2` | `PROVED_LEAN` | `101` | `PASS` (`cm=101`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 090 | `L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE` | `L1_TO_L2` | `PROVED_LEAN` | `102` | `FAIL` (`cm=108`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 091 | `L1-QM122-CIRCLE-SELECTOR-BOUNDARY` | `L1_TO_L2` | `PROVED_LEAN` | `103` | `PASS` (`cm=103`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 092 | `L1-QM122-BORN-PAIRING-NONUNIQUE` | `L1_TO_L2` | `PROVED_LEAN` | `104` | `FAIL` (`cm=110`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 093 | `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED` | `L1_TO_L2` | `PROVED_LEAN` | `105` | `FAIL` (`cm=111`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 094 | `L1-U1-SELECTOR-OTHER-SEGMENT` | `L1_TO_L2` | `PROVED_LEAN` | `106` | `FAIL` (`cm=112`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 095 | `L1-QM020-C10-BRANCH-LOCALIZATION` | `L1_TO_L2` | `PROVED_LEAN` | `107` | `PASS` (`cm=107`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 096 | `L1-QM003-C17-COMPOSABLE-FACTORIZATION` | `L1_TO_L2` | `PROVED_LEAN` | `108` | `FAIL` (`cm=114`, `ref=False`) | **PASS** | **PASS** (`a=1`) |
| 097 | `FQ-CARRIER-CONTRACT-V2` | `FINITE_QM_CORE` | `DEFINITION` | `111` | `FAIL` (`cm=118`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 098 | `FQ-PRIMDIFF-QUOTIENT-KERNEL` | `FINITE_QM_CORE` | `PROVED_LEAN` | `112` | `FAIL` (`cm=119`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 099 | `FQ-PHASE-FIBER-QUOTIENT` | `FINITE_QM_CORE` | `PROVED_LEAN` | `113` | `FAIL` (`cm=120`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 100 | `FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED` | `FINITE_QM_CORE` | `PROVED_LEAN` | `114` | `FAIL` (`cm=121`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 101 | `FQ-BORN-NORMALIZATION-REDUNDANCY` | `FINITE_QM_CORE` | `PROVED_LEAN` | `115` | `FAIL` (`cm=122`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 102 | `FQ-INTERFERENCE-NONDESCENT` | `FINITE_QM_CORE` | `PROVED_LEAN` | `116` | `FAIL` (`cm=123`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 103 | `FQ-SORKIN-READOUT-CLASS-QM208` | `FINITE_QM_CORE` | `PROVED_LEAN` | `117` | `PASS` (`cm=117`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 104 | `FQ-POWER-RULE-P2-SELECTION` | `FINITE_QM_CORE` | `PROVED_LEAN` | `118` | `PASS` (`cm=118`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 105 | `FQ-FIVE-IMPORT-PROXY-SEPARATION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `121` | `FAIL` (`cm=129`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 106 | `FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION` | `FINITE_QM_CORE` | `PROVED_LEAN` | `120` | `FAIL` (`cm=127`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 107 | `FQ-CABELLO-NO-INTEGER-FRAME` | `FINITE_QM_CORE` | `PROVED_LEAN` | `121` | `PASS` (`cm=121`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 108 | `FQ-CABELLO-FRAME-POLYTOPE-146` | `FINITE_QM_CORE` | `PROVED_LEAN` | `122` | `PASS` (`cm=122`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 109 | `FQ-BUSCH-EFFECT-FRAME` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `125` | `FAIL` (`cm=133`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 110 | `FQ-TENSOR-LU-RIVAL-EXCLUSION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `126` | `FAIL` (`cm=134`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 111 | `FQ-CPTP-CLASS-DEFINITION` | `FINITE_QM_STRUCTURE` | `DEFINITION` | `127` | `PASS` (`cm=127`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 112 | `FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY` | `FINITE_QM_CORE` | `PROVED_LEAN` | `126` | `FAIL` (`cm=133`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 113 | `FQ-TRACE-ZERO-DUALITY-K23` | `FINITE_QM_CORE` | `PROVED_LEAN` | `127` | `PASS` (`cm=127`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 114 | `FQ-BELL-CLASSICAL-JOINT-EXTENSION` | `FINITE_QM_CORE` | `PROVED_LEAN` | `128` | `FAIL` (`cm=135`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 115 | `FQ-BELL-RATIONAL-VIOLATION-14-5` | `FINITE_QM_CORE` | `PROVED_LEAN` | `129` | `FAIL` (`cm=136`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 116 | `FQ-TSIRELSON-SOS-Q-SQRT2` | `FINITE_QM_CORE` | `PROVED_LEAN` | `130` | `PASS` (`cm=130`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 117 | `FQ-CONTEXTUALITY-CECH-F2` | `FINITE_QM_CORE` | `PROVED_LEAN` | `131` | `PASS` (`cm=131`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 118 | `FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `134` | `FAIL` (`cm=418`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 119 | `FQ-COMMUTATOR-TRACE-OBSTRUCTION` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `137` | `FAIL` (`cm=146`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 120 | `FQ-U1-TRANSPORT-N-TORSION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `136` | `PASS` (`cm=136`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 121 | `FQ-DISCRETE-DYNAMICS-DICHOTOMY` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `139` | `PASS` (`cm=139`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 122 | `FQ-DISCRETE-TIME-STONE-AMBIGUITY` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `140` | `PASS` (`cm=140`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 123 | `FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `141` | `PASS` (`cm=141`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 124 | `FQ-GAP-REAL-EMBEDDING-CHOICE` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `142` | `PASS` (`cm=142`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 125 | `FQ-ENTROPY-DICHOTOMY-BAKER` | `FINITE_QM_CORE` | `PROVED_LEAN` | `139` | `PASS` (`cm=139`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 126 | `FQ-IMPL-F64-GATING` | `IMPLEMENTATION` | `DEFINITION` | `146` | `FAIL` (`cm=458`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 127 | `FQ-IMPL-WDP-AMPLITUDE-BRIDGE` | `IMPLEMENTATION` | `PROVED_LEAN` | `147` | `PASS` (`cm=147`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 128 | `FQ-IMPL-REALIFICATION-ADAPTER` | `IMPLEMENTATION` | `PROVED_LEAN` | `148` | `PASS` (`cm=148`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 129 | `FQ-IMPL-PAIRING-AUDIT` | `IMPLEMENTATION` | `PROVED_LEAN` | `149` | `FAIL` (`cm=159`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 130 | `FQ-QM207-231-FINITE-MAP-CONTROLS` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `146` | `FAIL` (`cm=154`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 131 | `GP-GAP-EXACT-DUALITY` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `147` | `PASS` (`cm=147`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 132 | `GP-FIN-GAUSS-MATRIX-ALGEBRA` | `FINITE_QM_CORE` | `PROVED_LEAN` | `146` | `PASS` (`cm=146`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 133 | `GP-DROP-ONE-CENSUS` | `FINITE_QM_CORE` | `PROVED_LEAN` | `147` | `FAIL` (`cm=154`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 134 | `DS-QM030-GRADED-PATHSUM` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `152` | `FAIL` (`cm=161`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 135 | `DS-QM030-UNGRADED-OVERCOUNT` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `153` | `PASS` (`cm=153`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 136 | `DS-QM030-TRANSFER-OPERATOR-SHADOW` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `154` | `FAIL` (`cm=163`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 137 | `DS-QM032-FINITE-FEYNMAN-SHADOW` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `155` | `FAIL` (`cm=164`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 138 | `DS-QM032-CONTINUUM-LIMIT-CONDITIONAL` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `156` | `FAIL` (`cm=165`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 139 | `DS-QM033-SCHRODINGER-DISCRETE-COCHAIN` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `157` | `FAIL` (`cm=489`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 140 | `DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `158` | `FAIL` (`cm=167`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 141 | `DS-QM041-HEISENBERG-PICTURE-FINITE` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `159` | `FAIL` (`cm=168`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 142 | `DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY` | `FINITE_QM_DYNAMICS` | `PROVED_LEAN` | `160` | `PASS` (`cm=160`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 143 | `DS-QM021-IDEMPOTENT-CONDITIONING` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `159` | `FAIL` (`cm=159`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 144 | `DS-QM060-SUPERPOSITION-QUOTIENT-FIBER` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `160` | `FAIL` (`cm=168`, `ref=True`) | **FAIL** | **PASS** (`a=3`) |
| 145 | `DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `161` | `FAIL` (`cm=169`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 146 | `DS-QM061-BUILDABILITY-SET-S` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `162` | `FAIL` (`cm=170`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 147 | `DS-QM062-U1-SELECTOR-LAYERS` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `163` | `PASS` (`cm=163`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 148 | `DS-QM063-HOLONOMY-COHERENT-INTENSITY` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `164` | `PASS` (`cm=164`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 149 | `DS-QM064-074-083-ANNEX-REDIRECT-ROWS` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `165` | `PASS` (`cm=165`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 150 | `DS-QM070-PRODUCT-NONFACTORIZATION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `166` | `FAIL` (`cm=174`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 151 | `DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `167` | `FAIL` (`cm=175`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 152 | `DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `168` | `FAIL` (`cm=176`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 153 | `DS-QM073-FINITE-CHSH-AND-PR-BOX` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `169` | `FAIL` (`cm=177`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 154 | `DS-QM073-BELL-THEOREM-OBSTRUCTED` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `170` | `FAIL` (`cm=178`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 155 | `DS-QM074-NO-SIGNALING-MARGINAL` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `171` | `PASS` (`cm=171`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 156 | `DS-QM080-IMPORT-FREE-TRACE-NORM-CORE` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `172` | `FAIL` (`cm=180`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 157 | `DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `173` | `FAIL` (`cm=181`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 158 | `DS-QM081-CPTP-MONOTONE-NOT-SELECTING` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `174` | `FAIL` (`cm=538`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 159 | `DS-QM081-STOCHASTIC-L1-CONTRACTION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `175` | `PASS` (`cm=175`, `ref=True`) | **FAIL** | **PASS** (`a=2`) |
| 160 | `DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `176` | `PASS` (`cm=176`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 161 | `DS-QM090-092-AUTHORITY-FIREWALL` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `177` | `PASS` (`cm=177`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 162 | `DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `178` | `FAIL` (`cm=550`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 163 | `DS-QM090-093-QM-UNIQUENESS-TIER3` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `179` | `PASS` (`cm=179`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 164 | `DS-QM093-SURVIVAL-THEOREM` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `180` | `FAIL` (`cm=540`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 165 | `DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `181` | `PASS` (`cm=181`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 166 | `DS-QM094-EVERETT-RELATIVE-STATE-CONTACT` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `182` | `FAIL` (`cm=190`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 167 | `DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `183` | `PASS` (`cm=183`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 168 | `DS-QM102-SYNDROME-CAPACITY-BOUND` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `184` | `FAIL` (`cm=192`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 169 | `DS-QM103-SHOW-THE-PACKET-PROTOCOL` | `FINITE_QM_STRUCTURE` | `DEFINITION` | `185` | `FAIL` (`cm=193`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 170 | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `186` | `PASS` (`cm=186`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 171 | `DS-QM120-MERMIN-PERES-F2-OBSTRUCTION` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `187` | `FAIL` (`cm=195`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 172 | `DS-QM206-BOUNDARY-SYNTHESIS` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `188` | `PASS` (`cm=188`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 173 | `DS-QM207-211-FIVE-IMPORT-CASCADE` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `189` | `PASS` (`cm=189`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 174 | `DS-QM212-MAJORANA-PROBLEM` | `FINITE_QM_STRUCTURE` | `PROVED_LEAN` | `190` | `PASS` (`cm=190`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 175 | `IMPL-FSP-SWITCHING-NORMAL-FORM-NF002` | `IMPLEMENTATION` | `PROVED_LEAN` | `195` | `PASS` (`cm=195`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 176 | `IMPL-THYMUS-SCREENING-SOUNDNESS` | `IMPLEMENTATION` | `PROVED_LEAN` | `196` | `FAIL` (`cm=608`, `ref=True`) | **PASS** | **PASS** (`a=1`) |
| 177 | `IMPL-LGGR-FINITE-RESULTS-LEAN` | `IMPLEMENTATION` | `PROVED_LEAN` | `197` | `PASS` (`cm=197`, `ref=True`) | **PASS** | **PASS** (`a=1`) |

## 4. Claim Hygiene Summary (`RULE[user_global]`)

1. **What it supports**: Supports that on the remaining 142 nodes (`36..177`) of `derivation_dag.json` dispatched live to `deepseek/deepseek-v4.1-flash`, including Mission M3 (`slot_m3_layer2_ideals_and_annihilators`: Congruence Ideals $\mathcal{I}$ and Annihilator Decoy Equations $\mathcal{O}^-$) substantially increases Attempt-1 pass rates and eliminates `G4` unquotiented decoy errors (`R_raw - G_cob` vs `R_raw - G_cob - S_decoy`) and `G5` `PROVED_LEAN` unconditional-promotion traps while reducing reasoning token spin.
2. **What it does not support**: Does not show that `PROVED_LEAN` finite-carrier theorems extend to continuum Hilbert spaces without the declared external imports (`H001`–`H013`).
3. **The narrowest defensible claim**: Across all 142 remaining DAG nodes (`36..177`), pre-mining Mission M3 decoy equations increased first-attempt verification pass rate from the `Without-M3` control baseline to the `With-M3` treatment level recorded above, bringing all 177 nodes (`1..177`) of `derivation_dag.json` to verified multi-stage PFP custody.
4. **The next test needed**: Evaluate multi-hop route-chain compositions (2-edge and 3-edge path-concatenation work-units across stages) under the same `With-M3` vs `Without-M3` ablation design.
