import sys
import signal
from app import create_app, listen, speak
from app.utils.logger import log_info, log_error, log_command
from app.config.settings import settings

class JarvisRuntime:
    def __init__(self):
        self.jarvis = create_app()
        self.running = True
        self.mode = "voice" if settings.VOICE_ENABLED else "text"

    # ----------------------------------------
    # 🚀 START SYSTEM
    # ----------------------------------------
    def start(self):
        log_info("Jarvis runtime starting", mode=self.mode)

        self._setup_signal_handlers()

        if self.mode == "voice":
            self._run_voice_mode()
        else:
            self._run_text_mode()

    # ----------------------------------------
    # 🎤 VOICE MODE
    # ----------------------------------------
    def _run_voice_mode(self):
        speak("Jarvis is online.")

        while self.running:
            try:
                query = listen()

                if not query:
                    continue

                response = self._process(query)
                speak(response)

            except Exception as e:
                log_error("Voice loop error", error=str(e))

    # ----------------------------------------
    # 💻 TEXT MODE
    # ----------------------------------------
    def _run_text_mode(self):
        print("Jarvis (text mode) is online.")

        while self.running:
            try:
                query = input("You: ").strip()

                if not query:
                    continue

                response = self._process(query)
                print("Jarvis:", response)

            except Exception as e:
                log_error("Text loop error", error=str(e))

    # ----------------------------------------
    # 🧠 PROCESS INPUT
    # ----------------------------------------
    def _process(self, query):
        log_info("Processing query", query=query)

        # Exit commands
        if query.lower() in ["exit", "quit", "shutdown"]:
            self.shutdown()
            return "Shutting down Jarvis"

        # Core execution
        response = self.jarvis.process(query)

        # Log command
        log_command(query, response)

        return response

    # ----------------------------------------
    # ⛔ SHUTDOWN SYSTEM
    # ----------------------------------------
    def shutdown(self):
        log_info("Shutting down Jarvis")
        self.running = False
        sys.exit(0)

    # ----------------------------------------
    # 🔄 RESTART SYSTEM
    # ----------------------------------------
    def restart(self):
        log_info("Restarting Jarvis")
        self.shutdown()

    # ----------------------------------------
    # ⚠️ SIGNAL HANDLING (CTRL+C SAFE EXIT)
    # ----------------------------------------
    def _setup_signal_handlers(self):
        def handle_signal(sig, frame):
            log_info("Interrupt received, shutting down")
            self.shutdown()

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)


# ----------------------------------------
# 🚀 ENTRY FUNCTION
# ----------------------------------------
def run_assistant():
    runtime = JarvisRuntime()
    runtime.start()


# ----------------------------------------
# ▶️ DIRECT EXECUTION
# ----------------------------------------
if __name__ == "__main__":
    run_assistant()