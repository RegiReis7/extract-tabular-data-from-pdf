import streamlit as st
import tabula


def extract_tables_from_pdf(pdf_file):
    # Extract tables from the PDF
    tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
    return tables

def main():
    st.title("PDF Table Extractor")

    # File uploader
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])
    
    if pdf_file is not None:
        st.write("PDF file uploaded successfully!")

        # Extract tables
        tables = extract_tables_from_pdf(pdf_file)

        if tables:
            st.write(f"Number of tables found: {len(tables)}")

            # Display tables and convert to JSON
            for i, table in enumerate(tables):
                st.write(f"Table {i + 1}")
                st.write(table)

                # Convert table to JSON
                table_json = table.to_json(orient="records")
                st.write("Table JSON:")
                st.code(table_json)

                # Option to download JSON
                st.download_button(
                    label="Download JSON",
                    data=table_json,
                    file_name=f"table_{i + 1}.json",
                    mime="application/json"
                )
        else:
            st.write("No tables found in the PDF.")
    
if __name__ == "__main__":
    main()
