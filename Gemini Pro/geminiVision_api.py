import pyautogui

myScreenshot = pyautogui.screenshot()
myScreenshot.save('Gemini Pro\\Images\\screen'+str(1)+'.png')
import pathlib
import textwrap

import google.generativeai as genai

genai.configure(api_key='AIzaSyDL-rzwGx6VVEtln2V4n7yX8_VXAZqAZoo')

model = genai.GenerativeModel('gemini-pro-vision')
import PIL.Image

img = PIL.Image.open('Gemini Pro\\Images\\screen.png')
response = model.generate_content(["Can you tell me whats on my screen", img], stream=True)
response.resolve()

print(response.text)