import os
import shlex
quote = shlex.quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

@eel.expose
def processQuery(query):
    """Central function to process user queries and route to appropriate handlers."""
    if not query or query.strip() == "":
        return
    
    # Display user query in chat canvas
    eel.senderText(query)
    
    query_lower = query.lower()
    
    try:
        if "open" in query_lower:
            openCommand(query_lower)
        elif "play" in query_lower and "youtube" in query_lower:
            PlayYoutube(query_lower)
        elif any(word in query_lower for word in ["whatsapp", "call", "message", "video"]):
            mobile_no, name = findContact(query_lower)
            if mobile_no:
                if "message" in query_lower:
                    message = query_lower.replace("send message to", "").replace(name.lower(), "").strip()
                    whatsApp(mobile_no, message, "message", name)
                elif "call" in query_lower:
                    if "video" in query_lower:
                        whatsApp(mobile_no, "", "video", name)
                    else:
                        whatsApp(mobile_no, "", "call", name)
        else:
            chatBot(query_lower)
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(error_msg)
        speak("Something went wrong")
        eel.receiverText("Error: Something went wrong")

@eel.expose
def openCommand(query):
    query = query.replace(ASSISTANT_NAME.lower(), "").replace("open", "").strip()
    if not query:
        eel.receiverText("Please specify an app or website to open")
        return

    try:
        cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (query,))
        results = cursor.fetchall()

        if results:
            speak(f"Opening {query}")
            eel.receiverText(f"Opening {query}")
            os.startfile(results[0][0])
        else:
            cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (query,))
            results = cursor.fetchall()
            if results:
                speak(f"Opening {query}")
                eel.receiverText(f"Opening {query}")
                webbrowser.open(results[0][0])
            else:
                speak(f"Opening {query} failed")
                eel.receiverText(f"Opening {query} failed: not found")
                try:
                    os.system(f'start {query}')
                except:
                    speak("Not found")
                    eel.receiverText("Error: Application or website not found")
    except Exception as e:
        speak("Something went wrong")
        eel.receiverText(f"Error: {str(e)}")

@eel.expose
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    eel.receiverText(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)

@eel.expose
def findContact(query):
    words_to_remove = [ASSISTANT_NAME.lower(), 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        if results:
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('98'):
                mobile_number_str = '98' + mobile_number_str
            eel.receiverText(f"Found contact: {query}")
            return mobile_number_str, query
        else:
            speak("Contact not found")
            eel.receiverText("Contact not found")
            return 0, 0
    except:
        speak("Contact not found")
        eel.receiverText("Error: Contact not found")
        return 0, 0

@eel.expose
def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = f"Message sent successfully to {name}"
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = f"Calling {name}"
    else:
        target_tab = 6
        message = ''
        jarvis_message = f"Starting video call with {name}"

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')
    for _ in range(target_tab):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    
    speak(jarvis_message)
    eel.receiverText(jarvis_message)

@eel.expose
def chatBot(query):
    try:
        chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(query)
        print(response)  # For terminal debugging
        speak(response)
        eel.receiverText(response)  # Send to chat canvas
        return response
    except Exception as e:
        error_msg = f"Error in chatbot: {str(e)}"
        print(error_msg)
        speak("Chatbot error")
        eel.receiverText("Error: Could not process your request")
        return error_msg

@eel.expose
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(
    access_key="jbodRT89r/MZSXW7UTA5lPLwWg730sbk7OJkg6yhsmtyag0YAZ/xvA==",
    keywords=["jarvis", "alexa"]
)

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            
            if keyword_index >= 0:
                print("Hotword detected")
                eel.receiverText("Hotword detected")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
    except Exception as e:
        print(f"Hotword error: {str(e)}")
        eel.receiverText("Error: Hotword detection failed")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

@eel.expose
def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak(f"Calling {name}")
    eel.receiverText(f"Calling {name}")
    command = f'adb shell am start -a android.intent.action.CALL -d tel:{mobileNo}'
    os.system(command)

@eel.expose
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("Sending message")
    eel.receiverText(f"Sending message to {name}")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    tapEvents(136, 2220)
    tapEvents(819, 2192)
    adbInput(mobileNo)
    tapEvents(601, 574)
    tapEvents(390, 2270)
    adbInput(message)
    tapEvents(957, 1397)
    speak(f"Message sent successfully to {name}")
    eel.receiverText(f"Message sent successfully to {name}")