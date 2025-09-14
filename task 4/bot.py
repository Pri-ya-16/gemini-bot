import json
from googletrans import Translator
from unidecode import unidecode  # pip install unidecode

# Language code ↔ name mapping
LANG_CODES = {
    "tamil": "ta",
    "english": "en",
    "malayalam": "ml",
    "hindi": "hi",
    "telugu": "te"
}

# Load language mappings
with open("languages.json", "r", encoding="utf-8") as f:
    LANG_MAP = json.load(f)["languages"]

translator = Translator()

def find_mapping(from_code):
    """Find mapping by language code from JSON"""
    for mapping in LANG_MAP:
        if LANG_CODES.get(mapping["from"].lower()) == from_code:
            return mapping
    return None

def get_romanized(text, src, dest):
    """Return romanized pronunciation; fallback to unidecode"""
    result = translator.translate(text, src=src, dest=dest)
    if result.pronunciation:
        return result.pronunciation
    else:
        # fallback: convert native script to closest English letters
        return unidecode(result.text)

def transliterate_text(user_text, from_code, to_code):
    """Get From and To in romanized English letters"""
    from_roman = get_romanized(user_text, src=from_code, dest=from_code)
    to_roman = get_romanized(user_text, src=from_code, dest=to_code)
    return from_roman, to_roman

if __name__ == "__main__":
    print("🌍 Multilingual Chat (Romanized English Letters)\n")

    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Detect language automatically
        detected = translator.detect(user_text)
        detected_code = detected.lang

        mapping = find_mapping(detected_code)

        if mapping:
            from_code = LANG_CODES[mapping["from"].lower()]
            to_code = LANG_CODES[mapping["to"].lower()]

            from_side, to_side = transliterate_text(user_text, from_code, to_code)

            print(f"\nFrom language ({mapping['from']}): {from_side}")
            print(f"To language   ({mapping['to']}): {to_side}\n")
        else:
            roman = get_romanized(user_text, src=detected_code, dest=detected_code)
            print(f"\n(No mapping found, showing same language in English letters): {roman}\n")
