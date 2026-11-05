"""Versioned cross-language keys; frozen derivation.iso stays unchanged."""
from derivation.iso import CanonKey, IsoBudgetError, canonical_bruteforce
from derivation.model import Regime

PREFIX = b"GENESIS-KEY\x00\x01"
U64_MAX = 2**64 - 1


class PortableKeyError(ValueError):
    """Malformed structure, unsigned-word overflow, or invalid wire format."""


def _word(value: int) -> int:
    if type(value) is not int or not 0 <= value <= U64_MAX:
        raise PortableKeyError("protocol integers must be unsigned 64-bit values")
    return value


def _validate_key(key: CanonKey, require_sorted: bool = True) -> None:
    n, forms, insts, rules, reqs = key
    _word(n)
    for items in (forms, insts, rules, reqs):
        _word(len(items))
    if any(_word(a) == 0 for a in forms):
        raise PortableKeyError("form arities must be positive")
    for form, args in insts:
        _word(form)
        _word(len(args))
        if form >= len(forms) or len(args) != forms[form]:
            raise PortableKeyError("instance form or arity is invalid")
        if any(_word(d) >= n for d in args):
            raise PortableKeyError("instance datum is out of range")
    if any(_word(f) >= len(forms) for f in rules):
        raise PortableKeyError("uniform-rule form is out of range")
    if any(not _word(i) < _word(j) < n for i, j in reqs):
        raise PortableKeyError("requirements must have ordered, distinct admitted endpoints")
    if require_sorted and (insts != tuple(sorted(set(insts))) or rules != tuple(sorted(set(rules)))
                           or reqs != tuple(sorted(set(reqs)))):
        raise PortableKeyError("collections must be strictly sorted and duplicate-free")


def structural_words(key: CanonKey) -> tuple[int, ...]:
    """The exact length-prefixed fields used by the Lean wire model."""
    _validate_key(key)
    n, forms, insts, rules, reqs = key
    words = [n, len(forms), *forms, len(insts)]
    for form, args in insts:
        words.extend((form, len(args), *args))
    words.extend((len(rules), *rules, len(reqs)))
    for pair in reqs:
        words.extend(pair)
    return tuple(words)


def encode_structural_key_v1(key: CanonKey) -> bytes:
    """Encode an already sorted structural tuple; does not perform minimization."""
    return PREFIX + b"".join(x.to_bytes(8, "big") for x in structural_words(key))


def decode_portable_key_v1(data: bytes) -> CanonKey:
    """Decode the layout with bounded reads, rejecting trailing or malformed data.

    A decoded tuple is well-formed and sorted. Acceptance does not certify that
    it is the minimum of its isomorphism orbit.
    """
    if not isinstance(data, bytes) or not data.startswith(PREFIX):
        raise PortableKeyError("invalid portable-key prefix or version")
    payload = data[len(PREFIX):]
    if len(payload) % 8:
        raise PortableKeyError("truncated unsigned 64-bit word")
    words = [int.from_bytes(payload[i:i + 8], "big") for i in range(0, len(payload), 8)]
    cursor = 0

    def take(count: int) -> tuple[int, ...]:
        nonlocal cursor
        if count > len(words) - cursor:
            raise PortableKeyError("declared length exceeds remaining input")
        values = tuple(words[cursor:cursor + count])
        cursor += count
        return values

    def word() -> int:
        return take(1)[0]

    def counted() -> tuple[int, ...]:
        return take(word())

    n = word()
    forms = counted()
    inst_count = word()
    if inst_count > (len(words) - cursor) // 2:
        raise PortableKeyError("instance count exceeds remaining input")
    insts = tuple((word(), counted()) for _ in range(inst_count))
    rules = counted()
    pair_count = word()
    if pair_count > (len(words) - cursor) // 2:
        raise PortableKeyError("requirement count exceeds remaining input")
    reqs = tuple((word(), word()) for _ in range(pair_count))
    if cursor != len(words):
        raise PortableKeyError("trailing portable-key data")
    key = (n, forms, insts, rules, reqs)
    _validate_key(key)
    return key


def portable_key_v1(regime: Regime, budget: int = 100_000) -> bytes:
    """Exhaustive structural minimum; budget exhaustion never returns a key.

    Integers and collection lengths use unsigned 64-bit big-endian words.
    Presentation labels are erased; requirement endpoints are unordered.
    """
    _word(budget)
    _validate_key((regime.n_data(), regime.forms, tuple(regime.insts),
                   tuple(regime.rules), tuple(regime.reqs)), require_sorted=False)
    count = 1
    for size in (regime.n_data(), len(regime.forms)):
        for factor in range(2, size + 1):
            count *= factor
            if count > budget or count >= U64_MAX:
                raise IsoBudgetError(f"candidate bijections exceed budget {budget}")
    if count > budget:
        raise IsoBudgetError(f"candidate bijections exceed budget {budget}")
    return encode_structural_key_v1(canonical_bruteforce(regime))
