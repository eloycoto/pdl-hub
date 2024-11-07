import os
import sys
import logging


# Environment configurations
class Config:
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.environ.get("FLASK_PORT", "5000"))


def setup_logging():
    logging.basicConfig(
        stream=sys.stderr,
        level=Config.LOG_LEVEL
    )


def register_lib_folder(root_dir: str):
    lib_path = os.path.join(root_dir, 'lib')
    if os.path.isdir(lib_path):
        sys.path.append(lib_path)
