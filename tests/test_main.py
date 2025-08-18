"""Tests for the main gpt4shell functionality."""

import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from gpt4shell import main


class TestMain:
    """Test cases for the main function."""

    @patch('gpt4shell.ChatOpenAI')
    @patch('gpt4shell.rich.print')
    @patch('sys.argv', ['gpt', 'What is Python?'])
    def test_main_successful_execution(self, mock_rich_print, mock_chat_openai):
        """Test successful execution of main function with mocked OpenAI."""
        # Setup mocks
        mock_model = MagicMock()
        mock_chat_openai.return_value = mock_model
        
        # Mock the chain execution result
        expected_response = "Python is a programming language."
        
        # Patch the chain creation (prompt | model | parser)
        with patch('gpt4shell.ChatPromptTemplate') as mock_prompt_template, \
             patch('gpt4shell.StrOutputParser') as mock_output_parser:
            
            mock_prompt = MagicMock()
            mock_prompt_template.from_template.return_value = mock_prompt
            mock_parser = MagicMock()
            mock_output_parser.return_value = mock_parser
            
            # Create the final chain mock that will be the result of prompt | model | parser
            mock_final_chain = MagicMock()
            mock_final_chain.invoke.return_value = expected_response
            
            # Mock the pipe operator behavior - each step returns the next level
            mock_prompt_model_chain = MagicMock()
            mock_prompt_model_chain.__or__.return_value = mock_final_chain
            mock_prompt.__or__.return_value = mock_prompt_model_chain
            
            # Execute main
            main()
            
            # Verify interactions
            mock_chat_openai.assert_called_once_with(model="gpt-3.5-turbo", temperature=1.0)
            mock_prompt_template.from_template.assert_called_once_with(
                "Answer the question from the user in simple terms:\n{question}"
            )
            mock_final_chain.invoke.assert_called_once_with({"question": "What is Python?"})
            mock_rich_print.assert_called_once_with(expected_response)

    @patch('sys.argv', ['gpt', '--help'])
    def test_help_argument(self):
        """Test that --help argument works without errors."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # argparse exits with code 0 for help
        assert exc_info.value.code == 0

    @patch('sys.argv', ['gpt'])
    def test_missing_question_argument(self):
        """Test that missing question argument raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # argparse exits with code 2 for missing required arguments
        assert exc_info.value.code == 2

    @patch('gpt4shell.ChatOpenAI')
    @patch('sys.argv', ['gpt', 'test question'])
    def test_openai_api_key_missing_error(self, mock_chat_openai):
        """Test that missing OpenAI API key raises appropriate error."""
        from pydantic.v1.error_wrappers import ValidationError
        
        # Mock ChatOpenAI to raise ValidationError (as it does in real scenario)
        mock_chat_openai.side_effect = ValidationError(
            [{"type": "value_error", "msg": "Did not find openai_api_key"}], 
            model=MagicMock
        )
        
        with pytest.raises(ValidationError):
            main()

    @patch('gpt4shell.ChatOpenAI')
    @patch('gpt4shell.rich.print')
    @patch('sys.argv', ['gpt', 'Hello world'])
    def test_main_with_different_question(self, mock_rich_print, mock_chat_openai):
        """Test main function with a different question to ensure argument parsing works."""
        # Setup mocks
        mock_model = MagicMock()
        mock_chat_openai.return_value = mock_model
        
        # Mock the chain execution result
        expected_response = "Hello! How can I help you?"
        
        # Patch the chain creation
        with patch('gpt4shell.ChatPromptTemplate') as mock_prompt_template, \
             patch('gpt4shell.StrOutputParser') as mock_output_parser:
            
            mock_prompt = MagicMock()
            mock_prompt_template.from_template.return_value = mock_prompt
            mock_parser = MagicMock()
            mock_output_parser.return_value = mock_parser
            
            # Create the final chain mock that will be the result of prompt | model | parser
            mock_final_chain = MagicMock()
            mock_final_chain.invoke.return_value = expected_response
            
            # Mock the pipe operator behavior - each step returns the next level
            mock_prompt_model_chain = MagicMock()
            mock_prompt_model_chain.__or__.return_value = mock_final_chain
            mock_prompt.__or__.return_value = mock_prompt_model_chain
            
            # Execute main
            main()
            
            # Verify the question was passed correctly
            mock_final_chain.invoke.assert_called_once_with({"question": "Hello world"})
            mock_rich_print.assert_called_once_with(expected_response)

    @patch('gpt4shell.ChatOpenAI')
    @patch('gpt4shell.rich.print')
    @patch('sys.argv', ['gpt', 'What is the meaning of life?'])
    def test_chain_components_creation(self, mock_rich_print, mock_chat_openai):
        """Test that all chain components are created correctly."""
        # Setup mocks
        mock_model = MagicMock()
        mock_chat_openai.return_value = mock_model
        
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "42"
        
        with patch('gpt4shell.ChatPromptTemplate') as mock_prompt_template, \
             patch('gpt4shell.StrOutputParser') as mock_output_parser:
            
            mock_prompt = MagicMock()
            mock_prompt_template.from_template.return_value = mock_prompt
            mock_parser = MagicMock()
            mock_output_parser.return_value = mock_parser
            
            # Mock the pipe operator behavior
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)
            mock_model.__or__ = MagicMock(return_value=mock_chain)
            
            # Execute main
            main()
            
            # Verify all components were created
            mock_chat_openai.assert_called_once_with(model="gpt-3.5-turbo", temperature=1.0)
            mock_prompt_template.from_template.assert_called_once()
            mock_output_parser.assert_called_once()
            
            # Verify the prompt template is correct
            template_call = mock_prompt_template.from_template.call_args[0][0]
            assert "Answer the question from the user in simple terms:" in template_call
            assert "{question}" in template_call