import re
import time
import functools
import traceback
from difflib import get_close_matches

# ----------------------------------------
# 🧠 TEXT NORMALIZATION
# ----------------------------------------
def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


# ----------------------------------------
# 🔍 FUZZY MATCH
# ----------------------------------------
def fuzzy_match(query, choices, cutoff=0.6):
    matches = get_close_matches(query, choices, n=1, cutoff=cutoff)
    return matches[0] if matches else None


# ----------------------------------------
# 🧩 COMMAND SPLITTER
# ----------------------------------------
def split_commands(query):
    separators = [" and ", " then ", ","]
    for sep in separators:
        if sep in query:
            return [q.strip() for q in query.split(sep)]
    return [query]


# ----------------------------------------
# 🧠 KEYWORD EXTRACTOR (LIGHT NLP)
# ----------------------------------------
def extract_keywords(text):
    words = normalize_text(text).split()
    stopwords = {"the", "is", "at", "which", "on", "a", "an", "please"}
    return [w for w in words if w not in stopwords]


# ----------------------------------------
# ⏱️ TIMER DECORATOR (PERFORMANCE)
# ----------------------------------------
def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIME] {func.__name__}: {round(end - start, 3)}s")
        return result
    return wrapper


# ----------------------------------------
# 🔁 RETRY DECORATOR
# ----------------------------------------
def retry(retries=2, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator


# ----------------------------------------
# 🔐 SAFE EXECUTION WRAPPER
# ----------------------------------------
def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return f"Error: {str(e)}"


# ----------------------------------------
# 🧠 CONFIDENCE CALCULATOR
# ----------------------------------------
def confidence_score(matches, total):
    if total == 0:
        return 0
    return round(matches / total, 2)


# ----------------------------------------
# 📊 FORMAT RESPONSE (CLEAN OUTPUT)
# ----------------------------------------
def format_response(text, limit=300):
    text = str(text).strip()
    if len(text) > limit:
        return text[:limit] + "..."
    return text


# ----------------------------------------
# 🧬 MEMORY FORMATTER
# ----------------------------------------
def format_memory(entries):
    return "\n".join([
        f"User: {e['query']}\nJarvis: {e['response']}"
        for e in entries
    ])


# ----------------------------------------
# 🧠 SIMPLE INTENT HINT
# ----------------------------------------
def guess_intent(query):
    q = normalize_text(query)

    if any(x in q for x in ["open", "close", "restart"]):
        return "system"

    if any(x in q for x in ["search", "youtube", "google"]):
        return "web"

    return "ai"


# ----------------------------------------
# 🔄 DEBOUNCE (FOR VOICE INPUT)
# ----------------------------------------
def debounce(wait=0.5):
    def decorator(func):
        last_call = [0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_call[0] > wait:
                last_call[0] = now
                return func(*args, **kwargs)

        return wrapper
    return decorator


# ----------------------------------------
# 📦 TRACEBACK LOGGER
# ----------------------------------------
def get_traceback():
    return traceback.format_exc()