import pathlib
import textwrap

import google.generativeai as genai

genai.configure(api_key='AIzaSyDL-rzwGx6VVEtln2V4n7yX8_VXAZqAZoo')

model = genai.GenerativeModel('gemini-pro-vision')

img="D:\code\Python\Edith_3.1\grey-crowned-crane-bird-crane-animal.jpeg"
while True:
    question = input(">>")
    if question=='q':
        break
    else:
        try:
            response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
            response.resolve()
            print("Edith:",response.text)
        except Exception:
            print("Edith: Sorry I failed to generate content")