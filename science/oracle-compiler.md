# A coherent compiler for noisy Boolean queries

This document proves that the balanced code in [A balanced query code](convex-code.md) simulates an ideal Boolean bit oracle with a number of physical calls controlled by the complementary-state dimension. The proof covers arbitrary Boolean functions and inputs entangled with references. Each encoded probe is queried once, including probes whose responses are prepared to acquire no oracle phase.

The noise channel can have nondiagonal Kraus operators. The circuit places each address-noise operation after all oracle dependence on that particular address register. Subsequent controls use protected registers and other probes, so the noise can be moved to the end of the circuit without moving it through its own oracle call.

## 1. Registers, channels and the balanced code

The supplied physical oracle is

```math
U_f\lvert z\rangle_Q\lvert a\rangle_A
=\lvert z\rangle_Q\lvert a\mathbin{\oplus}f(z)\rangle_A,
\qquad
f:[N]\longrightarrow\{0,1\}.
```

One physical call is the channel

```math
\mathcal N_f
=(\Phi_Q\otimes\mathrm{id}_A)\circ\mathrm{Ad}_{U_f}.
```

The channel $`\Phi`$ is known, fixed, independent of $`f`$, and memoryless between calls. Only the physical address register is noisy. The logical address $`X`$, logical response $`Y`$, tags and other workspace are protected. The target channel is $`\mathrm{Ad}_{U_f^{XY}}`$.

Use the notation and code from [the geometric construction](convex-code.md): $`d`$ is the real affine dimension of the computational-basis complementary states,

```math
m=d+1,
\qquad
\eta=\frac1{d+1},
\qquad
V_L\lvert x\rangle_X
=\lvert x\rangle_X\lvert\Theta_x\rangle_{B_1Q_1}
\cdots\lvert\Theta_x\rangle_{B_LQ_L}.
```

In every probe, tag zero has weight $`\eta`$ and carries physical address $`x`$. The other tags carry the anchor addresses with channel-dependent weights. They can have arbitrary values under $`f`$. Write $`\mathcal E_L`$ for $`\Phi^{\otimes L}`$ on the probe addresses, with identity action on all protected registers. There is a known recovery $`\mathcal R_L`$ satisfying

```math
\mathcal R_L\circ\mathcal E_L\circ\mathrm{Ad}_{V_L}
=\mathrm{id}_X.
```

All channels and isometries in this identity can be tensored with an arbitrary reference or with the protected response $`Y`$.

## 2. Selecting the first distinguished branch

For a computational-basis string of protected tags $`b=(b_1,\ldots,b_L)`$, define

```math
s_i(b)
=\mathbf 1_{\{b_i=0\}}
\prod_{j\lt i}\mathbf 1_{\{b_j\ne0\}}.
```

The selectors are mutually exclusive. If any tag is zero, exactly the first such tag is selected; otherwise all selectors vanish. Define

```math
h(b)=\sum_{i=1}^{L}s_i(b)
=\mathbf 1_{\{\text{at least one }b_i=0\}}.
```

These functions can be computed reversibly into protected work registers and uncomputed later. The computation reads only tag labels, and its circuit is independent of $`f`$ and of every noisy address output.

To explain the full bit-oracle simulation, first work in the Hadamard basis of the protected response. For a logical response basis value $`y\in\{0,1\}`$, the desired controlled phase is

```math
C_f\lvert x,y\rangle=(-1)^{y f(x)}\lvert x,y\rangle,
\qquad
U_f^{XY}=(I_X\otimes H_Y)C_f(I_X\otimes H_Y).
```

The expression in terms of $`y`$ specifies a coherent controlled operation; it does not measure the logical response.

## 3. One physical query for each probe

For $`i=1,\ldots,L`$, perform the following operations in order.

1. Start an answer qubit $`A_i`$ in $`\lvert0\rangle`$. Compute $`c_i=s_i(b)y`$ into it with a protected controlled bit flip, and then apply a Hadamard. Its state is $`H\lvert c_i\rangle`$: $`\lvert+\rangle`$ when $`c_i=0`$ and $`\lvert-\rangle`$ when $`c_i=1`$.
2. Apply the supplied noisy bit query to $`Q_i,A_i`$. This is one paid physical call, with the channel $`\Phi`$ acting after its ideal bit-query part.
3. Undo the answer preparation by applying a Hadamard and the same protected controlled bit flip. The answer returns to $`\lvert0\rangle`$.

The bit oracle acts on these response eigenstates as

```math
U_f\lvert z\rangle H\lvert c\rangle
=(-1)^{c f(z)}\lvert z\rangle H\lvert c\rangle.
```

Consequently the ideal part of step $`i`$ applies the phase

```math
(-1)^{s_i(b)y f(z_i)}.
```

The answer's prepared eigenstate is unchanged by the ideal query. Since address noise acts on $`Q_i`$ alone, it commutes with the answer-unpreparation gates. The answer therefore returns to zero even in the actual noisy circuit, without a second oracle call or a measurement. A single physical answer qubit can be reused sequentially.

On the encoded support, $`s_i(b)=1`$ implies $`b_i=0`$ and hence $`z_i=x`$. Every other response is $`\lvert+\rangle`$ on that branch and acquires no oracle phase. The product of the $`L`$ ideal phases is thus

```math
(-1)^{y f(x)h(b)}.
```

When a distinguished branch is present, this is exactly the target controlled phase. When no distinguished branch is present, it is the identity. No information about the anchor values is required. Selecting only the first distinguished branch also prevents repeated occurrences of $`x`$ from cancelling the phase in pairs.

The procedure is ordinary phase kickback through the supplied bit oracle. It does not assume an independently supplied controlled extension of an unknown phase-only oracle.

## 4. Moving arbitrary address noise to the end

Let $`D_i^f`$ denote the ideal diagonal phase operation from step $`i`$, after the answer has returned to zero. It acts on the protected tags, $`Y`$, and $`Q_i`$. Let $`K_{\alpha_i}^{(i)}`$ be a Kraus operator of the noise on $`Q_i`$.

For distinct probes, the relevant operators commute:

```math
K_{\alpha_i}^{(i)}D_j^f
=D_j^fK_{\alpha_i}^{(i)}
\qquad(i\ne j).
```

The noise on $`Q_i`$ also commutes with all later selector uncomputation and response preparation or unpreparation, because those operations act on protected registers. Therefore each complete Kraus trajectory can be rewritten as

```math
\begin{aligned}
K_{\alpha_L}^{(L)}D_L^f\cdots
K_{\alpha_1}^{(1)}D_1^f
&=\left(\prod_{i=1}^{L}K_{\alpha_i}^{(i)}\right)
  \left(\prod_{i=1}^{L}D_i^f\right).
\end{aligned}
```

This rearrangement never moves $`K_{\alpha_i}^{(i)}`$ through $`D_i^f`$. They may fail to commute. The ordering is valid because each already-queried address is stored until the final recovery, while all later physical queries use other probe registers.

Summing the Kraus trajectories proves an equality of channels: the actual circuit before recovery is $`\mathcal E_L`$ applied after the ideal routed isometry. Memorylessness is used here to obtain the product channel $`\Phi^{\otimes L}`$.

After the responses and selector work registers have been unprepared, apply the known recovery $`\mathcal R_L`$. Exact correction is asserted on the balanced code. The next section bounds how far the ideal routed isometry is from that code after the desired logical query.

## 5. Error bound on the whole logical input space

Let $`P_{\mathrm{miss}}`$ project onto tag strings with no zero entry, acting as identity on all other registers. Extend the encoding by the protected response and write

```math
\overline V_L=V_L\otimes I_Y,
\qquad
V_{\mathrm{miss}}=P_{\mathrm{miss}}\overline V_L,
\qquad
V_{\mathrm{hit}}=(I-P_{\mathrm{miss}})\overline V_L.
```

The designated branch probability is independent of the logical address. Hence

```math
q_L=(1-\eta)^L,
\qquad
V_{\mathrm{miss}}^\dagger V_{\mathrm{miss}}=q_L I_{XY},
\qquad
V_{\mathrm{hit}}^\dagger V_{\mathrm{miss}}=0.
```

The ideal routed isometry is exactly

```math
W_f=V_{\mathrm{hit}}C_f+V_{\mathrm{miss}}.
```

The target encoded isometry is $`\overline V_L C_f`$. Their difference obeys

```math
\begin{aligned}
W_f-\overline V_L C_f
&=V_{\mathrm{miss}}(I-C_f),\\
\left\|W_f-\overline V_L C_f\right\|_\infty
&\leq2\sqrt{q_L}.
\end{aligned}
```

This is an operator-norm bound on the full logical space. It already includes superpositions of different addresses and response values, and it is unchanged by tensoring an arbitrary reference identity.

For any two isometries $`W,V`$, the associated channels satisfy

```math
\left\|\mathrm{Ad}_W-\mathrm{Ad}_V\right\|_\diamond
\leq2\|W-V\|_\infty.
```

Indeed, expand their action on an arbitrary trace-class operator, including a reference, as

```math
WZW^\dagger-VZV^\dagger
=(W-V)ZW^\dagger+VZ(W^\dagger-V^\dagger)
```

and use the operator-norm/trace-norm inequality and $`\|V\|_\infty=\|W\|_\infty=1`$. This directly proves a diamond-norm estimate rather than a bound restricted to unentangled inputs.

Applying the product noise and CPTP recovery cannot increase the diamond distance. Exact correction on $`\overline V_L C_f`$ therefore gives

```math
\left\|
(\mathcal R_L\otimes\mathrm{id}_Y)
\circ\mathcal E_L\circ\mathrm{Ad}_{W_f}
-\mathrm{Ad}_{C_f}
\right\|_\diamond
\leq\min\{2,4(1-\eta)^{L/2}\}.
```

Finally conjugate the protected response by $`H_Y`$ before and after the controlled-phase procedure. Unitary conjugation preserves diamond distance, so the same estimate holds for the full Boolean bit oracle:

```math
\boxed{
\left\|\widetilde{\mathcal U}_{f,L}
-\mathrm{Ad}_{U_f^{XY}}\right\|_\diamond
\leq\min\{2,4(1-\eta)^{L/2}\}.
}
```

The norm is unhalved; its maximum for two channels is two. The estimate holds uniformly over every Boolean function. The no-match subspace contributes approximation error and is retained throughout the protocol. No branch is postselected away.

## 6. Physical call count and composition

For $`d\geq1`$ and desired per-query error $`0<\delta\leq1`$, the sufficient choice

```math
L=\left\lceil2(d+1)\ln\frac4\delta\right\rceil
```

follows from

```math
(1-\eta)^{L/2}\leq\exp\left(-\frac{\eta L}{2}\right).
```

There are exactly $`L`$ physical noisy calls. If $`d=0`$, then $`\eta=1`$, the no-match subspace has zero weight, and $`L=1`$ gives exact simulation.

Now consider an algorithm making at most $`T\geq1`$ ideal bit queries. Its other operations may be arbitrary known CPTP maps, with measurements, classical control and retained quantum memory. Replace each query by the compiler with $`\delta=\epsilon/T`$, where $`0<\epsilon\leq1`$ is the desired total unhalved diamond error. A hybrid sequence that replaces one query at a time has total distance at most

```math
\sum_{t=1}^{T}\delta\leq\epsilon.
```

The per-query estimate permits arbitrary reference systems, so the input to each replaced query can contain all previous algorithmic records and correlations. Adaptivity requires no additional independence assumption on those inputs. The fresh-environment assumption concerns the physical noise channel itself.

For $`d\geq1`$, a sufficient total number of physical calls is

```math
T\left\lceil2(d+1)\ln\frac{4T}\epsilon\right\rceil
=O\left((d+1)T\log\frac{4T}\epsilon\right)
\leq O\left(r^2T\log\frac{4T}\epsilon\right).
```

For $`d=0`$, the algorithm is simulated exactly with $`T`$ physical calls. An algorithm with no ideal queries needs no compilation. A final measurement changes any event probability by at most $`\epsilon/2`$ under the unhalved convention.

## 7. A single physical port and protected storage

The abstract circuit applies the noisy oracle to $`Q_1,\ldots,Q_L`$ in turn. It can be implemented with one fixed physical query port. Initialize that port in a known basis state, swap $`Q_i`$ into it, perform one noisy call, and swap the address output back. The original known port state is parked in the protected $`Q_i`$ register during the call, so the second swap restores it to the port. The noisy output is retained in protected storage until decoding.

This routing requires the noise to act only at the oracle invocation. The proof does not supply protection against additional noise on stored probes, the logical address, branch tags or answer. It also does not require access to the physical noise environment. Discarding a probe instead of retaining and decoding it would generally leak logical information and is not an implementation of this compiler.

The number of query calls is the central bound. Preparing a generic channel-dependent code and compiling its recovery have separate costs, described in [Model and results](model-and-results.md). The weak-query/error-correction approach is related to [Shen and Choi's *Oracle Distillation*](https://arxiv.org/abs/2609.31596); the proof here specifies the complementary-state construction and the first-match response routing used for the present post-address noise model.
