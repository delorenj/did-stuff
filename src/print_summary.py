#!/usr/bin/env python3

import sys
from pathlib import Path

from src.commit_message_generator import CONFIG_FILENAME, generate_and_print_message, load_and_validate_config

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    config_file = Path(__file__).resolve().parents[1] / CONFIG_FILENAME
    if not config_file.exists():
        config_file = Path.home() / CONFIG_FILENAME
    config = load_and_validate_config(config_file)

    generate_and_print_message(config)
