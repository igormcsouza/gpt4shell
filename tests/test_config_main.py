"""
Unit tests for gpt4shell main module.

Tests model creation, argument parsing, and integration
with the configuration system.
"""

import argparse
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock, call

from gpt4shell import create_model, main
from gpt4shell.settings import SUPPORTED_PROVIDERS


class TestCreateModel(unittest.TestCase):
    """Test model creation functionality."""

    def test_create_model_with_openai_default_config(self):
        """Test creating OpenAI model with default configuration."""
        config = {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 1.0
        }
        
        with patch('gpt4shell.ChatOpenAI') as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            
            result = create_model(config)
            
            mock_openai.assert_called_once_with(
                model="gpt-3.5-turbo",
                temperature=1.0
            )
            self.assertEqual(result, mock_instance)

    def test_create_model_with_openai_custom_config(self):
        """Test creating OpenAI model with custom configuration."""
        config = {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000,
            "api_base": "https://custom.api.com"
        }
        
        with patch('gpt4shell.ChatOpenAI') as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            
            result = create_model(config)
            
            mock_openai.assert_called_once_with(
                model="gpt-4",
                temperature=0.7,
                max_tokens=1000,
                openai_api_base="https://custom.api.com"
            )
            self.assertEqual(result, mock_instance)

    def test_create_model_with_openai_partial_config(self):
        """Test creating OpenAI model with partial configuration."""
        config = {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.5,
            "max_tokens": 500,
            # api_base not provided
        }
        
        with patch('gpt4shell.ChatOpenAI') as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            
            result = create_model(config)
            
            mock_openai.assert_called_once_with(
                model="gpt-4",
                temperature=0.5,
                max_tokens=500
            )
            self.assertEqual(result, mock_instance)

    def test_create_model_with_unsupported_provider(self):
        """Test creating model with unsupported provider raises error."""
        config = {
            "provider": "unsupported_provider",
            "model": "some-model"
        }
        
        with self.assertRaises(ValueError) as context:
            create_model(config)
        
        error_message = str(context.exception)
        self.assertIn("Unsupported provider: unsupported_provider", error_message)
        self.assertIn("Currently supported providers:", error_message)
        for provider in SUPPORTED_PROVIDERS:
            self.assertIn(provider, error_message)

    def test_create_model_with_case_insensitive_provider(self):
        """Test creating model with case-insensitive provider name."""
        config = {
            "provider": "OpenAI",  # Mixed case
            "model": "gpt-3.5-turbo",
            "temperature": 1.0
        }
        
        with patch('gpt4shell.ChatOpenAI') as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            
            result = create_model(config)
            
            mock_openai.assert_called_once()
            self.assertEqual(result, mock_instance)

    def test_create_model_with_missing_provider_uses_default(self):
        """Test creating model with missing provider uses openai default."""
        config = {
            "model": "gpt-4",
            "temperature": 0.7
            # provider not specified
        }
        
        with patch('gpt4shell.ChatOpenAI') as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            
            result = create_model(config)
            
            mock_openai.assert_called_once_with(
                model="gpt-4",
                temperature=0.7
            )
            self.assertEqual(result, mock_instance)


class TestMainFunction(unittest.TestCase):
    """Test main function argument parsing and execution."""

    def setUp(self):
        """Set up test fixtures."""
        self.original_argv = sys.argv

    def tearDown(self):
        """Clean up after tests."""
        sys.argv = self.original_argv

    def test_main_with_config_example_flag(self):
        """Test main function with --config-example flag."""
        sys.argv = ['gpt', '--config-example']
        
        with patch('gpt4shell.create_example_config') as mock_create:
            result = main()
            
            mock_create.assert_called_once()
            self.assertEqual(result, 0)

    def test_main_without_question_shows_error(self):
        """Test main function without question shows error."""
        sys.argv = ['gpt']
        
        with patch('sys.stderr', new=StringIO()) as mock_stderr:
            with self.assertRaises(SystemExit):
                main()
            
            error_output = mock_stderr.getvalue()
            self.assertIn("Question is required", error_output)

    def test_main_with_question_processes_request(self):
        """Test main function with question processes the request."""
        sys.argv = ['gpt', 'What is Python?']
        
        mock_config = {
            "model": "gpt-3.5-turbo",
            "provider": "openai",
            "temperature": 1.0,
            "prompt_template": "Answer: {question}"
        }
        
        mock_model = MagicMock()
        mock_prompt = MagicMock()
        mock_parser = MagicMock()
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Python is a programming language."
        
        with patch('gpt4shell.get_config', return_value=mock_config), \
             patch('gpt4shell.create_model', return_value=mock_model), \
             patch('gpt4shell.ChatPromptTemplate') as mock_prompt_class, \
             patch('gpt4shell.StrOutputParser', return_value=mock_parser), \
             patch('gpt4shell.rich.print') as mock_print:
            
            mock_prompt_class.from_template.return_value = mock_prompt
            
            # Mock the chain creation (prompt | model | parser)
            # Simulate the pipe operator chain
            temp_chain1 = MagicMock()
            temp_chain1.__or__ = MagicMock(return_value=mock_chain)
            mock_prompt.__or__ = MagicMock(return_value=temp_chain1)
            
            main()
            
            # Verify prompt template was created
            mock_prompt_class.from_template.assert_called_once_with("Answer: {question}")
            
            # Verify chain was created properly
            mock_prompt.__or__.assert_called_once_with(mock_model)
            temp_chain1.__or__.assert_called_once_with(mock_parser)
            
            # Verify chain was invoked with question
            mock_chain.invoke.assert_called_once_with({"question": "What is Python?"})
            
            # Verify answer was printed
            mock_print.assert_called_once_with("Python is a programming language.")

    def test_main_with_custom_prompt_template(self):
        """Test main function uses custom prompt template from config."""
        sys.argv = ['gpt', 'Test question']
        
        custom_template = "Custom prompt: {question}"
        mock_config = {
            "prompt_template": custom_template,
            "model": "gpt-3.5-turbo",
            "provider": "openai"
        }
        
        mock_model = MagicMock()
        mock_prompt = MagicMock()
        mock_parser = MagicMock()
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Answer"
        
        with patch('gpt4shell.get_config', return_value=mock_config), \
             patch('gpt4shell.create_model', return_value=mock_model), \
             patch('gpt4shell.ChatPromptTemplate') as mock_prompt_class, \
             patch('gpt4shell.StrOutputParser', return_value=mock_parser), \
             patch('gpt4shell.rich.print'):
            
            mock_prompt_class.from_template.return_value = mock_prompt
            
            # Mock the chain creation
            temp_chain1 = MagicMock()
            temp_chain1.__or__ = MagicMock(return_value=mock_chain)
            mock_prompt.__or__ = MagicMock(return_value=temp_chain1)
            
            main()
            
            mock_prompt_class.from_template.assert_called_once_with(custom_template)

    def test_main_uses_default_prompt_template_when_missing(self):
        """Test main function uses default prompt template when not in config."""
        sys.argv = ['gpt', 'Test question']
        
        mock_config = {
            "model": "gpt-3.5-turbo",
            "provider": "openai"
            # prompt_template not provided
        }
        
        expected_default = "Answer the question from the user in simple terms:\n{question}"
        
        mock_model = MagicMock()
        mock_prompt = MagicMock()
        mock_parser = MagicMock()
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Answer"
        
        with patch('gpt4shell.get_config', return_value=mock_config), \
             patch('gpt4shell.create_model', return_value=mock_model), \
             patch('gpt4shell.ChatPromptTemplate') as mock_prompt_class, \
             patch('gpt4shell.StrOutputParser', return_value=mock_parser), \
             patch('gpt4shell.rich.print'):
            
            mock_prompt_class.from_template.return_value = mock_prompt
            
            # Mock the chain creation
            temp_chain1 = MagicMock()
            temp_chain1.__or__ = MagicMock(return_value=mock_chain)
            mock_prompt.__or__ = MagicMock(return_value=temp_chain1)
            
            main()
            
            mock_prompt_class.from_template.assert_called_once_with(expected_default)


class TestArgumentParsing(unittest.TestCase):
    """Test argument parsing functionality."""

    def test_parser_accepts_question_argument(self):
        """Test parser accepts question as positional argument."""
        parser = argparse.ArgumentParser(description='Ask a question to GPT-4')
        parser.add_argument('question', type=str, nargs='?', help='The question to ask GPT-4')
        parser.add_argument('--config-example', action='store_true', 
                           help='Create an example configuration file and exit')
        
        args = parser.parse_args(['What is Python?'])
        self.assertEqual(args.question, 'What is Python?')
        self.assertFalse(args.config_example)

    def test_parser_accepts_config_example_flag(self):
        """Test parser accepts --config-example flag."""
        parser = argparse.ArgumentParser(description='Ask a question to GPT-4')
        parser.add_argument('question', type=str, nargs='?', help='The question to ask GPT-4')
        parser.add_argument('--config-example', action='store_true', 
                           help='Create an example configuration file and exit')
        
        args = parser.parse_args(['--config-example'])
        self.assertIsNone(args.question)
        self.assertTrue(args.config_example)

    def test_parser_handles_both_question_and_flag(self):
        """Test parser handles both question and flag (flag takes precedence)."""
        parser = argparse.ArgumentParser(description='Ask a question to GPT-4')
        parser.add_argument('question', type=str, nargs='?', help='The question to ask GPT-4')
        parser.add_argument('--config-example', action='store_true', 
                           help='Create an example configuration file and exit')
        
        args = parser.parse_args(['--config-example', 'Some question'])
        self.assertEqual(args.question, 'Some question')
        self.assertTrue(args.config_example)


class TestIntegration(unittest.TestCase):
    """Integration tests for main function with configuration."""

    def test_integration_config_example_creates_file(self):
        """Test integration: --config-example creates actual config file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / ".gpt4shell" / "config.json"
            
            with patch('gpt4shell.settings.get_config_path', return_value=config_path), \
                 patch('sys.argv', ['gpt', '--config-example']), \
                 patch('builtins.print'):  # Suppress output
                
                result = main()
                
                self.assertEqual(result, 0)
                self.assertTrue(config_path.exists())
                
                # Verify the file contains valid JSON
                with open(config_path, 'r') as f:
                    import json
                    config = json.load(f)
                    self.assertIn("model", config)
                    self.assertIn("provider", config)

    def test_integration_error_handling_for_invalid_provider_in_config(self):
        """Test integration: invalid provider in config raises appropriate error."""
        sys.argv = ['gpt', 'test question']
        
        invalid_config = {
            "provider": "invalid_provider",
            "model": "some-model"
        }
        
        with patch('gpt4shell.get_config', return_value=invalid_config):
            with self.assertRaises(ValueError) as context:
                main()
            
            self.assertIn("Unsupported provider: invalid_provider", str(context.exception))


if __name__ == '__main__':
    unittest.main()