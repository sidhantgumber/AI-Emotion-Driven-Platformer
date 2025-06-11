import pygame
import os
from typing import Dict, Optional


class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.sound_enabled = True
        self.music_enabled = True
        self.volume = 0.7 
        self.music_volume = 0.2 
        self.current_bgm = None  
        self.bgm_channel = None  
        self.current_bgm_sound = None  
        
        self.sound_paths = {
            'jump': '../audio/sfx/jump.wav',
            'coin': '../audio/sfx/coin.wav', 
            'game_over': '../audio/sfx/die.wav',
            'game_win': '../audio/sfx/win.wav'
        }
        
        self.bgm_paths = {
            'joy': '../audio/bgm/bgm_joy.wav',
            'fear': '../audio/bgm/bgm_fear.wav',
            'anger': '../audio/bgm/bgm_anger.wav',
            'neutral': '../audio/bgm/bgm_neutral.wav'
        }
        
        self.load_sounds()
        print("Audio Manager initialized")
    
    def load_sounds(self):
        for sound_name, sound_path in self.sound_paths.items():
            try:
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.volume)
                    self.sounds[sound_name] = sound
                    print(f"Loaded {sound_name} sound from {sound_path}")
                else: print("Sound dooes not exist")
                
            except Exception as e:
                print(f"Error loading {sound_name} sound: {e}")
    
   
    
    def play_sound(self, sound_name: str, volume_override: Optional[float] = None):
        """Play a sound effect."""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                if volume_override is not None:
                    # Temporarily change volume for this play
                    original_volume = sound.get_volume()
                    sound.set_volume(volume_override * self.volume)
                    sound.play()
                    sound.set_volume(original_volume)
                else:
                    sound.play()
            except Exception as e:
                print(f"Error playing {sound_name}: {e}")
        else:
            print(f"Sound '{sound_name}' not found")
    
    def play_background_music(self, emotion: str):
        """Play background music based on emotion."""
        if not self.music_enabled:
            return
        
        emotion = emotion.lower()
        self.stop_background_music()
        bgm_path = self.bgm_paths.get(emotion, self.bgm_paths['neutral'])
    
        try:
            if os.path.exists(bgm_path):
                bgm_sound = pygame.mixer.Sound(bgm_path)
                self.bgm_channel = pygame.mixer.Channel(0)
                self.bgm_channel.play(bgm_sound, loops=-1) 
                self.bgm_channel.set_volume(self.music_volume)
                
                self.current_bgm = emotion
                self.current_bgm_sound = bgm_sound
                print(f"Playing {emotion.upper()} background music: {bgm_path}")
            else:
                print(f"Background music file not found: {bgm_path}")
        except Exception as e:
            print(f"Error playing background music for {emotion}: {e}")
    
    
    def stop_background_music(self):
        """Stop the currently playing background music."""
        try:
            if hasattr(self, 'bgm_channel') and self.bgm_channel:
                self.bgm_channel.stop()
            pygame.mixer.music.stop()
            
            if self.current_bgm:
                print(f"Stopped {self.current_bgm.upper()} background music")
                self.current_bgm = None
                if hasattr(self, 'current_bgm_sound'):
                    self.current_bgm_sound = None
        except Exception as e:
            print(f"Error stopping background music: {e}")
    
    def set_music_volume(self, volume: float):
        """Set background music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        if hasattr(self, 'bgm_channel') and self.bgm_channel:
            self.bgm_channel.set_volume(self.music_volume)
            
        print(f"Music volume set to {self.music_volume:.1f}")
    
    def toggle_music(self):
        """Toggle background music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_background_music()
        status = "enabled" if self.music_enabled else "disabled"
        print(f"Background music {status}")
        return self.music_enabled
    
    def is_music_enabled(self) -> bool:
        """Check if background music is enabled."""
        return self.music_enabled
    
    def play_jump(self):
        """Play jump sound effect."""
        self.play_sound('jump', volume_override=0.6)
    
    def play_coin_collect(self):
        """Play coin collection sound effect."""
        self.play_sound('coin', volume_override=0.8)
    
    def play_game_over(self):
        """Play game over sound effect and stop background music."""
        self.stop_background_music() 
        self.play_sound('game_over', volume_override=1.0)
    
    def play_game_win(self):
        """Play game win sound effect and stop background music."""
        self.stop_background_music() 
        self.play_sound('game_win', volume_override=1.0)
    
    def set_volume(self, volume: float):
        """Set global volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
        print(f"Audio volume set to {self.volume:.1f}")
    
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self.sound_enabled = not self.sound_enabled
        status = "enabled" if self.sound_enabled else "disabled"
        print(f"Sound effects {status}")
        return self.sound_enabled
    
    def is_sound_enabled(self) -> bool:
        """Check if sound is enabled."""
        return self.sound_enabled
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()
    
    def cleanup(self):
        """Clean up audio resources."""
        self.stop_background_music()
        self.stop_all_sounds()
        self.sounds.clear()
        print("Audio Manager cleaned up")

# Unity like singleton to easily play sounds from any script
audio_manager = AudioManager()


def get_audio_manager() -> AudioManager:
    """Get the global audio manager instance."""
    return audio_manager
