import json
import logging
import os
import shutil
import subprocess
from pathlib import Path

import click

from did_stuff import commit_message_generator, config
from did_stuff.config import load_and_validate_config


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
def enable(path):
    """Enable the pre-commit hook in the specified repository."""
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

    click.echo(f"Git hook enabled successfully in {path}")


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
        click.echo(message)
    else:
        click.echo("Failed to generate commit message.")


@main.command()
@click.pass_context
def configure(ctx):
    """Interactive configuration for Did Stuff."""
    config_file = Path.home() / ".git-commit-message-generator-config.json"

    click.echo("Let's configure Did Stuff!")

    # Choose AI provider
    provider = click.prompt("Choose AI provider", type=click.Choice(["aws-bedrock", "openai"]), default="aws-bedrock")

    # Common AI settings
    model_id = click.prompt(
        "Model ID",
        default="anthropic.claude-3-5-sonnet-20240620-v1:0" if provider == "aws-bedrock" else "gpt-3.5-turbo",
    )
    max_tokens = click.prompt("Max tokens", type=int, default=300)
    temperature = click.prompt("Temperature", type=float, default=0.3)

    # Provider-specific settings
    if provider == "aws-bedrock":
        # Get available AWS profiles
        try:
            profiles = subprocess.check_output(["aws", "configure", "list-profiles"]).decode().splitlines()
            if profiles:
                click.echo("Available AWS profiles:")
                for i, profile in enumerate(profiles, 1):
                    click.echo(f"{i}. {profile}")
                profile_choice = click.prompt(
                    "Choose a profile number or enter a new profile name", type=str, default="1"
                )
                if profile_choice.isdigit() and 1 <= int(profile_choice) <= len(profiles):
                    profile_name = profiles[int(profile_choice) - 1]
                else:
                    profile_name = profile_choice
            else:
                profile_name = click.prompt("Enter AWS profile name")
        except subprocess.CalledProcessError:
            click.echo("Unable to list AWS profiles. Make sure AWS CLI is installed and configured.")
            profile_name = click.prompt("Enter AWS profile name")

        config_data = {
            "AI": {
                "provider": provider,
                "model_id": model_id,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "user_prompt": "Generate a concise and informative commit message based on the following git diff:\n\n{diff}\n\nThe commit message should:\n1. Start with a summary in imperative mood\n2. Explain the 'why' behind changes, when possible. Don't make anything up.\n3. Keep the summary under 50 characters\n4. Use bullet points for multiple changes",
                "system_prompt": "You are an AI assistant helping to generate Git commit messages.",
            },
            "AWS": {"profile_name": profile_name},
        }
    else:  # openai
        api_key = click.prompt("OpenAI API Key")
        config_data = {
            "AI": {
                "provider": provider,
                "model_id": model_id,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "user_prompt": "Generate a concise and informative commit message based on the following git diff:\n\n{diff}\n\nThe commit message should:\n1. Start with a summary in imperative mood\n2. Explain the 'why' behind changes, when possible. Don't make anything up.\n3. Keep the summary under 50 characters\n4. Use bullet points for multiple changes",
                "system_prompt": "You are an AI assistant helping to generate Git commit messages.",
            },
            "OpenAI": {"api_key": api_key},
        }

    # Write configuration to file
    with config_file.open("w") as f:
        json.dump(config_data, f, indent=2)

    click.echo(f"Configuration saved to {config_file}")


@main.command()
@click.pass_context
def show_config(ctx):
    """Show current configuration."""
    try:
        config = load_and_validate_config()
        click.echo(json.dumps(config.__dict__, indent=2, default=lambda o: o.__dict__))
    except Exception as e:
        click.echo(f"Error loading configuration: {str(e)}", err=True)


if __name__ == "__main__":
    main()
