# Derivation Control: SG-48

**AuthorityEffect:** None.

## Scope and Claim

This finite control (`SG-48`) executes a two-episode operator-discovery and reuse loop over the 3-element carrier $T = \{a, b, c\}$ starting from registry $\mathcal{R}_0 = \{\mathrm{id}, \mathrm{swap}_{ab}\}$:

1. **Episode 1 (`task_1: a -> c`, `task_2` Sealed)**:
   - Under $\mathcal{R}_0$, $\operatorname{Reach}_{\mathcal{R}_0}(a) = \{a, b\} \not\ni c$, recording a finite reachability gap.
   - Candidate operator $\mathrm{swap}_{bc}: (a \mapsto a, b \mapsto c, c \mapsto b)$ is checked by the Stage 5 host verifier for totality, bijection, and involution across all of $T$, admitted into $\mathcal{R}_1 = \mathcal{R}_0 \cup \{\mathrm{swap}_{bc}\}$, and composed as $\mathrm{swap}_{bc}(\mathrm{swap}_{ab}(a)) = c$.
2. **Episode 2 (`task_2: b -> c`, Unsealed After Admission)**:
   - Unsealed only after Episode 1 Stage 5 admission, reusing $\mathrm{swap}_{bc} \in \mathcal{R}_1$ to map $b \mapsto c$ with a distinct problem-bound receipt (`episode_2_task_2`).
3. **Adversarial & Refusal Controls**:
   - Using $\mathrm{swap}_{bc}$ prior to Stage 5 verification, replaying Episode 1's receipt for Episode 2, mutating the task target, unsealing `task_2` early, or proposing a non-involution (`MetaLift` / collapsing map) is refused.

## Non-Claims

- This finite control does not claim open-ended synthesis over infinite carrier sets or paid external model invocation.
