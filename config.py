import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Prefer using environment variables in production:
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8200201915:AAHxipR8nov2PSAJ3oJLIZDqplOnxhHYRUc")
# Put your staff group ID here (e.g. -1001234567890) or set ADMIN_GROUP_ID env var
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "-1000000000000"))

# Public jobs group link (you can change this later in the admin panel)
PUBLIC_JOBS_GROUP_LINK = os.getenv("PUBLIC_JOBS_GROUP_LINK", "https://t.me/SafeJobGroup")

# Database and upload folders
DATABASE_URL = "sqlite:///safejob.db"
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESUME_DIR = os.path.join(UPLOAD_DIR, "resumes")
VIDEO_DIR = os.path.join(UPLOAD_DIR, "videos")

os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
