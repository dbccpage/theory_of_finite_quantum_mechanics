"""Cryptographic hashing for homology complexes and witnesses."""
import hashlib
from typing import Sequence

def hash_matrix(mat) -> str:
    if hasattr(mat, "sha256"):
        return mat.sha256()
    return hashlib.sha256(str(mat).encode("utf-8")).hexdigest()

def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
