import pdfplumber

from app.ingestion.models import DocumentTable


class TableExtractor:

    def extract(self, pdf_path):

        tables = {}

        with pdfplumber.open(pdf_path) as pdf:

            for page_no, page in enumerate(pdf.pages, start=1):

                extracted = page.extract_tables()

                page_tables = []

                for table in extracted:

                    page_tables.append(

                        DocumentTable(

                            page=page_no,

                            rows=table,

                        )

                    )

                tables[page_no] = page_tables

        return tables