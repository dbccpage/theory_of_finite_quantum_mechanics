# Status: independent check for TFQ-0374. No repository imports.
"""One old letter and one new letter, three recovery contracts."""

from __future__ import annotations

OLD = 0
FRESH = 1


def all_old(word):
    return all(letter == OLD for letter in word)


def restrict_language(language):
    return tuple(word for word in language if all_old(word))


def recover_word(word):
    if all_old(word):
        return word
    return None


def erase_word(word):
    return tuple(letter for letter in word if letter == OLD)


def main():
    failures = 0
    checked = 0

    def expect(cond):
        nonlocal failures, checked
        checked += 1
        if not cond:
            failures += 1

    letters = (OLD, FRESH)
    expect(len(letters) == 2)
    expect(len(set(letters)) == 2)
    expect(FRESH != OLD)
    for letter in letters:
        expect(letter == OLD or letter == FRESH)

    old_word = (OLD,)
    witness = (OLD, FRESH)
    expect(witness == (OLD, FRESH))
    expect(sum(1 for letter in witness if letter == FRESH) == 1)
    expect(sum(1 for letter in old_word if letter == FRESH) == 0)

    sample = (witness, old_word)
    restricted = restrict_language(sample)
    recovered = recover_word(witness)
    erased = erase_word(witness)
    expect(restricted == (old_word,))
    expect(recovered is None)
    expect(erased == old_word)
    expect(recovered != erased)
    expect(erased != witness)
    expect(old_word in restricted)
    expect(witness not in restricted)
    expect(recover_word(old_word) == old_word)
    expect(erase_word(old_word) == old_word)
    expect(restrict_language((old_word,)) == (old_word,))

    # The three results are a tuple of words, an absent recovery, and a word.
    expect(type(restricted) is tuple)
    expect(type(erased) is tuple)
    expect(recovered is None)
    expect(len(restricted) == 1)
    expect(len(erased) == 1)
    expect(len(witness) == 2)

    print(f"checked {checked} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
