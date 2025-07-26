# uv pip install google-generativeai
# uv pip install pymupdf

# filename: pdf_agent.py

import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai


# Step 1: Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Step 2: Load Gemini Model
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# Step 3: PDF Reader Agent
class PDFReaderAgent:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_text = self._extract_pdf_text()
        
    def _extract_pdf_text(self):
        text = ""
        doc = fitz.open(self.pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def ask(self, question):
        prompt = f"""
        You are a smart PDF assistant. Only answer using the information in this PDF:

        {self.pdf_text}

        Now answer this question:
        {question}
        """
        response = model.generate_content(prompt)
        return response.text

# Step 4: Use the Agent
if __name__ == "__main__":
    agent = PDFReaderAgent("infomation.pdf")  # 🔁 Apni PDF file ka naam yahan do
    question = input("📄 PDF se kya poochna hai? Sawal likho: ")
    answer = agent.ask(question)

    print("\n🤖 Agent ka jawab:")
    print(answer)

   


# import os
# import fitz  # PyMuPDF

# file_name = "infomation.pdf"  # <-- yahan file ka sahi naam likho

# if os.path.exists(file_name):
#     print("✅ File mil gayi!")
#     doc = fitz.open(file_name)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     print(text[:500])  # sirf first 500 characters print hon
# else:
#     print("❌ File nahi mili. Name ya path galat hai.")
