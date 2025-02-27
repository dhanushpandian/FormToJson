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
    messages = [{"role": "user", "content": "Form to JSON! " + messages}]  
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    
    raw_response = response.choices[0].message.content.strip()  
    
    
    print("AI Raw Response:", raw_response)  
    
    # Extract JSON content using regex
    json_match = re.search(r'```json\s*([\s\S]+?)\s*```', raw_response)  
    if json_match:
        raw_response = json_match.group(1).strip()
    else:
       
        raw_response = raw_response.strip()
    
   
    try:
        json_data = json.loads(raw_response)
        return json_data  
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}", "response": raw_response} 




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
