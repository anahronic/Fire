"""
Standard normal quantile function (probit) via own convergent Taylor series
for Phi(x) = 0.5 + (1/sqrt(2*pi)) * sum_k (-1)^k x^(2k+1) / (2^k k! (2k+1)),
inverted by high-precision Newton iteration (plain mpmath.mp), then certified
by rigorous interval-arithmetic bracketing (mpmath.iv) of the rounding
boundary -- this is the interval-arithmetic certification basis (option A,
companion section 14/7.1): Phi is strictly increasing (Phi' = pdf > 0
everywhere), so if interval-evaluated Phi(lo) < p < Phi(hi) with lo, hi the
Q24 rounding boundary points, the true root is certified inside (lo, hi) and
rounds to the candidate integer -- no interval root search required.
"""
import sys
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts")
from common import mp, iv, CertificationError

TERM_CUTOFF_EXP = -100


def phi_plain(x, dps):
    mp.dps = dps
    x2 = x * x
    term = x
    total = mp.mpf(0)
    k = 0
    fact = 1
    pow2 = 1
    cutoff = mp.mpf(2) ** TERM_CUTOFF_EXP
    while True:
        total += term
        if abs(term) < cutoff:
            break
        k += 1
        fact *= k
        pow2 *= 2
        term = ((-1) ** k) * (x ** (2 * k + 1)) / (pow2 * fact * (2 * k + 1))
        if k > 400:
            raise CertificationError("Phi series (plain) failed to converge within 400 terms")
    S = total
    return mp.mpf("0.5") + S / mp.sqrt(2 * mp.pi)


def phi_interval(x_iv):
    total = iv.mpf(0)
    term = x_iv
    k = 0
    fact = 1
    pow2 = 1
    cutoff = iv.mpf(2) ** TERM_CUTOFF_EXP
    while True:
        total += term
        if abs(term.a) < cutoff and abs(term.b) < cutoff:
            break
        k += 1
        fact *= k
        pow2 *= 2
        term = ((-1) ** k) * (x_iv ** (2 * k + 1)) / (pow2 * fact * (2 * k + 1))
        if k > 400:
            raise CertificationError("Phi series (interval) failed to converge within 400 terms")
    S = total
    return iv.mpf("0.5") + S / iv.sqrt(2 * iv.pi)


def pdf_plain(x, dps):
    mp.dps = dps
    return mp.e ** (-(x * x) / 2) / mp.sqrt(2 * mp.pi)


def newton_solve(p_val, dps, x0, max_iter=20):
    mp.dps = dps
    x = mp.mpf(x0)
    tol = mp.mpf(10) ** (-(dps - 8))
    for _ in range(max_iter):
        Phi_val = phi_plain(x, dps)
        pdf_val = pdf_plain(x, dps)
        dx = (Phi_val - p_val) / pdf_val
        x = x - dx
        if abs(dx) < tol:
            break
    else:
        raise CertificationError(f"newton_solve: did not converge for p={p_val}")
    return x


def certify_bracket(n_candidate, p_val, dps):
    """
    Rigorously certify that ICDF(p_val) rounds (half-to-even) to n_candidate
    at Q24, by interval-evaluating Phi at the two rounding-boundary abscissas
    and checking strict bracketing (relies on Phi strictly increasing).
    """
    iv.dps = dps
    scale = iv.mpf(2) ** 24
    lo_x = (iv.mpf(n_candidate) - iv.mpf('0.5')) / scale
    hi_x = (iv.mpf(n_candidate) + iv.mpf('0.5')) / scale
    Phi_lo = phi_interval(lo_x)
    Phi_hi = phi_interval(hi_x)
    if not (Phi_lo.b < p_val < Phi_hi.a):
        raise CertificationError(
            f"bracket cert failed for n={n_candidate}: Phi_lo={Phi_lo}, p={p_val}, Phi_hi={Phi_hi}"
        )
    return True
