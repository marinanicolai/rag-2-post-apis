import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_excel_content(excel_file, chunk_size=1000, chunk_overlap=200):
    """
    Extract and chunk content from an Excel file using LangChain's RecursiveCharacterTextSplitter.

    :param excel_file: Excel file path or file object.
    :param chunk_size: Size of each chunk in characters.
    :param chunk_overlap: Overlap between chunks in characters.
    :return: List of text chunks.
    """
    try:
        excel_data = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
    except ValueError as e:
        if "Excel file format cannot be determined" in str(e):
            try:
                excel_data = pd.read_excel(excel_file, sheet_name=None, engine='xlrd')
            except Exception as fallback_e:
                raise ValueError(f"Excel read failed with both engines: {fallback_e}")
        else:
            raise ValueError(f"Error reading the Excel file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading the Excel file: {e}")

    full_text = ""

    for sheet_name, df in excel_data.items():
        sheet_text = df.to_string(index=False)
        full_text += f"Sheet: {sheet_name}\n{sheet_text}\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(full_text)

    return chunks