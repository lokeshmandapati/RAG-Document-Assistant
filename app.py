import streamlit as st
from dotenv import load_dotenv
import tempfile
import os
import time
import requests
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    Docx2txtLoader, 
    CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

st.set_page_config(page_title="RAG File Assistant")

st.title("📚 RAG File Assistant")
st.write("Upload a document and ask questions from it")

uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx", "csv"])


if uploaded_file:

    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    st.success("File uploaded successfully!")

    if st.button("Create Vector Database"):

        with st.spinner("Processing document..."):

            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_extension == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")
            elif file_extension == ".docx":
                loader = Docx2txtLoader(file_path)
            elif file_extension == ".csv":
                loader = CSVLoader(file_path)
            else:
                st.error("Unsupported file format!")
                st.stop()
                
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(docs)

            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

            vectorstore = Chroma(
                persist_directory="chroma_db",
                embedding_function=embeddings
            )
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Processing document chunks...")
            vectorstore.add_documents(chunks)
            progress_bar.progress(1.0)
            
            status_text.text("Finished processing all chunks!")

            vectorstore.persist()

        st.success("Vector database created!")


if os.path.exists("chroma_db"):

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )

    # ✅ FAST GROQ API
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    st.divider()
    
    st.subheader("AI Output Format")
    ai_format = st.radio("Choose the AI Persona:", ("System AI", "Human AI"), horizontal=True)
    
    if ai_format == "System AI":
        system_instructions = """You are a highly objective, precise, and analytical System AI.
Your task is to answer questions using ONLY the provided context.

Guidelines:
- Provide answers in a structured, concise, and direct manner.
- Use bullet points, bold text, and clear formatting.
- Maintain a formal, robotic, and highly factual tone.
- Do NOT make up information outside the context.

If the answer is not present in the context, say:
"SYSTEM ERROR: Information not found in context."
"""
    else:
        system_instructions = """You are a warm, friendly, and conversational Human AI.
Your task is to answer questions using ONLY the provided context.

Guidelines:
- Explain things simply as if you were talking to a friend.
- Be empathetic and use natural, flowing language.
- Provide examples or analogies if it helps.
- Avoid overly technical jargon; keep it accessible.
- Do NOT make up information outside the context.

If the answer is not present in the context, say:
"I'm sorry, but I couldn't find the answer to that in the document."
"""

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_instructions
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}

Provide a detailed explanation.
"""
        )
    ]
)

    st.divider()
    st.subheader("Ask Questions From the Document")

    query = st.text_input("Enter your question")

    if query:

        docs = retriever.invoke(query)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        final_prompt = prompt.invoke({
            "context": context,
            "question": query
        })

        response = llm.invoke(final_prompt)

        st.write("### AI Answer")
        st.write(response.content)