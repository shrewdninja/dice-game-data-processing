from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Filenames
FILES = {
    "user": "user.csv",
    "user_registration": "user_registration.csv",
    "plan": "plan.csv",
    "plan_freq": "plan_payment_frequency.csv",
    "user_plan": "user_plan.csv",
    "user_payment": "user_payment_detail.csv",
    "sessions": "user_play_session.csv",
    "status": "status_code.csv",
    "channel": "channel_code.csv"
}
