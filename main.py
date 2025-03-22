import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import pywhatkit 

import pyautogui

import datetime
import time
import vlc
currentTime = datetime.datetime.now()
currentTime.hour

from helper import *

#/usr/bin/python3 -m pip install --user python-vlc  

engine = pyttsx3.init()

voices = engine.getProperty('voices')
# newVoiceRate = 150
# engine.setProperty('rate',newVoiceRate)
# engine.setProperty('voice', voices[0].id)
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex') 

 
recognizer  = sr.Recognizer() 

def speak(text):
    engine.say(text)
    engine.runAndWait()


def open_software(software_name):
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if is_app_running("chrome"):
            speak('Chrome is already running!')
            url = 'https://www.google.com'
            subprocess.run(['open', '-a', 'Google Chrome', url])

        else:
            speak("New chrome opened!")
            subprocess.Popen([chrome_path])
    
    elif 'brave browser' in software_name:
        speak('Opening Brave browser...')
        path = "/Applications/Brave Browser.app/Contents/MacOS/Brave"
        if is_app_running("brave"):
            speak('Brave browser is already running!')
            url = 'https://www.google.com'
            subprocess.run(['open', '-a', 'Brave Browser', url])

        else:
            speak("New brave browser opened!")
            subprocess.Popen([path])

    elif 'play' in software_name:
        b='Opening Youtube'
        engine.say(b)
        engine.runAndWait()
        pywhatkit.playonyt(software_name)

    # elif 'notepad' in software_name:
    #     speak('Opening Notepad...')
    #     subprocess.Popen(['notepad.exe'])
     
    # elif 'calculator' in software_name:
    #     speak('Opening Calculator...')
    #     subprocess.Popen(['calc.exe'])
    else:
        speak(f"I couldn't find the software {software_name}")

def close_software(software_name):
    if 'chrome' in software_name:
        speak('Closing Chrome...')
        close_app('chrome')

    # elif 'notepad' in software_name:
    #     speak('Closing Notepad...')
    #     os.system("taskkill /f /im notepad.exe")
    
    # elif 'calculator' in software_name:
    #     speak('Closing Calculator...')
    #     os.system("taskkill /f /im calculator.exe")
    else:
        speak(f"I couldn't find any open software named {software_name}")


def get_greeting():
    if currentTime.hour < 12:
        text='Good morning.'
    elif 12 <= currentTime.hour < 18:
        text='Good afternoon.'
    else:
        text='Good evening.'
    return text + "sir, give password to help you"

def listen_to_wake():
    with sr.Microphone() as source:
        print('Listening for wake word...')
       # greeting = get_greeting()
       # speak(greeting)
        while True:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recorded_audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(recorded_audio, language='en_US')
                text = text.lower()
                if 'jarvis' in text:
                    print('Wake word detected!')
                    mp3_path="./assets/startup1.mp3"
                    player = vlc.MediaPlayer(mp3_path)
                    player.play()
                    time.sleep(6.5) 
                    # speak('Welcome home sir, congratulations on unlocking...  How can I help you?')
                    return True
            except Exception as ex:
                print("Unable to understand the input, please try again!")

def cmd():
    with sr.Microphone() as source:
        print('Clearing background noise... please wait!')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything...')
        recorded_audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(recorded_audio, language='en_US')
        text = text.lower()
        print('Your message:', text)
    except Exception as ex:
        print(ex)
        return

    # if len(text):
    #     pyautogui.press('f10')
    #     time.sleep(2)
    #     pyautogui.press('f10')

    if 'open' in text:
        software_name = text.replace('open', '').strip()
        open_software(software_name)
        
    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        close_software(software_name)

    elif 'stop youtube' in text:
        print("pause youtube")
        b=text or "Pause"
        engine.say(b)
        engine.runAndWait()
        pyautogui.press("k")
        
    elif 'play youtube' in text:
        print("play youtube")
        b=text or 'Play Youtube'
        engine.say(b)
        engine.runAndWait()
        pyautogui.press("k")

    elif substring_in_list([ "remove full screen"], text):
        print("full screen")
        b=text or 'Changing the scree size'
        engine.say(b)
        engine.runAndWait()
        pyautogui.press("f")

    elif substring_in_list(["full screen",  "make full screen", "change screen size"], text):
        print("full screen")
        b=text or 'Changing the scree size'
        engine.say(b)
        engine.runAndWait()
        pyautogui.press("f")

    elif 'unmute' in text:
        print("unmute")
        b=text or "Unmute"
        engine.say(b)
        engine.runAndWait()
        pyautogui.press("m")

    elif 'mute' in text:
        print("mute")
        b=text 

        engine.say(b)
        engine.runAndWait()
        pyautogui.press("m")
    
    # elif 'volume up' in text:
    #     print("volume up")
    #     b='Volume Up'
    #     engine.say(b)
    #     engine.runAndWait()
    #     pyautogui.press("up")

    # elif 'volume down' in text:
    #     print("volume down")
    #     b='Volume Down'
    #     engine.say(b)
    #     engine.runAndWait()
    #     pyautogui.press("down")

    elif 'time' in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print(current_time)
        speak(current_time)
    elif 'who is god' in text:
        engine.setProperty('rate',150)
        speak('Ajith yee Kadavul yee!!')
        engine.setProperty('rate',200)

    elif 'what is your name' in text:
        speak('I am Jarvis, I am your Artificial Intelligence')
    elif substring_in_list(["turn off", "switch off", "off"], text):
        speak('Turning off the program. Goodbye!')
        sys.exit()


# Main program (starting point)
while True:
    if listen_to_wake():
        while True:
            if cmd():
                break