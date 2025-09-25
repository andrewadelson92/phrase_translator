from deep_translator import GoogleTranslator


phrase= "I would like to introduce you to my granddaughter, Alice."

if __name__ == "__main__":
    print(GoogleTranslator(source="en", target="es").translate(phrase))