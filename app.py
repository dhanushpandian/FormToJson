import streamlit as st
#from pymupdf 
import fitz  
from azure_document_intelligence import text_Extractor
from llm import ai



st.title("Form to JSON!")

f = st.file_uploader("Upload a PDF file", type=["pdf"])

typ=st.selectbox("Select a type", options=['OCR','HTR'])

if f is not None:
    if st.button("Convert to JSON"):
        with st.spinner("Processing... Please wait."):

            if typ=='OCR':
                    doc = fitz.open("pdf", f.read())  
                    text = ""  
                    for page in doc:
                        text += page.get_text("text") + "\n"
                    result = ai(text)  
                    st.json(result)

            elif typ=='HTR':
                    text = str(text_Extractor(f))
                    result = ai(text)  
                    st.json(result)
            
            else:
                st.error("No text found in the PDF file.")


