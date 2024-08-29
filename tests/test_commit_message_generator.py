import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.commit_message_generator import (
    load_and_validate_config,
    validate_config,
    get_git_diff,
    generate_commit_message,
    update_commit_message,
    Config,
    AIConfig,
    AWSConfig,
    OpenAIConfig,
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
            system_prompt="Test system prompt"
        ),
        openai=OpenAIConfig(api_key="test_key")
    )

def test_load_and_validate_config():
    with patch("builtins.open", MagicMock()) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = '{"AI": {"provider": "openai"}}'
        config = load_and_validate_config(Path("test_config.json"))
        assert config.ai.provider == "openai"

def test_validate_config_valid(sample_config):
    validate_config(sample_config)  # Should not raise any exception

def test_validate_config_invalid():
    invalid_config = Config(ai=AIConfig(provider="invalid", model_id="", max_tokens=0, temperature=2, user_prompt="", system_prompt=""))
    with pytest.raises(ValueError):
        validate_config(invalid_config)

@patch('subprocess.check_output')
def test_get_git_diff(mock_check_output):
    mock_check_output.return_value = "Test diff"
    assert get_git_diff() == "Test diff"

@patch('src.commit_message_generator.generate_commit_message_openai')
def test_generate_commit_message(mock_generate_openai, sample_config):
    mock_generate_openai.return_value = "Test commit message"
    assert generate_commit_message(sample_config, "Test diff") == "Test commit message"

def test_update_commit_message(tmp_path):
    file_path = tmp_path / "commit_msg"
    file_path.write_text("Original message")
    update_commit_message(str(file_path), "New message")
    assert file_path.read_text().startswith("New message")

# Add more tests for other functions as needed