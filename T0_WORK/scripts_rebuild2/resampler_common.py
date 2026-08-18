"""
Shared Kaiser-windowed-sinc polyphase resampler prototype builder.
Companion d0_bench_integer_dsp_semantics_v1_7.md section 9.

For a given max(L,M) the continuous prototype (N_h, c, omega, h_id, Kaiser
window w, and their sum S) is identical regardless of which of the two
paired directions is being generated, because it depends only on
max(L,M) = 1/min(1/L,1/M). Only the final normalization scale
s = L_direction / S and the polyphase reshape (P = L_direction) differ
per direction. This module computes h_id, w and S once per prototype
with two independent evaluators, then a caller applies direction-specific
scale + reshape per table.

Evaluator A: interval arithmetic (mpmath.iv) -- rigorous enclosure.
Evaluator B: convergence procedure, plain mpmath.mp at dps=P and dps=2P.
"""
import sys
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts_rebuild2")
from common import mp, iv, round_half_even_from_interval, round_half_even_plain, CertificationError

BETA = 12
I0_TERM_CUTOFF = mp.mpf(2) ** -100


def i0_series_interval(x_iv):
    """I0(x) = sum_k ((x/2)^k / k!)^2, truncated when term < 2^-100 (companion def)."""
    half_x = x_iv / 2
    term = iv.mpf(1)  # k = 0 term: (1/1)^2 = 1
    total = iv.mpf(0)
    k = 0
    fact = 1
    while True:
        total += term
        if term.b < I0_TERM_CUTOFF:
            break
        k += 1
        fact *= k
        val = (half_x ** k) / fact
        term = val * val
        if k > 400:
            raise CertificationError("I0 series (interval) failed to converge within 400 terms")
    return total


def i0_series_plain(x, dps_check=None):
    half_x = x / 2
    term = mp.mpf(1)
    total = mp.mpf(0)
    k = 0
    fact = 1
    cutoff = mp.mpf(2) ** -100
    while True:
        total += term
        if term < cutoff:
            break
        k += 1
        fact *= k
        val = (half_x ** k) / fact
        term = val * val
        if k > 400:
            raise CertificationError("I0 series (plain) failed to converge within 400 terms")
    return total


def build_prototype_interval(max_LM, dps=60):
    """Returns (N_h, c, h_scaled_unnormalized_list_of_iv_intervals) i.e. h_id[n]*w[n]
    for n=0..N_h-1, plus S (interval) = sum of that list."""
    iv.dps = dps
    N_h = 24 * max_LM + 1
    c = (N_h - 1) // 2
    omega = iv.pi * iv.mpf(9) / 10 / max_LM
    i0_beta = i0_series_interval(iv.mpf(BETA))
    terms = [None] * N_h
    total = iv.mpf(0)
    for n in range(N_h):
        if n == c:
            h_id = omega / iv.pi
        else:
            arg = omega * (n - c)
            h_id = iv.sin(arg) / (iv.pi * (n - c))
        ratio = iv.mpf(n - c) / c
        inside = 1 - ratio * ratio
        # guard against tiny negative interval at the extreme edges due to rounding
        if inside.a < 0:
            inside = iv.mpf([max(mp.mpf('0'), inside.a), inside.b])
        x_win = BETA * iv.sqrt(inside)
        w = i0_series_interval(x_win) / i0_beta
        t = h_id * w
        terms[n] = t
        total += t
    return N_h, c, terms, total


def build_prototype_plain(max_LM, dps):
    mp.dps = dps
    N_h = 24 * max_LM + 1
    c = (N_h - 1) // 2
    omega = mp.pi * mp.mpf(9) / 10 / max_LM
    i0_beta = i0_series_plain(mp.mpf(BETA))
    terms = [None] * N_h
    total = mp.mpf(0)
    for n in range(N_h):
        if n == c:
            h_id = omega / mp.pi
        else:
            arg = omega * (n - c)
            h_id = mp.sin(arg) / (mp.pi * (n - c))
        ratio = mp.mpf(n - c) / c
        inside = 1 - ratio * ratio
        if inside < 0:
            inside = mp.mpf(0)
        x_win = BETA * mp.sqrt(inside)
        w = i0_series_plain(x_win) / i0_beta
        t = h_id * w
        terms[n] = t
        total += t
    return N_h, c, terms, total


def quantize_direction(N_h, terms_iv, S_iv, terms_plainP, S_plainP, terms_plain2P, S_plain2P,
                        L_direction, label, dps_iv=60, P=60):
    """
    Scale by s = L_direction / S for each evaluator independently, quantize to
    Q30 with round-half-to-even, cross-check all three evaluators agree per
    sample, return list of N_h integers (unnormalized reshape happens by caller).
    """
    scale_pow = mp.mpf(2) ** 30
    out = [None] * N_h
    disagreements = 0
    for n in range(N_h):
        # Evaluator A: interval
        s_iv = iv.mpf(L_direction) / S_iv
        scaled_iv = terms_iv[n] * s_iv * (iv.mpf(2) ** 30)
        lo = mp.mpf(scaled_iv.a)
        hi = mp.mpf(scaled_iv.b)
        try:
            nA = round_half_even_from_interval(lo, hi, label=f"{label}[{n}] evalA")
        except CertificationError as e:
            raise CertificationError(f"{label}[{n}]: evalA cert failure: {e}")

        # Evaluator B: convergence P vs 2P
        mp.dps = P
        sP = mp.mpf(L_direction) / S_plainP
        vP = terms_plainP[n] * sP * scale_pow
        nP = round_half_even_plain(vP, label=f"{label}[{n}] evalB@P")

        mp.dps = 2 * P
        s2P = mp.mpf(L_direction) / S_plain2P
        v2P = terms_plain2P[n] * s2P * scale_pow
        n2P = round_half_even_plain(v2P, label=f"{label}[{n}] evalB@2P")
        mp.dps = P

        if nP != n2P:
            raise CertificationError(f"{label}[{n}]: evalB P/2P disagree {nP} vs {n2P}")
        if nA != nP:
            disagreements += 1
            continue
        out[n] = nA
    return out, disagreements
