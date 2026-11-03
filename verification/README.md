# Reproducible finite-channel checks

The verification program checks the circuit identities used by the proofs, including the full Boolean bit oracle on a target entangled with a reference. It is a finite-dimensional numerical audit, not a proof of the asymptotic theorem or an estimate of its worst-case diamond norm.

## Run

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python verification/verify.py --check
```

The only third-party dependency is pinned in [requirements.txt](../requirements.txt): NumPy 2.3.5. The reference output was generated with CPython 3.12.14. The program uses no network, quantum SDK, optimization solver, or external dataset.

Expected success output:

```text
PASS: 9 scoped channel checks, 3 noise fixtures, complete full-bit Choi checks.
All invariant residuals satisfy 2e-10; committed numerical output agrees within tolerance.
```

To inspect a newly computed report without modifying the committed reference:

```sh
.venv/bin/python verification/verify.py
```

The full reference report is [expected-results.json](expected-results.json). The check command compares its structure and discrete parameters exactly and its floating-point values with absolute and relative tolerance $`5\times10^{-9}`$. Independently of that comparison, each run enforces the circuit and channel identities at tolerance $`2\times10^{-10}`$. Small negative Choi eigenvalues at rounding scale are permitted.

## What is simulated

For every logical input column and every physical Kraus trajectory, the program applies:

1. The protected-target Hadamard when testing the full bit oracle.
2. Physical-response preparation controlled on the protected target and first distinguished tag.
3. The actual bit-oracle permutation $`U_f`$.
4. A possibly non-diagonal address Kraus operator immediately after that query.
5. The physical-response unpreparation.
6. The controlled recovery and final protected-target Hadamard.

The program separately constructs the ideal first-match phase followed by all address noise and compares it with the physical sequence. It checks the probability of any response failing to return to zero before excluding those response registers from subsequent calculations.

The recovery is obtained either from the common error Gram matrix or, for the phase-gradient family, from the explicit reversible address circuit, $`Y`$-basis syndrome decoder, and logical correction. General recovery matrices are completed deterministically on their orthogonal complements. The fixtures have well-separated nonzero Gram eigenvalues, so this check is not a test of a generic ill-conditioned numerical recovery.

## The three fixtures and their purpose

| Fixture | Consequential issue checked |
|---|---|
| Five-level globally rotated amplitude damping, Kraus rank two | Non-diagonal post-query noise, complex noncommuting complementary states, four simplex anchors plus a nonanchor, and a negative barycentric coefficient |
| Generic global rank-two channel from an $`8\times4`$ Stinespring isometry | Recovery and routing without amplitude-damping or diagonal structure |
| Two-branch phase-gradient code | The circuit-derived syndrome recovery and $`q=2^{-L}`$ logical channel; an additional eight-address decoder check exercises nontrivial phase angles |

The random fixtures use fixed seeds and canonicalized QR factors. They are generated locally from the documented formulas. The first fixture's minimum barycentric coefficient is approximately $`-0.613`$, and its complementary states do not commute. The program requires both properties, so a changed fixture cannot silently reduce the intended test to a classical or convex-interior special case.

The nine channel cases cover a marked anchor, a marked nonanchor, full bit oracles with one and several marked addresses, and the explicit structured code. Their small sizes were chosen to permit exact enumeration of every Kraus trajectory and every logical matrix element.

## Full bit-oracle and reference-entanglement checks

For logical dimension $`D=2N`$, the simulator constructs a complete Kraus tensor $`K_{o,i,e}`$. The environment index $`e`$ includes both the physical channel's Kraus label and the discarded recovery syndrome. The same environment indices are shared across all logical input columns; this retains every address and target coherence.

The normalized Choi matrix is

```math
J=\frac1D\sum_e
|\operatorname{vec}K_e\rangle
\langle\operatorname{vec}K_e|.
```

Equivalently, it is the output on the maximally entangled state between the complete logical address-target system and a $`D`$-dimensional reference. In particular, the logical target is entangled with its reference copy. Agreement of this whole matrix establishes agreement of the finite channels, rather than merely agreement on computational-basis inputs or a target initialized to $`|-\rangle`$.

For a unique mark the program compares the entire Choi matrix against

```math
(1-q)J(\operatorname{Ad}_{U_w})
+qJ(\operatorname{id}),
\qquad q=(1-\eta)^L.
```

For all tested Boolean functions, it also checks exact preservation of a target in $`|+\rangle`$ while the logical address is maximally entangled with a separate reference. The protected target makes the ideal bit oracle idle on this subspace, so the check exercises exact code recovery and target controls together.

The report includes complete positivity, trace preservation, the exact unique-mark residual, and the trace-norm difference between the normalized Choi matrix and the ideal one. **The reported Choi trace norm is not the diamond norm.** The diamond-norm bound is supplied by the analytic isometry proof in [Search and resources](../science/search-and-resources.md).

## Scope

These checks target the points at which an incorrect circuit can invalidate the argument: moving noncommuting noise to the end, protecting response coherence, aligning recovery syndromes, handling anchor collisions, and applying the target-Hadamard wrappers. They do not estimate large-system runtime, certify optimal dependence on Kraus rank, validate unknown-noise calibration, or replace the proofs of the simplex lemma and the uniform reference-system error bound.
