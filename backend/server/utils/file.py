import os
from pathlib import Path

def join_paths(paths) -> str:
    return os.path.realpath(os.path.join(*paths))

def get_relative_path(file_path : str, folder_path : str) -> str :
    return os.path.relpath(file_path, folder_path)

def create_folder_structure(path) -> None:
    directory = Path(path)
    if not directory.exists():
        directory.mkdir(parents=True)


def file_exists(path) -> bool:
    return os.path.isfile(path)


def file_empty(path) -> bool:
    return os.stat(path).st_size == 0


# Very crude checks but for the time being, it's okay
def check_file_or_folder(path) -> bool:
    if os.path.exists(path):
        return True
    return False


def is_directory_empty(path) -> bool:
    if os.path.isdir(path) and not os.listdir(path):
        return True
    return False
