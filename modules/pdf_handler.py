import streamlit as st
import tempfile

# Allow upload of multiple files: PDF, DOCX, TXT
def upload_files():
    with st.sidebar:
        st.header("Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose PDF, DOCX, or TXT files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        submit = st.button("Submit to DB")
    return uploaded_files, submit

# Save uploaded files to temp location for processing
def save_uploaded(uploaded_files):
    file_paths = []
    for file in uploaded_files:
        suffix = f".{file.name.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            file_paths.append(tmp.name)
    return file_paths
