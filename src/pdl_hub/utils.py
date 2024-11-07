from pathlib import Path
import os
from typing import List
from .models import PDLScript


def find_pdl_files(root_dir: str) -> List[PDLScript]:
    """
    Find all files with .pdl extension in the given directory and its
    subdirectories.
    Args:
        root_dir (str): The root directory to start searching from
    Returns:
        List[str]: List of absolute paths to all .pdl files found
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
