import streamlit as st
#from pymupdf 
import fitz  
import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai(user_message, model="gpt-4o", temperature=0):
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that converts forms into JSON."},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature  
    )
    
    return response.choices[0].message.content

st.title("Form to JSON!")

f = st.file_uploader("Upload a PDF file", type=["pdf"])

if f is not None:
    doc = fitz.open("pdf", f.read())  
    
    text = ""  
    for page in doc:
        text += page.get_text("text") + "\n"
    
    with st.spinner("Processing... Please wait."):
        result = ai(text)  
  
    st.json(result)
