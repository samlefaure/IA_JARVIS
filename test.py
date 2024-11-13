# import struct
# import time
# import pvporcupine
# import pyaudio
# import pyautogui as autogui

# def hotword():
#     porcupine = None
#     paud = None
#     audio_stream = None
#     try:
#         print("Initialisation de Porcupine...")
#         porcupine = pvporcupine.create(access_key='4jqFk8dI8SvWHK8t8LXuo9m5Wieae3ZP/3IIstMpl4X1BRQSI+dcFQ==', keywords=["alexa", "jarvis"]) 
#         print("Porcupine initialisé.")
        
#         paud = pyaudio.PyAudio()
#         audio_stream = paud.open(rate=porcupine.sample_rate,
#                                  channels=1,
#                                  format=pyaudio.paInt16,
#                                  input=True,
#                                  frames_per_buffer=porcupine.frame_length)
#         print("Stream audio ouvert.")

#         print("Prêt à détecter les mots clés. Parlez maintenant...")
#         while True:
#             audio_frame = audio_stream.read(porcupine.frame_length)
#             audio_frame = struct.unpack_from("h" * porcupine.frame_length, audio_frame)

#             keyword_index = porcupine.process(audio_frame)

#             if keyword_index >= 0:
#                 print("Mot clé détecté")
#                 autogui.keyDown("win")
#                 autogui.press("j")
#                 time.sleep(2)
#                 autogui.keyUp("win")
#             else:
#                 print("Aucun mot clé détecté.")

#     except Exception as e:
#         print(f"Erreur : {e}")
#     finally:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()

# # Appeler la fonction hotword
# if __name__ == "__main__":
#     hotword()
import struct
import time
import pyautogui
import sounddevice as sd
import pvporcupine

def hotword():
    porcupine = None
    try:
        # Crée une instance de Porcupine pour la détection de mots-clés
        porcupine = pvporcupine.create(
            access_key='4jqFk8dI8SvWHK8t8LXuo9m5Wieae3ZP/3IIstMpl4X1BRQSI+dcFQ==',
            keywords=["alexa", "hey siri", "jarvis"]
        )

        # Variable pour éviter plusieurs appels à hotkey dans un court laps de temps
        last_triggered = time.time()

        # Fonction de callback pour traiter les données audio
        def audio_callback(indata, frames, time, status):
            if status:
                print(status)

            pcm = struct.unpack_from("h" * porcupine.frame_length, indata)
            keyword_index = porcupine.process(pcm)

            # Détecte un mot-clé
            if keyword_index >= 0:
                current_time = time.time()
                
                # Seuil pour éviter d'exécuter plusieurs fois en peu de temps
                if current_time - last_triggered > 2:
                    print("Mot clé détecté")
                    pyautogui.hotkey("win", "j")
                    last_triggered = current_time  # Mettre à jour le temps du dernier déclenchement

        # Démarre le flux audio
        with sd.InputStream(channels=1, samplerate=porcupine.sample_rate, callback=audio_callback):
            while True:
                time.sleep(1)  # Juste pour garder le programme en vie

    except Exception as e:
        print("Erreur : ", e)
    finally:
        if porcupine is not None:
            porcupine.delete()


hotword()