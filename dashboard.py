import streamlit as st
import requests

st.set_page_config(
    page_title="Ambient Clinical Scribe",
    page_icon="🏥",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"

st.title("🏥 Ambient Clinical Scribe")
st.caption("AI-powered medical documentation assistant — Human-in-the-Loop review")
st.divider()

with st.sidebar:
    st.header("Controls")
    st.info("Upload a doctor-patient audio recording. The AI will transcribe it, generate a SOAP note, and suggest ICD-10 billing codes.")
    st.divider()

    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if health.status_code == 200:
            st.success("✓ Backend connected")
        else:
            st.error("✗ Backend error")
    except Exception:
        st.error("✗ Backend not running — start uvicorn first")

    st.divider()
    st.subheader("Upload audio")
    uploaded_file = st.file_uploader(
        "Choose audio file",
        type=["mp3", "wav", "m4a", "mp4"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.audio(uploaded_file)
        st.caption(f"📎 {uploaded_file.name}")

        if st.button("▶ Transcribe + Generate SOAP", type="primary", use_container_width=True):
            st.session_state["audio_bytes"] = uploaded_file.getvalue()
            st.session_state["filename"] = uploaded_file.name
            st.session_state["soap_approved"] = False
            st.session_state["soap_data"] = None
            st.session_state["transcript_data"] = None
            st.session_state["icd10_data"] = {}

            with st.spinner("Running full pipeline... (1-3 minutes)"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(
                        f"{BACKEND_URL}/soap-note",
                        files=files,
                        timeout=300
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state["soap_data"] = result.get("soap_note", {})
                        st.session_state["transcript_data"] = result.get("transcript", "")
                        st.session_state["icd10_data"] = result.get("icd10_suggestions", {})
                        st.success("Done! Review the output →")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.Timeout:
                    st.error("Timed out — try a shorter audio clip")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    st.divider()
    st.caption("Ambient Scribe v1.0")

tab1, tab2, tab3 = st.tabs(["📝 Transcript", "🩺 SOAP Note Editor", "🏷️ ICD-10 Codes"])

with tab1:
    if "transcript_data" in st.session_state and st.session_state["transcript_data"]:
        st.subheader("Labeled transcript")
        st.caption("Automatically labeled by speaker using gap-detection diarization")
        lines = st.session_state["transcript_data"].strip().split("\n")
        for line in lines:
            if line.startswith("Doctor:"):
                with st.container(border=True):
                    st.markdown(f"🩺 **{line}**")
            elif line.startswith("Patient:"):
                with st.container(border=True):
                    st.markdown(f"🧑 {line}")
            elif line.strip():
                st.text(line)
    else:
        st.info("Upload and process an audio file to see the transcript here.")

with tab2:
    if "soap_data" in st.session_state and st.session_state["soap_data"]:
        soap = st.session_state["soap_data"]
        st.subheader("SOAP note — review and edit")
        st.caption("Review the AI-generated note below. Edit any field before approving.")

        st.markdown("#### S — Subjective")
        st.caption("What the patient reported")
        edited_subjective = st.text_area(
            "Subjective", value=soap.get("subjective", ""),
            height=100, label_visibility="collapsed", key="edit_subjective"
        )

        st.markdown("#### O — Objective")
        st.caption("Measurable findings and vital signs")
        objective = soap.get("objective", {})
        oc1, oc2, oc3, oc4 = st.columns(4)
        with oc1:
            edited_temp = st.text_input("Temperature (°F)", value=str(objective.get("temperature_f") or ""), key="edit_temp")
        with oc2:
            edited_bp = st.text_input("Blood pressure", value=str(objective.get("blood_pressure") or ""), key="edit_bp")
        with oc3:
            edited_hr = st.text_input("Heart rate (bpm)", value=str(objective.get("heart_rate_bpm") or ""), key="edit_hr")
        with oc4:
            edited_rr = st.text_input("Respiratory rate", value=str(objective.get("respiratory_rate") or ""), key="edit_rr")

        edited_obj_notes = st.text_area(
            "Other exam findings", value=soap.get("objective_notes", "") or "",
            height=80, key="edit_obj_notes"
        )

        st.markdown("#### A — Assessment")
        st.caption("Diagnoses — one per line")
        edited_assessment = st.text_area(
            "Assessment", value="\n".join(soap.get("assessment", [])),
            height=100, label_visibility="collapsed", key="edit_assessment"
        )

        st.markdown("#### P — Plan")
        st.caption("Next steps — one per line")
        edited_plan = st.text_area(
            "Plan", value="\n".join(soap.get("plan", [])),
            height=120, label_visibility="collapsed", key="edit_plan"
        )

        if st.button("💾 Save edits", use_container_width=True):
            st.session_state["soap_data"]["subjective"] = edited_subjective
            st.session_state["soap_data"]["objective_notes"] = edited_obj_notes
            st.session_state["soap_data"]