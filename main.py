from deep_translator import GoogleTranslator
from voice_module import VoiceModule


def _find_voice_by_prefix(voice_module: VoiceModule, name_prefixes):
    """Return the first available voice whose name starts with any prefix."""
    if not name_prefixes:
        return None
    for voice_name in voice_module.voices:
        candidate = voice_name.strip()
        for prefix in name_prefixes:
            if candidate.startswith(prefix):
                return voice_name
    return None


def _find_localized_voice(voice_module: VoiceModule, language_code: str, name_prefixes):
    """Pick a voice that matches language locale and desired name prefix.

    Example: language_code="es" will try to match voices containing es_ES/es_MX.
    """
    def has_lang_locale(v: str, lang: str) -> bool:
        # Normalize hyphen/underscore and split tokens
        normalized = v.replace('-', '_')
        tokens = [t for t in normalized.strip().split() if t]
        # Match tokens like es_ES, es_MX, en_US, en_GB, etc.
        return any(t.startswith(f"{lang}_") for t in tokens)

    # Filter to voices for the target language by locale markers (supports hyphen or underscore)
    localized = [v for v in voice_module.voices if has_lang_locale(v, language_code)]
    # Within localized, prefer those starting with desired prefixes
    for prefix in name_prefixes or []:
        for v in localized:
            if v.strip().startswith(prefix):
                return v
    # If no prefix match, return the first localized option if any
    return localized[0] if localized else None


def speak_phrase_in_en_and_es(phrase: str, gender: str = "male") -> str:
    """
    Translate an English phrase to Spanish and speak both using a male or female voice.

    Args:
        phrase: English text to translate and speak.
        gender: "male" or "female" voice selection.

    Returns:
        The translated Spanish phrase.
    """
    gender = (gender or "").strip().lower()
    if gender not in ("male", "female"):
        gender = "female"

    # Translate EN -> ES
    translator = GoogleTranslator(source="en", target="es")
    translated_phrase = translator.translate(phrase)

    print(f"Original (en): {phrase}")
    print(f"Translation (es): {translated_phrase}")

    voice = VoiceModule()

    # Speak English with gendered voice (force specific installed voices)
    en_prefixes = ["Alex", "Daniel", "Eddy (English (US))", "Eddy (English (UK))"] if gender == "male" else ["Samantha", "Victoria"]
    en_voice = _find_localized_voice(voice, "en", en_prefixes) or _find_voice_by_prefix(voice, en_prefixes)
    if en_voice:
        voice.set_voice(en_voice)
    else:
        voice.set_voice_for_language("en")
    print("\nSpeaking original phrase in English...")
    if en_voice:
        print(f"Using English voice: {voice._clean_voice_name(en_voice)}")
    voice.speak(phrase)

    # Speak Spanish with gendered voice (mirror female flow by reordering mapping and using set_voice_for_language)
    if "es" in voice.language_voices:
        spanish = voice.language_voices["es"]
        if gender == "male":
            # Prefer male Eddy first (Spain then Mexico), then others
            preferred = [
                v for v in spanish
                if v.strip().startswith("Eddy (Spanish (Spain))") or v.strip().startswith("Eddy (Spanish (Mexico))") or v.strip().startswith("Eddy")
            ]
            others = [v for v in spanish if v not in preferred]
            voice.language_voices["es"] = preferred + others
        else:
            preferred = [v for v in spanish if v.strip().startswith(("Mónica", "Paulina"))]
            others = [v for v in spanish if v not in preferred]
            voice.language_voices["es"] = preferred + others
    voice.set_voice_for_language("es")
    print("\nSpeaking translated phrase in Spanish...")
    if voice.voice:
        print(f"Using Spanish voice: {voice._clean_voice_name(voice.voice)}")
    voice.speak(translated_phrase)

    return translated_phrase


# Keep the original helper for compatibility with other scripts, but the
# program entrypoint below provides the simplified single-example flow.
def translate_and_speak(phrase, source_lang="en", target_lang="es", speak_original=False, speak_translation=True):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    translated_phrase = translator.translate(phrase)
    print(f"Original ({source_lang}): {phrase}")
    print(f"Translation ({target_lang}): {translated_phrase}")
    voice = VoiceModule()
    if speak_original:
        voice.set_voice_for_language(source_lang)
        voice.speak(phrase)
    if speak_translation:
        voice.set_voice_for_language(target_lang)
        voice.speak(translated_phrase)
    return translated_phrase


if __name__ == "__main__":
    # Simple non-interactive test: default to male voice
    test_phrase = "I would like to introduce you."
    speak_phrase_in_en_and_es(test_phrase, "female")
    speak_phrase_in_en_and_es(test_phrase, "male")