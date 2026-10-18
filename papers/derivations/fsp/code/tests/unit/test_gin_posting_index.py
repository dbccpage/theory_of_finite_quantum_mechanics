"""
test_gin_posting_index.py — Unit Tests for Mock GIN Index and Inverted Posting List
Status: Unit Test Suite
AuthorityEffect: None
"""

import pytest
import sys
from pathlib import Path

# Add code directory to path
current_dir = Path(__file__).resolve().parent
pkg_dir = current_dir.parent.parent
if str(pkg_dir) not in sys.path:
    sys.path.insert(0, str(pkg_dir))

from fermion_gin_index import MockFermionGinIndex


class TestGinPostingIndex:
    def test_gin_posting_index_creation_and_fast_lookup(self):
        """Validates that MockFermionGinIndex builds inverted posting lists and resolves set intersections."""
        gin = MockFermionGinIndex(in_memory=True)
        try:
            gin.index_configuration(1, "TestModel", {1, 2}, 4, 1.0, 1, 1)
            gin.index_configuration(2, "TestModel", {2, 3}, 4, 1.0, -1, 1)
            gin.index_configuration(3, "TestModel", {1, 3}, 4, 1.0, 1, 1)

            # Posting list of mode 2 contains {1, 2}
            assert gin.posting_index[2] == {1, 2}
            # Posting list of mode 1 contains {1, 3}
            assert gin.posting_index[1] == {1, 3}

            # Query: required {1, 2} -> {1}
            res = gin.query_by_modes(required_modes={1, 2}, forbidden_modes=set())
            assert res == {1}

            # Query: required {2}, forbidden {1} -> {2}
            res2 = gin.query_by_modes(required_modes={2}, forbidden_modes={1})
            assert res2 == {2}
        finally:
            gin.close()

    def test_gin_find_spectator_involution_partner(self):
        """Validates that GIN inverted lookup finds involution partners with exact spectator preservation."""
        gin = MockFermionGinIndex(in_memory=True)
        try:
            gin.index_configuration(1, "TestModel", {1, 4}, 4, 1.0, 1, 1)
            gin.index_configuration(2, "TestModel", {2, 4}, 4, 1.0, -1, 1)
            gin.index_configuration(3, "TestModel", {3, 4}, 4, 1.0, 1, 1)

            # Flip modes {1, 2}: partner of 1 should be 2
            partner = gin.find_involution_partner(cfg_id=1, flip_modes={1, 2}, total_modes=4)
            assert partner == 2
        finally:
            gin.close()

    def test_gin_posting_empty_query(self):
        """Empty query returns all or empty depending on mode specification."""
        gin = MockFermionGinIndex(in_memory=True)
        try:
            gin.index_configuration(1, "TestModel", {1}, 2, 1.0, 1, 1)
            gin.index_configuration(2, "TestModel", {2}, 2, 1.0, -1, 1)
            # Query non-existent mode
            res = gin.query_by_modes(required_modes={99}, forbidden_modes=set())
            assert res == set()
        finally:
            gin.close()
