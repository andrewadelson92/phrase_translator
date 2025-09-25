from deep_translator import GoogleTranslator
from voice_module import VoiceModule


def translate_and_speak(phrase, source_lang="en", target_lang="es", speak_original=False, speak_translation=True):
    """
    Translate a phrase and optionally speak it out loud.
    
    Args:
        phrase (str): The phrase to translate
        source_lang (str): Source language code (default: "en")
        target_lang (str): Target language code (default: "es")
        speak_original (bool): Whether to speak the original phrase (default: False)
        speak_translation (bool): Whether to speak the translated phrase (default: True)
    
    Returns:
        str: The translated phrase
    """
    # Translate the phrase
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    translated_phrase = translator.translate(phrase)
    
    print(f"Original ({source_lang}): {phrase}")
    print(f"Translation ({target_lang}): {translated_phrase}")
    
    # Initialize voice module
    voice = VoiceModule()
    
    # Speak the original phrase if requested
    if speak_original:
        print(f"\nSpeaking original phrase in {source_lang}...")
        voice.set_voice_for_language(source_lang)
        voice.speak(phrase)
    
    # Speak the translated phrase if requested
    if speak_translation:
        print(f"\nSpeaking translated phrase in {target_lang}...")
        voice.set_voice_for_language(target_lang)
        voice.speak(translated_phrase)
    
    return translated_phrase


if __name__ == "__main__":
    phrase = "I would like to introduce you to my granddaughter, Alice."
    
    # Translate and speak the phrase
    translated = translate_and_speak(
        phrase=phrase,
        source_lang="en", 
        target_lang="es",
        speak_original=True,  # Speak the original English phrase
        speak_translation=True  # Speak the Spanish translation
    )