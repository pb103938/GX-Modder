import shutil
import time
import os

def cleanup_expired_folders(base_dir="mods", max_age_seconds=30*60):
    """
    Deletes folders in `base_dir` older than max_age_seconds.
    """
    now = time.time()
    for modID_folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, modID_folder)
        if os.path.isdir(folder_path):
            # Check the folder's modification time
            folder_age = now - os.path.getmtime(folder_path)
            if folder_age > max_age_seconds:
                shutil.rmtree(folder_path)  # deletes folder and all contents
                print(f"Deleted expired folder: {folder_path}")
