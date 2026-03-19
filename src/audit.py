import datetime

LOG_FILE = "app.log"

def log_event(user, role, action):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | {user} | {role} | {action}\n")
