import streamlit as st
from read_pdf import read_pdf, extract_tables_from_pdf
from rag import RAG
import pandas as pd



def main():

    st.title("PDF Table Extractor")
    
    MISTRAL_API_KEY = st.text_input("Mistral API Key", type="password")
    
    if MISTRAL_API_KEY:
    
        rag = RAG(mistral_api_key=MISTRAL_API_KEY)
        
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
                query = f"""Give me the invoice data"""
                response = rag.get_response(query, vector_store)
                

                st.divider()
                st.write(response)

            else:
                st.write("No tables found in the PDF file.")
    else:
        st.write("Please enter your Mistral API key.")


if __name__ == "__main__":
    main()
