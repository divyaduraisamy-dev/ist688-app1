import streamlit as st

# Define the two pages of the app
tip_page = st.Page("pages/tip_calculator.py", title="Tip Calculator")
qa_page = st.Page("pages/document_qa.py", title="Document Q&A")

# Build the navigation menu and run whichever page the user selects
page = st.navigation([tip_page, qa_page])
page.run()
