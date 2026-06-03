import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.log')


def log(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    print(entry)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(entry + '\n')
    except OSError:
        pass
