from jiwer import wer
import whisper

# ---- CONFIG ----
AUDIO_FILE = "test_audio.wav"
GROUND_TRUTH_FILE = "ground_truth.txt"
# ----------------

# Read ground truth
with open(GROUND_TRUTH_FILE, "r") as f:
    ground_truth = f.read().strip().lower()

# Load the local Whisper model (downloads once, then cached)
print("Loading Whisper model... (first time takes a minute)")
model = whisper.load_model("base")
print("Model loaded!")

# Transcribe without medical hint
print("Transcribing without medical hint...")
result_basic = model.transcribe(AUDIO_FILE)
basic_transcript = result_basic["text"].strip().lower()
basic_wer = wer(ground_truth, basic_transcript)

# Transcribe WITH medical hint
print("Transcribing WITH medical hint...")
medical_hint = (
    "Patient presents with fever, headache, chest pain, dyspnea. "
    "Doctor prescribes paracetamol, ibuprofen, metformin, amoxicillin. "
    "Diagnosis: hypertension, diabetes, pneumonia, tachycardia."
)
result_hinted = model.transcribe(AUDIO_FILE, initial_prompt=medical_hint)
hinted_transcript = result_hinted["text"].strip().lower()
hinted_wer = wer(ground_truth, hinted_transcript)

# Show results
print("\n========== BENCHMARK RESULTS ==========")
print(f"Ground truth:        {ground_truth}")
print(f"Basic transcript:    {basic_transcript}")
print(f"Hinted transcript:   {hinted_transcript}")
print(f"WER without hint:    {round(basic_wer * 100, 1)}%")
print(f"WER with hint:       {round(hinted_wer * 100, 1)}%")
print(f"Improvement:         {round((basic_wer - hinted_wer) * 100, 1)}%")
print("=======================================")

# Save results
with open("benchmarks/results.txt", "w") as f:
    f.write(f"Ground truth: {ground_truth}\n")
    f.write(f"Basic WER: {round(basic_wer * 100, 1)}%\n")
    f.write(f"Hinted WER: {round(hinted_wer * 100, 1)}%\n")
    f.write(f"Improvement: {round((basic_wer - hinted_wer) * 100, 1)}%\n")

print("Results saved to benchmarks/results.txt")