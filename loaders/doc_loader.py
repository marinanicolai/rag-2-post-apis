from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_docx_content(docx_file, chunk_size=1000, chunk_overlap=200):

    try:
        doc = Document(docx_file)

        full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_text(full_text)

        return chunks

    except Exception as e:
        raise ValueError(f"Error reading the DOCX file: {str(e)}")
