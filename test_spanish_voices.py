#!/usr/bin/env python3
"""
Test script to compare different Spanish voices and find the best one.
This will help you choose which Spanish voice sounds best for your needs.
"""

from voice_module import VoiceModule
import time


def test_spanish_voices():
    """Test different Spanish voices to find the best pronunciation."""
    print("=== Spanish Voice Comparison Test ===")
    print("This will test different Spanish voices so you can choose the best one.")
    print("Each voice will speak the same Spanish phrase.\n")
    
    voice = VoiceModule()
    
    # Test phrase in Spanish
    test_phrase = "Hola, ¿cómo estás? Me llamo Mónica y soy de España."
    
    # Spanish voices to test (in order of preference)
    spanish_voices = [
        ("Mónica", "Spanish (Spain) - Female - Recommended"),
        ("Paulina", "Spanish (Mexico) - Female"),
        ("Eddy", "Spanish (Spain) - Male"),
        ("Flo", "Spanish (Spain) - Female"),
        ("Sandy", "Spanish (Spain) - Female"),
        ("Shelley", "Spanish (Spain) - Female")
    ]
    
    print(f"Test phrase: '{test_phrase}'\n")
    
    for i, (voice_name, description) in enumerate(spanish_voices, 1):
        print(f"--- Voice {i}: {voice_name} ---")
        print(f"Description: {description}")
        
        # Set the voice
        voice.set_voice(voice_name)
        
        # Speak the test phrase
        print(f"Speaking with {voice_name}...")
        voice.speak(test_phrase)
        
        # Wait a moment between voices
        time.sleep(1)
        print()
    
    print("=== Voice Selection Complete ===")
    print("Which voice sounded best to you?")
    print("You can set your preferred voice by modifying the voice mapping in voice_module.py")
    print("or by calling voice.set_voice('VoiceName') directly.")


def test_voice_customization():
    """Test voice customization options."""
    print("\n=== Voice Customization Test ===")
    
    voice = VoiceModule()
    
    # Test with different rates
    test_phrase = "Esta es una prueba de velocidad de voz."
    
    rates = [100, 150, 200, 250]
    
    for rate in rates:
        print(f"\nTesting rate: {rate} words per minute")
        voice.set_rate(rate)
        voice.set_voice("Mónica")
        voice.speak(test_phrase)
        time.sleep(0.5)


def interactive_voice_selection():
    """Interactive voice selection."""
    print("\n=== Interactive Voice Selection ===")
    
    voice = VoiceModule()
    
    # Get available Spanish voices
    spanish_voices = [v for v in voice.voices if 'es_ES' in v or 'es_MX' in v]
    
    print("Available Spanish voices:")
    for i, voice_name in enumerate(spanish_voices, 1):
        cleaned_name = voice._clean_voice_name(voice_name)
        print(f"{i}. {cleaned_name}")
    
    try:
        choice = input("\nEnter the number of the voice you want to test (or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            return
        
        choice_num = int(choice)
        if 1 <= choice_num <= len(spanish_voices):
            selected_voice = spanish_voices[choice_num - 1]
            cleaned_name = voice._clean_voice_name(selected_voice)
            
            print(f"\nTesting voice: {cleaned_name}")
            voice.set_voice(cleaned_name)
            
            test_phrases = [
                "Hola, ¿cómo estás?",
                "Me gustaría pedir comida.",
                "¿Dónde está el baño?",
                "Muchas gracias por tu ayuda."
            ]
            
            for phrase in test_phrases:
                print(f"Speaking: {phrase}")
                voice.speak(phrase)
                time.sleep(0.5)
        else:
            print("Invalid choice.")
            
    except ValueError:
        print("Please enter a valid number.")
    except KeyboardInterrupt:
        print("\nTest interrupted.")


if __name__ == "__main__":
    print("Spanish Voice Pronunciation Test")
    print("=" * 50)
    
    try:
        # Test different Spanish voices
        test_spanish_voices()
        
        # Test voice customization
        test_voice_customization()
        
        # Interactive voice selection
        interactive_voice_selection()
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    print("\n" + "=" * 50)
    print("Spanish voice testing completed!")
    print("The pronunciation should now be much better with the cleaned voice names.")
