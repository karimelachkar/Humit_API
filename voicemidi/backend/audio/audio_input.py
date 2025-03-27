import numpy as np
import sounddevice as sd
import threading
import queue
import logging
from typing import List, Dict, Any, Optional

class AudioInput:
    """
    Handles real-time audio input from the microphone.
    
    This class initializes an audio stream with the specified parameters
    and provides methods to access the audio data in real-time.
    """
    
    def __init__(self, sample_rate: int = 44100, block_size: int = 1024, channels: int = 1, device: Optional[int] = None):
        """
        Initialize the audio input handler.
        
        Args:
            sample_rate (int): Audio sample rate in Hz
            block_size (int): Number of frames per block
            channels (int): Number of audio channels (1 for mono, 2 for stereo)
            device (int, optional): Audio device index. If None, uses default.
        """
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self.device = device
        self.audio_queue = queue.Queue()
        self.stream = None
        self.is_running = False
        self.thread = None
        self.logger = logging.getLogger("VoiceMIDI.Audio")
        
    def audio_callback(self, indata, frames, time, status):
        """
        Callback function for the audio stream.
        
        This function is called by the sounddevice library whenever
        a new block of audio data is available.
        
        Args:
            indata (ndarray): Input audio data
            frames (int): Number of frames in the audio data
            time (CData): Timestamps
            status (CallbackFlags): Status flags
        """
        if status:
            self.logger.warning(f"Audio callback status: {status}")
        
        # Convert to mono if needed
        if self.channels > 1:
            audio_data = np.mean(indata, axis=1)
        else:
            audio_data = indata.copy().flatten()
        
        # Put the audio data in the queue
        try:
            self.audio_queue.put(audio_data, block=False)
        except queue.Full:
            # Queue is full, discard oldest data
            try:
                self.audio_queue.get_nowait()
                self.audio_queue.put(audio_data, block=False)
            except queue.Empty:
                pass
    
    def start(self) -> None:
        """Start the audio input stream."""
        if self.is_running:
            return
            
        self.is_running = True
        
        # Create and start the audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            channels=self.channels,
            callback=self.audio_callback,
            device=self.device
        )
        self.stream.start()
        
        self.logger.info(f"Audio input started: {self.sample_rate}Hz, {self.block_size} frames per block")
    
    def stop(self) -> None:
        """Stop the audio input stream."""
        if not self.is_running:
            return
            
        self.is_running = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        self.logger.info("Audio input stopped")
    
    def get_audio_block(self, timeout: float = 0.1):
        """
        Get the next block of audio data from the queue.
        
        Args:
            timeout (float): Timeout in seconds for queue.get()
            
        Returns:
            ndarray: Audio data block or None if timeout occurs
        """
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_devices(self) -> List[Dict[str, Any]]:
        """
        Get a list of available audio devices.
        
        Returns:
            List[Dict[str, Any]]: Audio devices information
        """
        return sd.query_devices()
    
    def __del__(self) -> None:
        """Clean up resources when the object is deleted."""
        self.stop() 