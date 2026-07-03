from app.ingestion.processors.text_processor import TextProcessor


def test_text_processor():

    processor = TextProcessor()

    text = """

        Hello

        World


    """

    cleaned = processor.process(text)

    assert cleaned == "Hello\nWorld"