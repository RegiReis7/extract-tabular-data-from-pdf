import streamlit as st
import tabula
from PyPDF2 import PdfReader


def extract_tables_from_pdf(pdf_file):
    # Extract tables from the PDF
    tables = tabula.read_pdf(
        pdf_file, pages='all', multiple_tables=True, pandas_options={'header': None})
    return tables


def main():
    
    data_list = []
    
    st.title("PDF Table Extractor")

    # File uploader
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file is not None:
        st.write("PDF file uploaded successfully!")
        
        data = PdfReader(pdf_file).pages[0].extract_text()

        # Extract tables
        tables = extract_tables_from_pdf(pdf_file)
        
        st.divider()

        if tables:
            st.write(f"Number of tables found: {len(tables)}")

            # Display tables and convert to JSON
            for i, table in enumerate(tables):
                st.write(f"Table {i + 1}")
                st.write(table)
                
                if(i == 1):
                    service = table.to_dict(orient="records")[1][0]
                elif (i == 3):
                    tax_base = table.to_dict(orient="records")[0][1]
                    total_usd = table.to_dict(orient="records")[2][1]

                # Convert table to JSON
                table_json = table.to_json(orient="records")

                st.write("JSON Output:")
                st.code(table.to_dict(orient="records"))

                # Option to download JSON
                st.download_button(
                    label="Download JSON",
                    data=table_json,
                    file_name=f"table_{i + 1}.json",
                    mime="application/json"
                )
            
            st.divider()
                
            st.write("Product/service description: " + service)
            st.write("Date: " + data[data.find("Fecha:")+6:data.find("Fecha:")+18])
            st.write("Tax Base: " + tax_base)
            st.write("TOTAL (USD): " + total_usd)
        
        else:
            st.write("No tables found in the PDF.")


if __name__ == "__main__":
    main()
