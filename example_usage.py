#!/usr/bin/env python3
"""
Example usage of the phrase translator with voice functionality.
This script demonstrates various ways to use the voice-enabled translator.
"""

from main import translate_and_speak
from voice_module import VoiceModule


def example_basic_translation():
    """Basic translation with voice output using language-appropriate voices."""
    print("=== Basic Translation Example ===")
    phrase = "Hello, how are you today?"
    translated = translate_and_speak(
        phrase=phrase,
        source_lang="en",
        target_lang="es",
        speak_original=True,  # Will use English voice (Samantha)
        speak_translation=True  # Will use Spanish voice (Mónica)
    )
    return translated


def example_multiple_languages():
    """Translate the same phrase to multiple languages."""
    print("\n=== Multiple Languages Example ===")
    phrase = "Good morning, have a wonderful day!"
    
    languages = [
        ("en", "es", "Spanish"),
        ("en", "fr", "French"),
        ("en", "de", "German"),
        ("en", "it", "Italian")
    ]
    
    for source, target, name in languages:
        print(f"\nTranslating to {name}:")
        translate_and_speak(
            phrase=phrase,
            source_lang=source,
            target_lang=target,
            speak_original=False,  # Only speak the first time
            speak_translation=True  # Will use appropriate voice for each language
        )


def example_voice_customization():
    """Demonstrate voice customization options."""
    print("\n=== Voice Customization Example ===")
    
    # Create a custom voice module
    voice = VoiceModule(rate=120, volume=0.8)
    
    # List available voices
    print("Available voices (showing first 10):")
    for i, voice_name in enumerate(voice.voices[:10]):
        print(f"{i}: {voice_name}")
    
    # Try different voices
    test_phrases = [
        "This is the default voice.",
        "This is Alex voice.",
        "This is Samantha voice."
    ]
    
    voices_to_try = [None, "Alex", "Samantha"]
    
    for phrase, voice_name in zip(test_phrases, voices_to_try):
        if voice_name:
            voice.set_voice(voice_name)
            print(f"\nUsing voice: {voice_name}")
        else:
            print(f"\nUsing default voice")
        
        voice.speak(phrase)


def example_interactive_translator():
    """Interactive translator that asks for user input."""
    print("\n=== Interactive Translator ===")
    
    while True:
        print("\n" + "="*50)
        print("Interactive Phrase Translator")
        print("="*50)
        
        # Get user input
        phrase = input("Enter a phrase to translate (or 'quit' to exit): ").strip()
        
        if phrase.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not phrase:
            print("Please enter a valid phrase.")
            continue
        
        # Get target language
        print("\nAvailable languages:")
        languages = {
            "1": ("es", "Spanish"),
            "2": ("fr", "French"), 
            "3": ("de", "German"),
            "4": ("it", "Italian"),
            "5": ("pt", "Portuguese"),
            "6": ("ru", "Russian"),
            "7": ("ja", "Japanese"),
            "8": ("ko", "Korean"),
            "9": ("zh", "Chinese")
        }
        
        for key, (code, name) in languages.items():
            print(f"{key}: {name}")
        
        choice = input("Choose target language (1-9): ").strip()
        
        if choice in languages:
            target_lang, lang_name = languages[choice]
            
            # Ask about voice options
            speak_original = input("Speak original phrase? (y/n): ").lower().startswith('y')
            speak_translation = input("Speak translation? (y/n): ").lower().startswith('y')
            
            print(f"\nTranslating to {lang_name}...")
            translate_and_speak(
                phrase=phrase,
                source_lang="en",
                target_lang=target_lang,
                speak_original=speak_original,
                speak_translation=speak_translation
            )
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("Phrase Translator with Voice - Example Usage")
    print("=" * 50)
    
    # Run examples
    try:
        # Basic example
        example_basic_translation()
        
        # Multiple languages
        example_multiple_languages()
        
        # Voice customization
        example_voice_customization()
        
        # Interactive mode
        example_interactive_translator()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    print("\nThank you for using the Phrase Translator with Voice!")
