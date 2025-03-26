import json
import os
import datetime

# Default configuration values
DEFAULT_CONFIG = {
    # Audio settings
    "audio": {
        "sample_rate": 44100,
        "block_size": 1024,
        "channels": 1,
        "device": None
    },
    
    # Pitch detection settings
    "pitch": {
        "min_confidence": 0.7,
        "min_frequency": 50,
        "max_frequency": 1000,
        "buffer_size": 3
    },
    
    # Onset detection settings
    "onset": {
        "threshold": 0.3,
        "silence": -60,
        "minimum_inter_onset_interval_ms": 80
    },
    
    # MIDI settings
    "midi": {
        "virtual_port_name": "VoiceToMIDI",
        "port_name": None,
        "velocity": 64,
        "channel": 0
    },
    
    # Application settings
    "app": {
        "debug": False,
        "log_file": "voicemidi.log",
        "save_recordings": False,
        "recordings_folder": "recordings"
    }
}

class Config:
    """
    Configuration manager for the voice-to-MIDI application.
    
    This class handles loading, saving, and accessing configuration
    values for all components of the application.
    """
    
    def __init__(self, config_file="config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """
        Load configuration from file.
        
        If the file doesn't exist, uses the default configuration.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    
                # Update the default config with loaded values
                self._update_dict(self.config, loaded_config)
                
                print(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                print(f"Error loading configuration: {e}")
                print("Using default configuration")
        else:
            print(f"Configuration file {self.config_file} not found, using defaults")
    
    def save(self):
        """Save the current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
                
            print(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get(self, section, key=None):
        """
        Get a configuration value.
        
        Args:
            section (str): Configuration section
            key (str, optional): Configuration key. If None, returns the whole section.
        
        Returns:
            The configuration value, or None if not found
        """
        if section not in self.config:
            return None
            
        if key is None:
            return self.config[section]
            
        if key in self.config[section]:
            return self.config[section][key]
            
        return None
    
    def set(self, section, key, value):
        """
        Set a configuration value.
        
        Args:
            section (str): Configuration section
            key (str): Configuration key
            value: Configuration value
            
        Returns:
            bool: True if successful, False otherwise
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
        return True
    
    def reset_to_defaults(self):
        """Reset the configuration to default values."""
        self.config = DEFAULT_CONFIG.copy()
        return True
    
    def _update_dict(self, target, source):
        """
        Update a nested dictionary recursively.
        
        Args:
            target (dict): Target dictionary to update
            source (dict): Source dictionary with new values
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_dict(target[key], value)
            else:
                target[key] = value 