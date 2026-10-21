"""Unit, negative, integration, end-to-end, and mutation checks for the exact Majorana slice.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem trichotomy_pairwise_disjoint
Claim: urn:omega:fqm:ms-majorana:l5a-exact-slice:harness:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent harness mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: The harness falsifies these certificates. It does not certify a device, a continuum limit, or AuthorityEffect.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

CODE = Path(__file__).resolve().parents[2]
PACKAGE = "majcode_l5a"


class HarnessFault(RuntimeError):
    """The falsification harness could not execute a declared mutant."""

    def __init__(self, invariant: str, parameters: dict[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else parameters
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def handshake_expected(edge_count: int) -> int:
    return edge_count * 2


def ising_sigma_target() -> int:
    return 2


def gram_trace_target() -> int:
    return 5


def radical_of_twelve() -> int:
    return 3


def _ensure_package() -> str:
    if PACKAGE not in sys.modules:
        module = types.ModuleType(PACKAGE)
        module.__path__ = [str(CODE)]
        sys.modules[PACKAGE] = module
    return PACKAGE


def _module(name: str) -> types.ModuleType:
    return importlib.import_module(f"{_ensure_package()}.{name}")


def _load_source(source: str, name: str) -> dict[str, object]:
    package = _ensure_package()
    qualified = f"{package}.{name}"
    spec = importlib.util.spec_from_loader(qualified, loader=None)
    if spec is None:
        raise HarnessFault("could not allocate a mutant module", {"name": name})
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package
    module.__file__ = str(CODE / "tests" / "unit" / "test_l5a_exact_slice.py")
    sys.modules[qualified] = module
    exec(compile(source, qualified + ".py", "exec"), module.__dict__)
    return module.__dict__


def _message(error: type[BaseException], probe: Callable[[], object]) -> str | None:
    try:
        probe()
    except error as caught:
        return str(caught)
    return None


def _invariant(error: type[BaseException], probe: Callable[[], object]) -> str | None:
    try:
        probe()
    except error as caught:
        text = getattr(caught, "invariant", None)
        if isinstance(text, str):
            return text
        return None
    return None


def _refused(namespace: dict[str, object], error_name: str, probes: Sequence[tuple[Callable[[], object], str]]) -> bool:
    error = namespace[error_name]
    if not isinstance(error, type):
        return False
    for probe, invariant in probes:
        if _invariant(error, probe) != invariant:
            return False
    return True


def _killed(source: str, mutants: Sequence[tuple[str, str, str]], oracle: Callable[[dict[str, object]], bool], prefix: str) -> int:
    killed = 0
    for index, (name, old, new) in enumerate(mutants):
        if source.count(old) != 1:
            raise HarnessFault("mutant site is not unique", {"name": name, "count": source.count(old)})
        try:
            survived = oracle(_load_source(source.replace(old, new, 1), f"{prefix}_{index}"))
        except Exception:
            survived = False
        if survived:
            raise HarnessFault("mutant survived", {"name": name, "prefix": prefix})
        killed += 1
    return killed


def _adjacency_known(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_handshaking"]
    build = namespace["build_adjacency"]
    if not callable(certify) or not callable(build):
        return False
    try:
        certificate = certify(("a", "b", "c"), (("a", "b"), ("b", "c")))
        built = build(("a", "b"), (("a", "b"),))
    except Exception:
        return False
    pairs = dict(getattr(certificate, "adjacency"))
    if getattr(certificate, "degree_sum") != handshake_expected(2):
        return False
    if pairs["b"] != ("a", "c"):
        return False
    return bool(built == {"a": ["b"], "b": ["a"]})


def _adjacency_refused(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_handshaking"]
    if not callable(certify):
        return False
    probes = (
        (lambda: certify(("a", float("1")), ()), "float refused at the public boundary"),
        (lambda: certify(("a", True), ()), "boolean refused where a node was required"),
        (lambda: certify(("a",), (("a", "a"),)), "loop edge refused"),
        (lambda: certify(("a", "b"), (("a", "b"), ("b", "a"))), "undirected edge is repeated"),
        (lambda: certify(("a",), (("a", "b"),)), "edge endpoint is not a declared node"),
    )
    return _refused(namespace, "AdjacencyError", probes)


def harness_adjacency(namespace: dict[str, object]) -> bool:
    if not _adjacency_known(namespace):
        return False
    return _adjacency_refused(namespace)


def harness_domain(namespace: dict[str, object]) -> bool:
    admit = namespace["admit_domain"]
    as_str = namespace["as_str"]
    if not callable(admit) or not callable(as_str):
        return False
    try:
        integers = admit("Integers")
        field = admit("FiniteField", 2)
        rendered = as_str(getattr(integers, "domain"))
    except Exception:
        return False
    if rendered != "Integers" or getattr(field, "modulus") != 2:
        return False
    probes = (
        (lambda: admit(float("1")), "float refused at the public boundary"),
        (lambda: admit("Real"), "real coefficient domain refused"),
        (lambda: admit("FiniteField", 3), "only the prime field F2 is admitted"),
        (lambda: admit("FiniteField", True), "boolean or non-integer modulus refused"),
    )
    return _refused(namespace, "CoefficientDomainError", probes)


def harness_cocycle(namespace: dict[str, object]) -> bool:
    try_cocycle = namespace["try_cocycle"]
    if not callable(try_cocycle):
        return False
    try:
        closed = try_cocycle((1, 1, 0), (1, 1, 0))
    except Exception:
        return False
    if getattr(closed, "image") != 0:
        return False
    probes = (
        (lambda: try_cocycle((1, 0), (1, 0)), "cochain is not an F2 cocycle"),
        (lambda: try_cocycle((float("1"),), (1,)), "float refused at the public boundary"),
        (lambda: try_cocycle((True,), (1,)), "boolean or non-bit refused"),
        (lambda: try_cocycle((1, 0), (1,)), "cocycle form length does not match the cochain"),
    )
    return _refused(namespace, "CocycleError", probes)


def harness_cycle(namespace: dict[str, object]) -> bool:
    try_cycle = namespace["try_cycle"]
    if not callable(try_cycle):
        return False
    try:
        cycle = try_cycle(3, ((0, 1), (1, 2), (2, 0)), (1, 1, 1))
    except Exception:
        return False
    if getattr(cycle, "boundary") != (0, 0, 0):
        return False
    probes = (
        (lambda: try_cycle(3, ((0, 1), (1, 2), (2, 0)), (1, 0, 0)), "chain is not an F2 cycle"),
        (lambda: try_cycle(True, (), ()), "vertex count is not a nonnegative integer"),
        (lambda: try_cycle(2, ((0, 1),), (float("1"),)), "float refused at the public boundary"),
        (lambda: try_cycle(2, ((0, 1),), (1, 0)), "chain length does not match the edge set"),
    )
    return _refused(namespace, "CycleError", probes)


def harness_coboundary(namespace: dict[str, object]) -> bool:
    new = namespace["new"]
    certify = namespace["certify_closed_loop"]
    if not callable(new) or not callable(certify):
        return False
    try:
        coboundary = new(3, ((0, 1), (1, 2)))
        image = coboundary.apply((0, 1, Fraction(3)))
        loop = certify(coboundary, (0, 1, 3), (0, 1, 2))
    except Exception:
        return False
    if image != (Fraction(1), Fraction(2)) or getattr(loop, "image_sum") != 0:
        return False
    probes = (
        (lambda: new(3, ((0, 1),)).apply((float("1"), 0, 0)), "float refused at the public boundary"),
        (lambda: new(True, ()), "vertex count is not a positive integer"),
        (lambda: new(2, ((0, 5),)), "vertex index is outside the declared set"),
    )
    return _refused(namespace, "CoboundaryError", probes)


def _four_callable(
    namespace: dict[str, object], names: tuple[str, str, str, str]
) -> tuple[Callable[..., object], Callable[..., object], Callable[..., object], Callable[..., object]] | None:
    raw = tuple(namespace[name] for name in names)
    if not all(callable(item) for item in raw):
        return None
    return cast(
        tuple[Callable[..., object], Callable[..., object], Callable[..., object], Callable[..., object]],
        raw,
    )


def _trichotomy_bits(witnessed: object, residual: object, paired: object, same: object) -> bool:
    if witnessed is not True or residual is not False or paired is not True:
        return False
    return same is True


def _trichotomy_kinds(exact: object, closed: object, opened: object) -> bool:
    if getattr(exact, "kind") != "Exact" or getattr(exact, "closed_residual") is not False:
        return False
    if getattr(closed, "kind") != "ClosedResidual" or getattr(opened, "kind") != "OpenObstruction":
        return False
    return getattr(closed, "exact") is False


def harness_trichotomy(namespace: dict[str, object]) -> bool:
    found = _four_callable(namespace, ("classify_residual", "cohomologous", "is_exact", "is_cocycle"))
    if found is None:
        return False
    classify, cohomologous, exact_fn, cocycle_fn = found
    try:
        exact = classify(((1,), (0,)), ((0, 0),), (1, 0))
        closed = classify(((1,), (0,)), ((0, 0),), (0, 1))
        opened = classify(((0,), (0,)), ((1, 0),), (1, 0))
        same = cohomologous(((1,), (0,)), (1, 0), (0, 0))
        witnessed = exact_fn(((1,), (0,)), (1, 0))
        residual = exact_fn(((1,), (0,)), (0, 1))
        paired = cocycle_fn(((1, 1),), (1, 1))
    except Exception:
        return False
    if not _trichotomy_bits(witnessed, residual, paired, same):
        return False
    if not _trichotomy_kinds(exact, closed, opened):
        return False
    probes = (
        (lambda: classify(((1,), (1,)), ((1, 0),), (1, 0)), "complex is not nilpotent"),
        (lambda: classify(((float("1"),),), ((0,),), (0,)), "float refused at the public boundary"),
        (lambda: classify(((1,),), ((0,),), (True,)), "boolean or non-bit refused"),
    )
    return _refused(namespace, "TrichotomyError", probes)


def _require_callable(namespace: dict[str, object], names: tuple[str, ...]) -> bool:
    for name in names:
        if not callable(namespace[name]):
            return False
    return True


def _contract_numbers(square: object, sign: object, dims: object, distance: object, product: object) -> bool:
    if getattr(square, "square") != 1 or getattr(sign, "square") != 1:
        return False
    if getattr(dims, "sigma_sq") != ising_sigma_target():
        return False
    return bool(getattr(distance, "distance") == 3 and getattr(product, "product") == 6)


def harness_contract(namespace: dict[str, object]) -> bool:
    names = ("certify_parity_square", "certify_pfaffian_sign", "certify_ising_dimensions", "certify_toric_distance", "certify_transfer_gap")
    if not _require_callable(namespace, names):
        return False
    parity = cast(Callable[..., object], namespace["certify_parity_square"])
    pfaffian = cast(Callable[..., object], namespace["certify_pfaffian_sign"])
    ising = cast(Callable[..., object], namespace["certify_ising_dimensions"])
    toric = cast(Callable[..., object], namespace["certify_toric_distance"])
    gap = cast(Callable[..., object], namespace["certify_transfer_gap"])
    try:
        square = parity(-1)
        sign = pfaffian(1)
        dims = ising()
        distance = toric(3, 4)
        product = gap(2, 3)
    except Exception:
        return False
    if not _contract_numbers(square, sign, dims, distance, product):
        return False
    probes = (
        (lambda: parity(2), "sign is not 1 or -1"),
        (lambda: parity(float("1")), "float refused at the public boundary"),
        (lambda: parity(True), "boolean or non-integer sign refused"),
        (lambda: gap(0, 1), "positive integer required"),
    )
    return _refused(namespace, "ContractError", probes)


def harness_serialization(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_encoding"]
    vector = namespace["canonical_vector"]
    if not callable(certify) or not callable(vector):
        return False
    try:
        encoded = certify(Fraction(2, 4))
        row = vector((1, Fraction(1, 2)))
    except Exception:
        return False
    if getattr(encoded, "text") != "1/2" or row != ("1/1", "1/2"):
        return False
    probes = (
        (lambda: certify(float("1")), "float refused at the public boundary"),
        (lambda: certify(True), "boolean refused where a rational was required"),
        (lambda: certify("1.5"), "decimal or empty text refused"),
    )
    return _refused(namespace, "SerializationError", probes)


def harness_coset(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_coset_weight"]
    verify = namespace["verify_primal_dual_certificate"]
    if not callable(certify) or not callable(verify):
        return False
    try:
        weight = certify((1, 0, 1), (1, 1, 0))
        same = verify((1, 0, 1), (1, 1, 0))
    except Exception:
        return False
    if getattr(weight, "combined") != (0, 1, 1) or getattr(weight, "weight") != 2:
        return False
    if getattr(same, "weight") != getattr(weight, "weight"):
        return False
    probes = (
        (lambda: certify((1, 0), (1,)), "correction length does not match the witness"),
        (lambda: certify((float("1"),), (0,)), "float refused at the public boundary"),
        (lambda: certify((2,), (0,)), "F2 coordinate is not 0 or 1"),
    )
    return _refused(namespace, "PrimalResidualError", probes)


def harness_scalar(namespace: dict[str, object]) -> bool:
    construct = namespace["q"]
    digest = namespace["hash_rational"]
    certify = namespace["certify_scalar"]
    if not callable(construct) or not callable(digest) or not callable(certify):
        return False
    try:
        value = construct("2/4")
        text = digest(2, 4)
        certificate = certify(value)
    except Exception:
        return False
    if value != Fraction(1, 2) or text != "1/2" or getattr(certificate, "text") != "1/2":
        return False
    probes = (
        (lambda: construct(float("1")), "float refused at the public boundary"),
        (lambda: construct(True), "boolean refused where a rational was required"),
        (lambda: digest(1, 0), "rational denominator is zero"),
    )
    return _refused(namespace, "ScalarError", probes)


def _ids_types(degree: object, basis: object, provenance: object, certify: object) -> bool:
    if not isinstance(degree, type) or not isinstance(basis, type) or not isinstance(provenance, type):
        return False
    return callable(certify)


def _new(kind: type, value: object) -> object:
    method = cast(Callable[..., object], getattr(kind, "new"))
    return method(value)


def _ids_refusals(
    error: type[BaseException],
    invalid: type[BaseException],
    degree: type,
    basis: type,
    provenance: type,
) -> bool:
    if _invariant(error, lambda: _new(degree, True)) != "degree is not an exact integer":
        return False
    if _invariant(error, lambda: _new(basis, "")) != "basis label must be a nonempty string":
        return False
    if _invariant(error, lambda: _new(basis, float("1"))) != "float refused at the public boundary":
        return False
    if _message(invalid, lambda: _new(provenance, "")) != "provenance verification_source must be non-empty":
        return False
    return _invariant(error, lambda: _new(degree, float("1"))) == "float refused at the public boundary"


def harness_ids(namespace: dict[str, object]) -> bool:
    degree = namespace["Degree"]
    basis = namespace["BasisId"]
    provenance = namespace["TheoremProvenance"]
    certify = namespace["certify_identifiers"]
    if not _ids_types(degree, basis, provenance, certify):
        return False
    degree_type = cast(type, degree)
    basis_type = cast(type, basis)
    provenance_type = cast(type, provenance)
    try:
        admitted = cast(Callable[..., object], certify)(1, "papers/derivations/ms_majorana/lean4/MajoranaCore.lean")
        label = _new(basis_type, "test")
    except Exception:
        return False
    if getattr(getattr(admitted, "degree"), "value") != 1 or getattr(label, "label") != "test":
        return False
    error = namespace["IdentifierError"]
    invalid = getattr(_module("errors"), "InvalidProvenance")
    if not isinstance(error, type) or not isinstance(invalid, type):
        return False
    return _ids_refusals(error, invalid, degree_type, basis_type, provenance_type)


def harness_filtration(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_filtration"]
    if not callable(certify):
        return False
    try:
        filtration = certify((((0,), 0, 0), ((0, 1), 1, 1)))
    except Exception:
        return False
    if len(filtration) != 2 or filtration.values_nondecreasing() is not True:
        return False
    probes = (
        (lambda: certify((((0,), float("1"), 0),)), "float refused at the public boundary"),
        (lambda: certify((((0,), 1, 0), ((0, 1), 0, 1))), "filtration values are not nondecreasing"),
        (lambda: certify((((0,), 0, 1),)), "vertex count does not match the dimension"),
    )
    return _refused(namespace, "FiltrationError", probes)


def harness_persistence(namespace: dict[str, object]) -> bool:
    finite = namespace["finite"]
    certify = namespace["certify_diagram"]
    if not callable(finite) or not callable(certify):
        return False
    try:
        point = finite(1, 3, 0)
        diagram = certify(((0, 2, 1),))
    except Exception:
        return False
    if point.persistence() != 2 or diagram.points[0].dimension != 1:
        return False
    probes = (
        (lambda: finite(float("1"), 2, 0), "float refused at the public boundary"),
        (lambda: finite(2, 2, 0), "death is not strictly after birth"),
        (lambda: finite(0, 1, True), "dimension is not a nonnegative integer"),
    )
    return _refused(namespace, "PersistenceError", probes)


def harness_barcode(namespace: dict[str, object]) -> bool:
    diagram_mod = _module("persistence_diagram")
    from_diagram = namespace["from_diagram"]
    total = namespace["total_length"]
    if not callable(from_diagram) or not callable(total):
        return False
    try:
        diagram = diagram_mod.certify_diagram(((0, 2, 0), (1, Fraction(5, 2), 1)))
        barcode = from_diagram(diagram)
        length = total(barcode)
    except Exception:
        return False
    if length != Fraction(7, 2) or len(barcode.bars) != 2:
        return False
    probes = (
        (lambda: from_diagram(object()), "barcode requires a persistence diagram"),
        (lambda: total(object()), "total length requires a barcode"),
    )
    return _refused(namespace, "BarcodeError", probes)


def harness_bottleneck(namespace: dict[str, object]) -> bool:
    diagrams = _module("persistence_diagram")
    distance = namespace["bottleneck_distance"]
    diagonal = namespace["diagonal_cost"]
    if not callable(distance) or not callable(diagonal):
        return False
    empty = diagrams.certify_diagram(())
    one = diagrams.certify_diagram(((0, 2, 0),))
    try:
        to_empty = distance(one, empty)
        apart = distance(one, diagrams.certify_diagram(((0, 4, 0),)))
        blank = distance(empty, empty)
        near = distance(diagrams.certify_diagram(((0, 10, 0),)), diagrams.certify_diagram(((0, 12, 0),)))
        cost = diagonal(one.points[0])
    except Exception:
        return False
    if to_empty != 1 or apart != 2 or cost != 1 or blank != 0 or near != 2:
        return False
    probes = (
        (lambda: distance(diagrams.certify_diagram(((0, 1, 0), (1, 2, 0))), empty), "bottleneck certificate admits at most one finite point"),
        (lambda: distance(object(), empty), "bottleneck requires a persistence diagram"),
    )
    return _refused(namespace, "BottleneckError", probes)


def harness_cup(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_unit"]
    cochain = namespace["cochain"]
    product = namespace["CupProduct"]
    if not callable(certify) or not callable(cochain) or not isinstance(product, type):
        return False
    try:
        certificate = certify(((0, 2), (1, Fraction(3, 2))))
        cup = cast(Callable[..., object], getattr(product, "of"))
        swapped = cup(cochain(((1, 3), (0, 2))), cochain(((0, 4), (1, 5))))
    except Exception:
        return False
    if getattr(getattr(certificate, "result"), "terms") != ((0, Fraction(2)), (1, Fraction(3, 2))):
        return False
    if getattr(getattr(swapped, "result"), "terms") != ((0, Fraction(8)), (1, Fraction(15))):
        return False
    probes = (
        (lambda: cochain(((0, float("1")),)), "float refused at the public boundary"),
        (lambda: cochain(((0, 1), (0, 2))), "cochain vertex is repeated"),
        (lambda: cochain(((True, 1),)), "vertex is not an exact index"),
    )
    return _refused(namespace, "CupProductError", probes)


def harness_vietoris(namespace: dict[str, object]) -> bool:
    build = namespace["vietoris_rips_filtration"]
    if not callable(build):
        return False
    try:
        full = build((0, 1, 1, 0), 1)
        vertices = build((0, 1, 1, 0), 0)
    except Exception:
        return False
    if len(full) != 3 or len(vertices) != 2 or full.values_nondecreasing() is not True:
        return False
    probes = (
        (lambda: build((float("0"),), 1), "float refused at the public boundary"),
        (lambda: build((0, 1, 1, 0), -1), "radius is negative"),
        (lambda: build((0, 1, 0), 1), "distance table is not square"),
    )
    return _refused(namespace, "VietorisError", probes)


def harness_incidence(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_incidence"]
    build = namespace["build_incidence_matrix"]
    if not callable(certify) or not callable(build):
        return False

    class _Graph:
        nodes = ("a", "b")
        edges = (("a", "b"),)

    try:
        certificate = certify(_Graph())
        matrix, index, edges = build(_Graph())
    except Exception:
        return False
    if matrix[0] != (Fraction(-1), Fraction(1)) or index["a"] != 0 or edges != (("a", "b"),):
        return False
    if certificate.matrix != matrix:
        return False
    probes = (
        (lambda: certify(object()), "poset must declare nodes and edges"),
        (lambda: certify(type("G", (), {"nodes": ("a", float("1")), "edges": ()})()), "float refused at the public boundary"),
        (lambda: certify(type("G", (), {"nodes": ("a",), "edges": (("a", "a"),)})()), "loop edge refused"),
    )
    return _refused(namespace, "IncidenceError", probes)


def harness_gram(namespace: dict[str, object]) -> bool:
    density = namespace["density"]
    certify = namespace["certify_gram"]
    if not callable(density) or not callable(certify):
        return False
    try:
        certificate = certify((1, 2))
        matrix = density((1, 2))
    except Exception:
        return False
    if certificate.trace != gram_trace_target() or matrix[0] != (Fraction(1), Fraction(2)):
        return False
    probes = (
        (lambda: density((float("1"),)), "float refused at the public boundary"),
        (lambda: density((True,)), "boolean refused where a rational was required"),
        (lambda: density(()), "state must be a nonempty sequence"),
    )
    return _refused(namespace, "StateError", probes)


def harness_triangular(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_upper_triangular"]
    if not callable(certify):
        return False
    try:
        certificate = certify(((1, 2, 3), (0, 4, 5), (0, 0, 6)))
    except Exception:
        return False
    if certificate.determinant != 24 or certificate.diagonal_product != 24:
        return False
    probes = (
        (lambda: certify(((1, 2), (3, 4))), "matrix is not upper triangular"),
        (lambda: certify(((float("1"),),)), "float refused at the public boundary"),
        (lambda: certify(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))), "triangular certificate admits size at most 3"),
    )
    return _refused(namespace, "TriangularError", probes)


def harness_lambda(namespace: dict[str, object]) -> bool:
    build = namespace["graph_from_poset"]
    if not callable(build):
        return False
    try:
        certificate = build(("a", "b", "c"), (("a", "b"), ("b", "c")))
    except Exception:
        return False
    if certificate.order != ("a", "b", "c") or certificate.relation_count != 2:
        return False
    probes = (
        (lambda: build(("a", "b"), (("a", "b"), ("b", "a"))), "relation graph contains a directed cycle"),
        (lambda: build(("a",), (("a", "a"),)), "reflexive relation refused"),
        (lambda: build((float("1"),), ()), "float refused at the public boundary"),
    )
    return _refused(namespace, "LambdaGraphError", probes)


def harness_primitive(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_square_split"]
    if not callable(certify):
        return False
    try:
        twelve = certify(12)
        thirty_six = certify(36)
        eighteen = certify(18)
    except Exception:
        return False
    if twelve.square != 2 or twelve.radical != radical_of_twelve():
        return False
    if thirty_six.square != 6 or thirty_six.radical != 1:
        return False
    if eighteen.square != 3 or eighteen.radical != 2:
        return False
    probes = (
        (lambda: certify(float("4")), "float refused at the public boundary"),
        (lambda: certify(True), "boolean or non-integer refused"),
        (lambda: certify(0), "positive integer required"),
    )
    return _refused(namespace, "PrimitiveError", probes)


def harness_error(namespace: dict[str, object]) -> bool:
    certify = namespace["certify_boundary_square"]
    if not callable(certify):
        return False
    try:
        certificate = certify((0, Fraction(0)))
    except Exception:
        return False
    if certificate.defect != 0:
        return False
    if not _refused(namespace, "BoundarySquaredNonzero", ((lambda: certify((1, -1)), "boundary square is not zero"),)):
        return False
    return _refused(
        namespace,
        "HomologyError",
        (
            (lambda: certify((float("1"),)), "float refused at the public boundary"),
            (lambda: certify((True,)), "boolean refused where a rational was required"),
        ),
    )


def _cases() -> tuple[tuple[str, Callable[[dict[str, object]], bool], tuple[tuple[str, str, str], ...]], ...]:
    return (
        ("adjacency", harness_adjacency, _adjacency_mutants()),
        ("coefficient_domain", harness_domain, _domain_mutants()),
        ("cocycle", harness_cocycle, _cocycle_mutants()),
        ("cycle", harness_cycle, _cycle_mutants()),
        ("coboundary", harness_coboundary, _coboundary_mutants()),
        ("trichotomy_witness", harness_trichotomy, _trichotomy_mutants()),
        ("contract_property_witnesses", harness_contract, _contract_mutants()),
        ("serialization", harness_serialization, _serialization_mutants()),
        ("primal_residual", harness_coset, _coset_mutants()),
        ("scalar", harness_scalar, _scalar_mutants()),
        ("ids", harness_ids, _ids_mutants()),
        ("filtration", harness_filtration, _filtration_mutants()),
        ("persistence_diagram", harness_persistence, _persistence_mutants()),
        ("barcode", harness_barcode, _barcode_mutants()),
        ("bottleneck_distance", harness_bottleneck, _bottleneck_mutants()),
        ("cup_product", harness_cup, _cup_mutants()),
        ("vietoris_rips", harness_vietoris, _vietoris_mutants()),
        ("incidence", harness_incidence, _incidence_mutants()),
        ("quantum_states", harness_gram, _gram_mutants()),
        ("upper_triangular_pairs", harness_triangular, _triangular_mutants()),
        ("lambda_graph", harness_lambda, _lambda_mutants()),
        ("primitive_decomposition", harness_primitive, _primitive_mutants()),
        ("error", harness_error, _error_mutants()),
    )


def _flip(prefix: str, old: str, new: str) -> tuple[str, str, str]:
    return (prefix, old, new)


def _adjacency_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("handshaking", "if degree_sum != edge_count * 2:", "if degree_sum != edge_count * 3:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return str(value)"),
        _flip("bool", 'raise _fail("boolean refused where a node was required", role=role)', "return str(value)"),
        _flip("loop", 'raise _fail("loop edge refused", node=str(left))', "return None"),
        _flip("repeat", 'raise _fail("undirected edge is repeated", left=str(left), right=str(right))', "return None"),
        _flip("reverse", "neighbors[right].append(left)", "neighbors[left].append(left)"),
    )


def _domain_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("real", 'raise _fail("real coefficient domain refused", name="Real")', "return DomainCertificate(CoefficientDomain.Integers, None)"),
        _flip("modulus", "if parsed != 2:", "if parsed != 3:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role="name", received="float")', "return DomainCertificate(CoefficientDomain.Integers, None)"),
        _flip("name", 'return domain.value', "return domain.value + 'x'"),
        _flip("integers", 'return DomainCertificate(CoefficientDomain.Integers, None)', "return DomainCertificate(CoefficientDomain.Rational, None)"),
    )


def _cocycle_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("image", "if image != 0:", "if image != 1:"),
        _flip("dot", "total = (total + coeff * bit) % 2", "total = (total + coeff * bit) % 3"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return 0"),
        _flip("bool", 'raise _fail("boolean or non-bit refused", role=role, received=type(value).__name__)', "return 1"),
        _flip("length", "if len(form) != len(vector):", "if len(form) == len(vector):"),
    )


def _cycle_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("boundary", 'raise _fail("chain is not an F2 cycle", boundary=boundary)', "return Cycle(parsed_chain, boundary)"),
        _flip("mod", "boundary[src] = (boundary[src] + bit) % 2", "boundary[src] = (boundary[src] + bit) % 3"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return 0"),
        _flip("count", "if isinstance(value, bool) or type(value) is not int or value < 0:", "if type(value) is float:"),
        _flip("length", "if len(parsed_edges) != len(parsed_chain):", "if len(parsed_edges) == len(parsed_chain):"),
    )


def _coboundary_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("sign", "image.append(parsed[dst] - parsed[src])", "image.append(parsed[dst] + parsed[src])"),
        _flip("loop", "if image_sum != 0:", "if image_sum != 1:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
        _flip("count", "if isinstance(vertex_count, bool) or type(vertex_count) is not int or vertex_count < 1:", "if type(vertex_count) is float:"),
        _flip("close", "total += values[loop[0]] - values[previous]", "total += values[loop[0]] + values[previous]"),
    )


def _trichotomy_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("image", "return _in_image(matrix, vector)", "return True"),
        _flip("nil", 'raise _fail("complex is not nilpotent", relation="d1 d0 = 0")', "return None"),
        _flip("open", 'if opened:\n        return "OpenObstruction"', 'if opened:\n        return "Exact"'),
        _flip("closed", 'if closed:\n        return "ClosedResidual"', 'if closed:\n        return "Exact"'),
        _flip("dot", "total = (total + coeff * bit) % 2", "total = (total + coeff * bit) % 3"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return 0"),
    )


def _contract_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("square", "square = sign * sign", "square = sign + sign"),
        _flip("ising", "if sigma_sq != one_sq + psi_sq:", "if sigma_sq == one_sq + psi_sq:"),
        _flip("toric", "distance = parsed_rows if parsed_rows < parsed_cols else parsed_cols", "distance = parsed_rows if parsed_rows > parsed_cols else parsed_cols"),
        _flip("gap", "if product <= 0:", "if product > 0:"),
        _flip("sign", "if value != 1 and value != -1:", "if value != 1 and value != 2:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")\n    if isinstance(value, bool) or type(value) is not int:\n        raise _fail("boolean or non-integer sign refused", role=role, received=type(value).__name__)', "return 1"),
    )


def _serialization_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("text", 'return f"{parsed.numerator}/{parsed.denominator}"', 'return f"{parsed.numerator}/1"'),
        _flip("decode", "if decoded != parsed:", "if decoded == parsed:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
        _flip("bool", 'raise _fail("boolean refused where a rational was required", role=role)', "return Fraction(1)"),
        _flip("decimal", 'raise _fail("decimal or empty text refused", role=role)', "return Fraction(1)"),
    )


def _coset_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("add", "combined = tuple((a + b) % 2 for a, b in zip(left, right))", "combined = tuple((a + b) % 3 for a, b in zip(left, right))"),
        _flip("count", "if bit == 1:\n            total += 1", "if bit == 0:\n            total += 1"),
        _flip("length", "if len(left) != len(right):", "if len(left) == len(right):"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return 0"),
        _flip("range", "if value not in (0, 1):", "if value not in (0, 1, 2):"),
    )


def _scalar_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("text", 'return f"{reduced.numerator}/{reduced.denominator}"', 'return f"{reduced.numerator}/1"'),
        _flip("zero", "if denominator == 0:", "if denominator == 1:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role="value", received="float")', "return Fraction(0)"),
        _flip("bool", 'raise _fail("boolean refused where a rational was required", role="value")', "return Fraction(1)"),
        _flip("rebuild", "if rebuilt != parsed:", "if rebuilt == parsed:"),
    )


def _ids_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("degree", "if isinstance(self.value, bool) or type(self.value) is not int:", "if type(self.value) is float:"),
        _flip("empty", 'if not isinstance(self.verification_source, str) or self.verification_source == "":', "if not isinstance(self.verification_source, str):"),
        _flip("label", 'if not isinstance(self.label, str) or self.label == "":', "if not isinstance(self.label, str):"),
        _flip("float", 'raise _fail("float refused at the public boundary", role="degree", received="float")', "return Degree(0)"),
        _flip("basis", 'raise _fail("float refused at the public boundary", role="label", received="float")', 'return BasisId("x")'),
    )


def _filtration_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("order", "if not filtration.values_nondecreasing():", "if filtration.values_nondecreasing():"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
        _flip("dimension", "if len(parsed.vertices) != dimension + 1:", "if len(parsed.vertices) == dimension + 1:"),
        _flip("compare", "if simplex.value < previous:", "if simplex.value > previous:"),
    )


def _persistence_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("death", "if died <= born:", "if died > born:"),
        _flip("length", "return self.death - self.birth", "return self.death + self.birth"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
        _flip("dimension", "if isinstance(value, bool) or type(value) is not int or value < 0:", "if type(value) is float:"),
    )


def _barcode_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("length", "return self.death - self.birth", "return self.birth - self.death"),
        _flip("copy", "bars = tuple(_bar(point) for point in diagram.points)", "bars = tuple()"),
        _flip("type", 'raise _fail("barcode requires a persistence diagram", received=type(diagram).__name__)', "return Barcode(())"),
        _flip("sum", "total += bar.length()", "total -= bar.length()"),
    )


def _bottleneck_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("diagonal", "return (point.death - point.birth) / 2", "return (point.death - point.birth) / 4"),
        _flip("cap", "if matched < cap:", "if matched > cap:"),
        _flip("limit", "if len(diagram.points) > 1:", "if len(diagram.points) > 3:"),
        _flip("empty", "return Fraction(0)", "return Fraction(1)"),
    )


def _cup_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("product", "product.append((vertex, coeff * right_map[vertex]))", "product.append((vertex, coeff + right_map[vertex]))"),
        _flip("unit", "tuple((vertex, Fraction(1)) for vertex, _coeff in left.terms)", "tuple((vertex, Fraction(2)) for vertex, _coeff in left.terms)"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
        _flip("repeat", 'raise _fail("cochain vertex is repeated", vertex=vertex)', "return ((0, Fraction(0)),)"),
    )


def _vietoris_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("radius", "if gap <= radius:", "if gap > radius:"),
        _flip("negative", "if limit < 0:", "if limit > 0:"),
        _flip("square", "if count * count != len(self.distances):", "if count * count == len(self.distances):"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
    )


def _incidence_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("sign", "row[index[src]] = Fraction(-1)", "row[index[src]] = Fraction(1)"),
        _flip("sum", "if _row_sum(frozen) != 0:", "if _row_sum(frozen) == 0:"),
        _flip("loop", 'raise _fail("loop edge refused", node=str(src))', "return (tuple(Fraction(0) for _ in range(len(index))), (src, dst))"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', 'return "0"'),
    )


def _gram_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("trace", "if trace != _norm_sq(coords):", "if trace == _norm_sq(coords):"),
        _flip("entry", "return tuple(left * right for right in coords)", "return tuple(left + right for right in coords)"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received=type(value).__name__)', "return Fraction(0)"),
        _flip("empty", 'raise _fail("state must be a nonempty sequence", received=type(values).__name__)', "return ()"),
    )


def _triangular_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("det", "return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)", "return a * (e + i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)"),
        _flip("lower", "if column < row and entry != 0:", "if column < row and entry == 0:"),
        _flip("size", "if width > 3:", "if width > 8:"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', "return Fraction(0)"),
    )


def _lambda_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("cycle", "if len(ordered) != len(declared):", "if len(ordered) == len(declared):"),
        _flip("reflexive", 'raise _fail("reflexive relation refused", node=lower)', "return (lower, upper)"),
        _flip("degree", "degree[upper] += 1", "degree[upper] -= 1"),
        _flip("float", 'raise _fail("float refused at the public boundary", role=role, received="float")', 'return "0"'),
    )


def _primitive_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("rebuild", "if square * square * radical != parsed:", "if square * square * radical == parsed:"),
        _flip("peel", "while rest % (prime * prime) == 0:", "while rest % prime == 0:"),
        _flip("free", "if _square_divides(radical):", "if not _square_divides(radical):"),
        _flip("float", 'raise _fail("float refused at the public boundary", received="float")', "return 1"),
    )


def _error_mutants() -> tuple[tuple[str, str, str], ...]:
    return (
        _flip("defect", "if defect != 0:", "if defect == 0:"),
        _flip("abs", "total -= entry", "total += entry"),
        _flip("float", 'raise HomologyError("float refused at the public boundary", {"role": role, "received": "float"})', "return Fraction(0)"),
        _flip("bool", 'raise HomologyError("boolean refused where a rational was required", {"role": role})', "return Fraction(1)"),
    )


def harness_all(modules: dict[str, dict[str, object]]) -> bool:
    for stem, oracle, _mutants in _cases():
        if oracle(modules[stem]) is not True:
            return False
    return True


def _load_real() -> dict[str, dict[str, object]]:
    loaded: dict[str, dict[str, object]] = {}
    for stem, _oracle, _mutants in _cases():
        loaded[stem] = dict(vars(_module(stem)))
    return loaded


def test_unit_known_certificates() -> None:
    modules = _load_real()
    for stem, oracle, _mutants in _cases():
        assert oracle(modules[stem]) is True, stem


def test_negative_float_bool_and_invariant_refusals() -> None:
    modules = _load_real()
    adjacency = modules["adjacency"]
    scalar = modules["scalar"]
    certify = cast(Callable[[object, object], object], adjacency["certify_handshaking"])
    construct = cast(Callable[[object], Fraction], scalar["q"])
    with pytest.raises(cast(type[BaseException], adjacency["AdjacencyError"]), match="float refused"):
        certify(("a", float("1")), ())
    with pytest.raises(cast(type[BaseException], scalar["ScalarError"]), match="boolean refused"):
        construct(True)


def test_integration_barcode_matches_persistence() -> None:
    diagrams = _module("persistence_diagram")
    bars = _module("barcode")
    distance = _module("bottleneck_distance")
    diagram = diagrams.certify_diagram(((0, 2, 0),))
    barcode = bars.from_diagram(diagram)
    assert bars.total_length(barcode) == diagram.points[0].persistence()
    assert distance.bottleneck_distance(diagram, diagrams.certify_diagram(())) == Fraction(1)


def test_e2e_trichotomy_and_integer_contracts() -> None:
    trichotomy = _module("trichotomy_witness")
    contract = _module("contract_property_witnesses")
    closed = trichotomy.classify_residual(((1,), (0,)), ((0, 0),), (0, 1))
    assert closed.kind == "ClosedResidual"
    assert closed.exact is False
    assert closed.open_obstruction is False
    assert contract.certify_toric_distance(3, 4).distance == 3
    assert contract.certify_transfer_gap(2, 3).product == 6
    assert contract.certify_ising_dimensions().sigma_sq == ising_sigma_target()


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    killed_total = 0
    for stem, oracle, mutants in _cases():
        source = (CODE / f"{stem}.py").read_text(encoding="utf-8")
        baseline = _load_source(source, f"baseline_{stem}")
        assert oracle(baseline) is True
        killed = _killed(source, mutants, oracle, f"mut_{stem}")
        assert killed == len(mutants)
        assert f"Mutation-Kills: {killed} non-equivalent" in source
        killed_total += killed
    assert killed_total == 106


def test_harness_mutants_are_killed() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    real = _load_real()
    assert harness_all(real) is True
    mutants = (
        ("handshake scale", "return edge_count * " + "2", "return edge_count * 3"),
        ("ising target", "return " + "2", "return " + "3"),
        ("gram target", "return " + "5", "return 4"),
        ("radical target", "return " + "3", "return 1"),
    )
    killed = 0
    for index, (name, old, new) in enumerate(mutants):
        if source.count(old) != 1:
            raise HarnessFault("harness mutant site is not unique", {"name": name, "count": source.count(old)})
        namespace = _load_source(source.replace(old, new, 1), f"harness_mut_{index}")
        oracle = namespace["harness_all"]
        if not callable(oracle):
            raise HarnessFault("harness oracle missing", {"name": name})
        assert oracle(real) is False
        killed += 1
    assert killed == 4
    assert f"Mutation-Kills: {killed} non-equivalent" in source
