
# 🧠 KnowledgeMind

> **Agentic Personal Knowledge Assistant powered by LangGraph, Ollama and ChromaDB**

KnowledgeMind is an AI-powered Personal Knowledge Assistant that enables users to upload documents, build a semantic knowledge base, and interact with their content using natural language.

Unlike a traditional Retrieval-Augmented Generation (RAG) application, KnowledgeMind uses a **multi-agent workflow** built with **LangGraph** to intelligently plan, retrieve, reason, analyze, compare, summarize, and explain responses.

---

                    🧠 KnowledgeMind

                 Agentic Personal Knowledge Assistant

┌────────────────────────────────────────────────────────────┐
│                     User Interface                         │
│                      Streamlit UI                          │
└────────────────────────────────────────────────────────────┘
                           │
                           ▼
                 User Question / PDF Upload
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                  LangGraph Workflow                        │
└────────────────────────────────────────────────────────────┘
                           │
                           ▼
        ┌────────────── Planner Agent ───────────────┐
        │                                            │
        ▼                                            ▼
 Question Rewriter                           Document Selector
        │
        ▼
┌────────────────────────────────────────────────────────────┐
│                  Semantic Retriever                        │
│      Sentence Transformers + ChromaDB                     │
└────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                 Context Builder                            │
│  • Remove duplicates                                      │
│  • Merge chunks                                           │
│  • Add conversation history                               │
└────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                  Reasoning Agent                           │
└────────────────────────────────────────────────────────────┘
                           │
                           ▼
      ┌────────────┬────────────┬─────────────┐
      ▼            ▼            ▼
 Summary Agent  Compare Agent  Analysis Agent
      │            │            │
      └────────────┴────────────┘
                   ▼
          Response Generator
                   ▼
           Final Answer
        Workflow + Sources

# ✨ Features

## 📄 Document Processing

- PDF ingestion
- OCR support for scanned PDFs
- Automatic document chunking
- Metadata extraction
- Table extraction support
- Image extraction support

---

## 🧠 Agentic Workflow

KnowledgeMind uses multiple AI agents instead of a single prompt.

### Planner Agent

Determines the user's intent and selects the appropriate workflow.

Examples:

- Question Answering
- Summarization
- Document Comparison
- Analysis
- Follow-up Questions

---

### Question Rewriter

Rewrites follow-up questions into standalone questions using conversation history.

Example:

User:

> What is John's salary?

Follow-up:

> What about Alice?

Rewritten to:

> What is Alice's salary?

---

### Retriever

Retrieves semantically relevant document chunks using embeddings stored in ChromaDB.

Supports:

- Search across all documents
- Search within a selected document

---

### Context Builder

Builds an optimized context for the LLM by:

- Removing duplicate chunks
- Merging relevant information
- Preserving page metadata
- Including conversation history

---

### Summary Agent

Generates concise document summaries using Ollama.

Features:

- Markdown formatting
- Bullet points
- Employee summaries
- Table summarization

---

### Compare Agent

Compares multiple documents using the LLM.

Highlights:

- Similarities
- Differences
- Unique information
- Final conclusion

---

### Analysis Agent

Performs reasoning over retrieved information.

Supports:

- Count
- Average
- Maximum
- Minimum
- Grouping
- Sorting
- Filtering

---

# 🚀 Architecture

```
                PDF Documents
                      │
                      ▼
            Knowledge Pipeline
                      │
      ┌───────────────┴───────────────┐
      │                               │
      ▼                               ▼
 PDF Parser                    OCR Processor
      │
      ▼
 Chunk Builder
      │
      ▼
 Embedding Generator
      │
      ▼
 ChromaDB Vector Store
      │
      ▼
        LangGraph Workflow
      │
      ▼
 Planner Agent
      │
      ▼
 Question Rewriter
      │
      ▼
 Retriever
      │
      ▼
 Context Builder
      │
      ▼
 Reasoning Agent
      │
      ▼
 Summary / Compare / Analysis Agent
      │
      ▼
 Response Generator
      │
      ▼
 Streamlit UI
```

---

# 🏗 Project Structure

```
KnowledgeMind
│
├── app
│   ├── agents
│   ├── chunking
│   ├── graph
│   ├── ingestion
│   ├── knowledge
│   ├── llm
│   ├── memory
│   ├── reasoning
│   ├── retrieval
│   ├── services
│   ├── ui
│   └── workflow
│
├── chroma_db
│
├── documents
│
├── requirements.txt
│
└── README.md
```

---

# 🛠 Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.12 |
| Workflow Engine | LangGraph |
| LLM | Ollama (Llama 3.2) |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| UI | Streamlit |
| OCR | Tesseract OCR |
| PDF Parsing | PyMuPDF |

---

# 🔄 Agent Workflow

```
User Question
      │
      ▼
Planner Agent
      │
      ▼
Question Rewriter
      │
      ▼
Retriever
      │
      ▼
Context Builder
      │
      ▼
Reasoning Agent
      │
      ▼
Summary / Compare / Analysis
      │
      ▼
Response Generator
      │
      ▼
Answer + Sources + Workflow
```

---

# 📚 Explainability

KnowledgeMind provides complete transparency for every response.

For every answer the application displays:

- ✅ Agent Workflow
- ✅ Why this answer?
- ✅ Retrieved Sources
- ✅ Source Pages
- ✅ Search Scope

This makes the reasoning process explainable and easy to follow.

---

# 💬 Conversation Memory

KnowledgeMind remembers previous conversations.

Example:

User:

> Summarize this document.

Later:

> Explain section 2.

The Question Rewriter converts the follow-up question into a standalone query before retrieval.

---

# 🔍 Semantic Search

Uses Sentence Transformer embeddings with ChromaDB.

Supports:

- Semantic similarity search
- Document-level filtering
- Cross-document retrieval
- Multi-document reasoning

---

# 📷 User Interface

The Streamlit application includes:

- 📄 PDF Upload
- 📚 Search Scope Selection
- 🧠 Agent Workflow
- 💡 Why this Answer?
- 📑 Source Documents
- 📊 Collection Statistics
- ⚙ AI Stack Overview

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/KnowledgeMind.git

cd KnowledgeMind
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Application

Start Ollama

```bash
ollama serve
```

Pull the model

```bash
ollama pull llama3.2
```

Run Streamlit

```bash
streamlit run app/ui/streamlit_app.py
```

---

# 📖 Example Questions

Summarization

- Summarize this document.
- Give me the key points.

Question Answering

- What is John's salary?
- Who works in HR?

Comparison

- Compare these two documents.
- What are the differences?

Analysis

- Count the employees.
- Which employee has the highest salary?
- Group employees by department.

Follow-up

- What about Alice?
- Explain that section.

---

# 🎯 Future Enhancements

- DOCX support
- Excel support
- PowerPoint support
- Image search
- Confidence scores
- Citation highlighting
- Multi-modal retrieval
- Web search integration
- Knowledge Graph visualization

---

# 📸 Screenshots

Add screenshots here:

- Home Screen
- Document Upload
- Agent Workflow
- Why this Answer
- Sources
- Document Comparison

---

# 👨‍💻 Author

**Nishi Jain**

Senior Software Engineer

Java | Python | Generative AI | LangGraph | Agentic AI

---

# 📄 License

This project is licensed under the MIT License.
