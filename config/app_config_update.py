import json, os

CONFIG_PATH = "config/settings.json"

def save_db_choice(size, source):
    settings = {"db_size": size, "source": source}
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def load_db_choice():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

