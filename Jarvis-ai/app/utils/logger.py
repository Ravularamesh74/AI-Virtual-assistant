import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from app.config.settings import settings

# ----------------------------------------
# 📁 ENSURE LOG DIRECTORY
# ----------------------------------------
os.makedirs(settings.LOG_DIR, exist_ok=True)


# ----------------------------------------
# 🧠 CUSTOM FORMATTER (CLEAN + STRUCTURED)
# ----------------------------------------
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            f"[{log_time}] "
            f"[{record.levelname}] "
            f"[{record.name}] "
            f"{record.getMessage()}"
        )


# ----------------------------------------
# ⚙️ LOGGER FACTORY
# ----------------------------------------
def get_logger(name="jarvis"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # avoid duplicate handlers

    logger.setLevel(settings.LOG_LEVEL)

    formatter = CustomFormatter()

    # ------------------------------------
    # 🖥️ CONSOLE HANDLER
    # ------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ------------------------------------
    # 📁 FILE HANDLER (ROTATING)
    # ------------------------------------
    log_file = os.path.join(settings.LOG_DIR, "jarvis.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2 * 1024 * 1024,  # 2MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# ----------------------------------------
# 🚀 GLOBAL LOGGER
# ----------------------------------------
logger = get_logger()


# ----------------------------------------
# 🧠 STRUCTURED LOG HELPERS
# ----------------------------------------
def log_info(message, **kwargs):
    logger.info(_format(message, kwargs))


def log_debug(message, **kwargs):
    if settings.DEBUG:
        logger.debug(_format(message, kwargs))


def log_error(message, **kwargs):
    logger.error(_format(message, kwargs))


def log_critical(message, **kwargs):
    logger.critical(_format(message, kwargs))


# ----------------------------------------
# 🧬 FORMAT CONTEXT DATA
# ----------------------------------------
def _format(message, data):
    if not data:
        return message

    context = " | ".join([f"{k}={v}" for k, v in data.items()])
    return f"{message} | {context}"


# ----------------------------------------
# ⏱️ PERFORMANCE LOGGER
# ----------------------------------------
def log_execution(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()

        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start).total_seconds()

            log_debug(
                f"Executed {func.__name__}",
                duration=f"{duration}s"
            )

            return result

        except Exception as e:
            log_error(
                f"Error in {func.__name__}",
                error=str(e)
            )
            raise

    return wrapper


# ----------------------------------------
# 🧠 TRACE USER COMMAND
# ----------------------------------------
def log_command(query, response=None):
    log_info(
        "User Command",
        query=query,
        response=response
    )


# ----------------------------------------
# 🚨 EXCEPTION LOGGER
# ----------------------------------------
def log_exception(e):
    log_error("Exception occurred", error=str(e))