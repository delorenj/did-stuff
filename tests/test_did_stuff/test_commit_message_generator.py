import pytest
from unittest.mock import patch, MagicMock
from did_stuff.commit_message_generator import CommitMessageGenerator
from did_stuff.config import Config, AIConfig, OpenRouterConfig

@pytest.fixture
def mock_openrouter_response():
    return {
        "choices": [{
            "message": {
                "content": "Test commit message\n- Added new feature\n- Fixed bug"
            }
        }]
    }

@pytest.fixture
def mock_config():
    return Config(
        ai=AIConfig(
            provider="openrouter",
            model_id="anthropic/claude-2",
            max_tokens=300,
            temperature=0.3,
            user_prompt="Test prompt {diff}",
            system_prompt="Test system prompt"
        ),
        openrouter=OpenRouterConfig(api_key="test-key")
    )

def test_generate_message_openrouter(mock_openrouter_response, mock_config):
    with patch("httpx.post") as mock_post, \
         patch.object(CommitMessageGenerator, "get_git_diff") as mock_get_diff:
        # Mock the git diff
        mock_get_diff.return_value = "test diff content"
        
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_openrouter_response
        mock_response.text = "Mock response text"
        mock_post.return_value = mock_response
        
        generator = CommitMessageGenerator(mock_config)
        result = generator.generate_message()
        
        assert result == "Test commit message\n- Added new feature\n- Fixed bug"
        mock_post.assert_called_once_with(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer test-key",
                "HTTP-Referer": "https://github.com/jaraddelorenzo/did-stuff",
            },
            json={
                "model": "anthropic/claude-2",
                "messages": [
                    {"role": "system", "content": "Test system prompt"},
                    {"role": "user", "content": "Test prompt test diff content"},
                ],
                "max_tokens": 300,
                "temperature": 0.3,
            },
            timeout=30.0
        )

def test_generate_message_openrouter_error(mock_config):
    with patch("httpx.post") as mock_post, \
         patch.object(CommitMessageGenerator, "get_git_diff") as mock_get_diff:
        # Mock the git diff
        mock_get_diff.return_value = "test diff content"
        
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Error response"
        mock_post.return_value = mock_response
        mock_post.return_value.raise_for_status.side_effect = Exception("API Error")
        
        generator = CommitMessageGenerator(mock_config)
        result = generator.generate_message()
        
        assert result is None