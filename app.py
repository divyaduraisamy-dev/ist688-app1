import streamlit as st

# Define the three pages of the app
tip_page = st.Page("pages/tip_calculator.py", title="Tip Calculator")
qa_page = st.Page("pages/document_qa.py", title="Document Q&A")
# default=True makes the PDF Summarizer the page that opens first
pdf_page = st.Page("pages/pdf_summarizer.py", title="PDF Summarizer", default=True)

# Build the navigation menu and run whichever page the user selects
page = st.navigation([tip_page, qa_page, pdf_page])
page.run()
