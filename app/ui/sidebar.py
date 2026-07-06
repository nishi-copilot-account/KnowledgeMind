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

        st.divider()

        st.subheader("📊 Collection")

        st.metric(
            "Documents",
            statistics["document_count"],
        )

        st.metric(
            "Chunks",
            statistics["chunk_count"],
        )

        st.divider()

        st.subheader("📄 Indexed Documents")

        documents = statistics.get(
            "documents",
            [],
        )

        if documents:

            for document in documents:

                st.write(f"• {document}")

        else:

            st.caption("No documents indexed.")

        st.divider()

        st.caption(
            "⚡ Powered by LangGraph + Ollama"
        )