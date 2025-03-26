import mido
import time
import threading
import queue

class MidiOutput:
    """
    Handles MIDI output to external devices.
    
    This class manages MIDI connections and sends MIDI messages
    to external devices such as DAWs or hardware synthesizers.
    """
    
    def __init__(self, virtual_port_name="VoiceToMIDI", port_name=None):
        """
        Initialize the MIDI output manager.
        
        Args:
            virtual_port_name (str): Name for the virtual MIDI port
            port_name (str, optional): Name of the MIDI output port to use.
                If None, will try to use IAC Driver or create a virtual port.
        """
        self.virtual_port_name = virtual_port_name
        self.port_name = port_name
        self.midi_out = None
        self.message_queue = queue.Queue()
        self.is_running = False
        self.thread = None
        self.current_note = None
        self.velocity = 64  # Default velocity
        self.channel = 0    # MIDI channel (0-15)
        
    def open_port(self):
        """
        Open a MIDI output port.
        
        First tries to use the specified port, then looks for IAC Driver
        ports, and finally creates a virtual output port if neither is available.
        
        Returns:
            bool: True if successfully opened a port, False otherwise
        """
        available_ports = mido.get_output_names()
        print(f"Available MIDI output ports: {available_ports}")
        
        # Try to use the specified port
        if self.port_name and self.port_name in available_ports:
            try:
                self.midi_out = mido.open_output(self.port_name)
                print(f"Connected to MIDI port: {self.port_name}")
                return True
            except Exception as e:
                print(f"Error opening MIDI port {self.port_name}: {e}")
        
        # Look for IAC Driver ports
        iac_ports = [port for port in available_ports if "IAC" in port]
        if iac_ports:
            try:
                self.port_name = iac_ports[0]
                self.midi_out = mido.open_output(self.port_name)
                print(f"Connected to IAC Driver port: {self.port_name}")
                return True
            except Exception as e:
                print(f"Error opening IAC Driver port: {e}")
        
        # Create a virtual output port
        try:
            self.midi_out = mido.open_output(self.virtual_port_name, virtual=True)
            print(f"Created virtual MIDI port: {self.virtual_port_name}")
            return True
        except Exception as e:
            print(f"Error creating virtual MIDI port: {e}")
            print("Could not open any MIDI output port")
            return False
    
    def close_port(self):
        """Close the MIDI output port."""
        if self.midi_out:
            self.all_notes_off()
            self.midi_out.close()
            self.midi_out = None
            print("MIDI output port closed")
    
    def send_note_on(self, note, velocity=None):
        """
        Send a MIDI note on message.
        
        Args:
            note (int): MIDI note number (0-127)
            velocity (int, optional): Note velocity (0-127)
        """
        if not self.midi_out or note <= 0 or note > 127:
            return
            
        vel = velocity if velocity is not None else self.velocity
        
        # Store the current note
        self.current_note = note
        
        # Create and send the note on message
        msg = mido.Message('note_on', note=note, velocity=vel, channel=self.channel)
        self.midi_out.send(msg)
        
        print(f"Note ON: {note}, Velocity: {vel}")
    
    def send_note_off(self, note=None):
        """
        Send a MIDI note off message.
        
        Args:
            note (int, optional): MIDI note number (0-127)
                If None, uses the last sent note.
        """
        if not self.midi_out:
            return
            
        # If no note specified, use the current note
        if note is None:
            note = self.current_note
            
        if note is None or note <= 0 or note > 127:
            return
            
        # Create and send the note off message
        msg = mido.Message('note_off', note=note, velocity=0, channel=self.channel)
        self.midi_out.send(msg)
        
        print(f"Note OFF: {note}")
        
        # Clear the current note if it matches
        if self.current_note == note:
            self.current_note = None
    
    def all_notes_off(self):
        """Send all notes off message on all channels."""
        if not self.midi_out:
            return
            
        # Send control change 123 (all notes off) on all channels
        for channel in range(16):
            msg = mido.Message('control_change', control=123, value=0, channel=channel)
            self.midi_out.send(msg)
            
        print("All notes off")
        self.current_note = None
    
    def set_velocity(self, velocity):
        """
        Set the default MIDI velocity.
        
        Args:
            velocity (int): MIDI velocity (0-127)
        """
        if 0 <= velocity <= 127:
            self.velocity = velocity
    
    def set_channel(self, channel):
        """
        Set the MIDI channel.
        
        Args:
            channel (int): MIDI channel (0-15)
        """
        if 0 <= channel <= 15:
            self.channel = channel
    
    def send_pitch_bend(self, value):
        """
        Send a MIDI pitch bend message.
        
        Args:
            value (float): Pitch bend value (-1 to 1)
        """
        if not self.midi_out:
            return
            
        # Convert from -1 to 1 range to 0-16383 range
        bend_value = int((value + 1) * 8192)
        bend_value = max(0, min(16383, bend_value))
        
        msg = mido.Message('pitchwheel', pitch=bend_value - 8192, channel=self.channel)
        self.midi_out.send(msg)
    
    def send_control_change(self, control, value):
        """
        Send a MIDI control change message.
        
        Args:
            control (int): Controller number (0-127)
            value (int): Controller value (0-127)
        """
        if not self.midi_out or not (0 <= control <= 127) or not (0 <= value <= 127):
            return
            
        msg = mido.Message('control_change', control=control, value=value, channel=self.channel)
        self.midi_out.send(msg)
    
    def list_output_ports(self):
        """
        Get a list of available MIDI output ports.
        
        Returns:
            list: Available MIDI output port names
        """
        return mido.get_output_names()
    
    def __del__(self):
        """Clean up resources when the object is deleted."""
        self.close_port() 