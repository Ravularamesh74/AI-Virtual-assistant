import re
from app.automation.system import SystemKernel
from app.automation.web import WebEngine
from app.config.settings import settings
from app.nlp.openai_client import ask_ai

class CommandCenter:
    def __init__(self):
        self.system = SystemKernel()
        self.web = WebEngine()
        self.plugins = {}
        self.history = []

    # ----------------------------------------
    # 🔌 PLUGIN REGISTRATION SYSTEM
    # ----------------------------------------
    def register(self, name, func):
        self.plugins[name] = func

    # ----------------------------------------
    # 🧠 PREPROCESSING (CLEAN INPUT)
    # ----------------------------------------
    def preprocess(self, query):
        query = query.lower().strip()

        # remove filler words
        query = re.sub(r"(please|can you|could you|jarvis)", "", query)

        return query.strip()

    # ----------------------------------------
    # 🧠 PRIORITY ROUTER
    # ----------------------------------------
    def detect_intent(self, query):
        system_patterns = r"(open|close|restart|volume|battery|status|run)"
        web_patterns = r"(search|youtube|google|find|website)"

        if re.search(system_patterns, query):
            return "system"

        if re.search(web_patterns, query):
            return "web"

        return "ai"

    # ----------------------------------------
    # 🤖 AI ROUTER (SMART OVERRIDE)
    # ----------------------------------------
    def ai_router(self, query):
        if not settings.ENABLE_AI_ROUTING:
            return None

        prompt = f"""
        Classify this command into:
        system / web / ai

        Command: {query}
        """

        try:
            decision = ask_ai(prompt).lower()

            if "system" in decision:
                return "system"
            elif "web" in decision:
                return "web"
        except:
            pass

        return None

    # ----------------------------------------
    # ⚙️ EXECUTION LAYER
    # ----------------------------------------
    def execute(self, query):
        query = self.preprocess(query)

        # Step 1: Plugin check (highest priority)
        for name, func in self.plugins.items():
            if name in query:
                return func(query)

        # Step 2: Rule-based intent
        intent = self.detect_intent(query)

        # Step 3: AI override (god mode)
        ai_intent = self.ai_router(query)
        if ai_intent:
            intent = ai_intent

        # Step 4: Execution
        if intent == "system" and settings.ENABLE_SYSTEM_CONTROL:
            return self.system.handle(query)

        elif intent == "web":
            return self.web.handle(query)

        else:
            return self.ask_ai(query)

    # ----------------------------------------
    # 🧠 AI FALLBACK
    # ----------------------------------------
    def ask_ai(self, query):
        return ask_ai(f"You are Jarvis. Answer: {query}")

    # ----------------------------------------
    # 🧬 MULTI-COMMAND SUPPORT
    # ----------------------------------------
    def split_commands(self, query):
        separators = [" and ", " then ", ","]
        for sep in separators:
            if sep in query:
                return [q.strip() for q in query.split(sep)]
        return [query]

    # ----------------------------------------
    # ⚡ PARALLEL / SEQUENTIAL EXECUTION
    # ----------------------------------------
    def handle(self, query):
        commands = self.split_commands(query)

        results = []
        for cmd in commands:
            result = self.execute(cmd)
            results.append(result)

        final = " | ".join(results)

        self.history.append({
            "query": query,
            "response": final
        })

        return final


# ----------------------------------------
# 🚀 GLOBAL INSTANCE
# ----------------------------------------
command_center = CommandCenter()


# ----------------------------------------
# 🎯 DEFAULT COMMAND ENTRY FUNCTION
# ----------------------------------------
def execute_command(query):
    return command_center.handle(query)