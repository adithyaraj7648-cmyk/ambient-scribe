import ollama
import json
from prompts import build_full_prompt
from models import SOAPNote
from pydantic import ValidationError


def clean_json_response(raw_text: str) -> str:
    """Strips markdown code fences and extra text that local LLMs sometimes add."""
    text = raw_text.strip()

    # Remove markdown code fences like ```json ... ```
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break

    # If there's extra text before/after the JSON object, extract just the {...}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text


def generate_soap_note(transcript_text: str, max_retries: int = 2) -> SOAPNote:
    """
    Sends a transcript to the local Ollama model and returns a validated SOAPNote.
    Retries once if the first attempt produces invalid JSON.
    """
    prompt = build_full_prompt(transcript_text)
    last_error = None

    for attempt in range(max_retries + 1):
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_output = response["message"]["content"]
        cleaned = clean_json_response(raw_output)

        try:
            parsed_json = json.loads(cleaned)
            soap_note = SOAPNote(**parsed_json)
            return soap_note  # success — return immediately

        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {e}")
            continue

    # If we get here, all retries failed
    raise ValueError(
        f"Failed to generate valid SOAP note after {max_retries + 1} attempts. "
        f"Last error: {last_error}"
    )