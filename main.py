import os
import eel
from engine.features import *
from engine.command import *

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        
        speak("Salut, en quoi puis-je vous aider ?")
        eel.hideStart()
        playAssistantSound()

    os.system('start chrome --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)