import numpy as np
import aubio

class OnsetDetector:
    """
    Detects note onsets in audio data.
    
    This class uses the aubio library to detect the onset of notes
    in an audio signal, which can be used to trigger MIDI notes.
    """
    
    def __init__(self, sample_rate=44100, block_size=1024, method="hfc", 
                 threshold=0.3, silence=-60, minimum_inter_onset_interval_ms=80):
        """
        Initialize the onset detector.
        
        Args:
            sample_rate (int): Audio sample rate in Hz
            block_size (int): Number of frames per block
            method (str): Onset detection method ('energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux')
            threshold (float): Detection threshold (0-1)
            silence (float): Silence threshold in dB
            minimum_inter_onset_interval_ms (int): Minimum time between onsets in milliseconds
        """
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.threshold = threshold
        self.silence = silence
        
        # Calculate minimum samples between onsets
        min_interval_samples = int(minimum_inter_onset_interval_ms * sample_rate / 1000)
        
        # Initialize aubio onset detector
        self.onset_detector = aubio.onset(
            method=method,
            buf_size=block_size * 2,  # Larger window for better detection
            hop_size=block_size,
            samplerate=sample_rate
        )
        
        # Set parameters
        self.onset_detector.set_threshold(threshold)
        self.onset_detector.set_silence(silence)
        self.onset_detector.set_minioi_ms(minimum_inter_onset_interval_ms)
        
        # Onset state
        self.last_onset_time = 0
        self.onset_count = 0
        
    def detect_onset(self, audio_data, current_time=None):
        """
        Detect if there's an onset in the audio data.
        
        Args:
            audio_data (ndarray): Audio data
            current_time (float, optional): Current time in seconds
            
        Returns:
            bool: True if onset detected, False otherwise
        """
        if audio_data is None or len(audio_data) < self.block_size:
            return False
            
        # Ensure audio data is float32 and properly shaped
        audio_float = audio_data.astype(np.float32)
        
        # Detect onset
        is_onset = self.onset_detector(audio_float)
        
        if is_onset:
            self.onset_count += 1
            if current_time is not None:
                self.last_onset_time = current_time
            return True
            
        return False
    
    def get_onset_count(self):
        """Get the total number of onsets detected."""
        return self.onset_count
    
    def reset_onset_count(self):
        """Reset the onset counter."""
        self.onset_count = 0
    
    def set_threshold(self, threshold):
        """
        Set the onset detection threshold.
        
        Args:
            threshold (float): Threshold value (0-1)
        """
        if 0 <= threshold <= 1:
            self.threshold = threshold
            self.onset_detector.set_threshold(threshold)
    
    def set_silence(self, silence_db):
        """
        Set the silence threshold.
        
        Args:
            silence_db (float): Silence threshold in dB (negative value)
        """
        self.silence = silence_db
        self.onset_detector.set_silence(silence_db) 