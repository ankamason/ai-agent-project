import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

# Verify API key was loaded
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    print("Make sure your .env file exists and contains the API key")
    exit(1)

# Create a Gemini client
client = genai.Client(api_key=api_key)

# Generate content using the Gemini model
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    
    # Print the AI response
    print("AI Response:")
    print(response.text)
    print()
    
    # Print token usage information
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
except Exception as e:
    print(f"Error generating content: {e}")
    print("Check your API key and internet connection")
