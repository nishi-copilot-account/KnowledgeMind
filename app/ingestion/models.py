from dataclasses import dataclass, field


@dataclass
class DocumentMetadata:

    title: str = ""

    author: str = ""

    subject: str = ""

    keywords: str = ""

    page_count: int = 0


@dataclass
class DocumentImage:

    page: int

    image_path: str

    ocr_text: str = ""


@dataclass
class DocumentTable:

    page: int

    rows: list


@dataclass
class DocumentPage:

    page_number: int

    text: str = ""

    images: list[DocumentImage] = field(default_factory=list)

    tables: list[DocumentTable] = field(default_factory=list)


@dataclass
class ParsedDocument:

    filename: str

    metadata: DocumentMetadata

    pages: list[DocumentPage]