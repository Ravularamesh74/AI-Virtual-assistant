import pyttsx3
import threading
import queue
import time
from app.config.settings import settings
from app.utils.helpers import format_response
from app.utils.logger import log_info, log_error

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        self.is_speaking = False
        self._configure()
        self._start_worker()

    # ----------------------------------------
    # ⚙️ CONFIGURE VOICE ENGINE
    # ----------------------------------------
    def _configure(self):
        self.engine.setProperty("rate", settings.VOICE_RATE)
        self.engine.setProperty("volume", settings.VOICE_VOLUME)

        voices = self.engine.getProperty("voices")

        # Select best available voice (female preferred fallback)
        if voices:
            self.engine.setProperty("voice", voices[0].id)

        log_info("Voice engine initialized")

    # ----------------------------------------
    # 🔊 SPEAK (QUEUE BASED - NON BLOCKING)
    # ----------------------------------------
    def speak(self, text):
        if not settings.VOICE_ENABLED:
            return

        text = format_response(text, limit=500)
        self.queue.put(text)

    # ----------------------------------------
    # 🧠 BACKGROUND WORKER (ASYNC SPEECH)
    # ----------------------------------------
    def _worker(self):
        while True:
            text = self.queue.get()

            if text is None:
                break

            try:
                self.is_speaking = True
                log_info("Speaking", text=text)

                self.engine.say(text)
                self.engine.runAndWait()

            except Exception as e:
                log_error("Speech error", error=str(e))

            finally:
                self.is_speaking = False
                self.queue.task_done()

    def _start_worker(self):
        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    # ----------------------------------------
    # ⛔ STOP CURRENT SPEECH
    # ----------------------------------------
    def stop(self):
        try:
            self.engine.stop()
            self._clear_queue()
            log_info("Speech stopped")
        except Exception as e:
            log_error("Stop failed", error=str(e))

    def _clear_queue(self):
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except:
                pass

    # ----------------------------------------
    # ⚡ PRIORITY SPEAK (INTERRUPT CURRENT)
    # ----------------------------------------
    def speak_priority(self, text):
        self.stop()
        self.speak(text)

    # ----------------------------------------
    # 🧠 SMART FORMAT (AI → HUMAN SPEECH)
    # ----------------------------------------
    def clean_text(self, text):
        # Remove code-like or symbols
        text = text.replace("\n", ". ")
        text = text.replace(":", "")
        text = text.replace("  ", " ")
        return text.strip()

    # ----------------------------------------
    # 🎭 EXPRESSIVE SPEECH (SIMULATED)
    # ----------------------------------------
    def speak_expressive(self, text, mode="normal"):
        if mode == "fast":
            self.engine.setProperty("rate", settings.VOICE_RATE + 40)
        elif mode == "slow":
            self.engine.setProperty("rate", settings.VOICE_RATE - 40)
        else:
            self.engine.setProperty("rate", settings.VOICE_RATE)

        self.speak(self.clean_text(text))

    # ----------------------------------------
    # 🔁 WAIT UNTIL DONE
    # ----------------------------------------
    def wait(self):
        self.queue.join()


# ----------------------------------------
# 🚀 GLOBAL INSTANCE
# ----------------------------------------
voice_engine = VoiceEngine()


# ----------------------------------------
# 🎯 SIMPLE FUNCTION (FOR ASSISTANT)
# ----------------------------------------
def speak(text):
    voice_engine.speak(text)