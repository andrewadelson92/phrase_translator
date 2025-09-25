import subprocess
import threading
import time
import platform


class VoiceModule:
    """
    A voice module that provides text-to-speech functionality for the phrase translator.
    Uses the built-in 'say' command on macOS for reliable TTS.
    """
    
    def __init__(self, rate=150, volume=0.9, voice=None):
        """
        Initialize the voice module with specified speech rate and volume.
        
        Args:
            rate (int): Speech rate in words per minute (default: 150)
            volume (float): Volume level between 0.0 and 1.0 (default: 0.9)
            voice (str): Voice to use (default: system default)
        """
        self.rate = rate
        self.volume = volume
        self.voice = voice
        self.system = platform.system()
        
        # Get available voices
        self.voices = self._get_available_voices()
        
        # Language to voice mapping for better pronunciation
        self.language_voices = self._get_language_voice_mapping()
        
    def _get_available_voices(self):
        """
        Get available voices for the current system.
        """
        if self.system == "Darwin":  # macOS
            try:
                result = subprocess.run(['say', '-v', '?'], 
                                      capture_output=True, text=True, timeout=10)
                voices = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        # Parse voice info: "Alex en_US # Default Voice"
                        parts = line.split('#')
                        if len(parts) >= 1:
                            voice_info = parts[0].strip()
                            voices.append(voice_info)
                return voices
            except Exception as e:
                print(f"Error getting voices: {e}")
                return ["Alex", "Samantha", "Victoria"]
        else:
            return ["default"]
    
    def _get_language_voice_mapping(self):
        """
        Create a mapping of language codes to appropriate voices.
        """
        return {
            "es": ["Mónica              es_ES", "Paulina             es_MX", "Eddy (Spanish (Spain)) es_ES", "Eddy (Spanish (Mexico)) es_MX"],
            "fr": ["Amélie              fr_CA", "Thomas              fr_FR", "Eddy (French (France)) fr_FR", "Eddy (French (Canada)) fr_CA"],
            "de": ["Anna                de_DE", "Eddy (German (Germany)) de_DE", "Flo (German (Germany)) de_DE"],
            "it": ["Alice               it_IT", "Eddy (Italian (Italy)) it_IT", "Flo (Italian (Italy)) it_IT"],
            "pt": ["Luciana             pt_BR", "Joana               pt_PT", "Eddy (Portuguese (Brazil)) pt_BR", "Flo (Portuguese (Brazil)) pt_BR"],
            "ru": ["Milena              ru_RU", "Eddy (Russian (Russia)) ru_RU", "Flo (Russian (Russia)) ru_RU"],
            "ja": ["Kyoko               ja_JP", "Eddy (Japanese (Japan)) ja_JP", "Flo (Japanese (Japan)) ja_JP"],
            "ko": ["Yuna                ko_KR", "Eddy (Korean (South Korea)) ko_KR", "Flo (Korean (South Korea)) ko_KR"],
            "zh": ["Tingting            zh_CN", "Meijia              zh_TW", "Eddy (Chinese (China mainland)) zh_CN", "Eddy (Chinese (Taiwan)) zh_TW"],
            "en": ["Samantha            en_US", "Alex                en_US", "Victoria             en_US", "Daniel               en_GB", "Eddy (English (US)) en_US", "Eddy (English (UK)) en_GB"],
            "ar": ["Majed               ar_001"],
            "hi": ["Lekha               hi_IN"],
            "th": ["Kanya               th_TH"],
            "vi": ["Linh                vi_VN"],
            "tr": ["Yelda               tr_TR"],
            "pl": ["Zosia               pl_PL"],
            "cs": ["Zuzana              cs_CZ"],
            "sk": ["Laura               sk_SK"],
            "hr": ["Lana                hr_HR"],
            "ro": ["Ioana               ro_RO"],
            "hu": ["Tünde               hu_HU"],
            "el": ["Melina              el_GR"],
            "uk": ["Lesya               uk_UA"],
            "bg": ["Daria               bg_BG"],
            "da": ["Sara                da_DK"],
            "fi": ["Satu                fi_FI", "Eddy (Finnish (Finland)) fi_FI", "Flo (Finnish (Finland)) fi_FI"],
            "sv": ["Alva                sv_SE"],
            "no": ["Nora                nb_NO"],
            "nl": ["Xander              nl_NL", "Ellen               nl_BE"],
            "ca": ["Montse              ca_ES"],
            "sl": ["Tina                sl_SI"],
            "ta": ["Vani                ta_IN"],
            "ms": ["Amira               ms_MY"],
            "id": ["Damayanti           id_ID"],
            "he": ["Carmit              he_IL"],
            "au": ["Karen               en_AU"],
            "ie": ["Moira               en_IE"],
            "za": ["Tessa               en_ZA"],
            "in": ["Rishi               en_IN"],
            "gb": ["Daniel               en_GB", "Eddy (English (UK)) en_GB", "Flo (English (UK)) en_GB"],
            "us": ["Samantha            en_US", "Alex                en_US", "Eddy (English (US)) en_US", "Flo (English (US)) en_US"]
        }
    
    def set_voice(self, voice_name=None):
        """
        Set the voice to use for speech synthesis.
        
        Args:
            voice_name (str): Name of the voice to use (default: system default)
        """
        if voice_name and voice_name in self.voices:
            self.voice = voice_name
        else:
            self.voice = None  # Use system default
    
    def set_voice_for_language(self, language_code):
        """
        Automatically set the best voice for a given language code.
        
        Args:
            language_code (str): Language code (e.g., 'es', 'fr', 'de')
        """
        if language_code in self.language_voices:
            # Try to find the first available voice for this language
            for voice_name in self.language_voices[language_code]:
                if voice_name in self.voices:
                    self.voice = voice_name
                    cleaned_name = self._clean_voice_name(voice_name)
                    print(f"Selected voice '{cleaned_name}' for {language_code}")
                    return
            
            # If no preferred voice is available, use default
            print(f"No preferred voice found for {language_code}, using default")
            self.voice = None
        else:
            print(f"No voice mapping found for language code: {language_code}")
            self.voice = None
    
    def set_rate(self, rate):
        """
        Set the speech rate.
        
        Args:
            rate (int): Speech rate in words per minute
        """
        self.rate = rate
    
    def set_volume(self, volume):
        """
        Set the volume level.
        
        Args:
            volume (float): Volume level between 0.0 and 1.0
        """
        self.volume = volume
    
    def speak(self, text, blocking=True):
        """
        Convert text to speech and play it.
        
        Args:
            text (str): The text to be spoken
            blocking (bool): If True, wait for speech to complete before returning
        """
        if not text or not text.strip():
            print("No text provided for speech synthesis")
            return
            
        print(f"Speaking: {text}")
        
        if self.system == "Darwin":  # macOS
            self._speak_macos(text, blocking)
        else:
            print("TTS not supported on this system")
    
    def _speak_macos(self, text, blocking=True):
        """
        Use macOS 'say' command for speech synthesis.
        """
        try:
            # Build the say command
            cmd = ['say']
            
            # Add voice if specified
            if self.voice:
                # Clean up the voice name - extract just the voice name part
                voice_name = self._clean_voice_name(self.voice)
                cmd.extend(['-v', voice_name])
            
            # Add rate (convert from WPM to a reasonable range for say)
            # say command uses a different rate scale, so we'll map it
            if self.rate != 150:  # Default rate
                # Map rate to say's scale (roughly 50-400)
                say_rate = max(50, min(400, int(self.rate * 0.8)))
                cmd.extend(['-r', str(say_rate)])
            
            # Add the text
            cmd.append(text)
            
            if blocking:
                subprocess.run(cmd, check=True)
            else:
                # Run in a separate thread for non-blocking speech
                def speak_thread():
                    subprocess.run(cmd, check=True)
                
                thread = threading.Thread(target=speak_thread)
                thread.daemon = True
                thread.start()
                
        except subprocess.CalledProcessError as e:
            print(f"Error with speech synthesis: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def _clean_voice_name(self, voice_name):
        """
        Clean up voice name to extract just the voice name part for the say command.
        
        Args:
            voice_name (str): Full voice name with language code
            
        Returns:
            str: Cleaned voice name
        """
        if not voice_name:
            return None
            
        # Remove extra spaces and language codes
        # Example: "Mónica              es_ES" -> "Mónica"
        # Example: "Eddy (Spanish (Spain)) es_ES" -> "Eddy"
        
        # Split by spaces and take the first part
        parts = voice_name.strip().split()
        if not parts:
            return None
            
        # If the first part contains parentheses, extract the name before parentheses
        first_part = parts[0]
        if '(' in first_part:
            return first_part.split('(')[0].strip()
        else:
            return first_part
    
    def speak_async(self, text):
        """
        Convert text to speech asynchronously (non-blocking).
        
        Args:
            text (str): The text to be spoken
        """
        self.speak(text, blocking=False)
    
    def list_voices(self):
        """
        List all available voices.
        """
        print("Available voices:")
        for i, voice in enumerate(self.voices):
            print(f"{i}: {voice}")
    
    def list_voices_for_language(self, language_code):
        """
        List available voices for a specific language.
        
        Args:
            language_code (str): Language code (e.g., 'es', 'fr', 'de')
        """
        if language_code in self.language_voices:
            print(f"Available voices for {language_code}:")
            available_voices = []
            for voice_name in self.language_voices[language_code]:
                if voice_name in self.voices:
                    available_voices.append(voice_name)
                    print(f"  ✓ {voice_name}")
                else:
                    print(f"  ✗ {voice_name} (not available)")
            
            if not available_voices:
                print(f"  No specific voices available for {language_code}, will use default")
        else:
            print(f"No voice mapping found for language code: {language_code}")
    
    def stop(self):
        """
        Stop any ongoing speech synthesis.
        """
        if self.system == "Darwin":
            try:
                subprocess.run(['pkill', 'say'], check=False)
            except Exception:
                pass
    
    def cleanup(self):
        """
        Clean up the TTS engine resources.
        """
        self.stop()


def test_voice_module():
    """
    Test function to demonstrate the voice module functionality.
    """
    voice = VoiceModule()
    
    print("Testing voice module...")
    voice.list_voices()
    
    # Test basic speech
    voice.speak("Hello, this is a test of the voice module.")
    
    # Test with different settings
    voice.set_rate(120)
    voice.speak("This is spoken at a slower rate.")
    
    voice.set_rate(180)
    voice.speak("This is spoken at a faster rate.")
    
    # Test non-blocking speech
    print("Testing non-blocking speech...")
    voice.speak_async("This speech will not block the program.")
    time.sleep(1)  # Give it time to start
    print("This message should appear while speech is still playing.")


if __name__ == "__main__":
    test_voice_module()
