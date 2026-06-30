from models import SOAPNote, VitalSigns

# This is the "correct answer" — what a human doctor would write
# for the same test_audio.wav conversation. Edit this to match
# what's actually said in your test audio file.

GOLD_STANDARD_SOAP = SOAPNote(
    subjective="Patient reports headache and mild fever since yesterday, with mild nausea, no vomiting.",
    objective=VitalSigns(
        temperature_f=100.8,
        blood_pressure="122/78",
        heart_rate_bpm=88,
        respiratory_rate=None
    ),
    objective_notes=None,
    assessment=["Mild viral infection"],
    plan=[
        "Paracetamol 500mg twice daily",
        "Drink plenty of fluids",
        "Rest",
        "Follow up if no improvement in 3 days"
    ]
)