import os, json
from constants import PROGRESS_FILE

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('unlocked_topic', 0), data.get('topic_progress', {})
        except Exception:
            pass
    return 0, {}

def save_progress(unlocked_topic, topic_progress):
    payload = {
        'unlocked_topic': unlocked_topic,
        'topic_progress': topic_progress
    }
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def reset_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
