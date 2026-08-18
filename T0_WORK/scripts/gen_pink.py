"""
PINK_V1[3][5] -- EXACT_INTEGER, companion section 11.
Per-section field order: b0, b1, b2, a1, a2. b2 = a2 = 0, present explicitly.
Values copied verbatim from companion; not designed, not recomputed.
"""
import sys
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts")
from common import int64_le, sha256_bytes

SECTIONS = [
    # b0, b1, b2, a1, a2
    (2631693208, -2597467940, 0, -1069306727, 0),
    (353978446, -310430765, 0, -1030194144, 0),
    (429140238, -56497384, 0, -701098970, 0),
]

def main():
    assert len(SECTIONS) == 3
    for s in SECTIONS:
        assert len(s) == 5
        assert s[2] == 0 and s[4] == 0
    out = b"".join(int64_le(v) for section in SECTIONS for v in section)
    assert len(out) == 15 * 8 == 120
    with open("E:/000_Audiotext/T0_OUTPUT/PINK_V1.bin", "wb") as f:
        f.write(out)
    digest = sha256_bytes(out)
    report = {
        "table_id": "PINK_V1",
        "entry_count": 15,
        "explicit_zero_count": 6,
        "bytes": len(out),
        "sha256": digest,
    }
    print(report)
    with open("E:/000_Audiotext/T0_WORK/logs/pink_log.txt", "w") as f:
        f.write(str(report) + "\n")

if __name__ == "__main__":
    main()
