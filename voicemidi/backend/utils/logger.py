import logging
import os
import time
import datetime

class Logger:
    """
    Logger for the voice-to-MIDI application.
    
    This class provides logging functionality with different
    log levels and options for console and file output.
    """
    
    def __init__(self, log_file="voicemidi.log", debug=False):
        """
        Initialize the logger.
        
        Args:
            log_file (str): Path to the log file
            debug (bool): Whether to enable debug logging
        """
        self.log_file = log_file
        self.debug_enabled = debug
        
        # Create logger
        self.logger = logging.getLogger("VoiceMIDI")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        
        # Create file handler
        try:
            file_handler = logging.FileHandler(log_file, mode='a')
            file_handler.setLevel(logging.DEBUG)
        except Exception as e:
            print(f"Warning: Could not create log file: {e}")
            file_handler = None
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Add formatter to handlers
        console_handler.setFormatter(formatter)
        if file_handler:
            file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        if file_handler:
            self.logger.addHandler(file_handler)
        
        self.info(f"Logger initialized, debug mode: {debug}")
    
    def debug(self, message):
        """
        Log a debug message.
        
        Args:
            message (str): Debug message
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        Log an info message.
        
        Args:
            message (str): Info message
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        Log a warning message.
        
        Args:
            message (str): Warning message
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        Log an error message.
        
        Args:
            message (str): Error message
        """
        self.logger.error(message)
    
    def set_debug(self, debug):
        """
        Set the debug logging mode.
        
        Args:
            debug (bool): Whether to enable debug logging
        """
        self.debug_enabled = debug
        
        # Update log levels
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(logging.DEBUG if debug else logging.INFO)
        
        self.info(f"Debug logging {'enabled' if debug else 'disabled'}")
    
    def start_timer(self, name):
        """
        Start a timer for performance tracking.
        
        Args:
            name (str): Timer name
            
        Returns:
            tuple: (name, start_time)
        """
        return (name, time.time())
    
    def stop_timer(self, timer):
        """
        Stop a timer and log the elapsed time.
        
        Args:
            timer (tuple): Timer tuple from start_timer
            
        Returns:
            float: Elapsed time in seconds
        """
        name, start_time = timer
        elapsed = time.time() - start_time
        self.debug(f"Timer '{name}': {elapsed:.4f} seconds")
        return elapsed 