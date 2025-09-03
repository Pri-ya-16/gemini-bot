import os
import google.generativeai as genai
from indic_transliteration.sanscript import transliterate, TAMIL, ITRANS

# Function: Convert Tamil script to Romanized style
def tamil_to_roman(text):
    try:
        roman = transliterate(text, TAMIL, ITRANS)
        roman = roman.replace("_", "").capitalize()
        if not roman.endswith("?"):
            roman += "?"
        return roman
    except Exception:
        return text

# Function: Ask Gemini for translation (direct and clean output)
def translate_with_gemini(text, direction="en-ta"):
    model = "gemini-1.5-flash"

    if direction == "en-ta":
        prompt = (
            f"Translate the following English text to Tamil. "
            f"Output ONLY the Tamil text in Tamil script without explanations:\n{text}"
        )
    else:
        prompt = (
            f"Translate the following Tamil text to English. "
            f"Output ONLY the English text without explanations:\n{text}"
        )

    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text.strip()

# Load API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = input("Enter your Gemini API key: ").strip()

# Configure Gemini
genai.configure(api_key=api_key)

# Menu
print("What do you want to translate?")
print("1) English - Tamil")
print("2) Tamil - English")

try:
    choice = int(input("Choose (number): ").strip())
except ValueError:
    print("Invalid input. Please choose 1 or 2.")
    exit()

# Get text input
if choice == 1:
    user_text = input("English text: ").strip()
    translation = translate_with_gemini(user_text, "en-ta")
    roman = tamil_to_roman(translation)
    print(f"Priya: {user_text}")
    print(f"Bot: {roman}")

elif choice == 2:
    user_text = input("Tamil text: ").strip()
    translation = translate_with_gemini(user_text, "ta-en")
    print(f"Priya: {user_text}")
    print(f"Bot: {translation}")

else:
    print("Invalid choice. Please run the script again.")
