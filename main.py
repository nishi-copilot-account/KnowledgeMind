from app.ingestion.models import (
    ParsedDocument,
    DocumentMetadata,
)

def main():

    metadata = DocumentMetadata(
        title="KnowledgeMind Demo",
        author="Nishi Jain",
        page_count=10,
    )

    document = ParsedDocument(
        filename="sample.pdf",
        metadata=metadata,
        pages=[],
    )

    print(document)


if __name__ == "__main__":
    main()