import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal, Optional


@dataclass
class AIConfig:
    provider: Literal["aws-bedrock", "openai"]
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
class Config:
    ai: AIConfig
    aws: Optional[AWSConfig] = None
    openai: Optional[OpenAIConfig] = None


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
CONFIG_FILENAME = ".git-commit-message-generator-config.json"

# Set up logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_and_validate_config(custom_path: Optional[Path] = None) -> Config:
    config_dict = load_config(custom_path)

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
    openai = OpenAIConfig(api_key=openai_config["api_key"]) if openai_config and "api_key" in openai_config else None

    config = Config(ai=ai, aws=aws, openai=openai)
    validate_config(config)
    return config


def validate_config(config: Config) -> None:
    if config.ai.provider not in {"aws-bedrock", "openai"}:
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


def load_config(custom_path: Optional[Path] = None) -> Dict[str, Any]:
    config_locations = [custom_path, Path(CONFIG_FILENAME), Path.home() / CONFIG_FILENAME]

    for location in config_locations:
        if location is None:
            continue

        logger.info(f"Attempting to load configuration from {location}")
        if location.exists():
            try:
                with location.open() as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded successfully from {location}")
                return config
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON from {location}. Skipping.")
        else:
            logger.info(f"Config file not found at {location}")

    logger.warning("No valid configuration file found. Returning empty config.")
    return {}


def set_config(scope: str, key: str, value: str):
    logger.info(f"Setting config: scope={scope}, key={key}, value={value}")
    config = load_config()
    if scope not in config:
        logger.info(f"Creating new scope: {scope}")
        config[scope] = {}
    config[scope][key] = value

    config_file = Path(CONFIG_FILENAME) if scope == "local" else Path.home() / CONFIG_FILENAME
    logger.info(f"Saving configuration to {config_file}")
    with config_file.open("w") as f:
        json.dump(config, f, indent=2)
    logger.info("Configuration saved successfully")


# Add other configuration-related functions as needed
