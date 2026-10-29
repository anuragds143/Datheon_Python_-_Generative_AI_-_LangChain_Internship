# Datheon Python + Generative AI & LangChain Internship

A beginner-friendly portfolio app demonstrating three Generative AI tasks with Python, Streamlit, and LangChain.

## Included projects

1. **Text Summarizer** — turns pasted text into bullet points, a short paragraph, or an executive summary.
2. **Conversational AI Chatbot** — answers questions and keeps a short chat history during the session.
3. **PDF Question Answering (RAG)** — extracts PDF text, splits it into chunks, indexes the chunks with embeddings, retrieves relevant passages, and answers using the retrieved context.

> Important: These are sample projects. Compare them with the official Datheon syllabus and adjust them to match the assigned tasks before submitting.

## Requirements

- Python 3.10 or newer
- An OpenAI API key with API access and billing configured
- Internet connection for model and embedding API calls

## Setup on Windows

1. Install Python from https://www.python.org/downloads/ if needed.
2. Extract this project ZIP.
3. Open Command Prompt or the terminal in this folder.
4. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Copy `.env.example` to `.env` and add your API key:

   ```env
   OPENAI_API_KEY=your_real_api_key_here
   ```

   Keep `.env` private. It is ignored by Git and must never be uploaded to GitHub.

7. Start the app:

   ```bash
   streamlit run app.py
   ```

8. Streamlit will show a local URL, usually `http://localhost:8501`.

## Setup on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Add your key to `.env`, then run:

```bash
streamlit run app.py
```

## Folder structure

```text
Datheon_Python_Generative_AI_LangChain_Internship/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How the PDF Q&A task works

This is a simple Retrieval-Augmented Generation (RAG) workflow:

1. Load PDF text with `PyPDFLoader`.
2. Split text into overlapping chunks.
3. Create embeddings and store them in FAISS.
4. Retrieve the most relevant chunks for a question.
5. Ask the language model to answer based on the retrieved context.

## Privacy and safety

- Do not upload API keys, `.env` files, private documents, or personal information.
- PDF text is sent to the configured model/embedding provider when you process and query it.
- Model responses can be incorrect; verify important information.
- API usage may incur charges depending on your provider account.

## Before submitting to Datheon

- [ ] Run the app and test each tab.
- [ ] Confirm the three tasks match the official syllabus.
- [ ] Add screenshots or a short demo if useful.
- [ ] Push the project to the required **public** GitHub repository.
- [ ] Check that `.env` and your API key are not in the repository.
- [ ] Submit the public repository URL through Datheon's official form.

## Suggested GitHub repository name

`Datheon_Python_+_Generative_AI_&_LangChain_Internship`
