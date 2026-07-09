from app.ingestion.readers.factory import ReaderFactory


class KnowledgePipeline:
    """
    Main orchestration class for processing any supported knowledge source.
    """

    def process(self, file_path: str, original_filename: str | None = None,):

        reader = ReaderFactory.get_reader(file_path)

        knowledge_document = reader.read(file_path,original_filename=original_filename,)

        return knowledge_document