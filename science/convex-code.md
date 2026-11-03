# A balanced query code from complementary-state geometry

The construction in this document attaches a protected tag and a noisy query register to a protected logical address. Every logical address receives the same designated query weight, while the noise environment receives the same density operator for every logical input. The resulting code has an explicit recovery that depends only on the known noise channel.

The prescribed query weight is what connects the code to an unknown oracle. Its use in the physical query circuit is proved in [The oracle compiler](oracle-compiler.md). The complete access and resource contract is stated in [Model and results](model-and-results.md).

## 1. Complementary states of computational-basis addresses

Let $`\mathcal H_Q=\mathbb C^N`$ be the address space, with basis indexed by $`[N]=\{0,\ldots,N-1\}`$. Fix a known channel

```math
\Phi(\rho)=\sum_{\alpha=1}^{r}K_\alpha\rho K_\alpha^\dagger,
\qquad
\sum_{\alpha=1}^{r}K_\alpha^\dagger K_\alpha=I_Q,
```

where $`r`$ is its Kraus rank. A minimal Stinespring isometry is

```math
W_\Phi\lvert\psi\rangle
=\sum_{\alpha=1}^{r}K_\alpha\lvert\psi\rangle
  \otimes\lvert\alpha\rangle_E.
```

Write $`\widehat\Phi`$ for the associated complementary channel and define

```math
\sigma_x=\widehat\Phi(\lvert x\rangle\langle x\rvert),
\qquad
(\sigma_x)_{\alpha\beta}
=\langle x\rvert K_\beta^\dagger K_\alpha\lvert x\rangle.
```

Each $`\sigma_x`$ is a density operator on $`\mathbb C^r`$. The relevant dimension is the real affine dimension

```math
d=\dim_{\mathbb R}\operatorname{aff}\{\sigma_x:x\in[N]\},
\qquad
0\leq d\leq\min\{N-1,r^2-1\}.
```

A different minimal Stinespring representation conjugates all the states by the same environment unitary, so this affine dimension is unchanged. A supplied nonminimal representation can also be used; its Kraus count gives a possibly weaker upper bound.

## 2. A common mixture with a prescribed contribution

### Lemma 1: a maximum-volume simplex

There exist $`m=d+1`$ anchor addresses $`a_1,\ldots,a_m`$ and real functions $`\lambda_j(x)`$ such that

```math
\sigma_x=\sum_{j=1}^{m}\lambda_j(x)\sigma_{a_j},
\qquad
\sum_{j=1}^{m}\lambda_j(x)=1,
\qquad
\lvert\lambda_j(x)\rvert\leq1.
```

For $`d>0`$, choose an affine coordinate system on the hull and select a simplex of maximum absolute volume among all $`d+1`$ address states. A nonzero-volume simplex exists by the definition of $`d`$, and a maximizer exists because the address set is finite. Its vertices are affinely independent, so the barycentric coordinates of every $`\sigma_x`$ are unique.

In homogeneous affine coordinates, replacing column $`j`$ of the simplex matrix by the coordinate vector of $`\sigma_x`$ multiplies its determinant by $`\lambda_j(x)`$. A coefficient with absolute value greater than one would therefore produce a larger-volume simplex using address states, contradicting maximality. This proves the bound, including points outside the selected simplex.

If $`d=0`$, all the states coincide. Choose any anchor $`a_1`$ and put $`\lambda_1(x)=1`$. This proves the singleton case without assigning a positive-dimensional volume to it.

The determinant argument is the standard maximum-volume barycentric-spanner construction; see [Awerbuch and Kleinberg, Proposition 2.2](https://www.cs.cornell.edu/courses/cs683/2007sp/papers/OLSP.pdf). The proof is included to specify the exact finite-set guarantee used here.

### Corollary 2: environmental balance

Set

```math
\eta=\frac1m=\frac1{d+1},
\qquad
p_j(x)=\frac{1-\lambda_j(x)}m,
\qquad
\tau=\frac1m\sum_{j=1}^{m}\sigma_{a_j}.
```

These are valid mixture weights:

```math
p_j(x)\geq0,
\qquad
\eta+\sum_{j=1}^{m}p_j(x)=1.
```

Moreover,

```math
\begin{aligned}
\eta\sigma_x+\sum_{j=1}^{m}p_j(x)\sigma_{a_j}
&=\frac1m\left(
\sigma_x+\sum_j\sigma_{a_j}
-\sum_j\lambda_j(x)\sigma_{a_j}
\right)\\
&=\tau.
\end{aligned}
```

Thus every address can be included in a common environmental mixture with the same weight $`\eta\geq r^{-2}`$. The barycentric coefficients themselves can be negative; the physical probabilities $`p_j(x)`$ are nonnegative.

The anchor addresses are selected using the known channel alone. Their oracle values are not required or separately learned; physical anchor branches are still included in the compiler's paid calls.

## 3. The protected tagged encoding

Let $`X`$ be a protected logical address register. Let $`B`$ be a protected tag register with orthonormal labels $`0,1,\ldots,m`$, and let $`Q`$ be the address register that will undergo noise. Define

```math
\lvert\Theta_x\rangle_{BQ}
=\sqrt\eta\,\lvert0\rangle_B\lvert x\rangle_Q
+\sum_{j=1}^{m}\sqrt{p_j(x)}\,
  \lvert j\rangle_B\lvert a_j\rangle_Q,
```

and the encoding isometry

```math
V\lvert x\rangle_X
=\lvert x\rangle_X\lvert\Theta_x\rangle_{BQ}.
```

The probabilities sum to one, so every $`\lvert\Theta_x\rangle`$ is normalized. Orthogonality of the protected logical labels then gives $`V^\dagger V=I_X`$.

The branch labels are essential. They keep the distinguished address branch separate even when $`x`$ equals an anchor. They also remove cross terms between physical query addresses when the environment state is computed. This remains true for arbitrary nondiagonal Kraus operators.

The encoding is a coherent operation controlled in a specified basis. It does not produce independent copies of an arbitrary input state. In particular, retaining the protected register does not by itself preserve its reduced state: tracing out the probe multiplies its $`x,y`$ coherence by $`\langle\Theta_y\vert\Theta_x\rangle`$. Recovery acts jointly on the protected logical register and the retained noisy probe.

## 4. Exact correction, including reference systems

Let

```math
\mathcal E=\operatorname{id}_{XB}\otimes\Phi_Q.
```

The complement of $`\mathcal E\circ\operatorname{Ad}_V`$ traces out the protected registers as well as the channel output. For an arbitrary reference $`R`$, expand a joint input as

```math
\rho_{RX}=\sum_{x,y}\rho^R_{xy}\otimes\lvert x\rangle\langle y\rvert.
```

Tracing $`X`$ leaves only $`x=y`$, and tracing $`B`$ leaves only equal branch labels. The environmental balance identity therefore gives

```math
\begin{aligned}
\left(\operatorname{id}_R\otimes
\widehat{\mathcal E\circ\operatorname{Ad}_V}\right)(\rho_{RX})
&=\sum_x\rho^R_{xx}\otimes
\left(\eta\sigma_x+\sum_jp_j(x)\sigma_{a_j}\right)\\
&=\rho_R\otimes\tau.
\end{aligned}
```

The environment is independent of the full logical input, including its reference correlations.

Equivalently, the error operators obey the exact Knill–Laflamme equations

```math
V^\dagger
\left(I_{XB}\otimes K_\alpha^\dagger K_\beta\right)V
=C_{\alpha\beta}I_X,
\qquad
C_{\alpha\beta}=\tau_{\beta\alpha}.
```

The matrix $`C=\tau^{\mathsf T}`$ is positive semidefinite and has trace one. These are the standard exact-correction conditions of [Knill and Laflamme (1997)](https://doi.org/10.1103/PhysRevA.55.900). The following construction makes the recovery explicit and fixes its action on reference-entangled inputs.

### Proposition 3: a known controlled recovery

For each logical label, define the physical error vectors

```math
\lvert w_{x,\alpha}\rangle
=(I_B\otimes K_\alpha)\lvert\Theta_x\rangle.
```

Their Gram matrix is the same for every $`x`$:

```math
\langle w_{x,\alpha}\vert w_{x,\beta}\rangle=C_{\alpha\beta}.
```

Choose one eigendecomposition

```math
C=H\operatorname{diag}(\mu_1,\ldots,\mu_r)H^\dagger.
```

For each positive eigenvalue, put

```math
\lvert u_{x,k}\rangle
=\frac1{\sqrt{\mu_k}}
\sum_{\alpha=1}^{r}H_{\alpha k}\lvert w_{x,\alpha}\rangle.
```

Direct substitution of the common Gram matrix shows that the vectors $`\lvert u_{x,k}\rangle`$ are orthonormal. If $`\mu_k=0`$, the corresponding linear combination of error vectors is zero and is omitted. No inverse of a zero eigenvalue is taken.

Choose fixed orthonormal syndrome vectors $`\lvert s_k\rangle`$ in the physical $`BQ`$ output space. For every $`x`$, extend the map

```math
D_x\lvert u_{x,k}\rangle=\lvert s_k\rangle
```

to a unitary $`D_x`$ on that space. Such an extension exists because both families are orthonormal and have equal size. The common size is at most the dimension of the physical output space. Define the controlled decoder

```math
D=\sum_x\lvert x\rangle\langle x\rvert_X\otimes D_x.
```

Its action on the original Kraus vectors is

```math
D_x\lvert w_{x,\alpha}\rangle
=\sum_{k:\mu_k>0}\sqrt{\mu_k}\,
  \overline{H_{\alpha k}}\lvert s_k\rangle,
```

which is independent of $`x`$. Consequently the Stinespring isometry of encoding, noise and decoding sends every logical pure state to

```math
\lvert\psi\rangle_X\otimes\lvert\chi\rangle_{BQ,E},
\qquad
\lvert\chi\rangle
=\sum_{\alpha,k:\mu_k>0}
\sqrt{\mu_k}\,\overline{H_{\alpha k}}
\lvert s_k\rangle\lvert\alpha\rangle_E.
```

The syndrome–environment vector is normalized and fixed. The same factorization holds with an arbitrary reference attached to $`\lvert\psi\rangle`$. Discarding $`BQ`$ after $`D`$ defines a CPTP recovery $`\mathcal R`$ satisfying

```math
\mathcal R\circ\mathcal E\circ\operatorname{Ad}_V
=\operatorname{id}_X.
```

All choices in this decoder depend on the known channel and the code, and none depends on the unknown Boolean function. The arbitrary unitary completion also defines a valid recovery on states outside the code; the approximation proof in the compiler only requires exactness on the code itself.

## 5. Several probes and degenerate cases

For $`L\geq1`$, use

```math
V_L\lvert x\rangle
=\lvert x\rangle\lvert\Theta_x\rangle^{\otimes L},
\qquad
\mathcal E_L
=\operatorname{id}_{X B_1\cdots B_L}\otimes\Phi^{\otimes L}.
```

The fresh-environment assumption makes the complementary state on each logical basis input equal to $`\tau^{\otimes L}`$. Tracing the protected logical and branch registers again gives, for every reference,

```math
\left(\operatorname{id}_R\otimes
\widehat{\mathcal E_L\circ\operatorname{Ad}_{V_L}}\right)(\rho_{RX})
=\rho_R\otimes\tau^{\otimes L}.
```

Applying the controlled decoder $`D_x`$ independently to the probes and discarding their outputs gives a known recovery $`\mathcal R_L`$ with

```math
\mathcal R_L\circ\mathcal E_L\circ\operatorname{Ad}_{V_L}
=\operatorname{id}_X.
```

If $`d=0`$, then $`m=1`$, $`\eta=1`$ and $`p_1(x)=0`$. The probe is simply $`\lvert0\rangle_B\lvert x\rangle_Q`$, and the same recovery proof applies. Thus one physical query will suffice exactly in the compiler. This case can occur even when the channel has more than one Kraus operator.

If $`r=1`$, trace preservation gives $`K_1^\dagger K_1=I`$. The channel has equal input and output dimension, so $`K_1`$ is a known unitary. Here $`d=0`$, and the direct recovery $`K_1^\dagger`$ is available after the query. The general construction is consistent with this elementary case.

## 6. What the lemma supplies

For each fixed finite channel description, this gives a finite construction of the anchors, all code amplitudes, and a decoder. It does not bound the gate complexity of finding a maximum-volume simplex or coherently applying the $`x`$-dependent unitaries $`D_x`$. Those costs must be analyzed for an efficiently specified channel family.

The recovery argument also applies to any explicitly supplied tagged encoding whose distinguished branch carries address $`x`$ with a constant weight and whose average complementary state is independent of $`x`$. Such a structured encoding can have a larger designated weight than the generic guarantee $`\eta=1/(d+1)`$. The dimension bound provides one construction for every channel; it is not an optimality statement about all codes or all oracle simulators.
