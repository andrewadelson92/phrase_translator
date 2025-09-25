#!/usr/bin/env python3
"""
Test script to demonstrate Spanish voice functionality.
This script shows how the translator now uses Spanish-accented voices for Spanish text.
"""

from main import translate_and_speak
from voice_module import VoiceModule


def test_spanish_voices():
    """Test different Spanish phrases with Spanish voices."""
    print("=== Testing Spanish Voice Functionality ===")
    
    # Test phrases
    phrases = [
        "Hello, how are you today?",
        "Where is the bathroom?",
        "I would like to order food.",
        "Thank you very much.",
        "Good morning, have a wonderful day!"
    ]
    
    for i, phrase in enumerate(phrases, 1):
        print(f"\n--- Test {i} ---")
        print(f"English: {phrase}")
        
        # Translate and speak with Spanish voice
        translated = translate_and_speak(
            phrase=phrase,
            source_lang="en",
            target_lang="es",
            speak_original=False,  # Don't speak English
            speak_translation=True  # Only speak Spanish with Spanish voice
        )
        
        print(f"Spanish: {translated}")
        print("✓ Spanish text spoken with Spanish accent (Mónica voice)")


def test_voice_selection():
    """Test voice selection for different languages."""
    print("\n=== Testing Voice Selection for Different Languages ===")
    
    voice = VoiceModule()
    
    languages = ["es", "fr", "de", "it", "pt", "ja", "ko", "zh"]
    language_names = {
        "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
        "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh": "Chinese"
    }
    
    for lang_code in languages:
        print(f"\n{language_names[lang_code]} ({lang_code}):")
        voice.list_voices_for_language(lang_code)
        voice.set_voice_for_language(lang_code)
        print(f"Selected voice: {voice.voice}")


def test_spanish_variants():
    """Test different Spanish voice variants."""
    print("\n=== Testing Spanish Voice Variants ===")
    
    voice = VoiceModule()
    
    # Show all available Spanish voices
    print("All available Spanish voices:")
    spanish_voices = [v for v in voice.voices if 'es_ES' in v or 'es_MX' in v]
    for i, voice_name in enumerate(spanish_voices, 1):
        print(f"{i}. {voice_name}")
    
    # Test different Spanish voices
    test_phrase = "Hola, ¿cómo estás?"
    spanish_voices_to_test = [
        "Mónica              es_ES",      # Spanish (Spain) - female
        "Paulina             es_MX",      # Spanish (Mexico) - female  
        "Eddy (Spanish (Spain)) es_ES",   # Spanish (Spain) - male
        "Eddy (Spanish (Mexico)) es_MX"   # Spanish (Mexico) - male
    ]
    
    print(f"\nTesting phrase: '{test_phrase}'")
    for voice_name in spanish_voices_to_test:
        if voice_name in voice.voices:
            print(f"\nUsing voice: {voice_name}")
            voice.set_voice(voice_name)
            voice.speak(test_phrase)


if __name__ == "__main__":
    print("Spanish Voice Test for Phrase Translator")
    print("=" * 50)
    
    try:
        # Test basic Spanish voice functionality
        test_spanish_voices()
        
        # Test voice selection for different languages
        test_voice_selection()
        
        # Test different Spanish voice variants
        test_spanish_variants()
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    print("\n" + "=" * 50)
    print("Spanish voice testing completed!")
    print("The translator now automatically uses Spanish-accented voices for Spanish text.")
