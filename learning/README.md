# Learning route

The single educational anchor is **John Watrous, [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/) (2018)**. The route uses its descriptions of states, channels, Kraus and Stinespring representations, and channel distances. The repository supplies the additional convex geometry, explicit recovery and oracle-routing argument.

Start with [From Watrous to coherent queries through address noise](watrous-bridge.md). It translates the notation, identifies the relevant textbook sections, and works through the four-address phase-gradient example from preparation to recovery and the full logical bit query. The book is a foundation to consult alongside the explanation; reading all of it is unnecessary.

## The thirty-milestone map

The [milestone map](milestones.md) develops the project in two phases:

| Phase | Route | Endpoint |
|---|---|---|
| Background and preliminaries, M01–M12 | Registers and coherence, channels and environments, geometric mixtures, recovery, reference systems and operational error | The exact task and the resources the compiler may use |
| Narrative and innovation, M13–M30 | Complementary-state geometry, balanced probes, known recovery, paid full-bit routing, uniform error, search, explicit circuitry and precision | The complete theorem, its algorithmic consequence and its scope |

Each milestone states a central question, understanding target, earlier dependencies, conceptual connection and source pointers. The 12/18 allocation gives the channel framework enough space before following the longer construction. Both phases build from individual objects toward the complete task or result.

## Keep the scientific distinctions visible

A correct answer bit does not by itself establish coherent oracle simulation. The protected logical answer and arbitrary references are part of the target channel. Likewise, a small query count does not make a generic encoder or recovery efficient. The explicit phase-gradient family provides the separately charged gate implementation.

The [scientific guide](../science/README.md) is the direct route to complete proofs and exact assumptions. [Related work](../references/related-work.md) credits the primary research ingredients beyond the educational anchor. The [verification guide](../verification/README.md) explains what the finite calculations check and why they do not replace the analytical theorem.
