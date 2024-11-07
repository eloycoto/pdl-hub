import argparse

from flask import Flask
from .config import Config, setup_logging, register_lib_folder
from .utils import find_pdl_files
from .handlers import register_handlers


def create_app(root_dir: str):
    app = Flask(__name__)
    setup_logging()

    pdl_files = find_pdl_files(root_dir)
    register_handlers(app, pdl_files)
    register_lib_folder(root_dir)

    return app


def main():
    parser = argparse.ArgumentParser(description='PDL Hub')
    parser.add_argument('--root-dir', type=str, default='./examples/', help='Root directory for PDL files')
    args = parser.parse_args()

    app = create_app(args.root_dir)
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT
    )


if __name__ == "__main__":
    main()
