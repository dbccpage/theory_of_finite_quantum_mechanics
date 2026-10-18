"""Exact adjoint braid action on a declared list of Majorana generators.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

MAX_BRAID_MODES: int = 1_048_576


class BraidActionError(Exception):
    pass


@dataclass(frozen=True)
class SignedMajorana:
    mode: int  # 1-indexed mode
    sign: int  # +1 or -1

    def __post_init__(self) -> None:
        if self.sign not in (1, -1):
            raise BraidActionError(f"sign must be +1 or -1, got {self.sign}")
        if self.mode < 1:
            raise BraidActionError(f"mode must be >= 1, got {self.mode}")


class MajoranaBraidAction:
    def __init__(self, images: Sequence[SignedMajorana]) -> None:
        count = len(images)
        if count < 2 or count > MAX_BRAID_MODES:
            raise BraidActionError(f"Mode count {count} outside 2..={MAX_BRAID_MODES}")
        seen_modes = set()
        for sm in images:
            if sm.mode < 1 or sm.mode > count:
                raise BraidActionError(f"mode {sm.mode} outside 1..={count}")
            if sm.mode in seen_modes:
                raise BraidActionError(f"duplicate mode {sm.mode}")
            seen_modes.add(sm.mode)
        self._images = tuple(images)
        self._count = count

    @classmethod
    def try_from_images(cls, images: Sequence[SignedMajorana]) -> MajoranaBraidAction:
        return cls(images)

    @classmethod
    def identity(cls, count: int) -> MajoranaBraidAction:
        if count < 2 or count > MAX_BRAID_MODES:
            raise BraidActionError(f"Mode count {count} outside 2..={MAX_BRAID_MODES}")
        return cls([SignedMajorana(mode=j, sign=1) for j in range(1, count + 1)])

    @classmethod
    def elementary(cls, count: int, index: int, inverse: bool = False) -> MajoranaBraidAction:
        if count < 2 or count > MAX_BRAID_MODES:
            raise BraidActionError(f"Mode count {count} outside 2..={MAX_BRAID_MODES}")
        if index < 1 or index >= count:
            raise BraidActionError(f"braid index {index} outside 1..{count}")
        images = [SignedMajorana(mode=j, sign=1) for j in range(1, count + 1)]
        # index is 1-based, list is 0-based:
        # gamma_j -> gamma_{j+1}, gamma_{j+1} -> -gamma_j
        j0 = index - 1
        j1 = index
        if not inverse:
            images[j0] = SignedMajorana(mode=index + 1, sign=1)
            images[j1] = SignedMajorana(mode=index, sign=-1)
        else:
            images[j0] = SignedMajorana(mode=index + 1, sign=-1)
            images[j1] = SignedMajorana(mode=index, sign=1)
        return cls(images)

    @classmethod
    def from_word(cls, count: int, steps: Sequence[tuple[int, bool]]) -> MajoranaBraidAction:
        action = cls.identity(count)
        for idx, inv in steps:
            elem = cls.elementary(count, idx, inv)
            action = action.compose(elem)
        return action

    def append(self, index: int, inverse: bool = False) -> None:
        elem = self.elementary(self._count, index, inverse)
        composed = self.compose(elem)
        self._images = composed._images

    def mode_count(self) -> int:
        return self._count

    def image(self, mode: int) -> SignedMajorana:
        if mode < 1 or mode > self._count:
            raise BraidActionError(f"mode {mode} outside 1..={self._count}")
        return self._images[mode - 1]

    def images(self) -> tuple[SignedMajorana, ...]:
        return self._images

    def compose(self, other: MajoranaBraidAction) -> MajoranaBraidAction:
        if self._count != other._count:
            raise BraidActionError(f"Dimension mismatch {self._count} != {other._count}")
        new_images = []
        for j in range(1, self._count + 1):
            target = self.image(j)
            second = other.image(target.mode)
            new_images.append(SignedMajorana(mode=second.mode, sign=target.sign * second.sign))
        return MajoranaBraidAction(new_images)

    def inverse(self) -> MajoranaBraidAction:
        # Inverse permutation
        inv_images = [None] * self._count
        for j in range(1, self._count + 1):
            img = self.image(j)
            inv_images[img.mode - 1] = SignedMajorana(mode=j, sign=img.sign)
        return MajoranaBraidAction(inv_images)

    def determinant_sign(self) -> int:
        # Sign of permutation * product of signs
        perm = [img.mode - 1 for img in self._images]
        sign = 1
        n = self._count
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                cycle_len = 0
                curr = i
                while not visited[curr]:
                    visited[curr] = True
                    curr = perm[curr]
                    cycle_len += 1
                if cycle_len % 2 == 0:
                    sign = -sign
        for img in self._images:
            sign *= img.sign
        return sign
