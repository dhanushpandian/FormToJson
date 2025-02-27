import streamlit as st
#from pymupdf 
import fitz  
import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import json

def ai(messages, model="gpt-4o-mini", temperature=0):
    messages = "Form to JSON!" + messages   
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": messages}],  # Ensure messages is a list
        temperature=temperature,
    )
    
    raw_response = response.choices[0].message.content
    
    # Remove markdown code blocks if present
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:]  # Remove ```json
    if raw_response.endswith("```"):
        raw_response = raw_response[:-3]  # Remove ```
    
    try:
        json_data = json.loads(raw_response)  # Validate JSON format
        return json_data  # Return parsed JSON
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}\nResponse: {raw_response}"




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
