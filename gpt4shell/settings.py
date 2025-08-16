"""
Configuration management for gpt4shell.

This module handles loading configuration from ~/.gpt4shell/config.json
and provides default values when the configuration file doesn't exist.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


# Supported providers
SUPPORTED_PROVIDERS = ["openai"]

# Default configuration values
DEFAULT_CONFIG = {
    "model": "gpt-3.5-turbo",
    "provider": "openai",
    "temperature": 1.0,
    "prompt_template": "Answer the question from the user in simple terms:\n{question}",
    "max_tokens": None,  # Use provider default
    "api_base": None,    # Use provider default
}


def get_config_path() -> Path:
    """Get the path to the configuration file."""
    home = Path.home()
    return home / ".gpt4shell" / "config.json"


def load_config() -> Dict[str, Any]:
    """
    Load configuration from ~/.gpt4shell/config.json.
    
    Returns default configuration if file doesn't exist or is invalid.
    Merges user config with defaults to ensure all required keys are present.
    """
    config = DEFAULT_CONFIG.copy()
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge user config with defaults, keeping user values where provided
                config.update(user_config)
        except (json.JSONDecodeError, IOError) as e:
            # Log error but continue with defaults
            print(f"Warning: Could not load config from {config_path}: {e}")
            print("Using default configuration.")
    
    return config


def create_example_config() -> None:
    """Create an example configuration file at ~/.gpt4shell/config.json"""
    config_path = get_config_path()
    
    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Example configuration with comments (as a regular dict since JSON doesn't support comments)
    example_config = {
        "model": "gpt-4",  # Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo-preview, etc.
        "provider": "openai",  # Currently only openai is supported
        "temperature": 0.7,  # Controls randomness: 0.0 (deterministic) to 2.0 (very random)
        "prompt_template": "You are a helpful assistant. Answer the question concisely and accurately:\n{question}",
        "max_tokens": 1000,  # Maximum tokens in response (null for provider default)
        "api_base": None  # Custom API base URL (null for provider default)
    }
    
    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=2)
    
    print(f"Example configuration created at {config_path}")


# Global configuration instance
_config = None


def get_config() -> Dict[str, Any]:
    """Get the current configuration, loading it if not already loaded."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def reload_config() -> Dict[str, Any]:
    """Reload configuration from file."""
    global _config
    _config = load_config()
    return _config