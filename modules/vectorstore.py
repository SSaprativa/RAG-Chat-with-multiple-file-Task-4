from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from modules.pdf_handler import save_uploaded
import os

PERSIST_DIR = "./chroma_store"

def load_vectorstore(uploaded_files):
    paths = save_uploaded(uploaded_files)

    docs = []
    for path in paths:
        ext = os.path.splitext(path)[1].lower()

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(path)
            elif ext == ".docx":
                loader = Docx2txtLoader(path)
            elif ext == ".txt":
                loader = TextLoader(path)
            else:
                print(f"Unsupported file type: {ext}")
                continue

            docs.extend(loader.load())

        except Exception as e:
            print(f"Error loading {path}: {e}")
            continue

    if not docs:
        print("No documents were loaded.")
        return None

    # Split and embed
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2")

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
        vectorstore.add_documents(texts)
        vectorstore.persist()
    else:
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )
        vectorstore.persist()

    return vectorstore
