from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from did_stuff.cli import install, main


@pytest.fixture
def runner():
    return CliRunner()


def test_main_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Did Stuff CLI for managing AI-powered Git commit messages." in result.output


def test_install_to_current_path_when_path_is_a_git_repo(runner, tmp_path):
    # Create a mock .git directory
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    with patch("shutil.copy2") as mock_copy, patch("os.chmod") as mock_chmod, patch(
        "pathlib.Path.exists", return_value=True
    ):  # Mock the existence of the source hook file
        result = runner.invoke(install, [str(tmp_path)])

    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.output}")

    assert result.exit_code == 0, f"Command failed with output: {result.output}"
    assert "Git hook installed successfully" in result.output

    mock_copy.assert_called_once()
    mock_chmod.assert_called_once()

    # Verify the target path for the hook
    expected_target = git_dir / "hooks" / "prepare-commit-msg"
    mock_copy.assert_called_with(
        Path(__file__).parent.parent.parent / "did_stuff" / "prepare-commit-msg", expected_target
    )
