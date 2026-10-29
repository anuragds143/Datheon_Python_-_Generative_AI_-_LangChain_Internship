import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()

st.set_page_config(page_title="Datheon AI Internship Projects", page_icon="🤖", layout="wide")
st.title("🤖 Python + Generative AI + LangChain")
st.caption("Datheon Internship Portfolio — three demonstration tasks")

api_key = os.getenv("OPENAI_API_KEY", "")
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input(
        "OpenAI API key",
        value=api_key,
        type="password",
        help="Your key is used only by this local app. Do not upload it to GitHub."
    )
    model_name = st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4.1-mini"], index=0)
    st.info("Set OPENAI_API_KEY in a local .env file or enter it here for this session.")

def get_llm():
    if not api_key_input.strip():
        st.error("Add your OpenAI API key in the sidebar or in a local .env file.")
        st.stop()
    return ChatOpenAI(model=model_name, api_key=api_key_input.strip(), temperature=0.2)

tab1, tab2, tab3 = st.tabs(["1. Text Summarizer", "2. AI Chatbot", "3. PDF Q&A"])

with tab1:
    st.subheader("Task 1 — Text Summarizer")
    st.write("Summarize long text into clear, useful bullet points.")
    source_text = st.text_area("Paste text to summarize", height=220, placeholder="Paste an article, notes, or other text here...")
    summary_style = st.selectbox("Summary style", ["Bullet points", "Short paragraph", "Executive summary"])
    if st.button("Summarize text", key="summarize"):
        if not source_text.strip():
            st.warning("Please paste some text first.")
        else:
            with st.spinner("Creating summary..."):
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a careful assistant. Summarize only the supplied text. Do not invent facts. Use this format: {style}."),
                    ("human", "Summarize the following text:\n\n{text}")
                ])
                response = (prompt | get_llm()).invoke({"style": summary_style, "text": source_text})
                st.markdown("### Summary")
                st.write(response.content)

with tab2:
    st.subheader("Task 2 — Conversational AI Chatbot")
    st.write("Ask a question and continue the conversation using chat history.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    question = st.chat_input("Ask the chatbot something...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history_text = "\n".join(
                    f'{m["role"].capitalize()}: {m["content"]}'
                    for m in st.session_state.chat_history[-10:]
                )
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful Python and Generative AI learning assistant. Be clear, accurate, and beginner-friendly."),
                    ("human", "Conversation so far:\n{history}\n\nRespond to the latest user message.")
                ])
                answer = (prompt | get_llm()).invoke({"history": history_text})
                answer_text = str(answer.content)
                st.markdown(answer_text)
        st.session_state.chat_history.append({"role": "assistant", "content": answer_text})
    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

with tab3:
    st.subheader("Task 3 — Ask Questions About a PDF")
    st.write("Upload a PDF, index its text, and ask questions grounded in the document.")
    pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if pdf_file is not None:
        if st.button("Process PDF", key="process_pdf"):
            with st.spinner("Reading and indexing PDF..."):
                temp_path = "uploaded_document.pdf"
                with open(temp_path, "wb") as f:
                    f.write(pdf_file.getvalue())
                try:
                    pages = PyPDFLoader(temp_path).load()
                    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
                    chunks = splitter.split_documents(pages)
                    if not chunks:
                        st.error("No readable text was found in this PDF.")
                    else:
                        embeddings = OpenAIEmbeddings(api_key=api_key_input.strip())
                        vectorstore = FAISS.from_documents(chunks, embeddings)
                        st.session_state.pdf_vectorstore = vectorstore
                        st.session_state.pdf_name = pdf_file.name
                        st.success(f"Indexed {len(chunks)} text chunks from {pdf_file.name}.")
                except Exception as exc:
                    st.error(f"Could not process this PDF: {exc}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    pdf_question = st.text_input("Ask a question about the processed PDF")
    if st.button("Ask about PDF", key="ask_pdf"):
        if "pdf_vectorstore" not in st.session_state:
            st.warning("Upload a PDF and click Process PDF first.")
        elif not pdf_question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("Searching the document..."):
                docs = st.session_state.pdf_vectorstore.similarity_search(pdf_question, k=4)
                context = "\n\n".join(doc.page_content for doc in docs)
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Answer using only the provided document context. If the answer is not present, say you could not find it in the PDF. Be concise and mention relevant page numbers when available."),
                    ("human", "Document context:\n{context}\n\nQuestion: {question}")
                ])
                result = (prompt | get_llm()).invoke({"context": context, "question": pdf_question})
                st.markdown("### Answer")
                st.write(result.content)
                with st.expander("View retrieved context"):
                    for i, doc in enumerate(docs, 1):
                        page = doc.metadata.get("page")
                        st.markdown(f"**Passage {i}**" + (f" — page {page + 1}" if isinstance(page, int) else ""))
                        st.write(doc.page_content)
