"""
Generate H_147_160, H_160_147, H_999_1000, H_1000_999, H_DRIFT_Q30.
Companion section 9. GENERATED_REAL, dual independent evaluator required.
"""
import sys, time, json
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts_rebuild2")
from common import int64_le, sha256_bytes, mp, iv
from resampler_common import (build_prototype_interval, build_prototype_plain,
                               quantize_direction, CertificationError)

OUT = "E:/000_Audiotext/T0_OUTPUT_BUILD2"
LOG = "E:/000_Audiotext/T0_WORK/logs_rebuild2"


def ceil_div(a, b):
    return -(-a // b)


def reshape_polyphase(h_flat, N_h, L):
    P = L
    K = ceil_div(N_h, P)
    H = [[0] * K for _ in range(P)]
    for p in range(P):
        for i in range(K):
            idx = p + i * L
            if idx < N_h:
                H[p][i] = h_flat[idx]
    return H, P, K


def serialize(H, P, K):
    return b"".join(int64_le(H[p][i]) for p in range(P) for i in range(K))


def build_pair(max_LM, dirs, prototype_label, P_prec=60):
    """dirs: list of (table_id, L_direction) both sharing the same prototype."""
    t0 = time.time()
    N_h_iv, c_iv, terms_iv, S_iv = build_prototype_interval(max_LM, dps=P_prec)
    N_h_p, c_p, terms_p, S_p = build_prototype_plain(max_LM, dps=P_prec)
    N_h_2p, c_2p, terms_2p, S_2p = build_prototype_plain(max_LM, dps=2 * P_prec)
    assert N_h_iv == N_h_p == N_h_2p
    assert c_iv == c_p == c_2p
    N_h, c = N_h_iv, c_iv
    build_time = time.time() - t0

    results = {}
    for table_id, L in dirs:
        t1 = time.time()
        flat, disagreements = quantize_direction(
            N_h, terms_iv, S_iv, terms_p, S_p, terms_2p, S_2p,
            L_direction=L, label=table_id, dps_iv=P_prec, P=P_prec)
        if disagreements:
            raise SystemExit(f"{table_id}: {disagreements} evaluator disagreements -- T0 FAIL")
        H, P, K = reshape_polyphase(flat, N_h, L)
        data = serialize(H, P, K)
        with open(f"{OUT}/{table_id}.bin", "wb") as f:
            f.write(data)
        digest = sha256_bytes(data)
        report = {
            "table_id": table_id,
            "prototype": prototype_label,
            "N_h": N_h, "c": c,
            "dimensions": [P, K],
            "entry_count": P * K,
            "bytes": len(data),
            "sha256": digest,
            "evaluator_disagreements": disagreements,
            "prototype_build_time_sec": round(build_time, 2),
            "direction_time_sec": round(time.time() - t1, 2),
        }
        print(report)
        results[table_id] = report
    return results


def main():
    all_reports = {}
    all_reports.update(build_pair(160, [("H_147_160", 147), ("H_160_147", 160)], "48000<->44100 (max_LM=160)"))
    all_reports.update(build_pair(1000, [("H_999_1000", 999), ("H_1000_999", 1000)], "48000<->47952 (max_LM=1000)"))
    all_reports.update(build_pair(1024, [("H_DRIFT_Q30", 1024)], "drift (max_LM=1024)"))

    with open(f"{LOG}/resampler_log.json", "w") as f:
        json.dump(all_reports, f, indent=2)
    print("ALL RESAMPLER TABLES DONE")


if __name__ == "__main__":
    main()
