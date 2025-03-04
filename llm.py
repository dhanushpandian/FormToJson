import openai
import os
from dotenv import load_dotenv
import json
import re
import requests

# Load environment variables
load_dotenv()

def ai(messages):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = [
        {"role": "system", "content": "You are a JSON generator. Respond only with valid JSON."},
        {"role": "user", "content": "Give me a JSON output for the data: " + messages}
    ]  

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )

        raw_response = response["choices"][0]["message"]["content"].strip()
        print("AI Raw Response:", raw_response)

        # Extract JSON content using regex
        json_match = re.search(r'```json\s*([\s\S]+?)\s*```', raw_response)
        if json_match:
            raw_response = json_match.group(1).strip()

        return json.loads(raw_response)

    except Exception as e:
        print(f"OpenAI Error: {str(e)}")

    # Fallback to Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY not found in environment variables."}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": f"Convert this text into JSON: {messages}"}]}]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        # Print full API response for debugging
        print("Gemini API Response:", response_data)

        # Extract text response properly
        if "candidates" in response_data:
            return json.loads(response_data["candidates"][0]["content"]["parts"][0]["text"])

        return {"error": "Gemini API failed", "response": response_data}

    except Exception as e:
        return {"error": f"Gemini API Error: {str(e)}"}


if __name__ == "__main__":
    messages = "hii"
    print(ai(messages))