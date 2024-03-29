import streamlit as st
from read_pdf import read_pdf, extract_tables_from_pdf
from rag import RAG

rag = RAG()

def main():

    st.title("PDF Table Extractor")

    # File uploader
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file is not None:
        st.write("PDF file uploaded successfully!")

        # Extract tables
        tables = extract_tables_from_pdf(pdf_file)
        
        if (tables):
            data = read_pdf(pdf_file)
            text_chunks = rag.text_splitter(data)
            vector_store = rag.vector_store(text_chunks)
            query = f"""Give me the \"Product/Service description\", \"Date\", \"Tax Base\", \"Total (USD)\" and \"Email\". If you don't the given variables values, just put it as \"\""""
            response = rag.get_response(query, vector_store)

            st.divider()
            st.write(response)
            
            vector_store.delete_collection()
        else:
            st.write("No tables found in the PDF file.")


if __name__ == "__main__":
    main()
