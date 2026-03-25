import time
from app.automation.system import SystemKernel
from app.automation.web import WebEngine
from app.config.settings import settings
from app.nlp.openai_client import ask_ai

class Jarvis:
    def __init__(self):
        self.system = SystemKernel()
        self.web = WebEngine()
        self.memory = []
        self.context = {}
        self.active = True

    # ----------------------------------------
    # 🧠 MEMORY ENGINE
    # ----------------------------------------
    def remember(self, query, response):
        if not settings.MEMORY_ENABLED:
            return

        self.memory.append({
            "query": query,
            "response": response,
            "time": time.time()
        })

        # Limit memory
        if len(self.memory) > settings.MEMORY_LIMIT:
            self.memory.pop(0)

    def get_context(self):
        return self.memory[-5:] if self.memory else []

    # ----------------------------------------
    # 🧠 INTENT CLASSIFICATION (CORE AI ROUTER)
    # ----------------------------------------
    def classify_intent(self, query):
        q = query.lower()

        system_keywords = ["open", "close", "restart", "volume", "battery", "status", "run"]
        web_keywords = ["search", "youtube", "google", "website", "find"]

        if any(word in q for word in system_keywords):
            return "system"

        if any(word in q for word in web_keywords):
            return "web"

        return "ai"

    # ----------------------------------------
    # 🤖 AI DECISION ENGINE (SMART ROUTING)
    # ----------------------------------------
    def ai_route(self, query):
        if not settings.ENABLE_AI_ROUTING:
            return "ai"

        prompt = f"""
        You are an AI router.
        Classify this command into one of:
        - system (OS control)
        - web (internet tasks)
        - ai (general question)

        Command: "{query}"
        Answer only: system / web / ai
        """

        try:
            decision = ask_ai(prompt).lower()

            if "system" in decision:
                return "system"
            elif "web" in decision:
                return "web"
        except:
            pass

        return "ai"

    # ----------------------------------------
    # ⚙️ TASK EXECUTION LAYER
    # ----------------------------------------
    def execute(self, query):
        # Step 1: rule-based quick routing
        intent = self.classify_intent(query)

        # Step 2: AI override (god-level)
        if settings.ENABLE_AI_ROUTING:
            intent = self.ai_route(query)

        # Step 3: execution
        if intent == "system" and settings.ENABLE_SYSTEM_CONTROL:
            return self.system.handle(query)

        elif intent == "web":
            return self.web.handle(query)

        else:
            return self.ask_ai_with_context(query)

    # ----------------------------------------
    # 🧠 CONTEXTUAL AI RESPONSE
    # ----------------------------------------
    def ask_ai_with_context(self, query):
        context = self.get_context()

        history_text = "\n".join(
            [f"User: {m['query']}\nJarvis: {m['response']}" for m in context]
        )

        prompt = f"""
        You are Jarvis, an advanced AI assistant.

        Conversation history:
        {history_text}

        User: {query}
        Jarvis:
        """

        return ask_ai(prompt)

    # ----------------------------------------
    # 🧬 MULTI-STEP REASONING (AGENT MODE)
    # ----------------------------------------
    def plan_and_execute(self, query):
        prompt = f"""
        Break this task into steps:
        "{query}"

        Respond as numbered steps.
        """

        plan = ask_ai(prompt)

        steps = [line for line in plan.split("\n") if line.strip()]

        results = []
        for step in steps:
            result = self.execute(step)
            results.append(result)

        return " | ".join(results)

    # ----------------------------------------
    # 🧠 MASTER CONTROL LOOP
    # ----------------------------------------
    def process(self, query):
        if not query:
            return ""

        # Exit condition
        if "exit" in query or "shutdown" in query:
            self.active = False
            return "Shutting down Jarvis"

        # Multi-step intelligent execution
        if " and " in query or "then" in query:
            response = self.plan_and_execute(query)
        else:
            response = self.execute(query)

        # Store memory
        self.remember(query, response)

        return response

    # ----------------------------------------
    # 🚀 START LOOP (VOICE / TEXT)
    # ----------------------------------------
    def start(self, input_fn=None, output_fn=None):
        print("Jarvis is online.")

        while self.active:
            query = input_fn() if input_fn else input("You: ")

            response = self.process(query)

            if output_fn:
                output_fn(response)
            else:
                print("Jarvis:", response)