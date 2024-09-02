import json
from pathlib import Path
from typing import Any, Dict

CONFIG_FILENAME = ".git-commit-message-generator-config.json"


def load_config() -> Dict[str, Any]:
    config_file = Path(CONFIG_FILENAME)
    if not config_file.exists():
        config_file = Path.home() / CONFIG_FILENAME

    with config_file.open() as f:
        return json.load(f)


def set_config(scope: str, key: str, value: str):
    config = load_config()
    if scope not in config:
        config[scope] = {}
    config[scope][key] = value

    config_file = Path(CONFIG_FILENAME) if scope == "local" else Path.home() / CONFIG_FILENAME
    with config_file.open("w") as f:
        json.dump(config, f, indent=2)


# Add other configuration-related functions as needed
