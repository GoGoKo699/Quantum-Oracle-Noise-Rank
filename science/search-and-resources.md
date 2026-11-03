# Search, algorithm composition, and resource accounting

This note derives the search consequence of the oracle compiler and separates query complexity from the cost of implementing its known controls. The [structured example](structured-example.md) supplies an explicit circuit with polylogarithmic overhead in the address-space size.

Throughout, the supplied physical query is

```math
\mathcal N_f=(\Phi_Q\otimes\mathrm{id}_A)\circ\mathrm{Ad}_{U_f},
\qquad
U_f|z,b\rangle=|z,b\oplus f(z)\rangle.
```

The address channel $`\Phi`$ is fixed, known, independent of $`f`$, and memoryless. It acts after the ideal query. Responses and other algorithm registers are protected. All channel distances below use the diamond norm without a factor of one half; the distance between two channels is at most two.

## 1. The compiled query as an isometry

The tagged code assigns a normalized state $`|\Theta_x\rangle`$ to each protected logical address $`x`$. Its distinguished tag has the same probability $`\eta>0`$ for every address. For the maximum-volume-simplex construction,

```math
\eta=\frac1m,\qquad m=d+1\le r^2,
```

where $`d`$ is the real affine dimension of the basis-state complementary outputs and $`r`$ is the supplied channel's Kraus rank. A structured code can have a larger $`\eta`$ than this general guarantee.

Use $`L`$ probes, with encoding

```math
V_L|x\rangle=|x\rangle|\Theta_x\rangle^{\otimes L}.
```

Let $`P_{\rm miss}`$ project onto the tag strings with no distinguished tag. The constant distinguished weight gives

```math
V_L^\dagger P_{\rm miss}V_L=qI,
\qquad q=(1-\eta)^L.
```

The first-match response routing uses exactly one physical bit query per probe. On the first distinguished tag it prepares the physical response in $`|-\rangle`$; on every other branch it prepares $`|+\rangle`$. With a protected logical target, the selection is additionally controlled on that target. Each response is unprepared with known gates after its query.

All operations following a query act on protected registers or other probes until final recovery. Consequently its post-query address noise can be moved to the end of the ideal routing circuit. This statement never commutes an arbitrary address channel through the unknown oracle acting on the same register.

For a logical phase oracle $`O_f|x\rangle=(-1)^{f(x)}|x\rangle`$, the ideal routed isometry is

```math
W_f=(I-P_{\rm miss})V_LO_f+P_{\rm miss}V_L.
```

For the full bit oracle, first conjugate the protected target $`Y`$ by a Hadamard. In this basis the desired unitary is

```math
C_f|x,t\rangle=(-1)^{t f(x)}|x,t\rangle.
```

The same expression for $`W_f`$ holds with $`C_f`$ and with $`V_L`$ acting trivially on $`Y`$. A final target Hadamard returns to the bit-query basis. These are paid bit-oracle calls and known response preparations; no controlled extension of an unknown phase-only oracle is assumed.

## 2. Exact logical channel for a unique marked address

Assume $`f(x)=\mathbf 1[x=w]`$. Choose the explicit controlled recovery that aligns the error syndromes for all logical labels. Include the physical environment and recovered syndrome in a Stinespring description. On the exactly correctable code, this gives isometries $`A_x`$ and one normalized state $`|s\rangle`$ such that

```math
A_x|\Theta_x\rangle^{\otimes L}=|s\rangle
\quad\text{for every }x.
```

The common state is a purification of the fixed complementary output. Its independence of $`x`$ follows from the common error Gram matrix and the chosen controlled recovery. The isometry $`A_x`$ also has an arbitrary fixed extension outside the code-error span.

Every unmarked logical address undergoes no ideal routed phase and therefore produces the same syndrome $`|s\rangle`$. The marked branch produces

```math
-|s\rangle+2|t_w\rangle,
\qquad
|t_w\rangle=A_wP_{\rm miss}|\Theta_w\rangle^{\otimes L}.
```

Isometry preservation of inner products gives both identities needed for the channel:

```math
\langle s|t_w\rangle=q,
\qquad
\langle t_w|t_w\rangle=q.
```

In particular, the marked branch still has norm one. The overlap of a marked and an unmarked recovered branch is $`-1+2q`$. Logical populations remain unchanged, all unmarked-to-unmarked coherences remain unchanged, and every marked-to-unmarked coherence receives that multiplier. Thus the full logical phase channel is exactly

```math
\widetilde{\mathcal O}_w
=(1-q)\mathrm{Ad}_{O_w}
+q\,\mathrm{id},
\qquad
O_w=I-2|w\rangle\langle w|.
```

This identity is independent of how the recovery was completed outside the error span. It also holds when the marked address is one of the code's anchors: the protected tag distinguishes the distinguished query branch from its anchor branches.

### The full bit oracle

In the controlled-phase basis, a unique-mark function has exactly one negative basis label, $`(w,1)`$. Every other logical address-target label produces the same recovered syndrome. The identical overlap argument therefore proves

```math
\widetilde{\mathcal U}_w
=(1-q)\mathrm{Ad}_{U_w}
+q\,\mathrm{id}
```

after the target-Hadamard wrappers. This is equality of channels on the entire logical address-target system, including inputs entangled with an arbitrary reference. It is stronger than agreement on a target initialized to a classical bit. The [verification program](../verification/README.md) checks the complete normalized Choi matrix of this identity.

For several marked addresses, the vectors $`|t_x\rangle`$ need not agree. The exact global faulty-channel mixture is therefore not asserted for an arbitrary Boolean function. The uniform bound below supplies that case.

## 3. Arbitrary Boolean functions and arbitrary algorithms

For either the phase or controlled-phase representation,

```math
W_f-V_LC_f=P_{\rm miss}V_L(I-C_f).
```

The constant no-match weight implies

```math
\|P_{\rm miss}V_L\|=\sqrt q,
\qquad
\|W_f-V_LC_f\|\le 2\sqrt q.
```

This operator-norm estimate is uniform on the complete logical space and remains true after tensoring an arbitrary reference. The diamond distance of the corresponding isometric channels is at most twice the isometry distance. Physical noise and recovery are completely positive and trace preserving, so they cannot increase that distance. Exact correction on the ideal encoded state then gives

```math
\bigl\|\widetilde{\mathcal U}_f-
\mathrm{Ad}_{U_f}\bigr\|_\diamond
\le \min\{2,4(1-\eta)^{L/2}\}.
```

Suppose an ideal algorithm makes at most $`T\ge1`$ Boolean queries, with arbitrary known channels, measurements, classical feedforward, and retained reference systems between queries. Replace its queries one at a time. Each replacement changes the final channel by at most the per-query diamond error because the surrounding channels are contractions. Therefore the total error is at most $`T`$ times the per-query bound. Adaptive stopping can be padded to $`T`$ calls by using an idle $`|+\rangle`$ physical response under protected control.

For $`0<\eta<1`$, define $`a=-\ln(1-\eta)>0`$. A sufficient exact choice for total diamond error at most $`\epsilon`$ is

```math
L=\max\left\{1,
\left\lceil\frac{2\ln(4T/\epsilon)}{a}\right\rceil\right\}.
```

Since $`a\ge\eta=1/m`$, the simpler choice

```math
L=\left\lceil2m\ln(4T/\epsilon)\right\rceil
```

also suffices. If $`\eta=1`$, one physical call is exact and the logarithmic formula is unnecessary. The general physical query count is

```math
M=TL=O\!\left(T(d+1)\log\frac{4T}{\epsilon}\right)
\le O\!\left(Tr^2\log\frac{4T}{\epsilon}\right).
```

This is a uniform simulation guarantee for algorithms using the supplied bit oracle. It does not cover arbitrary noisy unitaries whose input-output structure supplies no idle response eigenstate.

## 4. Search and verification

For a unique mark, the exact mixture gives the sharper per-query estimate

```math
\|\widetilde{\mathcal O}_w-\mathrm{Ad}_{O_w}\|_\diamond
=2q
\quad(N\ge2).
```

The equality follows because $`O_w`$ has both eigenvalues $`+1`$ and $`-1`$: a balanced superposition of a marked and an unmarked address perfectly distinguishes its channel from the identity.

An ideal Grover search uses $`T=O(\sqrt N)`$ phase queries [1]. Replacing those queries changes its final channel by at most $`2Tq`$. It suffices to take

```math
L=\max\left\{1,
\left\lceil\frac{\ln(2T/\epsilon)}{-\ln(1-\eta)}\right\rceil
\right\},
```

or the simpler $`L=\lceil m\ln(2T/\epsilon)\rceil`$. At fixed error, the resulting search complexity is

```math
M=O\bigl((d+1)\sqrt N\log N\bigr)
\le O(r^2\sqrt N\log N).
```

For completeness, with $`\theta=\arcsin(N^{-1/2})`$, choose the Grover iteration count nearest to $`\pi/(4\theta)-1/2`$. Its ideal success is at least $`1-1/N`$. A final channel diamond error of at most $`\epsilon`$ reduces the success probability by at most $`\epsilon/2`$.

After measuring a candidate $`x`$, make one additional physical basis query with response initialized to zero. Its output is

```math
\Phi(|x\rangle\langle x|)\otimes
|f(x)\rangle\langle f(x)|.
```

The protected response therefore verifies the candidate exactly, even if the address channel changes its address output. This call is counted. For the zero-or-one-mark promise, rejection reports no mark; when there is no mark, the verifier always rejects. The resulting decision/search procedure has the same bounded-error query scaling.

An ideal bit oracle can simulate a noisy call by applying the known $`\Phi`$ afterward. The ordinary quantum search lower bound [2] therefore gives $`\Omega(\sqrt N)`$ calls in the noisy model as well. For fixed Kraus rank, the present upper bound preserves the quadratic query exponent. Neither the logarithmic factor nor the dependence on $`r`$ is proved optimal.

## 5. What the abstract query theorem charges

The channel description is supplied and is independent of the unknown function. Computing its complementary basis-state outputs, selecting a maximum-volume simplex, preparing coefficient-dependent states coherently, and implementing the controlled recovery use no queries to $`f`$. They nevertheless consume classical computation, memory, and known quantum gates.

For arbitrary explicitly supplied feature points, a maximum-volume simplex can be found by checking all $`\binom Nm`$ candidate sets of $`m=d+1`$ points in the affine hull. This is an existence procedure with potentially prohibitive preprocessing. Likewise, an arbitrary table of $`x`$-dependent recovery matrices is not a polylogarithmic quantum circuit, and coherent access to such a table is not assumed free.

Before optional recovery work registers, the probe register width is

```math
O\!\left(\log N+
L\bigl(\log N+\log(m+1)\bigr)\right).
```

One physical query port can be reused by swapping each fresh probe into the port, calling the oracle, and swapping its output into protected storage. Responses may be reused after their known unpreparation returns them to zero. Query outputs are not used again until recovery.

This width estimate permits clean initialization, discarding syndrome registers, and resetting discarded workspace between compiled calls. If such operations are forbidden, syndrome records must be retained and their storage grows with the number of calls. The algorithm's own workspace is additional. These are resource conventions, not consequences of the Kraus-rank bound.

The [two-branch phase-gradient construction](structured-example.md) avoids generic coefficient tables and recovery synthesis. It has $`\eta=1/2`$, explicit reversible address arithmetic, and an analytic syndrome decoder.

## 6. Finite control precision and channel mismatch

Let $`\Phi_0`$ be the channel used to design the code and recovery. Suppose the actual memoryless channel obeys

```math
\|\Phi_{\rm actual}-\Phi_0\|_\diamond\le\delta_\Phi.
```

The actual physical oracle differs from its design version by at most $`\delta_\Phi`$, uniformly in $`f`$. Tensoring with a protected response and composing with $`U_f`$ do not increase the distance. Replacing the $`M=TL`$ physical calls one at a time therefore contributes at most $`M\delta_\Phi`$ to the final error.

For each implemented known unitary $`\widehat G_j`$, let $`G_j`$ be the intended unitary and allow an irrelevant overall phase in its approximation error:

```math
\min_{\chi_j\in\mathbb R}
\|\widehat G_j-e^{i\chi_j}G_j\|\le\zeta_j.
```

Their channel distance is at most $`2\zeta_j`$. This phase convention applies to the complete operation being implemented, including its controls. A phase on a unitary before adding a control need not remain an overall phase. A second hybrid argument, allowing intervening noise and measurements, yields the complete conservative budget

```math
\boxed{
\|\mathcal A_{\rm actual}-\mathcal A_{\rm ideal}\|_\diamond
\le 4T(1-\eta)^{L/2}
+2\sum_j\zeta_j
+TL\delta_\Phi .
}
```

For the unique-mark search implementation, replace the first term by $`2T(1-\eta)^L`$. The final exact basis verifier can be included as one additional physical call in a global mismatch budget, although address-only channel mismatch still cannot change its protected response bit.

One convenient three-part allocation is

```math
4T(1-\eta)^{L/2}\le\epsilon/3,\qquad
\sum_j\zeta_j\le\epsilon/6,\qquad
\delta_\Phi\le\frac{\epsilon}{3TL}.
```

If at most $`G`$ known gates per compiled query require approximation, the uniform condition $`\zeta_j\le\epsilon/(6TG)`$ suffices. This is an operational gate-error statement. For a generic numerical recovery, translating it into coefficient precision can depend on small Gram eigenvalues and other conditioning parameters; no bound on those parameters follows from Kraus rank alone.

The structured example has a fixed, well-conditioned analytic decoder and avoids that issue. Even there, a fixed unknown discrepancy in the noise model is not automatically harmless as the number of calls grows. Calibration cost and its statistical guarantee are separate inputs, rather than an uncharged part of the compiler.

## References

1. L. K. Grover, “A fast quantum mechanical algorithm for database search,” STOC 1996. [Primary paper](https://arxiv.org/abs/quant-ph/9605043); [published version](https://doi.org/10.1145/237814.237866).
2. C. H. Bennett, E. Bernstein, G. Brassard, and U. Vazirani, “Strengths and Weaknesses of Quantum Computing,” *SIAM Journal on Computing* **26**, 1510–1523 (1997). [Primary paper](https://arxiv.org/abs/quant-ph/9701001); [published version](https://doi.org/10.1137/S0097539796300933).
