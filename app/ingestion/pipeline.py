from app.ingestion.readers.factory import ReaderFactory


class KnowledgePipeline:
    """
    Main orchestration class for processing any supported knowledge source.
    """

    def process(self, file_path: str):

        reader = ReaderFactory.get_reader(file_path)

        knowledge_document = reader.read(file_path)

        return knowledge_document