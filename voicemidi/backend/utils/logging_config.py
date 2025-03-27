"""
Logging configuration for the Voice-to-MIDI application.
"""
import os
import logging
import logging.handlers
from pathlib import Path


def setup_logging(debug_mode=False):
    """Configure logging for the application.

    Args:
        debug_mode (bool): Whether to enable debug logging
    """
    # Create logs directory if it doesn't exist
    log_dir = Path.home() / ".voicemidi" / "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = log_dir / "voicemidi.log"

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(console_formatter)
    root_logger.addHandler(console)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Set library logging levels
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("numpy").setLevel(logging.WARNING)
    logging.getLogger("sounddevice").setLevel(logging.WARNING)
    logging.getLogger("mido").setLevel(logging.WARNING)

    return root_logger 