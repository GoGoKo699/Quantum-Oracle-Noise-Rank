# Scientific reading guide

The question is whether a bounded noise environment is enough to preserve coherent Boolean-query power, even when the address noise is strong and global. Under the exact post-query, known-channel model, the answer is a constructive sufficient guarantee. The affine geometry of complementary outputs supplies an error-correcting probe with a uniform amount of the desired query; protected response routing amplifies that amount without reusing a noisy address.

## The connected account

| Read | Question answered |
|---|---|
| [Model and results](model-and-results.md) | What physical oracle is supplied, what remains protected, and which simulation bounds are established? |
| [Balanced query code](convex-code.md) | How can every logical address leave the same environmental state while retaining a known positive weight on its own physical query? |
| [Oracle compiler](oracle-compiler.md) | How is the unknown Boolean action applied coherently, and why can arbitrary post-query address noise be corrected afterward? |
| [Search and resources](search-and-resources.md) | What is the exact unique-mark channel, how does error accumulate, and which preparation, memory and precision costs must be charged? |
| [Structured example](structured-example.md) | Can the general query theorem be realized with efficient known gates for a globally supported rank-two channel? |
| [Interpretation](interpretation.md) | What does this establish about the role of the noise environment, and which stronger conclusions remain unsupported? |

The code and compiler are the two main proof dependencies. Search is a consequence of the coherent-query theorem, with a sharper exact channel identity for a unique marked address. The structured example uses an explicit two-branch code in place of generic simplex selection; the same routing and error analysis apply.

## Focused routes

- **Check the theorem:** read the access contract and Theorem 1 in [Model and results](model-and-results.md), followed by the complete [code](convex-code.md) and [compiler](oracle-compiler.md) proofs.
- **Inspect the implementation claim:** read [Structured example](structured-example.md) and its precision budget, then reproduce the [finite channel checks](../verification/README.md).
- **Assess the relation to previous work:** read [Related work](../references/related-work.md), especially the oracle-distillation comparison and the distinction from function-dependent faulty oracles.

All channel distances are unhalved diamond norms. The address label is $`x`$, the protected logical registers are $`X,Y`$, and $`T`$ counts ideal queries. The common parameter definitions live in [Model and results](model-and-results.md#2-parameters-and-error-convention).
