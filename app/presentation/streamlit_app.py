"""Streamlit web application for KnowledgeMind."""

import streamlit as st


def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="KnowledgeMind", layout="wide")
    
    st.title("KnowledgeMind - Enterprise Knowledge Intelligence Platform")
    
    st.markdown("""
    Welcome to KnowledgeMind, an agentic enterprise knowledge intelligence platform
    built with LangGraph, LangChain, ChromaDB, and Large Language Models.
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Query", "Documents", "Settings"])
    
    if page == "Home":
        st.write("Welcome to the home page")
    elif page == "Query":
        st.write("Query the knowledge base")
    elif page == "Documents":
        st.write("Manage documents")
    elif page == "Settings":
        st.write("Application settings")


if __name__ == "__main__":
    main()
