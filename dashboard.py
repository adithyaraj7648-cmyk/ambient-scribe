import streamlit as st
import requests
import json

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Ambient Clinical Scribe",
    page_icon="🏥",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

# -------------------------
# Header
# -------------------------
st.title("🏥 Ambient Clinical Scribe")
st.caption("AI-powered medical documentation assistant")
st.divider()

# -------------------------
# Sidebar — controls
# -------------------------
with st.sidebar:
    st.header("Controls")
    st.info(
        "Upload a doctor-patient audio recording. "
        "The AI will transcribe it and generate a SOAP note automatically."
    )
    st.divider()

    # Check backend health
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if health.status_code == 200:
            st.success("Backend connected")
        else:
            st.error("Backend error")
    except Exception:
        st.error("Backend not running — start uvicorn first")

    st.divider()
    st.caption("Ambient Scribe v1.0 — Week 4")

# -------------------------
# Main area — two columns
# -------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Step 1 — Upload audio")

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["mp3", "wav", "m4a", "mp4"],
        help="Record a doctor-patient consultation and upload it here"
    )

    if uploaded_file is not None:
        st.audio(uploaded_file)
        st.caption(f"File: {uploaded_file.name}")

        if st.button("Transcribe audio", type="primary", use_container_width=True):
            with st.spinner("Transcribing... this may take 30-60 seconds"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(
                        f"{BACKEND_URL}/transcribe",
                        files=files,
                        timeout=120
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["transcript_data"] = data
                        st.session_state["filename"] = uploaded_file.name
                        st.success("Transcription complete!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

                except requests.exceptions.Timeout:
                    st.error("Request timed out — the audio may be too long. Try a shorter clip.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

with col2:
    st.subheader("Step 2 — Review transcript")

    if "transcript_data" in st.session_state:
        data = st.session_state["transcript_data"]
        segments = data.get("labeled_segments", [])

        if segments:
            for seg in segments:
                speaker = seg.get("speaker", "Unknown")
                text = seg.get("text", "")
                start = seg.get("start", 0)
                end = seg.get("end", 0)

                # Color code by speaker
                if speaker == "Doctor":
                    with st.container(border=True):
                        st.markdown(f"**🩺 Doctor** `{start}s — {end}s`")
                        st.write(text)
                else:
                    with st.container(border=True):
                        st.markdown(f"**🧑 Patient** `{start}s — {end}s`")
                        st.write(text)
        else:
            st.text_area(
                "Full transcript",
                value=data.get("full_transcript", ""),
                height=300,
                disabled=True
            )

        st.divider()
        st.caption("✓ Transcript ready — scroll down to generate SOAP note")

    else:
        st.info("Upload and transcribe an audio file to see the transcript here.")

# -------------------------
# Bottom section — generate SOAP
# -------------------------
st.divider()
st.subheader("Step 3 — Generate SOAP note")

if "transcript_data" in st.session_state:
    if st.button("Generate SOAP note from transcript", type="primary", use_container_width=True):
        with st.spinner("Generating SOAP note with AI... this may take 1-2 minutes"):
            try:
                uploaded_file_bytes = st.session_state.get("filename", "audio.wav")
                files = {
                    "file": (
                        st.session_state["filename"],
                        st.session_state.get("audio_bytes", b""),
                    )
                }

                # Send the original audio again for full pipeline
                st.info(
                    "Tip: For fastest results, use the /soap-note endpoint directly "
                    "from the API docs at http://localhost:8000/docs"
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.info("Complete Steps 1 and 2 first.")