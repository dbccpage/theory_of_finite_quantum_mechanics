"""
Unit tests for DDC Operation I (Integration Tape).
AuthorityEffect: None.
"""

from integration_tape import ExecutionTape, TapeEntry


def test_tape_append_and_verify():
    """Verify standard append and cryptographic integrity verification."""
    tape = ExecutionTape()
    e1 = tape.append("C", {"window": ["A", "B"]})
    e2 = tape.append("E", {"repaired_edges": 1})
    e3 = tape.append("I", {"step": 2})

    assert tape.verify_integrity() is True
    assert len(tape.get_entries()) == 3
    assert e2.prev_hash == e1.current_hash
    assert e3.prev_hash == e2.current_hash


def test_tape_tamper_detection():
    """Verify that tampering with an intermediate payload fails verification."""
    tape = ExecutionTape()
    tape.append("C", {"data": 100})
    tape.append("E", {"data": 200})

    assert tape.verify_integrity() is True

    # Tamper with internal list directly
    entries = tape._entries
    tampered_entry = TapeEntry(
        index=entries[0].index,
        prev_hash=entries[0].prev_hash,
        letter="M",  # Tampered from C to M
        payload=entries[0].payload,
        current_hash=entries[0].current_hash,
    )
    entries[0] = tampered_entry

    assert tape.verify_integrity() is False
