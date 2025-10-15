from deep_translator import GoogleTranslator


def translate_text(text, target_language="te"):
    """
    Translates text into the given target language using Deep Translator.
    Default target language is Telugu ('te').

    Args:
        text (str): Text to translate.
        target_language (str): Target language code (e.g., 'te', 'hi', 'ta', 'ml').

    Returns:
        str: Translated text, or original text if translation fails.
    """
    if not text:
        return ""

    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return text  # Return original text if translation fails


if __name__ == "__main__":
    # Example usage
    text = "Wash your hands regularly to prevent infections."
    print("Original:", text)
    print("Telugu Translation:", translate_text(text, "te"))
    print("Hindi Translation:", translate_text(text, "hi"))
    print("Tamil Translation:", translate_text(text, "ta"))