import os

from utils.file import join_paths

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = join_paths([SERVER_DIR, "..", "logs"])