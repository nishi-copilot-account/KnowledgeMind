import streamlit as st

from app.services.statistics_service import StatisticsService


def render_sidebar():

    statistics_service = StatisticsService()

    statistics = statistics_service.statistics()

    with st.sidebar:

        st.title("🧠 KnowledgeMind")

        st.caption(
            "Agentic Personal Knowledge Assistant"
        )

        st.success(
            "🚀 AI-powered document reasoning"
        )

        
        st.divider()

        # ----------------------------------
        # Search Scope
        # ----------------------------------

        st.subheader("🔍 Search Scope")

        documents = statistics.get(
            "documents",
            [],
        )

        options = [
            "All Documents",
            *documents,
        ]

        selected_document = st.radio(
            "Search in",
            options,
        )

        if selected_document == "All Documents":

            st.info(
                "📚 Searching all indexed documents"
            )

        else:

            st.success(
                f"📄 Current document:\n\n{selected_document}"
            )

        st.divider()

        # ----------------------------------
        # Collection
        # ----------------------------------

        st.subheader("📊 Collection")


        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Documents",
                statistics["document_count"],
            )

        with col2:
            st.metric(
                "Chunks",
                statistics["chunk_count"],
            )

        st.divider()

        # ----------------------------------
        # Indexed Documents
        # ----------------------------------

        st.subheader("📄 Indexed Documents")

        if documents:

            for document in documents:

                st.markdown(f"📄 {document}")

        else:

            st.caption(
                "No documents indexed."
            )

        st.divider()

        st.caption(
            "⚡ Powered by LangGraph + Ollama"
        )

        st.divider()

        st.subheader("⚙️ AI Stack")

        st.info(
            """
        ### ⚙️ AI Stack

        🤖 LLM : llama3.2

        🧠 Embeddings : all-MiniLM-L6-v2

        🗄️ Vector DB : ChromaDB

        🔀 Workflow : LangGraph
        """
        )

    # Return selected document to main app

    if selected_document == "All Documents":

        return ""

    return selected_document