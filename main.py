from app.ingestion.readers.factory import ReaderFactory


def main():

    reader = ReaderFactory.get_reader(
        "data/documents/sample.pdf"
    )

    document = reader.read(
        "data/documents/sample.pdf"
    )

    print()

    print("=" * 60)

    print(document.filename)

    print(document.metadata)

    print("=" * 60)

    for page in document.pages:

        print(f"Page {page.page_number}")

        print(page.text[:200])

        print()

if __name__ == "__main__":
    main()