from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import shutil
import os
import whisper
from soap_generator import generate_soap_note
from icd10_lookup import get_suggestions_for_assessment_list
app = FastAPI()

print("Loading Whisper model... please wait")
model = whisper.load_model("base")
print("Whisper model loaded!")

MEDICAL_HINT = (
    "Patient presents with fever, headache, chest pain, dyspnea. "
    "Doctor prescribes paracetamol, ibuprofen, metformin, amoxicillin. "
    "Diagnosis: hypertension, diabetes, pneumonia, tachycardia."
)


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": True}


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1] or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        result = model.transcribe(temp_path, initial_prompt=MEDICAL_HINT)

        labeled_segments = []
        current_speaker = "Doctor"
        prev_end = 0.0
        GAP_THRESHOLD = 1.5

        for seg in result["segments"]:
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()

            if start - prev_end > GAP_THRESHOLD and labeled_segments:
                current_speaker = "Patient" if current_speaker == "Doctor" else "Doctor"

            labeled_segments.append({
                "speaker": current_speaker,
                "start": round(start, 2),
                "end": round(end, 2),
                "text": text
            })

            prev_end = end

        os.unlink(temp_path)

        return {
            "status": "success",
            "filename": file.filename,
            "full_transcript": result["text"],
            "labeled_segments": labeled_segments
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/soap-note")
async def create_soap_note(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1] or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        print("Transcribing audio...")
        result = model.transcribe(temp_path, initial_prompt=MEDICAL_HINT)

        os.unlink(temp_path)

        labeled_segments = []
        current_speaker = "Doctor"
        prev_end = 0.0
        GAP_THRESHOLD = 1.5

        for seg in result["segments"]:
            start = seg["start"]
            text = seg["text"].strip()
            if start - prev_end > GAP_THRESHOLD and labeled_segments:
                current_speaker = "Patient" if current_speaker == "Doctor" else "Doctor"
            labeled_segments.append(f"{current_speaker}: {text}")
            prev_end = seg["end"]

        readable_transcript = "\n".join(labeled_segments)

        print("Generating SOAP note...")
        soap_note = generate_soap_note(readable_transcript)

        print("Looking up ICD-10 codes...")
        icd10_suggestions = get_suggestions_for_assessment_list(soap_note.assessment)

        return {
            "status": "success",
            "filename": file.filename,
            "transcript": readable_transcript,
            "soap_note": soap_note.model_dump(),
            "icd10_suggestions": icd10_suggestions
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=str(e))