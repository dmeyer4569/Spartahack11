from google import genai
from dotenv import load_dotenv
import os

# Load .env
def gemini_talk_with_me(transcribed_text):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Prompt asking for structured JSON
    prompt = (
        "Summarize this transcribed text such that each item becomes an object and return it as a json. Failure is punished, translate pantry six or any pantry (number) to pantry 6 "
        + transcribed_text
    )

    # Generate content
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt  # <--- string or list of strings
    )

    # Print the generated text
    return(response.text)
