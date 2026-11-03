# Thirty milestones for Quantum Oracle Noise Rank

This map follows one question: when can a noisy physical Boolean query be turned into a reliable coherent logical query? It develops the required objects, then connects the balanced code, response routing and recovery into the simulation theorem and its resource consequences.

The single educational anchor is **John Watrous, [The Theory of Quantum Information (2018)](https://cs.uwaterloo.ca/~watrous/TQI/)**. The [Watrous bridge](watrous-bridge.md) explains how its channel and distance formalism enters this project. Watrous supplies the foundations; the repository supplies the complementary-output construction, convex balancing proof, recovery construction and oracle-specific circuit. The [related-work account](../references/related-work.md) attributes the research ingredients separately.

## Allocation and reading order

| Phase | Milestones | Role in the argument |
|---|---|---|
| Background and preliminaries | M01–M12 | Assemble registers, channels, environmental information, correction and composable error into the precise oracle task. |
| Narrative and innovation | M13–M30 | Build the balanced code, preserve the unknown query, derive the bound, and connect it to search and an efficient circuit. |

Twelve background milestones establish the framework needed to connect quantum channels with query algorithms. Eighteen narrative milestones follow the longer construction and its consequences. Both phases proceed from individual objects to the complete scientific claim. The map records understanding targets and dependencies; specialist derivations remain in the linked science pages.

The relevant anchor passages are [§2.1.2 on states](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), [§§2.2.1–2.2.2 on channels and their representations](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), and [§3.1.1 and §§3.3.2–3.3.3 on operational distances](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf). These are selected passages, not a requirement to read the entire book first.

## Phase I: background and preliminaries

### M01. Registers and the Boolean oracle task

**Central question.** What does a Boolean oracle do, and which systems enter or leave one physical call?

**Understanding target.** Distinguish the address, physical answer, protected logical registers and inaccessible environment. Explain the action $`U_f\lvert x,a\rangle=\lvert x,a\oplus f(x)\rangle`$ while keeping the unknown function separate from known controls.

**Dependencies and story role.** No earlier milestone. This identifies the task and the systems to which later channel statements refer.

**Conceptual connection.** A register is a physical information-bearing subsystem; the oracle is a specified joint operation on two such subsystems.

**Sources.** Watrous §2.1, [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [Model and results, §1](../science/model-and-results.md#1-the-physical-oracle-and-its-accessible-outputs).

### M02. Coherence and basis-controlled encoding

**Central question.** What changes when an oracle address is a superposition rather than a classical label?

**Understanding target.** Track relative amplitudes and distinguish a coherent basis-controlled isometry from measurement or independent copying of an unknown quantum state. Explain why a clean logical register can become entangled with a probe.

**Dependencies and story role.** M01. This makes preserving off-diagonal logical matrix elements part of the task before noise is introduced.

**Conceptual connection.** Reversible copying of basis labels is an encoding operation; the reduced state of either subsystem need not retain the original coherence by itself.

**Sources.** Watrous §2.1.2, [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [Convex code, §3](../science/convex-code.md#3-the-protected-tagged-encoding).

### M03. Channels and discarded systems

**Central question.** How can a physical evolution be described when part of its output is unavailable?

**Understanding target.** Interpret density operators and completely positive trace-preserving maps. Explain the distinct roles of unitary evolution, adding an ancilla and taking a partial trace.

**Dependencies and story role.** M01–M02. This replaces an isolated state-vector description with the language needed for noise and recovery.

**Conceptual connection.** Discarding an environment is a physical channel, and retaining the noisy address output gives the recovery more information than discarding that output as well.

**Sources.** Watrous §§2.1.2 and 2.2.1, [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [Model and results, §1](../science/model-and-results.md#1-the-physical-oracle-and-its-accessible-outputs).

### M04. Kraus operators and an environment representation

**Central question.** How do Kraus operators and a Stinespring isometry describe the same channel?

**Understanding target.** Read $`\Phi(\rho)=\sum_\alpha K_\alpha\rho K_\alpha^\dagger`$ and connect its trace-preservation condition to an isometric system-environment evolution. Distinguish the minimal Kraus rank $`r`$ from an unnecessarily long representation.

**Dependencies and story role.** M03. This identifies the environment dimension that will bound the query overhead.

**Conceptual connection.** A channel's rank counts a minimal environmental representation; it does not measure how close the channel is to the identity.

**Sources.** Watrous §2.2.2 and Theorem 2.22, [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [Convex code, §1](../science/convex-code.md#1-complementary-states-of-computational-basis-addresses).

### M05. What the environment learns

**Central question.** Which part of the same isometric evolution describes information lost to the environment?

**Understanding target.** Obtain the complementary output by tracing out the accessible output instead of the environment. Explain how different environment states can reveal a logical label and reduce coherence.

**Dependencies and story role.** M02–M04. This shifts attention from the visible noisy state to the information responsible for its loss of coherence.

**Conceptual connection.** Watrous's Stinespring representation supplies the joint evolution; the project explicitly defines and uses its other marginal.

**Sources.** Watrous §2.2.2, [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [Convex code, §1](../science/convex-code.md#1-complementary-states-of-computational-basis-addresses); [Interpretation: the protected copy](../science/interpretation.md#why-the-protected-copy-is-not-enough-by-itself).

### M06. Affine coordinates and physical mixtures

**Central question.** How does expressing one state in affine coordinates differ from preparing a probabilistic mixture?

**Understanding target.** Distinguish an affine combination, whose coefficients sum to one but may be negative, from a convex combination with nonnegative weights. Interpret affine dimension as the number of independent directions among the relevant states.

**Dependencies and story role.** M03 and M05. This supplies the geometric distinction needed before negative barycentric coefficients appear in the construction.

**Conceptual connection.** Affine coordinates describe geometry; only a subsequent conversion into nonnegative weights gives a physical preparation.

**Sources.** [Convex code, §2](../science/convex-code.md#2-a-common-mixture-with-a-prescribed-contribution); [Related work: classical convex geometry](../references/related-work.md#the-convex-geometry-is-classical). This geometric argument is supplied locally, rather than assigned to the educational anchor.

### M07. Inner products and common error Gram matrices

**Central question.** What information is retained by the pairwise inner products of a set of error vectors?

**Understanding target.** Interpret a Gram matrix and explain why two families with the same Gram matrix can be aligned coherently on their spans. Recognize why relative phases must be aligned consistently across logical labels.

**Dependencies and story role.** M02 and M04. This prepares the linear-algebra mechanism behind the explicit recovery.

**Conceptual connection.** Equal error statistics alone are not the whole issue; a common Gram matrix preserves the inner products needed for one coherent decoder.

**Sources.** [Convex code, §4 and Proposition 3](../science/convex-code.md#proposition-3-a-known-controlled-recovery).

### M08. Exact recovery as a channel identity

**Central question.** What must a recovery accomplish on an encoded logical state?

**Understanding target.** Interpret exact correction as encoding, noise and recovery composing to the logical identity. Distinguish a known channel-dependent decoder from a decoder that would require the unknown oracle function.

**Dependencies and story role.** M03–M05 and M07. This states the recovery objective before choosing a particular code.

**Conceptual connection.** Environmental independence and common error moments connect information leakage to the possibility of a physical recovery operation.

**Sources.** [Convex code, §4](../science/convex-code.md#4-exact-correction-including-reference-systems); [Related work: error correction and common moments](../references/related-work.md#error-correction-and-common-moment-constructions). The recovery theorem and construction have their own primary attribution.

### M09. Logical inputs with a reference

**Central question.** Why is checking the action on isolated basis inputs insufficient for a coherent subroutine?

**Understanding target.** Explain how a logical system can be correlated with an untouched reference. Distinguish preservation of basis populations from preservation of every logical coherence and reference correlation.

**Dependencies and story role.** M02–M03 and M08. This expands the success criterion to the input states a query algorithm may actually supply.

**Conceptual connection.** An untouched reference represents the rest of a computation, so a usable recovery must preserve the joint state rather than only a local marginal.

**Sources.** Watrous §3.3.2, [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf); [Convex code, §4](../science/convex-code.md#4-exact-correction-including-reference-systems).

### M10. Channel distance and observable error

**Central question.** Which error measure controls the action of a subroutine on reference-entangled inputs?

**Understanding target.** Interpret the unhalved diamond norm, its maximization over reference systems, and the maximum distance of two between channels. Relate total channel error $`\epsilon`$ to a change of at most $`\epsilon/2`$ in a final measurement-event probability.

**Dependencies and story role.** M03 and M09. This gives a quantitative version of the full-input-space requirement.

**Conceptual connection.** The operational meaning of channel distance connects an analytical norm bound to a final algorithm's observable behavior.

**Sources.** Watrous §3.1.1 and §§3.3.2–3.3.3, [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf); [Model and results, §2](../science/model-and-results.md#2-parameters-and-error-convention).

### M11. Composition and separately charged resources

**Central question.** How does a reliable query subroutine become part of a complete algorithm?

**Understanding target.** Explain why surrounding channels cannot increase diamond distance and why a hybrid replacement sums per-query errors. Keep oracle calls, known gates, preprocessing, memory and calibration as separate resource quantities.

**Dependencies and story role.** M01, M03 and M10. This connects one operation to an algorithm without identifying query count with total execution cost.

**Conceptual connection.** Composable accuracy makes substitution legitimate, while an explicit resource contract determines whether the substitution is also computationally efficient.

**Sources.** Watrous §§2.2.1 and 3.3.2, [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) and [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf); [Search and resources, §§3 and 5](../science/search-and-resources.md#3-arbitrary-boolean-functions-and-arbitrary-algorithms).

### M12. The complete access contract

**Central question.** What must the code and the physical oracle jointly preserve?

**Understanding target.** Assemble the exact model: known, fixed, function-independent, memoryless address noise after each bit query; protected response, logical memory, tags, controls and stored outputs; inaccessible fresh environments. Explain why correcting a known channel alone does not yet implement an unknown Boolean action.

**Dependencies and story role.** M01–M11. This closes the background phase by specifying the full task the construction must solve.

**Conceptual connection.** A correction code needs both environmental balance and a usable branch carrying the requested address. The answer eigenstates will later connect these requirements.

**Sources.** [Model and results, §1](../science/model-and-results.md#1-the-physical-oracle-and-its-accessible-outputs); [Interpretation: a correctable code carrying a query](../science/interpretation.md#why-a-correctable-code-can-still-carry-an-unknown-query).

## Phase II: narrative and innovation

### M13. The geometry of basis-address environment states

**Central question.** Which part of the noise channel controls the construction's designated query weight?

**Understanding target.** Form $`\sigma_x=\widehat\Phi(\lvert x\rangle\langle x\rvert)`$ and distinguish its affine dimension $`d`$ from Kraus rank $`r`$. Explain $`d\leq\min\{N-1,r^2-1\}`$ and the meaning of the singleton case $`d=0`$.

**Dependencies and story role.** M04–M06 and M12. This extracts the finite geometric problem from the physical channel.

**Conceptual connection.** The environment dimension bounds the space in which the address-dependent outputs can vary, while their actual geometry can be much smaller.

**Sources.** [Convex code, §1](../science/convex-code.md#1-complementary-states-of-computational-basis-addresses); [Model and results, §5](../science/model-and-results.md#5-what-the-environment-dimension-does-and-does-not-say).

### M14. A simplex that controls every address

**Central question.** How can a finite set of actual address states provide bounded affine coordinates for all the others?

**Understanding target.** Explain the maximum-volume simplex argument and why replacing one vertex bounds each barycentric coefficient in absolute value by one. Recognize that the selected simplex need not contain every state as a convex combination.

**Dependencies and story role.** M06 and M13. This produces the anchors and coefficient bounds used by the physical code.

**Conceptual connection.** A determinant comparison converts finite-dimensional geometry into a uniform statement over every oracle address.

**Sources.** [Convex code, Lemma 1](../science/convex-code.md#lemma-1-a-maximum-volume-simplex); [Classical geometric attribution](../references/related-work.md#the-convex-geometry-is-classical).

### M15. Nonnegative balancing weights

**Central question.** How do signed affine coordinates become a common physical mixture?

**Understanding target.** Explain why $`\eta=1/(d+1)`$ and $`p_j(x)=(1-\lambda_j(x))/(d+1)`$ are nonnegative normalized branch weights and make the average environmental state independent of $`x`$.

**Dependencies and story role.** M13–M14. This converts the geometric lemma into a preparation rule with a uniform designated-address contribution.

**Conceptual connection.** The coefficient bound supplies physical probabilities, while the affine identity cancels the address dependence of the environmental mixture.

**Sources.** [Convex code, Corollary 2](../science/convex-code.md#corollary-2-environmental-balance).

### M16. Protected tags realize the mixture coherently

**Central question.** How can a classical mixture condition define a coherent query code?

**Understanding target.** Construct $`\lvert\Theta_x\rangle`$ with a distinguished tag and separate anchor tags, keeping the protected logical label in $`X`$. Explain why tags remove branch cross terms and remain necessary when an address equals an anchor.

**Dependencies and story role.** M02, M12 and M15. This turns the balancing weights into the actual encoding isometry.

**Conceptual connection.** Orthogonal protected labels implement environmental averaging without measuring which branch will contribute the unknown query.

**Sources.** [Convex code, §3](../science/convex-code.md#3-the-protected-tagged-encoding); [Watrous bridge](watrous-bridge.md).

### M17. Environmental balance for every logical input

**Central question.** Why does the balanced code protect superpositions and their reference correlations?

**Understanding target.** Follow the traces over the retained logical label and branch tags to obtain $`\rho_R\otimes\tau`$ as the environment-reference output. Distinguish this full decoupling identity from a statement only about basis-state probabilities.

**Dependencies and story role.** M05, M09 and M16. This establishes the information-theoretic condition for exact correction of the code.

**Conceptual connection.** The protected labels remove the relevant cross terms in the complementary output, while the balancing identity removes the remaining dependence on the logical address.

**Sources.** [Convex code, §4](../science/convex-code.md#4-exact-correction-including-reference-systems).

### M18. A coherent decoder independent of the oracle

**Central question.** How can the common environmental state be converted into an explicit known recovery?

**Understanding target.** Use the common error Gram matrix to align normalized error vectors with fixed syndrome vectors. Explain why one eigendecomposition fixes coherent phases across logical labels, why zero eigenvalues are omitted, and why a unitary extension defines recovery outside the exact code span.

**Dependencies and story role.** M07–M08 and M17. This supplies the decoder used in the later approximate simulation.

**Conceptual connection.** Exact correction on the reference code and a CPTP extension to all inputs are different requirements, both needed when the routed query slightly leaves that code.

**Sources.** [Convex code, Proposition 3](../science/convex-code.md#proposition-3-a-known-controlled-recovery).

### M19. Several probes and the exact endpoint

**Central question.** What survives when several balanced probes are prepared coherently for the same logical address?

**Understanding target.** Explain why fresh environments give the common output $`\tau^{\otimes L}`$ and permit a product of controlled recoveries. Distinguish repeated basis-controlled preparation from cloning an arbitrary state. Recover exact one-call correction when $`d=0`$.

**Dependencies and story role.** M13 and M16–M18. This builds the recoverable multi-probe resource without yet applying the unknown query.

**Conceptual connection.** Memorylessness is used to factor the noise and its environment; it is not an assumption that the algorithm's logical input lacks correlations.

**Sources.** [Convex code, §5](../science/convex-code.md#5-several-probes-and-degenerate-cases).

### M20. Select exactly one designated branch

**Central question.** Why should the circuit select the first matching tag rather than activate every matching tag?

**Understanding target.** Explain the mutually exclusive first-match selectors and their reversible implementation on protected tags. Show conceptually why two applications of a Boolean phase could otherwise cancel.

**Dependencies and story role.** M12, M16 and M19. This begins the unknown-oracle part of the construction while preserving its coherent branch structure.

**Conceptual connection.** The same protected tags that enforce environmental balance also provide a control record that survives address noise.

**Sources.** [Oracle compiler, §2](../science/oracle-compiler.md#2-selecting-the-first-distinguished-branch).

### M21. Paid response routing for the full bit oracle

**Central question.** How can a standard bit oracle contribute either a phase or no phase without a free controlled-oracle primitive?

**Understanding target.** Use physical responses $`\lvert+\rangle`$ and $`\lvert-\rangle`$ for idle and active phase kickback, and explain their known unpreparation after each paid call. Include the protected logical answer $`Y`$ coherently and its Hadamard wrappers.

**Dependencies and story role.** M01–M02, M12 and M20. This implements the desired unknown action on the full logical address-answer space.

**Conceptual connection.** Standard bit access supplies the response eigenstates; a phase-only black box would require a different access argument. Anchor values need not be learned, although their branches still undergo paid noisy calls.

**Sources.** [Oracle compiler, §§2–3](../science/oracle-compiler.md#3-one-physical-query-for-each-probe).

### M22. Move noise past later routing

**Central question.** Why can arbitrary address noise be collected after the ideal routed action?

**Understanding target.** Identify which later operators act on other probes or protected controls and therefore commute with a given address error. Explain why the argument never moves an error through its own unknown oracle or through the final recovery.

**Dependencies and story role.** M04, M12 and M19–M21. This connects the actual noisy physical circuit with the exactly correctable product channel.

**Conceptual connection.** Scheduling and protected storage replace a diagonal-noise assumption. A fixed physical port can be reused by swaps, provided its noisy outputs are retained until decoding.

**Sources.** [Oracle compiler, §4](../science/oracle-compiler.md#4-moving-arbitrary-address-noise-to-the-end) and [§7](../science/oracle-compiler.md#7-a-single-physical-port-and-protected-storage).

### M23. From a missed branch to a uniform error bound

**Central question.** How does a branch probability control the error of the whole logical channel?

**Understanding target.** Interpret $`q=(1-\eta)^L`$ and the identity $`V_{\mathrm{miss}}^\dagger V_{\mathrm{miss}}=qI`$. Connect the resulting isometry error $`2\sqrt q`$ to the unhalved diamond bound $`\min\{2,4\sqrt q\}`$ after noise and recovery.

**Dependencies and story role.** M09–M10 and M18–M22. This completes the single-query theorem for arbitrary Boolean functions and references.

**Conceptual connection.** The no-match branch is retained, not postselected away. Uniform operator control converts its weight into a composable channel guarantee.

**Sources.** [Oracle compiler, §5](../science/oracle-compiler.md#5-error-bound-on-the-whole-logical-input-space); [Model and results, Theorem 1](../science/model-and-results.md#theorem-1).

### M24. Compile an adaptive query algorithm

**Central question.** How does the single-query guarantee extend to an algorithm with intermediate operations and records?

**Understanding target.** Allocate $`\delta=\epsilon/T`$ and derive the physical-call scaling $`O((d+1)T\log(4T/\epsilon))`$. Explain why a reference-uniform bound permits measurements, classical feedforward and retained quantum memory between queries.

**Dependencies and story role.** M11–M12 and M23. This turns a corrected query into an algorithm-independent simulation statement.

**Conceptual connection.** The hybrid sum controls accumulated error while the product-noise assumption applies only to the physical environments, not to algorithmic inputs.

**Sources.** [Oracle compiler, §6](../science/oracle-compiler.md#6-physical-call-count-and-composition); [Model and results, Corollary 2](../science/model-and-results.md#corollary-2).

### M25. The sharper channel for one marked address

**Central question.** What extra structure is available when the Boolean function has a unique mark?

**Understanding target.** Explain why the controlled-phase basis has only one negative logical label, $`(w,1)`$, and use common-syndrome overlaps to obtain $`(1-q)\mathrm{Ad}_{U_w}+q\mathrm{id}`$. Distinguish this exact full-bit identity from the universal arbitrary-function bound.

**Dependencies and story role.** M07, M18, M21 and M23. This extracts the special structure that sharpens the search analysis.

**Conceptual connection.** A single active logical label fixes all relevant environment overlaps; several marked labels need additional overlaps and do not automatically give the same mixture.

**Sources.** [Search and resources, §2](../science/search-and-resources.md#2-exact-logical-channel-for-a-unique-marked-address), including [the full-bit argument](../science/search-and-resources.md#the-full-bit-oracle).

### M26. Search with a counted verification call

**Central question.** What search advantage follows from the compiled query, and what does a final candidate check cost?

**Understanding target.** Combine Grover's ideal query count with the unique-mark channel to obtain $`O(r^2\sqrt N\log N)`$ physical calls at fixed error. Explain why one additional basis query verifies the measured candidate exactly in its protected response.

**Dependencies and story role.** M24–M25. This gives a concrete algorithmic consequence and connects the channel guarantee to a decision or search outcome.

**Conceptual connection.** Post-address noise can change the queried address output without changing the answer bit already written. The ordinary $`\Omega(\sqrt N)`$ lower bound does not establish optimal rank dependence or a matching logarithmic factor.

**Sources.** [Search and resources, §4](../science/search-and-resources.md#4-search-and-verification), with its cited primary search results.

### M27. An explicit balanced probe for global rank-two noise

**Central question.** Can environmental balance be realized without searching for a simplex or loading a coefficient table?

**Understanding target.** Examine the phase-gradient channel and the two addresses separated by $`N/4`$. Explain their orthogonal environmental vectors, their common average $`I_E/2`$, and the designated weight $`\eta=1/2`$.

**Dependencies and story role.** M04–M06 and M15–M19. This begins an explicit circuit realization of the abstract theorem; the bridge's $`N=4`$ example makes the construction concrete.

**Conceptual connection.** Channel structure can supply a better encoding than the generic dimensional guarantee. Rank two permits strong global noise here and does not mean the channel approaches the identity.

**Sources.** [Structured example, §1](../science/structured-example.md#1-channel-and-encoded-probe); [Watrous bridge](watrous-bridge.md).

### M28. Recover the syndrome and charge the circuit

**Central question.** How does the explicit code become an efficient implementation?

**Understanding target.** Follow reversible address preparation, its inverse, the $`HS^\dagger`$ syndrome decoder and the known logical phase correction. Connect the circuit to $`O(nL)`$ known elementary gates and protected qubits before finite-set synthesis, with $`n=\log_2N`$.

**Dependencies and story role.** M18, M20–M22 and M27. This turns the structured encoding into a complete compiled query with counted controls and storage.

**Conceptual connection.** Known formulas replace generic address-dependent tables. Reusable width allows syndrome discard/reset; retaining every syndrome instead requires accumulated storage. No QRAM is supplied for free.

**Sources.** [Structured example, §§2–5](../science/structured-example.md#2-preparation-using-elementary-reversible-gates); [Search and resources, §5](../science/search-and-resources.md#5-what-the-abstract-query-theorem-charges).

### M29. Allocate approximation and model errors

**Central question.** What accuracy must known controls and the channel description have in a complete computation?

**Understanding target.** Separate missed-branch error, known-gate approximation and actual-versus-design channel mismatch. Interpret the budget $`4T(1-\eta)^{L/2}+2\sum_j\zeta_j+TL\delta_\Phi`$ and the sharper first term for a unique mark.

**Dependencies and story role.** M10–M11, M24 and M28. This supplies the operational precision conditions needed to turn the explicit circuit into an end-to-end resource statement.

**Conceptual connection.** An irrelevant overall phase of a complete elementary operation must be distinguished from a relative phase under control. Efficient synthesis does not provide free calibration or tolerance of a fixed unknown mismatch as the algorithm grows.

**Sources.** [Search and resources, §6](../science/search-and-resources.md#6-finite-control-precision-and-channel-mismatch); [Structured example, §§6–7](../science/structured-example.md#6-finite-precision-and-noise-model-mismatch).

### M30. The complete theorem, its evidence and its boundary

**Central question.** What does the construction establish about noise and coherent query power?

**Understanding target.** Reconstruct the chain from complementary-state geometry to balanced coding, paid full-bit routing, reference-uniform error and algorithmic consequences. Distinguish a sufficient rank bound from a classification, the generic query theorem from the efficient structured family, and finite numerical checks from the analytical proof.

**Dependencies and story role.** M12–M29. This closes the narrative by integrating the mechanism, consequence, resource conditions and interpretation.

**Conceptual connection.** Environmental information and accessible error syndromes explain why strong post-query address noise can coexist with coherent algorithms under this access model. Fourier-basis dephasing, the faulty-oracle comparison and the remaining overhead gaps show why the exact assumptions and inherited ingredients matter.

**Sources.** [Interpretation](../science/interpretation.md); [Model and results, §§5–7](../science/model-and-results.md#5-what-the-environment-dimension-does-and-does-not-say); [Related work](../references/related-work.md); [Verification scope](../verification/README.md#scope).
