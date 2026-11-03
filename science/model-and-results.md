# Model and oracle-simulation theorem

A known, fixed, memoryless channel acting on the address **after** a Boolean bit query can be corrected well enough to simulate arbitrary coherent Boolean queries. If its Kraus rank is $`r`$, one ideal query can be simulated to unhalved diamond error $`\delta`$ using $`O(r^2\log(4/\delta))`$ physical noisy queries. The response register and the compiler's other workspace are protected.

The finer parameter is the affine dimension of the environment states produced by computational-basis addresses. A convex construction gives a balanced query code, and a circuit using protected response eigenstates preserves the unknown oracle action while leaving its address noise correctable. The full proofs are in [A balanced query code](convex-code.md) and [The oracle compiler](oracle-compiler.md).

## 1. The physical oracle and its accessible outputs

Let $`[N]=\{0,\ldots,N-1\}`$ and let $`f:[N]\to\{0,1\}`$ be unknown. The ideal bit oracle acts on a physical address register $`Q`$ and answer qubit $`A`$ as

```math
U_f\lvert x,a\rangle
=\lvert x,a\mathbin{\oplus}f(x)\rangle.
```

One physical noisy call is

```math
\mathcal N_f
=(\Phi_Q\otimes\operatorname{id}_A)\circ\operatorname{Ad}_{U_f},
\qquad
\operatorname{Ad}_U(\rho)=U\rho U^\dagger.
```

Here $`\Phi`$ is a known CPTP channel on $`\mathbb C^N`$, with equal input and output dimension. It is independent of $`f`$ and is the same channel on every call. Each use has a fresh environment, initially uncorrelated with the algorithm and other uses. The algorithm retains both the noisy address output and the answer; the environment is inaccessible.

All other registers and known operations are noiseless. In particular, the compiler can store a logical address, branch tags, answer qubits and already-queried address outputs in protected memory. It may route successive query registers through one physical oracle port using known swaps. The noise is incurred at the oracle invocation; the model does not add noise to stored outputs between calls.

The supplied access is the standard Boolean **bit** oracle. Preparing its answer in $`\lvert+\rangle`$ or $`\lvert-\rangle`$ is an allowed known operation. Every invocation still counts and still applies $`\Phi`$. A freely controlled extension of an unknown phase-only unitary, an inverse noisy channel, or access to the noise environment is not part of the construction.

Noise may act on all address qubits at once, and its Kraus operators may be noncommuting and nondiagonal. There is no locality or small-noise assumption within $`Q`$. The placement after the ideal query and the protection of the answer and workspace are essential to the proof.

## 2. Parameters and error convention

Use a Kraus representation of minimal size,

```math
\Phi(\rho)=\sum_{\alpha=1}^{r}K_\alpha\rho K_\alpha^\dagger,
\qquad
\sum_{\alpha=1}^{r}K_\alpha^\dagger K_\alpha=I.
```

The rank $`r`$ is the minimum Stinespring environment dimension. Define the complementary output states

```math
\sigma_x=\widehat\Phi(\lvert x\rangle\langle x\rvert),
\qquad
(\sigma_x)_{\alpha\beta}
=\langle x\rvert K_\beta^\dagger K_\alpha\lvert x\rangle,
```

and their real affine dimension

```math
d=\dim_{\mathbb R}\operatorname{aff}\{\sigma_x:x\in[N]\}
\leq\min\{N-1,r^2-1\}.
```

The generic construction uses $`d+1`$ anchors and a designated query weight

```math
\eta=\frac1{d+1}.
```

This dimension is unchanged by changing the minimal environment representation.

| Symbol | Meaning |
|---|---|
| $`X,Y`$ | Protected logical address and logical answer |
| $`Q_i,A_i`$ | Address and answer used by physical call $`i`$ |
| $`B_i`$ | Protected branch tag of probe $`i`$ |
| $`r`$ | Kraus rank of the known address channel |
| $`d`$ | Affine dimension of the states $`\sigma_x`$ |
| $`\eta`$ | Designated-address weight, $`1/(d+1)`$ for the generic code |
| $`L`$ | Physical noisy calls used for one simulated query |
| $`\delta`$ | Per-query unhalved diamond error |
| $`T`$ | Ideal queries in the algorithm being simulated |
| $`\epsilon`$ | Total unhalved diamond error after composition |

For a linear map $`\Lambda`$, the diamond norm is

```math
\|\Lambda\|_\diamond
=\sup_{k\geq1}\ \sup_{\|Z\|_1=1}
\left\|(\Lambda\otimes\operatorname{id}_k)(Z)\right\|_1.
```

We do not divide this norm by two. Two channels have diamond distance at most two. An output-channel error at most $`\epsilon`$ changes the probability of any final measurement event by at most $`\epsilon/2`$.

## 3. Universal coherent-query simulation

### Theorem 1

For every channel and access model described above, there are encoding, routing and recovery operations depending on $`\Phi`$ and $`L`$, but independent of $`f`$, whose induced channel $`\widetilde{\mathcal U}_{f,L}`$ on the protected logical registers satisfies

```math
\left\|
\widetilde{\mathcal U}_{f,L}
-\operatorname{Ad}_{U_f^{XY}}
\right\|_\diamond
\leq\min\left\{2,4(1-\eta)^{L/2}\right\}
\qquad\text{for every }f:[N]\to\{0,1\}.
```

The protocol makes exactly $`L`$ physical noisy bit queries. It is deterministic and retains every branch. The estimate applies to arbitrary inputs of $`XY`$, including entanglement with an unrestricted reference.

For $`d\geq1`$ and $`0<\delta\leq1`$, a sufficient call count is

```math
L=\left\lceil2(d+1)\ln\frac4\delta\right\rceil.
```

For $`d=0`$, a single physical query gives exact simulation. Thus the general overhead is

```math
O\left((d+1)\log\frac4\delta\right)
\leq O\left(r^2\log\frac4\delta\right).
```

The displayed ceiling gives an explicit count throughout the stated error interval.

### Proof structure

A maximum-volume simplex of the complementary states supplies nonnegative mixtures with the same environmental density operator and designated weight $`\eta`$ on every requested address. Protected branch tags make these mixtures valid error-correcting codes even for nondiagonal Kraus operators. Keeping the logical address in protected memory and decoding jointly with the retained probes gives a known exact recovery on the code.

Across $`L`$ probes, a reversible computation selects the first designated-address branch. Its paid bit query receives answer state $`\lvert-\rangle`$ when the protected logical payload requires phase kickback; all other responses receive $`\lvert+\rangle`$. The unknown logical phase is therefore applied whenever at least one designated branch occurs. Address noise on an already-queried probe commutes with all subsequent routing and query operations before recovery, which use protected registers or other probes. The entire physical noise can consequently be placed after this ideal routed action.

The no-match weight is $`(1-\eta)^L`$ for every logical address. Its square root bounds the error of the whole encoded isometry. Exact recovery and channel contractivity then give the stated diamond estimate. The [code proof](convex-code.md) and [compiler proof](oracle-compiler.md) establish each step, including the full bit-oracle wrappers and arbitrary-reference bound.

## 4. Simulation of query algorithms

### Corollary 2

An algorithm making at most $`T\geq1`$ ideal Boolean queries can be simulated within total unhalved diamond error $`0<\epsilon\leq1`$ using, for $`d\geq1`$,

```math
T\left\lceil2(d+1)\ln\frac{4T}\epsilon\right\rceil
=O\left((d+1)T\log\frac{4T}\epsilon\right)
```

physical noisy queries. For $`d=0`$, it can be simulated exactly with $`T`$ physical queries.

The algorithm may contain measurements, classical adaptive choices and protected quantum memory. Set the error of each simulated query to $`\delta=\epsilon/T`$ and replace queries one at a time. Each hybrid step contributes at most $`\delta`$ because the single-query theorem permits arbitrary reference correlations. Summing the steps proves the corollary.

For example, substituting the $`O(\sqrt N)`$ ideal query count of [Grover search](https://arxiv.org/abs/quant-ph/9605043) in the zero-or-one-mark setting gives

```math
O\left((d+1)\sqrt N\log N\right)
\leq O\left(r^2\sqrt N\log N\right)
```

physical queries at fixed final error. A computational-basis query can verify a proposed marked address exactly in its protected answer, and such a verification call must be counted. For bounded $`r`$, the construction preserves the quadratic search exponent up to a logarithm. Optimal dependence on $`r`$ and removal of the logarithmic overhead are not established here.

## 5. What the environment dimension does and does not say

The rank bound is a sufficient worst-case guarantee. The affine geometry can be substantially more informative than $`r`$ alone.

When $`r=1`$, the noise is a known unitary channel and can be undone directly. More generally, $`d=0`$ means that all computational-basis addresses give the same environmental state, and the tagged-copy code gives exact one-call simulation even for a channel of larger Kraus rank.

For a concrete limiting case, let $`\lvert\widetilde k\rangle`$ be the discrete Fourier basis and consider complete dephasing in that basis:

```math
\Phi(\rho)
=\sum_{k=0}^{N-1}
\lvert\widetilde k\rangle\langle\widetilde k\rvert
\rho
\lvert\widetilde k\rangle\langle\widetilde k\rvert.
```

Its Kraus rank is $`N`$, but $`\sigma_x=I_N/N`$ for every computational-basis address. Hence $`d=0`$ and the theorem gives exact one-call simulation. This example also emphasizes that the address output is retained: its error syndrome remains available for the known recovery.

The theorem therefore does not classify noisy-query difficulty by Kraus rank alone. It gives a rank-controlled construction through the more detailed set of complementary states.

## 6. Resource accounting and implementation precision

**Known-channel preprocessing.** The channel description is supplied independently of the unknown function. Selecting a maximum-volume simplex, computing its barycentric coordinates and diagonalizing the common error Gram matrix use this description. These operations make no queries to $`f`$, but their classical cost can grow substantially with $`N`$ and $`d`$. No calibration algorithm or generic polynomial-in-$`\log N`$ preprocessing bound is assumed.

**Protected quantum memory.** The code uses one protected logical address and $`L`$ physical address registers, each with a protected tag of dimension $`d+2`$. Including response and selector registers, the construction has register width

```math
O\left(\log N+L\bigl(\log N+\log(d+2)\bigr)\right)
```

qubits, before additional workspace chosen by a particular gate-synthesis method. Already-queried addresses are stored until recovery. Generic decoding is a controlled known unitary followed by discarding a syndrome. If an implementation forbids resets or discards, those syndrome records must be retained and their accumulated storage charged.

**Known gates.** A finite-dimensional controlled encoder and recovery exist for every supplied channel, but this alone does not give an efficient gate decomposition. The abstract result is a query-complexity theorem. A computational-time speedup additionally requires efficient coherent preparation and recovery for the chosen channel family.

**Precision and model error.** The theorem first treats the specified channel and known controls exactly. Standard hybrid bounds account for implementation errors. If every actual physical query differs from its modeled channel by unhalved diamond distance at most $`\zeta`$, a subroutine making $`L`$ calls incurs at most $`L\zeta`$ additional error. Errors of known gates can be added in the same way. Over an entire compiled algorithm, the precision budget scales with the total number of physical calls and implemented gates. The theorem does not promise tolerance of a fixed unknown calibration error as the computation grows.

## 7. Relation to the underlying methods

The weak-query and error-correction approach is developed in [Ruohan Shen and Soonwon Choi, *Oracle Distillation*](https://arxiv.org/abs/2609.31596). Exact recovery uses the standard [Knill–Laflamme conditions](https://doi.org/10.1103/PhysRevA.55.900), and the maximum-volume simplex argument is classical convex geometry. The present account makes explicit the designated-address mixture and response-routing construction that yields a guarantee for an arbitrary known finite-rank channel in the stated post-query address model.

The scope is the full coherent Boolean-query simulation theorem. It does not transfer automatically to pre-query noise, answer noise, temporally correlated environments, an unknown channel, or an uncontrolled phase-only oracle. Those access and noise contracts require separate arguments.
