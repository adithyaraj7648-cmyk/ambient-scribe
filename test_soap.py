import ollama
import json
from prompts import build_full_prompt
from models import SOAPNote

# A sample transcript to test with
sample_transcript = """
Doctor: Good morning, how are you feeling today?
Patient: I have had a headache and mild fever since yesterday.
Doctor: Any nausea or vomiting?
Patient: A little nausea, no vomiting.
Doctor: Your temperature is 100.8, blood pressure 122 over 78, heart rate 88.
Doctor: This seems like a mild viral infection. Take paracetamol 500mg twice daily, 
drink plenty of fluids, and rest. Come back if it doesn't improve in 3 days.
"""

print("Sending transcript to Ollama...")
prompt = build_full_prompt(sample_transcript)

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": prompt}]
)

raw_output = response["message"]["content"]
print("\n--- RAW AI OUTPUT ---")
print(raw_output)

# Try to parse it into our strict schema
print("\n--- VALIDATING WITH PYDANTIC ---")
try:
    # Sometimes models wrap JSON in markdown code blocks, strip that
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    parsed_json = json.loads(cleaned)
    soap_note = SOAPNote(**parsed_json)
    print("SUCCESS! Valid SOAP note created:\n")
    print(soap_note.model_dump_json(indent=2))

except Exception as e:
    print(f"FAILED to parse: {e}")