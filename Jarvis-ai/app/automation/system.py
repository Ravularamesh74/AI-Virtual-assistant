import os
import subprocess
import psutil
import asyncio
import platform
import time
from difflib import get_close_matches
from threading import Thread

class SystemKernel:
    def __init__(self):
        self.os_name = platform.system().lower()
        self.apps = self._discover_apps()
        self.memory = []
        self.background_tasks = []

    # ---------------------------------------
    # 🔍 SMART APP DISCOVERY (AUTO LEARNING)
    # ---------------------------------------
    def _discover_apps(self):
        known = {
            "chrome": "chrome",
            "edge": "msedge",
            "notepad": "notepad",
            "calculator": "calc",
            "vscode": "code"
        }
        return known

    # ---------------------------------------
    # 🧠 CONTEXT MEMORY (SELF LEARNING BASE)
    # ---------------------------------------
    def remember(self, command, result):
        self.memory.append({
            "command": command,
            "result": result,
            "time": time.time()
        })

    # ---------------------------------------
    # 🔥 MULTI-COMMAND PARSER
    # ---------------------------------------
    def parse_commands(self, query):
        separators = [" and ", " then ", ","]
        commands = [query]

        for sep in separators:
            if sep in query:
                commands = query.split(sep)
                break

        return [cmd.strip() for cmd in commands]

    # ---------------------------------------
    # 🚀 OPEN APP
    # ---------------------------------------
    def open_app(self, name):
        match = get_close_matches(name, self.apps.keys(), n=1, cutoff=0.5)

        if match:
            app = self.apps[match[0]]
            try:
                subprocess.Popen(app)
                return f"{match[0]} opened"
            except:
                return f"failed to open {name}"

        return f"{name} not found"

    # ---------------------------------------
    # ❌ CLOSE APP (SMART)
    # ---------------------------------------
    def close_app(self, name):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    psutil.Process(proc.info['pid']).terminate()
                    return f"{name} closed"
            except:
                pass

        return f"{name} not running"

    # ---------------------------------------
    # 🔄 RESTART APP
    # ---------------------------------------
    def restart_app(self, name):
        self.close_app(name)
        time.sleep(1)
        return self.open_app(name)

    # ---------------------------------------
    # 📊 SYSTEM INTELLIGENCE
    # ---------------------------------------
    def system_health(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"CPU {cpu}%, RAM {ram}%"

    # ---------------------------------------
    # 🧠 AI DECISION ENGINE (CRITICAL)
    # ---------------------------------------
    def decide_action(self, command):
        cmd = command.lower()

        if "open" in cmd:
            return ("open", cmd.replace("open", "").strip())

        elif "close" in cmd:
            return ("close", cmd.replace("close", "").strip())

        elif "restart" in cmd:
            return ("restart", cmd.replace("restart", "").strip())

        elif "status" in cmd or "health" in cmd:
            return ("status", None)

        elif "run" in cmd:
            return ("run", cmd.replace("run", "").strip())

        return ("unknown", cmd)

    # ---------------------------------------
    # ⚙️ EXECUTION ENGINE
    # ---------------------------------------
    def execute(self, command):
        action, value = self.decide_action(command)

        if action == "open":
            return self.open_app(value)

        elif action == "close":
            return self.close_app(value)

        elif action == "restart":
            return self.restart_app(value)

        elif action == "status":
            return self.system_health()

        elif action == "run":
            return self.run_terminal(value)

        return f"AI fallback needed: {command}"

    # ---------------------------------------
    # 💻 TERMINAL EXECUTION
    # ---------------------------------------
    def run_terminal(self, cmd):
        try:
            result = subprocess.check_output(cmd, shell=True)
            return result.decode()[:300]
        except Exception as e:
            return str(e)

    # ---------------------------------------
    # ⏳ BACKGROUND TASK SYSTEM
    # ---------------------------------------
    def schedule_task(self, command, delay=5):
        def task():
            time.sleep(delay)
            print(f"[Background Task]: {self.execute(command)}")

        t = Thread(target=task)
        t.start()
        self.background_tasks.append(t)

        return f"Scheduled '{command}' in {delay} sec"

    # ---------------------------------------
    # ⚡ PARALLEL EXECUTION (ASYNC STYLE)
    # ---------------------------------------
    async def execute_parallel(self, commands):
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, self.execute, cmd) for cmd in commands]
        results = await asyncio.gather(*tasks)
        return results

    # ---------------------------------------
    # 🧠 MASTER CONTROL (MAIN ENTRY)
    # ---------------------------------------
    def handle(self, query):
        commands = self.parse_commands(query)

        if len(commands) > 1:
            results = asyncio.run(self.execute_parallel(commands))
            final = " | ".join(results)
        else:
            final = self.execute(commands[0])

        self.remember(query, final)
        return final