import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal, Optional


@dataclass
class AIConfig:
    provider: Literal["aws-bedrock", "openai", "openrouter"]
    model_id: str
    max_tokens: int
    temperature: float
    user_prompt: str
    system_prompt: str


@dataclass
class AWSConfig:
    profile_name: str


@dataclass
class OpenAIConfig:
    api_key: str


@dataclass
class OpenRouterConfig:
    api_key: str


@dataclass
class Config:
    ai: AIConfig
    aws: Optional[AWSConfig] = None
    openai: Optional[OpenAIConfig] = None
    openrouter: Optional[OpenRouterConfig] = None


# Constants
DEFAULT_USER_PROMPT = (
    "You are an AI assistant specialized in analyzing git diffs and generating concise, "
    "informative commit messages. Your task is to examine the provided git diff output "
    "and create a commit message that summarizes the changes effectively. Follow these "
    "guidelines when generating the commit message: Start with a brief, high-level summary "
    "of the commit on the first line. This should be a concise overview of the main purpose "
    "or impact of the changes. After the high-level summary, provide a bulleted list of "
    "specific changes. Remember to analyze the git diff carefully and produce a commit "
    "message that accurately reflects the changes made. Output: Github Markdown, result ONLY! "
    "Your response should be a commit message that is formatted correctly for a git commit "
    "message \n\n{diff}"
)
DEFAULT_SYSTEM_PROMPT = "You are an AI assistant helping to generate Git commit messages from diffs."
CONFIG_FILENAME = "config.json"

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_and_validate_config(custom_path: Optional[Path] = None) -> Config:
    config_dict = load_config(custom_path)
    logger.info(f"Loaded config dict: {config_dict}")

    ai_config = config_dict.get("AI", {})
    ai = AIConfig(
        provider=ai_config.get("provider", "openai"),
        model_id=ai_config.get("model_id", "gpt-3.5-turbo"),
        max_tokens=ai_config.get("max_tokens", 300),
        temperature=ai_config.get("temperature", 0.3),
        user_prompt=ai_config.get("user_prompt", DEFAULT_USER_PROMPT),
        system_prompt=ai_config.get("system_prompt", DEFAULT_SYSTEM_PROMPT),
    )

    aws_config = config_dict.get("AWS")
    aws = AWSConfig(profile_name=aws_config["profile_name"]) if aws_config else None

    openai_config = config_dict.get("OpenAI")
    logger.info(f"OpenAI config: {openai_config}")
    openai = OpenAIConfig(api_key=openai_config["api_key"]) if openai_config and "api_key" in openai_config else None
    logger.info(f"Created OpenAI config object: {openai}")

    openrouter_config = config_dict.get("OpenRouter")
    logger.info(f"OpenRouter config: {openrouter_config}")
    openrouter = OpenRouterConfig(api_key=openrouter_config["api_key"]) if openrouter_config and "api_key" in openrouter_config else None
    logger.info(f"Created OpenRouter config object: {openrouter}")

    config = Config(ai=ai, aws=aws, openai=openai, openrouter=openrouter)
    validate_config(config)
    return config


def validate_config(config: Config) -> None:
    if config.ai.provider not in {"aws-bedrock", "openai", "openrouter"}:
        raise ValueError(f"Invalid AI provider: {config.ai.provider}")

    if config.ai.max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")

    if not 0 <= config.ai.temperature <= 1:
        raise ValueError("temperature must be between 0 and 1")

    if config.ai.provider == "aws-bedrock" and not config.aws:
        raise ValueError("AWS configuration is required when using aws-bedrock provider")

    if config.ai.provider == "openai" and not config.openai and not os.environ.get("OPENAI_API_KEY"):
        logger.warning(
            "OpenAI API key is not set in config or environment. "
            "Make sure to set it before generating commit messages."
        )

    if config.ai.provider == "openrouter" and not config.openrouter:
        raise ValueError("OpenRouter configuration is required when using openrouter provider")


class ConfigManager:
    def __init__(self):
        self.global_config_dir = Path.home() / ".config" / "did-stuff"
        self.project_config_file = Path(".did-stuff") / CONFIG_FILENAME
        self.global_config_file = self.global_config_dir / CONFIG_FILENAME

    def _load_single_config(self, path: Path) -> Dict[str, Any]:
        """Load a single config file if it exists and is valid"""
        if not path.exists():
            return {}
            
        try:
            with path.open() as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to load config from {path}: {str(e)}")
            return {}

    def load_config(self, custom_path: Optional[Path] = None) -> Dict[str, Any]:
        """Load and merge configurations from multiple sources with precedence:
        1. Custom path (highest precedence)
        2. Project config (.did-stuff/config.json)
        3. Global config (~/.config/did-stuff/config.json)
        """
        # Ensure global config directory exists
        self.global_config_dir.mkdir(parents=True, exist_ok=True)

        # Load configs in order of increasing precedence
        config = {}
        
        # Global config
        global_config = self._load_single_config(self.global_config_file)
        config.update(global_config)
        
        # Project config
        project_config = self._load_single_config(self.project_config_file)
        config.update(project_config)
        
        # Custom path (highest precedence)
        if custom_path:
            custom_config = self._load_single_config(custom_path)
            config.update(custom_config)

        return config

    def save_config(self, config: Dict[str, Any], scope: str = "project") -> None:
        """Save configuration to appropriate location based on scope"""
        if scope == "project":
            self.project_config_file.parent.mkdir(exist_ok=True)
            target_file = self.project_config_file
        else:
            self.global_config_dir.mkdir(parents=True, exist_ok=True)
            target_file = self.global_config_file

        try:
            with target_file.open("w") as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved successfully to {target_file}")
        except OSError as e:
            logger.error(f"Failed to save config to {target_file}: {str(e)}")
            raise


def load_config(custom_path: Optional[Path] = None) -> Dict[str, Any]:
    """Backward-compatible wrapper for ConfigManager"""
    return ConfigManager().load_config(custom_path)


def set_config(scope: str, key: str, value: str):
    logger.info(f"Setting config: scope={scope}, key={key}, value={value}")
    config = load_config()
    if scope not in config:
        logger.info(f"Creating new scope: {scope}")
        config[scope] = {}
    config[scope][key] = value

    config_dir = Path.home() / ".config" / "did-stuff"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / CONFIG_FILENAME
    logger.info(f"Saving configuration to {config_file}")
    with config_file.open("w") as f:
        json.dump(config, f, indent=2)
    logger.info("Configuration saved successfully")


# Add other configuration-related functions as needed
