from app.document_loader import load_pdf, split_documents


pdf_path = "data/annual_report.pdf"

documents = load_pdf(pdf_path)

print("Pages:", len(documents))

chunks = split_documents(documents)

print("Chunks:", len(chunks))

print("\nFirst chunk:")
print(chunks[0].page_content)

print("\nMetadata:")
print(chunks[0].metadata)