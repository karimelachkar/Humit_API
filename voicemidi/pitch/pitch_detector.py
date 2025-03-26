import numpy as np
import aubio

class PitchDetector:
    """
    Detects pitch from audio data and converts it to MIDI notes.
    
    This class uses the aubio library to detect the fundamental frequency
    of an audio signal and convert it to MIDI notes.
    """
    
    def __init__(self, sample_rate=44100, block_size=1024, method="yin", 
                 min_confidence=0.7, min_frequency=50, max_frequency=1000):
        """
        Initialize the pitch detector.
        
        Args:
            sample_rate (int): Audio sample rate in Hz
            block_size (int): Number of frames per block
            method (str): Pitch detection method ('yin', 'yinfft', 'fcomb', 'mcomb', 'schmitt')
            min_confidence (float): Minimum confidence threshold (0-1)
            min_frequency (float): Minimum detectable frequency in Hz
            max_frequency (float): Maximum detectable frequency in Hz
        """
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.min_confidence = min_confidence
        
        # Initialize aubio pitch detector
        self.pitch_detector = aubio.pitch(
            method=method,
            buf_size=block_size,
            hop_size=block_size,
            samplerate=sample_rate
        )
        
        # Set frequency limits
        self.pitch_detector.set_unit("Hz")
        self.pitch_detector.set_silence(-60)
        self.pitch_detector.set_tolerance(0.8)
        
        # Set frequency range
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        
        # Pitch tracking state
        self.last_midi_note = 0
        self.note_buffer = []
        self.buffer_size = 3  # Number of frames to buffer for smoothing
        
    def detect_pitch(self, audio_data):
        """
        Detect the pitch from audio data.
        
        Args:
            audio_data (ndarray): Audio data
            
        Returns:
            tuple: (frequency in Hz, confidence level)
        """
        if audio_data is None or len(audio_data) < self.block_size:
            return 0, 0
            
        # Ensure audio data is float32 and properly shaped
        audio_float = audio_data.astype(np.float32)
        
        # Detect pitch
        frequency = self.pitch_detector(audio_float)[0]
        confidence = self.pitch_detector.get_confidence()
        
        # Apply confidence threshold and frequency range limits
        if confidence < self.min_confidence or frequency < self.min_frequency or frequency > self.max_frequency:
            return 0, confidence
            
        return frequency, confidence
        
    def frequency_to_midi_note(self, frequency):
        """
        Convert frequency to MIDI note number.
        
        Args:
            frequency (float): Frequency in Hz
            
        Returns:
            int: MIDI note number (0-127)
        """
        if frequency <= 0:
            return 0
            
        # A4 = 69, 440Hz
        midi_note = 69 + 12 * np.log2(frequency / 440.0)
        return int(round(midi_note))
    
    def midi_note_to_name(self, midi_note):
        """
        Convert MIDI note number to note name.
        
        Args:
            midi_note (int): MIDI note number
            
        Returns:
            str: Note name (e.g., "C4")
        """
        if midi_note <= 0:
            return "None"
            
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = (midi_note // 12) - 1
        note = note_names[midi_note % 12]
        return f"{note}{octave}"
    
    def get_midi_note(self, audio_data, smooth=True):
        """
        Get MIDI note from audio data with optional smoothing.
        
        Args:
            audio_data (ndarray): Audio data
            smooth (bool): Whether to apply note smoothing
            
        Returns:
            tuple: (MIDI note number, confidence, note name)
        """
        frequency, confidence = self.detect_pitch(audio_data)
        
        if frequency <= 0:
            return 0, confidence, "None"
            
        midi_note = self.frequency_to_midi_note(frequency)
        
        # Apply smoothing if enabled
        if smooth:
            self.note_buffer.append(midi_note)
            if len(self.note_buffer) > self.buffer_size:
                self.note_buffer.pop(0)
                
            # Get the most common note in the buffer
            if self.note_buffer:
                from collections import Counter
                counter = Counter(self.note_buffer)
                midi_note = counter.most_common(1)[0][0]
        
        note_name = self.midi_note_to_name(midi_note)
        return midi_note, confidence, note_name 