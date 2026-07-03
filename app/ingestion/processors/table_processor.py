"""
Table extraction processor for KnowledgeMind.

Extracts structured tables from PDF documents using pdfplumber.
"""

import pdfplumber

from app.knowledge.models import KnowledgeTable
from app.utils.logger import logger


class TableProcessor:
    """
    Extract tables from a PDF document.
    """

    def process(self, file_path: str) -> dict[int, list[KnowledgeTable]]:
        """
        Extract tables from each page of a PDF.

        Returns:
            Dictionary where:
                key   -> page number
                value -> list of KnowledgeTable objects
        """

        page_tables = {}

        with pdfplumber.open(file_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                extracted_tables = []

                tables = page.extract_tables()

                logger.info(
                    "Page %s: %s table(s) found",
                    page_number,
                    len(tables),
                )

                for table in tables:

                    cleaned_rows = []

                    for row in table:

                        cleaned_row = []

                        for cell in row:

                            if cell is None:
                                cleaned_row.append("")
                            else:
                                cleaned_row.append(cell.strip())

                        # Remove empty columns from the beginning
                        while cleaned_row and cleaned_row[0] == "":
                            cleaned_row.pop(0)

                        # Remove empty columns from the end
                        while cleaned_row and cleaned_row[-1] == "":
                            cleaned_row.pop()

                        cleaned_rows.append(cleaned_row)

                    extracted_tables.append(
                        KnowledgeTable(
                            page=page_number,
                            rows=cleaned_rows,
                        )
                    )

                page_tables[page_number] = extracted_tables

        return page_tables