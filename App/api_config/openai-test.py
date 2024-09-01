import os                                                     # Edited #2!!!
from openai import OpenAI
from api_config import OPENAI_API_KEY
from PyPDF2 import PdfReader

client = OpenAI(api_key=OPENAI_API_KEY)

'''completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in \
      explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept \
      of recursion in programming."}
  ]
) '''

pdf_path = os.path.join("../test_docs", "HW1.pdf")            # Edited #3!!!
reader = PdfReader(pdf_path)                                  # Edited #1!!!
page = reader.pages[0]
print(page.extract_text())
# print(completion.choices[0].message)
