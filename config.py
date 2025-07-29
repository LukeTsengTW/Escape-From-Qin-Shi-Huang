import json
import os

CONFIG_FILE = "config.json"

default_config = {
    "DIFFICULTY" : "normal",
    "master_volume" : 1.0,
    "music_volume" : 1.0,
    "sfx_volume" : 1.0,
    "current_language" : "zh_tw",
    "first_open_game" : False,
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                config = json.load(f)
                return config
            except json.JSONDecodeError:
                print("config file is destroyed, loading the default of config")
                return default_config
    else:
        return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)