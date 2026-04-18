# CONVERTS SIMPLIFIED TEXT INTO AUDIO USING OFFLINE TEXT-TO-SPEECH
# PROVIDES MULTIPLE VOICE OPTIONS AND SPEECH CONTROL

import os
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


@dataclass
class TTSConfig:
    """Configuration for text-to-speech settings."""
    rate: int = 150  # Speed (words per minute), typical: 100-200
    volume: float = 1.0  # Volume level (0.0-1.0)
    voice_index: int = 0  # Which voice to use (0 = default)
    output_format: str = 'wav'  # Audio format: wav, mp3, etc.
    save_to_file: bool = False
    filename: Optional[str] = None


class TTSEngine:
    """Offline text-to-speech engine using pyttsx3."""
    
    def __init__(self, config=None):
        """
        Initialize TTS engine.
        
        Args:
            config: TTSConfig object (uses defaults if None)
            
        Raises:
            RuntimeError: If pyttsx3 is not installed
        """
        if pyttsx3 is None:
            raise RuntimeError(
                "pyttsx3 not installed. Install with: pip install pyttsx3"
            )
        
        self.config = config if config else TTSConfig()
        self.engine = pyttsx3.init()
        
        # Configure engine
        self.set_rate(self.config.rate)
        self.set_volume(self.config.volume)
        self.set_voice(self.config.voice_index)
    
    def get_voices(self):
        """
        Get list of available voices.
        
        Returns:
            List of voice dictionaries with 'id' and 'name' keys
        """
        voices = self.engine.getProperty('voices')
        voice_list = []
        for i, voice in enumerate(voices):
            voice_list.append({
                'index': i,
                'id': voice.id,
                'name': voice.name,
                'gender': voice.gender if hasattr(voice, 'gender') else 'Unknown',
            })
        return voice_list
    
    def print_available_voices(self):
        """Print available voices to console."""
        voices = self.get_voices()
        print("Available Voices:")
        print("-" * 60)
        for voice in voices:
            print(f"Index: {voice['index']}")
            print(f"  Name: {voice['name']}")
            print(f"  ID: {voice['id']}")
            print(f"  Gender: {voice['gender']}")
            print()
    
    def set_rate(self, rate):
        """
        Set speech rate (words per minute).
        
        Args:
            rate: Speed in WPM (typical: 100-200, default: 150)
        """
        self.engine.setProperty('rate', rate)
        self.config.rate = rate
    
    def set_volume(self, volume):
        """
        Set volume level.
        
        Args:
            volume: Level from 0.0 to 1.0
        """
        volume = max(0.0, min(1.0, volume))  # Clamp to 0-1
        self.engine.setProperty('volume', volume)
        self.config.volume = volume
    
    def set_voice(self, voice_index):
        """
        Select voice by index.
        
        Args:
            voice_index: Index of voice (see get_voices())
        """
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            self.config.voice_index = voice_index
    
    def speak_text(self, text):
        """
        Speak text immediately (blocking call).
        
        Args:
            text: Text to speak
        """
        self.engine.say(text)
        self.engine.runAndWait()
    
    def save_to_audio(self, text, filename):
        """
        Save text-to-speech to audio file.
        
        Args:
            text: Text to convert
            filename: Output filename (e.g., 'output.wav')
        """
        # Ensure output directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to file
        self.engine.save_to_file(text, str(output_path))
        self.engine.runAndWait()
        
        if output_path.exists():
            print(f"Audio saved to: {output_path}")
        else:
            print(f"Failed to save audio to: {output_path}")
    
    def process_text(self, text):
        """
        Process text with TTS engine.
        
        Either speaks directly or saves to file based on config.
        
        Args:
            text: Text to process
        """
        if self.config.save_to_file:
            if not self.config.filename:
                raise ValueError("filename required when save_to_file=True")
            self.save_to_audio(text, self.config.filename)
        else:
            self.speak_text(text)


@dataclass
class SpeakRequest:
    """Represents a text-to-speech request."""
    text: str
    voice_index: int = 0
    rate: int = 150
    volume: float = 1.0
    filename: Optional[str] = None


def speak_inline(text, rate=150, volume=1.0, voice_index=0):
    """
    Quick function to speak text immediately.
    
    Args:
        text: Text to speak
        rate: Speech rate in WPM (default: 150)
        volume: Volume from 0.0-1.0 (default: 1.0)
        voice_index: Voice index (default: 0)
    """
    config = TTSConfig(rate=rate, volume=volume, voice_index=voice_index)
    engine = TTSEngine(config)
    engine.speak_text(text)


def speak_to_file(text, filename, rate=150, volume=1.0, voice_index=0):
    """
    Quick function to save TTS to audio file.
    
    Args:
        text: Text to convert
        filename: Output filename (e.g., 'output.wav')
        rate: Speech rate in WPM (default: 150)
        volume: Volume from 0.0-1.0 (default: 1.0)
        voice_index: Voice index (default: 0)
    """
    config = TTSConfig(
        rate=rate,
        volume=volume,
        voice_index=voice_index,
        save_to_file=True,
        filename=filename,
    )
    engine = TTSEngine(config)
    engine.save_to_audio(text, filename)


def batch_speak_to_files(texts_and_filenames, config=None):
    """
    Convert multiple texts to audio files.
    
    Args:
        texts_and_filenames: List of tuples (text, filename)
        config: TTSConfig object for all texts
        
    Example:
        texts = [
            ("Hello world", "output1.wav"),
            ("Goodbye", "output2.wav"),
        ]
        batch_speak_to_files(texts)
    """
    if config is None:
        config = TTSConfig()
    
    engine = TTSEngine(config)
    
    for i, (text, filename) in enumerate(texts_and_filenames, 1):
        print(f"Processing [{i}/{len(texts_and_filenames)}]: {filename}")
        engine.save_to_audio(text, filename)
    
    print(f"Completed batch processing of {len(texts_and_filenames)} files")


class BatchSpeaker:
    """Handle batch TTS requests."""
    
    def __init__(self, config=None):
        """
        Initialize batch speaker.
        
        Args:
            config: TTSConfig object
        """
        self.config = config if config else TTSConfig()
        self.engine = TTSEngine(self.config)
        self.requests = []
    
    def add_request(self, request):
        """
        Add TTS request to queue.
        
        Args:
            request: SpeakRequest object
        """
        self.requests.append(request)
    
    def add_text_with_file(self, text, filename, voice_index=None, rate=None, volume=None):
        """
        Convenience method to add a request.
        
        Args:
            text: Text to convert
            filename: Output filename
            voice_index: Optional voice override
            rate: Optional rate override
            volume: Optional volume override
        """
        request = SpeakRequest(
            text=text,
            filename=filename,
            voice_index=voice_index if voice_index is not None else self.config.voice_index,
            rate=rate if rate is not None else self.config.rate,
            volume=volume if volume is not None else self.config.volume,
        )
        self.add_request(request)
    
    def process_all(self):
        """Process all queued requests."""
        total = len(self.requests)
        for i, request in enumerate(self.requests, 1):
            print(f"Processing [{i}/{total}]: {request.filename}")
            
            # Update engine settings for this request
            self.engine.set_rate(request.rate)
            self.engine.set_volume(request.volume)
            self.engine.set_voice(request.voice_index)
            
            # Save to file
            self.engine.save_to_audio(request.text, request.filename)
        
        print(f"Completed batch processing of {total} requests")
    
    def clear_requests(self):
        """Clear all queued requests."""
        self.requests = []


def speak_with_pauses(text, pause_duration=1.0, rate=150, volume=1.0, voice_index=0):
    """
    Speak text with natural pauses at sentence boundaries.
    
    Args:
        text: Text to speak
        pause_duration: Pause duration in seconds between sentences
        rate: Speech rate in WPM
        volume: Volume from 0.0-1.0
        voice_index: Voice index
    """
    config = TTSConfig(rate=rate, volume=volume, voice_index=voice_index)
    engine = TTSEngine(config)
    
    # Split on sentence boundaries
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for i, sentence in enumerate(sentences):
        if sentence.strip():
            print(f"Speaking: {sentence}")
            engine.speak_text(sentence)
            
            # Add pause between sentences (except after last)
            if i < len(sentences) - 1:
                import time
                time.sleep(pause_duration)


if __name__ == "__main__":
    # Example usage
    print("TTS Module - Example Usage")
    print("-" * 60)
    
    # List available voices
    try:
        engine = TTSEngine()
        engine.print_available_voices()
    except RuntimeError as e:
        print(f"Error: {e}")
