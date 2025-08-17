"""Integration tests for gpt4shell CLI."""

import subprocess
import sys
import pytest


class TestCLIIntegration:
    """Integration test cases for the CLI interface."""

    def test_help_command_via_subprocess(self):
        """Test that the help command works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "gpt4shell", "--help"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        assert result.returncode == 0
        assert "Ask a question to GPT-4" in result.stdout
        assert "positional arguments:" in result.stdout
        assert "question" in result.stdout

    def test_missing_question_via_subprocess(self):
        """Test missing question argument via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "gpt4shell"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        # Should exit with error code for missing argument
        assert result.returncode == 2
        assert "error" in result.stderr.lower()

    def test_api_key_error_via_subprocess(self):
        """Test that missing API key produces expected error via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "gpt4shell", "test question"],
            capture_output=True,
            text=True,
            cwd=".",
            env={"PATH": "/usr/bin:/bin"}  # Clean environment without OPENAI_API_KEY
        )
        
        # Should exit with error due to missing API key
        assert result.returncode == 1
        assert "openai_api_key" in result.stderr.lower()

    def test_poetry_run_help(self):
        """Test that poetry run gpt --help works."""
        result = subprocess.run(
            ["poetry", "run", "gpt", "--help"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        assert result.returncode == 0
        assert "Ask a question to GPT-4" in result.stdout