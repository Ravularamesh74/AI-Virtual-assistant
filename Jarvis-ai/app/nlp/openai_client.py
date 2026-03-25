import time
import hashlib
from functools import lru_cache
from openai import OpenAI
from app.config.settings import settings

# ----------------------------------------
# 🔑 INIT CLIENT (MODERN SDK)
# ----------------------------------------
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# ----------------------------------------
# ⚡ SIMPLE CACHE (AVOID REPEATED CALLS)
# ----------------------------------------
def _cache_key(prompt):
    return hashlib.md5(prompt.encode()).hexdigest()


_cache_store = {}


def _get_cached(prompt):
    key = _cache_key(prompt)
    return _cache_store.get(key)


def _set_cache(prompt, response):
    key = _cache_key(prompt)
    _cache_store[key] = response


# ----------------------------------------
# 🔁 RETRY MECHANISM
# ----------------------------------------
def _retry(func, retries=2, delay=1):
    for attempt in range(retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == retries:
                return f"AI Error: {str(e)}"
            time.sleep(delay)


# ----------------------------------------
# 🧠 CORE CHAT FUNCTION
# ----------------------------------------
def chat(prompt, system_prompt=None):
    cached = _get_cached(prompt)
    if cached:
        return cached

    def _call():
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=settings.AI_TEMPERATURE,
            max_tokens=settings.AI_MAX_TOKENS,
        )

        return response.choices[0].message.content.strip()

    result = _retry(_call)
    _set_cache(prompt, result)

    return result


# ----------------------------------------
# 🤖 GENERAL AI (DEFAULT ENTRY)
# ----------------------------------------
def ask_ai(prompt):
    system_prompt = "You are Jarvis, an intelligent AI assistant."
    return chat(prompt, system_prompt)


# ----------------------------------------
# 🧠 INTENT / ROUTING AI
# ----------------------------------------
def classify_intent(prompt):
    system_prompt = """
    You are an AI intent classifier.
    Output ONLY one word:
    system / web / ai
    """
    return chat(prompt, system_prompt).lower()


# ----------------------------------------
# 🧬 TASK PLANNER (AGENT MODE)
# ----------------------------------------
def plan_task(goal):
    system_prompt = """
    Break the user goal into clear step-by-step actions.
    Return only numbered steps.
    """

    return chat(goal, system_prompt)


# ----------------------------------------
# ⚡ SUMMARIZER
# ----------------------------------------
def summarize(text):
    system_prompt = "Summarize the following text concisely."
    return chat(text, system_prompt)


# ----------------------------------------
# 🧠 CONTEXTUAL RESPONSE (WITH MEMORY)
# ----------------------------------------
def ask_with_context(query, context):
    prompt = f"""
    You are Jarvis.

    Context:
    {context}

    User: {query}
    Jarvis:
    """
    return chat(prompt)


# ----------------------------------------
# 🔧 TOOL-CALL READY (FUTURE AGENTS)
# ----------------------------------------
def ask_with_tools(prompt, tools=None):
    """
    Placeholder for future function calling / agent tools
    """
    system_prompt = "You can use tools if needed."
    return chat(prompt, system_prompt)


# ----------------------------------------
# 📊 DEBUG INFO
# ----------------------------------------
def debug_info():
    return {
        "model": settings.OPENAI_MODEL,
        "temperature": settings.AI_TEMPERATURE,
        "cache_size": len(_cache_store)
    }