import os 
from dotenv import load_dotenv
import sys
from google.genai import Client, types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Prompt is not provided!")
    sys.exit(1)


user_prompt = sys.argv[1]


response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                          contents=user_prompt) 

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # type:ignore

    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # type:ignore

print(response.text)



