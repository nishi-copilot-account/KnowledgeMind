from docx import Document

from app.ingestion.readers.docx_reader import DOCXReader


def test_docx_reader_reads_simple_document(tmp_path):
    path = tmp_path / "sample.docx"

    document = Document()
    document.add_paragraph("Hello world")
    document.save(path)

    reader = DOCXReader()
    knowledge = reader.read(str(path))

    assert knowledge.filename == path.name
    assert knowledge.pages[0].text.strip() == "Hello world"
