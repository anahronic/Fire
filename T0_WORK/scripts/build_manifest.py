"""
Build dsp_tables_manifest.json per companion section 14 / Prompt.md section 15-16.
Closed schema, JCS bytes, tables[] in ascending table_id order, plus the
normative tables_manifest_sha256 = SHA256(LP("D0BENCH-DSP-TABLES-MANIFEST-V1") || LP(JCS(...))).
"""
import sys, os
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts")
from common import sha256_bytes, canonical_json_bytes, LP

OUT = "E:/000_Audiotext/T0_OUTPUT"

# table_id -> (dimensions, q_format)
TABLES = {
    "H_1000_999":   ([1000, 25], 30),
    "H_147_160":    ([147, 27], 30),
    "H_160_147":    ([160, 25], 30),
    "H_999_1000":   ([999, 25], 30),
    "H_DRIFT_Q30":  ([1024, 25], 30),
    "ICDF_Q24":     ([65536], 24),
    "PINK_V1":      ([3, 5], 30),
    "SIN48000_Q30": ([48000], 30),
    "TP_FIR_Q30":   ([4, 12], 30),
}

EXPECTED_ENTRY_COUNT = {
    "H_1000_999": 25000, "H_147_160": 3969, "H_160_147": 4000,
    "H_999_1000": 24975, "H_DRIFT_Q30": 25600, "ICDF_Q24": 65536,
    "PINK_V1": 15, "SIN48000_Q30": 48000, "TP_FIR_Q30": 48,
}
EXPECTED_BYTES = {k: v * 8 for k, v in EXPECTED_ENTRY_COUNT.items()}


def prod(seq):
    r = 1
    for x in seq:
        r *= x
    return r


def main():
    ordered_ids = sorted(TABLES.keys())  # ASCII byte order == required order
    assert ordered_ids == [
        "H_1000_999", "H_147_160", "H_160_147", "H_999_1000", "H_DRIFT_Q30",
        "ICDF_Q24", "PINK_V1", "SIN48000_Q30", "TP_FIR_Q30",
    ], ordered_ids

    tables_entries = []
    total_bytes = 0
    for table_id in ordered_ids:
        dims, q = TABLES[table_id]
        filename = f"{table_id}.bin"
        path = os.path.join(OUT, filename)
        with open(path, "rb") as f:
            data = f.read()
        entry_count = prod(dims)
        assert entry_count == EXPECTED_ENTRY_COUNT[table_id], (table_id, entry_count)
        assert len(data) == entry_count * 8 == EXPECTED_BYTES[table_id], (table_id, len(data))
        digest = sha256_bytes(data)
        tables_entries.append({
            "table_id": table_id,
            "filename": filename,
            "element_type": "int64_le_twos_complement",
            "dimensions": dims,
            "q_format": q,
            "entry_count": entry_count,
            "sha256": digest,
        })
        total_bytes += len(data)

    assert sum(e["entry_count"] * 8 for e in tables_entries) == 1577144, \
        sum(e["entry_count"] * 8 for e in tables_entries)
    assert total_bytes == 1577144

    manifest = {"schema_version": 1, "tables": tables_entries}
    manifest_bytes = canonical_json_bytes(manifest)

    manifest_path = os.path.join(OUT, "dsp_tables_manifest.json")
    with open(manifest_path, "wb") as f:
        f.write(manifest_bytes)

    ordinary_sha256 = sha256_bytes(manifest_bytes)
    tables_manifest_sha256 = sha256_bytes(
        LP(b"D0BENCH-DSP-TABLES-MANIFEST-V1") + LP(manifest_bytes)
    )

    report = {
        "manifest_bytes_len": len(manifest_bytes),
        "manifest_ordinary_sha256": ordinary_sha256,
        "tables_manifest_sha256": tables_manifest_sha256,
        "sum_entry_count_x8": sum(e["entry_count"] * 8 for e in tables_entries),
        "table_ids_order": [e["table_id"] for e in tables_entries],
    }
    print(report)
    for e in tables_entries:
        print(" ", e["table_id"], e["dimensions"], e["entry_count"], e["sha256"])
    with open("E:/000_Audiotext/T0_WORK/logs/manifest_log.txt", "w") as f:
        f.write(str(report) + "\n")
        for e in tables_entries:
            f.write(f"{e}\n")


if __name__ == "__main__":
    main()
