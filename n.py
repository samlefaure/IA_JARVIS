import os
# from pipes import quote
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
# from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("db.db")
cursor = con.cursor()
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contact WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
        print(mobile_number_str)
    except:
        print('not exist in contacts')
        return 0, 0

findContact("Pablo")