"""Bounded executable witnesses for the Witnessed Difference Programme.

Every public result is finite and replayable.  Nothing in this package mints
authority or upgrades an open mathematical claim into a theorem.
"""

from .outcomes import Accepted, AuthorityEffect, RefusalCode, Refused

__all__ = ["Accepted", "AuthorityEffect", "Refused", "RefusalCode"]
# Executable finite evidence; AuthorityEffect: None.
