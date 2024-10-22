import struct
import time
import pvporcupine
import pyaudio
import pyautogui as autogui

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