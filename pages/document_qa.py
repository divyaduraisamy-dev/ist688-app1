import streamlit as st
from openai import OpenAI

# 1. Add a title to the web page
st.title("Document Q&A")
st.write("Upload a .txt document and ask a question about it.")

# 2. Ask for the user's OpenAI API key.
#    type="password" hides the key on screen. We never save or print it.
api_key = st.text_input("OpenAI API key", type="password")

# 3. Let the user upload a .txt file
uploaded_file = st.file_uploader("Upload a document (.txt)", type="txt")

# 4. Let the user type a question about the document
question = st.text_input("Your question about the document")

# 5. Only continue when all three things have been provided
if not api_key:
    st.info("Please enter your OpenAI API key to continue.")
elif not uploaded_file:
    st.info("Please upload a .txt document.")
elif not question:
    st.info("Please enter a question.")
elif st.button("Get answer"):
    # 6. Read the uploaded file's text
    document = uploaded_file.read().decode("utf-8")

    # 7. Send the document and the question to OpenAI
    client = OpenAI(api_key=api_key)
    try:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Answer the question using only the document provided.",
                    },
                    {
                        "role": "user",
                        "content": f"Document:\n{document}\n\nQuestion: {question}",
                    },
                ],
            )
        # 8. Show the answer
        st.subheader("Answer")
        st.write(response.choices[0].message.content)
    except Exception as error:
        st.error(f"Something went wrong: {error}")
