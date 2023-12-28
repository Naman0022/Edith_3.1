import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',1)
engine.say("अच्छा हूँ भाई, आप कैसे हैं?")
engine.runAndWait()
engine.stop()