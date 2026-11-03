#!/usr/bin/env python3
"""Finite channel checks for the single-use post-address oracle compiler.

The physical simulation orders response preparation, U_f, address noise, and
response unpreparation explicitly. Full-bit checks include both target Hadamards
and build the complete normalized Choi matrix from shared Kraus trajectories.
No network, quantum SDK, SDP solver, or external data is required.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


TOLERANCE = 2e-10
HADAMARD = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def apply_axis(state: np.ndarray, matrix: np.ndarray, axis: int) -> np.ndarray:
    return np.moveaxis(np.tensordot(matrix, state, axes=(1, axis)), 0, axis)


def tensor(vectors: list[np.ndarray]) -> np.ndarray:
    result = np.array([1.0 + 0j])
    for vector in vectors:
        result = np.kron(result, vector)
    return result


def complete_basis(vectors: list[np.ndarray], dimension: int) -> np.ndarray:
    """Deterministic twice-reorthogonalized completion by standard basis vectors."""
    columns: list[np.ndarray] = []
    sources = list(vectors) + list(np.eye(dimension, dtype=complex))
    for source in sources:
        vector = np.array(source, dtype=complex)
        for _ in range(2):
            for column in columns:
                vector -= column * np.vdot(column, vector)
        length = np.linalg.norm(vector)
        if length > 1e-11:
            columns.append(vector / length)
        if len(columns) == dimension:
            break
    result = np.column_stack(columns)
    require(np.max(np.abs(result.conj().T @ result - np.eye(dimension))) < TOLERANCE,
            "Recovery completion is not unitary")
    return result


def canonical_qr(matrix: np.ndarray) -> np.ndarray:
    """QR isometry with positive-real diagonal in its triangular factor."""
    q, r = np.linalg.qr(matrix)
    diagonal = np.diag(r)
    phases = diagonal / np.abs(diagonal)
    return q * phases[np.newaxis, :]


@dataclass
class Code:
    N: int
    eta: float
    states: list[np.ndarray]
    recoveries: list[np.ndarray]
    metadata: dict[str, Any]


def simplex_code(kraus: list[np.ndarray]) -> Code:
    """Construct the finite maximum-volume-simplex code and an exact recovery."""
    rank = len(kraus)
    N = kraus[0].shape[0]
    tp_error = float(np.linalg.norm(sum(k.conj().T @ k for k in kraus) - np.eye(N)))
    require(tp_error < TOLERANCE, "Input Kraus operators are not trace preserving")
    # These Gram matrices are transposes of the complementary states. Transpose
    # is an invertible real-linear map, so their barycentric geometry is identical.
    points = np.array([[[np.vdot(a[:, x], b[:, x]) for b in kraus]
                        for a in kraus] for x in range(N)])
    features = np.array([[point[a, a].real for a in range(rank)]
                         + [point[a, b].real for a in range(rank) for b in range(a+1, rank)]
                         + [point[a, b].imag for a in range(rank) for b in range(a+1, rank)]
                         for point in points])
    centered = features - features[0]
    _, singular, vh = np.linalg.svd(centered, full_matrices=False)
    d = int(np.sum(singular > 1e-11))
    coordinates = centered @ vh[:d].T
    affine = np.c_[np.ones(N), coordinates]
    anchors = max(itertools.combinations(range(N), d+1),
                  key=lambda indices: abs(np.linalg.det(affine[list(indices)])))
    barycentric = np.linalg.solve(affine[list(anchors)].T, affine.T).T
    require(np.max(np.abs(barycentric)) <= 1 + TOLERANCE,
            "Maximum-volume barycentric bound failed")
    m = d+1
    # An anchor's barycentric coordinates are mathematically a standard basis
    # vector. Set them exactly to avoid taking square roots of roundoff-sized
    # spurious probabilities at those known boundary points.
    barycentric[list(anchors)] = np.eye(m)
    eta = 1/m
    gram = np.mean(points[list(anchors)], axis=0)
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    # Fix eigenvector phases for a reproducible extension outside the code span.
    for column in range(rank):
        first = np.flatnonzero(np.abs(eigenvectors[:, column]) > 1e-12)[0]
        phase = eigenvectors[first, column] / abs(eigenvectors[first, column])
        eigenvectors[:, column] /= phase
    active = np.flatnonzero(eigenvalues > 1e-12)
    rotated = [sum(eigenvectors[b, a]*kraus[b] for b in range(rank)) for a in active]
    positive_eigenvalues = eigenvalues[active]
    states: list[np.ndarray] = []
    recoveries: list[np.ndarray] = []
    gram_error = 0.0
    for x in range(N):
        theta = np.zeros((m+1, N), dtype=complex)
        theta[0, x] = math.sqrt(eta)
        for j, anchor in enumerate(anchors):
            theta[j+1, anchor] = math.sqrt(max(0.0, (1-barycentric[x, j])/m))
        actual_gram = np.array([[np.vdot(theta @ a.T, theta @ b.T) for b in kraus]
                                for a in kraus])
        gram_error = max(gram_error, float(np.max(np.abs(actual_gram-gram))))
        normalized_errors = [(theta @ k.T).reshape(-1)/math.sqrt(gamma)
                             for k, gamma in zip(rotated, positive_eigenvalues)]
        recovery = complete_basis(normalized_errors, (m+1)*N).conj().T
        states.append(theta)
        recoveries.append(recovery)
    require(gram_error < TOLERANCE, "Complement equalization failed")
    commutator = max(float(np.linalg.norm(a @ b-b @ a)) for a in points for b in points)
    metadata = {
        "address_dimension": N,
        "kraus_rank": rank,
        "affine_dimension": d,
        "eta": eta,
        "anchors": list(anchors),
        "minimum_barycentric_coefficient": float(np.min(barycentric)),
        "maximum_absolute_barycentric_coefficient": float(np.max(np.abs(barycentric))),
        "common_gram_eigenvalues": positive_eigenvalues.tolist(),
        "maximum_complement_commutator_norm": commutator,
        "trace_preservation_residual": tp_error,
        "common_gram_residual": gram_error,
    }
    return Code(N, eta, states, recoveries, metadata)


def structured_code(N: int) -> tuple[list[np.ndarray], Code]:
    """The explicit N/4-shift code and circuit-derived syndrome recovery."""
    require(N >= 4 and N & (N-1) == 0, "Structured fixture needs N=2^n, n>=2")
    phases = np.exp(2j*np.pi*np.arange(N)/N)
    unitaries = [np.diag(phases), np.diag(phases.conj())]
    kraus = [unitary/math.sqrt(2) for unitary in unitaries]
    decoder = HADAMARD @ np.diag([1, -1j])  # H S^dagger
    states, recoveries = [], []
    max_recovery_error = 0.0
    for x in range(N):
        theta = np.zeros((2, N), dtype=complex)
        theta[0, x] = theta[1, (x+N//4) % N] = 1/math.sqrt(2)
        # Inverse controlled addition, then CNOT-copy uncomputation (XOR x).
        undo_address = np.zeros((2*N, 2*N), dtype=complex)
        for tag in range(2):
            for address in range(N):
                output = ((address-tag*(N//4)) % N) ^ x
                undo_address[tag*N+output, tag*N+address] = 1
        correction = np.diag([phases[x].conjugate(), phases[x]])
        recovery = np.kron(correction @ decoder, np.eye(N)) @ undo_address
        for syndrome, unitary in enumerate(unitaries):
            actual = recovery @ (theta @ unitary.T).reshape(-1)
            expected = np.zeros(2*N, dtype=complex)
            expected[syndrome*N] = 1
            max_recovery_error = max(max_recovery_error,
                                     float(np.max(np.abs(actual-expected))))
        states.append(theta)
        recoveries.append(recovery)
    require(max_recovery_error < TOLERANCE, "Explicit syndrome decoder failed")
    code = Code(N, .5, states, recoveries, {
        "address_dimension": N,
        "kraus_rank": 2,
        "eta": .5,
        "tag_dimension": 2,
        "shift": N//4,
        "explicit_decoder_vector_residual": max_recovery_error,
    })
    return kraus, code


def physical_branch(theta: np.ndarray, recovery: np.ndarray,
                    kraus: list[np.ndarray], labels: tuple[int, ...],
                    marked: set[int], target_input: int,
                    bit_wrappers: bool) -> tuple[np.ndarray, float, float]:
    """Apply the physical circuit, retaining logical target and all syndromes.

    The protected logical address is fixed to one basis label for this column.
    Different columns later share the same environment labels, retaining every
    address/target/reference coherence in the reconstructed channel.
    """
    L = len(labels)
    B, N = theta.shape
    dimensions = [2] + [B, N, 2]*L
    target = np.eye(2, dtype=complex)[:, target_input]
    if bit_wrappers:
        target = HADAMARD @ target
    probe = np.kron(theta.reshape(-1), np.array([1, 0], dtype=complex))
    source = np.kron(target, tensor([probe]*L)).reshape(dimensions)
    indices = np.indices(dimensions, sparse=True)
    target_one = indices[0] == 1
    state = source
    first_masks = []
    for j in range(L):
        tag_axis, address_axis, answer_axis = 1+3*j, 2+3*j, 3+3*j
        first = indices[tag_axis] == 0
        for k in range(j):
            first = first & (indices[1+3*k] != 0)
        first_masks.append(first)
        answer_one = indices[answer_axis] == 1
        response_phase = np.where(first & target_one & answer_one, -1, 1)
        state = apply_axis(state, HADAMARD, answer_axis)
        state = state * response_phase
        oracle_flip = np.isin(indices[address_axis], list(marked))
        state = np.where(oracle_flip, np.flip(state, axis=answer_axis), state)
        state = apply_axis(state, kraus[labels[j]], address_axis)
        state = state * response_phase
        state = apply_axis(state, HADAMARD, answer_axis)
    # Separate reference route: ideal first-match phase, THEN all address noise.
    ideal_phase = np.ones(dimensions, dtype=float)
    for j in range(L):
        sign = first_masks[j] & target_one & np.isin(indices[2+3*j], list(marked))
        ideal_phase *= np.where(sign, -1, 1)
    pushed = source * ideal_phase
    for j in range(L):
        pushed = apply_axis(pushed, kraus[labels[j]], 2+3*j)
    commutation_error = float(np.max(np.abs(state-pushed)))
    # All physical responses should be zero before reuse. Do not silently
    # discard a response error: its total probability is checked below.
    selectors = (slice(None),) + tuple(0 if axis % 3 == 2 else slice(None)
                                      for axis in range(3*L))
    without_answers = state[selectors]
    answer_leakage = max(0.0, float(np.vdot(state, state).real
                                   - np.vdot(without_answers, without_answers).real))
    output = without_answers.reshape([2] + [B*N]*L)
    for j in range(L):
        output = apply_axis(output, recovery, j+1)
    if bit_wrappers:
        output = apply_axis(output, HADAMARD, 0)
    return output.reshape(2, -1), commutation_error, answer_leakage


def phase_check(kraus: list[np.ndarray], code: Code, L: int, marked: int) -> dict[str, Any]:
    trajectories = list(itertools.product(range(len(kraus)), repeat=L))
    outputs = []
    max_commutation = max_response = 0.0
    for theta, recovery in zip(code.states, code.recoveries):
        rows = []
        for labels in trajectories:
            output, residual, leakage = physical_branch(theta, recovery, kraus, labels,
                                                        {marked}, 1, False)
            rows.append(output.reshape(-1))
            max_commutation = max(max_commutation, residual)
            max_response = max(max_response, leakage)
        outputs.append(rows)
    multiplier = np.array([[sum(np.vdot(outputs[y][a], outputs[x][a])
                               for a in range(len(trajectories)))
                            for y in range(code.N)] for x in range(code.N)])
    signs = np.ones(code.N)
    signs[marked] = -1
    q = (1-code.eta)**L
    expected = (1-q)*np.outer(signs, signs) + q*np.ones((code.N, code.N))
    channel_residual = float(np.max(np.abs(multiplier-expected)))
    require(max(max_commutation, max_response, channel_residual) < TOLERANCE,
            "Unique-mark phase channel failed")
    return {"kind":"unique_mark_phase", "L":L, "marked":marked,
            "miss_probability":q, "physical_commutation_residual":max_commutation,
            "response_leakage_probability":max_response,
            "exact_channel_entry_residual":channel_residual}


def ideal_bit_matrix(N: int, marked: set[int]) -> np.ndarray:
    unitary = np.zeros((2*N, 2*N), dtype=complex)
    for x in range(N):
        for target in range(2):
            unitary[2*x+(target ^ int(x in marked)), 2*x+target] = 1
    return unitary


def bit_check(kraus: list[np.ndarray], code: Code, L: int,
              marked: set[int]) -> dict[str, Any]:
    trajectories = list(itertools.product(range(len(kraus)), repeat=L))
    D = 2*code.N
    local_dimension = code.states[0].size
    syndrome_dimension = local_dimension**L
    # K[o,i,e] is a full logical-bit Kraus representation; environment e includes
    # BOTH physical-noise trajectories and all recovered/discarded syndromes.
    operators = np.zeros((D, D, len(trajectories)*syndrome_dimension), dtype=complex)
    max_commutation = max_response = 0.0
    for x, (theta, recovery) in enumerate(zip(code.states, code.recoveries)):
        for target_input in range(2):
            for a, labels in enumerate(trajectories):
                output, residual, leakage = physical_branch(theta, recovery, kraus, labels,
                                                            marked, target_input, True)
                operators[2*x:2*x+2, 2*x+target_input,
                          a*syndrome_dimension:(a+1)*syndrome_dimension] = output
                max_commutation = max(max_commutation, residual)
                max_response = max(max_response, leakage)
    flat = operators.reshape(D*D, -1)
    choi = flat @ flat.conj().T / D
    trace_output = np.einsum("oioj->ij", choi.reshape(D, D, D, D))
    tp_residual = float(np.max(np.abs(trace_output-np.eye(D)/D)))
    smallest_eigenvalue = float(np.min(np.linalg.eigvalsh(choi)))
    require(max(max_commutation, max_response, tp_residual) < TOLERANCE,
            "Full-bit physical/trace-preservation check failed")
    require(smallest_eigenvalue > -TOLERANCE, "Full-bit Choi matrix is not positive")
    unitary = ideal_bit_matrix(code.N, marked)
    unitary_vector = unitary.reshape(-1)/math.sqrt(D)
    ideal_choi = np.outer(unitary_vector, unitary_vector.conj())
    q = (1-code.eta)**L
    result = {"kind":"full_bit_choi", "L":L, "marked":sorted(marked),
              "logical_dimension":D, "reference_dimension":D,
              "miss_probability":q, "physical_commutation_residual":max_commutation,
              "response_leakage_probability":max_response,
              "choi_trace_preservation_residual":tp_residual,
              "choi_minimum_eigenvalue":smallest_eigenvalue,
              "choi_trace_norm_error_to_ideal":float(np.linalg.norm(choi-ideal_choi, ord='nuc')),
              "proved_diamond_upper_bound":min(2.0, 4*math.sqrt(q))}
    if len(marked) <= 1:
        identity_vector = np.eye(D).reshape(-1)/math.sqrt(D)
        expected = (1-q)*ideal_choi + q*np.outer(identity_vector, identity_vector.conj())
        residual = float(np.max(np.abs(choi-expected)))
        require(residual < TOLERANCE, "Exact full-bit faulty-channel identity failed")
        result["exact_faulty_bit_choi_residual"] = residual
    # A target in |+> makes every Boolean bit oracle idle. Test this on a state
    # maximally entangled between the logical address and a retained reference.
    psi = np.zeros((D, code.N), dtype=complex)
    for x in range(code.N):
        psi[2*x:2*x+2, x] = 1/math.sqrt(2*code.N)
    output = np.einsum("oie,ir->ore", operators, psi).reshape(D*code.N, -1)
    rho = output @ output.conj().T
    expected = np.outer(psi.reshape(-1), psi.reshape(-1).conj())
    idle_residual = float(np.max(np.abs(rho-expected)))
    require(idle_residual < TOLERANCE, "Entangled-address idle-target identity failed")
    result["entangled_address_plus_target_residual"] = idle_residual
    return result


def suite() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    rng = np.random.default_rng(482371)
    raw = rng.normal(size=(5, 5)) + 1j*rng.normal(size=(5, 5))
    unitary = canonical_qr(raw)
    damp0 = np.eye(5)
    damp0[1, 1] = math.sqrt(.35)
    damp1 = np.zeros((5, 5))
    damp1[0, 1] = math.sqrt(.65)
    kraus = [damp0 @ unitary, damp1 @ unitary]
    code = simplex_code(kraus)
    nonanchor = next(x for x in range(code.N) if x not in code.metadata["anchors"])
    require(code.metadata["minimum_barycentric_coefficient"] < -.1,
            "Fixture no longer tests a negative barycentric coefficient")
    require(code.metadata["maximum_complement_commutator_norm"] > .01,
            "Fixture no longer tests noncommuting complementary states")
    checks = [phase_check(kraus, code, 1, code.metadata["anchors"][0]),
              phase_check(kraus, code, 2, nonanchor),
              bit_check(kraus, code, 2, {nonanchor}),
              bit_check(kraus, code, 2, {1, 3, 4})]
    results.append({"fixture":"five_level_globally_rotated_amplitude_damping",
                    "seed":482371, "geometry":code.metadata, "checks":checks})

    rng = np.random.default_rng(482372)
    raw = rng.normal(size=(8, 4)) + 1j*rng.normal(size=(8, 4))
    isometry = canonical_qr(raw)
    kraus = [isometry[:4], isometry[4:]]
    code = simplex_code(kraus)
    checks = [bit_check(kraus, code, 2, {1}), bit_check(kraus, code, 2, {0, 2})]
    results.append({"fixture":"global_rank_two_random_stinespring",
                    "seed":482372, "geometry":code.metadata, "checks":checks})

    _, larger_code = structured_code(8)
    kraus, code = structured_code(4)
    checks = [phase_check(kraus, code, 3, 1),
              bit_check(kraus, code, 3, {2}),
              bit_check(kraus, code, 3, {0, 1})]
    results.append({"fixture":"explicit_two_branch_phase_gradient",
                    "geometry":code.metadata,
                    "additional_eight_address_decoder_check":larger_code.metadata,
                    "checks":checks})
    return {"schema_version":1, "tolerance":TOLERANCE,
            "query_model":"fixed_known_memoryless_post_address_bit_oracle",
            "fixtures":results}


def compare_expected(actual: Any, expected: Any, path: str = "report") -> None:
    """Tolerant numerical comparison; structure and discrete metadata are exact."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(),
                f"Expected-output keys differ at {path}")
        for key in expected:
            compare_expected(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected),
                f"Expected-output list differs at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare_expected(left, right, f"{path}[{index}]")
    elif isinstance(expected, float):
        require(math.isclose(actual, expected, rel_tol=5e-9, abs_tol=5e-9),
                f"Expected-output number differs at {path}: {actual} vs {expected}")
    else:
        require(actual == expected, f"Expected-output value differs at {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="compare against committed expected-results.json")
    arguments = parser.parse_args()
    report = suite()
    if arguments.check:
        expected_path = Path(__file__).with_name("expected-results.json")
        compare_expected(report, json.loads(expected_path.read_text()))
        count = sum(len(fixture["checks"]) for fixture in report["fixtures"])
        print(f"PASS: {count} scoped channel checks, 3 noise fixtures, complete full-bit Choi checks.")
        print("All invariant residuals satisfy 2e-10; committed numerical output agrees within tolerance.")
    else:
        print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
