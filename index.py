import streamlit as st
import warnings
import logging

from modules.pdf_handler import upload_files
from modules.vectorstore import load_vectorstore
from modules.chroma_inspector import inspect_chroma
from modules.chat import display_chat_history, handle_user_input, download_chat_history
from modules.llm import get_llm_chain

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

st.set_page_config(page_title="Ragbot")

# application title
st.title("Ask Ragbot!")

# step 1 : upload pdf and submit
uploaded_files,submitted = upload_files()

# step 2 : user submit to vectostore
if submitted and uploaded_files:
    with st.spinner("Updating Vector Databases..."):
        vectorstore = load_vectorstore(uploaded_files)
        st.session_state.vectorstore = vectorstore

# step 3 : display vectorstore inspector(chromadb)
if "vectorstore" in st.session_state:
    inspect_chroma(st.session_state.vectorstore)

# step 4 : display chat history
display_chat_history()

# step 5 : handle new user prompt
if "vectorstore" in st.session_state:
    handle_user_input(get_llm_chain(st.session_state.vectorstore))

# step 6 : download chat history
download_chat_history()