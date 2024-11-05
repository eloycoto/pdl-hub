import logging
import os
import sys
import time

from dataclasses import dataclass
from flask import Flask, jsonify, request
from pathlib import Path
from pdl.pdl import exec_file
from typing import List

logging.basicConfig(
    stream=sys.stderr,
    level=os.environ.get('LOG_LEVEL', 'INFO').upper())

app = Flask(__name__)


@dataclass
class PDLScript:
    root_dir: str
    filename: str

    # @TODO this should load the file and do not open the file each time that
    # execute

    @property
    def absolute_path(self):
        return os.path.join(self.root_dir, self.filename)

    def route_path(self) -> str:
        return '/' + self.filename.replace('.pdl', '')

    def endpoint_name(self) -> str:
        return f"route_func_{self.route_path()}"


def find_pdl_files(root_dir: str) -> List[PDLScript]:
    """
    Find all files with .pdl extension in the given directory and its
    subdirectories.
    Args:
        root_dir (str): The root directory to start searching from
    Returns:
        List[str]: List of absolute paths to all .pdl files found
    Example:
        pdl_files = find_pdl_files("/path/to/search")
        for file in pdl_files:
            print(f"Found PDL file: {file}")
    """
    pdl_files = []
    root_path = Path(root_dir)
    if not root_path.exists():
        raise ValueError(f"Directory does not exist: {root_dir}")
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.lower().endswith('.pdl'):
                full_path = os.path.join(dirpath, filename)
                script = PDLScript(
                        root_dir=root_dir,
                        filename=os.path.relpath(full_path, root_dir))
                pdl_files.append(script)
    return pdl_files


def http_handler(path: PDLScript):
    start_time = time.time()
    data = request.get_json(force=True)

    result = exec_file(path.absolute_path, scope=data)
    return {
        "time": time.time() - start_time,
        "result": result
    }


def register_handlers(paths: List[PDLScript]):
    results = []

    for path in paths:
        route_path = path.route_path()

        def route_func(path=path):
            result = http_handler(path)
            return jsonify(result)

        app.add_url_rule(route_path,
                         endpoint=path.endpoint_name(),
                         view_func=route_func,
                         methods=["POST"])
        logging.info(f"registered handler for: {route_path}")
        results.append(route_path)

    app.add_url_rule(
            "/status",
            view_func=lambda: jsonify(results),
            methods=["GET"])


def main():
    root_dir = "./examples/"
    pdl_files = find_pdl_files(root_dir)
    register_handlers(pdl_files)

    app.run(debug=True)


if __name__ == "__main__":
    main()
