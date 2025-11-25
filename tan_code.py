import datetime, os, time, webbrowser, pyautogui
import speech_recognition as sr

import pyttsx3
from fuzzywuzzy import fuzz

from queues import incoming_queue

import threading
import asyncio
import websockets
from llm import run_llm

log_to_gui = None  # Will be injected from gui_server

# ---------- Speech engine ----------

engine = pyttsx3.init()

def speak(text):
    print(f"Tan: {text}")
    if log_to_gui:
        log_to_gui(f"Tan: {text}")
    #engine.say(text)
    #engine.runAndWait()

# ---------- Listener ----------
recognizer = sr.Recognizer()
recognizer = sr.Recognizer()

def listen(timeout=100, phrase_time_limit=5):
    try:
        # Wait for a message from the queue (block for at most `timeout` seconds)
        return incoming_queue.get(timeout=timeout)
    except incoming_queue.empty:
        # If no message arrives in time, fallback to input()
        return input()
        

    '''try:
        # Try microphone first
        with sr.Microphone(device_index=6) as source:
            if log_to_gui:
                log_to_gui("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        # Try speech-to-text
        try:
            command = recognizer.recognize_google(audio, language="en-in")
            if log_to_gui:
                log_to_gui(f"You (voice): {command}")
            return command.lower()

        except Exception:
            # Speech not recognized, fall back to text
            if log_to_gui:
                log_to_gui("Voice not recognized. Switching to text mode.")
            return input("You (text): ").strip().lower()

    except Exception as e:
        # Microphone completely unavailable
        if log_to_gui:
            log_to_gui(f"Mic unavailable ({e}). Switching to text mode.")
        return input("You (text): ").strip().lower()'''



# ---------- Wake word ----------
def wait_for_wake_word():
    while True:
        command = listen()
        if command:
            print(f"[DEBUG] Wake check: {command}")
            # Reliable wake word: "hey tan"
            if "hey tan" in command or fuzz.partial_ratio("hey tan", command) > 60:
                speak("Yes, I'm listening...")
                return

# ---------- Command handler ----------
def handle_command(command):
    command = command.lower()

    if "stop" in command or "go to sleep" in command:
        speak("Goodbye!")
        return False

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "screenshot" in command:
        pyautogui.screenshot("screenshot.png")
        speak("Screenshot taken")

    elif "volume up" in command:
        pyautogui.press("volumeup")
        speak("Volume increased")

    elif "volume down" in command:
        pyautogui.press("volumedown")
        speak("Volume decreased")

    else:
        speak(run_llm("Before answering, .Do not correct, expand, autocorrect, infer, or add context. Read my text byte-for-byte.Then answer normally ." +command, "/home/rito/Downloads/Triangulum-10B-Q8_0.gguf")
)

    return True

# ---------- Continuous Tan Loop ----------
def tan_loop():
    speak("Hello, I am Tan. Say 'Hey Tan' to wake me up.")
    while True:
        wait_for_wake_word()  # wait for "hey tan"
        active = True
        speak("I am listening for your commands now.")
        while active:
            command = listen()
            if not command:
                continue
            active = handle_command(command)

def start_ai(logger=None):
    global log_to_gui
    log_to_gui = logger
    tan_loop()



