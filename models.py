from pydantic import BaseModel, Field
from typing import List, Optional


# -------------------------------------------
# Objective section sub-structure
# Vitals are numbers, so we give them their own shape
# -------------------------------------------
class VitalSigns(BaseModel):
    temperature_f: Optional[float] = Field(
        default=None,
        description="Body temperature in Fahrenheit, e.g. 101.5"
    )
    blood_pressure: Optional[str] = Field(
        default=None,
        description="Blood pressure as a string, e.g. '120/80'"
    )
    heart_rate_bpm: Optional[int] = Field(
        default=None,
        description="Heart rate in beats per minute, e.g. 88"
    )
    respiratory_rate: Optional[int] = Field(
        default=None,
        description="Breaths per minute, e.g. 16"
    )


# -------------------------------------------
# The full SOAP note structure
# This is the exact shape the AI must fill in
# -------------------------------------------
class SOAPNote(BaseModel):
    subjective: str = Field(
        description="What the patient reports in their own words — symptoms, "
                     "complaints, history of the current problem."
    )

    objective: VitalSigns = Field(
        description="Measurable findings — vital signs mentioned during the visit."
    )

    objective_notes: Optional[str] = Field(
        default=None,
        description="Any other physical exam findings mentioned, in free text."
    )

    assessment: List[str] = Field(
        description="The doctor's diagnosis or clinical impressions, as a list. "
                     "E.g. ['Acute viral pharyngitis', 'Mild dehydration']"
    )

    plan: List[str] = Field(
        description="Next steps — medications prescribed, tests ordered, "
                     "follow-up instructions. E.g. ['Prescribe paracetamol 500mg "
                     "twice daily', 'Order CBC blood test', 'Follow up in 1 week']"
    )


# -------------------------------------------
# Quick self-test — run this file directly to check it works
# -------------------------------------------
if __name__ == "__main__":
    example = SOAPNote(
        subjective="Patient reports headache and fever for 2 days.",
        objective=VitalSigns(
            temperature_f=101.2,
            blood_pressure="118/76",
            heart_rate_bpm=92,
            respiratory_rate=18
        ),
        objective_notes="No signs of respiratory distress.",
        assessment=["Viral fever", "Tension headache"],
        plan=[
            "Prescribe paracetamol 500mg every 6 hours",
            "Advise rest and hydration",
            "Follow up if fever persists beyond 3 days"
        ]
    )

    print("SOAP note created successfully!\n")
    print(example.model_dump_json(indent=2))