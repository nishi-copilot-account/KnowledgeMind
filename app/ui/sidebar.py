import streamlit as st

from app.services.statistics_service import StatisticsService


def render_sidebar():

    statistics_service = StatisticsService()
    indexing_service = st.session_state.get("indexing_service")

    if indexing_service is None:
        from app.services.indexing_service import IndexingService

        indexing_service = IndexingService()
        st.session_state["indexing_service"] = indexing_service

    statistics = statistics_service.statistics()

    with st.sidebar:

        st.title("🧠 KnowledgeMind")

        st.caption(
            "Agentic Personal Knowledge Assistant"
        )

        st.success(
            "🚀 AI-powered document reasoning"
        )

        # ----------------------------------
        # Upload Document
        # ----------------------------------

        st.subheader("📤 Upload Document")

        uploaded_file = st.file_uploader(
            "Choose a document",
            type=[
                "pdf",
                "docx",
                "txt",
                "md",
                "pptx",
                "xlsx",
            ],
            key="document_uploader",
        )

        if uploaded_file is not None:

            st.session_state["uploaded_file"] = uploaded_file


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
        # Delete Document
        # ----------------------------------

        st.subheader("🗑️ Delete Document")

        documents = indexing_service.vector_store.list_documents()

        if documents:

            document_to_delete = st.selectbox(
                "Select document",
                documents,
                key="delete_document",
            )

            confirm_delete = st.checkbox(
                "I understand this cannot be undone.",
                key="confirm_delete",
            )

            if st.button(
                "🗑️ Delete Document",
                use_container_width=True,
            ):

                if not confirm_delete:
                    st.warning(
                        "Please confirm deletion first."
                    )
                else:
                    indexing_service.delete_document(
                        document_to_delete,
                    )

                    st.session_state.pop(
                        "last_uploaded_file",
                        None,
                    )

                    st.session_state.pop(
                        "uploaded_file",
                        None,
                    )

                    # Reset the uploader widget
                    st.session_state.pop(
                        "document_uploader",
                        None,
                    )

                    # Allow the same document to be uploaded again
                    st.session_state.pop(
                        "last_indexed_file",
                        None,
                    )

                    # Clear the uploader as well
                    st.session_state.pop(
                        "uploaded_file",
                        None,
                    )

                    st.success(
                        f"✅ {document_to_delete} deleted successfully."
                    )

                    st.rerun()

        else:

            st.caption(
                "No documents available to delete."
            )

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

    