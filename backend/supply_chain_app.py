import streamlit as st
import requests
import json
import pandas as pd


# -------------------------
# Streamlit UI Setup
# -------------------------
st.set_page_config(page_title="Supply Chain AI Assistant", layout="wide")
st.title("📦 Supply Chain AI Assistant")
st.write("Upload your Excel files and ask questions about inventory, suppliers, orders, and forecasts.")

# -------------------------
# 1️⃣ File Upload Section
# -------------------------
st.header("1️⃣ Upload Excel File")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "pdf", "docx"])

if uploaded_file:
    # Save the file locally before sending to FastAPI
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("Upload File to AI Agent"):
        with st.spinner("Uploading and embedding file..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/upload/",
                    files={"file": open(file_path, "rb")}
                )
                result = response.json()
                if response.status_code == 200:
                    st.success(result.get("message"))
                else:
                    st.error(result.get("error"))
            except Exception as e:
                st.error(f"Upload failed: {str(e)}")

# -------------------------
# 2️⃣ Ask Question Section
# -------------------------
st.header("2️⃣ Ask a Question")
query = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    if not query:
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Processing query..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask/",
                    json={"q": query}
                )
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.subheader("Query:")
                    st.write(result.get("query"))

                    # Beautify JSON answer
                    raw_answer = result.get("answer", "")
                    clean_json_str = raw_answer.replace("```json", "").replace("```", "").strip()
                    try:
                        json_data = json.loads(clean_json_str)
                        df = pd.DataFrame(json_data)
                        st.subheader("Answer (Row-specific Data):")
                        st.dataframe(df)
                    except json.JSONDecodeError:
                        st.subheader("Answer:")
                        st.write(raw_answer)
            except Exception as e:
                st.error(f"Failed to get answer: {str(e)}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.write("Powered by your Supply Chain AI Agent with FAISS embeddings and Open-Source LLM.")

if __name__ == "__main__":
    import os

    # Cloud Run will provide the PORT environment variable
    port = os.environ.get("PORT", "8080")

    # Run Streamlit with correct host + port
    os.system(f"streamlit run streamlit.py --server.port={port} --server.address=0.0.0.0")