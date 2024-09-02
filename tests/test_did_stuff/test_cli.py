from click.testing import CliRunner

from did_stuff.cli import cli


def test_install_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["install-cli"])
    assert result.exit_code == 0
    assert "Did Stuff CLI installed successfully" in result.output


# Add more tests for other CLI commands
