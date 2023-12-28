import pyautogui
import os

import pyttsx3
import speech_recognition as sr

engine=pyttsx3.init()

engine.setProperty('rate', 180)
handsfree=False
i=1

def speak(text):
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
    if(detect(text)=="hi"):
        engine.setProperty("languages",'hi')
        voices=engine.getProperty('voices')
        engine.setProperty('voice',voices[1].id)
    else:
        engine.setProperty("languages",'en')
        voices=engine.getProperty('voices')
        engine.setProperty('voice',voices[2].id)
    engine.say(text)
    engine.runAndWait()


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

print("Edith:",response.text)
speak(response.text)

os.system("python Edith\model.py")