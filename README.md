\# Ambient Clinical Scribe



An AI-powered tool that transcribes doctor-patient conversations

and labels who said what.



\## What it does

\- Accepts an audio file of a medical consultation

\- Transcribes it using OpenAI Whisper

\- Labels each segment as Doctor or Patient

\- Returns structured JSON output



\## Week 1 results

\- WER without medical hint: \[fill in your number]%

\- WER with medical hint: \[fill in your number]%



\## How to run

1\. Clone the repo

2\. Create .env with OPENAI\_API\_KEY=your-key

3\. pip install -r requirements.txt

4\. uvicorn main:app --reload

5\. Visit http://localhost:8000/docs



\## Tech stack

\- FastAPI

\- OpenAI Whisper API

\- Python





\## Week 2 results

\- SOAP note generation: working via local Ollama (llama3.2)

\- Clinical accuracy on test transcript: \[fill in your %]

\- Vitals extraction: \[fill in X/X matched]





\## Week 3 results

\- ICD-10 vector database: 56 codes (common primary care codes)

\- Top-1 precision: \[fill in]%

\- Top-3 precision: \[fill in]%

\- Top-5 precision: \[fill in]%

\- Endpoints: /icd10-search (standalone), /soap-note (auto-suggests codes)

