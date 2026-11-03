# Related work and attribution

Last checked: 3 November 2026. Bibliographic records are in [references.bib](references.bib).

## The statement being compared

The model in this repository is a standard Boolean bit oracle followed by a **known, fixed, memoryless, function-independent channel on the address register alone**. The response register and workspace are noiseless. If the address channel has Kraus rank $`r`$, the construction simulates one ideal query to unhalved diamond error $`\delta`$ using $`O(r^2\log(4/\delta))`$ physical queries. The sharper parameter is $`d+1\leq r^2`$, where $`d`$ is the affine dimension of the complementary outputs on basis addresses. General gate efficiency is a separate question.

The comparison below concerns this particular simulation statement. It is not a claim that finite rank characterizes every distillable oracle, or that the bibliography establishes exhaustive priority.

## Oracle distillation is the closest comparator

[Shen and Choi, *Oracle Distillation*](https://arxiv.org/abs/2609.31596) supply the central weak-query idea: preserve a matched population $`\eta`$ while maintaining correctability, then amplify the response with logarithmic dependence on the desired error and inverse-linear dependence on $`\eta`$. Their coherent simulation framework, protected computation, and composition into algorithms are direct predecessors. Appendix F, Lemma 35, Eq. (F6), already expresses a common Knill–Laflamme matrix as a convex mixture of error-feature matrices.

Their Theorem 1a treats bounded-Pauli-weight adversarial index noise; Theorem 1b treats sufficiently weak independent depolarization, including response noise. The adversarial model can depend on the unknown function. Their explicit protocol uses two calls per block, aggregation, and oracle uncomputation; Appendix B, Lemma 10, moves diagonal noise through those operations.

The present construction uses a fixed known channel, complementary-state geometry, and protected first-match response routing. It handles arbitrary global address channels without assuming diagonal noise or bounded Pauli weight. The known-channel assumption and clean-response assumption remain material differences. The models should therefore be compared along these separate axes.

**Inspected version:** arXiv:2609.31596v1; [full primary manuscript](https://pdfs.assets.alphaxiv.org/2609.31596v1.pdf), Sec. IV, Appendix B, Appendix F, and Sec. IX.A. BibTeX key: `shenchoi2026`.

## Black-box error filtration

[Lee, Hann, Puri, Girvin, and Jiang](https://doi.org/10.1103/PhysRevLett.131.190601) establish gate-based error filtration for unknown black-box operations. Their circuit coherently routes a desired state and a filler state through multiple calls, then **postselects** the control outcome. For a Kraus operator close to the target unitary, main-text Eqs. (6)–(7) give conditional infidelity $`(1-F)_0/T+O(\varepsilon^2)`$; Eqs. (8)–(9) analyze success probability.

The supplement also treats nonperturbative fidelity improvement, so its scope is broader than a first-order expansion alone. Nevertheless, Sec. II.C explicitly leaves coherent unitary error unchanged, and Sec. IV analyzes a residual error floor as $`T\to\infty`$ under favorable common-eigenstate assumptions. These results do not provide deterministic, arbitrary-precision diamond-norm simulation solely from finite Kraus rank.

The relevant shared idea is coherent routing around a noisy black box. Here the routing uses the Boolean response eigenstates and protected branch tags, followed by exact channel-specific recovery; it does not condition the output on a successful filtration event.

**Inspected sources:** [accepted article](https://link.aps.org/accepted/10.1103/PhysRevLett.131.190601) and [arXiv:2210.10733v2, including the supplement](https://arxiv.org/pdf/2210.10733v2). BibTeX key: `leeetal2023`.

## Existing positive results and noisy-search obstructions

### One-sided local noise already has a positive example

[Rosmanis's 2024 addendum](https://arxiv.org/pdf/2405.11973) explicitly preserves quadratic search speedup when a known single index qubit is depolarized only after the oracle. Appendix B.1 fixes that bit to each of its two values, searches the two sectors, and reinitializes the bit before each call. The slowdown is only a constant factor. Thus preserving Grover speedup under one-sided address noise is already established.

The present statement extends this positive baseline to arbitrary globally supported fixed channels and to coherent simulation of every Boolean query, rather than a search-specific sector decomposition. The addendum's main linear lower bound instead uses independent noise both before and after the oracle. The ordering assumption is essential. BibTeX key: `rosmanis2024`.

### Complete dephasing and faulty oracles concern different models

[Rosmanis's 2023 paper](https://arxiv.org/pdf/2309.14944) proves lower bounds for global depolarizing and dephasing oracle noise. Complete dephasing of an $`N`$-dimensional address has Kraus rank $`N`$, so it does not contradict a guarantee at fixed rank as $`N`$ grows. BibTeX key: `rosmanis2023`.

[Regev and Schiff](https://cims.nyu.edu/~regev/papers/faultygrover.pdf) prove the loss of Grover speedup when each oracle call is replaced by the identity with constant probability. Although this faulty-oracle channel has two Kraus operators, expressing it as ideal oracle followed by noise produces a function-dependent noise channel. For the standard bit oracle that effective noise also involves the response. It is outside the fixed address-only model here. BibTeX key: `regevschiff2008`.

[Lolck, Mančinska, and Paraashar](https://arxiv.org/pdf/2411.04931) give a general robustification for the faulty-oracle model, with a roughly quadratic multiplicative query overhead. This is an important predecessor for algorithm-independent noisy-query simulation, under the same distinct faulty-oracle access assumption. BibTeX key: `lolcketal2024`.

## The convex geometry is classical

The maximum-volume-simplex argument used here is the affine form of the determinant argument for barycentric spanners. [Awerbuch and Kleinberg, Proposition 2.2](https://www.cs.cornell.edu/courses/cs683/2007sp/papers/OLSP.pdf) select a determinant-maximizing basis and bound its expansion coefficients by replacing one basis vector. Applying that argument to affine coordinates gives the anchor coefficients used in this repository. BibTeX key: `awerbuchkleinberg2008`.

There is also a direct formulation using Minkowski asymmetry. For a non-singleton convex body $`K`$, the largest uniform weight $`\eta`$ such that one center can be written as $`\eta x+(1-\eta)y_x`$ for every $`x\in K`$, with $`y_x\in K`$, is

```math
\eta_* = \frac{1}{1+s(K)}.
```

Indeed, the mixture condition is equivalent to $`-(K-c)\subseteq[(1-\eta)/\eta](K-c)`$. The classical bound $`s(K)\leq d`$ in affine dimension $`d`$ gives $`\eta_*\geq1/(d+1)`$. [Brandenberg and König, Proposition 3.4](https://arxiv.org/pdf/1310.4368), records this bound and its simplex equality case. For singleton $`K`$, the usable weight is $`1`$. BibTeX key: `brandenbergkoenig2015`.

The repository therefore claims an application of this geometry to complementary-channel outputs, not a new convex-geometric theorem. Simplex equality establishes sharpness of the matched-weight bound within this mixture construction; it is not a lower bound for all noisy-oracle protocols.

## Error correction and common moment constructions

The recovery step is an application of the established [Knill–Laflamme conditions](https://doi.org/10.1103/PhysRevA.55.900). Making the complementary channel constant on a code is an equivalent way to express exact correctability. The standard theorem, rather than a new recovery principle, is doing this work. BibTeX key: `knilllaflamme1997`.

Convex geometry has long been used to meet common error-moment conditions. [Knill, Laflamme, and Viola, Theorem 4](https://arxiv.org/pdf/quant-ph/9908066), construct codes through common convex combinations. [Li and Poon, Proposition 2.4](https://arxiv.org/pdf/0812.4772), use a Tverberg partition after diagonal compression to obtain joint higher-rank numerical ranges. [Aydin, Albert, and Barg, Sec. VII.B](https://arxiv.org/pdf/2509.20545), give modern code constructions based on the same convex-intersection principle. BibTeX keys: `knilllaflammeviola2000`, `lipoon2011`, and `aydin2026`.

Those code-existence results do not impose the additional oracle requirement used here: every prescribed basis address must remain available with a uniform positive matched weight. The anchor construction supplies that requirement, and the protected response routing converts it into an unknown Boolean operation.

## Consequential difference and limits

The substantive statement is a sufficient condition for **coherent query simulation controlled by the environment dimension**, with no noise-strength or locality bound, under the stated known-channel access model. Its proof combines established ingredients with a routing construction that lets arbitrary post-query address noise move past every subsequent protected operation. The resulting overhead is independent of the oracle's domain size when $`r`$ is fixed.

This should be assessed as a synthesis yielding a particular universal simulation theorem. Weak queries, convex error moments, exact correction, and coherent routing each have substantial prior literature. The remaining scientific questions include optimal rank dependence, efficient implementations for broad channel families, and robustness when the channel is known only approximately. General finite-rank existence alone does not resolve those questions.

