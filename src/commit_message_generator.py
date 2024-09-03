import json
import logging
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional


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
    "Generate a concise and informative commit message based on the following "
    "git diff:{diff} :: Structure: Short summary describing the changes followed by a bulleted list of changes. :: output ONLY the commit message."
)
DEFAULT_SYSTEM_PROMPT = "You are an AI assistant helping to generate Git commit messages."
CONFIG_FILENAME = ".git-commit-message-generator-config.json"

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_and_validate_config(config_file: Path) -> Config:
    try:
        with config_file.open("r") as f:
            config_dict = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config file not found at {config_file}. Using default values.")
        config_dict = {}

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


def get_git_diff() -> Optional[str]:
    try:
        return subprocess.check_output(["git", "diff", "--cached"], text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get git diff: {e}")
        return None


def generate_message(config: Config, diff: str) -> Optional[str]:
    generator = {
        "aws-bedrock": generate_message_bedrock,
        "openai": generate_message_openai,
    }.get(config.ai.provider)

    if not generator:
        logger.error(f"Unsupported AI provider: {config.ai.provider}")
        return None

    return generator(config, diff)


def generate_message_bedrock(config: Config, diff: str) -> Optional[str]:
    try:
        import boto3
    except ImportError:
        logger.error("boto3 is required for AWS Bedrock. " "Install it with 'pip install boto3'")
        return None

    try:
        session = boto3.Session(profile_name=config.aws.profile_name)
        bedrock = session.client("bedrock-runtime")

        messages = [{"role": "user", "content": config.ai.user_prompt.format(diff=diff)}]

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": config.ai.max_tokens,
                "messages": messages,
                "temperature": config.ai.temperature,
                "top_p": 1,
            }
        )

        response = bedrock.invoke_model(modelId=config.ai.model_id, body=body)

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]
    except Exception as e:
        logger.error(f"Failed to generate commit message with AWS Bedrock: {e}")
        return None


def generate_message_openai(config: Config, diff: str) -> Optional[str]:
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("openai is required for OpenAI. " "Install it with 'pip install openai'")
        return None

    try:
        api_key = config.openai.api_key if config.openai else None
        api_key = api_key or os.environ.get("OPENAI_API_KEY")

        if not api_key:
            logger.error(
                "OpenAI API key is not set. Please set it in the config file " "or as an environment variable."
            )
            return None

        client = OpenAI(api_key=api_key)

        messages = [
            {"role": "system", "content": config.ai.system_prompt},
            {"role": "user", "content": config.ai.user_prompt.format(diff=diff)},
        ]

        response = client.chat.completions.create(
            model=config.ai.model_id,
            messages=messages,
            max_tokens=config.ai.max_tokens,
            temperature=config.ai.temperature,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Failed to generate commit message with OpenAI: {e}")
        return None


def update_message(file_path: str, new_message: str) -> None:
    try:
        with open(file_path, "r+") as f:
            content = f.read()
            f.seek(0)
            f.write(f"{new_message.strip()}\n\n{content}")
        logger.info("Successfully updated commit message")
    except IOError as e:
        logger.error(f"Failed to update commit message file: {e}")


def generate_and_print_message(config: Config) -> None:
    diff = get_git_diff()
    if diff:
        commit_message = generate_message(config, diff)
        if commit_message:
            print(commit_message)
        else:
            logger.warning("No commit message generated.")
    else:
        logger.warning("No diff found. Nothing to summarize.")


def main(config: Config, commit_msg_file: str) -> None:
    diff = get_git_diff()
    if diff:
        commit_message = generate_message(config, diff)
        if commit_message:
            print(commit_message)
            update_message(commit_msg_file, commit_message)
        else:
            logger.warning("No commit message generated. " "Using default message.")
    else:
        logger.warning("No diff found. Skipping commit message generation.")
