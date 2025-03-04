import streamlit as st
import fitz  # PyMuPDF
from azure_document_intelligence import text_Extractor
from llm import ai
st.markdown(
    """
    <style>
        /* Gradient background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to right, #2b5876, #4e4376);
            color: white;
        }
        
        /* Center title */
        h1 {
            text-align: center;
            font-family: 'Arial', sans-serif;
        }

        /* Custom file uploader */
        .st-emotion-cache-1d3w5wq {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
        }

        /* Stylish button */
        div.stButton > button {
            background: #ff9800;
            color: white;
            border-radius: 5px;
            width: 100%;
            font-size: 16px;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background: #ff5722;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 Form to JSON Converter")

f = st.file_uploader("📤 Upload a PDF file", type=["pdf"], help="Only PDF files are supported.")

typ = st.selectbox("⚙ Select Processing Type", options=['OCR', 'HTR'])

if f is not None and st.button("🚀 Convert to JSON"):
    with st.spinner("⏳ Processing... Please wait."):
        try:
            if typ == 'OCR':
                doc = fitz.open("pdf", f.read())  
                text = "\n".join([page.get_text("text") for page in doc])  
                result = ai(text)  
                st.json(result)

            elif typ == 'HTR':
                text = str(text_Extractor(f))
                result = ai(text)  
                st.json(result)

            else:
                st.error("❌ No text found in the PDF file.")
        
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
