import numpy as np
import librosa
import logging

class OnsetDetector:
    """
    Detects note onsets in audio data.
    
    This class uses the librosa library to detect the onset of notes
    in an audio signal, which can be used to trigger MIDI notes.
    """
    
    def __init__(self, sample_rate=44100, block_size=1024, 
                 threshold=0.3, silence=-60, minimum_inter_onset_interval_ms=80):
        """
        Initialize the onset detector.
        
        Args:
            sample_rate (int): Audio sample rate in Hz
            block_size (int): Number of frames per block
            threshold (float): Detection threshold (0-1)
            silence (float): Silence threshold in dB
            minimum_inter_onset_interval_ms (int): Minimum time between onsets in milliseconds
        """
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.threshold = threshold
        self.silence = silence
        
        # Calculate minimum samples between onsets
        self.min_interval_samples = int(minimum_inter_onset_interval_ms * sample_rate / 1000)
        
        # Buffer for onset detection
        self.buffer = None
        self.buffer_size = 4  # Store multiple frames for better onset detection
        
        # Onset state
        self.last_onset_time = 0
        self.onset_count = 0
        self.last_onset_sample = 0
        
        # Setup logger
        self.logger = logging.getLogger("VoiceMIDI.OnsetDetector")
        
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
        
        # Update buffer
        if self.buffer is None:
            self.buffer = np.zeros((self.buffer_size, self.block_size), dtype=np.float32)
            
        # Shift buffer and add new audio data
        self.buffer = np.roll(self.buffer, -1, axis=0)
        self.buffer[-1] = audio_float
        
        # Concatenate buffer for processing
        audio_concat = self.buffer.flatten()
        
        # Check if audio is loud enough (above silence threshold)
        rms = np.sqrt(np.mean(np.square(audio_concat)))
        db = 20 * np.log10(rms) if rms > 0 else -100
        
        self.logger.debug(f"Audio level: {db:.1f} dB, silence threshold: {self.silence} dB")
        
        if db < self.silence:
            return False
        
        # Minimum time between onsets check
        current_sample = int(current_time * self.sample_rate) if current_time is not None else 0
        if self.last_onset_sample > 0 and current_sample - self.last_onset_sample < self.min_interval_samples:
            self.logger.debug(f"Too soon for new onset ({(current_sample - self.last_onset_sample) / self.sample_rate:.3f} sec)")
            return False
            
        try:
            # Use librosa for onset detection
            # First calculate onset strength signal
            onset_env = librosa.onset.onset_strength(
                y=audio_concat, 
                sr=self.sample_rate,
                hop_length=self.block_size // 4
            )
            
            # Calculate mean and standard deviation of onset strength
            mean_strength = np.mean(onset_env)
            std_strength = np.std(onset_env)
            
            self.logger.debug(f"Onset strength: mean={mean_strength:.4f}, std={std_strength:.4f}")
            
            # Then find peaks using librosa
            onsets = librosa.onset.onset_detect(
                onset_envelope=onset_env,
                sr=self.sample_rate,
                hop_length=self.block_size // 4,
                backtrack=False,
                # We're not using threshold parameter here as it's not compatible
            )
            
            # Manually filter onsets based on threshold
            if len(onsets) > 0:
                # Get the onset strengths at the detected peaks
                onset_strengths = onset_env[onsets]
                
                self.logger.debug(f"Detected {len(onsets)} potential onsets with strengths: {onset_strengths}")
                
                # Normalize onset strengths to 0-1 range
                if std_strength > 0:
                    normalized_strengths = (onset_strengths - mean_strength) / std_strength
                    normalized_strengths = (normalized_strengths + 2) / 4  # Map to approximate 0-1 range
                    
                    self.logger.debug(f"Normalized strengths: {normalized_strengths}, threshold: {self.threshold}")
                    
                    # Check if any onset is above threshold
                    if np.any(normalized_strengths > self.threshold):
                        self.onset_count += 1
                        if current_time is not None:
                            self.last_onset_time = current_time
                        self.last_onset_sample = current_sample
                        self.logger.debug(f"Onset detected! Count: {self.onset_count}")
                        return True
                    else:
                        self.logger.debug("Onset strength below threshold")
                else:
                    self.logger.debug("Standard deviation is zero, can't normalize strengths")
            else:
                self.logger.debug("No potential onsets detected")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in onset detection: {e}")
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
            self.logger.debug(f"Onset threshold set to {threshold}")
    
    def set_silence(self, silence_db):
        """
        Set the silence threshold.
        
        Args:
            silence_db (float): Silence threshold in dB (negative value)
        """
        self.silence = silence_db
        self.logger.debug(f"Silence threshold set to {silence_db} dB") 