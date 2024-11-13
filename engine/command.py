import pyttsx3
import speech_recognition as sr
import eel
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

import pyttsx3
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    
    # Vérifiez les voix disponibles pour sélectionner une voix en français
    voices = engine.getProperty('voices')
    french_voice_found = False
    
    for voice in voices:
        if "fr" in voice.id or "french" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            french_voice_found = True
            break
    
    if not french_voice_found:
        print("Aucune voix en français n'est disponible. Utilisation de la voix par défaut.")
    
    # Configurer la vitesse de lecture
    engine.setProperty('rate', 174)
    
    # Afficher le message dans l'interface via eel
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    print("J'écoutes...")
    eel.DisplayMessage("J'écoutes...")

    # Configuration pour l'enregistrement audio
    fs = 44100  # Fréquence d'échantillonnage
    duration = 6  # Durée d'enregistrement en secondes
    try:
        # Enregistrement audio avec sounddevice
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Attendre la fin de l'enregistrement

        # Sauvegarde dans un fichier temporaire
        wav.write("temp_audio.wav", fs, audio_data)

        # Chargement et reconnaissance vocale avec SpeechRecognition
        with sr.AudioFile("temp_audio.wav") as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)

        print("Analyse en cours...")
        eel.DisplayMessage('Analyse en cours...')
        query = r.recognize_google(audio, language='fr-FR')
        print(f"Vous avez dit : {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query

    except Exception as e:
        print(f"Erreur : {e}")
        return ""

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        query = query.lower().strip()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        if 'ouvre' in query:
            from engine.features import openCommand
            openCommand(query)
        elif "envoie un message" in query or "appel audio" in query or "appel video" in query:
            print(query)
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if contact_no != 0:
                if "envoie un message" in query:
                    message = 'message'
                    speak("Quelle est ton message ?")
                    query = takecommand()
                elif "appel audio" in query:
                    message = 'audio'
                else:
                    message = 'appel video'
                whatsApp(contact_no, query, message, name)
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(f"Erreur d'execution : {e}")

    eel.ShowHood()
