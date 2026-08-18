"""
D0 Bench T0 offline tooling -- shared utilities.

NOT src/d0bench. NOT a reference implementation. Offline table-generation
and verification tooling only, produced for step T0 per Prompt.md / companion
d0_bench_integer_dsp_semantics_v1_7.md section 14.

Tool versions (record in T0_REPORT.md):
    Python  3.12.10  (E:\\000_Audiotext\\T0_WORK\\venv)
    mpmath  1.4.1
"""
import hashlib
import json
import struct
from fractions import Fraction

import mpmath
from mpmath import mp, iv


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def LP(x: bytes) -> bytes:
    """LP(x) = u32be(len(x)) || x"""
    return struct.pack(">I", len(x)) + x


def int64_le(n: int) -> bytes:
    """signed int64 little-endian two's complement"""
    return struct.pack("<q", n)


def canonical_json_bytes(obj) -> bytes:
    """
    JCS bytes for our restricted data model: plain non-negative JSON
    integers, ASCII strings, arrays (order preserved), objects (keys
    sorted by code point, which for ASCII-only keys equals RFC 8785
    UTF-16 code unit ordering), no floats anywhere in this schema.
    """
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Round-half-to-even quantization of a real target value r*2^Q to an integer,
# certified two ways:
#   - interval bounds [lo, hi] (mpmath.iv) enclosing r*2^Q rigorously
#   - plain high precision value(s) at dps=P and dps=2P (mpmath.mp)
# ---------------------------------------------------------------------------

class CertificationError(Exception):
    pass


def round_half_even_from_interval(lo, hi, label=""):
    """
    lo, hi: mpmath.mpf (already extracted from an mpmath.iv.mpf bound),
    both understood to rigorously bracket the true scaled value.
    Returns the unique nearest integer (ties to even), certifying the
    interval width is far below the 0.25 ULP requirement and that no
    rounding tie is possible at this precision.
    """
    width = hi - lo
    if width < 0 or width > mp.mpf("0.25"):
        raise CertificationError(
            f"{label}: interval width {width} not < 0.25 ULP -- increase precision"
        )
    mid = (lo + hi) / 2
    n_floor = int(mp.floor(mid))
    frac = mid - n_floor
    # distance from the 0.5 tie boundary must exceed the interval half-width
    # by a wide margin, else the rounding direction is not certified unique.
    half_width = width / 2
    if abs(frac - mp.mpf("0.5")) <= half_width + mp.mpf("1e-20"):
        raise CertificationError(
            f"{label}: value too close to round-half tie at this precision"
        )
    n = n_floor + 1 if frac > mp.mpf("0.5") else n_floor
    # cross-check: both lo and hi independently round to the same n
    for bound, bname in ((lo, "lo"), (hi, "hi")):
        bf = int(mp.floor(bound))
        bfrac = bound - bf
        bn = bf + 1 if bfrac > mp.mpf("0.5") else bf
        if bn != n:
            raise CertificationError(
                f"{label}: bound {bname} rounds to {bn} != midpoint round {n}"
            )
    return n


def round_half_even_plain(x, label=""):
    """
    x: mpmath.mp.mpf at working precision dps. Same tie logic as above,
    used for the convergence-procedure evaluator (P vs 2P).
    """
    n_floor = int(mp.floor(x))
    frac = x - n_floor
    if abs(frac - mp.mpf("0.5")) < mp.mpf(10) ** (-(mp.dps - 5)):
        raise CertificationError(f"{label}: value too close to round-half tie")
    return n_floor + 1 if frac > mp.mpf("0.5") else n_floor


def iv_bounds(x_iv):
    """Extract (lo, hi) as mp.mpf from an mpmath.iv.mpf, at current iv precision."""
    return mp.mpf(x_iv.a), mp.mpf(x_iv.b)
