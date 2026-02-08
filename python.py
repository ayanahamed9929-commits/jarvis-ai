# =========================================
# Premium Jarvis - Boss Edition 😎
# Full Ready-to-Run for GitHub Hosting
# =========================================

import os
import webbrowser
import datetime
import psutil
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from threading import Thread
import time
import random

# Optional: AI ChatGPT
import openai
openai.api_key = "YOUR_OPENAI_API_KEY"  # <-- Boss, replace with your key

# -------------------------------
# Voice Setup
# -------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"Boss said: {command}")
        except:
            speak("Sorry Boss, I did not get that")
            return ""
    return command.lower()

# -------------------------------
# AI Chat Function
# -------------------------------
def ai_chat(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Boss, AI didn't respond. Error: {e}"

# -------------------------------
# Commands Logic
# -------------------------------
MUSIC_FOLDER = "./music"
music_files = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

def play_music():
    if not music_files:
        speak("No music files found Boss")
        return
    song = random.choice(music_files)
    speak(f"Playing {os.path.basename(song)}")
    os.system(f'start {song}')  # Windows only

def execute_command(command):
    if 'open youtube' in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube, Boss")
    elif 'open google' in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif 'time' in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Boss, the time is {now}")
    elif 'date' in command:
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        speak(f"Today's date is {today}")
    elif 'cpu' in command:
        usage = psutil.cpu_percent()
        speak(f"Boss, CPU usage is {usage} percent")
    elif 'ram' in command:
        ram = psutil.virtual_memory().percent
        speak(f"Boss, RAM usage is {ram} percent")
    elif 'play music' in command:
        play_music()
    elif 'stop' in command or 'exit' in command:
        speak("Goodbye Boss! Jarvis shutting down")
        app.destroy()
    else:
        response = ai_chat(command)
        speak(response)

# -------------------------------
# GUI Setup (Tkinter)
# -------------------------------
app = tk.Tk()
app.title("Premium Jarvis - Boss Edition 😎")
app.geometry("600x400")
app.resizable(False, False)
app.configure(bg="#0b0f1a")

# Background Label
bg_label = tk.Label(app, bg="#0b0f1a")
bg_label.pack(fill="both", expand=True)

# Title
title = tk.Label(bg_label, text="Jarvis - Boss Edition", font=("Helvetica", 20, "bold"),
                 fg="#00f5ff", bg="#0b0f1a")
title.pack(pady=20)

# Live Clock
time_label = tk.Label(bg_label, text="", font=("Helvetica", 16), fg="#ffffff", bg="#0b0f1a")
time_label.pack(pady=10)

def update_time():
    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        time_label.config(text=f"Time: {now}")
        time.sleep(1)

Thread(target=update_time, daemon=True).start()

# Command Entry
command_var = tk.StringVar()

def execute_gui_command():
    cmd = command_var.get()
    execute_command(cmd)
    command_var.set("")

entry = tk.Entry(bg_label, textvariable=command_var, font=("Helvetica", 14), width=30)
entry.pack(pady=10)
entry.focus()

btn = tk.Button(bg_label, text="Execute", font=("Helvetica", 12), command=execute_gui_command,
                bg="#00c8ff", fg="#0b0f1a", activebackground="#0099ff", activeforeground="#ffffff")
btn.pack(pady=5)

# Voice Command Button
def voice_loop():
    while True:
        cmd = take_command()
        if cmd:
            execute_command(cmd)

voice_btn = tk.Button(bg_label, text="🎤 Voice Command", font=("Helvetica", 12),
                      command=lambda: Thread(target=voice_loop, daemon=True).start(),
                      bg="#ff5f5f", fg="#0b0f1a", activebackground="#ff0000", activeforeground="#ffffff")
voice_btn.pack(pady=5)

# Start
speak("Hello Boss! Jarvis at your service")
app.mainloop()
