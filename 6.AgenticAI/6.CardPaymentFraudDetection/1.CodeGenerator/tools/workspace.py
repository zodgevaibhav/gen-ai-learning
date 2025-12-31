import os
import shutil

BASE_DIR = "runs"

def clean_workspace():
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(BASE_DIR)
