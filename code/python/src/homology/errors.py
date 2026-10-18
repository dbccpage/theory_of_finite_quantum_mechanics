"""Homology error definitions."""
class HomologyError(Exception):
    pass

class NonZeroCompositionError(HomologyError):
    pass

class DimensionMismatchError(HomologyError):
    pass
