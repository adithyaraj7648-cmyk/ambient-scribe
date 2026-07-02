\# Ambient Clinical Scribe



An AI-powered ambient medical documentation assistant that transcribes

doctor-patient conversations and automatically generates structured

SOAP notes with ICD-10 billing code suggestions.



\## Project overview



Built as a 4-week internship project demonstrating end-to-end AI

integration in a clinical workflow, with strict Human-in-the-Loop

validation before any note is finalized.



\## Features



\- Audio transcription with speaker labeling (Doctor / Patient)

\- Structured SOAP note generation (Subjective, Objective, Assessment, Plan)

\- ICD-10 billing code suggestions with confidence scores

\- Physician review dashboard with editable fields

\- Human-in-the-Loop approval before export

\- Downloadable finalized note (.txt)



\## Tech stack



| Component | Technology |

|---|---|

| Backend API | FastAPI + Python |

| Speech-to-text | OpenAI Whisper (local, free) |

| SOAP generation | Ollama + llama3.2 (local, free) |

| Data validation | Pydantic |

| ICD-10 search | ChromaDB + sentence-transformers (RAG) |

| Dashboard UI | Streamlit |



\## Week-by-week results



\### Week 1 — Audio transcription

\- Whisper base model running locally (free, no API cost)

\- Speaker diarization via gap-detection algorithm

\- WER benchmarking with medical vocabulary hint



\### Week 2 — SOAP note generation

\- Few-shot prompting with 2 clinical examples

\- Pydantic schema enforces valid structured output

\- Full pipeline: audio to SOAP note in one API call



\### Week 3 — ICD-10 RAG pipeline

\- 56-code curated ICD-10 vector database (ChromaDB)

\- Semantic search using all-MiniLM-L6-v2 embeddings

\- Top-1 precision: 93.3% | Top-5 precision: 100.0%



\### Week 4 — Physician dashboard

\- Streamlit UI with transcript viewer and SOAP editor

\- Editable fields for all SOAP sections

\- ICD-10 suggestions with confidence traffic lights

\- HITL approve + download workflow



\## How to run



\### Prerequisites

\- Python 3.10+

\- Ollama installed (ollama.com) with llama3.2 pulled

\- FFmpeg installed (gyan.dev/ffmpeg/builds)



\### Setup



```bash

git clone https://github.com/adithyaraj7648-cmyk/ambient-scribe

cd ambient-scribe

python -m venv venv

venv\\Scripts\\activate        # Windows

pip install -r requirements.txt

```



Create a `.env` file:

