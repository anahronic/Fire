"""
ICDF_Q24[65536] -- GENERATED_REAL, companion sections 7 and 14.
ICDF_Q24[u] = round_half_to_even( invnorm((u+0.5)/65536) * 2^24 ), u=0..65535.

Evaluator A: interval-arithmetic certified bracket around the Q24 rounding
             boundary (see icdf_common.certify_bracket) -- certified basis.
Evaluator B: convergence procedure, plain mpmath.mp Newton solve at P and 2P
             dps, requiring identical rounded results -- certified basis.
Both evaluators must agree on every one of the 65536 entries.
"""
import sys, time, statistics
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts_rebuild2")
from common import mp, round_half_even_plain, int64_le, sha256_bytes, CertificationError
from icdf_common import newton_solve, certify_bracket

P = 60
N = 65536
OUT = "E:/000_Audiotext/T0_OUTPUT_BUILD2/ICDF_Q24.bin"
LOG = "E:/000_Audiotext/T0_WORK/logs_rebuild2/icdf_log.txt"


def main():
    t0 = time.time()
    nd = statistics.NormalDist()
    values = [None] * N
    disagreements = 0
    x_prev_P = None
    x_prev_2P = None
    progress_every = 4096

    for u in range(N):
        p_frac_num = 2 * u + 1
        p_frac_den = 131072

        # --- evaluator B: plain Newton at P then 2P, must agree ---
        mp.dps = P
        p_val_P = mp.mpf(p_frac_num) / mp.mpf(p_frac_den)
        x0 = nd.inv_cdf(p_frac_num / p_frac_den) if x_prev_P is None else float(x_prev_P)
        x_P = newton_solve(p_val_P, P, x0)
        n_P = round_half_even_plain(x_P * (mp.mpf(2) ** 24), label=f"ICDF[{u}] evalB@P")

        mp.dps = 2 * P
        p_val_2P = mp.mpf(p_frac_num) / mp.mpf(p_frac_den)
        x0_2P = float(x_prev_2P) if x_prev_2P is not None else float(x_P)
        x_2P = newton_solve(p_val_2P, 2 * P, x0_2P)
        n_2P = round_half_even_plain(x_2P * (mp.mpf(2) ** 24), label=f"ICDF[{u}] evalB@2P")
        mp.dps = P

        if n_P != n_2P:
            raise SystemExit(f"ICDF_Q24[{u}]: evalB P/2P disagree {n_P} vs {n_2P} -- T0 FAIL")

        # --- evaluator A: interval bracket certification of n_P ---
        try:
            certify_bracket(n_P, p_val_P, P)
        except CertificationError as e:
            raise SystemExit(f"ICDF_Q24[{u}]: evalA bracket certification failed: {e} -- T0 FAIL")

        values[u] = n_P
        x_prev_P = x_P
        x_prev_2P = x_2P

        if (u + 1) % progress_every == 0:
            elapsed = time.time() - t0
            print(f"  progress u={u + 1}/{N} elapsed={elapsed:.1f}s")

    out = b"".join(int64_le(v) for v in values)
    assert len(out) == N * 8
    with open(OUT, "wb") as f:
        f.write(out)
    digest = sha256_bytes(out)
    elapsed = time.time() - t0
    report = {
        "table_id": "ICDF_Q24",
        "entry_count": N,
        "bytes": len(out),
        "sha256": digest,
        "evaluator_disagreements": disagreements,
        "monotonic_nondecreasing": all(values[i] <= values[i + 1] for i in range(N - 1)),
        "elapsed_sec": round(elapsed, 2),
    }
    print(report)
    with open(LOG, "w") as f:
        f.write(str(report) + "\n")


if __name__ == "__main__":
    main()
