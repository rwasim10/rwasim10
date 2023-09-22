#!/usr/bin/env python
# coding: utf-8

# In[25]:


import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator
import pyttsx3


# In[26]:


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Clearing background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        status_label.config(text="Listening for message...")
        audio = recognizer.listen(source, timeout=5)
        status_label.config(text="Done recording...")

    try:
        status_label.config(text="Recognizing...")
        result = recognizer.recognize_google(audio, language='en')
        input_text.delete(1.0, tk.END)  # Clear the text box
        input_text.insert(tk.END, result)
        return result
    except sr.UnknownValueError:
        status_label.config(text="Google Web Speech API could not understand the audio")
        return None
    except sr.RequestError as ex:
        status_label.config(text=f"Could not request results from Google Web Speech API: {ex}")
        return None

def translate_text():
    text_to_translate = input_text.get(1.0, tk.END).strip()
    if not text_to_translate:
        status_label.config(text="Please record speech first.")
        return

    lang_input = target_language.get()
    translator = Translator()
    translated = translator.translate(text_to_translate, dest=lang_input)
    output_text.delete(1.0, tk.END)  # Clear the output text box
    output_text.insert(tk.END, translated.text)
    status_label.config(text=f'Translated text: {translated.text}')

    engine = pyttsx3.init()
    engine.say(translated.text)
    engine.runAndWait()

# Create the main window
root = tk.Tk()
root.title("Speech-to-Text and Translator")
root.geometry("600x400")

# Create and configure widgets
header_label = ttk.Label(root, text="Speech-to-Text and Translator", font=("Arial", 16))
header_label.pack(pady=10)

record_button = ttk.Button(root, text="Record Speech", command=recognize_speech)
record_button.pack(pady=10)

input_label = ttk.Label(root, text="Recognized Speech:")
input_label.pack()

input_text = tk.Text(root, wrap=tk.WORD, width=40, height=5)
input_text.pack()

target_language_label = ttk.Label(root, text="Enter the target language code (e.g., 'es' for Spanish):")
target_language_label.pack()

target_language = ttk.Entry(root)
target_language.pack()

translate_button = ttk.Button(root, text="Translate and Speak", command=translate_text)
translate_button.pack(pady=10)

output_label = ttk.Label(root, text="Translated Text:")
output_label.pack()

output_text = tk.Text(root, wrap=tk.WORD, width=40, height=5)
output_text.pack()

status_label = ttk.Label(root, text="", font=("Arial", 10))
status_label.pack()

# Start the GUI main loop
root.mainloop()


# In[ ]:




