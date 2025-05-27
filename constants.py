import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, whether running from source or bundled by PyInstaller.
    """
    try:
        # When bundled by PyInstaller, _MEIPASS stores the path to the temporary folder
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in development mode
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Paths to data directories and files
BASE_DIR = os.path.abspath(".")
LESSONS_DIR = resource_path('lessons')
PROGRESS_FILE = resource_path('progress.json')
