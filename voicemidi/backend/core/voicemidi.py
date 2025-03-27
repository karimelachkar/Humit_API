import time
import threading
from typing import Optional, List, Dict, Any

from voicemidi.backend.audio import AudioInput
from voicemidi.backend.pitch import PitchDetector
from voicemidi.backend.onset import OnsetDetector
from voicemidi.backend.midi import MidiOutput
from voicemidi.backend.utils import Config, Logger

class VoiceToMidi:
    """
    Main application class for Voice-to-MIDI conversion.
    
    This class coordinates all components and handles the real-time
    processing of audio input to MIDI output.
    """
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the Voice-to-MIDI application.
        
        Args:
            config_file (str): Path to the configuration file
        """
        # Load configuration
        self.config = Config(config_file)
        
        # Setup logger
        debug_mode = self.config.get("app", "debug")
        log_file = self.config.get("app", "log_file")
        self.logger = Logger(log_file, debug_mode)
        
        # Initialize components
        self._init_components()
        
        # Processing state
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.last_note = 0
        self.note_on = False
        self.current_time = 0
        
    def _init_components(self) -> None:
        """Initialize all components based on configuration."""
        # Audio input
        audio_config = self.config.get("audio")
        self.audio_input = AudioInput(
            sample_rate=audio_config["sample_rate"],
            block_size=audio_config["block_size"],
            channels=audio_config["channels"],
            device=audio_config["device"]
        )
        
        # Pitch detector
        pitch_config = self.config.get("pitch")
        self.pitch_detector = PitchDetector(
            sample_rate=audio_config["sample_rate"],
            block_size=audio_config["block_size"],
            min_confidence=pitch_config["min_confidence"],
            min_frequency=pitch_config["min_frequency"],
            max_frequency=pitch_config["max_frequency"]
        )
        
        # Onset detector
        onset_config = self.config.get("onset")
        self.onset_detector = OnsetDetector(
            sample_rate=audio_config["sample_rate"],
            block_size=audio_config["block_size"],
            threshold=onset_config["threshold"],
            silence=onset_config["silence"],
            minimum_inter_onset_interval_ms=onset_config["minimum_inter_onset_interval_ms"]
        )
        
        # MIDI output
        midi_config = self.config.get("midi")
        self.midi_output = MidiOutput(
            virtual_port_name=midi_config["virtual_port_name"],
            port_name=midi_config["port_name"]
        )
        
        self.logger.info("All components initialized")
    
    def start(self) -> bool:
        """
        Start the Voice-to-MIDI conversion.
        
        Returns:
            bool: True if successfully started, False otherwise
        """
        if self.is_running:
            self.logger.warning("Already running")
            return False
            
        self.logger.info("Starting Voice-to-MIDI conversion")
        
        # Open MIDI port
        if not self.midi_output.open_port():
            self.logger.error("Failed to open MIDI port")
            return False
            
        # Start audio input
        try:
            self.audio_input.start()
        except Exception as e:
            self.logger.error(f"Failed to start audio input: {e}")
            return False
            
        # Start processing thread
        self.is_running = True
        self.thread = threading.Thread(target=self._process_loop)
        self.thread.daemon = True
        self.thread.start()
        
        self.logger.info("Voice-to-MIDI conversion started")
        return True
    
    def stop(self) -> None:
        """Stop the Voice-to-MIDI conversion."""
        if not self.is_running:
            return
            
        self.logger.info("Stopping Voice-to-MIDI conversion")
        
        # Stop processing
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
        
        # Stop audio input
        self.audio_input.stop()
        
        # Close MIDI output
        self.midi_output.close_port()
        
        self.logger.info("Voice-to-MIDI conversion stopped")
    
    def _process_loop(self) -> None:
        """Main processing loop for audio to MIDI conversion."""
        block_time = self.config.get("audio", "block_size") / self.config.get("audio", "sample_rate")
        
        while self.is_running:
            # Get audio block
            audio_data = self.audio_input.get_audio_block()
            if audio_data is None:
                time.sleep(0.001)  # Small sleep to prevent CPU usage
                continue
                
            # Update current time
            self.current_time += block_time
            
            # Process audio block
            self._process_audio_block(audio_data)
    
    def _process_audio_block(self, audio_data) -> None:
        """
        Process a single block of audio data.
        
        Args:
            audio_data (ndarray): Audio data block
        """
        # Detect pitch
        midi_note, confidence, note_name = self.pitch_detector.get_midi_note(audio_data)
        
        # Detect onset
        is_onset = self.onset_detector.detect_onset(audio_data, self.current_time)
        
        # Handle MIDI output based on onset and pitch
        if is_onset and midi_note > 0 and not self.note_on:
            # New note onset detected
            self.midi_output.send_note_on(midi_note)
            self.last_note = midi_note
            self.note_on = True
            self.logger.debug(f"Note ON: {midi_note} ({note_name}), confidence: {confidence:.2f}")
        elif midi_note != self.last_note and midi_note > 0 and self.note_on:
            # Pitch changed while holding a note
            self.midi_output.send_note_off(self.last_note)
            self.midi_output.send_note_on(midi_note)
            self.last_note = midi_note
            self.logger.debug(f"Note change: {midi_note} ({note_name}), confidence: {confidence:.2f}")
        elif is_onset and self.note_on:
            # New onset while a note is on - retrigger the same note
            self.midi_output.send_note_off(self.last_note)
            self.midi_output.send_note_on(midi_note if midi_note > 0 else self.last_note)
            self.logger.debug(f"Note retrigger: {self.last_note}")
        elif midi_note == 0 and self.note_on:
            # No pitch detected, turn off the current note
            self.midi_output.send_note_off(self.last_note)
            self.note_on = False
            self.logger.debug(f"Note OFF: {self.last_note}")
    
    def list_audio_devices(self) -> List[Dict[str, Any]]:
        """
        List available audio devices.
        
        Returns:
            List[Dict[str, Any]]: List of available audio devices
        """
        devices = self.audio_input.get_devices()
        self.logger.info("Available audio devices:")
        for i, device in enumerate(devices):
            self.logger.info(f"  {i}: {device['name']}")
        return devices
        
    def list_midi_ports(self) -> List[str]:
        """
        List available MIDI ports.
        
        Returns:
            List[str]: List of available MIDI ports
        """
        ports = self.midi_output.list_output_ports()
        self.logger.info("Available MIDI output ports:")
        for i, port in enumerate(ports):
            self.logger.info(f"  {i}: {port}")
        return ports
        
    def set_debug(self, enabled: bool) -> None:
        """
        Set debug mode.
        
        Args:
            enabled (bool): True to enable debug mode, False to disable
        """
        self.logger.set_debug(enabled) 