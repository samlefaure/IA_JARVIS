import os
from pipes import quote
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
# from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

ASSISTANT_NAME = "machido"
# playiong assistant sound when onclick on mic button
@eel.expose

# play assistant sound function
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    query = query[5:]
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Ouverture de "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Ouverture de "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Ouverture de "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("Non trouvé")
        except:
            speak("Il y a un probléme")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Je joue {search_term} sur YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine = pvporcupine.create(access_key='4jqFk8dI8SvWHK8t8LXuo9m5Wieae3ZP/3IIstMpl4X1BRQSI+dcFQ==', keywords=["alexa", "hey siri"]) 
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("mot clé détecté")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

hotword()

# Whatsapp Message Sending
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'envoie', 'un', 'à', 'téléphonique', 'appel', ' ', 'message', 'wahtsapp', 'audio']
    query = remove_words(query, words_to_remove)
    print(query)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacte WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+228'):
            mobile_number_str = '+228' + mobile_number_str

        return mobile_number_str, query
    except:
        speak("ce contact n'existe pas")
        return 0, 0

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 13
        jarvis_message = "message bien envoyé à "+name

    elif flag == 'audio':
        target_tab = 8
        message = ''
        jarvis_message = "appel à "+name

    else:
        target_tab = 7
        message = ''
        jarvis_message = "Vous etes en video avec "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation

# def makeCall(name, mobileNo):
#     mobileNo =mobileNo.replace(" ", "")
#     speak("Calling "+name)
#     command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
#     os.system(command)


# # to send message
# def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)