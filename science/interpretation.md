# What the environment criterion explains

The construction preserves the action of an unknown Boolean oracle by controlling the information released to its noise environment. A small environment limits the affine dimension of its computational-basis output states. Classical convex geometry then supplies a common mixture that contains every requested address with a uniform positive weight. The protected branch tag realizes that mixture coherently, and exact error correction removes the channel's effect on the encoded logical state.

This connects an environmental description of noise to an operational query bound. The result does not use a bound on the probability or strength of the physical error. A known rank-one unitary error is directly reversible; a general rank-$`r`$ channel admits the construction with designated weight at least $`r^{-2}`$. The full logical query is recovered approximately by using several probes and retaining all branches.

## Why the protected copy is not enough by itself

Keeping the logical address in a clean register does not automatically preserve its phase coherence. A probe correlated with that address can release which-address information to the environment. Discarding either the environment or an uncorrected probe can then dephase the protected register.

The balancing identity makes the environmental output independent of the logical input, including its reference correlations. The retained probe still carries an error syndrome. A joint recovery controlled by the logical address aligns that syndrome across all logical labels before it is discarded. Both the common environmental state and the accessible noisy output are needed in this argument. [The recovery proof](convex-code.md#4-exact-correction-including-reference-systems) makes these roles explicit.

## Why a correctable code can still carry an unknown query

The code alone would only preserve information through a known channel. To use it as an oracle probe, every logical address must retain a branch on which the physical address is exactly the desired one. Its weight must be uniform across logical inputs.

The standard bit response supplies the required control. An answer in $`|+\rangle`$ makes a paid oracle call contribute no Boolean phase; an answer in $`|-\rangle`$ produces phase kickback. Protected tags select the first designated branch, so only that probe contributes the logical phase. A probe's address is not used again after its noisy call. Its arbitrary noise can therefore commute past later controls and queries on other registers, leaving a product channel for the known recovery. This scheduling property is the reason the argument does not require diagonal Kraus operators. The [compiler proof](oracle-compiler.md) also gives the protected-response wrappers for a full bit oracle.

## Rank, geometry and implementation are different questions

The bound $`d+1\le r^2`$ is a worst-case consequence of the environment dimension. The actual complementary-state geometry can be much more favorable. Complete dephasing in the Fourier basis has Kraus rank $`N`$, yet all computational-basis inputs produce the same environmental state. It has $`d=0`$ and permits exact one-call simulation in this access model. Thus increasing rank does not by itself prove that a channel destroys coherent-query power.

The convex construction also does not imply efficient known controls. A generic channel can require a large description, costly simplex selection and expensive address-dependent encoders and decoders. Its query bound becomes a computational-time advantage only for families where those operations are efficient. The [phase-gradient example](structured-example.md) supplies a concrete family: reversible binary arithmetic and an explicit two-outcome syndrome give a fully charged implementation with polylogarithmic overhead per ideal query at inverse-polynomial accuracy.

The protected registers and the independence of the channel from the unknown function are substantive resources. For example, the rank-two faulty oracle studied by [Regev and Schiff](https://cims.nyu.edu/~regev/papers/faultygrover.pdf) does not contradict this theorem. Writing that oracle as an ideal call followed by noise makes the latter depend on the unknown marked function. [Related work](../references/related-work.md) compares the models directly.

## Established consequence and remaining questions

For fixed Kraus rank in the stated model, every Boolean-query algorithm admits logarithmic simulation overhead in its accuracy requirement. In particular, unstructured search retains its quadratic query exponent up to a logarithm. The result applies to arbitrary reference-entangled inputs and composes through adaptive algorithms.

Optimal rank dependence, removal of the logarithmic search overhead, and efficient implementations for broad channel classes remain separate questions. The theorem also does not extend by itself to noise before the oracle, a noisy response, temporally correlated environments, unknown channel parameters or an uncontrolled phase-only oracle. The precision analysis quantifies an implementation of the specified model; it does not provide a noise-calibration procedure or a fault-tolerance threshold.
