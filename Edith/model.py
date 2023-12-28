from tkinter import *
import google.generativeai as genai

import time
import os
import sys
import urllib
import keyboard
import re


genai.configure(api_key='AIzaSyDL-rzwGx6VVEtln2V4n7yX8_VXAZqAZoo')

model = genai.GenerativeModel('gemini-pro')

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

def handsfreeMode():
    global handsfree
    r=sr.Recognizer()
    # r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.0
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            print('Recognising...')
            question=r.recognize_google(audio,language='en-in')

        except Exception as e:
            speak("please say that again")
            return handsfreeMode()

        audio=r.listen(source)
        if "switch" in question and "mode" in question:
            handsfree = False
            return takeCommand()
        else:
            handsfree=True
            return question

def handsOnMode():
    global handsfree
    question = input("User:")
    if "switch" in question or "mode" in question:
        handsfree = True
        return takeCommand()
    else:
        handsfree=False
        return question

def takeCommand():
    global handsfree
    print(handsfree)
    if handsfree==True:
        return handsfreeMode()
    else:
        return handsOnMode()
    
def updateRules(chat,update):
    if update==False:
        with open('rules.txt') as f:
            rules = f.readlines()
        chat.send_message(rules)
        return
    elif update==True:
        while True:
            print('Edith: Please present the rules you want to add')
            speak('Please present the rules you want to add')
            newcond=takeCommand()
            print("Edith: Please wait...")
            speak("please wait")
            response = chat.send_message("Write these instructions as rules that will be followed by you and seperate lines by symbol ~ and do not include previous instructions only these"+newcond)
            rule = open("rules.txt","a+")
            for rules in response.text.split("~"):
                rule.write(rules)
            rule.close()
            with open('rules.txt') as f:
                rules = f.readlines()
            chat.send_message(rules)
            print("Rules have been updated successfully")
            speak("Rules have been updated successfully")
            speak("Do you wish to add more rules?")
            addRules=takeCommand()
            response=chat.send_message(addRules)
            if "yes" in response.text.lower() or "yep" in response.text.lower():
                continue
            else:
                speak("Developer mode turned off")
                print("Developer mode turned off")
                break   
        return

def developerMode(chat):
    print("Developer Mode on...")
    speak("Developer Mode onn")
    code="None"
    while True:
        code=takeCommand().lower()
        print(">> "+code)
        if "kuala" in code or "koala" in code:
            updateRules(chat,True)
            return
        elif "return" in code or "exit" in code or "get me out" in code:
            break
        else:
            speak("Sorry Code didn't match please try again or say return or exit to turn off developer mode")
            print("Sorry Code didn't match please try again or say return or exit to turn off developer mode")

def playMusic():
    print('Edith: Please tell me name of any song you wantme to play')
    speak('please tell me name of any song you want me to play')
    music_name='none'
    while music_name=='none':
        music_name = takeCommand().lower()
    print("Song name :",music_name)
    
    # importing vlc module 
    import vlc
    import pafy
    import urllib.parse
    import urllib.request
    import re

    music_name = "your_music_name"  # Replace with the actual music name
    query_string = urllib.parse.urlencode({"search_query": music_name})
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_string)

    # Decode the HTML content with UTF-8 encoding to handle potential non-ASCII characters
    video_ids = re.findall(r"watch\?v=(\S{10})", html.read().decode("utf-8"))

    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    print('YouTube link : ', url)

    is_opening = False
    is_playing = False

    video = pafy.new(url)
    best = video.getbestaudio()
    play_url = best.url

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    player.play()

    good_states = [
    	"State.Playing", 
    	"State.NothingSpecial", 
    	"State.Opening"
    ]
    
    while str(player.get_state()) in good_states:
        if str(player.get_state()) == "State.Opening" and is_opening is False:
            print("Status: Loading")
            is_opening = True

        if str(player.get_state()) == "State.Playing" and is_playing is False:
            print("Status: Playing")
            is_playing = True

    print("Status: Finish")
    player.stop()


def longmsg(text):
    f = open('response.txt', 'w')
    f.write(text)
    f.close()
    # Example usage
    filename = "response.txt"
    open_and_wait_for_file_close(filename)
    # window=Tk()
    # window.title('Edith')
    # lbl=Label(window,width=80,wraplength=500,text=text, fg="white", bg="black",justify=LEFT ,font=("Arial",12))
    # lbl.place(x=20, y=20)
    # window.configure(background='black')
    # # window.geometry("")
    # window.mainloop()
    return

import subprocess
import time

def open_and_wait_for_file_close(filename):
  command = f"notepad.exe {filename}"

  # Start the editor process using subprocess.Popen
  process = subprocess.Popen(command)

  # Continuously check if the process is still running
  while True:
    time.sleep(1)  # Check every second to avoid excessive CPU usage
    if process.poll() is not None:  # Use poll() from subprocess
      print("File closed. Resuming program...")
      break


chat = model.start_chat(history=[])

updateRules(chat,False)

quit=False
handsfree=True
question="None"
while True:
    if quit==True:
        break
    question=takeCommand( )
    print(">> "+str(question))
    # try:
    if "developer" in question.lower() and "mode" in question.lower():
        developerMode(chat)
        continue

    response = chat.send_message(question)
    if "reload" in response.text.lower() or "rerun" in response.text.lower() or "reload" in question.lower():
        print("reloading pease wait")
        speak("reloading pease wait")
        quit=True
        os.system("python Edith\model.py")
        # sys.exit(0)
        break
    
    
    elif len(response.text)<=400:
        print("Edith:",response.text)
        speak(response.text)
    else:
        print("Edith: replied on window")
        speak("replied on window")
        longmsg(response.text)
    
    if "song" in response.text.lower():
        playMusic()
    
    if "bye" in response.text.lower():
        quit=True
