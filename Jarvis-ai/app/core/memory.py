import os
import json
import time
from collections import deque
from math import sqrt
from app.config.settings import settings

class MemoryEngine:
    def __init__(self):
        self.short_term = deque(maxlen=settings.MEMORY_LIMIT)
        self.long_term_file = os.path.join(settings.DATA_DIR, "memory.json")
        self.long_term = self._load_long_term()

    # ----------------------------------------
    # 💾 LOAD / SAVE (PERSISTENCE)
    # ----------------------------------------
    def _load_long_term(self):
        if not os.path.exists(self.long_term_file):
            return []

        try:
            with open(self.long_term_file, "r") as f:
                return json.load(f)
        except:
            return []

    def _save_long_term(self):
        with open(self.long_term_file, "w") as f:
            json.dump(self.long_term[-200:], f, indent=2)

    # ----------------------------------------
    # 🧠 STORE MEMORY
    # ----------------------------------------
    def store(self, query, response):
        if not settings.MEMORY_ENABLED:
            return

        entry = {
            "query": query,
            "response": response,
            "time": time.time()
        }

        # Short-term (fast access)
        self.short_term.append(entry)

        # Long-term (persistent)
        self.long_term.append(entry)
        self._save_long_term()

    # ----------------------------------------
    # 🔍 SIMPLE SEMANTIC MATCH (NO EMBEDDINGS)
    # ----------------------------------------
    def _similarity(self, a, b):
        a_words = set(a.lower().split())
        b_words = set(b.lower().split())

        intersection = len(a_words & b_words)
        union = len(a_words | b_words)

        return intersection / union if union else 0

    # ----------------------------------------
    # 🔎 RETRIEVE RELEVANT MEMORIES
    # ----------------------------------------
    def recall(self, query, limit=5):
        scored = []

        for item in self.long_term:
            score = self._similarity(query, item["query"])
            if score > 0:
                scored.append((score, item))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [item for _, item in scored[:limit]]

    # ----------------------------------------
    # ⚡ GET CONTEXT (RECENT + RELEVANT)
    # ----------------------------------------
    def get_context(self, query):
        recent = list(self.short_term)[-3:]
        relevant = self.recall(query, limit=3)

        combined = recent + relevant

        # Remove duplicates
        seen = set()
        unique = []

        for item in combined:
            key = item["query"]
            if key not in seen:
                unique.append(item)
                seen.add(key)

        return unique

    # ----------------------------------------
    # 🧹 MEMORY CLEANUP
    # ----------------------------------------
    def prune(self):
        # Remove very old memories
        cutoff = time.time() - (7 * 24 * 60 * 60)  # 7 days

        self.long_term = [
            m for m in self.long_term if m["time"] > cutoff
        ]

        self._save_long_term()

    # ----------------------------------------
    # 📊 MEMORY STATS
    # ----------------------------------------
    def stats(self):
        return {
            "short_term": len(self.short_term),
            "long_term": len(self.long_term)
        }

    # ----------------------------------------
    # 🧠 FORMAT FOR AI PROMPT
    # ----------------------------------------
    def format_for_prompt(self, query):
        context = self.get_context(query)

        formatted = "\n".join([
            f"User: {m['query']}\nJarvis: {m['response']}"
            for m in context
        ])

        return formatted if formatted else "No prior context."