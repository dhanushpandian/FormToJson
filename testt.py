import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"

# Generate response
response = model.generate_content("Explain how AI works")

# Print response
print(response.text)
