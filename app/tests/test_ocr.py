from app.ingestion.processors.ocr_processor import OCRProcessor

processor = OCRProcessor()

text = processor.process(
    "data/test_images/sample.png"
)

print(text)