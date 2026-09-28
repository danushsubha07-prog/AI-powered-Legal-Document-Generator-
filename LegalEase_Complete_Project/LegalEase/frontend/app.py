from __future__ import annotations

import os

import requests
import streamlit as st

from utils.document_formatters import format_docx, format_pdf, format_txt
from utils.text_utils import safe_filename, text_to_html

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("FRONTEND_API_URL", "http://127.0.0.1:8000").rstrip("/")

st.markdown(
    """
    <style>
    .main-title { text-align:center; margin-bottom:0.1rem; }
    .subtitle { text-align:center; color:#8b93a7; margin-bottom:1.5rem; }
    .preview { background:#171922; color:#f4f4f5; border:1px solid #333746; border-radius:12px; padding:20px; max-height:620px; overflow-y:auto; line-height:1.65; }
    .notice { background:#fff7ed; border-left:4px solid #f97316; padding:12px; border-radius:8px; color:#4a2a0a; }
    </style>
    """,
    unsafe_allow_html=True,
)

if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=190)

st.markdown("<h1 class='main-title'>LegalEase</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Legal Document Generator</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Document settings")
    jurisdiction = st.text_input("Jurisdiction (optional)", placeholder="e.g. India")
    language = st.selectbox("Language", ["English", "Tamil", "Hindi", "Telugu"])
    st.caption("The language option is sent to the AI model; quality depends on model support.")
    st.divider()
    st.markdown("**Safety notice**")
    st.caption("AI output is a draft. Review it against the applicable law and facts before signing or relying on it.")

DOCUMENT_TYPES = [
    "Employment Contract",
    "Non-Disclosure Agreement (NDA)",
    "Lease Agreement",
    "Freelance Work Contract",
    "Service Agreement",
    "Employment Offer Letter",
    "General Agreement",
    "Custom",
]

with st.form("document_form"):
    selected_type = st.selectbox("Document Type", DOCUMENT_TYPES)
    custom_type = ""
    if selected_type == "Custom":
        custom_type = st.text_input("Custom document type", placeholder="e.g. Consultancy Agreement")
    document_type = custom_type.strip() if custom_type.strip() else selected_type

    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=100,
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        height=150,
        help="Separate each clause with a semicolon.",
    )
    dates = st.text_input("Effective Date", placeholder="September 27, 2026")

    submitted = st.form_submit_button("⚖️ Generate Document", use_container_width=True)

if submitted:
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please complete document type, parties, terms, and effective date.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
            "jurisdiction": jurisdiction,
            "language": language,
        }
        try:
            with st.spinner("Generating your document..."):
                response = requests.post(f"{API_URL}/generate", json=payload, timeout=130)
            if response.ok:
                result = response.json()
                st.session_state.generated_text = result["document"]
                st.session_state.generation_meta = result
                st.session_state.document_type = document_type
                st.session_state.parties = parties
                st.session_state.terms = terms
                st.success(f"Document generated successfully ({result.get('mode', 'AI')} mode).")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Backend error ({response.status_code}): {detail}")
        except requests.RequestException as exc:
            st.error(f"Cannot reach FastAPI at {API_URL}. Start the backend first. Details: {exc}")

if "generated_text" in st.session_state:
    st.divider()
    st.subheader("Document Generated")

    meta = st.session_state.get("generation_meta", {})
    if meta:
        st.caption(f"Generation mode: {meta.get('mode')} • Model: {meta.get('model')}")

    st.markdown("### Preview")
    html = text_to_html(st.session_state.generated_text)
    st.markdown(f"<div class='preview'>{html}</div>", unsafe_allow_html=True)

    st.markdown("### Edit Document")
    edited = st.text_area(
        "Edit the generated document below",
        value=st.session_state.generated_text,
        height=450,
        key="editor",
    )
    if st.button("💾 Apply Edits", use_container_width=True):
        st.session_state.generated_text = edited
        st.success("Edits applied.")
        st.rerun()

    current = st.session_state.generated_text
    filename = safe_filename(st.session_state.get("document_type", "legal_document"))

    st.markdown("### Download")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "⬇️ Download TXT",
            data=format_txt(current),
            file_name=f"{filename}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            "⬇️ Download DOCX",
            data=format_docx(
                current,
                st.session_state.get("document_type", "Legal Document"),
                st.session_state.get("parties", ""),
                st.session_state.get("terms", ""),
            ),
            file_name=f"{filename}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with col3:
        st.download_button(
            "⬇️ Download PDF",
            data=format_pdf(
                current,
                st.session_state.get("document_type", "Legal Document"),
                st.session_state.get("parties", ""),
                st.session_state.get("terms", ""),
            ),
            file_name=f"{filename}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.markdown(
    "<div class='notice'><b>LegalEase notice:</b> Generated content is AI-assisted drafting material, not legal advice. Verify facts, governing law, and enforceability with a qualified legal professional before use.</div>",
    unsafe_allow_html=True,
)
