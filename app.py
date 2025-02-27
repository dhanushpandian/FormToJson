import streamlit as st
#from pymupdf 
import fitz  
import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import json

import re

def ai(messages, model="gpt-4o-mini", temperature=0):
    messages = [{"role": "user", "content": "Form to JSON! " + messages}]  # Correct messages format
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    
    raw_response = response.choices[0].message.content.strip()  # Ensure clean response
    
    # Debug: Print AI response
    print("AI Raw Response:", raw_response)  
    
    # Extract JSON content using regex
    json_match = re.search(r'```json\s*([\s\S]+?)\s*```', raw_response)  # Match content inside ```json ... ```
    if json_match:
        raw_response = json_match.group(1).strip()
    else:
        # If no markdown, assume the whole response is JSON
        raw_response = raw_response.strip()
    
    # Try parsing as JSON
    try:
        json_data = json.loads(raw_response)
        return json_data  # Successfully parsed JSON
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}", "response": raw_response}  # Return error for debugging





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
