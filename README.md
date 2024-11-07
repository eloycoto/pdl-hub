# PDL-HUB

PDL-HUB is a Python Flask-based application for discovering, loading, and
executing .pdl (Prompt Declaration Language) files. It automatically registers
routes based on the files it finds, allowing each .pdl file to be executed
through HTTP POST requests.

This is a pet and personal project that I'm running, don't use this in
production.

## Features

- Automatic Route Registration: Each .pdl file in a specified directory is
  exposed as a POST endpoint.
- Execution Time Tracking: Each execution returns timing data to evaluate
  performance.
- Library Support: Automatically adds a lib subfolder to PYTHONPATH for
  project-specific modules or dependencies.

## Getting Started

```
poetry install
poetry run pdl-hub --root-dir ./examples/
```

### Run an example

```
curl -d '{"url": "http://acalustra.com/"}' http://localhost:5000/utils/summarise | jq ".result" -r
```

### List all endpoints available

```
$ curl http://localhost:5000/status
[
  "/home/rain",
  "/github/issues",
  "/utils/summarise"
]
```


