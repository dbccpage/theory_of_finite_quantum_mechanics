# Video Storyboard: Lesson 700.02: The Witness Function and Outcome Monad

AuthorityEffect: None.

**Target Duration:** `120s`  
**Format:** 1080p 60fps / 940x580 Dark-Mode Canvas  
**Voiceover Style:** Concise, mathematically precise, zero hype. Ready for spoken voiceover recording.

---

## Scene Breakdown

| Scene | Timestamp | Visual Cue / On-Screen Action | Voiceover Script | Epistemic Target |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `0:00 - 0:30` | Visual flow diagram illustrating an operation mapping input to an explicit pair `(output, witness)`. | "Welcome to Lesson 700.02. In the Witnessed Difference Programme, an operation does not confer authority; it yields an explicit witness record." | `[Declared]` |
| **02** | `0:30 - 1:00` | Code editor highlighting the `Outcome[T]` type with `Accepted` and `Refused` variants. | "Computations return through an explicit Outcome monad. Valid results are wrapped with zero authority effect, while failures yield typed refusal codes." | `[Executed]` |
| **03** | `1:00 - 1:30` | Terminal executing the safe division probe with zero-division input. | "Adversarial inputs are intercepted before unhandled exceptions occur. The host fails closed into an immutable refusal code." | `[Tested]` |
| **04** | `1:30 - 2:00` | Summary view of the nonclaim rule and link to the companion notebook. | "Open the companion laboratory notebook to execute environment preflights and verify the outcome monad invariants." | `[Pinned]` |

---

## Technical Recording Notes
1. Render accompanying diagram SVG in dark-mode (940x580) before live capture.
2. Execute notebook code cells live in terminal or headless environment to capture exact stdout.
3. Adhere strictly to the voiceover script pacing (120s target).
