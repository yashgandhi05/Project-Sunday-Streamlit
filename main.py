import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import google.generativeai as genai
# import requests
# AIzaSyDaXN-I-YX1I_e5uRGGQ55nVf9o0AkEvrk 

recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

genai.configure(api_key="AIzaSyDLM2ba1zd3CEexQKPdvDv-xjcUmd2vevc")
model = genai.GenerativeModel("models/gemini-2.5-flash") 

def aiResponse(prompt):
    response = model.generate_content(prompt)
    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    else:
         speak("Let me think...")
         result = aiResponse(c)
         print("AI:", result)
         speak(result)

if __name__ == "__main__":
    speak("Initializing Sunday")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout = 2, phrase_time_limit = 1)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "sunday":
                print("Activate Sunday...")
                speak("yes")  

                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                processCommand(command)

        except Exception as e:
            print("Error:", e)
