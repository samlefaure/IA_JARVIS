import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
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
        # eel.ShowHood()
        time.sleep(2)
        return query
       
    except Exception as e:
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
        

        if 'ouvre' in  query:
            from engine.features import openCommand
            openCommand(query)
        # elif 'youtube':
        #     from engine.features import PlayYoutube
        #     PlayYoutube(query)
        elif "envoie un message" in query or "appel audio" in query or "appel video" in query:
            print(query)
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

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
    except:
        print("Erreur d'execution")

    eel.ShowHood()
    # findContact('Pablo')
