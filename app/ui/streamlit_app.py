import tempfile
from pathlib import Path

import streamlit as st

from app.services.indexing_service import IndexingService
from app.services.knowledge_service import KnowledgeService
from app.ui.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="KnowledgeMind",
    page_icon="🧠",
    layout="wide",
)

# --------------------------------------------------
# Initialize Services
# --------------------------------------------------

if "knowledge_service" not in st.session_state:

    st.session_state.knowledge_service = KnowledgeService()

if "indexing_service" not in st.session_state:

    st.session_state.indexing_service = IndexingService()

knowledge_service = st.session_state.knowledge_service
indexing_service = st.session_state.indexing_service

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

selected_document = render_sidebar()

# --------------------------------------------------
# Handle PDF Upload
# --------------------------------------------------

uploaded_file = st.session_state.get(
    "uploaded_file"
)

index_clicked = st.session_state.get(
    "index_clicked",
    False,
)

if uploaded_file and index_clicked:

    with st.spinner(
        "📄 Indexing document..."
    ):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as tmp:

            tmp.write(
                uploaded_file.getbuffer()
            )

            temp_path = Path(tmp.name)

        try:

            indexing_service.index_document(
                str(temp_path)
            )

            st.success(
                f"✅ {uploaded_file.name} indexed successfully!"
            )

        except Exception as ex:

            st.error(str(ex))

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 KnowledgeMind")

st.markdown(
    """
### Agentic Personal Knowledge Assistant

Upload • Search • Summarize • Compare • Analyze
"""
)

# --------------------------------------------------
# Chat History
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

if not st.session_state.messages:

    st.info(
        """
### 👋 Welcome to KnowledgeMind

Try asking questions like:

- 📄 Summarize this document
- ⚖️ Compare both documents
- 🔍 What is John's salary?
- 📊 List all employees
- 💡 Explain this document
"""
    )    

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your indexed documents..."
)

if question:

    # --------------------------------------
    # User Message
    # --------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # --------------------------------------
    # Live Workflow Status
    # --------------------------------------

    status = st.status(
        "🧠 Executing Agent Workflow...",
        expanded=True,
    )

    status.write("🧠 Planner started")
    status.write("🔍 Searching knowledge base")
    status.write("🧩 Building context")
    status.write("🤖 Generating response")

    # --------------------------------------
    # Ask KnowledgeMind
    # --------------------------------------

    response = knowledge_service.ask(
        question=question,
        selected_document=selected_document,
    )

    # --------------------------------------
    # Show executed workflow
    # --------------------------------------

    if response.workflow:

        for step in response.workflow:

            status.write(
                f"✅ {step}"
            )

    status.update(
        label="✅ KnowledgeMind Finished",
        state="complete",
    )

    # --------------------------------------
    # Save Assistant Message
    # --------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
        }
    )

    # --------------------------------------
    # Assistant Response
    # --------------------------------------

    with st.chat_message("assistant"):
    
        if selected_document:

            st.info(
                f"📄 Search Scope: **{selected_document}**"
            )

        else:

            st.info(
                "📚 Search Scope: **All Documents**"
            )
        
        st.markdown(response.answer)

        # ----------------------------------
        # Workflow
        # ----------------------------------

        if response.workflow:

            with st.expander(
                "🧠 Agent Workflow",
                expanded=False,
            ):

                for step in response.workflow:

                    st.write(
                        f"✅ {step}"
                    )
        # ----------------------------------
        # Why this Answer
        # ----------------------------------

        if response.explanation:

            with st.expander(
                "🧠 Why this answer?",
                expanded=False,
            ):

                for item in response.explanation:

                    st.write(
                        f"✓ {item}"
                    )

        # ----------------------------------
        # Sources
        # ----------------------------------

        if response.sources:

            st.markdown("---")

            st.caption(
                "📄 Sources"
            )

            shown = set()

            for result in response.sources:

                key = (
                    result.chunk.source_document,
                    result.chunk.page_number,
                )

                if key in shown:
                    continue

                shown.add(key)

                with st.expander(
                    f"📄 {result.chunk.source_document} "
                    f"(Page {result.chunk.page_number})"
                ):

                    st.markdown(
                        f"**Document:** "
                        f"{result.chunk.source_document}"
                    )

                    st.markdown(
                        f"**Page:** "
                        f"{result.chunk.page_number}"
                    )

                    st.divider()

                    st.caption(
                        f"Preview ({len(result.chunk.text)} characters)"
                    )

                    preview = result.chunk.text

                    if len(preview) > 400:

                        preview = preview[:400] + "..."

                    st.text(preview)

st.markdown("---")

st.caption("Powered by LangGraph • Ollama • ChromaDB • Sentence Transformers • Streamlit")                    