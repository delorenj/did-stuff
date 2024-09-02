#!/usr/bin/env python3

import subprocess
from pathlib import Path

from .commit_message_generator import CONFIG_FILENAME, load_and_validate_config, main


def install_hook(path: str):
    hook_path = Path(path) / ".git" / "hooks" / "prepare-commit-msg"
    # TODO: Implement hook installation logic


def get_git_diff() -> str:
    return subprocess.check_output(["git", "diff", "--cached"], text=True)


if __name__ == "__main__":
    config_file = Path(__file__).resolve().parents[2] / CONFIG_FILENAME
    if not config_file.exists():
        config_file = Path.home() / CONFIG_FILENAME
    config = load_and_validate_config(config_file)

    main(config, sys.argv[1])
