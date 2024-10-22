import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("J'écoutes...")
        eel.DisplayMessage("J'écoutes...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:      
        print("Analyse en cours...")
        eel.DisplayMessage('Analyse en cours...')
        query = r.recognize_google(audio, language='fr-FR')
        print(f"Vous avez dit : {query}")
        eel.DisplayMessage(query)
        speak(query)
        eel.ShowHood()
        time.sleep(2)
        return query
       
    except Exception as e:
        return ""


@eel.expose
def allCommands():
    # Nettoyer la requête (query)
    query = takecommand()
    query = query.lower().strip()

    # print(f"Requête nettoyée : {query}")

    # Vérifier si "ouvrir" est dans query
    # if 'salut' in query:
    #     print("La condition 'ouvrir' est vraie.")
    # else:
    #     print("Pas d'ouverture.")

    if 'ouvrir' in  query:
        from engine.features import openCommand
        openCommand(query)
    else:
        print("Pas d'ouverture")
