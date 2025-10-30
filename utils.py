import os, uuid
from config import RESUME_DIR, VIDEO_DIR

ALLOWED_RESUME_EXT = {'.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'}
ALLOWED_VIDEO_EXT = {'.mp4', '.mov', '.avi', '.mkv'}

def save_file(dirpath: str, filename: str, content: bytes) -> str:
    _, ext = os.path.splitext(filename.lower())
    # allow unknown extension (server-side) but you can block:
    name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(dirpath, name)
    with open(path, 'wb') as f:
        f.write(content)
    return path

def save_resume(filename: str, content: bytes) -> str:
    return save_file(RESUME_DIR, filename, content)

def save_video(filename: str, content: bytes) -> str:
    return save_file(VIDEO_DIR, filename, content)
