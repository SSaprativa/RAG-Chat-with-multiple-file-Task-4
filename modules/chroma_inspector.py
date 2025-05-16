import streamlit as st
from langchain.vectorstores import Chroma

def inspect_chroma(vectorstore):
    st.sidebar.markdown("**ChromaDB Inspector**")
    
    try:
        doc_count = vectorstore._collection.count()
        st.sidebar.success(f"{doc_count} documents stored in DB.")
    except Exception as e:
        st.sidebar.error("Could not fetch document")
        st.sidebar.code(str(e))

    # Search inside the vectorstore
    query = st.sidebar.text_input("Test a query against ChromaDB")

    if query:
        try:
            results = vectorstore.similarity_search(query, k=3)
            st.sidebar.markdown("Top Matching Chunks:")
            for i, doc in enumerate(results):
                st.sidebar.markdown(f"**Result {i+1}:**")
                st.sidebar.markdown(doc.page_content[:300] + "...")
                st.sidebar.markdown("---")
        except Exception as e:
            st.sidebar.error("Error querying ChromaDB")
            st.sidebar.code(str(e))