from icd10_lookup import get_icd10_suggestions

# -------------------------------------------
# Test cases: (diagnosis_text, expected_code)
# These are the "right answers" a real medical
# coder would assign for each diagnosis phrase
# -------------------------------------------
TEST_CASES = [
    ("fever and high temperature", "R50.9"),
    ("patient has headache", "R51.9"),
    ("shortness of breath and difficulty breathing", "R06.02"),
    ("chest pain", "R07.9"),
    ("nausea and vomiting", "R11.0"),
    ("high blood pressure hypertension", "I10"),
    ("type 2 diabetes mellitus", "E11.9"),
    ("common cold runny nose", "J00"),
    ("pneumonia lung infection", "J18.9"),
    ("urinary tract infection", "N39.0"),
    ("fatigue and tiredness", "R53.83"),
    ("acute bronchitis cough", "J20.9"),
    ("low back pain", "M54.5"),
    ("anxiety disorder", "F41.9"),
    ("depression", "F32.9"),
]

print("Running ICD-10 precision evaluation...\n")

top1_hits = 0  # correct code was the #1 result
top3_hits = 0  # correct code was in top 3
top5_hits = 0  # correct code was in top 5
total = len(TEST_CASES)

results_log = []

for diagnosis, expected_code in TEST_CASES:
    suggestions = get_icd10_suggestions(diagnosis, top_n=5)
    suggested_codes = [s["code"] for s in suggestions]

    in_top1 = len(suggested_codes) > 0 and suggested_codes[0] == expected_code
    in_top3 = expected_code in suggested_codes[:3]
    in_top5 = expected_code in suggested_codes[:5]

    if in_top1:
        top1_hits += 1
    if in_top3:
        top3_hits += 1
    if in_top5:
        top5_hits += 1

    status = "✓" if in_top5 else "✗"
    rank = suggested_codes.index(expected_code) + 1 if in_top5 else "not found"

    results_log.append({
        "diagnosis": diagnosis,
        "expected": expected_code,
        "got": suggested_codes,
        "rank": rank,
        "status": status
    })

    print(f"{status} '{diagnosis}'")
    print(f"   Expected: {expected_code}")
    print(f"   Got:      {', '.join(suggested_codes[:3])}{'...' if len(suggested_codes) > 3 else ''}")
    print(f"   Rank:     {rank}\n")

# -------------------------------------------
# Summary
# -------------------------------------------
top1_pct = round((top1_hits / total) * 100, 1)
top3_pct = round((top3_hits / total) * 100, 1)
top5_pct = round((top5_hits / total) * 100, 1)

print("=" * 50)
print("ICD-10 CODE PRECISION RESULTS")
print("=" * 50)
print(f"Top-1 precision:  {top1_hits}/{total} ({top1_pct}%)")
print(f"Top-3 precision:  {top3_hits}/{total} ({top3_pct}%)")
print(f"Top-5 precision:  {top5_hits}/{total} ({top5_pct}%)")
print("=" * 50)

if top5_pct >= 70:
    print("RESULT: KPI MET — good enough for medical coder review")
elif top5_pct >= 50:
    print("RESULT: MARGINAL — acceptable for a learning project")
else:
    print("RESULT: NEEDS IMPROVEMENT — consider expanding the ICD-10 dataset")

# Save results to file
with open("benchmarks/icd10_precision.txt", "w", encoding="utf-8") as f:
    f.write("ICD-10 CODE PRECISION EVALUATION\n")
    f.write("=" * 50 + "\n")
    f.write(f"Top-1 precision: {top1_hits}/{total} ({top1_pct}%)\n")
    f.write(f"Top-3 precision: {top3_hits}/{total} ({top3_pct}%)\n")
    f.write(f"Top-5 precision: {top5_hits}/{total} ({top5_pct}%)\n\n")
    for r in results_log:
        f.write(f"{r['status']} {r['diagnosis']}\n")
        f.write(f"   Expected: {r['expected']}, Rank: {r['rank']}\n")
        f.write(f"   Got: {', '.join(r['got'])}\n\n")

print("\nResults saved to benchmarks/icd10_precision.txt")