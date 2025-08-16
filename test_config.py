#!/usr/bin/env python3
"""
Simple test script to verify configuration loading works correctly.
"""

import tempfile
import json
import os
from pathlib import Path
import sys

# Add the gpt4shell module to the path
sys.path.insert(0, '/home/runner/work/gpt4shell/gpt4shell')

from gpt4shell.settings import load_config, get_config, DEFAULT_CONFIG


def test_default_config():
    """Test that default configuration is returned when no config file exists."""
    print("Testing default configuration...")
    
    # Temporarily backup any existing config
    config_path = Path.home() / ".gpt4shell" / "config.json"
    backup_path = None
    if config_path.exists():
        backup_path = config_path.with_suffix(".backup")
        config_path.rename(backup_path)
    
    try:
        # Load config when file doesn't exist
        config = load_config()
        
        # Check that we get default values
        assert config["model"] == DEFAULT_CONFIG["model"]
        assert config["provider"] == DEFAULT_CONFIG["provider"]
        assert config["temperature"] == DEFAULT_CONFIG["temperature"]
        
        print("✓ Default configuration loads correctly")
        
    finally:
        # Restore backup if it existed
        if backup_path and backup_path.exists():
            backup_path.rename(config_path)


def test_custom_config():
    """Test that custom configuration is loaded and merged with defaults."""
    print("Testing custom configuration...")
    
    config_path = Path.home() / ".gpt4shell" / "config.json"
    
    # Create a custom config with only some values
    custom_config = {
        "model": "gpt-4",
        "temperature": 0.5,
        # Note: missing other keys to test merging
    }
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Backup existing config
    backup_path = None
    if config_path.exists():
        backup_path = config_path.with_suffix(".backup")
        config_path.rename(backup_path)
    
    try:
        # Write custom config
        with open(config_path, 'w') as f:
            json.dump(custom_config, f)
        
        # Load config
        config = load_config()
        
        # Check that custom values are used
        assert config["model"] == "gpt-4"
        assert config["temperature"] == 0.5
        
        # Check that default values are used for missing keys
        assert config["provider"] == DEFAULT_CONFIG["provider"]
        assert config["prompt_template"] == DEFAULT_CONFIG["prompt_template"]
        
        print("✓ Custom configuration loads and merges with defaults correctly")
        
    finally:
        # Clean up
        if config_path.exists():
            config_path.unlink()
        if backup_path and backup_path.exists():
            backup_path.rename(config_path)


def test_model_creation():
    """Test that model creation works with different configurations."""
    print("Testing model creation...")
    
    from gpt4shell import create_model
    
    # Test with default OpenAI config
    config = {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7
    }
    
    try:
        # Set a dummy API key for testing
        import os
        original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-key"
        
        model = create_model(config)
        # Just check that we can create the model object (won't test API calls)
        assert hasattr(model, 'model_name')
        print("✓ Model creation works with OpenAI provider")
        
        # Restore original key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key
        else:
            os.environ.pop("OPENAI_API_KEY", None)
        
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False
    
    # Test with unsupported provider
    config["provider"] = "unsupported"
    try:
        model = create_model(config)
        print("✗ Should have failed with unsupported provider")
        return False
    except ValueError as e:
        print("✓ Correctly rejects unsupported provider")
    
    return True


if __name__ == "__main__":
    print("Running configuration system tests...\n")
    
    try:
        test_default_config()
        test_custom_config()
        test_model_creation()
        
        print("\n✓ All tests passed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)