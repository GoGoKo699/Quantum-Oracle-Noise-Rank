# An efficient two-branch phase-gradient example

This family makes the query compiler explicit at the circuit level. It uses one protected tag qubit per probe, reversible address arithmetic, and a two-outcome syndrome decoder. It needs no table of address-dependent amplitudes, no QRAM, and no search for a simplex.

The noise has fixed nonzero strength and global support, but is known and acts only on the address after each supplied Boolean bit query. The response and other workspace remain protected.

## 1. Channel and encoded probe

Let $`N=2^n`$ with $`n\ge2`$. Define the known diagonal unitary and channel

```math
Z|x\rangle=e^{i\theta_x}|x\rangle,
\qquad
\theta_x=\frac{2\pi x}{N},
\qquad
\Phi(\rho)=\frac12 Z\rho Z^\dagger+
\frac12 Z^\dagger\rho Z.
```

One fresh fair sign is drawn independently on each call. This is a rank-two correlated phase channel. It is not independent noise on the individual address qubits.

A Stinespring representation has environment vector

```math
|e_x\rangle
=\frac{e^{i\theta_x}|+\rangle_E+
e^{-i\theta_x}|-\rangle_E}{\sqrt2}.
```

Put $`h=N/4`$ and use the protected tag/address state

```math
|\Theta_x\rangle_{BQ}
=\frac{|0\rangle_B|x\rangle_Q+
|1\rangle_B|x+h\bmod N\rangle_Q}{\sqrt2}.
```

The two environment vectors are orthogonal:

```math
\langle e_x|e_{x+h}\rangle
=\cos(\theta_{x+h}-\theta_x)=0.
```

Tracing the protected tag therefore gives the same complementary output for every logical address:

```math
\frac12|e_x\rangle\langle e_x|
+\frac12|e_{x+h}\rangle\langle e_{x+h}|
=\frac{I_E}{2}.
```

The tag-zero branch is the distinguished query with probability $`\eta=1/2`$. The alternate address may itself be marked. Its response is prepared in $`|+\rangle`$, so its unknown Boolean value contributes no phase and does not need to be learned.

This channel completely removes the coherence between $`|x\rangle`$ and $`|x+h\rangle`$. For example, it maps their balanced superposition to the incoherent equal mixture. Thus the construction does not require the full-register channel to approach the identity as $`N`$ grows. The largest coordinate subspaces on which the two error unitaries are proportional have dimension two: equality of environment rays identifies only $`x`$ and $`x+N/2`$. No extensive noiseless address block is used.

## 2. Preparation using elementary reversible gates

Keep the logical address in a protected $`n`$-qubit register $`X`$. Initialize $`B`$ and $`Q`$ to zero.

1. Apply $`H_B`$.
2. Copy the computational-basis label from $`X`$ to $`Q`$ using $`n`$ CNOTs.
3. Add $`Bh`$ modulo $`N`$ to $`Q`$.

The second step is a controlled encoding of a basis label. On a superposition it creates entanglement; it does not create two independent copies of an unknown quantum state.

For $`N=2^n`$, adding $`h=2^{n-2}`$ changes only the two highest address bits. Number bits from $`0`$ at the least significant position. A controlled addition is exactly the following two gates, in this order:

```text
Toffoli(B, Q[n-2]; target Q[n-1])
CNOT(B; target Q[n-2])
```

The Toffoli propagates the old low bit of this two-bit block as the carry; the CNOT then flips that bit. Lower address bits are unchanged. Reversing these two gates performs controlled subtraction. After this subtraction, copying $`X`$ into $`Q`$ again returns a correctly encoded address to zero.

Preparation and address uncomputation each cost $`n+O(1)`$ elementary reversible gates per probe.

## 3. Exact syndrome recovery

First consider the correctable code before the weak oracle phase. Conditional on a physical error $`Z_Q^s`$, where $`s\in\{+1,-1\}`$,

```math
Z_Q^s|\Theta_x\rangle
=e^{is\theta_x}
\frac{|0\rangle|x\rangle+
is\,|1\rangle|x+h\bmod N\rangle}{\sqrt2}.
```

Undo the controlled address addition and then the computational-basis copy. The address returns to zero, leaving

```math
Z_X^s|x\rangle_X\otimes|y_s\rangle_B\otimes|0\rangle_Q,
\qquad
|y_s\rangle=\frac{|0\rangle+is|1\rangle}{\sqrt2}.
```

Let $`S=\operatorname{diag}(1,i)`$. The known decoder $`H S^\dagger`$ on the tag sends

```math
|y_{+1}\rangle\longmapsto|0\rangle,
\qquad
|y_{-1}\rangle\longmapsto|1\rangle.
```

If the decoded tag is $`b`$, then $`s=(-1)^b`$. Apply the known logical correction $`Z_X^{-s}`$. It restores the logical state exactly and leaves the tag recording the syndrome. The decoder can be coherent throughout; measuring the syndrome and applying classical feedforward is optional.

This proves exact correction on every logical input, including arbitrary references. It also explicitly fixes the recovery outside the code-error span, which is needed when applying it to a weak-query state.

The same circuit is used after the first-match oracle operation. In that case the discarded syndrome can depend slightly on the logical state, producing the quantified compiler error. Independence of the syndrome is asserted for the exactly correctable code, not for every state in the larger physical space.

### Gate decomposition of the correction

Write the protected logical address as $`x=\sum_{k=0}^{n-1}2^k x_k`$ and define $`P(\varphi)=\operatorname{diag}(1,e^{i\varphi})`$. Then

```math
Z_X=\bigotimes_{k=0}^{n-1}P(2\pi\,2^{k-n}).
```

The syndrome-controlled correction can be implemented as an unconditional $`Z_X^\dagger`$, followed by $`Z_X^2`$ controlled on $`b=1`$:

```math
Z_X^{-(-1)^b}=Z_X^\dagger(Z_X^2)^b.
```

It uses $`O(n)`$ known one-qubit phase gates and controlled phase gates. Each controlled phase can be decomposed into two CNOTs and three one-qubit phase gates. For control $`c`$ and target $`t`$,

```math
\operatorname{CP}(\varphi)
=P_c(\varphi/2)P_t(\varphi/2)\,
\operatorname{CNOT}_{c,t}\,
P_t(-\varphi/2)\,
\operatorname{CNOT}_{c,t}.
```

Here operator products act right to left; the two outside phase gates commute. This identity includes the relative controlled phase explicitly and does not discard a phase that becomes observable under control.

## 4. First-match circuit for the full Boolean bit oracle

Prepare $`L`$ copies of the two-branch code. From their protected tags $`b_1,\ldots,b_L`$, compute prefix bits

```math
p_0=1,\qquad p_i=p_{i-1}b_i,
\qquad s_i=p_{i-1}(1-b_i).
```

The selectors $`s_i`$ are mutually exclusive and identify the first tag equal to zero. Both the prefix bits and selectors can be computed and later uncomputed with $`O(L)`$ Toffoli/CNOT gates and $`O(L)`$ clean protected bits. Negative controls can be implemented with exact $`X`$ gates.

For the full bit query on protected $`X,Y`$:

1. Apply $`H_Y`$.
2. For probe $`i`$, prepare a fresh or reused physical response $`A`$ in $`|+\rangle`$ and apply a controlled-controlled $`Z`$ using $`s_i,Y`$ as controls. It becomes $`|-\rangle`$ exactly when $`s_i=Y=1`$.
3. Call the supplied noisy bit oracle once on $`Q_i,A`$.
4. Reverse the response preparation, returning $`A`$ to zero.
5. After all probes, uncompute the selectors and prefix workspace.
6. Apply the syndrome recovery of Section 3 to every probe, discard the decoded syndrome tags, and apply $`H_Y`$ again.

The selector workspace must be uncomputed before the tag recovery changes the tags. The response can be reused because its known unpreparation is exact in the ideal control model, even though its queried address has already suffered noise. The logical target is never measured.

When at least one distinguished branch is present, exactly one response receives the phase determined by $`f(x)`$. If no distinguished branch is present, every physical response is $`|+\rangle`$ and the operation is idle. Hence

```math
q=2^{-L}.
```

The full logical bit-query diamond error is at most $`4\,2^{-L/2}`$. For a unique mark, the logical channel is exactly $`(1-2^{-L})\operatorname{Ad}_{U_w}+2^{-L}\operatorname{id}`$, as proved in [Search and resources](search-and-resources.md).

## 5. Gate count, width, and resets

Before synthesizing arbitrary known rotations into a finite gate set, one compiled query has the following resources.

| Resource | Cost | What is included |
|---|---:|---|
| Noisy physical bit queries | $`L`$ | One call per probe; no oracle uncomputation |
| Known elementary gates | $`O(nL)`$ | Probe preparation, first-match logic, response routing, address uncomputation, syndrome decoding, and correction |
| Protected workspace | $`O(nL)`$ qubits | Stored query outputs, tags, prefix/selector bits, and temporary response; algorithm workspace is additional |
| Discarded/reset syndrome bits | $`L`$ per compiled call | Enables the stated workspace to be reused |
| Noise-dependent data table | None | The shift and phases are computed from the fixed formula |

If a designated physical query port is required, two $`n`$-qubit swaps per probe add $`O(nL)`$ known gates and one $`n`$-qubit port. This does not change the asymptotic bounds. All already queried outputs are protected while waiting for recovery.

No large arithmetic subroutine is hidden in these counts: the address shift uses two elementary gates, and the rotation angles are binary fractions of $`2\pi`$. On the actual weak-query state, the inverse address arithmetic still returns every address register to zero because the phase channel has not changed its computational-basis address. Tags may remain correlated with the logical system and are discarded as part of the recovery channel.

If discarding and resetting are disallowed, retaining all syndrome tags over $`T`$ logical calls adds $`O(TL)`$ protected qubits. The reusable-width claim explicitly allows those standard channel operations.

## 6. Finite precision and noise-model mismatch

Suppose the target algorithm makes $`T`$ logical queries and the desired total channel error is $`\epsilon`$. Allocate one third of the error to the weak-query approximation, one third to known-control synthesis, and one third to channel mismatch. A sufficient choice is

```math
L=\left\lceil2\log_2(12T/\epsilon)\right\rceil.
```

Then $`4T\,2^{-L/2}\le\epsilon/3`$. Let $`G\le CnL`$ bound the number of known gates requiring approximation in one compiled query, for a fixed implementation constant $`C`$. After decomposing controlled phases into CNOTs and ordinary one-qubit phase gates as above, it suffices to approximate each such elementary unitary in operator norm, up to an overall phase, to

```math
\zeta\le\frac{\epsilon}{6TG}.
```

The known-control contribution is then at most $`2TG\zeta\le\epsilon/3`$. The overall phase of each unconditionally applied elementary gate is irrelevant to its channel; the relative phases of controlled operations are retained by their explicit decomposition. This requires $`O(\log(TnL/\epsilon))`$ bits of angular precision. Single-qubit phase errors obey $`\|P(\varphi+\Delta)-P(\varphi)\|\le|\Delta|`$.

A fixed finite universal gate set can approximate the required one-qubit rotations with a number of gates polynomial in $`\log(1/\zeta)`$; the constructive Solovay–Kitaev result [1] is sufficient. Exact Clifford and Toffoli components have constant-size decompositions in a suitable fixed universal set. Consequently the compiled known-gate count is

```math
O\!\left(
TnL\;\operatorname{polylog}\frac{TnL}{\epsilon}
\right).
```

No optimal rotation-synthesis exponent or hardware noise threshold is claimed here.

For a channel implemented with $`\|\Phi_{\rm actual}-\Phi\|_\diamond\le\delta_\Phi`$, the additional error is at most $`TL\delta_\Phi`$. The third allocation is satisfied by

```math
\delta_\Phi\le\frac{\epsilon}{3TL}.
```

As a concrete sufficient condition, suppose the actual random unitaries use phases $`\widetilde\theta_x`$ satisfying $`\sup_x|\widetilde\theta_x-\theta_x|\le\kappa`$ with the same mixture convention. Then

```math
\|\widetilde Z-Z\|\le\kappa,
\qquad
\|\widetilde\Phi-\Phi\|_\diamond\le2\kappa.
```

Thus $`\kappa\le\epsilon/(6TL)`$ suffices for this conservative budget. This statement assumes that such a uniform model-error bound has been supplied; it does not provide a free calibration procedure.

The decoder has common Gram eigenvalues exactly $`1/2`$. Its implementation does not require inversion of a small singular value or evaluation of an address-dependent recovery table. This distinguishes its explicit precision accounting from the generic existence construction.

## 7. End-to-end search cost

At fixed final error, a Grover search has $`T=O(\sqrt N)`$, $`n=\log_2N`$, and $`L=O(\log N)`$. The construction therefore uses

```math
\begin{aligned}
\text{noisy queries} &:\quad O(\sqrt N\log N),\\
\text{known gates before finite-set synthesis} &:\quad
O(\sqrt N\log^2N),\\
\text{known gates after finite-set synthesis} &:\quad
\sqrt N\,\operatorname{polylog}N,\\
\text{reusable protected width} &:\quad O(\log^2N).
\end{aligned}
```

The search diffusion operators and state preparation have polylogarithmic known-gate cost per iteration and fit within this bound. One additional physical basis query verifies the measured candidate exactly. The result is an explicit end-to-end sublinear-query and sublinear-gate construction in the stated oracle model, with the cost of implementing the physical oracle itself treated as an oracle call.

The result does not assert that every arbitrary rank-two channel has an efficient gate implementation. Nor does it cover noise on the protected target, stored workspace, or a temporally correlated environment. The generic theorem supplies the rank-dependent query guarantee; this channel supplies a concrete efficient realization.

## Reference

1. C. M. Dawson and M. A. Nielsen, “The Solovay–Kitaev algorithm,” *Quantum Information & Computation* **6**, 81–95 (2006). [Primary paper](https://arxiv.org/abs/quant-ph/0505030); [published version](https://doi.org/10.26421/QIC6.1-6).
