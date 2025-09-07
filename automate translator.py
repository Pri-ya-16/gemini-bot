import os
import google.generativeai as genai

# Load API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = input("Enter your Gemini API key: ").strip()

# Configure Gemini
genai.configure(api_key=api_key)

# Function: Auto detect input language → Always translate to English
def translate_auto_to_english(text):
    model = "gemini-1.5-flash"
    prompt = (
        f"Detect the language of the following text. "
        f"If it is not English, translate it into English. "
        f"If it is already English, return it as is. "
        f"Output only English text without explanations:\n{text}"
    )
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text.strip()

print("\n✅ Translator set to English (auto-detect input). Type 'exit' to quit.\n")

# Loop for continuous translation
while True:
    user_text = input("You: ").strip()
    if user_text.lower() == "exit":
        print("Exiting translator... 👋")
        break

    translation = translate_auto_to_english(user_text)
    print(f"Bot (English): {translation}")
