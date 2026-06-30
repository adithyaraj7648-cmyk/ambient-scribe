SOAP_SYSTEM_PROMPT = """You are a medical scribe AI. Your job is to read a 
doctor-patient conversation transcript and convert it into a structured SOAP note.

SOAP stands for:
- Subjective: What the patient reports in their own words (symptoms, complaints)
- Objective: Measurable findings (vital signs, exam observations)
- Assessment: The doctor's diagnosis or clinical impression
- Plan: Next steps (medications, tests, follow-up instructions)

You must respond with ONLY valid JSON matching this exact structure, and nothing else:

{
  "subjective": "string describing patient's reported symptoms",
  "objective": {
    "temperature_f": number or null,
    "blood_pressure": "string like 120/80" or null,
    "heart_rate_bpm": number or null,
    "respiratory_rate": number or null
  },
  "objective_notes": "string with other exam findings" or null,
  "assessment": ["list", "of", "diagnoses"],
  "plan": ["list", "of", "next steps"]
}

Rules:
- Only include information that was actually mentioned in the transcript
- If a vital sign was not mentioned, use null for that field
- Do not invent or assume medical information not present in the transcript
- assessment and plan must always be lists, even if only one item
- Respond with ONLY the JSON object — no explanation, no markdown, no extra text
"""


# -------------------------------------------
# Few-shot examples — these teach the AI the pattern
# -------------------------------------------
FEW_SHOT_EXAMPLES = """
EXAMPLE 1:

Transcript:
Doctor: Good morning, how are you feeling today?
Patient: I have had a fever and headache for the past two days, and I feel very tired.
Doctor: Any cough or sore throat?
Patient: No cough, but my throat feels a little scratchy.
Doctor: Let me check your vitals. Your temperature is 101.4 and blood pressure is 118 over 76. Heart rate is 90.
Doctor: This looks like a viral infection. I'll prescribe paracetamol 500mg three times a day and recommend rest and fluids. Come back if symptoms worsen after 3 days.

Output:
{
  "subjective": "Patient reports fever and headache for the past two days, along with fatigue and a scratchy throat. No cough reported.",
  "objective": {
    "temperature_f": 101.4,
    "blood_pressure": "118/76",
    "heart_rate_bpm": 90,
    "respiratory_rate": null
  },
  "objective_notes": null,
  "assessment": ["Viral infection"],
  "plan": [
    "Prescribe paracetamol 500mg three times daily",
    "Recommend rest and fluids",
    "Follow up if symptoms worsen after 3 days"
  ]
}

EXAMPLE 2:

Transcript:
Doctor: What brings you in today?
Patient: I've had chest pain and shortness of breath since yesterday evening.
Doctor: Does the pain get worse with activity?
Patient: Yes, especially when I climb stairs.
Doctor: Your blood pressure is 145 over 92, heart rate 102, respiratory rate 22.
Doctor: I'm concerned this could be cardiac related. I'm ordering an ECG and chest X-ray immediately, and referring you to cardiology today.

Output:
{
  "subjective": "Patient reports chest pain and shortness of breath since yesterday evening, worsened by exertion such as climbing stairs.",
  "objective": {
    "temperature_f": null,
    "blood_pressure": "145/92",
    "heart_rate_bpm": 102,
    "respiratory_rate": 22
  },
  "objective_notes": null,
  "assessment": ["Possible cardiac event, rule out acute coronary syndrome"],
  "plan": [
    "Order ECG",
    "Order chest X-ray",
    "Urgent referral to cardiology"
  ]
}
"""


def build_full_prompt(transcript_text: str) -> str:
    """Combines system instructions + examples + the real transcript to analyze."""
    return f"""{SOAP_SYSTEM_PROMPT}

{FEW_SHOT_EXAMPLES}

NOW CONVERT THIS TRANSCRIPT:

Transcript:
{transcript_text}

Output:"""