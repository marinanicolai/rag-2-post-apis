
import fitz  
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pdf_content(pdf_file, chunk_size=1000, chunk_overlap=150):
    try:
        doc = fitz.open(pdf_file)

        full_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text("text") + "\n"

        if not full_text.strip():
            return []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_text(full_text)

        return chunks if isinstance(chunks, list) else []
    
    except Exception as e:
        print(f"[PDF Chunk Error]: {e}")
        return []