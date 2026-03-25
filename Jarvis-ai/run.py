import argparse
import sys
from app.main import run_assistant
from app.utils.logger import log_info, log_error
from app.config.settings import settings


# ----------------------------------------
# ⚙️ CLI ARGUMENTS
# ----------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="🚀 Jarvis AI Assistant Launcher"
    )

    parser.add_argument(
        "--mode",
        choices=["voice", "text"],
        default="voice" if settings.VOICE_ENABLED else "text",
        help="Run mode: voice or text"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    return parser.parse_args()


# ----------------------------------------
# 🚀 MAIN LAUNCHER
# ----------------------------------------
def main():
    args = parse_args()

    try:
        log_info("Starting Jarvis", mode=args.mode)

        # Override settings dynamically
        if args.debug:
            settings.DEBUG = True
            log_info("Debug mode enabled")

        if args.mode == "text":
            settings.VOICE_ENABLED = False

        # Start assistant
        run_assistant()

    except KeyboardInterrupt:
        log_info("Jarvis stopped by user")
        sys.exit(0)

    except Exception as e:
        log_error("Critical failure", error=str(e))
        sys.exit(1)


# ----------------------------------------
# ▶️ ENTRY POINT
# ----------------------------------------
if __name__ == "__main__":
    main()
    