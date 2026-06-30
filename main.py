from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
import os
import openai
import tempfile
import shutil

load_dotenv()

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "api_key_loaded": os.getenv("OPENAI_API_KEY") is not None
    }

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    suffix = os.path.splitext(file.filename)[-1] or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:
        print(f"Transcribing {file.filename}...")
        with open(temp_path, "rb") as audio_file:
            medical_hint = (
                "Patient presents with fever, headache, chest pain, dyspnea. "
                "Doctor prescribes paracetamol, ibuprofen, metformin, amoxicillin. "
                "Diagnosis: hypertension, diabetes, pneumonia, tachycardia."
              )
              transcript = openai.audio.transcriptions.create(
                  model="whisper-1",
                  file=audio_file,
                  response_format="verbose_json",
                  prompt=medical_hint
             )
        print("Transcription done!")

        labeled_segments = []
        current_speaker = "Doctor"
        prev_end = 0.0
        GAP_THRESHOLD = 1.5

        if hasattr(transcript, "segments") and transcript.segments:
            for seg in transcript.segments:
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
            "full_transcript": transcript.text,
            "labeled_segments": labeled_segments
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=str(e))