from app.ingestion.pipeline import KnowledgePipeline


def main():

    pipeline = KnowledgePipeline()

    knowledge = pipeline.process(
        "data/documents/test_club.pdf"
    )

    print("=" * 60)
    print(f"Source : {knowledge.filename}")
    print(f"Pages  : {knowledge.metadata.page_count}")
    print("=" * 60)

    for page in knowledge.pages:

        print(f"\nPage : {page.page_number}")
        print("-" * 40)

        # Display page text
        print(page.text[:250])

        # -----------------------------
        # Images
        # -----------------------------
        print(f"\nImages : {len(page.images)}")

        for index, image in enumerate(page.images, start=1):

            print(f"\nImage {index}")
            print(f"Path : {image.path}")

            print("\nOCR Text:")
            print(image.ocr_text)

            print("-" * 60)

        # -----------------------------
        # Tables
        # -----------------------------
        print(f"\nTables : {len(page.tables)}")

        for table_index, table in enumerate(page.tables, start=1):

            print(f"\nTable {table_index}")

            for row in table.rows:
                print(row)

            print("-" * 60)


if __name__ == "__main__":
    main()