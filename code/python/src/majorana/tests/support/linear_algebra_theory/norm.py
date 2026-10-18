from fractions import Fraction


class NormError(Exception):
    pass


class NonPositiveWeight(NormError):
    def __init__(self, index, value):
        super().__init__(f"non-positive weight at index {index}: {value}")


class NegativeTolerance(NormError):
    def __init__(self, index, value):
        super().__init__(f"negative tolerance at index {index}: {value}")


class WeightProfile:
    def __init__(self, weights: list):
        self._weights = [Fraction(w) for w in weights]
        for i, w in enumerate(self._weights):
            if w <= 0:
                raise NonPositiveWeight(i, w)

    @classmethod
    def new(cls, weights: list):
        return cls(weights)

    def dim(self) -> int:
        return len(self._weights)

    def weights(self) -> list:
        return self._weights


class ToleranceProfile:
    def __init__(self, epsilon):
        self._epsilon = Fraction(epsilon)
        if self._epsilon < 0:
            raise NegativeTolerance(0, self._epsilon)

    @classmethod
    def new(cls, epsilon):
        return cls(epsilon)

    def epsilon(self) -> Fraction:
        return self._epsilon

