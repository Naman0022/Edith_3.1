import pathlib
import textwrap
import markdown

import google.generativeai as genai

genai.configure(api_key='AIzaSyDL-rzwGx6VVEtln2V4n7yX8_VXAZqAZoo')

model = genai.GenerativeModel('gemini-pro')
# while True:
#     question = input(">>")
#     if question=='q':
#         break
#     else:
#         try:
#             response = model.generate_content(question)
#             print("Edith:",response.text)
#         except Exception:
#             print("Sorry I failed to generate content")
#     print("\n",response.prompt_feedback,"\n")

chat = model.start_chat(history=[])
while True:
    question = input(">>")
    if question=='q':
        break
    else:
        try:
            response = chat.send_message(question)
            print("Edith:",response.text)
        except Exception:
            print("Sorry I failed to generate content")
