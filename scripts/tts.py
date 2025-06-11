"""
Edge-TTS narrator - High quality Microsoft voices for game narratives.
"""

import edge_tts
import asyncio
import pygame
import tempfile
import os
import threading

class EdgeTTSNarrator:
    def __init__(self):
        """Initialize Edge TTS narrator with emotion-specific voices."""
        pygame.mixer.init()
        
        self.emotion_voices = {
            'joy': 'en-US-AvaMultilingualNeural',
            'fear': 'en-US-BrianMultilingualNeural',
            'anger': 'en-US-AndrewMultilingualNeural',
            'neutral': 'en-IN-PrabhatNeural'
        }
        
        self.is_generating = False
        self.generation_thread = None
        
        print("Edge TTS narrator initialized")
    
    def speak_narrative(self, text, emotion='neutral'):
        """Generate and play speech using Edge TTS (non-blocking)."""
        if self.is_generating:
            self.stop_speaking()
        
        voice = self.emotion_voices.get(emotion, self.emotion_voices['neutral'])
        print(f"Generating speech with {voice}...")
        
        # Start generation in background thread
        self.generation_thread = threading.Thread(
            target=self._run_async_generation,
            args=(text, voice)
        )
        self.generation_thread.daemon = True
        self.generation_thread.start()
    
    def _run_async_generation(self, text, voice):
        """Run async generation in thread."""
        try:
            self.is_generating = True
            asyncio.run(self._generate_and_play(text, voice))
        except Exception as e:
            print(f"Error in TTS generation: {e}")
        finally:
            self.is_generating = False
    
    async def _generate_and_play(self, text, voice):
        """Generate speech and play it."""
        try:
            communicate = edge_tts.Communicate(text=text, voice=voice)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            await communicate.save(temp_filename)
            
            # Play audio (this will happen in the background thread)
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Wait for completion in background
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            os.unlink(temp_filename)
            print("Finished speaking")
            
        except Exception as e:
            print(f"Error generating speech: {e}")
    
    def is_speaking(self):
        """Check if currently speaking or generating."""
        return pygame.mixer.music.get_busy() or self.is_generating
    
    def stop_speaking(self):
        """Stop current narration and generation."""
        pygame.mixer.music.stop()
        self.is_generating = False
        if self.generation_thread and self.generation_thread.is_alive():
            # Thread will finish naturally
            pass
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)