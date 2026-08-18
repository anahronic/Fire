"""
TP_FIR_Q30[4][12] -- IMPORTED_EXACT, companion section 5.
Source: TP_FIR_SOURCE_DECIMAL.txt, exact decimal literals, phase-major order.
Conversion: exact Fraction, multiply by 2^30, must be integer (no halfway case
on this data per companion), round half to even applied nominally.
"""
import sys, re
from fractions import Fraction
sys.path.insert(0, "E:/000_Audiotext/T0_WORK/scripts_rebuild2")
from common import int64_le, sha256_bytes

SRC_PATH = "E:/000_Audiotext/TP_FIR_SOURCE_DECIMAL.txt"
EXPECTED_SHA_SRC = "0935e97d0b2efd5fdb77826430e9dc161833b9c916585547d0d910b3cda37424"
EXPECTED_SIZE_SRC = 789
EXPECTED_SHA_BIN = "4fd922e97c8a656f20bb5e069f6c00917a4bd845cd7e71c71aed066fd5625270"

LITERAL_RE = re.compile(r"^-?0\.\d{13}$")


def check_source_bytes(raw: bytes):
    assert len(raw) == EXPECTED_SIZE_SRC, f"size {len(raw)} != {EXPECTED_SIZE_SRC}"
    digest = sha256_bytes(raw)
    assert digest == EXPECTED_SHA_SRC, f"source sha256 mismatch: {digest}"
    assert b"\x00" not in raw[:3] and not raw.startswith(b"\xef\xbb\xbf"), "BOM present"
    assert b"\r" not in raw, "CR byte present"
    assert not raw.endswith(b"\n"), "trailing LF present"  # normative: no trailing LF
    lf_count = raw.count(b"\n")
    assert lf_count == 47, f"LF count {lf_count} != 47"
    text = raw.decode("ascii")
    lines = text.split("\n")
    assert len(lines) == 48, f"logical lines {len(lines)} != 48"
    for i, line in enumerate(lines):
        assert line == line.strip(), f"line {i} has leading/trailing whitespace"
        assert line != "", f"line {i} empty"
        assert LITERAL_RE.match(line), f"line {i} bad literal format: {line!r}"
        assert "+" not in line, f"line {i} contains +"
        assert "e" not in line.lower(), f"line {i} exponent notation"
    return lines


def main():
    with open(SRC_PATH, "rb") as f:
        raw = f.read()
    lines = check_source_bytes(raw)

    literals = [Fraction(x) for x in lines]
    assert len(literals) == 48

    Q30 = []
    scale = 1 << 30
    for idx, frac in enumerate(literals):
        scaled = frac * scale
        num, den = scaled.numerator, scaled.denominator
        if den != 1:
            raise SystemExit(f"literal {idx} does not scale to an exact integer at Q30 "
                              f"(den={den}) -- halfway/non-exact case, T0 BLOCKED")
        Q30.append(num)

    # reshape phase-major: p = 0..3, i = 0..11
    TP = [Q30[p * 12:(p + 1) * 12] for p in range(4)]

    EXPECTED = [
        [1835008, 11796480, -21102592, 35651584, -63832064,
         147456000, 1043857408, -109838336, 51118080,
         -28573696, 15990784, -8912896],
        [-31326208, 31457280, -55574528, 95682560, -178782208,
         499384320, 837287936, -215089152, 109051904,
         -62521344, 35520512, -20316160],
        [-20316160, 35520512, -62521344, 109051904, -215089152,
         837287936, 499384320, -178782208, 95682560,
         -55574528, 31457280, -31326208],
        [-8912896, 15990784, -28573696, 51118080, -109838336,
         1043857408, 147456000, -63832064, 35651584,
         -21102592, 11796480, 1835008],
    ]
    mismatches = 0
    for p in range(4):
        for i in range(12):
            if TP[p][i] != EXPECTED[p][i]:
                mismatches += 1
                print(f"MISMATCH p={p} i={i} computed={TP[p][i]} expected={EXPECTED[p][i]}")
    if mismatches:
        raise SystemExit(f"TP_FIR_Q30: {mismatches} mismatches vs companion verification block -- T0 FAIL")

    # structural invariants
    for i in range(12):
        assert TP[3][i] == TP[0][11 - i], f"symmetry 3/0 fail at i={i}"
        assert TP[2][i] == TP[1][11 - i], f"symmetry 2/1 fail at i={i}"
    sum0 = sum(abs(v) for v in TP[0])
    sum3 = sum(abs(v) for v in TP[3])
    sum1 = sum(abs(v) for v in TP[1])
    sum2 = sum(abs(v) for v in TP[2])
    assert sum0 == sum3 == 1539964928, (sum0, sum3)
    assert sum1 == sum2 == 2171994112, (sum1, sum2)

    out = b"".join(int64_le(v) for p in range(4) for v in TP[p])
    assert len(out) == 48 * 8 == 384
    with open("E:/000_Audiotext/T0_OUTPUT_BUILD2/TP_FIR_Q30.bin", "wb") as f:
        f.write(out)
    digest = sha256_bytes(out)
    if digest != EXPECTED_SHA_BIN:
        raise SystemExit(f"TP_FIR_Q30.bin sha256 mismatch: got {digest} expected {EXPECTED_SHA_BIN} -- T0 FAIL")

    # also copy source file byte-identical into T0_OUTPUT
    with open("E:/000_Audiotext/T0_OUTPUT_BUILD2/TP_FIR_SOURCE_DECIMAL.txt", "wb") as f:
        f.write(raw)

    report = {
        "table_id": "TP_FIR_Q30",
        "entry_count": 48,
        "bytes": len(out),
        "sha256": digest,
        "mismatches_vs_companion_block": mismatches,
        "structural_invariants": "PASS",
        "source_sha256": sha256_bytes(raw),
        "source_size": len(raw),
    }
    print(report)
    with open("E:/000_Audiotext/T0_WORK/logs_rebuild2/tp_fir_log.txt", "w") as f:
        f.write(str(report) + "\n")

if __name__ == "__main__":
    main()
