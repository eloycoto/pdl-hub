import time
import logging
from flask import jsonify, request
from typing import List
from pdl.pdl import exec_file
from .models import PDLScript


def http_handler(path: PDLScript):
    start_time = time.time()
    data = request.get_json(force=True)

    result = exec_file(path.absolute_path, scope=data)
    return {
        "time": time.time() - start_time,
        "result": result
    }


def register_handlers(app, paths: List[PDLScript]):
    results = []

    for path in paths:
        route_path = path.route_path()

        def route_func(path=path):
            result = http_handler(path)
            return jsonify(result)

        app.add_url_rule(
            route_path,
            endpoint=path.endpoint_name(),
            view_func=route_func,
            methods=["POST"])
        logging.info(f"registered handler for: {route_path}")
        results.append(route_path)

    app.add_url_rule(
        "/status",
        view_func=lambda: jsonify(results),
        methods=["GET"])

    return results
