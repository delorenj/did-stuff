from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.commit_message_generator import (
    AIConfig,
    AWSConfig,
    Config,
    OpenAIConfig,
    generate_message,
    generate_message_bedrock,
    generate_message_openai,
    get_git_diff,
    load_and_validate_config,
    main,
    update_message,
    validate_config,
)


@pytest.fixture
def sample_config():
    return Config(
        ai=AIConfig(
            provider="openai",
            model_id="gpt-3.5-turbo",
            max_tokens=300,
            temperature=0.3,
            user_prompt="Test prompt",
            system_prompt="Test system prompt",
        ),
        openai=OpenAIConfig(api_key="test_key"),
    )


def test_load_and_validate_config():
    with patch("builtins.open", MagicMock()) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = '{"AI": {"provider": "openai"}}'
        config = load_and_validate_config(Path("test_config.json"))
        assert config.ai.provider == "openai"


def test_validate_config_valid(sample_config):
    validate_config(sample_config)  # Should not raise any exception


def test_validate_config_invalid():
    invalid_config = Config(
        ai=AIConfig(
            provider="invalid",
            model_id="",
            max_tokens=0,
            temperature=2,
            user_prompt="",
            system_prompt="",
        )
    )
    with pytest.raises(ValueError):
        validate_config(invalid_config)


@patch("subprocess.check_output")
def test_get_git_diff(mock_check_output):
    mock_check_output.return_value = "Test diff"
    assert get_git_diff() == "Test diff"


@patch("src.message_generator.generate_message_openai")
def test_generate_message(mock_generate_openai, sample_config):
    mock_generate_openai.return_value = "Test commit message"
    result = generate_message(sample_config, "Test diff")
    assert result == "Test commit message"


def test_update_message(tmp_path):
    file_path = tmp_path / "commit_msg"
    file_path.write_text("Original message")
    update_message(str(file_path), "New message")
    assert file_path.read_text().startswith("New message")


def test_generate_message_bedrock():
    config = Config(
        ai=AIConfig(
            provider="aws-bedrock",
            model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
            max_tokens=300,
            temperature=0.3,
            user_prompt="Test prompt",
            system_prompt="Test system prompt",
        ),
        aws=AWSConfig(profile_name="test_profile"),
    )

    with patch("boto3.Session") as mock_session:
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.invoke_model.return_value = {
            "body": MagicMock(read=MagicMock(return_value='{"content": [{"text": "Test commit message"}]}'))
        }

        message = generate_message_bedrock(config, "Test diff")
        assert message == "Test commit message"


def test_generate_message_openai():
    config = Config(
        ai=AIConfig(
            provider="openai",
            model_id="gpt-3.5-turbo",
            max_tokens=300,
            temperature=0.3,
            user_prompt="Test prompt",
            system_prompt="Test system prompt",
        ),
        openai=OpenAIConfig(api_key="test_key"),
    )

    with patch("openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test commit message"))]
        )

        message = generate_message_openai(config, "Test diff")
        assert message == "Test commit message"


def test_main(tmp_path):
    config = Config(
        ai=AIConfig(
            provider="openai",
            model_id="gpt-3.5-turbo",
            max_tokens=300,
            temperature=0.3,
            user_prompt="Test prompt",
            system_prompt="Test system prompt",
        ),
        openai=OpenAIConfig(api_key="test_key"),
    )

    commit_msg_file = tmp_path / "commit_msg"
    commit_msg_file.write_text("Original message")

    with patch("src.message_generator.get_git_diff", return_value="Test diff"):
        with patch(
            "src.message_generator.generate_message",
            return_value="New commit message",
        ):
            main(config, str(commit_msg_file))

    assert commit_msg_file.read_text().startswith("New commit message")


# Add more tests for other functions as needed
