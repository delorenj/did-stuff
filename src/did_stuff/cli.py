import click
from . import config, git_hooks, commit_message_generator

@click.group()
@click.version_option()
def cli():
    """Did Stuff CLI for managing AI-powered Git commit messages."""
    pass

@cli.command()
def install_cli():
    """Install the Did Stuff CLI tool."""
    click.echo("Installing Did Stuff CLI...")
    # TODO: Implement CLI installation logic
    click.echo("Did Stuff CLI installed successfully.")

@cli.command()
@click.option('--path', default='.', help='Path to install the git hook')
def install_hook(path):
    """Install the git hook to the specified repository."""
    click.echo(f"Installing git hook to {path}...")
    git_hooks.install_hook(path)
    click.echo("Git hook installed successfully.")

@cli.command()
@click.option('--global', 'is_global', is_flag=True, help='Set global config')
@click.option('--local', 'is_local', is_flag=True, help='Set local config')
@click.option('--key', required=True, help='Configuration key')
@click.option('--value', required=True, help='Configuration value')
def config(is_global, is_local, key, value):
    """Manage Did Stuff configuration."""
    if is_global == is_local:
        raise click.UsageError("Specify either --global or --local")
    scope = 'global' if is_global else 'local'
    click.echo(f"Setting {scope} config: {key} = {value}")
    config.set_config(scope, key, value)
    click.echo("Configuration updated successfully.")

@cli.command()
def generate_message():
    """Generate a commit message based on the current git diff."""
    diff = git_hooks.get_git_diff()
    if not diff:
        click.echo("No changes to commit.")
        return
    message = commit_message_generator.generate_message(config.load_config(), diff)
    click.echo("Generated commit message:")
    click.echo(message)

if __name__ == '__main__':
    cli()