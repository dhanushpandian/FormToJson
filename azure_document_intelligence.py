from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os 
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('key')
endpoint=os.getenv('endpoint')


def text_Extractor(file):
  document_analysis_client = DocumentAnalysisClient(
       endpoint=endpoint, credential=AzureKeyCredential(key)
   )
  poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", document=file, locale="en-US"
    )
  result = poller.result()
  extracted_text = []
  print(type(result))
  print("Analyze result:")
  for page in result.pages:
    print(f"Page {page.page_number}:")
    for line in page.lines:
        print(f" - {line.content}")
        extracted_text.append(line.content)
  return extracted_text   

