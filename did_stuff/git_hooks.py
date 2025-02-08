#!/usr/bin/env python3

import os
import shutil
from pathlib import Path


def install_hook(path: str):
    """Install the prepare-commit-msg hook in the specified Git repository.
    
    Args:
        path: Path to the Git repository where the hook should be installed
    """
    # Convert to Path object and resolve to absolute path
    repo_path = Path(path).resolve()
    hook_path = repo_path / ".git" / "hooks" / "prepare-commit-msg"
    
    # Get the path to our hook template
    template_path = Path(__file__).parent / "prepare-commit-msg"
    
    # Create hooks directory if it doesn't exist
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy the hook template
    shutil.copy2(template_path, hook_path)
    
    # Make the hook executable
    hook_path.chmod(0o755)
    
    print(f"Installed prepare-commit-msg hook in {repo_path}")
