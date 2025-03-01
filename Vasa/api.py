from openai import OpenAI
import document_Analyzer 
import json

client  = OpenAI()

def extract_json_from_file(file):
    """Extracts text from a file and converts it to structured JSON using OpenAI."""
    text = str(document_Analyzer.text_Extractor(file))

    openai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Convert the text to JSON with relatable keys and values"},
            {"role": "user", "content": text},
        ]
    )

    response = openai_response.choices[0].message.content.strip()
    
    # Clean the response
    if response.startswith('```json'):
        response = response[7:]
    if response.endswith('```'):
        response = response[:-3]

    try:
        structured_json = json.loads(response)  # Ensure valid JSON
        return structured_json
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from OpenAI"}




