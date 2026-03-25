import speech_recognition as sr
import time
from app.config.settings import settings
from app.utils.helpers import debounce, normalize_text
from app.utils.logger import log_info, log_error

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.energy_threshold = 300
        self.pause_threshold = 0.8
        self.last_input_time = 0

        self._configure()

    # ----------------------------------------
    # ⚙️ INITIAL SETUP
    # ----------------------------------------
    def _configure(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.pause_threshold = self.pause_threshold

        log_info("Voice listener initialized")

    # ----------------------------------------
    # 🎤 LISTEN ONCE
    # ----------------------------------------
    def listen_once(self, timeout=5, phrase_time_limit=7):
        with self.microphone as source:
            log_info("Listening...")

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                query = self.recognizer.recognize_google(audio)
                query = normalize_text(query)

                log_info("Voice input received", query=query)
                return query

            except sr.WaitTimeoutError:
                return ""

            except sr.UnknownValueError:
                log_error("Speech not understood")
                return ""

            except sr.RequestError as e:
                log_error("Speech API error", error=str(e))
                return ""

    # ----------------------------------------
    # 🔄 RETRY LISTEN (SMART)
    # ----------------------------------------
    def listen_with_retry(self, retries=2):
        for _ in range(retries + 1):
            result = self.listen_once()
            if result:
                return result
        return ""

    # ----------------------------------------
    # 🧠 WAKE WORD DETECTION (BASIC)
    # ----------------------------------------
    def detect_wake_word(self, text, wake_word="jarvis"):
        return wake_word in text.lower()

    # ----------------------------------------
    # ⚡ CONTINUOUS LISTEN MODE
    # ----------------------------------------
    def continuous_listen(self, callback):
        log_info("Continuous listening started")

        while True:
            query = self.listen_once()

            if not query:
                continue

            # Optional wake word filter
            if self.detect_wake_word(query):
                clean_query = query.replace("jarvis", "").strip()
                callback(clean_query)

    # ----------------------------------------
    # 🔇 DEBOUNCED INPUT (AVOID DUPLICATES)
    # ----------------------------------------
    @debounce(wait=1.0)
    def listen_debounced(self):
        return self.listen_once()


# ----------------------------------------
# 🚀 GLOBAL INSTANCE
# ----------------------------------------
listener = VoiceListener()


# ----------------------------------------
# 🎯 SIMPLE FUNCTION (FOR ASSISTANT)
# ----------------------------------------
def listen():
    return listener.listen_with_retry()