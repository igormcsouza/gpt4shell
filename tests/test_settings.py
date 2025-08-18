"""
Unit tests for gpt4shell.settings module.

Tests configuration loading, default values, file operations,
and provider validation functionality.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from gpt4shell.settings import (
    get_config_path,
    load_config,
    create_example_config,
    get_config,
    reload_config,
    DEFAULT_CONFIG,
    SUPPORTED_PROVIDERS
)


class TestConfigPath(unittest.TestCase):
    """Test configuration path generation."""

    def test_get_config_path_returns_correct_path(self):
        """Test that get_config_path returns expected path structure."""
        path = get_config_path()
        self.assertIsInstance(path, Path)
        self.assertEqual(path.name, "config.json")
        self.assertEqual(path.parent.name, ".gpt4shell")
        self.assertTrue(str(path).endswith("/.gpt4shell/config.json"))


class TestLoadConfig(unittest.TestCase):
    """Test configuration loading functionality."""

    def test_load_config_returns_defaults_when_file_missing(self):
        """Test load_config returns default config when file doesn't exist."""
        with patch('gpt4shell.settings.get_config_path') as mock_path:
            mock_path.return_value = Path("/nonexistent/config.json")
            config = load_config()
            self.assertEqual(config, DEFAULT_CONFIG)

    def test_load_config_merges_user_config_with_defaults(self):
        """Test that user config is merged with defaults."""
        user_config = {"model": "gpt-4", "temperature": 0.5}
        expected_config = DEFAULT_CONFIG.copy()
        expected_config.update(user_config)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(user_config, f)
            temp_path = f.name

        try:
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = Path(temp_path)
                config = load_config()
                self.assertEqual(config, expected_config)
        finally:
            os.unlink(temp_path)

    def test_load_config_handles_invalid_json(self):
        """Test load_config handles invalid JSON gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = Path(temp_path)
                with patch('builtins.print'):  # Suppress warning output
                    config = load_config()
                self.assertEqual(config, DEFAULT_CONFIG)
        finally:
            os.unlink(temp_path)

    def test_load_config_handles_io_error(self):
        """Test load_config handles file IO errors gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        # Make file unreadable by changing permissions
        os.chmod(temp_path, 0o000)
        
        try:
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = Path(temp_path)
                with patch('builtins.print'):  # Suppress warning output
                    config = load_config()
                self.assertEqual(config, DEFAULT_CONFIG)
        finally:
            # Restore permissions and clean up
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

    def test_load_config_preserves_unset_user_values(self):
        """Test that None/null values in user config are preserved."""
        user_config = {"model": "gpt-4", "max_tokens": None}
        expected_config = DEFAULT_CONFIG.copy()
        expected_config.update(user_config)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(user_config, f)
            temp_path = f.name

        try:
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = Path(temp_path)
                config = load_config()
                self.assertEqual(config, expected_config)
                self.assertIsNone(config["max_tokens"])
        finally:
            os.unlink(temp_path)


class TestCreateExampleConfig(unittest.TestCase):
    """Test example configuration file creation."""

    def test_create_example_config_creates_directory(self):
        """Test that create_example_config creates parent directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / ".gpt4shell" / "config.json"
            
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = config_path
                with patch('builtins.print'):  # Suppress output
                    create_example_config()
                
                self.assertTrue(config_path.exists())
                self.assertTrue(config_path.parent.exists())

    def test_create_example_config_writes_valid_json(self):
        """Test that created example config is valid JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / ".gpt4shell" / "config.json"
            
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = config_path
                with patch('builtins.print'):  # Suppress output
                    create_example_config()
                
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Verify it contains expected keys
                self.assertIn("model", config)
                self.assertIn("provider", config)
                self.assertIn("temperature", config)
                self.assertIn("prompt_template", config)
                self.assertIn("max_tokens", config)
                self.assertIn("api_base", config)

    def test_create_example_config_uses_gpt4_as_default(self):
        """Test that example config uses gpt-4 as default model."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / ".gpt4shell" / "config.json"
            
            with patch('gpt4shell.settings.get_config_path') as mock_path:
                mock_path.return_value = config_path
                with patch('builtins.print'):  # Suppress output
                    create_example_config()
                
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.assertEqual(config["model"], "gpt-4")
                self.assertEqual(config["provider"], "openai")
                self.assertEqual(config["temperature"], 0.7)


class TestGlobalConfig(unittest.TestCase):
    """Test global configuration management."""

    def setUp(self):
        """Reset global config before each test."""
        import gpt4shell.settings
        gpt4shell.settings._config = None

    def test_get_config_loads_once(self):
        """Test that get_config loads configuration only once."""
        with patch('gpt4shell.settings.load_config') as mock_load:
            mock_load.return_value = {"test": "value"}
            
            config1 = get_config()
            config2 = get_config()
            
            self.assertEqual(config1, config2)
            mock_load.assert_called_once()

    def test_reload_config_reloads_configuration(self):
        """Test that reload_config forces a reload."""
        with patch('gpt4shell.settings.load_config') as mock_load:
            mock_load.side_effect = [{"first": "load"}, {"second": "load"}]
            
            config1 = get_config()
            config2 = reload_config()
            
            self.assertNotEqual(config1, config2)
            self.assertEqual(mock_load.call_count, 2)

    def test_get_config_returns_same_instance_after_reload(self):
        """Test that get_config returns reloaded config after reload."""
        with patch('gpt4shell.settings.load_config') as mock_load:
            mock_load.side_effect = [{"first": "load"}, {"second": "load"}]
            
            get_config()  # First load
            reloaded = reload_config()
            current = get_config()
            
            self.assertEqual(reloaded, current)


class TestDefaultConfig(unittest.TestCase):
    """Test default configuration values."""

    def test_default_config_has_all_required_keys(self):
        """Test that DEFAULT_CONFIG contains all required keys."""
        required_keys = {
            "model", "provider", "temperature", 
            "prompt_template", "max_tokens", "api_base"
        }
        self.assertEqual(set(DEFAULT_CONFIG.keys()), required_keys)

    def test_default_config_values(self):
        """Test default configuration values are correct."""
        self.assertEqual(DEFAULT_CONFIG["model"], "gpt-3.5-turbo")
        self.assertEqual(DEFAULT_CONFIG["provider"], "openai")
        self.assertEqual(DEFAULT_CONFIG["temperature"], 1.0)
        self.assertIsNone(DEFAULT_CONFIG["max_tokens"])
        self.assertIsNone(DEFAULT_CONFIG["api_base"])
        self.assertIn("{question}", DEFAULT_CONFIG["prompt_template"])


class TestSupportedProviders(unittest.TestCase):
    """Test supported providers constant."""

    def test_supported_providers_contains_openai(self):
        """Test that SUPPORTED_PROVIDERS contains openai."""
        self.assertIn("openai", SUPPORTED_PROVIDERS)

    def test_supported_providers_is_list(self):
        """Test that SUPPORTED_PROVIDERS is a list."""
        self.assertIsInstance(SUPPORTED_PROVIDERS, list)

    def test_supported_providers_not_empty(self):
        """Test that SUPPORTED_PROVIDERS is not empty."""
        self.assertGreater(len(SUPPORTED_PROVIDERS), 0)


if __name__ == '__main__':
    unittest.main()