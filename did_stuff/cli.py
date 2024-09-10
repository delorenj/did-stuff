import logging
import os
import shutil
from pathlib import Path

import click

from did_stuff import commit_message_generator, config


# Add this at the beginning of the file
def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@click.group()
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.pass_context
def main(ctx, verbose):
    """Did Stuff CLI for managing AI-powered Git commit messages."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    setup_logging(verbose)


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True), default=".")
def install(path):
    """Install the pre-commit hook in the specified repository."""
    path = Path(path).resolve()
    if not (path / ".git").is_dir():
        raise click.UsageError(f"{path} is not a git repository.")

    hooks_dir = path / ".git" / "hooks"
    source_hook = Path(__file__).parent / "prepare-commit-msg"
    target_hook = hooks_dir / "prepare-commit-msg"

    if not source_hook.exists():
        raise click.UsageError("prepare-commit-msg hook file not found.")

    shutil.copy2(source_hook, target_hook)
    os.chmod(target_hook, 0o755)  # Make the hook executable

    click.echo(f"Git hook installed successfully in {path}")


@main.command()
@click.option("--global", "is_global", is_flag=True, help="Set global config")
@click.option("--local", "is_local", is_flag=True, help="Set local config")
@click.option("--key", required=True, help="Configuration key")
@click.option("--value", required=True, help="Configuration value")
def set_config(is_global, is_local, key, value):
    """Manage Did Stuff configuration."""
    if is_global == is_local:
        raise click.UsageError("Specify either --global or --local")
    scope = "global" if is_global else "local"
    click.echo(f"Setting {scope} config: {key} = {value}")
    config.set_config(scope, key, value)
    click.echo("Configuration updated successfully.")


@main.command()
@click.pass_context
def generate_message(ctx):
    """Generate a commit message based on the current git diff."""
    message = commit_message_generator.generate_message()
    if message:
        click.echo("Generated commit message:")
        click.echo(message)
    else:
        click.echo("Failed to generate commit message.")


if __name__ == "__main__":
    main()
