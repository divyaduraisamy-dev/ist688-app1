import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# 1. Add a title to the web page
st.title("PDF Summarizer")
st.write("Upload a PDF or .txt document and get a summary.")

# 2. Sidebar dropdown menus
summary_type = st.sidebar.selectbox(
    "Type of summary",
    [
        "Summarize the document in 100 words",
        "Summarize the document in 2 connecting paragraphs",
        "Summarize the document in 5 bullet points",
    ],
)

language = st.sidebar.selectbox(
    "Language",
    ["English", "Spanish", "French", "German", "Chinese", "Hindi"],
)

# Mini is the default (listed first): it is cheaper and faster,
# and good enough for most summaries.
model_choice = st.sidebar.selectbox("Model", ["Mini", "Flagship"])
if model_choice == "Mini":
    model = "gpt-4o-mini"
else:
    model = "gpt-4o"

# 3. Get the OpenAI API key from Streamlit secrets (not from the user)
if "OPENAI_API_KEY" not in st.secrets:
    st.error("No OpenAI API key found. Add OPENAI_API_KEY to your Streamlit secrets.")
    st.stop()
api_key = st.secrets["OPENAI_API_KEY"]

# 4. Let the user upload a PDF or .txt file
uploaded_file = st.file_uploader("Upload a document (.pdf or .txt)", type=["pdf", "txt"])

if not uploaded_file:
    st.info("Please upload a document.")
else:
    # 5. Get the text out of the file
    if uploaded_file.name.lower().endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        document = ""
        for page in reader.pages:
            document += (page.extract_text() or "") + "\n"
    else:
        document = uploaded_file.read().decode("utf-8")

    if not document.strip():
        st.warning("No text could be found in this document.")
    else:
        # 6. Send the document and the summary instructions to OpenAI
        client = OpenAI(api_key=api_key)
        instructions = f"{summary_type}. Write the summary in {language}."
        try:
            with st.spinner("Summarizing..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": f"Document:\n{document}"},
                    ],
                )
            # 7. Show the summary
            st.subheader("Summary")
            st.write(response.choices[0].message.content)
        except Exception as error:
            st.error(f"Something went wrong: {error}")
