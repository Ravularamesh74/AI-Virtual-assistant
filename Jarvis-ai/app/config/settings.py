import os
from dotenv import load_dotenv
from functools import lru_cache

# ----------------------------------------
# 🔐 LOAD ENVIRONMENT
# ----------------------------------------
load_dotenv()

class Settings:
    def __init__(self):
        # -----------------------------
        # 🔑 API CONFIG
        # -----------------------------
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # -----------------------------
        # 🧠 AI BEHAVIOR SETTINGS
        # -----------------------------
        self.AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", 0.7))
        self.AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", 500))

        # -----------------------------
        # 🎤 VOICE SETTINGS
        # -----------------------------
        self.VOICE_ENABLED = self._to_bool(os.getenv("VOICE_ENABLED", "true"))
        self.VOICE_RATE = int(os.getenv("VOICE_RATE", 180))
        self.VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", 1.0))

        # -----------------------------
        # 🌐 WEB ENGINE SETTINGS
        # -----------------------------
        self.DEFAULT_SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "google")
        self.MAX_WEB_RESULTS = int(os.getenv("MAX_WEB_RESULTS", 3))
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 5))

        # -----------------------------
        # 💻 SYSTEM AUTOMATION SETTINGS
        # -----------------------------
        self.ENABLE_SYSTEM_CONTROL = self._to_bool(os.getenv("ENABLE_SYSTEM_CONTROL", "true"))
        self.ALLOW_TERMINAL = self._to_bool(os.getenv("ALLOW_TERMINAL", "false"))
        self.MAX_PARALLEL_TASKS = int(os.getenv("MAX_PARALLEL_TASKS", 5))

        # -----------------------------
        # 🧠 MEMORY SETTINGS
        # -----------------------------
        self.MEMORY_ENABLED = self._to_bool(os.getenv("MEMORY_ENABLED", "true"))
        self.MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", 50))

        # -----------------------------
        # 🔥 FEATURE FLAGS (GOD MODE)
        # -----------------------------
        self.ENABLE_AI_ROUTING = self._to_bool(os.getenv("ENABLE_AI_ROUTING", "true"))
        self.ENABLE_BACKGROUND_TASKS = self._to_bool(os.getenv("ENABLE_BACKGROUND_TASKS", "true"))
        self.ENABLE_PARALLEL_EXECUTION = self._to_bool(os.getenv("ENABLE_PARALLEL_EXECUTION", "true"))

        # -----------------------------
        # 🛠️ DEBUG / DEV SETTINGS
        # -----------------------------
        self.DEBUG = self._to_bool(os.getenv("DEBUG", "true"))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # -----------------------------
        # 📂 PATH SETTINGS
        # -----------------------------
        self.BASE_DIR = os.getcwd()
        self.LOG_DIR = os.path.join(self.BASE_DIR, "logs")
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")

        self._ensure_directories()

    # ----------------------------------------
    # 🔄 UTILS
    # ----------------------------------------
    def _to_bool(self, value):
        return str(value).lower() in ["true", "1", "yes"]

    def _ensure_directories(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(self.DATA_DIR, exist_ok=True)

    # ----------------------------------------
    # 🔁 DYNAMIC RELOAD (HOT CONFIG)
    # ----------------------------------------
    def reload(self):
        load_dotenv(override=True)
        self.__init__()

    # ----------------------------------------
    # 📊 SUMMARY (DEBUG VIEW)
    # ----------------------------------------
    def summary(self):
        return {
            "AI_MODEL": self.OPENAI_MODEL,
            "VOICE": self.VOICE_ENABLED,
            "SYSTEM_CONTROL": self.ENABLE_SYSTEM_CONTROL,
            "MEMORY": self.MEMORY_ENABLED,
            "DEBUG": self.DEBUG
        }


# ----------------------------------------
# ⚡ SINGLETON (GLOBAL SETTINGS INSTANCE)
# ----------------------------------------
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()