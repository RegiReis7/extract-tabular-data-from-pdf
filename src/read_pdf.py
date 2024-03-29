from PyPDF2 import PdfReader
import tabula


def read_pdf(pdfFile : any) -> str:
    raw_text = ""
    for i, page in enumerate(PdfReader(pdfFile).pages):
        raw_text += page.extract_text()
    
    return raw_text

def extract_tables_from_pdf(pdf_file):
    # Extract tables from the PDF
    tables = tabula.read_pdf(
        pdf_file, pages='all', multiple_tables=True, pandas_options={'header': None})
    return tables