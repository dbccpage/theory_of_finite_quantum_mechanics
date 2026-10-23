"""Exact checks for strict positivity of the nonzero modes on ``0 < theta <= 1/192``.

This is the section "Window positivity" (TL-10 to TL-12) of
``docs/meron_euclidean_thermodynamic_limit.md``. The route
does not bound ``sup_u |g - 1/2|``. It uses three facts, each checked here:

1. Open chains are exactly SU(2) invariant. The staggered spin lowering
   ``G = sum_x (-1)^x J_x c_x`` (``J_x`` the Jordan-Wigner string) commutes with
   ``K``. On every bond ``[G, Y] = 4(Q_b - T11_b)`` and ``[G, Y'] = 4(Q_b - T00_b)``
   for explicit two-site ``Y, Y'`` (signed by ``(-1)^b``), so every Gibbs state of an open chain gives
   ``<h_b> = <P_b - Q_b> = (4 <P_b> - 1) / 3``.
2. A dimer trial state bounds the bond energy from below. Its exact
   expectations are ``(1 + s) / (4 + s)`` on dimer bonds and ``1/4`` on the
   bonds between dimers.
3. The Lehmann second moment is ``theta^3 / |I| * sum_x <W_x>`` with
   ``W_x = [ad_K^2 a_x, ad_K A]``. Its norm is at most 11/2 in every local
   configuration (exact certificate; the bound 5 fails).

Every value under ``exact`` is integer or Fraction arithmetic. The entries
under ``diagnostics`` use floating point and prove nothing.

Run ``python -m meron_thermodynamic_limit.positivity`` from ``code/`` to print
JSON.
"""

from __future__ import annotations

import json
from fractions import Fraction

import numpy as np

from . import car
from .checks import psd_exact

W_SCALE = 256            # 256 W_x = [ad_{4K}^2 (2a_x), ad_{4K} (2A)] is an integer matrix
W_BOUND = Fraction(11, 2)    # certified: ||W_x|| <= 11/2
W_FAILING = Fraction(5)      # mutation: ||W_x|| <= 5 is false in the interior
FOUR_PI_SQ_FLOOR = 39    # 4 pi^2 > 39, checked exactly below
WINDOW = Fraction(1, 192)
LIMIT_RADIUS = Fraction(1, 96)   # TL-3's open-chain limit exists on |theta| < 1/96
FLOOR = Fraction(1, 9)   # omega^2 khat >= theta^2 * FLOOR on the window
SHORT_CHAINS = (2, 4, 6, 8)
HOST_CHAIN = 9           # sites 0..8: every x <= 4 has its full right neighbourhood


# --------------------------------------------------------------------------- #
# Operators
# --------------------------------------------------------------------------- #

def _ad(k: np.ndarray, x: np.ndarray) -> np.ndarray:
    """``[k, x]`` in exact int64 through ``car._product`` (linear in the nonzeros)."""
    return car._product(k, x) - car._product(x, k)


def _numbers(n: int) -> list[np.ndarray]:
    return [c.T @ c for c in car.annihilators(n)]


def spin_lowerings(n: int) -> list[np.ndarray]:
    """``sigma_x = J_x c_x``: commuting single-site lowerings on an open chain."""
    cs = car.annihilators(n)
    num = [c.T @ c for c in cs]
    eye = np.eye(1 << n, dtype=np.int64)
    out = []
    string = eye.copy()
    for x in range(n):
        out.append(string @ cs[x])
        string = string @ (eye - 2 * num[x])
    return out


def staggered_lowering(n: int, *, staggered: bool = True) -> np.ndarray:
    sig = spin_lowerings(n)
    return sum(((-1) ** x if staggered else 1) * sig[x] for x in range(n))


def w_int(n: int, x: int) -> np.ndarray:
    """``256 W_x`` on the open chain ``0..n-1``; ``W_x = [ad_K^2 a_x, ad_K A]``."""
    k4, a2, _ = car.chain(0, n - 1)
    big_a = sum(a2[s] for s in range(n))
    left = _ad(k4, _ad(k4, a2[x]))
    right = _ad(k4, big_a)
    return _ad(left, right)


def _number_blocks(m: np.ndarray, n: int) -> list[np.ndarray]:
    """Split an operator that conserves the particle number into its blocks."""
    pops = np.array([bin(v).count("1") for v in range(1 << n)])
    off = m[pops[:, None] != pops[None, :]]
    if off.size and np.abs(off).max() != 0:
        raise ValueError("operator does not conserve the particle number")
    return [m[np.ix_(pops == k, pops == k)] for k in range(n + 1)]


def w_cases() -> list[tuple[int, int]]:
    """Every local configuration of ``W_x`` on an even open chain.

    ``W_x`` is supported on ``[x-4, x+4]`` cut to the chain. Chains of length at
    most 8 are listed up to reflection (``x < n/2``; reflection maps ``W_x`` to
    ``W_{n-1-x}``). On an even chain of length at least 10 every ``x`` has at
    least four sites on one side, so its ``W_x`` is the same CAR polynomial as
    some ``x <= 4`` on the host chain ``0..8`` or its mirror image.
    """
    cases = [(n, x) for n in SHORT_CHAINS for x in range((n + 1) // 2)]
    cases += [(HOST_CHAIN, x) for x in range(5)]
    return cases


# --------------------------------------------------------------------------- #
# Exact certificates
# --------------------------------------------------------------------------- #

def su2_certificate(lengths=(2, 4, 6, 8), *, staggered: bool = True) -> dict:
    """``[K, G] = 0`` and the two ladder identities on every bond, exactly."""
    out = {}
    for n in lengths:
        k4, _, fourp = car.chain(0, n - 1)
        g = staggered_lowering(n, staggered=staggered)
        sig = spin_lowerings(n)
        num = _numbers(n)
        eye = np.eye(1 << n, dtype=np.int64)
        commutes = not np.any(_ad(k4, g))
        ladders = True
        for b in range(n - 1):
            n0, n1 = num[b], num[b + 1]
            s0, s1 = sig[b].T, sig[b + 1].T          # raising operators
            q4 = 4 * (n0 + n1 - 2 * n0 @ n1) - fourp[(b, b + 1)]
            t11 = n0 @ n1
            t00 = (eye - n0) @ (eye - n1)
            sign = (-1) ** b                          # G is staggered
            y11 = sign * 2 * (s0 @ n1 - n0 @ s1)
            y00 = sign * 2 * (s1 - s0) + y11
            ladders &= not np.any(_ad(g, y11) - (q4 - 4 * t11))
            ladders &= not np.any(_ad(g, y00) - (q4 - 4 * t00))
        out[n] = {"K_commutes_with_G": bool(commutes), "ladders": bool(ladders)}
    out["all_pass"] = all(v["K_commutes_with_G"] and v["ladders"] for v in out.values())
    return out


def w_norm_certificate(bound: Fraction = W_BOUND) -> dict:
    """``(256 bound)^2 I - (256 W_x)^2`` is PSD in every local configuration."""
    if type(bound) not in (int, Fraction) or bound < 0:
        raise ValueError("norm bound must be an exact nonnegative rational")
    scaled = W_SCALE * Fraction(bound)
    if scaled.denominator != 1:
        raise ValueError("256 * bound must be an integer")
    c2 = int(scaled) ** 2
    rows = []
    for n, x in w_cases():
        w = w_int(n, x)
        if np.any(w != w.T):
            raise ValueError("W_x is not Hermitian")
        if np.abs(w).max() > 10**4:
            raise OverflowError("int64 guard")
        ok = True
        for blk in _number_blocks(w, n):
            if blk.size == 0:
                continue
            m = c2 * np.eye(len(blk), dtype=object) - blk.astype(object) @ blk.astype(object)
            if not psd_exact(m):
                ok = False
                break
        rows.append({"chain": n, "x": x, "psd": ok})
    return {"bound": str(bound), "cases": rows, "all_pass": all(r["psd"] for r in rows)}


def dimer_trial_certificate(n: int = 6, s: Fraction = Fraction(1, 3)) -> dict:
    """Exact dimer-trial expectations ``<P_b>_0`` on the open chain ``0..n-1``.

    ``rho_0`` is proportional to ``prod_d (I + s P_d)`` over the dimer bonds
    ``(0,1), (2,3), ...``; ``s = e^t - 1``.
    """
    if type(n) is not int or n < 2 or n % 2:
        raise ValueError("an even chain with at least two sites is required")
    if type(s) not in (int, Fraction) or s < -1:
        raise ValueError("positive trial operator requires exact s >= -1")
    s = Fraction(s)
    _, _, fourp = car.chain(0, n - 1)
    p, q = s.numerator, s.denominator
    eye = np.eye(1 << n, dtype=object)
    r = eye.copy()
    for d in range(0, n, 2):
        r = r @ (4 * q * eye + p * fourp[(d, d + 1)].astype(object))
    tr = int(np.trace(r))
    on = Fraction(1 + s, 4 + s)
    vals = {}
    for b in range(n - 1):
        vals[b] = Fraction(int(np.trace(r @ fourp[(b, b + 1)].astype(object))), 4 * tr)
    dimer_ok = all(vals[b] == (on if b % 2 == 0 else Fraction(1, 4)) for b in vals)
    norm_ok = Fraction(tr, (4 * q) ** (n // 2)) == (4 + s) ** (n // 2)
    return {"n": n, "s": str(s), "dimer_bonds": str(on), "between": "1/4",
            "all_pass": bool(dimer_ok and norm_ok)}


def _poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            out[i + j] += u * v
    return out


def elementary_g_identity(lead: int = 3) -> bool:
    """With ``y = t/4 + t^2/8``: ``(y - y^2/2)/2 - t/8 = t^2 (lead - t - t^2/4) / 64``.

    True exactly for ``lead = 3``. Together with ``e^t >= 1 + t + t^2/2`` and
    ``log(1 + y) >= y - y^2/2`` it gives ``g(t) >= t^2 (3 - t - t^2/4) / 64``.
    """
    y = [Fraction(0), Fraction(1, 4), Fraction(1, 8)]
    y2 = _poly_mul(y, y)
    lhs = [Fraction(0)] * 5
    for i, v in enumerate(y):
        lhs[i] += v / 2
    for i, v in enumerate(y2):
        lhs[i] -= v / 4
    lhs[1] -= Fraction(1, 8)
    rhs = [Fraction(0), Fraction(0), Fraction(lead, 64), Fraction(-1, 64), Fraction(-1, 256)]
    return lhs == rhs


def window_floor(theta: Fraction, *, bound: Fraction = W_BOUND) -> Fraction:
    """Lower bound of ``omega^2 khat / theta^2`` at ``m = 1``, decreasing in theta.

    ``2 theta Fbar >= (8/3) g`` and ``g >= theta^2 (3 - theta - theta^2/4)/64``
    give ``(3 - theta - theta^2/4)/24``; the second moment costs at most
    ``bound * theta / (4 pi^2) < bound * theta / 39``.
    """
    return (3 - theta - theta * theta / 4) / 24 - Fraction(bound) * theta / FOUR_PI_SQ_FLOOR


def window_certificate() -> dict:
    pi_lo = Fraction(314159, 100000)
    return {
        "four_pi_sq_above_39": 4 * pi_lo * pi_lo > FOUR_PI_SQ_FLOOR,
        "floor_at_1_192": str(window_floor(WINDOW)),
        "floor_at_1_192_ge_1_9": window_floor(WINDOW) >= FLOOR,
        "floor_at_1_96_ge_1_9": window_floor(LIMIT_RADIUS) >= FLOOR,
        "g_identity": elementary_g_identity(),
    }


def mutations() -> dict:
    """Each must be False: a wrong ingredient breaks an exact check."""
    return {
        "norm_bound_5": w_norm_certificate(W_FAILING)["all_pass"],
        "unstaggered_G": su2_certificate((4, 6), staggered=False)["all_pass"],
        "g_identity_lead_4": elementary_g_identity(4),
        "floor_1_8_at_1_192": window_floor(WINDOW) >= Fraction(1, 8),
    }


# --------------------------------------------------------------------------- #
# Floating-point diagnostics (not evidence)
# --------------------------------------------------------------------------- #

def lehmann_diagnostics(lengths=(4, 6), thetas=(1 / 192, 0.05), nodes: int = 2001) -> list[dict]:
    rows = []
    for n in lengths:
        k4, a2, fourp = car.chain(0, n - 1)
        k = k4 / 4.0
        big_a = sum(a2[s] for s in range(n)) / 2.0
        num = _numbers(n)
        cs = car.annihilators(n)
        e, v = np.linalg.eigh(k)
        ab = v.T @ big_a @ v
        ws = [w_int(n, x) / W_SCALE for x in range(n)]
        for th in thetas:
            p = np.exp(-th * (e - e.min()))
            p /= p.sum()
            rho = v @ np.diag(p) @ v.T

            def ex(op):
                return float(np.trace(rho @ op))

            fbar = sum(ex(cs[b].T @ cs[b + 1] + cs[b + 1].T @ cs[b]) for b in range(n - 1)) / n
            wbar = sum(ex(w) for w in ws) / n
            dl = th * (e[None, :] - e[:, None])
            wt = np.abs(ab) ** 2 * (p[:, None] - p[None, :]) * dl / n
            om = 2 * np.pi
            khat = float((wt / (dl ** 2 + om ** 2)).sum())
            us = np.linspace(0.0, 1.0, nodes)
            vals = []
            for u in us:
                au = v @ (np.exp(u * th * e)[:, None] * ab * np.exp(-u * th * e)[None, :]) @ v.T
                vals.append(np.trace(rho @ au @ big_a) / n)
            quad = float(np.trapezoid(np.array(vals) * np.exp(-1j * om * us), us).real)
            g = 0.5 * np.log((np.exp(th) + 3) / 4) - th / 8
            q_minus_t = max(
                abs(ex(4 * (num[b] + num[b + 1] - 2 * num[b] @ num[b + 1]) - fourp[(b, b + 1)]
                       - 4 * num[b] @ num[b + 1])) / 4
                for b in range(n - 1))
            rows.append({
                "n": n, "theta": th,
                "kms_jump_minus_2thetaF": float(wt.sum() - 2 * th * fbar),
                "moment_minus_theta3W": float((wt * dl ** 2).sum() - th ** 3 * wbar),
                "khat_lehmann": khat, "khat_quadrature": quad,
                "Fbar": fbar, "Fbar_floor": 4 * g / (3 * th),
                "khat_floor": th ** 2 / (36 * np.pi ** 2),
                "max_Q_minus_T11": q_minus_t,
            })
    return rows


def w_norms_float() -> dict:
    return {f"{n},{x}": float(np.linalg.norm(w_int(n, x).astype(float), 2) / W_SCALE)
            for n, x in w_cases()}


def ring_su2_defect_float(lengths=(4, 6), thetas=(0.05, 1 / 192)) -> list[dict]:
    """``<Q_b> - <T00_b>`` and ``<Q_b> - <T11_b>`` on the ring, bond ``(0, 1)``.

    Open chains have both exactly zero (``su2_certificate``); the ring at finite
    ``L`` does not. Floating point: these are the numbers the docs quote for
    the ring, and they prove nothing.
    """
    rows = []
    for length in lengths:
        k4, _, fourp = car.ring(length)
        num = _numbers(length)
        eye = np.eye(1 << length)
        e, v = np.linalg.eigh(k4 / 4.0)
        q = (4 * (num[0] + num[1] - 2 * num[0] @ num[1]) - fourp[(0, 1)]) / 4.0
        t00 = (eye - num[0]) @ (eye - num[1])
        t11 = num[0] @ num[1]
        for th in thetas:
            p = np.exp(-th * (e - e.min()))
            p /= p.sum()
            rho = v @ np.diag(p) @ v.T
            rows.append({"L": length, "theta": th,
                         "Q_minus_T00": float(np.trace(rho @ q) - np.trace(rho @ t00)),
                         "Q_minus_T11": float(np.trace(rho @ q) - np.trace(rho @ t11))})
    return rows


def run_all() -> dict:
    return {
        "exact": {
            "su2": su2_certificate(),
            "w_norm": w_norm_certificate(),
            "dimer": dimer_trial_certificate(),
            "window": window_certificate(),
            "mutations": mutations(),
        },
        "diagnostics": {"lehmann": lehmann_diagnostics(), "w_norms": w_norms_float(),
                        "ring_su2_defect": ring_su2_defect_float()},
    }


if __name__ == "__main__":  # pragma: no cover
    print(json.dumps(run_all(), indent=1, default=str))
