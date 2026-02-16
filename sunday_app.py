import streamlit as st
import speech_recognition as sr
import pyttsx3
import webbrowser
import google.generativeai as genai
import musicLibrary
import threading 

st.set_page_config(page_title="Sunday Voice Assistant", page_icon="🌞", layout="centered")

genai.configure(api_key="AIzaSyDLM2ba1zd3CEexQKPdvDv-xjcUmd2vevc")
model = genai.GenerativeModel("models/gemini-2.5-flash")

recognizer = sr.Recognizer()

engine = pyttsx3.init()

speech_thread = None 

def speak(text):
    global speech_thread 

    def run_speech():
        engine.say(text)
        engine.runAndWait()

    speech_thread = threading.Thread(target=run_speech) 
    speech_thread.start() 

def aiResponse(prompt):
    response = model.generate_content(prompt)
    return response.text

def takeVoiceCommand():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        return command
    except:
        return None

def processCommand(c):
    c_lower = c.lower()

    if "open google" in c_lower:
        webbrowser.open("https://www.google.com/")
        return "Opening Google..."

    elif "open linkedin" in c_lower:
        webbrowser.open("https://www.linkedin.com/")
        return "Opening LinkedIn..."

    elif "open youtube" in c_lower:
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube..."

    elif c_lower.startswith("play"):
        song = c_lower.split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            return f"Playing {song}..."
        else:
            return "Song not found in your music library."

    else:
        result = aiResponse(c)
        return result


st.title("🎤 Sunday - AI Voice Assistant")
st.write("Speak commands and get answer. Example: *open google*, *play song*, *what is AI?*")

if "chat" not in st.session_state:
    st.session_state.chat = []

if st.button("🎙️ Speak to Sunday"):
    st.info("Listening... Speak now 🎧")

    command = takeVoiceCommand()

    if command:
        st.success(f"✅ You said: {command}")

        st.session_state.chat.append(("You", command))

        with st.spinner("Sunday is thinking..."):
            reply = processCommand(command)

        st.session_state.chat.append(("Sunday", reply))

        st.write("### 🤖 Sunday Says:")
        st.write(reply)

        speak(reply)

    else:
        st.error("❌ Sorry, I couldn't understand. Try again.")

if st.button("⛔ Stop Sunday"):
    engine.stop()
    st.warning("Sunday stopped speaking!")

st.write("---")
st.write("## 💬 Conversation History")

for role, msg in st.session_state.chat[::-1]:
    if role == "You":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Sunday:** {msg}")
