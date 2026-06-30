# A curated set of common ICD-10-CM codes for general/primary care consultations.
# Each entry is (code, description). This is a learning-project subset —
# the full official list has ~70,000 codes (cms.gov).

ICD10_CODES = [
    ("R50.9", "Fever, unspecified"),
    ("R51.9", "Headache, unspecified"),
    ("R05.9", "Cough, unspecified"),
    ("R06.02", "Shortness of breath"),
    ("R07.9", "Chest pain, unspecified"),
    ("R10.9", "Unspecified abdominal pain"),
    ("R11.0", "Nausea"),
    ("R11.10", "Vomiting, unspecified"),
    ("R42", "Dizziness and giddiness"),
    ("R53.83", "Fatigue"),
    ("R60.9", "Edema, unspecified"),
    ("R09.81", "Nasal congestion"),
    ("M54.5", "Low back pain"),
    ("M25.50", "Pain in unspecified joint"),
    ("M79.1", "Myalgia"),

    ("J00", "Acute nasopharyngitis (common cold)"),
    ("J02.9", "Acute pharyngitis, unspecified"),
    ("J03.90", "Acute tonsillitis, unspecified"),
    ("J06.9", "Acute upper respiratory infection, unspecified"),
    ("J18.9", "Pneumonia, unspecified organism"),
    ("J20.9", "Acute bronchitis, unspecified"),
    ("J45.909", "Unspecified asthma, uncomplicated"),
    ("J44.9", "Chronic obstructive pulmonary disease, unspecified"),

    ("I10", "Essential (primary) hypertension"),
    ("I20.9", "Angina pectoris, unspecified"),
    ("I25.10", "Atherosclerotic heart disease of native coronary artery"),
    ("I48.91", "Unspecified atrial fibrillation"),
    ("I50.9", "Heart failure, unspecified"),
    ("R00.0", "Tachycardia, unspecified"),

    ("E11.9", "Type 2 diabetes mellitus without complications"),
    ("E10.9", "Type 1 diabetes mellitus without complications"),
    ("E66.9", "Obesity, unspecified"),
    ("E03.9", "Hypothyroidism, unspecified"),
    ("E78.5", "Hyperlipidemia, unspecified"),
    ("E86.0", "Dehydration"),

    ("K21.9", "Gastro-esophageal reflux disease without esophagitis"),
    ("K29.70", "Gastritis, unspecified, without bleeding"),
    ("K59.00", "Constipation, unspecified"),
    ("K52.9", "Noninfective gastroenteritis and colitis, unspecified"),
    ("K30", "Functional dyspepsia"),

    ("N39.0", "Urinary tract infection, site not specified"),
    ("N18.9", "Chronic kidney disease, unspecified"),

    ("L30.9", "Dermatitis, unspecified"),
    ("L20.9", "Atopic dermatitis, unspecified"),
    ("L03.90", "Cellulitis, unspecified"),

    ("F32.9", "Major depressive disorder, single episode, unspecified"),
    ("F41.9", "Anxiety disorder, unspecified"),
    ("G47.00", "Insomnia, unspecified"),
    ("G43.909", "Migraine, unspecified, not intractable"),

    ("H66.90", "Otitis media, unspecified"),
    ("H10.9", "Unspecified conjunctivitis"),

    ("S93.401A", "Sprain of unspecified ligament of right ankle, initial encounter"),
    ("S61.419A", "Laceration of right hand, initial encounter"),
    ("T78.40XA", "Allergy, unspecified, initial encounter"),

    ("Z00.00", "Encounter for general adult medical examination without abnormal findings"),
    ("Z23", "Encounter for immunization"),
    ("Z71.3", "Dietary counseling and surveillance"),
]


def get_all_codes():
    """Returns the full list of (code, description) tuples."""
    return ICD10_CODES


if __name__ == "__main__":
    codes = get_all_codes()
    print(f"Loaded {len(codes)} ICD-10 codes")
    print("\nFirst 5 examples:")
    for code, desc in codes[:5]:
        print(f"  {code}: {desc}")