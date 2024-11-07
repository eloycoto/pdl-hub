import os
from dataclasses import dataclass


@dataclass
class PDLScript:
    root_dir: str
    filename: str

    @property
    def absolute_path(self):
        return os.path.join(self.root_dir, self.filename)

    @property
    def pythonPath(self):
        return {"PYTHONPATH": os.path.dirname(self.absolute_path)}

    def route_path(self) -> str:
        return '/' + self.filename.replace('.pdl', '')

    def endpoint_name(self) -> str:
        return f"route_func_{self.route_path()}"
