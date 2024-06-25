import os

LOG_FILE_PATH = os.path.expanduser("C:\\company\\azure_vm\\logs\\server.log")


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(clientip)s:%(clientport)s - \"%(requestline)s\" %(status)s %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH,
        },
    },
    "root": {
        "handlers": ["default", "file"],
        "level": "INFO",
    }
}

log_dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)