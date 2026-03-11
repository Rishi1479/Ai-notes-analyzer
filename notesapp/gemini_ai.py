# from google import genai
# from pypdf import PdfReader

# client = genai.Client(api_key="AIzaSyBaT2aZhjWC8_iVNSEPFI_u40dQ1ZwIkIk")


# def extract_text(pdf_path):

#     reader = PdfReader(pdf_path)

#     text = ""

#     for page in reader.pages:
#         text += page.extract_text()

#     return text


# def ask_gemini(question, context):

#     prompt = f"""
# You are a helpful assistant.

# Answer the question ONLY using the provided PDF content.

# PDF Content:
# {context}

# Question:
# {question}
# """

#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=prompt
#     )

#     return response.text