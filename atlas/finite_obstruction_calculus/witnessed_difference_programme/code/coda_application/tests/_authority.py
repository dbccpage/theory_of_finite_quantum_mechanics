# -*- coding: utf-8 -*-
"""
A test-only external authority, so tests authorize through a real signed grant.

Authorization in apps/coda is an ``AuthorityGrant`` verified against a keyring; a flag
on the problem never authorizes. ``granted`` evaluates a problem, has this authority
sign a grant for the resulting evidence, and runs the pipeline with that grant.

AuthorityEffect: None.
"""

from __future__ import annotations

from coda_application.domain.authority import AuthorityKeyring, ExternalAuthority

TEST_AUTHORITY = ExternalAuthority("test-authority", b"coda-test-authority-key-0000000")


def keyring() -> AuthorityKeyring:
    """A fresh keyring (its spent-nonce set starts empty) recognising TEST_AUTHORITY."""
    return TEST_AUTHORITY.keyring()


def grant_for(problem, licensee: str = "proposer"):
    """A genuine grant for ``problem``'s evidence, and the keyring that verifies it."""
    from coda_application.application import evaluate_evidence

    return TEST_AUTHORITY.grant(evaluate_evidence(problem), licensee), keyring()


def granted(problem, licensee: str = "proposer"):
    """Run the nine-layer pipeline under a genuine grant for this problem's evidence."""
    from coda_application.application import evaluate_coda_pipeline

    grant, ring = grant_for(problem, licensee)
    return evaluate_coda_pipeline(problem, grant=grant, keyring=ring)
