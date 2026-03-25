import webbrowser
import requests
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import quote
from difflib import get_close_matches

class WebEngine:
    def __init__(self):
        self.search_engines = {
            "google": "https://www.google.com/search?q={}",
            "youtube": "https://www.youtube.com/results?search_query={}",
            "maps": "https://www.google.com/maps/search/{}"
        }

    # ----------------------------------------
    # 🔎 SMART SEARCH ENGINE
    # ----------------------------------------
    def search(self, query, platform="google"):
        platform = platform.lower()

        if platform not in self.search_engines:
            platform = "google"

        url = self.search_engines[platform].format(quote(query))
        webbrowser.open(url)

        return f"Searching {query} on {platform}"

    # ----------------------------------------
    # 🎯 INTENT-BASED SEARCH ROUTING
    # ----------------------------------------
    def smart_search(self, query):
        q = query.lower()

        if "youtube" in q or "video" in q:
            return self.search(q.replace("youtube", "").strip(), "youtube")

        elif "map" in q or "location" in q:
            return self.search(q.replace("map", "").strip(), "maps")

        return self.search(q, "google")

    # ----------------------------------------
    # 🌐 OPEN WEBSITE DIRECTLY
    # ----------------------------------------
    def open_website(self, site):
        if not site.startswith("http"):
            site = f"https://{site}.com"

        webbrowser.open(site)
        return f"Opening {site}"

    # ----------------------------------------
    # 🧠 FETCH WEB DATA (SCRAPING)
    # ----------------------------------------
    def fetch_data(self, url):
        try:
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")

            title = soup.title.string if soup.title else "No title"
            paragraphs = [p.text for p in soup.find_all("p")[:3]]

            return {
                "title": title,
                "content": paragraphs
            }

        except Exception as e:
            return {"error": str(e)}

    # ----------------------------------------
    # 🤖 AUTO EXTRACT INFO FROM SEARCH
    # ----------------------------------------
    def quick_answer(self, query):
        url = f"https://www.google.com/search?q={quote(query)}"
        data = self.fetch_data(url)

        if "error" in data:
            return "Failed to fetch data"

        return f"{data['title']} - {data['content'][:2]}"

    # ----------------------------------------
    # ⚡ MULTI-TAB EXECUTION
    # ----------------------------------------
    async def open_multiple(self, queries):
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, self.smart_search, q) for q in queries]
        results = await asyncio.gather(*tasks)
        return results

    # ----------------------------------------
    # 🧠 COMMAND PARSER
    # ----------------------------------------
    def parse(self, query):
        q = query.lower()

        if "search" in q:
            return ("search", q.replace("search", "").strip())

        elif "open" in q:
            return ("open", q.replace("open", "").strip())

        elif "find" in q:
            return ("answer", q.replace("find", "").strip())

        elif "youtube" in q:
            return ("youtube", q.replace("youtube", "").strip())

        return ("search", q)

    # ----------------------------------------
    # ⚙️ EXECUTION ENGINE
    # ----------------------------------------
    def execute(self, query):
        action, value = self.parse(query)

        if action == "search":
            return self.smart_search(value)

        elif action == "open":
            return self.open_website(value)

        elif action == "youtube":
            return self.search(value, "youtube")

        elif action == "answer":
            return self.quick_answer(value)

        return "Web command not recognized"

    # ----------------------------------------
    # 🧠 MASTER HANDLER
    # ----------------------------------------
    def handle(self, query):
        if " and " in query:
            parts = query.split(" and ")
            results = asyncio.run(self.open_multiple(parts))
            return " | ".join(results)

        return self.execute(query)