import streamlit as st
import api


st.title("📄 File to JSON Converter")

uploaded_file = st.file_uploader("Upload a file (PDF, Word, Image, etc.)", type=["pdf", "docx", "png", "jpg", "jpeg"])

if uploaded_file:
    st.write("✅ File uploaded successfully!")
    
    if st.button("Process File"):
        with st.spinner('Processing your file... This may take a moment.'):
            try:
                json_output = api.extract_json_from_file(uploaded_file)
                
                st.success("Processing complete!")
                st.subheader("📌 JSON Output")
                st.json(json_output)
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")