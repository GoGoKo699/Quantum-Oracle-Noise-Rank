# Quantum Oracle Noise Rank

How much coherent query power survives when a Boolean oracle is followed by strong noise on its address register? For a **known, fixed, memoryless channel of Kraus rank $`r`$**, the construction here simulates every ideal Boolean bit query with $`O(r^2\log(4/\delta))`$ physical calls at unhalved diamond error $`\delta`$. The channel can act globally and need not be close to the identity. Its placement after the query, its independence from the unknown Boolean function, and the protection of the response and workspace are essential assumptions.

The controlling object is the set of environment states produced by the basis addresses. A common convex mixture balances those states while retaining a prescribed weight on every requested address. A protected response circuit then applies the unknown logical query whenever a designated branch occurs, and a known error-correction operation recovers the logical registers.

## Results

Let $`d`$ be the real affine dimension of the complementary outputs on computational-basis addresses. Then $`d+1\le r^2`$. The generic code has designated weight $`\eta=1/(d+1)`$ and uses $`L`$ physical calls per simulated query:

```math
\left\|\widetilde{\mathcal U}_{f,L}
-\mathrm{Ad}_{U_f}\right\|_\diamond
\leq \min\{2,4(1-\eta)^{L/2}\}.
```

This estimate is uniform over Boolean functions and arbitrary reference-entangled inputs. It is deterministic: every branch is retained.

| Result | Guarantee | Authoritative account |
|---|---|---|
| Coherent Boolean query | $`L=\lceil2(d+1)\ln(4/\delta)\rceil`$ suffices when $`d\ge1`$ | [Model and theorem](science/model-and-results.md), [compiler proof](science/oracle-compiler.md) |
| Degenerate environment geometry | Exact one-call simulation when $`d=0`$, even for some high-rank channels | [Limiting cases](science/model-and-results.md#5-what-the-environment-dimension-does-and-does-not-say) |
| General $`T`$-query algorithm | $`O((d+1)T\log(4T/\epsilon))`$ physical calls at total error $`\epsilon`$ | [Composition and resources](science/search-and-resources.md) |
| Unstructured search | $`O(r^2\sqrt N\log N)`$ physical calls at fixed error | [Search consequence](science/search-and-resources.md#4-search-and-verification) |
| Explicit global rank-two channel | Search with $`\sqrt N\,\mathrm{polylog}N`$ known gates and $`O(\log^2N)`$ reusable protected qubits | [Phase-gradient construction](science/structured-example.md) |

The rank bound is sufficient, not a classification or a matching lower bound. The general theorem counts oracle calls; efficient channel-dependent preparation and recovery require additional structure. The rank-two example supplies such a circuit explicitly, including finite gate precision and channel-mismatch accounting.

## Read the argument

Start with the [science guide](science/README.md) for the connected account, or choose a direct route:

1. [Model and results](science/model-and-results.md): access assumptions, error convention and principal statements.
2. [Balanced query code](science/convex-code.md): complementary states, the simplex construction and explicit recovery.
3. [Oracle compiler](science/oracle-compiler.md): first-match response routing, arbitrary address noise and the reference-uniform bound.
4. [Search and resources](science/search-and-resources.md): the exact unique-mark channel, query composition, memory and precision.
5. [Efficient structured example](science/structured-example.md): a complete rank-two construction with charged gate costs.
6. [Interpretation](science/interpretation.md): what the environment criterion explains and where it stops.

[Related work](references/related-work.md) compares the result with oracle distillation, error filtration, noisy-search results and convex error-correction constructions. The [bibliography](references/references.bib) records the cited primary sources. The weak-query framework, exact error correction and convex geometry have established antecedents; the contribution is their specified combination into the present universal simulation theorem.

## Learn the construction

The [learning route](learning/README.md) uses **John Watrous, The Theory of Quantum Information (2018)** as its single educational anchor. The [source-to-project bridge](learning/watrous-bridge.md) translates the channel and distance formalism and develops a four-address worked example. The [30-milestone map](learning/milestones.md) connects 12 foundation milestones with 18 milestones that assemble the construction, its consequences and its resource limits.

## Reproduce the finite checks

From the repository root, install the pinned numerical dependency and run:

```bash
python -m pip install -r requirements.txt
python verification/verify.py --check
```

The [verification guide](verification/README.md) describes the tested channels, complete bit-channel checks, expected output and numerical tolerances. The checks exercise the construction and catch implementation errors; the proofs establish the statements for arbitrary dimensions and inputs.

## Scope

The physical access is a standard bit oracle followed by known address-only noise. The response, branch tags, logical memory, stored query outputs and known controls are protected. A fresh noise environment is used for every physical call, and the noisy address output remains available for recovery. No QRAM or free controlled extension of an unknown phase-only oracle is assumed.

Generic channel description, calibration, preprocessing and gate synthesis have their own costs. Fixed noise strength is allowed, while a fixed unmodeled discrepancy is not automatically tolerated over an increasingly long algorithm. [Resource accounting](science/search-and-resources.md#6-finite-control-precision-and-channel-mismatch) gives the explicit error budget.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
