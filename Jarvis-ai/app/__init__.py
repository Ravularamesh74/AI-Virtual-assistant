from app.core.assistant import Jarvis
from app.voice.listen import listen
from app.voice.speak import speak

def create_app():
    return Jarvis()
