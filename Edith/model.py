from tkinter import *
import google.generativeai as genai

import time
import os

genai.configure(api_key='AIzaSyDL-rzwGx6VVEtln2V4n7yX8_VXAZqAZoo')

model = genai.GenerativeModel('gemini-pro')

import pyttsx3
import speech_recognition as sr

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    #r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.0
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            print('Recognising...')
            statement=r.recognize_google(audio,language='en-in')

        except Exception as e:
            speak("Sorry could not hear you. please say that again")
            return "None"

        audio=r.listen(source)
        return statement
    
def developerMode(quit):
    print("Developer Mode on...")
    speak("Developer Mode onn")
    while True:
        code=takeCommand().lower()
        print(">> "+code)
        if "quit" in code or "exit" in code:
            return
        if "kuala" in code or "koala" in code:
            speak('Please speak the rules you want to add')
            print('Please speak the rules you want to add')
            newcond=takeCommand()
            print("Edith: Please wait...")
            speak("please wait")
            with open("d:\code\Python\Edith_3.1\Edith\model_dummy.py") as f:
                lines = f.readlines()
            with open("d:\code\Python\Edith_3.1\Edith\model_dummy.py", "w") as f:
                lines.insert(90, "\nchat.send_message("+newcond+")\n")
                f.write("".join(lines))
                speak('code successfully updated')
            time.sleep(1)
            speak("do you want to restart project to save changes made")
            confirm="none"
            while confirm.lower() == "none":
                confirm = takeCommand()
                if 'yes' in confirm or 'yep' in confirm:
                    speak("restarting project. please wait")
                    quit=True
                    os.system('python d:\code\Python\Edith_3.1\Edith\model_dummy.py')
                    return
            speak('the changes will be made on next rerun of the project')
            speak("if you wish to rerun program then speak reload or restart in next input")
        else:
            speak("Sorry Code didn't match please try again or say return or exit to turn off developer mode")
            print("Sorry Code didn't match please try again or say return or exit to turn off developer mode")


def longmsg(text):
    window=Tk()
    window.title('Edith')
    lbl=Label(window,width=80,wraplength=500,text=text, fg="white", bg="black",justify=LEFT ,font=("Arial",12))
    lbl.place(x=20, y=20)
    window.configure(background='black')
    # window.geometry("")
    window.mainloop()



chat = model.start_chat(history=[])

chat.send_message("You are Edith version 3.1 and you were a language model created by google and integrated by Naman Punj .You have to check if any of the text you are given is indicating if a user is sad and if so do try to cheer them up. Alsodo reply every answer in short and do not give anything extra in the reply.if a user says bye or want to leave or wants you to leave your reply should contain the word bye. if user askes to play music reply 'playing : song name'")


quit=False
while True:
    if quit==True:
        break
    question = takeCommand()
    print(">> "+question)
    # try:
    if "developer mode" in question:
        developerMode(quit)
        continue

    response = chat.send_message(question)
    if len(response.text)<=500:
        print("Edith:",response.text)
        speak(response.text)
    else:
        print("replied on window")
        speak("replied on window")
        longmsg(response.text)
    if "bye" in response.text.lower():
        quit=True

