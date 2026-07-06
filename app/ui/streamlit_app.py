import streamlit as st

from app.ui.sidebar import render_sidebar
from app.services.knowledge_service import KnowledgeService

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="KnowledgeMind",
    page_icon="🧠",
    layout="wide",
)

# --------------------------------------------------
# Initialize Knowledge Service
# --------------------------------------------------

if "knowledge_service" not in st.session_state:

    st.session_state.knowledge_service = KnowledgeService()

knowledge_service = st.session_state.knowledge_service

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

render_sidebar()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 KnowledgeMind")

st.write(
    "Agentic Personal Knowledge Assistant"
)

# --------------------------------------------------
# Chat History
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask your documents..."
)

if question:

    # -------------------------------
    # Show User Message
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # -------------------------------
    # Ask KnowledgeMind
    # -------------------------------

    with st.spinner("🧠 Thinking..."):

        response = knowledge_service.ask(question)

    # -------------------------------
    # Save Assistant Message
    # -------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
        }
    )

        # -------------------------------
        # Display Assistant Response
        # -------------------------------

        with st.chat_message("assistant"):

            st.markdown(response.answer)

            # -----------------------------------
            # Workflow
            # -----------------------------------

            if response.workflow:

        st.markdown("---")
        st.caption("🧠 AI Workflow")

        for step in response.workflow:
            st.write(step)

            # -----------------------------------
            # Sources
            # -----------------------------------

            if response.sources:

                st.markdown("---")

                st.caption("📄 Sources")

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
                        f"(Page {result.chunk.page_number})",
                        expanded=False,
                    ):

                        st.markdown(
                            f"**Document:** "
                            f"{result.chunk.source_document}"
                        )

                        st.markdown(
                            f"**Page:** {result.chunk.page_number}"
                        )

                        st.divider()

                        st.text(
                            result.chunk.text
                        )

        # -----------------------------------
        # Workflow Trace
        # -----------------------------------

        if response.workflow:

            st.markdown("---")

            with st.expander(
                "🧠 Agent Workflow",
                expanded=False,
            ):

                st.caption(
                    "Execution Trace"
                )

                for step in response.workflow:

                    st.write(
                        f"✅ {step}"
                    )