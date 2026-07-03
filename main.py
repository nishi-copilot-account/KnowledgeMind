from app.ingestion.pipeline import KnowledgePipeline


def main():

    pipeline = KnowledgePipeline()

    knowledge = pipeline.process(
        "data/documents/sample.pdf"
    )

    print("=" * 60)
    print(f"Source : {knowledge.filename}")
    print(f"Pages  : {knowledge.metadata.page_count}")
    print("=" * 60)

    for page in knowledge.pages:

        print(f"\nPage : {page.page_number}")

        print("-" * 40)

        print(page.text[:250])

        print()

        print(f"Images : {len(page.images)}")

    for image in page.images:

        print(image["path"])


if __name__ == "__main__":
    main()