# Video Storyboard: Lesson 720: 11 Linear Sensing Projection Walkthrough

AuthorityEffect: None.

**Target Duration:** `120s`  
**Format:** 1080p 60fps / 940x580 Dark-Mode Canvas  
**Voiceover Style:** Concise, mathematically precise, zero hype. Ready for spoken voiceover recording.

---

## Scene Breakdown

| Scene | Timestamp | Visual Cue / On-Screen Action | Voiceover Script | Epistemic Target |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `0:00 - 0:30` | `006_oewdp` `level_11_linear_sensing_projection.md` is Chapter 12. The filename says linear sensing. The level is the observation ladder. `classify_observation` promotes only after the ladder checks. Any authority effect is `CLAIM_STATUS_FIREWALL`. The bout stays in `woland_stage` on `018_oeos`. | "OEWDP lesson 720.11 is five observation events, not a sensing projection. Interaction, registration, typed witness, re-comparison, and evaluator acceptance stay separate. A receipt records an attempt. Only a verified receipt with Accept is an accepted observation. Refusal, rejection, and undetermined are not one no. Acceptance is not authority and not a measurement. This is not an OEPFP residual or an OEEIS admission. The bout stays in OEWOLAND. Host effects stay on OEOS." | `[Declared]` |
| **02** | `0:30 - 1:00` | Code editor highlighting key data structures and function calls. | "We examine the discrete carrier structures and transformation rules governing this stage." | `[Executed]` |
| **03** | `1:00 - 1:30` | Terminal output executing the falsifier test and counterexample assertions. | "We verify fail-closed boundary assertions against invalid inputs." | `[Tested]` |
| **04** | `1:30 - 2:00` | Summary view linking concept page to companion laboratory notebook. | "Launch the companion laboratory notebook to execute environment preflights and verify assertions." | `[Pinned]` |

---

## Joint route

Scene 01 names the ladder. This section names the typed folders. `AuthorityEffect: None`. The lesson source is [`level_11_linear_sensing_projection.md`](../../../levels/level_11_linear_sensing_projection.md). The descent it follows is [`lesson_720_10_observation_measurement_calibration.md`](lesson_720_10_observation_measurement_calibration.md). The concept page calls the ladder Raw, Filtered, Feature, Classification, Decision, and puts a projection matrix on it ([`lesson_720_11_linear_sensing_projection.md`](../concepts/lesson_720_11_linear_sensing_projection.md)). Chapter 12 does not. Measurement is Level 12 ([`level_12_context_interference_state_spaces.md`](../../../levels/level_12_context_interference_state_spaces.md)).

**OEWDP** (`006_oewdp/`) keeps the ladder in that level file. `WDP-CH12-D01` is the receipt $\mathsf{Obs}=(i,g,w,m,e)$: interaction, registration, typed witness, re-comparison, and evaluator result. An accepted E-observation needs the first four predicates and $e=\mathsf{Accept}$. §12.2 names eight stops: no coupling, no registration, misregistration, no retention, profile drift, evaluator refusal, evaluator rejection, and undetermined. `WDP-CH12-P01` says `ObservationAccept` does not imply `AuthStanding` or `Promote`. No coercion into those types is defined.

[`classify_observation`](../../../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/observation.py) returns an `AcceptedObservation` only after the ladder checks pass. The first failed check is the refusal: `NO_INTERACTION`, `NO_REGISTRATION`, `COUPLING_MISMATCH`, `NO_WITNESS`, `DIGEST_MISMATCH`, `NO_ACCEPTING_EVALUATOR`, `NON_ACCEPTING_STANDING`, or `EVALUATOR_MISMATCH`. `Reject`, `Refuse`, and `Undetermined` share `NO_ACCEPTING_EVALUATOR`; the status stays on the receipt. There is no profile-drift code. Constructing a receipt or accepted observation with an authority effect other than `AuthorityEffect.NONE` raises `ValueError`. A field altered after construction is `CLAIM_STATUS_FIREWALL`.

1. **OEPFP** (`004_oepfp/`) measures. A ladder refusal is not a residual. **OEEIS** (`009_oeeis/`) admits ([`lesson_520_09_external_admission_boundary.md`](../../../../009_oeeis/curriculum/520_eis_levels/scripts/lesson_520_09_external_admission_boundary.md)). This receipt is not that admission.
2. **OEWAS** (`008_oeop/`) compiles the plan ([`lesson_900_01_was_operadic_foundations.md`](../../../../008_oeop/curriculum/900_was_operad_foundations/scripts/lesson_900_01_was_operadic_foundations.md)). **OEWOLAND** (`011_oewoland/`) runs the bout ([`lesson_1200_01_woland_dialectic_architecture.md`](../../../../011_oewoland/curriculum/1200_woland_retinue_swarm_foundations/scripts/lesson_1200_01_woland_dialectic_architecture.md)). An accepted observation is not the bout. **OEPCIV** does not own this chapter.
3. The bout occurs in **OEWOLAND** ([`woland_stage/README.md`](../../../../woland_stage/README.md)). **OEOS** implements `HostPortV1` under that arena ([`018_oeos/README.md`](../../../../018_oeos/README.md)). the city production modules do not import the operating system. Evaluator acceptance is not that port.

## Technical Recording Notes
1. Render accompanying diagram SVG in dark-mode (940x580) before live capture.
2. Execute notebook code cells live in terminal or headless environment to capture exact stdout.
3. Adhere strictly to the voiceover script pacing (120s target).
