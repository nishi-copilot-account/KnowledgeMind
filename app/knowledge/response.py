    """
    Knowledge response model.
    """

    from dataclasses import dataclass

    from app.knowledge.search_result import KnowledgeSearchResult


    @dataclass
    class KnowledgeResponse:
        """
        Final response returned to the UI.
        """

        answer: str

        sources: list[KnowledgeSearchResult]

        workflow: list[str]