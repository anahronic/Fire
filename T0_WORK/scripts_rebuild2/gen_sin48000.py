"""
SIN48000_Q30[k] = round_half_to_even( sin(2*pi*k/48000) * 2^30 ),  k = 0..47999
Companion d0_bench_integer_dsp_semantics_v1_7.md section 3.

Evaluator A: interval arithmetic (mpmath.iv), rigorous enclosure.
Evaluator B: convergence procedure, plain mpmath.mp at P=60 and 2P=120 dps.
"""
import sys, time
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts_rebuild2")
from common import (mp, iv, round_half_even_from_interval, round_half_even_plain,
                     CertificationError, int64_le, sha256_bytes)

Q = 30
SCALE = mp.mpf(2) ** Q
N = 48000

def eval_A_interval(k, dps=60):
    iv.dps = dps
    theta = 2 * iv.pi * k / N
    s = iv.sin(theta)
    scaled = s * (iv.mpf(2) ** Q)
    lo = mp.mpf(scaled.a)
    hi = mp.mpf(scaled.b)
    return round_half_even_from_interval(lo, hi, label=f"SIN48000[{k}] evalA")

def eval_B_convergence(k, P=60):
    mp.dps = P
    theta = 2 * mp.pi * k / N
    v1 = mp.sin(theta) * (mp.mpf(2) ** Q)
    n1 = round_half_even_plain(v1, label=f"SIN48000[{k}] evalB@P")
    mp.dps = 2 * P
    theta2 = 2 * mp.pi * k / N
    v2 = mp.sin(theta2) * (mp.mpf(2) ** Q)
    n2 = round_half_even_plain(v2, label=f"SIN48000[{k}] evalB@2P")
    mp.dps = P
    if n1 != n2:
        raise CertificationError(f"SIN48000[{k}] evalB P/2P disagree: {n1} vs {n2}")
    return n1

ANCHORS = {0: 0, 4000: 536870912, 12000: 1073741824, 24000: 0, 36000: -1073741824}

def main():
    t0 = time.time()
    values = [None] * N
    disagreements = 0
    log_lines = []
    for k in range(N):
        a = eval_A_interval(k)
        b = eval_B_convergence(k)
        if a != b:
            disagreements += 1
            log_lines.append(f"DISAGREE k={k} A={a} B={b}")
            continue
        values[k] = a
    if disagreements:
        raise SystemExit(f"SIN48000_Q30: {disagreements} evaluator disagreements -- T0 FAIL")

    for k, expected in ANCHORS.items():
        if values[k] != expected:
            raise SystemExit(f"SIN48000_Q30 anchor FAIL at k={k}: got {values[k]} expected {expected}")

    out = b"".join(int64_le(v) for v in values)
    assert len(out) == N * 8
    with open("E:/000_Audiotext/T0_OUTPUT_BUILD2/SIN48000_Q30.bin", "wb") as f:
        f.write(out)
    digest = sha256_bytes(out)
    elapsed = time.time() - t0
    report = {
        "table_id": "SIN48000_Q30",
        "entry_count": N,
        "bytes": len(out),
        "sha256": digest,
        "evaluator_disagreements": disagreements,
        "anchors_ok": True,
        "elapsed_sec": round(elapsed, 2),
    }
    print(report)
    with open("E:/000_Audiotext/T0_WORK/logs_rebuild2/sin48000_log.txt", "w") as f:
        f.write(str(report) + "\n")
        f.write("\n".join(log_lines))

if __name__ == "__main__":
    main()
