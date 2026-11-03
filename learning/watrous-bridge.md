# From Watrous to coherent queries through address noise

A Boolean oracle can return a correct answer bit while losing the address coherence needed by a quantum algorithm. This project asks how to preserve that coherent operation when each bit query is followed by a known noise channel on its address. The response, logical memory and stored query outputs are protected. The noise is fixed, independent of the unknown Boolean function, and uses a fresh environment on every call.

The educational anchor is **John Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/) (2018)**. Its channel representations explain what the environment can learn, and its channel-distance framework explains why a simulated query remains usable inside a larger computation. The project then supplies the geometric code and oracle circuit connecting those ideas.

## 1. A focused source route

The relevant sections can be read alongside the construction; the whole book is not a prerequisite.

| Watrous section | Use here |
|---|---|
| [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), §§2.1.2 and 2.2.1: states and channels | Describe retained registers, discarded environments and product channels. |
| Chapter 2, §2.2.2: representations and characterizations of channels | Move between Kraus and Stinespring descriptions; Theorem 2.22 relates the minimum representation size to Choi rank. |
| [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf), §§3.3.2–3.3.3: completely bounded trace norm and channel distances | Include auxiliary reference systems and quantify the error of replacing an operation. |

Watrous denotes adjoints by a star; the science pages use $`\dagger`$. His completely bounded trace norm is the diamond norm written here as $`\|\cdot\|_\diamond`$, without division by two. The letters $`X,Y`$ identify protected logical registers in this project, rather than a channel's generic input and output spaces. Physical queries use $`Q_i,A_i`$, with protected branch tags $`B_i`$.

The complementary output below is defined by taking the other marginal of a Stinespring representation. The simplex construction, prescribed query branch, explicit recovery and first-match routing are supplied in the repository. Their research-level antecedents remain attributed in [Related work](../references/related-work.md); they are not assigned to the selected textbook sections.

## 2. From a channel representation to a balanced probe

For Kraus operators $`K_1,\ldots,K_r`$, introduce a mathematical environment $`E`$ through

```math
W_\Phi|\psi\rangle
=\sum_{\alpha=1}^{r}K_\alpha|\psi\rangle\otimes|\alpha\rangle_E.
```

Tracing out $`E`$ gives the address channel $`\Phi`$. Tracing out the address output gives its complementary channel $`\widehat\Phi`$. The algorithm has no access to $`E`$; this representation describes information leakage, not an additional control resource.

For each basis address, put $`\sigma_x=\widehat\Phi(|x\rangle\langle x|)`$. These are density matrices on an $`r`$-dimensional environment. Their real affine dimension satisfies $`d\le r^2-1`$. The [geometric construction](../science/convex-code.md#2-a-common-mixture-with-a-prescribed-contribution) selects anchor addresses and nonnegative weights satisfying

```math
\eta\sigma_x+\sum_jp_j(x)\sigma_{a_j}=\tau,
\qquad
\eta=\frac1{d+1},
\qquad
\eta+\sum_jp_j(x)=1.
```

The same environment state $`\tau`$ can therefore contain every desired address with the same positive weight $`\eta`$. Orthogonal protected tags turn these probabilities into amplitudes of a probe $`|\Theta_x\rangle`$, with tag zero reserved for physical address $`x`$. The logical encoding is $`|x\rangle_X\mapsto|x\rangle_X|\Theta_x\rangle`$.

Keeping $`X`$ alone would not prevent dephasing: a correlated probe could still reveal $`x`$ to its environment. The balance identity removes that information. For any reference $`R`$, the environment becomes $`\rho_R\otimes\tau`$, and the code's error vectors have one common Gram matrix. The [explicit controlled recovery](../science/convex-code.md#4-exact-correction-including-reference-systems) aligns their syndromes without knowing the Boolean function. Recovery needs the retained noisy probe as well as the protected logical register.

## 3. Four addresses: see the balance and recovery

Take the existing [phase-gradient example](../science/structured-example.md) at $`N=4`$. Its known address noise is

```math
Z=\mathrm{diag}(1,i,-1,-i),
\qquad
\Phi(\rho)=\frac12Z\rho Z^\dagger
+\frac12Z^\dagger\rho Z.
```

Label the two error alternatives by environment basis states $`|0\rangle_E,|1\rangle_E`$. An address $`x`$ produces

```math
|e_x\rangle
=\frac{i^x|0\rangle_E+(-i)^x|1\rangle_E}{\sqrt2}.
```

The states for consecutive addresses are orthogonal. Prepare the tagged probe

```math
|\Theta_x\rangle
=\frac{|0\rangle_B|x\rangle_Q
+|1\rangle_B|x+1\bmod4\rangle_Q}{\sqrt2}.
```

For $`x=0`$, for example, the two environment vectors are $`(|0\rangle+|1\rangle)/\sqrt2`$ and $`i(|0\rangle-|1\rangle)/\sqrt2`$. Their equally weighted density matrices sum to $`I_E/2`$. The same is true for every $`x`$. The tag-zero address remains available with weight $`\eta=1/2`$.

The physical noise draws a sign $`s\in\{+1,-1\}`$ and applies $`Z_Q^s`$. On the correctable code, reverse the controlled address increment and the basis-label copy. The address returns to zero, leaving

```math
Z_X^s|x\rangle_X\otimes|y_s\rangle_B,
\qquad
|y_s\rangle=\frac{|0\rangle+is|1\rangle}{\sqrt2}.
```

The two tag states are orthogonal. With $`S=\mathrm{diag}(1,i)`$, applying $`HS^\dagger`$ maps them to a syndrome bit $`b`$ satisfying $`s=(-1)^b`$. The known correction $`Z_X^{-s}`$ restores the logical state. This works coherently on a superposition of addresses and with a reference attached. No measurement is required; the syndrome can be discarded after correction. Exact syndrome independence applies to this code state. The routed query below slightly perturbs the code and has a separately bounded error.

## 4. Carry the unknown query through the code

The bit oracle has a useful response control: $`|+\rangle`$ acquires no Boolean phase, whereas $`|-\rangle`$ acquires $`(-1)^{f(x)}`$. Both are ordinary paid calls and both suffer address noise. The alternative address may itself be marked; its value need not be learned.

Prepare $`L`$ probes and select the first tag equal to zero. Only its answer is active. For two probes, the protected tag strings give:

| Tags | Active probe | Does the desired phase occur? |
|---|---|---|
| 00 | First | Yes |
| 01 | First | Yes |
| 10 | Second | Yes |
| 11 | None | No |

Selecting only the first avoids applying the phase twice and cancelling it. Each queried address is then stored untouched until recovery. Its noise can move past later controls and other-probe queries, even for arbitrary nondiagonal Kraus operators. It never has to commute through its own unknown oracle.

To recover a full bit query, conjugate the protected logical answer $`Y`$ by a Hadamard before and after the procedure. In between, activate the selected physical response only when the logical answer label is $`y=1`$. The desired action is $`|x,y\rangle\mapsto(-1)^{yf(x)}|x,y\rangle`$, so the wrappers implement the bit flip coherently, including an answer entangled with a reference. Each physical response is unprepared after its call and may be reused.

In the four-address example, the no-match weight is $`q=2^{-L}`$. For one marked address $`w`$, the [exact logical channel](../science/search-and-resources.md#2-exact-logical-channel-for-a-unique-marked-address) is

```math
\widetilde{\mathcal U}_w
=(1-q)\mathrm{Ad}_{U_w}+q\mathrm{id}.
```

With two probes, input $`|w,0\rangle`$ therefore returns answer one with probability $`3/4`$. All branches remain in the output; there is no successful-outcome postselection. The channel identity also specifies the action on coherent inputs, rather than only this measurement example.

## 5. Why the guarantee composes, and what it costs

For general Boolean functions, the [compiler proof](../science/oracle-compiler.md#5-error-bound-on-the-whole-logical-input-space) compares entire isometries, including references. The no-match component has operator norm $`\sqrt q`$, giving

```math
\left\|\widetilde{\mathcal U}_{f,L}
-\mathrm{Ad}_{U_f}\right\|_\diamond
\le\min\{2,4(1-\eta)^{L/2}\}.
```

This is where the channel-distance language of Chapter 3 becomes operational. A query can be replaced inside an adaptive computation whose memory is already entangled with its inputs. Setting the per-query error to $`\delta=\epsilon/T`$ makes the accumulated error at most $`\epsilon`$ for $`T`$ ideal queries. The generic physical cost is $`O(r^2T\log(4T/\epsilon))`$; $`d=0`$ instead gives exact one-call simulation.

Query count and implementation cost remain distinct. Generic balancing and recovery may require expensive channel-dependent data and gates. The phase-gradient family has explicit preparation and recovery using $`O(nL)`$ known gates and protected qubits per compiled query, before finite-set synthesis, with $`n=\log_2N`$. Reusing that width permits syndrome resets or discards. Channel mismatch and gate approximation consume additional error budget, as quantified in [Search and resources](../science/search-and-resources.md#6-finite-control-precision-and-channel-mismatch).

The [30-milestone map](milestones.md) organizes this route from the basic objects to the full construction. The canonical proof and resource statements remain in [science/](../science/README.md).
