from soap_generator import generate_soap_note
from gold_standard import GOLD_STANDARD_SOAP

# The same transcript used to create your gold standard
TEST_TRANSCRIPT = """
Doctor: Good morning, how are you feeling today?
Patient: I have had a headache and mild fever since yesterday.
Doctor: Any nausea or vomiting?
Patient: A little nausea, no vomiting.
Doctor: Your temperature is 100.8, blood pressure 122 over 78, heart rate 88.
Doctor: This seems like a mild viral infection. Take paracetamol 500mg twice daily,
drink plenty of fluids, and rest. Come back if it doesn't improve in 3 days.
"""


def compare_vitals(ai_vitals, gold_vitals):
    """Compares each vital sign field and returns a match score."""
    fields = ["temperature_f", "blood_pressure", "heart_rate_bpm", "respiratory_rate"]
    matches = 0
    total = 0
    details = []

    for field in fields:
        ai_val = getattr(ai_vitals, field)
        gold_val = getattr(gold_vitals, field)

        if gold_val is None and ai_val is None:
            continue  # both agree it's missing, don't penalize

        total += 1
        if ai_val == gold_val:
            matches += 1
            details.append(f"  ✓ {field}: {ai_val} (matches)")
        else:
            details.append(f"  ✗ {field}: AI said {ai_val}, gold standard says {gold_val}")

    return matches, total, details


def keyword_overlap(ai_list, gold_list):
    """Simple check: how many gold-standard keywords appear in AI's output."""
    ai_text = " ".join(ai_list).lower()
    found = 0
    details = []

    for item in gold_list:
        # Check if key words from the gold item appear in AI's text
        keywords = [w for w in item.lower().split() if len(w) > 4]
        if any(kw in ai_text for kw in keywords):
            found += 1
            details.append(f"  ✓ Found reference to: '{item}'")
        else:
            details.append(f"  ✗ Missing: '{item}'")

    return found, len(gold_list), details


print("Generating AI SOAP note for evaluation...")
ai_soap = generate_soap_note(TEST_TRANSCRIPT)

print("\n" + "=" * 50)
print("CLINICAL ACCURACY EVALUATION")
print("=" * 50)

# Compare vitals
v_matches, v_total, v_details = compare_vitals(ai_soap.objective, GOLD_STANDARD_SOAP.objective)
print(f"\nOBJECTIVE (Vitals): {v_matches}/{v_total} matched")
for d in v_details:
    print(d)

# Compare assessment
a_matches, a_total, a_details = keyword_overlap(ai_soap.assessment, GOLD_STANDARD_SOAP.assessment)
print(f"\nASSESSMENT: {a_matches}/{a_total} diagnoses referenced")
for d in a_details:
    print(d)

# Compare plan
p_matches, p_total, p_details = keyword_overlap(ai_soap.plan, GOLD_STANDARD_SOAP.plan)
print(f"\nPLAN: {p_matches}/{p_total} action items referenced")
for d in p_details:
    print(d)

# Overall score
total_matches = v_matches + a_matches + p_matches
total_possible = v_total + a_total + p_total
overall_pct = round((total_matches / total_possible) * 100, 1) if total_possible else 0

print("\n" + "=" * 50)
print(f"OVERALL CLINICAL ACCURACY: {overall_pct}%")
print("=" * 50)

# Save results
with open("benchmarks/soap_evaluation.txt", "w") as f:
    f.write(f"Overall Clinical Accuracy: {overall_pct}%\n")
    f.write(f"Objective (vitals): {v_matches}/{v_total}\n")
    f.write(f"Assessment: {a_matches}/{a_total}\n")
    f.write(f"Plan: {p_matches}/{p_total}\n\n")
    f.write("AI Generated SOAP Note:\n")
    f.write(ai_soap.model_dump_json(indent=2))

print("\nResults saved to benchmarks/soap_evaluation.txt")