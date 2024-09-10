import json
import logging
import os
import subprocess
from typing import Optional

from .config import Config, load_and_validate_config

# Add logging configuration
logging.basicConfig(level=logging.WARN, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_git_diff() -> Optional[str]:
    try:
        return subprocess.check_output(["git", "diff", "--cached"], text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get git diff: {e}")
        return None


def generate_message() -> Optional[str]:
    config = load_and_validate_config()
    diff = get_git_diff()
    logger.info(f"Generating message using config: {config}")
    if config.ai.provider == "aws-bedrock":
        return generate_message_bedrock(config, diff)
    elif config.ai.provider == "openai":
        return generate_message_openai(config, diff)
    else:
        logger.error(f"Unsupported AI provider: {config.ai.provider}")
        return None


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


def generate_and_print_message() -> None:
    diff = get_git_diff()
    if diff:
        commit_message = generate_message()
        if commit_message:
            print(commit_message)
        else:
            logger.warning("No commit message generated.")
    else:
        logger.warning("No diff found. Nothing to summarize.")


def main(config: Config, commit_msg_file: str) -> None:
    commit_message = generate_message()
    if commit_message:
        print(commit_message)
        update_message(commit_msg_file, commit_message)
    else:
        logger.warning("No commit message generated. " "Using default message.")
